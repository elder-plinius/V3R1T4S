#!/usr/bin/env python3
"""
Generate and inspect candidate anchored certificates at thresh=0 (and compare Option A vs Option B)
for the certificate package. Uses the C kernel for fast generation; the package's first checker
(verify-it-yourself/check.py) uses only the Python standard library.
"""
import os
import sys
import json
import time
import itertools
from math import lcm
from fractions import Fraction
from collections import Counter
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from neon_global_anchored_probe_r12 import GeneralExponentModel
from neon_exp_ladder_probe_r11 import core_cells, s_counts, geom_batch
from neon_fast_ladder_scan_r11 import geom_multi_off


def surviving_rows(b):
    return tuple(h for h in range(27) if h % 3 != 0 and h % 9 != 1 and h != b)


def xi_list(a):
    r15s = tuple(x for x in range(15) if x % 3 != 0 and x % 5 != 0 and x != a)
    return tuple(itertools.product((1, 2), (1, 2, 3, 4), (2, 4, 5, 7, 8), r15s))


def eval_stage7_coarse_common(mod, state):
    xs, blocks = mod.cell_weight_blocks(state)
    a, b, c, r, j, d, k, i_e, z = state
    assert z == -1
    delta7 = (mod.TAU7 - 1) - mod.W7_ext
    D = lcm(mod.W7_rem.denominator, delta7.denominator)
    w_rem_i = int(mod.W7_rem * D)
    sh_i = -int(delta7 * D)
    zeros = [0] * len(xs)

    u_modes = (False, True) if mod.u_has_pos else (False,)
    tot = Fraction(0)
    blk_stats = {}
    for upos in u_modes:
        u_atoms = mod.u_pos if upos else ((0, Fraction(1)),)
        for vpos in (False, True):
            v_atoms = mod.v_pos if vpos else ((0, Fraction(1)),)
            aw, den_blk = blocks[(upos, vpos)]
            queries = []
            weights = []
            for u, pu in u_atoms:
                for v, pv in v_atoms:
                    queries.append((
                        sh_i,
                        w_rem_i, w_rem_i, D * (1 + u),
                        D * v + w_rem_i, D * v + w_rem_i, D * (1 + v),
                        D * (1 + u) * (1 + v),
                    ))
                    weights.append(pu * pv)
            if queries:
                res = geom_batch(xs, aw, zeros, queries)
                for w_uv, val in zip(weights, res):
                    tot += w_uv * Fraction(val, D * den_blk)
            if mod.u_tail_p > 0 or mod.v_tail_p > 0:
                mx_w = max(aw)
                h_g = []
                for g in (3, 9, 27, 5, 15, 45):
                    d_g = {}
                    for x, w in zip(xs, aw):
                        d_g[x % g] = d_g.get(x % g, 0) + w
                    h_g.append(max(d_g.values()))
                blk_stats[(upos, vpos)] = (den_blk, mx_w, h_g)

    def add_c_tail(upos, vpos, p_u, m_u, p_v, m_v):
        nonlocal tot
        if p_u == 0 or p_v == 0:
            return
        den_blk, mx_w, h_g = blk_stats[(upos, vpos)]
        p_uv = p_u * p_v
        eu1 = p_u + m_u
        ev1 = p_v + m_v
        val = (
            p_uv * mod.W7_rem * (h_g[0] + h_g[1] + h_g[3] + h_g[4])
            + eu1 * p_v * h_g[2]
            + p_u * m_v * (h_g[3] + h_g[4])
            + p_u * ev1 * h_g[5]
            + eu1 * ev1 * mx_w
        ) / den_blk
        tot += val

    if mod.u_tail_p > 0:
        add_c_tail(True, False, mod.u_tail_p, mod.u_tail_m, Fraction(1), Fraction(0))
        vp_sum = sum(pv for _, pv in mod.v_pos)
        vm_sum = sum(v * pv for v, pv in mod.v_pos)
        add_c_tail(True, True, mod.u_tail_p, mod.u_tail_m, vp_sum, vm_sum)
        if mod.v_tail_p > 0:
            add_c_tail(True, True, mod.u_tail_p, mod.u_tail_m, mod.v_tail_p, mod.v_tail_m)
    if mod.v_tail_p > 0:
        add_c_tail(False, True, Fraction(1), Fraction(0), mod.v_tail_p, mod.v_tail_m)
        if mod.u_has_pos:
            up_sum = sum(pu for _, pu in mod.u_pos)
            um_sum = sum(u * pu for u, pu in mod.u_pos)
            add_c_tail(True, True, up_sum, um_sum, mod.v_tail_p, mod.v_tail_m)

    col_full = [
        Fraction(1)
        - (Fraction(1, 5) if x % 5 == c else Fraction(0))
        - (mod.T_budget if x % 5 == j else Fraction(0))
        - ((Fraction(1, 5) - i_e * mod.T_budget) if (d != 0 and x % 3 == d and x % 5 == k) else Fraction(0))
        for x in xs
    ]
    return tot / mod.BETA7, xs, col_full


