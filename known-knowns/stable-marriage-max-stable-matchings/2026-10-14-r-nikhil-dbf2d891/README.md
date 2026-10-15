# 2026-10-14-r-nikhil-dbf2d891: order-28 stable marriage instance with 2497797760 stable matchings

## What
instance_n28.prefs is a valid order-28 stable marriage instance (28 men and 28 women, every list a permutation of 1..28) that equals the O[K2] doubling applied twice to an order-7 instance with 85 stable matchings, and it has exactly 2497797760 stable matchings by three agreeing exact counters (the claim's memoised rotation-poset count, the claim's reverse-search enumeration with 0 unstable matchings, and an independent counter), which is strictly more than the n = 28 value a(28) = 2000043808 in the status source A357271.txt and than the 2369365120 stable matchings obtained by applying the same doubling twice to the status source's own order-7 instance in a357271_1.txt.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (run from this folder). Expected last line: `PASS` (about 10 seconds and 2 GB of memory for the memoised count; FULL=1 adds the 45-minute verified enumeration; needs a C compiler).
Main command inside it: `cc -O2 -o verify-it-yourself/smcount3 verify-it-yourself/smcount3.c -lm && MEMO_MAX_STATES=40000000 ./verify-it-yourself/smcount3 count object/instance_n28.txt 0`.
The object file object/instance_n28.txt is byte-identical to the claim folder's instance_n28.prefs named in the scope sentence (same sha256 dbf2d89155213b672ef7514493d16c7f02225a84dbcc31f4ae30068f085e1ad0).

## Compared to
| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A357271 data line (Thurber 2002 compositions) | n = 28 | 2000043808 | 2497797760 | https://oeis.org/A357271 | 2026-10-14T15:20:43Z |

## Not claimed
- Nothing about the maximum f(28) itself: this is a lower bound (an explicit instance), not a proof of optimality.
- Nothing about any other order n; one cell per package.
- No claim that the instance is unique, minimal or structurally special.

## Credits
- Dan Eilers (OEIS A357269 / A357271 maintainer): https://oeis.org/A357271
- Ryan Ong, Bethany Ang, Abigail Ho, Dan Eilers, Justin Marks, Genti Buzi, "Improved Hill Climbing for the Stable Marriage Problem", IFoRE 2024 poster, record instances for n = 7, 9, 11, 13, 15: https://oeis.org/A357271/a357271_1.txt
- Edward G. Thurber, "Concerning the maximum number of stable matchings in the stable marriage problem", Discrete Mathematics 248 (2002) 195-219: https://doi.org/10.1016/S0012-365X(01)00194-7 (the composition bounds in A357271)
- Robert W. Irving, Paul Leather, "The complexity of counting stable marriages", SIAM J. Computing 15 (1986) (rotations, the lattice)
- Dan Gusfield, Robert W. Irving, The Stable Marriage Problem: Structure and Algorithms, MIT Press (1989) (rotation poset theory used by the counters)
- Donald E. Knuth, Mariages stables (1976) (the order-2 and order-4 instances used in tests and products)
- Myunglae Jo, "A computer-assisted proof that the maximum number of stable matchings of order seven is 85", Zenodo (2026-10-13), https://doi.org/10.5281/zenodo.23329599 (the order-7 85-instance used as a block)
