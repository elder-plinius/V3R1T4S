"""
MATSP 1-Task Solver (charlie/solve_1task.py) — 3-Stage Architecture:
  Stage 1: Symmetry-free Aggregate Shift-Count CP-SAT with Exact Hall Rest-Cutoff
           Inequalities + 5-in-6 aggregate bounds + exact linear y^2 epigraph.
  Stage 2: Fast Employee Chain Packer (CP-SAT) threading Stage 1's daily shifts into
           |E| individual schedules obeying 14h rest, 5-in-6 days, and [min, max] hours.
  Stage 3: Ultra-fast Numba O(1) Delta-Eval Simulated Annealing + Greedy Polish
           (resize/slide, add/drop, 2-emp day swap, cross-day move, coupled 2-emp flatten).

Writes verified wins (< record, 0 violations, verify_claim.py PASS) to charlie/wins/<stem>.xml.
DOES NOT modify any existing scout files, runs/, or outbox/.
"""
import argparse
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


B1_TARGETS = [
    (6, "6_7_20_1", 751, 733),
    (7, "7_7_20_1", 727, 704),
    (81, "81_14_20_1", 1510, 1480),
    (82, "82_14_20_1", 1493, 1473),
    (156, "156_28_20_1", 3359, 3278),
    (157, "157_28_20_1", 3074, 2993),
]

B2_TARGETS = [
    (11, "11_7_30_1", 726, 696),
    (86, "86_14_30_1", 1585, 1538),
    (161, "161_28_30_1", 3058, 2955),
]


def load_instance(stem):
    with zipfile.ZipFile(ZIP_PATH) as zf:
        txt = zf.read(f"instances1_225/txt/{stem}.txt").decode("utf-8")
    return matsp.read_instance(txt), txt


def allowed_shifts_by_day(I):
    """Return per-day (0..h) list of valid (t, l) shift tuples."""
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


def _lp_prune_shifts(I, by_day, radius=1):
    """Solve fast continuous LP relaxation of Stage 1 and keep shifts within +-radius of LP support."""
    h, N = I["h"], I["N"]
    D = h + 1
    nE = len(I["staff"])
    vmin, vmax = I["vmin"][1], I["vmax"][1]
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
        T_i = sv.NumVar(float(vmin[i]), float(nE), "")
        T_vars.append(T_i)
        dc = sv.Constraint(0.0, 0.0)
        dc.SetCoefficient(T_i, 1.0)
        if i > 0:
            dc.SetCoefficient(T_vars[i - 1], -1.0)
        for v in start_at_iv[i]:
            dc.SetCoefficient(v, -1.0)
        for v in end_at_iv[i]:
            dc.SetCoefficient(v, 1.0)
        cap = vmax[i]
        if cap < nE:
            ov = sv.Constraint(-sv.infinity(), float(cap))
            ov.SetCoefficient(T_i, 1.0)
            for ex in range(nE - cap):
                z = sv.NumVar(0.0, 1.0, "")
                ov.SetCoefficient(z, -1.0)
                obj.SetCoefficient(z, float(2 * ex + 1))

    st = sv.Solve()
    if st not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        return by_day
    pruned = [[] for _ in range(D)]
    for d_idx in range(D):
        keep = set()
        for k, (t, l) in enumerate(by_day[d_idx]):
            if c_vars[d_idx, k].solution_value() > 1e-6:
                for dt in range(-radius, radius + 1):
                    for dl in range(-radius, radius + 1):
                        keep.add((t + dt, l + dl))
        pruned[d_idx] = [(t, l) for (t, l) in by_day[d_idx] if (t, l) in keep]
        if not pruned[d_idx]:
            pruned[d_idx] = by_day[d_idx]
    return pruned


