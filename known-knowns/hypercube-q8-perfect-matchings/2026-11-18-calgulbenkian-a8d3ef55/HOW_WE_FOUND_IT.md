# How We Found It (`contributor text, unverified`)

> Note: contributor text, unverified. For machine-verified evidence, run `sh verify-it-yourself/run_checks.sh`.

## Brief and Strategy
The exact number of perfect matchings of the 8-cube `Q_8` (`A005271(8)`) equals the permanent of a `128 x 128` 0–1 matrix and remains far beyond direct computation. Partial win `p2` of `hypercube-q8-perfect-matchings` asks for `A005271(8)` modulo an odd prime `p >= 3` without computing the full count. Since `|Aut(Q_8)| = 2^8 * 8! = 2^15 * 3^2 * 5 * 7`, we targeted the cyclic Sylow `5`-subgroup `P_5 = <(0 1 2 3 4)>` of prime order `5`, which was pre-registered in `PREREG.md` before any `Q_8` computation because `|P_5| = 5` is prime (requiring no subgroup-lattice inclusion-exclusion) and produces strictly positive fixed-point counts on `Q_6`, `Q_7`, and `Q_8`.

## What Worked
1. **Stabilizer-stratified orbit quotient (Engine A1):** Because coordinate permutations preserve Hamming weight parity and any `P_5`-invariant matching satisfies `Stab_{P_5}(u) = Stab_{P_5}(v)` across every matched edge `{u, v}`, `|Fix_{M(Q_8)}(P_5)|` splits into two disjoint strata: the `16` fixed vertices `Q_3 uplus Q_3` (`9^2 = 81` matchings) and `48` free `5`-orbits (`24` even and `24` odd), reducing `Q_8` from a `128 x 128` permanent to a `24 x 24` weighted permanent (`9,174,591,260,928`), giving `81 * 9,174,591,260,928 = 743,141,892,135,168 == 3 (mod 5)`.
2. **Direct 256-bit hypercube DP (Engine A2):** To avoid relying solely on the quotient-permanent reduction, we wrote a zero-shared-code Python engine operating directly on `256`-bit vertex masks of `Q_8`, ordering vertices by `(wt(v), v)` so the frontier stays narrow (`0.42s` runtime). Engine A1 and Engine A2 agreed to the last digit on `Q_5, Q_6, Q_7, Q_8` (`0, 836, 5741584, 743141892135168`), reproducing `A005271(5..7) mod 5 = 0, 1, 4`.

## What Did Not Reach Full Count (`p1`)
We also probed the folded 8-cube `FQ_8` (`128` vertices, `8`-regular bipartite, `p1`). While exact counts for `FQ_2..FQ_6` (`1, 3, 24, 705, 7114752`) and Sylow residues of `FQ_8` (`4 mod 7`, `0 mod 5`) were fast, the middle folded shell `min(w, 7-w) = 3` has `70` vertices (`>= 2^35` frontier states), and `p1` additionally requires reproducing full `A005271(7)` from scratch, exceeding a 4-thread / 4.5 GiB laptop budget.
