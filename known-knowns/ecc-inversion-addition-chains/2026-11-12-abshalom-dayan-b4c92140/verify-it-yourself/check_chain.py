#!/usr/bin/env python3
"""Standalone checker for one addition chain (Python standard library only, no network).

Written from the definition in the V3R1T4S bank entry ecc-inversion-addition-chains:
an addition chain 1 = a_0, a_1, ..., a_L = E in which every a_i (i >= 1) equals a_j + a_k
for some j, k < i (j = k is a doubling). L counts every step, doublings and additions alike,
and not the starting 1. Here E = N - 2, the exponent that inverts modulo the prime N.

Cell: secp256k1 scalar inversion (N = the order n of the secp256k1 base point).

usage: python3 check_chain.py object/chain.txt
File format: two '#' header lines, then one line "j k" per step t = 1..L: a_t = a_j + a_k.
"""
import random
import sys

# N from the curve standard, written two independent ways.
N_FORMULA = 2**256 - 432420386565659656852420866394968145599   # SEC 2 version 2.0 section 2.4.1 (n), written as 2^256 minus a 129-bit number
N_HEX = int("fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141", 16)   # SEC 2 version 2.0 section 2.4.1, n in hexadecimal
# N - 2 as printed in the "N-d" row of addchain's doc/results.md, section "secp256k1 (Bitcoin) Scalar Inversion".
E_RESULTS_MD = int("fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd036413f", 16)
CLAIMED_LENGTH = 281
CLAIMED_DOUBLINGS = 251
LOWEST_PUBLIC_LENGTH = 282   # see the-record-we-beat/RECORD.md
HEADER = [
    "# secp256k1 scalar inversion exponent N-2 = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd036413f",
    "# addition chain, length 281; line t: i j means a[t] = a[i] + a[j], a[0] = 1",
]


def is_probable_prime(n):
    """Miller-Rabin with 40 fixed bases: a sanity check that N is the prime the standard says."""
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
              73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def fail(msg):
    print("CHECK: FAIL - " + msg)
    sys.exit(1)


def main(path):
    if N_FORMULA != N_HEX:
        fail("the two forms of N disagree")
    N = N_HEX
    E = N - 2
    if E != E_RESULTS_MD:
        fail("N - 2 differs from the exponent printed in results.md")
    if not is_probable_prime(N):
        fail("N is not prime")
    lines = open(path, encoding="ascii").read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if lines[:2] != HEADER:
        fail("header lines differ from the expected ones")
    steps = []
    for n, line in enumerate(lines[2:], 3):
        parts = line.split(" ")
        if len(parts) != 2 or not all(p.isdigit() and str(int(p)) == p for p in parts):
            fail("line %d is not two non-negative integers" % n)
        steps.append((int(parts[0]), int(parts[1])))
    a = [1]
    for t, (j, k) in enumerate(steps, 1):
        if not (j < t and k < t):
            fail("step %d uses an element that does not exist yet" % t)
        a.append(a[j] + a[k])
    L = len(steps)
    if a[-1] != E:
        fail("the last element is not N - 2")
    doublings = sum(1 for (j, k) in steps if j == k)
    print("exponent N - 2 = 0x%x (%d bits)" % (E, E.bit_length()))
    print("every one of the %d steps is a sum of two earlier elements; the last element equals N - 2" % L)
    print("length %d = %d doublings + %d additions" % (L, doublings, L - doublings))
    print("distinct elements: %d of %d; strictly increasing: %s" % (len(set(a)), len(a), all(x < y for x, y in zip(a, a[1:]))))
    if L != CLAIMED_LENGTH or doublings != CLAIMED_DOUBLINGS:
        fail("length or doubling count differs from the claimed %d (%d doublings)" % (CLAIMED_LENGTH, CLAIMED_DOUBLINGS))
    if not L < LOWEST_PUBLIC_LENGTH:
        fail("not strictly shorter than the lowest public length %d" % LOWEST_PUBLIC_LENGTH)
    print("strictly shorter than the lowest public length on record, %d, by %d" % (LOWEST_PUBLIC_LENGTH, LOWEST_PUBLIC_LENGTH - L))
    rng = random.Random(20261110)
    for _ in range(100):
        x = rng.randrange(1, N)
        p = [x]
        for (j, k) in steps:
            p.append(p[j] * p[k] % N)
        if p[-1] * x % N != 1:
            fail("x * x^E != 1 (mod N) for some x")
    print("x * x^E = 1 (mod N) for 100 nonzero x, following the chain step by step")
    print("CHECK: PASS")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "object/chain.txt")
