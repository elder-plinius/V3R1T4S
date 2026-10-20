#!/usr/bin/env python3
"""
STEP 5 SELF-BREAK for the A054759(15) candidate.
Assume the candidate is WRONG and try to break it with INDEPENDENT code written from
the definition (Eulerian orientations of the n x n torus = square ice / six-vertex at
the ice point), NOT reusing sixvertex.py.

Parts:
  A. Ground truth: FULL edge-orientation brute force for n=1,2,3 (enumerate every one of
     the 2^(2 n^2) orientations of all edges, check the ice rule at every vertex directly).
     No transfer matrix, no recurrence, no sector blocking.
  B. Independent transfer matrix: build T[a][b] by BRUTE enumeration of all 2^n horizontal
     edge configs per (a,b) and a DIRECT ice-rule check at each vertex (no h_{j+1} recurrence,
     no min/max closed form, no sector pre-blocking). a(n)=Tr(T^n) exact big integers.
     Run n=1..8, compare to https://oeis.org/A054759/b054759.txt
     (sha256: 26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada).
  C. Independent CRT: re-CRT the 23 recorded residues (RUN_A,RUN_B) with our own CRT and
     verify candidate % p == recorded residue for every prime.
  D. Growth gate, literal: a(n)^(1/n^2) vs Lieb ice constant W=(4/3)^(3/2), for n=14 and the
     candidate n=15, printed to high precision. No rounding in our favour.
"""
import os
import sys
from itertools import product, combinations
from functools import reduce
from decimal import Decimal, getcontext

CANDIDATE = 4310182149988584261406143524214457416387448

# Published terms from https://oeis.org/A054759/b054759.txt
# (sha256: 26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada)
BFILE = {
    1: 4, 2: 18, 3: 148, 4: 2970, 5: 143224, 6: 16448400, 7: 4484823396,
    8: 2901094068042, 9: 4448410550095612, 10: 16178049740086515288,
    11: 139402641051212392498528, 12: 2849295959501939989625992464,
    13: 137950545200232788276834783781648,
    14: 15844635835975276495290739119895808472,
}

# ---------------------------------------------------------------------------
# PART A: full edge-orientation brute force (totally independent ground truth)
# ---------------------------------------------------------------------------
# Torus n x n. Vertices (i,j), i,j in 0..n-1.
# Horizontal edge H[i][j] between vertex (i,j) and (i,(j+1)%n): bit=1 means points RIGHT
#   (out of (i,j), into (i,(j+1)%n)); bit=0 points LEFT.
# Vertical edge V[i][j] between vertex (i,j) and ((i+1)%n,j): bit=1 means points DOWN
#   (out of (i,j) toward (i+1,j), i.e. into (i+1,j)); bit=0 points UP (into (i,j)).
# Ice rule at (i,j): in-degree == 2 (equivalently out-degree==2).
#   In-edges at (i,j):
#     left  horizontal  H[i][(j-1)%n] == 1  (points right -> into (i,j))
#     right horizontal  H[i][j]       == 0  (points left  -> into (i,j))
#     up    vertical     V[(i-1)%n][j] == 1 (points down  -> into (i,j))
#     down  vertical     V[i][j]       == 0 (points up    -> into (i,j))
def brute_full(n):
    nH = n * n
    nV = n * n
    total = 0
    for Hbits in product((0, 1), repeat=nH):
        H = [list(Hbits[i*n:(i+1)*n]) for i in range(n)]
        for Vbits in product((0, 1), repeat=nV):
            V = [list(Vbits[i*n:(i+1)*n]) for i in range(n)]
            ok = True
            for i in range(n):
                for j in range(n):
                    indeg = 0
                    if H[i][(j-1) % n] == 1:
                        indeg += 1
                    if H[i][j] == 0:
                        indeg += 1
                    if V[(i-1) % n][j] == 1:
                        indeg += 1
                    if V[i][j] == 0:
                        indeg += 1
                    if indeg != 2:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                total += 1
    return total

# ---------------------------------------------------------------------------
# PART B: independent transfer matrix (brute horizontal, direct ice check)
# ---------------------------------------------------------------------------
def Tentry_brute(n, a, b):
    cnt = 0
    for h in product((0, 1), repeat=n):
        good = True
        for j in range(n):
            indeg = 0
            if a[j] == 1:
                indeg += 1
            if b[j] == 0:
                indeg += 1
            if h[j] == 1:
                indeg += 1
            if h[(j+1) % n] == 0:
                indeg += 1
            if indeg != 2:
                good = False
                break
        if good:
            cnt += 1
    return cnt

