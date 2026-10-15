# 2026-10-14-r-nikhil-2eeddab2: order-14 stable marriage instance with 24992 stable matchings

## What
The explicit order-14 stable marriage instance in instance_n14.prefs (sha256 2eeddab210507ca8fecf7cb18e88a27245dd861ab7497acfc0d023766cf76965; 14 men and 14 women, every list a complete strict permutation of 1..14) has exactly 24992 stable matchings by agreeing exact rotation-poset and exhaustive-enumeration counts, which is strictly more than 20176, the n = 14 term of OEIS A357271 as saved in A357271.txt (revision #23, May 26 2025) and the bar the criterion names for its n = 14 cell.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (run from this folder). Expected last line: `PASS` (about 5 seconds on a laptop; Python 3 only).
Main command inside it: `python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n14.txt --brute --expect 24992`.
The object file object/instance_n14.txt is byte-identical to the claim folder's instance_n14.prefs named in the scope sentence (same sha256 2eeddab210507ca8fecf7cb18e88a27245dd861ab7497acfc0d023766cf76965).

## Compared to
| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A357271 data line (Thurber 2002 compositions) | n = 14 | 20176 | 24992 | https://oeis.org/A357271 | 2026-10-14T15:20:43Z |

## Not claimed
- Nothing about the maximum f(14) itself: this is a lower bound (an explicit instance), not a proof of optimality.
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
