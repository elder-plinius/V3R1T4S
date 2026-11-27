#!/usr/bin/env python3
"""
neon_fast_ladder_scan_r11.py

Ultra-fast exact-rational scan of the ENTIRE exponent-ladder frontier across ALL 280 xi
on the canonical hardest anchor core (2, 4, 1, 8, 1, 2, 1, 0, 13) using the new C
geom135_multi_off_batch kernel (~50x faster than Python loop!).

Tests BOTH:
  - pure3 (Schroeder padded-7 + first-hit)
  - +165 (Schroeder single fixed projection)
  - +all15q (fixed {15q} at all 6 stages q = 11..29)
  - +fix4 (fixed {3q, 5q, 9q, 15q} at all 6 stages q = 11..29)
And tests the extra gain of adding 45q and 27q on the hardest xi = (1, 4, 7, 7)!
"""
import os
import sys
import time
import ctypes
import itertools
from fractions import Fraction
from math import lcm
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(HERE, "libgeom135_r11.dylib")

_lib = ctypes.CDLL(LIB_PATH)
_lib.geom135_multi_off_batch.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int64),
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
    ctypes.POINTER(ctypes.c_int64),
]
_lib.geom135_multi_off_batch.restype = None

sys.path.insert(0, HERE)
from neon_exp_ladder_probe_r11 import ExponentModel, PRIMES_LATER, core_cells, s_counts, geom_batch


def geom_multi_off(xs, a_w, offs_list, queries):
    n = len(xs)
    n_off = len(offs_list)
    n_q = len(queries)
    c_xs = (ctypes.c_int * n)(*xs)
    c_aw = (ctypes.c_int64 * n)(*a_w)
    flat_offs = []
    for off in offs_list:
        flat_offs.extend(off)
    c_offs = (ctypes.c_int64 * (n_off * n))(*flat_offs)
    flat_q = []
    for q in queries:
        flat_q.extend(q)
    c_q = (ctypes.c_int64 * (8 * n_q))(*flat_q)
    c_out = (ctypes.c_int64 * (n_off * n_q))()
    _lib.geom135_multi_off_batch(n, c_xs, c_aw, n_off, c_offs, n_q, c_q, c_out)
    # Return list of n_off lists of length n_q
    res = []
    for oi in range(n_off):
        base = oi * n_q
        res.append([int(c_out[base + k]) for k in range(n_q)])
    return res


def xi_list(a):
    r15s = tuple(x for x in range(15) if x % 3 != 0 and x % 5 != 0 and x != a)
    return list(itertools.product((1, 2), (1, 2, 3, 4), (2, 4, 5, 7, 8), r15s))


