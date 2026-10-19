"""Counterexample validation for VNNLIB 2.0 queries.

Scope (checked against the official ``vnncomp2026_benchmarks`` repo, 2026-06):
every 2.0 ``.vnnlib`` query in the benchmark set uses only the features handled
below, so this validator is functionally complete for the 2026 competition:

  * element types: ``float32`` and ``real`` only (``real`` is parsed as
    ``DType.Unknown`` and treated as float64);
  * a single ``declare-network``, OR two networks related by ``equal-to``
    (monotonic_acasxu_2026, same ONNX) or ``isomorphic-to`` (isomorphic_acasxu_2026,
    two distinct ONNX files -- handled because ``isomorphic-to`` leaves
    ``Network.equal_to`` empty, so g is run as an independent network);
  * linear AND polynomial assertions (``*`` is used by
    adaptive_cruise_control_non_linear_2026 and linearizenn_2024);
  * ``and`` / ``or`` / ``==`` / ``!=`` / unary ``-`` / multi-dim indexing.

Query parsing AND type/scope checking are delegated to the official VNNLIB-Python
package (``vnnlib==1.0.2``): ``parse_query_string`` runs the reference type checker
and raises ``vnnlib.VNNLibException`` on any ill-typed/ill-scoped query, which we map
to ``UNSUPPORTED`` below. The hand-rolled type logic that remains here
(``_assignment_type_matches``, ``_validate_element_type``) is deliberately NOT a
re-implementation of that checker -- it validates two things the official checker
does not see: the solver's textual counterexample assignment, and the declared
element types vs. the actual ONNX tensor types at run time.

TODO (not required by any 2026 benchmark; each currently returns UNSUPPORTED so a
tool is never penalized for our gap -- see the raises below):
  * ``declare-hidden`` variables (no 2026 benchmark uses them);
  * element types beyond float32/real (the package's DType enum also defines
    BF16, the int/uint family, bool, the float8 variants, complex, string);
  * actually *enforcing* the ``equal-to`` / ``isomorphic-to`` structural relation
    (we currently ignore it, which is sound for counterexample checking but would
    be needed to validate the relation itself).
"""

import functools
import gzip
import math
import re

import numpy as np
import onnxruntime as ort
import vnnlib

from benchmark_instances import parse_network_field, resolve_benchmark_path
from cex_checks import CPU_PROVIDER


_ASSIGNMENT_HEADER = re.compile(r"^(\S+)\s+(\S+)\s+\[([0-9,\s]*)\]$")

_NUMPY_DTYPES = {
    "F16": np.float16,
    "F32": np.float32,
    "F64": np.float64,
    "I8": np.int8,
    "I16": np.int16,
    "I32": np.int32,
    "I64": np.int64,
    "U8": np.uint8,
    "U16": np.uint16,
    "U32": np.uint32,
    "U64": np.uint64,
    "Bool": np.bool_,
    "Real": np.float64,
    # Retain compatibility with queries parsed by vnnlib 1.0.1.
    "Unknown": np.float64,
}

_VNNLIB_TYPE_NAMES = {
    "F16": "float16",
    "F32": "float32",
    "F64": "float64",
    "I8": "int8",
    "I16": "int16",
    "I32": "int32",
    "I64": "int64",
    "U8": "uint8",
    "U16": "uint16",
    "U32": "uint32",
    "U64": "uint64",
    "Bool": "bool",
    "Real": "real",
    "Unknown": "real",
}

_FLOAT_DTYPE_KEYS = {"F16", "F32", "F64", "Real", "Unknown"}

_ONNX_RUNTIME_DTYPES = {
    "tensor(float16)": np.float16,
    "tensor(float)": np.float32,
    "tensor(double)": np.float64,
    "tensor(int8)": np.int8,
    "tensor(int16)": np.int16,
    "tensor(int32)": np.int32,
    "tensor(int64)": np.int64,
    "tensor(uint8)": np.uint8,
    "tensor(uint16)": np.uint16,
    "tensor(uint32)": np.uint32,
    "tensor(uint64)": np.uint64,
    "tensor(bool)": np.bool_,
}

_VNNLIB_TO_ONNX_TYPES = {
    "F16": "tensor(float16)",
    "F32": "tensor(float)",
    "F64": "tensor(double)",
    "I8": "tensor(int8)",
    "I16": "tensor(int16)",
    "I32": "tensor(int32)",
    "I64": "tensor(int64)",
    "U8": "tensor(uint8)",
    "U16": "tensor(uint16)",
    "U32": "tensor(uint32)",
    "U64": "tensor(uint64)",
    "Bool": "tensor(bool)",
}

