#!/usr/bin/env python3
"""Standalone checker for the claim A002224(42) = 6072205049848081 (Python standard library only).

OEIS A002224: "Smallest prime p of form p = 8k+1 such that first n primes (p_1=2, ..., p_n) are quadratic residues
mod p."

  check.py object OBJECT.json
      property of the value: q = 1 mod 8; Euler's criterion p^((q-1)/2) = 1 mod q for the first 42 primes; least QNR;
      a Lucas primality certificate (q-1 fully factored, every factor proven prime by trial division).
  check.py minimality OBJECT.json SURVIVORS X
      SURVIVORS is the output of enum.c run with bound X >= value (every q = 1 mod 8 in [1, X] whose residue mod every
      odd prime <= 113 is a nonzero square, filtered by 2^(q-1) = 1 mod q, which every odd prime passes). Every line
      is re-tested here (deterministic Miller-Rabin, Euler's criterion); the least prime for n = 30..41 must equal the
      OEIS b-file terms, and the least prime with the first 42 primes as QRs must equal the value.
Exit status 0 and a final line OK on success; nonzero and a final line FAIL otherwise."""
import json, sys

DEFINITION = ("Smallest prime p of form p = 8k+1 such that first n primes (p_1=2, ..., p_n) are quadratic "
              "residues mod p.")
# A002224(30..41), from https://oeis.org/A002224/b002224.txt (b-file by Michael Hortmann), fetched 2026-11-27.
BFILE = {30: 196265095009, 31: 196265095009, 32: 2871842842801, 33: 2871842842801, 34: 2871842842801,
         35: 26437680473689, 36: 89436364375801, 37: 112434732901969, 38: 112434732901969,
         39: 112434732901969, 40: 178936222537081, 41: 178936222537081}

def primes_upto_count(k):
    out, c = [], 2
    while len(out) < k:
        if all(c % d for d in range(2, int(c ** 0.5) + 1)):
            out.append(c)
        c += 1
    return out

P = primes_upto_count(60)

def is_prime_td(n):                      # trial division, for small factors of q-1
    if n < 2: return False
    d = 2
    while d * d <= n:
        if n % d == 0: return False
        d += 1
    return True

def is_prime_mr(n):                      # deterministic for n < 3.317e24 (bases = first 13 primes)
    if n < 2: return False
    for p in P[:13]:
        if n % p == 0: return n == p
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in P[:13]:
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else:
            return False
    return True

def leading_qr(q):                       # number of leading primes that are QRs mod q (Euler's criterion)
    n = 0
    while n < len(P) and pow(P[n], (q - 1) // 2, q) == 1: n += 1
    return n

def fail(msg):
    print(msg); print("FAIL"); sys.exit(1)

def check_object(path):
    o = json.load(open(path))
    if o.get("sequence") != "A002224" or o.get("definition") != DEFINITION: fail("object: wrong sequence/definition")
    n, q = o["n"], int(o["value"])
    if n != 42: fail("object: n is %r, expected 42" % n)
    if q % 8 != 1: fail("object: q mod 8 = %d" % (q % 8))
    if q >= 3317044064679887385961981: fail("object: value outside the deterministic Miller-Rabin range")
    k = leading_qr(q)
    if k < n: fail("object: only the first %d primes are QRs mod q" % k)
    lq = P[k]
    if lq != o["least_quadratic_nonresidue"]: fail("object: least QNR is %d, object says %r" % (lq, o["least_quadratic_nonresidue"]))
    c = o["primality_certificate"]; a = c["witness"]
    prod = 1
    for f, e in c["q_minus_1_factorization"]:
        f = int(f)
        if not is_prime_td(f): fail("certificate: %d is not prime" % f)
        prod *= f ** e
    if prod != q - 1: fail("certificate: factorization does not multiply to q-1")
    if pow(a, q - 1, q) != 1: fail("certificate: a^(q-1) != 1 mod q")
    for f, e in c["q_minus_1_factorization"]:
        if pow(a, (q - 1) // int(f), q) == 1: fail("certificate: a^((q-1)/%s) = 1 mod q" % f)
    if not is_prime_mr(q): fail("object: Miller-Rabin says composite")
    print("object: q = %d, q mod 8 = 1, first %d primes are QRs (needs 42), least QNR %d, Lucas certificate valid, "
          "Miller-Rabin agrees" % (q, k, lq))
    print("OK")
    return q

def check_minimality(path, surv, X):
    q = check_object(path)
    X = int(X)
    if X < q: fail("minimality: bound X = %d is below the value" % X)
    best, nprime = {}, 0
    for line in open(surv):
        s = int(line.split()[0])
        if s > X or not is_prime_mr(s): continue
        if s % 8 != 1: fail("minimality: survivor %d is not 1 mod 8" % s)
        nprime += 1
        k = leading_qr(s)
        for m in range(30, k + 1):
            if m not in best or s < best[m]: best[m] = s
    print("minimality: %d primes among the survivors in [1, %d]" % (nprime, X))
    for m, v in BFILE.items():
        if best.get(m) != v: fail("calibration: least prime for n = %d is %s, b-file says %d" % (m, best.get(m), v))
    print("calibration: A002224(30..41) reproduced from 1, all equal to the b-file")
    if best.get(42) != q: fail("minimality: least prime with the first 42 primes QR is %s, not %d" % (best.get(42), q))
    print("minimality: least prime q = 1 mod 8 with the first 42 primes as QRs is %d" % q)
    print("OK")

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "object": check_object(sys.argv[2])
    elif len(sys.argv) == 5 and sys.argv[1] == "minimality": check_minimality(*sys.argv[2:])
    else: print(__doc__); print("FAIL"); sys.exit(2)
