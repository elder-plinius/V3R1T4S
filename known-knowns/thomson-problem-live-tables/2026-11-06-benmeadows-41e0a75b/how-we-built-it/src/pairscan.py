import sys, os, time, glob
import numpy as np
sys.path.insert(0, '/work')
import thomson as T

csv = {}
for line in open('/work/table.csv'):
    n, e, s = line.strip().split(',')
    csv[int(n)] = (float(e), s)


def load(n):
    """Best available start for n (prefer record-holding source, then any)."""
    src = csv[n][1]
    fn = f'/work/starts/{n}_{src}.npy'
    if os.path.exists(fn):
        return np.load(fn)
    c = glob.glob(f'/work/starts/{n}_*.npy')
    if c:
        return np.load(c[0])
    c = glob.glob(f'/work/cells/{n}.txt')
    if c:
        return np.loadtxt(c[0], delimiter=',')
    return None


def save_cell(n, x):
    x = T.normalize(x)
    E = T.energy_exact(x)
    tmp = f'/work/cells/{n}.txt.tmp'
    with open(tmp, 'w') as f:
        for row in x:
            f.write(f'{row[0]:.21f},{row[1]:.21f},{row[2]:.21f}\n')
    os.rename(tmp, f'/work/cells/{n}.txt')
    return E


def grow1(x, rng, ntry=5):
    """Add one point; try ntry largest holes, keep best relaxed."""
    c, rad = T.holes(x)
    tr = T.dist_to_set(c, x)
    order = np.argsort(tr)[::-1]
    best = None
    tried = 0
    for idx in order[:max(ntry * 2, 8)]:
        if tried >= ntry:
            break
        tried += 1
        y = np.vstack([x, c[idx][None, :] + 0.01 * rng.standard_normal((1, 3))])
        y, Ey = T.local_min(y, maxiter=1200, ftol=1e-14)
        if best is None or Ey < best[1]:
            best = (y, Ey)
    return best


def prune1(x, rng, ntry=5):
    """Remove one point; try ntry hottest, keep best relaxed."""
    pp = T.per_point_energy(x)
    hot = np.argsort(pp)[::-1][:ntry]
    best = None
    for h in hot:
        y = np.delete(x, h, axis=0)
        y, Ey = T.local_min(y, maxiter=1200, ftol=1e-14)
        if best is None or Ey < best[1]:
            best = (y, Ey)
    return best


def growk(x, k, rng):
    c, rad = T.holes(x)
    tr = T.dist_to_set(c, x)
    order = np.argsort(tr)[::-1]
    put = []
    for idx in order:
        if len(put) >= k:
            break
        if all(np.dot(c[idx], p) < 0.995 for p in put):
            put.append(c[idx])
    y = x.copy()
    for p in put:
        y = np.vstack([y, p[None, :] + 0.01 * rng.standard_normal((1, 3))])
    y, Ey = T.local_min(y, maxiter=1200, ftol=1e-14)
    return y, Ey


def prunek(x, k):
    pp = T.per_point_energy(x)
    drop = np.argsort(pp)[::-1][:k]
    y = np.delete(x, drop, axis=0)
    y, Ey = T.local_min(y, maxiter=1200, ftol=1e-14)
    return y, Ey


def try_target(dst, seed=0, ntry=5):
    rng = np.random.default_rng(seed * 104729 + dst)
    rec = csv[dst][0]
    cands = []
    for src in (dst - 1, dst + 1, dst - 2, dst + 2):
        if src not in csv:
            continue
        x = load(src)
        if x is None:
            continue
        d = dst - src
        if d == 1:
            cands.append((src, grow1(x, rng, ntry)))
        elif d == -1:
            cands.append((src, prune1(x, rng, ntry)))
        elif d == 2:
            cands.append((src, growk(x, 2, rng)))
        elif d == -2:
            cands.append((src, prunek(x, 2)))
    bestE, bestx, bestsrc = None, None, None
    for src, r in cands:
        if r is None:
            continue
        y, Ey = r
        if bestE is None or Ey < bestE:
            bestE, bestx, bestsrc = Ey, y, src
    if bestE is None:
        print(f'{dst}: no candidates', flush=True)
        return
    gap = bestE - rec
    print(f'{dst}: E={bestE:.7f} rec={rec:.7f} gap={gap:+.6f} src={bestsrc}', flush=True)
    if bestE < rec - 1e-6:
        px, pE = T.local_min(bestx, maxiter=5000, ftol=1e-16)
        if pE < rec - 1e-6:
            Ee = save_cell(dst, px)
            print(f'  *** SAVED {dst} E={Ee:.7f} gain={rec-Ee:.6f}', flush=True)
    return bestE


if __name__ == '__main__':
    targets = eval(sys.argv[1])
    ntry = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    for t in targets:
        t0 = time.time()
        try:
            try_target(t, ntry=ntry)
        except Exception:
            import traceback; traceback.print_exc()
        open(f'/work/done/{t}.pair', 'w').write('x')
