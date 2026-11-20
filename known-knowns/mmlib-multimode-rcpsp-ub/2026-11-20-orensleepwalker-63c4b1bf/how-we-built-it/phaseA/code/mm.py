"""Independent MRCPSP tools (standard library), written from the PSPLIB/MMLIB .mm format and the bank's definition.
read(text) -> dict(n, succ, modes[j] = [(dur, [renewable demands], [nonrenewable demands])], Rcap, Ncap)   (jobs 0-based)
check(inst, modes, starts) -> 'VALID makespan M' or 'INVALID: reason'. modes: 1-based mode per job; starts: start per job (all n jobs,
dummies included). Checks one valid mode per job, non-renewable totals <= availability, every precedence (successor starts no earlier
than predecessor finishes), renewable usage <= capacity in every period, and reports the makespan (latest finish)."""
import re
def read(t):
    L = t.splitlines(); n = int(re.search(r'jobs\s+\(incl\.\s*supersource/sink\s*\):\s*(\d+)', t).group(1))
    nR = int(re.search(r'- renewable\s*:\s*(\d+)', t).group(1)); nN = int(re.search(r'- nonrenewable\s*:\s*(\d+)', t).group(1))
    i = next(k for k, l in enumerate(L) if l.startswith('PRECEDENCE RELATIONS')) + 2; succ = {}; nm = {}
    for k in range(n):
        p = L[i + k].split(); j = int(p[0]) - 1; nm[j] = int(p[1]); succ[j] = [int(x) - 1 for x in p[3:3 + int(p[2])]]
    i = next(k for k, l in enumerate(L) if l.startswith('REQUESTS/DURATIONS')) + 3; modes = {j: [] for j in range(n)}; j = None
    while not L[i].startswith('*'):
        p = L[i].split()
        if len(p) == 3 + nR + nN: j = int(p[0]) - 1; p = p[1:]
        modes[j].append((int(p[1]), [int(x) for x in p[2:2 + nR]], [int(x) for x in p[2 + nR:2 + nR + nN]])); i += 1
    assert all(len(modes[j]) == nm[j] for j in range(n)), 'mode count mismatch'
    i = next(k for k, l in enumerate(L) if 'RESOURCE AVAILABILITIES' in l) + 2; cap = [int(x) for x in L[i].split()]
    return dict(n=n, succ=succ, modes=[modes[j] for j in range(n)], Rcap=cap[:nR], Ncap=cap[nR:nR + nN])
def check(I, mode, start):
    n = I['n']
    if len(mode) != n or len(start) != n: return 'INVALID: need %d modes and %d starts' % (n, n)
    if any(not (1 <= mode[j] <= len(I['modes'][j])) for j in range(n)): return 'INVALID: mode out of range'
    if any(s < 0 for s in start): return 'INVALID: negative start'
    M = [I['modes'][j][mode[j] - 1] for j in range(n)]; fin = [start[j] + M[j][0] for j in range(n)]
    for k, c in enumerate(I['Ncap']):
        if sum(m[2][k] for m in M) > c: return 'INVALID: non-renewable %d uses %d > %d' % (k + 1, sum(m[2][k] for m in M), c)
    for j in range(n):
        for s in I['succ'][j]:
            if start[s] < fin[j]: return 'INVALID: job %d starts before predecessor %d finishes' % (s + 1, j + 1)
    T = max(fin); use = [[0] * T for _ in I['Rcap']]
    for j in range(n):
        for k in range(len(I['Rcap'])):
            if M[j][1][k]:
                for t in range(start[j], fin[j]): use[k][t] += M[j][1][k]
    for k, c in enumerate(I['Rcap']):
        if max(use[k], default=0) > c: return 'INVALID: renewable %d over capacity at t=%d' % (k + 1, use[k].index(max(use[k])))
    return 'VALID makespan %d' % T
