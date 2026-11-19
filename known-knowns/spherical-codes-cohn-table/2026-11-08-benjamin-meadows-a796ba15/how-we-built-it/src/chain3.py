"""Chained seeded optimizer: for target (d,N), pick best donor below N
(our cell > tmp near-miss > posted, nearest & lowest-max), insert k pts,
L-BFGS beta ramp + SLP. Optionally subtractive from a donor above N.

Queue line: d,N[,mode]   mode in {auto,add,sub}
"""
import numpy as np, sys, time, os
sys.path.insert(0, '/work')
import sph, slbfgs, slpf

TP = os.environ.get('TP', 'tmp')
tab = {}
for line in open('/inputs/plain_2026-11-04.txt'):
    f = line.strip().split(',')
    tab[(int(f[0]), int(f[1]))] = float(f[2])


def maxip(X):
    G = X @ X.T; np.fill_diagonal(G, -9); return G.max()


def loadf(path):
    X = np.loadtxt(path, delimiter=',')
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def try_loadf(path):
    try:
        X = np.loadtxt(path, delimiter=',')
        if X.ndim != 2:
            return None
        return X / np.linalg.norm(X, axis=1, keepdims=True)
    except Exception:
        return None


import glob as _glob


def donor_paths(d, n):
    seen = set()
    pats = [f'cells/{d}-{n}.txt', f'{TP}_{d}-{n}.txt',
            f'tmp_{d}-{n}.txt', f'tmp_sub_{d}-{n}.txt',
            f'data/{d}-{n}.txt', f'tp*_{d}-{n}.txt']
    for pat in pats:
        for p in sorted(_glob.glob(pat)):
            if p not in seen:
                seen.add(p)
                yield p


def find_donor(d, N, maxgap=8):
    """Return (path, k, mx) best donor below N. Prefer lowest max-ip with
    penalty per extra missing point."""
    cands = []
    for k in range(1, maxgap + 1):
        n = N - k
        for p in donor_paths(d, n):
            Xc = try_loadf(p)
            if Xc is None:
                continue
            mx = maxip(Xc)
            cands.append((mx, k, p))
    if not cands:
        return None
    near = [c for c in cands if c[1] <= 3]
    pool = near if near else cands
    pool.sort(key=lambda c: c[0] + 3e-4 * c[1])
    mx, k, p = pool[0]
    return p, k, mx


def find_donor_up(d, N, maxgap=8):
    cands = []
    for k in range(1, maxgap + 1):
        n = N + k
        for p in donor_paths(d, n):
            Xc = try_loadf(p)
            if Xc is None:
                continue
            mx = maxip(Xc)
            cands.append((mx, k, p))
    if not cands:
        return None
    near = [c for c in cands if c[1] <= 3]
    pool = near if near else cands
    pool.sort(key=lambda c: c[0] + 3e-4 * c[1])
    mx, k, p = pool[0]
    return p, k, mx


def polish(X, iters, slp_iter=10, floor=None):
    for i, b in enumerate((1e3, 3e3, 1e4, 3e4, 1e5, 5e5, 2e6)):
        X = slbfgs.lbfgs_b(X, b, iters)
        if floor is not None and i in (2, 4):
            g = maxip(X)
            if g > floor + (8e-3 if i == 2 else 2.5e-3):
                return g, X  # hopeless; skip remaining stages and SLP
    if slp_iter:
        X, g = slpf.slp_fast(X, max_iter=slp_iter, cap=700)
    else:
        g = maxip(X)
    return g, X


