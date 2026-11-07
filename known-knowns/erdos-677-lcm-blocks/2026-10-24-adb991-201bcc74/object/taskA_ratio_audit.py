#!/usr/bin/env python3
"""Task A: audit completeness of deep_cf.admissible_r(k) against Lemma A, k = 3..25.

Independent generation (does not use deep_cf internals):
  (1) S_A(k): enumerate one sign in {-1,0,1} per LEVEL q = p^i < k with q not dividing k (Lemma A summands), build
      r = num/den as a pair of Python ints, reduce, keep 1 < r <= R(k), R(k) = lcm(1..k)/k computed from prime powers.
  (2) S_cnt(k) (refinement, subset of S_A): per prime p, the realisable d_p = sigma(s1) - sigma(s2) where
      sigma(s) = sum over levels q of #{multiples of q in s+1..s+k}, s over residues mod the largest level p^a < k
      (CRT makes primes independent). These are the r that the block counts alone can produce.
  (3) Brute force: every pair n < m <= NB with lcm(n+1..n+k) = lcm(m+1..m+k), k = 3..25; r = f(m)/f(n) must lie in
      S_cnt(k) and in admissible_r(k).
Then check S_A(k) subset of admissible_r(k) (a missing r would be a hole in R2), and report counts.
usage: taskA_ratio_audit.py NB
"""
import sys, math, itertools, hashlib
sys.dont_write_bytecode = True
DEEP = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
sys.path.insert(0, DEEP)
from fractions import Fraction
import deep_cf


def is_prime(p):
    if p < 2:
        return False
    d = 2
    while d * d <= p:
        if p % d == 0:
            return False
        d += 1
    return True


def R_of_k(k):
    """lcm(1..k)/k as (num, den) ints, lcm from prime powers p^floor(log_p k)"""
    L = 1
    for p in range(2, k + 1):
        if is_prime(p):
            q = p
            while q * p <= k:
                q *= p
            L *= q
    g = math.gcd(L, k)
    return L // g, k // g


def levels(k):
    """list of (p, q) with q = p^i < k, i >= 1, q not dividing k"""
    out = []
    for p in range(2, k):
        if is_prime(p):
            q = p
            while q < k:
                if k % q != 0:
                    out.append((p, q))
                q *= p
    return out


def S_A(k):
    lev = levels(k)
    Rn, Rd = R_of_k(k)
    res = set()
    for signs in itertools.product((-1, 0, 1), repeat=len(lev)):
        num = den = 1
        for (p, q), s in zip(lev, signs):
            if s == 1:
                num *= p
            elif s == -1:
                den *= p
        g = math.gcd(num, den)
        num //= g; den //= g
        # 1 < num/den <= Rn/Rd
        if num > den and num * Rd <= Rn * den:
            res.add((num, den))
    return res


def count_mult(s, k, q):
    """# multiples of q in s+1..s+k"""
    return (s + k) // q - s // q


def S_cnt(k):
    Rn, Rd = R_of_k(k)
    per_prime = []
    for p in range(2, k):
        if not is_prime(p):
            continue
        qs = [q for (pp, q) in levels(k) if pp == p]
        top = p
        while top * p < k:
            top *= p
        sig = set(sum(count_mult(s, k, q) for q in qs) for s in range(top))
        ds = sorted(set(a - b for a in sig for b in sig))
        per_prime.append((p, ds))
    res = set()
    for ds in itertools.product(*[d for _, d in per_prime]):
        num = den = 1
        for (p, _), d in zip(per_prime, ds):
            if d > 0:
                num *= p ** d
            elif d < 0:
                den *= p ** (-d)
        if num > den and num * Rd <= Rn * den:
            res.add((num, den))
    return res, per_prime


def main():
    NB = int(sys.argv[1])
    with open(DEEP + "/deep_cf.py", "rb") as fh:
        print("deep_cf.py sha256", hashlib.sha256(fh.read()).hexdigest())
    tot_missing = 0
    adm_all = {}
    for k in range(3, 26):
        adm = set((r.numerator, r.denominator) for r in deep_cf.admissible_r(k))
        adm_all[k] = adm
        A = S_A(k)
        C, per = S_cnt(k)
        missing = sorted(A - adm)
        extra = sorted(adm - A)
        tot_missing += len(missing)
        Lp = {}
        for p, q in levels(k):
            Lp[p] = Lp.get(p, 0) + 1
        narrow = {p: (min(ds), max(ds)) for p, ds in per if (min(ds), max(ds)) != (-Lp.get(p, 0), Lp.get(p, 0))
                  or len(ds) != 2 * Lp.get(p, 0) + 1}
        Rn, Rd = R_of_k(k)
        print("k=%2d R=%s levels=%d |S_A|=%d |admissible_r|=%d missing=%d extra=%d |S_cnt|=%d C_subset_A=%s "
              "narrowed_primes=%s" % (k, Fraction(Rn, Rd), len(levels(k)), len(A), len(adm), len(missing),
                                      len(extra), len(C), C <= A, narrow), flush=True)
        if missing:
            print("  MISSING", missing[:50])
    print("TOTAL missing over k=3..25:", tot_missing)
    # brute force
    seen = {}
    nbad = 0; npairs = 0
    for k in range(3, 26):
        groups = {}
        for x in range(0, NB + 1):
            L = 1
            for y in range(x + 1, x + k + 1):
                L = L * y // math.gcd(L, y)
            groups.setdefault(L, []).append(x)
        Cset, _ = S_cnt(k)
        for L, xs in groups.items():
            if len(xs) < 2:
                continue
            for i in range(len(xs)):
                for j in range(i + 1, len(xs)):
                    n, m = xs[i], xs[j]
                    fm = math.prod(range(m + 1, m + k + 1)); fn = math.prod(range(n + 1, n + k + 1))
                    g = math.gcd(fm, fn)
                    rr = (fm // g, fn // g)
                    npairs += 1
                    ok = rr in adm_all[k] and rr in Cset
                    if not ok:
                        nbad += 1
                        print("  BRUTE r not in set: k=%d n=%d m=%d r=%s" % (k, n, m, rr))
                    seen[k] = seen.get(k, 0) + 1
    print("brute force n<m<=%d: equal-lcm pairs per k %s; total %d; r outside sets: %d" % (NB, seen, npairs, nbad))


if __name__ == "__main__":
    main()
