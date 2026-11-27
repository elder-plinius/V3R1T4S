#!/usr/bin/env python3
"""
Fast C-backed generator for Theorem A (A8, 8 primes 3..23, all exps = inf)
using ONLY Schroeder's original Phases 1..6 + fixed165 (NO all15q beyond 165, NO fix4!).
Compares (taus, U_cut, V_cut) to find the cleanest, smallest, fastest-to-check A8 certificate.
"""
import os, sys, json, time
from fractions import Fraction
from collections import Counter
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from neon_global_anchored_probe_r12 import GeneralExponentModel
from neon_exp_ladder_probe_r11 import s_counts
from neon_r13_gen_candidates import surviving_rows, xi_list, eval_stage7_coarse_common

_MOD = None

def _init_w(primes_later, exps, C7, taus_later, U_cut, V_cut):
    global _MOD
    _MOD = GeneralExponentModel(primes_later, exps, C7=C7, taus_later=taus_later, U_cut=U_cut, V_cut=V_cut)

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

def _w_fixed165(args):
    state, xi, R, Ls = args
    a = state[0]
    r15s = [x for x in range(15) if x % 3 != 0 and x % 5 != 0 and x != a]
    out = []
    for eta in r15s:
        l11 = _MOD.eval_fixed165(state, xi, eta)
        L_new = (Ls[0], l11) + Ls[2:]
        out.append((state, xi, eta, R, L_new))
    return out


def gen_thmA(name, taus_later, U_cut, V_cut, thresh=Fraction(0), procs=6, save_path=None):
    t0 = time.time()
    P8 = (7, 11, 13, 17, 19, 23)
    exps = (None,) * 8
    C7 = Fraction(3, 2)
    rows = []
    min_m = None
    fails = []

    def rec(phase, key, R, L):
        nonlocal min_m
        S = sum(L)
        m = R - S
        if m <= 0:
            fails.append((phase, key, float(m)))
            return
        rows.append([phase, list(key), str(R), str(S)])
        if min_m is None or m < min_m[0]:
            min_m = (m, phase, list(key), R, L)

    with Pool(procs, initializer=_init_w, initargs=(P8, exps, C7, taus_later, U_cut, V_cut)) as pool:
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
        need_165 = []
        for res_list in pool.imap_unordered(_w_spatial_group, sorted(g_p3.items())):
            for st, xi, R, Ls in res_list:
                if R > sum(Ls) and R >= sum(Ls) + thresh:
                    rec("pure3", st + xi, R, Ls)
                else:
                    need_165.append((st, xi, R, Ls))

        if need_165:
            for out in pool.imap_unordered(_w_fixed165, need_165):
                for st, xi, eta, R, L_new in out:
                    rec("fixed165", st + xi + (eta,), R, L_new)

    counts = dict(Counter(r[0] for r in rows))
    dt = time.time() - t0
    if fails:
        print(f"[FAIL] {name:18s} | fails={len(fails)} worst={min(fails, key=lambda x:x[2])} | {counts} | {dt:.1f}s")
        return None
    m, phs, mk, mR, mL = min_m
    # Sort rows canonically!
    rows.sort(key=lambda r: (r[0], r[1]))
    tsv_ex = sum(len(r[0]) + len(",".join(map(str, r[1]))) + len(r[2]) + len(r[3]) + 4 for r in rows)
    print(f"[PASS] {name:18s} | rows={len(rows):5d} | min={float(m):.6f} ({phs:8s}) | ex={tsv_ex/1e6:4.2f}MB | {counts} | {dt:.1f}s")
    if save_path:
        with open(save_path, "w") as f:
            json.dump({
                "name": name,
                "primes_later": list(P8),
                "exps": [None] * 8,
                "C7": str(C7),
                "taus_later": [str(t) for t in taus_later],
                "U_cut": U_cut,
                "V_cut": V_cut,
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


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "r13_cand"), exist_ok=True)
    for tag, taus, uc, vc in [
        ("A8_t7_U9_V7",  (4, 4, 7, 8, 12), 9, 7),
        ("A8_t8_U10_V7", (4, 4, 8, 8, 12), 10, 7),
        ("A8_t7_U10_V7", (4, 4, 7, 8, 12), 10, 7),
    ]:
        gen_thmA(tag, taus, uc, vc, thresh=Fraction(0),
                 save_path=os.path.join(HERE, "r13_cand", f"{tag}.json"))
