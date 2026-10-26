#!/usr/bin/env python3
"""
Standalone deterministic verifier for Conway's 99-Graph Problem (srg(99, 14, 1, 2)),
Tracks p2 (forced-structure reduction of arXiv:2608.11211) and p1 (DRAT/LRAT-checked
prime-order and Frobenius automorphism exclusions).

Uses only the Python standard library. Independently:
1. Re-generates all 26 CNF formulas from scratch across two independent cardinality
   encodings:
   - Encoding A: Sinz (2005) Sequential Counter
   - Encoding B: Bailleux & Boufkhad (2003) Binary Tree Unary Totalizer
2. Verifies positive non-vacuity on srg(9, 4, 1, 2) = K_3 box K_3 by propagating the
   explicit 4-cycle outer truth assignment on the unblocked Encoding A and Encoding B
   formulas and confirming every clause is satisfied.
3. Verifies that every clause in each of the 26 trimmed CNF core files (*_core.cnf)
   is an exact member of the freshly generated CNF from its corresponding encoder.
4. Verifies all SHA-256 digests, clause counts, variable counts, and cycle-structure
   invariants against certificate.json.
5. Verifies all 26 LRAT proofs (19,693 Reverse Unit Propagation steps across Encoding A
   and Encoding B, with 0 RAT lemmas) from the trimmed CNF cores to the empty clause 0
   using a self-contained pure-Python LRAT RUP checker.
"""

import hashlib
import itertools
import json
import os
import sys


# ==============================================================================
# Dual Cardinality Encoders (Encoding A = Sinz 2005, Encoding B = Totalizer 2003)
# ==============================================================================

def add_exact_sinz(clauses, L, k, next_var):
    """Encoding A: Sinz (2005) Linear Sequential Counter for sum(L) == k."""
    n = len(L)
    if k == 0:
        for x in L:
            clauses.append([-x])
        return next_var
    if n < k:
        clauses.append([])
        return next_var
    s = [[next_var + i * k + j for j in range(k)] for i in range(n)]
    next_var += n * k
    clauses.append([-L[0], s[0][0]])
    clauses.append([L[0], -s[0][0]])
    for j in range(1, k):
        clauses.append([-s[0][j]])
    for i in range(1, n):
        x = L[i]
        clauses.append([-s[i - 1][0], s[i][0]])
        clauses.append([-x, s[i][0]])
        clauses.append([s[i - 1][0], x, -s[i][0]])
        for j in range(1, k):
            clauses.append([-s[i - 1][j], s[i][j]])
            clauses.append([-s[i - 1][j - 1], -x, s[i][j]])
            clauses.append([s[i - 1][j], s[i - 1][j - 1], -s[i][j]])
            clauses.append([s[i - 1][j], x, -s[i][j]])
        clauses.append([-s[i - 1][k - 1], -x])
    clauses.append([s[n - 1][k - 1]])
    return next_var


def add_exact_totalizer(clauses, L, k, next_var):
    """Encoding B: Bailleux & Boufkhad (2003) Binary Tree Totalizer for sum(L) == k."""
    if k == 0:
        for x in L:
            clauses.append([-x])
        return next_var
    if len(L) < k:
        clauses.append([])
        return next_var

    def build_tree(items):
        nonlocal next_var
        if len(items) == 1:
            return [items[0]]
        mid = len(items) // 2
        left = build_tree(items[:mid])
        right = build_tree(items[mid:])
        m = min(k, len(left) + len(right))
        out = [next_var + i for i in range(m)]
        next_var += m
        for a in range(len(left) + 1):
            for b in range(len(right) + 1):
                if a == 0 and b == 0:
                    continue
                lits = []
                if a > 0:
                    lits.append(-left[a - 1])
                if b > 0:
                    lits.append(-right[b - 1])
                if a + b > k:
                    clauses.append(lits)
                else:
                    clauses.append(lits + [out[a + b - 1]])
        for c in range(1, m + 1):
            for a in range(c):
                b = c - 1 - a
                if a > len(left) or b > len(right):
                    continue
                cl = [-out[c - 1]]
                if a < len(left):
                    cl.append(left[a])
                if b < len(right):
                    cl.append(right[b])
                clauses.append(cl)
        return out

    root = build_tree(L)
    clauses.append([root[k - 1]])
    return next_var


def add_exact(clauses, L, k, next_var, encoding):
    if encoding == "A":
        return add_exact_sinz(clauses, L, k, next_var)
    return add_exact_totalizer(clauses, L, k, next_var)


def deduplicate_clauses(clauses):
    return sorted(set(tuple(sorted(set(c))) for c in clauses))


