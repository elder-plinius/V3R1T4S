"""
Fast Numba Disjunctive-Graph Critical-Path Tabu Search for FJSSP-W.
Maintains explicit machine & worker doubly-linked sequences + exact O(N) DAG evaluation
(earliest start est[u], tail[u], critical path detection) and Mastrolilli-Gambardella
cycle-free insertion evaluation for critical-path (op, machine, worker) moves.
"""
import os
import time
import numpy as np
from numba import njit


def build_numba_instance(J, M, W, jobs):
    """Convert parsed (J, M, W, jobs) into flat Numba arrays (0-based machines/workers)."""
    N = sum(len(ops) for ops in jobs)
    op_job = np.empty(N, dtype=np.int32)
    op_idx = np.empty(N, dtype=np.int32)
    job_pred = np.full(N, -1, dtype=np.int32)
    job_succ = np.full(N, -1, dtype=np.int32)

    alt_start = np.empty(N + 1, dtype=np.int32)
    alt_m_list = []
    alt_w_list = []
    alt_d_list = []

    u = 0
    for j, ops in enumerate(jobs):
        for o, alt in enumerate(ops):
            op_job[u] = j
            op_idx[u] = o
            if o > 0:
                job_pred[u] = u - 1
                job_succ[u - 1] = u
            alt_start[u] = len(alt_m_list)
            # Sort alternatives by duration ascending for faster good-mode scanning
            items = sorted(alt.items(), key=lambda kv: (kv[1], kv[0][0], kv[0][1]))
            for (m, w), d in items:
                alt_m_list.append(m - 1)  # 0-based
                alt_w_list.append(w - 1)  # 0-based
                alt_d_list.append(d)
            u += 1
    alt_start[N] = len(alt_m_list)

    return dict(
        J=np.int32(J),
        M=np.int32(M),
        W=np.int32(W),
        N=np.int32(N),
        op_job=op_job,
        op_idx=op_idx,
        job_pred=job_pred,
        job_succ=job_succ,
        alt_start=alt_start,
        alt_m=np.array(alt_m_list, dtype=np.int32),
        alt_w=np.array(alt_w_list, dtype=np.int32),
        alt_d=np.array(alt_d_list, dtype=np.int32),
    )


@njit(cache=True)
def eval_dag(N, job_pred, job_succ, mach_pred, mach_succ, work_pred, work_succ, dur,
             est, tail, topo, indeg):
    """
    Exact O(N) forward + backward pass on the disjunctive graph.
    Returns makespan (> 0) if acyclic, or -1 if cyclic.
    """
    q_head = 0
    q_tail = 0
    for u in range(N):
        deg = 0
        if job_pred[u] != -1:
            deg += 1
        if mach_pred[u] != -1:
            deg += 1
        if work_pred[u] != -1:
            deg += 1
        indeg[u] = deg
        est[u] = 0
        if deg == 0:
            topo[q_tail] = u
            q_tail += 1

    while q_head < q_tail:
        u = topo[q_head]
        q_head += 1
        fin = est[u] + dur[u]

        v = job_succ[u]
        if v != -1:
            if fin > est[v]:
                est[v] = fin
            indeg[v] -= 1
            if indeg[v] == 0:
                topo[q_tail] = v
                q_tail += 1

        v = mach_succ[u]
        if v != -1:
            if fin > est[v]:
                est[v] = fin
            indeg[v] -= 1
            if indeg[v] == 0:
                topo[q_tail] = v
                q_tail += 1

        v = work_succ[u]
        if v != -1:
            if fin > est[v]:
                est[v] = fin
            indeg[v] -= 1
            if indeg[v] == 0:
                topo[q_tail] = v
                q_tail += 1

    if q_tail != N:
        return -1

    mk = 0
    for u in range(N):
        f = est[u] + dur[u]
        if f > mk:
            mk = f

    # Backward pass: tail[u] = longest path from finish(u) to sink
    for i in range(N - 1, -1, -1):
        u = topo[i]
        t = 0
        v = job_succ[u]
        if v != -1:
            val = dur[v] + tail[v]
            if val > t:
                t = val
        v = mach_succ[u]
        if v != -1:
            val = dur[v] + tail[v]
            if val > t:
                t = val
        v = work_succ[u]
        if v != -1:
            val = dur[v] + tail[v]
            if val > t:
                t = val
        tail[u] = t

    return mk


