"""
MATSP Multi-Task Solver (charlie/solve_mtask.py) — 4-Stage Architecture for A >= 2 (B3 & B4):
  Stage 1: Symmetry-free Sparse HiGHS Aggregate Envelope + Aggregate 1h-Block MIP
           (O(1)-nonzero difference-array coverage, sparse Hall rest cutoffs, 5-in-6,
            aggregate 4-interval minimum-run inequalities, LP-support pruning on D > 10).
  Stage 2: Fast Employee Chain Packer (CP-SAT + greedy fallback) threading Stage 1's
           daily shift envelopes into |E| individual schedules (14h rest, 5-in-6, [min, max]).
  Stage 3: Global Within-Shift Task-Block Partitioner (HiGHS) painting fixed shift
           envelopes into valid >= 4-interval (1h) task blocks across all employees at once.
  Stage 4: Ultra-fast Multi-Task Numba O(1) Delta-Eval Simulated Annealing (7 move types:
           task split-slide, block flip, split/merge block, surgical envelope nudge/add/drop,
           2-emp day swap, same-emp 2-day length transfer, cross-day move) + mid-run Stage 3 LNS.

Writes verified wins (< record, 0 violations, verify_claim.py PASS) to charlie/wins/<stem>.xml
with monotonic-best protection. Does NOT modify any existing scout files, runs/, or outbox/.
"""
import argparse
import bisect
import hashlib
import json
import math
import os
import resource
import subprocess
import sys
import time
import zipfile
from concurrent.futures import ProcessPoolExecutor, as_completed

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMBA_NUM_THREADS"] = "1"

CHARLIE_DIR = os.path.dirname(os.path.abspath(__file__))
SCOUT_DIR = os.path.dirname(CHARLIE_DIR)
ZIP_PATH = os.path.join(SCOUT_DIR, "raw/instances1_225.zip")
VERIFY_SCRIPT = os.path.join(SCOUT_DIR, "claimkit/verify_claim.py")
WINS_DIR = os.path.join(CHARLIE_DIR, "wins")
LOGS_DIR = os.path.join(CHARLIE_DIR, "logs")

sys.path.insert(0, os.path.join(SCOUT_DIR, "code"))

import numpy as np  # noqa: E402
from numba import njit  # noqa: E402
from ortools.linear_solver import pywraplp  # noqa: E402
from ortools.sat.python import cp_model  # noqa: E402
import matsp  # noqa: E402

MAX_BLK = 6

# B3: 18 Medium A=2 instances (30-60 staff)
B3_7_14_TARGETS = [
    (12, "12_7_30_2", 1375, 1217),
    (13, "13_7_30_2", 1283, 1148),
    (16, "16_7_40_2", 1486, 1291),
    (17, "17_7_40_2", 1563, 1374),
    (21, "21_7_50_2", 1461, 1263),
    (26, "26_7_60_2", 1490, 1287),
    (87, "87_14_30_2", 2397, 2176),
    (88, "88_14_30_2", 2337, 2138),
    (91, "91_14_40_2", 3080, 2672),
    (92, "92_14_40_2", 3342, 2896),
    (96, "96_14_50_2", 3184, 2758),
    (101, "101_14_60_2", 3125, 2734),
]

B3_28_TARGETS = [
    (162, "162_28_30_2", 4937, 4432),
    (163, "163_28_30_2", 4896, 4458),
    (166, "166_28_40_2", 6467, 5534),
    (167, "167_28_40_2", 6455, 5603),
    (171, "171_28_50_2", 6207, 5335),
    (176, "176_28_60_2", 6233, 5427),
]

# B4: 5 Counting-Tight Snipers + 9 Wide (A=3..4, 40-60 staff)
B4_TIGHT_TARGETS = [
    (23, "23_7_50_4", 1927, 1905),
    (93, "93_14_40_3", 2988, 2926),
    (98, "98_14_50_4", 3867, 3855),
    (168, "168_28_40_3", 6000, 5890),
    (173, "173_28_50_4", 7399, 7393),
]

B4_WIDE_TARGETS = [
    (22, "22_7_50_3", 2424, 2054),
    (27, "27_7_60_3", 2402, 1944),
    (28, "28_7_60_4", 2582, 2172),
    (97, "97_14_50_3", 4066, 3442),
    (102, "102_14_60_3", 4807, 3948),
    (103, "103_14_60_4", 5412, 4482),
    (172, "172_28_50_3", 8164, 6954),
    (177, "177_28_60_3", 9343, 7608),
    (178, "178_28_60_4", 11590, 9406),
]

ALL_B3_B4 = B3_7_14_TARGETS + B3_28_TARGETS + B4_TIGHT_TARGETS + B4_WIDE_TARGETS


def load_instance(stem):
    with zipfile.ZipFile(ZIP_PATH) as zf:
        txt = zf.read(f"instances1_225/txt/{stem}.txt").decode("utf-8")
    return matsp.read_instance(txt), txt


def allowed_shifts_by_day(I):
    h, N = I["h"], I["N"]
    idx = lambda d, m: (d - 1) * 96 + m // 15 - 24
    by_day = []
    for d in range(1, h + 2):
        shs = []
        for s0 in range(0, 1440, 15):
            if not matsp.allowed_start(d, s0, h):
                continue
            t = idx(d, s0)
            if t < 0:
                continue
            for l in range(24, 41):
                if t + l <= N:
                    shs.append((t, l))
        by_day.append(shs)
    return by_day


