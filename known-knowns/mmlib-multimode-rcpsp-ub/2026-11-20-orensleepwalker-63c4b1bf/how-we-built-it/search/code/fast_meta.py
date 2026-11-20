"""High-speed Numba-compiled Memetic / ILS / Mode-Swap + Activity-List engine for MMLIB+."""
import os
import sys
import time
import numpy as np
import numba as nb

PHASEB_DIR = os.path.dirname(os.path.abspath(__file__))
SOLVER_CODE = os.path.abspath(os.path.join(PHASEB_DIR, "..", "code"))
if SOLVER_CODE not in sys.path:
    sys.path.insert(0, SOLVER_CODE)

import engine  # noqa: E402


@nb.njit(cache=True)
def psgs(order, d, q, cap, pp, pi, H):
    """Parallel Schedule Generation Scheme (PSGS) in Numba."""
    n = len(order)
    R = len(cap)
    st = np.full(n, -1, np.int64)
    fin = np.full(n, -1, np.int64)
    u = np.zeros((H + 1, R), np.int64)
    done = np.zeros(n, np.uint8)
    # Track remaining unscheduled predecessors
    rem_pred = np.zeros(n, np.int64)
    for j in range(n):
        rem_pred[j] = pp[j + 1] - pp[j]

    # Priority rank from activity list `order`
    rank = np.empty(n, np.int64)
    for idx in range(n):
        rank[order[idx]] = idx

    st[0] = 0
    fin[0] = 0
    done[0] = 1
    scheduled = 1
    t = 0

    while scheduled < n:
        # Advance t to earliest active completion if needed
        # Find all eligible jobs whose predecessors finished <= t, sorted by rank
        # Simple O(n) scan in order of `order` (already priority-ordered!)
        started_any = False
        for idx in range(n):
            j = order[idx]
            if done[j] == 1:
                continue
            # Check all predecessors finished <= t
            ready = True
            for e in range(pp[j], pp[j + 1]):
                p = pi[e]
                if done[p] == 0 or fin[p] > t:
                    ready = False
                    break
            if not ready:
                continue
            dj = d[j]
            if dj == 0:
                st[j] = t
                fin[j] = t
                done[j] = 1
                scheduled += 1
                started_any = True
                continue
            # Check renewable capacity over [t, t + dj)
            ok = True
            for tau in range(t, t + dj):
                for r in range(R):
                    if u[tau, r] + q[j, r] > cap[r]:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                st[j] = t
                fin[j] = t + dj
                for tau in range(t, t + dj):
                    for r in range(R):
                        u[tau, r] += q[j, r]
                done[j] = 1
                scheduled += 1
                started_any = True
        if scheduled >= n:
            break
        if not started_any:
            # Advance t to next finish time > t
            next_t = H
            for j in range(n):
                if done[j] == 1 and fin[j] > t and fin[j] < next_t:
                    next_t = fin[j]
            if next_t == H:
                t += 1
            else:
                t = next_t
    return st


@nb.njit(cache=True)
def eval_modes_order(order, modes, dur, req, cap, pp, pi, sp, si, H, fbi_rounds):
    n = len(order)
    R = req.shape[2]
    d = np.empty(n, np.int64)
    q = np.empty((n, R), np.int64)
    for j in range(n):
        m = modes[j] - 1
        d[j] = dur[j, m]
        for r in range(R):
            q[j, r] = req[j, m, r]
    st = engine.sgs(order, d, q, cap, pp, pi, H)
    if fbi_rounds > 0:
        st, mk = engine.fbi(st, d, q, cap, pp, pi, sp, si, H, fbi_rounds)
    else:
        mk = st[n - 1]
    return mk, st


@nb.njit(cache=True)
def eval_both_sgs(order, modes, dur, req, cap, pp, pi, sp, si, H, fbi_rounds):
    """Evaluate BOTH Serial SGS + FBI and Parallel SGS + FBI, returning the better schedule."""
    n = len(order)
    R = req.shape[2]
    d = np.empty(n, np.int64)
    q = np.empty((n, R), np.int64)
    for j in range(n):
        m = modes[j] - 1
        d[j] = dur[j, m]
        for r in range(R):
            q[j, r] = req[j, m, r]
    st1 = engine.sgs(order, d, q, cap, pp, pi, H)
    st1, mk1 = engine.fbi(st1, d, q, cap, pp, pi, sp, si, H, fbi_rounds)
    st2 = psgs(order, d, q, cap, pp, pi, H)
    st2, mk2 = engine.fbi(st2, d, q, cap, pp, pi, sp, si, H, fbi_rounds)
    if mk2 < mk1:
        return mk2, st2
    return mk1, st1


@nb.njit(cache=True)
def order_from_starts(starts, topo):
    n = len(starts)
    # Insertion / argsort by (starts[j], topo_pos[j])
    pos = np.empty(n, np.int64)
    for idx in range(n):
        pos[topo[idx]] = idx
    keys = np.empty(n, np.int64)
    for j in range(n):
        keys[j] = starts[j] * n + pos[j]
    return np.argsort(keys)


@nb.njit(cache=True)
def check_nr_feasible(modes, nreq, ncap):
    N = len(ncap)
    n = len(modes)
    rem = ncap.copy()
    for j in range(n):
        m = modes[j] - 1
        for k in range(N):
            rem[k] -= nreq[j, m, k]
    for k in range(N):
        if rem[k] < 0:
            return False, rem
    return True, rem


