# fmm-catalogue-small-format-rank: partial win p1, <18,18,19> rank 3225 over Q

## What
object/u.txt, object/v.txt (object/v.part1.txt followed by object/v.part2.txt) and object/w.txt form an exactly verified bilinear scheme over Q for <18,18,19> with 3225 rank-one terms (no zero or mergeable terms), which is strictly below the rank 3355 for [18,18,19] in fmm_sota.json and in the Lille catalogue index (both re-fetched 2026-10-24T19:34Z) and below the 3524 on the Lille per-format page as recorded in the-record-we-beat/RECORD.md; this meets partial win p1 of fmm-catalogue-small-format-rank, not the main criterion.

Path note: the panel files refer to the run's claim folder, claim/. There, CLAIM.md is README.md as gated (same What sentence), REPRODUCE.md is RUN_IT_YOURSELF.md, and check_scheme.py (also named in verify-it-yourself/RECEIPTS.md) is verify-it-yourself/check_scheme_second.py. Work files named in this package are not shipped: panel/claim.sha256, rebuild_16x16x17.py, the data/ inputs of how-we-built-it/code/predict_p1_band.py, the earlier run's attempts/ and out/ files cited in how-we-built-it/PREREG.md, and the save folders tables/, prs/ and lit/ named in the-record-we-beat/FETCH_LOG.txt. After the gate, how-we-built-it/PREREG.md had only run and workspace names replaced by neutral wording.

Claimed as partial win p1; the three skeptic reports are in panel/. The scheme is A 18x18 times B 18x19. It comes from
Khoruzhii, Serafin, Gelss and Pokutta's published LITA 19x19x19 rank-3633 scheme by two exact non-coordinate
one-slice restrictions, each followed by one exact 2-reduction; the rebuild is deterministic and byte-identical
(how-we-built-it/COMMANDS.md).

Prior publication (disclosed by the novelty panelist): PR #708 by the same contributor (opened
2026-10-24T18:58:23Z, sibling cell <18,19,19> rank 3424) already published the value 3225 for this cell, and its
how-we-built-it/ already published the identical deterministic code (code/rebuild_lita_slices.py, engine.py,
convert.py, export_txt.py; the docstring of rebuild_lita_slices.py here has since gained two
"(not shipped)" marks, no code change) that rebuilds this exact scheme from LITA's 19x19x19 scheme. The scheme files themselves
(object/ here) are first filed in this package. Dated note for the record: value and generator first made public by
the contributor in #708 on 2026-10-24.

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: `PASS`. Needs only python3 (standard library), no network; about 75 seconds on a laptop, peak
memory about 1.2 to 1.4 GB. It joins object/v.part1.txt and object/v.part2.txt into v.txt (the 1 MB per-file limit),
checks the sha256 of u.txt (37ffaf4d...5eca), v.txt and w.txt, then runs two exact checkers: check_brent_stdlib.py
checks all 37,896,336 Brent equations in integer arithmetic (after clearing each factor matrix's least common
denominator: U 8400, V 84, W 84) plus three exact random evaluations, and check_scheme_second.py is a separately
written exact Brent checker. RUN_IT_YOURSELF.md has the full expected output; verify-it-yourself/RECEIPTS.md has a
real run.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| fmm_sota.json (Lille catalogue digest) | [18, 18, 19] | 3355 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-24T19:05:59Z (unchanged at 19:28:14Z and 19:34:29Z) |
| Lille catalogue index | row 18x18x19 | 3355, construction ⟨18×18×1:324⟩ + ⟨18×18×18:3031⟩ | https://fmm.univ-lille.fr/ | 2026-10-24T19:05:59Z (unchanged at 19:28:13Z and 19:34:28Z) |
| Lille per-format page | ⟨18×18×19⟩ | 3524 (Kronecker product ⟨18×9×19:1762⟩ ⊗ ⟨1×2×1:2⟩) | https://fmm.univ-lille.fr/18x18x19.html | 2026-10-24T19:05:59Z (unchanged at 19:28:13Z) |
| matmulcatalog docs/catalog.json | [18, 18, 19] | 3355 (also 3356, 3524) | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json | 2026-10-24T19:06:00Z (unchanged at 19:28:15Z) |
| Perminov FastMatrixMultiplication; MerlijnW70/fmm-schemes | - | no entry (formats up to 16) | https://github.com/dronperminov/FastMatrixMultiplication, https://github.com/MerlijnW70/fmm-schemes | 2026-10-24T19:06:01Z to 19:06:04Z |

Lowest value listed for <18,18,19> in any axis order by any table, catalogue, paper or other party's filing: 3355 (the Lille pages for 18x19x18 and 19x18x18 return 404;
the catalogue lists sorted formats only). Snapshots with sha256, headers and the full request log:
the-record-we-beat/RECORD.md and the-record-we-beat/FETCH_LOG.txt. INDEX.csv's table_fetched_utc (2026-10-24T19:34:29Z) is
a panel re-fetch; the primary fetches are at 2026-10-24T19:05:59Z.

How 3225 relates to the listed values: 3355 is the block sum ⟨18×18×1:324⟩ + ⟨18×18×18:3031⟩. Plain coordinate
projections of LITA's <19,19,19> rank 3633 give at best 3557 for this format, and deleting one column of the sibling
3424 scheme gives 3395, both above 3355. Here slice 1 (direction e* = (1,...,1,-7,1,...,1), -7 at index 9) kills 208
terms (180 + 28) and one 2-reduction gives 3424; slice 2 kills 198 terms (19 + 179) and one 2-reduction gives 3225.
Total removed: 208 + 1 + 198 + 1 = 408 = 3633 - 3225.

