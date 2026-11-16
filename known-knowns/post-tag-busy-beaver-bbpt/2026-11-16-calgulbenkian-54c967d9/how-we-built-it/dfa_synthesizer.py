#!/usr/bin/env python3
"""Automatic DFA Inductive Invariant Synthesizer & Verifier for 2-Tag Systems.

Combines:
1. Exact first-principles product-BFS verifier `verify_dfa_invariant(rules, cert)`.
2. Moore partition-refinement minimal total DFA engine.
3. Even-Position Projection `(k, m)`-local DFA + Greatest Fixpoint (`L <- L \\ Pre(~L)`),
   exploiting the exact theorem that odd tape indices `tape[1], tape[3], ...` never influence future steps.
4. Even-Position Immortal Factor Least Fixpoint (`L <- L union Post(L)` starting from `B in s(w)`).
5. Raw `(k, m)`-local DFA + Greatest Fixpoint and Backward Halting Closure (`Sigma^(>= 2)`).
"""
from collections import deque


def verify_dfa_invariant(rules, cert):
    """Exact standalone mathematical verification of a DFA inductive invariant."""
    n = len(rules)
    t0 = cert["entry_step"]
    K = cert["num_states"]
    trans = cert["transitions"]
    acc = set(cert["accepting"])

    if K < 1 or len(trans) != K:
        return False, "bad state count"
    for row in trans:
        if len(row) != n or any(not (0 <= q < K) for q in row):
            return False, "bad transition row"
    if any(not (0 <= q < K) for q in acc):
        return False, "bad accepting set"

    tape = (0, 0)
    for _ in range(t0):
        if len(tape) < 2:
            return False, "halted before entry_step"
        tape = tape[2:] + rules[tape[0]]

    # 1. Entry check: tape[t0] in L(M)
    q = 0
    for ch in tape:
        q = trans[q][ch]
    if q not in acc:
        return False, "tape[entry_step] not accepted by DFA"

    # 2. Safety check: epsilon not in L(M), and for all a in A, a not in L(M)
    if 0 in acc:
        return False, "epsilon accepted by DFA"
    for a in range(n):
        if trans[0][a] in acc:
            return False, f"single symbol {a} accepted by DFA"

    after_wa = []
    for a in range(n):
        wa = rules[a]
        row = []
        for p2 in range(K):
            cur = p2
            for ch in wa:
                cur = trans[cur][ch]
            row.append(cur)
        after_wa.append(row)

    # 3. Exact 1-step closure: for all a, b in A and u in A*, a b u in L(M) => u w_a in L(M).
    for a in range(n):
        qa = trans[0][a]
        after_a = after_wa[a]
        for b in range(n):
            qab = trans[qa][b]
            start = (qab, 0)
            visited = {start}
            queue = deque([start])
            while queue:
                p1, p2 = queue.popleft()
                if p1 in acc and after_a[p2] not in acc:
                    return False, f"closure violation for prefix ({a},{b}) at pair ({p1},{p2})"
                for c in range(n):
                    nxt = (trans[p1][c], trans[p2][c])
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append(nxt)

    return True, "OK"


def find_counterexample(rules, trans, acc_set):
    """Return True if closed, False otherwise."""
    n = len(rules)
    K = len(trans)
    after_wa = []
    for a in range(n):
        wa = rules[a]
        row = []
        for p2 in range(K):
            cur = p2
            for ch in wa:
                cur = trans[cur][ch]
            row.append(cur)
        after_wa.append(row)

    for a in range(n):
        qa = trans[0][a]
        after_a = after_wa[a]
        for b in range(n):
            qab = trans[qa][b]
            start = (qab, 0)
            visited = {start}
            queue = deque([start])
            while queue:
                p1, p2 = queue.popleft()
                if p1 in acc_set and after_a[p2] not in acc_set:
                    return False
                for c in range(n):
                    nxt = (trans[p1][c], trans[p2][c])
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append(nxt)
    return True