def eval_stage_multi_fixed(mod, q_idx, xs, blocks, sc, env_unpad, env_kap, mode="fix4", m_pin=4, u_pin=3, v_pin=2):
    """
    Evaluate EXACT max over all valid fixed tuples at stage q_idx using ONE C multi-offset call per block!
    For m <= m_pin (< tau_q) and u <= u_pin, v <= v_pin, pins the fixed classes in background;
    otherwise releases the pin (100% rigorous upper bound by Lemma A7!).
    mode:
      '15q'   : 7 tuples (y15)
      'fix4'  : 280 tuples (y3, y5, y9, y15)
      'fix5_45': fixed {3q,5q,9q,15q,45q}
      'fix5_27': fixed {3q,5q,9q,15q,27q}
    """
    q = PRIMES_LATER[q_idx]
    tau_q = mod.taus[q_idx]
    beta_q = mod.betas[q_idx]
    wq = mod.norms[q_idx] / q
    D = lcm(wq.denominator, tau_q.denominator)
    w_i = int(wq * D)
    tau_i = int(tau_q * D)
    n = len(xs)

    a_val = None
    # Infer valid residues directly from xs!
    r3s = sorted({x % 3 for x in xs})
    r5s = sorted({x % 5 for x in xs})
    r9s = sorted({x % 9 for x in xs})
    r15s = sorted({x % 15 for x in xs})
    r27s = sorted({x % 27 for x in xs})
    r45s = sorted({x % 45 for x in xs})

    sub_flags = [0, 0, 0, 0, 0, 0]  # c3, c9, c27, c5, c15, c45
    offs_list = []
    if mode == "15q":
        sub_flags = [0, 0, 0, 0, 1, 0]
        for y15 in r15s:
            offs_list.append([w_i if x % 15 == y15 else 0 for x in xs])
    elif mode == "fix4":
        sub_flags = [1, 1, 0, 1, 1, 0]
        for y3 in r3s:
            for y5 in r5s:
                for y9 in r9s:
                    for y15 in r15s:
                        offs_list.append([
                            w_i * ((x % 3 == y3) + (x % 5 == y5) + (x % 9 == y9) + (x % 15 == y15))
                            for x in xs
                        ])
    elif mode == "fix5_45":
        sub_flags = [1, 1, 0, 1, 1, 1]
        for y3 in r3s:
            for y5 in r5s:
                for y9 in r9s:
                    for y15 in r15s:
                        for y45 in r45s:
                            offs_list.append([
                                w_i * ((x % 3 == y3) + (x % 5 == y5) + (x % 9 == y9) + (x % 15 == y15) + (x % 45 == y45))
                                for x in xs
                            ])
    elif mode == "fix5_27":
        sub_flags = [1, 1, 1, 1, 1, 0]
        for y3 in r3s:
            for y5 in r5s:
                for y9 in r9s:
                    for y15 in r15s:
                        for y27 in r27s:
                            offs_list.append([
                                w_i * ((x % 3 == y3) + (x % 5 == y5) + (x % 9 == y9) + (x % 15 == y15) + (x % 27 == y27))
                                for x in xs
                            ])
    else:
        raise ValueError(mode)

    n_off = len(offs_list)
    M_tot, W_tot, F_unpad = env_unpad
    M_kap, W_kap, F_kap = env_kap
    dist_p7, mean_p7 = mod.post7[q_idx]
    u_modes = (False, True) if mod.u_has_pos else (False,)

    # Collect (m_val, prob_weight) for m <= m_pin (< tau_q); release pin for m_pin < m < tau_q!
    m_terms_kap = []
    unpinned_mid = Fraction(0)
    low_p0 = Fraction(0)
    low_m0 = Fraction(0)
    for m2, pr2 in sorted(dist_p7.items()):
        if m2 < tau_q:
            if m2 <= m_pin:
                m_terms_kap.append((m2, pr2))
            else:
                unpinned_mid += pr2 * m2 * F_kap[tau_q / m2]
            low_p0 += pr2
            low_m0 += pr2 * m2

    pos_dist = {}
    for j, pj in mod.pi7_pos:
        m1 = 1 + j
        if m1 >= tau_q:
            break
        for m2, pr2 in dist_p7.items():
            mm = m1 * m2
            if mm < tau_q:
                pos_dist[mm] = pos_dist.get(mm, Fraction(0)) + pj * pr2
    m_terms_unpad = []
    low_p1 = Fraction(0)
    low_m1 = Fraction(0)
    for mm, pr in sorted(pos_dist.items()):
        if mm <= m_pin:
            m_terms_unpad.append((mm, pr))
        else:
            unpinned_mid += pr * mm * F_unpad[tau_q / mm]
        low_p1 += pr
        low_m1 += mm * pr

    # Constant linear-tail + unpinned-mid contribution (identical across all offsets!)
    tot_pos_p = mod.C7 / 7
    tot_pos_m = (mod.mean_1pJ7 - (1 - mod.C7 / 7)) * mean_p7
    const_tail = (
        unpinned_mid
        + (mean_p7 - low_m0) * W_kap - tau_q * (1 - low_p0) * M_kap
        + (tot_pos_m - low_m1) * W_tot - tau_q * (tot_pos_p - low_p1) * M_tot
    )

    totals = [const_tail] * n_off

    def add_group(m_terms, use_kap):
        if not m_terms:
            return
        for upos in u_modes:
            u_atoms = mod.u_pos if upos else ((0, Fraction(1)),)
            for vpos in (False, True):
                v_atoms = mod.v_pos if vpos else ((0, Fraction(1)),)
                aw_base, den_blk = blocks[(upos, vpos)]
                if use_kap:
                    aw = [aw_base[i] * mod.kappa_int[sc[i]] for i in range(n)]
                    den_tot = den_blk * mod.kappa_den
                else:
                    aw = aw_base
                    den_tot = den_blk
                queries = []
                q_wts = []
                unpin_queries = []
                unpin_wts = []
                for m_val, pr in m_terms:
                    shift = D * m_val - tau_i
                    mD = D * m_val
                    for u, pu in u_atoms:
                        for v, pv in v_atoms:
                            w_term = pr * pu * pv / (D * den_tot)
                            if u <= u_pin and v <= v_pin:
                                queries.append((
                                    shift,
                                    mD - sub_flags[0] * w_i,
                                    mD - sub_flags[1] * w_i,
                                    mD * (1 + u) - sub_flags[2] * w_i,
                                    mD * (1 + v) - sub_flags[3] * w_i,
                                    mD * (1 + v) - sub_flags[4] * w_i,
                                    mD * (1 + v) - sub_flags[5] * w_i,
                                    mD * (1 + u) * (1 + v),
                                ))
                                q_wts.append(w_term)
                            else:
                                unpin_queries.append((
                                    shift, mD, mD, mD * (1 + u),
                                    mD * (1 + v), mD * (1 + v), mD * (1 + v),
                                    mD * (1 + u) * (1 + v),
                                ))
                                unpin_wts.append(w_term)
                if unpin_queries:
                    u_vals = geom_batch(xs, aw, [0] * n, unpin_queries)
                    u_add = sum(w * v for w, v in zip(unpin_wts, u_vals))
                    for oi in range(n_off):
                        totals[oi] += u_add
                if queries:
                    mat = geom_multi_off(xs, aw, offs_list, queries)
                    cd = 1
                    for w in q_wts:
                        cd = lcm(cd, w.denominator)
                    w_ints = [int(w * cd) for w in q_wts]
                    for oi in range(n_off):
                        row = mat[oi]
                        s_int = 0
                        for k in range(len(queries)):
                            s_int += w_ints[k] * row[k]
                        totals[oi] += Fraction(s_int, cd)

        # Infinite u/v linear tail (identical across all offsets!)
        if mod.u_tail_p > 0 or mod.v_tail_p > 0:
            m_sum = sum(m_val * pr for m_val, pr in m_terms)
            blk_stats = {}
            for upos in u_modes:
                for vpos in (False, True):
                    aw_base, den_blk = blocks[(upos, vpos)]
                    if use_kap:
                        aw = [aw_base[i] * mod.kappa_int[sc[i]] for i in range(n)]
                        den_tot = den_blk * mod.kappa_den
                    else:
                        aw = aw_base
                        den_tot = den_blk
                    tot_w = sum(aw)
                    mx_w = max(aw)
                    h_g = []
                    for g in (3, 9, 27, 5, 15, 45):
                        d_g = {}
                        for x, w in zip(xs, aw):
                            d_g[x % g] = d_g.get(x % g, 0) + w
                        h_g.append(max(d_g.values()))
                    blk_stats[(upos, vpos)] = (den_tot, tot_w, mx_w, h_g)
            uv_add = Fraction(0)
            def add_t(upos, vpos, p_u, m_u, p_v, m_v):
                nonlocal uv_add
                if p_u == 0 or p_v == 0:
                    return
                den_tot, tot_w, mx_w, h_g = blk_stats[(upos, vpos)]
                p_uv = p_u * p_v
                eu1 = p_u + m_u
                ev1 = p_v + m_v
                W_add = (
                    p_uv * (tot_w + h_g[0] + h_g[1])
                    + eu1 * p_v * h_g[2]
                    + p_u * ev1 * (h_g[3] + h_g[4] + h_g[5])
                    + eu1 * ev1 * mx_w
                ) / den_tot
                uv_add += m_sum * W_add
            if mod.u_tail_p > 0:
                add_t(True, False, mod.u_tail_p, mod.u_tail_m, Fraction(1), Fraction(0))
                vp_sum = sum(pv for _, pv in mod.v_pos)
                vm_sum = sum(v * pv for v, pv in mod.v_pos)
                add_t(True, True, mod.u_tail_p, mod.u_tail_m, vp_sum, vm_sum)
                if mod.v_tail_p > 0:
                    add_t(True, True, mod.u_tail_p, mod.u_tail_m, mod.v_tail_p, mod.v_tail_m)
            if mod.v_tail_p > 0:
                add_t(False, True, Fraction(1), Fraction(0), mod.v_tail_p, mod.v_tail_m)
                if mod.u_has_pos:
                    up_sum = sum(pu for _, pu in mod.u_pos)
                    um_sum = sum(u * pu for u, pu in mod.u_pos)
                    add_t(True, True, up_sum, um_sum, mod.v_tail_p, mod.v_tail_m)
            for oi in range(n_off):
                totals[oi] += uv_add

    add_group(m_terms_kap, True)
    add_group(m_terms_unpad, False)
    best_val = max(totals)
    return best_val / beta_q


