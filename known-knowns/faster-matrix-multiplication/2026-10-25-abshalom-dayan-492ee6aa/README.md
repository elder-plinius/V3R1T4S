# fmm-catalogue-small-format-rank: partial win p1, <22,22,23> rank 5423 over Q

## What
The joined object files (sha256 u 492ee6aa9886..., v 3d78b1a87e54..., w 477a6d278146...) define a bilinear scheme over Q with exactly 5423 rank-one terms for <22,22,23> whose 123921424 Brent equations I verified exactly, and 5423 is strictly below both the live fmm_sota.json entry (5625) and the live Lille per-format page (6050) fetched 2026-10-25, is not a listed Lille construction, and is below every value for this format I found in those tables, the Lille index, matmulcatalog and the V3R1T4S pull requests, so it meets partial win p1 (not the main criterion).

Path note: the panel files, how-we-built-it/PREREG.md and verify-it-yourself/RECEIPTS.md refer to the run's claim folder, claim/. There, CLAIM.md is README.md as gated (same What sentence), REPRODUCE.md is RUN_IT_YOURSELF.md, and object/, verify-it-yourself/ and the-record-we-beat/ are the folders of the same names here. Work files and folders named in those files, in how-we-built-it/COMMANDS.md and in the-record-we-beat/FETCH_LOG.txt (STATEMENT.txt, panel/claim.sha256, cells/, data/, fetch_log.txt, and the save folders tables/, prs/ and lit/) are not shipped; the comparator records are in the-record-we-beat/. The band run named in COMMANDS.md and PREREG.md is the run that built the cells of this batch.

Claimed as partial win p1; the three skeptic reports are in panel/. The scheme is A 22x22 times B 22x23. It comes from Khoruzhii, Serafin, Gelss and Pokutta's published LITA 23^3 rank-6009 scheme by two exact non-coordinate one-slice restrictions, each followed by one exact 2-reduction; the first restriction passes through the sibling <22,23,23> scheme (a separate package of this batch). The rebuild was done twice and the two runs are byte-identical (how-we-built-it/COMMANDS.md).

Margin: 202 below the lowest public value for this format (5625), 202 below the two tables (5625). One fresh panel subagent per role (REPRODUCE, NOVELTY, CRITERION) judged all 12 cells of this batch (panel/gate.md).

