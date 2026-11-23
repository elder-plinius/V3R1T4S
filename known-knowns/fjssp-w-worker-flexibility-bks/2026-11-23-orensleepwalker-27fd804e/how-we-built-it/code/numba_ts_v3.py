"""
Numba Critical-Path Tabu Search v3 (numba_ts_v3.py) for FJSSP-W.
Five major structural upgrades over v2 (specifically targeting crowded bottlenecks
like Behnke16-20, Behnke60, Behnke32-35, and DPpaulli):

  1. Exact Clean Scratch Buffers (est_tmp, tail_tmp): fixes v1/v2 bug where verifying
     candidate moves inside the neighborhood loop overwrote est/tail in-place.
  2. Joint Two-Resource Idle-Slot Insertion (find_best_joint_insertion): evaluates
     top valid M&G positions on machine m2 AND worker w2 jointly to match overlapping
     idle gaps instead of picking m_after and w_after independently.
  3. Load-Aware Mode Selection: tracks live mach_load[M] and work_load[W] in O(1)
     and scans fastest modes + least-loaded eligible (m, w) pairs + random modes.
  4. True N5 Critical-Block Swap Neighborhood: tests adjacent critical arcs on the
     same machine or worker (zero mode change, unlocks tight critical blocks).
  5. Elite Pool + Path Relinking + Iterated Tabu Search (CMRTS-style): keeps up to 8
     structurally diverse elite schedules and periodically relinks pairs (S_init -> S_guide)
     to bridge distant basins.
"""
import time
import numpy as np
from numba import njit

import numba_ts


@njit(cache=True)
def collect_valid_positions(head_r, succ, est, tail, dur, j_est, j_tail,
                            res_list, out_after, out_est, out_tail, max_keep):
    """
    Collect up to max_keep best Mastrolilli-Gambardella valid insertion slots on resource r.
    Returns count of kept slots (at least 1).
    """
    k = 0
    cur = head_r
    while cur != -1:
        res_list[k] = cur
        k += 1
        cur = succ[cur]

    if k == 0:
        out_after[0] = -1
        out_est[0] = 0
        out_tail[0] = 0
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

    n_kept = 0
    # Keep up to max_keep slots sorted by single-resource lb = max(j_est, r_est) + max(j_tail, r_tail)
    # Using a tiny inline insertion sort (max_keep <= 4)
    best_lb = np.empty(4, dtype=np.int32)
    for pos in range(lo, hi + 1):
        r_est = est[res_list[pos - 1]] + dur[res_list[pos - 1]] if pos > 0 else 0
        r_tail = dur[res_list[pos]] + tail[res_list[pos]] if pos < k else 0
        e = j_est if j_est > r_est else r_est
        t = j_tail if j_tail > r_tail else r_tail
        lb = e + t
        after_node = res_list[pos - 1] if pos > 0 else -1

        if n_kept < max_keep:
            idx = n_kept
            n_kept += 1
            while idx > 0 and lb < best_lb[idx - 1]:
                best_lb[idx] = best_lb[idx - 1]
                out_after[idx] = out_after[idx - 1]
                out_est[idx] = out_est[idx - 1]
                out_tail[idx] = out_tail[idx - 1]
                idx -= 1
            best_lb[idx] = lb
            out_after[idx] = after_node
            out_est[idx] = r_est
            out_tail[idx] = r_tail
        elif lb < best_lb[max_keep - 1]:
            idx = max_keep - 1
            while idx > 0 and lb < best_lb[idx - 1]:
                best_lb[idx] = best_lb[idx - 1]
                out_after[idx] = out_after[idx - 1]
                out_est[idx] = out_est[idx - 1]
                out_tail[idx] = out_tail[idx - 1]
                idx -= 1
            best_lb[idx] = lb
            out_after[idx] = after_node
            out_est[idx] = r_est
            out_tail[idx] = r_tail

    return n_kept


