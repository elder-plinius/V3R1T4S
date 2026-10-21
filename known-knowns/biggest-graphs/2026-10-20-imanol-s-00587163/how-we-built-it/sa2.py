"""
SA2: same move set as sa.py, but with SOUND early rejection so big graphs (N ~ 3k-12k) are affordable.

Bookkeeping: BAD[p] = bitset of q with d(p,q) > D (exact, from the last full evaluation / exact updates).
For a proposed move (removals R, additions A) with Metropolis threshold thr = -T ln(u) >= 0:
  gain = # currently-bad pairs fixed (exact: BFS in G' from the endpoints of added edges; a bad pair can only be fixed
         by a path through an added edge, and d' are exact distances in G')
  L    = # currently-good pairs that become bad (>= 0); L >= L_part = # such pairs with one end in the
         endpoints of removed edges (BFS in G' from those endpoints).
  dcost = L - gain >= L_part - gain.  If L_part - gain > thr: reject (sound).
  If no removals: dcost = -gain exactly, update BAD without a full evaluation.
  Otherwise: full exact bitset evaluation.
"""
import numpy as np
from numba import njit
from ddlib import bfs_dist, has_edge, add_edge, rm_edge, popcount64


@njit(cache=True)
def full_eval_store(adj, deg, n, D, W, R, Rn, BAD, defic):
    for v in range(n):
        for w in range(W):
            R[v, w] = 0
        R[v, v >> 6] |= np.uint64(1) << np.uint64(v & 63)
    for step in range(D - 1):
        for v in range(n):
            for w in range(W):
                Rn[v, w] = R[v, w]
            for j in range(deg[v]):
                u = adj[v, j]
                for w in range(W):
                    Rn[v, w] |= R[u, w]
        R, Rn = Rn, R
    total = 0
    lastmask = np.uint64(0xFFFFFFFFFFFFFFFF)
    rem = n & 63
    if rem != 0:
        lastmask = (np.uint64(1) << np.uint64(rem)) - np.uint64(1)
    for v in range(n):
        c = 0
        for w in range(W):
            x = R[v, w]
            for j in range(deg[v]):
                x |= R[adj[v, j], w]
            nb = ~x
            if w == W - 1:
                nb &= lastmask
            BAD[v, w] = nb
            c += popcount64(nb)
        defic[v] = c
        total += c
    return total // 2


@njit(cache=True)
def _undo(adj, deg, ops, nops):
    for t in range(nops - 1, -1, -1):
        typ = ops[t, 0]; a = ops[t, 1]; b = ops[t, 2]
        if typ == 1:
            rm_edge(adj, deg, a, b)
        else:
            add_edge(adj, deg, a, b)


@njit(cache=True)
def _isbad(BAD, p, q):
    return (BAD[p, q >> 6] >> np.uint64(q & 63)) & np.uint64(1)


