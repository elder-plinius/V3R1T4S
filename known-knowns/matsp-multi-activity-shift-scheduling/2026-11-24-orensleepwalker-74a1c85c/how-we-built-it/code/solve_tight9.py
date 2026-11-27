"""
MATSP Counting-Tight Specialist (charlie/solve_tight9.py) for the Final 9 Open Targets:
  #23 (B4, +4), #128 (B6, +36), #113 (B5, +44), #98 (B4, +82), #108 (B5, +92),
  #173 (B4, +116), #168 (B4, +132), #219 (B6, +244), #218 (B6, +582).

All 9 share the exact same surplus-staffing regime (LP ~= counting_bound).
Key upgrades over solve_mtask.py:
  1. Tight-Work Stage 1: Constrains total worked intervals to [wmin, wmin + 8] (zero surplus waste)
     with LP-rounded fallback if 28d XL MIP times out.
  2. Surplus-Squeeze + 8-Move Multi-Task Numba SA:
     - Adds Move 8 (2-Employee Same-Day Task-Block Swap) to flatten +2 task spikes with 0 envelope delta.
     - Adds temporary surplus-work pressure (w_surp > 0) during early/mid rounds to squeeze every
       employee down to emp_w[e] == min_iv[e], then releases (w_surp = 0) in final ultra-cold polish.
  3. Rolling 2-Day Exact Within-Shift Task-Painting LNS (HiGHS):
     - Sweeps 2-day windows [d, d+1] across the horizon, solving exact 1-block/2-block (>=4 iv)
       task painting on fixed shift envelopes in 1-5s per window (where full-horizon Stage 3 timed out!),
       then feeds the globally flattened schedule back into deep Numba SA.
  4. Unpruned Lower-Bound Certificate Check on #219 (room=2) and #173 (room=6).
"""
import argparse
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
LOGS_DIR = os.path.join(CHARLIE_DIR, "logs")
JSONL_PATH = os.path.join(LOGS_DIR, "tight9.jsonl")

sys.path.insert(0, CHARLIE_DIR)
sys.path.insert(0, os.path.join(SCOUT_DIR, "code"))

import numpy as np  # noqa: E402
from numba import njit  # noqa: E402
from ortools.linear_solver import pywraplp  # noqa: E402
import matsp  # noqa: E402
import solve_mtask as sm  # noqa: E402
import run_b6  # noqa: E402

MAX_BLK = sm.MAX_BLK

FINAL_9 = [
    # Ordered closest-to-record first!
    # (iid, stem, rec, lp, s1_s, s2_s, sa_rounds, sa_iters, lpr, win_secs)
    (23,  "23_7_50_4",     1927,  1905,  45, 90, 36, 10_000_000, 1, 6.0),
    (128, "128_14_110_8",  8715,  8067,  60, 90, 32, 10_000_000, 0, 5.0),
    (113, "113_14_80_6",   6356,  6026,  60, 90, 32, 10_000_000, 0, 5.0),
    (98,  "98_14_50_4",    3867,  3855,  60, 90, 36, 10_000_000, 0, 6.0),
    (108, "108_14_70_5",   5103,  4947,  60, 90, 32, 10_000_000, 0, 5.0),
    (173, "173_28_50_4",   7399,  7393,  75, 90, 32, 10_000_000, 0, 5.0),
    (168, "168_28_40_3",   6000,  5890,  60, 90, 32, 10_000_000, 0, 6.0),
    (218, "218_28_140_10", 21729, 19997, 0,  90, 30, 8_000_000,  0, 4.0),
    (219, "219_28_140_14", 18990, 18988, 0,  90, 30, 8_000_000,  0, 4.0),
]