@njit(cache=True)
def find_best_joint_insertion(mh_r, ms, wh_r, ws, est, tail, dur,
                              j_est, j_tail, res_list,
                              m_afters, m_ests, m_tails,
                              w_afters, w_ests, w_tails):
    """
    Jointly choose (m_after, w_after) from the top-4 valid M&G positions on machine m2
    and top-4 valid M&G positions on worker w2 to minimize:
        max(j_est, m_est, w_est) + max(j_tail, m_tail, w_tail)
    Returns (best_m_after, best_w_after, best_lb_without_d).
    """
    nm = collect_valid_positions(mh_r, ms, est, tail, dur, j_est, j_tail,
                                 res_list, m_afters, m_ests, m_tails, 4)
    nw = collect_valid_positions(wh_r, ws, est, tail, dur, j_est, j_tail,
                                 res_list, w_afters, w_ests, w_tails, 4)

    best_lb = 1000000000
    best_ma = m_afters[0]
    best_wa = w_afters[0]
    for i in range(nm):
        me = m_ests[i]
        mt = m_tails[i]
        e0 = j_est if j_est > me else me
        t0 = j_tail if j_tail > mt else mt
        for j in range(nw):
            we = w_ests[j]
            wt = w_tails[j]
            e = e0 if e0 > we else we
            t = t0 if t0 > wt else wt
            lb = e + t
            if lb < best_lb:
                best_lb = lb
                best_ma = m_afters[i]
                best_wa = w_afters[j]
    return best_ma, best_wa, best_lb


