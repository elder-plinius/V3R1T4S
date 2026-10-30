"""Frame tools for the extender lens: sumset complements K = F_3^n \\ -(B1+B2), linear images, exact max cap in K."""
import numpy as np, sys, time
import os
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # the how-we-built-it/ folder

def load(path, n):
    pts = []
    for line in open(path):
        s = line.split('#')[0].replace(',', ' ').split()
        if not s: continue
        d = ''.join(s); assert len(d) == n
        pts.append([int(c) for c in d])
    return np.array(pts, dtype=np.int64)

def enc(V):
    n = V.shape[1]
    return (V % 3) @ (3 ** np.arange(n))

def dec(codes, n):
    codes = np.asarray(codes)
    return np.stack([(codes // 3**k) % 3 for k in range(n)], axis=1)

def K_of(V1, V2):
    """boolean mask over F_3^n of points NOT of the form -(b1+b2)"""
    n = V1.shape[1]
    P = 3 ** np.arange(n)
    c1 = (V1 @ P); c2 = (V2 @ P)
    # third point code via digit sums: precompute per-digit
    S = (-(V1[:, None, :] + V2[None, :, :])) % 3
    z = (S.reshape(-1, n) @ P)
    hit = np.zeros(3**n, bool); hit[z] = True
    return ~hit

def is_cap_codes(codes, n):
    codes = np.unique(np.asarray(codes))
    V = dec(codes, n)
    M = np.zeros(3**n, bool); M[codes] = True
    i, j = np.triu_indices(len(codes), 1)
    z = enc((-(V[i] + V[j])) % 3)
    return not M[z].any()

def maxcap_in(cand_codes, n, time_limit=60, workers=1, lb=None, log=False, hint=None):
    """exact max cap inside the candidate set (CP-SAT)."""
    from ortools.sat.python import cp_model
    cand = np.asarray(sorted(int(c) for c in cand_codes))
    N = 3**n
    idx = -np.ones(N, np.int64); idx[cand] = np.arange(len(cand))
    V = dec(cand, n)
    m = cp_model.CpModel()
    v = [m.NewBoolVar('') for _ in cand]
    if len(cand) > 2:
        a, b = np.triu_indices(len(cand), 1)
        w = enc((-(V[a] + V[b])) % 3)
        k = idx[w]
        sel = k > b
        for p, q, r in zip(a[sel], b[sel], k[sel]):
            m.AddBoolOr([v[p].Not(), v[q].Not(), v[r].Not()])
    m.Maximize(sum(v))
    if lb is not None:
        m.Add(sum(v) >= lb)
    if hint is not None:
        for t, c in enumerate(cand): m.AddHint(v[t], int(c) in hint)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = time_limit; s.parameters.num_workers = workers
    s.parameters.log_search_progress = log
    st = s.Solve(m)
    chosen = [int(cand[t]) for t in range(len(cand)) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) and s.Value(v[t])]
    return s.StatusName(st), len(chosen), s.BestObjectiveBound(), chosen

def write_pts(path, codes, n):
    V = dec(np.unique(np.asarray(codes)), n)
    with open(path, 'w') as f:
        for row in V:
            f.write(''.join(str(int(x)) for x in row) + '\n')