@njit(cache=True)
def construct_greedy(N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d,
                     seed, noise_lvl):
    """
    Fast randomized priority-rule constructive heuristic (ECT + MWR + noise).
    Builds a guaranteed-valid schedule with explicit machine & worker linked lists.
    """
    np.random.seed(seed)
    # Precompute min duration per op and remaining work per op
    min_d = np.empty(N, dtype=np.int32)
    for u in range(N):
        min_d[u] = alt_d[alt_start[u]]  # sorted ascending
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
    job_avail = np.zeros(N, dtype=np.int32)

    # Ready operations list
    ready = np.empty(N, dtype=np.int32)
    n_ready = 0
    for u in range(N):
        if job_pred[u] == -1:
            ready[n_ready] = u
            n_ready += 1

    rule = seed % 3  # 0: MWR, 1: Earliest-Finish, 2: Mixed
    for _ in range(N):
        # Choose next ready op
        best_pos = 0
        best_score = -1e18
        for i in range(n_ready):
            u = ready[i]
            if rule == 0:
                sc = float(rem_work[u]) + noise_lvl * np.random.random() * 20.0
            elif rule == 1:
                sc = -float(job_avail[u]) + 0.5 * float(rem_work[u]) + noise_lvl * np.random.random() * 20.0
            else:
                sc = float(rem_work[u]) - 0.5 * float(job_avail[u]) + noise_lvl * np.random.random() * 30.0
            if sc > best_score:
                best_score = sc
                best_pos = i
        u = ready[best_pos]
        ready[best_pos] = ready[n_ready - 1]
        n_ready -= 1

        # Choose best (m, w) mode (Earliest Completion Time + light noise)
        a0 = alt_start[u]
        a1 = alt_start[u + 1]
        ja = job_avail[u]
        best_a = a0
        best_ect = 1e18
        for a in range(a0, a1):
            m = alt_m[a]
            w = alt_w[a]
            d = alt_d[a]
            s = ja
            if mach_avail[m] > s:
                s = mach_avail[m]
            if work_avail[w] > s:
                s = work_avail[w]
            ect = float(s + d)
            if noise_lvl > 0.0:
                ect += noise_lvl * np.random.random() * 4.0
            if ect < best_ect:
                best_ect = ect
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

        # Append to machine m
        mt = mach_tail[m]
        if mt == -1:
            mach_head[m] = u
        else:
            mach_succ[mt] = u
            mach_pred[u] = mt
        mach_tail[m] = u
        mach_avail[m] = fin

        # Append to worker w
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
def remove_from_seq(u, head, tail, pred, succ, r):
    p = pred[u]
    s = succ[u]
    if p != -1:
        succ[p] = s
    else:
        head[r] = s
    if s != -1:
        pred[s] = p
    else:
        tail[r] = p
    pred[u] = -1
    succ[u] = -1


@njit(cache=True)
def insert_after_in_seq(u, after_node, head, tail, pred, succ, r):
    """Insert u immediately after after_node (-1 means insert at head) in resource r."""
    if after_node == -1:
        h = head[r]
        pred[u] = -1
        succ[u] = h
        if h != -1:
            pred[h] = u
        else:
            tail[r] = u
        head[r] = u
    else:
        s = succ[after_node]
        pred[u] = after_node
        succ[u] = s
        succ[after_node] = u
        if s != -1:
            pred[s] = u
        else:
            tail[r] = u