def solve_stage1_mip(I, by_day, secs=30.0, workers=2, seed=1, lp_radius=1):
    """
    Stage 1: Symmetry-free Aggregate Shift-Count HiGHS MIP with Exact Hall Rest-Cutoff
    Inequalities, 5-in-6 day aggregate cap, and exact sparse piecewise-linear y^2 objective.
    Uses LP-support pruning automatically on 14d/28d horizons (D > 10) for 10x+ speedup.
    """
    h, N = I["h"], I["N"]
    D = h + 1
    if D > 10 and lp_radius is not None:
        by_day = _lp_prune_shifts(I, by_day, radius=lp_radius)
    E = sorted(I["staff"], key=int)
    nE = len(E)
    vmin = I["vmin"][1]
    vmax = I["vmax"][1]
    wmin = sum(math.ceil(b / 15) for b, c in I["staff"].values())
    wmax = sum(c // 15 for b, c in I["staff"].values())
    smin = sum(math.ceil(math.ceil(b / 15) / 40) for b, c in I["staff"].values())
    smax = sum(min((h + 1) - (h + 1) // 6, (c // 15) // 24) for b, c in I["staff"].values())

    sv = pywraplp.Solver.CreateSolver("HIGHS")
    sv.SetTimeLimit(int(secs * 1000))
    sv.SetNumThreads(int(workers))
    sv.SetSolverSpecificParametersAsString("mip_rel_gap = 0.002")

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

    # 5-in-6 consecutive calendar days aggregate bound
    for d0 in range(0, D - 5):
        ct = sv.Constraint(-sv.infinity(), float(5 * nE))
        for d in range(d0, d0 + 6):
            for v in day_totals[d]:
                ct.SetCoefficient(v, 1.0)

    # Exact Hall Marriage Rest-Cutoff inequalities in O(1) nonzeros/row via sparse prefix/suffix sums:
    import bisect
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

    # Exact O(1)-nonzero-per-shift coverage via difference equation:
    #   T[i] - T[i-1] = sum_{t == i} c - sum_{t+l == i} c,  with vmin[i] <= T[i] <= nE
    # Plus exact sparse incremental piecewise-linear y^2 objective
    obj = sv.Objective()
    obj.SetMinimization()
    T_vars = []
    for i in range(N):
        T_i = sv.NumVar(float(vmin[i]), float(nE), "")
        T_vars.append(T_i)
        diff_ct = sv.Constraint(0.0, 0.0)
        diff_ct.SetCoefficient(T_i, 1.0)
        if i > 0:
            diff_ct.SetCoefficient(T_vars[i - 1], -1.0)
        for v in start_at_iv[i]:
            diff_ct.SetCoefficient(v, -1.0)
        for v in end_at_iv[i]:
            diff_ct.SetCoefficient(v, 1.0)

        cap = vmax[i]
        if cap < nE:
            max_ex = nE - cap
            ov_ct = sv.Constraint(-sv.infinity(), float(cap))
            ov_ct.SetCoefficient(T_i, 1.0)
            for ex in range(max_ex):
                z = sv.NumVar(0.0, 1.0, "")
                ov_ct.SetCoefficient(z, -1.0)
                obj.SetCoefficient(z, float(2 * ex + 1))

    st = sv.Solve()
    st_map = {
        pywraplp.Solver.OPTIMAL: "OPTIMAL",
        pywraplp.Solver.FEASIBLE: "FEASIBLE",
        pywraplp.Solver.INFEASIBLE: "INFEASIBLE",
        pywraplp.Solver.NOT_SOLVED: "NOT_SOLVED",
    }
    st_name = st_map.get(st, str(st))
    if st not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        return None, None, None, st_name

    shifts_by_day = [[] for _ in range(D)]
    for d_idx in range(D):
        for k, (t, l) in enumerate(by_day[d_idx]):
            cnt = int(round(c_vars[d_idx, k].solution_value()))
            for _ in range(cnt):
                shifts_by_day[d_idx].append((t, l))
    return int(round(obj.Value())), int(math.ceil(obj.BestBound() - 1e-6)), shifts_by_day, st_name


def pack_employee_chains(I, shifts_by_day, secs=25.0, workers=2, seed=1):
    """
    Stage 2: Assign Stage 1's daily shifts to individual employees E respecting
    <=1 shift/day, 14h rest (exact cutoff inequalities), and 5-in-6 days, minimizing
    total [min_e, max_e] contract violation (0 = immediately checker-valid!).
    """
    h = I["h"]
    D = h + 1
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

    # 5-in-6 days per employee
    for ei in range(nE):
        for d0 in range(0, D - 5):
            m.Add(sum(work[ei, d] for d in range(d0, d0 + 6)) <= 5)

    # Exact 14h rest per employee via end-time cutoffs (linear size, zero quadratic blowup)
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

    # Soft [min_iv, max_iv] contract violation
    viols = []
    for ei in range(nE):
        tot = sum(shifts_by_day[d][k][1] * x[ei, d, k] for d in range(D) for k in range(len(shifts_by_day[d])))
        u_v = m.NewIntVar(0, min_iv[ei], "")
        o_v = m.NewIntVar(0, D * 40, "")
        m.Add(u_v >= min_iv[ei] - tot)
        m.Add(o_v >= tot - max_iv[ei])
        viols.append(u_v)
        viols.append(o_v)

    m.Minimize(sum(viols))
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = float(secs)
    sv.parameters.num_workers = int(workers)
    sv.parameters.random_seed = int(seed)
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, None, None, sv.StatusName(st)

    sh_t = np.full((nE, D), -1, dtype=np.int32)
    sh_l = np.zeros((nE, D), dtype=np.int32)
    for d in range(D):
        for k, (t, l) in enumerate(shifts_by_day[d]):
            for ei in range(nE):
                if sv.Value(x[ei, d, k]):
                    sh_t[ei, d] = t
                    sh_l[ei, d] = l
                    break
    return int(round(sv.ObjectiveValue())), sh_t, sh_l, sv.StatusName(st)


def build_allowed_arrays(I, by_day):
    """Pack per-day allowed starts & valid length ranges into flat Numba arrays."""
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
def _interval_cost(c, vmin_i, vmax_i, W_HARD):
    cost = 0
    if c < vmin_i:
        d = vmin_i - c
        cost += W_HARD * d * d
    elif c > vmax_i:
        d = c - vmax_i
        cost += d * d
    return cost


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
    """Check if setting sh_l[e, d] > 0 violates 5-in-6 working days."""
    lo = d - 5 if d - 5 > 0 else 0
    hi = d if d + 5 < D else D - 6
    for d0 in range(lo, hi + 1):
        cnt = 1  # counting day d as active
        for k in range(d0, d0 + 6):
            if k != d and sh_l[e, k] > 0:
                cnt += 1
        if cnt > 5:
            return False
    return True


@njit(cache=True)
def sa_polish_1task(sh_t_in, sh_l_in, vmin, vmax, min_iv, max_iv, opt_t, opt_l, opt_cnt, start_ok,
                    n_iters, temp_start, temp_end, w_hard, seed):
    """
    Ultra-fast Numba O(1) Delta-Eval Simulated Annealing for A=1 MATSP.
    Always maintains 14h rest and 5-in-6 hard; drives under-cover and contract violations
    to 0 with w_hard and minimizes sum_i max(0, cov[i] - vmax[i])^2.
    """
    np.random.seed(seed)
    nE, D = sh_t_in.shape
    N = len(vmin)
    W_HARD = w_hard

    sh_t = sh_t_in.copy()
    sh_l = sh_l_in.copy()
    cov = np.zeros(N, dtype=np.int32)
    emp_w = np.zeros(nE, dtype=np.int32)

    for e in range(nE):
        for d in range(D):
            l = sh_l[e, d]
            if l > 0:
                t = sh_t[e, d]
                emp_w[e] += l
                for i in range(t, t + l):
                    cov[i] += 1

    cur_pen = 0
    cur_ucov = 0
    for i in range(N):
        c = cov[i]
        if c < vmin[i]:
            d = vmin[i] - c
            cur_ucov += d * d
        elif c > vmax[i]:
            d = c - vmax[i]
            cur_pen += d * d

    cur_cviol = 0
    for e in range(nE):
        cur_cviol += _emp_viol(emp_w[e], min_iv[e], max_iv[e])

    cur_obj = W_HARD * (cur_ucov + cur_cviol) + cur_pen

    best_feas_pen = 1000000000
    best_t = sh_t.copy()
    best_l = sh_l.copy()
    if cur_ucov == 0 and cur_cviol == 0:
        best_feas_pen = cur_pen

    # Exponential cooling factor
    cool = (temp_end / temp_start) ** (1.0 / max(1, n_iters))
    temp = temp_start
    accepted = 0

    for it in range(n_iters):
        r = np.random.random()

        if r < 0.42:
            # Move 1: Modify shift (surgical +-1/+-2 resize/slide, random replace, or add/drop) on (e, d)
            e = np.random.randint(0, nE)
            d = np.random.randint(0, D)
            n_o = opt_cnt[d]
            if n_o == 0:
                temp *= cool
                continue
            old_t = sh_t[e, d]
            old_l = sh_l[e, d]

            if old_l > 0 and np.random.random() < 0.08:
                # Drop shift
                new_t = -1
                new_l = 0
            else:
                if old_l == 0:
                    if not _five_in_six_ok(sh_l, e, d, D):
                        temp *= cool
                        continue
                    idx_o = np.random.randint(0, n_o)
                    new_t = opt_t[d, idx_o]
                    new_l = opt_l[d, idx_o]
                elif np.random.random() < 0.72:
                    # Surgical local nudge: resize (+-1/2), slide (+-1/2), or move start keeping end fixed
                    sub = np.random.randint(0, 3)
                    step = 1 if np.random.random() < 0.75 else 2
                    if np.random.random() < 0.5:
                        step = -step
                    if sub == 0:
                        new_t = old_t
                        new_l = old_l + step
                    elif sub == 1:
                        new_t = old_t + step
                        new_l = old_l
                    else:
                        new_t = old_t + step
                        new_l = old_l - step
                    if new_l < 24 or new_l > 40 or new_t < 0 or new_t + new_l > N or start_ok[d, new_t] == 0:
                        temp *= cool
                        continue
                else:
                    idx_o = np.random.randint(0, n_o)
                    new_t = opt_t[d, idx_o]
                    new_l = opt_l[d, idx_o]
                if new_t == old_t and new_l == old_l:
                    temp *= cool
                    continue
                if not _rest_ok(sh_t, sh_l, e, d, new_t, new_l, D):
                    temp *= cool
                    continue

            # Compute exact O(1) delta
            old_ev = _emp_viol(emp_w[e], min_iv[e], max_iv[e])
            new_ew = emp_w[e] - old_l + new_l
            new_ev = _emp_viol(new_ew, min_iv[e], max_iv[e])
            d_cviol = new_ev - old_ev

            d_pen = 0
            d_ucov = 0
            if old_l > 0 and new_l > 0:
                # Apply delta only on symmetric difference of [old_t, old_t+old_l) and [new_t, new_t+new_l)
                a0, a1 = old_t, old_t + old_l
                b0, b1 = new_t, new_t + new_l
                for i in range(a0, a1):
                    if i < b0 or i >= b1:
                        c = cov[i]
                        if c <= vmin[i]:
                            d_ucov += (vmin[i] - (c - 1)) ** 2 - (vmin[i] - c) ** 2
                        if c > vmax[i]:
                            d_pen += (c - 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2
                for i in range(b0, b1):
                    if i < a0 or i >= a1:
                        c = cov[i]
                        if c < vmin[i]:
                            d_ucov += (vmin[i] - (c + 1)) ** 2 - (vmin[i] - c) ** 2
                        if c >= vmax[i]:
                            d_pen += (c + 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2
            elif old_l > 0:
                for i in range(old_t, old_t + old_l):
                    c = cov[i]
                    if c <= vmin[i]:
                        d_ucov += (vmin[i] - (c - 1)) ** 2 - (vmin[i] - c) ** 2
                    if c > vmax[i]:
                        d_pen += (c - 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2
            else:
                for i in range(new_t, new_t + new_l):
                    c = cov[i]
                    if c < vmin[i]:
                        d_ucov += (vmin[i] - (c + 1)) ** 2 - (vmin[i] - c) ** 2
                    if c >= vmax[i]:
                        d_pen += (c + 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2

            d_obj = W_HARD * (d_ucov + d_cviol) + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                if old_l > 0:
                    for i in range(old_t, old_t + old_l):
                        cov[i] -= 1
                if new_l > 0:
                    for i in range(new_t, new_t + new_l):
                        cov[i] += 1
                sh_t[e, d] = new_t
                sh_l[e, d] = new_l
                emp_w[e] = new_ew
                cur_pen += d_pen
                cur_ucov += d_ucov
                cur_cviol += d_cviol
                cur_obj += d_obj
                accepted += 1
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy()
                    best_l = sh_l.copy()

        elif r < 0.62:
            # Move 2: Swap day d between two employees (e1, e2) — zero cover delta, rebalances contracts & rest!
            e1 = np.random.randint(0, nE)
            e2 = np.random.randint(0, nE - 1)
            if e2 >= e1:
                e2 += 1
            d = np.random.randint(0, D)
            t1, l1 = sh_t[e1, d], sh_l[e1, d]
            t2, l2 = sh_t[e2, d], sh_l[e2, d]
            if t1 == t2 and l1 == l2:
                temp *= cool
                continue
            if l2 > 0 and l1 == 0 and not _five_in_six_ok(sh_l, e1, d, D):
                temp *= cool
                continue
            if l1 > 0 and l2 == 0 and not _five_in_six_ok(sh_l, e2, d, D):
                temp *= cool
                continue
            if not _rest_ok(sh_t, sh_l, e1, d, t2, l2, D):
                temp *= cool
                continue
            if not _rest_ok(sh_t, sh_l, e2, d, t1, l1, D):
                temp *= cool
                continue

            old_ev = _emp_viol(emp_w[e1], min_iv[e1], max_iv[e1]) + _emp_viol(emp_w[e2], min_iv[e2], max_iv[e2])
            nw1 = emp_w[e1] - l1 + l2
            nw2 = emp_w[e2] - l2 + l1
            new_ev = _emp_viol(nw1, min_iv[e1], max_iv[e1]) + _emp_viol(nw2, min_iv[e2], max_iv[e2])
            d_cviol = new_ev - old_ev
            d_obj = W_HARD * d_cviol
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e1, d], sh_l[e1, d] = t2, l2
                sh_t[e2, d], sh_l[e2, d] = t1, l1
                emp_w[e1] = nw1
                emp_w[e2] = nw2
                cur_cviol += d_cviol
                cur_obj += d_obj
                accepted += 1
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy()
                    best_l = sh_l.copy()

        elif r < 0.74:
            # Move 3: Move shift for one employee from working day d1 -> off day d2
            e = np.random.randint(0, nE)
            d1 = np.random.randint(0, D)
            d2 = np.random.randint(0, D)
            if d1 == d2 or sh_l[e, d1] == 0 or sh_l[e, d2] > 0 or opt_cnt[d2] == 0:
                temp *= cool
                continue
            old_t, old_l = sh_t[e, d1], sh_l[e, d1]
            # Temporarily drop d1 to check 5-in-6 and rest on d2
            sh_l[e, d1] = 0
            ok56 = _five_in_six_ok(sh_l, e, d2, D)
            if not ok56:
                sh_l[e, d1] = old_l
                temp *= cool
                continue
            idx_o = np.random.randint(0, opt_cnt[d2])
            new_t = opt_t[d2, idx_o]
            new_l = opt_l[d2, idx_o]
            if not _rest_ok(sh_t, sh_l, e, d2, new_t, new_l, D):
                sh_l[e, d1] = old_l
                temp *= cool
                continue
            sh_l[e, d1] = old_l  # restore before delta eval

            old_ev = _emp_viol(emp_w[e], min_iv[e], max_iv[e])
            new_ew = emp_w[e] - old_l + new_l
            d_cviol = _emp_viol(new_ew, min_iv[e], max_iv[e]) - old_ev

            d_pen = 0
            d_ucov = 0
            # Remove d1 temporarily from cov to handle any overnight overlap cleanly
            for i in range(old_t, old_t + old_l):
                c = cov[i]
                if c <= vmin[i]:
                    d_ucov += (vmin[i] - (c - 1)) ** 2 - (vmin[i] - c) ** 2
                if c > vmax[i]:
                    d_pen += (c - 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2
                cov[i] = c - 1
            for i in range(new_t, new_t + new_l):
                c = cov[i]
                if c < vmin[i]:
                    d_ucov += (vmin[i] - (c + 1)) ** 2 - (vmin[i] - c) ** 2
                if c >= vmax[i]:
                    d_pen += (c + 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2
                cov[i] = c + 1

            d_obj = W_HARD * (d_ucov + d_cviol) + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e, d1] = -1
                sh_l[e, d1] = 0
                sh_t[e, d2] = new_t
                sh_l[e, d2] = new_l
                emp_w[e] = new_ew
                cur_pen += d_pen
                cur_ucov += d_ucov
                cur_cviol += d_cviol
                cur_obj += d_obj
                accepted += 1
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy()
                    best_l = sh_l.copy()
            else:
                # Revert cov
                for i in range(new_t, new_t + new_l):
                    cov[i] -= 1
                for i in range(old_t, old_t + old_l):
                    cov[i] += 1

        elif r < 0.90:
            # Move 4: Same-employee 2-day length transfer (+step on d1, -step on d2) — ZERO contract delta!
            e = np.random.randint(0, nE)
            d1 = np.random.randint(0, D)
            d2 = np.random.randint(0, D - 1)
            if d2 >= d1:
                d2 += 1
            ot1, ol1 = sh_t[e, d1], sh_l[e, d1]
            ot2, ol2 = sh_t[e, d2], sh_l[e, d2]
            if ol1 == 0 or ol2 == 0:
                temp *= cool
                continue
            step = 1 if np.random.random() < 0.75 else 2
            # Grow d1 by +step (at start or end), shrink d2 by -step (at start or end)
            if np.random.random() < 0.5:
                nt1, nl1 = ot1, ol1 + step
            else:
                nt1, nl1 = ot1 - step, ol1 + step
            if np.random.random() < 0.5:
                nt2, nl2 = ot2, ol2 - step
            else:
                nt2, nl2 = ot2 + step, ol2 - step
            if nl1 > 40 or nl2 < 24 or nt1 < 0 or nt1 + nl1 > N or nt2 < 0 or nt2 + nl2 > N:
                temp *= cool
                continue
            if start_ok[d1, nt1] == 0 or start_ok[d2, nt2] == 0:
                temp *= cool
                continue
            # Check rest with both changes applied temporarily
            sh_t[e, d1], sh_l[e, d1] = nt1, nl1
            sh_t[e, d2], sh_l[e, d2] = nt2, nl2
            ok_r = _rest_ok(sh_t, sh_l, e, d1, nt1, nl1, D) and _rest_ok(sh_t, sh_l, e, d2, nt2, nl2, D)
            sh_t[e, d1], sh_l[e, d1] = ot1, ol1
            sh_t[e, d2], sh_l[e, d2] = ot2, ol2
            if not ok_r:
                temp *= cool
                continue

            d_pen = 0
            d_ucov = 0
            # Apply sequentially on cov and revert if rejected
            for i in range(ot1, ot1 + ol1):
                c = cov[i]
                if c <= vmin[i]: d_ucov += (vmin[i] - (c - 1)) ** 2 - (vmin[i] - c) ** 2
                if c > vmax[i]: d_pen += (c - 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2
                cov[i] = c - 1
            for i in range(ot2, ot2 + ol2):
                c = cov[i]
                if c <= vmin[i]: d_ucov += (vmin[i] - (c - 1)) ** 2 - (vmin[i] - c) ** 2
                if c > vmax[i]: d_pen += (c - 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2
                cov[i] = c - 1
            for i in range(nt1, nt1 + nl1):
                c = cov[i]
                if c < vmin[i]: d_ucov += (vmin[i] - (c + 1)) ** 2 - (vmin[i] - c) ** 2
                if c >= vmax[i]: d_pen += (c + 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2
                cov[i] = c + 1
            for i in range(nt2, nt2 + nl2):
                c = cov[i]
                if c < vmin[i]: d_ucov += (vmin[i] - (c + 1)) ** 2 - (vmin[i] - c) ** 2
                if c >= vmax[i]: d_pen += (c + 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2
                cov[i] = c + 1

            d_obj = W_HARD * d_ucov + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e, d1], sh_l[e, d1] = nt1, nl1
                sh_t[e, d2], sh_l[e, d2] = nt2, nl2
                cur_pen += d_pen
                cur_ucov += d_ucov
                cur_obj += d_obj
                accepted += 1
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy()
                    best_l = sh_l.copy()
            else:
                for i in range(nt2, nt2 + nl2): cov[i] -= 1
                for i in range(nt1, nt1 + nl1): cov[i] -= 1
                for i in range(ot2, ot2 + ol2): cov[i] += 1
                for i in range(ot1, ot1 + ol1): cov[i] += 1

        else:
            # Move 5: Coupled 2-employee same-day move (adjust e1 and e2 together to flatten a spike!)
            d = np.random.randint(0, D)
            n_o = opt_cnt[d]
            if n_o == 0:
                temp *= cool
                continue
            e1 = np.random.randint(0, nE)
            e2 = np.random.randint(0, nE - 1)
            if e2 >= e1:
                e2 += 1
            ot1, ol1 = sh_t[e1, d], sh_l[e1, d]
            ot2, ol2 = sh_t[e2, d], sh_l[e2, d]
            if ol1 == 0 or ol2 == 0:
                temp *= cool
                continue
            idx1 = np.random.randint(0, n_o)
            idx2 = np.random.randint(0, n_o)
            nt1, nl1 = opt_t[d, idx1], opt_l[d, idx1]
            nt2, nl2 = opt_t[d, idx2], opt_l[d, idx2]
            if not _rest_ok(sh_t, sh_l, e1, d, nt1, nl1, D) or not _rest_ok(sh_t, sh_l, e2, d, nt2, nl2, D):
                temp *= cool
                continue

            old_ev = _emp_viol(emp_w[e1], min_iv[e1], max_iv[e1]) + _emp_viol(emp_w[e2], min_iv[e2], max_iv[e2])
            nw1 = emp_w[e1] - ol1 + nl1
            nw2 = emp_w[e2] - ol2 + nl2
            d_cviol = (_emp_viol(nw1, min_iv[e1], max_iv[e1]) + _emp_viol(nw2, min_iv[e2], max_iv[e2])) - old_ev

            d_pen = 0
            d_ucov = 0
            # Apply sequentially on cov and revert if rejected
            for i in range(ot1, ot1 + ol1):
                c = cov[i]
                if c <= vmin[i]: d_ucov += (vmin[i] - (c - 1)) ** 2 - (vmin[i] - c) ** 2
                if c > vmax[i]: d_pen += (c - 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2
                cov[i] = c - 1
            for i in range(ot2, ot2 + ol2):
                c = cov[i]
                if c <= vmin[i]: d_ucov += (vmin[i] - (c - 1)) ** 2 - (vmin[i] - c) ** 2
                if c > vmax[i]: d_pen += (c - 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2
                cov[i] = c - 1
            for i in range(nt1, nt1 + nl1):
                c = cov[i]
                if c < vmin[i]: d_ucov += (vmin[i] - (c + 1)) ** 2 - (vmin[i] - c) ** 2
                if c >= vmax[i]: d_pen += (c + 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2
                cov[i] = c + 1
            for i in range(nt2, nt2 + nl2):
                c = cov[i]
                if c < vmin[i]: d_ucov += (vmin[i] - (c + 1)) ** 2 - (vmin[i] - c) ** 2
                if c >= vmax[i]: d_pen += (c + 1 - vmax[i]) ** 2 - (c - vmax[i]) ** 2
                cov[i] = c + 1

            d_obj = W_HARD * (d_ucov + d_cviol) + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e1, d], sh_l[e1, d] = nt1, nl1
                sh_t[e2, d], sh_l[e2, d] = nt2, nl2
                emp_w[e1] = nw1
                emp_w[e2] = nw2
                cur_pen += d_pen
                cur_ucov += d_ucov
                cur_cviol += d_cviol
                cur_obj += d_obj
                accepted += 1
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy()
                    best_l = sh_l.copy()
            else:
                for i in range(nt2, nt2 + nl2): cov[i] -= 1
                for i in range(nt1, nt1 + nl1): cov[i] -= 1
                for i in range(ot2, ot2 + ol2): cov[i] += 1
                for i in range(ot1, ot1 + ol1): cov[i] += 1

        temp *= cool

    return best_feas_pen, best_t, best_l, cur_ucov, cur_cviol, accepted


def to_xml(stem, I, sh_t, sh_l, pen):
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
            out.append(
                f"<Shift><Day>{d}</Day><Start>{mm // 60:02d}:{mm % 60:02d}:00</Start>"
                f"<Task><ID>1</ID><Length>{l * 15}</Length></Task></Shift>"
            )
        out.append("</Employee>")
    out.append("</Solution>")
    return "\n".join(out) + "\n"


def solve_instance(inst_id, stem, record, lp_bound, s1_secs=35.0, s2_secs=25.0, sa_rounds=8, sa_iters=3_000_000, workers=2, seed=101, lp_radius=1):
    lim = 4 * 1024 * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    I, raw_txt = load_instance(stem)
    by_day = allowed_shifts_by_day(I)

    # Stage 1: Aggregate Shift-Count MIP with Hall Rest Cutoffs
    s1_obj, s1_bd, shifts_by_day, s1_st = solve_stage1_mip(I, by_day, secs=s1_secs, workers=workers, seed=seed, lp_radius=lp_radius)
    if shifts_by_day is None and I["h"] + 1 > 10 and lp_radius > 0:
        s1_obj, s1_bd, shifts_by_day, s1_st = solve_stage1_mip(I, by_day, secs=s1_secs, workers=workers, seed=seed, lp_radius=0)
    t_s1 = round(time.time() - t0, 1)
    if shifts_by_day is None:
        return dict(id=inst_id, stem=stem, record=record, lp_bound=lp_bound, s1_status=s1_st, best_pen=None, win=False, secs=t_s1)

    # Stage 2: Employee Chain Packer
    t1 = time.time()
    s2_viol, sh_t, sh_l, s2_st = pack_employee_chains(I, shifts_by_day, secs=s2_secs, workers=workers, seed=seed + 13)
    t_s2 = round(time.time() - t1, 1)
    if sh_t is None:
        return dict(id=inst_id, stem=stem, record=record, lp_bound=lp_bound, s1_obj=s1_obj, s1_bd=s1_bd, s2_status=s2_st, best_pen=None, win=False, secs=round(time.time() - t0, 1))

    # Stage 3: Fast Numba O(1) SA Polish (Round 0 cold surgical repair, then gentle reheat rounds)
    opt_t, opt_l, opt_cnt, start_ok = build_allowed_arrays(I, by_day)
    vmin = np.array(I["vmin"][1], dtype=np.int32)
    vmax = np.array(I["vmax"][1], dtype=np.int32)
    E = sorted(I["staff"], key=int)
    min_iv = np.array([math.ceil(I["staff"][e][0] / 15) for e in E], dtype=np.int32)
    max_iv = np.array([I["staff"][e][1] // 15 for e in E], dtype=np.int32)

    best_pen = 10**9
    best_t = sh_t.copy()
    best_l = sh_l.copy()
    cur_t = sh_t.copy()
    cur_l = sh_l.copy()

    # Check if Stage 2 is already 0-violation feasible!
    if s2_viol == 0:
        best_pen = s1_obj

    for rd in range(sa_rounds):
        if rd == 0:
            t_start, t_end, w_hard = 2.0, 0.02, 40
        elif rd == sa_rounds - 1:
            t_start, t_end, w_hard = 3.0, 0.02, 300
        elif rd % 3 == 1:
            t_start, t_end, w_hard = 6.0, 0.05, 35
        elif rd % 3 == 2:
            t_start, t_end, w_hard = 3.0, 0.02, 60
        else:
            t_start, t_end, w_hard = 10.0, 0.05, 35
        fp, bt, bl, ucov, cviol, acc = sa_polish_1task(
            cur_t, cur_l, vmin, vmax, min_iv, max_iv, opt_t, opt_l, opt_cnt, start_ok,
            int(sa_iters), t_start, t_end, int(w_hard), int(seed + rd * 997),
        )
        if fp < best_pen:
            best_pen = int(fp)
            best_t = bt.copy()
            best_l = bl.copy()
        if best_pen < 10**9:
            cur_t = best_t.copy()
            cur_l = best_l.copy()

    # Validate best feasible roster
    valid = False
    verify_line = ""
    win_path = None
    sha256 = None
    if best_pen < 10**9:
        xml_txt = to_xml(stem, I, best_t, best_l, best_pen)
        S_chk, _ = matsp.read_solution(xml_txt)
        bad, pen_chk = matsp.evaluate(I, S_chk)
        assert len(bad) == 0 and pen_chk == best_pen, f"matsp.evaluate FAIL {stem}: bad={bad[:3]} pen={pen_chk} vs {best_pen}"
        valid = True

        if best_pen < record:
            os.makedirs(WINS_DIR, exist_ok=True)
            win_path = os.path.join(WINS_DIR, f"{stem}.xml")
            write_it = True
            if os.path.exists(win_path):
                with open(win_path) as ef:
                    old_s, _ = matsp.read_solution(ef.read())
                old_bad, old_pen = matsp.evaluate(I, old_s)
                if len(old_bad) == 0 and old_pen <= best_pen:
                    write_it = False
            if write_it:
                with open(win_path, "w") as wf:
                    wf.write(xml_txt)
            with open(win_path) as rf:
                final_xml = rf.read()
            sha256 = hashlib.sha256(final_xml.encode("utf-8")).hexdigest()
            # Run standalone claimkit/verify_claim.py
            tmp_inst = os.path.join(LOGS_DIR, f"_tmp_{stem}_{os.getpid()}.txt")
            os.makedirs(LOGS_DIR, exist_ok=True)
            with open(tmp_inst, "w") as tf:
                tf.write(raw_txt)
            proc = subprocess.run(
                [sys.executable, VERIFY_SCRIPT, tmp_inst, win_path, str(record)],
                capture_output=True, text=True, check=False,
            )
            os.remove(tmp_inst)
            verify_line = (proc.stdout + proc.stderr).strip()
            assert proc.returncode == 0 and "PASS" in verify_line, f"verify_claim FAIL {stem}: {verify_line}"

    return dict(
        id=inst_id, stem=stem, record=record, lp_bound=lp_bound,
        s1_obj=s1_obj, s1_bd=s1_bd, s1_st=s1_st, s1_secs=t_s1,
        s2_viol=s2_viol, s2_st=s2_st, s2_secs=t_s2,
        best_pen=best_pen if valid else None,
        vs_rec=(best_pen - record) if valid else None,
        win=bool(valid and best_pen < record),
        verify_line=verify_line, sha256=sha256, win_path=win_path,
        secs=round(time.time() - t0, 1),
    )


def main():
    parser = argparse.ArgumentParser(description="MATSP 1-Task 3-Stage Solver (B1 & B2)")
    parser.add_argument("--bucket", choices=["smoke", "B1", "B2", "all"], default="smoke")
    parser.add_argument("--s1-secs", type=float, default=45.0)
    parser.add_argument("--s2-secs", type=float, default=30.0)
    parser.add_argument("--sa-rounds", type=int, default=12)
    parser.add_argument("--sa-iters", type=int, default=4_000_000)
    args = parser.parse_args()

    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, f"solve_1task_{args.bucket}.jsonl")

    if args.bucket == "smoke":
        print("=== SMOKE TEST on #6 (6_7_20_1, record=751, LP=733) ===", flush=True)
        r = solve_instance(6, "6_7_20_1", 751, 733, s1_secs=20.0, s2_secs=15.0, sa_rounds=4, sa_iters=2_000_000, workers=4, seed=101)
        print(json.dumps(r, indent=2), flush=True)
        return

    targets = B1_TARGETS if args.bucket == "B1" else (B2_TARGETS if args.bucket == "B2" else B1_TARGETS + B2_TARGETS)
    with open(log_path, "w"):
        pass

    t_all = time.time()
    print(f"=== RUNNING {args.bucket} ({len(targets)} targets, 3w x 2t) ===", flush=True)
    with ProcessPoolExecutor(max_workers=3) as ex:
        futs = {
            ex.submit(solve_instance, iid, stem, rec, lpb, args.s1_secs, args.s2_secs, args.sa_rounds, args.sa_iters, 2, 1000 + iid * 17): stem
            for iid, stem, rec, lpb in targets
        }
        for fut in as_completed(futs):
            r = fut.result()
            with open(log_path, "a") as lf:
                lf.write(json.dumps(r) + "\n")
            vs = r.get("vs_rec")
            tag = "WIN!!" if r["win"] else (f"{vs:+d}" if vs is not None else f"NO_FEAS({r.get('s1_status', r.get('s2_status', '?'))})")
            print(
                f"  [#{r['id']:3d} {r['stem']:12s}] S1={r.get('s1_obj')} (bd={r.get('s1_bd')}, {r.get('s1_secs')}s) | "
                f"S2_viol={r.get('s2_viol')} ({r.get('s2_secs')}s) | FINAL={r['best_pen']} vs rec={r['record']} ({tag}) | {r['secs']}s",
                flush=True,
            )
    print(f"=== DONE {args.bucket} in {round((time.time() - t_all)/60.0, 2)}m wall ===", flush=True)


if __name__ == "__main__":
    main()
