"""Search for a domatic 19-partition of Q_11 (lower-bound attempt; any output grid is re-checked by check.py).
Necessary structure (see certificate): 2*t5 + t6 >= 12 with t5 <= 1 (the two 5-sets intersect).
Loop: (1) HiGHS picks a family P of disjoint 5/6-sets (exact lists) with weight >= 12, different from previous ones
(no-good cut on the exact family); (2) EnumDomSub enumerates ALL dominating 7-sets (and 8-sets if room) inside the
remaining squares; (3) HiGHS maximises the number of disjoint remaining sets; success if |P| + that >= 19.
Usage: python drive19.py sets5 sets6 enumsub.exe workdir max_iters time_budget_s
"""
import sys, os, subprocess, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

n, N, K = 11, 121, 19
f5, f6, exe, wd, iters, budget = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), float(sys.argv[6])
S5 = [tuple(map(int, l.split())) for l in open(f5) if l.strip()]
S6 = [tuple(map(int, l.split())) for l in open(f6) if l.strip()]
base = [(S, 2) for S in S5] + [(S, 1) for S in S6]
cuts = []
t0 = time.time()


def pack(sets, weights, extra_rows=(), lb_weight=None, tl=30):
    M = lil_matrix((N + len(extra_rows) + (1 if lb_weight else 0), len(sets)))
    lo = [-np.inf] * N; hi = [1] * N
    for j, S in enumerate(sets):
        for v in S:
            M[v, j] = 1
    r = N
    for cut in extra_rows:            # no-good: sum_{j in cut} x_j <= |cut| - 1
        for j in cut:
            M[r, j] = 1
        lo.append(-np.inf); hi.append(len(cut) - 1); r += 1
    if lb_weight:
        for j, w in enumerate(weights):
            M[r, j] = w
        lo.append(lb_weight); hi.append(np.inf)
    rng = np.random.default_rng(len(extra_rows))
    c = -(np.array(weights, float) + 0.01 * rng.random(len(sets)))   # random tie-break for diversity
    res = milp(c=c, constraints=LinearConstraint(M.tocsr(), lo, hi), integrality=np.ones(len(sets)),
               bounds=Bounds(0, 1), options={'time_limit': tl, 'disp': False})
    if res.x is None:
        return None
    return [j for j in range(len(sets)) if res.x[j] > 0.5]


for it in range(iters):
    if time.time() - t0 > budget:
        print('budget reached'); break
    sel = pack([S for S, _ in base], [w for _, w in base], cuts, lb_weight=12, tl=8)
    if sel is None:
        print('no further family with weight >= 12'); break
    cuts.append(sel)
    P = [base[j][0] for j in sel]
    used = {v for S in P for v in S}
    rest = [v for v in range(N) if v not in used]
    need = K - len(P)
    room = len(rest) - 7 * need          # squares available beyond all-7 parts
    allowed = os.path.join(wd, 'allowed.txt')
    open(allowed, 'w').write(' '.join(map(str, rest)) + '\n')
    cand = []
    for m in [7] + ([8] if room >= 1 else []):
        outp = os.path.join(wd, 'sub-m%d.txt' % m)
        subprocess.run([exe, str(n), 'dom', str(m), outp, '1', allowed], check=True, capture_output=True)
        cand += [tuple(map(int, l.split())) for l in open(outp) if l.strip()]
    # also 6-sets inside the remainder (exact list)
    cand += [S for S in S6 if not (set(S) & used)]
    got = pack(cand, [1] * len(cand)) if cand else []
    total = len(P) + (len(got) if got else 0)
    print('iter %d: |P|=%d (weight %d) rest=%d need=%d room=%d candidates=%d -> total %d  [%.0fs]' %
          (it, len(P), sum(base[j][1] for j in sel), len(rest), need, room, len(cand), total, time.time() - t0), flush=True)
    if total >= K:
        fam = P + [cand[j] for j in got]
        lab = [0] * N
        for i, S in enumerate(fam):
            for v in S:
                lab[v] = i
        g = os.path.join(wd, 'FOUND-dom-Q11-19.txt')
        with open(g, 'w') as f:
            for r in range(n):
                f.write(' '.join(str(lab[r * n + c]) for c in range(n)) + '\n')
        print('FOUND 19 disjoint dominating sets ->', g); break
