"""Lane sloanes, round 3: re-optimise / extend searches for low-coherence packings of n lines in C^d.

One job = one cell (d, n) with a wall-clock budget. The incumbent starts from the best of the
given seed files (earlier packings, or (d, n+1) packings with one vector deleted) and from fresh
random starts. Each iteration produces a candidate by one of:
  - basin hop: incumbent (or a pool member) plus complex Gaussian noise of scale sigma,
    then high-p log-sum-exp descent;
  - fresh random start with the full p schedule (occasionally followed by alternating projection);
  - deletion seed (if a (d, n+1) packing is given): drop one random vector, then descend.
Candidates within 2e-3 of the incumbent are polished by sequential LP (search.polish).
The best packing is written to out/<d>x<n>.txt only if it improves on the file already there.
"""
import json, os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from search import descend, polish, coherence, normalise, random_start, altproj, save

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def load(path, d, n):
    v = np.array([float(t) for line in open(path) if not line.startswith("#") for t in line.split()])
    assert v.size == 2 * d * n, (path, v.size)
    return normalise((v[: d * n].reshape(n, d) + 1j * v[d * n:].reshape(n, d)).T)


def run_job(job):
    d, n, budget, seed = job["d"], job["n"], job["budget"], job.get("seed", 0)
    rng = np.random.default_rng(seed * 7919 + 1000 * d + n)
    t0 = time.time()
    starts = []
    for p in job.get("starts", []):
        if os.path.exists(p):
            starts.append(load(p, d, n))
    parents = [load(p, d, n + 1) for p in job.get("parents", []) if os.path.exists(p)]
    pool = []  # (mu, X)
    for X in starts:
        X = polish(X, rounds=100, r0=1e-4)
        pool.append((coherence(X), X))
    start_mu = min([m for m, _ in pool], default=np.inf)
    if not pool:
        X = descend(random_start(d, n, rng))
        pool.append((coherence(X), X))
    pool.sort(key=lambda t: t[0])
    best_mu, best_X = pool[0]
    stats = dict(hop=0, fresh=0, dele=0, improve=[])
    frac_fresh = job.get("frac_fresh", 0.25)
    it = 0
    while time.time() - t0 < budget:
        it += 1
        u = rng.random()
        if parents and u < 0.2:
            P = parents[rng.integers(len(parents))]
            k = rng.integers(n + 1)
            Y = np.delete(P, k, axis=1) + 0.02 * rng.random() * (rng.standard_normal((d, n)) + 1j * rng.standard_normal((d, n)))
            Y = descend(normalise(Y), ps=(300, 1e3, 3e3, 1e4, 3e4))
            kind = "dele"
        elif u < 0.2 + frac_fresh:
            Y = descend(random_start(d, n, rng))
            if rng.random() < 0.25:
                Y2 = descend(altproj(Y, coherence(Y) * 0.99), ps=(1e3, 1e4, 3e4))
                if coherence(Y2) < coherence(Y):
                    Y = Y2
            kind = "fresh"
        else:
            base = pool[0][1] if rng.random() < 0.7 else pool[rng.integers(len(pool))][1]
            sigma = 10 ** rng.uniform(-2.3, -0.4)
            Y = normalise(base + sigma * (rng.standard_normal((d, n)) + 1j * rng.standard_normal((d, n))))
            ps = (300, 1e3, 3e3, 1e4, 3e4) if sigma > 0.05 else (1e3, 3e3, 1e4, 3e4)
            Y = descend(Y, ps=ps)
            kind = "hop"
        stats[kind] += 1
        mu = coherence(Y)
        if mu < best_mu + 2e-3:
            Y = polish(Y, rounds=150)
            mu = coherence(Y)
        if mu < best_mu - 1e-12:
            stats["improve"].append((kind, round(time.time() - t0, 1), float(best_mu - mu)))
            best_mu, best_X = mu, Y
        pool.append((mu, Y))
        pool.sort(key=lambda t: t[0])
        # keep a small diverse elite: drop near-duplicates in coherence
        el = []
        for m, X in pool:
            if all(abs(m - m2) > 1e-9 for m2, _ in el):
                el.append((m, X))
        pool = el[:6]
    best_X = polish(best_X, rounds=400, r0=1e-4, tmax=20 + 0.03 * d * n)
    best_mu = coherence(best_X)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{d}x{n}.txt")
    prev = coherence(load(path, d, n)) if os.path.exists(path) else np.inf
    if best_mu < prev:
        save(path, best_X, best_mu)
    res = dict(d=d, n=n, slice=job["slice"], table=job["table"], start=float(start_mu),
               best=float(min(best_mu, prev)), this_run=float(best_mu), iters=it,
               time=round(time.time() - t0, 1), hops=stats["hop"], fresh=stats["fresh"],
               dele=stats["dele"], improvements=stats["improve"][-5:], seed=seed)
    return res


if __name__ == "__main__":
    import multiprocessing as mp
    jobs = json.load(open(sys.argv[1]))
    nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    log = os.path.join(HERE, "runs.jsonl")
    with mp.Pool(nproc, maxtasksperchild=1) as pool:
        for r in pool.imap_unordered(run_job, jobs, chunksize=1):
            with open(log, "a") as f:
                f.write(json.dumps(r) + "\n")
            print(json.dumps(r), flush=True)
