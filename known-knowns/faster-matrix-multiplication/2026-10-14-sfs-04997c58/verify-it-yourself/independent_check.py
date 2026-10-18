"""Exact reduced-SLP check, written before opening claim/verify.py.

Definition: C[i,j] = sum_k A[i,k] B[k,j] over Z. A[i,k] has
coordinate i*n2+k, B[k,j] has k*n3+j, C[i,j] has j*n1+i.
The public Scheme.naive source independently fixes these coordinates.
Only Python integer arithmetic is used. Public or author code is not imported.
"""
import hashlib
import json
import pathlib
import sys


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def load(path):
    return json.loads(pathlib.Path(path).read_text(), object_pairs_hook=unique_object)


def check_form(row, available, location):
    require(type(row) is list and len(row) > 0, location + ": empty/nonlist linear form")
    for term in row:
        require(type(term) is dict and set(term) == {"index", "value"}, location + ": extra/missing term fields")
        require(type(term["index"]) is int and 0 <= term["index"] < available, location + ": unavailable/forward reference")
        require(type(term["value"]) is int and term["value"] in (-1, 1), location + ": nonunit or noninteger literal scalar")


def linear_value(row, values):
    # Signs are unary free negations. Combining k terms is exactly k-1 binary sums.
    return sum(term["value"] * values[term["index"]] for term in row)


def canonical(vector):
    first = next(x for x in vector if x)
    return tuple(x if first > 0 else -x for x in vector)


def side(fresh, outputs, base, label):
    require(type(fresh) is list and type(outputs) is list, label + ": arrays required")
    vectors = [tuple(int(i == j) for j in range(base)) for i in range(base)]
    dependencies = []
    cost, aliases, binary_gates, max_intermediate = 0, 0, 0, 1
    for gate, row in enumerate(fresh):
        check_form(row, base + gate, label + " fresh " + str(gate))
        vector = tuple(sum(term["value"] * vectors[term["index"]][j] for term in row) for j in range(base))
        vectors.append(vector)
        dependencies.append([term["index"] for term in row])
        cost += len(row) - 1
        aliases += len(row) == 1
        binary_gates += len(row) == 2
        max_intermediate = max(max_intermediate, max(map(abs, vector)))
    expanded = []
    live = set()
    for index, row in enumerate(outputs):
        check_form(row, len(vectors), label + " output " + str(index))
        expanded.append(tuple(sum(term["value"] * vectors[term["index"]][j] for term in row) for j in range(base)))
        cost += len(row) - 1
        live.update(term["index"] for term in row)
    pending = list(live)
    while pending:
        variable = pending.pop()
        if variable >= base:
            for dependency in dependencies[variable - base]:
                if dependency not in live:
                    live.add(dependency)
                    pending.append(dependency)
    require(all(base + gate in live for gate in range(len(fresh))), label + ": dead fresh gate")
    require(all(x in (-1, 0, 1) for row in expanded for x in row), label + ": nonternary expanded factor")
    return expanded, {"binary_cost": cost, "fresh_count": len(fresh), "fresh_binary_gates": binary_gates,
                      "fresh_aliases": aliases, "output_aliases": sum(len(row) == 1 for row in outputs),
                      "max_abs_intermediate": max_intermediate, "dead_gates": 0}, live


def run_side(fresh, outputs, values):
    values = list(values)
    for row in fresh:
        values.append(linear_value(row, values))
    return [linear_value(row, values) for row in outputs]


