# fmm-catalogue-small-format-rank: partial win p1, <18,19,19> rank 3424 over Q

## What
The files in object/ define a bilinear scheme over Q for <18,19,19> (A 18x19 times B 19x19) with 3424 rank-one terms, each with three nonzero factors, satisfying all 42224004 Brent equations in exact arithmetic, and 3424 is strictly below the rank 3633 for (18,19,19) in the live fmm_sota.json and the rank 3816 on the live Lille page 18x19x19.html (both fetched for the claim at 2026-10-24T17:37:57Z and re-fetched unchanged at 2026-10-24T18:18:21Z) and below the 3633 of the only listed Lille construction Proj([[19, 0], [0]], <19x19x19:3633>) (index fetched 2026-10-24T15:58:56Z), so it meets partial win p1 of fmm-catalogue-small-format-rank and not the main criterion.

Claimed as partial win p1; the three skeptic reports are in panel/. The scheme comes from Khoruzhii, Serafin, Gelss and
Pokutta's published LITA 19x19x19 rank-3633 scheme by one exact one-slice restriction (208 terms vanish) and one
exact 2-reduction; the rebuild is deterministic and byte-identical (how-we-built-it/COMMANDS.md).

Path note: the panel files and how-we-built-it/PREREG.md refer to the run's claim folder and work folders. There,
claim/object/ is object/ (u.txt is shipped as object/u.part1.txt and object/u.part2.txt), CLAIM.md is README.md,
REPRODUCE.md is RUN_IT_YOURSELF.md, TABLE_RECORD.md is the-record-we-beat/RECORD.md, claim/verify-it-yourself/ is
verify-it-yourself/ and rebuild/ is how-we-built-it/ (its code in how-we-built-it/code/; LITA's
19x19x19_r3633.npz is fetched by how-we-built-it/COMMANDS.md, not shipped). Work files and folders named there
(self_break.md, panel_work/, claim_copy/, attempts/, data/, rounds/r1-16x16x17/) are not shipped. In
panel/gate.md and panel/criterion.md the confirmed_scope sentence originally read "The files in claim/object/";
panel/gate.md now reads "The files in object/", as in the What sentence above.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS`. Needs only python3 (standard library), no network; about 45 seconds on a laptop. It
joins object/u.part1.txt and object/u.part2.txt into u.txt (the 1 MB per-file limit), prints the three sha256 values
(u.txt 47419363...298a, the u.txt named in the panel files), checks all 42,224,004 Brent equations exactly, and runs
three exact random evaluations. RUN_IT_YOURSELF.md has the full expected output. The number 352800 that the checker
prints as "common denominator" (also quoted in panel/criterion.md) is the checker's scaling factor (the lcm over
terms of the product of each term's three factor denominators), not the least common denominator of the
coefficients, which is 8400 for U and 84 for V and W.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| fmm_sota.json (Lille catalogue digest) | [18, 19, 19] | 3633 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-24T17:37:57Z (unchanged at 18:05:47Z and 18:18:21Z) |
| Lille per-format page | <18x19x19> | 3816 | https://fmm.univ-lille.fr/18x19x19.html | 2026-10-24T17:37:57Z (unchanged at 18:05:47Z and 18:18:21Z) |
| Lille catalogue index | row 18x19x19 | 3633, construction Proj([[19, 0], [0]], <19x19x19:3633>) | https://fmm.univ-lille.fr/ | 2026-10-24T18:05:46Z |
| matmulcatalog docs/catalog.json (lowest other public value) | [18, 19, 19] | 3595 | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json | 2026-10-24T18:06:50Z |

The bar is matmulcatalog's 3595, the lowest public value found for this format; 3424 is 171 below it (and 209
below the 3633 in fmm_sota.json and the Lille index). How the values relate: the Lille 3633 is LITA's 19x19x19
rank-3633 scheme projected to 18x19x19 without dropping the terms that vanish. A plain coordinate projection (delete
row 9) drops 38 terms and gives 3595, the value matmulcatalog lists ("19x19x19 minus row 9"). This package instead
slices with a non-coordinate vector (-7 at index 9), so 208 terms vanish (3633 - 208 = 3425), and one exact
2-reduction then gives 3424.

Snapshots with sha256 and headers: the-record-we-beat/RECORD.md.

## Not claimed
- Not the main criterion: max(18,19,19) = 19 > 16. Partial win p1 only.
- Not the tensor rank of <18,19,19>: 3424 is an upper bound (a scheme with 3424 multiplications), not a proof that
  fewer are impossible.
- Not a ring upgrade: the coefficients are rationals (denominators up to 1200); nothing is claimed over Z or GF(2).
- Not a new method: the slice-and-reduce step uses the published LITA scheme, and earlier merged packages in this
  repository used the same LITA non-coordinate slice and exact reduction (see Credits). The new part is only the
  value 3424 for <18,19,19>, which no table, catalogue, pull request or paper we could read lists (lowest found: 3595).
- The run also built <18,18,19> at 3225 (fmm_sota.json 3355); it is not part of this package (one cell per package).

## Credits
- Kirill Khoruzhii, Luzian Serafin, Patrick Gelss and Sebastian Pokutta, Local Improvements to Trilinear Aggregation
  (LITA), https://github.com/khoruzhii/lita: the 19x19x19 rank-3633 scheme this one is restricted from.
- Alexandre Sedoglavic, the Lille fast matrix multiplication catalogue, https://fmm.univ-lille.fr/, and its digest
  https://github.com/sedoglavic/fmm_digest.
- Chatain Lacelle, matmulcatalog (arXiv 2606.13408), https://github.com/solven-eu/matmulcatalog.
- Perminov (dronperminov), FastMatrixMultiplication, https://github.com/dronperminov/FastMatrixMultiplication, and
  MerlijnW70/fmm-schemes, https://github.com/MerlijnW70/fmm-schemes (checked; neither covers max dimension 19).
- Earlier merged packages in known-knowns/faster-matrix-multiplication/ that used the same LITA slice-and-reduce
  method (a non-coordinate one-slice restriction of a LITA scheme followed by exact reduction):
  2026-10-14-anonymous-c6d1e0ab-710c8ff6 (13x15x15, rank 1763),
  2026-10-15-calgulbenkian-5b97769f (13x15x15, rank 1762),
  2026-10-15-anonymous-c6d1e0ab-9d6ef02f (14x16x16, rank 2117) and
  2026-10-15-anonymous-c6d1e0ab-0dee0512 (15x16x16, rank 2176). The new part of this package is the value 3424
  for <18,19,19>.
- Contributor: Abshalom Dayan (V3R1T4S run).