@njit(cache=True)
def sa2_run(adj, deg, n, D, Delta, iters, T0, T1, seed, p_target, p_fill, p_free, max_noimp, time_iters_check):
    np.random.seed(seed)
    W = (n + 63) // 64
    R = np.zeros((n, W), np.uint64); Rn = np.zeros((n, W), np.uint64)
    BAD = np.zeros((n, W), np.uint64)
    defic = np.zeros(n, np.int64)
    BAD2 = np.zeros((n, W), np.uint64); defic2 = np.zeros(n, np.int64)
    distx = np.empty(n, np.int32); disty = np.empty(n, np.int32); queue = np.empty(n, np.int32)
    lst = np.empty(n, np.int32); lst2 = np.empty(n, np.int32)
    # distances from up to 4 added-edge endpoints and 4 removed-edge endpoints
    dA = np.empty((4, n), np.int32)
    dR = np.empty((4, n), np.int32)
    cost = full_eval_store(adj, deg, n, D, W, R, Rn, BAD, defic)
    best = cost
    best_adj = adj.copy(); best_deg = deg.copy()
    ops = np.zeros((16, 3), np.int64)
    acc = 0; nfull = 0; nscreen = 0
    last_imp = 0
    # bad pair list (p<q) rebuilt after each full eval
    maxP = 200000
    Pp = np.empty(maxP, np.int32); Pq = np.empty(maxP, np.int32)
    nP = 0
    for p in range(n):
        if defic[p] > 0:
            for q in range(p + 1, n):
                if _isbad(BAD, p, q):
                    if nP < maxP:
                        Pp[nP] = p; Pq[nP] = q; nP += 1
    addA = np.empty((4, 2), np.int64); remR = np.empty((4, 2), np.int64)
    for it in range(iters):
        if cost == 0:
            break
        if it - last_imp > max_noimp:
            break
        T = T0 * (T1 / T0) ** (it / iters)
        nops = 0
        r = np.random.random()
        ok = False
        if r < p_fill + p_free:
            # pure addition between deficient vertices near a bad pair's ends (M1free)
            if nP > 0:
                k = np.random.randint(nP)
                x = Pp[k]; y = Pq[k]
                if np.random.random() < 0.5:
                    x, y = y, x
                bfs_dist(adj, deg, n, x, distx, queue)
                bfs_dist(adj, deg, n, y, disty, queue)
                na = 0
                for v in range(n):
                    if deg[v] < Delta and distx[v] >= 0 and distx[v] <= D - 1:
                        lst[na] = v; na += 1
                nb2 = 0
                for v in range(n):
                    if deg[v] < Delta and disty[v] >= 0 and disty[v] <= D - 1:
                        lst2[nb2] = v; nb2 += 1
                if na > 0 and nb2 > 0:
                    for tries in range(200):
                        a = lst[np.random.randint(na)]
                        b = lst2[np.random.randint(nb2)]
                        if a != b and distx[a] + disty[b] <= D - 1 and not has_edge(adj, deg, a, b):
                            add_edge(adj, deg, a, b)
                            ops[nops, 0] = 1; ops[nops, 1] = a; ops[nops, 2] = b; nops += 1
                            ok = True
                            break
        elif r < p_fill + p_free + p_target:
            if nP > 0:
                k = np.random.randint(nP)
                x = Pp[k]; y = Pq[k]
                if np.random.random() < 0.5:
                    x, y = y, x
                bfs_dist(adj, deg, n, x, distx, queue)
                bfs_dist(adj, deg, n, y, disty, queue)
                i = np.random.randint(D)
                j = D - 1 - i
                ma = 0
                for v in range(n):
                    if distx[v] == i:
                        lst[ma] = v; ma += 1
                a = lst[np.random.randint(ma)] if ma > 0 else -1
                mb = 0
                for v in range(n):
                    if disty[v] == j:
                        lst[mb] = v; mb += 1
                b = lst[np.random.randint(mb)] if mb > 0 else -1
                if a >= 0 and b >= 0 and a != b and not has_edge(adj, deg, a, b):
                    c = -1; d = -1
                    if deg[a] >= Delta:
                        for tries in range(6):
                            c = adj[a, np.random.randint(deg[a])]
                            if distx[c] >= i:
                                break
                    if deg[b] >= Delta:
                        for tries in range(6):
                            d = adj[b, np.random.randint(deg[b])]
                            if disty[d] >= j:
                                break
                    if c >= 0:
                        rm_edge(adj, deg, a, c)
                        ops[nops, 0] = 2; ops[nops, 1] = a; ops[nops, 2] = c; nops += 1
                    if d >= 0:
                        rm_edge(adj, deg, b, d)
                        ops[nops, 0] = 2; ops[nops, 1] = b; ops[nops, 2] = d; nops += 1
                    add_edge(adj, deg, a, b)
                    ops[nops, 0] = 1; ops[nops, 1] = a; ops[nops, 2] = b; nops += 1
                    if c >= 0 and d >= 0 and c != d and not has_edge(adj, deg, c, d):
                        add_edge(adj, deg, c, d)
                        ops[nops, 0] = 1; ops[nops, 1] = c; ops[nops, 2] = d; nops += 1
                    ok = True
        else:
            for tries in range(20):
                a = np.random.randint(n)
                if deg[a] == 0:
                    continue
                b = adj[a, np.random.randint(deg[a])]
                c = np.random.randint(n)
                if deg[c] == 0:
                    continue
                d = adj[c, np.random.randint(deg[c])]
                if a == c or a == d or b == c or b == d:
                    continue
                if has_edge(adj, deg, a, d) or has_edge(adj, deg, c, b):
                    continue
                rm_edge(adj, deg, a, b); rm_edge(adj, deg, c, d)
                add_edge(adj, deg, a, d); add_edge(adj, deg, c, b)
                ops[0, 0] = 2; ops[0, 1] = a; ops[0, 2] = b
                ops[1, 0] = 2; ops[1, 1] = c; ops[1, 2] = d
                ops[2, 0] = 1; ops[2, 1] = a; ops[2, 2] = d
                ops[3, 0] = 1; ops[3, 1] = c; ops[3, 2] = b
                nops = 4
                ok = True
                break
        if not ok:
            continue
        thr = -T * np.log(np.random.random() + 1e-300)
        # collect added / removed edges
        nA = 0; nR = 0
        for t in range(nops):
            if ops[t, 0] == 1:
                addA[nA, 0] = ops[t, 1]; addA[nA, 1] = ops[t, 2]; nA += 1
            else:
                remR[nR, 0] = ops[t, 1]; remR[nR, 1] = ops[t, 2]; nR += 1
        # exact gain on current bad pairs
        ne = 0
        for e in range(nA):
            bfs_dist(adj, deg, n, addA[e, 0], dA[ne], queue); ne += 1
            bfs_dist(adj, deg, n, addA[e, 1], dA[ne], queue); ne += 1
        gain = 0
        for k in range(nP):
            p = Pp[k]; q = Pq[k]
            fixed = False
            for e in range(nA):
                du_p = dA[2 * e, p]; dv_q = dA[2 * e + 1, q]
                dv_p = dA[2 * e + 1, p]; du_q = dA[2 * e, q]
                if du_p >= 0 and dv_q >= 0 and du_p + 1 + dv_q <= D:
                    fixed = True
                if dv_p >= 0 and du_q >= 0 and dv_p + 1 + du_q <= D:
                    fixed = True
                # also shortest distance via exact BFS values: d'(p,q) <= d'(p,u)+d'(u,q)
                if du_p >= 0 and du_q >= 0 and du_p + du_q <= D:
                    fixed = True
                if dv_p >= 0 and dv_q >= 0 and dv_p + dv_q <= D:
                    fixed = True
            if fixed:
                gain += 1
        if nR == 0:
            # pure addition: exact
            dc = -gain
            if gain > 0:
                # exact update: recompute BAD rows only for vertices in bad pairs via BFS
                cost = cost - gain
                acc += 1
                # rebuild P by BFS from each vertex currently in a bad pair (exact)
                nP2 = 0
                for k in range(nP):
                    p = Pp[k]; q = Pq[k]
                    still = True
                    for e in range(nA):
                        du_p = dA[2 * e, p]; dv_q = dA[2 * e + 1, q]
                        dv_p = dA[2 * e + 1, p]; du_q = dA[2 * e, q]
                        if du_p >= 0 and dv_q >= 0 and du_p + 1 + dv_q <= D:
                            still = False
                        if dv_p >= 0 and du_q >= 0 and dv_p + 1 + du_q <= D:
                            still = False
                        if du_p >= 0 and du_q >= 0 and du_p + du_q <= D:
                            still = False
                        if dv_p >= 0 and dv_q >= 0 and dv_p + dv_q <= D:
                            still = False
                    if still:
                        Pp[nP2] = p; Pq[nP2] = q; nP2 += 1
                    else:
                        BAD[p, q >> 6] &= ~(np.uint64(1) << np.uint64(q & 63))
                        BAD[q, p >> 6] &= ~(np.uint64(1) << np.uint64(p & 63))
                        defic[p] -= 1; defic[q] -= 1
                nP = nP2
                if cost < best:
                    best = cost
                    best_adj[:, :] = adj[:, :]; best_deg[:] = deg[:]
                    last_imp = it
            else:
                _undo(adj, deg, ops, nops)
            continue
        # screening with removed-edge endpoints (unique), sound lower bound on new bad pairs
        nscreen += 1
        ends = np.empty(4, np.int64)
        cnt = 0
        for e in range(nR):
            for s_ in range(2):
                v = remR[e, s_]
                dup = False
                for t in range(cnt):
                    if ends[t] == v:
                        dup = True
                if not dup:
                    ends[cnt] = v; cnt += 1
        Lp = 0
        for t in range(cnt):
            v = ends[t]
            bfs_dist(adj, deg, n, v, dR[t], queue)
            for q in range(n):
                dq = dR[t, q]
                if (dq < 0 or dq > D) and not _isbad(BAD, v, q):
                    Lp += 1
        dbl = 0
        for t1 in range(cnt):
            for t2 in range(t1 + 1, cnt):
                dd = dR[t1, ends[t2]]
                if (dd < 0 or dd > D) and not _isbad(BAD, ends[t1], ends[t2]):
                    dbl += 1
        Lp -= dbl
        if Lp - gain > thr:
            _undo(adj, deg, ops, nops)
            continue
        nfull += 1
        newcost = full_eval_store(adj, deg, n, D, W, R, Rn, BAD2, defic2)
        dc = newcost - cost
        if dc <= thr:
            cost = newcost
            tmpB = BAD; BAD = BAD2; BAD2 = tmpB
            tmpd = defic; defic = defic2; defic2 = tmpd
            acc += 1
            nP = 0
            for p in range(n):
                if defic[p] > 0:
                    for q in range(p + 1, n):
                        if _isbad(BAD, p, q):
                            if nP < maxP:
                                Pp[nP] = p; Pq[nP] = q; nP += 1
            if cost < best:
                best = cost
                best_adj[:, :] = adj[:, :]; best_deg[:] = deg[:]
                last_imp = it
        else:
            _undo(adj, deg, ops, nops)
    return best, best_adj, best_deg, acc, nfull, nscreen
