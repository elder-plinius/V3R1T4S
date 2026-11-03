# An order-9 stable marriage instance with 412 stable matchings (best published: 365)

## What
The order-9 instance claim/instance_n9.prefs (sha256 f8f0734081c8c613267257d617d9393d5ad591782b802beaa72c8b1639f35de1) has exactly 412 stable matchings, counted by brute force and by the rotation-poset method, which is strictly more than every published order-9 instance (max 365, Ong et al.) and every composition of published instances found (max 366, Z2^3 Latin order-8 ⊕ one pair block sum), and it contains no published order-7 or order-8 instance as a sub-instance.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (run from this folder). Expected last line: `PASS` (a few seconds on a laptop; Python 3 only, a C compiler optional for two extra counters).
Main command inside it: `python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n9.txt --brute --expect 412`.
The object file object/instance_n9.txt is byte-identical to the claim folder's instance_n9.prefs named in the scope sentence (same sha256 f8f0734081c8c613267257d617d9393d5ad591782b802beaa72c8b1639f35de1).

## Compared to
| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A357271 instance file (Ong et al. 2025) | n = 9 | 365 | 412 | https://oeis.org/A357271/a357271_1.txt | 2026-11-03T15:55:29Z |
| OEIS A357271 data line | n = 9 | 330 | 412 | https://oeis.org/A357271 | 2026-11-03T15:55:29Z |
| composition closure (block sums of published parts, panel's own search) | n = 9 | 378 | 412 | see panel/novelty.md | 2026-11-03T17:35:48Z |

The bank criterion uses the composition closure as the bar. The best composition the panel found was 378 (the order-8 Z2^3 Latin instance, 268, block-summed with one pair). This is a hill-climbed lower bound, not a proven maximum over all compositions. 412 is higher than every one of these values.

## Not claimed
- Nothing about the maximum f(9) itself: this instance is a lower bound, not a proof of optimality.
- No proof that no composition of published instances reaches 412. The composition values above come from search.
- Nothing about any other order n; one cell per package.
- No claim that the instance is unique, minimal or structurally special.

## Credits
- Contributor: GitHub account CharanRayudu (https://github.com/CharanRayudu), which submits this folder.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Dan Eilers (OEIS A357269 / A357271 maintainer): https://oeis.org/A357271
- Ryan Ong, Bethany Ang, Abigail Ho, Dan Eilers, Justin Marks, Genti Buzi, "Improved Hill Climbing for the Stable Marriage Problem", IFoRE 2024 poster, record instances for n = 7, 9, 11, 13, 15: https://oeis.org/A357271/a357271_1.txt
- Robert W. Irving, Paul Leather, "The complexity of counting stable marriages", SIAM J. Computing 15 (1986): https://doi.org/10.1137/0215048 (rotations, the lattice, the Latin-square instances such as the order-8 seed)
- Edward G. Thurber, "Concerning the maximum number of stable matchings in the stable marriage problem", Discrete Mathematics 248 (2002) 195-219: https://doi.org/10.1016/S0012-365X(01)00194-7
- M. Jo, order-7 instance with 85 stable matchings (Zenodo record 23329599): https://zenodo.org/records/23329599
- Dan Gusfield, Robert W. Irving, The Stable Marriage Problem: Structure and Algorithms (MIT Press, 1989)
- D. Gale, L. S. Shapley, "College admissions and the stability of marriage", American Mathematical Monthly 69 (1962): https://doi.org/10.2307/2312726
- The evaluator smcount3.c and checker count_stable.py are reused from the merged package known-knowns/stable-marriage-max-stable-matchings/2026-10-15-r-nikhil-ed514711 (r-nikhil)