_ORT_ERRORS = tuple(
    getattr(ort.capi.onnxruntime_pybind11_state, name)
    for name in (
        "EPFail",
        "EngineError",
        "Fail",
        "InvalidArgument",
        "InvalidGraph",
        "InvalidProtobuf",
        "ModelLoadCanceled",
        "ModelLoaded",
        "ModelRequiresCompilation",
        "NoModel",
        "NoSuchFile",
        "NotFound",
        "NotImplemented",
        "RuntimeException",
    )
    if hasattr(ort.capi.onnxruntime_pybind11_state, name)
)


class UnsupportedVNNLIB2Error(Exception):
    pass


class InvalidAssignmentError(Exception):
    pass


def _read_text(path):
    if str(path).endswith(".gz"):
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            return stream.read()
    with open(path, "r", encoding="utf-8") as stream:
        return stream.read()


def _definitions(query):
    return tuple(
        definition
        for network in query.networks
        for definition in (*network.inputs, *network.hidden, *network.outputs)
    )


def _dtype_name(dtype):
    return dtype.name


def _parse_value(value, dtype):
    if dtype == np.bool_:
        normalized = value.lower()
        if normalized not in ("true", "false", "0", "1"):
            raise ValueError(f"invalid boolean value {value!r}")
        return normalized in ("true", "1")
    if np.issubdtype(dtype, np.integer):
        return int(value)
    return float(value)


def _assignment_type_matches(dtype_key, type_name):
    expected_type_name = _VNNLIB_TYPE_NAMES[dtype_key]
    normalized_type_name = type_name.lower()
    if normalized_type_name == expected_type_name.lower():
        return True
    return dtype_key in _FLOAT_DTYPE_KEYS and normalized_type_name == "real"


def parse_text_assignment(content, query):
    """Parse the mandatory textual assignment format from VNNLIB 2.0 section 5.3."""

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if lines and lines[0] == "sat":
        lines.pop(0)

    assignment = {}
    position = 0

    for definition in _definitions(query):
        if position >= len(lines):
            raise InvalidAssignmentError(f"missing assignment for variable {definition.name}")

        match = _ASSIGNMENT_HEADER.fullmatch(lines[position])
        if not match:
            raise InvalidAssignmentError(f"invalid assignment header: {lines[position]!r}")
        position += 1

        name, type_name, dimensions = match.groups()
        if name != definition.name:
            raise InvalidAssignmentError(
                f"expected variable {definition.name}, found {name}"
            )

        shape = [] if not dimensions.strip() else [
            int(value.strip()) for value in dimensions.split(",")
        ]
        if shape != list(definition.shape):
            raise InvalidAssignmentError(
                f"variable {name} has shape {shape}, expected {list(definition.shape)}"
            )

        dtype_key = _dtype_name(definition.dtype)
        if dtype_key not in _NUMPY_DTYPES:
            # TODO: extend _NUMPY_DTYPES if a future benchmark uses a type beyond
            # float32/real (the package DType enum also defines BF16, the float8
            # variants, complex, string, etc.). 2026 uses only F32 and Unknown(real),
            # so anything else is reported UNSUPPORTED rather than mis-parsed.
            raise UnsupportedVNNLIB2Error(
                f"unsupported assignment type {definition.dtype} for {name}"
            )
        expected_type_name = _VNNLIB_TYPE_NAMES[dtype_key]
        if not _assignment_type_matches(dtype_key, type_name):
            raise InvalidAssignmentError(
                f"variable {name} has type {type_name}, expected {expected_type_name}"
            )

        value_count = math.prod(shape)
        if position + value_count > len(lines):
            raise InvalidAssignmentError(f"not enough values for variable {name}")

        dtype = _NUMPY_DTYPES[dtype_key]
        try:
            values = [_parse_value(value, dtype) for value in lines[position:position + value_count]]
            assignment[name] = np.asarray(values, dtype=dtype).reshape(shape)
        except (OverflowError, TypeError, ValueError) as error:
            raise InvalidAssignmentError(f"invalid value for variable {name}: {error}") from error
        position += value_count

    if position != len(lines):
        raise InvalidAssignmentError(f"unexpected content after assignments: {lines[position]!r}")

    return assignment


