"""MRCPSP engine, phase A (Andy, 2026-11-19): layers 1 and 2 of the dedicated solver.

Layer 1  mode_mix(I, ...): CP-SAT picks one mode per job that fits every non-renewable budget and minimises a lower-bound
         proxy T >= critical-path length and T * cap_r >= renewable work content of resource r (all with the chosen modes).
         Optional 'avoid' set forbids exact repeats; 'fix' keeps some jobs' modes.
Layer 2  sgs(...): serial schedule generation scheme (each job in list order at its earliest precedence- and
         resource-feasible time); fbi(...): forward-backward improvement (right-justify in decreasing finish order,
         left-justify in increasing start order, repeat while the makespan drops); biased random activity lists from
         latest finish times. Hot loops in numba.
Instance data come from mm.read(); every schedule a caller keeps must pass mm.check()."""
import numpy as np, numba as nb
from ortools.sat.python import cp_model


class Inst:
    """Array form of an mm.read() instance."""
    def __init__(self, I):
        self.I = I; n = I['n']; self.n = n
        self.nm = np.array([len(I['modes'][j]) for j in range(n)], np.int64); M = int(self.nm.max())
        R = len(I['Rcap']); N = len(I['Ncap']); self.R, self.N = R, N
        self.dur = np.zeros((n, M), np.int64); self.req = np.zeros((n, M, max(R, 1)), np.int64); self.nreq = np.zeros((n, M, max(N, 1)), np.int64)
        for j in range(n):
            for t, (d, r, q) in enumerate(I['modes'][j]):
                self.dur[j, t] = d; self.req[j, t, :R] = r; self.nreq[j, t, :N] = q
        self.cap = np.array(I['Rcap'] or [0], np.int64); self.ncap = np.array(I['Ncap'] or [0], np.int64)
        succ = [I['succ'][j] for j in range(n)]; pred = [[] for _ in range(n)]
        for j in range(n):
            for s in succ[j]: pred[s].append(j)
        self.pp, self.pi = _csr(pred); self.sp, self.si = _csr(succ)
        self.H = int(self.dur.max(axis=1).sum()) + 1


def _csr(lists):
    ptr = np.zeros(len(lists) + 1, np.int64); ptr[1:] = np.cumsum([len(x) for x in lists])
    idx = np.array([v for x in lists for v in x], np.int64) if ptr[-1] else np.zeros(0, np.int64)
    return ptr, idx


@nb.njit(cache=True)
def sgs(order, d, q, cap, pp, pi, H):
    """Serial SGS. order: activity list (each job after all its predecessors in pp/pi); d[j]: duration; q[j, r]: renewable
    demand. Returns start times (int64[n]). Infeasible inputs are the caller's responsibility."""
    n = len(order); R = len(cap); use = np.zeros((R, H), np.int64); st = np.zeros(n, np.int64); fin = np.zeros(n, np.int64)
    for k in range(n):
        j = order[k]; t = 0
        for a in range(pp[j], pp[j + 1]):
            if fin[pi[a]] > t: t = fin[pi[a]]
        dj = d[j]
        while True:
            ok = True
            for tt in range(t, t + dj):
                for r in range(R):
                    if use[r, tt] + q[j, r] > cap[r]:
                        ok = False; t = tt + 1; break
                if not ok: break
            if ok: break
        for tt in range(t, t + dj):
            for r in range(R): use[r, tt] += q[j, r]
        st[j] = t; fin[j] = t + dj
    return st


@nb.njit(cache=True)
def fbi(st, d, q, cap, pp, pi, sp, si, H, rounds):
    """Forward-backward improvement. Backward: schedule on the reversed network in decreasing order of finish time,
    then mirror; forward: schedule in increasing order of the mirrored starts. Keeps the best (shortest) schedule."""
    n = len(st); best = st.copy(); bm = 0
    for j in range(n):
        if st[j] + d[j] > bm: bm = st[j] + d[j]
    cur = st.copy()
    for _ in range(rounds):
        fin = cur + d
        ob = np.argsort(-fin, kind='mergesort')          # decreasing finish: a valid list for the reversed network
        rs = sgs(ob, d, q, cap, sp, si, H)               # reversed network: successors act as predecessors
        m = 0
        for j in range(n):
            if rs[j] + d[j] > m: m = rs[j] + d[j]
        bst = m - (rs + d)                               # mirrored back: a right-justified schedule of makespan m
        of = np.argsort(bst, kind='mergesort')
        cur = sgs(of, d, q, cap, pp, pi, H)
        cm = 0
        for j in range(n):
            if cur[j] + d[j] > cm: cm = cur[j] + d[j]
        if cm < bm:
            bm = cm; best = cur.copy()
        else:
            break
    return best, bm