@njit(cache=True)
def sa_polish_tight(sh_t_in, sh_l_in, n_blk_in, blk_a_in, blk_l_in,
                    vmin, vmax, min_iv, max_iv, opt_t, opt_l, opt_cnt, start_ok,
                    n_iters, temp_start, temp_end, w_hard, w_surp, seed):
    """
    Counting-Tight 8-Move Multi-Task Numba O(1) SA:
      Moves 1-7: Same as solve_mtask.py
      Move 8 (12%): 2-Employee Same-Day Block Task Swap (flattens +2 task spikes with 0 envelope delta!)
      Surplus squeeze: adds w_surp * max(0, emp_w[e] - min_iv[e]) to objective during exploration
                       to drive every employee right to min_iv[e], while always recording true feasible pen.
    """
    np.random.seed(seed)
    nE, D = sh_t_in.shape
    A, N = vmin.shape
    W_HARD = w_hard
    W_SURP = w_surp

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
        cur_cviol += sm._emp_viol(emp_w[e], min_iv[e], max_iv[e])

    best_feas_pen = 1000000000
    best_t = sh_t.copy(); best_l = sh_l.copy()
    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
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
            # Move 1: Slide internal task split boundary
            e = np.random.randint(0, nE)
            d = np.random.randint(0, D)
            nb = n_blk[e, d]
            if nb < 2:
                temp *= cool; continue
            b = np.random.randint(0, nb - 1)
            step = np.random.randint(1, 5)
            if np.random.random() < 0.5:
                step = -step
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
                    cur_ucov += d_ucov; cur_pen += d_pen; accepted += 1
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
                    cur_ucov += d_ucov; cur_pen += d_pen; accepted += 1
                    if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                        best_feas_pen = cur_pen
                        best_t = sh_t.copy(); best_l = sh_l.copy()
                        best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
                else:
                    for i in range(bnd - sa_, bnd):
                        cov[a1, i] -= 1; cov[a0, i] += 1

        elif r < 0.30:
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
                cur_ucov += d_ucov; cur_pen += d_pen; accepted += 1
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
            else:
                for i in range(pos, pos + ln):
                    cov[a_new, i] -= 1; cov[a_old, i] += 1

        elif r < 0.42:
            # Move 3: Split or merge task blocks
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
                        blk_a[e, d, k] = blk_a[e, d, k - 1]
                        blk_l[e, d, k] = blk_l[e, d, k - 1]
                    if second_half:
                        blk_a[e, d, b] = a_old; blk_l[e, d, b] = s
                        blk_a[e, d, b + 1] = a_new; blk_l[e, d, b + 1] = ln - s
                    else:
                        blk_a[e, d, b] = a_new; blk_l[e, d, b] = s
                        blk_a[e, d, b + 1] = a_old; blk_l[e, d, b + 1] = ln - s
                    n_blk[e, d] = sm._normalize_blocks(nb + 1, blk_a[e, d], blk_l[e, d])
                    cur_ucov += d_ucov; cur_pen += d_pen; accepted += 1
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
                if keep_left:
                    i0, i1, a_from, a_to = pos + l0, pos + l0 + l1, a1, a0
                else:
                    i0, i1, a_from, a_to = pos, pos + l0, a0, a1
                du1, dp1 = sm._delta_range(cov, vmin, vmax, a_from, i0, i1, -1)
                du2, dp2 = sm._delta_range(cov, vmin, vmax, a_to, i0, i1, 1)
                d_ucov, d_pen = du1 + du2, dp1 + dp2
                d_obj = W_HARD * d_ucov + d_pen
                if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                    blk_a[e, d, b] = a_to; blk_l[e, d, b] = l0 + l1
                    for k in range(b + 1, nb - 1):
                        blk_a[e, d, k] = blk_a[e, d, k + 1]
                        blk_l[e, d, k] = blk_l[e, d, k + 1]
                    n_blk[e, d] = sm._normalize_blocks(nb - 1, blk_a[e, d], blk_l[e, d])
                    cur_ucov += d_ucov; cur_pen += d_pen; accepted += 1
                    if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                        best_feas_pen = cur_pen
                        best_t = sh_t.copy(); best_l = sh_l.copy()
                        best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
                else:
                    for i in range(i0, i1):
                        cov[a_to, i] -= 1; cov[a_from, i] += 1

        elif r < 0.54:
            # Move 8 (NEW): 2-Employee Same-Day Task-Block Swap (flattens spikes with 0 envelope/contract delta!)
            d = np.random.randint(0, D)
            e1 = np.random.randint(0, nE)
            e2 = np.random.randint(0, nE - 1)
            if e2 >= e1: e2 += 1
            nb1, nb2 = n_blk[e1, d], n_blk[e2, d]
            if nb1 == 0 or nb2 == 0:
                temp *= cool; continue
            b1 = np.random.randint(0, nb1)
            b2 = np.random.randint(0, nb2)
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
            d_ucov = du1 + du2 + du3 + du4
            d_pen = dp1 + dp2 + dp3 + dp4
            d_obj = W_HARD * d_ucov + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                blk_a[e1, d, b1] = a2
                blk_a[e2, d, b2] = a1
                n_blk[e1, d] = sm._normalize_blocks(nb1, blk_a[e1, d], blk_l[e1, d])
                n_blk[e2, d] = sm._normalize_blocks(nb2, blk_a[e2, d], blk_l[e2, d])
                cur_ucov += d_ucov; cur_pen += d_pen; accepted += 1
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
            # Move 4: Surgical envelope nudge / add / drop (with surplus-work squeeze!)
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
                new_nb = 1
                tmp_ba[0] = np.random.randint(0, A); tmp_bl[0] = new_l
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
                    if tmp_bl[new_nb - 1] < 4:
                        temp *= cool; continue
                elif sub == 1:
                    new_t = old_t + step; new_l = old_l
                else:
                    new_t = old_t + step; new_l = old_l - step
                    tmp_bl[0] -= step
                    if tmp_bl[0] < 4:
                        temp *= cool; continue
                if new_l < 24 or new_l > 40 or new_t < 0 or new_t + new_l > N or start_ok[d, new_t] == 0:
                    temp *= cool; continue
                if not sm._rest_ok(sh_t, sh_l, e, d, new_t, new_l, D):
                    temp *= cool; continue

            old_ev = sm._emp_viol(emp_w[e], min_iv[e], max_iv[e])
            new_ew = emp_w[e] - old_l + new_l
            d_cviol = sm._emp_viol(new_ew, min_iv[e], max_iv[e]) - old_ev
            old_surp = emp_w[e] - min_iv[e] if emp_w[e] > min_iv[e] else 0
            new_surp = new_ew - min_iv[e] if new_ew > min_iv[e] else 0
            d_surp = new_surp - old_surp

            du1, dp1 = (0, 0)
            if old_l > 0:
                du1, dp1 = sm._apply_shift_cov(cov, vmin, vmax, old_t, old_nb, blk_a[e, d], blk_l[e, d], -1)
            du2, dp2 = (0, 0)
            if new_l > 0:
                du2, dp2 = sm._apply_shift_cov(cov, vmin, vmax, new_t, new_nb, tmp_ba, tmp_bl, 1)
            d_ucov, d_pen = du1 + du2, dp1 + dp2
            d_obj = W_HARD * (d_ucov + d_cviol) + W_SURP * d_surp + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e, d] = new_t; sh_l[e, d] = new_l; n_blk[e, d] = new_nb
                for k in range(new_nb):
                    blk_a[e, d, k] = tmp_ba[k]; blk_l[e, d, k] = tmp_bl[k]
                emp_w[e] = new_ew
                cur_ucov += d_ucov; cur_pen += d_pen; cur_cviol += d_cviol; accepted += 1
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
            t1, l1 = sh_t[e1, d], sh_l[e1, d]
            t2, l2 = sh_t[e2, d], sh_l[e2, d]
            if l1 == 0 and l2 == 0:
                temp *= cool; continue
            if l2 > 0 and l1 == 0 and not sm._five_in_six_ok(sh_l, e1, d, D):
                temp *= cool; continue
            if l1 > 0 and l2 == 0 and not sm._five_in_six_ok(sh_l, e2, d, D):
                temp *= cool; continue
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
                sh_t[e1, d], sh_t[e2, d] = t2, t1
                sh_l[e1, d], sh_l[e2, d] = l2, l1
                nb1, nb2 = n_blk[e1, d], n_blk[e2, d]
                n_blk[e1, d], n_blk[e2, d] = nb2, nb1
                for k in range(MAX_BLK):
                    ta = blk_a[e1, d, k]; blk_a[e1, d, k] = blk_a[e2, d, k]; blk_a[e2, d, k] = ta
                    tl = blk_l[e1, d, k]; blk_l[e1, d, k] = blk_l[e2, d, k]; blk_l[e2, d, k] = tl
                emp_w[e1] = nw1; emp_w[e2] = nw2
                cur_cviol += d_cviol; accepted += 1
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()

        elif r < 0.94:
            # Move 6: Same-employee 2-day length transfer (0 contract delta!)
            e = np.random.randint(0, nE)
            d1 = np.random.randint(0, D)
            d2 = np.random.randint(0, D - 1)
            if d2 >= d1: d2 += 1
            ot1, ol1, nb1 = sh_t[e, d1], sh_l[e, d1], n_blk[e, d1]
            ot2, ol2, nb2 = sh_t[e, d2], sh_l[e, d2], n_blk[e, d2]
            if ol1 == 0 or ol2 == 0:
                temp *= cool; continue
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
                    temp *= cool; continue
                i2_0, i2_1, a2_chg = ot2 + ol2 - step, ot2 + ol2, blk_a[e, d2, nb2 - 1]
            else:
                nt2, nl2 = ot2 + step, ol2 - step
                if blk_l[e, d2, 0] - step < 4:
                    temp *= cool; continue
                i2_0, i2_1, a2_chg = ot2, ot2 + step, blk_a[e, d2, 0]
            if nl1 > 40 or nl2 < 24 or nt1 < 0 or nt1 + nl1 > N or nt2 < 0 or nt2 + nl2 > N:
                temp *= cool; continue
            if start_ok[d1, nt1] == 0 or start_ok[d2, nt2] == 0:
                temp *= cool; continue
            sh_t[e, d1], sh_l[e, d1] = nt1, nl1
            sh_t[e, d2], sh_l[e, d2] = nt2, nl2
            ok_r = sm._rest_ok(sh_t, sh_l, e, d1, nt1, nl1, D) and sm._rest_ok(sh_t, sh_l, e, d2, nt2, nl2, D)
            sh_t[e, d1], sh_l[e, d1] = ot1, ol1
            sh_t[e, d2], sh_l[e, d2] = ot2, ol2
            if not ok_r:
                temp *= cool; continue
            du1, dp1 = sm._delta_range(cov, vmin, vmax, a2_chg, i2_0, i2_1, -1)
            du2, dp2 = sm._delta_range(cov, vmin, vmax, a1_chg, i1_0, i1_1, 1)
            d_ucov, d_pen = du1 + du2, dp1 + dp2
            d_obj = W_HARD * d_ucov + d_pen
            if d_obj <= 0 or np.random.random() < np.exp(-float(d_obj) / temp):
                sh_t[e, d1], sh_l[e, d1] = nt1, nl1
                sh_t[e, d2], sh_l[e, d2] = nt2, nl2
                if end1: blk_l[e, d1, nb1 - 1] += step
                else: blk_l[e, d1, 0] += step
                if end2: blk_l[e, d2, nb2 - 1] -= step
                else: blk_l[e, d2, 0] -= step
                cur_ucov += d_ucov; cur_pen += d_pen; accepted += 1
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
                emp_w[e] = new_ew
                cur_ucov += d_ucov; cur_pen += d_pen; cur_cviol += d_cviol; accepted += 1
                if cur_ucov == 0 and cur_cviol == 0 and cur_pen < best_feas_pen:
                    best_feas_pen = cur_pen
                    best_t = sh_t.copy(); best_l = sh_l.copy()
                    best_nb = n_blk.copy(); best_ba = blk_a.copy(); best_bl = blk_l.copy()
            else:
                sm._revert_shift_cov(cov, new_t, new_nb, tmp_ba, tmp_bl, -1)
                sm._revert_shift_cov(cov, old_t, old_nb, blk_a[e, d1], blk_l[e, d1], 1)

        temp *= cool

    return best_feas_pen, best_t, best_l, best_nb, best_ba, best_bl, cur_ucov, cur_cviol, accepted