## Check it yourself
From this folder, in a fresh shell (python3, standard library, no network; numpy only for the optional second checker):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. About 46 s wall for the whole script (check 1 about 43 s, check 2 about 2 s) on a laptop, peak memory about 1.3 GB resident (the stdlib checker; the numpy one needs less) (measured numbers: verify-it-yourself/RECEIPTS.md). The script joins the parts in object/ into u.txt, v.txt and w.txt, checks their sha256, then runs two exact checkers: check_brent_stdlib.py (python3 standard library only) checks all 123921424 Brent equations (22*22 * 22*23 * 22*23 index triples) in integer arithmetic after multiplying each factor matrix by its least common denominator, and evaluates the scheme on three random integer matrix pairs exactly; check_exact_np.py (numpy) is a separately written exact checker of the same equations, much faster, with its own exactness argument in its docstring (it is skipped with a message if numpy is not installed, and then the verdict rests on the first checker alone). The stdlib checker is the one from the <18,18,19> package (PR #714); that package's second stdlib checker (check_scheme_second.py) is not shipped here, to keep the batch to the two checkers above. This package's check_exact_np.py has sha256 prefix 3f9ebe84; the four later packages of the batch (<28,28,29> to <30,31,31>) ship a version with prefix 0eeb12c7 that adds an exact Python-integer path for terms too large for float64. RUN_IT_YOURSELF.md has the file format and the full expected output; how-we-built-it/COMMANDS.md rebuilds the object from LITA's published scheme.

## Compared to
| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| fmm_sota.json (Lille catalogue digest) | [22, 22, 23] | 5625 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-24T22:35:43Z (re-fetched by the criterion panelist 2026-10-25T09:09:45Z, byte-identical to the first fetch) |
| Lille catalogue index | row 22x22x23 | 5625, construction ⟨22×22×1:484⟩ + ⟨22×22×22:5141⟩ | https://fmm.univ-lille.fr/ | 2026-10-24T22:35:44Z (re-fetched 2026-10-25T09:09:46Z, byte-identical) |
| Lille per-format page | ⟨22×22×23⟩ | 6050 (The algorithm ⟨22×22×23:6050⟩ could be constructed using the following decomposition: ⟨22×22×23:6050⟩ = ⟨22×22×1:484⟩ + ⟨22×22×22:5566⟩ .) | https://fmm.univ-lille.fr/22x22x23.html | 2026-10-24T22:35:56Z (re-fetched 2026-10-25T09:09:46Z, byte-identical) |
| Lille pages for the other axis orders | - | HTTP 404 (sorted formats only) | https://fmm.univ-lille.fr/22x23x22.html, https://fmm.univ-lille.fr/23x22x22.html | 2026-10-24T22:35:58Z |
| matmulcatalog docs/catalog.json | [22, 22, 23] | 5625 (naive-22x22x1 +p 22x22x22); 5626 (naive-22x22x1 +p 22x22x22); 5917 (23x23x23 ∖[11|11|]); 6050 (naive-22x22x1 +p DIS09Lemma4(n=22)) | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/docs/catalog.json | 2026-10-24T22:35:44Z (re-read 2026-10-25T09:09:56Z by the criterion panelist: lowest 5625; no scheme listed at or below 5423) |
| matmulcatalog generated/COVERAGE.md | - | no row (sections stop at max dimension 16) | https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md | 2026-10-24T22:35:45Z |
| Perminov docs/ranks.md, docs/additions.md, README, repository tree | - | no entry (formats up to 16x16x16) | https://github.com/dronperminov/FastMatrixMultiplication | 2026-10-24T22:35:45Z to 2026-10-24T22:36:00Z |
| MerlijnW70/fmm-schemes | - | no entry (up to 16) | https://github.com/MerlijnW70/fmm-schemes | 2026-10-24T22:36:01Z |
| khoruzhii/lita schemes listing | - | square schemes only (13^3 to 32^3), no rectangular scheme | https://github.com/khoruzhii/lita | 2026-10-24T22:36:02Z |
| V3R1T4S pull requests (all 691, open and closed) and main | - | no scheme or rank filed for the cell in any order | https://github.com/elder-plinius/V3R1T4S | 2026-10-24T22:36:11Z to 2026-10-24T22:38:05Z |

Lowest public value for <22,22,23> in any axis order: 5625. Details, the literature search and every request with its sha256: the-record-we-beat/RECORD.md and the-record-we-beat/FETCH_LOG.txt.

INDEX.csv's table_fetched_utc (2026-10-25T09:09:45Z) is the criterion panelist's re-fetch of fmm_sota.json; the primary fetches are at 2026-10-24T22:35Z.

### How 5423 relates to the listed values
- 5625 (tables) is the block sum ⟨22×22×1:484⟩ + ⟨22×22×22:5141⟩ (naive 22x22x1 plus LITA's 22^3 scheme) as the Lille construction column writes it.
- From LITA's <23,23,23> rank 6009, plain coordinate projections (delete one index, drop the terms that vanish, no reductions) give at best 5917 for <22,22,23> (delete row 11 and column 11: 92 terms vanish); from the sibling 5710 scheme (<22,23,23>), the best single-coordinate deletion of that sibling scheme (every deletion of one index in either of its two size-23 axes, dropping the terms that vanish, no reductions; counted in panel/criterion.md) gives 5665 terms. All are above the table value 5625.
- This scheme uses non-coordinate slices instead. Slice 1 (row index shared by A and C; direction e* = (1,...,1,-9,1,...,1), -9 at index 11, on the A side and e_0 on the C side) kills 298 terms (264 on the A side, 34 on the C side, none on both): 6009 - 298 = 5711; one exact 2-reduction gives 5710 (<22,23,23>, the sibling cell). Slice 2 (column index of A = row index of B; e_0 on the A side, e* on the B side) kills 286 terms (23 + 263, none on both): 5710 - 286 = 5424; one exact 2-reduction gives 5423. Total removed: 298 + 1 + 286 + 1 = 586 = 6009 - 5423.

Correction to the figure in how-we-built-it/slice_accounting_output.txt: that file's "best column" line (5675 terms) counts only deleting a column of A together with the matching row of B. The panel's count in panel/criterion.md covers every single-coordinate deletion of the sibling scheme and gives 5665 terms; both are above this cell's rank 5423.

## Prior work on this method
The LITA slice-and-absorb method is not new in this repository. Earlier p1 claims with this slice method (PRs #41 to #51) were closed unmerged by their author on 2026-10-14 (12:51Z), together with about 115 of that author's other early pull requests, including main-criterion claims refiled and merged the next day (#130, #164); no maintainer comment or verdict on them exists. No p1 claim of this method has been merged yet, but the repository's own TROPHY_CASE rows 44 to 48 are restrictions of LITA squares. The merged PRs #130, #164, #172 and #197 (2026-10-15 and 2026-10-16, from LITA 15^3 and 17^3), and the merged LITA-based claims #166, #175, #177, #178 and #179, were for formats with max dimension at most 16. PRs #708 (<18,19,19> rank 3424) and #714 (<18,18,19> rank 3225) are open sibling claims by the same contributor with the same method, from LITA 19^3. What is new here is this format's value 5423 and this scheme.

## Not claimed
- Not the main criterion: max(22,22,23) = 23 > 16. Partial win p1 only.
- Not the tensor rank of <22,22,23>: 5423 is an upper bound (a scheme with 5423 multiplications), not a proof that fewer are impossible.
- Not a ring upgrade: the coefficients are rationals (denominators up to 2816); nothing is claimed over Z or GF(2).
- Not a new method. The same LITA non-coordinate slice with exact absorption was used earlier in this repository: PRs #41 to #51 (earlier p1 claims with this slice method, closed unmerged by their author on 2026-10-14, with no maintainer comment or verdict) and the merged PRs #130, #164, #172 and #197 (2026-10-15 and 2026-10-16; from LITA 15^3 and 17^3), and, for the 19-family from LITA 19^3, PR #708 (<18,19,19> rank 3424) and PR #714 (<18,18,19> rank 3225), both open. Only the value 5423 for this format, with this scheme, is new here.
- Not the sibling cells of this batch (one cell per claim): <22,23,23> rank 5710.
- Reproducibility of the rebuild: The rebuild was done twice in the run (two separate rebuilds for N = 23) and the step JSON and text exports are byte-identical; how-we-built-it/COMMANDS.md lets you redo it.
- The Lille page for this format (6050) is older than the index; the claim does not rest on it alone, since 5423 is below every value in every source read.

## Corrections to the panel text
README.md, RUN_IT_YOURSELF.md and HOW_WE_FOUND_IT.md were revised after the gate (wording, credits, file names, the join command), and how-we-built-it/PREREG.md had only its run id removed; the object, the What sentence and the panel files are as gated.

- panel/gate.md says the earlier p1 claims #41 to #51 "were closed unmerged on 2026-10-14 with no comment on record". In fact they were closed by their own author on 2026-10-14 (12:51Z), together with about 115 of that author's other early pull requests, including claims refiled and merged the next day (#130, #164); no maintainer comment or verdict on them exists.

## Credits
- Kirill Khoruzhii, Luzian Serafin, Patrick Gelss and Sebastian Pokutta, Local Improvements to Trilinear Aggregation (LITA), https://github.com/khoruzhii/lita (manuscript in preparation): the exact 2-reduction step (LITA's README defines 2-reducibility and src/reduce.h implements it) and the <23,23,23> rank-6009 scheme this one is restricted from (schemes/23x23x23_r6009.npz at commit 472a79fbc8248423a97bebb3aacbc89e769b9b3e). LITA builds on Victor Pan's trilinear aggregation (V. Ya. Pan, FOCS 1978, https://doi.org/10.1109/SFCS.1978.34; Comput. Math. Appl. 1982, https://doi.org/10.1016/0898-1221(82)90037-2).
- The earlier V3R1T4S claims that used this LITA slice-and-absorb method: https://github.com/elder-plinius/V3R1T4S/pull/41, https://github.com/elder-plinius/V3R1T4S/pull/51, https://github.com/elder-plinius/V3R1T4S/pull/130, https://github.com/elder-plinius/V3R1T4S/pull/164, https://github.com/elder-plinius/V3R1T4S/pull/172 and https://github.com/elder-plinius/V3R1T4S/pull/197 (contributor credit anonymous-c6d1e0ab, and calgulbenkian for #197), and the same contributor's 19-family claims https://github.com/elder-plinius/V3R1T4S/pull/708 and https://github.com/elder-plinius/V3R1T4S/pull/714 (open sibling claims, same method).
- Manuel Kauers and Isaac Wood, Exploring the Meta Flip Graph for Matrix Multiplication, arXiv:2510.19787 (https://arxiv.org/abs/2510.19787) (projection edges between formats; the slices here are non-coordinate versions), and Manuel Kauers and Jakob Moosbauer, Flip Graphs for Matrix Multiplication, arXiv:2212.01175 (https://arxiv.org/abs/2212.01175) (reductions; the 2-reduction step used here is LITA's, credited above). Richard P. Brent, STAN-CS-70-157 (1970), for the Brent equations.
- Alexandre Sedoglavic, the Lille fast matrix multiplication catalogue, https://fmm.univ-lille.fr/, and its digest https://github.com/sedoglavic/fmm_digest (the source of fmm_sota.json, https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json).
- Benoit Chatain Lacelle, matmulcatalog (arXiv:2606.13408, https://arxiv.org/abs/2606.13408), https://github.com/solven-eu/matmulcatalog.
- Perminov (dronperminov), FastMatrixMultiplication, https://github.com/dronperminov/FastMatrixMultiplication, and MerlijnW70/fmm-schemes, https://github.com/MerlijnW70/fmm-schemes (checked; neither has a format with a dimension above 16, so neither covers max dimension 23).
- V3R1T4S, https://github.com/elder-plinius/V3R1T4S: the challenge repository and the bank target fmm-catalogue-small-format-rank.
- Contributor: Abshalom Dayan (V3R1T4S runs).