@nb.njit(cache=True)
def biased_list(prio, pp, pi, sp, si, alpha, seed):
    """Random precedence-feasible activity list: among eligible jobs pick one with probability proportional to
    (max_prio - prio + 1) ** alpha (low prio first, e.g. latest finish time)."""
    np.random.seed(seed); n = len(prio); npred = np.zeros(n, np.int64)
    for j in range(n): npred[j] = pp[j + 1] - pp[j]
    elig = np.zeros(n, np.int64); ne = 0
    for j in range(n):
        if npred[j] == 0: elig[ne] = j; ne += 1
    out = np.zeros(n, np.int64); mx = prio.max()
    for k in range(n):
        tot = 0.0
        for e in range(ne): tot += (mx - prio[elig[e]] + 1.0) ** alpha
        u = np.random.random() * tot; acc = 0.0; pick = ne - 1
        for e in range(ne):
            acc += (mx - prio[elig[e]] + 1.0) ** alpha
            if acc >= u: pick = e; break
        j = elig[pick]; out[k] = j; elig[pick] = elig[ne - 1]; ne -= 1
        for a in range(sp[j], sp[j + 1]):
            s = si[a]; npred[s] -= 1
            if npred[s] == 0: elig[ne] = s; ne += 1
    return out


def lft(X, d):
    """Latest finish times (CPM backward pass with durations d, horizon = critical path length)."""
    n = X.n; ef = np.zeros(n, np.int64)
    for j in topo(X):
        ef[j] = d[j] + max([ef[X.pi[a]] for a in range(X.pp[j], X.pp[j + 1])], default=0)
    T = ef.max(); lf = np.full(n, T, np.int64)
    for j in reversed(topo(X)):
        for a in range(X.sp[j], X.sp[j + 1]):
            s = X.si[a]; lf[j] = min(lf[j], lf[s] - d[s])
    return lf


def topo(X):
    if getattr(X, '_topo', None) is None:
        indeg = np.diff(X.pp).copy(); q = [j for j in range(X.n) if indeg[j] == 0]; out = []
        while q:
            j = q.pop(); out.append(j)
            for a in range(X.sp[j], X.sp[j + 1]):
                s = X.si[a]; indeg[s] -= 1
                if indeg[s] == 0: q.append(s)
        X._topo = out
    return X._topo


def mode_mix(X, secs=5.0, workers=4, seed=1, avoid=(), fix=None):
    """Layer 1. Returns 1-based modes (np.int64[n]) and the proxy value, or (None, None) if no budget-feasible mix is found."""
    n = X.n; m = cp_model.CpModel(); x = {}
    for j in range(n):
        for t in range(X.nm[j]): x[j, t] = m.NewBoolVar('')
        m.AddExactlyOne([x[j, t] for t in range(X.nm[j])])
        if fix is not None and fix[j] > 0: m.Add(x[j, fix[j] - 1] == 1)
    for k in range(X.N):
        if X.ncap[k] or X.N:
            m.Add(sum(int(X.nreq[j, t, k]) * x[j, t] for j in range(n) for t in range(X.nm[j])) <= int(X.ncap[k]))
    dj = [sum(int(X.dur[j, t]) * x[j, t] for t in range(X.nm[j])) for j in range(n)]
    ef = [m.NewIntVar(0, X.H, '') for _ in range(n)]
    for j in range(n):
        m.Add(ef[j] >= dj[j])
        for a in range(X.pp[j], X.pp[j + 1]): m.Add(ef[j] >= ef[X.pi[a]] + dj[j])
    T = m.NewIntVar(0, X.H, ''); m.Add(T >= ef[n - 1])
    for r in range(X.R):
        if X.cap[r] > 0:
            m.Add(T * int(X.cap[r]) >= sum(int(X.dur[j, t] * X.req[j, t, r]) * x[j, t] for j in range(n) for t in range(X.nm[j])))
    for prev in avoid:
        m.AddBoolOr([x[j, t].Not() for j in range(n) for t in range(X.nm[j]) if prev[j] == t + 1])
    m.Minimize(T)
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = secs; sv.parameters.num_workers = workers; sv.parameters.random_seed = seed
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return None, None
    return np.array([[sv.Value(x[j, t]) for t in range(X.nm[j])].index(1) + 1 for j in range(n)], np.int64), int(sv.ObjectiveValue())


def realise(X, modes):
    """Durations and renewable demands of the chosen modes."""
    idx = modes - 1; r = np.arange(X.n)
    return X.dur[r, idx].copy(), X.req[r, idx, :].copy()


def multistart(X, modes, n_lists, seed=0, alpha=2.0, rounds=20):
    """Layer 2 for fixed modes: n_lists biased-random activity lists, SGS, FBI. Returns (best makespan, best starts)."""
    d, q = realise(X, modes); prio = lft(X, d); best = None
    for k in range(n_lists):
        order = biased_list(prio, X.pp, X.pi, X.sp, X.si, alpha, seed * 1000003 + k)
        st = sgs(order, d, q, X.cap, X.pp, X.pi, X.H)
        st, mk = fbi(st, d, q, X.cap, X.pp, X.pi, X.sp, X.si, X.H, rounds)
        if best is None or mk < best[0]: best = (int(mk), st)
    return best
