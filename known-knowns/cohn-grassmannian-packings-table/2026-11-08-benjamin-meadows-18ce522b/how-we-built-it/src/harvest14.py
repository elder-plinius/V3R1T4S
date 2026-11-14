import numpy as np, glob, os, json
import packlib, mkcell
from worker import overlap_mat

T = packlib.table()
mp = mkcell.mp

cells = {}
for p in glob.glob('cells/*.txt'):
    k = tuple(int(x) for x in os.path.basename(p)[:-4].split('-'))
    cells[k] = p

# best npy per row over all results
cand = {}
for p in sorted(glob.glob('results/*.npy')):
    base = os.path.basename(p)[:-4].split('.')[0].split('-')
    if len(base) != 3:
        continue
    try:
        k = tuple(int(x) for x in base)
    except ValueError:
        continue
    if k not in T or T[k]['val'] is None:
        continue
    try:
        U = np.load(p)
    except Exception:
        continue
    if U.shape != (k[0], k[1], k[2]):
        continue
    m, n, N = k
    iu = np.triu_indices(N, 1)
    d = n - overlap_mat(U)[iu].max()
    if k not in cand or d > cand[k][0]:
        cand[k] = (d, U)

def cell_f64(path, m, n, N):
    a = np.loadtxt(path, delimiter=',', comments='#')
    U = np.transpose(a.reshape(N, n, m), (2, 1, 0))
    iu = np.triu_indices(N, 1)
    return n - overlap_mat(U)[iu].max()

neww, thin_fail = [], []
for k, (d, U) in sorted(cand.items()):
    m, n, N = k
    tv, bnd = T[k]['val'], T[k]['bnd']
    if d <= tv + 1e-10:
        continue
    if k in cells and cell_f64(cells[k], m, n, N) >= d - 1e-15:
        continue
    # write to temp first, then move over (protect existing cells)
    path = f'cells/{m}-{n}-{N}.txt'
    tmp = f'cells/.tmp-{m}-{n}-{N}.txt'
    mkcell.write_cell(tmp, U, m, n, N, tag='q14')
    dn = cell_f64(tmp, m, n, N)
    ok = dn > tv + 1e-10 and (bnd is None or dn < bnd)
    if ok and dn - tv < 3e-10:
        dm, err = mkcell.verify_cell(tmp, m, n, N)
        ok = dm > tv + mp.mpf('1e-10')
        if not ok:
            thin_fail.append((k, str(dm - tv)))
    if ok:
        os.replace(tmp, path)
        neww.append((k, dn - tv))
    else:
        os.remove(tmp)

print('new cells written:', len(neww))
for k, g in neww:
    print(' ', k, '+%.3e' % g)
if thin_fail:
    print('thin-margin mpf rejects:', thin_fail)
print('total cells:', len(glob.glob('cells/*.txt')))
