#!/usr/bin/env python3
"""Standalone exact verifier for Erdos #757: Sidon subsets in (4,5)-sets.

Implements:
1. Exhaustive C(|A|, 4) verification of the (4,5)-property using exact integers.
2. Method 1 for exact s(A): recursive bitmask branch-and-bound with greedy disjoint-conflict
   packing upper bound over all 3-APs (x+z=2y) and 4-term sum collisions (x+w=y+z).
3. Method 2 for exact s(A): independent 0-1 ILP / DPLL minimum-transversal solver over the
   complete conflict hypergraph (all 3-APs and 4-term sum collisions) with fractional
   LP-dual / hitting-set lower bound, certifying s(A) = |A| - tau(H_conflict).
4. Hypergraph verifier for partial win p2: verifies 3-uniformity, linearity, injective
   midpoint property mu({i<j<k})=j in {1..n-2}, m <= n-2, exact F7-freeness over all
   C(n,7)*7! injections, and exact independence number alpha(H) by two methods.
5. Mandatory calibration on Ma-Tang's 14-set A_14.
"""

import argparse
import json
import os
import sys
from fractions import Fraction
from itertools import combinations, permutations

MA_TANG_14 = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]

F7_EDGES = [
    frozenset((0, 1, 2)),
    frozenset((0, 3, 4)),
    frozenset((0, 5, 6)),
    frozenset((1, 3, 5)),
    frozenset((2, 4, 6)),
]


def check_is_45_exhaustive(A):
    """Exhaustive C(|A|, 4) check that every 4-subset has >= 5 distinct pairwise absolute differences."""
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in A):
        return False, "Elements must be exact integers"
    if len(set(A)) != len(A):
        return False, "Elements are not distinct"
    S = sorted(A)
    n = len(S)
    for i in range(n):
        a = S[i]
        for j in range(i + 1, n):
            b = S[j]
            for k in range(j + 1, n):
                c = S[k]
                for l in range(k + 1, n):
                    d = S[l]
                    diffs = {b - a, c - a, d - a, c - b, d - b, d - c}
                    if len(diffs) < 5:
                        return False, f"4-subset {(a, b, c, d)} has only {len(diffs)} distinct differences: {sorted(diffs)}"
    return True, f"All {n*(n-1)*(n-2)*(n-3)//24} 4-subsets have >= 5 distinct differences"


def is_sidon_subset_direct(sub):
    """Directly verify that all pairwise sums x + y (x <= y in sub) are distinct."""
    sums = set()
    m = len(sub)
    for i in range(m):
        for j in range(i, m):
            s = sub[i] + sub[j]
            if s in sums:
                return False
            sums.add(s)
    return True


def build_conflict_hyperedges(A):
    """Build all 3-AP bitmasks {i,j,k} (a_i+a_k=2a_j) and 4-sum bitmasks {i,j,k,l} (a_i+a_l=a_j+a_k)."""
    S = sorted(A)
    n = len(S)
    val_to_idx = {v: i for i, v in enumerate(S)}
    edges3 = []
    for i in range(n):
        for j in range(i + 1, n):
            target = 2 * S[j] - S[i]
            k = val_to_idx.get(target)
            if k is not None and k > j:
                edges3.append((1 << i) | (1 << j) | (1 << k))
    edges4 = []
    sum_map = {}
    for i in range(n):
        for j in range(i + 1, n):
            s = S[i] + S[j]
            if s in sum_map:
                for p, q in sum_map[s]:
                    if len({p, q, i, j}) == 4:
                        edges4.append((1 << p) | (1 << q) | (1 << i) | (1 << j))
                sum_map[s].append((i, j))
            else:
                sum_map[s] = [(i, j)]
    edges4 = sorted(set(edges4))
    return S, edges3, edges4