# ==============================================================================
# Track p2 Builders (Forced-Structure Reduction of arXiv:2608.11211)
# ==============================================================================

def build_p2_1_inner_matching(k, encoding):
    pair_var = {}
    vc = 0
    for a in range(k):
        for b in range(a + 1, k):
            vc += 1
            pair_var[(a, b)] = vc
            pair_var[(b, a)] = vc
    clauses = []
    next_var = vc + 1
    for a in range(k):
        L = [pair_var[(a, b)] for b in range(k) if b != a]
        next_var = add_exact(clauses, L, 1, next_var, encoding)
    clauses.append([pair_var[(0, 1)]])
    clauses.append([pair_var[(0, 2)]])
    return next_var - 1, deduplicate_clauses(clauses)


def build_p2_2_outer_bijection(k, encoding):
    M = k * (k - 2) // 2

    def b_var(u, a):
        return u * k + a + 1

    clauses = []
    next_var = M * k + 1
    for u in range(min(M, 6)):
        L = [b_var(u, a) for a in range(k)]
        next_var = add_exact(clauses, L, 2, next_var, encoding)

    and_01 = []
    for u in range(M):
        c = next_var
        next_var += 1
        v1, v2 = b_var(u, 0), b_var(u, 1)
        clauses.append([-c, v1])
        clauses.append([-c, v2])
        clauses.append([c, -v1, -v2])
        and_01.append(c)
    next_var = add_exact(clauses, and_01, 0, next_var, encoding)

    and_02 = []
    for u in range(M):
        c = next_var
        next_var += 1
        v1, v2 = b_var(u, 0), b_var(u, 2)
        clauses.append([-c, v1])
        clauses.append([-c, v2])
        clauses.append([c, -v1, -v2])
        and_02.append(c)
    next_var = add_exact(clauses, and_02, 1, next_var, encoding)

    z1, z2 = next_var, next_var + 1
    next_var += 2
    clauses.append([z1, z2])
    clauses.append([-z1, b_var(0, 0)])
    clauses.append([-z1, b_var(0, 1)])
    clauses.append([-z2, b_var(0, 0)])
    clauses.append([-z2, b_var(0, 2)])
    clauses.append([-z2, b_var(1, 0)])
    clauses.append([-z2, b_var(1, 2)])
    return next_var - 1, deduplicate_clauses(clauses)


def build_p2_3_inner_outer_balance(k, encoding):
    clauses = []
    next_var = 1
    P_u = {0, 2}
    matched_partner = {i: (i ^ 1) for i in range(k)}

    viol_vars = []
    for a in range(k):
        edge_vars = [next_var + j for j in range(k - 2)]
        next_var += k - 2
        m_in_Pu = next_var
        next_var += 1
        if matched_partner[a] in P_u:
            clauses.append([m_in_Pu])
        else:
            clauses.append([-m_in_Pu])
        full_L = [m_in_Pu] + edge_vars
        full_rhs = 1 if a in P_u else 2
        next_var = add_exact(clauses, full_L, full_rhs, next_var, encoding)

        target_rhs = 1 if (a in P_u or matched_partner[a] in P_u) else 2
        v_low = next_var
        v_high = next_var + 1
        next_var += 2
        viol_vars.extend([v_low, v_high])
        for comb in itertools.combinations(edge_vars, target_rhs):
            clauses.append([-v_low] + [-x for x in comb])
        for comb in itertools.combinations(edge_vars, len(edge_vars) - target_rhs):
            clauses.append([-v_high] + list(comb))

    clauses.append(viol_vars)
    return next_var - 1, deduplicate_clauses(clauses)


def build_p2_4_outer_pair_cn(encoding):
    clauses = []
    next_var = 1
    viol_vars = []
    for s in (0, 1):
        e_uv = next_var
        s_var = next_var + 1
        cn_vars = [next_var + 2 + i for i in range(12)]
        next_var += 14
        if s == 1:
            clauses.append([s_var])
        else:
            clauses.append([-s_var])
        full_L = [s_var, e_uv] + cn_vars
        next_var = add_exact(clauses, full_L, 2, next_var, encoding)

        for adj_val, target in ((1, 1 - s), (0, 2 - s)):
            if target > 0:
                v_low = next_var
                next_var += 1
                viol_vars.append(v_low)
                clauses.append([-v_low, e_uv if adj_val == 1 else -e_uv])
                for comb in itertools.combinations(cn_vars, target):
                    clauses.append([-v_low] + [-x for x in comb])
            v_high = next_var
            next_var += 1
            viol_vars.append(v_high)
            clauses.append([-v_high, e_uv if adj_val == 1 else -e_uv])
            for comb in itertools.combinations(cn_vars, len(cn_vars) - target):
                clauses.append([-v_high] + list(comb))

    clauses.append(viol_vars)
    return next_var - 1, deduplicate_clauses(clauses)


