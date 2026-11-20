#!/usr/bin/env python3
"""Independent enumeration of 3-invariant CW(n,81) first rows, n = 13*m, gcd(3,n)=1.

Originally written independently, before reading the package's liftjoin.c.

Rigor notes (only filters that are implied by the defining equation are used):
  * Contraction: b_j = sum_{i = j mod 13} a_i has periodic autocorrelation 81*delta on Z_13
    (image of A A^(-1) = 81 under Z[Z_n] -> Z[Z_13]).  All such b are found by brute force,
    both signs, no WLOG.
  * Shifts that are multiples of 13 only pair positions with equal residue mod 13, so
    C(13t) is a sum of per-group terms.  Used as an additive join key (64-bit random linear
    hash: false positives possible, false negatives impossible; every hash match is
    re-checked exactly).
  * Every surviving tuple is tested by exact integer autocorrelation at every lag
    1..floor(n/2); remaining lags are equal by symmetry. No floating-point filters.
"""
import itertools
import sys
import time

import numpy as np

K = 81
P = 3
Q = 13


def orbits_mul(n, p):
    seen = [False] * n
    out = []
    for x in range(n):
        if seen[x]:
            continue
        orb = []
        y = x
        while not seen[y]:
            seen[y] = True
            orb.append(y)
            y = (p * y) % n
        out.append(orb)
    return out


def contractions(m):
    """All 3-invariant integer sequences on Z_13 with |entry|<=m, autocorrelation 81*delta."""
    zorb = orbits_mul(Q, P)  # [0], then 4 orbits of size 3
    assert [len(o) for o in zorb] == [1, 3, 3, 3, 3]
    res = []
    lim0 = min(m, 9)
    limc = min(m, 5)
    for b0 in range(-lim0, lim0 + 1):
        for cs in itertools.product(range(-limc, limc + 1), repeat=4):
            if b0 * b0 + 3 * sum(c * c for c in cs) != K:
                continue
            seq = [0] * Q
            seq[0] = b0
            for oi, c in enumerate(cs):
                for pos in zorb[oi + 1]:
                    seq[pos] = c
            if all(sum(seq[j] * seq[(j + t) % Q] for j in range(Q)) == 0 for t in range(1, Q)):
                res.append(tuple(seq))
    return zorb, sorted(set(res))


