# 2026-10-14-r-nikhil-213b4ac7: order-22 stable marriage instance with 12277568 stable matchings

## What
The explicit order-22 instance instance_n22.prefs (22 men and 22 women with complete strict preference lists, equal to the O[K2] doubling of the order-11 block published in a357271_1.txt) has 12277568 stable matchings according to three agreeing exact counts (a rotation-poset ideal DP, a visited-set lattice walk and a reverse-search enumeration, the last two re-checking every matching against the blocking-pair definition), which is strictly more than the order-22 value a(22) = 11221136 in the saved OEIS A357271 entry, whose linked instance file lists no order-22 instance.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (run from this folder). Expected last line: `PASS` (about 30 seconds on a laptop; needs a C compiler).
Main command inside it: `cc -O2 -o verify-it-yourself/smcount3 verify-it-yourself/smcount3.c -lm && ./verify-it-yourself/smcount3 enumerate object/instance_n22.txt`.
The object file object/instance_n22.txt is byte-identical to the claim folder's instance_n22.prefs named in the scope sentence (same sha256 213b4ac73bfb4218a4295514410d0d53b6a87f48e8f1462d61382579efdd5b37).

## Compared to
| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A357271 data line (Thurber 2002 compositions) | n = 22 | 11221136 | 12277568 | https://oeis.org/A357271 | 2026-10-14T15:20:43Z |

## Not claimed
- Nothing about the maximum f(22) itself: this is a lower bound (an explicit instance), not a proof of optimality.
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