def _lp_prune_shifts_mtask(I, by_day, radius=1):
    """Fast continuous aggregate LP (with bound2-style convex cost) to prune shift support on D > 10."""
    h, A, N = I["h"], I["A"], I["N"]
    D = h + 1
    nE = len(I["staff"])
    Vmin = [sum(I["vmin"][a][i] for a in range(1, A + 1)) for i in range(N)]
    Wcap = [sum(I["vmax"][a][i] for a in range(1, A + 1)) for i in range(N)]
    wmin = sum(math.ceil(b / 15) for b, c in I["staff"].values())
    wmax = sum(c // 15 for b, c in I["staff"].values())
    smin = sum(math.ceil(math.ceil(b / 15) / 40) for b, c in I["staff"].values())
    smax = sum(min(D - D // 6, (c // 15) // 24) for b, c in I["staff"].values())

    sv = pywraplp.Solver.CreateSolver("HIGHS")
    c_vars = {}
    start_at_iv = [[] for _ in range(N + 1)]
    end_at_iv = [[] for _ in range(N + 1)]
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
        day_totals.append(dv)

    for d0 in range(0, D - 5):
        ct = sv.Constraint(-sv.infinity(), float(5 * nE))
        for d in range(d0, d0 + 6):
            for v in day_totals[d]:
                ct.SetCoefficient(v, 1.0)

    obj = sv.Objective()
    obj.SetMinimization()
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
        if cap < nE:
            # Exact convex piecewise-linear cost of spreading excess across A tasks
            # Marginal cost of the (e+1)-th unit of excess is 2*(e // A) + 1
            max_ex = min(nE - cap, 14 * A)
            ov = sv.Constraint(-sv.infinity(), float(cap))
            ov.SetCoefficient(T_i, 1.0)
            for q in range(0, (max_ex + A - 1) // A):
                ub = float(min(A, max_ex - q * A))
                z = sv.NumVar(0.0, ub, "")
                ov.SetCoefficient(z, -1.0)
                obj.SetCoefficient(z, float(2 * q + 1))
            if nE - cap > max_ex:
                zt = sv.NumVar(0.0, float(nE - cap - max_ex), "")
                ov.SetCoefficient(zt, -1.0)
                obj.SetCoefficient(zt, float(2 * (max_ex // A) + 1))

    st = sv.Solve()
    if st not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        return by_day, None, None
    lp_val = int(math.ceil(obj.Value() - 1e-6))
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
        # Round up top fractional shifts up to sum(frac) without exceeding nE
        need_up = min(nE - day_cnt, int(round(sum(x[0] for x in fracs))))
        fracs.sort(key=lambda x: -x[0])
        for _, t, l in fracs[:need_up]:
            rounded[d_idx].append((t, l))
        pruned[d_idx] = [(t, l) for (t, l) in by_day[d_idx] if (t, l) in keep]
        if not pruned[d_idx]:
            pruned[d_idx] = by_day[d_idx]
    return pruned, rounded, lp_val


def solve_stage1_mtask_mip(I, by_day, secs=45.0, workers=2, lp_radius=1):
    """
    Stage 1: Sparse HiGHS Aggregate Shift-Envelope + Aggregate 1h-Block MIP.
    If secs <= 0 or MIP times out on 28d XL, falls back cleanly to LP-rounded shift counts!
    Returns (s1_obj, s1_bound, shifts_by_day, status_name).
    """
    h, A, N = I["h"], I["A"], I["N"]
    D = h + 1
    lp_rounded = None
    lp_val = None
    if D > 10 and lp_radius is not None:
        by_day, lp_rounded, lp_val = _lp_prune_shifts_mtask(I, by_day, radius=lp_radius)
    elif secs <= 0:
        _, lp_rounded, lp_val = _lp_prune_shifts_mtask(I, by_day, radius=0)

    if secs <= 0 and lp_rounded is not None:
        return lp_val, lp_val, lp_rounded, "LP_ROUNDED"

    nE = len(I["staff"])
    Vmin = [sum(I["vmin"][a][i] for a in range(1, A + 1)) for i in range(N)]
    wmin = sum(math.ceil(b / 15) for b, c in I["staff"].values())
    wmax = sum(c // 15 for b, c in I["staff"].values())
    smin = sum(math.ceil(math.ceil(b / 15) / 40) for b, c in I["staff"].values())
    smax = sum(min(D - D // 6, (c // 15) // 24) for b, c in I["staff"].values())

    sv = pywraplp.Solver.CreateSolver("HIGHS")
    sv.SetTimeLimit(int(secs * 1000))
    sv.SetNumThreads(int(workers))
    sv.SetSolverSpecificParametersAsString("mip_rel_gap = 0.003")

    c_vars = {}
    day_totals = []
    start_at_iv = [[] for _ in range(N + 1)]
    end_at_iv = [[] for _ in range(N + 1)]
    end_by_day = [{} for _ in range(D)]
    start_by_day = [{} for _ in range(D)]

    work_ct = sv.Constraint(float(wmin), float(wmax))
    sh_ct = sv.Constraint(float(smin), float(smax))

    for d_idx in range(D):
        d_vars = []
        d_ct = sv.Constraint(0.0, float(nE)) if by_day[d_idx] else None
        for k, (t, l) in enumerate(by_day[d_idx]):
            v = sv.IntVar(0.0, float(nE), "")
            c_vars[d_idx, k] = v
            d_vars.append(v)
            work_ct.SetCoefficient(v, float(l))
            sh_ct.SetCoefficient(v, 1.0)
            d_ct.SetCoefficient(v, 1.0)
            start_at_iv[t].append(v)
            end_at_iv[t + l].append(v)
            end_by_day[d_idx].setdefault(t + l, []).append(v)
            start_by_day[d_idx].setdefault(t, []).append(v)
        day_totals.append(d_vars)

    # 5-in-6 aggregate bound
    for d0 in range(0, D - 5):
        ct = sv.Constraint(-sv.infinity(), float(5 * nE))
        for d in range(d0, d0 + 6):
            for v in day_totals[d]:
                ct.SetCoefficient(v, 1.0)

    # Sparse exact Hall Marriage rest-cutoff inequalities
    for d_idx in range(D - 1):
        ends = sorted(end_by_day[d_idx].keys())
        starts = sorted(start_by_day[d_idx + 1].keys())
        if not ends or not starts:
            continue
        suf_end = {}
        prev_var = None
        for U in reversed(ends):
            s_var = sv.NumVar(0.0, float(nE), "")
            ct = sv.Constraint(0.0, 0.0)
            ct.SetCoefficient(s_var, 1.0)
            for v in end_by_day[d_idx][U]:
                ct.SetCoefficient(v, -1.0)
            if prev_var is not None:
                ct.SetCoefficient(prev_var, -1.0)
            suf_end[U] = s_var
            prev_var = s_var

        pre_st = {}
        prev_var = None
        for T in starts:
            p_var = sv.NumVar(0.0, float(nE), "")
            ct = sv.Constraint(0.0, 0.0)
            ct.SetCoefficient(p_var, 1.0)
            for v in start_by_day[d_idx + 1][T]:
                ct.SetCoefficient(v, -1.0)
            if prev_var is not None:
                ct.SetCoefficient(prev_var, -1.0)
            pre_st[T] = p_var
            prev_var = p_var

        for U in ends:
            pos = bisect.bisect_left(starts, U + 56) - 1
            if pos < 0:
                continue
            T_hi = starts[pos]
            ct = sv.Constraint(-sv.infinity(), float(nE))
            ct.SetCoefficient(suf_end[U], 1.0)
            ct.SetCoefficient(pre_st[T_hi], 1.0)
            if pos == len(starts) - 1:
                break

    # Difference-array total staff on duty T[i]
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

    # Aggregate task coverage C[a, i] + aggregate 4-interval minimum-run inequalities + y^2 cost
    obj = sv.Objective()
    obj.SetMinimization()
    C_vars = [[None] * N for _ in range(A)]
    st_vars = [[None] * N for _ in range(A)]

    for i in range(N):
        sum_ct = sv.Constraint(0.0, 0.0)
        sum_ct.SetCoefficient(T_vars[i], -1.0)
        for a0 in range(A):
            a = a0 + 1
            vmin_ai = I["vmin"][a][i]
            vmax_ai = I["vmax"][a][i]
            c_ai = sv.NumVar(float(vmin_ai), float(nE), "")
            C_vars[a0][i] = c_ai
            sum_ct.SetCoefficient(c_ai, 1.0)

            # st_a[a0, i] >= C[a0, i] - C[a0, i-1] for i >= 1
            if i >= 1:
                s_ai = sv.NumVar(0.0, float(nE), "")
                st_vars[a0][i] = s_ai
                sct = sv.Constraint(-sv.infinity(), 0.0)
                sct.SetCoefficient(c_ai, 1.0)
                sct.SetCoefficient(C_vars[a0][i - 1], -1.0)
                sct.SetCoefficient(s_ai, -1.0)

                # Valid 4-interval minimum-run inequality: C[a0, i] >= sum_{s=max(1, i-3)..i} st_a[a0, s]
                rct = sv.Constraint(0.0, sv.infinity())
                rct.SetCoefficient(c_ai, 1.0)
                for s in range(max(1, i - 3), i + 1):
                    rct.SetCoefficient(st_vars[a0][s], -1.0)

            if vmax_ai < nE:
                max_ex = min(nE - vmax_ai, 14)
                ov = sv.Constraint(-sv.infinity(), float(vmax_ai))
                ov.SetCoefficient(c_ai, 1.0)
                for ex in range(max_ex):
                    z = sv.NumVar(0.0, 1.0, "")
                    ov.SetCoefficient(z, -1.0)
                    obj.SetCoefficient(z, float(2 * ex + 1))
                if nE - vmax_ai > max_ex:
                    zt = sv.NumVar(0.0, float(nE - vmax_ai - max_ex), "")
                    ov.SetCoefficient(zt, -1.0)
                    obj.SetCoefficient(zt, float(2 * max_ex + 1))

    st = sv.Solve()
    st_map = {
        pywraplp.Solver.OPTIMAL: "OPTIMAL",
        pywraplp.Solver.FEASIBLE: "FEASIBLE",
        pywraplp.Solver.INFEASIBLE: "INFEASIBLE",
        pywraplp.Solver.NOT_SOLVED: "NOT_SOLVED",
    }
    st_name = st_map.get(st, str(st))
    if st not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        if lp_rounded is not None:
            return lp_val, lp_val, lp_rounded, "LP_ROUNDED_FALLBACK"
        return None, None, None, st_name

    shifts_by_day = [[] for _ in range(D)]
    for d_idx in range(D):
        for k, (t, l) in enumerate(by_day[d_idx]):
            cnt = int(round(c_vars[d_idx, k].solution_value()))
            for _ in range(cnt):
                shifts_by_day[d_idx].append((t, l))
    return int(round(obj.Value())), int(math.ceil(obj.BestBound() - 1e-6)), shifts_by_day, st_name


def _greedy_chain_fallback(I, shifts_by_day):
    """Fast greedy fallback packer if CP-SAT times out on huge 60-staff 28d instances."""
    D = I["h"] + 1
    E = sorted(I["staff"], key=int)
    nE = len(E)
    min_iv = [math.ceil(I["staff"][e][0] / 15) for e in E]
    max_iv = [I["staff"][e][1] // 15 for e in E]
    sh_t = np.full((nE, D), -1, dtype=np.int32)
    sh_l = np.zeros((nE, D), dtype=np.int32)
    emp_w = np.zeros(nE, dtype=np.int32)

    for d in range(D):
        # Assign earliest-starting shifts first to employees with lowest previous end time & most remaining need
        shs = sorted(shifts_by_day[d], key=lambda x: x[0])
        used = set()
        for t, l in shs:
            best_e = -1
            best_score = 10**9
            for e in range(nE):
                if e in used:
                    continue
                if d > 0 and sh_l[e, d - 1] > 0 and sh_t[e, d - 1] + sh_l[e, d - 1] + 56 > t:
                    continue
                if d >= 5 and sum(1 for k in range(d - 5, d) if sh_l[e, k] > 0) >= 5:
                    continue
                # Prefer employees furthest below min_iv, then below max_iv
                rem = min_iv[e] - emp_w[e]
                over = max(0, emp_w[e] + l - max_iv[e])
                sc = over * 100 - rem
                if sc < best_score:
                    best_score = sc
                    best_e = e
            if best_e >= 0:
                used.add(best_e)
                sh_t[best_e, d] = t
                sh_l[best_e, d] = l
                emp_w[best_e] += l
    viol = sum(max(0, min_iv[e] - int(emp_w[e])) + max(0, int(emp_w[e]) - max_iv[e]) for e in range(nE))
    return viol, sh_t, sh_l, "GREEDY_FALLBACK"


def pack_employee_chains(I, shifts_by_day, secs=35.0, workers=2, seed=1):
    """
    Stage 2: Assign Stage 1's daily shift envelopes to individual employees E respecting
    <=1 shift/day, 14h rest (exact cutoff inequalities), and 5-in-6 days, minimizing [min, max] violation.
    """
    D = I["h"] + 1
    E = sorted(I["staff"], key=int)
    nE = len(E)
    min_iv = [math.ceil(I["staff"][e][0] / 15) for e in E]
    max_iv = [I["staff"][e][1] // 15 for e in E]

    m = cp_model.CpModel()
    x = {}
    work = {}

    for d in range(D):
        K_d = len(shifts_by_day[d])
        for k in range(K_d):
            lits_k = []
            for ei in range(nE):
                v = m.NewBoolVar("")
                x[ei, d, k] = v
                lits_k.append(v)
            m.AddExactlyOne(lits_k)
        for ei in range(nE):
            if K_d > 0:
                w = m.NewBoolVar("")
                m.Add(sum(x[ei, d, k] for k in range(K_d)) == w)
                work[ei, d] = w
            else:
                work[ei, d] = 0

    for ei in range(nE):
        for d0 in range(0, D - 5):
            m.Add(sum(work[ei, d] for d in range(d0, d0 + 6)) <= 5)

    for d in range(D - 1):
        sh_cur = shifts_by_day[d]
        sh_nxt = shifts_by_day[d + 1]
        if not sh_cur or not sh_nxt:
            continue
        ends = sorted({t + l for t, l in sh_cur})
        min_nxt_s = min(t for t, _ in sh_nxt)
        for U in ends:
            if U + 56 <= min_nxt_s:
                continue
            late_k = [k for k, (t, l) in enumerate(sh_cur) if t + l >= U]
            early_k = [k for k, (t, l) in enumerate(sh_nxt) if t < U + 56]
            if late_k and early_k:
                for ei in range(nE):
                    m.Add(sum(x[ei, d, k] for k in late_k) + sum(x[ei, d + 1, k] for k in early_k) <= 1)

    viols = []
    surplus = []
    for ei in range(nE):
        tot = sum(shifts_by_day[d][k][1] * x[ei, d, k] for d in range(D) for k in range(len(shifts_by_day[d])))
        u_v = m.NewIntVar(0, min_iv[ei], "")
        o_v = m.NewIntVar(0, D * 40, "")
        s_v = m.NewIntVar(0, D * 40, "")
        m.Add(u_v >= min_iv[ei] - tot)
        m.Add(o_v >= tot - max_iv[ei])
        m.Add(s_v >= tot - min_iv[ei])
        viols.append(u_v)
        viols.append(o_v)
        surplus.append(s_v)

    m.Minimize(10 * sum(viols) + sum(surplus))
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(secs)
    sv.parameters.num_workers = int(workers)
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return _greedy_chain_fallback(I, shifts_by_day)

    sh_t = np.full((nE, D), -1, dtype=np.int32)
    sh_l = np.zeros((nE, D), dtype=np.int32)
    for d in range(D):
        for k, (t, l) in enumerate(shifts_by_day[d]):
            for ei in range(nE):
                if sv.Value(x[ei, d, k]):
                    sh_t[ei, d] = t
                    sh_l[ei, d] = l
                    break
    # Compute true contract violation (excluding surplus tie-breaker)
    true_viol = 0
    for ei in range(nE):
        w = int(np.sum(sh_l[ei]))
        if w < min_iv[ei]:
            true_viol += min_iv[ei] - w
        elif w > max_iv[ei]:
            true_viol += w - max_iv[ei]
    return true_viol, sh_t, sh_l, sv.StatusName(st)


def _greedy_paint_fallback(I, sh_t, sh_l):
    """Fast greedy 1-block task painter fallback if Stage 3 HiGHS times out."""
    A, N = I["A"], I["N"]
    nE, D = sh_t.shape
    cov = np.zeros((A, N), dtype=np.int32)
    n_blk = np.zeros((nE, D), dtype=np.int32)
    blk_a = np.zeros((nE, D, MAX_BLK), dtype=np.int32)
    blk_l = np.zeros((nE, D, MAX_BLK), dtype=np.int32)
    for d in range(D):
        for e in range(nE):
            l = int(sh_l[e, d])
            if l <= 0:
                continue
            t = int(sh_t[e, d])
            best_a = 0
            best_sc = 10**12
            for a0 in range(A):
                a = a0 + 1
                sc = 0
                for i in range(t, t + l):
                    c = int(cov[a0, i])
                    if c < I["vmin"][a][i]:
                        sc -= 500 * (I["vmin"][a][i] - c)
                    elif c >= I["vmax"][a][i]:
                        sc += 2 * (c - I["vmax"][a][i]) + 1
                if sc < best_sc:
                    best_sc = sc
                    best_a = a0
            n_blk[e, d] = 1
            blk_a[e, d, 0] = best_a
            blk_l[e, d, 0] = l
            for i in range(t, t + l):
                cov[best_a, i] += 1
    return None, n_blk, blk_a, blk_l, "GREEDY_FALLBACK"


def paint_shift_tasks_mip(I, sh_t, sh_l, secs=25.0, workers=2, grid_step=None):
    """
    Stage 3: Global Within-Shift Task-Block Partitioner (HiGHS).
    Given fixed shift envelopes (sh_t, sh_l), groups identical (t, l) envelopes into
    aggregate counts K_{t,l} (eliminating employee symmetry!), and chooses 1-block or
    2-block (>= 4 interval) task patterns on a `grid_step`-interval split grid to
    minimize hard vmin slack (weight 500) + exact quadratic vmax over-cover penalty.
    """
    A, N = I["A"], I["N"]
    nE, D = sh_t.shape
    if grid_step is None:
        grid_step = 4 if A <= 2 else (8 if A == 3 else (12 if A == 4 else 16))

    # Group identical (t, l) envelopes across all employees to eliminate symmetry!
    env_slots = {}
    for e in range(nE):
        for d in range(D):
            l = int(sh_l[e, d])
            if l > 0:
                key = (int(sh_t[e, d]), l)
                env_slots.setdefault(key, []).append((e, d))

    sv = pywraplp.Solver.CreateSolver("HIGHS")
    sv.SetTimeLimit(int(secs * 1000))
    sv.SetNumThreads(int(workers))
    sv.SetSolverSpecificParametersAsString("mip_rel_gap = 0.004")

    # Difference arrays per task a0 in 0..A-1: cov[a0, i] = cov[a0, i-1] + add[a0, i] - sub[a0, i]
    add_iv = [[[] for _ in range(N + 1)] for _ in range(A)]
    sub_iv = [[[] for _ in range(N + 1)] for _ in range(A)]

    pat_vars = {}  # key -> list of (var, blocks_tuple)
    for key, slots in env_slots.items():
        t, l = key
        cnt = len(slots)
        ct = sv.Constraint(float(cnt), float(cnt))
        plist = []
        # 1-block patterns
        for a0 in range(A):
            v = sv.IntVar(0.0, float(cnt), "")
            ct.SetCoefficient(v, 1.0)
            add_iv[a0][t].append(v)
            sub_iv[a0][t + l].append(v)
            plist.append((v, ((a0, l),)))
        # 2-block patterns on split grid (4, 4+step, ..., l-4)
        splits = list(range(4, l - 3, grid_step))
        if (l - 4) not in splits and l >= 8:
            splits.append(l - 4)
        for s in splits:
            for a1 in range(A):
                for a2 in range(A):
                    if a1 == a2:
                        continue
                    v = sv.IntVar(0.0, float(cnt), "")
                    ct.SetCoefficient(v, 1.0)
                    add_iv[a1][t].append(v)
                    sub_iv[a1][t + s].append(v)
                    add_iv[a2][t + s].append(v)
                    sub_iv[a2][t + l].append(v)
                    plist.append((v, ((a1, s), (a2, l - s))))
        pat_vars[key] = plist

    obj = sv.Objective()
    obj.SetMinimization()
    for a0 in range(A):
        a = a0 + 1
        C_prev = None
        for i in range(N):
            C_i = sv.NumVar(0.0, float(nE), "")
            dc = sv.Constraint(0.0, 0.0)
            dc.SetCoefficient(C_i, 1.0)
            if C_prev is not None:
                dc.SetCoefficient(C_prev, -1.0)
            for v in add_iv[a0][i]:
                dc.SetCoefficient(v, -1.0)
            for v in sub_iv[a0][i]:
                dc.SetCoefficient(v, 1.0)
            C_prev = C_i

            vmin_ai = I["vmin"][a][i]
            if vmin_ai > 0:
                u = sv.NumVar(0.0, float(vmin_ai), "")
                uct = sv.Constraint(float(vmin_ai), sv.infinity())
                uct.SetCoefficient(C_i, 1.0)
                uct.SetCoefficient(u, 1.0)
                obj.SetCoefficient(u, 500.0)

            vmax_ai = I["vmax"][a][i]
            if vmax_ai < nE:
                max_ex = min(nE - vmax_ai, 14)
                ov = sv.Constraint(-sv.infinity(), float(vmax_ai))
                ov.SetCoefficient(C_i, 1.0)
                for ex in range(max_ex):
                    z = sv.NumVar(0.0, 1.0, "")
                    ov.SetCoefficient(z, -1.0)
                    obj.SetCoefficient(z, float(2 * ex + 1))
                if nE - vmax_ai > max_ex:
                    zt = sv.NumVar(0.0, float(nE - vmax_ai - max_ex), "")
                    ov.SetCoefficient(zt, -1.0)
                    obj.SetCoefficient(zt, float(2 * max_ex + 1))

    st = sv.Solve()
    n_blk = np.zeros((nE, D), dtype=np.int32)
    blk_a = np.zeros((nE, D, MAX_BLK), dtype=np.int32)
    blk_l = np.zeros((nE, D, MAX_BLK), dtype=np.int32)

    if st not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        return _greedy_paint_fallback(I, sh_t, sh_l)

    for key, slots in env_slots.items():
        assigned = []
        for v, blocks in pat_vars[key]:
            c = int(round(v.solution_value()))
            for _ in range(c):
                assigned.append(blocks)
        while len(assigned) < len(slots):
            assigned.append(((0, key[1]),))
        for (e, d), blocks in zip(slots, assigned):
            n_blk[e, d] = len(blocks)
            for b, (a0, bl) in enumerate(blocks):
                blk_a[e, d, b] = a0
                blk_l[e, d, b] = bl

    st_name = "OPTIMAL" if st == pywraplp.Solver.OPTIMAL else "FEASIBLE"
    return int(round(obj.Value())), n_blk, blk_a, blk_l, st_name


def build_allowed_arrays(I, by_day):
    D = len(by_day)
    N = I["N"]
    max_opts = max(len(x) for x in by_day)
    opt_t = np.full((D, max_opts), -1, dtype=np.int32)
    opt_l = np.zeros((D, max_opts), dtype=np.int32)
    opt_cnt = np.zeros(D, dtype=np.int32)
    start_ok = np.zeros((D, N), dtype=np.uint8)
    for d in range(D):
        opt_cnt[d] = len(by_day[d])
        for k, (t, l) in enumerate(by_day[d]):
            opt_t[d, k] = t
            opt_l[d, k] = l
            start_ok[d, t] = 1
    return opt_t, opt_l, opt_cnt, start_ok


@njit(cache=True)
def _emp_viol(w, min_w, max_w):
    if w < min_w:
        return min_w - w
    if w > max_w:
        return w - max_w
    return 0


@njit(cache=True)
def _rest_ok(sh_t, sh_l, e, d, new_t, new_l, D):
    if new_l == 0:
        return True
    if d > 0 and sh_l[e, d - 1] > 0:
        if sh_t[e, d - 1] + sh_l[e, d - 1] + 56 > new_t:
            return False
    if d + 1 < D and sh_l[e, d + 1] > 0:
        if new_t + new_l + 56 > sh_t[e, d + 1]:
            return False
    return True


@njit(cache=True)
def _five_in_six_ok(sh_l, e, d, D):
    lo = d - 5 if d - 5 > 0 else 0
    hi = d if d + 5 < D else D - 6
    for d0 in range(lo, hi + 1):
        cnt = 1
        for k in range(d0, d0 + 6):
            if k != d and sh_l[e, k] > 0:
                cnt += 1
        if cnt > 5:
            return False
    return True


@njit(cache=True)
def _delta_range(cov, vmin, vmax, a, i0, i1, sign):
    """Apply +1 or -1 to cov[a, i0:i1] IN-PLACE and return (d_ucov, d_pen)."""
    d_ucov = 0
    d_pen = 0
    if sign > 0:
        for i in range(i0, i1):
            c = cov[a, i]
            if c < vmin[a, i]:
                d_ucov += (vmin[a, i] - (c + 1)) ** 2 - (vmin[a, i] - c) ** 2
            if c >= vmax[a, i]:
                d_pen += (c + 1 - vmax[a, i]) ** 2 - (c - vmax[a, i]) ** 2
            cov[a, i] = c + 1
    else:
        for i in range(i0, i1):
            c = cov[a, i]
            if c <= vmin[a, i]:
                d_ucov += (vmin[a, i] - (c - 1)) ** 2 - (vmin[a, i] - c) ** 2
            if c > vmax[a, i]:
                d_pen += (c - 1 - vmax[a, i]) ** 2 - (c - vmax[a, i]) ** 2
            cov[a, i] = c - 1
    return d_ucov, d_pen


@njit(cache=True)
def _apply_shift_cov(cov, vmin, vmax, t, nb, ba, bl, sign):
    """Apply +1 or -1 for all blocks of a shift IN-PLACE, returning (d_ucov, d_pen)."""
    du_tot = 0
    dp_tot = 0
    pos = t
    for b in range(nb):
        a = ba[b]
        ln = bl[b]
        du, dp = _delta_range(cov, vmin, vmax, a, pos, pos + ln, sign)
        du_tot += du
        dp_tot += dp
        pos += ln
    return du_tot, dp_tot


@njit(cache=True)
def _revert_shift_cov(cov, t, nb, ba, bl, sign):
    pos = t
    for b in range(nb):
        a = ba[b]
        ln = bl[b]
        for i in range(pos, pos + ln):
            cov[a, i] += sign
        pos += ln


@njit(cache=True)
def _normalize_blocks(nb, ba, bl):
    """Merge adjacent blocks with identical task IDs in-place; return new nb."""
    if nb <= 1:
        return nb
    w = 0
    for b in range(1, nb):
        if ba[b] == ba[w]:
            bl[w] += bl[b]
        else:
            w += 1
            ba[w] = ba[b]
            bl[w] = bl[b]
    return w + 1


@njit(cache=True)
def sa_polish_mtask(sh_t_in, sh_l_in, n_blk_in, blk_a_in, blk_l_in,
                    vmin, vmax, min_iv, max_iv, opt_t, opt_l, opt_cnt, start_ok,
                    n_iters, temp_start, temp_end, w_hard, seed):
    """
    Multi-Task Numba O(1) Delta-Eval SA with 7 move families:
      1. Slide internal task split (+-1..4)      [20%]
      2. Flip a block's task ID                  [10%]
      3. Split or merge task blocks              [12%]
      4. Surgical envelope nudge / add / drop    [22%]
      5. 2-employee day swap (0 cover delta)     [12%]
      6. Same-employee 2-day length transfer     [14%]
      7. Cross-day shift move (d1 -> d2)         [10%]
    Maintains 14h rest, 5-in-6, and block_len >= 4 HARD at all times.
    """
    np.random.seed(seed)
    nE, D = sh_t_in.shape
    A, N = vmin.shape
    W_HARD = w_hard

    sh_t = sh_t_in.copy()
    sh_l = sh_l_in.copy()
    n_blk = n_blk_in.copy()
    blk_a = blk_a_in.copy()
    blk_l = blk_l_in.copy()

    cov = np.zeros((A, N), dtype=np.int32)
    emp_w = np.zeros(nE, dtype=np.int32)

    for e in range(nE):
        for d in range(D):
            l = sh_l[e, d]
            if l > 0:
                emp_w[e] += l
                pos = sh_t[e, d]
                for b in range(n_blk[e, d]):
                    a = blk_a[e, d, b]
                    ln = blk_l[e, d, b]
                    for i in range(pos, pos + ln):
                        cov[a, i] += 1
                    pos += ln

    cur_pen = 0
    cur_ucov = 0
    for a in range(A):
        for i in range(N):
            c = cov[a, i]
            if c < vmin[a, i]:
                d_ = vmin[a, i] - c
                cur_ucov += d_ * d_
            elif c > vmax[a, i]:
                d_ = c - vmax[a, i]
                cur_pen += d_ * d_

    cur_cviol = 0
    for e in range(nE):
        cur_cviol += _emp_viol(emp_w[e], min_iv[e], max_iv[e])

    best_feas_pen = 1000000000
    best_t = sh_t.copy()
    best_l = sh_l.copy()
    best_nb = n_blk.copy()
    best_ba = blk_a.copy()
    best_bl = blk_l.copy()
    if cur_ucov == 0 and cur_cviol == 0:
        best_feas_pen = cur_pen

    cool = (temp_end / temp_start) ** (1.0 / max(1, n_iters))
    temp = temp_start
    accepted = 0

    tmp_ba = np.zeros(MAX_BLK, dtype=np.int32)
    tmp_bl = np.zeros(MAX_BLK, dtype=np.int32)

    for _it in range(n_iters):
        r = np.random.random()

        if r < 0.20:
            # Move 1: Slide internal task split boundary between blocks b and b+1
            e = np.random.randint(0, nE)
            d = np.random.randint(0, D)
            nb = n_blk[e, d]
            if nb < 2:
                temp *= cool
                continue
            b = np.random.randint(0, nb - 1)
            step = np.random.randint(1, 5)
            if np.random.random() < 0.5:
                step = -step
            l0 = blk_l[e, d, b]
            l1 = blk_l[e, d, b + 1]
            if l0 + step < 4 or l1 - step < 4:
                temp *= cool
                continue
            # Find boundary position
            pos = sh_t[e, d]
            for k in range(b):
                pos += blk_l[e, d, k]
            bnd = pos + l0
            a0 = blk_a[e, d, b]
            a1 = blk_a[e, d, b + 1]
            if step > 0:
                # [bnd, bnd+step) switches from a1 -> a0
                du1, dp1 = _delta_range(cov, vmin, vmax, a1, bnd, bnd + step, -1)
                du2, dp2 = _delta_range(cov, vmin, vmax, a0, bnd, bnd + step, 1)
                d_ucov = du1 + du2
                d_pen = dp1 + dp2
                d_obj = W_HARD * d_ucov + d_pen
                if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                    blk_l[e, d, b] = l0 + step
                    blk_l[e, d, b + 1] = l1 - step
                    cur_ucov += d_ucov
                    cur_pen += d_pen
                    accepted += 1
                    if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                        best_feas_pen = cur_pen
                        best_t = sh_t.copy(); best_l = sh_l.copy()
                        best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
                else:
                    for i in range(bnd, bnd + step):
                        cov[a0, i] -= 1
                        cov[a1, i] += 1
            else:
                st_abs = -step
                # [bnd-st_abs, bnd) switches from a0 -> a1
                du1, dp1 = _delta_range(cov, vmin, vmax, a0, bnd - st_abs, bnd, -1)
                du2, dp2 = _delta_range(cov, vmin, vmax, a1, bnd - st_abs, bnd, 1)
                d_ucov = du1 + du2
                d_pen = dp1 + dp2
                d_obj = W_HARD * d_ucov + d_pen
                if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                    blk_l[e, d, b] = l0 + step
                    blk_l[e, d, b + 1] = l1 - step
                    cur_ucov += d_ucov
                    cur_pen += d_pen
                    accepted += 1
                    if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                        best_feas_pen = cur_pen
                        best_t = sh_t.copy(); best_l = sh_l.copy()
                        best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
                else:
                    for i in range(bnd - st_abs, bnd):
                        cov[a1, i] -= 1
                        cov[a0, i] += 1

        elif r < 0.30:
            # Move 2: Flip a block's task ID (a_old -> a_new)
            e = np.random.randint(0, nE)
            d = np.random.randint(0, D)
            nb = n_blk[e, d]
            if nb == 0:
                temp *= cool
                continue
            b = np.random.randint(0, nb)
            a_old = blk_a[e, d, b]
            a_new = np.random.randint(0, A - 1)
            if a_new >= a_old:
                a_new += 1
            pos = sh_t[e, d]
            for k in range(b):
                pos += blk_l[e, d, k]
            ln = blk_l[e, d, b]
            du1, dp1 = _delta_range(cov, vmin, vmax, a_old, pos, pos + ln, -1)
            du2, dp2 = _delta_range(cov, vmin, vmax, a_new, pos, pos + ln, 1)
            d_ucov = du1 + du2
            d_pen = dp1 + dp2
            d_obj = W_HARD * d_ucov + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                blk_a[e, d, b] = a_new
                n_blk[e, d] = _normalize_blocks(nb, blk_a[e, d], blk_l[e, d])
                cur_ucov += d_ucov
                cur_pen += d_pen
                accepted += 1
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
            else:
                for i in range(pos, pos + ln):
                    cov[a_new, i] -= 1
                    cov[a_old, i] += 1

        elif r < 0.42:
            # Move 3: Split a block (len >= 8) into 2 blocks, or merge 2 adjacent blocks
            e = np.random.randint(0, nE)
            d = np.random.randint(0, D)
            nb = n_blk[e, d]
            if nb == 0:
                temp *= cool
                continue
            if (nb == 1) or (nb < MAX_BLK and np.random.random() < 0.55):
                # Split block b
                b = np.random.randint(0, nb)
                ln = blk_l[e, d, b]
                if ln < 8:
                    temp *= cool
                    continue
                s = np.random.randint(4, ln - 3)
                a_old = blk_a[e, d, b]
                a_new = np.random.randint(0, A - 1)
                if a_new >= a_old:
                    a_new += 1
                pos = sh_t[e, d]
                for k in range(b):
                    pos += blk_l[e, d, k]
                # Choose whether new task is on second half or first half
                second_half = np.random.random() < 0.5
                if second_half:
                    i0, i1 = pos + s, pos + ln
                else:
                    i0, i1 = pos, pos + s
                du1, dp1 = _delta_range(cov, vmin, vmax, a_old, i0, i1, -1)
                du2, dp2 = _delta_range(cov, vmin, vmax, a_new, i0, i1, 1)
                d_ucov = du1 + du2
                d_pen = dp1 + dp2
                d_obj = W_HARD * d_ucov + d_pen
                if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                    # Shift right blocks by 1
                    for k in range(nb, b + 1, -1):
                        blk_a[e, d, k] = blk_a[e, d, k - 1]
                        blk_l[e, d, k] = blk_l[e, d, k - 1]
                    if second_half:
                        blk_a[e, d, b] = a_old; blk_l[e, d, b] = s
                        blk_a[e, d, b + 1] = a_new; blk_l[e, d, b + 1] = ln - s
                    else:
                        blk_a[e, d, b] = a_new; blk_l[e, d, b] = s
                        blk_a[e, d, b + 1] = a_old; blk_l[e, d, b + 1] = ln - s
                    n_blk[e, d] = _normalize_blocks(nb + 1, blk_a[e, d], blk_l[e, d])
                    cur_ucov += d_ucov
                    cur_pen += d_pen
                    accepted += 1
                    if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                        best_feas_pen = cur_pen
                        best_t = sh_t.copy(); best_l = sh_l.copy()
                        best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
                else:
                    for i in range(i0, i1):
                        cov[a_new, i] -= 1
                        cov[a_old, i] += 1
            else:
                # Merge blocks b and b+1
                b = np.random.randint(0, nb - 1)
                pos = sh_t[e, d]
                for k in range(b):
                    pos += blk_l[e, d, k]
                l0, l1 = blk_l[e, d, b], blk_l[e, d, b + 1]
                a0, a1 = blk_a[e, d, b], blk_a[e, d, b + 1]
                keep_left = np.random.random() < 0.5
                if keep_left:
                    i0, i1, a_from, a_to = pos + l0, pos + l0 + l1, a1, a0
                else:
                    i0, i1, a_from, a_to = pos, pos + l0, a0, a1
                du1, dp1 = _delta_range(cov, vmin, vmax, a_from, i0, i1, -1)
                du2, dp2 = _delta_range(cov, vmin, vmax, a_to, i0, i1, 1)
                d_ucov = du1 + du2
                d_pen = dp1 + dp2
                d_obj = W_HARD * d_ucov + d_pen
                if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                    blk_a[e, d, b] = a_to
                    blk_l[e, d, b] = l0 + l1
                    for k in range(b + 1, nb - 1):
                        blk_a[e, d, k] = blk_a[e, d, k + 1]
                        blk_l[e, d, k] = blk_l[e, d, k + 1]
                    n_blk[e, d] = _normalize_blocks(nb - 1, blk_a[e, d], blk_l[e, d])
                    cur_ucov += d_ucov
                    cur_pen += d_pen
                    accepted += 1
                    if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                        best_feas_pen = cur_pen
                        best_t = sh_t.copy(); best_l = sh_l.copy()
                        best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
                else:
                    for i in range(i0, i1):
                        cov[a_to, i] -= 1
                        cov[a_from, i] += 1

        elif r < 0.64:
            # Move 4: Surgical envelope nudge (+-1/+-2 resize or slide), add, or drop on (e, d)
            e = np.random.randint(0, nE)
            d = np.random.randint(0, D)
            n_o = opt_cnt[d]
            if n_o == 0:
                temp *= cool
                continue
            old_t = sh_t[e, d]
            old_l = sh_l[e, d]
            old_nb = n_blk[e, d]

            if old_l > 0 and np.random.random() < 0.08:
                # Drop shift
                new_t = -1; new_l = 0; new_nb = 0
            elif old_l == 0:
                if not _five_in_six_ok(sh_l, e, d, D):
                    temp *= cool
                    continue
                idx_o = np.random.randint(0, n_o)
                new_t = opt_t[d, idx_o]; new_l = opt_l[d, idx_o]
                if not _rest_ok(sh_t, sh_l, e, d, new_t, new_l, D):
                    temp *= cool
                    continue
                if np.random.random() < 0.5:
                    new_nb = 1
                    tmp_ba[0] = np.random.randint(0, A)
                    tmp_bl[0] = new_l
                else:
                    new_nb = 2
                    s = np.random.randint(4, new_l - 3)
                    a1 = np.random.randint(0, A)
                    a2 = np.random.randint(0, A - 1)
                    if a2 >= a1: a2 += 1
                    tmp_ba[0] = a1; tmp_bl[0] = s
                    tmp_ba[1] = a2; tmp_bl[1] = new_l - s
            else:
                # Surgical nudge on active shift: slide, resize end, or resize start
                sub = np.random.randint(0, 3)
                step = 1 if np.random.random() < 0.75 else 2
                if np.random.random() < 0.5:
                    step = -step
                for k in range(old_nb):
                    tmp_ba[k] = blk_a[e, d, k]
                    tmp_bl[k] = blk_l[e, d, k]
                new_nb = old_nb
                if sub == 0:
                    # Resize end (last block)
                    new_t = old_t; new_l = old_l + step
                    tmp_bl[new_nb - 1] += step
                    if tmp_bl[new_nb - 1] < 4:
                        temp *= cool
                        continue
                elif sub == 1:
                    # Slide whole shift
                    new_t = old_t + step; new_l = old_l
                else:
                    # Resize start (first block)
                    new_t = old_t + step; new_l = old_l - step
                    tmp_bl[0] -= step
                    if tmp_bl[0] < 4:
                        temp *= cool
                        continue
                if new_l < 24 or new_l > 40 or new_t < 0 or new_t + new_l > N or start_ok[d, new_t] == 0:
                    temp *= cool
                    continue
                if not _rest_ok(sh_t, sh_l, e, d, new_t, new_l, D):
                    temp *= cool
                    continue

            old_ev = _emp_viol(emp_w[e], min_iv[e], max_iv[e])
            new_ew = emp_w[e] - old_l + new_l
            d_cviol = _emp_viol(new_ew, min_iv[e], max_iv[e]) - old_ev

            du1, dp1 = 0, 0
            if old_l > 0:
                du1, dp1 = _apply_shift_cov(cov, vmin, vmax, old_t, old_nb, blk_a[e, d], blk_l[e, d], -1)
            du2, dp2 = 0, 0
            if new_l > 0:
                du2, dp2 = _apply_shift_cov(cov, vmin, vmax, new_t, new_nb, tmp_ba, tmp_bl, 1)
            d_ucov = du1 + du2
            d_pen = dp1 + dp2
            d_obj = W_HARD * (d_ucov + d_cviol) + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e, d] = new_t; sh_l[e, d] = new_l; n_blk[e, d] = new_nb
                for k in range(new_nb):
                    blk_a[e, d, k] = tmp_ba[k]; blk_l[e, d, k] = tmp_bl[k]
                emp_w[e] = new_ew
                cur_ucov += d_ucov; cur_pen += d_pen; cur_cviol += d_cviol
                accepted += 1
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
            else:
                if new_l > 0:
                    _revert_shift_cov(cov, new_t, new_nb, tmp_ba, tmp_bl, -1)
                if old_l > 0:
                    _revert_shift_cov(cov, old_t, old_nb, blk_a[e, d], blk_l[e, d], 1)

        elif r < 0.76:
            # Move 5: 2-employee day swap (zero cover delta!)
            e1 = np.random.randint(0, nE)
            e2 = np.random.randint(0, nE - 1)
            if e2 >= e1:
                e2 += 1
            d = np.random.randint(0, D)
            t1, l1 = sh_t[e1, d], sh_l[e1, d]
            t2, l2 = sh_t[e2, d], sh_l[e2, d]
            if l1 == 0 and l2 == 0:
                temp *= cool
                continue
            if l2 > 0 and l1 == 0 and not _five_in_six_ok(sh_l, e1, d, D):
                temp *= cool
                continue
            if l1 > 0 and l2 == 0 and not _five_in_six_ok(sh_l, e2, d, D):
                temp *= cool
                continue
            if not _rest_ok(sh_t, sh_l, e1, d, t2, l2, D) or not _rest_ok(sh_t, sh_l, e2, d, t1, l1, D):
                temp *= cool
                continue
            old_ev = _emp_viol(emp_w[e1], min_iv[e1], max_iv[e1]) + _emp_viol(emp_w[e2], min_iv[e2], max_iv[e2])
            nw1 = emp_w[e1] - l1 + l2
            nw2 = emp_w[e2] - l2 + l1
            d_cviol = (_emp_viol(nw1, min_iv[e1], max_iv[e1]) + _emp_viol(nw2, min_iv[e2], max_iv[e2])) - old_ev
            d_obj = W_HARD * d_cviol
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e1, d], sh_t[e2, d] = t2, t1
                sh_l[e1, d], sh_l[e2, d] = l2, l1
                nb1, nb2 = n_blk[e1, d], n_blk[e2, d]
                n_blk[e1, d], n_blk[e2, d] = nb2, nb1
                for k in range(MAX_BLK):
                    ta = blk_a[e1, d, k]; blk_a[e1, d, k] = blk_a[e2, d, k]; blk_a[e2, d, k] = ta
                    tl = blk_l[e1, d, k]; blk_l[e1, d, k] = blk_l[e2, d, k]; blk_l[e2, d, k] = tl
                emp_w[e1] = nw1; emp_w[e2] = nw2
                cur_cviol += d_cviol
                accepted += 1
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()

        elif r < 0.90:
            # Move 6: Same-employee 2-day length transfer (+step on d1, -step on d2) — ZERO contract delta!
            e = np.random.randint(0, nE)
            d1 = np.random.randint(0, D)
            d2 = np.random.randint(0, D - 1)
            if d2 >= d1:
                d2 += 1
            ot1, ol1, nb1 = sh_t[e, d1], sh_l[e, d1], n_blk[e, d1]
            ot2, ol2, nb2 = sh_t[e, d2], sh_l[e, d2], n_blk[e, d2]
            if ol1 == 0 or ol2 == 0:
                temp *= cool
                continue
            step = 1 if np.random.random() < 0.75 else 2
            end1 = np.random.random() < 0.5
            end2 = np.random.random() < 0.5
            if end1:
                nt1, nl1 = ot1, ol1 + step
                i1_0, i1_1, a1_chg = ot1 + ol1, ot1 + ol1 + step, blk_a[e, d1, nb1 - 1]
            else:
                nt1, nl1 = ot1 - step, ol1 + step
                i1_0, i1_1, a1_chg = ot1 - step, ot1, blk_a[e, d1, 0]
            if end2:
                nt2, nl2 = ot2, ol2 - step
                if blk_l[e, d2, nb2 - 1] - step < 4:
                    temp *= cool
                    continue
                i2_0, i2_1, a2_chg = ot2 + ol2 - step, ot2 + ol2, blk_a[e, d2, nb2 - 1]
            else:
                nt2, nl2 = ot2 + step, ol2 - step
                if blk_l[e, d2, 0] - step < 4:
                    temp *= cool
                    continue
                i2_0, i2_1, a2_chg = ot2, ot2 + step, blk_a[e, d2, 0]
            if nl1 > 40 or nl2 < 24 or nt1 < 0 or nt1 + nl1 > N or nt2 < 0 or nt2 + nl2 > N:
                temp *= cool
                continue
            if start_ok[d1, nt1] == 0 or start_ok[d2, nt2] == 0:
                temp *= cool
                continue
            sh_t[e, d1], sh_l[e, d1] = nt1, nl1
            sh_t[e, d2], sh_l[e, d2] = nt2, nl2
            ok_r = _rest_ok(sh_t, sh_l, e, d1, nt1, nl1, D) and _rest_ok(sh_t, sh_l, e, d2, nt2, nl2, D)
            sh_t[e, d1], sh_l[e, d1] = ot1, ol1
            sh_t[e, d2], sh_l[e, d2] = ot2, ol2
            if not ok_r:
                temp *= cool
                continue

            du1, dp1 = _delta_range(cov, vmin, vmax, a2_chg, i2_0, i2_1, -1)
            du2, dp2 = _delta_range(cov, vmin, vmax, a1_chg, i1_0, i1_1, 1)
            d_ucov = du1 + du2
            d_pen = dp1 + dp2
            d_obj = W_HARD * d_ucov + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e, d1], sh_l[e, d1] = nt1, nl1
                sh_t[e, d2], sh_l[e, d2] = nt2, nl2
                if end1: blk_l[e, d1, nb1 - 1] += step
                else: blk_l[e, d1, 0] += step
                if end2: blk_l[e, d2, nb2 - 1] -= step
                else: blk_l[e, d2, 0] -= step
                cur_ucov += d_ucov; cur_pen += d_pen
                accepted += 1
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
            else:
                for i in range(i1_0, i1_1): cov[a1_chg, i] -= 1
                for i in range(i2_0, i2_1): cov[a2_chg, i] += 1

        else:
            # Move 7: Cross-day shift move (working day d1 -> off day d2)
            e = np.random.randint(0, nE)
            d1 = np.random.randint(0, D)
            d2 = np.random.randint(0, D)
            if d1 == d2 or sh_l[e, d1] == 0 or sh_l[e, d2] > 0 or opt_cnt[d2] == 0:
                temp *= cool
                continue
            old_t, old_l, old_nb = sh_t[e, d1], sh_l[e, d1], n_blk[e, d1]
            sh_l[e, d1] = 0
            if not _five_in_six_ok(sh_l, e, d2, D):
                sh_l[e, d1] = old_l
                temp *= cool
                continue
            idx_o = np.random.randint(0, opt_cnt[d2])
            new_t = opt_t[d2, idx_o]; new_l = opt_l[d2, idx_o]
            if not _rest_ok(sh_t, sh_l, e, d2, new_t, new_l, D):
                sh_l[e, d1] = old_l
                temp *= cool
                continue
            sh_l[e, d1] = old_l

            if np.random.random() < 0.5:
                new_nb = 1
                tmp_ba[0] = np.random.randint(0, A)
                tmp_bl[0] = new_l
            else:
                new_nb = 2
                s = np.random.randint(4, new_l - 3)
                a1 = np.random.randint(0, A)
                a2 = np.random.randint(0, A - 1)
                if a2 >= a1: a2 += 1
                tmp_ba[0] = a1; tmp_bl[0] = s
                tmp_ba[1] = a2; tmp_bl[1] = new_l - s

            old_ev = _emp_viol(emp_w[e], min_iv[e], max_iv[e])
            new_ew = emp_w[e] - old_l + new_l
            d_cviol = _emp_viol(new_ew, min_iv[e], max_iv[e]) - old_ev

            du1, dp1 = _apply_shift_cov(cov, vmin, vmax, old_t, old_nb, blk_a[e, d1], blk_l[e, d1], -1)
            du2, dp2 = _apply_shift_cov(cov, vmin, vmax, new_t, new_nb, tmp_ba, tmp_bl, 1)
            d_ucov = du1 + du2
            d_pen = dp1 + dp2
            d_obj = W_HARD * (d_ucov + d_cviol) + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e, d1] = -1; sh_l[e, d1] = 0; n_blk[e, d1] = 0
                sh_t[e, d2] = new_t; sh_l[e, d2] = new_l; n_blk[e, d2] = new_nb
                for k in range(new_nb):
                    blk_a[e, d2, k] = tmp_ba[k]; blk_l[e, d2, k] = tmp_bl[k]
                emp_w[e] = new_ew
                cur_ucov += d_ucov; cur_pen += d_pen; cur_cviol += d_cviol
                accepted += 1
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
            else:
                _revert_shift_cov(cov, new_t, new_nb, tmp_ba, tmp_bl, -1)
                _revert_shift_cov(cov, old_t, old_nb, blk_a[e, d1], blk_l[e, d1], 1)

        temp *= cool

    return best_feas_pen, best_t, best_l, best_nb, best_ba, best_bl, cur_ucov, cur_cviol, accepted


def to_xml_mtask(stem, I, sh_t, sh_l, n_blk, blk_a, blk_l, pen):
    E = sorted(I["staff"], key=int)
    D = I["h"] + 1
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<Solution>",
        f"<ProblemFile>{stem}.ros</ProblemFile>",
        f"<Penalty>{int(pen)}</Penalty>",
    ]
    for ei, e in enumerate(E):
        out.append(f'<Employee ID="{e}">')
        for d in range(D):
            l = int(sh_l[ei, d])
            if l <= 0:
                continue
            t = int(sh_t[ei, d])
            mm = ((t + 24) % 96) * 15
            t_parts = []
            for b in range(int(n_blk[ei, d])):
                a_id = int(blk_a[ei, d, b]) + 1
                bl_min = int(blk_l[ei, d, b]) * 15
                t_parts.append(f"<Task><ID>{a_id}</ID><Length>{bl_min}</Length></Task>")
            out.append(
                f"<Shift><Day>{d}</Day><Start>{mm // 60:02d}:{mm % 60:02d}:00</Start>"
                + "".join(t_parts)
                + "</Shift>"
            )
        out.append("</Employee>")
    out.append("</Solution>")
    return "\n".join(out) + "\n"


def save_and_verify_win(stem, I, raw_txt, record, best_pen, best_t, best_l, best_nb, best_ba, best_bl):
    xml_txt = to_xml_mtask(stem, I, best_t, best_l, best_nb, best_ba, best_bl, best_pen)
    S_chk, _ = matsp.read_solution(xml_txt)
    bad, pen_chk = matsp.evaluate(I, S_chk)
    assert len(bad) == 0 and pen_chk == best_pen, f"matsp.evaluate FAIL {stem}: bad={bad[:3]} pen={pen_chk} vs {best_pen}"

    verify_line = ""
    win_path = None
    sha256 = None
    if best_pen < record:
        os.makedirs(WINS_DIR, exist_ok=True)
        os.makedirs(LOGS_DIR, exist_ok=True)
        win_path = os.path.join(WINS_DIR, f"{stem}.xml")
        write_it = True
        if os.path.exists(win_path):
            with open(win_path) as ef:
                old_s, _ = matsp.read_solution(ef.read())
            old_bad, old_pen = matsp.evaluate(I, old_s)
            if len(old_bad) == 0 and old_pen <= best_pen:
                write_it = False
        if write_it:
            tmp_xml = os.path.join(WINS_DIR, f".tmp_{stem}_{os.getpid()}.xml")
            with open(tmp_xml, "w") as wf:
                wf.write(xml_txt)
            os.replace(tmp_xml, win_path)
        with open(win_path) as rf:
            final_xml = rf.read()
        sha256 = hashlib.sha256(final_xml.encode("utf-8")).hexdigest()
        tmp_inst = os.path.join(LOGS_DIR, f"_tmp_{stem}_{os.getpid()}.txt")
        with open(tmp_inst, "w") as tf:
            tf.write(raw_txt)
        proc = subprocess.run(
            [sys.executable, VERIFY_SCRIPT, tmp_inst, win_path, str(record)],
            capture_output=True, text=True, check=False,
        )
        if os.path.exists(tmp_inst):
            os.remove(tmp_inst)
        verify_line = (proc.stdout + proc.stderr).strip()
        assert proc.returncode == 0 and "PASS" in verify_line, f"verify_claim FAIL {stem}: {verify_line}"
    return True, verify_line, sha256, win_path


def solve_instance(inst_id, stem, record, lp_bound,
                   s1_secs=45.0, s2_secs=45.0, s3_secs=25.0,
                   sa_rounds=12, sa_iters=4_000_000, workers=2, seed=101,
                   lp_radius=1, mem_gb=3.0):
    lim = int(mem_gb * 1024 * 1024 * 1024)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    I, raw_txt = load_instance(stem)
    A, N = I["A"], I["N"]
    by_day = allowed_shifts_by_day(I)

    # Stage 1: Sparse HiGHS Aggregate Envelope + 1h-Block MIP
    s1_obj, s1_bd, shifts_by_day, s1_st = solve_stage1_mtask_mip(I, by_day, secs=s1_secs, workers=workers, lp_radius=lp_radius)
    if shifts_by_day is None and I["h"] + 1 > 10 and lp_radius > 0:
        s1_obj, s1_bd, shifts_by_day, s1_st = solve_stage1_mtask_mip(I, by_day, secs=s1_secs, workers=workers, lp_radius=0)
    t_s1 = round(time.time() - t0, 1)
    if shifts_by_day is None:
        return dict(id=inst_id, stem=stem, record=record, lp_bound=lp_bound,
                    s1_status=s1_st, best_pen=None, vs_rec=None, win=False, secs=t_s1)

    # Stage 2: Employee Chain Packer
    t1 = time.time()
    s2_viol, sh_t, sh_l, s2_st = pack_employee_chains(I, shifts_by_day, secs=s2_secs, workers=workers, seed=seed + 13)
    t_s2 = round(time.time() - t1, 1)

    # Stage 3: Global Within-Shift Task-Block Partitioner (skip HiGHS when s3_secs <= 0 for XL B6 speed)
    t2 = time.time()
    if s3_secs > 0:
        s3_obj, n_blk, blk_a, blk_l, s3_st = paint_shift_tasks_mip(I, sh_t, sh_l, secs=s3_secs, workers=workers)
    else:
        s3_obj, n_blk, blk_a, blk_l, s3_st = _greedy_paint_fallback(I, sh_t, sh_l)
    t_s3 = round(time.time() - t2, 1)

    # Stage 4: Multi-Task Numba O(1) SA + Mid-Run Stage 3 LNS Re-Painting
    opt_t, opt_l, opt_cnt, start_ok = build_allowed_arrays(I, by_day)
    vmin = np.array([I["vmin"][a] for a in range(1, A + 1)], dtype=np.int32)
    vmax = np.array([I["vmax"][a] for a in range(1, A + 1)], dtype=np.int32)
    E = sorted(I["staff"], key=int)
    min_iv = np.array([math.ceil(I["staff"][e][0] / 15) for e in E], dtype=np.int32)
    max_iv = np.array([I["staff"][e][1] // 15 for e in E], dtype=np.int32)

    best_pen = 10**9
    best_t, best_l = sh_t.copy(), sh_l.copy()
    best_nb, best_ba, best_bl = n_blk.copy(), blk_a.copy(), blk_l.copy()
    cur_t, cur_l = sh_t.copy(), sh_l.copy()
    cur_nb, cur_ba, cur_bl = n_blk.copy(), blk_a.copy(), blk_l.copy()

    mid_rd = sa_rounds // 2
    for rd in range(sa_rounds):
        if rd == 0:
            t_start, t_end, w_hard = 3.0, 0.03, 50
        elif rd == sa_rounds - 1:
            t_start, t_end, w_hard = 2.0, 0.005, 500
        elif rd % 3 == 1:
            t_start, t_end, w_hard = 8.0, 0.05, 45
        elif rd % 3 == 2:
            t_start, t_end, w_hard = 4.0, 0.02, 80
        else:
            t_start, t_end, w_hard = 14.0, 0.05, 45

        fp, bt, bl, bnb, bba, bbl, ucov, cviol, acc = sa_polish_mtask(
            cur_t, cur_l, cur_nb, cur_ba, cur_bl,
            vmin, vmax, min_iv, max_iv, opt_t, opt_l, opt_cnt, start_ok,
            int(sa_iters), t_start, t_end, int(w_hard), int(seed + rd * 997),
        )
        if fp < best_pen:
            best_pen = int(fp)
            best_t, best_l = bt.copy(), bl.copy()
            best_nb, best_ba, best_bl = bnb.copy(), bba.copy(), bbl.copy()

        # Mid-run Stage 3 Global Task Re-Painting LNS on evolved shift envelopes!
        if rd == mid_rd and best_pen < 10**9 and s3_secs > 0:
            _, rnb, rba, rbl, _ = paint_shift_tasks_mip(I, best_t, best_l, secs=min(25.0, s3_secs), workers=workers)
            # Test repainted tasks with a quick cold polish
            fp2, bt2, bl2, bnb2, bba2, bbl2, _, _, _ = sa_polish_mtask(
                best_t, best_l, rnb, rba, rbl,
                vmin, vmax, min_iv, max_iv, opt_t, opt_l, opt_cnt, start_ok,
                int(sa_iters // 2), 2.5, 0.02, 120, int(seed + 77777),
            )
            if fp2 < best_pen:
                best_pen = int(fp2)
                best_t, best_l = bt2.copy(), bl2.copy()
                best_nb, best_ba, best_bl = bnb2.copy(), bba2.copy(), bbl2.copy()

        if best_pen < 10**9:
            cur_t, cur_l = best_t.copy(), best_l.copy()
            cur_nb, cur_ba, cur_bl = best_nb.copy(), best_ba.copy(), best_bl.copy()

    valid = False
    verify_line = ""
    win_path = None
    sha256 = None
    if best_pen < 10**9:
        valid, verify_line, sha256, win_path = save_and_verify_win(
            stem, I, raw_txt, record, best_pen, best_t, best_l, best_nb, best_ba, best_bl
        )

    return dict(
        id=inst_id, stem=stem, A=A, record=record, lp_bound=lp_bound,
        s1_obj=s1_obj, s1_bd=s1_bd, s1_st=s1_st, s1_secs=t_s1,
        s2_viol=s2_viol, s2_st=s2_st, s2_secs=t_s2,
        s3_obj=s3_obj, s3_st=s3_st, s3_secs=t_s3,
        best_pen=best_pen if valid else None,
        vs_rec=(best_pen - record) if valid else None,
        win=bool(valid and best_pen < record),
        verify_line=verify_line, sha256=sha256, win_path=win_path,
        secs=round(time.time() - t0, 1),
    )


def main():
    parser = argparse.ArgumentParser(description="MATSP Multi-Task 4-Stage Solver (B3 & B4)")
    parser.add_argument("--bucket", choices=["smoke", "B3_7_14", "B3_28", "B4_tight", "B4_wide", "single"], default="smoke")
    parser.add_argument("--id", type=int, default=0)
    parser.add_argument("--stem", type=str, default="")
    parser.add_argument("--record", type=int, default=0)
    parser.add_argument("--lp", type=int, default=0)
    parser.add_argument("--seed", type=int, default=101)
    parser.add_argument("--lp-radius", type=int, default=1)
    parser.add_argument("--mem-gb", type=float, default=6.0)
    parser.add_argument("--out-json", type=str, default="")
    parser.add_argument("--s1-secs", type=float, default=60.0)
    parser.add_argument("--s2-secs", type=float, default=45.0)
    parser.add_argument("--s3-secs", type=float, default=30.0)
    parser.add_argument("--sa-rounds", type=int, default=14)
    parser.add_argument("--sa-iters", type=int, default=4_000_000)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--threads", type=int, default=2)
    args = parser.parse_args()

    os.makedirs(LOGS_DIR, exist_ok=True)

    if args.bucket == "single":
        r = solve_instance(
            args.id, args.stem, args.record, args.lp,
            s1_secs=args.s1_secs, s2_secs=args.s2_secs, s3_secs=args.s3_secs,
            sa_rounds=args.sa_rounds, sa_iters=args.sa_iters,
            workers=args.threads, seed=args.seed, lp_radius=args.lp_radius, mem_gb=args.mem_gb,
        )
        if args.out_json:
            with open(args.out_json, "w") as jf:
                jf.write(json.dumps(r))
        return

    if args.bucket == "smoke":
        print("=== SMOKE TEST on #12 (12_7_30_2, B3, A=2, rec=1375) & #23 (23_7_50_4, B4, A=4, rec=1927) ===", flush=True)
        smoke_jobs = [
            (12, "12_7_30_2", 1375, 1217, 30.0, 25.0, 20.0, 6, 2_500_000, 3, 101, 1, 3.0),
            (23, "23_7_50_4", 1927, 1905, 30.0, 25.0, 20.0, 6, 2_500_000, 3, 202, 1, 3.0),
        ]
        with ProcessPoolExecutor(max_workers=2) as ex:
            futs = [ex.submit(solve_instance, *j) for j in smoke_jobs]
            for fut in as_completed(futs):
                print(json.dumps(fut.result(), indent=2), flush=True)
        return

    bmap = {
        "B3_7_14": B3_7_14_TARGETS,
        "B3_28": B3_28_TARGETS,
        "B4_tight": B4_TIGHT_TARGETS,
        "B4_wide": B4_WIDE_TARGETS,
    }
    targets = bmap[args.bucket]
    log_path = os.path.join(LOGS_DIR, f"solve_mtask_{args.bucket}.jsonl")
    t_all = time.time()
    print(f"=== RUNNING {args.bucket} ({len(targets)} targets, {args.workers}w x {args.threads}t) ===", flush=True)
    with ProcessPoolExecutor(max_workers=args.workers) as ex:
        futs = {
            ex.submit(
                solve_instance, iid, stem, rec, lpb,
                args.s1_secs, args.s2_secs, args.s3_secs,
                args.sa_rounds, args.sa_iters, args.threads, 2000 + iid * 19,
                1, 2.5 if args.workers >= 3 else 3.5,
            ): stem
            for iid, stem, rec, lpb in targets
        }
        for fut in as_completed(futs):
            r = fut.result()
            with open(log_path, "a") as lf:
                lf.write(json.dumps(r) + "\n")
            vs = r.get("vs_rec")
            tag = "WIN!!" if r["win"] else (f"{vs:+d}" if vs is not None else f"NO_FEAS({r.get('s1_status', '?')})")
            print(
                f"  [#{r['id']:3d} {r['stem']:12s}] S1={r.get('s1_obj')} (bd={r.get('s1_bd')}, {r.get('s1_secs')}s) | "
                f"S2v={r.get('s2_viol')} ({r.get('s2_secs')}s) | S3={r.get('s3_obj')} ({r.get('s3_secs')}s) | "
                f"FINAL={r['best_pen']} vs rec={r['record']} ({tag}) | {r['secs']}s",
                flush=True,
            )
    print(f"=== DONE {args.bucket} in {round((time.time() - t_all)/60.0, 2)}m wall ===", flush=True)


if __name__ == "__main__":
    main()
