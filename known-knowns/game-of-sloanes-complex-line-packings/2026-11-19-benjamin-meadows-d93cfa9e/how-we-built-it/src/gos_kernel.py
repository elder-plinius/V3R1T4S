"""Game of Sloanes round 2: low-coherence packings of n lines in C^d, one shard of cells.

Self-contained Kaggle CPU kernel. Every job is one cell (d, n) with a wall-clock budget; jobs
run in WORKERS processes. A job seeds its pool from the given packings (our file, the open-PR
packings, the live current-best file), polishes each seed, then iterates
  - basin hop: pool member + complex Gaussian noise, log-sum-exp L-BFGS at rising p;
  - fresh random start with the full p schedule (sometimes followed by alternating projection);
  - deletion: a (d, n+1) packing with one vector dropped; addition: a (d, n-1) packing plus one
    random vector;
and polishes candidates within 2e-3 of the incumbent by sequential LP on the active set.
Outputs in OUT: best/<cell>_j<k>.txt (best packing of each job), improved/<cell>.txt (float
coherence below bar - 5e-8; the exact checker decides), progress.jsonl, results.tsv.
"""
import base64, gzip, json, os, sys, time

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize, linprog
from scipy.sparse import coo_matrix

SHARD = "__SHARD__"
HOURS = float(os.environ.get("GOS_HOURS", "__HOURS__"))
WORKERS = int(os.environ.get("GOS_WORKERS", "4"))
JOBS = json.loads(gzip.decompress(base64.b64decode("__DATA__")).decode())
ON_KAGGLE = os.path.isdir("/kaggle/working")
OUT = "/kaggle/working" if ON_KAGGLE else os.path.abspath(os.environ.get("GOS_OUT", "out_local"))
T0 = time.time()
DEADLINE = T0 + HOURS * 3600


# ------------------------------------------------------------------ optimiser

def normalise(X):
    return X / np.linalg.norm(X, axis=0, keepdims=True)


def coherence(X):
    Y = normalise(X)
    G = np.abs(Y.conj().T @ Y)
    np.fill_diagonal(G, 0)
    return G.max()


def lse_obj(v, d, n, p):
    X = (v[: d * n] + 1j * v[d * n:]).reshape(d, n)
    nrm = np.linalg.norm(X, axis=0)
    Y = X / nrm
    G = Y.conj().T @ Y
    S = G.real ** 2 + G.imag ** 2
    np.fill_diagonal(S, -np.inf)
    m = S.max()
    E = np.exp(p * (S - m))
    Z = E.sum()
    f = m + np.log(Z) / p
    W = E / Z
    gY = 2 * Y @ (W * G)
    gX = (gY - Y * np.real(np.sum(Y.conj() * gY, axis=0))) / nrm
    return f, np.concatenate([gX.real.ravel(), gX.imag.ravel()])


def descend(X, ps=(30, 100, 300, 1000, 3000, 1e4, 3e4), iters=400):
    d, n = X.shape
    for p in ps:
        v = np.concatenate([X.real.ravel(), X.imag.ravel()])
        r = minimize(lse_obj, v, args=(d, n, p), jac=True, method="L-BFGS-B",
                     options=dict(maxiter=iters, gtol=1e-12, ftol=1e-15))
        X = normalise((r.x[: d * n] + 1j * r.x[d * n:]).reshape(d, n))
    return X


def altproj(X, mu, iters=200):
    d, n = X.shape
    Y = normalise(X)
    for _ in range(iters):
        G = Y.conj().T @ Y
        a = np.abs(G)
        G = G * np.where(a > mu, mu / np.maximum(a, 1e-300), 1.0)
        np.fill_diagonal(G, 1.0)
        w, V = np.linalg.eigh(G)
        w = np.clip(w[-d:], 0, None)
        Y = normalise((V[:, -d:] * np.sqrt(w)).conj().T)
    return Y


