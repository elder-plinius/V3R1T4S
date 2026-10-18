#!/usr/bin/env python3
"""Standalone integer SLP audit, independently written before claim/verify.py.

Definition: C[i,j] = sum_k A[i,k]*B[k,j]. A index i*q+k,
B index k*p+j, C index j*n+i. No imports, saved source files, or network
are needed beyond the Python standard library and the supplied JSON object.

Sparse terms are literal signed references to earlier values. Each fresh row
is one binary +/- gate; terminal sums are left-folded and charged len(row)-1.
Intermediate integer coefficients may exceed one. Expanded product/output
factors must be ternary. All fresh gates and products must be live.
"""
import argparse
import hashlib
import json
import sys

EXPECTED_SHA256 = "61917376617f1db0a75f5e9f5efd8bbd748713896418760b469126ea042ae5ee"
REQUIRED = {"n", "m", "z2", "complexity", "u_fresh", "u", "v_fresh", "v", "w_fresh", "w"}


class CheckError(Exception):
    def __init__(self, stage, message):
        self.stage = stage
        super().__init__(message)


def require(condition, stage, message):
    if not condition:
        raise CheckError(stage, message)


def strict_integer(value):
    return type(value) is int


def reject_duplicate_keys(pairs):
    answer = {}
    for key, value in pairs:
        require(key not in answer, "json", "duplicate JSON key: " + key)
        answer[key] = value
    return answer


def schema(data):
    require(type(data) is dict, "schema", "object must be a JSON dictionary")
    require(REQUIRED <= data.keys() <= REQUIRED | {"research_method"}, "schema", "missing or unknown top-level fields")
    if "research_method" in data:
        require(type(data["research_method"]) is str, "schema", "research_method must be inert text")
    dims = data["n"]
    require(type(dims) is list and len(dims) == 3 and all(strict_integer(x) and 0 < x <= 8 for x in dims), "schema", "n must contain three positive integers at most 8")
    rank = data["m"]
    require(strict_integer(rank) and rank > 0, "schema", "m must be a positive integer")
    require(data["z2"] is False, "schema", "this checker requires exact integer arithmetic, z2=false")
    complexity = data["complexity"]
    require(type(complexity) is dict and set(complexity) == {"naive", "reduced"}, "schema", "complexity must contain exactly naive and reduced")
    require(all(strict_integer(x) and x >= 0 for x in complexity.values()), "schema", "complexity values must be nonnegative integer literals")
    for side, bases, terminals in [("u", dims[0] * dims[1], rank), ("v", dims[1] * dims[2], rank), ("w", rank, dims[0] * dims[2])]:
        fresh, final = data[side + "_fresh"], data[side]
        require(type(fresh) is list and type(final) is list and len(final) == terminals, "schema", side + ": wrong row lists or terminal count")
        for index, row in enumerate(fresh):
            validate_row(row, bases + index, side + "_fresh[" + str(index) + "]", binary=True)
        for index, row in enumerate(final):
            validate_row(row, bases + len(fresh), side + "[" + str(index) + "]")
    return dims, rank


def validate_row(row, available, label, binary=False):
    require(type(row) is list and len(row) > 0, "schema", label + ": nonempty sparse row required")
    if binary:
        require(len(row) == 2, "schema", label + ": a fresh gate must have exactly two operands")
    for term in row:
        require(type(term) is dict and set(term) == {"index", "value"}, "schema", label + ": malformed term or hidden operation")
        require(strict_integer(term["index"]) and 0 <= term["index"] < available, "references", label + ": non-backward or out-of-range reference")
        require(strict_integer(term["value"]) and term["value"] in (-1, 1), "literals", label + ": only literal integer +1/-1 allowed")


def combine(row, pool, width):
    out = [0] * width
    for term in row:
        operand = pool[term["index"]]
        sign = term["value"]
        for i, value in enumerate(operand):
            out[i] += sign * value
    return out


def expand_side(data, side, bases):
    pool = [[int(i == j) for j in range(bases)] for i in range(bases)]
    for row in data[side + "_fresh"]:
        pool.append(combine(row, pool, bases))
    final = [combine(row, pool, bases) for row in data[side]]
    live = set()
    pending = [term["index"] for row in data[side] for term in row]
    while pending:
        reference = pending.pop()
        if reference < bases or reference in live:
            continue
        live.add(reference)
        pending.extend(term["index"] for term in data[side + "_fresh"][reference - bases])
    dead = sorted(set(range(bases, len(pool))) - live)
    require(not dead, "liveness", side + ": unreferenced fresh gates " + str(dead))
    for i, row in enumerate(final):
        require(any(row), "activity", side + ": zero terminal factor at " + str(i))
        require(all(value in (-1, 0, 1) for value in row), "ternary", side + ": nonternary expanded factor at " + str(i))
    intermediate_max = max(abs(value) for row in pool[bases:] for value in row) if len(pool) > bases else 0
    return final, {"fresh_binary_gates": len(pool) - bases,
                   "terminal_binary_gates": sum(len(row) - 1 for row in data[side]),
                   "live_fresh_gates": len(live), "max_abs_intermediate_coefficient": intermediate_max}


def canonical_sign(vector):
    first = next(x for x in vector if x)
    return tuple(x if first > 0 else -x for x in vector)


