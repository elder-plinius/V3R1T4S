# fmm-catalogue-small-format-rank: partial win p1, <24,25,25> rank 7157 over Q

## What
The joined object files (sha256 u 0dd8ee872815..., v 2fa3c110aee7..., w 23207f290da5...) define a bilinear scheme over Q with exactly 7157 rank-one terms for <24,25,25> whose 225000000 Brent equations I verified exactly, and 7157 is strictly below both the live fmm_sota.json entry (7507) and the live Lille per-format page (8176) fetched 2026-10-25, is not a listed Lille construction, and is below every value for this format I found in those tables, the Lille index, matmulcatalog and the V3R1T4S pull requests, so it meets partial win p1 (not the main criterion).

Path note: the panel files, how-we-built-it/PREREG.md and verify-it-yourself/RECEIPTS.md refer to the run's claim folder, claim/. There, CLAIM.md is README.md as gated (same What sentence), REPRODUCE.md is RUN_IT_YOURSELF.md, and object/, verify-it-yourself/ and the-record-we-beat/ are the folders of the same names here. Work files and folders named in those files, in how-we-built-it/COMMANDS.md and in the-record-we-beat/FETCH_LOG.txt (STATEMENT.txt, panel/claim.sha256, cells/, data/, fetch_log.txt, and the save folders tables/, prs/ and lit/) are not shipped; the comparator records are in the-record-we-beat/. The band run named in COMMANDS.md and PREREG.md is the run that built the cells of this batch.

Claimed as partial win p1; the three skeptic reports are in panel/. The scheme is A 24x25 times B 25x25. It comes from Khoruzhii, Serafin, Gelss and Pokutta's published LITA 25^3 rank-7507 scheme by one exact non-coordinate one-slice restriction, followed by one exact 2-reduction. The rebuild was done twice and the two runs are byte-identical (how-we-built-it/COMMANDS.md).

Margin: 300 below the lowest public value for this format (7457), 350 below the two tables (7507). One fresh panel subagent per role (REPRODUCE, NOVELTY, CRITERION) judged all 12 cells of this batch (panel/gate.md).

