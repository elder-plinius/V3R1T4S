"""Simulated annealing for large union-free families on {1..n} (no member is the union of the members it properly
contains). Written for run 2026-11-09-1306.  python3 anneal_own.py n seconds seed out.txt
State: a set of bitmasks F. For S in F, cov[S] = OR of the members of F properly contained in S; S is 'bad' if
cov[S] == S. Energy = -|F| + LAM * (#bad). Moves toggle one mask; restricted to sizes 2..n-2 after a warm start."""
import math, random, sys, time
n, secs, seed, out = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rng = random.Random(seed)
FULL = (1 << n) - 1
masks = list(range(1, FULL + 1))
sub = {S: [T for T in range(1, S) if T & S == T] for S in masks}          # proper nonempty submasks
sup = {T: [S for S in range(T + 1, FULL + 1) if S & T == T] for T in masks}  # proper supermasks
inF = [False] * (FULL + 1)
cov = [0] * (FULL + 1)
LAM = 2.0
def covof(S):
    c = 0
    for T in sub[S]:
        if inF[T]: c |= T
    return c
def delta_toggle(m):
    """Return (dsize, dbad) for toggling m, without changing state."""
    if not inF[m]:
        dbad = 1 if covof(m) == m else 0
        for S in sup[m]:
            if inF[S] and cov[S] != S and (cov[S] | m) == S: dbad += 1
        return 1, dbad
    dbad = -1 if cov[m] == m else 0
    inF[m] = False
    for S in sup[m]:
        if inF[S] and cov[S] == S and covof(S) != S: dbad -= 1
    inF[m] = True
    return -1, dbad
def toggle(m):
    inF[m] = not inF[m]
    if inF[m]: cov[m] = covof(m)
    for S in sup[m]:
        if inF[S]: cov[S] = covof(S)
size = bad = 0
best = (0, [])
cand = [m for m in masks if 2 <= bin(m).count('1') <= n - 2]
t0 = time.time(); it = 0
T0, T1 = 1.5, 0.05
while time.time() - t0 < secs:
    it += 1
    frac = (time.time() - t0) / secs
    T = T0 * (T1 / T0) ** frac
    m = rng.choice(cand)
    ds, db = delta_toggle(m)
    dE = -ds + LAM * db
    if dE <= 0 or rng.random() < math.exp(-dE / T):
        toggle(m); size += ds; bad += db
        if bad == 0 and size > best[0]:
            best = (size, [x for x in masks if inF[x]])
# final validation from scratch
F = best[1]
Fs = set(F)
for S in F:
    c = 0
    for T in sub[S]:
        if T in Fs: c |= T
    assert c != S
with open(out, 'w') as f:
    f.write('# union-free family on {1..%d}, %d members (one member per line, elements separated by spaces)\n' % (n, len(F)))
    for S in sorted(F, key=lambda x: (bin(x).count('1'), [i + 1 for i in range(n) if x >> i & 1])):
        f.write(' '.join(str(i + 1) for i in range(n) if S >> i & 1) + '\n')
print('n=%d seed=%d best=%d iterations=%d seconds=%.0f' % (n, seed, best[0], it, time.time() - t0))
