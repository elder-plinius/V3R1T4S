import sys, os, time, glob
import numpy as np
sys.path.insert(0, '/work')
import thomson as T
from pairscan import load, save_cell, csv


def cheap_min(y):
    return T.local_min(y, maxiter=170, ftol=1e-12)


def full_min(y):
    return T.local_min(y, maxiter=2500, ftol=1e-15)


def gen_seeds(dst, rng, ntry=6):
    """Yield (src, seedarray) for all neighbor directions."""
    for src in (dst - 1, dst + 1, dst - 2, dst + 2):
        x = load(src)
        if x is None:
            continue
        d = dst - src
        if d == 1:
            c, rad = T.holes(x)
            tr = T.dist_to_set(c, x)
            order = np.argsort(tr)[::-1][:ntry]
            for idx in order:
                yield src, np.vstack([x, c[idx][None, :] + 0.01 * rng.standard_normal((1, 3))])
        elif d == -1:
            pp = T.per_point_energy(x)
            for h in np.argsort(pp)[::-1][:ntry]:
                yield src, np.delete(x, h, axis=0)
        else:
            k = abs(d)
            if d > 0:
                c, rad = T.holes(x)
                tr = T.dist_to_set(c, x)
                order = np.argsort(tr)[::-1][:10]
                sel = order[:k]
                put = [c[idx] for idx in sel]
                y = x.copy()
                for p in put:
                    y = np.vstack([y, p[None, :] + 0.01 * rng.standard_normal((1, 3))])
                yield src, y
            else:
                pp = T.per_point_energy(x)
                hot = np.argsort(pp)[::-1][:10]
                yield src, np.delete(x, hot[:k], axis=0)


def try_target(dst, seed=0, ntry=6, thresh=0.12):
    if dst not in csv:
        return None
    rng = np.random.default_rng(seed * 104729 + dst)
    rec = csv[dst][0]
    # stage A: cheap relax all seeds
    stageA = []
    for src, ys in gen_seeds(dst, rng, ntry):
        ya, Ea = cheap_min(ys)
        stageA.append((Ea, src, ya))
    stageA.sort(key=lambda t: t[0])
    # stage B: full relax candidates within thresh of record, plus top-3
    keep = [t for t in stageA if t[0] < rec + thresh][:6]
    for t in stageA[:3]:
        if not any(t[0] == k[0] and t[1] == k[1] for k in keep):
            keep.append(t)
    bestE, bestx, bestsrc = None, None, None
    for Ea, src, ya in keep[:7]:
        y, Ey = full_min(ya)
        if bestE is None or Ey < bestE:
            bestE, bestx, bestsrc = Ey, y, src
        if Ey < rec - 1e-6:
            px, pE = T.local_min(y, maxiter=5000, ftol=1e-16)
            if pE < rec - 1e-6:
                Ee = save_cell(dst, px)
                print(f'  *** SAVED {dst} E={Ee:.7f} gain={rec-Ee:.6f} src={src}', flush=True)
    if bestE is None:
        print(f'{dst}: no candidates', flush=True)
        return None
    gap = bestE - rec
    print(f'{dst}: E={bestE:.7f} rec={rec:.7f} gap={gap:+.6f} src={bestsrc} nB={len(keep)}', flush=True)
    return bestE


if __name__ == '__main__':
    targets = eval(sys.argv[1])
    ntry = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    for t in targets:
        if os.path.exists(f'/work/done/{t}.q{seed}'):
            continue
        try:
            try_target(t, seed=seed, ntry=ntry)
        except Exception:
            import traceback; traceback.print_exc()
        open(f'/work/done/{t}.q{seed}', 'w').write('x')
