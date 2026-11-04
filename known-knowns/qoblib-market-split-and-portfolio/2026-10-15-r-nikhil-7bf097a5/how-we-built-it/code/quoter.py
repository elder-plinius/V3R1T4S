"""quoter lens: one local-search 'book' on a QOBLIB 06-portfolio cell (net-position space, exact integer deltas).

Moves (all over a block of consecutive periods [t1, t2] inside t_beg..t_end-1; t_end stays flat):
  single  w[t, i] += a            for t in block, a in {-3..3}\\{0}
  pair    w[t, i] += a, w[t, j] += b   for t in block, a, b in {-2, -1, 1, 2}, i != j (hedges, swaps, rotations)
Steepest descent over all moves, then iterated local search: kick with k random net-preserving pair-block moves,
descend, accept with a threshold, keep the best. Writes a checkpoint .sol whenever the best improves and logs the
mark-to-market (best objective vs time) for the book.

Usage: quoter.py CODE_DIR INSTANCE_DIR B LAMBDA INSTANCE_NAME START(sol|empty) SEED KICK SECONDS OUT_PREFIX
"""
import sys
import time

import numpy as np

sys.path.insert(0, sys.argv[1])
from pfmodel import Model  # noqa: E402

SINGLE = [-3, -2, -1, 1, 2, 3]
PAIR = [-2, -1, 1, 2]


class Book:
    def __init__(self, m, W):
        self.m = m
        self.L = m.nT - 1
        self.W = W.astype(np.int64).copy()
        self.W[self.L] = 0
        self.G = np.einsum("tij,tj->ti", m.Qs, self.W)
        self.P = np.zeros((m.nT + 1, m.n, m.n), dtype=np.int64)
        for k in range(m.nT):
            self.P[k + 1] = self.P[k] + m.Qs[k]
        self.obj = m.objective(self.W)
        self.blocks = [(a, b) for a in range(self.L) for b in range(a, self.L)]

    def block_single(self, t1, t2, a):
        m, W = self.m, self.W
        seg = W[t1:t2 + 1]
        nv = seg + a
        valid = np.all(np.abs(nv) <= 3, axis=0)
        dv = (a * self.G[t1:t2 + 1] + a * a * m.diag[t1:t2 + 1] + a * m.lin[t1:t2 + 1]
              + m.s[t1:t2 + 1] * (np.maximum(-nv, 0) - np.maximum(-seg, 0))).sum(axis=0)
        if t1 == 0:
            dv = dv + m.d[0] * (np.abs(W[0] + a) - np.abs(W[0]))
        else:
            dv = dv + m.d[t1] * (np.abs(W[t1] + a - W[t1 - 1]) - np.abs(W[t1] - W[t1 - 1]))
        if t2 + 1 <= self.L - 1:
            dv = dv + m.d[t2 + 1] * (np.abs(W[t2 + 1] - W[t2] - a) - np.abs(W[t2 + 1] - W[t2]))
        bc = np.abs(nv) - np.abs(seg)
        return dv, valid, bc

    def best_move(self):
        m = self.m
        net = self.W.sum(axis=1)
        slack = m.B - np.abs(self.W).sum(axis=1)
        best = (0, None)
        big = np.iinfo(np.int64).max // 4
        for (t1, t2) in self.blocks:
            S = {}
            for a in SINGLE:
                dv, valid, bc = self.block_single(t1, t2, a)
                S[a] = (dv, valid, bc)
                ok = valid & np.all(bc <= slack[t1:t2 + 1, None], axis=0)
                if not (np.all(net[t1:t2 + 1] + a >= -5) and np.all(net[t1:t2 + 1] + a <= 10)):
                    continue
                cand = np.where(ok, dv, big)
                i = int(np.argmin(cand))
                if cand[i] < best[0]:
                    best = (int(cand[i]), ("single", t1, t2, i, a))
            Qb = self.P[t2 + 1] - self.P[t1]
            sl = slack[t1:t2 + 1]
            for a in PAIR:
                dva, va, bca = S[a]
                for b in PAIR:
                    nn = net[t1:t2 + 1] + a + b
                    if np.any(nn < -5) or np.any(nn > 10):
                        continue
                    dvb, vb, bcb = S[b]
                    M = dva[:, None] + dvb[None, :] + (a * b) * Qb
                    okm = va[:, None] & vb[None, :]
                    if sl.min() < 4:
                        for k in range(len(sl)):
                            okm &= (bca[k][:, None] + bcb[k][None, :]) <= sl[k]
                    np.fill_diagonal(okm, False)
                    M = np.where(okm, M, big)
                    f = int(np.argmin(M))
                    i, j = divmod(f, m.n)
                    if M[i, j] < best[0]:
                        best = (int(M[i, j]), ("pair", t1, t2, i, j, a, b))
        return best

    def apply(self, mv):
        m = self.m
        if mv[0] == "single":
            _, t1, t2, i, a = mv
            parts = [(i, a)]
        else:
            _, t1, t2, i, j, a, b = mv
            parts = [(i, a), (j, b)]
        for (i, a) in parts:
            for t in range(t1, t2 + 1):
                self.W[t, i] += a
                self.G[t] += m.Qs[t][:, i] * a

    def descend(self, deadline):
        steps = 0
        while time.time() < deadline:
            d, mv = self.best_move()
            if mv is None:
                return steps, True
            self.apply(mv)
            self.obj += d
            steps += 1
        return steps, False

    def kick(self, rng, k):
        m = self.m
        done = 0
        tries = 0
        while done < k and tries < 1000:
            tries += 1
            t1 = int(rng.integers(0, self.L))
            t2 = int(min(self.L - 1, t1 + rng.integers(0, 4)))
            i, j = rng.choice(m.n, 2, replace=False)
            a = int(rng.choice([-1, 1]))
            seg = self.W[t1:t2 + 1]
            ni, nj = seg[:, i] + a, seg[:, j] - a
            if np.any(np.abs(ni) > 3) or np.any(np.abs(nj) > 3):
                continue
            bc = (np.abs(ni) - np.abs(seg[:, i])) + (np.abs(nj) - np.abs(seg[:, j]))
            slack = m.B - np.abs(seg).sum(axis=1)
            if np.any(bc > slack):
                continue
            self.apply(("pair", t1, t2, int(i), int(j), a, -a))
            done += 1
        self.obj = m.objective(self.W)
        return done

    def resync(self):
        self.G = np.einsum("tij,tj->ti", self.m.Qs, self.W)
        self.obj = self.m.objective(self.W)


