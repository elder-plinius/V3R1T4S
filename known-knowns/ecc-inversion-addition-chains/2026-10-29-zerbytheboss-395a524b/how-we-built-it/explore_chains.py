#!/usr/bin/env python3
"""
Explore addition chains for the 12 secondary curves and 8 main curves.
Tests run-length factorization, continued fractions, and window decompositions.
"""

import sys

def bits(n):
    return bin(n)[2:]

def ones_run_cost(k, available_runs):
    """
    Cost in squarings and additions to build R(k) = 2^k - 1,
    given a dict of available_runs {length: (cost, chain_of_runs)}.
    R(a+b) = R(a) * 2^b + R(b) costs: b squarings + 1 addition.
    """
    pass

# Exponents
TARGETS = {
    # 12 Secondary Curves (p1 target: strictly less than baseline)
    'M-221': (231, '1ffffffffffffffffffffffffffffffffffffffffffffffffffffffb', 2**221-3, 2),
    'E-222': (233, '3fffffffffffffffffffffffffffffffffffffffffffffffffffff89', 2**222-117, 2),
    'Curve1174': (263, '7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff5', 2**251-9, 2),
    'E-382': (395, '3fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff95', 2**382-105, 2),
    'M-383': (396, '7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff43', 2**383-187, 2),
    'Curve41417': (426, '3fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffed', 2**414-17, 2),
    'M-511': (525, '7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff43', 2**511-187, 2),
    'P-192': (203, 'fffffffffffffffffffffffffffffffefffffffffffffffd', 2**192-2**64-1, 2),
    'P-224': (234, 'fffffffffffffffffffffffffffffffeffffffffffffffffffffffff', 2**224-2**96+1, 2),
    'Goldilocks': (460, 'fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffffffffffffffffffffffffffffffffffffffffffffffffffffd', 2**448-2**224-1, 2),
    'secp192k1': (205, 'fffffffffffffffffffffffffffffffffffffffeffffee35', 2**192-2**32-4553, 2),
    'secp224k1': (238, 'fffffffffffffffffffffffffffffffffffffffffffffffeffffe56b', 2**224-2**32-6803, 2),

    # 8 Main Curves (p2 target: fewer additions at same length, or shorter length)
    'Curve25519_F': (265, '7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeb', 2**255-19, 2),
    'P-256_F': (266, 'ffffffff00000001000000000000000000000000fffffffffffffffffffffffc', 2**256-2**224+2**192+2**96-1, 3),
    'P-384_F': (396, hex(2**384 - 2**128 - 2**96 + 2**32 - 4)[2:], 2**384-2**128-2**96+2**32-1, 3),
    'secp256k1_F': (269, 'fffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2c', 2**256-2**32-977, 3),
    'Curve25519_S': (283, '1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3eb', int('1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed', 16), 2),
    'P-256_S': (292, 'ffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc63254f', int('ffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551', 16), 2),
    'P-384_S': (433, 'ffffffffffffffffffffffffffffffffffffffffffffffffc7634d81f4372ddf581a0db248b0a77aecec196accc52971', int('ffffffffffffffffffffffffffffffffffffffffffffffffc7634d81f4372ddf581a0db248b0a77aecec196accc52973', 16), 2),
    'secp256k1_S': (290, 'fffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd036413f', int('fffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141', 16), 2),
}

for name, (bar, hex_e, N, d) in TARGETS.items():
    E = int(hex_e, 16)
    # verify E == N - d
    assert E == N - d, f"Mismatch for {name}: {E} != {N - d}"
    b = bin(E)[2:]
    print(f"Verified {name:15s}: E = N - {d}, bits = {len(b)}, weight = {b.count('1')}, bar = {bar}")