def build_p2_5_srg9_uniqueness(encoding, add_blocking_clause=True):
    inner4 = [(i, s) for i in range(2) for s in ("L", "R")]

    def matched4(v):
        return (v[0], "R" if v[1] == "L" else "L")

    outer4 = [
        ((0, "L"), (1, "L")),
        ((0, "L"), (1, "R")),
        ((0, "R"), (1, "L")),
        ((0, "R"), (1, "R")),
    ]
    pair_to_var = {}
    vc = 0
    for p in range(4):
        for q in range(p + 1, 4):
            vc += 1
            pair_to_var[(p, q)] = vc
            pair_to_var[(q, p)] = vc

    clauses = []
    next_var = vc + 1

    for p in range(4):
        P_p = set(outer4[p])
        M_p = {matched4(u) for u in P_p}
        for a in inner4:
            qs = [q for q in range(4) if q != p and a in outer4[q]]
            L = [pair_to_var[(p, q)] for q in qs]
            rhs = 1 if (a in P_p or a in M_p) else 2
            next_var = add_exact(clauses, L, rhs, next_var, encoding)

    for p in range(4):
        for q in range(p + 1, 4):
            s = len(set(outer4[p]) & set(outer4[q]))
            rhs = 2 - s
            L = [pair_to_var[(p, q)]]
            for r in range(4):
                if r == p or r == q:
                    continue
                c = next_var
                next_var += 1
                v1, v2 = pair_to_var[(p, r)], pair_to_var[(q, r)]
                clauses.append([-c, v1])
                clauses.append([-c, v2])
                clauses.append([c, -v1, -v2])
                L.append(c)
            next_var = add_exact(clauses, L, rhs, next_var, encoding)

    if add_blocking_clause:
        block = []
        for p in range(4):
            for q in range(p + 1, 4):
                s = len(set(outer4[p]) & set(outer4[q]))
                v = pair_to_var[(p, q)]
                block.append(-v if s == 1 else v)
        clauses.append(block)

    return next_var - 1, deduplicate_clauses(clauses)


# ==============================================================================
# Track p1 Builders (Automorphism Exclusions on srg(99, 14, 1, 2))
# ==============================================================================

INNER = [(i, s) for i in range(7) for s in ("L", "R")]
INNER_IDX = {v: idx for idx, v in enumerate(INNER)}


def matched(v):
    return (v[0], "R" if v[1] == "L" else "L")


OUTER = []
for _i1 in range(14):
    for _i2 in range(_i1 + 1, 14):
        _u, _v = INNER[_i1], INNER[_i2]
        if _v != matched(_u):
            OUTER.append((_u, _v))
OUTER_IDX = {pair: idx for idx, pair in enumerate(OUTER)}


def canon_pair(u, v):
    return (u, v) if INNER_IDX[u] < INNER_IDX[v] else (v, u)


def make_involution_perms(a, b, c):
    assert 2 * a + b + c == 7
    perm0 = {v: v for v in INNER}
    perm1 = {}
    for idx in range(a):
        e1, e2 = 2 * idx, 2 * idx + 1
        for s in ("L", "R"):
            perm1[(e1, s)] = (e2, s)
            perm1[(e2, s)] = (e1, s)
    for idx in range(2 * a, 2 * a + b):
        perm1[(idx, "L")] = (idx, "R")
        perm1[(idx, "R")] = (idx, "L")
    for idx in range(2 * a + b, 7):
        perm1[(idx, "L")] = (idx, "L")
        perm1[(idx, "R")] = (idx, "R")
    return [perm0, perm1]


def compute_cycle_stats(perms, prime_order):
    gen = perms[1]
    fix_inner = sum(1 for v in INNER if gen[v] == v)
    fix_outer = 0
    for p in range(84):
        u, v = OUTER[p]
        p_img = OUTER_IDX[canon_pair(gen[u], gen[v])]
        if p_img == p:
            fix_outer += 1
    total_fix = 1 + fix_inner + fix_outer
    moved = 99 - total_fix
    assert moved % prime_order == 0
    return {
        "generator_prime_order": prime_order,
        "group_order": len(perms),
        "fixed_root": 1,
        "fixed_in_Gamma1": fix_inner,
        "fixed_in_Gamma2": fix_outer,
        "total_fixed_vertices_in_Gamma": total_fix,
        "moved_vertices_in_Gamma": moved,
        "num_generator_p_cycles_in_Gamma": moved // prime_order,
    }