@njit(cache=True)
def find_best_insertion_on_res(u, head_r, succ, est, tail, dur,
                               j_est, j_tail, mk_cur, res_list):
    """
    Mastrolilli-Gambardella cycle-free insertion position on resource r for op u (already removed).
    Collects sequence of resource r into res_list[0..k-1].
    Finds the best after_node (-1 or res_list[pos]) that minimizes
    max(j_est, pred_fin) + d + max(j_tail, succ_full) while respecting cycle-free bounds:
      - Any op x with est[x] + dur[x] > mk_cur - j_tail (i.e. must be after u? No: cannot precede u if x is job-descendant!)
      - More precisely (M&G sufficient acyclicity condition):
        L_k = {x on r : est[x] + dur[x] > j_est} (candidates that can be placed AFTER u)
        R_k = {x on r : tail[x] + dur[x] > j_tail} (candidates that can be placed BEFORE u)
      Any insertion point pos (between res_list[pos-1] and res_list[pos]) where:
        for all i < pos: res_list[i] not forced after u (i.e. est[x] < j_est + dur_u? Use exact M&G:
        all i < pos have tail[x] + dur[x] > j_tail -> no wait: M&G Theorem:
        Place u after all x with est[x] + dur[x] <= j_est (Wait: if x can reach u, then est[x]+dur[x] <= est_old[u],
        and if u can reach x, then tail[x]+dur[x] <= tail_old[u]!)
    Returns (best_after_node, best_est_from_res, best_tail_from_res, best_len_without_d).
    """
    k = 0
    cur = head_r
    while cur != -1:
        res_list[k] = cur
        k += 1
        cur = succ[cur]

    if k == 0:
        return -1, 0, 0

    # Find valid interval [lo, hi] of insertion indices pos in 0..k
    # M&G: x in L (can be after u) iff tail[x] + dur[x] > j_tail? Wait:
    # Exact sufficient condition for acyclicity when inserting u into a DAG where u is removed:
    # A cycle is created iff there is a predecessor x of u on r that is reachable from u,
    # OR a successor y of u on r that can reach u.
    # If x is reachable from u, then est[x] >= j_est (wait: in G-u, job_succ[u] has est >= j_est? Not necessarily,
    # its tail is <= j_tail - dur[job_succ]!).
    # Exact Mastrolilli & Gambardella (2000) Lemma 1:
    #   L = {x on r : est[x] + dur[x] > j_est}  -> x CANNOT reach u if est[x] + dur[x] > est_u (actually if x reaches u, est[x]+dur[x] <= est_u_in_G!).
    #   Let's use the exact M&G bounds using current est & tail in G (before removing u, or in G-u):
    #   In G-u:
    #   - If x can reach job_pred[u], then est[x] + dur[x] <= j_est! (Wait: est[x]+dur[x] <= est[job_pred]+dur[job_pred] = j_est!)
    #     So if est[x] + dur[x] > j_est, x CANNOT reach job_pred[u] (and thus placing u BEFORE x creates NO cycle through job_pred!).
    #   - Symmetrically, if job_succ[u] can reach x, then tail[x] + dur[x] <= j_tail!
    #     So if tail[x] + dur[x] > j_tail, job_succ[u] CANNOT reach x (and thus placing u AFTER x creates NO cycle through job_succ!).
    #   Therefore, in G-u:
    #     - Every x with est[x] + dur[x] <= j_est might reach u -> safe to put u AFTER it (so pos >= last_must_before + 1? Wait: if x reaches u, x MUST be before u!).
    #     - Every x with tail[x] + dur[x] <= j_tail might be reached from u -> MUST be after u!
    #   So safe insertion positions pos satisfy:
    #     for all i < pos: tail[res_list[i]] + dur[res_list[i]] > j_tail  (no x before u is reachable from u)
    #     for all i >= pos: est[res_list[i]] + dur[res_list[i]] > j_est   (no y after u can reach u)
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
        # Rare overlap when j_est and j_tail are loose; swap to [hi, lo] and let eval_dag verify
        tmp = lo
        lo = hi
        hi = tmp

    best_pos = lo
    best_lb = 1000000000
    best_r_est = 0
    best_r_tail = 0

    for pos in range(lo, hi + 1):
        r_est = est[res_list[pos - 1]] + dur[res_list[pos - 1]] if pos > 0 else 0
        r_tail = dur[res_list[pos]] + tail[res_list[pos]] if pos < k else 0
        e = j_est if j_est > r_est else r_est
        t = j_tail if j_tail > r_tail else r_tail
        lb = e + t
        if lb < best_lb:
            best_lb = lb
            best_pos = pos
            best_r_est = r_est
            best_r_tail = r_tail

    after_node = res_list[best_pos - 1] if best_pos > 0 else -1
    return after_node, best_r_est, best_r_tail