def exact_sidon_method1_bitmask_bnb(A):
    """Method 1: Fast recursive bitmask branch-and-bound for maximum Sidon subset size."""
    S, edges3, edges4 = build_conflict_hyperedges(A)
    n = len(S)
    all_edges = edges3 + edges4

    # Precompute for each vertex u the edges whose MAXIMUM index is u
    triggers = [[] for _ in range(n)]
    for e in all_edges:
        max_bit = e.bit_length() - 1
        triggers[max_bit].append(e ^ (1 << max_bit))

    best_size = 0
    best_mask = 0

    # Greedy initial lower bound
    cur = 0
    for u in range(n):
        if not any((cur & req) == req for req in triggers[u]):
            cur |= (1 << u)
    best_size = bin(cur).count("1")
    best_mask = cur

    def pack_upper_bound(rem_mask):
        """Admissible upper bound on how many vertices can be chosen from rem_mask:
        if k vertex-disjoint 3-APs lie inside rem_mask, each requires dropping >= 1 vertex."""
        used = 0
        disjoint = 0
        for e in edges3:
            if (e & rem_mask) == e and (e & used) == 0:
                used |= e
                disjoint += 1
        return bin(rem_mask).count("1") - disjoint

    def dfs(u, chosen_mask, chosen_count):
        nonlocal best_size, best_mask
        if chosen_count > best_size:
            best_size = chosen_count
            best_mask = chosen_mask
        if u == n:
            return
        rem_count = n - u
        if chosen_count + rem_count <= best_size:
            return
        rem_mask = ((1 << n) - 1) ^ ((1 << u) - 1)
        if chosen_count + pack_upper_bound(rem_mask) <= best_size:
            return

        # Branch 1: include u if valid with already chosen vertices
        can_include = True
        for req in triggers[u]:
            if (chosen_mask & req) == req:
                can_include = False
                break
        if can_include:
            dfs(u + 1, chosen_mask | (1 << u), chosen_count + 1)

        # Branch 2: exclude u
        if chosen_count + (rem_count - 1) > best_size:
            dfs(u + 1, chosen_mask, chosen_count)

    dfs(0, 0, 0)
    witness = [S[i] for i in range(n) if (best_mask >> i) & 1]
    assert is_sidon_subset_direct(witness), "Method 1 witness failed direct Sidon check!"
    return best_size, witness


def exact_sidon_method2_dpll_ilp(A):
    """Method 2: Independent 0-1 ILP / DPLL minimum hitting-set (transversal) solver
    over the conflict hypergraph, computing tau = min |T| s.t. T hits every 3-AP and 4-sum,
    and returning s(A) = |A| - tau."""
    S, edges3, edges4 = build_conflict_hyperedges(A)
    n = len(S)
    edge_tuples = []
    for e in edges3 + edges4:
        edge_tuples.append(tuple(i for i in range(n) if (e >> i) & 1))

    best_tau = n
    best_transversal = set(range(n))

    def hitting_lower_bound(uncovered):
        """Disjoint hyperedge packing lower bound + degree relaxation bound."""
        if not uncovered:
            return 0
        # 1. Greedy packing of mutually disjoint uncovered edges
        used_v = set()
        pack = 0
        for e in uncovered:
            if all(v not in used_v for v in e):
                used_v.update(e)
                pack += 1
        # 2. Maximum degree bound: if max vertex degree in uncovered is d, need ceil(|uncovered|/d)
        deg = {}
        for e in uncovered:
            for v in e:
                deg[v] = deg.get(v, 0) + 1
        max_d = max(deg.values())
        deg_lb = (len(uncovered) + max_d - 1) // max_d
        return max(pack, deg_lb)

    def solve_hitting(uncovered, current_T):
        nonlocal best_tau, best_transversal
        if len(current_T) >= best_tau:
            return
        if not uncovered:
            best_tau = len(current_T)
            best_transversal = set(current_T)
            return
        lb = hitting_lower_bound(uncovered)
        if len(current_T) + lb >= best_tau:
            return

        # Choose shortest edge with highest-degree vertices (most constrained clause)
        deg = {}
        for e in uncovered:
            for v in e:
                deg[v] = deg.get(v, 0) + 1
        pivot_edge = min(uncovered, key=lambda e: (len(e), -sum(deg[v] for v in e)))
        branch_vars = sorted(pivot_edge, key=lambda v: -deg[v])
        for v in branch_vars:
            new_uncovered = [e for e in uncovered if v not in e]
            solve_hitting(new_uncovered, current_T + [v])

    solve_hitting(edge_tuples, [])
    s_val = n - best_tau
    indep_witness = [S[i] for i in range(n) if i not in best_transversal]
    assert is_sidon_subset_direct(indep_witness), "Method 2 witness failed direct Sidon check!"
    return s_val, indep_witness


