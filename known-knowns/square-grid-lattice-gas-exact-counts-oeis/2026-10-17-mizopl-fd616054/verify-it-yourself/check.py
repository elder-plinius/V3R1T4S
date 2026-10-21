#!/usr/bin/env python3
"""
Standalone checker for the A054759(15) claim, written from the definition.
Python standard library only (numpy is used ONLY for an optional extra n=15 recomputation
and is skipped cleanly if unavailable). Run from the package root:

    python3 verify-it-yourself/check.py

Prints 'PASS' (exit 0) or 'FAIL' (exit 1) as the last line.

A054759(n) = number of Eulerian orientations of the n x n torus grid, i.e. orientations of
all 2 n^2 edges with in-degree 2 (hence out-degree 2) at every vertex = square ice / the
six-vertex model at the ice point.
"""
import os
import sys
from itertools import product, combinations
from functools import reduce

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Published OEIS A054759 terms (offset 1), for the reproduction check.
BFILE = {
    1: 4, 2: 18, 3: 148, 4: 2970, 5: 143224, 6: 16448400, 7: 4484823396,
    8: 2901094068042, 9: 4448410550095612, 10: 16178049740086515288,
}

problems = []


def check(cond, msg):
    if not cond:
        problems.append(msg)
        print("  MISMATCH: " + msg)
    return cond


# --- read the claimed object ---
with open(os.path.join(ROOT, "object", "a054759_15.txt")) as f:
    VALUE = int(f.read().strip())


# --- A: ground-truth brute force n=1,2,3 (enumerate all edge orientations) ---
def brute_full(n):
    total = 0
    for Hbits in product((0, 1), repeat=n * n):
        H = [Hbits[i * n:(i + 1) * n] for i in range(n)]
        for Vbits in product((0, 1), repeat=n * n):
            V = [Vbits[i * n:(i + 1) * n] for i in range(n)]
            ok = True
            for i in range(n):
                for j in range(n):
                    indeg = (H[i][(j - 1) % n] == 1) + (H[i][j] == 0) \
                        + (V[(i - 1) % n][j] == 1) + (V[i][j] == 0)
                    if indeg != 2:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                total += 1
    return total


print("A. ground-truth brute force (all 2^(2n^2) orientations), n=1..3:")
for n in (1, 2, 3):
    v = brute_full(n)
    print("   n=%d: %d" % (n, v))
    check(v == BFILE[n], "brute force n=%d gave %d, expected %d" % (n, v, BFILE[n]))


# --- B: independent sector transfer matrix, pure-python modular, reproduce n=1..10 ---
def primes_below(bound, count):
    out = []
    x = bound - 1
    while len(out) < count and x > 2:
        p = True
        if x % 2 == 0:
            p = (x == 2)
        else:
            i = 3
            while i * i <= x:
                if x % i == 0:
                    p = False
                    break
                i += 2
        if p:
            out.append(x)
        x -= 1
    return out


def sector_T(n, k, p):
    combs = list(combinations(range(n), k))
    Ns = len(combs)
    bits = [[1 if j in c else 0 for j in range(n)] for c in combs]
    T = [[0] * Ns for _ in range(Ns)]
    for a in range(Ns):
        da = bits[a]
        for b in range(Ns):
            ub = bits[b]
            cur = 0
            mn = 0
            mx = 0
            for j in range(n - 1):
                cur += da[j] - ub[j]
                if cur < mn:
                    mn = cur
                if cur > mx:
                    mx = cur
            lo = max(0, -mn)
            hi = min(1, 1 - mx)
            c = hi - lo + 1
            T[a][b] = c % p if c > 0 else 0
    return T, Ns


def mat_mul_mod(A, B, p):
    N = len(A)
    out = [[0] * N for _ in range(N)]
    for i in range(N):
        Ai = A[i]
        Oi = out[i]
        for kk in range(N):
            aik = Ai[kk]
            if aik:
                Bk = B[kk]
                for j in range(N):
                    Oi[j] = (Oi[j] + aik * Bk[j]) % p
    return out


def trace_pow_mod(T, e, p):
    N = len(T)
    R = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    base = [row[:] for row in T]
    while e > 0:
        if e & 1:
            R = mat_mul_mod(R, base, p)
        e >>= 1
        if e > 0:
            base = mat_mul_mod(base, base, p)
    return sum(R[i][i] for i in range(N)) % p


def a_mod(n, p):
    tot = 0
    for k in range(n + 1):
        T, Ns = sector_T(n, k, p)
        if Ns == 0:
            continue
        tot = (tot + trace_pow_mod(T, n, p)) % p
    return tot % p