def build_automorphism_cnf(perms, encoding="A", r4_mode="all"):
    def group_elems_fn(p):
        u, v = OUTER[p]
        return [OUTER_IDX[canon_pair(perm[u], perm[v])] for perm in perms]

    num_outer = 84
    edge_orbits = {}
    pair_to_var = {}
    var_count = 0
    for p in range(num_outer):
        imgs_p = group_elems_fn(p)
        for q in range(p + 1, num_outer):
            imgs_q = group_elems_fn(q)
            canon = min((min(ip, iq), max(ip, iq)) for ip, iq in zip(imgs_p, imgs_q))
            if canon not in edge_orbits:
                var_count += 1
                edge_orbits[canon] = var_count
            pair_to_var[(p, q)] = edge_orbits[canon]
            pair_to_var[(q, p)] = edge_orbits[canon]

    clauses = []
    next_var = var_count + 1

    seen_p = set()
    outer_reps = []
    for p in range(num_outer):
        if p not in seen_p:
            outer_reps.append(p)
            for ip in group_elems_fn(p):
                seen_p.add(ip)

    for p in outer_reps:
        P_p = set(OUTER[p])
        M_p = {matched(u) for u in P_p}
        for a in INNER:
            qs = [q for q in range(num_outer) if q != p and a in OUTER[q]]
            L = [pair_to_var[(p, q)] for q in qs]
            rhs = 1 if (a in P_p or a in M_p) else 2
            for v in set(L):
                if L.count(v) > rhs:
                    clauses.append([-v])
            if encoding == "A":
                next_var = add_exact_sinz(clauses, L, rhs, next_var)
            else:
                next_var = add_exact_totalizer(clauses, L, rhs, next_var)

    if r4_mode != "none":
        seen_pairs = set()
        pair_reps = []
        for p in range(num_outer):
            imgs_p = group_elems_fn(p)
            for q in range(p + 1, num_outer):
                imgs_q = group_elems_fn(q)
                canon = min((min(ip, iq), max(ip, iq)) for ip, iq in zip(imgs_p, imgs_q))
                if canon not in seen_pairs:
                    seen_pairs.add(canon)
                    pair_reps.append(canon)

        for p, q in pair_reps:
            s = len(set(OUTER[p]) & set(OUTER[q]))
            rhs = 2 - s
            e_pq = pair_to_var[(p, q)]
            pair_counts = {}
            for r in range(num_outer):
                if r == p or r == q:
                    continue
                v1, v2 = pair_to_var[(p, r)], pair_to_var[(q, r)]
                if v1 > v2:
                    v1, v2 = v2, v1
                pair_counts[(v1, v2)] = pair_counts.get((v1, v2), 0) + 1
            for (v1, v2), m in pair_counts.items():
                if m > rhs:
                    clauses.append([-v1] if v1 == v2 else [-v1, -v2])
                elif m == rhs:
                    clauses.append(sorted(set([-e_pq, -v1, -v2])))

        and_cache = {}

        def get_and_var(v1, v2):
            nonlocal next_var
            if v1 == v2:
                return v1
            if v1 > v2:
                v1, v2 = v2, v1
            if (v1, v2) not in and_cache:
                c = next_var
                next_var += 1
                clauses.append([-c, v1])
                clauses.append([-c, v2])
                clauses.append([c, -v1, -v2])
                and_cache[(v1, v2)] = c
            return and_cache[(v1, v2)]

        for p, q in pair_reps:
            if r4_mode == "conj":
                if q not in group_elems_fn(p):
                    continue
            elif r4_mode == "conj_or_fix":
                gp = group_elems_fn(p)
                gq = group_elems_fn(q)
                if not ((q in gp) or (len(set(gp)) == 1 and len(set(gq)) == 1)):
                    continue
            s = len(set(OUTER[p]) & set(OUTER[q]))
            rhs = 2 - s
            L = [pair_to_var[(p, q)]]
            for r in range(num_outer):
                if r == p or r == q:
                    continue
                L.append(get_and_var(pair_to_var[(p, r)], pair_to_var[(q, r)]))
            if encoding == "A":
                next_var = add_exact_sinz(clauses, L, rhs, next_var)
            else:
                next_var = add_exact_totalizer(clauses, L, rhs, next_var)

    if r4_mode == "frob21_fig10":
        rep_LL = OUTER_IDX[((0, "L"), (1, "L"))]
        rep_RR = OUTER_IDX[((0, "R"), (1, "R"))]
        rep_LR = OUTER_IDX[((0, "L"), (1, "R"))]
        rep_RL = OUTER_IDX[((0, "R"), (1, "L"))]
        orbs = {
            "LL": sorted(set(group_elems_fn(rep_LL))),
            "RR": sorted(set(group_elems_fn(rep_RR))),
            "LR": sorted(set(group_elems_fn(rep_LR))),
            "RL": sorted(set(group_elems_fn(rep_RL))),
        }
        for name in ("LR", "RL"):
            for p in orbs[name]:
                for q in orbs[name]:
                    if p < q:
                        clauses.append([-pair_to_var[(p, q)]])
        add_fn = add_exact_sinz if encoding == "A" else add_exact_totalizer
        for p, target_orb in ((rep_LL, orbs["LL"]), (rep_LL, orbs["RR"]), (rep_RR, orbs["RR"])):
            L = [pair_to_var[(p, q)] for q in target_orb if q != p]
            next_var = add_fn(clauses, L, 2, next_var)

    return var_count, len(outer_reps), next_var - 1, deduplicate_clauses(clauses)


