# How we found it (contributor text, unverified)

The brief was the V3R1T4S bank target tsasm-a005164-order-51-exact: compute A005164(25) by exact enumeration,
without the Hagendorf-Lienardy formula. OEIS stops at a(24) (2022).

What worked. We used the symmetries to reduce a TSASM of order 2n+1 to a symmetric n x n {-1,0,1} matrix on one
quadrant, with row prefix sums in {0,1} and row sums fixed by parity. The reduction was proved in the run and checked
against brute force for a(0..10), and its half-row part against Kuperberg's VSASM formula for n = 0..6. Two transfer
matrices were written on that quadrant: Program A (row-major) and Program B (column-major, different state encoding).
They ran modulo disjoint sets of 61-62-bit primes, and Program B also ran exactly modulo 2^128. Both reproduce
a(0..24) and agree on a(25) and a(26). An exact-integer Python run agreed as well. In the panel, an independent
skeptic wrote a height-function DP with a different reduction and got byte-identical a(0..26). The checker in
verify-it-yourself/ follows that route.

What failed or was dropped. Brute force beyond a(10) is too slow (about 60x per order). Burnside over all ASMs is
hopeless at these sizes. Dense Program B beyond n = 26 hit the memory limit. No structure was found in the 2-adic
valuations or residues mod 4. A mod-3 pattern is a live lead and is not claimed.
