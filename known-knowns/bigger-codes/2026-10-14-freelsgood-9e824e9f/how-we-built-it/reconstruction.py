#!/usr/bin/env python3
"""
Standalone Zero-Dependency Reproducer & Verifier for the Constant-Weight Code Record:
    A(27, 6, 10) >= 13,026  (beating Brouwer's live table record 12,987g by +39 codewords)

Target ID in elder-plinius/V3R1T4S: constant-weight-codes
Live Status Source: https://aeb.win.tue.nl/codes/Andw.html (listed as 12987g-43529)

Mathematical Construction:
1. Constructs the 1-dimensional affine semilinear group G = A\\Gamma L(1, 27) of order
   27 * 26 * 3 = 2,106 acting on GF(27) = GF(3)[x] / (x^3 - x + 1).
2. Generates the 10-orbit base code C_base of size 12,987:
     - 4 orbits of size 2,106 (reps: 270194, 273325, 286102, 290529) -> 8,424 words
     - 1 orbit  of size 1,053 (rep:  40569)                          -> 1,053 words
     - 5 orbits of size   702 (reps: 275956, 289242, 292125, 308124, 804047) -> 3,510 words
     Total base size = 8,424 + 1,053 + 3,510 = 12,987 words.
3. Identifies the unique 702-element G-orbit (rep: 131583) that is 100% conflict-free
   (Hamming distance >= 6) with all 12,987 codewords of C_base, and whose internal
   conflict graph decomposes into 39 vertex-disjoint cliques K_18 (the 39 cosets of
   the 54-element subgroup {x -> +-x + b : b in GF(27)}).
4. Selects 1 codeword from each of the 39 disjoint K_18 cliques to obtain 39 mutually
   compatible free words, yielding M = 12,987 + 39 = 13,026 codewords.
"""

import hashlib
from itertools import combinations

BASE_ORBIT_REPS = [
    40569,   # orbit size 1053
    270194,  # orbit size 2106
    273325,  # orbit size 2106
    275956,  # orbit size  702
    286102,  # orbit size 2106
    289242,  # orbit size  702
    290529,  # orbit size 2106
    292125,  # orbit size  702
    308124,  # orbit size  702
    804047,  # orbit size  702
]

ADDED_39_FREE_WORDS = [
    131583, 523776, 1846791, 1865152, 14911495, 15208384, 15233080,
    19213604, 19239497, 22063196, 22102826, 22172833, 25740394, 25830044,
    27859217, 36772492, 36842082, 37274897, 38347926, 42287785, 42374228,
    43297034, 55199817, 69173304, 69814868, 69874954, 71619724, 71637218,
    73967777, 76637257, 76649106, 76695860, 86395026, 105259793, 105419556,
    117476920, 125857799, 126058944, 133955586,
]

def to_vec(a):
    return (a % 3, (a // 3) % 3, (a // 9) % 3)

def from_vec(v):
    return (v[0] % 3) + 3 * (v[1] % 3) + 9 * (v[2] % 3)

def gf27_add(a, b):
    va, vb = to_vec(a), to_vec(b)
    return from_vec((va[0] + vb[0], va[1] + vb[1], va[2] + vb[2]))

def gf27_mul(a, b):
    va, vb = to_vec(a), to_vec(b)
    res = [0] * 5
    for i in range(3):
        for j in range(3):
            res[i + j] += va[i] * vb[j]
    for i in range(4, 2, -1):
        c = res[i] % 3
        if c:
            res[i - 2] += c
            res[i - 3] += 2 * c
    return from_vec((res[0], res[1], res[2]))

def build_agammal_1_27():
    mul_tab = [[gf27_mul(a, b) for b in range(27)] for a in range(27)]
    add_tab = [[gf27_add(a, b) for b in range(27)] for a in range(27)]
    frob1 = [mul_tab[mul_tab[a][a]][a] for a in range(27)]
    frob2 = [frob1[frob1[a]] for a in range(27)]
    frobs = [[a for a in range(27)], frob1, frob2]
    perms = []
    for b in range(27):
        for m in range(1, 27):
            for f_idx in range(3):
                perms.append([add_tab[mul_tab[m][frobs[f_idx][x]]][b] for x in range(27)])
    return perms

def apply_perm(perm, mask):
    res = 0
    for i in range(27):
        if (mask >> i) & 1:
            res |= (1 << perm[i])
    return res

def rebuild_code():
    perms = build_agammal_1_27()
    code_set = set()
    for rep in BASE_ORBIT_REPS:
        for perm in perms:
            code_set.add(apply_perm(perm, rep))
    assert len(code_set) == 12987, f"Expected 12987 base words, got {len(code_set)}"
    for w in ADDED_39_FREE_WORDS:
        assert w not in code_set
        code_set.add(w)
    assert len(code_set) == 13026, f"Expected 13026 total words, got {len(code_set)}"
    return sorted(code_set)

def verify_code(words, n=27, d=6, w=10):
    assert len(words) == len(set(words)), "Duplicate codewords found!"
    for x in words:
        assert 0 <= x < (1 << n), f"Codeword {x} out of range!"
        assert x.bit_count() == w, f"Codeword {x} has weight {x.bit_count()} != {w}!"
    seen_8 = set()
    for idx, x in enumerate(words):
        bits = [i for i in range(n) if (x >> i) & 1]
        for comb8 in combinations(bits, 8):
            m8 = 0
            for b in comb8:
                m8 |= (1 << b)
            if m8 in seen_8:
                raise AssertionError(f"Distance violation (< 6) detected at word {idx}!")
            seen_8.add(m8)
    return True

if __name__ == "__main__":
    words = rebuild_code()
    print(f"Rebuilt {len(words)} codewords from 10 A\\Gamma L(1,27) orbits + 39 free words.")
    verify_code(words, n=27, d=6, w=10)
    print("Verification PASSED: all 13,026 words have length 27, weight 10, and pairwise Hamming distance >= 6!")
    payload = "".join(f"{w:027b}\n" for w in words).encode("utf-8")
    print(f"SHA-256 of A_27_6_10_size_13026.txt: {hashlib.sha256(payload).hexdigest()}")
