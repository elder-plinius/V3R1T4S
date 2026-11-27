"""
MATSP Final-8 Specialist (charlie/solve_final8.py) — 3-Pronged Attack on the Last 8 Open Targets:
  #23 (B4, +4), #113 (B5, +16), #173 (B4, +40), #98 (B4, +58),
  #168 (B4, +66), #108 (B5, +92), #219 (B6, +244, room=2), #218 (B6, +494).

Three upgrades built specifically for the 0 < ex < A*N flat-excess surplus regime:
  1. Phase 1 Unpruned Lower-Bound Certificate Check (#219, #173, #98, #23):
     Runs 100% unpruned relaxation MIP (zero heuristic pruning) to test if any razor-thin
     target proves bound >= record.
  2. Degeneracy-Broken "Smooth-Excess" Stage 1:
     Replaces the flat slope=1 plateau [Wcap, Wcap+A] with strictly convex micro-slopes
     (1.005, 1.015, 1.025, ...) + hole penalty (5.0 for T < Wcap) + exact work == wmin
     + tiny per-seed tie-break jitter so every seed explores a smooth, distinct shift basin.
  3. Exact O(L * A) Numba Single-Shift Viterbi DP (MAX_BLK=10) + Day Ruin-&-Recreate LNS:
     Computes the globally optimal 1..10-block (>= 4 interval) task partition of any shift in
     ~1 microsecond, plus multi-shift Day Ruin-&-Recreate sweeps and 8-move surplus-squeeze SA.
"""
import argparse
import bisect
import json
import math
import os
import resource
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMBA_NUM_THREADS"] = "1"

CHARLIE_DIR = os.path.dirname(os.path.abspath(__file__))
SCOUT_DIR = os.path.dirname(CHARLIE_DIR)
WINS_DIR = os.path.join(CHARLIE_DIR, "wins")
LOGS_DIR = os.path.join(CHARLIE_DIR, "logs")
JSONL_PATH = os.path.join(LOGS_DIR, "final8.jsonl")
BOUNDS_PATH = os.path.join(LOGS_DIR, "final8_bounds.json")

sys.path.insert(0, CHARLIE_DIR)
sys.path.insert(0, os.path.join(SCOUT_DIR, "code"))

import numpy as np  # noqa: E402
from numba import njit  # noqa: E402
from ortools.linear_solver import pywraplp  # noqa: E402
import matsp  # noqa: E402
import solve_mtask as sm  # noqa: E402
import run_b6  # noqa: E402

MAX_BLK = 10

FINAL_8 = [
    # (iid, stem, rec, lp, s1_s, s2_s, sa_rounds, sa_iters, lpr)
    (23,  "23_7_50_4",     1927,  1905,  45, 110, 44, 10_000_000, 1),
    (113, "113_14_80_6",   6356,  6026,  60, 120, 44, 10_000_000, 0),
    (168, "168_28_40_3",   6000,  5890,  60, 120, 44, 10_000_000, 0),
    (108, "108_14_70_5",   5103,  4947,  60, 120, 44, 10_000_000, 0),
    (98,  "98_14_50_4",    3867,  3855,  60, 120, 44, 10_000_000, 0),
    (173, "173_28_50_4",   7399,  7393,  75, 120, 44, 10_000_000, 0),
    (218, "218_28_140_10", 21729, 19997, 0,  120, 40, 10_000_000, 0),
    (219, "219_28_140_14", 18990, 18988, 0,  120, 36, 8_000_000,  0),
]

CERT_TARGETS = [
    (23,  "23_7_50_4",     1927,  1905),
    (98,  "98_14_50_4",    3867,  3855),
    (173, "173_28_50_4",   7399,  7393),
    (219, "219_28_140_14", 18990, 18988),
]