## Check it yourself
From this folder, in a fresh shell (python3, standard library, no network; numpy only for the optional second checker):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. About 50 s wall for the whole script (check 1 about 47 s, check 2 about 3 s) on a laptop, peak memory about 1.0 GB resident (the stdlib checker; the numpy one needs less) (measured numbers: verify-it-yourself/RECEIPTS.md). The script joins the parts in object/ into u.txt, v.txt and w.txt, checks their sha256, then runs two exact checkers: check_brent_stdlib.py (python3 standard library only) checks all 225000000 Brent equations (24*25 * 25*25 * 24*25 index triples) in integer arithmetic after multiplying each factor matrix by its least common denominator, and evaluates the scheme on three random integer matrix pairs exactly; check_exact_np.py (numpy) is a separately written exact checker of the same equations, much faster, with its own exactness argument in its docstring (it is skipped with a message if numpy is not installed, and then the verdict rests on the first checker alone). The stdlib checker is the one from the <18,18,19> package (PR #714); that package's second stdlib checker (check_scheme_second.py) is not shipped here, to keep the batch to the two checkers above. This package's check_exact_np.py has sha256 prefix 3f9ebe84; the four later packages of the batch (<28,28,29> to <30,31,31>) ship a version with prefix 0eeb12c7 that adds an exact Python-integer path for terms too large for float64. RUN_IT_YOURSELF.md has the file format and the full expected output; how-we-built-it/COMMANDS.md rebuilds the object from LITA's published scheme.

## Compared to
| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| fmm_sota.json (Lille catalogue digest) | [24, 25, 25] | 7507 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-24T22:35:43Z (re-fetched by the criterion panelist 2026-10-25T09:09:45Z, byte-identical to the first fetch) |
| Lille catalogue index | row 24x25x25 | 7507, construction Proj([[25, 0], [0]], ⟨25×25×25:7507⟩ ) | https://fmm.univ-lille.fr/ | 2026-10-24T22:35:44Z (re-fetched 2026-10-25T09:09:46Z, byte-identical) |
| Lille per-format page | ⟨24×25×25⟩ | 8176 (The algorithm ⟨24×25×25:8176⟩ is the projection [[1, 0], [0]] of ⟨25×25×25:8359⟩ .) | https://fmm.univ-lille.fr/24x25x25.html | 2026-10-24T22:35:56Z (re-fetched 2026-10-25T09:09:47Z, byte-identical) |
| Lille pages for the other axis orders | - | HTTP 404 (sorted formats only) | https://fmm.univ-lille.fr/25x24x25.html, https://fmm.univ-lille.fr/25x25x24.html | 2026-10-24T22:35:58Z |
| matmulcatalog docs/catalog.json | [24, 25, 25] | 7457 (25x25x25 ∖[12||]); 7996 (25x25x26^ABC->BCA ∖[12|25|]); 8028 (25x26x26 ∖[14|25|25]); 8076 (25x25x25 ∖[24||]); 8088 (5x5x12→⟨12,5,5⟩ ⊗ˢ⟨2,5,5⟩) | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json | 2026-10-24T22:35:44Z (re-read 2026-10-25T09:09:56Z by the criterion panelist: lowest 7457; no scheme listed at or below 7157) |
| matmulcatalog generated/COVERAGE.md | - | no row (sections stop at max dimension 16) | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-24T22:35:45Z |
| Perminov docs/ranks.md, docs/additions.md, README, repository tree | - | no entry (formats up to 16x16x16) | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-24T22:35:45Z to 2026-10-24T22:36:00Z |
| MerlijnW70/fmm-schemes | - | no entry (up to 16) | https://github.com/MerlijnW70/fmm-schemes | 2026-10-24T22:36:01Z |
| khoruzhii/lita schemes listing | - | square schemes only (13^3 to 32^3), no rectangular scheme | https://github.com/khoruzhii/lita | 2026-10-24T22:36:02Z |
| V3R1T4S pull requests (all 691, open and closed) and main | - | no scheme or rank filed for the cell in any order | https://github.com/elder-plinius/V3R1T4S | 2026-10-24T22:36:11Z to 2026-10-24T22:38:05Z |

Lowest public value for <24,25,25> in any axis order: 7457. Details, the literature search and every request with its sha256: the-record-we-beat/RECORD.md and the-record-we-beat/FETCH_LOG.txt.

INDEX.csv's table_fetched_utc (2026-10-25T09:09:45Z) is the criterion panelist's re-fetch of fmm_sota.json; the primary fetches are at 2026-10-24T22:35Z.

### How 7157 relates to the listed values
- 7507 (tables) is the Lille and fmm_sota.json value: LITA's <25,25,25> rank 7507 projected (the Lille construction column writes Proj([[25, 0], [0]], ⟨25×25×25:7507⟩)); matmulcatalog derives 7457 from the same scheme by deleting the best row (index 12: 50 terms vanish; reproduced in how-we-built-it/slice_accounting_output.txt).
- From LITA's <25,25,25> rank 7507, plain coordinate projections (delete one index, drop the terms that vanish, no reductions) give at best 7457 for <24,25,25> (delete index 12: 50 terms vanish). This scheme uses a non-coordinate slice instead: the slice (row index shared by A and C; direction e* = (1,...,1,-10,1,...,1), -10 at index 12, on the A side and e_0 on the C side) kills 349 terms (312 on the A side, 37 on the C side, none on both): 7507 - 349 = 7158; one exact 2-reduction gives 7157. Total removed: 350.

## Prior work on this method
The LITA slice-and-absorb method is not new in this repository. Earlier p1 claims with this slice method (PRs #41 to #51) were closed unmerged by their author on 2026-10-14 (12:51Z), together with about 115 of that author's other early pull requests, including main-criterion claims refiled and merged the next day (#130, #164); no maintainer comment or verdict on them exists. No p1 claim of this method has been merged yet, but the repository's own TROPHY_CASE rows 44 to 48 are restrictions of LITA squares. The merged PRs #130, #164, #172 and #197 (2026-10-15 and 2026-10-16, from LITA 15^3 and 17^3), and the merged LITA-based claims #166, #175, #177, #178 and #179, were for formats with max dimension at most 16. PRs #708 (<18,19,19> rank 3424) and #714 (<18,18,19> rank 3225) are open sibling claims by the same contributor with the same method, from LITA 19^3. What is new here is this format's value 7157 and this scheme.

## Not claimed
- Not the main criterion: max(24,25,25) = 25 > 16. Partial win p1 only.
- Not the tensor rank of <24,25,25>: 7157 is an upper bound (a scheme with 7157 multiplications), not a proof that fewer are impossible.
- Not a ring upgrade: the coefficients are rationals (denominators up to 5994); nothing is claimed over Z or GF(2).
- Not a new method. The same LITA non-coordinate slice with exact absorption was used earlier in this repository: PRs #41 to #51 (earlier p1 claims with this slice method, closed unmerged by their author on 2026-10-14, with no maintainer comment or verdict) and the merged PRs #130, #164, #172 and #197 (2026-10-15 and 2026-10-16; from LITA 15^3 and 17^3), and, for the 19-family from LITA 19^3, PR #708 (<18,19,19> rank 3424) and PR #714 (<18,18,19> rank 3225), both open. Only the value 7157 for this format, with this scheme, is new here.
- Not the sibling cells of this batch (one cell per claim): <24,24,25> rank 6820.
- Reproducibility of the rebuild: The rebuild was done twice in the run (two separate rebuilds for N = 25) and the step JSON and text exports are byte-identical; how-we-built-it/COMMANDS.md lets you redo it.
- The Lille page for this format (8176) is older than the index; the claim does not rest on it alone, since 7157 is below every value in every source read.

## Corrections to the panel text
README.md, RUN_IT_YOURSELF.md and HOW_WE_FOUND_IT.md were revised after the gate (wording, credits, file names, the join command), and how-we-built-it/PREREG.md had only its run id removed; the object, the What sentence and the panel files are as gated.

- panel/gate.md says the earlier p1 claims #41 to #51 "were closed unmerged on 2026-10-14 with no comment on record". In fact they were closed by their own author on 2026-10-14 (12:51Z), together with about 115 of that author's other early pull requests, including claims refiled and merged the next day (#130, #164); no maintainer comment or verdict on them exists.

## Credits
- Kirill Khoruzhii, Luzian Serafin, Patrick Gelss and Sebastian Pokutta, Local Improvements to Trilinear Aggregation (LITA), https://github.com/khoruzhii/lita (manuscript in preparation): the exact 2-reduction step (LITA's README defines 2-reducibility and src/reduce.h implements it) and the <25,25,25> rank-7507 scheme this one is restricted from (schemes/25x25x25_r7507.npz at commit 472a79fbc8248423a97bebb3aacbc89e769b9b3e). LITA builds on Victor Pan's trilinear aggregation (V. Ya. Pan, FOCS 1978, https://doi.org/10.1109/SFCS.1978.34; Comput. Math. Appl. 1982, https://doi.org/10.1016/0898-1221(82)90037-2).
- The earlier V3R1T4S claims that used this LITA slice-and-absorb method: https://github.com/elder-plinius/V3R1T4S/pull/41, https://github.com/elder-plinius/V3R1T4S/pull/51, https://github.com/elder-plinius/V3R1T4S/pull/130, https://github.com/elder-plinius/V3R1T4S/pull/164, https://github.com/elder-plinius/V3R1T4S/pull/172 and https://github.com/elder-plinius/V3R1T4S/pull/197 (contributor credit anonymous-c6d1e0ab, and calgulbenkian for #197), and the same contributor's 19-family claims https://github.com/elder-plinius/V3R1T4S/pull/708 and https://github.com/elder-plinius/V3R1T4S/pull/714 (open sibling claims, same method).
- Manuel Kauers and Isaac Wood, Exploring the Meta Flip Graph for Matrix Multiplication, arXiv:2510.19787 (https://arxiv.org/abs/2510.19787) (projection edges between formats; the slices here are non-coordinate versions), and Manuel Kauers and Jakob Moosbauer, Flip Graphs for Matrix Multiplication, arXiv:2212.01175 (https://arxiv.org/abs/2212.01175) (reductions; the 2-reduction step used here is LITA's, credited above). Richard P. Brent, STAN-CS-70-157 (1970), for the Brent equations.
- Alexandre Sedoglavic, the Lille fast matrix multiplication catalogue, https://fmm.univ-lille.fr/, and its digest https://github.com/sedoglavic/fmm_digest (the source of fmm_sota.json, https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json).
- Benoit Chatain Lacelle, matmulcatalog (arXiv:2606.13408, https://arxiv.org/abs/2606.13408), https://github.com/solven-eu/matmulcatalog.
- Perminov (dronperminov), FastMatrixMultiplication, https://github.com/dronperminov/FastMatrixMultiplication, and MerlijnW70/fmm-schemes, https://github.com/MerlijnW70/fmm-schemes (checked; neither has a format with a dimension above 16, so neither covers max dimension 25).
- V3R1T4S, https://github.com/elder-plinius/V3R1T4S: the challenge repository and the bank target fmm-catalogue-small-format-rank.
- Contributor: Abshalom Dayan (V3R1T4S runs).
