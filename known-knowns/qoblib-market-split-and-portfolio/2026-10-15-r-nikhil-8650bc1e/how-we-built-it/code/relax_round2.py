"""lattice-smuggler lens: zero-risk hedges live in the null space of each period's risk matrix (rank 29 of 200).

1. Continuous multi-period convex QP (HiGHS): w = wp - wm in [-3, 3], risk = ||F_k' w_k||^2 with F_k from the top-29
   eigenpairs of sym(Q_k), exact linear costs (return, cash, short, L1 trading), budget and net rows per period.
2. Residual-aware rounding (nearest-plane style on the identity basis): coordinates in order of decreasing ||F_k[i]||,
   each rounded down or up to keep the 29-dim risk residual F_k'(w - w*) small, with budget/net kept feasible and a
   trading penalty toward the previous period's rounded value. Several randomised orders.
3. Exact polish with the quoter's single/pair block descent (pfmodel integer tables), then a short ILS.
Writes the best integer solution found; the judge is checker/pf_eval.py.

Usage: relax_round.py QUOTER_CODE_DIR INSTANCE_DIR B LAMBDA INSTANCE_NAME SAMPLES SECONDS OUT_PREFIX
"""
import os
import sys
import time

import highspy
import numpy as np

sys.path.insert(0, sys.argv[1])
from pfmodel import Model  # noqa: E402
from quoter import Book  # noqa: E402

R = 29  # overwritten per instance in main(): number of eigenvalues above 50


def factors(m, K):
    F = []
    for k in range(K):
        S = (m.Q[k] + m.Q[k].T) / 2.0
        ev, V = np.linalg.eigh(S)
        F.append(V[:, -R:] * np.sqrt(np.maximum(ev[-R:], 0)))
    return F


def solve_qp(m, F, K):
    n = m.n
    nwp, nwm, na, nz = K * n, K * n, K * n, K * R
    bwp, bwm, ba, bz = 0, nwp, nwp + nwm, nwp + nwm + na
    ncol = bz + nz
    cost = np.zeros(ncol)
    lo = np.zeros(ncol)
    hi = np.zeros(ncol)
    for k in range(K):
        cost[bwp + k * n: bwp + (k + 1) * n] = m.lin[k]
        cost[bwm + k * n: bwm + (k + 1) * n] = -m.lin[k] + m.s[k]
        cost[ba + k * n: ba + (k + 1) * n] = m.d[k]
    hi[bwp:bwp + nwp] = 3
    hi[bwm:bwm + nwm] = 3
    hi[ba:ba + na] = highspy.kHighsInf
    lo[bz:] = -highspy.kHighsInf
    hi[bz:] = highspy.kHighsInf
    cols = [[] for _ in range(ncol)]
    rlo, rhi = [], []

    def row(entries, l, u):
        r = len(rlo)
        for c, v in entries:
            cols[c].append((r, v))
        rlo.append(l)
        rhi.append(u)

    inf = highspy.kHighsInf
    for k in range(K):
        for j in range(R):
            e = [(bz + k * R + j, 1.0)]
            for i in range(n):
                f = F[k][i, j]
                e.append((bwp + k * n + i, -f))
                e.append((bwm + k * n + i, f))
            row(e, 0.0, 0.0)
        for i in range(n):
            a, p, q = ba + k * n + i, bwp + k * n + i, bwm + k * n + i
            if k == 0:
                row([(a, 1.0), (p, -1.0), (q, 1.0)], 0.0, inf)
                row([(a, 1.0), (p, 1.0), (q, -1.0)], 0.0, inf)
            else:
                p0, q0 = bwp + (k - 1) * n + i, bwm + (k - 1) * n + i
                row([(a, 1.0), (p, -1.0), (q, 1.0), (p0, 1.0), (q0, -1.0)], 0.0, inf)
                row([(a, 1.0), (p, 1.0), (q, -1.0), (p0, -1.0), (q0, 1.0)], 0.0, inf)
        row([(bwp + k * n + i, 1.0) for i in range(n)] + [(bwm + k * n + i, 1.0) for i in range(n)], -inf, float(m.B))
        row([(bwp + k * n + i, 1.0) for i in range(n)] + [(bwm + k * n + i, -1.0) for i in range(n)], -5.0, 10.0)
    start, index, value = [0], [], []
    for c in range(ncol):
        for r, v in cols[c]:
            index.append(r)
            value.append(v)
        start.append(len(index))
    lp = highspy.HighsLp()
    lp.num_col_ = ncol
    lp.num_row_ = len(rlo)
    lp.col_cost_ = cost
    lp.col_lower_ = lo
    lp.col_upper_ = hi
    lp.row_lower_ = np.array(rlo)
    lp.row_upper_ = np.array(rhi)
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = np.array(start, dtype=np.int32)
    lp.a_matrix_.index_ = np.array(index, dtype=np.int32)
    lp.a_matrix_.value_ = np.array(value)
    hs = highspy.HighsHessian()
    hs.dim_ = ncol
    hs.format_ = highspy.HessianFormat.kTriangular
    hstart, hindex, hvalue = [0], [], []
    for c in range(ncol):
        if c >= bz:
            hindex.append(c)
            hvalue.append(2.0)
        hstart.append(len(hindex))
    hs.start_ = np.array(hstart, dtype=np.int32)
    hs.index_ = np.array(hindex, dtype=np.int32)
    hs.value_ = np.array(hvalue)
    model = highspy.HighsModel()
    model.lp_ = lp
    model.hessian_ = hs
    h = highspy.Highs()
    h.setOptionValue("output_flag", False)
    h.setOptionValue("threads", 1)
    h.passModel(model)
    h.run()
    status = h.modelStatusToString(h.getModelStatus())
    x = np.array(h.getSolution().col_value)
    obj = h.getInfo().objective_function_value
    Wc = np.zeros((m.nT, n))
    for k in range(K):
        Wc[k] = x[bwp + k * n: bwp + (k + 1) * n] - x[bwm + k * n: bwm + (k + 1) * n]
    return status, obj - 100 * m.nT, Wc