def crt(residues, moduli):
    M = reduce(lambda x, y: x * y, moduli)
    x = 0
    for r, m in zip(residues, moduli):
        Mi = M // m
        inv = pow(Mi % m, -1, m)
        x = (x + r * Mi * inv) % M
    return x, M


print("B. independent sector transfer matrix (pure python), reproduce n=1..10:")
rep_primes = primes_below(1 << 20, 4)  # 4 primes, product ~2^80 >> a(10) (64 bits)
for n in range(1, 11):
    res = [a_mod(n, p) for p in rep_primes]
    val, M = crt(res, rep_primes)
    ok = (val == BFILE[n])
    print("   n=%2d: %s  %s" % (n, val, "OK" if ok else "MISMATCH"))
    check(ok, "sector method n=%d gave %d, expected %d" % (n, val, BFILE[n]))


# --- C: verify the n=15 object against its saved residues (CRT + bound) ---
print("C. n=15 object vs saved residues (independent CRT + bound):")
runs = {}
with open(os.path.join(ROOT, "object", "residues.txt")) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        tag, pp, rr = line.split("\t")
        runs.setdefault(tag, []).append((int(pp), int(rr)))

all_primes = []
for tag, pairs in runs.items():
    primes = [p for p, _ in pairs]
    res = [r for _, r in pairs]
    all_primes.append(set(primes))
    val, M = crt(res, primes)
    bad = [(p, r) for p, r in pairs if VALUE % p != r]
    print("   %s: %d primes, CRT==object? %s, modulus bits=%d, residue mismatches=%d"
          % (tag, len(primes), val == VALUE, M.bit_length(), len(bad)))
    check(val == VALUE, "%s CRT (%d) != object value" % (tag, val))
    check(not bad, "%s has residue rows inconsistent with the object value: %s" % (tag, bad[:3]))
    check(M > VALUE * (1 << 64), "%s modulus does not exceed value*2^64 (CRT not bounded)" % tag)

if len(all_primes) >= 2:
    inter = set.intersection(*all_primes)
    print("   prime-set intersection across runs: %s" % (sorted(inter) or "empty"))
    check(not inter, "the two runs share primes (not independent prime sets)")

# --- D: optional extra — recompute one n=15 residue with numpy (gold-standard touch) ---
try:
    import numpy as np

    def _a_mod15_numpy(p, prime_list_tag, target_prime):
        # sector method with float64 BLAS (exact: entries<p<2^20, dim<=C(15,7)=6435, sum<2^53)
        n = 15
        tot = 0
        for k in range(n + 1):
            combs = list(combinations(range(n), k))
            Ns = len(combs)
            if Ns == 0:
                continue
            bits = np.zeros((Ns, n), dtype=np.int16)
            for idx, c in enumerate(combs):
                for pos in c:
                    bits[idx, pos] = 1
            cur = np.zeros((Ns, Ns), dtype=np.int16)
            mn = np.zeros((Ns, Ns), dtype=np.int16)
            mx = np.zeros((Ns, Ns), dtype=np.int16)
            for j in range(n - 1):
                sj = bits[:, j][:, None] - bits[:, j][None, :]
                cur = cur + sj
                np.minimum(mn, cur, out=mn)
                np.maximum(mx, cur, out=mx)
            cnt = np.minimum(1, 1 - mx) - np.maximum(0, -mn) + 1
            cnt[cnt < 0] = 0
            A = cnt.astype(np.float64)
            # A^15 mod p via repeated squaring
            R = None
            B = (A.astype(np.int64) % p).astype(np.float64)
            e = n
            while e > 0:
                if e & 1:
                    R = B.copy() if R is None else (np.rint(R @ B).astype(np.int64) % p).astype(np.float64)
                e >>= 1
                if e > 0:
                    B = (np.rint(B @ B).astype(np.int64) % p).astype(np.float64)
            tot = (tot + int(round(float(np.trace(R))))) % p
        return tot

    tp = sorted(runs["RUN_A"])[0][0]  # one RUN_A prime
    stored = dict(runs["RUN_A"])[tp]
    print("D. optional numpy recomputation of RUN_A residue mod %d (n=15):" % tp)
    got = _a_mod15_numpy(tp, "RUN_A", tp)
    print("   recomputed=%d  stored=%d  value%%p=%d  match=%s" % (got, stored, VALUE % tp, got == stored == VALUE % tp))
    check(got == stored == VALUE % tp, "numpy n=15 residue mod %d disagrees" % tp)
except ImportError:
    print("D. numpy not available: skipped the optional n=15 recomputation (stdlib checks stand).")

print()
if problems:
    print("FAIL")
    sys.exit(1)
print("PASS")
sys.exit(0)