## Not claimed
- Not the main criterion: max(18,18,19) = 19 > 16. Partial win p1 only.
- Not the tensor rank of <18,18,19>: 3225 is an upper bound (a scheme with 3225 multiplications), not a proof that
  fewer are impossible.
- Not a ring upgrade: the coefficients are rationals (denominators up to 1200); nothing is claimed over Z or GF(2).
- Not a new method. The same LITA non-coordinate slice with exact absorption was used earlier in this repository:
  PRs #41 and #51 (opened 2026-10-14, closed by their author the same day; from LITA 17^3 and 18^3) and the merged
  PRs #130, #164, #172 and #197 (2026-10-15 and 2026-10-16; from LITA 15^3 and 17^3). These are examples, not all
  earlier uses: this exact two-step recipe (slice with e = (1,...,-5,...,1), f = e_0, then e = e_0,
  f = (1,...,-5,...,1), with absorption) was first published in this repository's faster-matrix-multiplication family
  release of 2026-10-12 (known-knowns/faster-matrix-multiplication/README.md, <14,14,15>:1716 from LITA 15^3). Also
  related: #44 (<16,16,17> 2392, the N = 17 analogue of this cell) and the merged #166, #168, #175, #177, #178 and #179.
- Not first publication of the value or of the generator. PR #708 (same contributor, opened 2026-10-24T18:58:23Z)
  already published the value 3225 for this cell and, in its how-we-built-it/, the identical deterministic code that
  rebuilds this exact scheme from LITA 19^3. What is first filed here are the scheme files in object/. In this
  repository's #164 to #197 precedent, a value first seen in an earlier pull request's build log was later submitted
  and merged.
- Not the <18,19,19> value: that cell is PR #708 and is not part of this package (one cell per package).

## Corrections to the panel text
- panel/novelty.md quotes the earlier wording of README.md ("Not a new method" bullet) and of
  the-record-we-beat/RECORD.md ("The scheme itself has not been filed anywhere"). Both files were revised after the
  gate and now carry the #708 disclosure that panel/novelty.md asks for; the object and the What sentence did not
  change. panel/novelty.md was reissued after the gate read (login redacted, a placeholder rephrased; findings and
  verdict unchanged), as panel/gate.md records.
- check_scheme_second.py prints "common denominator 352800" (RUN_IT_YOURSELF.md, verify-it-yourself/RECEIPTS.md and
  panel/reproduce.md quote it); that number is the checker's scaling factor. The least common denominators are
  U 8400, V 84 and W 84.

## Credits
- Kirill Khoruzhii, Luzian Serafin, Patrick Gelss and Sebastian Pokutta, Local Improvements to Trilinear Aggregation
  (LITA), https://github.com/khoruzhii/lita (manuscript in preparation): the <19,19,19> rank-3633 scheme this one is
  restricted from (schemes/19x19x19_r3633.npz at commit 472a79fbc8248423a97bebb3aacbc89e769b9b3e), and the exact
  2-reduction step (LITA's README defines 2-reducibility and src/reduce.h implements it). LITA builds on Victor Pan's
  trilinear aggregation.
- The earlier V3R1T4S claims that used this LITA slice-and-absorb method: https://github.com/elder-plinius/V3R1T4S/pull/41,
  https://github.com/elder-plinius/V3R1T4S/pull/51, https://github.com/elder-plinius/V3R1T4S/pull/130,
  https://github.com/elder-plinius/V3R1T4S/pull/164, https://github.com/elder-plinius/V3R1T4S/pull/172 and
  https://github.com/elder-plinius/V3R1T4S/pull/197 (contributor credit anonymous-c6d1e0ab, and calgulbenkian for
  #197), this repository's faster-matrix-multiplication family release of 2026-10-12, which first published the
  two-step recipe used here, the related #44, #166, #168, #175, #177, #178 and #179, and the sibling claim #708 (https://github.com/elder-plinius/V3R1T4S/pull/708, same contributor).
- Manuel Kauers and Isaac Wood, Exploring the Meta Flip Graph for Matrix Multiplication, arXiv:2510.19787
  (projection edges between formats; the slices here are non-coordinate versions), and Manuel Kauers and Jakob
  Moosbauer, Flip Graphs for Matrix Multiplication, arXiv:2212.01175 (flip-graph reductions in general; the
  2-reduction step used here is LITA's, credited above). Richard P. Brent, STAN-CS-70-157 (1970), for the Brent equations.
- Alexandre Sedoglavic, the Lille fast matrix multiplication catalogue, https://fmm.univ-lille.fr/, and its digest
  https://github.com/sedoglavic/fmm_digest.
- Benoit Chatain Lacelle, matmulcatalog (arXiv 2606.13408), https://github.com/solven-eu/matmulcatalog.
- A. I. Perminov (dronperminov), FastMatrixMultiplication, https://github.com/dronperminov/FastMatrixMultiplication, and
  MerlijnW70/fmm-schemes, https://github.com/MerlijnW70/fmm-schemes (checked; neither covers max dimension 19).
- Contributor: Abshalom Dayan (V3R1T4S runs).