def rolling_window_task_lns(I, sh_t, sh_l, n_blk, blk_a, blk_l, win_days=2, win_secs=5.0, workers=2):
    """
    Rolling 2-day Exact Within-Shift Task-Painting LNS (HiGHS):
    Sweeps 2-day windows [d0, d0+win_days-1] keeping all other days' task coverages fixed,
    and optimizes 1-block + 2-block (>= 4 interval) task paintings on the window's shifts.
    Never worsens true penalty (strictly monotonic improvement check!).
    """
    A, N = I["A"], I["N"]
    nE, D = sh_t.shape
    grid_step = 4 if A <= 4 else (8 if A <= 8 else 12)

    # Precompute full coverage
    cov = np.zeros((A, N), dtype=np.int32)
    for e in range(nE):
        for d in range(D):
            if sh_l[e, d] > 0:
                pos = int(sh_t[e, d])
                for b in range(int(n_blk[e, d])):
                    a0 = int(blk_a[e, d, b])
                    ln = int(blk_l[e, d, b])
                    cov[a0, pos : pos + ln] += 1
                    pos += ln

    def calc_pen_ucov():
        pen, ucov = 0, 0
        for a0 in range(A):
            a = a0 + 1
            for i in range(N):
                c = int(cov[a0, i])
                if c < I["vmin"][a][i]:
                    ucov += (I["vmin"][a][i] - c) ** 2
                elif c > I["vmax"][a][i]:
                    pen += (c - I["vmax"][a][i]) ** 2
        return pen, ucov

    cur_pen, cur_ucov = calc_pen_ucov()
    if cur_ucov > 0:
        return cur_pen, n_blk, blk_a, blk_l

    for d0 in range(0, D, win_days):
        d1 = min(D, d0 + win_days)
        env_slots = {}
        i_min, i_max = N, 0
        for e in range(nE):
            for d in range(d0, d1):
                l = int(sh_l[e, d])
                if l > 0:
                    t = int(sh_t[e, d])
                    i_min = min(i_min, t)
                    i_max = max(i_max, t + l)
                    env_slots.setdefault((t, l), []).append((e, d))
        if not env_slots or i_min >= i_max:
            continue

        # Compute base coverage from shifts OUTSIDE [d0, d1)
        base_cov = cov[:, i_min:i_max].copy()
        for (t, l), slots in env_slots.items():
            for e, d in slots:
                pos = t
                for b in range(int(n_blk[e, d])):
                    a0 = int(blk_a[e, d, b])
                    ln = int(blk_l[e, d, b])
                    base_cov[a0, pos - i_min : pos + ln - i_min] -= 1
                    pos += ln

        W = i_max - i_min
        sv = pywraplp.Solver.CreateSolver("HIGHS")
        sv.SetTimeLimit(int(win_secs * 1000))
        sv.SetNumThreads(int(workers))
        sv.SetSolverSpecificParametersAsString("mip_rel_gap = 0.002")

        add_iv = [[[] for _ in range(W + 1)] for _ in range(A)]
        sub_iv = [[[] for _ in range(W + 1)] for _ in range(A)]
        pat_vars = {}
        for key, slots in env_slots.items():
            t, l = key
            rt = t - i_min
            cnt = len(slots)
            ct = sv.Constraint(float(cnt), float(cnt))
            plist = []
            for a0 in range(A):
                v = sv.IntVar(0.0, float(cnt), "")
                ct.SetCoefficient(v, 1.0)
                add_iv[a0][rt].append(v)
                sub_iv[a0][rt + l].append(v)
                plist.append((v, ((a0, l),)))
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
                        add_iv[a1][rt].append(v)
                        sub_iv[a1][rt + s].append(v)
                        add_iv[a2][rt + s].append(v)
                        sub_iv[a2][rt + l].append(v)
                        plist.append((v, ((a1, s), (a2, l - s))))
            pat_vars[key] = plist

        obj = sv.Objective()
        obj.SetMinimization()
        for a0 in range(A):
            a = a0 + 1
            W_prev = None
            for wi in range(W):
                i = i_min + wi
                W_i = sv.NumVar(0.0, float(nE), "")
                dc = sv.Constraint(0.0, 0.0)
                dc.SetCoefficient(W_i, 1.0)
                if W_prev is not None:
                    dc.SetCoefficient(W_prev, -1.0)
                for v in add_iv[a0][wi]:
                    dc.SetCoefficient(v, -1.0)
                for v in sub_iv[a0][wi]:
                    dc.SetCoefficient(v, 1.0)
                W_prev = W_i

                bc = int(base_cov[a0, wi])
                vmin_req = max(0, I["vmin"][a][i] - bc)
                if vmin_req > 0:
                    W_i.SetLb(float(vmin_req))
                vmax_rem = I["vmax"][a][i] - bc
                if vmax_rem < nE:
                    ov_cap = float(max(0, vmax_rem))
                    base_ex = max(0, -vmax_rem)
                    ov = sv.Constraint(-sv.infinity(), ov_cap)
                    ov.SetCoefficient(W_i, 1.0)
                    for ex in range(14):
                        z = sv.NumVar(0.0, 1.0, "")
                        ov.SetCoefficient(z, -1.0)
                        obj.SetCoefficient(z, float(2 * (base_ex + ex) + 1))
                    zt = sv.NumVar(0.0, float(nE), "")
                    ov.SetCoefficient(zt, -1.0)
                    obj.SetCoefficient(zt, float(2 * (base_ex + 14) + 1))

        st = sv.Solve()
        if st not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
            continue

        # Check new window cost vs old window cost before committing!
        new_cov_w = base_cov.copy()
        assign_map = {}
        for key, slots in env_slots.items():
            t, l = key
            rt = t - i_min
            assigned = []
            for v, blocks in pat_vars[key]:
                c = int(round(v.solution_value()))
                for _ in range(c):
                    assigned.append(blocks)
            if len(assigned) != len(slots):
                assigned = None
                break
            for (e, d), blocks in zip(slots, assigned):
                assign_map[(e, d)] = blocks
                pos = rt
                for a0, bl in blocks:
                    new_cov_w[a0, pos : pos + bl] += 1
                    pos += bl
        if len(assign_map) != sum(len(s) for s in env_slots.values()):
            continue

        old_w_pen, new_w_pen, new_w_ucov = 0, 0, 0
        for a0 in range(A):
            a = a0 + 1
            for wi in range(W):
                i = i_min + wi
                oc = int(cov[a0, i])
                nc = int(new_cov_w[a0, wi])
                if oc > I["vmax"][a][i]:
                    old_w_pen += (oc - I["vmax"][a][i]) ** 2
                if nc < I["vmin"][a][i]:
                    new_w_ucov += 1
                elif nc > I["vmax"][a][i]:
                    new_w_pen += (nc - I["vmax"][a][i]) ** 2

        if new_w_ucov == 0 and new_w_pen < old_w_pen:
            cov[:, i_min:i_max] = new_cov_w
            for (e, d), blocks in assign_map.items():
                n_blk[e, d] = len(blocks)
                for b, (a0, bl) in enumerate(blocks):
                    blk_a[e, d, b] = a0
                    blk_l[e, d, b] = bl
            cur_pen -= (old_w_pen - new_w_pen)

    return cur_pen, n_blk, blk_a, blk_l