@nb.njit(cache=True)
def repair_modes_nr(modes, nm, nreq, ncap, dur, seed):
    """Repair non-renewable infeasibility in-place (returns copy, ok)."""
    rng = np.uint64(seed * 6364136223846793005 + 1442695040888963407)
    n = len(modes)
    N = len(ncap)
    out = modes.copy()
    rem = ncap.copy()
    for j in range(n):
        m = out[j] - 1
        for k in range(N):
            rem[k] -= nreq[j, m, k]

    for _ in range(n * 3):
        viol = 0
        for k in range(N):
            if rem[k] < 0:
                viol -= rem[k]
        if viol == 0:
            return out, True

        best_j = -1
        best_m = -1
        best_score = -1e18
        for j in range(1, n - 1):
            cur_m = out[j] - 1
            # Check if j uses any violated NR
            uses_viol = False
            for k in range(N):
                if rem[k] < 0 and nreq[j, cur_m, k] > 0:
                    uses_viol = True
                    break
            if not uses_viol:
                continue
            for m2 in range(nm[j]):
                if m2 == cur_m:
                    continue
                new_viol = 0
                for k in range(N):
                    r_new = rem[k] + nreq[j, cur_m, k] - nreq[j, m2, k]
                    if r_new < 0:
                        new_viol -= r_new
                gain = viol - new_viol
                if gain > 0:
                    rng ^= rng >> np.uint64(12)
                    rng ^= rng << np.uint64(25)
                    rng ^= rng >> np.uint64(27)
                    noise = float(rng & np.uint64(0xFFFF)) / 65536.0
                    dur_pen = float(dur[j, m2] - dur[j, cur_m]) * 0.05
                    score = float(gain) - dur_pen + noise * 0.5
                    if score > best_score:
                        best_score = score
                        best_j = j
                        best_m = m2
        if best_j < 0:
            return out, False
        cur_m = out[best_j] - 1
        for k in range(N):
            rem[k] += nreq[best_j, cur_m, k] - nreq[best_j, best_m, k]
        out[best_j] = best_m + 1

    for k in range(N):
        if rem[k] < 0:
            return out, False
    return out, True


@nb.njit(cache=True)
def crossover_order(p1, p2, cut1, cut2):
    """Hartmann 2-point precedence-preserving activity-list crossover."""
    n = len(p1)
    child = np.empty(n, np.int64)
    used = np.zeros(n, np.uint8)
    idx = 0
    for i in range(cut1):
        j = p1[i]
        child[idx] = j
        used[j] = 1
        idx += 1
    for i in range(n):
        j = p2[i]
        if used[j] == 0:
            child[idx] = j
            used[j] = 1
            idx += 1
            if idx == cut2:
                break
    for i in range(n):
        j = p1[i]
        if used[j] == 0:
            child[idx] = j
            used[j] = 1
            idx += 1
    return child


@nb.njit(cache=True)
def compute_critical_mask(st, modes, dur, pp, pi, sp, si):
    """Return boolean mask of jobs with low precedence slack (<= 2) or on critical path."""
    n = len(st)
    mk = st[n - 1]
    es = np.zeros(n, np.int64)
    ls = np.full(n, mk, np.int64)
    # Forward pass on actual starts
    for j in range(n):
        es[j] = st[j]
    # Backward pass: latest start respecting precedences and mk
    # Process in reverse start-time order
    order_rev = np.argsort(-st)
    ls[n - 1] = mk
    for idx in range(n):
        j = order_rev[idx]
        if j == n - 1:
            continue
        dj = dur[j, modes[j] - 1]
        best = mk - dj
        for e in range(sp[j], sp[j + 1]):
            s = si[e]
            v = ls[s] - dj
            if v < best:
                best = v
        ls[j] = best
    crit = np.zeros(n, np.uint8)
    for j in range(1, n - 1):
        if ls[j] - es[j] <= 2:
            crit[j] = 1
    return crit