def polish(X, rounds=200, r0=1e-2, tmax=None):
    """Sequential LP on squared overlaps (min t s.t. linearised |G_jk|^2 <= t on the active set,
    tangent to the unit sphere, box trust region)."""
    d, n = X.shape
    tstart = time.time()
    if tmax is None:
        tmax = 5 + 0.01 * d * n
    stall = 0
    Y = normalise(X)
    iu = np.triu_indices(n, 1)
    best = coherence(Y) ** 2
    r = r0
    nv = 2 * d * n + 1
    er = np.repeat(np.arange(n), d)
    ec = (np.arange(d)[None, :] * n + np.arange(n)[:, None]).ravel()
    for _ in range(rounds):
        if time.time() - tstart > tmax or stall > 25:
            break
        G = Y.conj().T @ Y
        s = (np.abs(G) ** 2)[iu]
        m = s.max()
        idx = np.nonzero(s >= m - max(40 * r, 1e-6))[0]
        J, K = iu[0][idx], iu[1][idx]
        nc = len(idx)
        g = G[J, K]
        ck = np.conj(g)[:, None] * np.conj(Y[:, J]).T
        cj = g[:, None] * np.conj(Y[:, K]).T
        ar = np.arange(d)[None, :] * n
        R = np.repeat(np.arange(nc), d)
        rows = np.concatenate([R, R, R, R, np.arange(nc)])
        cols = np.concatenate([(ar + K[:, None]).ravel(), (ar + K[:, None]).ravel() + d * n,
                               (ar + J[:, None]).ravel(), (ar + J[:, None]).ravel() + d * n,
                               np.full(nc, nv - 1)])
        vals = np.concatenate([2 * ck.real.ravel(), -2 * ck.imag.ravel(),
                               2 * cj.real.ravel(), -2 * cj.imag.ravel(), -np.ones(nc)])
        A = coo_matrix((vals, (rows, cols)), shape=(nc, nv)).tocsr()
        Aeq = coo_matrix((np.concatenate([Y.T.real.ravel(), Y.T.imag.ravel()]),
                          (np.concatenate([er, er]), np.concatenate([ec, ec + d * n]))),
                         shape=(n, nv)).tocsr()
        cost = np.zeros(nv)
        cost[-1] = 1
        bounds = [(-r, r)] * (2 * d * n) + [(None, None)]
        try:
            res = linprog(cost, A_ub=A, b_ub=-s[idx], A_eq=Aeq, b_eq=np.zeros(n), bounds=bounds,
                          method="highs", options=dict(time_limit=max(1.0, 0.005 * d * n)))
        except Exception:
            break
        if res.status != 0 or res.x is None:
            r *= 0.5
            if r < 1e-12:
                break
            continue
        dx = res.x[:-1]
        Yn = normalise(Y + (dx[: d * n] + 1j * dx[d * n:]).reshape(d, n))
        new = coherence(Yn) ** 2
        stall = stall + 1 if new > best - 1e-13 else 0
        if new < best - 1e-16:
            pred = m - res.x[-1]
            Y, best = Yn, new
            if pred > 0 and (m - new) > 0.5 * pred:
                r = min(r * 2, 0.05)
        else:
            r *= 0.3
            if r < 1e-12:
                break
    return Y


def random_start(d, n, rng):
    return normalise(rng.standard_normal((d, n)) + 1j * rng.standard_normal((d, n)))


def from_vals(vals, d, n):
    v = np.asarray(vals, dtype=float)
    assert v.size == 2 * d * n
    return normalise((v[: d * n].reshape(n, d) + 1j * v[d * n:].reshape(n, d)).T)


def save(path, X):
    """Game of Sloanes layout: real parts vector by vector, then imaginary parts; 21 significant digits."""
    Y = normalise(X)
    d, n = Y.shape
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        for k in range(n):
            for i in range(d):
                f.write("%.20e\n" % Y[i, k].real)
        for k in range(n):
            for i in range(d):
                f.write("%.20e\n" % Y[i, k].imag)
    os.replace(tmp, path)


def log(rec):
    rec["t"] = round(time.time() - T0, 1)
    with open(os.path.join(OUT, "progress.jsonl"), "a") as f:
        f.write(json.dumps(rec) + "\n")
    print(json.dumps(rec), flush=True)


# ------------------------------------------------------------------ one job

