# REPRODUCE skeptic report: z(16,19;3,3) >= 142

context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)

Definition used (from the task): z(m,n;3,3) is the largest number of ones in an m x n 0/1 matrix with no all-ones 3 x 3 submatrix (3 rows and 3 columns, not necessarily adjacent).

## 1. Own checker, written before opening check/ or any other code
Command: `python work/my.py claim/matrix/z_16x19_142.txt` (UTC 2026-10-17 12:26:23 to 12:26:30). It parses the matrix, asserts rectangular 0/1, then tests all C(16,3) row triples (count of columns where all three rows have a 1; a K33 exists iff the count is >= 3) and all C(19,3) column triples (same test on rows).
Output: `16 19 142`, `row triples 560 bad 0`, `col triples 969 bad 0`. Exhaustive, not sampled. The matrix is 16 rows x 19 columns, 142 ones, K33-free.
`sha256sum matrix/z_16x19_142.txt` = 47ef934e67f7931526d0f9b57fbd617a7ea8100c4efdeccf765c4f29286f3fa8, equal to the hash stated in CLAIM.md.

## 2. Package checker and REPRODUCE.md commands
- `python check/check_matrix.py matrix/z_16x19_142.txt --rows 16 --cols 19 --ones 142`: shape 16 x 19, ones 142, methods A and B agree, PASS, exit 0. `--selftest` PASS.
- Baseline best matrices (baseline/output/best_seed1..4.txt): each is 16 x 19 with 141 ones, PASS under both the package checker and my own (560 and 969 triples, 0 bad).
- baseline/output/surgery_16x19_seed1..4.txt: every file ends `total runs 48000` and `BEST 141 ... re-verified K33-free: True`. Summing the saved histograms gives 66663 runs at 141 and 0 at 142, exactly the CLAIM.md figures (4 seeds x 48000 = 192000 runs). Per-base bests are 134 to 141. The 12 bases' own K33-free flags are printed True.
- `python baseline/derivability.py --selftest`: True for the permuted copy, False for the perturbed copy. `python baseline/derivability.py matrix/z_16x19_142.txt baseline`: bases checked 10, `EXACT_SUBMATRIX_COPIES: 0`.
- `python search/compare_reruns.py matrix/z_16x19_142.txt search/output`: six lines, all 142 ones, only seed 104 isomorphic to the claim, as stated.
- All six rerun matrices search/output/z_16x19_142_seed101..106.txt: my own checker gives 16 19 142, 0 bad triples for each. So 142 is independently re-obtained six times by the author's search; this supports the validity of the value (no non-determinism issue in the object itself, which is a fixed file).
- status_source/closure.py reproduces the upper-bound table (row 16 ends 147 at col 19 = the 5th entry... output printed matches the 147 stated and the "ours" line shows (16,19): 142). lb_closure.py runs; its (16,19) entry reads 139, matching CLAIM.md. (I did not rerun the 192000-run surgery or the 10-minute searches; I checked their saved outputs.)

## 3. Reasoning and limits
- The mathematical claim (an explicit 16 x 19 K33-free matrix with 142 ones, hence z >= 142) is confirmed exhaustively by an independent checker.
- Every number in CLAIM.md that is recomputable from saved files matched: dimensions, 142 ones, hash, 141 baseline best, 66663 runs at 141, 0 at 142, 192000 total, row weights 8,8,8, twelve 9s, one 10 (printed by compare_reruns).
- The surgery baseline is a bounded random sample and CLAIM.md says so; it is evidence, not proof, and I do not fail on that.
- NOT confirmed by me: the published-status table (136 best stated lower bound, 132, 147 upper) since no web access was allowed and the claim package itself says the status pages were not fetched. These come from status_source/scout_record.md, a saved earlier scout. The 142 > 136 comparison is consistent with that record and with the saved closures (139 numeric closure, 141 surgery), and 142 <= 147 upper bound contradicts nothing, but a live check of the sources remains for another stage. This is a limit of my scope, not a mismatch found.
- No mismatch, missing object or non-determinism found.

pass: true
