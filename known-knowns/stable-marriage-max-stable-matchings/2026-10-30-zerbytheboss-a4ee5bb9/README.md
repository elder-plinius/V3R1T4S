# Stable Marriage: Order-17 Instance with 206,728 Stable Matchings

## What
Explicit complete strict preference profile of order n = 17 for 17 men and 17 women admitting exactly 206,728 stable matchings, verified independently by Irving-Leather rotation poset closed-set enumeration and Gusfield stable matching lattice walk, strictly exceeding the composition-closure record and OEIS A357271 bound 200,832 by 5,896.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (run from this folder). Expected last line: `PASS`.
Main commands inside it:
- Method 1 (Python, standard library): `python3 -I verify-it-yourself/count_stable.py --prefs object/instance_n17.txt --expect 206728`
- Method 2 (C): compiled `smcount3` executing both rotation poset ideal enumeration and verified lattice walk.

The object file `object/instance_n17.txt` has SHA-256 `a4ee5bb91e8b1422d460df2330349a9e04140ebb017714b2bbb25398f60bd1c0`.

## Compared to
| table | cell | table value | our value | URL | fetched (UTC) |
|---|---|---|---|---|---|
| OEIS A357271 data line | n = 17 | 200832 | 206728 | https://oeis.org/A357271 | 2026-10-30T06:23:50Z |

Note on composition closure: Since 17 is a prime integer, no non-trivial composition of smaller published instances exists for n = 17. The composition closure record at verification time is precisely 200,832.

## Not claimed
- Nothing about the maximum f(17) itself: this is a lower bound (an explicit instance), not a proof of optimality.
- Nothing about any other order n; one cell per package.
- No claim that the instance is unique or minimal.

## Credits
- Donald E. Knuth, Mariages stables (1976) (posed the problem of maximizing stable matchings)
- Dan Gusfield, R. W. Irving, The Stable Marriage Problem: Structure and Algorithms, MIT Press (1989) (rotation poset theory and lattice traversal)
- Edward G. Thurber, "Concerning the maximum number of stable matchings in the stable marriage problem", Discrete Mathematics 248 (2002) 195-219 (the composition bounds and the baseline G17 construction)
- Dan Eilers, OEIS A357269 and A357271 sequences
- Ryan Ong, Bethany Ang, Abigail Ho, Dan Eilers, Justin Marks, Genti Buzi, IFoRE 2024 / OEIS 2025 (improved hill-climbing instances for small odd orders)
- Myunglae Jo, "A computer-assisted proof that the maximum number of stable matchings of order seven is 85", Zenodo (2026-10-13), https://doi.org/10.5281/zenodo.23329599
