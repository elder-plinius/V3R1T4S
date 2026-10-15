"""crossover lens, per-period books: ILS on one period's portfolio with both neighbours fixed, collecting a pool of
distinct local optima for the chain DP (pool_dp2.py).

Moves are quoter2's single and pair moves restricted to the block (k, k); deltas are exact and include the trading
terms to the fixed neighbours (k-1 and k+1). Kicks are random net-preserving pair moves inside period k. Every local
optimum reached is stored (distinct rows only) with its period cost; the best POOL rows are saved to OUT.npz.

Usage: period_ils.py QUOTER_CODE_DIR INSTANCE_DIR B LAMBDA BASE_SOL PERIOD SEED KICK SECONDS POOL OUT_PREFIX
"""
import sys
import time

import numpy as np

sys.path.insert(0, sys.argv[1])
from pfmodel import Model  # noqa: E402
from quoter2 import Book  # noqa: E402


def kick_period(bk, rng, k, n_moves):
    m = bk.m
    done, tries = 0, 0
    while done < n_moves and tries < 500:
        tries += 1
        i, j = rng.choice(m.n, 2, replace=False)
        a = int(rng.choice([-1, 1]))
        wi, wj = bk.W[k, i] + a, bk.W[k, j] - a
        if abs(wi) > 3 or abs(wj) > 3:
            continue
        bc = abs(wi) - abs(bk.W[k, i]) + abs(wj) - abs(bk.W[k, j])
        if np.abs(bk.W[k]).sum() + bc > m.B:
            continue
        bk.apply(("pair", k, k, int(i), int(j), a, -a))
        done += 1


def main():
    code, inst, B, lam, base, k, seed, kick, secs, pool_n, out = sys.argv[1:12]
    k, pool_n = int(k), int(pool_n)
    t0 = time.time()
    deadline = t0 + float(secs)
    m = Model(inst, int(B), lam)
    rng = np.random.default_rng(int(seed))
    W0 = m.read_solution(base)
    bk = Book(m, W0)
    bk.blocks = [(k, k)]
    base_obj = bk.obj
    bk.descend(deadline)
    pool = {}

    def record():
        key = bk.W[k].tobytes()
        if key not in pool:
            pool[key] = (bk.obj, bk.W[k].copy())

    record()
    best, best_row = bk.obj, bk.W[k].copy()
    cur, cur_row = bk.obj, bk.W[k].copy()
    it, thresh, since = 0, 1500.0, 0
    while time.time() < deadline:
        it += 1
        since += 1
        if since > 150:
            cur, cur_row, since, thresh = best, best_row.copy(), 0, 1500.0
        bk.W[k] = cur_row
        bk.resync()
        kick_period(bk, rng, k, int(kick) + int(rng.integers(0, int(kick) + 1)))
        bk.resync()
        bk.descend(deadline)
        record()
        if bk.obj < best:
            best, best_row, since = bk.obj, bk.W[k].copy(), 0
        if bk.obj < cur + thresh:
            cur, cur_row = bk.obj, bk.W[k].copy()
        thresh *= 0.997
    W = W0.copy()
    W[k] = best_row
    assert m.objective(W) == best, "period objective drift"
    items = sorted(pool.values(), key=lambda x: x[0])[:pool_n]
    np.savez(out + ".npz", rows=np.array([r for _, r in items]), objs=np.array([o for o, _ in items]), period=k)
    print("period %d: base %d -> best %d (gain %d); its=%d distinct optima=%d saved=%d; %.0fs" % (
        k, base_obj, best, base_obj - best, it, len(pool), len(items), time.time() - t0))


if __name__ == "__main__":
    main()