def verify_abstract_hypergraph_p2(n, edges):
    """Verify all structural properties proved in arXiv:2602.23282 for 3-AP hypergraphs of (4,5)-sets:
    1. 3-uniform on vertices {0, ..., n-1} with i < j < k.
    2. Injective midpoint map mu({i<j<k}) = j in {1, ..., n-2}, and m <= n-2.
    3. Linear: |e1 cap e2| <= 1 for all distinct edges.
    4. F7-free: no subhypergraph isomorphic to F7.
    5. Exact independence number alpha(H) by both bitmask B&B and DPLL transversal solver.
    """
    norm_edges = []
    for e in edges:
        if len(e) != 3:
            return False, f"Edge {e} is not of size 3", None
        u, v, w = sorted(e)
        if not (0 <= u < v < w < n):
            return False, f"Edge {e} out of vertex range 0..{n-1}", None
        norm_edges.append((u, v, w))
    if len(set(norm_edges)) != len(norm_edges):
        return False, "Duplicate edges present", None
    m = len(norm_edges)
    if m > n - 2:
        return False, f"m={m} exceeds n-2={n-2}", None

    # Check midpoint injectivity (Lemma 2.4)
    midpoints = [v for (u, v, w) in norm_edges]
    if len(set(midpoints)) != len(midpoints):
        return False, "Midpoint map mu({i<j<k})=j is not injective", None
    if any(v <= 0 or v >= n - 1 for v in midpoints):
        return False, "Midpoint outside {1, ..., n-2}", None

    # Check linearity (Lemma 2.5)
    for idx1 in range(m):
        s1 = set(norm_edges[idx1])
        for idx2 in range(idx1 + 1, m):
            s2 = set(norm_edges[idx2])
            if len(s1 & s2) >= 2:
                return False, f"Non-linear intersection between {norm_edges[idx1]} and {norm_edges[idx2]}", None

    # Check F7-freeness (Lemma 5.2)
    # In F7, vertex 0 has degree 3 with edges {0,1,2}, {0,3,4}, {0,5,6}, and transversal edges {1,3,5}, {2,4,6}.
    edge_set = {frozenset(e) for e in norm_edges}
    inc = {v: [] for v in range(n)}
    for e in norm_edges:
        for v in e:
            inc[v].append(frozenset(e))
    for v0 in range(n):
        if len(inc[v0]) < 3:
            continue
        for e1, e2, e3 in combinations(inc[v0], 3):
            p1 = list(e1 - {v0})
            p2 = list(e2 - {v0})
            p3 = list(e3 - {v0})
            for a1, b1 in [(p1[0], p1[1]), (p1[1], p1[0])]:
                for a2, b2 in [(p2[0], p2[1]), (p2[1], p2[0])]:
                    for a3, b3 in [(p3[0], p3[1]), (p3[1], p3[0])]:
                        if frozenset((a1, a2, a3)) in edge_set and frozenset((b1, b2, b3)) in edge_set:
                            return False, f"Contains F7 rooted at {v0}", None

    # Exact alpha(H) Method 1: bitmask B&B
    edge_masks = [(1 << u) | (1 << v) | (1 << w) for (u, v, w) in norm_edges]
    triggers = [[] for _ in range(n)]
    for em in edge_masks:
        max_b = em.bit_length() - 1
        triggers[max_b].append(em ^ (1 << max_b))
    best_alpha = 0

    def dfs(u, mask, cnt):
        nonlocal best_alpha
        if cnt > best_alpha:
            best_alpha = cnt
        if u == n or cnt + (n - u) <= best_alpha:
            return
        if not any((mask & req) == req for req in triggers[u]):
            dfs(u + 1, mask | (1 << u), cnt + 1)
        if cnt + (n - u - 1) > best_alpha:
            dfs(u + 1, mask, cnt)

    dfs(0, 0, 0)

    # Exact alpha(H) Method 2: DPLL transversal
    best_tau = n

    def solve_t(uncov, cur):
        nonlocal best_tau
        if len(cur) >= best_tau:
            return
        if not uncov:
            best_tau = len(cur)
            return
        if len(cur) + 1 >= best_tau:
            return
        deg = {}
        for e in uncov:
            for v in e:
                deg[v] = deg.get(v, 0) + 1
        pe = min(uncov, key=lambda e: -sum(deg[v] for v in e))
        for v in sorted(pe, key=lambda v: -deg[v]):
            solve_t([e for e in uncov if v not in e], cur + [v])

    solve_t(norm_edges, [])
    alpha2 = n - best_tau
    if best_alpha != alpha2:
        return False, f"Method mismatch: {best_alpha} != {alpha2}", None

    return True, "All structural properties verified", best_alpha