def verify(data):
    required = {"n", "m", "z2", "complexity", "u_fresh", "v_fresh", "w_fresh", "u", "v", "w"}
    require(type(data) is dict and required <= set(data) and set(data) <= required | {"research_method"}, "unknown/missing top-level field")
    if "research_method" in data:
        require(type(data["research_method"]) is str, "research_method must be inert text")
    require(type(data["n"]) is list and len(data["n"]) == 3 and all(type(x) is int and x > 0 for x in data["n"]), "invalid dimensions")
    require(type(data["m"]) is int and data["m"] > 0, "invalid multiplication count")
    require(data["z2"] is False, "integer claim must have z2=false")
    require(type(data["complexity"]) is dict and set(data["complexity"]) == {"naive", "reduced"} and
            all(type(x) is int and x >= 0 for x in data["complexity"].values()), "invalid cost metadata")
    n1, n2, n3 = data["n"]
    rank = data["m"]
    base_u, base_v, base_w = n1 * n2, n2 * n3, n1 * n3
    require(type(data["u"]) is list and type(data["v"]) is list and type(data["w"]) is list and
            len(data["u"]) == len(data["v"]) == rank and len(data["w"]) == base_w, "wrong number of factors/outputs")
    u, audit_u, _ = side(data["u_fresh"], data["u"], base_u, "U")
    v, audit_v, _ = side(data["v_fresh"], data["v"], base_v, "V")
    w_outputs, audit_w, live_w = side(data["w_fresh"], data["w"], rank, "W")
    w = [tuple(w_outputs[c][q] for c in range(base_w)) for q in range(rank)]
    require(all(any(row) for row in u + v + w), "zero/inactive multiplication factor")
    require(all(q in live_w for q in range(rank)), "unreferenced product")
    products = {(canonical(u[q]), canonical(v[q])) for q in range(rank)}
    require(len(products) == rank, "duplicate product up to free signs")
    cost = audit_u["binary_cost"] + audit_v["binary_cost"] + audit_w["binary_cost"]
    naive = sum(max(0, sum(x != 0 for x in row) - 1) for row in u + v + w_outputs)
    require(cost == data["complexity"]["reduced"], "reduced cost metadata mismatch")
    require(naive == data["complexity"]["naive"], "naive cost metadata mismatch")
    # Tensor contraction visits every coordinate, including all expected-zero coordinates.
    failures, mod2_failures, witness = 0, 0, None
    for a in range(base_u):
        i, k = divmod(a, n2)
        for b in range(base_v):
            ell, j = divmod(b, n3)
            for c in range(base_w):
                row, column = c % n1, c // n1
                expected = int(k == ell and i == row and j == column)
                got = sum(u[q][a] * v[q][b] * w[q][c] for q in range(rank))
                if got != expected:
                    failures += 1
                    mod2_failures += (got - expected) % 2 != 0
                    if witness is None:
                        witness = {"a": a, "b": b, "c": c, "expected": expected, "actual": got}
    # Separately execute the literal SLP for every pair of input basis vectors.
    basis_failures, first_basis = 0, None
    for a in range(base_u):
        av = [int(t == a) for t in range(base_u)]
        left = run_side(data["u_fresh"], data["u"], av)
        for b in range(base_v):
            bv = [int(t == b) for t in range(base_v)]
            right = run_side(data["v_fresh"], data["v"], bv)
            products_values = [left[q] * right[q] for q in range(rank)]
            got = run_side(data["w_fresh"], data["w"], products_values)
            # Ordinary matrix product computed by direct definition, without tensor expansion.
            expected = [sum(av[i * n2 + k] * bv[k * n3 + j] for k in range(n2))
                        for j in range(n3) for i in range(n1)]
            if got != expected:
                basis_failures += 1
                if first_basis is None:
                    first_basis = {"a": a, "b": b, "expected": expected, "actual": got}
    result = {"dimensions": data["n"], "rank": rank, "active_distinct_products": len(products),
              "reduced_cost": cost, "naive_cost": naive, "side_audit": {"U": audit_u, "V": audit_v, "W": audit_w},
              "tensor_coefficients_checked": base_u * base_v * base_w, "tensor_failures": failures,
              "mod2_tensor_failures": mod2_failures, "basis_pairs_checked": base_u * base_v,
              "basis_failures": basis_failures, "integer_tensor_witness": witness, "basis_witness": first_basis,
              "literal_scalars": sorted({t["value"] for name in ("u", "v", "w", "u_fresh", "v_fresh", "w_fresh") for row in data[name] for t in row}),
              "expanded_factor_scalars": sorted({x for row in u + v + w for x in row}),
              "exact_integer_identity": failures == 0 and basis_failures == 0}
    return result


if __name__ == "__main__":
    path = pathlib.Path(sys.argv[1])
    try:
        result = verify(load(path))
        result["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        print(json.dumps(result, indent=2, sort_keys=True))
        sys.exit(0 if result["exact_integer_identity"] else 1)
    except (Invalid, KeyError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps({"rejected": str(error), "exact_integer_identity": False}, sort_keys=True))
        sys.exit(1)