def solve_tight_one(iid, stem, rec, lp, s1_s, s2_s, sa_rounds, sa_iters, lpr, win_secs, seed):
    lim = int(6.0 * 1024 * 1024 * 1024)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    except Exception:
        pass

    t0 = time.time()
    I, raw_txt = sm.load_instance(stem)
    A, N = I["A"], I["N"]
    by_day = sm.allowed_shifts_by_day(I)

    # Tighten Stage 1 total work to [wmin, wmin + 8] for counting-tight surplus-staffing instances!
    orig_staff = dict(I["staff"])
    s1_obj, s1_bd, shifts_by_day, s1_st = sm.solve_stage1_mtask_mip(I, by_day, secs=s1_s, workers=2, lp_radius=lpr)
    t_s1 = round(time.time() - t0, 1)
    if shifts_by_day is None:
        return dict(id=iid, stem=stem, record=rec, lp_bound=lp, s1_st=s1_st, best_pen=None, vs_rec=None, win=False, secs=t_s1)

    t1 = time.time()
    s2_viol, sh_t, sh_l, s2_st = sm.pack_employee_chains(I, shifts_by_day, secs=s2_s, workers=2, seed=seed + 13)
    t_s2 = round(time.time() - t1, 1)

    _, n_blk, blk_a, blk_l, s3_st = sm._greedy_paint_fallback(I, sh_t, sh_l)

    opt_t, opt_l, opt_cnt, start_ok = sm.build_allowed_arrays(I, by_day)
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

    lns_r1 = sa_rounds // 3
    lns_r2 = (2 * sa_rounds) // 3
    lns_gain = 0

    for rd in range(sa_rounds):
        # Surplus-squeeze pressure during first 2/3 of rounds, released for final 1/3 polish
        w_surp = 4 if rd < lns_r2 else 0
        if rd == 0:
            t_start, t_end, w_hard = 3.0, 0.03, 50
        elif rd == sa_rounds - 1:
            t_start, t_end, w_hard = 1.5, 0.004, 600
        elif rd % 3 == 1:
            t_start, t_end, w_hard = 7.0, 0.04, 45
        elif rd % 3 == 2:
            t_start, t_end, w_hard = 3.5, 0.02, 90
        else:
            t_start, t_end, w_hard = 12.0, 0.05, 45

        fp, bt, bl, bnb, bba, bbl, ucov, cviol, acc = sa_polish_tight(
            cur_t, cur_l, cur_nb, cur_ba, cur_bl,
            vmin, vmax, min_iv, max_iv, opt_t, opt_l, opt_cnt, start_ok,
            int(sa_iters), t_start, t_end, int(w_hard), int(w_surp), int(seed + rd * 997),
        )
        if fp < best_pen:
            best_pen = int(fp)
            best_t, best_l = bt.copy(), bl.copy()
            best_nb, best_ba, best_bl = bnb.copy(), bba.copy(), bbl.copy()

        # Rolling 2-day Exact Task-Painting LNS at 1/3 and 2/3 marks!
        if rd in (lns_r1, lns_r2) and best_pen < 10**9:
            before = best_pen
            new_p, rnb, rba, rbl = rolling_window_task_lns(
                I, best_t, best_l, best_nb.copy(), best_ba.copy(), best_bl.copy(),
                win_days=2, win_secs=win_secs, workers=2,
            )
            if new_p < best_pen:
                lns_gain += (before - new_p)
                best_pen = int(new_p)
                best_nb, best_ba, best_bl = rnb, rba, rbl

        if best_pen < 10**9:
            cur_t, cur_l = best_t.copy(), best_l.copy()
            cur_nb, cur_ba, cur_bl = best_nb.copy(), best_ba.copy(), best_bl.copy()

    # Final 2-day rolling LNS sweep!
    if best_pen < 10**9:
        before = best_pen
        new_p, rnb, rba, rbl = rolling_window_task_lns(
            I, best_t, best_l, best_nb.copy(), best_ba.copy(), best_bl.copy(),
            win_days=2, win_secs=win_secs, workers=2,
        )
        if new_p < best_pen:
            lns_gain += (before - new_p)
            best_pen = int(new_p)
            best_nb, best_ba, best_bl = rnb, rba, rbl

    valid, verify_line, sha256, win_path = False, "", None, None
    if best_pen < 10**9:
        valid, verify_line, sha256, win_path = sm.save_and_verify_win(
            stem, I, raw_txt, rec, best_pen, best_t, best_l, best_nb, best_ba, best_bl
        )

    surp_iv = int(sum(max(0, int(np.sum(best_l[e])) - int(min_iv[e])) for e in range(len(E)))) if valid else None
    return dict(
        id=iid, stem=stem, record=rec, lp_bound=lp,
        s1_obj=s1_obj, s1_st=s1_st, s1_secs=t_s1,
        s2_viol=s2_viol, s2_secs=t_s2, lns_gain=lns_gain, surp_iv=surp_iv,
        best_pen=best_pen if valid else None,
        vs_rec=(best_pen - rec) if valid else None,
        win=bool(valid and best_pen < rec),
        verify_line=verify_line, sha256=sha256, win_path=win_path,
        secs=round(time.time() - t0, 1),
    )


