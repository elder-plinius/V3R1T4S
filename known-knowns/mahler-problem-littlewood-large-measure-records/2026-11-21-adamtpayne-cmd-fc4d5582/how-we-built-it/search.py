#!/usr/bin/env python3
"""Tabu / iterated local search for Littlewood polynomials (coefficients +-1) of degree d with large
Mahler measure M(f) = prod max(1, |root|)   (leading coefficient +-1).

Fast objective: log M(f) = (1/2pi) int log|f(e^{it})| dt (Jensen), approximated by the mean of
log|f| at N roots of unity. Flipping coefficient k changes f(w) by -2 a_k w^k, so all d+1 single
flips are scored at once. Candidates are re-scored at the end with numpy roots; certification is a
separate step (certify.py).

usage: search.py d seconds [seed] [N]   -> prints the best polynomials found
"""
import sys, time
import numpy as np


def logM_roots(a):
    r = np.roots(a[::-1].astype(float))  # numpy wants highest degree first; a[k] = coeff of x^k
    return float(np.sum(np.log(np.maximum(1.0, np.abs(r)))))


def search(d, seconds, seed=1, N=1024, tenure=None, log=None, seeds=None):
    rng = np.random.default_rng(seed)
    L = d + 1
    j = np.arange(N)
    W = np.exp(2j * np.pi * np.outer(np.arange(L), j) / N)  # (L, N)
    tenure = tenure or max(3, L // 6)
    best_score, best = -1e9, None
    found = {}
    t_end = time.time() + seconds
    a = rng.choice([-1, 1], size=L)
    restarts = 0
    while time.time() < t_end:
        restarts += 1
        if seeds and (best is None or rng.random() < 0.3):
            a = np.array(seeds[rng.integers(len(seeds))])
            if best is not None or rng.random() < 0.5:
                idx = rng.choice(L, size=rng.integers(1, max(2, L // 6)), replace=False)
                a[idx] *= -1
        elif best is not None and rng.random() < 0.7:
            a = best.copy()  # perturb the incumbent (iterated local search)
            idx = rng.choice(L, size=rng.integers(2, max(3, L // 5)), replace=False)
            a[idx] *= -1
        else:
            a = rng.choice([-1, 1], size=L)
        F = a @ W
        cur = np.mean(np.log(np.abs(F) + 1e-300))
        tabu = np.zeros(L, dtype=int)
        run_best, run_a = cur, a.copy()
        stall = 0
        it = 0
        while stall < 6 * L and time.time() < t_end:
            it += 1
            cand = F[None, :] - 2 * a[:, None] * W  # (L, N)
            sc = np.mean(np.log(np.abs(cand) + 1e-300), axis=1)
            ok = tabu < it
            sc_masked = np.where(ok | (sc > run_best + 1e-12), sc, -1e9)  # aspiration
            k = int(np.argmax(sc_masked))
            F = cand[k]
            a[k] *= -1
            cur = sc[k]
            tabu[k] = it + tenure + rng.integers(0, 3)
            if cur > run_best + 1e-12:
                run_best, run_a, stall = cur, a.copy(), 0
            else:
                stall += 1
        if run_best > best_score - 1e-6:
            key = canonical(run_a)
            if key not in found:
                found[key] = run_best
        if run_best > best_score + 1e-12:
            best_score, best = run_best, run_a.copy()
            if log:
                print(f"  d={d} restart {restarts}: approx M = {np.exp(best_score):.9f}", file=log, flush=True)
    return best, best_score, found, restarts


def canonical(a):
    """Representative of the 8-element symmetry class {f(x), -f(x), f(-x), x^d f(1/x)} (same M)."""
    a = np.array(a)
    alt = np.array([(-1) ** k for k in range(len(a))])
    forms = []
    for b in (a, a[::-1]):
        for c in (b, b * alt):
            for s in (c, -c):
                forms.append(''.join('+' if x > 0 else '-' for x in s))
    return max(forms)


if __name__ == "__main__":
    d = int(sys.argv[1]); secs = float(sys.argv[2])
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    N = int(sys.argv[4]) if len(sys.argv) > 4 else 1024
    seeds = None
    if len(sys.argv) > 5:
        import re
        seeds = []
        for line in open(sys.argv[5]):
            m = re.match(r'^(\d+)\s+[\d.]+\s+[\d.]+\s+([+-]+)\s*$', line)
            if m and int(m.group(1)) == d:
                seeds.append([1 if ch == '+' else -1 for ch in m.group(2)])
        print(f"  {len(seeds)} seeds for d={d}", file=sys.stderr)
    best, sc, found, restarts = search(d, secs, seed, N, log=sys.stderr, seeds=seeds)
    top = sorted(found.items(), key=lambda kv: -kv[1])[:5]
    for key, s in top:
        a = np.array([1 if ch == '+' else -1 for ch in key])
        print(f"{d} {np.exp(logM_roots(a)):.12f} {np.exp(logM_roots(a))/np.sqrt(d+1):.6f} {key}  (restarts {restarts})")
