"""
Numba Critical-Path Tabu Search v4 (numba_ts_v4.py) — Option 1 + Option 2 Combo.

Upgrades over numba_ts_v3.py:
  1. Exact O(|M_seq| + |W_seq|) Two-Pointer Synchronized Insertion (find_best_joint_insertion_v4):
     Eliminates v3's Top-4 x Top-4 blind spot across crowded machine/worker sequences.
  2. Lexicographic Co-Bottleneck Plateau Tie-Breaking:
     Ties on exact makespan break deterministically by (n_crit_after, max_mach_load, dur)
     to systematically drain tied bottleneck machines across multi-step plateaus.
  3. N6 Critical-Block Boundary Jumps (machine & worker blocks of len >= 3):
     Tests jumping interior/boundary critical ops before block head or after block tail
     with synchronized best slot on the paired resource.
  4. 5-Second CP-SAT Ultra-Low-Load Mode Assignment Seeder (generate_cpsat_balanced_seeds):
     Generates 6 diverse globally load-balanced (m, w) assignments via a fast pure-assignment
     CP-SAT model on pruned modes, decodes into active schedules via 3 priority rules, and
     seeds the Elite Pool before Iterated Tabu Search + Path Relinking runs.
"""
import time
import numpy as np
from numba import njit
from ortools.sat.python import cp_model

import numba_ts


@njit(cache=True)
def collect_range(head_r, succ, est, dur, tail, j_est, j_tail, res_list, out_after, out_e, out_t):
    """Collect all valid Mastrolilli-Gambardella insertion slots in [lo, hi] on resource r."""
    k = 0
    cur = head_r
    while cur != -1:
        res_list[k] = cur
        k += 1
        cur = succ[cur]

    if k == 0:
        out_after[0] = -1
        out_e[0] = 0
        out_t[0] = 0
        return 1

    lo = 0
    for i in range(k):
        x = res_list[i]
        if est[x] + dur[x] <= j_est:
            lo = i + 1
    hi = k
    for i in range(k - 1, -1, -1):
        x = res_list[i]
        if tail[x] + dur[x] <= j_tail:
            hi = i
    if lo > hi:
        tmp = lo
        lo = hi
        hi = tmp

    n = hi - lo + 1
    for p in range(n):
        pos = lo + p
        out_after[p] = res_list[pos - 1] if pos > 0 else -1
        out_e[p] = (est[res_list[pos - 1]] + dur[res_list[pos - 1]]) if pos > 0 else 0
        out_t[p] = (dur[res_list[pos]] + tail[res_list[pos]]) if pos < k else 0
    return n


@njit(cache=True)
def find_best_joint_insertion_v4(mh_r, ms, wh_r, ws, est, tail, dur,
                                 j_est, j_tail, res_list,
                                 m_afters, m_ests, m_tails,
                                 w_afters, w_ests, w_tails):
    """
    Exact O(|M_seq| + |W_seq|) two-pointer scan over all valid (pos_m, pos_w) pairs
    exploiting est monotonicity ascending and tail monotonicity descending.
    Returns (best_m_after, best_w_after, best_lb_without_d).
    """
    nm = collect_range(mh_r, ms, est, dur, tail, j_est, j_tail, res_list, m_afters, m_ests, m_tails)
    nw = collect_range(wh_r, ws, est, dur, tail, j_est, j_tail, res_list, w_afters, w_ests, w_tails)

    pm = 0
    pw = 0
    best_lb = 1000000000
    best_ma = m_afters[0]
    best_wa = w_afters[0]

    while pm < nm and pw < nw:
        me = m_ests[pm]
        mt = m_tails[pm]
        we = w_ests[pw]
        wt = w_tails[pw]
        e = j_est
        if me > e:
            e = me
        if we > e:
            e = we
        t = j_tail
        if mt > t:
            t = mt
        if wt > t:
            t = wt
        lb = e + t
        if lb < best_lb:
            best_lb = lb
            best_ma = m_afters[pm]
            best_wa = w_afters[pw]

        if pm + 1 < nm and pw + 1 < nw:
            if mt >= wt:
                pm += 1
            else:
                pw += 1
        elif pm + 1 < nm:
            if mt <= wt:
                break
            pm += 1
        elif pw + 1 < nw:
            if wt <= mt:
                break
            pw += 1
        else:
            break

    return best_ma, best_wa, best_lb


@njit(cache=True)
def swap_adjacent_in_seq(u, v, head, tail, pred, succ, r):
    """Swap adjacent pair (u -> v) into (v -> u) on resource r."""
    pu = pred[u]
    sv = succ[v]
    if pu != -1:
        succ[pu] = v
    else:
        head[r] = v
    if sv != -1:
        pred[sv] = u
    else:
        tail[r] = u
    pred[v] = pu
    succ[v] = u
    pred[u] = v
    succ[u] = sv


@njit(cache=True)
def decode_fixed_assignment(N, M, W, job_pred, job_succ, op_alt_in, alt_m, alt_w, alt_d, seed, rule):
    """Decode fixed mode assignment op_alt[0..N-1] into a feasible active schedule."""
    np.random.seed(seed)
    op_alt = op_alt_in.copy()
    op_m = np.empty(N, dtype=np.int32)
    op_w = np.empty(N, dtype=np.int32)
    dur = np.empty(N, dtype=np.int32)
    for u in range(N):
        a = op_alt[u]
        op_m[u] = alt_m[a]
        op_w[u] = alt_w[a]
        dur[u] = alt_d[a]

    rem_work = np.empty(N, dtype=np.int32)
    for u in range(N - 1, -1, -1):
        rem_work[u] = dur[u] + (rem_work[job_succ[u]] if job_succ[u] != -1 else 0)

    mach_head = np.full(M, -1, dtype=np.int32)
    mach_tail = np.full(M, -1, dtype=np.int32)
    work_head = np.full(W, -1, dtype=np.int32)
    work_tail = np.full(W, -1, dtype=np.int32)
    mach_pred = np.full(N, -1, dtype=np.int32)
    mach_succ = np.full(N, -1, dtype=np.int32)
    work_pred = np.full(N, -1, dtype=np.int32)
    work_succ = np.full(N, -1, dtype=np.int32)

    mach_avail = np.zeros(M, dtype=np.int32)
    work_avail = np.zeros(W, dtype=np.int32)
    job_avail = np.zeros(N, dtype=np.int32)

    ready = np.empty(N, dtype=np.int32)
    n_ready = 0
    for u in range(N):
        if job_pred[u] == -1:
            ready[n_ready] = u
            n_ready += 1

    mk = 0
    for _ in range(N):
        best_pos = 0
        best_sc = -1e18
        for i in range(n_ready):
            u = ready[i]
            m = op_m[u]
            w = op_w[u]
            s = job_avail[u]
            if mach_avail[m] > s:
                s = mach_avail[m]
            if work_avail[w] > s:
                s = work_avail[w]
            fin = s + dur[u]
            if rule == 0:
                sc = float(rem_work[u]) - 0.8 * float(s)
            elif rule == 1:
                sc = -float(fin) + 0.35 * float(rem_work[u])
            else:
                sc = -float(s) + 0.5 * float(rem_work[u]) + np.random.random() * 8.0
            if sc > best_sc:
                best_sc = sc
                best_pos = i

        u = ready[best_pos]
        ready[best_pos] = ready[n_ready - 1]
        n_ready -= 1

        m = op_m[u]
        w = op_w[u]
        s = job_avail[u]
        if mach_avail[m] > s:
            s = mach_avail[m]
        if work_avail[w] > s:
            s = work_avail[w]
        fin = s + dur[u]
        if fin > mk:
            mk = fin

        mt = mach_tail[m]
        if mt == -1:
            mach_head[m] = u
        else:
            mach_succ[mt] = u
            mach_pred[u] = mt
        mach_tail[m] = u
        mach_avail[m] = fin

        wt = work_tail[w]
        if wt == -1:
            work_head[w] = u
        else:
            work_succ[wt] = u
            work_pred[u] = wt
        work_tail[w] = u
        work_avail[w] = fin

        v = job_succ[u]
        if v != -1:
            job_avail[v] = fin
            ready[n_ready] = v
            n_ready += 1

    return mk, op_alt, op_m, op_w, dur, mach_head, mach_tail, work_head, work_tail, mach_pred, mach_succ, work_pred, work_succ