def run_add(d, N, T, trials, iters, donor):
    path, k, dmx = donor
    core = try_loadf(path)
    if core is None:
        print(f'  donor {path} unreadable, skip', flush=True)
        return (1e18, None)
    print(f'  donor {path} (k={k}, mx={dmx:.9f})', flush=True)
    best = (1e18, None)
    rng = np.random.default_rng(d * 977 + N)
    for tr in range(trials):
        c = core.copy()
        for j in range(k):
            if tr % 3 == 2:
                x = rng.standard_normal(c.shape[1])
                x /= np.linalg.norm(x)
            else:
                x, _ = sph._min_ip_to_core(np.ascontiguousarray(c), 70, 0.02,
                                           tr * 37 + j + int(d))
            c = np.vstack([c, x])
        g, Y = polish(c, iters, floor=T)
        print(f'  {d}-{N} tr{tr}: g={g:.12f} need<{T:.12f}', flush=True)
        if g < best[0]:
            best = (g, Y)
            np.savetxt(f'{TP}_{d}-{N}.txt', Y, delimiter=',', fmt='%.20e')
        if g < T:
            np.savetxt(f'cells/{d}-{N}.txt', Y, delimiter=',', fmt='%.20e')
            print(f'  WIN {d}-{N}', flush=True)
            return best
        if tr >= 2 and best[0] > T + 2e-3:
            break
    return best


def greedy_delete(X, k):
    keep = np.ones(len(X), bool)
    for _ in range(k):
        idx = np.where(keep)[0]
        A = X[idx]
        G = A @ A.T; np.fill_diagonal(G, -9)
        top = G.max(1)
        cnt = (G > (top[:, None] - 1e-6)).sum(1)
        kill = idx[np.argmax(top + cnt * 1e-7)]
        keep[kill] = False
    return X[keep]


SLP0_IT = int(os.environ.get('SLP0_IT', 20))
ALT_IT = int(os.environ.get('ALT_IT', 25))
DEEP_IT = int(os.environ.get('DEEP_IT', 50))
DEEP_MAX = float(os.environ.get('DEEP_MAX', 3e-4))
DEEP_MIN = float(os.environ.get('DEEP_MIN', 5e-10))


def run_sub(d, N, T, trials, iters, donor):
    path, k, dmx = donor
    core = try_loadf(path)
    if core is None:
        print(f'  donor {path} unreadable, skip', flush=True)
        return (1e18, None)
    print(f'  SUB donor {path} (del {k}, mx={dmx:.9f})', flush=True)
    best = (1e18, None)
    for tr in range(trials):
        X0 = greedy_delete(core, k)
        # first: monotone SLP descent on the raw subset (never climbs)
        Ys, gs = slpf.slp_fast(X0, max_iter=SLP0_IT, cap=700)
        print(f'  {d}-{N} sub tr{tr} slp0: g={gs:.12f} need<{T:.12f}',
              flush=True)
        if gs < best[0]:
            best = (gs, Ys)
            np.savetxt(f'{TP}_{d}-{N}.txt', Ys, delimiter=',', fmt='%.20e')
        if gs < T:
            np.savetxt(f'cells/{d}-{N}.txt', Ys, delimiter=',', fmt='%.20e')
            print(f'  WIN {d}-{N} (sub-slp)', flush=True)
            return best
        if gs > T + 2e-5:
            break  # L-BFGS polish climbs on flat donors; not worth it
        # gs within 2e-5 of target: try cheap alternate deletions first
        if k == 1:
            G = core @ core.T; np.fill_diagonal(G, -9)
            top = G.max(1)
            order = np.argsort(-top)[1:5]
            for i in order:
                Xa = np.delete(core, i, 0)
                Ya, ga = slpf.slp_fast(Xa, max_iter=ALT_IT, cap=700)
                print(f'  {d}-{N} sub alt{i}: g={ga:.12f}', flush=True)
                if ga < best[0]:
                    best = (ga, Ya)
                    np.savetxt(f'{TP}_{d}-{N}.txt', Ya, delimiter=',',
                               fmt='%.20e')
                if ga < T:
                    np.savetxt(f'cells/{d}-{N}.txt', Ya, delimiter=',',
                               fmt='%.20e')
                    print(f'  WIN {d}-{N} (sub-alt)', flush=True)
                    return best
        g, Y = polish(X0, iters, floor=T)
        print(f'  {d}-{N} sub tr{tr}: g={g:.12f} need<{T:.12f}', flush=True)
        if g < best[0]:
            best = (g, Y)
            np.savetxt(f'{TP}_{d}-{N}.txt', Y, delimiter=',', fmt='%.20e')
        if g < T:
            np.savetxt(f'cells/{d}-{N}.txt', Y, delimiter=',', fmt='%.20e')
            print(f'  WIN {d}-{N} (sub)', flush=True)
            return best
        break  # greedy_delete is deterministic; one trial is enough
    return best