def _smooth_lp_solve(I, by_day, radius=0, seed=1):
    """
    Degeneracy-broken strictly convex Smooth-Excess continuous LP:
      - Locks total work to [wmin, wmin + 2] (zero surplus waste)
      - Penalizes unused vmax holes T[i] < Wcap[i] by 5.0/unit
      - Micro-steps slope inside [Wcap[i], Wcap[i]+A] by 1.0 + 0.005*(2*k+1) so excess spreads evenly
      - Adds tiny per-seed jitter to diversify shift-envelope basins across seeds.
    """
    rng = np.random.default_rng(seed)
    h, A, N = I["h"], I["A"], I["N"]
    D = h + 1
    nE = len(I["staff"])
    Vmin = [sum(I["vmin"][a][i] for a in range(1, A + 1)) for i in range(N)]
    Wcap = [sum(I["vmax"][a][i] for a in range(1, A + 1)) for i in range(N)]
    wmin = sum(math.ceil(b / 15) for b, c in I["staff"].values())
    wmax = min(wmin + 2, sum(c // 15 for b, c in I["staff"].values()))
    smin = sum(math.ceil(math.ceil(b / 15) / 40) for b, c in I["staff"].values())
    smax = sum(min(D - D // 6, (c // 15) // 24) for b, c in I["staff"].values())

    sv = pywraplp.Solver.CreateSolver("HIGHS")
    obj = sv.Objective()
    obj.SetMinimization()

    c_vars = {}
    start_at_iv = [[] for _ in range(N + 1)]
    end_at_iv = [[] for _ in range(N + 1)]
    end_by_day = [{} for _ in range(D)]
    start_by_day = [{} for _ in range(D)]
    day_totals = []

    work_ct = sv.Constraint(float(wmin), float(wmax))
    sh_ct = sv.Constraint(float(smin), float(smax))

    for d_idx in range(D):
        dv = []
        dc = sv.Constraint(0.0, float(nE)) if by_day[d_idx] else None
        for k, (t, l) in enumerate(by_day[d_idx]):
            v = sv.NumVar(0.0, float(nE), "")
            c_vars[d_idx, k] = v
            dv.append(v)
            work_ct.SetCoefficient(v, float(l))
            sh_ct.SetCoefficient(v, 1.0)
            dc.SetCoefficient(v, 1.0)
            start_at_iv[t].append(v)
            end_at_iv[t + l].append(v)
            end_by_day[d_idx].setdefault(t + l, []).append(v)
            start_by_day[d_idx].setdefault(t, []).append(v)
            # Tiny jitter for seed diversity without distorting optimal excess
            obj.SetCoefficient(v, float(rng.uniform(-0.0004, 0.0004)))
        day_totals.append(dv)

    for d0 in range(0, D - 5):
        ct = sv.Constraint(-sv.infinity(), float(5 * nE))
        for d in range(d0, d0 + 6):
            for v in day_totals[d]:
                ct.SetCoefficient(v, 1.0)

    # Include sparse Hall rest-cutoffs even in LP so rounded envelopes respect 14h rest!
    for d_idx in range(D - 1):
        ends = sorted(end_by_day[d_idx].keys())
        starts = sorted(start_by_day[d_idx + 1].keys())
        if not ends or not starts:
            continue
        suf_end = {}
        prev_v = None
        for U in reversed(ends):
            sv_u = sv.NumVar(0.0, float(nE), "")
            ct = sv.Constraint(0.0, 0.0)
            ct.SetCoefficient(sv_u, 1.0)
            for v in end_by_day[d_idx][U]:
                ct.SetCoefficient(v, -1.0)
            if prev_v is not None:
                ct.SetCoefficient(prev_v, -1.0)
            suf_end[U] = sv_u
            prev_v = sv_u
        pre_st = {}
        prev_v = None
        for T in starts:
            pv_t = sv.NumVar(0.0, float(nE), "")
            ct = sv.Constraint(0.0, 0.0)
            ct.SetCoefficient(pv_t, 1.0)
            for v in start_by_day[d_idx + 1][T]:
                ct.SetCoefficient(v, -1.0)
            if prev_v is not None:
                ct.SetCoefficient(prev_v, -1.0)
            pre_st[T] = pv_t
            prev_v = pv_t
        for U in ends:
            pos = bisect.bisect_left(starts, U + 56) - 1
            if pos < 0:
                continue
            ct = sv.Constraint(-sv.infinity(), float(nE))
            ct.SetCoefficient(suf_end[U], 1.0)
            ct.SetCoefficient(pre_st[starts[pos]], 1.0)
            if pos == len(starts) - 1:
                break

    T_vars = []
    for i in range(N):
        T_i = sv.NumVar(float(Vmin[i]), float(nE), "")
        T_vars.append(T_i)
        dc = sv.Constraint(0.0, 0.0)
        dc.SetCoefficient(T_i, 1.0)
        if i > 0:
            dc.SetCoefficient(T_vars[i - 1], -1.0)
        for v in start_at_iv[i]:
            dc.SetCoefficient(v, -1.0)
        for v in end_at_iv[i]:
            dc.SetCoefficient(v, 1.0)

        cap = Wcap[i]
        # Hole penalty for T[i] < Wcap[i]
        if cap > Vmin[i]:
            hole = sv.NumVar(0.0, float(cap - Vmin[i]), "")
            hct = sv.Constraint(float(cap), sv.infinity())
            hct.SetCoefficient(T_i, 1.0)
            hct.SetCoefficient(hole, 1.0)
            obj.SetCoefficient(hole, 5.0)

        if cap < nE:
            ov = sv.Constraint(-sv.infinity(), float(cap))
            ov.SetCoefficient(T_i, 1.0)
            # First A units: strictly convex micro-slopes 1.005, 1.015, ..., 1 + 0.005*(2*k+1)
            first_a = min(A, nE - cap)
            for k in range(first_a):
                z = sv.NumVar(0.0, 1.0, "")
                ov.SetCoefficient(z, -1.0)
                obj.SetCoefficient(z, 1.0 + 0.005 * (2 * k + 1))
            # Above cap + A: standard quadratic slopes 3, 5, 7, ...
            rem = nE - cap - first_a
            for q in range(1, min(14, (rem + A - 1) // A + 1)):
                ub = float(min(A, rem - (q - 1) * A))
                if ub <= 0:
                    break
                z = sv.NumVar(0.0, ub, "")
                ov.SetCoefficient(z, -1.0)
                obj.SetCoefficient(z, float(2 * q + 1))
            if rem > 13 * A:
                zt = sv.NumVar(0.0, float(rem - 13 * A), "")
                ov.SetCoefficient(zt, -1.0)
                obj.SetCoefficient(zt, 29.0)

    st = sv.Solve()
    if st not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        return by_day, None, None

    pruned = [[] for _ in range(D)]
    rounded = [[] for _ in range(D)]
    for d_idx in range(D):
        keep = set()
        fracs = []
        day_cnt = 0
        for k, (t, l) in enumerate(by_day[d_idx]):
            val = c_vars[d_idx, k].solution_value()
            if val > 1e-6:
                for dt in range(-radius, radius + 1):
                    for dl in range(-radius, radius + 1):
                        keep.add((t + dt, l + dl))
                fl = int(math.floor(val + 1e-9))
                for _ in range(fl):
                    rounded[d_idx].append((t, l))
                day_cnt += fl
                rem = val - fl
                if rem > 1e-6:
                    fracs.append((rem, t, l))
        need_up = min(nE - day_cnt, int(round(sum(x[0] for x in fracs))))
        fracs.sort(key=lambda x: -x[0])
        for _, t, l in fracs[:need_up]:
            rounded[d_idx].append((t, l))
        pruned[d_idx] = [(t, l) for (t, l) in by_day[d_idx] if (t, l) in keep]
        if not pruned[d_idx]:
            pruned[d_idx] = by_day[d_idx]
    return pruned, rounded, int(round(obj.Value()))


def solve_stage1_smooth(I, by_day, secs=60.0, workers=2, lp_radius=0, seed=1):
    """Degeneracy-broken Smooth-Excess Stage 1 (integer MIP on pruned support, or LP-rounded if secs<=0)."""
    h, A, N = I["h"], I["A"], I["N"]
    D = h + 1
    pruned, lp_rounded, lp_val = _smooth_lp_solve(I, by_day, radius=lp_radius, seed=seed)
    if secs <= 0 and lp_rounded is not None:
        return lp_val, lp_val, lp_rounded, "SMOOTH_LP_ROUNDED"

    use_days = pruned if D > 10 else by_day
    nE = len(I["staff"])
    Vmin = [sum(I["vmin"][a][i] for a in range(1, A + 1)) for i in range(N)]
    Wcap = [sum(I["vmax"][a][i] for a in range(1, A + 1)) for i in range(N)]
    wmin = sum(math.ceil(b / 15) for b, c in I["staff"].values())
    wmax = min(wmin + 2, sum(c // 15 for b, c in I["staff"].values()))
    smin = sum(math.ceil(math.ceil(b / 15) / 40) for b, c in I["staff"].values())
    smax = sum(min(D - D // 6, (c // 15) // 24) for b, c in I["staff"].values())

    rng = np.random.default_rng(seed + 7)
    sv = pywraplp.Solver.CreateSolver("HIGHS")
    sv.SetTimeLimit(int(secs * 1000))
    sv.SetNumThreads(int(workers))
    sv.SetSolverSpecificParametersAsString("mip_rel_gap = 0.002")
    obj = sv.Objective()
    obj.SetMinimization()

    c_vars = {}
    start_at_iv = [[] for _ in range(N + 1)]
    end_at_iv = [[] for _ in range(N + 1)]
    end_by_day = [{} for _ in range(D)]
    start_by_day = [{} for _ in range(D)]
    day_totals = []

    work_ct = sv.Constraint(float(wmin), float(wmax))
    sh_ct = sv.Constraint(float(smin), float(smax))

    for d_idx in range(D):
        dv = []
        dc = sv.Constraint(0.0, float(nE)) if use_days[d_idx] else None
        for k, (t, l) in enumerate(use_days[d_idx]):
            v = sv.IntVar(0.0, float(nE), "")
            c_vars[d_idx, k] = v
            dv.append(v)
            work_ct.SetCoefficient(v, float(l))
            sh_ct.SetCoefficient(v, 1.0)
            dc.SetCoefficient(v, 1.0)
            start_at_iv[t].append(v)
            end_at_iv[t + l].append(v)
            end_by_day[d_idx].setdefault(t + l, []).append(v)
            start_by_day[d_idx].setdefault(t, []).append(v)
            obj.SetCoefficient(v, float(rng.uniform(-0.0004, 0.0004)))
        day_totals.append(dv)

    for d0 in range(0, D - 5):
        ct = sv.Constraint(-sv.infinity(), float(5 * nE))
        for d in range(d0, d0 + 6):
            for v in day_totals[d]:
                ct.SetCoefficient(v, 1.0)

    for d_idx in range(D - 1):
        ends = sorted(end_by_day[d_idx].keys())
        starts = sorted(start_by_day[d_idx + 1].keys())
        if not ends or not starts:
            continue
        suf_end = {}
        prev_v = None
        for U in reversed(ends):
            sv_u = sv.NumVar(0.0, float(nE), "")
            ct = sv.Constraint(0.0, 0.0)
            ct.SetCoefficient(sv_u, 1.0)
            for v in end_by_day[d_idx][U]:
                ct.SetCoefficient(v, -1.0)
            if prev_v is not None:
                ct.SetCoefficient(prev_v, -1.0)
            suf_end[U] = sv_u
            prev_v = sv_u
        pre_st = {}
        prev_v = None
        for T in starts:
            pv_t = sv.NumVar(0.0, float(nE), "")
            ct = sv.Constraint(0.0, 0.0)
            ct.SetCoefficient(pv_t, 1.0)
            for v in start_by_day[d_idx + 1][T]:
                ct.SetCoefficient(v, -1.0)
            if prev_v is not None:
                ct.SetCoefficient(prev_v, -1.0)
            pre_st[T] = pv_t
            prev_v = pv_t
        for U in ends:
            pos = bisect.bisect_left(starts, U + 56) - 1
            if pos < 0:
                continue
            ct = sv.Constraint(-sv.infinity(), float(nE))
            ct.SetCoefficient(suf_end[U], 1.0)
            ct.SetCoefficient(pre_st[starts[pos]], 1.0)
            if pos == len(starts) - 1:
                break

    T_vars = []
    for i in range(N):
        T_i = sv.NumVar(float(Vmin[i]), float(nE), "")
        T_vars.append(T_i)
        dc = sv.Constraint(0.0, 0.0)
        dc.SetCoefficient(T_i, 1.0)
        if i > 0:
            dc.SetCoefficient(T_vars[i - 1], -1.0)
        for v in start_at_iv[i]:
            dc.SetCoefficient(v, -1.0)
        for v in end_at_iv[i]:
            dc.SetCoefficient(v, 1.0)
        cap = Wcap[i]
        if cap > Vmin[i]:
            hole = sv.NumVar(0.0, float(cap - Vmin[i]), "")
            hct = sv.Constraint(float(cap), sv.infinity())
            hct.SetCoefficient(T_i, 1.0)
            hct.SetCoefficient(hole, 1.0)
            obj.SetCoefficient(hole, 5.0)
        if cap < nE:
            ov = sv.Constraint(-sv.infinity(), float(cap))
            ov.SetCoefficient(T_i, 1.0)
            first_a = min(A, nE - cap)
            for k in range(first_a):
                z = sv.NumVar(0.0, 1.0, "")
                ov.SetCoefficient(z, -1.0)
                obj.SetCoefficient(z, 1.0 + 0.005 * (2 * k + 1))
            rem = nE - cap - first_a
            for q in range(1, min(14, (rem + A - 1) // A + 1)):
                ub = float(min(A, rem - (q - 1) * A))
                if ub <= 0:
                    break
                z = sv.NumVar(0.0, ub, "")
                ov.SetCoefficient(z, -1.0)
                obj.SetCoefficient(z, float(2 * q + 1))
            if rem > 13 * A:
                zt = sv.NumVar(0.0, float(rem - 13 * A), "")
                ov.SetCoefficient(zt, -1.0)
                obj.SetCoefficient(zt, 29.0)

    st = sv.Solve()
    if st not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        if lp_rounded is not None:
            return lp_val, lp_val, lp_rounded, "SMOOTH_LP_FALLBACK"
        return None, None, None, "NOT_SOLVED"

    shifts_by_day = [[] for _ in range(D)]
    for d_idx in range(D):
        for k, (t, l) in enumerate(use_days[d_idx]):
            cnt = int(round(c_vars[d_idx, k].solution_value()))
            for _ in range(cnt):
                shifts_by_day[d_idx].append((t, l))
    st_name = "SMOOTH_OPT" if st == pywraplp.Solver.OPTIMAL else "SMOOTH_FEAS"
    return int(round(obj.Value())), int(math.ceil(obj.BestBound() - 1e-6)), shifts_by_day, st_name


@njit(cache=True)
def _viterbi_repaint_shift(cov, vmin, vmax, t, L, A, W_HARD, out_ba, out_bl):
    """
    Exact O(L * A) Single-Shift Viterbi DP:
    Given shift [t, t+L) ALREADY REMOVED from cov, finds the globally optimal partition
    into 1..MAX_BLK contiguous task blocks of length >= 4 minimizing W_HARD * ucov + pen.
    Writes blocks to (out_ba, out_bl) and returns (n_blk, delta_ucov, delta_pen).
    """
    INF = 10**15
    # Prefix incremental cost of assigning 1 unit of task a across [t, t+p)
    pref = np.zeros((A, L + 1), dtype=np.int64)
    for a in range(A):
        acc = 0
        for p in range(L):
            i = t + p
            c = cov[a, i]
            du = 0
            dp_ = 0
            if c < vmin[a, i]:
                du = (vmin[a, i] - (c + 1)) ** 2 - (vmin[a, i] - c) ** 2
            if c >= vmax[a, i]:
                dp_ = (c + 1 - vmax[a, i]) ** 2 - (c - vmax[a, i]) ** 2
            acc += W_HARD * du + dp_
            pref[a, p + 1] = acc

    dp = np.full((L + 1, A), INF, dtype=np.int64)
    par_p = np.zeros((L + 1, A), dtype=np.int32)
    par_a = np.full((L + 1, A), -1, dtype=np.int32)

    # Base case p = 4: single block [0, 4) of task a
    for a in range(A):
        dp[4, a] = pref[a, 4]
        par_p[4, a] = 0
        par_a[4, a] = -1

    for p in range(5, L + 1):
        # Precompute best and second-best at p - 4 (if p >= 8)
        b1_val = INF; b1_a = -1
        b2_val = INF; b2_a = -1
        if p >= 8:
            p4 = p - 4
            for a in range(A):
                v = dp[p4, a]
                if v < b1_val:
                    b2_val = b1_val; b2_a = b1_a
                    b1_val = v; b1_a = a
                elif v < b2_val:
                    b2_val = v; b2_a = a

        for a in range(A):
            # Option 1: continue task a from p-1
            best_v = INF
            best_pp = 0
            best_pa = -1
            if dp[p - 1, a] < INF:
                best_v = dp[p - 1, a] + (pref[a, p] - pref[a, p - 1])
                best_pp = par_p[p - 1, a]
                best_pa = par_a[p - 1, a]
            # Option 2: start a new 4-interval block of task a at p-4 from best a' != a
            if p >= 8:
                prev_best = b2_val if b1_a == a else b1_val
                prev_a = b2_a if b1_a == a else b1_a
                if prev_best < INF:
                    cand = prev_best + (pref[a, p] - pref[a, p - 4])
                    if cand < best_v:
                        best_v = cand
                        best_pp = p - 4
                        best_pa = prev_a
            dp[p, a] = best_v
            par_p[p, a] = best_pp
            par_a[p, a] = best_pa

    # Pick best ending task at L
    best_a = 0
    best_v = dp[L, 0]
    for a in range(1, A):
        if dp[L, a] < best_v:
            best_v = dp[L, a]
            best_a = a

    # Backtrack blocks in reverse
    rev_a = np.zeros(MAX_BLK, dtype=np.int32)
    rev_l = np.zeros(MAX_BLK, dtype=np.int32)
    cnt = 0
    cur_p = L
    cur_a = best_a
    while cur_p > 0:
        pp = par_p[cur_p, cur_a]
        pa = par_a[cur_p, cur_a]
        rev_a[cnt] = cur_a
        rev_l[cnt] = cur_p - pp
        cnt += 1
        cur_p = pp
        cur_a = pa

    for k in range(cnt):
        out_ba[k] = rev_a[cnt - 1 - k]
        out_bl[k] = rev_l[cnt - 1 - k]

    # Apply new blocks to cov and return exact (cnt, du, dp)
    du, dp_ = sm._apply_shift_cov(cov, vmin, vmax, t, cnt, out_ba, out_bl, 1)
    return cnt, du, dp_


@njit(cache=True)
def viterbi_sweep_all(sh_t, sh_l, n_blk, blk_a, blk_l, vmin, vmax, W_HARD, n_passes, seed):
    """Run n_passes of randomized-order Exact Viterbi DP coordinate descent across all shifts."""
    np.random.seed(seed)
    nE, D = sh_t.shape
    A, N = vmin.shape
    cov = np.zeros((A, N), dtype=np.int32)
    for e in range(nE):
        for d in range(D):
            if sh_l[e, d] > 0:
                pos = sh_t[e, d]
                for b in range(n_blk[e, d]):
                    a = blk_a[e, d, b]
                    ln = blk_l[e, d, b]
                    for i in range(pos, pos + ln):
                        cov[a, i] += 1
                    pos += ln

    cur_pen = 0; cur_ucov = 0
    for a in range(A):
        for i in range(N):
            c = cov[a, i]
            if c < vmin[a, i]: cur_ucov += (vmin[a, i] - c) ** 2
            elif c > vmax[a, i]: cur_pen += (c - vmax[a, i]) ** 2

    out_ba = np.zeros(MAX_BLK, dtype=np.int32)
    out_bl = np.zeros(MAX_BLK, dtype=np.int32)
    order = np.arange(nE * D, dtype=np.int32)

    for _ in range(n_passes):
        # Fisher-Yates shuffle
        for idx in range(nE * D - 1, 0, -1):
            j = np.random.randint(0, idx + 1)
            tmp = order[idx]; order[idx] = order[j]; order[j] = tmp
        improved = False
        for idx in range(nE * D):
            flat = order[idx]
            e = flat // D
            d = flat % D
            L = sh_l[e, d]
            if L <= 0:
                continue
            t = sh_t[e, d]
            old_nb = n_blk[e, d]
            du1, dp1 = sm._apply_shift_cov(cov, vmin, vmax, t, old_nb, blk_a[e, d], blk_l[e, d], -1)
            new_nb, du2, dp2 = _viterbi_repaint_shift(cov, vmin, vmax, t, L, A, W_HARD, out_ba, out_bl)
            d_obj = W_HARD * (du1 + du2) + (dp1 + dp2)
            if d_obj <= 0:
                n_blk[e, d] = new_nb
                for k in range(new_nb):
                    blk_a[e, d, k] = out_ba[k]
                    blk_l[e, d, k] = out_bl[k]
                cur_ucov += du1 + du2
                cur_pen += dp1 + dp2
                if d_obj < 0:
                    improved = True
            else:
                sm._revert_shift_cov(cov, t, new_nb, out_ba, out_bl, -1)
                sm._revert_shift_cov(cov, t, old_nb, blk_a[e, d], blk_l[e, d], 1)
        if not improved:
            break
    return cur_pen, cur_ucov


@njit(cache=True)
def sa_polish_final8(sh_t_in, sh_l_in, n_blk_in, blk_a_in, blk_l_in,
                     vmin, vmax, min_iv, max_iv, opt_t, opt_l, opt_cnt, start_ok,
                     n_iters, temp_start, temp_end, w_hard, w_surp, seed):
    """
    Final-8 Numba SA with 9 moves (Moves 1-8 + periodic Exact Viterbi Day Ruin-&-Recreate!).
    Uses MAX_BLK = 10.
    """
    np.random.seed(seed)
    nE, D = sh_t_in.shape
    A, N = vmin.shape
    W_HARD = w_hard
    W_SURP = w_surp

    sh_t = sh_t_in.copy(); sh_l = sh_l_in.copy()
    n_blk = n_blk_in.copy(); blk_a = blk_a_in.copy(); blk_l = blk_l_in.copy()

    cov = np.zeros((A, N), dtype=np.int32)
    emp_w = np.zeros(nE, dtype=np.int32)
    for e in range(nE):
        for d in range(D):
            l = sh_l[e, d]
            if l > 0:
                emp_w[e] += l
                pos = sh_t[e, d]
                for b in range(n_blk[e, d]):
                    a = blk_a[e, d, b]; ln = blk_l[e, d, b]
                    for i in range(pos, pos + ln): cov[a, i] += 1
                    pos += ln

    cur_pen = 0; cur_ucov = 0
    for a in range(A):
        for i in range(N):
            c = cov[a, i]
            if c < vmin[a, i]: cur_ucov += (vmin[a, i] - c) ** 2
            elif c > vmax[a, i]: cur_pen += (c - vmax[a, i]) ** 2
    cur_cviol = 0
    for e in range(nE):
        cur_cviol += sm._emp_viol(emp_w[e], min_iv[e], max_iv[e])

    best_feas_pen = 1000000000
    best_t = sh_t.copy(); best_l = sh_l.copy()
    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
    if cur_ucov == 0 and cur_cviol == 0:
        best_feas_pen = cur_pen

    cool = (temp_end / temp_start) ** (1.0 / max(1, n_iters))
    temp = temp_start
    tmp_ba = np.zeros(MAX_BLK, dtype=np.int32)
    tmp_bl = np.zeros(MAX_BLK, dtype=np.int32)
    # Buffers for Day Ruin-&-Recreate (up to 8 shifts)
    K_MAX = 8
    rr_e = np.zeros(K_MAX, dtype=np.int32)
    rr_old_nb = np.zeros(K_MAX, dtype=np.int32)
    rr_old_ba = np.zeros((K_MAX, MAX_BLK), dtype=np.int32)
    rr_old_bl = np.zeros((K_MAX, MAX_BLK), dtype=np.int32)
    rr_new_nb = np.zeros(K_MAX, dtype=np.int32)
    rr_new_ba = np.zeros((K_MAX, MAX_BLK), dtype=np.int32)
    rr_new_bl = np.zeros((K_MAX, MAX_BLK), dtype=np.int32)

    for it in range(n_iters):
        # Every 25,000 iters: Exact Viterbi Day Ruin-&-Recreate on k=4..8 shifts of a random day!
        if it > 0 and (it % 25000 == 0):
            d = np.random.randint(0, D)
            k_pick = 0
            for _try in range(24):
                if k_pick >= 6:
                    break
                e = np.random.randint(0, nE)
                if sh_l[e, d] <= 0:
                    continue
                dup = False
                for q in range(k_pick):
                    if rr_e[q] == e:
                        dup = True; break
                if not dup:
                    rr_e[k_pick] = e
                    k_pick += 1
            if k_pick >= 2:
                du_tot = 0; dp_tot = 0
                for q in range(k_pick):
                    e = rr_e[q]
                    nb_ = n_blk[e, d]
                    rr_old_nb[q] = nb_
                    for b in range(nb_):
                        rr_old_ba[q, b] = blk_a[e, d, b]
                        rr_old_bl[q, b] = blk_l[e, d, b]
                    du1, dp1 = sm._apply_shift_cov(cov, vmin, vmax, sh_t[e, d], nb_, blk_a[e, d], blk_l[e, d], -1)
                    du_tot += du1; dp_tot += dp1
                for q in range(k_pick):
                    e = rr_e[q]
                    nb2, du2, dp2 = _viterbi_repaint_shift(cov, vmin, vmax, sh_t[e, d], sh_l[e, d], A, W_HARD, tmp_ba, tmp_bl)
                    rr_new_nb[q] = nb2
                    for b in range(nb2):
                        rr_new_ba[q, b] = tmp_ba[b]
                        rr_new_bl[q, b] = tmp_bl[b]
                    du_tot += du2; dp_tot += dp2
                d_obj = W_HARD * du_tot + dp_tot
                if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                    for q in range(k_pick):
                        e = rr_e[q]
                        nb2 = rr_new_nb[q]
                        n_blk[e, d] = nb2
                        for b in range(nb2):
                            blk_a[e, d, b] = rr_new_ba[q, b]
                            blk_l[e, d, b] = rr_new_bl[q, b]
                    cur_ucov += du_tot; cur_pen += dp_tot
                    if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                        best_feas_pen = cur_pen
                        best_t = sh_t.copy(); best_l = sh_l.copy()
                        best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
                else:
                    for q in range(k_pick - 1, -1, -1):
                        e = rr_e[q]
                        sm._revert_shift_cov(cov, sh_t[e, d], rr_new_nb[q], rr_new_ba[q], rr_new_bl[q], -1)
                    for q in range(k_pick - 1, -1, -1):
                        e = rr_e[q]
                        sm._revert_shift_cov(cov, sh_t[e, d], rr_old_nb[q], rr_old_ba[q], rr_old_bl[q], 1)

        r = np.random.random()

        if r < 0.04:
            # Move 9: Single-shift Exact Viterbi DP repaint!
            e = np.random.randint(0, nE); d = np.random.randint(0, D)
            L = sh_l[e, d]
            if L <= 0:
                temp *= cool; continue
            t = sh_t[e, d]; old_nb = n_blk[e, d]
            du1, dp1 = sm._apply_shift_cov(cov, vmin, vmax, t, old_nb, blk_a[e, d], blk_l[e, d], -1)
            new_nb, du2, dp2 = _viterbi_repaint_shift(cov, vmin, vmax, t, L, A, W_HARD, tmp_ba, tmp_bl)
            d_ucov = du1 + du2; d_pen = dp1 + dp2
            d_obj = W_HARD * d_ucov + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                n_blk[e, d] = new_nb
                for k in range(new_nb):
                    blk_a[e, d, k] = tmp_ba[k]; blk_l[e, d, k] = tmp_bl[k]
                cur_ucov += d_ucov; cur_pen += d_pen
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
            else:
                sm._revert_shift_cov(cov, t, new_nb, tmp_ba, tmp_bl, -1)
                sm._revert_shift_cov(cov, t, old_nb, blk_a[e, d], blk_l[e, d], 1)

        elif r < 0.22:
            # Move 1: Slide internal task split boundary
            e = np.random.randint(0, nE); d = np.random.randint(0, D)
            nb = n_blk[e, d]
            if nb < 2:
                temp *= cool; continue
            b = np.random.randint(0, nb - 1)
            step = np.random.randint(1, 5)
            if np.random.random() < 0.5: step = -step
            l0, l1 = blk_l[e, d, b], blk_l[e, d, b + 1]
            if l0 + step < 4 or l1 - step < 4:
                temp *= cool; continue
            pos = sh_t[e, d]
            for k in range(b): pos += blk_l[e, d, k]
            bnd = pos + l0
            a0, a1 = blk_a[e, d, b], blk_a[e, d, b + 1]
            if step > 0:
                du1, dp1 = sm._delta_range(cov, vmin, vmax, a1, bnd, bnd + step, -1)
                du2, dp2 = sm._delta_range(cov, vmin, vmax, a0, bnd, bnd + step, 1)
                d_ucov, d_pen = du1 + du2, dp1 + dp2
                d_obj = W_HARD * d_ucov + d_pen
                if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                    blk_l[e, d, b] = l0 + step; blk_l[e, d, b + 1] = l1 - step
                    cur_ucov += d_ucov; cur_pen += d_pen
                    if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                        best_feas_pen = cur_pen
                        best_t = sh_t.copy(); best_l = sh_l.copy()
                        best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
                else:
                    for i in range(bnd, bnd + step):
                        cov[a0, i] -= 1; cov[a1, i] += 1
            else:
                sa_ = -step
                du1, dp1 = sm._delta_range(cov, vmin, vmax, a0, bnd - sa_, bnd, -1)
                du2, dp2 = sm._delta_range(cov, vmin, vmax, a1, bnd - sa_, bnd, 1)
                d_ucov, d_pen = du1 + du2, dp1 + dp2
                d_obj = W_HARD * d_ucov + d_pen
                if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                    blk_l[e, d, b] = l0 + step; blk_l[e, d, b + 1] = l1 - step
                    cur_ucov += d_ucov; cur_pen += d_pen
                    if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                        best_feas_pen = cur_pen
                        best_t = sh_t.copy(); best_l = sh_l.copy()
                        best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
                else:
                    for i in range(bnd - sa_, bnd):
                        cov[a1, i] -= 1; cov[a0, i] += 1

        elif r < 0.32:
            # Move 2: Flip block task ID
            e = np.random.randint(0, nE); d = np.random.randint(0, D)
            nb = n_blk[e, d]
            if nb == 0:
                temp *= cool; continue
            b = np.random.randint(0, nb)
            a_old = blk_a[e, d, b]
            a_new = np.random.randint(0, A - 1)
            if a_new >= a_old: a_new += 1
            pos = sh_t[e, d]
            for k in range(b): pos += blk_l[e, d, k]
            ln = blk_l[e, d, b]
            du1, dp1 = sm._delta_range(cov, vmin, vmax, a_old, pos, pos + ln, -1)
            du2, dp2 = sm._delta_range(cov, vmin, vmax, a_new, pos, pos + ln, 1)
            d_ucov, d_pen = du1 + du2, dp1 + dp2
            d_obj = W_HARD * d_ucov + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                blk_a[e, d, b] = a_new
                n_blk[e, d] = sm._normalize_blocks(nb, blk_a[e, d], blk_l[e, d])
                cur_ucov += d_ucov; cur_pen += d_pen
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
            else:
                for i in range(pos, pos + ln):
                    cov[a_new, i] -= 1; cov[a_old, i] += 1

        elif r < 0.42:
            # Move 3: Split or merge blocks
            e = np.random.randint(0, nE); d = np.random.randint(0, D)
            nb = n_blk[e, d]
            if nb == 0:
                temp *= cool; continue
            if (nb == 1) or (nb < MAX_BLK and np.random.random() < 0.55):
                b = np.random.randint(0, nb)
                ln = blk_l[e, d, b]
                if ln < 8:
                    temp *= cool; continue
                s = np.random.randint(4, ln - 3)
                a_old = blk_a[e, d, b]
                a_new = np.random.randint(0, A - 1)
                if a_new >= a_old: a_new += 1
                pos = sh_t[e, d]
                for k in range(b): pos += blk_l[e, d, k]
                second_half = np.random.random() < 0.5
                i0, i1 = (pos + s, pos + ln) if second_half else (pos, pos + s)
                du1, dp1 = sm._delta_range(cov, vmin, vmax, a_old, i0, i1, -1)
                du2, dp2 = sm._delta_range(cov, vmin, vmax, a_new, i0, i1, 1)
                d_ucov, d_pen = du1 + du2, dp1 + dp2
                d_obj = W_HARD * d_ucov + d_pen
                if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                    for k in range(nb, b + 1, -1):
                        blk_a[e, d, k] = blk_a[e, d, k - 1]; blk_l[e, d, k] = blk_l[e, d, k - 1]
                    if second_half:
                        blk_a[e, d, b] = a_old; blk_l[e, d, b] = s
                        blk_a[e, d, b + 1] = a_new; blk_l[e, d, b + 1] = ln - s
                    else:
                        blk_a[e, d, b] = a_new; blk_l[e, d, b] = s
                        blk_a[e, d, b + 1] = a_old; blk_l[e, d, b + 1] = ln - s
                    n_blk[e, d] = sm._normalize_blocks(nb + 1, blk_a[e, d], blk_l[e, d])
                    cur_ucov += d_ucov; cur_pen += d_pen
                    if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                        best_feas_pen = cur_pen
                        best_t = sh_t.copy(); best_l = sh_l.copy()
                        best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
                else:
                    for i in range(i0, i1):
                        cov[a_new, i] -= 1; cov[a_old, i] += 1
            else:
                b = np.random.randint(0, nb - 1)
                pos = sh_t[e, d]
                for k in range(b): pos += blk_l[e, d, k]
                l0, l1 = blk_l[e, d, b], blk_l[e, d, b + 1]
                a0, a1 = blk_a[e, d, b], blk_a[e, d, b + 1]
                keep_left = np.random.random() < 0.5
                i0, i1, a_from, a_to = (pos + l0, pos + l0 + l1, a1, a0) if keep_left else (pos, pos + l0, a0, a1)
                du1, dp1 = sm._delta_range(cov, vmin, vmax, a_from, i0, i1, -1)
                du2, dp2 = sm._delta_range(cov, vmin, vmax, a_to, i0, i1, 1)
                d_ucov, d_pen = du1 + du2, dp1 + dp2
                d_obj = W_HARD * d_ucov + d_pen
                if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                    blk_a[e, d, b] = a_to; blk_l[e, d, b] = l0 + l1
                    for k in range(b + 1, nb - 1):
                        blk_a[e, d, k] = blk_a[e, d, k + 1]; blk_l[e, d, k] = blk_l[e, d, k + 1]
                    n_blk[e, d] = sm._normalize_blocks(nb - 1, blk_a[e, d], blk_l[e, d])
                    cur_ucov += d_ucov; cur_pen += d_pen
                    if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                        best_feas_pen = cur_pen
                        best_t = sh_t.copy(); best_l = sh_l.copy()
                        best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
                else:
                    for i in range(i0, i1):
                        cov[a_to, i] -= 1; cov[a_from, i] += 1

        elif r < 0.54:
            # Move 8: 2-Employee Same-Day Task-Block Swap
            d = np.random.randint(0, D)
            e1 = np.random.randint(0, nE)
            e2 = np.random.randint(0, nE - 1)
            if e2 >= e1: e2 += 1
            nb1, nb2 = n_blk[e1, d], n_blk[e2, d]
            if nb1 == 0 or nb2 == 0:
                temp *= cool; continue
            b1 = np.random.randint(0, nb1); b2 = np.random.randint(0, nb2)
            a1, a2 = blk_a[e1, d, b1], blk_a[e2, d, b2]
            if a1 == a2:
                temp *= cool; continue
            p1 = sh_t[e1, d]
            for k in range(b1): p1 += blk_l[e1, d, k]
            ln1 = blk_l[e1, d, b1]
            p2 = sh_t[e2, d]
            for k in range(b2): p2 += blk_l[e2, d, k]
            ln2 = blk_l[e2, d, b2]
            du1, dp1 = sm._delta_range(cov, vmin, vmax, a1, p1, p1 + ln1, -1)
            du2, dp2 = sm._delta_range(cov, vmin, vmax, a2, p2, p2 + ln2, -1)
            du3, dp3 = sm._delta_range(cov, vmin, vmax, a2, p1, p1 + ln1, 1)
            du4, dp4 = sm._delta_range(cov, vmin, vmax, a1, p2, p2 + ln2, 1)
            d_ucov = du1 + du2 + du3 + du4; d_pen = dp1 + dp2 + dp3 + dp4
            d_obj = W_HARD * d_ucov + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                blk_a[e1, d, b1] = a2; blk_a[e2, d, b2] = a1
                n_blk[e1, d] = sm._normalize_blocks(nb1, blk_a[e1, d], blk_l[e1, d])
                n_blk[e2, d] = sm._normalize_blocks(nb2, blk_a[e2, d], blk_l[e2, d])
                cur_ucov += d_ucov; cur_pen += d_pen
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
            else:
                for i in range(p2, p2 + ln2): cov[a1, i] -= 1
                for i in range(p1, p1 + ln1): cov[a2, i] -= 1
                for i in range(p2, p2 + ln2): cov[a2, i] += 1
                for i in range(p1, p1 + ln1): cov[a1, i] += 1

        elif r < 0.72:
            # Move 4: Surgical envelope nudge / add / drop (with surplus squeeze)
            e = np.random.randint(0, nE); d = np.random.randint(0, D)
            n_o = opt_cnt[d]
            if n_o == 0:
                temp *= cool; continue
            old_t, old_l, old_nb = sh_t[e, d], sh_l[e, d], n_blk[e, d]
            if old_l > 0 and np.random.random() < 0.08:
                new_t = -1; new_l = 0; new_nb = 0
            elif old_l == 0:
                if not sm._five_in_six_ok(sh_l, e, d, D):
                    temp *= cool; continue
                idx_o = np.random.randint(0, n_o)
                new_t, new_l = opt_t[d, idx_o], opt_l[d, idx_o]
                if not sm._rest_ok(sh_t, sh_l, e, d, new_t, new_l, D):
                    temp *= cool; continue
                new_nb = 1; tmp_ba[0] = np.random.randint(0, A); tmp_bl[0] = new_l
            else:
                sub = np.random.randint(0, 3)
                step = 1 if np.random.random() < 0.75 else 2
                if np.random.random() < 0.5: step = -step
                for k in range(old_nb):
                    tmp_ba[k] = blk_a[e, d, k]; tmp_bl[k] = blk_l[e, d, k]
                new_nb = old_nb
                if sub == 0:
                    new_t = old_t; new_l = old_l + step
                    tmp_bl[new_nb - 1] += step
                    if tmp_bl[new_nb - 1] < 4: temp *= cool; continue
                elif sub == 1:
                    new_t = old_t + step; new_l = old_l
                else:
                    new_t = old_t + step; new_l = old_l - step
                    tmp_bl[0] -= step
                    if tmp_bl[0] < 4: temp *= cool; continue
                if new_l < 24 or new_l > 40 or new_t < 0 or new_t + new_l > N or start_ok[d, new_t] == 0:
                    temp *= cool; continue
                if not sm._rest_ok(sh_t, sh_l, e, d, new_t, new_l, D):
                    temp *= cool; continue

            old_ev = sm._emp_viol(emp_w[e], min_iv[e], max_iv[e])
            new_ew = emp_w[e] - old_l + new_l
            d_cviol = sm._emp_viol(new_ew, min_iv[e], max_iv[e]) - old_ev
            old_surp = emp_w[e] - min_iv[e] if emp_w[e] > min_iv[e] else 0
            new_surp = new_ew - min_iv[e] if new_ew > min_iv[e] else 0
            du1, dp1 = (0, 0)
            if old_l > 0:
                du1, dp1 = sm._apply_shift_cov(cov, vmin, vmax, old_t, old_nb, blk_a[e, d], blk_l[e, d], -1)
            du2, dp2 = (0, 0)
            if new_l > 0:
                du2, dp2 = sm._apply_shift_cov(cov, vmin, vmax, new_t, new_nb, tmp_ba, tmp_bl, 1)
            d_ucov, d_pen = du1 + du2, dp1 + dp2
            d_obj = W_HARD * (d_ucov + d_cviol) + W_SURP * (new_surp - old_surp) + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e, d] = new_t; sh_l[e, d] = new_l; n_blk[e, d] = new_nb
                for k in range(new_nb):
                    blk_a[e, d, k] = tmp_ba[k]; blk_l[e, d, k] = tmp_bl[k]
                emp_w[e] = new_ew; cur_ucov += d_ucov; cur_pen += d_pen; cur_cviol += d_cviol
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
            else:
                if new_l > 0: sm._revert_shift_cov(cov, new_t, new_nb, tmp_ba, tmp_bl, -1)
                if old_l > 0: sm._revert_shift_cov(cov, old_t, old_nb, blk_a[e, d], blk_l[e, d], 1)

        elif r < 0.82:
            # Move 5: 2-employee day swap
            e1 = np.random.randint(0, nE)
            e2 = np.random.randint(0, nE - 1)
            if e2 >= e1: e2 += 1
            d = np.random.randint(0, D)
            t1, l1 = sh_t[e1, d], sh_l[e1, d]; t2, l2 = sh_t[e2, d], sh_l[e2, d]
            if l1 == 0 and l2 == 0: temp *= cool; continue
            if l2 > 0 and l1 == 0 and not sm._five_in_six_ok(sh_l, e1, d, D): temp *= cool; continue
            if l1 > 0 and l2 == 0 and not sm._five_in_six_ok(sh_l, e2, d, D): temp *= cool; continue
            if not sm._rest_ok(sh_t, sh_l, e1, d, t2, l2, D) or not sm._rest_ok(sh_t, sh_l, e2, d, t1, l1, D):
                temp *= cool; continue
            old_ev = sm._emp_viol(emp_w[e1], min_iv[e1], max_iv[e1]) + sm._emp_viol(emp_w[e2], min_iv[e2], max_iv[e2])
            nw1, nw2 = emp_w[e1] - l1 + l2, emp_w[e2] - l2 + l1
            d_cviol = (sm._emp_viol(nw1, min_iv[e1], max_iv[e1]) + sm._emp_viol(nw2, min_iv[e2], max_iv[e2])) - old_ev
            os1 = emp_w[e1] - min_iv[e1] if emp_w[e1] > min_iv[e1] else 0
            os2 = emp_w[e2] - min_iv[e2] if emp_w[e2] > min_iv[e2] else 0
            ns1 = nw1 - min_iv[e1] if nw1 > min_iv[e1] else 0
            ns2 = nw2 - min_iv[e2] if nw2 > min_iv[e2] else 0
            d_obj = W_HARD * d_cviol + W_SURP * ((ns1 + ns2) - (os1 + os2))
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e1, d], sh_t[e2, d] = t2, t1; sh_l[e1, d], sh_l[e2, d] = l2, l1
                nb1, nb2 = n_blk[e1, d], n_blk[e2, d]; n_blk[e1, d], n_blk[e2, d] = nb2, nb1
                for k in range(MAX_BLK):
                    ta = blk_a[e1, d, k]; blk_a[e1, d, k] = blk_a[e2, d, k]; blk_a[e2, d, k] = ta
                    tl = blk_l[e1, d, k]; blk_l[e1, d, k] = blk_l[e2, d, k]; blk_l[e2, d, k] = tl
                emp_w[e1] = nw1; emp_w[e2] = nw2; cur_cviol += d_cviol
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()

        elif r < 0.94:
            # Move 6: Same-employee 2-day length transfer (0 contract delta!)
            e = np.random.randint(0, nE)
            d1 = np.random.randint(0, D); d2 = np.random.randint(0, D - 1)
            if d2 >= d1: d2 += 1
            ot1, ol1, nb1 = sh_t[e, d1], sh_l[e, d1], n_blk[e, d1]
            ot2, ol2, nb2 = sh_t[e, d2], sh_l[e, d2], n_blk[e, d2]
            if ol1 == 0 or ol2 == 0: temp *= cool; continue
            step = 1 if np.random.random() < 0.75 else 2
            end1 = np.random.random() < 0.5; end2 = np.random.random() < 0.5
            if end1:
                nt1, nl1 = ot1, ol1 + step
                i1_0, i1_1, a1_chg = ot1 + ol1, ot1 + ol1 + step, blk_a[e, d1, nb1 - 1]
            else:
                nt1, nl1 = ot1 - step, ol1 + step
                i1_0, i1_1, a1_chg = ot1 - step, ot1, blk_a[e, d1, 0]
            if end2:
                nt2, nl2 = ot2, ol2 - step
                if blk_l[e, d2, nb2 - 1] - step < 4: temp *= cool; continue
                i2_0, i2_1, a2_chg = ot2 + ol2 - step, ot2 + ol2, blk_a[e, d2, nb2 - 1]
            else:
                nt2, nl2 = ot2 + step, ol2 - step
                if blk_l[e, d2, 0] - step < 4: temp *= cool; continue
                i2_0, i2_1, a2_chg = ot2, ot2 + step, blk_a[e, d2, 0]
            if nl1 > 40 or nl2 < 24 or nt1 < 0 or nt1 + nl1 > N or nt2 < 0 or nt2 + nl2 > N:
                temp *= cool; continue
            if start_ok[d1, nt1] == 0 or start_ok[d2, nt2] == 0:
                temp *= cool; continue
            sh_t[e, d1], sh_l[e, d1] = nt1, nl1; sh_t[e, d2], sh_l[e, d2] = nt2, nl2
            ok_r = sm._rest_ok(sh_t, sh_l, e, d1, nt1, nl1, D) and sm._rest_ok(sh_t, sh_l, e, d2, nt2, nl2, D)
            sh_t[e, d1], sh_l[e, d1] = ot1, ol1; sh_t[e, d2], sh_l[e, d2] = ot2, ol2
            if not ok_r: temp *= cool; continue
            du1, dp1 = sm._delta_range(cov, vmin, vmax, a2_chg, i2_0, i2_1, -1)
            du2, dp2 = sm._delta_range(cov, vmin, vmax, a1_chg, i1_0, i1_1, 1)
            d_ucov, d_pen = du1 + du2, dp1 + dp2
            d_obj = W_HARD * d_ucov + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e, d1], sh_l[e, d1] = nt1, nl1; sh_t[e, d2], sh_l[e, d2] = nt2, nl2
                if end1: blk_l[e, d1, nb1 - 1] += step
                else: blk_l[e, d1, 0] += step
                if end2: blk_l[e, d2, nb2 - 1] -= step
                else: blk_l[e, d2, 0] -= step
                cur_ucov += d_ucov; cur_pen += d_pen
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
            else:
                for i in range(i1_0, i1_1): cov[a1_chg, i] -= 1
                for i in range(i2_0, i2_1): cov[a2_chg, i] += 1

        else:
            # Move 7: Cross-day shift move
            e = np.random.randint(0, nE)
            d1 = np.random.randint(0, D); d2 = np.random.randint(0, D)
            if d1 == d2 or sh_l[e, d1] == 0 or sh_l[e, d2] > 0 or opt_cnt[d2] == 0:
                temp *= cool; continue
            old_t, old_l, old_nb = sh_t[e, d1], sh_l[e, d1], n_blk[e, d1]
            sh_l[e, d1] = 0
            if not sm._five_in_six_ok(sh_l, e, d2, D):
                sh_l[e, d1] = old_l; temp *= cool; continue
            idx_o = np.random.randint(0, opt_cnt[d2])
            new_t, new_l = opt_t[d2, idx_o], opt_l[d2, idx_o]
            if not sm._rest_ok(sh_t, sh_l, e, d2, new_t, new_l, D):
                sh_l[e, d1] = old_l; temp *= cool; continue
            sh_l[e, d1] = old_l
            new_nb = 1; tmp_ba[0] = np.random.randint(0, A); tmp_bl[0] = new_l
            old_ev = sm._emp_viol(emp_w[e], min_iv[e], max_iv[e])
            new_ew = emp_w[e] - old_l + new_l
            d_cviol = sm._emp_viol(new_ew, min_iv[e], max_iv[e]) - old_ev
            old_surp = emp_w[e] - min_iv[e] if emp_w[e] > min_iv[e] else 0
            new_surp = new_ew - min_iv[e] if new_ew > min_iv[e] else 0
            du1, dp1 = sm._apply_shift_cov(cov, vmin, vmax, old_t, old_nb, blk_a[e, d1], blk_l[e, d1], -1)
            du2, dp2 = sm._apply_shift_cov(cov, vmin, vmax, new_t, new_nb, tmp_ba, tmp_bl, 1)
            d_ucov, d_pen = du1 + du2, dp1 + dp2
            d_obj = W_HARD * (d_ucov + d_cviol) + W_SURP * (new_surp - old_surp) + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e, d1] = -1; sh_l[e, d1] = 0; n_blk[e, d1] = 0
                sh_t[e, d2] = new_t; sh_l[e, d2] = new_l; n_blk[e, d2] = new_nb
                blk_a[e, d2, 0] = tmp_ba[0]; blk_l[e, d2, 0] = tmp_bl[0]
                emp_w[e] = new_ew; cur_ucov += d_ucov; cur_pen += d_pen; cur_cviol += d_cviol
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
            else:
                sm._revert_shift_cov(cov, new_t, new_nb, tmp_ba, tmp_bl, -1)
                sm._revert_shift_cov(cov, old_t, old_nb, blk_a[e, d1], blk_l[e, d1], 1)

        temp *= cool

    return best_feas_pen, best_t, best_l, best_nb, best_ba, best_bl, cur_ucov, cur_cviol


def solve_final8_one(iid, stem, rec, lp, s1_s, s2_s, sa_rounds, sa_iters, lpr, seed):
    lim = int(6.0 * 1024 * 1024 * 1024)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    I, raw_txt = sm.load_instance(stem)
    A, N = I["A"], I["N"]
    by_day = sm.allowed_shifts_by_day(I)

    # Smooth-Excess Stage 1 (breaks [Wcap, Wcap+A] plateau degeneracy!)
    s1_obj, s1_bd, shifts_by_day, s1_st = solve_stage1_smooth(I, by_day, secs=s1_s, workers=2, lp_radius=lpr, seed=seed)
    t_s1 = round(time.time() - t0, 1)
    if shifts_by_day is None:
        return dict(id=iid, stem=stem, record=rec, lp_bound=lp, s1_st=s1_st, best_pen=None, vs_rec=None, win=False, secs=t_s1)

    t1 = time.time()
    s2_viol, sh_t, sh_l, s2_st = sm.pack_employee_chains(I, shifts_by_day, secs=s2_s, workers=2, seed=seed + 13)
    t_s2 = round(time.time() - t1, 1)

    nE, D = sh_t.shape
    n_blk = np.zeros((nE, D), dtype=np.int32)
    blk_a = np.zeros((nE, D, MAX_BLK), dtype=np.int32)
    blk_l = np.zeros((nE, D, MAX_BLK), dtype=np.int32)
    for e in range(nE):
        for d in range(D):
            if sh_l[e, d] > 0:
                n_blk[e, d] = 1
                blk_a[e, d, 0] = (e + d) % A
                blk_l[e, d, 0] = sh_l[e, d]

    opt_t, opt_l, opt_cnt, start_ok = sm.build_allowed_arrays(I, by_day)
    vmin = np.array([I["vmin"][a] for a in range(1, A + 1)], dtype=np.int32)
    vmax = np.array([I["vmax"][a] for a in range(1, A + 1)], dtype=np.int32)
    E = sorted(I["staff"], key=int)
    min_iv = np.array([math.ceil(I["staff"][e][0] / 15) for e in E], dtype=np.int32)
    max_iv = np.array([I["staff"][e][1] // 15 for e in E], dtype=np.int32)

    # Initial 4-pass Exact Viterbi DP task painting!
    viterbi_sweep_all(sh_t, sh_l, n_blk, blk_a, blk_l, vmin, vmax, 500, 4, seed + 5)

    best_pen = 10**9
    best_t, best_l = sh_t.copy(), sh_l.copy()
    best_nb, best_ba, best_bl = n_blk.copy(), blk_a.copy(), blk_l.copy()
    cur_t, cur_l = sh_t.copy(), sh_l.copy()
    cur_nb, cur_ba, cur_bl = n_blk.copy(), blk_a.copy(), blk_l.copy()

    vit_gain = 0
    for rd in range(sa_rounds):
        w_surp = 4 if rd < (2 * sa_rounds) // 3 else 0
        if rd == 0:
            t_start, t_end, w_hard = 3.0, 0.03, 50
        elif rd == sa_rounds - 1:
            t_start, t_end, w_hard = 1.2, 0.003, 600
        elif rd % 3 == 1:
            t_start, t_end, w_hard = 6.5, 0.03, 45
        elif rd % 3 == 2:
            t_start, t_end, w_hard = 3.0, 0.015, 90
        else:
            t_start, t_end, w_hard = 11.0, 0.04, 45

        fp, bt, bl, bnb, bba, bbl, ucov, cviol = sa_polish_final8(
            cur_t, cur_l, cur_nb, cur_ba, cur_bl,
            vmin, vmax, min_iv, max_iv, opt_t, opt_l, opt_cnt, start_ok,
            int(sa_iters), t_start, t_end, int(w_hard), int(w_surp), int(seed + rd * 997),
        )
        if fp < best_pen:
            best_pen = int(fp)
            best_t, best_l = bt.copy(), bl.copy()
            best_nb, best_ba, best_bl = bnb.copy(), bba.copy(), bbl.copy()

        # Every 6 rounds: run Exact Viterbi DP full-horizon coordinate descent polish!
        if (rd + 1) % 6 == 0 and best_pen < 10**9:
            tnb, tba, tbl = best_nb.copy(), best_ba.copy(), best_bl.copy()
            vp, vu = viterbi_sweep_all(best_t, best_l, tnb, tba, tbl, vmin, vmax, 600, 3, seed + rd * 31)
            if vu == 0 and vp < best_pen:
                vit_gain += (best_pen - int(vp))
                best_pen = int(vp)
                best_nb, best_ba, best_bl = tnb, tba, tbl

        if best_pen < 10**9:
            cur_t, cur_l = best_t.copy(), best_l.copy()
            cur_nb, cur_ba, cur_bl = best_nb.copy(), best_ba.copy(), best_bl.copy()

    # Final Exact Viterbi sweep!
    if best_pen < 10**9:
        tnb, tba, tbl = best_nb.copy(), best_ba.copy(), best_bl.copy()
        vp, vu = viterbi_sweep_all(best_t, best_l, tnb, tba, tbl, vmin, vmax, 600, 5, seed + 99991)
        if vu == 0 and vp < best_pen:
            vit_gain += (best_pen - int(vp))
            best_pen = int(vp)
            best_nb, best_ba, best_bl = tnb, tba, tbl

    valid, verify_line, sha256, win_path = False, "", None, None
    if best_pen < 10**9:
        valid, verify_line, sha256, win_path = sm.save_and_verify_win(
            stem, I, raw_txt, rec, best_pen, best_t, best_l, best_nb, best_ba, best_bl
        )

    surp_iv = int(sum(max(0, int(np.sum(best_l[e])) - int(min_iv[e])) for e in range(len(E)))) if valid else None
    return dict(
        id=iid, stem=stem, record=rec, lp_bound=lp,
        s1_st=s1_st, s1_secs=t_s1, s2_viol=s2_viol, s2_secs=t_s2,
        vit_gain=vit_gain, surp_iv=surp_iv,
        best_pen=best_pen if valid else None,
        vs_rec=(best_pen - rec) if valid else None,
        win=bool(valid and best_pen < rec),
        verify_line=verify_line, sha256=sha256, win_path=win_path,
        secs=round(time.time() - t0, 1),
    )


def run_phase1_bounds():
    """Phase 1: Unpruned mathematically valid lower-bound check on #23, #98, #173, #219."""
    print("\n=== PHASE 1: UNPRUNED LOWER-BOUND CERTIFICATE CHECK (#23, #98, #173, #219) ===", flush=True)
    cert_closed = set()
    rows = []
    for iid, stem, rec, lp in CERT_TARGETS:
        t0 = time.time()
        I, _ = sm.load_instance(stem)
        by_day = sm.allowed_shifts_by_day(I)
        # lp_radius=None -> 100% unpruned relaxation (every valid schedule is feasible!)
        obj, bd, _, st = sm.solve_stage1_mtask_mip(I, by_day, secs=90.0, workers=4, lp_radius=None)
        secs = round(time.time() - t0, 1)
        proved = bool(bd is not None and bd >= rec)
        if proved:
            cert_closed.add(stem)
        row = dict(id=iid, stem=stem, record=rec, old_lp=lp, new_bound=bd, obj=obj, status=st, proved_optimal=proved, secs=secs)
        rows.append(row)
        print(f"  [#{iid:3d} {stem:14s}] old_lp={lp} -> unpruned_bd={bd} (st={st}) vs rec={rec} | PROVED={proved} | {secs}s", flush=True)
    with open(BOUNDS_PATH, "w") as bf:
        bf.write(json.dumps(rows, indent=2) + "\n")
    return cert_closed


def run_one_sub(job, seed):
    iid, stem, rec, lp, s1_s, s2_s, rds, iters, lpr = job
    out_j = os.path.join(LOGS_DIR, f"_f8_{stem}_{seed}_{os.getpid()}.json")
    cmd = [
        sys.executable, "-u", os.path.abspath(__file__),
        "--single", "--id", str(iid), "--stem", stem, "--record", str(rec), "--lp", str(lp),
        "--s1", str(s1_s), "--s2", str(s2_s), "--rounds", str(rds), "--iters", str(iters),
        "--lpr", str(lpr), "--seed", str(seed), "--out-json", out_j,
    ]
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1100, check=False)
        if os.path.exists(out_j):
            r = json.load(open(out_j))
            os.remove(out_j)
            return r
        err = (proc.stderr or proc.stdout or "").strip().splitlines()
        return dict(id=iid, stem=stem, record=rec, lp_bound=lp, best_pen=None, vs_rec=None, win=False,
                    error=(err[-1] if err else f"rc={proc.returncode}")[:120], secs=round(time.time() - t0, 1))
    except Exception as exc:
        if os.path.exists(out_j):
            os.remove(out_j)
        return dict(id=iid, stem=stem, record=rec, lp_bound=lp, best_pen=None, vs_rec=None, win=False,
                    error=repr(exc), secs=round(time.time() - t0, 1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--single", action="store_true")
    parser.add_argument("--id", type=int, default=0)
    parser.add_argument("--stem", type=str, default="")
    parser.add_argument("--record", type=int, default=0)
    parser.add_argument("--lp", type=int, default=0)
    parser.add_argument("--s1", type=float, default=60.0)
    parser.add_argument("--s2", type=float, default=120.0)
    parser.add_argument("--rounds", type=int, default=44)
    parser.add_argument("--iters", type=int, default=10_000_000)
    parser.add_argument("--lpr", type=int, default=0)
    parser.add_argument("--seed", type=int, default=400001)
    parser.add_argument("--out-json", type=str, default="")
    parser.add_argument("--max-hours", type=float, default=2.8)
    args = parser.parse_args()

    os.makedirs(LOGS_DIR, exist_ok=True)
    if args.single:
        r = solve_final8_one(args.id, args.stem, args.record, args.lp,
                             args.s1, args.s2, args.rounds, args.iters, args.lpr, args.seed)
        if args.out_json:
            open(args.out_json, "w").write(json.dumps(r))
        return

    t_start = time.time()
    deadline = t_start + args.max_hours * 3600.0
    print(f"=== FINAL-8 CAMPAIGN START ({time.strftime('%Y-%m-%d %H:%M:%S')}) | Budget: {args.max_hours:.2f}h ===", flush=True)

    # Phase 1: Unpruned lower-bound certificate check (~6m)
    cert_closed = run_phase1_bounds()

    # Phase 2-3: Multi-seed waves (up to 6 seeds per target, immediately skipping any target once won or proved optimal!)
    for wave_idx in range(1, 7):
        if time.time() + 300 >= deadline:
            break
        todo = [
            j for j in FINAL_8
            if (j[1] not in cert_closed) and (not os.path.exists(os.path.join(WINS_DIR, f"{j[1]}.xml")))
        ]
        if not todo:
            print("=== ALL 8 TARGETS RESOLVED!! STOPPING EARLY! ===", flush=True)
            break
        t_w = time.time()
        print(f"\n=== FINAL-8 SEED WAVE {wave_idx}/6 ({len(todo)} open, 2w x 2t) ===", flush=True)
        with ThreadPoolExecutor(max_workers=2) as ex:
            futs = {}
            for j in todo:
                if time.time() >= deadline:
                    break
                seed = 400000 + wave_idx * 10000 + j[0] * 59
                futs[ex.submit(run_one_sub, j, seed)] = j
            for fut in as_completed(futs):
                r = fut.result()
                r["wave"] = f"Final8_Seed_{wave_idx}"
                r["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
                with open(JSONL_PATH, "a") as jf:
                    jf.write(json.dumps(r) + "\n")
                vs = r.get("vs_rec")
                tag = "WIN!!" if r.get("win") else (f"{vs:+d}" if vs is not None else f"ERR({r.get('error', '?')})")
                print(
                    f"  [#{r['id']:3d} {r['stem']:14s}] S1={r.get('s1_st')} ({r.get('s1_secs')}s) | S2v={r.get('s2_viol')} | "
                    f"vit={r.get('vit_gain')} | surp={r.get('surp_iv')} | FINAL={r.get('best_pen')} vs {r['record']} ({tag}) | {r.get('secs')}s",
                    flush=True,
                )
                if r.get("win"):
                    run_b6.rebuild_manifest_all()
        n_wins, tot_d = run_b6.rebuild_manifest_all()
        print(f"=== END SEED WAVE {wave_idx} in {(time.time()-t_w)/60.0:.1f}m | Total verified wins: {n_wins}/123 ({tot_d:+d} pts) ===", flush=True)

    n_wins, tot_d = run_b6.rebuild_manifest_all()
    print(f"\n=== FINAL-8 CAMPAIGN COMPLETE in {(time.time()-t_start)/60.0:.1f}m | Total verified wins: {n_wins}/123 ({tot_d:+d} pts) | Certs: {sorted(cert_closed)} ===", flush=True)


if __name__ == "__main__":
    main()
