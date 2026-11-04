"""quoter lens v2: same moves and exact integer deltas as quoter.py, with a per-block move cache.

A block (t1, t2) move's delta depends only on W[t1-1 .. t2+1], G[t1 .. t2] and the slack/net of periods t1..t2, so
after a move that changes periods [a, b] only blocks with [t1-1, t2+1] meeting [a, b] are re-evaluated. ILS as in
quoter.py (random net-preserving pair-block kicks, threshold acceptance), plus a restart from the book's best after
`stall` non-improving iterations. Checkpoints the best .sol on every improvement and logs marks every 20 iterations.

Usage: quoter2.py CODE_DIR INSTANCE_DIR B LAMBDA INSTANCE_NAME START SEED KICK SECONDS OUT_PREFIX [STALL] [THRESH0]
"""
import sys
import time

import numpy as np

sys.path.insert(0, sys.argv[1])
from pfmodel import Model  # noqa: E402
from quoter import Book as Book1  # noqa: E402


class Book(Book1):
    def __init__(self, m, W):
        super().__init__(m, W)
        self.cache = {}

    def eval_block(self, t1, t2, net, slack):
        m = self.m
        big = np.iinfo(np.int64).max // 4
        best = (0, None)
        S = {}
        for a in (-3, -2, -1, 1, 2, 3):
            dv, valid, bc = self.block_single(t1, t2, a)
            S[a] = (dv, valid, bc)
            if not (np.all(net[t1:t2 + 1] + a >= -5) and np.all(net[t1:t2 + 1] + a <= 10)):
                continue
            ok = valid & np.all(bc <= slack[t1:t2 + 1, None], axis=0)
            cand = np.where(ok, dv, big)
            i = int(np.argmin(cand))
            if cand[i] < best[0]:
                best = (int(cand[i]), ("single", t1, t2, i, a))
        Qb = self.P[t2 + 1] - self.P[t1]
        sl = slack[t1:t2 + 1]
        for a in (-2, -1, 1, 2):
            dva, va, bca = S[a]
            for b in (-2, -1, 1, 2):
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

    def best_move(self):
        net = self.W.sum(axis=1)
        slack = self.m.B - np.abs(self.W).sum(axis=1)
        best = (0, None)
        for blk in self.blocks:
            if blk not in self.cache:
                self.cache[blk] = self.eval_block(blk[0], blk[1], net, slack)
            c = self.cache[blk]
            if c[1] is not None and c[0] < best[0]:
                best = c
        return best

    def apply(self, mv):
        super().apply(mv)
        a, b = mv[1], mv[2]
        for blk in list(self.cache):
            if blk[0] - 1 <= b and blk[1] + 1 >= a:
                del self.cache[blk]

    def resync(self):
        super().resync()
        self.cache = {}


def main():
    (code, inst, B, lam, name, start, seed, kick, secs, out) = sys.argv[1:11]
    stall = int(sys.argv[11]) if len(sys.argv) > 11 else 60
    thresh0 = float(sys.argv[12]) if len(sys.argv) > 12 else 2000.0
    t_start = time.time()
    deadline = t_start + float(secs)
    m = Model(inst, int(B), lam)
    W = np.zeros((m.nT, m.n), dtype=np.int64) if start == "empty" else m.read_solution(start)
    rng = np.random.default_rng(int(seed))
    bk = Book(m, W)
    log = open(out + ".log", "w")

    def mark(msg):
        log.write("%7.1fs %s\n" % (time.time() - t_start, msg))
        log.flush()

    note = "V3R1T4S lane C quoter2 book (search output; judge with pf_eval.py)"
    mark("start=%s obj=%d feasible=%s" % (start, bk.obj, m.feasible(bk.W)))
    steps, local = bk.descend(deadline)
    assert m.objective(bk.W) == bk.obj, "incremental objective drifted"
    mark("descent steps=%d obj=%d" % (steps, bk.obj))
    best_W, best = bk.W.copy(), bk.obj
    m.write_solution(out + "_best.sol", best_W, name, lam, note)
    cur_W, cur = bk.W.copy(), bk.obj
    it, since = 0, 0
    thresh = thresh0
    while time.time() < deadline:
        it += 1
        since += 1
        if since > stall:
            cur_W, cur, since = best_W.copy(), best, 0
            thresh = thresh0
            mark("it=%d restart from best %d" % (it, best))
        bk.W = cur_W.copy()
        bk.resync()
        k = int(kick) + int(rng.integers(0, int(kick) + 1))
        bk.kick(rng, k)
        bk.resync()
        steps, local = bk.descend(deadline)
        if not local:
            break
        true_obj = m.objective(bk.W)
        if bk.obj != true_obj or not m.feasible(bk.W):
            mark("ERROR drift (%d vs %d) or infeasible at it=%d" % (bk.obj, true_obj, it))
            bk.resync()
            continue
        if bk.obj < best:
            best, best_W, since = bk.obj, bk.W.copy(), 0
            m.write_solution(out + "_best.sol", best_W, name, lam, note)
            mark("it=%d NEW BEST %d (kick %d, %d steps)" % (it, best, k, steps))
        if bk.obj < cur + thresh:
            cur_W, cur = bk.W.copy(), bk.obj
        thresh *= 0.995
        if it % 20 == 0:
            mark("it=%d cur=%d best=%d thresh=%.0f" % (it, cur, best, thresh))
    mark("END best=%d its=%d" % (best, it))
    print("best", best)


if __name__ == "__main__":
    main()