def _network_model_paths(query, network_field, benchmark_dir):
    supplied = parse_network_field(network_field)
    explicit = {}

    if supplied[0][0] is None:
        if len(supplied) != 1:
            raise UnsupportedVNNLIB2Error(
                "unnamed ONNX model mappings cannot be combined with other mappings"
            )
        implemented = [
            network for network in query.networks
            if not network.equal_to
        ]
        if len(implemented) != 1:
            raise UnsupportedVNNLIB2Error(
                "a single ONNX path can only be used with one implemented network"
            )
        explicit[implemented[0].name] = resolve_benchmark_path(
            benchmark_dir, supplied[0][1], "onnx"
        )
    else:
        declared = {network.name: network for network in query.networks}
        for name, path in supplied:
            if name in explicit:
                raise UnsupportedVNNLIB2Error(
                    f"multiple ONNX models were provided for network {name}"
                )
            if name not in declared:
                raise UnsupportedVNNLIB2Error(
                    f"ONNX model was provided for undeclared network {name}"
                )
            explicit[name] = resolve_benchmark_path(benchmark_dir, path, "onnx")

    paths = {}
    for network in query.networks:
        if network.name in explicit:
            if network.equal_to:
                if network.equal_to not in paths:
                    raise UnsupportedVNNLIB2Error(
                        f"equal-to network {network.name} references unavailable "
                        f"network {network.equal_to}"
                    )
                expected_path = paths[network.equal_to]
                if explicit[network.name].resolve() != expected_path.resolve():
                    raise UnsupportedVNNLIB2Error(
                        f"ONNX model provided for equal-to network {network.name} "
                        f"does not match network {network.equal_to}"
                    )
                paths[network.name] = expected_path
            else:
                paths[network.name] = explicit[network.name]
        elif network.equal_to and network.equal_to in paths:
            paths[network.name] = paths[network.equal_to]
        else:
            raise UnsupportedVNNLIB2Error(
                f"no ONNX model was provided for network {network.name}"
            )

    return paths


# Reuse the session across counterexamples that share a network; bounded to a
# couple of networks so memory stays flat (the arena is off, so an evicted
# session frees its native allocations).
@functools.lru_cache(maxsize=2)
def _session(model_path):
    # Disable the CPU memory arena so native allocations are freed with the
    # session; otherwise per-CE sessions accumulate memory until OOM.
    opts = ort.SessionOptions()
    opts.enable_cpu_mem_arena = False
    if str(model_path).endswith(".gz"):
        with gzip.open(model_path, "rb") as stream:
            return ort.InferenceSession(stream.read(), opts, providers=[CPU_PROVIDER])
    return ort.InferenceSession(str(model_path), opts, providers=[CPU_PROVIDER])


def _reshape_for_onnx(value, onnx_shape, variable_name):
    if len(value.shape) == len(onnx_shape) and all(
        not isinstance(onnx_dimension, int)
        or onnx_dimension <= 0
        or value_dimension == onnx_dimension
        for value_dimension, onnx_dimension in zip(value.shape, onnx_shape)
    ):
        return value

    if all(isinstance(dimension, int) and dimension > 0 for dimension in onnx_shape):
        if value.size == math.prod(onnx_shape):
            return value.reshape(onnx_shape)

    raise UnsupportedVNNLIB2Error(
        f"cannot reshape VNNLIB variable {variable_name} from {value.shape} "
        f"to ONNX shape {onnx_shape}"
    )


def _match_onnx_values(definitions, onnx_values, network_name, value_kind):
    if len(onnx_values) != len(definitions):
        raise UnsupportedVNNLIB2Error(
            f"network {network_name} declares {len(definitions)} {value_kind}s, "
            f"but ONNX has {len(onnx_values)}"
        )

    by_name = {value.name: value for value in onnx_values}
    matches = []
    for definition, positional_value in zip(definitions, onnx_values):
        if definition.onnx_name:
            if definition.onnx_name not in by_name:
                raise UnsupportedVNNLIB2Error(
                    f"ONNX {value_kind} {definition.onnx_name} declared for "
                    f"{definition.name} was not found"
                )
            matches.append((definition, by_name[definition.onnx_name]))
        else:
            matches.append((definition, positional_value))
    return matches


def _validate_element_type(definition, onnx_value, network_name):
    dtype_name = _dtype_name(definition.dtype)
    if dtype_name in ("Real", "Unknown"):
        return

    expected = _VNNLIB_TO_ONNX_TYPES.get(dtype_name)
    if expected is None:
        raise UnsupportedVNNLIB2Error(
            f"unsupported VNNLIB element type {definition.dtype} for {definition.name}"
        )
    if onnx_value.type != expected:
        raise UnsupportedVNNLIB2Error(
            f"network {network_name} declares {definition.name} as "
            f"{_VNNLIB_TYPE_NAMES[dtype_name]}, but ONNX {onnx_value.name} has "
            f"type {onnx_value.type}"
        )


