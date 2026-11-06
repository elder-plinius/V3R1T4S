"""H1/H3: |K| for B1 = X, B2 = M X with M monomial (signed coordinate permutation), X = 512-cap (n=8) or 236-cap (n=7).
Translations do not change |K| (K shifts), so only the linear part matters."""
import numpy as np, itertools, sys, time, json
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from framelib import *
rng = np.random.default_rng(1)
which = sys.argv[1]
if which == '8':
    X = load(RUN + '/checker/record_512_n8.txt', 8); n = 8
else:
    X = load(RUN + '/checker/record_236_n7.txt', 7); n = 7
nsamp = int(sys.argv[2])
t0 = time.time()
res = []
# identity and -I
for name, M in [('I', np.eye(n, dtype=np.int64)), ('-I', 2*np.eye(n, dtype=np.int64))]:
    k = K_of(X, (X @ M.T) % 3).sum(); res.append((int(k), name)); print(name, k, flush=True)
# all sign diagonals
for s in itertools.product([1, 2], repeat=n):
    M = np.diag(s)
    k = K_of(X, (X @ M.T) % 3).sum(); res.append((int(k), 'diag' + ''.join(map(str, s))))
print('signs done', time.time() - t0, flush=True)
# random signed permutations
for it in range(nsamp):
    p = rng.permutation(n); s = rng.integers(1, 3, n)
    M = np.zeros((n, n), np.int64); M[np.arange(n), p] = s
    k = K_of(X, (X @ M.T) % 3).sum(); res.append((int(k), 'perm' + ''.join(map(str, p)) + 's' + ''.join(map(str, s))))
res.sort(reverse=True)
vals = np.array([r[0] for r in res])
print('n', n, 'evaluated', len(res), 'time', round(time.time() - t0, 1))
print('distribution of |K|:', {int(v): int(c) for v, c in zip(*np.unique(vals, return_counts=True))})
print('top 15:', res[:15])
