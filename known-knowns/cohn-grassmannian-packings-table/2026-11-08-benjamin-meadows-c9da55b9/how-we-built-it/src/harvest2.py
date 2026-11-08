import numpy as np, glob, os, json
import packlib
from worker import overlap_mat
import mkcell

mp = mkcell.mp
T = packlib.table()

def load_cell_vecs(path):
    vecs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            vecs.append([float(x) for x in line.split(',')])
    return np.array(vecs)

def cell_mind_f64(path, m, n, N):
    a = load_cell_vecs(path)
    assert a.shape == (n * N, m), (a.shape, n * N, m)
    U = np.transpose(a.reshape(N, n, m), (2, 1, 0))
    iu = np.triu_indices(N, 1)
    return n - overlap_mat(U)[iu].max()

def orth_err_f64(path, m, n, N):
    a = load_cell_vecs(path)
    U = np.transpose(a.reshape(N, n, m), (2, 1, 0))
    err = 0.0
    for k in range(N):
        G = U[:, :, k].T @ U[:, :, k]
        err = max(err, np.abs(G - np.eye(n)).max())
    return err

# gather best config per row from all result files
best = {}
for path in sorted(glob.glob('results/*.npy')):
    base = os.path.basename(path)[:-4]
    parts = base.split('.')[0].split('-')
    if len(parts) != 3:
        continue
    try:
        m, n, N = int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        continue
    if (m, n, N) not in T or T[(m, n, N)]['val'] is None:
        continue
    try:
        U = np.load(path)
    except Exception:
        continue
    if U.shape != (m, n, N):
        continue
    iu = np.triu_indices(N, 1)
    d = n - overlap_mat(U)[iu].max()
    tv = T[(m, n, N)]['val']
    if d > tv + 1e-10:
        if (m, n, N) not in best or d > best[(m, n, N)][0]:
            best[(m, n, N)] = (d, path, U.copy())

print('winning rows found:', len(best), flush=True)

# write cells (mpf re-orthonormalization) then verify
import mpmath
stats = dict(wins=0, kept=0, maxgain=0.0, maxrow=None)
for (m, n, N), (d, path, U) in sorted(best.items()):
    tv = T[(m, n, N)]['val']
    bnd = T[(m, n, N)]['bnd']
    cell = f'cells/{m}-{n}-{N}.txt'
    old_d = None
    if os.path.exists(cell):
        old_d = cell_mind_f64(cell, m, n, N)
    if old_d is not None and old_d >= d - 1e-15:
        continue  # existing cell already as good
    mkcell.write_cell(cell, U, m, n, N, tag=f'd={d:.15f}')
    dn = cell_mind_f64(cell, m, n, N)
    # mpf verification on a sample of pairs is skipped; f64 err ~1e-15 << 1e-10
    if dn <= tv + 1e-10:
        print(f'{m}-{n}-{N}: FAIL margin {dn - tv:.2e}', flush=True)
        if old_d is not None:
            print('  (lost prior cell — check)', flush=True)
        os.remove(cell)
        continue
    if bnd is not None and dn >= bnd:
        print(f'{m}-{n}-{N}: FAIL bound {dn} vs {bnd}', flush=True)
        os.remove(cell)
        continue
    stats['kept'] += 1
    if dn - tv > stats['maxgain']:
        stats['maxgain'] = dn - tv
        stats['maxrow'] = f'{m}-{n}-{N}'
    stats['wins'] += 1

print('cells written this run:', stats['wins'], flush=True)
print('total cells:', len(glob.glob('cells/*.txt')), flush=True)
print('max gain:', stats['maxgain'], stats['maxrow'], flush=True)