if __name__ == '__main__':
    fname = sys.argv[1]
    for line in open(fname):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        p = line.split(',')
        d, N = int(p[0]), int(p[1])
        mode = p[2].strip() if len(p) > 2 else 'auto'
        trials = int(p[3]) if len(p) > 3 else 4
        iters = int(p[4]) if len(p) > 4 else 160
        if (d, N) not in tab:
            print(f'--- {d}-{N}: not in table, skip', flush=True)
            continue
        T = tab[(d, N)] - 1e-11
        t0 = time.time()
        # resolve donors BEFORE printing the === header so that rows skipped
        # for lack of donor are NOT marked processed in b*.log scans
        don_add = don_sub = None
        if mode.startswith('add:'):
            path = mode.split(':', 1)[1]
            Xc = try_loadf(path)
            if Xc is not None:
                don_add = (path, N - len(Xc), maxip(Xc))
        elif mode in ('auto', 'add'):
            don_add = find_donor(d, N)
        if mode.startswith('sub:'):
            path = mode.split(':', 1)[1]
            Xc = try_loadf(path)
            if Xc is not None:
                don_sub = (path, len(Xc) - N, maxip(Xc))
        elif mode in ('auto', 'sub'):
            don_sub = find_donor_up(d, N)
        if don_add is None and don_sub is None:
            print(f'--- {d}-{N}: no donor, skip', flush=True)
            continue
        print(f'=== {d}-{N} mode={mode} T={T:.12f} ===', flush=True)
        best = (1e18, None)
        if mode.startswith('add:') or mode == 'add':
            if don_add is not None:
                best = run_add(d, N, T, trials, iters, don_add)
                if best[0] < T or mode == 'add':
                    print(f'    done {time.time()-t0:.0f}s', flush=True)
                    if best[0] < T:
                        continue
        elif mode == 'auto':
            if don_add is not None:
                best = run_add(d, N, T, trials, iters, don_add)
                if best[0] < T:
                    print(f'    done {time.time()-t0:.0f}s', flush=True)
                    continue
            if best[0] > T and don_sub is not None:
                best2 = run_sub(d, N, T, trials, iters, don_sub)
                if best2[0] < best[0]:
                    best = best2
        elif mode == 'sub' or mode.startswith('sub:'):
            if don_sub is not None:
                best = run_sub(d, N, T, trials, iters, don_sub)
        # deep SLP squeeze if close (skip true-optimum floors <5e-10)
        if DEEP_MIN < best[0] - T < DEEP_MAX and best[1] is not None:
            print(f'  close ({best[0]-T:.2e}); deep SLP...', flush=True)
            Y, g = slpf.slp_fast(best[1], max_iter=DEEP_IT, cap=1200)
            print(f'  deep: {g:.12f}', flush=True)
            if g < best[0]:
                best = (g, Y)
                np.savetxt(f'{TP}_{d}-{N}.txt', Y, delimiter=',', fmt='%.20e')
            if g < T:
                np.savetxt(f'cells/{d}-{N}.txt', Y, delimiter=',', fmt='%.20e')
                print(f'  WIN {d}-{N} (deep)', flush=True)
        print(f'    done {time.time()-t0:.0f}s best={best[0]:.12f}', flush=True)