@njit(cache=True)
def construct_load_balanced(N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d,
                            seed, noise_lvl):
    """Diverse randomized constructive heuristic for fallback greedy starts."""
    np.random.seed(seed)
    min_d = np.empty(N, dtype=np.int32)
    for u in range(N):
        min_d[u] = alt_d[alt_start[u]]
    rem_work = np.empty(N, dtype=np.int32)
    for u in range(N - 1, -1, -1):
        rem_work[u] = min_d[u] + (rem_work[job_succ[u]] if job_succ[u] != -1 else 0)

    mach_head = np.full(M, -1, dtype=np.int32)
    mach_tail = np.full(M, -1, dtype=np.int32)
    work_head = np.full(W, -1, dtype=np.int32)
    work_tail = np.full(W, -1, dtype=np.int32)
    mach_pred = np.full(N, -1, dtype=np.int32)
    mach_succ = np.full(N, -1, dtype=np.int32)
    work_pred = np.full(N, -1, dtype=np.int32)
    work_succ = np.full(N, -1, dtype=np.int32)

    op_alt = np.empty(N, dtype=np.int32)
    op_m = np.empty(N, dtype=np.int32)
    op_w = np.empty(N, dtype=np.int32)
    dur = np.empty(N, dtype=np.int32)
    mach_avail = np.zeros(M, dtype=np.int32)
    work_avail = np.zeros(W, dtype=np.int32)
    mach_load = np.zeros(M, dtype=np.int32)
    work_load = np.zeros(W, dtype=np.int32)
    job_avail = np.zeros(N, dtype=np.int32)

    ready = np.empty(N, dtype=np.int32)
    n_ready = 0
    for u in range(N):
        if job_pred[u] == -1:
            ready[n_ready] = u
            n_ready += 1

    rule = seed % 4
    load_w = 0.25 if rule == 2 else (0.10 if rule == 3 else 0.0)

    for _ in range(N):
        best_pos = 0
        best_score = -1e18
        for i in range(n_ready):
            u = ready[i]
            if rule == 0:
                sc = float(rem_work[u]) + noise_lvl * np.random.random() * 20.0
            elif rule == 1:
                sc = -float(job_avail[u]) + 0.5 * float(rem_work[u]) + noise_lvl * np.random.random() * 20.0
            elif rule == 2:
                sc = float(rem_work[u]) - 0.3 * float(job_avail[u]) + noise_lvl * np.random.random() * 25.0
            else:
                sc = float(rem_work[u]) - 0.6 * float(job_avail[u]) + noise_lvl * np.random.random() * 30.0
            if sc > best_score:
                best_score = sc
                best_pos = i
        u = ready[best_pos]
        ready[best_pos] = ready[n_ready - 1]
        n_ready -= 1

        a0 = alt_start[u]
        a1 = alt_start[u + 1]
        ja = job_avail[u]
        best_a = a0
        best_cost = 1e18
        for a in range(a0, a1):
            m = alt_m[a]
            w = alt_w[a]
            d = alt_d[a]
            s = ja
            if mach_avail[m] > s:
                s = mach_avail[m]
            if work_avail[w] > s:
                s = work_avail[w]
            cost = float(s + d) + load_w * float(mach_load[m] + work_load[w])
            if noise_lvl > 0.0:
                cost += noise_lvl * np.random.random() * 4.0
            if cost < best_cost:
                best_cost = cost
                best_a = a

        m = alt_m[best_a]
        w = alt_w[best_a]
        d = alt_d[best_a]
        s = ja
        if mach_avail[m] > s:
            s = mach_avail[m]
        if work_avail[w] > s:
            s = work_avail[w]
        fin = s + d

        op_alt[u] = best_a
        op_m[u] = m
        op_w[u] = w
        dur[u] = d
        mach_load[m] += d
        work_load[w] += d

        mt = mach_tail[m]
        if mt == -1:
            mach_head[m] = u
        else:
            mach_succ[mt] = u
            mach_pred[u] = mt
        mach_tail[m] = u
        mach_avail[m] = fin

        wt = work_tail[w]
        if wt == -1:
            work_head[w] = u
        else:
            work_succ[wt] = u
            work_pred[u] = wt
        work_tail[w] = u
        work_avail[w] = fin

        v = job_succ[u]
        if v != -1:
            job_avail[v] = fin
            ready[n_ready] = v
            n_ready += 1

    return op_alt, op_m, op_w, dur, mach_head, mach_tail, work_head, work_tail, mach_pred, mach_succ, work_pred, work_succ


@njit(cache=True)
def _push_cand(est_lb, ctype, u, a, ma, wa, is_t, K_TOP,
               cand_lb, cand_type, cand_u, cand_a, cand_ma, cand_wa, cand_tabu, n_cand, worst_lb):
    """Insert candidate into fixed Top-K min-heap array sorted by est_lb."""
    if n_cand < K_TOP or est_lb < worst_lb or (est_lb == worst_lb and np.random.random() < 0.25):
        idx = n_cand if n_cand < K_TOP else K_TOP - 1
        if n_cand < K_TOP:
            n_cand += 1
        while idx > 0 and est_lb < cand_lb[idx - 1]:
            cand_lb[idx] = cand_lb[idx - 1]
            cand_type[idx] = cand_type[idx - 1]
            cand_u[idx] = cand_u[idx - 1]
            cand_a[idx] = cand_a[idx - 1]
            cand_ma[idx] = cand_ma[idx - 1]
            cand_wa[idx] = cand_wa[idx - 1]
            cand_tabu[idx] = cand_tabu[idx - 1]
            idx -= 1
        cand_lb[idx] = est_lb
        cand_type[idx] = ctype
        cand_u[idx] = u
        cand_a[idx] = a
        cand_ma[idx] = ma
        cand_wa[idx] = wa
        cand_tabu[idx] = is_t
        worst_lb = cand_lb[n_cand - 1]
    return n_cand, worst_lb


