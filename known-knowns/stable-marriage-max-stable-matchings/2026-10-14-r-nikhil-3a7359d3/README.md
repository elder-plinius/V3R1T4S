# 2026-10-14-r-nikhil-3a7359d3: order-15 stable marriage instance with 27510 stable matchings

## What
The order-15 stable marriage instance in claim/instance_n15.prefs (sha256 3a7359d3db2f878cae106c2f527763c6abf150c0788b943de38661076ab539a8; 15 men and 15 women with complete strict preference lists) has exactly 27510 stable matchings according to four agreeing exact counters, two of them exhaustive enumerations, which is strictly more than the 27059 of the order-15 instance given as lb(15)=27059 in the OEIS A357271 instance file claim/a357271_1.txt (sha256 95735e185c5435e7cbe4c6753fe4e4ee120321457279f1f3283523654db5cd47), the n = 15 bar named in the charter criterion.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (run from this folder). Expected last line: `PASS` (about 15 seconds on a laptop; Python 3 only).
Main command inside it: `python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n15.txt --brute --expect 27510`.
The object file object/instance_n15.txt is byte-identical to the claim folder's instance_n15.prefs named in the scope sentence (same sha256 3a7359d3db2f878cae106c2f527763c6abf150c0788b943de38661076ab539a8).

## Compared to
| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A357271 instance file (Ong et al. 2025) | n = 15 | 27059 | 27510 | https://oeis.org/A357271/a357271_1.txt | 2026-10-14T15:18:18Z |

## Not claimed
- Nothing about the maximum f(15) itself: this is a lower bound (an explicit instance), not a proof of optimality.
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