def eval_stage_multi_fixed_gen(mod, q_idx, xs, blocks, sc, env_unpad, env_kap, mode="15q", m_pin=99, u_pin=2, v_pin=2):
    q = mod.primes_later[q_idx]
    tau_q = mod.taus[q_idx]
    beta_q = mod.betas[q_idx]
    wq = mod.norms[q_idx] / q
    D = lcm(wq.denominator, tau_q.denominator)
    w_i = int(wq * D)
    tau_i = int(tau_q * D)
    n = len(xs)

    r3s = sorted({x % 3 for x in xs})
    r5s = sorted({x % 5 for x in xs})
    r9s = sorted({x % 9 for x in xs})
    r15s = sorted({x % 15 for x in xs})

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
    else:
        raise ValueError(mode)

    n_off = len(offs_list)
    M_tot, W_tot, F_unpad = env_unpad
    M_kap, W_kap, F_kap = env_kap
    dist_p7, mean_p7 = mod.post7[q_idx]
    u_modes = (False, True) if mod.u_has_pos else (False,)

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
    return max(totals) / beta_q


_MOD = None
_MPIN = 4
_UPIN = 2
_VPIN = 2

def _init_w(primes_later, exps, C7, taus_later, U_cut, V_cut, m_pin, u_pin, v_pin):
    global _MOD, _MPIN, _UPIN, _VPIN
    _MOD = GeneralExponentModel(primes_later, exps, C7=C7, taus_later=taus_later, U_cut=U_cut, V_cut=V_cut)
    _MPIN, _UPIN, _VPIN = m_pin, u_pin, v_pin

def _ord_stages(state):
    env = _MOD.eval_ord_envelope(state, xi=None, use_kappa=False)
    L = tuple(
        _MOD.stage_expectation(env, dist, mean, t, mult_scale=1) / b
        for (dist, mean), t, b in zip(_MOD.full, _MOD.taus, _MOD.betas)
    )
    return env, L

def _w_basic(state):
    return state, _MOD.exact_reserve(state), _ord_stages(state)[1]

def _w_coarse(state):
    R = _MOD.exact_reserve(state)
    _, L_ord = _ord_stages(state)
    common, xs, col_full = eval_stage7_coarse_common(_MOD, state)
    fac = _MOD.W7_ext / _MOD.BETA7
    out = []
    for xi in xi_list(state[0]):
        sc = s_counts(xs, xi)
        s_pen = sum(col_full[i] * (sc[i] - 1) for i in range(len(xs)) if sc[i] > 1)
        out.append((xi, (common + fac * s_pen,) + L_ord[1:]))
    return state, R, out

def _w_spatial_group(args):
    state, xis = args
    R = _MOD.exact_reserve(state)
    env_unpad = _MOD.eval_ord_envelope(state, xi=None, use_kappa=False)
    n_p = len(_MOD.primes_later)
    L_jpos = [Fraction(0)]
    for q in range(1, n_p):
        dist_p7, mean_p7 = _MOD.post7[q]
        t_q, b_q = _MOD.taus[q], _MOD.betas[q]
        jpos = Fraction(0)
        used_p = Fraction(0)
        used_m = Fraction(0)
        for j, pj in _MOD.pi7_pos:
            mm = 1 + j
            if mm < t_q:
                jpos += pj * _MOD.stage_expectation(env_unpad, dist_p7, mean_p7, t_q, mult_scale=mm)
                used_p += pj
                used_m += mm * pj
        rem_p = _MOD.C7 / 7 - used_p
        rem_m = (_MOD.mean_1pJ7 - (1 - _MOD.C7 / 7)) - used_m
        if rem_p > 0:
            M_tot, W_tot, _ = env_unpad
            jpos += rem_m * mean_p7 * W_tot - t_q * rem_p * M_tot
        L_jpos.append(jpos / b_q)

    res = []
    for xi in xis:
        l7 = _MOD.eval_stage7_padded(state, xi)
        env_kap = _MOD.eval_ord_envelope(state, xi=xi, use_kappa=True)
        Ls = [l7] + [
            _MOD.stage_expectation(env_kap, _MOD.post7[q][0], _MOD.post7[q][1], _MOD.taus[q], mult_scale=1) / _MOD.betas[q] + L_jpos[q]
            for q in range(1, n_p)
        ]
        res.append((state, xi, R, tuple(Ls)))
    return res