def _run_networks(query, model_paths, assignment):
    computed_outputs = {}
    effective_inputs = {}

    for network in query.networks:
        if network.hidden:
            # TODO: hidden-node support. No 2026 benchmark declares hidden variables,
            # so this returns UNSUPPORTED (non-penalizing) rather than being implemented.
            # Implementing it requires feeding intermediate tensors / reading them back
            # out of the ONNX graph, which onnxruntime does not expose directly.
            raise UnsupportedVNNLIB2Error(
                f"network {network.name} declares hidden variables, which are not supported yet"
            )

        session = _session(model_paths[network.name])
        session_inputs = session.get_inputs()
        session_outputs = session.get_outputs()
        input_matches = _match_onnx_values(
            network.inputs, session_inputs, network.name, "input"
        )
        output_matches = _match_onnx_values(
            network.outputs, session_outputs, network.name, "output"
        )

        feeds = {}
        for definition, onnx_input in input_matches:
            onnx_name = onnx_input.name
            _validate_element_type(definition, onnx_input, network.name)
            if onnx_input.type not in _ONNX_RUNTIME_DTYPES:
                raise UnsupportedVNNLIB2Error(
                    f"unsupported ONNX input type {onnx_input.type} for {onnx_name}"
                )
            value = assignment[definition.name].astype(
                _ONNX_RUNTIME_DTYPES[onnx_input.type], copy=False
            )
            effective_inputs[definition.name] = value
            feeds[onnx_name] = _reshape_for_onnx(
                value, onnx_input.shape, definition.name
            )

        for definition, onnx_output in output_matches:
            _validate_element_type(definition, onnx_output, network.name)

        output_names = [onnx_output.name for _, onnx_output in output_matches]
        outputs = session.run(output_names, feeds)
        for (definition, onnx_output), output in zip(output_matches, outputs):
            output = np.asarray(output)
            if output.shape != tuple(definition.shape):
                if output.size != math.prod(definition.shape):
                    raise UnsupportedVNNLIB2Error(
                        f"cannot reshape ONNX output for {definition.name} from "
                        f"{output.shape} to {definition.shape}"
                    )
                output = output.reshape(definition.shape)
            computed_outputs[definition.name] = output

    return computed_outputs, effective_inputs


def _eval_arithmetic(expression, assignment):
    node_type = type(expression).__name__

    if node_type == "Var":
        value = assignment[expression.name]
        return value[tuple(expression.indices)]
    if node_type in ("Float", "Int", "IntExpr"):
        return expression.value
    if node_type == "Literal":
        return float(expression.lexeme)
    if node_type == "Negate":
        return -_eval_arithmetic(expression.expr, assignment)
    if node_type == "Plus":
        return sum(_eval_arithmetic(arg, assignment) for arg in expression.args)
    if node_type == "Minus":
        value = _eval_arithmetic(expression.head, assignment)
        return value - sum(_eval_arithmetic(arg, assignment) for arg in expression.rest)
    if node_type == "Multiply":
        return math.prod(_eval_arithmetic(arg, assignment) for arg in expression.args)

    raise UnsupportedVNNLIB2Error(f"unsupported arithmetic expression {node_type}")


def _eval_boolean(expression, assignment, tolerance):
    node_type = type(expression).__name__

    if node_type == "And":
        return all(_eval_boolean(arg, assignment, tolerance) for arg in expression.args)
    if node_type == "Or":
        return any(_eval_boolean(arg, assignment, tolerance) for arg in expression.args)

    lhs = _eval_arithmetic(expression.lhs, assignment)
    rhs = _eval_arithmetic(expression.rhs, assignment)
    if node_type == "GreaterThan":
        return lhs > rhs - tolerance
    if node_type == "LessThan":
        return lhs < rhs + tolerance
    if node_type == "GreaterEqual":
        return lhs >= rhs - tolerance
    if node_type == "LessEqual":
        return lhs <= rhs + tolerance
    if node_type == "Equal":
        return abs(lhs - rhs) <= tolerance
    if node_type == "NotEqual":
        return abs(lhs - rhs) > tolerance

    raise UnsupportedVNNLIB2Error(f"unsupported boolean expression {node_type}")