@njit(cache=True)
def construct_load_balanced(N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d,
                            seed, noise_lvl):
    """
    Diverse randomized constructive heuristic with 4 priority rules including
    Global Load-Balanced ECT (essential for crowded Behnke16-20 / Behnke60).
    """
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

    rule = seed % 4  # 0: MWR, 1: Earliest-Finish, 2: Load-Balanced, 3: Mixed
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
def tabu_search_v3_run(N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d,
                       seed, max_iters, max_no_improve, max_modes_per_op,
                       init_op_alt, init_op_m, init_op_w, init_dur,
                       init_mh, init_mt, init_wh, init_wt,
                       init_mp, init_ms, init_wp, init_ws):
    """
    Upgraded Numba Critical-Path Tabu Search v3:
      - Clean scratch buffers (est_tmp, tail_tmp) so est/tail are NEVER corrupted mid-scan.
      - Load-aware mode selection (fastest + least-loaded eligible (m, w) + random).
      - Joint two-resource idle-slot insertion (find_best_joint_insertion).
      - Top-K exact DAG verification per iteration (verifies top-8 candidates + N5 swaps).
      - True N5 adjacent critical-arc swaps on machines and workers.
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

    # Live machine & worker load tracking
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
    res_list = np.empty(N, dtype=np.int32)
    crit_ops = np.empty(N, dtype=np.int32)
    is_crit = np.zeros(N, dtype=np.int8)

    # Small fixed buffers for joint insertion
    m_afters = np.empty(4, dtype=np.int32)
    m_ests = np.empty(4, dtype=np.int32)
    m_tails = np.empty(4, dtype=np.int32)
    w_afters = np.empty(4, dtype=np.int32)
    w_ests = np.empty(4, dtype=np.int32)
    w_tails = np.empty(4, dtype=np.int32)

    # Top-K candidate move buffer (K = 10): type 0 = reassign+insert, type 1 = mach swap, type 2 = work swap
    K_TOP = 10
    cand_lb = np.empty(K_TOP, dtype=np.int32)
    cand_type = np.empty(K_TOP, dtype=np.int8)
    cand_u = np.empty(K_TOP, dtype=np.int32)
    cand_a = np.empty(K_TOP, dtype=np.int32)  # alt idx (type 0) or partner v (type 1/2)
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
    base_tenure = 12 + (N // 28)

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

        # Reset top-K candidate heap
        n_cand = 0
        worst_cand_lb = 1000000000

        step_c = 1 if n_crit <= 48 else (n_crit // 48)
        offset_c = it % step_c

        # Adaptive load-weight for mode filtering on large alternative sets
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

            # --- Neighborhood A: N5 Adjacent Critical-Block Swaps on Machine & Worker ---
            v_m = ms[u]
            if v_m != -1 and is_crit[v_m] == 1 and est[u] + old_d == est[v_m]:
                # Only swap if not job-related and on block boundary (classic N5)
                if job_succ[u] != v_m and job_pred[v_m] != u:
                    u_prev_c = (old_mp != -1 and is_crit[old_mp] == 1 and est[old_mp] + dur[old_mp] == est[u])
                    v_next = ms[v_m]
                    v_next_c = (v_next != -1 and is_crit[v_next] == 1 and est[v_m] + dur[v_m] == est[v_next])
                    if (not u_prev_c) or (not v_next_c):
                        # Quick proxy score for swapping (u, v_m)
                        # v_m moves before u: approximate new length through u, v_m
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
                        if (is_t == 0 or est_lb < best_mk) and (n_cand < K_TOP or est_lb < worst_cand_lb):
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
                            cand_type[idx] = 1
                            cand_u[idx] = u
                            cand_a[idx] = v_m
                            cand_ma[idx] = old_m
                            cand_wa[idx] = 0
                            cand_tabu[idx] = is_t
                            worst_cand_lb = cand_lb[n_cand - 1]

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
                        if (is_t == 0 or est_lb < best_mk) and (n_cand < K_TOP or est_lb < worst_cand_lb):
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
                            cand_type[idx] = 2
                            cand_u[idx] = u
                            cand_a[idx] = v_w
                            cand_ma[idx] = 0
                            cand_wa[idx] = old_w
                            cand_tabu[idx] = is_t
                            worst_cand_lb = cand_lb[n_cand - 1]

            # --- Neighborhood B: Load-Aware Mode Reassignment + Joint Idle-Slot Insertion ---
            jp = job_pred[u]
            js = job_succ[u]
            j_est = (est[jp] + dur[jp]) if jp != -1 else 0
            j_tail = (dur[js] + tail[js]) if js != -1 else 0

            numba_ts.remove_from_seq(u, mh, mt, mp, ms, old_m)
            numba_ts.remove_from_seq(u, wh, wt, wp, ws, old_w)

            a0 = alt_start[u]
            a1 = alt_start[u + 1]
            n_alts = a1 - a0

            # If n_alts <= max_modes_per_op, scan ALL modes; otherwise scan:
            #   - top fastest 20 modes
            #   - load-aware modes (those on below-average loaded machine OR worker, strided/sampled)
            #   - random modes for diversity
            if n_alts <= max_modes_per_op:
                for a in range(a0, a1):
                    m2 = alt_m[a]
                    w2 = alt_w[a]
                    d2 = alt_d[a]
                    if j_est + d2 + j_tail > worst_cand_lb + 2:
                        continue
                    ma, wa, lb_no_d = find_best_joint_insertion(
                        mh[m2], ms, wh[w2], ws, est, tail, dur,
                        j_est, j_tail, res_list,
                        m_afters, m_ests, m_tails, w_afters, w_ests, w_tails
                    )
                    if a == old_a and ma == old_mp and wa == old_wp:
                        continue
                    est_lb = lb_no_d + d2
                    evals += 1
                    is_t = 1 if ((tabu_m[u, m2] > it) or (tabu_w[u, w2] > it) or (tabu_op[u] > it)) else 0
                    if is_t == 1 and est_lb >= best_mk:
                        continue
                    if n_cand < K_TOP or est_lb < worst_cand_lb or (est_lb == worst_cand_lb and np.random.random() < 0.25):
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
                        cand_type[idx] = 0
                        cand_u[idx] = u
                        cand_a[idx] = a
                        cand_ma[idx] = ma
                        cand_wa[idx] = wa
                        cand_tabu[idx] = is_t
                        worst_cand_lb = cand_lb[n_cand - 1]
            else:
                # 1) Top 20 fastest modes
                n_fast = 20
                for a in range(a0, a0 + n_fast):
                    m2 = alt_m[a]
                    w2 = alt_w[a]
                    d2 = alt_d[a]
                    if j_est + d2 + j_tail > worst_cand_lb + 2:
                        continue
                    ma, wa, lb_no_d = find_best_joint_insertion(
                        mh[m2], ms, wh[w2], ws, est, tail, dur,
                        j_est, j_tail, res_list,
                        m_afters, m_ests, m_tails, w_afters, w_ests, w_tails
                    )
                    if a == old_a and ma == old_mp and wa == old_wp:
                        continue
                    est_lb = lb_no_d + d2
                    evals += 1
                    is_t = 1 if ((tabu_m[u, m2] > it) or (tabu_w[u, w2] > it) or (tabu_op[u] > it)) else 0
                    if is_t == 1 and est_lb >= best_mk:
                        continue
                    if n_cand < K_TOP or est_lb < worst_cand_lb or (est_lb == worst_cand_lb and np.random.random() < 0.25):
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
                        cand_type[idx] = 0
                        cand_u[idx] = u
                        cand_a[idx] = a
                        cand_ma[idx] = ma
                        cand_wa[idx] = wa
                        cand_tabu[idx] = is_t
                        worst_cand_lb = cand_lb[n_cand - 1]

                # 2) Load-aware scan: sweep remaining modes cheaply and evaluate those on lightly loaded machines/workers
                #    Cap evaluated modes to max_modes_per_op - n_fast
                rem_budget = max_modes_per_op - n_fast
                load_checked = 0
                # Start at a rotating offset so all machines/workers get fair coverage over iterations
                span = n_alts - n_fast
                start_off = (it * 37 + u * 13) % span
                for step_k in range(span):
                    if load_checked >= rem_budget:
                        break
                    a = a0 + n_fast + ((start_off + step_k) % span)
                    m2 = alt_m[a]
                    w2 = alt_w[a]
                    d2 = alt_d[a]
                    # Filter: prefer lightly loaded machine or worker (or accept 15% random diversity)
                    if mach_load[m2] > avg_m_load and work_load[w2] > avg_m_load and (step_k % 7 != 0):
                        continue
                    if j_est + d2 + j_tail > worst_cand_lb + 2:
                        continue
                    load_checked += 1
                    ma, wa, lb_no_d = find_best_joint_insertion(
                        mh[m2], ms, wh[w2], ws, est, tail, dur,
                        j_est, j_tail, res_list,
                        m_afters, m_ests, m_tails, w_afters, w_ests, w_tails
                    )
                    if a == old_a and ma == old_mp and wa == old_wp:
                        continue
                    est_lb = lb_no_d + d2
                    evals += 1
                    is_t = 1 if ((tabu_m[u, m2] > it) or (tabu_w[u, w2] > it) or (tabu_op[u] > it)) else 0
                    if is_t == 1 and est_lb >= best_mk:
                        continue
                    if n_cand < K_TOP or est_lb < worst_cand_lb or (est_lb == worst_cand_lb and np.random.random() < 0.25):
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
                        cand_type[idx] = 0
                        cand_u[idx] = u
                        cand_a[idx] = a
                        cand_ma[idx] = ma
                        cand_wa[idx] = wa
                        cand_tabu[idx] = is_t
                        worst_cand_lb = cand_lb[n_cand - 1]

            # Restore u to original position (est/tail were NEVER modified!)
            numba_ts.insert_after_in_seq(u, old_mp, mh, mt, mp, ms, old_m)
            numba_ts.insert_after_in_seq(u, old_wp, wh, wt, wp, ws, old_w)

        # --- Exact DAG verification of Top-K candidate moves using CLEAN est_tmp/tail_tmp ---
        chosen_idx = -1
        chosen_exact_mk = 1000000000

        for ci in range(n_cand):
            ctype = cand_type[ci]
            u = cand_u[ci]
            is_t = cand_tabu[ci]

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
                swap_adjacent_in_seq(v, u, mh, mt, mp, ms, r_m)
            else:
                v = cand_a[ci]
                r_w = cand_wa[ci]
                swap_adjacent_in_seq(u, v, wh, wt, wp, ws, r_w)
                ex_mk = numba_ts.eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est_tmp, tail_tmp, topo, indeg)
                swap_adjacent_in_seq(v, u, wh, wt, wp, ws, r_w)

            if ex_mk != -1:
                if is_t == 1 and ex_mk >= best_mk:
                    continue
                if ex_mk < chosen_exact_mk or (ex_mk == chosen_exact_mk and np.random.random() < 0.3):
                    chosen_exact_mk = ex_mk
                    chosen_idx = ci

        if chosen_idx == -1:
            # Safe diversification kick on a critical op
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
            ma, wa, _ = find_best_joint_insertion(
                mh[m2], ms, wh[w2], ws, est, tail, dur,
                j_est, j_tail, res_list,
                m_afters, m_ests, m_tails, w_afters, w_ests, w_tails
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
        ten = base_tenure + np.random.randint(0, 12)

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
def path_relink_step(N, M, W, job_pred, job_succ, alt_m, alt_w, alt_d,
                     src_alt, src_m, src_w, src_d,
                     src_mh, src_mt, src_wh, src_wt,
                     src_mp, src_ms, src_wp, src_ws,
                     guide_alt, seed):
    """
    Path Relinking from source schedule toward guide schedule's (m, w) mode assignments.
    At each step, picks a differing operation (preferring critical ops), reassigns it to
    guide_alt[u] using exact joint idle-slot insertion, and returns the best intermediate
    feasible schedule found along the path (at least 15% away from endpoints).
    """
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
    res_list = np.empty(N, dtype=np.int32)
    m_afters = np.empty(4, dtype=np.int32)
    m_ests = np.empty(4, dtype=np.int32)
    m_tails = np.empty(4, dtype=np.int32)
    w_afters = np.empty(4, dtype=np.int32)
    w_ests = np.empty(4, dtype=np.int32)
    w_tails = np.empty(4, dtype=np.int32)

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
        # Sample up to 12 differing ops and pick the one whose move to guide_alt[u] gives lowest lb
        best_di = 0
        best_u = diff_ops[0]
        best_ma = -1
        best_wa = -1
        best_sc = 1000000000
        n_try = n_diff if n_diff <= 12 else 12

        for t_i in range(n_try):
            di = t_i if n_diff <= 12 else np.random.randint(0, n_diff)
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
            ma, wa, lb_no_d = find_best_joint_insertion(
                mh[m2], ms, wh[w2], ws, est, tail, dur,
                j_est, j_tail, res_list,
                m_afters, m_ests, m_tails, w_afters, w_ests, w_tails
            )
            numba_ts.insert_after_in_seq(u, old_mp, mh, mt, mp, ms, old_m)
            numba_ts.insert_after_in_seq(u, old_wp, wh, wt, wp, ws, old_w)

            sc = lb_no_d + d2
            # Small bonus if u is critical
            if est[u] + dur[u] + tail[u] == cur_mk:
                sc -= 2
            if sc < best_sc:
                best_sc = sc
                best_di = di
                best_u = u
                best_ma = ma
                best_wa = wa

        # Apply best_u -> guide_alt[best_u]
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
def perturb_v3(N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d,
               op_alt_in, op_m_in, op_w_in, dur_in,
               mh_in, mt_in, wh_in, wt_in,
               mp_in, ms_in, wp_in, ws_in,
               n_kicks, seed):
    """Joint-insertion perturbation kick biased 70% toward critical/near-critical ops."""
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
    res_list = np.empty(N, dtype=np.int32)
    crit_ops = np.empty(N, dtype=np.int32)
    m_afters = np.empty(4, dtype=np.int32)
    m_ests = np.empty(4, dtype=np.int32)
    m_tails = np.empty(4, dtype=np.int32)
    w_afters = np.empty(4, dtype=np.int32)
    w_ests = np.empty(4, dtype=np.int32)
    w_tails = np.empty(4, dtype=np.int32)

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
        # Allow broader mode pool on kicks to escape crowded machines
        top_k = span if span <= 80 else 80
        a = a0 + np.random.randint(0, top_k)
        m2 = alt_m[a]
        w2 = alt_w[a]
        d2 = alt_d[a]

        jp = job_pred[u]
        js = job_succ[u]
        j_est = (est[jp] + dur[jp]) if jp != -1 else 0
        j_tail = (dur[js] + tail[js]) if js != -1 else 0

        ma, wa, _ = find_best_joint_insertion(
            mh[m2], ms, wh[w2], ws, est, tail, dur,
            j_est, j_tail, res_list,
            m_afters, m_ests, m_tails, w_afters, w_ests, w_tails
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


def _elite_update(elite_pool, mk, state, max_pool=8, min_diff_frac=0.08):
    """Maintain up to max_pool structurally diverse elite solutions (sorted by mk ascending)."""
    alt = state[0]
    N = len(alt)
    min_diff = max(3, int(N * min_diff_frac))

    # Check if too similar to an existing elite
    for idx, (emk, estate) in enumerate(elite_pool):
        diff = int(np.sum(alt != estate[0]))
        if diff < min_diff:
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


def cmrts_v3_search(inst_name, nb_inst, time_budget_s=600.0, seed0=100):
    """
    Full v3 Memetic / Path-Relinking Iterated Critical-Path Tabu Search:
      - Cycles across:
          * Diverse Load-Balanced Greedy Starts (25%)
          * Elite Pool Path Relinking + TS Polish (25%, once >=2 elites exist)
          * Perturbed-Best ILS Intensification (50%)
    Returns (best_mk, best_state, stats_dict).
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
    best_mk = 10**9
    best_state = None
    elite_pool = []  # list of (mk, state_tuple)
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

        # Decide trajectory source: first 4 are diverse greedy starts to seed elite pool
        if starts < 4 or (starts % 4 == 0):
            noise = 0.0 if starts == 0 else (0.20 + 0.80 * ((starts % 5) / 4.0))
            init = construct_load_balanced(
                N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d, seed, noise
            )
            max_it = 4500
            max_ni = 550
        elif len(elite_pool) >= 2 and (starts % 4 == 2):
            # Path Relinking between two distinct elites
            i_src = pr_runs % len(elite_pool)
            i_g = (i_src + 1 + (pr_runs // len(elite_pool)) % (len(elite_pool) - 1)) % len(elite_pool)
            s_st = elite_pool[i_src][1]
            g_alt = elite_pool[i_g][1][0]
            pr_res = path_relink_step(
                N, M, W, job_pred, job_succ, alt_m, alt_w, alt_d,
                s_st[0], s_st[1], s_st[2], s_st[3],
                s_st[4], s_st[5], s_st[6], s_st[7],
                s_st[8], s_st[9], s_st[10], s_st[11],
                g_alt, seed,
            )
            init = pr_res[1:]  # (op_alt..ws)
            pr_runs += 1
            max_it = 6500
            max_ni = 700
        else:
            # Perturbed-Elite ILS (70% from global best, 30% from another top elite)
            src_idx = 0 if (len(elite_pool) == 1 or (ils_kicks % 3 != 2)) else (1 + (ils_kicks % (len(elite_pool) - 1)))
            st = elite_pool[src_idx][1]
            n_kicks = 6 + (ils_kicks % 4) * 5  # 6, 11, 16, 21 kicks
            init = perturb_v3(
                N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d,
                st[0], st[1], st[2], st[3],
                st[4], st[5], st[6], st[7],
                st[8], st[9], st[10], st[11],
                n_kicks, seed,
            )
            ils_kicks += 1
            max_it = 7500
            max_ni = 800

        res = tabu_search_v3_run(
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
