#!/usr/bin/env python3
"""Exact orbit set cover for C(v,k,t) under a permutation group given by generators (numpy, low memory).
k-set orbits by min-label propagation on colex ranks over the generators; CP-SAT weighted set cover over orbits.
API: solve(perms, v, k, t, cap, workers, hint=None) -> dict(status, best, bound, korb, torb, blocks)"""
import itertools, numpy as np
from math import comb
from ortools.sat.python import cp_model

MEMLIM = 350   # SCIP memory limit in MB (run budget: total < ~2 GB)
BIN = np.array([[comb(n, r) for r in range(9)] for n in range(65)], dtype=np.int64)

def colex_rank(S):  # S: (N,k) sorted ascending, int
    k = S.shape[1]; r = np.zeros(S.shape[0], dtype=np.int64)
    for i in range(k): r += BIN[S[:, i].astype(np.int64), i+1]
    return r

def all_sets_colex(v, k):
    S = np.fromiter(itertools.chain.from_iterable(itertools.combinations(range(v), k)), dtype=np.uint8).reshape(-1, k)
    r = colex_rank(S); out = np.empty_like(S); out[r] = S
    return out

def orbit_labels(S, perms, chunk=500000):
    N, k = S.shape; imgs = []
    for p in perms:
        P = np.asarray(p, dtype=np.uint8); im = np.empty(N, dtype=np.int64)
        for a in range(0, N, chunk):
            T = np.sort(P[S[a:a+chunk]], axis=1); im[a:a+chunk] = colex_rank(T)
        imgs.append(im.astype(np.int32 if N < 2**31 else np.int64))
    lab = np.arange(N, dtype=imgs[0].dtype)
    while True:
        new = lab.copy()
        for im in imgs:
            np.minimum(new, new[im], out=new)
        new = new[new]
        if np.array_equal(new, lab): break
        lab = new
    return lab

def orbit_labels_sym(S, perms):
    # inverse permutations make the propagation symmetric
    inv = []
    for p in perms:
        q = [0]*len(p)
        for i, x in enumerate(p): q[x] = i
        inv.append(q)
    return orbit_labels(S, list(perms) + inv)

def solve(perms, v, k, t, cap=60, workers=2, hint=None, maxorb=60000, log=None):
    S = all_sets_colex(v, k)
    lab = orbit_labels_sym(S, perms)
    reps, inv_idx, sizes = np.unique(lab, return_inverse=True, return_counts=True)
    R = len(reps)
    if R > maxorb: return dict(status='SKIPPED_TOO_MANY', korb=int(R))
    T = all_sets_colex(v, t); tl = orbit_labels_sym(T, perms)
    treps, tinv = np.unique(tl, return_inverse=True)
    pos = np.array(list(itertools.combinations(range(k), t)), dtype=np.int64)
    RS = S[reps].astype(np.int64)                      # (R,k) sorted
    sub = RS[:, pos]                                    # (R,C(k,t),t) sorted
    tr = colex_rank(sub.reshape(-1, t)).reshape(R, -1)
    tj = tinv[tr]                                       # t-orbit index per (rep, subset)
    md = cp_model.CpModel(); x = [md.NewBoolVar('') for _ in range(R)]
    cov = [[] for _ in range(len(treps))]
    for i in range(R):
        for j in set(tj[i].tolist()): cov[j].append(i)
    for l in cov: md.AddBoolOr([x[i] for i in l])
    md.Minimize(sum(int(sizes[i])*x[i] for i in range(R)))
    if hint is not None:   # hint = set of block bitmasks / or label set: list of k-set colex ranks
        hl = set(inv_idx[np.asarray(hint, dtype=np.int64)].tolist())
        for i in range(R): md.AddHint(x[i], 1 if i in hl else 0)
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = cap; sv.parameters.num_workers = workers
    st = sv.Solve(md)
    res = dict(status=sv.StatusName(st), korb=int(R), torb=int(len(treps)))
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        ch = np.array([i for i in range(R) if sv.Value(x[i])], dtype=np.int64)
        res['best'] = int(sizes[ch].sum()); res['bound'] = int(round(sv.BestObjectiveBound()))
        mask = np.isin(inv_idx, ch); res['blocks'] = (S[mask].astype(int) + 1).tolist()
        res['block_ranks'] = np.nonzero(mask)[0]
    return res

def check(blocks, v, k, t):
    bm = set()
    for b in blocks:
        assert len(b) == k and len(set(b)) == k
        for c in itertools.combinations(sorted(b), t): bm.add(c)
    return len(bm) == comb(v, t)

if __name__ == '__main__':
    # self-test: PSL(2,7) on 14+14+1 for C(29,5,3) must give a valid cover; cyclic Z7 on 7 points C(7,3,2)=7 (Fano)
    z7 = [tuple((i+1) % 7 for i in range(7))]
    r = solve(z7, 7, 3, 2, cap=10); print('Z7 C(7,3,2):', r['status'], r['best'], check(r['blocks'], 7, 3, 2))

def solve_mip(perms, v, k, t, cap=60, threads=1, maxorb=60000, solver_name='SCIP'):
    """Same orbit set cover, solved by a MIP solver (LP bound + branch and bound) via OR-tools pywraplp."""
    from ortools.linear_solver import pywraplp
    S = all_sets_colex(v, k); lab = orbit_labels_sym(S, perms)
    reps, inv_idx, sizes = np.unique(lab, return_inverse=True, return_counts=True); R = len(reps)
    if R > maxorb: return dict(status='SKIPPED_TOO_MANY', korb=int(R))
    T = all_sets_colex(v, t); tl = orbit_labels_sym(T, perms); treps, tinv = np.unique(tl, return_inverse=True)
    pos = np.array(list(itertools.combinations(range(k), t)), dtype=np.int64)
    tj = tinv[colex_rank(S[reps].astype(np.int64)[:, pos].reshape(-1, t)).reshape(R, -1)]
    m = pywraplp.Solver.CreateSolver(solver_name)
    x = [m.BoolVar(f'x{i}') for i in range(R)]
    cov = [[] for _ in range(len(treps))]
    for i in range(R):
        for j in set(tj[i].tolist()): cov[j].append(i)
    for l in cov: m.Add(sum(x[i] for i in l) >= 1)
    m.Minimize(sum(int(sizes[i])*x[i] for i in range(R)))
    m.SetTimeLimit(int(cap*1000)); m.SetNumThreads(threads)
    m.SetSolverSpecificParametersAsString(f'limits/memory = {MEMLIM}\n')
    st = m.Solve()
    name = {pywraplp.Solver.OPTIMAL:'OPTIMAL', pywraplp.Solver.FEASIBLE:'FEASIBLE'}.get(st, f'STATUS{st}')
    res = dict(status=name, korb=int(R), torb=int(len(treps)))
    if st in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        ch = np.array([i for i in range(R) if x[i].solution_value() > 0.5], dtype=np.int64)
        res['best'] = int(sizes[ch].sum()); res['bound'] = int(np.ceil(m.Objective().BestBound()-1e-6))
        mask = np.isin(inv_idx, ch); res['blocks'] = (S[mask].astype(int) + 1).tolist()
    return res
