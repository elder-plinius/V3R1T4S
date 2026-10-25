"""Independent VNN-COMP counterexample checker, written from the bank success criterion (b)-(c) of
vnncomp-2026-unsolved-instance-counterexample, not from the official validator's code.

  python -I vnncheck_own.py --onnx NET.onnx[.gz] --vnnlib PROP.vnnlib[.gz] --witness W [--margin 1e-6]

Witness formats read: plain (one input value per line), VNN-LIB 1.0 ((X_i v) ... (Y_i v)), VNN-LIB 2.0 text
assignment (optional "sat", "X float32 [dims]" header, values, then outputs). Any outputs in the witness are
ignored: outputs are always replayed. VNN-COMP semantics: the .vnnlib file encodes the violation, so a
counterexample must make EVERY assertion true.

Checks (all must pass for VERDICT: PASS):
  1. every input-only assertion holds STRICTLY (>= read as >, <= as <), in exact rational arithmetic, for the
     values as written AND after rounding to float32;
  2. onnxruntime CPUExecutionProvider, float32: every assertion holds at zero tolerance (exact rationals on the
     float32 outputs), and every output assertion holds with margin >= --margin (atomic margin lhs-rhs in the
     required direction; 'and' = min, 'or' = max);
  3. the same with onnx.reference.ReferenceEvaluator as a second runtime.
Exit status 0 iff PASS.
"""
import argparse, gzip, math, re, sys
from fractions import Fraction

import numpy as np

TOK = re.compile(r"\(|\)|[^\s()\[\]]+(?:\[[^\]]*\])?|\[[^\]]*\]")


def read_text(path):
    data = open(path, "rb").read()
    if path.endswith(".gz"):
        data = gzip.decompress(data)
    return data.decode("utf-8")


def sexprs(text):
    text = "\n".join(line.split(";", 1)[0] for line in text.splitlines())
    stack, top = [[]], None
    for tok in TOK.findall(text):
        if tok == "(":
            stack.append([])
        elif tok == ")":
            top = stack.pop()
            stack[-1].append(top)
        else:
            stack[-1].append(tok)
    if len(stack) != 1:
        raise ValueError("unbalanced parentheses in vnnlib")
    return stack[0]


class Prop:
    """Variables: name -> shape. A reference is (name, flat index)."""

    def __init__(self, text):
        self.inputs, self.outputs, self.asserts, self.version = {}, {}, [], "1.0"
        legacy = []
        for form in sexprs(text):
            head = form[0]
            if head == "vnnlib-version":
                self.version = form[1].strip("<>")
            elif head == "declare-network":
                for d in form[2:]:
                    shape = [int(s) for s in d[3].strip("[]").split(",") if s.strip()]
                    if d[2] != "float32":
                        raise ValueError("unexpected element type %s" % d[2])
                    (self.inputs if d[0] == "declare-input" else self.outputs)[d[1]] = shape
            elif head == "declare-const":
                legacy.append(form[1])
            elif head == "assert":
                self.asserts.append(form[1])
            else:
                raise ValueError("unsupported top-level form %r" % head)
        if legacy:  # VNN-LIB 1.0: X_i, Y_i flattened
            nx = sum(1 for v in legacy if v.startswith("X_"))
            ny = sum(1 for v in legacy if v.startswith("Y_"))
            self.inputs, self.outputs = {"X": [nx]}, {"Y": [ny]}
        self.shapes = dict(self.inputs, **self.outputs)

    def ref(self, atom):
        m = re.fullmatch(r"([A-Za-z_]\w*)\[([\d,\s]+)\]", atom)
        if m:
            name, idx = m.group(1), [int(i) for i in m.group(2).split(",")]
            shape = self.shapes[name]
            if len(idx) != len(shape) or any(not 0 <= i < s for i, s in zip(idx, shape)):
                raise ValueError("index out of range: %s" % atom)
            return name, int(np.ravel_multi_index(idx, shape))
        m = re.fullmatch(r"([XY])_(\d+)", atom)
        if m:
            return m.group(1), int(m.group(2))
        return None

    def variables(self, e):
        if isinstance(e, str):
            r = self.ref(e)
            return {r[0]} if r else set()
        return set().union(*(self.variables(x) for x in e[1:])) if len(e) > 1 else set()


def term(prop, e, env):
    if isinstance(e, str):
        r = prop.ref(e)
        if r:
            return env[r[0]][r[1]]
        return Fraction(e)
    op, args = e[0], [term(prop, a, env) for a in e[1:]]
    if op == "+":
        return sum(args, Fraction(0))
    if op == "-":
        return -args[0] if len(args) == 1 else args[0] - sum(args[1:], Fraction(0))
    if op == "*":
        return math.prod(args)
    raise ValueError("unsupported arithmetic %r" % op)


def margin(prop, e, env):
    """Signed satisfaction margin: > 0 strictly true, == 0 on the boundary, < 0 false."""
    op = e[0]
    if op == "and":
        return min(margin(prop, a, env) for a in e[1:])
    if op == "or":
        return max(margin(prop, a, env) for a in e[1:])
    a, b = term(prop, e[1], env), term(prop, e[2], env)
    if op in (">=", ">"):
        return a - b
    if op in ("<=", "<"):
        return b - a
    raise ValueError("unsupported comparison %r" % op)