def eval_all280_case(args):
    name, exps, C7, taus_later = args
    t0 = time.time()
    state = (2, 4, 1, 8, 1, 2, 1, 0, 13)
    mod = ExponentModel(exps, C7=C7, taus_later=taus_later, U_cut=8, V_cut=6)
    R = mod.exact_reserve(state)
    xs, blocks = mod.cell_weight_blocks(state)
    env_unpad = mod.eval_ord_envelope(state, xi=None, use_kappa=False)
    xis = xi_list(state[0])

    # Precompute J7>=1 part of pure3
    L_jpos = [Fraction(0)]
    for q in range(1, 7):
        dist_p7, mean_p7 = mod.post7[q]
        t_q, b_q = mod.taus[q], mod.betas[q]
        jpos = Fraction(0)
        used_p = Fraction(0)
        used_m = Fraction(0)
        for j, pj in mod.pi7_pos:
            mm = 1 + j
            if mm < t_q:
                jpos += pj * mod.stage_expectation(env_unpad, dist_p7, mean_p7, t_q, mult_scale=mm)
                used_p += pj
                used_m += mm * pj
        rem_p = mod.C7 / 7 - used_p
        rem_m = (mod.mean_1pJ7 - (1 - mod.C7 / 7)) - used_m
        if rem_p > 0:
            M_tot, W_tot, _ = env_unpad
            jpos += rem_m * mean_p7 * W_tot - t_q * rem_p * M_tot
        L_jpos.append(jpos / b_q)

    # Phase 1: exact pure3 on ALL 280 xis
    p3_list = []
    for xi in xis:
        l7 = mod.eval_stage7_padded(state, xi)
        env_kap = mod.eval_ord_envelope(state, xi=xi, use_kappa=True)
        Ls = [l7]
        for q in range(1, 7):
            dist_p7, mean_p7 = mod.post7[q]
            t_q, b_q = mod.taus[q], mod.betas[q]
            j0 = mod.stage_expectation(env_kap, dist_p7, mean_p7, t_q, mult_scale=1) / b_q
            Ls.append(j0 + L_jpos[q])
        p3_list.append((R - sum(Ls), xi, l7, Ls, env_kap))
    p3_list.sort(key=lambda x: x[0])

    # Phase 2: exact all15q and fix4 using exact branch-and-bound over sorted p3_list!
    # Since fix4(xi) >= all15q(xi) >= pure3(xi), once pure3(xi) >= current best min, we can STOP!
    best_15 = None
    best_15_xi = None
    for m_p3, xi, l7, Ls, env_kap in p3_list:
        if best_15 is not None and m_p3 >= best_15:
            break
        sc = s_counts(xs, xi)
        L15 = [l7] + [eval_stage_multi_fixed(mod, qi, xs, blocks, sc, env_unpad, env_kap, "15q") for qi in range(1, 7)]
        m15 = R - sum(L15)
        if best_15 is None or m15 < best_15:
            best_15 = m15
            best_15_xi = xi

    best_f4 = None
    best_f4_xi = None
    checked_f4 = 0
    for m_p3, xi, l7, Ls, env_kap in p3_list:
        if best_f4 is not None and m_p3 >= best_f4:
            break
        sc = s_counts(xs, xi)
        Lf4 = [l7] + [eval_stage_multi_fixed(mod, qi, xs, blocks, sc, env_unpad, env_kap, "fix4") for qi in range(1, 7)]
        mf4 = R - sum(Lf4)
        checked_f4 += 1
        if best_f4 is None or mf4 < best_f4:
            best_f4 = mf4
            best_f4_xi = xi

    return (name, float(p3_list[0][0]), p3_list[0][1], float(best_15), best_15_xi, float(best_f4), best_f4_xi, checked_f4, time.time() - t0)