def minimize_dfa(n, trans, acc):
    """Minimize a total DFA (state 0 = initial), keeping reachable states in canonical BFS order."""
    reach = []
    seen = {0}
    queue = deque([0])
    while queue:
        q = queue.popleft()
        reach.append(q)
        for c in range(n):
            qn = trans[q][c]
            if qn not in seen:
                seen.add(qn)
                queue.append(qn)
    remap = {old: i for i, old in enumerate(reach)}
    K = len(reach)
    t_sub = [[remap[trans[old][c]] for c in range(n)] for old in reach]
    acc_sub = {remap[old] for old in acc if old in remap}

    if K <= 1:
        return t_sub, sorted(acc_sub)

    cls = [1 if q in acc_sub else 0 for q in range(K)]
    num_cls = len(set(cls))
    if num_cls == 1:
        return [[0] * n], ([0] if 0 in acc_sub else [])

    while True:
        sig_map = {}
        new_cls = [0] * K
        for q in range(K):
            sig = (cls[q],) + tuple(cls[t_sub[q][c]] for c in range(n))
            cid = sig_map.get(sig)
            if cid is None:
                cid = len(sig_map)
                sig_map[sig] = cid
            new_cls[q] = cid
        if len(sig_map) == num_cls:
            cls = new_cls
            break
        cls = new_cls
        num_cls = len(sig_map)

    reps = {}
    for q, cid in enumerate(cls):
        if cid not in reps:
            reps[cid] = q
    bfs_cids = []
    seen_c = {cls[0]}
    q_c = deque([cls[0]])
    while q_c:
        cid = q_c.popleft()
        bfs_cids.append(cid)
        rep_q = reps[cid]
        for c in range(n):
            ncid = cls[t_sub[rep_q][c]]
            if ncid not in seen_c:
                seen_c.add(ncid)
                q_c.append(ncid)
    cid_to_new = {cid: i for i, cid in enumerate(bfs_cids)}
    min_trans = [
        [cid_to_new[cls[t_sub[reps[cid]][c]]] for c in range(n)]
        for cid in bfs_cids
    ]
    min_acc = sorted(cid_to_new[cid] for cid in bfs_cids if reps[cid] in acc_sub)
    return min_trans, min_acc


def dfa_accepts(trans, acc_set, word):
    q = 0
    for ch in word:
        q = trans[q][ch]
    return q in acc_set


def refine_step_closure(rules, trans, acc, entry_word, max_iters=40, max_states=500):
    """Greatest fixpoint L_{j+1} = { w in L_j : |w| >= 2 and step(w) in L_j }."""
    n = len(rules)
    trans, acc = minimize_dfa(n, trans, set(acc))
    for _ in range(max_iters):
        acc_set = set(acc)
        if not dfa_accepts(trans, acc_set, entry_word):
            return None
        if 0 not in acc_set and all(trans[0][a] not in acc_set for a in range(n)):
            if find_counterexample(rules, trans, acc_set):
                return trans, acc

        K = len(trans)
        if K > max_states:
            return None

        good_after_wa = []
        for a in range(n):
            wa = rules[a]
            good_p2 = set()
            for p2 in range(K):
                cur = p2
                for ch in wa:
                    cur = trans[cur][ch]
                if cur in acc_set:
                    good_p2.add(p2)
            good_after_wa.append(good_p2)

        new_trans = [[0] * n for _ in range(1 + n)]
        for a in range(n):
            new_trans[0][a] = 1 + a

        tuple_to_id = {}
        new_acc = []
        queue = deque()

        for a in range(n):
            qa = trans[0][a]
            for b in range(n):
                qab = trans[qa][b]
                st = (a, qab, 0)
                sid = tuple_to_id.get(st)
                if sid is None:
                    sid = len(new_trans)
                    tuple_to_id[st] = sid
                    new_trans.append([0] * n)
                    if qab in acc_set and 0 in good_after_wa[a]:
                        new_acc.append(sid)
                    queue.append(st)
                new_trans[1 + a][b] = sid

        aborted = False
        while queue:
            if len(new_trans) > max_states * 4:
                aborted = True
                break
            a, p1, p2 = queue.popleft()
            sid = tuple_to_id[(a, p1, p2)]
            for c in range(n):
                st2 = (a, trans[p1][c], trans[p2][c])
                sid2 = tuple_to_id.get(st2)
                if sid2 is None:
                    sid2 = len(new_trans)
                    tuple_to_id[st2] = sid2
                    new_trans.append([0] * n)
                    if st2[1] in acc_set and st2[2] in good_after_wa[a]:
                        new_acc.append(sid2)
                    queue.append(st2)
                new_trans[sid][c] = sid2

        if aborted:
            return None
        trans, acc = minimize_dfa(n, new_trans, set(new_acc))
    return None


