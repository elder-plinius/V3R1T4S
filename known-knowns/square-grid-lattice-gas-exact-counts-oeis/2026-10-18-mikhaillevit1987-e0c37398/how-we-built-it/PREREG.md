# PREREG — written 2026-10-18T10:09:30Z, before any n>=11 run

Criterion (verbatim): Success means the exact integer value of the first unknown term a(N) of A028420, A006506 or A063443, where N is one more than the largest index in the sequence's DATA and b-file re-fetched live immediately before claiming, computed by two independent runs that agree exactly (different primes/CRT moduli sets AND a different decomposition, e.g. row vs column sweep or a different state encoding, or one exact big-integer run), with the same code reproducing every published term for n <= N-1 exactly, and the result consistent with the known growth constant (a(N)^(1/N^2) within 1e-3 of the corresponding entropy constant).
Targeted enumerated partial win (verbatim): p1: The next unknown term(s) of A054759 (square ice on the n x n torus) or A027683 (hard squares on the n x n torus), same two-run and reproduction rules; A054759 is expected to be easy (row transfer matrix with 2^n states plus one tracked boundary edge) and is a partial only.

Object: a(n) of OEIS A054759 = number of Eulerian orientations of the n x n torus (2n^2 edges, in=out=2 at every vertex), offset 1.
Checker: attempts/transfer_matrix/code/ice.rs. trace(T^n) by cell-by-cell sweep modulo primes.
- Run A: left-to-right recursion, symmetry reduction by cyclic shifts x reflection x global arrow reversal, primes A in primes.txt (4 primes < 2^62).
- Run B: right-to-left recursion (different recurrence), cyclic shifts only, primes B in primes.txt (4 primes < 2^61), disjoint from A.
- Each run's 4 residues are CRT-combined; the CRT modulus (> 2^243 ~ 1.4e73 for A, > 2^239 for B) must exceed the bound 4^(n^2)... no: must exceed a(n) <= 2^(2n^2)? that is too loose; we use the bound a(n) <= 6^(n^2) (6 vertex types per vertex) only as an order check and require instead that A and B (independent moduli sets) give the SAME integer, which is impossible by chance unless both equal the true value below min(MA, MB).
Acceptance (all required):
1. Both runs reproduce every published term n = 1..14 (data/b054759.txt) exactly.
2. Runs A and B give the identical integer for n = 15 and n = 16.
3. Value < min(MA, MB)/10^6 (digit headroom) and a(n)^(1/n^2) is reported next to W = (4/3)^(3/2) (Lieb); the 1e-3 clause is reported, not used (p1 does not require it).
4. a(16) counts as new only if the live OEIS b-file / DATA still ends below 16 at claim time and no open PR/issue lists a(16).
Thresholds: exact integer equality only.
null_test: not needed because the claim is an explicit integer checked by two deterministic independent computations against published terms, no search or statistic.
