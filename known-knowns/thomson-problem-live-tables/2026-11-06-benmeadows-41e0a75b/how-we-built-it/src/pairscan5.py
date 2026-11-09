import sys, os, glob
import numpy as np
sys.path.insert(0, '/work')
import thomson as T
from pairscan import load, save_cell, csv
from pairscan3 import cheap_min, full_min


def all_sources(src):
    """Every saved config at N=src: record + nm seeds + cell."""
    out = []
    x = load(src)
    if x is not None:
        out.append((f'{src}rec', x))
    for fn in sorted(glob.glob(f'/work/seeds/{src}_nm*.npy')):
        out.append((os.path.basename(fn)[:-4], np.load(fn)))
    if os.path.exists(f'/work/cells/{src}.txt'):
        out.append((f'{src}cell', np.loadtxt(f'/work/cells/{src}.txt', delimiter=',')))
    return out


def gen_from(x, dst, rng, ntry):
    """grow/prune seeds from config x toward dst."""
    d = dst - len(x)
    k = abs(d)
    out = []
    if k == 0:
        return out
    if d > 0:
        c, rad = T.holes(x)
        if len(c) == 0:
            return out
        tr = T.dist_to_set(c, x)
        order = np.argsort(tr)[::-1][:max(10, ntry)]
        for v in range(ntry):
            if k == 1:
                idx = order[v] if v < len(order) else rng.choice(order)
                out.append(np.vstack([x, c[idx][None, :] + 0.01 * rng.standard_normal((1, 3))]))
            else:
                sel = order[:k] if v == 0 else rng.choice(order, size=k, replace=False)
                put = list(sel)
                # de-cluster
                fixed = [put[0]]
                for p in put[1:]:
                    for q in order:
                        if all(np.dot(c[q], c[r]) < 0.995 for r in fixed):
                            fixed.append(q)
                            break
                put = fixed[:k]
                y = x.copy()
                for p in put:
                    y = np.vstack([y, c[p][None, :] + 0.01 * rng.standard_normal((1, 3))])
                out.append(y)
    else:
        pp = T.per_point_energy(x)
        hot = np.argsort(pp)[::-1][:max(10, ntry)]
        for v in range(ntry):
            if k == 1:
                h = hot[v] if v < len(hot) else rng.choice(hot)
                out.append(np.delete(x, int(h), axis=0))
            else:
                sel = hot[:k] if v == 0 else rng.choice(hot, size=k, replace=False)
                out.append(np.delete(x, [int(s) for s in sel], axis=0))
    return out


def try_target(dst, ntry=4, thresh=0.10, cap=48):
    if dst not in csv:
        return
    rec = csv[dst][0]
    rng = np.random.default_rng(dst * 131 + 17)
    stage = []
    for src in (dst - 1, dst + 1, dst - 2, dst + 2):
        for tag, xs in all_sources(src):
            for ys in gen_from(xs, dst, rng, ntry):
                stage.append((tag, ys))
    rng.shuffle(stage)
    stage = stage[:cap]
    A = []
    for tag, ys in stage:
        ya, Ea = cheap_min(ys)
        A.append((Ea, tag, ya))
    A.sort(key=lambda t: t[0])
    keep = [t for t in A if t[0] < rec + thresh][:6]
    for t in A[:3]:
        if not any(t[0] == k[0] for k in keep):
            keep.append(t)
    best = None
    for Ea, tag, ya in keep[:7]:
        y, Ey = full_min(ya)
        if best is None or Ey < best[0]:
            best = (Ey, tag)
        if Ey < rec - 1e-6:
            px, pE = T.local_min(y, maxiter=6000, ftol=1e-16)
            if pE < rec - 1e-6:
                Ee = save_cell(dst, px)
                print(f'  *** SAVED {dst} E={Ee:.7f} gain={rec-Ee:.6f} src={tag}', flush=True)
                return
    if best:
        print(f'{dst}: E={best[0]:.7f} rec={rec:.7f} gap={best[0]-rec:+.6f} src={best[1]}', flush=True)


if __name__ == '__main__':
    targets = eval(sys.argv[1])
    for t in targets:
        if os.path.exists(f'/work/done/{t}.p5'):
            continue
        try:
            try_target(t)
        except Exception:
            import traceback; traceback.print_exc()
        open(f'/work/done/{t}.p5', 'w').write('x')