@nb.njit(cache=True)
def mode_local_search(
    order, modes, st, mk, dur, req, nreq, nm, cap, ncap, pp, pi, sp, si, H,
    topo, max_evals, fbi_rounds, seed
):
    """Fast 1-job mode change + 2-job NR-trading mode swap local search."""
    rng = np.uint64(seed * 2862933555777941757 + 3037000493)
    n = len(modes)
    N = len(ncap)
    cur_m = modes.copy()
    cur_o = order.copy()
    cur_st = st.copy()
    cur_mk = mk

    rem = ncap.copy()
    for j in range(n):
        mj = cur_m[j] - 1
        for k in range(N):
            rem[k] -= nreq[j, mj, k]

    evals = 0
    improved_any = True
    while improved_any and evals < max_evals:
        improved_any = False
        crit = compute_critical_mask(cur_st, cur_m, dur, pp, pi, sp, si)

        # Build shuffled job list with critical jobs first
        jobs = np.empty(n - 2, np.int64)
        c_idx = 0
        for j in range(1, n - 1):
            if crit[j] == 1:
                jobs[c_idx] = j
                c_idx += 1
        for j in range(1, n - 1):
            if crit[j] == 0:
                jobs[c_idx] = j
                c_idx += 1

        # 1-job mode moves
        for ji in range(n - 2):
            if evals >= max_evals:
                break
            j = jobs[ji]
            old_m = cur_m[j] - 1
            for m2 in range(nm[j]):
                if m2 == old_m:
                    continue
                # Check NR feasibility
                feas = True
                for k in range(N):
                    if rem[k] + nreq[j, old_m, k] - nreq[j, m2, k] < 0:
                        feas = False
                        break
                if not feas:
                    continue
                cur_m[j] = m2 + 1
                new_mk, new_st = eval_modes_order(cur_o, cur_m, dur, req, cap, pp, pi, sp, si, H, fbi_rounds)
                evals += 1
                if new_mk < cur_mk:
                    for k in range(N):
                        rem[k] += nreq[j, old_m, k] - nreq[j, m2, k]
                    cur_mk = new_mk
                    cur_st = new_st
                    cur_o = order_from_starts(cur_st, topo)
                    old_m = m2
                    improved_any = True
                else:
                    cur_m[j] = old_m + 1
                if evals >= max_evals:
                    break

        if improved_any or evals >= max_evals:
            continue

        # 2-job NR-trading mode swaps: speed up critical/random job u, compensate with job v
        n_tries = min(n - 2, 40)
        for ti in range(n_tries):
            if evals >= max_evals:
                break
            u = jobs[ti]
            old_u = cur_m[u] - 1
            for mu in range(nm[u]):
                if mu == old_u or dur[u, mu] > dur[u, old_u]:
                    continue
                # Compute deficit if u switches to mu
                need_trade = False
                for k in range(N):
                    if rem[k] + nreq[u, old_u, k] - nreq[u, mu, k] < 0:
                        need_trade = True
                        break
                if not need_trade:
                    continue  # already tested in 1-job move

                # Sample up to 16 candidate partner jobs v
                for _ in range(16):
                    if evals >= max_evals:
                        break
                    rng ^= rng >> np.uint64(12)
                    rng ^= rng << np.uint64(25)
                    rng ^= rng >> np.uint64(27)
                    v = 1 + int(rng % np.uint64(n - 2))
                    if v == u:
                        continue
                    old_v = cur_m[v] - 1
                    for mv in range(nm[v]):
                        if mv == old_v:
                            continue
                        feas = True
                        for k in range(N):
                            if (rem[k]
                                + nreq[u, old_u, k] - nreq[u, mu, k]
                                + nreq[v, old_v, k] - nreq[v, mv, k]) < 0:
                                feas = False
                                break
                        if not feas:
                            continue
                        cur_m[u] = mu + 1
                        cur_m[v] = mv + 1
                        new_mk, new_st = eval_modes_order(cur_o, cur_m, dur, req, cap, pp, pi, sp, si, H, fbi_rounds)
                        evals += 1
                        if new_mk < cur_mk:
                            for k in range(N):
                                rem[k] += (nreq[u, old_u, k] - nreq[u, mu, k]
                                           + nreq[v, old_v, k] - nreq[v, mv, k])
                            cur_mk = new_mk
                            cur_st = new_st
                            cur_o = order_from_starts(cur_st, topo)
                            old_u = mu
                            improved_any = True
                            break
                        else:
                            cur_m[u] = old_u + 1
                            cur_m[v] = old_v + 1
                    if improved_any:
                        break
                if improved_any:
                    break
            if improved_any:
                break

    return cur_mk, cur_o, cur_m, cur_st, evals


@nb.njit(cache=True)
def perturb_order_numba(order, pp, pi, n_swaps, seed):
    """Apply precedence-preserving adjacent/nearby swaps to activity list."""
    rng = np.uint64(seed * 6364136223846793005 + 1)
    n = len(order)
    out = order.copy()
    pos = np.empty(n, np.int64)
    for i in range(n):
        pos[out[i]] = i

    for _ in range(n_swaps):
        rng ^= rng >> np.uint64(12)
        rng ^= rng << np.uint64(25)
        rng ^= rng >> np.uint64(27)
        i = 1 + int(rng % np.uint64(n - 3))
        a = out[i]
        b = out[i + 1]
        # Check if a is a predecessor of b
        is_pred = False
        for e in range(pp[b], pp[b + 1]):
            if pi[e] == a:
                is_pred = True
                break
        if not is_pred:
            out[i] = b
            out[i + 1] = a
            pos[b] = i
            pos[a] = i + 1
    return out


def random_feasible_modes(X, rng):
    """Generate a random budget-feasible mode vector using repair."""
    n = X.n
    modes = np.ones(n, dtype=np.int64)
    for j in range(1, n - 1):
        modes[j] = int(rng.integers(1, X.nm[j] + 1))
    repaired, ok = repair_modes_nr(modes, X.nm, X.nreq, X.ncap, X.dur, int(rng.integers(1, 1 << 30)))
    return repaired if ok else None