@njit(cache=True)
def tabu_search_run(N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d,
                    seed, max_iters, max_no_improve, max_modes_per_op,
                    init_op_alt, init_op_m, init_op_w, init_dur,
                    init_mh, init_mt, init_wh, init_wt,
                    init_mp, init_ms, init_wp, init_ws):
    """
    Core Numba Critical-Path Tabu Search (Mastrolilli-Gambardella style for FJSSP-W).
    At each iteration:
      1. Identify critical operations (est[u] + dur[u] + tail[u] == cur_mk).
      2. For each critical op u, evaluate:
         - Reassigning u to candidate (m', w') modes + optimal M&G insertion on m' and w'.
         - Swapping u with its critical machine/worker successor.
      3. Apply best non-tabu (or aspiration-beating) move, update tabu tenure.
    Returns (best_mk, best_op_alt, best_est, iters_done, evals_done).
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

    est = np.empty(N, dtype=np.int32)
    tail = np.empty(N, dtype=np.int32)
    topo = np.empty(N, dtype=np.int32)
    indeg = np.empty(N, dtype=np.int32)
    res_list = np.empty(N, dtype=np.int32)
    crit_ops = np.empty(N, dtype=np.int32)

    cur_mk = eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est, tail, topo, indeg)
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

    # Tabu table: tabu_until[u, m] and tabu_op[u]
    tabu_m = np.zeros((N, M), dtype=np.int32)
    tabu_w = np.zeros((N, W), dtype=np.int32)
    tabu_op = np.zeros(N, dtype=np.int32)

    no_imp = 0
    evals = 0
    base_tenure = 12 + (N // 30)

    for it in range(1, max_iters + 1):
        # Collect critical operations
        n_crit = 0
        for u in range(N):
            if est[u] + dur[u] + tail[u] == cur_mk:
                crit_ops[n_crit] = u
                n_crit += 1

        if n_crit == 0:
            break

        # Sample critical ops if huge critical set
        best_move_score = 1000000000
        best_u = -1
        best_a = -1
        best_m_after = -1
        best_w_after = -1
        best_exact_mk = 1000000000

        # Evaluate neighborhood over critical operations
        # To keep each iteration fast (~0.5-2ms), cap crit ops scanned if n_crit > 40
        step_c = 1 if n_crit <= 40 else (n_crit // 40)
        offset_c = it % step_c

        for ci in range(offset_c, n_crit, step_c):
            u = crit_ops[ci]
            old_m = op_m[u]
            old_w = op_w[u]
            old_a = op_alt[u]
            old_mp = mp[u]
            old_wp = wp[u]

            jp = job_pred[u]
            js = job_succ[u]
            j_est = (est[jp] + dur[jp]) if jp != -1 else 0
            j_tail = (dur[js] + tail[js]) if js != -1 else 0

            # Temporarily remove u from its machine and worker sequences
            remove_from_seq(u, mh, mt, mp, ms, old_m)
            remove_from_seq(u, wh, wt, wp, ws, old_w)

            a0 = alt_start[u]
            a1 = alt_start[u + 1]
            n_alts = a1 - a0

            # Scan candidate modes: always include top fastest + random sample if n_alts > max_modes_per_op
            n_scan = n_alts if n_alts <= max_modes_per_op else max_modes_per_op
            top_fast = n_scan // 2

            for k_idx in range(n_scan):
                if n_alts <= max_modes_per_op:
                    a = a0 + k_idx
                elif k_idx < top_fast:
                    a = a0 + k_idx
                else:
                    a = a0 + top_fast + np.random.randint(0, n_alts - top_fast)

                m2 = alt_m[a]
                w2 = alt_w[a]
                d2 = alt_d[a]

                # Quick lower bound prune: even with zero resource wait, can it beat best_move_score?
                if j_est + d2 + j_tail > best_move_score + 2:
                    continue

                m_after, m_est, m_tail = find_best_insertion_on_res(
                    u, mh[m2], ms, est, tail, dur, j_est, j_tail, cur_mk, res_list
                )
                w_after, w_est, w_tail = find_best_insertion_on_res(
                    u, wh[w2], ws, est, tail, dur, j_est, j_tail, cur_mk, res_list
                )

                # Skip no-op move
                if a == old_a and m_after == old_mp and w_after == old_wp:
                    continue

                e = j_est
                if m_est > e:
                    e = m_est
                if w_est > e:
                    e = w_est
                t = j_tail
                if m_tail > t:
                    t = m_tail
                if w_tail > t:
                    t = w_tail
                est_mk = e + d2 + t
                evals += 1

                is_tabu = (tabu_m[u, m2] > it) or (tabu_w[u, w2] > it) or (tabu_op[u] > it)
                # Aspiration: allow if est_mk < best_mk
                if is_tabu and est_mk >= best_mk:
                    continue

                # Slight tie-break noise to avoid cycling
                score = est_mk
                if score < best_move_score or (score == best_move_score and np.random.random() < 0.25):
                    # Verify exact DAG makespan only for promising moves!
                    insert_after_in_seq(u, m_after, mh, mt, mp, ms, m2)
                    insert_after_in_seq(u, w_after, wh, wt, wp, ws, w2)
                    old_d_save = dur[u]
                    dur[u] = d2
                    exact_mk = eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est, tail, topo, indeg)
                    dur[u] = old_d_save
                    remove_from_seq(u, mh, mt, mp, ms, m2)
                    remove_from_seq(u, wh, wt, wp, ws, w2)

                    if exact_mk != -1:
                        if is_tabu and exact_mk >= best_mk:
                            pass
                        elif exact_mk < best_exact_mk or (exact_mk == best_exact_mk and np.random.random() < 0.3):
                            best_exact_mk = exact_mk
                            best_move_score = exact_mk
                            best_u = u
                            best_a = a
                            best_m_after = m_after
                            best_w_after = w_after

            # Restore u to its original position and restore est/tail for next crit op
            insert_after_in_seq(u, old_mp, mh, mt, mp, ms, old_m)
            insert_after_in_seq(u, old_wp, wh, wt, wp, ws, old_w)
            eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est, tail, topo, indeg)

        if best_u == -1:
            # Diversification kick: random feasible reassignment of a critical op
            u = crit_ops[np.random.randint(0, n_crit)]
            old_m = op_m[u]
            old_w = op_w[u]
            old_mp = mp[u]
            old_wp = wp[u]
            remove_from_seq(u, mh, mt, mp, ms, old_m)
            remove_from_seq(u, wh, wt, wp, ws, old_w)
            a0 = alt_start[u]
            a1 = alt_start[u + 1]
            a = a0 + np.random.randint(0, min(a1 - a0, 20))
            m2 = alt_m[a]
            w2 = alt_w[a]
            d2 = alt_d[a]
            jp = job_pred[u]
            js = job_succ[u]
            j_est = (est[jp] + dur[jp]) if jp != -1 else 0
            j_tail = (dur[js] + tail[js]) if js != -1 else 0
            m_after, _, _ = find_best_insertion_on_res(u, mh[m2], ms, est, tail, dur, j_est, j_tail, cur_mk, res_list)
            w_after, _, _ = find_best_insertion_on_res(u, wh[w2], ws, est, tail, dur, j_est, j_tail, cur_mk, res_list)
            insert_after_in_seq(u, m_after, mh, mt, mp, ms, m2)
            insert_after_in_seq(u, w_after, wh, wt, wp, ws, w2)
            old_d_save = dur[u]
            dur[u] = d2
            new_mk = eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est, tail, topo, indeg)
            if new_mk != -1:
                op_alt[u] = a
                op_m[u] = m2
                op_w[u] = w2
                cur_mk = new_mk
            else:
                dur[u] = old_d_save
                remove_from_seq(u, mh, mt, mp, ms, m2)
                remove_from_seq(u, wh, wt, wp, ws, w2)
                insert_after_in_seq(u, old_mp, mh, mt, mp, ms, old_m)
                insert_after_in_seq(u, old_wp, wh, wt, wp, ws, old_w)
                eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est, tail, topo, indeg)
            no_imp += 1
            if no_imp >= max_no_improve:
                break
            continue

        # Apply best_u move
        u = best_u
        old_m = op_m[u]
        old_w = op_w[u]
        remove_from_seq(u, mh, mt, mp, ms, old_m)
        remove_from_seq(u, wh, wt, wp, ws, old_w)

        m2 = alt_m[best_a]
        w2 = alt_w[best_a]
        d2 = alt_d[best_a]
        insert_after_in_seq(u, best_m_after, mh, mt, mp, ms, m2)
        insert_after_in_seq(u, best_w_after, wh, wt, wp, ws, w2)
        op_alt[u] = best_a
        op_m[u] = m2
        op_w[u] = w2
        dur[u] = d2
        cur_mk = eval_dag(N, job_pred, job_succ, mp, ms, wp, ws, dur, est, tail, topo, indeg)

        # Update tabu tenures
        ten = base_tenure + np.random.randint(0, 10)
        tabu_m[u, old_m] = it + ten
        tabu_w[u, old_w] = it + ten
        tabu_op[u] = it + (ten // 2)

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


def to_schedule_json(inst_name, nb_inst, op_alt, est):
    """Convert Numba solution arrays to canonical FJSSP-W schedule JSON."""
    N = int(nb_inst["N"])
    op_job = nb_inst["op_job"]
    op_idx = nb_inst["op_idx"]
    alt_m = nb_inst["alt_m"]
    alt_w = nb_inst["alt_w"]
    alt_d = nb_inst["alt_d"]
    ops = []
    for u in range(N):
        a = int(op_alt[u])
        ops.append([
            int(op_job[u]),
            int(op_idx[u]),
            int(alt_m[a]) + 1,  # 1-based
            int(alt_w[a]) + 1,  # 1-based
            int(est[u]),
            int(alt_d[a]),
        ])
    return {"instance": inst_name, "ops": ops}


def multi_start_ts(inst_name, nb_inst, time_budget_s=60.0, seed0=100, target_mk=0):
    """Run multi-start Critical-Path Tabu Search within time_budget_s."""
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

    max_modes = 80 if N <= 250 else 50
    best_mk = 10**9
    best_alt = None
    best_est = None
    total_evals = 0
    total_iters = 0
    starts = 0

    while time.time() - t0 < time_budget_s:
        seed = seed0 + starts * 97
        noise = 0.0 if starts == 0 else (0.3 + 0.7 * ((starts % 5) / 4.0))
        init = construct_greedy(N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d, seed, noise)
        res = tabu_search_run(
            N, M, W, job_pred, job_succ, alt_start, alt_m, alt_w, alt_d,
            seed + 1, 2500, 350, max_modes,
            init[0], init[1], init[2], init[3],
            init[4], init[5], init[6], init[7],
            init[8], init[9], init[10], init[11],
        )
        mk, b_alt, b_est = int(res[0]), res[1], res[2]
        total_iters += int(res[11])
        total_evals += int(res[12])
        starts += 1
        if mk < best_mk:
            best_mk = mk
            best_alt = b_alt.copy()
            best_est = b_est.copy()
            if target_mk > 0 and best_mk < target_mk:
                # Keep going a bit to deepen, or stop if close to budget
                pass

    return best_mk, best_alt, best_est, dict(starts=starts, iters=total_iters, evals=total_evals, secs=round(time.time() - t0, 2))