# ==============================================================================
# Pure-Python Verification Routines (Positive Control, CNF Membership, LRAT)
# ==============================================================================

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def parse_dimacs_clauses(cnf_path):
    clauses = []
    with open(cnf_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("c") or line.startswith("p"):
                continue
            toks = [int(x) for x in line.split()]
            if toks and toks[-1] == 0:
                toks = toks[:-1]
            clauses.append(tuple(sorted(toks)))
    return clauses


def verify_positive_control_srg9(clauses):
    """
    Verifies that the unique outer 4-cycle assignment of srg(9, 4, 1, 2) = K_3 box K_3:
      E(0,1)=True (var 1), E(0,2)=True (var 2), E(0,3)=False (var 3),
      E(1,2)=False (var 4), E(1,3)=True (var 5), E(2,3)=True (var 6)
    propagates deterministically via unit propagation to a complete satisfying assignment
    of every clause in the unblocked formula (both Encoding A and Encoding B).
    """
    assign = {1: True, 2: True, 3: False, 4: False, 5: True, 6: True}
    changed = True
    while changed:
        changed = False
        for cl in clauses:
            satisfied = False
            unassigned = []
            for lit in cl:
                v = abs(lit)
                if v in assign:
                    val = assign[v]
                    if (lit > 0 and val) or (lit < 0 and not val):
                        satisfied = True
                        break
                else:
                    unassigned.append(lit)
            if satisfied:
                continue
            if len(unassigned) == 0:
                return False
            if len(unassigned) == 1:
                u_lit = unassigned[0]
                assign[abs(u_lit)] = (u_lit > 0)
                changed = True
    for cl in clauses:
        if not any(
            (lit > 0 and assign.get(abs(lit), False))
            or (lit < 0 and not assign.get(abs(lit), True))
            for lit in cl
        ):
            return False
    return True


def verify_lrat_python(cnf_clauses, lrat_paths):
    """Standalone pure-Python LRAT/RUP verifier across one or more sequential LRAT files."""
    active = {idx + 1: list(cl) for idx, cl in enumerate(cnf_clauses)}
    derived_count = 0
    empty_clause_proved = False

    for lrat_path in lrat_paths:
        with open(lrat_path, "r") as f:
            for raw_line in f:
                tokens = raw_line.strip().split()
                if not tokens:
                    continue
                if len(tokens) >= 2 and tokens[1] == "d":
                    for tok in tokens[2:]:
                        cid = int(tok)
                        if cid != 0:
                            active.pop(cid, None)
                    continue
                ints = [int(x) for x in tokens]
                new_id = ints[0]
                zero1 = ints.index(0, 1)
                lemma_lits = ints[1:zero1]
                hints = [h for h in ints[zero1 + 1:] if h != 0]
                if any(h < 0 for h in hints):
                    raise ValueError(f"RAT hint encountered at step {new_id}")

                falsified = set(lemma_lits)
                conflict = False
                for h in hints:
                    cl = active.get(abs(h))
                    if cl is None:
                        raise ValueError(f"LRAT step {new_id} references inactive clause {h}")
                    unassigned = []
                    satisfied = False
                    for lit in cl:
                        if -lit in falsified:
                            satisfied = True
                            break
                        if lit not in falsified:
                            unassigned.append(lit)
                    if satisfied:
                        continue
                    if len(unassigned) == 0:
                        conflict = True
                        break
                    if len(unassigned) == 1:
                        falsified.add(-unassigned[0])
                    else:
                        raise ValueError(f"LRAT step {new_id} hint {h} is not unit: {unassigned}")

                if not conflict:
                    raise ValueError(f"LRAT step {new_id} failed to reach conflict via RUP hints")
                active[new_id] = lemma_lits
                derived_count += 1
                if len(lemma_lits) == 0:
                    empty_clause_proved = True

    if not empty_clause_proved:
        raise ValueError("LRAT proof did not derive empty clause")
    return derived_count


def fail(msg):
    print(f"ERROR: {msg}")
    print("FAIL")
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    obj_cert = os.path.join(here, "..", "object", "certificate.json")
    local_cert = os.path.join(here, "certificate.json")
    cert_path = obj_cert if os.path.isfile(obj_cert) else local_cert

    obj_proofs = os.path.join(here, "..", "object", "proofs")
    local_proofs = os.path.join(here, "proofs")
    proofs_dir = obj_proofs if os.path.isdir(obj_proofs) else local_proofs

    if not os.path.isfile(cert_path):
        fail("certificate.json not found")
    if not os.path.isdir(proofs_dir):
        fail("proofs directory not found")

    try:
        with open(cert_path, "r") as f:
            cert = json.load(f)
    except Exception as e:
        fail(f"Could not parse certificate.json: {e}")

    if cert.get("target_id") != "conway-99-graph":
        fail("Invalid target_id")
    if cert.get("parameters") != [99, 14, 1, 2]:
        fail("Invalid parameters")
    summary = cert.get("summary", {})
    if summary.get("total_theorems_certified") != 13:
        fail("Invalid total_theorems_certified")
    if summary.get("total_unsat_proofs") != 26:
        fail("Invalid total_unsat_proofs")
    if summary.get("total_rat_lemmas") != 0:
        fail("Invalid total_rat_lemmas")
    if summary.get("encoding_A_name") != "Sinz_2005_Sequential_Counter":
        fail("Invalid encoding_A_name")
    if summary.get("encoding_B_name") != "Bailleux_Boufkhad_2003_Binary_Tree_Totalizer":
        fail("Invalid encoding_B_name")

    # 1. Positive Non-Vacuity Control on srg(9, 4, 1, 2) = K_3 box K_3
    _, clauses_srg9_A = build_p2_5_srg9_uniqueness("A", add_blocking_clause=False)
    _, clauses_srg9_B = build_p2_5_srg9_uniqueness("B", add_blocking_clause=False)
    if not verify_positive_control_srg9(clauses_srg9_A):
        fail("Positive control srg(9,4,1,2) failed on Encoding A")
    if not verify_positive_control_srg9(clauses_srg9_B):
        fail("Positive control srg(9,4,1,2) failed on Encoding B")
    if summary.get("positive_control_srg_9_4_1_2_encoding_A_sat") is not True:
        fail("Certificate positive_control_srg_9_4_1_2_encoding_A_sat is not True")
    if summary.get("positive_control_srg_9_4_1_2_encoding_B_sat") is not True:
        fail("Certificate positive_control_srg_9_4_1_2_encoding_B_sat is not True")
    print("[PASS] Positive non-vacuity control on srg(9, 4, 1, 2) = K_3 box K_3 (Encoding A & Encoding B)")

    # 2. Verify Track p2 propositions (5 propositions x 2 encodings = 10 proofs)
    p2_builders = {
        "p2_1_inner_matching_k14": lambda enc: build_p2_1_inner_matching(14, enc),
        "p2_2_outer_bijection_k14": lambda enc: build_p2_2_outer_bijection(14, enc),
        "p2_3_inner_outer_balance_k14": lambda enc: build_p2_3_inner_outer_balance(14, enc),
        "p2_4_outer_pair_cn_k14": lambda enc: build_p2_4_outer_pair_cn(enc),
        "p2_5_srg9_uniqueness": lambda enc: build_p2_5_srg9_uniqueness(enc, add_blocking_clause=True),
    }

    p2_props = cert.get("track_p2_forced_structure_reduction", [])
    if len(p2_props) != 5:
        fail("Expected 5 propositions in track_p2_forced_structure_reduction")

    total_core_A = 0
    total_core_B = 0
    total_lrat_A = 0
    total_lrat_B = 0

    for prop in p2_props:
        pid = prop.get("proposition_id")
        if pid not in p2_builders:
            fail(f"Unknown proposition_id {pid}")
        for enc_key, enc_code in [("encoding_A", "A"), ("encoding_B", "B")]:
            ed = prop.get(enc_key, {})
            exp_enc_name = "Sinz_2005_Sequential_Counter" if enc_code == "A" else "Bailleux_Boufkhad_2003_Binary_Tree_Totalizer"
            if ed.get("encoding_name") != exp_enc_name:
                fail(f"{pid} {enc_key}: encoding_name mismatch")
            nvars, clauses = p2_builders[pid](enc_code)
            if ed.get("full_variables") != nvars:
                fail(f"{pid} {enc_key}: full_variables mismatch ({ed.get('full_variables')} vs {nvars})")
            if ed.get("full_clauses") != len(clauses):
                fail(f"{pid} {enc_key}: full_clauses mismatch ({ed.get('full_clauses')} vs {len(clauses)})")
            if ed.get("rat_lemmas") != 0:
                fail(f"{pid} {enc_key}: rat_lemmas must be 0")

            core_cnf_path = os.path.join(proofs_dir, ed.get("core_cnf_file", ""))
            core_drat_path = os.path.join(proofs_dir, ed.get("core_drat_file", ""))
            lrat_files = ed.get("core_lrat_files", [])
            lrat_sha256s = ed.get("core_lrat_sha256s", [])
            if len(lrat_files) != len(lrat_sha256s) or not lrat_files:
                fail(f"{pid} {enc_key}: invalid core_lrat_files")
            lrat_paths = [os.path.join(proofs_dir, fn) for fn in lrat_files]

            if sha256_file(core_cnf_path) != ed.get("core_cnf_sha256"):
                fail(f"{pid} {enc_key}: core_cnf_sha256 mismatch")
            if sha256_file(core_drat_path) != ed.get("core_drat_sha256"):
                fail(f"{pid} {enc_key}: core_drat_sha256 mismatch")
            for lp, lsha in zip(lrat_paths, lrat_sha256s):
                if sha256_file(lp) != lsha:
                    fail(f"{pid} {enc_key}: core_lrat_sha256 mismatch on {os.path.basename(lp)}")

            full_clause_set = set(clauses)
            core_clauses = parse_dimacs_clauses(core_cnf_path)
            for cl in core_clauses:
                if cl not in full_clause_set:
                    fail(f"{pid} {enc_key}: core clause {cl} not in generated CNF")

            try:
                nl = verify_lrat_python(core_clauses, lrat_paths)
            except Exception as e:
                fail(f"{pid} {enc_key}: LRAT verification failed: {e}")

            nc = len(core_clauses)
            if nc != ed.get("core_clauses"):
                fail(f"{pid} {enc_key}: core_clauses mismatch ({nc} vs {ed.get('core_clauses')})")
            if nl != ed.get("lrat_rup_lemmas"):
                fail(f"{pid} {enc_key}: lrat_rup_lemmas mismatch ({nl} vs {ed.get('lrat_rup_lemmas')})")

            if enc_key == "encoding_A":
                total_core_A += nc
                total_lrat_A += nl
            else:
                total_core_B += nc
                total_lrat_B += nl
        print(f"[PASS] Track p2 {pid}: Enc A & Enc B CNF membership + LRAT RUP verified")

    # 3. Verify Track p1 automorphism exclusions (8 cases x 2 encodings = 16 proofs)
    p3_t1_perms = [{(i, s): (((i + step) % 3, s) if i < 3 else (i, s)) for i, s in INNER} for step in range(3)]
    frob21_perms = [{(i, s): (((i * m + sh) % 7, s)) for i, s in INNER} for m in (1, 2, 4) for sh in range(7)]

    p1_specs = {
        "p3_t1_fix33": (p3_t1_perms, 3, "none"),
        "p2_a0_b1_c6_fix73": (make_involution_perms(0, 1, 6), 2, "conj"),
        "p2_a0_b2_c5_fix51": (make_involution_perms(0, 2, 5), 2, "conj_or_fix"),
        "p2_a1_b0_c5_fix53": (make_involution_perms(1, 0, 5), 2, "conj_or_fix"),
        "p2_a0_b4_c3_fix19": (make_involution_perms(0, 4, 3), 2, "conj_or_fix"),
        "p2_a1_b2_c3_fix21": (make_involution_perms(1, 2, 3), 2, "conj_or_fix"),
        "p2_a1_b3_c2_fix11": (make_involution_perms(1, 3, 2), 2, "conj_or_fix"),
        "frob21_z7_z3": (frob21_perms, 7, "frob21_fig10"),
    }

    p1_cases = cert.get("track_p1_automorphism_exclusions", [])
    if len(p1_cases) != 8:
        fail("Expected 8 cases in track_p1_automorphism_exclusions")

    for case in p1_cases:
        cid = case.get("case_id")
        if cid not in p1_specs:
            fail(f"Unknown case_id {cid}")
        perms, prime_p, expected_r4 = p1_specs[cid]
        if case.get("r4_mode") != expected_r4:
            fail(f"{cid}: r4_mode mismatch")
        stats = compute_cycle_stats(perms, prime_p)
        if case.get("cycle_structure") != stats:
            fail(f"{cid}: cycle_structure mismatch")

        for enc_key, enc_code in [("encoding_A", "A"), ("encoding_B", "B")]:
            ed = case.get(enc_key, {})
            exp_enc_name = "Sinz_2005_Sequential_Counter" if enc_code == "A" else "Bailleux_Boufkhad_2003_Binary_Tree_Totalizer"
            if ed.get("encoding_name") != exp_enc_name:
                fail(f"{cid} {enc_key}: encoding_name mismatch")
            n_edge_orbits, n_v_orbits, nvars, clauses = build_automorphism_cnf(perms, encoding=enc_code, r4_mode=expected_r4)
            if ed.get("primary_edge_orbit_variables") != n_edge_orbits:
                fail(f"{cid} {enc_key}: primary_edge_orbit_variables mismatch")
            if ed.get("outer_vertex_orbits") != n_v_orbits:
                fail(f"{cid} {enc_key}: outer_vertex_orbits mismatch")
            if ed.get("full_variables") != nvars:
                fail(f"{cid} {enc_key}: full_variables mismatch ({ed.get('full_variables')} vs {nvars})")
            if ed.get("full_clauses") != len(clauses):
                fail(f"{cid} {enc_key}: full_clauses mismatch ({ed.get('full_clauses')} vs {len(clauses)})")
            if ed.get("rat_lemmas") != 0:
                fail(f"{cid} {enc_key}: rat_lemmas must be 0")

            core_cnf_path = os.path.join(proofs_dir, ed.get("core_cnf_file", ""))
            core_drat_path = os.path.join(proofs_dir, ed.get("core_drat_file", ""))
            lrat_files = ed.get("core_lrat_files", [])
            lrat_sha256s = ed.get("core_lrat_sha256s", [])
            if len(lrat_files) != len(lrat_sha256s) or not lrat_files:
                fail(f"{cid} {enc_key}: invalid core_lrat_files")
            lrat_paths = [os.path.join(proofs_dir, fn) for fn in lrat_files]

            if sha256_file(core_cnf_path) != ed.get("core_cnf_sha256"):
                fail(f"{cid} {enc_key}: core_cnf_sha256 mismatch")
            if sha256_file(core_drat_path) != ed.get("core_drat_sha256"):
                fail(f"{cid} {enc_key}: core_drat_sha256 mismatch")
            for lp, lsha in zip(lrat_paths, lrat_sha256s):
                if sha256_file(lp) != lsha:
                    fail(f"{cid} {enc_key}: core_lrat_sha256 mismatch on {os.path.basename(lp)}")

            full_clause_set = set(clauses)
            core_clauses = parse_dimacs_clauses(core_cnf_path)
            for cl in core_clauses:
                if cl not in full_clause_set:
                    fail(f"{cid} {enc_key}: core clause {cl} not in generated CNF")

            try:
                nl = verify_lrat_python(core_clauses, lrat_paths)
            except Exception as e:
                fail(f"{cid} {enc_key}: LRAT verification failed: {e}")

            nc = len(core_clauses)
            if nc != ed.get("core_clauses"):
                fail(f"{cid} {enc_key}: core_clauses mismatch ({nc} vs {ed.get('core_clauses')})")
            if nl != ed.get("lrat_rup_lemmas"):
                fail(f"{cid} {enc_key}: lrat_rup_lemmas mismatch ({nl} vs {ed.get('lrat_rup_lemmas')})")

            if enc_key == "encoding_A":
                total_core_A += nc
                total_lrat_A += nl
            else:
                total_core_B += nc
                total_lrat_B += nl
        print(f"[PASS] Track p1 {cid}: Enc A & Enc B CNF membership + LRAT RUP verified")

    if total_core_A != summary.get("total_core_clauses_encoding_A"):
        fail("total_core_clauses_encoding_A mismatch")
    if total_core_B != summary.get("total_core_clauses_encoding_B"):
        fail("total_core_clauses_encoding_B mismatch")
    if total_lrat_A != summary.get("total_lrat_rup_lemmas_encoding_A"):
        fail("total_lrat_rup_lemmas_encoding_A mismatch")
    if total_lrat_B != summary.get("total_lrat_rup_lemmas_encoding_B"):
        fail("total_lrat_rup_lemmas_encoding_B mismatch")

    print(
        f"All 26 UNSAT proofs (13 theorems x 2 encodings, {total_lrat_A + total_lrat_B} RUP lemmas, 0 RAT lemmas) verified."
    )
    print("VERIFY: PASS")


if __name__ == "__main__":
    main()