@njit(cache=True)
def tabu_search_v4_run(N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d,
                       seed, max_iters, max_no_improve, max_modes_per_op,
                       init_op_alt, init_op_m, init_op_w, init_dur,
                       init_mh, init_mt, init_wh, init_wt,
                       init_mp, init_ms, init_wp, init_ws):
    """
    Critical-Path Tabu Search v4:
      - Exact O(|M|+|W|) two-pointer joint idle-slot insertion (find_best_joint_insertion_v4).
      - N5 adjacent critical-arc swaps + N6 critical-block boundary jumps (len >= 3).
      - Lexicographic co-bottleneck plateau tie-breaking: (ex_mk, n_crit_after, max_mach_load, dur).
    """
    np.random.seed(seed)

    op_alt = init_op_alt.copy()
    op_m = init_op_m.copy()
    op_w = init_op_w.copy()
    dur = init_dur.copy()
    mh = init_mh.copy()
    mt = init_mt.copy()
    wh = init_wh.copy()
    wt = init_wt.copy()
    mp = init_mp.copy()
    ms = init_ms.copy()
    wp = init_wp.copy()
    ws = init_ws.copy()

    mach_load = np.zeros(M, dtype=np.int32)
    work_load = np.zeros(W, dtype=np.int32)
    for u in range(N):
        mach_load[op_m[u]] += dur[u]
        work_load[op_w[u]] += dur[u]

    est = np.empty(N, dtype=np.int32)
    tail = np.empty(N, dtype=np.int32)
    est_tmp = np.empty(N, dtype=np.int32)
    tail_tmp = np.empty(N, dtype=np.int32)
    topo = np.empty(N, dtype=np.int32)
    indeg = np.empty(N, dtype=np.int32)
    res_list = np.empty(N + 1, dtype=np.int32)
    crit_ops = np.empty(N, dtype=np.int32)
    is_crit = np.zeros(N, dtype=np.int8)

    m_afters = np.empty(N + 1, dtype=np.int32)
    m_ests = np.empty(N + 1, dtype=np.int32)
    m_tails = np.empty(N + 1, dtype=np.int32)
    w_afters = np.empty(N + 1, dtype=np.int32)
    w_ests = np.empty(N + 1, dtype=np.int32)
    w_tails = np.empty(N + 1, dtype=np.int32)

    K_TOP = 14
    cand_lb = np.empty(K_TOP, dtype=np.int32)
    cand_type = np.empty(K_TOP, dtype=np.int8)
    cand_u = np.empty(K_TOP, dtype=np.int32)
    cand_a = np.empty(K_TOP, dtype=np.int32)
    cand_ma = np.empty(K_TOP, dtype=np.int32)
    cand_wa = np.empty(K_TOP, dtype=np.int32)
    cand_tabu = np.empty(K_TOP, dtype=np.int8)

    cur_mk = numba_ts.eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est, tail, topo, indeg)
    best_mk = cur_mk
    best_op_alt = op_alt.copy()
    best_est = est.copy()
    best_mh = mh.copy()
    best_mt = mt.copy()
    best_wh = wh.copy()
    best_wt = wt.copy()
    best_mp = mp.copy()
    best_ms = ms.copy()
    best_wp = wp.copy()
    best_ws = ws.copy()

    tabu_m = np.zeros((N, M), dtype=np.int32)
    tabu_w = np.zeros((N, W), dtype=np.int32)
    tabu_op = np.zeros(N, dtype=np.int32)

    no_imp = 0
    evals = 0
    base_tenure = 14 + (N // 26)

    for it in range(1, max_iters + 1):
        n_crit = 0
        for u in range(N):
            if est[u] + dur[u] + tail[u] == cur_mk:
                crit_ops[n_crit] = u
                is_crit[u] = 1
                n_crit += 1
            else:
                is_crit[u] = 0

        if n_crit == 0:
            break

        n_cand = 0
        worst_cand_lb = 1000000000

        step_c = 1 if n_crit <= 48 else (n_crit // 48)
        offset_c = it % step_c

        avg_m_load = 0
        for mm in range(M):
            avg_m_load += mach_load[mm]
        avg_m_load = avg_m_load // M if M > 0 else 1

        for ci in range(offset_c, n_crit, step_c):
            u = crit_ops[ci]
            old_m = op_m[u]
            old_w = op_w[u]
            old_a = op_alt[u]
            old_mp = mp[u]
            old_wp = wp[u]
            old_d = dur[u]

            # --- Walk critical blocks around u BEFORE removing u ---
            bm_head = u
            bm_len = 1
            cur = u
            while True:
                p = mp[cur]
                if p != -1 and is_crit[p] == 1 and est[p] + dur[p] == est[cur]:
                    bm_head = p
                    bm_len += 1
                    cur = p
                else:
                    break
            bm_pred = mp[bm_head]
            bm_tail = u
            cur = u
            while True:
                nx = ms[cur]
                if nx != -1 and is_crit[nx] == 1 and est[cur] + dur[cur] == est[nx]:
                    bm_tail = nx
                    bm_len += 1
                    cur = nx
                else:
                    break

            bw_head = u
            bw_len = 1
            cur = u
            while True:
                p = wp[cur]
                if p != -1 and is_crit[p] == 1 and est[p] + dur[p] == est[cur]:
                    bw_head = p
                    bw_len += 1
                    cur = p
                else:
                    break
            bw_pred = wp[bw_head]
            bw_tail = u
            cur = u
            while True:
                nx = ws[cur]
                if nx != -1 and is_crit[nx] == 1 and est[cur] + dur[cur] == est[nx]:
                    bw_tail = nx
                    bw_len += 1
                    cur = nx
                else:
                    break

            # --- Neighborhood A: N5 Adjacent Critical-Block Swaps ---
            v_m = ms[u]
            if v_m != -1 and is_crit[v_m] == 1 and est[u] + old_d == est[v_m]:
                if job_succ[u] != v_m and job_pred[v_m] != u:
                    u_prev_c = (old_mp != -1 and is_crit[old_mp] == 1 and est[old_mp] + dur[old_mp] == est[u])
                    v_next = ms[v_m]
                    v_next_c = (v_next != -1 and is_crit[v_next] == 1 and est[v_m] + dur[v_m] == est[v_next])
                    if (not u_prev_c) or (not v_next_c):
                        pm_fin = (est[old_mp] + dur[old_mp]) if old_mp != -1 else 0
                        jv_p = job_pred[v_m]
                        jv_est = (est[jv_p] + dur[jv_p]) if jv_p != -1 else 0
                        wv_p = wp[v_m]
                        wv_est = (est[wv_p] + dur[wv_p]) if wv_p != -1 else 0
                        new_ev = pm_fin
                        if jv_est > new_ev:
                            new_ev = jv_est
                        if wv_est > new_ev:
                            new_ev = wv_est
                        new_eu = new_ev + dur[v_m]
                        ju_p = job_pred[u]
                        ju_est = (est[ju_p] + dur[ju_p]) if ju_p != -1 else 0
                        wu_p = wp[u]
                        wu_est = (est[wu_p] + dur[wu_p]) if wu_p != -1 else 0
                        if ju_est > new_eu:
                            new_eu = ju_est
                        if wu_est > new_eu:
                            new_eu = wu_est
                        ns_tail = (dur[v_next] + tail[v_next]) if v_next != -1 else 0
                        ju_s = job_succ[u]
                        ju_tail = (dur[ju_s] + tail[ju_s]) if ju_s != -1 else 0
                        wu_s = ws[u]
                        wu_tail = (dur[wu_s] + tail[wu_s]) if wu_s != -1 else 0
                        ut = ns_tail
                        if ju_tail > ut:
                            ut = ju_tail
                        if wu_tail > ut:
                            ut = wu_tail
                        est_lb = new_eu + old_d + ut
                        evals += 1
                        is_t = 1 if (tabu_op[u] > it and tabu_op[v_m] > it) else 0
                        if is_t == 0 or est_lb < best_mk:
                            n_cand, worst_cand_lb = _push_cand(
                                est_lb, 1, u, v_m, old_m, 0, is_t, K_TOP,
                                cand_lb, cand_type, cand_u, cand_a, cand_ma, cand_wa, cand_tabu,
                                n_cand, worst_cand_lb,
                            )

            v_w = ws[u]
            if v_w != -1 and is_crit[v_w] == 1 and est[u] + old_d == est[v_w]:
                if job_succ[u] != v_w and job_pred[v_w] != u and v_w != v_m:
                    u_prev_c = (old_wp != -1 and is_crit[old_wp] == 1 and est[old_wp] + dur[old_wp] == est[u])
                    v_next = ws[v_w]
                    v_next_c = (v_next != -1 and is_crit[v_next] == 1 and est[v_w] + dur[v_w] == est[v_next])
                    if (not u_prev_c) or (not v_next_c):
                        pw_fin = (est[old_wp] + dur[old_wp]) if old_wp != -1 else 0
                        jv_p = job_pred[v_w]
                        jv_est = (est[jv_p] + dur[jv_p]) if jv_p != -1 else 0
                        mv_p = mp[v_w]
                        mv_est = (est[mv_p] + dur[mv_p]) if mv_p != -1 else 0
                        new_ev = pw_fin
                        if jv_est > new_ev:
                            new_ev = jv_est
                        if mv_est > new_ev:
                            new_ev = mv_est
                        new_eu = new_ev + dur[v_w]
                        ju_p = job_pred[u]
                        ju_est = (est[ju_p] + dur[ju_p]) if ju_p != -1 else 0
                        mu_p = mp[u]
                        mu_est = (est[mu_p] + dur[mu_p]) if mu_p != -1 else 0
                        if ju_est > new_eu:
                            new_eu = ju_est
                        if mu_est > new_eu:
                            new_eu = mu_est
                        ns_tail = (dur[v_next] + tail[v_next]) if v_next != -1 else 0
                        ju_s = job_succ[u]
                        ju_tail = (dur[ju_s] + tail[ju_s]) if ju_s != -1 else 0
                        mu_s = ms[u]
                        mu_tail = (dur[mu_s] + tail[mu_s]) if mu_s != -1 else 0
                        ut = ns_tail
                        if ju_tail > ut:
                            ut = ju_tail
                        if mu_tail > ut:
                            ut = mu_tail
                        est_lb = new_eu + old_d + ut
                        evals += 1
                        is_t = 1 if (tabu_op[u] > it and tabu_op[v_w] > it) else 0
                        if is_t == 0 or est_lb < best_mk:
                            n_cand, worst_cand_lb = _push_cand(
                                est_lb, 2, u, v_w, 0, old_w, is_t, K_TOP,
                                cand_lb, cand_type, cand_u, cand_a, cand_ma, cand_wa, cand_tabu,
                                n_cand, worst_cand_lb,
                            )

            # Remove u once for N6 boundary jumps + Neighborhood B
            jp = job_pred[u]
            js = job_succ[u]
            j_est = (est[jp] + dur[jp]) if jp != -1 else 0
            j_tail = (dur[js] + tail[js]) if js != -1 else 0

            numba_ts.remove_from_seq(u, mh, mt, mp, ms, old_m)
            numba_ts.remove_from_seq(u, wh, wt, wp, ws, old_w)

            # --- Neighborhood A2: N6 Critical-Block Boundary Jumps (same mode, best other-resource slot) ---
            if bm_len >= 3:
                nw_u = collect_range(wh[old_w], ws, est, dur, tail, j_est, j_tail, res_list, w_afters, w_ests, w_tails)
                for side in range(2):
                    if side == 0:
                        if u == bm_head:
                            continue
                        ma = bm_pred
                    else:
                        if u == bm_tail:
                            continue
                        ma = bm_tail
                    mn = ms[ma] if ma != -1 else mh[old_m]
                    me = (est[ma] + dur[ma]) if ma != -1 else 0
                    m_tl = (dur[mn] + tail[mn]) if mn != -1 else 0
                    e0 = j_est if j_est > me else me
                    t0 = j_tail if j_tail > m_tl else m_tl
                    best_w_lb = 1000000000
                    best_wa = w_afters[0]
                    for pw in range(nw_u):
                        ee = e0 if e0 > w_ests[pw] else w_ests[pw]
                        tt = t0 if t0 > w_tails[pw] else w_tails[pw]
                        lbw = ee + tt
                        if lbw < best_w_lb:
                            best_w_lb = lbw
                            best_wa = w_afters[pw]
                    if ma != old_mp or best_wa != old_wp:
                        est_lb = best_w_lb + old_d
                        evals += 1
                        is_t = 1 if (tabu_op[u] > it) else 0
                        if is_t == 0 or est_lb < best_mk:
                            n_cand, worst_cand_lb = _push_cand(
                                est_lb, 0, u, old_a, ma, best_wa, is_t, K_TOP,
                                cand_lb, cand_type, cand_u, cand_a, cand_ma, cand_wa, cand_tabu,
                                n_cand, worst_cand_lb,
                            )

            if bw_len >= 3:
                nm_u = collect_range(mh[old_m], ms, est, dur, tail, j_est, j_tail, res_list, m_afters, m_ests, m_tails)
                for side in range(2):
                    if side == 0:
                        if u == bw_head:
                            continue
                        wa = bw_pred
                    else:
                        if u == bw_tail:
                            continue
                        wa = bw_tail
                    wn = ws[wa] if wa != -1 else wh[old_w]
                    we = (est[wa] + dur[wa]) if wa != -1 else 0
                    w_tl = (dur[wn] + tail[wn]) if wn != -1 else 0
                    e0 = j_est if j_est > we else we
                    t0 = j_tail if j_tail > w_tl else w_tl
                    best_m_lb = 1000000000
                    best_ma = m_afters[0]
                    for pm in range(nm_u):
                        ee = e0 if e0 > m_ests[pm] else m_ests[pm]
                        tt = t0 if t0 > m_tails[pm] else m_tails[pm]
                        lbm = ee + tt
                        if lbm < best_m_lb:
                            best_m_lb = lbm
                            best_ma = m_afters[pm]
                    if best_ma != old_mp or wa != old_wp:
                        est_lb = best_m_lb + old_d
                        evals += 1
                        is_t = 1 if (tabu_op[u] > it) else 0
                        if is_t == 0 or est_lb < best_mk:
                            n_cand, worst_cand_lb = _push_cand(
                                est_lb, 0, u, old_a, best_ma, wa, is_t, K_TOP,
                                cand_lb, cand_type, cand_u, cand_a, cand_ma, cand_wa, cand_tabu,
                                n_cand, worst_cand_lb,
                            )

            # --- Neighborhood B: Mode Reassignment + Exact O(|M|+|W|) Two-Pointer Joint Insertion ---
            a0 = alt_start[u]
            a1 = alt_start[u + 1]
            n_alts = a1 - a0

            if n_alts <= max_modes_per_op:
                for a in range(a0, a1):
                    m2 = alt_m[a]
                    w2 = alt_w[a]
                    d2 = alt_d[a]
                    if j_est + d2 + j_tail > worst_cand_lb + 2:
                        continue
                    ma, wa, lb_no_d = find_best_joint_insertion_v4(
                        mh[m2], ms, wh[w2], ws, est, tail, dur,
                        j_est, j_tail, res_list,
                        m_afters, m_ests, m_tails, w_afters, w_ests, w_tails,
                    )
                    if a == old_a and ma == old_mp and wa == old_wp:
                        continue
                    est_lb = lb_no_d + d2
                    evals += 1
                    is_t = 1 if ((tabu_m[u, m2] > it) or (tabu_w[u, w2] > it) or (tabu_op[u] > it)) else 0
                    if is_t == 1 and est_lb >= best_mk:
                        continue
                    n_cand, worst_cand_lb = _push_cand(
                        est_lb, 0, u, a, ma, wa, is_t, K_TOP,
                        cand_lb, cand_type, cand_u, cand_a, cand_ma, cand_wa, cand_tabu,
                        n_cand, worst_cand_lb,
                    )
            else:
                n_fast = 24
                for a in range(a0, a0 + n_fast):
                    m2 = alt_m[a]
                    w2 = alt_w[a]
                    d2 = alt_d[a]
                    if j_est + d2 + j_tail > worst_cand_lb + 2:
                        continue
                    ma, wa, lb_no_d = find_best_joint_insertion_v4(
                        mh[m2], ms, wh[w2], ws, est, tail, dur,
                        j_est, j_tail, res_list,
                        m_afters, m_ests, m_tails, w_afters, w_ests, w_tails,
                    )
                    if a == old_a and ma == old_mp and wa == old_wp:
                        continue
                    est_lb = lb_no_d + d2
                    evals += 1
                    is_t = 1 if ((tabu_m[u, m2] > it) or (tabu_w[u, w2] > it) or (tabu_op[u] > it)) else 0
                    if is_t == 1 and est_lb >= best_mk:
                        continue
                    n_cand, worst_cand_lb = _push_cand(
                        est_lb, 0, u, a, ma, wa, is_t, K_TOP,
                        cand_lb, cand_type, cand_u, cand_a, cand_ma, cand_wa, cand_tabu,
                        n_cand, worst_cand_lb,
                    )

                rem_budget = max_modes_per_op - n_fast
                load_checked = 0
                span = n_alts - n_fast
                start_off = (it * 37 + u * 13) % span
                for step_k in range(span):
                    if load_checked >= rem_budget:
                        break
                    a = a0 + n_fast + ((start_off + step_k) % span)
                    m2 = alt_m[a]
                    w2 = alt_w[a]
                    d2 = alt_d[a]
                    if mach_load[m2] > avg_m_load and work_load[w2] > avg_m_load and (step_k % 7 != 0):
                        continue
                    if j_est + d2 + j_tail > worst_cand_lb + 2:
                        continue
                    load_checked += 1
                    ma, wa, lb_no_d = find_best_joint_insertion_v4(
                        mh[m2], ms, wh[w2], ws, est, tail, dur,
                        j_est, j_tail, res_list,
                        m_afters, m_ests, m_tails, w_afters, w_ests, w_tails,
                    )
                    if a == old_a and ma == old_mp and wa == old_wp:
                        continue
                    est_lb = lb_no_d + d2
                    evals += 1
                    is_t = 1 if ((tabu_m[u, m2] > it) or (tabu_w[u, w2] > it) or (tabu_op[u] > it)) else 0
                    if is_t == 1 and est_lb >= best_mk:
                        continue
                    n_cand, worst_cand_lb = _push_cand(
                        est_lb, 0, u, a, ma, wa, is_t, K_TOP,
                        cand_lb, cand_type, cand_u, cand_a, cand_ma, cand_wa, cand_tabu,
                        n_cand, worst_cand_lb,
                    )

            numba_ts.insert_after_in_seq(u, old_mp, mh, mt, mp, ms, old_m)
            numba_ts.insert_after_in_seq(u, old_wp, wh, wt, wp, ws, old_w)

        # --- Exact DAG Verification + Lexicographic Co-Bottleneck Plateau Tie-Breaking ---
        chosen_idx = -1
        chosen_exact_mk = 1000000000
        chosen_ncrit = 1000000000
        chosen_max_ml = 1000000000
        chosen_dur = 1000000000

        base_max_ml = 0
        for mm in range(M):
            if mach_load[mm] > base_max_ml:
                base_max_ml = mach_load[mm]

        for ci in range(n_cand):
            ctype = cand_type[ci]
            u = cand_u[ci]
            is_t = cand_tabu[ci]

            cand_max_ml = base_max_ml
            cand_dur_u = dur[u]
            n_crit_after = 0

            if ctype == 0:
                old_m = op_m[u]
                old_w = op_w[u]
                old_mp = mp[u]
                old_wp = wp[u]
                old_d = dur[u]
                a = cand_a[ci]
                m2 = alt_m[a]
                w2 = alt_w[a]
                d2 = alt_d[a]
                ma = cand_ma[ci]
                wa = cand_wa[ci]

                numba_ts.remove_from_seq(u, mh, mt, mp, ms, old_m)
                numba_ts.remove_from_seq(u, wh, wt, wp, ws, old_w)
                numba_ts.insert_after_in_seq(u, ma, mh, mt, mp, ms, m2)
                numba_ts.insert_after_in_seq(u, wa, wh, wt, wp, ws, w2)
                dur[u] = d2
                ex_mk = numba_ts.eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est_tmp, tail_tmp, topo, indeg)
                if ex_mk != -1:
                    for x in range(N):
                        if est_tmp[x] + dur[x] + tail_tmp[x] == ex_mk:
                            n_crit_after += 1
                    mach_load[old_m] -= old_d
                    mach_load[m2] += d2
                    cand_max_ml = 0
                    for mm in range(M):
                        if mach_load[mm] > cand_max_ml:
                            cand_max_ml = mach_load[mm]
                    mach_load[m2] -= d2
                    mach_load[old_m] += old_d
                    cand_dur_u = d2
                dur[u] = old_d
                numba_ts.remove_from_seq(u, mh, mt, mp, ms, m2)
                numba_ts.remove_from_seq(u, wh, wt, wp, ws, w2)
                numba_ts.insert_after_in_seq(u, old_mp, mh, mt, mp, ms, old_m)
                numba_ts.insert_after_in_seq(u, old_wp, wh, wt, wp, ws, old_w)
            elif ctype == 1:
                v = cand_a[ci]
                r_m = cand_ma[ci]
                swap_adjacent_in_seq(u, v, mh, mt, mp, ms, r_m)
                ex_mk = numba_ts.eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est_tmp, tail_tmp, topo, indeg)
                if ex_mk != -1:
                    for x in range(N):
                        if est_tmp[x] + dur[x] + tail_tmp[x] == ex_mk:
                            n_crit_after += 1
                swap_adjacent_in_seq(v, u, mh, mt, mp, ms, r_m)
            else:
                v = cand_a[ci]
                r_w = cand_wa[ci]
                swap_adjacent_in_seq(u, v, wh, wt, wp, ws, r_w)
                ex_mk = numba_ts.eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est_tmp, tail_tmp, topo, indeg)
                if ex_mk != -1:
                    for x in range(N):
                        if est_tmp[x] + dur[x] + tail_tmp[x] == ex_mk:
                            n_crit_after += 1
                swap_adjacent_in_seq(v, u, wh, wt, wp, ws, r_w)

            if ex_mk != -1:
                if is_t == 1 and ex_mk >= best_mk:
                    continue
                better = False
                if ex_mk < chosen_exact_mk:
                    better = True
                elif ex_mk == chosen_exact_mk:
                    if n_crit_after < chosen_ncrit:
                        better = True
                    elif n_crit_after == chosen_ncrit:
                        if cand_max_ml < chosen_max_ml:
                            better = True
                        elif cand_max_ml == chosen_max_ml:
                            if cand_dur_u < chosen_dur or (cand_dur_u == chosen_dur and np.random.random() < 0.10):
                                better = True
                if better:
                    chosen_exact_mk = ex_mk
                    chosen_ncrit = n_crit_after
                    chosen_max_ml = cand_max_ml
                    chosen_dur = cand_dur_u
                    chosen_idx = ci

        if chosen_idx == -1:
            u = crit_ops[np.random.randint(0, n_crit)]
            old_m = op_m[u]
            old_w = op_w[u]
            old_mp = mp[u]
            old_wp = wp[u]
            old_d = dur[u]
            numba_ts.remove_from_seq(u, mh, mt, mp, ms, old_m)
            numba_ts.remove_from_seq(u, wh, wt, wp, ws, old_w)
            a0 = alt_start[u]
            a1 = alt_start[u + 1]
            a = a0 + np.random.randint(0, min(a1 - a0, 30))
            m2 = alt_m[a]
            w2 = alt_w[a]
            d2 = alt_d[a]
            jp = job_pred[u]
            js = job_succ[u]
            j_est = (est[jp] + dur[jp]) if jp != -1 else 0
            j_tail = (dur[js] + tail[js]) if js != -1 else 0
            ma, wa, _ = find_best_joint_insertion_v4(
                mh[m2], ms, wh[w2], ws, est, tail, dur,
                j_est, j_tail, res_list,
                m_afters, m_ests, m_tails, w_afters, w_ests, w_tails,
            )
            numba_ts.insert_after_in_seq(u, ma, mh, mt, mp, ms, m2)
            numba_ts.insert_after_in_seq(u, wa, wh, wt, wp, ws, w2)
            dur[u] = d2
            new_mk = numba_ts.eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est_tmp, tail_tmp, topo, indeg)
            if new_mk != -1:
                mach_load[old_m] -= old_d
                work_load[old_w] -= old_d
                mach_load[m2] += d2
                work_load[w2] += d2
                op_alt[u] = a
                op_m[u] = m2
                op_w[u] = w2
                cur_mk = new_mk
                for i_cp in range(N):
                    est[i_cp] = est_tmp[i_cp]
                    tail[i_cp] = tail_tmp[i_cp]
            else:
                dur[u] = old_d
                numba_ts.remove_from_seq(u, mh, mt, mp, ms, m2)
                numba_ts.remove_from_seq(u, wh, wt, wp, ws, w2)
                numba_ts.insert_after_in_seq(u, old_mp, mh, mt, mp, ms, old_m)
                numba_ts.insert_after_in_seq(u, old_wp, wh, wt, wp, ws, old_w)
            no_imp += 1
            if no_imp >= max_no_improve:
                break
            continue

        # --- Commit chosen move ---
        ctype = cand_type[chosen_idx]
        u = cand_u[chosen_idx]
        ten = base_tenure + np.random.randint(0, 14)

        if ctype == 0:
            old_m = op_m[u]
            old_w = op_w[u]
            old_d = dur[u]
            a = cand_a[chosen_idx]
            m2 = alt_m[a]
            w2 = alt_w[a]
            d2 = alt_d[a]
            ma = cand_ma[chosen_idx]
            wa = cand_wa[chosen_idx]

            numba_ts.remove_from_seq(u, mh, mt, mp, ms, old_m)
            numba_ts.remove_from_seq(u, wh, wt, wp, ws, old_w)
            numba_ts.insert_after_in_seq(u, ma, mh, mt, mp, ms, m2)
            numba_ts.insert_after_in_seq(u, wa, wh, wt, wp, ws, w2)

            mach_load[old_m] -= old_d
            work_load[old_w] -= old_d
            mach_load[m2] += d2
            work_load[w2] += d2
            op_alt[u] = a
            op_m[u] = m2
            op_w[u] = w2
            dur[u] = d2
            tabu_m[u, old_m] = it + ten
            tabu_w[u, old_w] = it + ten
            tabu_op[u] = it + (ten // 2)
        elif ctype == 1:
            v = cand_a[chosen_idx]
            r_m = cand_ma[chosen_idx]
            swap_adjacent_in_seq(u, v, mh, mt, mp, ms, r_m)
            tabu_op[u] = it + (ten // 2)
            tabu_op[v] = it + (ten // 2)
        else:
            v = cand_a[chosen_idx]
            r_w = cand_wa[chosen_idx]
            swap_adjacent_in_seq(u, v, wh, wt, wp, ws, r_w)
            tabu_op[u] = it + (ten // 2)
            tabu_op[v] = it + (ten // 2)

        cur_mk = numba_ts.eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est, tail, topo, indeg)

        if cur_mk < best_mk:
            best_mk = cur_mk
            best_op_alt = op_alt.copy()
            best_est = est.copy()
            best_mh = mh.copy()
            best_mt = mt.copy()
            best_wh = wh.copy()
            best_wt = wt.copy()
            best_mp = mp.copy()
            best_ms = ms.copy()
            best_wp = wp.copy()
            best_ws = ws.copy()
            no_imp = 0
        else:
            no_imp += 1
            if no_imp >= max_no_improve:
                break

    return best_mk, best_op_alt, best_est, best_mh, best_mt, best_wh, best_wt, best_mp, best_ms, best_wp, best_ws, it, evals


@njit(cache=True)
def path_relink_v4(N, M, W, job_pred, job_succ, alt_m, alt_w, alt_d,
                   src_alt, src_m, src_w, src_d,
                   src_mh, src_mt, src_wh, src_wt,
                   src_mp, src_ms, src_wp, src_ws,
                   guide_alt, seed):
    """Path Relinking using exact O(|M|+|W|) two-pointer joint insertion."""
    np.random.seed(seed)
    op_alt = src_alt.copy()
    op_m = src_m.copy()
    op_w = src_w.copy()
    dur = src_d.copy()
    mh = src_mh.copy()
    mt = src_mt.copy()
    wh = src_wh.copy()
    wt = src_wt.copy()
    mp = src_mp.copy()
    ms = src_ms.copy()
    wp = src_wp.copy()
    ws = src_ws.copy()

    est = np.empty(N, dtype=np.int32)
    tail = np.empty(N, dtype=np.int32)
    est_tmp = np.empty(N, dtype=np.int32)
    tail_tmp = np.empty(N, dtype=np.int32)
    topo = np.empty(N, dtype=np.int32)
    indeg = np.empty(N, dtype=np.int32)
    res_list = np.empty(N + 1, dtype=np.int32)
    m_afters = np.empty(N + 1, dtype=np.int32)
    m_ests = np.empty(N + 1, dtype=np.int32)
    m_tails = np.empty(N + 1, dtype=np.int32)
    w_afters = np.empty(N + 1, dtype=np.int32)
    w_ests = np.empty(N + 1, dtype=np.int32)
    w_tails = np.empty(N + 1, dtype=np.int32)

    diff_ops = np.empty(N, dtype=np.int32)
    n_diff = 0
    for u in range(N):
        if op_alt[u] != guide_alt[u]:
            diff_ops[n_diff] = u
            n_diff += 1

    cur_mk = numba_ts.eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est, tail, topo, indeg)
    best_mk = 1000000000
    best_alt = op_alt.copy()
    best_m = op_m.copy()
    best_w = op_w.copy()
    best_d = dur.copy()
    best_mh = mh.copy()
    best_mt = mt.copy()
    best_wh = wh.copy()
    best_wt = wt.copy()
    best_mp = mp.copy()
    best_ms = ms.copy()
    best_wp = wp.copy()
    best_ws = ws.copy()

    if n_diff < 4 or cur_mk == -1:
        return cur_mk, op_alt, op_m, op_w, dur, mh, mt, wh, wt, mp, ms, wp, ws

    max_steps = min(n_diff, max(20, n_diff // 2))
    min_rec_step = max(3, max_steps // 5)

    for step in range(max_steps):
        if n_diff == 0:
            break
        best_di = 0
        best_u = diff_ops[0]
        best_ma = -1
        best_wa = -1
        best_sc = 1000000000
        n_try = n_diff if n_diff <= 14 else 14

        for t_i in range(n_try):
            di = t_i if n_diff <= 14 else np.random.randint(0, n_diff)
            u = diff_ops[di]
            old_m = op_m[u]
            old_w = op_w[u]
            old_mp = mp[u]
            old_wp = wp[u]
            a2 = guide_alt[u]
            m2 = alt_m[a2]
            w2 = alt_w[a2]
            d2 = alt_d[a2]

            jp = job_pred[u]
            js = job_succ[u]
            j_est = (est[jp] + dur[jp]) if jp != -1 else 0
            j_tail = (dur[js] + tail[js]) if js != -1 else 0

            numba_ts.remove_from_seq(u, mh, mt, mp, ms, old_m)
            numba_ts.remove_from_seq(u, wh, wt, wp, ws, old_w)
            ma, wa, lb_no_d = find_best_joint_insertion_v4(
                mh[m2], ms, wh[w2], ws, est, tail, dur,
                j_est, j_tail, res_list,
                m_afters, m_ests, m_tails, w_afters, w_ests, w_tails,
            )
            numba_ts.insert_after_in_seq(u, old_mp, mh, mt, mp, ms, old_m)
            numba_ts.insert_after_in_seq(u, old_wp, wh, wt, wp, ws, old_w)

            sc = lb_no_d + d2 - (2 if est[u] + dur[u] + tail[u] == cur_mk else 0)
            if sc < best_sc:
                best_sc = sc
                best_di = di
                best_u = u
                best_ma = ma
                best_wa = wa

        u = best_u
        diff_ops[best_di] = diff_ops[n_diff - 1]
        n_diff -= 1

        old_m = op_m[u]
        old_w = op_w[u]
        old_mp = mp[u]
        old_wp = wp[u]
        old_d = dur[u]
        a2 = guide_alt[u]
        m2 = alt_m[a2]
        w2 = alt_w[a2]
        d2 = alt_d[a2]

        numba_ts.remove_from_seq(u, mh, mt, mp, ms, old_m)
        numba_ts.remove_from_seq(u, wh, wt, wp, ws, old_w)
        numba_ts.insert_after_in_seq(u, best_ma, mh, mt, mp, ms, m2)
        numba_ts.insert_after_in_seq(u, best_wa, wh, wt, wp, ws, w2)
        dur[u] = d2
        new_mk = numba_ts.eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est_tmp, tail_tmp, topo, indeg)
        if new_mk != -1:
            op_alt[u] = a2
            op_m[u] = m2
            op_w[u] = w2
            cur_mk = new_mk
            for i_cp in range(N):
                est[i_cp] = est_tmp[i_cp]
                tail[i_cp] = tail_tmp[i_cp]
            if step >= min_rec_step and cur_mk < best_mk:
                best_mk = cur_mk
                best_alt = op_alt.copy()
                best_m = op_m.copy()
                best_w = op_w.copy()
                best_d = dur.copy()
                best_mh = mh.copy()
                best_mt = mt.copy()
                best_wh = wh.copy()
                best_wt = wt.copy()
                best_mp = mp.copy()
                best_ms = ms.copy()
                best_wp = wp.copy()
                best_ws = ws.copy()
        else:
            dur[u] = old_d
            numba_ts.remove_from_seq(u, mh, mt, mp, ms, m2)
            numba_ts.remove_from_seq(u, wh, wt, wp, ws, w2)
            numba_ts.insert_after_in_seq(u, old_mp, mh, mt, mp, ms, old_m)
            numba_ts.insert_after_in_seq(u, old_wp, wh, wt, wp, ws, old_w)

    if best_mk == 1000000000:
        return cur_mk, op_alt, op_m, op_w, dur, mh, mt, wh, wt, mp, ms, wp, ws
    return best_mk, best_alt, best_m, best_w, best_d, best_mh, best_mt, best_wh, best_wt, best_mp, best_ms, best_wp, best_ws


@njit(cache=True)
def perturb_v4(N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d,
               op_alt_in, op_m_in, op_w_in, dur_in,
               mh_in, mt_in, wh_in, wt_in,
               mp_in, ms_in, wp_in, ws_in,
               n_kicks, seed):
    """Joint-insertion perturbation kick using exact two-pointer slot selection."""
    np.random.seed(seed)
    op_alt = op_alt_in.copy()
    op_m = op_m_in.copy()
    op_w = op_w_in.copy()
    dur = dur_in.copy()
    mh = mh_in.copy()
    mt = mt_in.copy()
    wh = wh_in.copy()
    wt = wt_in.copy()
    mp = mp_in.copy()
    ms = ms_in.copy()
    wp = wp_in.copy()
    ws = ws_in.copy()

    est = np.empty(N, dtype=np.int32)
    tail = np.empty(N, dtype=np.int32)
    est_tmp = np.empty(N, dtype=np.int32)
    tail_tmp = np.empty(N, dtype=np.int32)
    topo = np.empty(N, dtype=np.int32)
    indeg = np.empty(N, dtype=np.int32)
    res_list = np.empty(N + 1, dtype=np.int32)
    crit_ops = np.empty(N, dtype=np.int32)
    m_afters = np.empty(N + 1, dtype=np.int32)
    m_ests = np.empty(N + 1, dtype=np.int32)
    m_tails = np.empty(N + 1, dtype=np.int32)
    w_afters = np.empty(N + 1, dtype=np.int32)
    w_ests = np.empty(N + 1, dtype=np.int32)
    w_tails = np.empty(N + 1, dtype=np.int32)

    cur_mk = numba_ts.eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est, tail, topo, indeg)
    if cur_mk == -1:
        return op_alt, op_m, op_w, dur, mh, mt, wh, wt, mp, ms, wp, ws

    for _ in range(n_kicks):
        n_crit = 0
        for u in range(N):
            if est[u] + dur[u] + tail[u] >= cur_mk - 3:
                crit_ops[n_crit] = u
                n_crit += 1

        if n_crit > 0 and np.random.random() < 0.70:
            u = crit_ops[np.random.randint(0, n_crit)]
        else:
            u = np.random.randint(0, N)

        old_m = op_m[u]
        old_w = op_w[u]
        old_mp = mp[u]
        old_wp = wp[u]
        old_d = dur[u]

        numba_ts.remove_from_seq(u, mh, mt, mp, ms, old_m)
        numba_ts.remove_from_seq(u, wh, wt, wp, ws, old_w)

        a0 = alt_start[u]
        a1 = alt_start[u + 1]
        span = a1 - a0
        top_k = span if span <= 80 else 80
        a = a0 + np.random.randint(0, top_k)
        m2 = alt_m[a]
        w2 = alt_w[a]
        d2 = alt_d[a]

        jp = job_pred[u]
        js = job_succ[u]
        j_est = (est[jp] + dur[jp]) if jp != -1 else 0
        j_tail = (dur[js] + tail[js]) if js != -1 else 0

        ma, wa, _ = find_best_joint_insertion_v4(
            mh[m2], ms, wh[w2], ws, est, tail, dur,
            j_est, j_tail, res_list,
            m_afters, m_ests, m_tails, w_afters, w_ests, w_tails,
        )

        numba_ts.insert_after_in_seq(u, ma, mh, mt, mp, ms, m2)
        numba_ts.insert_after_in_seq(u, wa, wh, wt, wp, ws, w2)
        dur[u] = d2
        new_mk = numba_ts.eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est_tmp, tail_tmp, topo, indeg)
        if new_mk != -1:
            op_alt[u] = a
            op_m[u] = m2
            op_w[u] = w2
            cur_mk = new_mk
            for i_cp in range(N):
                est[i_cp] = est_tmp[i_cp]
                tail[i_cp] = tail_tmp[i_cp]
        else:
            dur[u] = old_d
            numba_ts.remove_from_seq(u, mh, mt, mp, ms, m2)
            numba_ts.remove_from_seq(u, wh, wt, wp, ws, w2)
            numba_ts.insert_after_in_seq(u, old_mp, mh, mt, mp, ms, old_m)
            numba_ts.insert_after_in_seq(u, old_wp, wh, wt, wp, ws, old_w)

    return op_alt, op_m, op_w, dur, mh, mt, wh, wt, mp, ms, wp, ws


def generate_cpsat_balanced_seeds(nb_inst, n_seeds=6, per_seed_s=3.0, seed0=100):
    """
    Option 2 Seeder: Solve pure resource-assignment CP-SAT (no sequencing) on pruned modes
    to produce n_seeds globally load-balanced initial (m, w) assignments, then decode
    each into a low-makespan feasible schedule in Numba.
    """
    N = int(nb_inst["N"])
    M = int(nb_inst["M"])
    W = int(nb_inst["W"])
    job_pred = nb_inst["job_pred"]
    job_succ = nb_inst["job_succ"]
    alt_start = nb_inst["alt_start"]
    alt_m = nb_inst["alt_m"]
    alt_w = nb_inst["alt_w"]
    alt_d = nb_inst["alt_d"]

    # Build pruned candidate mode index lists per operation (faster solving on M > 30 like Behnke60)
    cap_m = 16 if M > 30 else 25
    hard_cap_m = 20 if M > 30 else 32
    if M > 30:
        per_seed_s = max(per_seed_s, 4.5)
    op_cands = []
    for u in range(N):
        a0 = int(alt_start[u])
        a1 = int(alt_start[u + 1])
        by_m = {}
        for a in range(a0, a1):
            m = int(alt_m[a])
            d = int(alt_d[a])
            by_m.setdefault(m, []).append((d, a))
        firsts = []
        extras = []
        for m, items in by_m.items():
            items.sort()
            firsts.append(items[0])
            for it in items[1:2]:
                extras.append(it)
        firsts.sort()
        extras.sort()
        if len(firsts) >= cap_m:
            chosen = [a for _, a in firsts[: min(len(firsts), hard_cap_m)]]
        else:
            chosen = [a for _, a in (firsts + extras[: cap_m - len(firsts)])]
        op_cands.append(chosen)

    seeds_out = []
    weight_profiles = [
        (100, 30, 0),
        (120, 40, 2),
        (80, 40, 3),
        (100, 20, 4),
        (90, 35, 3),
        (110, 25, 5),
    ]

    diag_stats = []
    for s_idx in range(n_seeds):
        wm, ww, jit_max = weight_profiles[s_idx % len(weight_profiles)]
        rng = np.random.default_rng(seed0 + s_idx * 97)

        cm = cp_model.CpModel()
        x_vars = []
        mach_terms = [[] for _ in range(M)]
        work_terms = [[] for _ in range(W)]
        obj_terms = []
        max_sum_d = 0

        for u in range(N):
            cands = op_cands[u]
            xs = [cm.NewBoolVar("") for _ in cands]
            cm.AddExactlyOne(xs)
            x_vars.append((cands, xs))
            max_sum_d += int(alt_d[cands[-1]])
            for a, bvar in zip(cands, xs):
                m = int(alt_m[a])
                w = int(alt_w[a])
                d = int(alt_d[a])
                mach_terms[m].append(d * bvar)
                work_terms[w].append(d * bvar)
                jit = int(rng.integers(0, jit_max + 1)) if jit_max > 0 else 0
                obj_terms.append((d + jit) * bvar)

        L_m = cm.NewIntVar(0, max_sum_d, "Lm")
        L_w = cm.NewIntVar(0, max_sum_d, "Lw")
        for m in range(M):
            if mach_terms[m]:
                cm.Add(sum(mach_terms[m]) <= L_m)
        for w in range(W):
            if work_terms[w]:
                cm.Add(sum(work_terms[w]) <= L_w)
        cm.Minimize(wm * L_m + ww * L_w + sum(obj_terms))

        sv = cp_model.CpSolver()
        sv.parameters.max_time_in_seconds = float(per_seed_s)
        sv.parameters.num_workers = 1
        sv.parameters.random_seed = int(seed0 + s_idx * 71)
        st = sv.Solve(cm)

        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            continue

        op_alt_arr = np.empty(N, dtype=np.int32)
        for u in range(N):
            cands, xs = x_vars[u]
            chosen_a = cands[0]
            for a, bvar in zip(cands, xs):
                if sv.Value(bvar):
                    chosen_a = a
                    break
            op_alt_arr[u] = chosen_a

        # Decode with 3 priority rules and keep lowest initial makespan
        best_dec = None
        for rule in (0, 1, 2):
            dec = decode_fixed_assignment(
                N, M, W, job_pred, job_succ, op_alt_arr, alt_m, alt_w, alt_d,
                seed0 + s_idx * 31 + rule, rule,
            )
            if best_dec is None or dec[0] < best_dec[0]:
                best_dec = dec

        m_loads = np.zeros(M, dtype=np.int32)
        for u in range(N):
            m_loads[alt_m[op_alt_arr[u]]] += alt_d[op_alt_arr[u]]
        diag_stats.append((int(m_loads.max()), round(float(alt_d[op_alt_arr].mean()), 2), int(best_dec[0])))
        seeds_out.append(best_dec[1:])

    return seeds_out, diag_stats


def _elite_update(elite_pool, mk, state, max_pool=8, min_diff_frac=0.08):
    """Maintain up to max_pool structurally diverse elite solutions."""
    alt = state[0]
    N = len(alt)
    min_diff = max(3, int(N * min_diff_frac))

    for idx, (emk, estate) in enumerate(elite_pool):
        if int(np.sum(alt != estate[0])) < min_diff:
            if mk < emk:
                elite_pool[idx] = (mk, state)
                elite_pool.sort(key=lambda x: x[0])
            return

    if len(elite_pool) < max_pool:
        elite_pool.append((mk, state))
        elite_pool.sort(key=lambda x: x[0])
    elif mk < elite_pool[-1][0]:
        elite_pool[-1] = (mk, state)
        elite_pool.sort(key=lambda x: x[0])


def cmrts_v4_search(inst_name, nb_inst, time_budget_s=900.0, seed0=100):
    """
    Full v4 Option 1 + Option 2 Memetic Tabu Search:
      - Seeds with 6 CP-SAT ultra-low-load balanced schedules (~18s upfront)
      - Alternates across Path Relinking (25%), Perturbed-Elite ILS (50%), and
        fresh diverse greedy starts (25%) using v4 exact two-pointer + N6 + plateau tie-break TS.
    """
    t0 = time.time()
    N = nb_inst["N"]
    M = nb_inst["M"]
    W = nb_inst["W"]
    job_pred = nb_inst["job_pred"]
    job_succ = nb_inst["job_succ"]
    alt_start = nb_inst["alt_start"]
    alt_m = nb_inst["alt_m"]
    alt_w = nb_inst["alt_w"]
    alt_d = nb_inst["alt_d"]

    max_modes = 90 if N <= 250 else 65
    cpsat_seeds, cpsat_diag = generate_cpsat_balanced_seeds(
        nb_inst, n_seeds=6, per_seed_s=3.0, seed0=seed0
    )

    best_mk = 10**9
    best_state = None
    elite_pool = []
    total_evals = 0
    total_iters = 0
    starts = 0
    ils_kicks = 0
    pr_runs = 0
    best_found_at = 0.0

    while time.time() - t0 < time_budget_s:
        rem_s = time_budget_s - (time.time() - t0)
        if rem_s < 1.5:
            break
        seed = seed0 + starts * 137

        if starts < len(cpsat_seeds):
            init = cpsat_seeds[starts]
            max_it = 12000
            max_ni = 1400
        elif starts % 4 == 0:
            noise = 0.20 + 0.80 * ((starts % 5) / 4.0)
            init = construct_load_balanced(
                N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d, seed, noise
            )
            max_it = 9000
            max_ni = 1000
        elif len(elite_pool) >= 2 and (starts % 4 == 2):
            i_src = pr_runs % len(elite_pool)
            i_g = (i_src + 1 + (pr_runs // len(elite_pool)) % (len(elite_pool) - 1)) % len(elite_pool)
            s_st = elite_pool[i_src][1]
            g_alt = elite_pool[i_g][1][0]
            pr_res = path_relink_v4(
                N, M, W, job_pred, job_succ, alt_m, alt_w, alt_d,
                s_st[0], s_st[1], s_st[2], s_st[3],
                s_st[4], s_st[5], s_st[6], s_st[7],
                s_st[8], s_st[9], s_st[10], s_st[11],
                g_alt, seed,
            )
            init = pr_res[1:]
            pr_runs += 1
            max_it = 12000
            max_ni = 1400
        else:
            src_idx = 0 if (len(elite_pool) == 1 or (ils_kicks % 3 != 2)) else (1 + (ils_kicks % (len(elite_pool) - 1)))
            st = elite_pool[src_idx][1]
            n_kicks = 6 + (ils_kicks % 4) * 5
            init = perturb_v4(
                N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d,
                st[0], st[1], st[2], st[3],
                st[4], st[5], st[6], st[7],
                st[8], st[9], st[10], st[11],
                n_kicks, seed,
            )
            ils_kicks += 1
            max_it = 12000
            max_ni = 1400

        res = tabu_search_v4_run(
            N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d,
            seed + 1, max_it, max_ni, max_modes,
            init[0], init[1], init[2], init[3],
            init[4], init[5], init[6], init[7],
            init[8], init[9], init[10], init[11],
        )
        mk = int(res[0])
        b_alt, b_est = res[1], res[2]
        b_mh, b_mt, b_wh, b_wt = res[3], res[4], res[5], res[6]
        b_mp, b_ms, b_wp, b_ws = res[7], res[8], res[9], res[10]
        total_iters += int(res[11])
        total_evals += int(res[12])
        starts += 1

        b_m_arr = alt_m[b_alt].astype(np.int32)
        b_w_arr = alt_w[b_alt].astype(np.int32)
        b_d_arr = alt_d[b_alt].astype(np.int32)
        state = (
            b_alt.copy(), b_m_arr, b_w_arr, b_d_arr,
            b_mh.copy(), b_mt.copy(), b_wh.copy(), b_wt.copy(),
            b_mp.copy(), b_ms.copy(), b_wp.copy(), b_ws.copy(),
            b_est.copy(),
        )
        _elite_update(elite_pool, mk, state)

        if mk < best_mk:
            best_mk = mk
            best_state = state
            best_found_at = round(time.time() - t0, 1)

    stats = dict(
        cpsat_seeds=len(cpsat_seeds),
        cpsat_diag=cpsat_diag,
        starts=starts,
        ils_kicks=ils_kicks,
        pr_runs=pr_runs,
        elite_sz=len(elite_pool),
        iters=total_iters,
        evals=total_evals,
        best_at_s=best_found_at,
        secs=round(time.time() - t0, 2),
    )
    return best_mk, best_state, stats