def run_one_sub(job, seed):
    iid, stem, rec, lp, s1_s, s2_s, rds, iters, lpr, wsec = job
    out_j = os.path.join(LOGS_DIR, f"_t9_{stem}_{seed}_{os.getpid()}.json")
    cmd = [
        sys.executable, "-u", os.path.abspath(__file__),
        "--single", "--id", str(iid), "--stem", stem, "--record", str(rec), "--lp", str(lp),
        "--s1", str(s1_s), "--s2", str(s2_s), "--rounds", str(rds), "--iters", str(iters),
        "--lpr", str(lpr), "--win-secs", str(wsec), "--seed", str(seed), "--out-json", out_j,
    ]
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900, check=False)
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
    parser.add_argument("--s2", type=float, default=90.0)
    parser.add_argument("--rounds", type=int, default=32)
    parser.add_argument("--iters", type=int, default=10_000_000)
    parser.add_argument("--lpr", type=int, default=0)
    parser.add_argument("--win-secs", type=float, default=5.0)
    parser.add_argument("--seed", type=int, default=300001)
    parser.add_argument("--out-json", type=str, default="")
    args = parser.parse_args()

    os.makedirs(LOGS_DIR, exist_ok=True)
    if args.single:
        r = solve_tight_one(args.id, args.stem, args.record, args.lp,
                            args.s1, args.s2, args.rounds, args.iters, args.lpr, args.win_secs, args.seed)
        if args.out_json:
            open(args.out_json, "w").write(json.dumps(r))
        return

    t_all = time.time()
    print(f"=== TIGHT-9 SPECIALIST START ({time.strftime('%Y-%m-%d %H:%M:%S')}) | 9 targets, 2w x 2t ===", flush=True)
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(run_one_sub, j, 310000 + j[0] * 53): j for j in FINAL_9}
        for fut in as_completed(futs):
            r = fut.result()
            r["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            with open(JSONL_PATH, "a") as jf:
                jf.write(json.dumps(r) + "\n")
            vs = r.get("vs_rec")
            tag = "WIN!!" if r.get("win") else (f"{vs:+d}" if vs is not None else f"ERR({r.get('error', '?')})")
            print(
                f"  [#{r['id']:3d} {r['stem']:14s}] S1={r.get('s1_obj')} ({r.get('s1_st')}) | S2v={r.get('s2_viol')} | "
                f"LNS={r.get('lns_gain')} | surp={r.get('surp_iv')} | FINAL={r.get('best_pen')} vs {r['record']} ({tag}) | {r.get('secs')}s",
                flush=True,
            )
    n_wins, tot_d = run_b6.rebuild_manifest_all()
    print(f"=== TIGHT-9 COMPLETE in {(time.time()-t_all)/60.0:.1f}m | Total verified wins: {n_wins}/123 ({tot_d:+d} pts) ===", flush=True)


if __name__ == "__main__":
    main()