def holds(prop, e, env):
    """Truth at zero tolerance, exactly as written (>= allows equality, > does not)."""
    op = e[0]
    if op == "and":
        return all(holds(prop, a, env) for a in e[1:])
    if op == "or":
        return any(holds(prop, a, env) for a in e[1:])
    a, b = term(prop, e[1], env), term(prop, e[2], env)
    return {">=": a >= b, ">": a > b, "<=": a <= b, "<": a < b, "=": a == b}[op]


def read_witness(path, n_in):
    text = read_text(path)
    pairs = re.findall(r"\(\s*X_(\d+)\s+([^\s()]+)\s*\)", text)
    if pairs:
        vals = dict((int(i), v) for i, v in pairs)
        if sorted(vals) != list(range(n_in)):
            raise ValueError("1.0 witness does not assign X_0..X_%d" % (n_in - 1))
        return [vals[i] for i in range(n_in)], "vnnlib-1.0"
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines and lines[0] == "sat":
        lines = lines[1:]
    if lines and re.match(r"^[A-Za-z_]\w*\s+float32\s+\[", lines[0]):
        vals = lines[1:1 + n_in]
        if len(vals) != n_in or not all(re.fullmatch(r"[-+0-9.eE]+", v) for v in vals):
            raise ValueError("2.0 witness has too few input values")
        return vals, "vnnlib-2.0"
    if len(lines) < n_in:
        raise ValueError("plain witness has %d values, need %d" % (len(lines), n_in))
    return lines[:n_in], "plain"


def run_ort(model_bytes, x):
    import onnxruntime as ort
    so = ort.SessionOptions()
    so.intra_op_num_threads = 4
    so.inter_op_num_threads = 1
    s = ort.InferenceSession(model_bytes, so, providers=["CPUExecutionProvider"])
    i = s.get_inputs()[0]
    shp = [d if isinstance(d, int) and d > 0 else 1 for d in i.shape]
    return np.asarray(s.run(None, {i.name: x.reshape(shp)})[0], dtype=np.float32).ravel(), i.shape


def run_reference(model_bytes, x):
    import onnx
    from onnx.reference import ReferenceEvaluator
    m = onnx.load_from_string(model_bytes)
    inits = {t.name for t in m.graph.initializer}
    inp = [v for v in m.graph.input if v.name not in inits][0]
    shp = [d.dim_value if d.dim_value > 0 else 1 for d in inp.type.tensor_type.shape.dim]
    out = ReferenceEvaluator(m).run(None, {inp.name: x.reshape(shp)})[0]
    return np.asarray(out, dtype=np.float32).ravel()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--onnx", required=True)
    ap.add_argument("--vnnlib", required=True)
    ap.add_argument("--witness", required=True)
    ap.add_argument("--margin", type=float, default=1e-6)
    a = ap.parse_args()
    prop = Prop(read_text(a.vnnlib))
    (xname, xshape), = prop.inputs.items()
    (yname, yshape), = prop.outputs.items()
    n_in = math.prod(xshape)
    raw, fmt = read_witness(a.witness, n_in)
    exact = [Fraction(v) for v in raw]
    x32 = np.array([float(v) for v in raw], dtype=np.float32)
    exact32 = [Fraction(float(v)) for v in x32]
    print("vnnlib version %s, input %s %s, output %s %s, %d assertions" % (prop.version, xname, xshape, yname, yshape, len(prop.asserts)))
    print("witness format %s, %d input values, %d not exactly float32" % (fmt, n_in, sum(e != f for e, f in zip(exact, exact32))))
    in_asserts = [e for e in prop.asserts if prop.variables(e) and prop.variables(e) <= {xname}]
    out_asserts = [e for e in prop.asserts if e not in in_asserts]
    ok = True
    for label, xs in (("as written", exact), ("float32-rounded", exact32)):
        env = {xname: xs}
        ms = [margin(prop, e, env) for e in in_asserts]
        n_strict = sum(m > 0 for m in ms)
        n_bound = sum(m == 0 for m in ms)
        worst = min(ms) if ms else None
        strict = n_strict == len(ms)
        ok &= strict
        print("inputs %-15s: %d/%d input assertions strictly true, %d on a bound, %d violated; min slack %s (= %.10g) -> strict: %s"
              % (label, n_strict, len(ms), n_bound, len(ms) - n_strict - n_bound, worst, float(worst), strict))
    model = read_text_bytes(a.onnx)
    y_ort, onnx_shape = run_ort(model, x32)
    y_ref = run_reference(model, x32)
    print("onnx input shape %s; output length ort %d, reference %d; max |ort - reference| = %.3g"
          % (onnx_shape, y_ort.size, y_ref.size, float(np.max(np.abs(y_ort.astype(np.float64) - y_ref)))))
    for rt, y in (("onnxruntime-cpu", y_ort), ("onnx.reference", y_ref)):
        env = {xname: exact32, yname: [Fraction(float(v)) for v in y]}
        all_true = all(holds(prop, e, env) for e in prop.asserts)
        ms = [margin(prop, e, env) for e in out_asserts]
        mmin = min(ms) if ms else Fraction(0)
        good = all_true and float(mmin) >= a.margin
        ok &= good
        print("%-16s: all %d assertions hold at zero tolerance: %s; min output margin %.8f (need >= %g) -> %s"
              % (rt, len(prop.asserts), all_true, float(mmin), a.margin, good))
    top = int(np.argmax(y_ort))
    print("onnxruntime argmax output index %d, value %.8f" % (top, float(y_ort[top])))
    print("VERDICT: %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


def read_text_bytes(path):
    data = open(path, "rb").read()
    return gzip.decompress(data) if path.endswith(".gz") else data


if __name__ == "__main__":
    main()
