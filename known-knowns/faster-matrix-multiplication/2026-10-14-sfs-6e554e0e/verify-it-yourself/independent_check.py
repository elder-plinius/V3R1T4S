#!/usr/bin/env python3
"""Independent exact checker; Python standard library only.

Written before inspecting or executing claim/verify.py. Sparse rows are literal
ordered signed sums. Every multi-term row is compiled to binary left folds.
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def pairs_no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs_no_duplicates,
                      parse_constant=lambda s: (_ for _ in ()).throw(Invalid(s)))


def row_check(row, limit, label):
    require(type(row) is list and len(row) > 0, f"{label}: empty/non-list form")
    seen = set()
    for entry in row:
        require(type(entry) is dict and set(entry) == {"index", "value"},
                f"{label}: term schema")
        index, sign = entry["index"], entry["value"]
        require(type(index) is int and 0 <= index < limit,
                f"{label}: reference {index!r} outside earlier pool [0,{limit})")
        require(type(sign) is int and sign in (-1, 1),
                f"{label}: forbidden scalar {sign!r}; only integer +/-1 allowed")
        require(index not in seen, f"{label}: duplicate sparse index {index}")
        seen.add(index)


def combine(row, pool):
    out = [0] * len(pool[0])
    for entry in row:
        for index, coefficient in enumerate(pool[entry["index"]]):
            out[index] += entry["value"] * coefficient
    return out


def phase(data, side, size, output_count):
    fresh, final = data[side + "_fresh"], data[side]
    require(type(fresh) is list and type(final) is list, f"{side}: arrays required")
    require(len(final) == output_count, f"{side}: wrong final form count")
    pool = [[int(i == j) for j in range(size)] for i in range(size)]
    names = [f"{side}{i}" for i in range(size)]
    gates, assignments, operations = [], [], []
    fresh_vectors = []
    for group, rows in (("fresh", fresh), ("final", final)):
        vectors = []
        for position, row in enumerate(rows):
            label = f"{side}_{group}[{position}]"
            row_check(row, len(pool), label)
            target = (f"{side}{size + position}" if group == "fresh"
                      else f"{side}_out{position}")
            first = row[0]
            accumulator = [first["value"] * c for c in pool[first["index"]]]
            accumulator_name = ("-" if first["value"] == -1 else "") + names[first["index"]]
            for gate_position, entry in enumerate(row[1:], 1):
                next_vector = [a + entry["value"] * b
                               for a, b in zip(accumulator, pool[entry["index"]])]
                gate_name = f"{target}_sum{gate_position}"
                gates.append({"id": gate_name, "form": label,
                              "lhs": accumulator_name,
                              "operator": "+" if entry["value"] == 1 else "-",
                              "rhs": names[entry["index"]],
                              "expanded": next_vector})
                operations.append({"kind": "binary", **gates[-1]})
                accumulator, accumulator_name = next_vector, gate_name
            vectors.append(accumulator)
            assignments.append({"id": target, "source": accumulator_name,
                                "free": True, "expanded": accumulator})
            operations.append({"kind": "alias", **assignments[-1]})
            if group == "fresh":
                pool.append(accumulator)
                names.append(target)
        if group == "fresh":
            fresh_vectors = vectors
        else:
            final_vectors = vectors

    # Backward graph traversal starts only at consumed final forms.
    live = set(entry["index"] for row in final for entry in row)
    stack = list(live)
    while stack:
        index = stack.pop()
        if index >= size:
            for entry in fresh[index - size]:
                if entry["index"] not in live:
                    live.add(entry["index"])
                    stack.append(entry["index"])
    dead = [i for i in range(size, size + len(fresh)) if i not in live]
    require(not dead, f"{side}: dead fresh variables {dead}")
    require(all(any(vector) for vector in final_vectors), f"{side}: zero final form")
    require(all(c in (-1, 0, 1) for vector in final_vectors for c in vector),
            f"{side}: expanded final coefficient outside ternary domain")
    # Report fresh coefficient domains too; scalar restrictions concern literal gates.
    cost_fresh = sum(len(row) - 1 for row in fresh)
    cost_final = sum(len(row) - 1 for row in final)
    stats = {"base_inputs": size, "fresh_count": len(fresh),
             "final_count": len(final), "fresh_additions": cost_fresh,
             "final_additions": cost_final, "additions": cost_fresh + cost_final,
             "dead_fresh": dead, "live_base_count": len(live.intersection(range(size))),
             "free_singleton_positive": sum(len(r) == 1 and r[0]["value"] == 1 for r in final),
             "free_singleton_negative": sum(len(r) == 1 and r[0]["value"] == -1 for r in final),
             "fresh_expanded_values": sorted({c for v in fresh_vectors for c in v}),
             "final_expanded_values": sorted({c for v in final_vectors for c in v})}
    require(len(gates) == stats["additions"], f"{side}: compilation count disagreement")
    return {"final": final_vectors, "fresh": fresh_vectors, "gates": gates, "operations": operations,
            "assignments": assignments, "stats": stats}


def direct_phase(data, side, base_values, symbolic, basis_weights, gate_checks):
    """Execute literal signed scalar additions, auditing each binary prefix."""
    pool = list(base_values)
    answers = []
    gate_cursor = 0
    for group in ("fresh", "final"):
        for position, row in enumerate(data[side + "_fresh"] if group == "fresh" else data[side]):
            accumulator = row[0]["value"] * pool[row[0]["index"]]
            for term in row[1:]:
                if term["value"] == 1:
                    accumulator += pool[term["index"]]
                else:
                    accumulator -= pool[term["index"]]
                expected = sum(c * b for c, b in zip(symbolic["gates"][gate_cursor]["expanded"], basis_weights))
                require(accumulator == expected, f"{side}: binary gate execution disagreement")
                gate_checks[0] += 1
                gate_cursor += 1
            expected_vector = symbolic[group][position]
            require(accumulator == sum(c * b for c, b in zip(expected_vector, basis_weights)),
                    f"{side}_{group}[{position}]: alias/form execution disagreement")
            if group == "fresh":
                pool.append(accumulator)
            else:
                answers.append(accumulator)
    return answers


def check(data, claimed_count=None):
    required = {"n", "m", "z2", "complexity", "u", "v", "w", "u_fresh", "v_fresh", "w_fresh"}
    require(type(data) is dict and required <= set(data), "missing required top-level fields")
    require(set(data) <= required | {"research_method"}, "unknown executable/top-level fields")
    if "research_method" in data:
        require(type(data["research_method"]) is str, "research_method must be inert text")
    require(type(data["n"]) is list and len(data["n"]) == 3
            and all(type(x) is int for x in data["n"]), "integer dimensions required")
    require(data["n"] == [2, 5, 6], "wrong format; expected (2,5,6)")
    require(type(data["m"]) is int and data["m"] == 47, "wrong multiplication count")
    require(data["z2"] is False, "integer ring required; z2 must be false")
    require(type(data["complexity"]) is dict and set(data["complexity"]) == {"naive", "reduced"},
            "complexity schema")
    require(all(type(x) is int and x >= 0 for x in data["complexity"].values()), "integer counts required")
    nr, inner, nc = data["n"]
    sizes = (nr * inner, inner * nc, data["m"])
    counts = (data["m"], data["m"], nr * nc)
    phases = {s: phase(data, s, size, count) for s, size, count in zip("uvw", sizes, counts)}
    cost = sum(p["stats"]["additions"] for p in phases.values())
    require(cost == data["complexity"]["reduced"], f"count mismatch: computed {cost}, metadata {data['complexity']['reduced']}")
    if claimed_count is not None:
        require(cost == claimed_count, f"claim count mismatch: computed {cost}, expected {claimed_count}")
    naive = sum(max(0, sum(c != 0 for c in vector) - 1)
                for p in phases.values() for vector in p["final"])
    require(naive == data["complexity"]["naive"], f"naive count mismatch: computed {naive}")
    U, V, W = (phases[s]["final"] for s in "uvw")
    active = [k for k in range(47) if any(U[k]) and any(V[k]) and any(W[o][k] for o in range(12))]
    require(active == list(range(47)), f"inactive products: {sorted(set(range(47)) - set(active))}")
    rank_one_terms = [(tuple(U[k]), tuple(V[k]), tuple(W[o][k] for o in range(12))) for k in range(47)]
    require(len(set(rank_one_terms)) == 47, "duplicate rank-one terms")
    tensor = [[[sum(W[o][k] * U[k][a] * V[k][b] for k in range(47))
                for b in range(30)] for a in range(10)] for o in range(12)]
    bad = []
    for o in range(12):
        out_col, out_row = divmod(o, nr)
        for a in range(10):
            ar, ak = divmod(a, inner)
            for b in range(30):
                bk, bc = divmod(b, nc)
                expected = int(ar == out_row and bc == out_col and ak == bk)
                if tensor[o][a][b] != expected:
                    bad.append((o, a, b, tensor[o][a][b], expected))
    require(not bad, f"integer tensor mismatch: {len(bad)} coefficients; first {bad[:5]}")

    # An independent direct interpreter runs all 300 basis pairs and every gate.
    gate_checks = [0]
    direct_tensor = [[[0] * 30 for _ in range(10)] for _ in range(12)]
    for a in range(10):
        A = [int(i == a) for i in range(10)]
        for b in range(30):
            B = [int(i == b) for i in range(30)]
            left = direct_phase(data, "u", A, phases["u"], A, gate_checks)
            right = direct_phase(data, "v", B, phases["v"], B, gate_checks)
            products = [x * y for x, y in zip(left, right)]
            require(all(products[k] == U[k][a] * V[k][b] for k in range(47)), "product execution disagreement")
            outputs = direct_phase(data, "w", products, phases["w"], products, gate_checks)
            for o, value in enumerate(outputs):
                direct_tensor[o][a][b] = value
    require(direct_tensor == tensor, "direct execution and symbolic tensor disagree")
    require(gate_checks[0] == cost * 300, "not every binary gate audited on every basis pair")
    summary = {"format": data["n"], "ring": "Z", "active_products": len(active),
               "rank_one_terms_distinct": 47, "coefficient_count": 3600,
               "expected_one_coefficients": 60, "expected_zero_coefficients": 3540,
               "mismatches": 0, "additions": cost, "naive_additions": naive,
               "binary_gates": cost, "basis_pairs": 300,
               "basis_binary_gate_checks": gate_checks[0], "basis_product_checks": 47 * 300,
               "basis_output_checks": 3600,
               "phases": {s: p["stats"] for s, p in phases.items()},
               "expanded_tensor_value_histogram": dict(Counter(c for x in tensor for y in x for c in y)),
               "ordering": "A[i,k]=i*5+k; B[k,j]=k*6+j; output C[i,j]=j*2+i",
               "pass": True}
    return summary, {"expanded": {s: {g: phases[s][g] for g in ("fresh", "final")} for s in "uvw"},
                     "phases": {s: {g: phases[s][g] for g in ("gates", "assignments", "operations")} for s in "uvw"},
                     "tensor_output_A_B": tensor, "direct_tensor_output_A_B": direct_tensor}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scheme")
    parser.add_argument("--expect-additions", type=int)
    parser.add_argument("--artifacts", type=Path)
    args = parser.parse_args()
    try:
        result, audit = check(load(args.scheme), args.expect_additions)
    except (Invalid, ValueError, TypeError, KeyError, IndexError) as error:
        print(json.dumps({"pass": False, "error": str(error)}, indent=2))
        return 1
    result["scheme_sha256"] = hashlib.sha256(Path(args.scheme).read_bytes()).hexdigest()
    if args.artifacts:
        args.artifacts.mkdir(parents=True, exist_ok=True)
        (args.artifacts / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
        (args.artifacts / "audit.json").write_text(json.dumps(audit, indent=2) + "\n")
        lines = []
        for s in "uvw":
            if s == "w":
                lines.extend(f"w{k} = u_out{k} * v_out{k}" for k in range(47))
            for op in audit["phases"][s]["operations"]:
                if op["kind"] == "binary":
                    lines.append(f"{op['id']} = {op['lhs']} {op['operator']} {op['rhs']}")
                else:
                    lines.append(f"{op['id']} = {op['source']}  # free alias/sign")
        (args.artifacts / "straight_line_program.txt").write_text("\n".join(lines) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