def run(n, verbose=True, stats=None):
    t0 = time.time()
    assert n % Q == 0 and n % P != 0
    m = n // Q
    orbs = orbits_mul(n, P)
    assert sum(len(o) for o in orbs) == n
    zorb, contr = contractions(m)
    res_gid = {}
    for gi, o in enumerate(zorb):
        for r in o:
            res_gid[r] = gi
    groups = [[] for _ in range(5)]
    for o in orbs:
        gids = {res_gid[i % Q] for i in o}
        assert len(gids) == 1
        groups[gids.pop()].append(o)
    if verbose:
        print(f"n={n} orbits={len(orbs)} per-group orbit counts={[len(g) for g in groups]} "
              f"contractions={len(contr)}", flush=True)

    nshift = m // 2 + 1  # shifts 13*t, t=0..m//2 (rest by symmetry)
    rng = np.random.default_rng(20261114)
    rmul = rng.integers(1, 2**63, size=nshift, dtype=np.uint64) * np.uint64(2) + np.uint64(1)

    V = []      # signings per group, (3^k, n) int8
    C = []      # exact per-group contribution to C(13t), (3^k, nshift) int64
    H = []      # additive hash of C
    RS = []     # residue sums mod 13, (3^k, 13)
    for g in range(5):
        k = len(groups[g])
        vals = np.array(list(itertools.product((-1, 0, 1), repeat=k)), dtype=np.int8)
        v = np.zeros((vals.shape[0], n), dtype=np.int8)
        for oi, o in enumerate(groups[g]):
            v[:, o] = vals[:, [oi]]
        c = np.zeros((v.shape[0], nshift), dtype=np.int64)
        v64 = v.astype(np.int64)
        for t in range(nshift):
            c[:, t] = (v64 * np.roll(v64, -Q * t, axis=1)).sum(axis=1)
        h = (c.astype(np.uint64) * rmul[None, :]).sum(axis=1, dtype=np.uint64)
        rs = np.zeros((v.shape[0], Q), dtype=np.int64)
        for r in range(Q):
            rs[:, r] = v64[:, r::Q].sum(axis=1)
        V.append(v); C.append(c); H.append(h); RS.append(rs)

    target_c = np.zeros(nshift, dtype=np.int64)
    target_c[0] = K
    target_h = (target_c.astype(np.uint64) * rmul).sum(dtype=np.uint64)

    tot_cand = 0
    tot_hash = 0
    tot_match = 0
    hits = []
    for ti, seq in enumerate(contr):
        seq = np.array(seq, dtype=np.int64)
        idx = []
        for g in range(5):
            res = zorb[g]
            ok = np.all(RS[g][:, res] == seq[res][None, :], axis=1)
            idx.append(np.nonzero(ok)[0])
        sizes = [len(x) for x in idx]
        if min(sizes) == 0:
            continue
        # left: groups 1,2 ; right: groups 0,3,4
        hl = (H[1][idx[1]][:, None] + H[2][idx[2]][None, :]).ravel()
        order = np.argsort(hl, kind="stable")
        hl_sorted = hl[order]
        n2 = sizes[2]
        h34 = (H[3][idx[3]][:, None] + H[4][idx[4]][None, :]).ravel()
        n4 = sizes[4]
        tmatch = 0
        for a0, i0 in enumerate(idx[0]):
            # Defined arithmetic modulo 2^64. Python masks the scalar subtraction
            # explicitly; the array subtraction uses NumPy's unsigned wraparound.
            residual = np.uint64((int(target_h) - int(H[0][i0])) & ((1 << 64) - 1))
            need = residual - h34
            lo = np.searchsorted(hl_sorted, need, side="left")
            hi = np.searchsorted(hl_sorted, need, side="right")
            tot_cand += need.size
            cnt = hi - lo
            nz = np.nonzero(cnt)[0]
            if nz.size == 0:
                continue
            rep_r = np.repeat(nz, cnt[nz])
            # positions in sorted left array
            starts = lo[nz]
            offs = np.arange(cnt[nz].sum()) - np.repeat(np.cumsum(cnt[nz]) - cnt[nz], cnt[nz])
            lpos = order[np.repeat(starts, cnt[nz]) + offs]
            i1 = idx[1][lpos // n2]
            i2 = idx[2][lpos % n2]
            i3 = idx[3][rep_r // n4]
            i4 = idx[4][rep_r % n4]
            tot_hash += i1.size
            # exact additive check
            csum = C[0][i0][None, :] + C[1][i1] + C[2][i2] + C[3][i3] + C[4][i4]
            good = np.all(csum == target_c[None, :], axis=1)
            i1, i2, i3, i4 = i1[good], i2[good], i3[good], i4[good]
            tmatch += i1.size
            # full check in batches
            B = 200000
            for s in range(0, i1.size, B):
                sl = slice(s, s + B)
                a = (V[0][i0][None, :].astype(np.int8) + V[1][i1[sl]] + V[2][i2[sl]]
                     + V[3][i3[sl]] + V[4][i4[sl]])
                # Exact integer rejection only; product in {-1,0,1}, sum int64.
                for lag in range(1, n // 2 + 1):
                    if not len(a):
                        break
                    corr = (a * np.roll(a, -lag, axis=1)).sum(axis=1, dtype=np.int64)
                    a = a[corr == 0]
                for row in a:
                    assert int((row.astype(np.int64)**2).sum()) == K
                    hits.append(row.copy())
        tot_match += tmatch
        if verbose:
            print(f"  target {ti+1}/{len(contr)} seq={tuple(int(x) for x in seq)} sizes={sizes} "
                  f"matches={tmatch} hits_so_far={len(hits)} t={time.time()-t0:.0f}s", flush=True)

    proper = 0
    primes = [r for r in range(2, n + 1) if n % r == 0 and all(r % d for d in range(2, r))]
    for row in hits:
        sup = np.nonzero(row)[0]
        if not any(len(set(int(x) % r for x in sup)) == 1 for r in primes):
            proper += 1
    print(f"RESULT n={n} contractions={len(contr)} lookups={tot_cand} hash_matches={tot_hash} "
          f"exact_matches={tot_match} hits={len(hits)} proper_hits={proper} "
          f"elapsed={time.time()-t0:.0f}s", flush=True)
    if hits:
        row = hits[0]
        print("  example:", "".join("+" if x > 0 else "-" if x < 0 else "0" for x in row))
    if stats is not None:
        stats.update(contractions=len(contr), exact_matches=tot_match, proper_hits=proper)
    return hits


def verify():
    """Fail closed unless controls and the target reproduce exactly."""
    from pathlib import Path
    expected = sorted(tuple(map(int, line.split())) for line in
                      (Path(__file__).resolve().parents[1] / 'object' /
                       'contractions.txt').read_text().splitlines() if line.strip())
    positive = sorted(row for row in contractions(16)[1] if sum(row) == 9)
    if len(positive) != 25 or positive != expected:
        raise ValueError('Independent contraction set differs from object')
    for n, expected_hits in ((91, 48), (104, 0), (208, 0)):
        stats = {}
        hits = run(n, verbose=False, stats=stats)
        if len(hits) != expected_hits:
            raise ValueError(f'n={n}: expected {expected_hits} solutions, got {len(hits)}')
        expected_stats = {91: (48, 9720), 104: (48, 0), 208: (50, 1499136)}[n]
        if (stats['contractions'], stats['exact_matches']) != expected_stats:
            raise ValueError(f'n={n}: unexpected contraction or exact-match count')
        if n == 91:
            rows = {tuple(int(x) for x in row) for row in hits}
            if (len(rows) != 48 or stats['proper_hits'] != 48 or
                    sum(sum(row) == 9 for row in rows) != 24 or
                    any(tuple(-x for x in row) not in rows for row in rows)):
                raise ValueError('Positive control lacks distinct proper sign-paired rows')
            # Independent scalar recheck of every positive-control row and lag.
            if any(sum(x*x for x in row) != K or
                   any(sum(row[j]*row[(j+t)%n] for j in range(n)) != 0
                       for t in range(1, n)) for row in rows):
                raise ValueError('Positive control failed scalar autocorrelation recheck')
    print('INDEPENDENT PASS: positive control, negative control, target')


if __name__ == "__main__":
    if sys.argv[1:] not in ([], ['--verify']):
        raise SystemExit('usage: independent.py [--verify]')
    verify()