def main():
    (code, inst, B, lam, name, start, seed, kick, secs, out) = sys.argv[1:11]
    t_start = time.time()
    deadline = t_start + float(secs)
    m = Model(inst, int(B), lam)
    if start == "empty":
        W = np.zeros((m.nT, m.n), dtype=np.int64)
    else:
        W = m.read_solution(start)
    rng = np.random.default_rng(int(seed))
    bk = Book(m, W)
    log = open(out + ".log", "w")

    def mark(msg):
        log.write("%7.1fs %s\n" % (time.time() - t_start, msg))
        log.flush()

    mark("start=%s obj=%d feasible=%s" % (start, bk.obj, m.feasible(bk.W)))
    steps, local = bk.descend(deadline)
    true_obj = m.objective(bk.W)
    mark("descent steps=%d local_opt=%s obj=%d recomputed=%d feasible=%s" % (steps, local, bk.obj, true_obj, m.feasible(bk.W)))
    assert true_obj == bk.obj, "incremental objective drifted"
    best_W, best = bk.W.copy(), bk.obj
    m.write_solution(out + "_best.sol", best_W, name, lam, "V3R1T4S lane C quoter book (search output; judge with pf_eval.py)")
    cur_W, cur = bk.W.copy(), bk.obj
    it = 0
    thresh = 2000.0
    while time.time() < deadline:
        it += 1
        bk.W = cur_W.copy()
        bk.resync()
        k = int(kick) + int(rng.integers(0, int(kick) + 1))
        bk.kick(rng, k)
        bk.resync()
        steps, local = bk.descend(deadline)
        if not local:
            break
        if bk.obj != m.objective(bk.W) or not m.feasible(bk.W):
            mark("ERROR drift or infeasible at it=%d" % it)
            bk.resync()
            continue
        if bk.obj < best:
            best, best_W = bk.obj, bk.W.copy()
            m.write_solution(out + "_best.sol", best_W, name, lam, "V3R1T4S lane C quoter book (search output; judge with pf_eval.py)")
            mark("it=%d NEW BEST %d (kick %d, %d steps)" % (it, best, k, steps))
        if bk.obj < cur + thresh:
            cur_W, cur = bk.W.copy(), bk.obj
        thresh *= 0.995
        if it % 10 == 0:
            mark("it=%d cur=%d best=%d thresh=%.0f" % (it, cur, best, thresh))
    mark("END best=%d its=%d" % (best, it))
    print("best", best)


if __name__ == "__main__":
    main()