def round_residual(m, F, Wc, K, rng, mu):
    n = m.n
    W = np.zeros((m.nT, n), dtype=np.int64)
    for k in range(K):
        w = Wc[k]
        lo = np.floor(w + 1e-9).astype(np.int64)
        frac = w - lo
        W[k] = lo
        fr = np.nonzero(frac > 1e-6)[0]
        rho = F[k].T @ (lo - w)
        norms = np.linalg.norm(F[k][fr], axis=1)
        order = fr[np.argsort(-norms + rng.normal(0, 0.15, len(fr)) * norms)]
        for i in order:
            best = None
            for c in (lo[i], lo[i] + 1):
                W[k, i] = c
                if np.abs(W[k]).sum() > m.B or not (-5 <= W[k].sum() <= 10 + 3 * len(order)):
                    continue
                r2 = rho + F[k][i] * (c - w[i])
                tr = 0 if k == 0 else m.d[k, i] * abs(c - W[k - 1, i])
                sc = float(r2 @ r2) + mu * tr + m.lin[k, i] * c
                if best is None or sc < best[0]:
                    best = (sc, c, r2)
            if best is None:
                W[k, i] = lo[i] if abs(lo[i]) <= abs(lo[i] + 1) else lo[i] + 1
                rho = rho + F[k][i] * (W[k, i] - w[i])
            else:
                W[k, i] = best[1]
                rho = best[2]
        # repair net and budget if needed (move toward zero the cheapest coordinates)
        while W[k].sum() > 10:
            i = int(np.argmax(np.where(W[k] > 0, -m.lin[k] * 0 + rng.random(n), -1)))
            W[k, i] -= 1
        while W[k].sum() < -5:
            i = int(np.argmax(np.where(W[k] < 0, rng.random(n), -1)))
            W[k, i] += 1
        while np.abs(W[k]).sum() > m.B:
            i = int(np.argmax(np.where(W[k] != 0, rng.random(n), -1)))
            W[k, i] -= np.sign(W[k, i])
    W = np.clip(W, -3, 3)
    return W


def main():
    code, inst, B, lam, name, samples, secs, out = sys.argv[1:9]
    t0 = time.time()
    deadline = t0 + float(secs)
    m = Model(inst, int(B), lam)
    K = m.nT - 1
    global R
    ev0 = np.linalg.eigvalsh((m.Q[0] + m.Q[0].T) / 2.0)
    R = int((ev0 > 50).sum())
    F = factors(m, K)
    log = open(out + ".log", "w")

    def mark(s):
        log.write("%7.1fs %s\n" % (time.time() - t0, s))
        log.flush()
        print(s, flush=True)

    status, cobj, Wc = solve_qp(m, F, K)
    mark("rank used R=%d" % R)
    mark("QP status=%s continuous objective (incl. cash constant) = %.1f" % (status, cobj))
    mark("continuous |w|_1 per period: %s" % np.round(np.abs(Wc).sum(axis=1), 2).tolist())
    np.save(out + "_Wc.npy", Wc)
    rng = np.random.default_rng(int(os.environ.get("RR_SEED", "7")))
    best, bestW = None, None
    for s in range(int(samples)):
        if time.time() > deadline:
            break
        mu = [0.0, 1.0, 5.0][s % 3]
        W = round_residual(m, F, Wc, K, rng, mu)
        feas = m.feasible(W)
        o0 = m.objective(W) if feas else None
        bk = Book(m, W)
        steps, local = bk.descend(deadline)
        o1 = m.objective(bk.W)
        ok = m.feasible(bk.W)
        mark("sample %d mu=%.0f rounded obj=%s feasible=%s -> descent %d steps obj=%d feasible=%s" % (s, mu, o0, feas, steps, o1, ok))
        if ok and (best is None or o1 < best):
            best, bestW = o1, bk.W.copy()
            m.write_solution(out + "_best.sol", bestW, name, lam, "V3R1T4S lane C lattice-smuggler (search output; judge with pf_eval.py)")
            mark("NEW BEST %d" % best)
    mark("END best=%s" % best)


if __name__ == "__main__":
    main()