def _w_pin_group(args):
    state, items, mode = args
    xs, blocks = _MOD.cell_weight_blocks(state)
    env_unpad = _MOD.eval_ord_envelope(state, xi=None, use_kappa=False)
    n_p = len(_MOD.primes_later)
    mp = 99 if mode == "15q" else _MPIN
    out = []
    for xi, R, l7 in items:
        sc = s_counts(xs, xi)
        env_kap = _MOD.eval_ord_envelope(state, xi=xi, use_kappa=True)
        Lp = [l7] + [
            eval_stage_multi_fixed_gen(_MOD, qi, xs, blocks, sc, env_unpad, env_kap, mode=mode, m_pin=mp, u_pin=_UPIN, v_pin=_VPIN)
            for qi in range(1, n_p)
        ]
        out.append((state, xi, R, tuple(Lp)))
    return out


def run_cert(name, primes_later, exps, taus_later, C7=Fraction(3, 2), U_cut=8, V_cut=6, m_pin=4, u_pin=2, v_pin=2, thresh=Fraction(0), procs=6, out_json=None):
    t0 = time.time()
    rows = []
    min_m = None
    fails = []

    def rec(phase, key, R, L):
        nonlocal min_m
        S = sum(L)
        m = R - S
        assert m > 0
        rows.append([phase, list(key), str(R), str(S)])
        if min_m is None or m < min_m[0]:
            min_m = (m, phase, list(key), R, L)

    with Pool(procs, initializer=_init_w, initargs=(primes_later, exps, C7, taus_later, U_cut, V_cut, m_pin, u_pin, v_pin)) as pool:
        basic_states = [(a, b, c, -1, j, 0, 0, 0, -1) for a in (1, 2) for b in (2, 4) for c in (a, 3 - a) for j in range(1, 5)]
        groups = {}
        for st, R, L in pool.map(_w_basic, basic_states):
            groups.setdefault(st[:3], []).append((st, R, L))
        rem_abc = []
        for abc, items in sorted(groups.items()):
            if all(R > sum(L) and R >= sum(L) + thresh for _, R, L in items):
                for st, R, L in items:
                    rec("basic", st, R, L)
            elif abc[1] == 2 and all(R + Fraction(1, 5) > sum(L) and R + Fraction(1, 5) >= sum(L) + thresh for _, R, L in items):
                for st, R, L in items:
                    rec("basic75", st, R + Fraction(1, 5), L)
            else:
                rem_abc.append(abc)

        mixed_states = []
        for a, b, c in rem_abc:
            reps = {}
            for r in range(45):
                if r % 3 and r % 9 != 1 and r % 5 and r % 15 != a:
                    reps.setdefault((r % 3, r % 9 == b % 9, r % 5 == a, r % 5 == c), r)
            for r in reps.values():
                for d in (1, 2):
                    for k in range(1, 5):
                        if (d, k) == (a % 3, a % 5):
                            continue
                        for j, i_e in [(jj, 0) for jj in range(1, 5)] + [(k, 1)]:
                            mixed_states.append((a, b, c, r, j, d, k, i_e, -1))
        pending_mixed = []
        for st, R, L in pool.map(_w_basic, mixed_states, chunksize=4):
            if R > sum(L) and R >= sum(L) + thresh:
                rec("mixed", st, R, L)
            else:
                pending_mixed.append(st)

        need_sp = []
        for st, R, out in pool.map(_w_coarse, pending_mixed, chunksize=2):
            for xi, Lc in out:
                if R > sum(Lc) and R >= sum(Lc) + thresh:
                    rec("coarse", st + xi, R, Lc)
                else:
                    need_sp.append((st, xi))

        g_sp = {}
        for st, xi in need_sp:
            g_sp.setdefault(st, []).append(xi)
        need_p3 = []
        for res_list in pool.imap_unordered(_w_spatial_group, sorted(g_sp.items())):
            for st, xi, R, Ls in res_list:
                if R > sum(Ls) and R >= sum(Ls) + thresh:
                    rec("spatial", st + xi, R, Ls)
                else:
                    for z in surviving_rows(st[1]):
                        need_p3.append((st[:-1] + (z,), xi))

        g_p3 = {}
        for st, xi in need_p3:
            g_p3.setdefault(st, []).append(xi)
        need_15 = []
        for res_list in pool.imap_unordered(_w_spatial_group, sorted(g_p3.items())):
            for st, xi, R, Ls in res_list:
                if R > sum(Ls) and R >= sum(Ls) + thresh:
                    rec("pure3", st + xi, R, Ls)
                else:
                    need_15.append((st, xi, R, Ls[0]))

        g_15 = {}
        for st, xi, R, l7 in need_15:
            g_15.setdefault(st, []).append((xi, R, l7))
        need_f4 = []
        if g_15:
            for res_list in pool.imap_unordered(_w_pin_group, [(st, its, "15q") for st, its in sorted(g_15.items())]):
                for st, xi, R, Lp in res_list:
                    if R > sum(Lp) and R >= sum(Lp) + thresh:
                        rec("all15q", st + xi, R, Lp)
                    else:
                        need_f4.append((st, xi, R, Lp[0]))

        g_f4 = {}
        for st, xi, R, l7 in need_f4:
            g_f4.setdefault(st, []).append((xi, R, l7))
        if g_f4:
            for res_list in pool.imap_unordered(_w_pin_group, [(st, its, "fix4") for st, its in sorted(g_f4.items())]):
                for st, xi, R, Lp in res_list:
                    if R > sum(Lp):
                        rec("fix4", st + xi, R, Lp)
                    else:
                        fails.append((st, xi, float(R - sum(Lp))))

    counts = dict(Counter(r[0] for r in rows))
    dt = time.time() - t0
    if fails:
        print(f"[FAIL] {name:16s} | fails={len(fails)} | {counts} | {dt:.1f}s")
        return None
    m, phs, mk, mR, mL = min_m
    tsv_ex = sum(len(r[0]) + len(",".join(map(str, r[1]))) + len(r[2]) + len(r[3]) + 4 for r in rows)
    tsv_12 = sum(len(r[0]) + len(",".join(map(str, r[1]))) + len(r[2]) + 15 + 4 for r in rows)
    print(f"[PASS] {name:16s} | rows={len(rows):5d} | min={float(m):.6f} ({phs:6s}) | ex={tsv_ex/1e6:4.2f}MB c12={tsv_12/1e6:4.2f}MB | {counts} | {dt:.1f}s")
    if out_json:
        with open(out_json, "w") as f:
            json.dump({
                "name": name,
                "primes_later": list(primes_later),
                "exps": list(exps),
                "C7": str(C7),
                "taus_later": [str(t) for t in taus_later],
                "thresh": str(thresh),
                "U_cut": U_cut,
                "V_cut": V_cut,
                "m_pin": m_pin,
                "u_pin": u_pin,
                "v_pin": v_pin,
                "counts": counts,
                "total_rows": len(rows),
                "min_margin": str(m),
                "min_margin_float": float(m),
                "min_phase": phs,
                "min_key": mk,
                "min_R": str(mR),
                "min_L": [str(x) for x in mL],
                "rows": rows,
            }, f, separators=(",", ":"))
    return rows


