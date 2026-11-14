"""Column worker v3: full del-1 enumeration chaining down a column.

python3 worker3.py <n> <Nlo> <Nhi> <outdir> <hop_budget> <seed> <rounds>

For each N (high to low), seeds:
  - all (N+1 choose 1) deletions of best[N+1]  [the historically productive move]
  - del-1 of posted(N+2) -> take best few -> del-1 each (only when time allows)
  - augment best[N-1] with deep-hole point
  - basin hops for remaining budget
best[N] carries improved configs so gains chain down the column.
"""
import sys, os, time, glob
import numpy as np
from opt import energy_grad, minimize_energy

NPZ = np.load('/work/configs/E.npy.npz', allow_pickle=False)


def get_cfg(N, n):
    k = f"{N}-{n}"
    return NPZ[k] if k in NPZ else None


def relax(Y, p, maxiter=1200):
    return minimize_energy(Y, p, maxiter=maxiter, gtol=1e-10, ftol=1e-16)


def contrib(Y, p):
    D = Y[:, None, :] - Y[None, :, :]
    r2 = np.einsum('ijk,ijk->ij', D, D)
    np.fill_diagonal(r2, np.inf)
    rp = r2 ** (-p / 2.0)
    np.fill_diagonal(rp, 0.0)
    return rp.sum(axis=1)


def deep_hole(Y, rng, ntry=300):
    n = Y.shape[1]
    C = rng.normal(size=(ntry, n))
    C /= np.linalg.norm(C, axis=1)[:, None]
    C = np.vstack([C, -Y])
    d2 = ((C[:, None, :] - Y[None, :, :]) ** 2).sum(-1).min(axis=1)
    return C[d2.argmax()]


def main():
    n = int(sys.argv[1]); Nlo = int(sys.argv[2]); Nhi = int(sys.argv[3])
    outdir = sys.argv[4]; hop_budget = float(sys.argv[5])
    seed = int(sys.argv[6]); rounds = int(sys.argv[7]) if len(sys.argv) > 7 else 1
    do_del2 = len(sys.argv) > 8 and sys.argv[8] == '1'
    os.makedirs(outdir, exist_ok=True)
    rng = np.random.default_rng(seed)
    p = n - 2
    logf = open(os.path.join(outdir, f'col{n}.log'), 'a')

    def log(msg):
        logf.write(f"{time.strftime('%H:%M:%S')} n={n} {msg}\n"); logf.flush()

    best = {}
    for N in range(Nlo, Nhi + 2):
        c = get_cfg(N, n)
        if c is not None:
            best[N] = [c.copy(), float(energy_grad(c, p)[0])]
        for f in glob.glob(f'/work/run*/**/{N}-{n}.npz', recursive=True) + \
                 glob.glob(f'{outdir}/{N}-{n}.npz'):
            z = np.load(f)
            if float(z['E']) < best.get(N, [None, np.inf])[1]:
                best[N] = [z['Y'], float(z['E'])]
    for N in sorted(best):
        log(f"init {N}-{n}: E={best[N][1]:.10f}")

    def save(N):
        np.savez(os.path.join(outdir, f"{N}-{n}.npz"), Y=best[N][0], E=best[N][1])

    for rnd in range(rounds):
        for N in range(Nhi, Nlo - 1, -1):
            if N not in best:
                continue
            t0 = time.time()
            # 1) full del-1 enumeration of best[N+1]
            if N + 1 in best:
                B = best[N + 1][0]
                for i in range(N + 1):
                    S = np.delete(B, i, axis=0)
                    try:
                        Yr, E, _ = relax(S, p)
                    except Exception:
                        continue
                    if E < best[N][1] - 1e-11:
                        best[N] = [Yr, float(E)]
                        log(f"{N}-{n} r{rnd} del1[{i}]: E={E:.10f} *")
            save(N)
            # 2) del-1 of posted/best N+2 -> distinct top-3 -> del-1 each
            if do_del2 and N + 2 in best:
                B = best[N + 2][0]
                cands = []
                for i in range(N + 2):
                    S = np.delete(B, i, axis=0)
                    try:
                        Yr, E, _ = relax(S, p)
                    except Exception:
                        continue
                    cands.append((E, Yr))
                cands.sort(key=lambda t: t[0])
                seen = []
                for E, Yr in cands:
                    if len(seen) >= 3:
                        break
                    if all(abs(E - e) > 1e-7 for e in seen):
                        seen.append(E)
                        for j in range(N + 1):
                            S = np.delete(Yr, j, axis=0)
                            try:
                                Yr2, E2, _ = relax(S, p)
                            except Exception:
                                continue
                            if E2 < best[N][1] - 1e-11:
                                best[N] = [Yr2, float(E2)]
                                log(f"{N}-{n} r{rnd} del2: E={E2:.10f} *")
                    if time.time() - t0 > hop_budget * 2:
                        break
                save(N)
            # 3) augment from N-1
            if N - 1 in best and time.time() - t0 < hop_budget:
                for _ in range(2):
                    S = np.vstack([best[N - 1][0], deep_hole(best[N - 1][0], rng)])
                    try:
                        Yr, E, _ = relax(S, p)
                    except Exception:
                        continue
                    if E < best[N][1] - 1e-11:
                        best[N] = [Yr, float(E)]
                        log(f"{N}-{n} r{rnd} aug: E={E:.10f} *")
            # 4) basin hops until budget
            it = 0
            while time.time() - t0 < hop_budget:
                it += 1
                move = rng.integers(0, 5)
                Y = best[N][0].copy()
                if move == 0:
                    Y += rng.choice([0.03, 0.07, 0.15, 0.3]) * rng.normal(size=Y.shape)
                elif move == 1:
                    k = rng.integers(1, 6)
                    idx = rng.choice(N, size=min(k, N), replace=False)
                    Y[idx] = rng.normal(size=(len(idx), n))
                    Y += 0.08 * rng.normal(size=Y.shape)
                elif move == 2:
                    k = rng.integers(1, 5)
                    S = Y.copy()
                    for _ in range(k):
                        c = contrib(S, p)
                        S = np.delete(S, c.argmax(), axis=0)
                    Sr, _, _ = relax(S, p, maxiter=500)
                    for _ in range(k):
                        Sr = np.vstack([Sr, deep_hole(Sr, rng)])
                    Y = Sr
                elif move == 3:
                    k = rng.integers(1, 5)
                    idx = rng.choice(N, size=min(k, N), replace=False)
                    Y[idx] += rng.choice([0.1, 0.25]) * rng.normal(size=(len(idx), n))
                else:
                    k = rng.integers(1, 4)
                    idx = rng.choice(N, size=min(k, N), replace=False)
                    Y[idx] = -Y[idx]
                    Y += 0.05 * rng.normal(size=Y.shape)
                Y /= np.linalg.norm(Y, axis=1)[:, None]
                try:
                    Yr, E, _ = relax(Y, p)
                except Exception:
                    continue
                if E < best[N][1] - 1e-11:
                    best[N] = [Yr, float(E)]
                    log(f"{N}-{n} r{rnd} hop{it} m{move}: E={E:.10f} *")
            save(N)
        log(f"--- round {rnd} done ---")
    for N in sorted(best):
        save(N)
        log(f"final {N}-{n}: E={best[N][1]:.10f}")


if __name__ == '__main__':
    main()
