#!/usr/bin/env python3
"""
Constructive Symbolic Theorem Prover for Bond Perimeter Polynomial Coefficients
[binom(d, e - m)] D_e(q) (m = 1, 2, 3), extending Mertens & Moore (2018) Theorems 4-6
to m = 3 (Theorem 7: [binom(d, e - 3)] D_e(q)) with zero free parameters or fitting.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from math import factorial
import json
import os
import time


def ipoly_add(A, B):
    if len(A) < len(B):
        A, B = B, A
    out = list(A)
    for i, b in enumerate(B):
        out[i] += b
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def ipoly_mul(A, B):
    out = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        if a:
            for j, b in enumerate(B):
                out[i + j] += a * b
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def ipoly_scale(A, c):
    if c == 0:
        return [0]
    return [x * c for x in A]


def poly_divmod_linear(P, root):
    deg = len(P) - 1
    if deg < 1:
        return [Fraction(0)], P[0]
    q = [Fraction(0)] * deg
    rem = P[deg]
    for i in range(deg - 1, -1, -1):
        q[i] = rem
        rem = P[i] + rem * root
    while len(q) > 1 and q[-1] == 0:
        q.pop()
    return q, rem


def poly_eval(P, x):
    acc = Fraction(0)
    xp = Fraction(1)
    for c in P:
        acc += c * xp
        xp *= x
    return acc


def gen_connected_animals_up_to(r, max_e):
    by_size = {}
    origin = tuple([0] * r)

    def canonicalize(bonds):
        pts = set()
        for u, ax in bonds:
            pts.add(u)
            v = list(u)
            v[ax] += 1
            pts.add(tuple(v))
        mins = [min(p[c] for p in pts) for c in range(r)]
        return tuple(sorted((tuple(u[c] - mins[c] for c in range(r)), ax) for u, ax in bonds))

    cur = {canonicalize([(origin, ax)]) for ax in range(r)}
    by_size[1] = sorted(cur)
    for sz in range(2, max_e + 1):
        nxt = set()
        for animal in cur:
            bset = set(animal)
            pts = set()
            for u, ax in animal:
                pts.add(u)
                v = list(u)
                v[ax] += 1
                pts.add(tuple(v))
            for p in pts:
                for ax in range(r):
                    if (p, ax) not in bset:
                        nxt.add(canonicalize(list(animal) + [(p, ax)]))
                    pm = list(p)
                    pm[ax] -= 1
                    pm = tuple(pm)
                    if (pm, ax) not in bset:
                        nxt.add(canonicalize(list(animal) + [(pm, ax)]))
        cur = nxt
        by_size[sz] = sorted(cur)
    return by_size


def animal_info(r, animal):
    pts = set()
    bset = set(animal)
    ax_cnt = [0] * r
    for u, ax in animal:
        ax_cnt[ax] += 1
        pts.add(u)
        v = list(u)
        v[ax] += 1
        pts.add(tuple(v))
    chords = 0
    for p in pts:
        for ax in range(r):
            q = list(p)
            q[ax] += 1
            q = tuple(q)
            if q in pts and (p, ax) not in bset:
                chords += 1
    e_cnt = len(animal)
    v_cnt = len(pts)
    cyc = e_cnt - v_cnt + 1
    return tuple(sorted(pts)), e_cnt, v_cnt, cyc, chords, tuple(ax_cnt)


def derive_symbolic_formulas(m: int):
    t0 = time.time()
    cores = []
    wtilde_cache = {}

    for r in range(1, m + 1):
        e_R = m + r
        by_sz = gen_connected_animals_up_to(r, e_R)
        all_conn = []
        for sz in range(1, e_R + 1):
            for idx_a, a in enumerate(by_sz[sz]):
                pts, ec, vc, cyc, ch, axc = animal_info(r, a)
                if cyc <= 1:
                    all_conn.append(((r, sz, idx_a), pts, ec, vc, cyc, ch, axc))

        def rec(start_idx, rem_e, rem_cyc, chosen, ax_sum):
            if rem_e == 0:
                if all(c >= 2 for c in ax_sum):
                    cores.append((r, e_R, list(chosen)))
                return
            for idx in range(start_idx, len(all_conn)):
                item = all_conn[idx]
                ec, cyc, axc = item[2], item[4], item[6]
                if ec > rem_e or cyc > rem_cyc:
                    continue
                rec(
                    idx,
                    rem_e - ec,
                    rem_cyc - cyc,
                    chosen + [item],
                    [ax_sum[c] + axc[c] for c in range(r)],
                )

        rec(0, e_R, 1, [], [0] * r)

    M_shift = 3 * m + 2
    DENOM = factorial(m) * factorial(2 * m) * (1 << (2 * m))

    pow_v = {0: [[1]], 1: [[1]]}
    for _ in range(1, M_shift + 2):
        pow_v[0].append(ipoly_mul(pow_v[0][-1], [1, 1]))
        pow_v[1].append(ipoly_mul(pow_v[1][-1], [0, 1]))

    fall_em = {0: [1]}
    for r in range(1, m + 1):
        fall_em[r] = ipoly_mul(fall_em[r - 1], [-m - (r - 1), 1])

    poly_acc = defaultdict(lambda: [0])

    for r, e_R, comp_list in cores:
        c0 = len(comp_list)
        v0 = sum(x[3] for x in comp_list)
        cyc_tot = sum(x[4] for x in comp_list)
        cnts = Counter(x[0] for x in comp_list)
        sym_div = 1
        for c in cnts.values():
            sym_div *= factorial(c)
        base_chords = sum(x[5] for x in comp_list)

        pair_wtilde = {}
        active_edges = []
        for i in range(c0):
            id_i, pts_i = comp_list[i][0], comp_list[i][1]
            for j in range(i + 1, c0):
                id_j, pts_j = comp_list[j][0], comp_list[j][1]
                ckey = (id_i, id_j) if id_i <= id_j else (id_j, id_i)
                if ckey not in wtilde_cache:
                    diff_counts = Counter()
                    for pi in pts_i:
                        for pj in pts_j:
                            diff_counts[tuple(pi[c] - pj[c] for c in range(r))] += 1
                    poly = Counter()
                    for pi in pts_i:
                        for pj in pts_j:
                            ds = diff_counts[tuple(pi[c] - pj[c] for c in range(r))] - 1
                            poly[ds] += 1
                    poly[0] -= len(pts_i) * len(pts_j)
                    wtilde_cache[ckey] = {d: val for d, val in poly.items() if val != 0}
                poly = wtilde_cache[ckey]
                if poly:
                    pair_wtilde[(i, j)] = poly
                    active_edges.append((i, j))

        denom_here = factorial(r) * sym_div * (1 << e_R)
        mult_int = DENOM // denom_here
        v_const = 1 - cyc_tot
        p_pref = ipoly_scale(fall_em[r], mult_int)
        for j in range(1, c0):
            p_pref = ipoly_mul(p_pref, [v_const - v0 + j, 1])

        forest_weights = defaultdict(int)

        def enum_forests(e_idx, parent, cur_poly, num_edges):
            if e_idx == len(active_edges):
                c_prime = c0 - num_edges
                comp_sizes = [0] * c0
                for idx_c in range(c0):
                    root = idx_c
                    while parent[root] != root:
                        root = parent[root]
                    comp_sizes[root] += comp_list[idx_c][3]
                prod_S = 1
                for s_val in comp_sizes:
                    if s_val:
                        prod_S *= s_val
                shift_here = -(v_const + c_prime - v0 - 2)
                extra_pow = M_shift - shift_here
                for ch_d, w_c in cur_poly.items():
                    forest_weights[(extra_pow, base_chords + ch_d)] += prod_S * w_c
                return

            enum_forests(e_idx + 1, parent, cur_poly, num_edges)
            u, w = active_edges[e_idx]
            ru, rw = u, w
            while parent[ru] != ru:
                ru = parent[ru]
            while parent[rw] != rw:
                rw = parent[rw]
            if ru != rw:
                new_parent = list(parent)
                new_parent[rw] = ru
                wpoly = pair_wtilde[(u, w)]
                new_poly = defaultdict(int)
                for d1, c1 in cur_poly.items():
                    for d2, c2 in wpoly.items():
                        new_poly[d1 + d2] += c1 * c2
                enum_forests(e_idx + 1, new_parent, dict(new_poly), num_edges + 1)

        enum_forests(0, list(range(c0)), {0: 1}, 0)

        for (extra_pow, tot_ch), weight in forest_weights.items():
            if weight == 0:
                continue
            term = ipoly_mul(p_pref, ipoly_scale(pow_v[cyc_tot][extra_pow], weight))
            key = (cyc_tot, tot_ch)
            poly_acc[key] = ipoly_add(poly_acc[key], term)

    results = {}
    for key in sorted(poly_acc.keys()):
        Pint = poly_acc[key]
        if Pint == [0]:
            continue
        P = [Fraction(c, DENOM) for c in Pint]
        cyc_tot, ch = key
        root = Fraction(-1 if cyc_tot == 0 else 0)
        shift = M_shift
        while len(P) > 1:
            q, rem = poly_divmod_linear(P, root)
            if rem == 0:
                P = q
                shift -= 1
            else:
                break
        results[key] = (shift, P)
    return results, len(cores), time.time() - t0


def factor_out_small_roots(P):
    """Extract integer linear factors (e - r) for r in 1..6."""
    roots = []
    cur = list(P)
    for r in range(1, 7):
        while len(cur) > 1:
            q, rem = poly_divmod_linear(cur, Fraction(r))
            if rem == 0:
                roots.append(r)
                cur = q
            else:
                break
    return roots, cur


def main():
    for m in [1, 2, 3]:
        res, ncores, dt = derive_symbolic_formulas(m)
        print(f"=== m = {m}: {ncores} canonical cores processed in {dt:.3f}s ===")
        for (cyc, ch), (shift, P) in res.items():
            roots, quot = factor_out_small_roots(P)
            base_s = "(e+1)" if cyc == 0 else "e"
            q_s = f"q^(-{ch})" if cyc == 0 else ("q^(-2d)" if ch == 0 else f"q^(-2d-{ch})")
            rf_s = "".join(f"(e-{r})" for r in roots)
            q_terms = [f"{c.numerator}/{c.denominator}*e^{i}" if c.denominator != 1 else f"{c.numerator}*e^{i}"
                       for i, c in enumerate(quot) if c != 0]
            print(f"  {q_s:10s}: 2^e * {base_s}^(e-{shift}) * {rf_s} * ({' + '.join(reversed(q_terms))})")


if __name__ == "__main__":
    main()
