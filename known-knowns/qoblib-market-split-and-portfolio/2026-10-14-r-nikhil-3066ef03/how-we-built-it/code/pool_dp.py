"""crossover lens: exact chain DP over a pool of per-period portfolios, then exact descent polish.

Each pool solution contributes its portfolio w_k for every active period k = 0..L-1 (period L = t_end stays flat). The
objective splits into node costs (risk, return, cash, short of w_k) and edge costs (trading d_k |w_k - w_{k-1}|, entry
d_0 |w_0|; nothing into t_end), so the best mix of pool rows is a shortest path (Viterbi) over periods. Each row is
feasible on its own (budget and net are per period), so every path is feasible. Then polish with quoter2's descent.

Usage: pool_dp.py QUOTER_CODE_DIR INSTANCE_DIR B LAMBDA INSTANCE_NAME OUT_PREFIX POLISH_SECONDS SOL [SOL ...]
"""
import sys
import time

import numpy as np

sys.path.insert(0, sys.argv[1])
from pfmodel import Model  # noqa: E402
from quoter2 import Book  # noqa: E402


def main():
    code, inst, B, lam, name, out, polish = sys.argv[1:8]
    sols = sys.argv[8:]
    t0 = time.time()
    m = Model(inst, int(B), lam)
    L = m.nT - 1
    pool = []
    for s in sols:
        W = m.read_solution(s)
        if m.feasible(W) and not W[L].any():
            pool.append((s, W, m.objective(W)))
    print("pool: %d solutions; best single %d (%s)" % (len(pool), min(p[2] for p in pool), min(pool, key=lambda p: p[2])[0]))
    cands = []
    for k in range(L):
        rows = {}
        for (_, W, _) in pool:
            rows[W[k].tobytes()] = W[k].copy()
        cands.append(list(rows.values()))
    node = [np.array([int(w @ m.Q[k] @ w) + int(m.lin[k] @ w) + int(m.s[k] @ np.maximum(-w, 0)) for w in cands[k]])
            for k in range(L)]
    best = [node[0] + np.array([int(m.d[0] @ np.abs(w)) for w in cands[0]])]
    back = [None]
    for k in range(1, L):
        A = np.array(cands[k - 1])
        cost = np.zeros((len(cands[k]),), dtype=np.int64)
        arg = np.zeros((len(cands[k]),), dtype=np.int64)
        for c, w in enumerate(cands[k]):
            e = np.abs(A - w) @ m.d[k] + best[k - 1]
            arg[c] = int(np.argmin(e))
            cost[c] = int(e[arg[c]]) + node[k][c]
        best.append(cost)
        back.append(arg)
    c = int(np.argmin(best[L - 1]))
    W = np.zeros((m.nT, m.n), dtype=np.int64)
    for k in range(L - 1, -1, -1):
        W[k] = cands[k][c]
        if k > 0:
            c = int(back[k][c])
    obj = m.objective(W)
    print("DP mix objective %d (DP value + cash constant %d)" % (obj, int(best[L - 1].min()) - 100 * m.nT))
    src = []
    for k in range(L):
        src.append([i for i, (_, P, _) in enumerate(pool) if np.array_equal(P[k], W[k])][:1])
    print("period sources (pool index):", src)
    m.write_solution(out + "_mix.sol", W, name, lam, "V3R1T4S lane C crossover chain-DP mix (judge with pf_eval.py)")
    bk = Book(m, W)
    steps, local = bk.descend(time.time() + float(polish))
    print("polish: %d steps, local_opt=%s, objective %d (recomputed %d)" % (steps, local, bk.obj, m.objective(bk.W)))
    m.write_solution(out + "_polished.sol", bk.W, name, lam, "V3R1T4S lane C crossover chain-DP mix + descent (judge with pf_eval.py)")
    print("seconds %.1f" % (time.time() - t0))


if __name__ == "__main__":
    main()