def run_job(job):
    d, n, cell, k = job["d"], job["n"], job["cell"], job["k"]
    bar = float(job["bar"])
    t0 = time.time()
    end = min(t0 + job["budget"], DEADLINE - 120)
    rng = np.random.default_rng(1000003 * k + 7919 * d + n + int(job.get("seed", 0)))
    best_path = os.path.join(OUT, "best", "%s_j%d.txt" % (cell, k))
    imp_path = os.path.join(OUT, "improved", "%s_j%d.txt" % (cell, k))
    pool = []
    seed_mu = {}
    for s in job["seeds"]:
        X = from_vals(s["vals"], d, n)
        m0 = coherence(X)
        X = polish(X, rounds=200, r0=1e-4, tmax=20 + 0.02 * d * n)
        m1 = coherence(X)
        seed_mu[s["src"]] = [float(m0), float(m1)]
        pool.append((m1, X, s["src"]))
    parents = [from_vals(p["vals"], d, n + 1) for p in job.get("parents", [])]
    children = [from_vals(c["vals"], d, n - 1) for c in job.get("children", [])]
    if not pool:
        X = descend(random_start(d, n, rng))
        pool.append((coherence(X), X, "fresh"))
    pool.sort(key=lambda t: t[0])
    start_mu = pool[0][0]
    best_mu, best_X, best_src = pool[0]
    save(best_path, best_X)
    log(dict(ev="start", cell=cell, k=k, bar=bar, start=float(start_mu), start_src=best_src, seeds=seed_mu))
    stats = dict(hop=0, fresh=0, dele=0, add=0)
    improvements = []
    frac_fresh = job.get("frac_fresh", 0.15)
    it = 0
    last_log = time.time()
    while time.time() < end:
        it += 1
        u = rng.random()
        if parents and u < 0.12:
            P = parents[rng.integers(len(parents))]
            Y = np.delete(P, rng.integers(n + 1), axis=1)
            Y = Y + 0.02 * rng.random() * (rng.standard_normal((d, n)) + 1j * rng.standard_normal((d, n)))
            Y = descend(normalise(Y), ps=(300, 1e3, 3e3, 1e4, 3e4))
            kind, src = "dele", "dele"
        elif children and u < 0.18:
            C = children[rng.integers(len(children))]
            Y = np.concatenate([C, random_start(d, 1, rng)], axis=1)
            Y = Y + 0.02 * rng.random() * (rng.standard_normal((d, n)) + 1j * rng.standard_normal((d, n)))
            Y = descend(normalise(Y), ps=(100, 300, 1e3, 3e3, 1e4, 3e4))
            kind, src = "add", "add"
        elif u < 0.18 + frac_fresh:
            Y = descend(random_start(d, n, rng))
            if rng.random() < 0.25:
                Y2 = descend(altproj(Y, coherence(Y) * 0.99), ps=(1e3, 1e4, 3e4))
                if coherence(Y2) < coherence(Y):
                    Y = Y2
            kind, src = "fresh", "fresh"
        else:
            j = 0 if rng.random() < 0.6 else rng.integers(len(pool))
            base, src = pool[j][1], pool[j][2]
            sigma = 10 ** rng.uniform(-2.7, -0.4)
            Y = normalise(base + sigma * (rng.standard_normal((d, n)) + 1j * rng.standard_normal((d, n))))
            Y = descend(Y, ps=(300, 1e3, 3e3, 1e4, 3e4) if sigma > 0.05 else (1e3, 3e3, 1e4, 3e4))
            kind = "hop"
        stats[kind] += 1
        mu = coherence(Y)
        if mu < best_mu + 2e-3:
            Y = polish(Y, rounds=150)
            mu = coherence(Y)
        if mu < best_mu - 1e-12:
            improvements.append((kind, src, round(time.time() - t0, 1), float(best_mu - mu)))
            best_mu, best_X, best_src = mu, Y, src
            save(best_path, best_X)
            if best_mu < bar - 5e-8:
                save(imp_path, best_X)
            log(dict(ev="improve", cell=cell, k=k, mu=float(mu), kind=kind, src=src, gap=float(mu - bar)))
        pool.append((mu, Y, src))
        pool.sort(key=lambda t: t[0])
        el = []
        for m, X, s in pool:
            if all(abs(m - m2) > 1e-9 for m2, _, _ in el):
                el.append((m, X, s))
        pool = el[:6]
        if time.time() - last_log > 1800:
            last_log = time.time()
            log(dict(ev="tick", cell=cell, k=k, best=float(best_mu), gap=float(best_mu - bar), iters=it, **stats))
    fin = polish(best_X, rounds=400, r0=1e-4, tmax=20 + 0.03 * d * n)
    if coherence(fin) < best_mu:
        best_X, best_mu = fin, coherence(fin)
    save(best_path, best_X)
    if best_mu < bar - 5e-8:
        save(imp_path, best_X)
    res = dict(ev="done", cell=cell, k=k, d=d, n=n, bar=bar, start=float(start_mu), best=float(best_mu),
               gap=float(best_mu - bar), src=best_src, iters=it, time=round(time.time() - t0, 1),
               improvements=improvements[-8:], **stats)
    log(res)
    return res


def run_job_safe(job):
    try:
        return run_job(job)
    except Exception as e:  # one bad job must not stop the shard
        import traceback
        log(dict(ev="error", cell=job["cell"], k=job["k"], err=repr(e), tb=traceback.format_exc()[-2000:]))
        return dict(cell=job["cell"], k=job["k"], bar=float(job["bar"]), start=float("nan"), best=float("nan"),
                    gap=float("nan"), src="error", iters=0, time=0.0)


def write_table(results):
    with open(os.path.join(OUT, "results.tsv"), "w") as f:
        f.write("cell\tjob\tbar\tstart\tbest\tbest_minus_bar\tbest_src\titers\tseconds\n")
        for r in sorted(results, key=lambda r: (r["cell"], r["k"])):
            f.write("%s\t%d\t%.12f\t%.15f\t%.15f\t%.3e\t%s\t%d\t%.0f\n" % (
                r["cell"], r["k"], r["bar"], r["start"], r["best"], r["gap"], r["src"], r["iters"], r["time"]))


def main():
    import multiprocessing as mp
    for sub in ("best", "improved"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    jobs = sorted(JOBS, key=lambda j: j.get("wave", 0))
    if os.environ.get("GOS_ONLY"):  # local smoke test: a subset of cells with a short budget
        keep = os.environ["GOS_ONLY"].split(",")
        jobs = [dict(j, budget=float(os.environ.get("GOS_BUDGET", "30"))) for j in jobs if j["cell"] in keep and j["k"] == 0]
    log(dict(ev="kernel", shard=SHARD, hours=HOURS, workers=WORKERS, jobs=[(j["cell"], j["k"], j["budget"]) for j in jobs]))
    results = []
    with mp.get_context("fork").Pool(WORKERS, maxtasksperchild=1) as pool:
        for r in pool.imap_unordered(run_job_safe, jobs, chunksize=1):
            results.append(r)
            write_table(results)
    write_table(results)
    log(dict(ev="kernel_done", n=len(results)))


if __name__ == "__main__":
    main()