def mat_mul(A, B):
    N = len(A)
    out = [[0]*N for _ in range(N)]
    for i in range(N):
        Ai = A[i]
        Oi = out[i]
        for k in range(N):
            aik = Ai[k]
            if aik:
                Bk = B[k]
                for j in range(N):
                    Oi[j] += aik * Bk[j]
    return out

def mat_pow_trace(T, e):
    N = len(T)
    R = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    base = [row[:] for row in T]
    while e > 0:
        if e & 1:
            R = mat_mul(R, base)
        e >>= 1
        if e > 0:
            base = mat_mul(base, base)
    return sum(R[i][i] for i in range(N))

def a_via_brute_tm(n):
    states = list(product((0, 1), repeat=n))
    N = len(states)
    T = [[Tentry_brute(n, states[i], states[j]) for j in range(N)] for i in range(N)]
    return mat_pow_trace(T, n)

# ---------------------------------------------------------------------------
# PART C: independent CRT and residue check
# ---------------------------------------------------------------------------
def crt(residues, moduli):
    M = reduce(lambda x, y: x * y, moduli)
    x = 0
    for r, m in zip(residues, moduli):
        Mi = M // m
        inv = pow(Mi % m, -1, m)
        x = (x + r * Mi * inv) % M
    return x, M

def load_residues(path):
    runs = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tag, p, r = line.split('\t')
            runs.setdefault(tag, []).append((int(p), int(r)))
    return runs

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    default_resid = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "object", "residues.txt")
    resid_path = sys.argv[1] if len(sys.argv) > 1 else default_resid

    print("=== PART A: full edge-orientation brute force (ground truth) ===", flush=True)
    for n in (1, 2, 3):
        v = brute_full(n)
        ok = (v == BFILE[n])
        print(f"  n={n}: brute_full={v}  bfile={BFILE[n]}  MATCH={ok}", flush=True)
        assert ok, f"GROUND TRUTH MISMATCH at n={n}"

    print("=== PART B: independent brute-horizontal transfer matrix, n=1..8 ===", flush=True)
    for n in range(1, 9):
        v = a_via_brute_tm(n)
        ok = (v == BFILE[n])
        print(f"  n={n}: brute_TM={v}  bfile={BFILE[n]}  MATCH={ok}", flush=True)
        assert ok, f"INDEPENDENT TM MISMATCH at n={n}"

    print("=== PART C: independent CRT of recorded n=15 residues ===", flush=True)
    runs = load_residues(resid_path)
    for tag, pairs in runs.items():
        primes = [p for p, _ in pairs]
        res = [r for _, r in pairs]
        bad = [(p, r, CANDIDATE % p) for p, r in pairs if CANDIDATE % p != r]
        val, M = crt(res, primes)
        print(f"  {tag}: {len(primes)} primes, CRT={val}", flush=True)
        print(f"        CRT == candidate ? {val == CANDIDATE}", flush=True)
        print(f"        modulus bits = {M.bit_length()}  residue mismatches = {len(bad)}", flush=True)
        if bad:
            print(f"        MISMATCHES: {bad}", flush=True)
        assert val == CANDIDATE, f"{tag} CRT != candidate"
        assert not bad, f"{tag} residue mismatch"

    print("=== PART D: growth gate (literal) ===", flush=True)
    getcontext().prec = 60
    W = (Decimal(4) / Decimal(3)) ** (Decimal(3) / Decimal(2))
    print(f"  Lieb ice constant W=(4/3)^(3/2) = {W}", flush=True)
    for n, val in ((14, BFILE[14]), (15, CANDIDATE)):
        g = Decimal(val).ln() / Decimal(n * n)
        g = g.exp()
        gap = abs(g - W)
        print(f"  n={n}: a(n)^(1/n^2) = {g}", flush=True)
        print(f"        |gap to W| = {gap}   within 1e-3 ? {gap < Decimal('1e-3')}", flush=True)

    print("\nALL INDEPENDENT CHECKS PASSED (candidate survives self-break on A-C; see D for growth).", flush=True)
