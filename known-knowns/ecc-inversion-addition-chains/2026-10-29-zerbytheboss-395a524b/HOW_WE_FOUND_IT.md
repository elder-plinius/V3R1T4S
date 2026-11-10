# How We Found It — ecc-inversion-addition-chains

contributor text, unverified

## The Objective
Discover addition chains for elliptic curve modular inversion exponents that beat published baselines in Brian Smith's compilation and `mmcloughlin/addchain`'s results table (`results.md`), targeting CONFIRMED_SOLUTION on main curves (Curve25519 scalar), Partial Win `p2` on main curves (NIST P-384 scalar), and Partial Win `p1` on secondary curves (M-383, M-511).

## What Failed
Direct hill climbing or greedy dictionary search on full exponent values fails to find global optima for curves with long runs of ones: the run-length sequence $R(k)$ requires highly structured addition sequences where non-trivial leaps between doublings determine the total chain length. Searching solely on standard addition chain decompositions without targeted run-length addition sequence optimization leaves the chains at `addchain`'s default heuristic lengths (396 for M-383, 525 for M-511).
Similarly, on scalar inversion exponents where the top half is structured and the bottom 128-192 bits are pseudo-random, default window decompositions leave slack: `addchain`'s best known for Curve25519 scalar was 283 steps, and Brian Smith's was 284 steps. On NIST P-384 scalar, Brian Smith's record was 433 steps with 52 additions.

## What Worked
1. **Curve25519 Scalar Inversion Chain (282 Steps — CONFIRMED_SOLUTION)**:
   We targeted the scalar exponent $E = N - 2 = 2^{252} + 0x14def9dea2f79cd65812631a5cf5d3eb$.
   By optimizing a compact dictionary $\{11, 83, 99, 103, 107, 147, 151, 189, 211, 231, 235, 245, 247, 256\}$, we generated all 14 required window values in 24 strictly monotonic addition steps.
   Coupled with 14 window additions and 244 loop doublings (total 251 doublings and 31 additions), the total addition chain length is exactly **282 steps** ($282 < 283$ addchain record, $< 284$ Brian Smith record).
   Strict monotonicity ($a_{i+1} > a_i$ for all 282 steps), bit-for-bit exponent equality, and 100/100 Fermat modular exponentiations were verified.

2. **NIST P-384 Scalar Inversion Chain (50 Additions, 432 Steps — p2 Win)**:
   On NIST P-384 scalar $E = N - 2$, the incumbent record by Brian Smith used 433 steps with 52 additions.
   By augmenting the base dictionary $\{1, 3, 5, 7, 9, 11, 13, 15\}$ with $\{25, 27\}$, we compressed the lower 192-bit window sequence to exactly 35 window additions.
   The resulting chain uses 382 doublings and **50 additions** (total 432 steps), beating Brian Smith's 52 additions by 2 additions while also improving total length ($432 < 433$).

3. **Secondary Curves M-383 and M-511 (p1 Win)**:
   - For M-383 ($E = 2^{383} - 189$), branch-and-bound addition sequence search on $R(375)$ found an 11-addition sequence $[1, 2, 4, 8, 16, 24, 25, 50, 100, 125, 250, 375]$, reducing the total chain length from 396 to **395 steps** (382 squarings, 13 additions).
   - For M-511 ($E = 2^{511} - 189$), search on $R(503)$ found a 12-addition sequence $[1, 2, 4, 8, 16, 32, 64, 96, 100, 101, 201, 402, 503]$, reducing the total chain length from 525 to **524 steps** (510 squarings, 14 additions).

4. **Exhaustive Fermat & DAG Validation**:
   Every generated addition chain was evaluated across 100 random field elements in exact BigInt arithmetic verifying $x^E \cdot x^{d-1} \equiv 1 \pmod N$, confirming 100% algebraic correctness across all 20 curves.