def memetic_search(
    X,
    time_budget: float,
    seed: int = 1,
    init_solutions=None,
    pop_size: int = 20,
    target_mk: int = -1,
    cpsat_mixes: int = 4,
    cpsat_workers: int = 1,
):
    """
    Hybrid Memetic GA + Mode Local Search + Biased Multistart.
    init_solutions: optional list of (modes_np, starts_np) tuples (e.g., BKS warm start).
    Returns: (best_mk, best_modes, best_starts, stats_dict)
    """
    t0 = time.time()
    rng = np.random.default_rng(seed)
    topo = np.array(engine.topo(X), dtype=np.int64)
    pop = []  # list of (mk, order, modes, st)
    seen_sigs = set()
    total_evals = 0

    def add_ind(modes, order=None, st=None, mk=None):
        nonlocal total_evals
        ok, _ = check_nr_feasible(modes, X.nreq, X.ncap)
        if not ok:
            modes, ok = repair_modes_nr(modes, X.nm, X.nreq, X.ncap, X.dur, int(rng.integers(1, 1 << 30)))
            if not ok:
                return None
        if order is None:
            if st is not None:
                order = order_from_starts(st, topo)
            else:
                order = topo.copy()
        if mk is None or st is None:
            mk, st = eval_modes_order(order, modes, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 10)
            total_evals += 1
        sig = (int(mk), bytes(modes.astype(np.uint8).tobytes()))
        if sig not in seen_sigs:
            seen_sigs.add(sig)
            pop.append((int(mk), order.copy(), modes.copy(), st.copy()))
        return int(mk)

    # 1. Seed from init_solutions (e.g. posted BKS schedule)
    if init_solutions:
        for m_init, s_init in init_solutions:
            m_arr = np.asarray(m_init, dtype=np.int64)
            s_arr = np.asarray(s_init, dtype=np.int64)
            o_arr = order_from_starts(s_arr, topo)
            mk, st = eval_modes_order(o_arr, m_arr, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 20)
            total_evals += 1
            add_ind(m_arr, o_arr, st, mk)
            # Also run immediate mode LS on warm start
            mk2, o2, m2, st2, ev = mode_local_search(
                o_arr, m_arr, st, mk, X.dur, X.req, X.nreq, X.nm, X.cap, X.ncap,
                X.pp, X.pi, X.sp, X.si, X.H, topo, 400, 6, int(rng.integers(1, 1 << 30))
            )
            total_evals += ev
            add_ind(m2, o2, st2, mk2)

    # 2. Seed diversified CP-SAT mode mixes
    avoid = [ind[2] for ind in pop]
    for mix_idx in range(cpsat_mixes):
        if time.time() - t0 > time_budget * 0.35 and len(pop) >= 4:
            break
        m_mix, _ = engine.mode_mix(X, secs=min(2.5, max(0.5, time_budget * 0.1)), workers=cpsat_workers, seed=seed + mix_idx * 17, avoid=avoid)
        if m_mix is None:
            break
        avoid.append(m_mix)
        mk, st = engine.multistart(X, m_mix, 200, seed=seed + mix_idx * 31)
        total_evals += 200
        o = order_from_starts(st, topo)
        add_ind(m_mix, o, st, mk)

    # 3. Fill remaining population with random feasible modes + multistart
    tries = 0
    while len(pop) < pop_size and tries < pop_size * 5 and (time.time() - t0) < time_budget * 0.5:
        tries += 1
        if pop and rng.random() < 0.6:
            # Perturb an existing mode vector
            base = pop[int(rng.integers(0, len(pop)))]
            m_new = base[2].copy()
            k_mut = int(rng.integers(2, max(4, X.n // 6)))
            for _ in range(k_mut):
                j = int(rng.integers(1, X.n - 1))
                m_new[j] = int(rng.integers(1, X.nm[j] + 1))
            m_new, ok = repair_modes_nr(m_new, X.nm, X.nreq, X.ncap, X.dur, int(rng.integers(1, 1 << 30)))
            if not ok:
                continue
        else:
            m_new = random_feasible_modes(X, rng)
            if m_new is None:
                continue
        mk, st = engine.multistart(X, m_new, 60, seed=int(rng.integers(1, 1 << 30)))
        total_evals += 60
        o = order_from_starts(st, topo)
        add_ind(m_new, o, st, mk)

    if not pop:
        return None, None, None, {"evals": total_evals, "secs": time.time() - t0}

    pop.sort(key=lambda x: x[0])
    pop = pop[:pop_size]

    # 4. Main Memetic Loop
    gen = 0
    stagnation = 0
    best_mk = pop[0][0]
    while time.time() - t0 < time_budget:
        gen += 1
        # Select two parents (tournament)
        i1 = min(int(rng.integers(0, len(pop))), int(rng.integers(0, len(pop))))
        i2 = min(int(rng.integers(0, len(pop))), int(rng.integers(0, len(pop))))
        p1, p2 = pop[i1], pop[i2]

        # Crossover order + modes
        c1 = int(rng.integers(1, X.n - 2))
        c2 = int(rng.integers(c1 + 1, X.n - 1))
        child_o = crossover_order(p1[1], p2[1], c1, c2)

        mask = rng.random(X.n) < 0.5
        child_m = np.where(mask, p1[2], p2[2]).astype(np.int64)
        child_m[0] = 1
        child_m[X.n - 1] = 1

        # Mutate modes
        mut_rate = 0.06 if stagnation < 15 else 0.15
        n_mut = max(1, int((X.n - 2) * mut_rate))
        for _ in range(n_mut):
            j = int(rng.integers(1, X.n - 1))
            child_m[j] = int(rng.integers(1, X.nm[j] + 1))

        child_m, ok = repair_modes_nr(child_m, X.nm, X.nreq, X.ncap, X.dur, int(rng.integers(1, 1 << 30)))
        if not ok:
            continue

        # Mutate order
        child_o = perturb_order_numba(child_o, X.pp, X.pi, int(rng.integers(2, 12)), int(rng.integers(1, 1 << 30)))

        # Evaluate child
        mk, st = eval_modes_order(child_o, child_m, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 8)
        total_evals += 1

        # Apply mode local search if promising or every 3rd gen
        if mk <= pop[min(4, len(pop) - 1)][0] + 2 or gen % 3 == 0:
            mk, child_o, child_m, st, ev = mode_local_search(
                child_o, child_m, st, mk, X.dur, X.req, X.nreq, X.nm, X.cap, X.ncap,
                X.pp, X.pi, X.sp, X.si, X.H, topo, 250, 4, int(rng.integers(1, 1 << 30))
            )
            total_evals += ev

        # Intensive multistart polish on new best or close to best
        if mk <= best_mk:
            mk_ms, st_ms = engine.multistart(X, child_m, 250, seed=int(rng.integers(1, 1 << 30)))
            total_evals += 250
            if mk_ms < mk:
                mk = int(mk_ms)
                st = st_ms
                child_o = order_from_starts(st, topo)

        if mk < best_mk:
            best_mk = mk
            stagnation = 0
        else:
            stagnation += 1

        add_ind(child_m, child_o, st, mk)
        pop.sort(key=lambda x: x[0])
        if len(pop) > pop_size:
            # Keep top 70% + 30% diverse
            pop = pop[:pop_size]

        # Periodically run biased multistart on top elite
        if gen % 10 == 0 and time.time() - t0 < time_budget:
            elite = pop[int(rng.integers(0, min(3, len(pop))))]
            mk_ms, st_ms = engine.multistart(X, elite[2], 300, seed=int(rng.integers(1, 1 << 30)))
            total_evals += 300
            if mk_ms < elite[0]:
                o_ms = order_from_starts(st_ms, topo)
                add_ind(elite[2], o_ms, st_ms, mk_ms)
                pop.sort(key=lambda x: x[0])
                pop = pop[:pop_size]
                if mk_ms < best_mk:
                    best_mk = int(mk_ms)
                    stagnation = 0

        if target_mk > 0 and best_mk <= target_mk:
            # Quick polish on the winning mode vector before returning
            best = pop[0]
            mk_ms, st_ms = engine.multistart(X, best[2], 400, seed=int(rng.integers(1, 1 << 30)))
            total_evals += 400
            if mk_ms < best[0]:
                o_ms = order_from_starts(st_ms, topo)
                add_ind(best[2], o_ms, st_ms, mk_ms)
                pop.sort(key=lambda x: x[0])
            break

    best = pop[0]
    top_pop = [(int(p[0]), p[2].copy(), p[3].copy()) for p in pop[:10]]
    return int(best[0]), best[2], best[3], {
        "evals": total_evals,
        "gens": gen,
        "secs": round(time.time() - t0, 2),
        "pop_best": [p[0] for p in pop[:5]],
        "top_pop": top_pop,
    }


@nb.njit(cache=True)
def insert_move_numba(order, pos, pp, pi, sp, si, rng_state):
    """Pick a random job j and insert it at a random precedence-feasible position."""
    n = len(order)
    rng = rng_state
    rng ^= rng >> np.uint64(12)
    rng ^= rng << np.uint64(25)
    rng ^= rng >> np.uint64(27)
    j = 1 + int(rng % np.uint64(n - 2))
    cur_p = pos[j]

    lo = 1
    for e in range(pp[j], pp[j + 1]):
        p_idx = pos[pi[e]] + 1
        if p_idx > lo:
            lo = p_idx
    hi = n - 2
    for e in range(sp[j], sp[j + 1]):
        s_idx = pos[si[e]] - 1
        if s_idx < hi:
            hi = s_idx

    if lo >= hi:
        return order, False, rng

    rng ^= rng >> np.uint64(12)
    rng ^= rng << np.uint64(25)
    rng ^= rng >> np.uint64(27)
    new_p = lo + int(rng % np.uint64(hi - lo + 1))
    if new_p == cur_p:
        new_p = lo if cur_p > lo else hi

    out = order.copy()
    if new_p < cur_p:
        for k in range(cur_p, new_p, -1):
            out[k] = out[k - 1]
        out[new_p] = j
    else:
        for k in range(cur_p, new_p):
            out[k] = out[k + 1]
        out[new_p] = j
    return out, True, rng


@nb.njit(cache=True)
def sa_joint_numba(
    init_order, init_modes, dur, req, nreq, nm, cap, ncap, pp, pi, sp, si, H,
    topo, n_iters, t_start, t_end, seed
):
    """
    Ultra-fast Numba Simulated Annealing over joint (activity_list, mode_vector).
    Moves:
      - 35% 1-job NR-feasible mode change
      - 30% 2-job NR-trading mode swap
      - 35% precedence-preserving activity-list insert move
    Accepts plateau moves & uphill moves via Metropolis criterion with periodic reheating.
    """
    rng = np.uint64(seed * 6364136223846793005 + 1442695040888963407)
    n = len(init_modes)
    N = len(ncap)

    cur_o = init_order.copy()
    cur_m = init_modes.copy()
    cur_mk, cur_st = eval_modes_order(cur_o, cur_m, dur, req, cap, pp, pi, sp, si, H, 10)
    cur_o = order_from_starts(cur_st, topo)

    best_mk = cur_mk
    best_o = cur_o.copy()
    best_m = cur_m.copy()
    best_st = cur_st.copy()

    rem = ncap.copy()
    for j in range(n):
        mj = cur_m[j] - 1
        for k in range(N):
            rem[k] -= nreq[j, mj, k]

    pos = np.empty(n, np.int64)
    for i in range(n):
        pos[cur_o[i]] = i

    # Cooling schedule with reheating every n_iters // 3
    cycle_len = max(1000, n_iters // 3)
    evals = 1

    for it in range(n_iters):
        frac = float(it % cycle_len) / float(cycle_len)
        temp = t_start * ((t_end / t_start) ** frac)

        rng ^= rng >> np.uint64(12)
        rng ^= rng << np.uint64(25)
        rng ^= rng >> np.uint64(27)
        mv_type = int(rng % np.uint64(100))

        if mv_type < 35:
            # 1-job mode change
            rng ^= rng >> np.uint64(12)
            rng ^= rng << np.uint64(25)
            rng ^= rng >> np.uint64(27)
            j = 1 + int(rng % np.uint64(n - 2))
            if nm[j] <= 1:
                continue
            old_m = cur_m[j] - 1
            rng ^= rng >> np.uint64(12)
            rng ^= rng << np.uint64(25)
            rng ^= rng >> np.uint64(27)
            m2 = np.int64(rng % np.uint64(nm[j]))
            if m2 == old_m:
                m2 = (old_m + 1) % np.int64(nm[j])
            feas = True
            for k in range(N):
                if rem[k] + nreq[j, old_m, k] - nreq[j, m2, k] < 0:
                    feas = False
                    break
            if not feas:
                continue
            cur_m[j] = m2 + 1
            new_mk, new_st = eval_modes_order(cur_o, cur_m, dur, req, cap, pp, pi, sp, si, H, 3)
            evals += 1
            delta = new_mk - cur_mk
            accept = False
            if delta <= 0:
                accept = True
            else:
                rng ^= rng >> np.uint64(12)
                rng ^= rng << np.uint64(25)
                rng ^= rng >> np.uint64(27)
                u = float(rng & np.uint64(0xFFFFFF)) / 16777216.0
                if u < np.exp(-float(delta) / temp):
                    accept = True
            if accept:
                for k in range(N):
                    rem[k] += nreq[j, old_m, k] - nreq[j, m2, k]
                cur_mk = new_mk
                cur_st = new_st
                if new_mk <= best_mk + 1:
                    # Polish with deeper FBI
                    p_mk, p_st = eval_modes_order(cur_o, cur_m, dur, req, cap, pp, pi, sp, si, H, 15)
                    evals += 1
                    if p_mk < cur_mk:
                        cur_mk = p_mk
                        cur_st = p_st
                    if cur_mk < best_mk:
                        best_mk = cur_mk
                        best_m = cur_m.copy()
                        best_st = cur_st.copy()
                        best_o = order_from_starts(cur_st, topo)
                        cur_o = best_o.copy()
                        for i in range(n):
                            pos[cur_o[i]] = i
            else:
                cur_m[j] = old_m + 1

        elif mv_type < 65:
            # 2-job NR-trading mode swap
            rng ^= rng >> np.uint64(12)
            rng ^= rng << np.uint64(25)
            rng ^= rng >> np.uint64(27)
            u = 1 + int(rng % np.uint64(n - 2))
            rng ^= rng >> np.uint64(12)
            rng ^= rng << np.uint64(25)
            rng ^= rng >> np.uint64(27)
            v = 1 + int(rng % np.uint64(n - 2))
            if u == v or nm[u] <= 1 or nm[v] <= 1:
                continue
            old_u = cur_m[u] - 1
            old_v = cur_m[v] - 1
            rng ^= rng >> np.uint64(12)
            rng ^= rng << np.uint64(25)
            rng ^= rng >> np.uint64(27)
            mu = np.int64(rng % np.uint64(nm[u]))
            if mu == old_u:
                mu = (old_u + 1) % np.int64(nm[u])
            rng ^= rng >> np.uint64(12)
            rng ^= rng << np.uint64(25)
            rng ^= rng >> np.uint64(27)
            mv = np.int64(rng % np.uint64(nm[v]))
            if mv == old_v:
                mv = (old_v + 1) % np.int64(nm[v])
            feas = True
            for k in range(N):
                if (rem[k]
                    + nreq[u, old_u, k] - nreq[u, mu, k]
                    + nreq[v, old_v, k] - nreq[v, mv, k]) < 0:
                    feas = False
                    break
            if not feas:
                continue
            cur_m[u] = mu + 1
            cur_m[v] = mv + 1
            new_mk, new_st = eval_modes_order(cur_o, cur_m, dur, req, cap, pp, pi, sp, si, H, 3)
            evals += 1
            delta = new_mk - cur_mk
            accept = False
            if delta <= 0:
                accept = True
            else:
                rng ^= rng >> np.uint64(12)
                rng ^= rng << np.uint64(25)
                rng ^= rng >> np.uint64(27)
                u_r = float(rng & np.uint64(0xFFFFFF)) / 16777216.0
                if u_r < np.exp(-float(delta) / temp):
                    accept = True
            if accept:
                for k in range(N):
                    rem[k] += (nreq[u, old_u, k] - nreq[u, mu, k]
                               + nreq[v, old_v, k] - nreq[v, mv, k])
                cur_mk = new_mk
                cur_st = new_st
                if new_mk <= best_mk + 1:
                    p_mk, p_st = eval_modes_order(cur_o, cur_m, dur, req, cap, pp, pi, sp, si, H, 15)
                    evals += 1
                    if p_mk < cur_mk:
                        cur_mk = p_mk
                        cur_st = p_st
                    if cur_mk < best_mk:
                        best_mk = cur_mk
                        best_m = cur_m.copy()
                        best_st = cur_st.copy()
                        best_o = order_from_starts(cur_st, topo)
                        cur_o = best_o.copy()
                        for i in range(n):
                            pos[cur_o[i]] = i
            else:
                cur_m[u] = old_u + 1
                cur_m[v] = old_v + 1

        else:
            # Activity-list insert move
            cand_o, ok, rng = insert_move_numba(cur_o, pos, pp, pi, sp, si, rng)
            if not ok:
                continue
            new_mk, new_st = eval_modes_order(cand_o, cur_m, dur, req, cap, pp, pi, sp, si, H, 3)
            evals += 1
            delta = new_mk - cur_mk
            accept = False
            if delta <= 0:
                accept = True
            else:
                rng ^= rng >> np.uint64(12)
                rng ^= rng << np.uint64(25)
                rng ^= rng >> np.uint64(27)
                u_r = float(rng & np.uint64(0xFFFFFF)) / 16777216.0
                if u_r < np.exp(-float(delta) / temp):
                    accept = True
            if accept:
                cur_o = cand_o
                for i in range(n):
                    pos[cur_o[i]] = i
                cur_mk = new_mk
                cur_st = new_st
                if new_mk <= best_mk + 1:
                    p_mk, p_st = eval_modes_order(cur_o, cur_m, dur, req, cap, pp, pi, sp, si, H, 15)
                    evals += 1
                    if p_mk < cur_mk:
                        cur_mk = p_mk
                        cur_st = p_st
                    if cur_mk < best_mk:
                        best_mk = cur_mk
                        best_m = cur_m.copy()
                        best_st = cur_st.copy()
                        best_o = order_from_starts(cur_st, topo)
                        cur_o = best_o.copy()
                        for i in range(n):
                            pos[cur_o[i]] = i

    return best_mk, best_o, best_m, best_st, evals


def run_sa(X, init_modes, init_starts, time_budget: float, seed: int = 1):
    """Run timed chunked Numba SA with periodic restarts from best."""
    t0 = time.time()
    topo = np.array(engine.topo(X), dtype=np.int64)
    best_m = np.asarray(init_modes, dtype=np.int64).copy()
    best_st = np.asarray(init_starts, dtype=np.int64).copy()
    best_o = order_from_starts(best_st, topo)
    best_mk, best_st = eval_modes_order(best_o, best_m, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 15)
    best_o = order_from_starts(best_st, topo)

    total_evals = 1
    chunk_iters = 15000 if X.n <= 60 else 8000
    round_idx = 0
    while time.time() - t0 < time_budget:
        t_start = max(1.5, best_mk * 0.04)
        t_end = 0.08
        mk, o, m, st, ev = sa_joint_numba(
            best_o, best_m, X.dur, X.req, X.nreq, X.nm, X.cap, X.ncap,
            X.pp, X.pi, X.sp, X.si, X.H, topo, chunk_iters, t_start, t_end, seed + round_idx * 997
        )
        total_evals += ev
        round_idx += 1
        if mk < best_mk:
            best_mk, best_o, best_m, best_st = int(mk), o, m, st
    return best_mk, best_m, best_st, {"evals": total_evals, "rounds": round_idx, "secs": round(time.time() - t0, 2)}


@nb.njit(cache=True)
def sa_penalty_numba(
    init_order, init_modes, dur, req, nreq, nm, cap, ncap, pp, pi, sp, si, H,
    topo, n_iters, t_start, t_end, seed
):
    """
    Strategic-Oscillation Penalty-Guided Simulated Annealing over (activity_list, mode_vector).
    Allows stepping through NR-infeasible mode space (crucial when NR_rem == [0, 0, ...])
    with an adaptive penalty W_nr that oscillates to push trajectories across feasibility boundaries!
    Also tracks best STRICTLY NR-feasible solution found.
    """
    rng = np.uint64(seed * 6364136223846793005 + 1442695040888963407)
    n = len(init_modes)
    N = len(ncap)

    cur_o = init_order.copy()
    cur_m = init_modes.copy()
    cur_mk, cur_st = eval_modes_order(cur_o, cur_m, dur, req, cap, pp, pi, sp, si, H, 10)
    cur_o = order_from_starts(cur_st, topo)

    rem = ncap.copy()
    for j in range(n):
        mj = cur_m[j] - 1
        for k in range(N):
            rem[k] -= nreq[j, mj, k]

    cur_viol = 0
    for k in range(N):
        if rem[k] < 0:
            cur_viol -= rem[k]

    best_mk = cur_mk if cur_viol == 0 else H
    best_o = cur_o.copy()
    best_m = cur_m.copy()
    best_st = cur_st.copy()

    pos = np.empty(n, np.int64)
    for i in range(n):
        pos[cur_o[i]] = i

    # Adaptive penalty weight per unit of NR violation
    # Scale initial W_nr relative to typical NR usage
    w_nr = 0.5
    w_min = 0.08
    w_max = 8.0
    feas_streak = 0
    infeas_streak = 0

    cycle_len = max(2000, n_iters // 3)
    evals = 1
    feas_hits = 0

    for it in range(n_iters):
        frac = float(it % cycle_len) / float(cycle_len)
        temp = t_start * ((t_end / t_start) ** frac)

        # Strategic oscillation of penalty weight every 25 steps
        if cur_viol == 0:
            feas_streak += 1
            infeas_streak = 0
            if feas_streak >= 25:
                w_nr = max(w_min, w_nr * 0.85)
                feas_streak = 0
        else:
            infeas_streak += 1
            feas_streak = 0
            if infeas_streak >= 25:
                w_nr = min(w_max, w_nr * 1.18)
                infeas_streak = 0

        cur_energy = float(cur_mk) + w_nr * float(cur_viol)

        rng ^= rng >> np.uint64(12)
        rng ^= rng << np.uint64(25)
        rng ^= rng >> np.uint64(27)
        mv_type = int(rng % np.uint64(100))

        if mv_type < 65:
            # 1-job mode change (unrestricted by NR; penalized by w_nr)
            rng ^= rng >> np.uint64(12)
            rng ^= rng << np.uint64(25)
            rng ^= rng >> np.uint64(27)
            j = 1 + int(rng % np.uint64(n - 2))
            if nm[j] <= 1:
                continue
            old_m = cur_m[j] - 1
            rng ^= rng >> np.uint64(12)
            rng ^= rng << np.uint64(25)
            rng ^= rng >> np.uint64(27)
            m2 = np.int64(rng % np.uint64(nm[j]))
            if m2 == old_m:
                m2 = (old_m + 1) % np.int64(nm[j])

            new_viol = 0
            for k in range(N):
                rk = rem[k] + nreq[j, old_m, k] - nreq[j, m2, k]
                if rk < 0:
                    new_viol -= rk

            # Skip huge violations to keep trajectory near feasibility boundary
            if new_viol > 25 and new_viol > cur_viol:
                continue

            cur_m[j] = m2 + 1
            new_mk, new_st = eval_modes_order(cur_o, cur_m, dur, req, cap, pp, pi, sp, si, H, 2)
            evals += 1
            new_energy = float(new_mk) + w_nr * float(new_viol)
            delta = new_energy - cur_energy

            accept = False
            if delta <= 0.0:
                accept = True
            else:
                rng ^= rng >> np.uint64(12)
                rng ^= rng << np.uint64(25)
                rng ^= rng >> np.uint64(27)
                u = float(rng & np.uint64(0xFFFFFF)) / 16777216.0
                if u < np.exp(-delta / temp):
                    accept = True

            if accept:
                for k in range(N):
                    rem[k] += nreq[j, old_m, k] - nreq[j, m2, k]
                cur_viol = new_viol
                cur_mk = new_mk
                cur_st = new_st
                if cur_viol == 0:
                    feas_hits += 1
                    if cur_mk <= best_mk + 1:
                        p_mk, p_st = eval_modes_order(cur_o, cur_m, dur, req, cap, pp, pi, sp, si, H, 15)
                        evals += 1
                        if p_mk < cur_mk:
                            cur_mk = p_mk
                            cur_st = p_st
                        if cur_mk < best_mk:
                            best_mk = cur_mk
                            best_m = cur_m.copy()
                            best_st = cur_st.copy()
                            best_o = order_from_starts(cur_st, topo)
                            cur_o = best_o.copy()
                            for i in range(n):
                                pos[cur_o[i]] = i
            else:
                cur_m[j] = old_m + 1

        else:
            # Activity-list insert move
            cand_o, ok, rng = insert_move_numba(cur_o, pos, pp, pi, sp, si, rng)
            if not ok:
                continue
            new_mk, new_st = eval_modes_order(cand_o, cur_m, dur, req, cap, pp, pi, sp, si, H, 2)
            evals += 1
            delta = float(new_mk - cur_mk)
            accept = False
            if delta <= 0.0:
                accept = True
            else:
                rng ^= rng >> np.uint64(12)
                rng ^= rng << np.uint64(25)
                rng ^= rng >> np.uint64(27)
                u = float(rng & np.uint64(0xFFFFFF)) / 16777216.0
                if u < np.exp(-delta / temp):
                    accept = True
            if accept:
                cur_o = cand_o
                for i in range(n):
                    pos[cur_o[i]] = i
                cur_mk = new_mk
                cur_st = new_st
                if cur_viol == 0 and cur_mk <= best_mk + 1:
                    p_mk, p_st = eval_modes_order(cur_o, cur_m, dur, req, cap, pp, pi, sp, si, H, 15)
                    evals += 1
                    if p_mk < cur_mk:
                        cur_mk = p_mk
                        cur_st = p_st
                    if cur_mk < best_mk:
                        best_mk = cur_mk
                        best_m = cur_m.copy()
                        best_st = cur_st.copy()
                        best_o = order_from_starts(cur_st, topo)
                        cur_o = best_o.copy()
                        for i in range(n):
                            pos[cur_o[i]] = i

    return best_mk, best_o, best_m, best_st, evals, feas_hits


def run_sa_penalty(X, init_modes, init_starts, time_budget: float, seed: int = 1):
    """Run timed chunked Strategic-Oscillation Penalty SA."""
    t0 = time.time()
    topo = np.array(engine.topo(X), dtype=np.int64)
    best_m = np.asarray(init_modes, dtype=np.int64).copy()
    best_st = np.asarray(init_starts, dtype=np.int64).copy()
    best_o = order_from_starts(best_st, topo)
    best_mk, best_st = eval_modes_order(best_o, best_m, X.dur, X.req, X.cap, X.pp, X.pi, X.sp, X.si, X.H, 15)
    best_o = order_from_starts(best_st, topo)

    total_evals = 1
    total_feas = 0
    chunk_iters = 25000 if X.n <= 60 else 15000
    round_idx = 0
    while time.time() - t0 < time_budget:
        t_start = max(1.5, best_mk * 0.035)
        t_end = 0.08
        mk, o, m, st, ev, fh = sa_penalty_numba(
            best_o, best_m, X.dur, X.req, X.nreq, X.nm, X.cap, X.ncap,
            X.pp, X.pi, X.sp, X.si, X.H, topo, chunk_iters, t_start, t_end, seed + round_idx * 997
        )
        total_evals += ev
        total_feas += fh
        round_idx += 1
        if mk < best_mk:
            best_mk, best_o, best_m, best_st = int(mk), o, m, st
    return best_mk, best_m, best_st, {
        "evals": total_evals,
        "feas_hits": total_feas,
        "rounds": round_idx,
        "secs": round(time.time() - t0, 2),
    }