def _expression_variables(expression):
    node_type = type(expression).__name__
    if node_type == "Var":
        return {expression.name}

    variables = set()
    for attr in ("expr", "lhs", "rhs", "head"):
        if hasattr(expression, attr):
            variables.update(_expression_variables(getattr(expression, attr)))
    for attr in ("args", "rest"):
        if hasattr(expression, attr):
            for child in getattr(expression, attr):
                variables.update(_expression_variables(child))
    return variables


def _input_names(query):
    return {
        definition.name
        for network in query.networks
        for definition in network.inputs
    }


def _assertions_hold(query, assignment, input_tolerance, output_tolerance=0.0):
    inputs = _input_names(query)
    for assertion in query.assertions:
        variables = _expression_variables(assertion.expr)
        tolerance = input_tolerance if variables and variables <= inputs else output_tolerance
        if not _eval_boolean(assertion.expr, assignment, tolerance):
            return False
    return True


def _assertions_rationale(query, assignment, input_tolerance, output_tolerance=0.0):
    inputs = _input_names(query)
    failures = []
    for index, assertion in enumerate(query.assertions):
        variables = _expression_variables(assertion.expr)
        tolerance = input_tolerance if variables and variables <= inputs else output_tolerance
        if not _eval_boolean(assertion.expr, assignment, tolerance):
            failures.append(
                f"assertion {index} failed with tolerance {tolerance} "
                f"({'input' if variables and variables <= inputs else 'output/mixed'})"
            )
    if failures:
        return "; ".join(failures)
    return f"all assertions hold with input_tolerance={input_tolerance}, output_tolerance={output_tolerance}"


def _legacy_assertions_hold(query, assignment, tolerance):
    return all(
        _eval_boolean(assertion.expr, assignment, tolerance)
        for assertion in query.assertions
    )


def _outputs_match(expected, computed, abs_tol, rel_tol):
    messages = []
    matches = True
    for name, actual in computed.items():
        witness = expected[name]
        if witness.shape != actual.shape:
            return False, f"output {name} has shape {witness.shape}, ONNX produced {actual.shape}"
        if not np.allclose(witness, actual, atol=abs_tol, rtol=rel_tol):
            matches = False
        difference = float(np.max(np.abs(witness - actual))) if witness.size else 0.0
        messages.append(f"{name} maximum absolute execution difference: {difference}")
    return matches, "; ".join(messages)


def validate_vnnlib2_counterexample(
    benchmark_dir,
    network_field,
    property_field,
    ce_path,
    abs_tol,
    rel_tol,
    result_type,
    ignore_ce_outputs=False,
):
    """Validate one VNNLIB 2.0 textual assignment."""

    try:
        assignment_content = _read_text(ce_path)
    except FileNotFoundError as error:
        return result_type.NO_CE, str(error)

    try:
        property_path = resolve_benchmark_path(benchmark_dir, property_field, "vnnlib")
        query = vnnlib.parse_query_string(_read_text(property_path))
        assignment = parse_text_assignment(assignment_content, query)
        model_paths = _network_model_paths(query, network_field, benchmark_dir)
        computed, effective_inputs = _run_networks(query, model_paths, assignment)
    except InvalidAssignmentError as error:
        return result_type.MALFORMED_CE, str(error)
    except (
        FileNotFoundError,
        UnsupportedVNNLIB2Error,
        vnnlib.VNNLibException,
        *_ORT_ERRORS,
    ) as error:
        return result_type.UNSUPPORTED, str(error)

    evaluation_assignment = dict(assignment)
    evaluation_assignment.update(effective_inputs)
    evaluation_assignment.update(computed)
    execution_message = "counterexample outputs ignored; using ONNX CPU replay outputs"

    if _assertions_hold(query, evaluation_assignment, 0.0, 0.0):
        return (
            result_type.CORRECT,
            f"{execution_message}; "
            + _assertions_rationale(query, evaluation_assignment, 0.0, 0.0),
        )

    if _assertions_hold(query, evaluation_assignment, abs_tol, 0.0):
        return (
            result_type.CORRECT_UP_TO_TOLERANCE,
            f"{execution_message}; input constraints require at most {abs_tol} absolute tolerance; "
            + _assertions_rationale(query, evaluation_assignment, abs_tol, 0.0),
        )

    return (
        result_type.SPEC_NOT_VIOLATED,
        f"{execution_message}; "
        + _assertions_rationale(query, evaluation_assignment, abs_tol, 0.0),
    )