def build_even_km_local_dfa(n, words, k, m):
    """Build total DFA over Sigma* that ignores odd indices (tape[1], tape[3], ...)
    and learns (last k even-index chars, even_len mod m, total_len_parity) from `words`!"""
    state_map = {(0, 0, (), 0): 0}  # (pos_parity, len_cap_2, even_hist, even_idx_mod_m)
    edges = {}
    accepting_states = set()

    def get_id(st):
        sid = state_map.get(st)
        if sid is None:
            sid = len(state_map)
            state_map[st] = sid
        return sid

    # Notice: at odd indices (pos_parity == 1), ANY symbol c in 0..n-1 is allowed and transitions
    # to the SAME state (0, min(2, lcap+1), hist, emod)!
    odd_states_to_expand = set()
    for w in words:
        if len(w) < 2:
            continue
        par = 0
        lcap = 0
        hist = ()
        emod = 0
        cur_id = 0
        for ch in w:
            nlcap = min(2, lcap + 1)
            if par == 0:
                nhist = (hist + (ch,))[-k:] if k > 0 else ()
                nemod = (emod + 1) % m
                nst = (1, nlcap, nhist, nemod)
                nid = get_id(nst)
                edges[(cur_id, ch)] = nid
                odd_states_to_expand.add((nid, nlcap, nhist, nemod))
                par, lcap, hist, emod, cur_id = 1, nlcap, nhist, nemod, nid
            else:
                nst = (0, nlcap, hist, emod)
                nid = get_id(nst)
                for any_c in range(n):
                    edges[(cur_id, any_c)] = nid
                par, lcap, cur_id = 0, nlcap, nid
        accepting_states.add(cur_id)

    # Ensure odd states reached at the end of odd-length words ALSO allow transitioning to even length if needed
    dead_id = len(state_map)
    total_states = dead_id + 1
    trans = [[dead_id] * n for _ in range(total_states)]
    for (u, ch), v in edges.items():
        trans[u][ch] = v
    return minimize_dfa(n, trans, accepting_states)


def build_km_local_dfa(n, words, k, m):
    state_map = {("", 0): 0}
    edges = {}
    accepting_states = set()

    def get_id(st):
        sid = state_map.get(st)
        if sid is None:
            sid = len(state_map)
            state_map[st] = sid
        return sid

    for w in words:
        if len(w) < 2:
            continue
        hist = ()
        pos_mod = 0
        cur_id = 0
        for idx, ch in enumerate(w):
            nxt_hist = (hist + (ch,))[-k:] if k > 0 else ()
            nxt_mod = (pos_mod + 1) % m
            len_cap = min(idx + 1, 2)
            nxt_st = (len_cap, nxt_hist, nxt_mod)
            nxt_id = get_id(nxt_st)
            edges[(cur_id, ch)] = nxt_id
            hist = nxt_hist
            pos_mod = nxt_mod
            cur_id = nxt_id
        accepting_states.add(cur_id)

    dead_id = len(state_map)
    total_states = dead_id + 1
    trans = [[dead_id] * n for _ in range(total_states)]
    for (u, ch), v in edges.items():
        trans[u][ch] = v
    return minimize_dfa(n, trans, accepting_states)