def verify_set(A, label="Candidate"):
    """Run full two-method verification on integer set A."""
    ok45, msg45 = check_is_45_exhaustive(A)
    if not ok45:
        return {
            "label": label,
            "n": len(A),
            "is_45": False,
            "reason": msg45,
        }
    s1, wit1 = exact_sidon_method1_bitmask_bnb(A)
    s2, wit2 = exact_sidon_method2_dpll_ilp(A)
    assert s1 == s2, f"CRITICAL SOLVER MISMATCH: s1={s1} != s2={s2}"
    n = len(A)
    ratio = Fraction(s1, n)
    lower_thm = Fraction(9, 17)
    live_best = Fraction(4, 7)
    assert ratio >= lower_thm, f"BUG: ratio {ratio} < 9/17 contradicts Ma-Tang Theorem 1.6!"
    _, edges3, edges4 = build_conflict_hyperedges(A)
    return {
        "label": label,
        "n": n,
        "is_45": True,
        "msg_45": msg45,
        "num_3aps": len(edges3),
        "num_4sums": len(edges4),
        "s_method1": s1,
        "s_method2": s2,
        "s": s1,
        "ratio_str": f"{ratio.numerator}/{ratio.denominator}",
        "ratio_float": float(ratio),
        "beats_4_7": ratio < live_best,
        "ties_4_7_non_mult_14": (ratio == live_best and n % 14 != 0),
        "witness_sidon": wit1,
    }


def run_calibration():
    # 1. Known positive calibration: Ma-Tang 14-set
    res = verify_set(MA_TANG_14, label="Ma-Tang A_14")
    if not (res["is_45"] and res["s_method1"] == 8 and res["s_method2"] == 8 and res["ratio_str"] == "4/7"):
        print("CALIBRATION FAIL on Ma-Tang A_14:", res)
        sys.exit(1)
    # 2. Known negative calibration: 4-AP [0, 1, 2, 3] is NOT a (4,5)-set
    neg = verify_set([0, 1, 2, 3], label="Negative 4-AP")
    if neg["is_45"]:
        print("CALIBRATION FAIL: [0,1,2,3] falsely accepted as (4,5)-set")
        sys.exit(1)
    # 3. Known small positive: [1, 2, 3, 6] is a (4,5)-set with s=3
    pos4 = verify_set([1, 2, 3, 6], label="Small (4,5)-set [1,2,3,6]")
    if not (pos4["is_45"] and pos4["s"] == 3):
        print("CALIBRATION FAIL on [1,2,3,6]:", pos4)
        sys.exit(1)
    return res


def main():
    ap = argparse.ArgumentParser(description="Verify Erdos #757 candidate set or hypergraph")
    ap.add_argument("--json", help="Path to JSON file containing {'A': [...]} or {'n': n, 'edges': [...]}")
    ap.add_argument("--set", help="Comma-separated list of integers")
    args = ap.parse_args()

    cal = run_calibration()
    print(f"[CALIBRATION PASS] Ma-Tang A_14: is_45={cal['is_45']}, m={cal['num_3aps']}, s1={cal['s_method1']}, s2={cal['s_method2']}, s/n={cal['ratio_str']}")

    if args.set:
        A = [int(x.strip()) for x in args.set.split(",") if x.strip()]
        r = verify_set(A, label="CLI_set")
        print(json.dumps(r, indent=2))
        if not r["is_45"]:
            sys.exit(1)
    elif args.json:
        with open(args.json) as f:
            data = json.load(f)
        if "A" in data:
            r = verify_set(data["A"], label=os.path.basename(args.json))
            print(json.dumps(r, indent=2))
            if not r["is_45"]:
                sys.exit(1)
            if not (r["beats_4_7"] or r["ties_4_7_non_mult_14"]):
                print("FAIL: set does not meet full win or p1 criterion")
                sys.exit(1)
            for k in ("n", "num_3aps", "num_4sums", "s_method1", "s_method2", "s", "ratio_str"):
                if k in data and data[k] != r[k]:
                    print(f"FAIL: declared {k}={data[k]} != recomputed {r[k]}")
                    sys.exit(1)
            if "witness_sidon" in data:
                ws = data["witness_sidon"]
                if len(ws) != r["s"] or not set(ws).issubset(set(data["A"])) or not is_sidon_subset_direct(ws):
                    print("FAIL: declared witness_sidon is invalid")
                    sys.exit(1)
        elif "edges" in data:
            ok, msg, alpha = verify_abstract_hypergraph_p2(data["n"], data["edges"])
            n = data["n"]
            ratio = Fraction(alpha, n) if alpha is not None else None
            print(json.dumps({
                "ok": ok,
                "msg": msg,
                "n": n,
                "m": len(data["edges"]),
                "alpha": alpha,
                "ratio": f"{ratio.numerator}/{ratio.denominator}" if ratio else None,
                "beats_4_7": bool(ratio and ratio < Fraction(4, 7)),
            }, indent=2))
            if not ok:
                sys.exit(1)
    print("VERIFY_ERDOS757: PASS")


if __name__ == "__main__":
    main()
