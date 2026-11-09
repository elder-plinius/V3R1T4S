import sys, os, time, glob
import numpy as np
sys.path.insert(0, '/work')
import thomson as T
from pairscan import load, save_cell, csv


def grow1(x, rng, ntry=6):
    c, rad = T.holes(x)
    tr = T.dist_to_set(c, x)
    order = np.argsort(tr)[::-1]
    best = None
    tried = 0
    for idx in order[:max(ntry * 2, 10)]:
        if tried >= ntry:
            break
        tried += 1
        y = np.vstack([x, c[idx][None, :] + 0.01 * rng.standard_normal((1, 3))])
        y, Ey = T.local_min(y, maxiter=1200, ftol=1e-14)
        if best is None or Ey < best[1]:
            best = (y, Ey)
    return best


def prune1(x, rng, ntry=6):
    pp = T.per_point_energy(x)
    hot = np.argsort(pp)[::-1][:ntry]
    best = None
    for h in hot:
        y = np.delete(x, h, axis=0)
        y, Ey = T.local_min(y, maxiter=1200, ftol=1e-14)
        if best is None or Ey < best[1]:
            best = (y, Ey)
    return best


def growk_combo(x, k, rng, ncombo=3, pool=8):
    """Insert k points: try ncombo different hole sets drawn from top `pool`."""
    c, rad = T.holes(x)
    tr = T.dist_to_set(c, x)
    order = np.argsort(tr)[::-1][:pool]
    best = None
    for ctry in range(ncombo):
        if ctry == 0:
            sel = order[:k]
        else:
            sel = rng.choice(order, size=min(k, len(order)), replace=False)
        put = []
        for idx in sel:
            if all(np.dot(c[idx], p) < 0.995 for p in put):
                put.append(c[idx])
        if len(put) < k:
            continue
        y = x.copy()
        for p in put:
            y = np.vstack([y, p[None, :] + 0.01 * rng.standard_normal((1, 3))])
        y, Ey = T.local_min(y, maxiter=1200, ftol=1e-14)
        if best is None or Ey < best[1]:
            best = (y, Ey)
    return best


def prunek_combo(x, k, rng, ncombo=3, pool=8):
    """Remove k points: try ncombo different sets drawn from top-`pool` hottest."""
    pp = T.per_point_energy(x)
    hot = np.argsort(pp)[::-1][:pool]
    best = None
    for ctry in range(ncombo):
        if ctry == 0:
            drop = hot[:k]
        else:
            drop = rng.choice(hot, size=min(k, len(hot)), replace=False)
        y = np.delete(x, drop, axis=0)
        y, Ey = T.local_min(y, maxiter=1200, ftol=1e-14)
        if best is None or Ey < best[1]:
            best = (y, Ey)
    return best


def try_target(dst, seed=0, ntry=6, tag='p2'):
    if dst not in csv:
        return None
    rng = np.random.default_rng(seed * 104729 + dst)
    rec = csv[dst][0]
    cands = []
    for src in (dst - 1, dst + 1, dst - 2, dst + 2, dst - 3, dst + 3):
        x = load(src)
        if x is None:
            continue
        d = dst - src
        if d == 1:
            cands.append((src, grow1(x, rng, ntry)))
        elif d == -1:
            cands.append((src, prune1(x, rng, ntry)))
        elif d in (2, 3):
            cands.append((src, growk_combo(x, d, rng)))
        elif d in (-2, -3):
            cands.append((src, prunek_combo(x, -d, rng)))
    bestE, bestx, bestsrc = None, None, None
    for src, r in cands:
        if r is None:
            continue
        y, Ey = r
        if bestE is None or Ey < bestE:
            bestE, bestx, bestsrc = Ey, y, src
    if bestE is None:
        print(f'{dst}: no candidates', flush=True)
        return None
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
    ntry = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    for t in targets:
        try:
            try_target(t, seed=seed, ntry=ntry)
        except Exception:
            import traceback; traceback.print_exc()
        open(f'/work/done/{t}.p{seed}', 'w').write('x')
