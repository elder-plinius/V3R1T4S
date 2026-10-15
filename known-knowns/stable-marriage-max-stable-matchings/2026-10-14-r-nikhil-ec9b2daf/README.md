# 2026-10-14-r-nikhil-ec9b2daf: order-13 stable marriage instance with 7698 stable matchings

## What
The explicit order-13 stable marriage instance instance_n13.prefs (sha256 ec9b2daf4bafd04fb7118987cc88ae424471d1bb49f6e3632fb0367c9e3acc69; 13 men and 13 women, all 26 lists complete strict orderings of 1..13) has exactly 7698 stable matchings, as counted by every counter supplied in the claim and by an independent brute-force recount, which is strictly more than the 7123 stable matchings of the order-13 instance stated in the status-source file a357271_1.txt (OEIS A357271, fetched 2026-10-14) and named as the charter's n = 13 bar, so the charter criterion is met in the n = 13 cell only.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (run from this folder). Expected last line: `PASS` (about 5 seconds on a laptop; Python 3 only).
Main command inside it: `python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n13.txt --brute --expect 7698`.
The object file object/instance_n13.txt is byte-identical to the claim folder's instance_n13.prefs named in the scope sentence (same sha256 ec9b2daf4bafd04fb7118987cc88ae424471d1bb49f6e3632fb0367c9e3acc69).

## Compared to
| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A357271 instance file (Ong et al. 2025) | n = 13 | 7123 | 7698 | https://oeis.org/A357271/a357271_1.txt | 2026-10-14T15:18:18Z |

## Not claimed
- Nothing about the maximum f(13) itself: this is a lower bound (an explicit instance), not a proof of optimality.
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