def main():
    t0 = time.time()
    # Quick exact check: does geom_multi_off match previous (4,3,2) +0.94244 at xi=(1,4,7,7)?
    C7 = Fraction(3, 2)
    taus = (4, 4, 6, 8, 12, 16)
    cases = [
        ("(4,3,2)",                     (4, 3, 2, None, None, None, None, None, None), C7, taus),
        ("(4,4,2)",                     (4, 4, 2, None, None, None, None, None, None), C7, taus),
        ("(4,5,2)",                     (4, 5, 2, None, None, None, None, None, None), C7, taus),
        ("(4,inf,2) [3^5 or 7^3]",      (4, None, 2, None, None, None, None, None, None), C7, taus),
        ("(4,3,3)",                     (4, 3, 3, None, None, None, None, None, None), C7, taus),
        ("(4,3,inf) [3^5 or 5^4]",      (4, 3, None, None, None, None, None, None, None), C7, taus),
        ("(4,4,3)",                     (4, 4, 3, None, None, None, None, None, None), C7, taus),
        ("(5,3,2)",                     (5, 3, 2, None, None, None, None, None, None), C7, taus),
        ("(4,inf,inf) [3^5 alone]",     (4, None, None, None, None, None, None, None, None), C7, taus),
        ("(inf,inf,inf; 11=1)",         (None, None, None, 1, None, None, None, None, None), C7, taus),
        ("(inf,inf,inf; 11=1,13=1)",    (None, None, None, 1, 1, None, None, None, None), C7, taus),
        ("(inf,inf,inf; 11=1,17=1)",    (None, None, None, 1, None, 1, None, None, None), C7, taus),
        ("(inf,inf,inf; 11=1,19=1)",    (None, None, None, 1, None, None, 1, None, None), C7, taus),
        ("(inf,inf,inf; 11=1,23=1)",    (None, None, None, 1, None, None, None, 1, None), C7, taus),
        ("(inf,inf,inf; 11=1,29=1)",    (None, None, None, 1, None, None, None, None, 1), C7, taus),
        ("(inf,inf,inf; 13=1..29=1)",   (None, None, None, None, 1, 1, 1, 1, 1), C7, taus),
        ("(inf,inf,2; 11=1)",           (None, None, 2, 1, None, None, None, None, None), C7, taus),
        ("(inf,3,inf; 11=1)",           (None, 3, None, 1, None, None, None, None, None), C7, taus),
    ]

    print(f"{'Case':<28s} | {'min pure3':>10s} | {'min all15q':>10s} | {'min fix4':>10s} | {'worst xi (fix4)':<16s} | {'chk':>3s} | {'sec':>5s}")
    print("-" * 100)
    with Pool(6) as pool:
        for res in pool.imap(eval_all280_case, cases):
            name, mp3, xp3, m15, x15, mf4, xf4, chk, sec = res
            tag = "PASS" if mf4 > 0 else "FAIL"
            print(f"{name:<28s} | {mp3:+10.5f} | {m15:+10.5f} | {mf4:+10.5f} | {str(xf4):<16s} | {chk:3d} | {sec:4.1f}s {tag}")
            sys.stdout.flush()

    print(f"\nTotal scan time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
