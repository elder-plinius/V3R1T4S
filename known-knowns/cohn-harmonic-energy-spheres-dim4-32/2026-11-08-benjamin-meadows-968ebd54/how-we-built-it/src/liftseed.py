"""Lift/project seeding: seed row (N,n) from best (N,n-1) lifted with noise
in the new coordinate, and from (N,n+1) projected down along weakest axes.
Then a few basin hops. Saves npz on improvement.

python3 liftseed.py <outdir> <per_row_budget> <seed> <N-n> [...]
"""
import sys, os, time, glob
import numpy as np
from opt import energy_grad, minimize_energy

NPZ = np.load('/work/configs/E.npy.npz', allow_pickle=False)
ROWS = {}
UNIV = set()
for line in open('/inputs/cohn_harmonic.tsv'):
    if line.startswith('#') or line.startswith('N\t') or not line.strip():
        continue
    N, n, te, e2, d, u = line.rstrip('\n').split('\t')
    ROWS[f"{N}-{n}"] = (int(N), int(n), min(float(te), float(e2)))
    if u == 'yes':
        UNIV.add(f"{N}-{n}")
PUB = set(open('/inputs/already_published.txt').read().split())


def get_cfg(N, n):
    k = f"{N}-{n}"
    return NPZ[k] if k in NPZ else None


def relax(Y, p, maxiter=1000):
    return minimize_energy(Y, p, maxiter=maxiter, gtol=1e-10, ftol=1e-16)


def best_file(N, n, outdir):
    """Best saved npz for (N,n) in any run dir (excludes posted)."""
    key = f"{N}-{n}"
    best = None
    for f in glob.glob(f'/work/run*/**/{key}.npz', recursive=True) + \
             glob.glob(f'{outdir}/{key}.npz'):
        try:
            z = np.load(f)
            E = float(z['E'])
        except Exception:
            continue
        if best is None or E < best[1]:
            best = [z['Y'], E]
    return best


def cfg(N, n, outdir):
    b = best_file(N, n, outdir)
    if b is not None:
        return b[0], b[1]
    c = get_cfg(N, n)
    if c is None:
        return None, None
    return c, float(energy_grad(c, n - 2)[0])


def main():
    outdir = sys.argv[1]
    budget = float(sys.argv[2])
    seed = int(sys.argv[3])
    keys = sys.argv[4:]
    os.makedirs(outdir, exist_ok=True)
    rng = np.random.default_rng(seed)
    logf = open(os.path.join(outdir, 'liftseed.log'), 'a')

    def log(m):
        logf.write(f"{time.strftime('%H:%M:%S')} {m}\n")
        logf.flush()

    for key in keys:
        if key not in ROWS or key in UNIV or key in PUB:
            continue
        N, n, tgt = ROWS[key]
        p = n - 2
        cur = cfg(N, n, outdir)
        if cur[0] is None:
            continue
        bestY, bestE = cur
        t0 = time.time()
        log(f"{key}: start E={bestE:.8f} tgt={tgt:.8f}")

        def upd(Y, E, tag):
            nonlocal bestY, bestE
            if E < bestE - 1e-11:
                bestY, bestE = Y, float(E)
                np.savez(os.path.join(outdir, f"{key}.npz"), Y=Y, E=float(E))
                log(f"{key} {tag}: E={E:.8f} *")

        seeds = []
        B1, _ = cfg(N, n - 1, outdir)
        if B1 is not None and B1.shape[1] == n - 1:
            for s in (0.05, 0.15, 0.35):
                Y = np.hstack([B1, s * rng.normal(size=(N, 1))])
                Y /= np.linalg.norm(Y, axis=1)[:, None]
                seeds.append((Y, f'lift{s}'))
        B2, _ = cfg(N, n + 1, outdir)
        if B2 is not None and B2.shape[1] == n + 1:
            Cc = B2 - B2.mean(0)
            _, Sv, Vt = np.linalg.svd(Cc, full_matrices=False)
            Br = B2 @ Vt.T
            for drop in np.argsort(Sv)[:3]:
                Y = np.delete(Br, drop, axis=1)
                Y /= np.linalg.norm(Y, axis=1)[:, None]
                seeds.append((Y, f'proj{drop}'))
        for Y, tag in seeds:
            if time.time() - t0 > budget:
                break
            try:
                Yr, E, _ = relax(Y, p)
                upd(Yr, E, tag)
            except Exception:
                continue
        # short basin hop on best
        while time.time() - t0 < budget:
            Y = bestY + rng.choice([0.05, 0.15]) * rng.normal(size=bestY.shape)
            Y /= np.linalg.norm(Y, axis=1)[:, None]
            try:
                Yr, E, _ = relax(Y, p, maxiter=600)
                upd(Yr, E, 'hop')
            except Exception:
                continue
        log(f"{key}: done E={bestE:.8f}")


if __name__ == '__main__':
    main()