def tensor_check(dims, rank, U, V, output_forms):
    n, q, p = dims
    left, right, outputs = n * q, q * p, n * p
    # Each output form is a vector of product coefficients, so transpose it
    # explicitly to obtain the third rank-one factor of each product.
    W = [[output_forms[c][s] for c in range(outputs)] for s in range(rank)]
    require(all(any(row) for row in W), "activity", "a product is not active in any expanded output")
    signatures = {(canonical_sign(U[s]), canonical_sign(V[s])) for s in range(rank)}
    require(len(signatures) == rank, "distinctness", "duplicate products up to free signs")
    coefficients = [[[0] * outputs for _ in range(right)] for _ in range(left)]
    for s in range(rank):
        a_support = [(a, v) for a, v in enumerate(U[s]) if v]
        b_support = [(b, v) for b, v in enumerate(V[s]) if v]
        c_support = [(c, v) for c, v in enumerate(W[s]) if v]
        for a, u in a_support:
            for b, v in b_support:
                for c, w in c_support:
                    coefficients[a][b][c] += u * v * w
    mismatch = []
    inspected = 0
    nonzero = 0
    for a in range(left):
        for b in range(right):
            for c in range(outputs):
                inspected += 1
                target = int(a // q == c % n and a % q == b // p and b % p == c // n)
                actual = coefficients[a][b][c]
                nonzero += int(actual != 0)
                if actual != target:
                    mismatch.append([a, b, c, actual, target])
    require(not mismatch, "tensor", "integer tensor mismatch: " + str(mismatch[:8]) + "; total=" + str(len(mismatch)))
    return W, {"coefficients_checked": inspected, "nonzero_tensor_coefficients": nonzero, "active_distinct_products": len(signatures)}


def numeric_row(row, values):
    # This interpreter evaluates the signed operands in order, charging no
    # implicit scalar operation. It does not use expanded symbolic factors.
    answer = row[0]["value"] * values[row[0]["index"]]
    for term in row[1:]:
        if term["value"] == 1:
            answer += values[term["index"]]
        else:
            answer -= values[term["index"]]
    return answer


def execute_side(data, side, values):
    values = list(values)
    for row in data[side + "_fresh"]:
        values.append(numeric_row(row, values))
    return [numeric_row(row, values) for row in data[side]]


def basis_check(data, dims):
    n, q, p = dims
    tested = 0
    mismatches = []
    for a in range(n * q):
        A = [0] * (n * q)
        A[a] = 1
        for b in range(q * p):
            B = [0] * (q * p)
            B[b] = 1
            u = execute_side(data, "u", A)
            v = execute_side(data, "v", B)
            products = [x * y for x, y in zip(u, v)]
            got = execute_side(data, "w", products)
            ordinary = []
            for j in range(p):
                for i in range(n):
                    value = 0
                    for k in range(q):
                        value += A[i * q + k] * B[k * p + j]
                    ordinary.append(value)
            tested += 1
            if got != ordinary:
                mismatches.append([a, b, got, ordinary])
    require(not mismatches, "basis", "operational basis-pair mismatch: " + str(mismatches[:2]))
    return {"basis_pairs_executed": tested, "output_comparisons": tested * n * p}


def audit(data, sha256=None, expected_candidate=False):
    dims, rank = schema(data)
    U, u_cost = expand_side(data, "u", dims[0] * dims[1])
    V, v_cost = expand_side(data, "v", dims[1] * dims[2])
    O, w_cost = expand_side(data, "w", rank)
    costs = {"u": u_cost, "v": v_cost, "w": w_cost}
    reduced = sum(c["fresh_binary_gates"] + c["terminal_binary_gates"] for c in costs.values())
    naive = sum(sum(value != 0 for value in row) - 1 for matrix in [U, V, O] for row in matrix)
    require(data["complexity"] == {"naive": naive, "reduced": reduced}, "cost", "cost metadata mismatch; measured naive=" + str(naive) + " reduced=" + str(reduced))
    W, tensor = tensor_check(dims, rank, U, V, O)
    basis = basis_check(data, dims)
    if expected_candidate:
        require(dims == [4, 5, 8] and rank == 118 and reduced == 486, "expected-candidate", "candidate format/rank/cost differs from immutable target")
        require(sha256 == EXPECTED_SHA256, "expected-candidate", "candidate bytes differ from immutable snapshot")
    return {"pass": True, "sha256": sha256, "format": dims, "rank": rank,
            "integer_exact": True, "expanded_factors_ternary": True,
            "complexity": {"naive": naive, "reduced": reduced},
            "cost_detail": costs, "tensor": tensor, "execution": basis,
            "expanded_support": {"u": sum(bool(x) for row in U for x in row),
                                 "v": sum(bool(x) for row in V for x in row),
                                 "w": sum(bool(x) for row in W for x in row)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("object_path", help="SLP JSON object; no other input files needed")
    parser.add_argument("--expected-candidate", action="store_true", help="also require frozen ordered 4x5x8, rank 118, cost 486 and candidate SHA256")
    args = parser.parse_args()
    digest = None
    try:
        with open(args.object_path, "rb") as stream:
            raw = stream.read()
        digest = hashlib.sha256(raw).hexdigest()
        data = json.loads(raw, object_pairs_hook=reject_duplicate_keys)
        result = audit(data, digest, args.expected_candidate)
    except (CheckError, OSError, ValueError) as exc:
        result = {"pass": False, "sha256": digest, "stage": getattr(exc, "stage", "input"), "error": str(exc)}
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