def union_post_dfa(rules, trans, acc, max_states=400):
    """Compute minimal DFA for L union Post(L), returning None if Post(L) intersects Sigma^(< 2) or blows up."""
    n = len(rules)
    K = len(trans)
    acc_set = set(acc)

    # Build NFA for L unionbigcup_{a in A} { u w_a : exists b in A, a b u in L }
    # NFA states:
    # - 0..K-1: original DFA M (start state 0, accepting acc_set)
    # - For each a in 0..n-1:
    #     copy of M states (offset_a + 0 .. offset_a + K - 1), started at { trans[trans[0][a]][b] for b in 0..n-1 },
    #     plus tail chain for w_a: tail_a_0 -> tail_a_1 -> ... -> tail_a_{|w_a|} (accepting),
    #     where whenever copy-state q is in acc_set, epsilon-transition to tail_a_0!
    # Subset construction directly!
    tail_offsets = []
    cur_id = K
    copy_offsets = []
    for a in range(n):
        copy_offsets.append(cur_id)
        cur_id += K
        tail_offsets.append(cur_id)
        cur_id += len(rules[a]) + 1

    total_nfa = cur_id
    eps = [set() for _ in range(total_nfa)]
    nfa_moves = [[set() for _ in range(n)] for _ in range(total_nfa)]
    nfa_acc = set(acc_set)

    # Original DFA transitions
    for q in range(K):
        for c in range(n):
            nfa_moves[q][c].add(trans[q][c])

    # Start epsilon transitions from super-start? Include {0} union start_a
    init_set = {0}
    for a in range(n):
        coff = copy_offsets[a]
        toff = tail_offsets[a]
        wa = rules[a]
        for b in range(n):
            init_set.add(coff + trans[trans[0][a]][b])
        for q in range(K):
            for c in range(n):
                nfa_moves[coff + q][c].add(coff + trans[q][c])
            if q in acc_set:
                eps[coff + q].add(toff)
        for j, ch in enumerate(wa):
            nfa_moves[toff + j][ch].add(toff + j + 1)
        nfa_acc.add(toff + len(wa))

    def eps_close(ss):
        out = set(ss)
        st = list(ss)
        while st:
            x = st.pop()
            for y in eps[x]:
                if y not in out:
                    out.add(y)
                    st.append(y)
        return frozenset(out)

    s0 = eps_close(init_set)
    if s0 & nfa_acc:
        return None  # epsilon accepted -> unsafe!
    sub_map = {s0: 0}
    d_trans = [[0] * n]
    d_acc = []
    queue = deque([s0])
    while queue:
        if len(d_trans) > max_states:
            return None
        cur_s = queue.popleft()
        uid = sub_map[cur_s]
        for c in range(n):
            raw_nxt = set()
            for x in cur_s:
                raw_nxt |= nfa_moves[x][c]
            ns = eps_close(raw_nxt)
            vid = sub_map.get(ns)
            if vid is None:
                vid = len(d_trans)
                sub_map[ns] = vid
                d_trans.append([0] * n)
                if ns & nfa_acc:
                    d_acc.append(vid)
                queue.append(ns)
            d_trans[uid][c] = vid

    # Check length-1 safety
    d_acc_set = set(d_acc)
    if any(d_trans[0][a] in d_acc_set for a in range(n)):
        return None
    return minimize_dfa(n, d_trans, d_acc_set)


def build_even_factor_dfa(n, factor):
    """Total DFA for { w in Sigma^(>= 2) : `factor` is a contiguous substring of (w[0], w[2], ...) }."""
    r = len(factor)
    # KMP prefix lengths 0..r on even positions; state = (pos_parity, min(len, 2), matched_len)
    states = [(0, 0, 0)]
    smap = {states[0]: 0}
    trans = []
    acc = set()
    idx = 0
    while idx < len(states):
        par, lcap, mlen = states[idx]
        row = []
        for ch in range(n):
            nlcap = min(2, lcap + 1)
            if par == 0:
                if mlen == r:
                    nmlen = r
                else:
                    cand = factor[:mlen] + (ch,)
                    nmlen = 0
                    for k in range(len(cand), 0, -1):
                        if cand[-k:] == factor[:k]:
                            nmlen = k
                            break
                nst = (1, nlcap, nmlen)
            else:
                nst = (0, nlcap, mlen)
            if nst not in smap:
                smap[nst] = len(states)
                states.append(nst)
            row.append(smap[nst])
        trans.append(row)
        if lcap >= 2 and mlen == r:
            acc.add(idx)
        idx += 1
    return minimize_dfa(n, trans, acc)


def try_immortal_even_factors(rules, traj):
    """Try Least-Fixpoint Post* closure from single immortal substrings on the even projection."""
    n = len(rules)
    t0 = min(20, len(traj) - 1)
    w0 = traj[t0]
    ev = w0[0::2]
    seen_factors = []
    for r in (1, 2, 3):
        for i in range(len(ev) - r + 1):
            fac = ev[i : i + r]
            if fac not in seen_factors:
                seen_factors.append(fac)
    for fac in seen_factors[:16]:
        tr, ac = build_even_factor_dfa(n, fac)
        for _ in range(12):
            if find_counterexample(rules, tr, set(ac)):
                if dfa_accepts(tr, set(ac), w0):
                    cert = {"type": "DFA_INVARIANT", "entry_step": t0, "num_states": len(tr), "transitions": tr, "accepting": ac}
                    ok, _ = verify_dfa_invariant(rules, cert)
                    if ok:
                        return cert
                break
            nxt = union_post_dfa(rules, tr, ac, max_states=300)
            if nxt is None:
                break
            tr, ac = nxt
    return None