def main():
    os.makedirs(os.path.join(HERE, "r13_cand"), exist_ok=True)
    P8 = (7, 11, 13, 17, 19, 23)
    P9 = (7, 11, 13, 17, 19, 23, 29)
    P9_no19 = (7, 11, 13, 17, 23, 29, 31)
    cases = [
        ("thmA",          P8,      (None,)*8,                               (4, 4, 7, 8, 12),      10, 8, 4, 2, 2),
        ("w9_no19",       P9_no19, (None,)*9,                               (4, 4, 6, 10, 14, 18),  8, 6, 4, 2, 2),
        ("w9_v3_3",       P9,      (3,)+(None,)*8,                          (4, 4, 8, 8, 12, 16),   8, 6, 4, 2, 2),
        ("w9_v5_2",       P9,      (None, 2)+(None,)*7,                     (4, 4, 6, 8, 12, 16),  11, 2, 4, 2, 2),
        ("w9_v7_1",       P9,      (None, None, 1)+(None,)*6,               (4, 4, 8, 8, 12, 16),   8, 6, 4, 2, 2),
        ("w9_4_3_2",      P9,      (4, 3, 2)+(None,)*6,                     (4, 4, 6, 8, 12, 16),   8, 6, 4, 2, 2),
        ("w9_v11_v13",    P9,      (None, None, None, 1, 1)+(None,)*4,      (4, 4, 6, 8, 12, 16),   8, 6, 4, 2, 2),
        ("w9_v11_v17",    P9,      (None, None, None, 1, None, 1)+(None,)*3,(4, 4, 6, 8, 12, 16),   8, 6, 4, 2, 2),
        ("w9_v13_to_29",  P9,      (None, None, None, None, 1, 1, 1, 1, 1), (4, 4, 6, 8, 12, 16),   8, 6, 4, 2, 2),
    ]
    for name, pl, exps, taus, uc, vc, mp, up, vp in cases:
        run_cert(name, pl, exps, taus, U_cut=uc, V_cut=vc, m_pin=mp, u_pin=up, v_pin=vp, thresh=Fraction(0),
                 out_json=os.path.join(HERE, "r13_cand", f"{name}.json"))


if __name__ == "__main__":
    main()