def synthesize_dfa_for_system(rules, sim_steps=800, max_tape_len=900):
    n = len(rules)

    if all(len(w) >= 2 for w in rules):
        trans = [[1] * n, [2] * n, [2] * n]
        cert = {"type": "DFA_INVARIANT", "entry_step": 0, "num_states": 3, "transitions": trans, "accepting": [2]}
        ok, _ = verify_dfa_invariant(rules, cert)
        if ok:
            return cert

    tape = (0, 0)
    traj = [tape]
    seen = {tape: 0}
    for t in range(1, sim_steps + 1):
        if len(tape) < 2:
            return {"type": "HALT", "steps": t - 1}
        tape = tape[2:] + rules[tape[0]]
        if len(tape) < 2:
            return {"type": "HALT", "steps": t}
        if tape in seen:
            t1 = seen[tape]
            return {"type": "CYCLE", "entry_step": t1, "period": t - t1}
        if len(tape) <= max_tape_len:
            seen[tape] = t
            traj.append(tape)
        else:
            break

    # Tier 1: Immortal even-projection factor Post* closure (instant, tiny DFAs!)
    imm = try_immortal_even_factors(rules, traj)
    if imm is not None:
        return imm

    # Tier 2: Even-Projection (k, m)-local DFA + greatest fixpoint (ignores dead odd positions!)
    for max_st, max_it in [(200, 25), (450, 40)]:
        for t0 in [min(30, len(traj) // 4), min(80, len(traj) // 2), 0]:
            sample_words = traj[t0 : t0 + 350]
            if len(sample_words) < 10:
                continue
            for k in [1, 2, 3, 4]:
                for m in [1, 2, 3, 4]:
                    tr0, ac0 = build_even_km_local_dfa(n, sample_words, k, m)
                    if len(tr0) > max_st:
                        continue
                    res = refine_step_closure(rules, tr0, ac0, traj[t0], max_iters=max_it, max_states=max_st)
                    if res is not None:
                        tr, ac = res
                        cert = {
                            "type": "DFA_INVARIANT",
                            "entry_step": t0,
                            "num_states": len(tr),
                            "transitions": tr,
                            "accepting": ac,
                        }
                        ok, _ = verify_dfa_invariant(rules, cert)
                        if ok:
                            return cert

    # Tier 3: Full-tape (k, m)-local DFA + greatest fixpoint
    for t0 in [min(30, len(traj) // 4), 0]:
        sample_words = traj[t0 : t0 + 300]
        if len(sample_words) < 10:
            continue
        for k in [2, 3, 4]:
            for m in [1, 2, 4]:
                tr0, ac0 = build_km_local_dfa(n, sample_words, k, m)
                if len(tr0) > 350:
                    continue
                res = refine_step_closure(rules, tr0, ac0, traj[t0], max_iters=30, max_states=400)
                if res is not None:
                    tr, ac = res
                    cert = {
                        "type": "DFA_INVARIANT",
                        "entry_step": t0,
                        "num_states": len(tr),
                        "transitions": tr,
                        "accepting": ac,
                    }
                    ok, _ = verify_dfa_invariant(rules, cert)
                    if ok:
                        return cert

    # Tier 4: Backward quotient from Sigma^(>= 2)
    trans_ge2 = [[1] * n, [2] * n, [2] * n]
    for t0 in [0, min(20, len(traj) - 1)]:
        res = refine_step_closure(rules, trans_ge2, [2], traj[t0], max_iters=25, max_states=250)
        if res is not None:
            tr, ac = res
            cert = {"type": "DFA_INVARIANT", "entry_step": t0, "num_states": len(tr), "transitions": tr, "accepting": ac}
            ok, _ = verify_dfa_invariant(rules, cert)
            if ok:
                return cert

    return None
