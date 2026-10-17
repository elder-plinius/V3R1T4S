# PREREG (frozen 2026-10-17T12:12:16Z)

Honest timing note: the 16x19 matrix with 142 ones, the local-search code and the surgery baseline code existed
before this run folder was created (found in an earlier session). This file freezes how the existing claim is
JUDGED, before this run's verification and baseline outputs were produced. It does not pretend the search itself
was preregistered.

criterion: verbatim in target.md (charter quarry 5). Cell: z(16,19;3,3) only.

statistic and checkers (deterministic, exact integer arithmetic):
1. claim/check/check_matrix.py on claim/matrix/z_16x19_142.txt with --rows 16 --cols 19 --ones 142 prints PASS
   (shape 16x19, 142 ones, zero all-ones 3x3 submatrices by method A and method B).
2. An independent checker written from the definition (attempts/settled-check/code/own_k33.py) agrees.

thresholds (all required for the claim to stand):
- 142 > 136, the best explicitly stated lower bound in the saved scout (strictly greater; a tie is not a record).
- 142 > the best value reached by the surgery baseline (claim/baseline/surgery_baseline.py, 12 public witness bases,
  fixed seeds, fixed run counts) when rerun in this run. If any rerun reaches 142 or more, the cell is
  "derivable" and the claim is withdrawn (verdict REFUTED for novelty).
- a rerun that stays below 142 is evidence only, never proof that 142 is not derivable; the claim text must say so.

null_test: not needed because the claim is one explicit object judged by a deterministic checker against table values; the controls are the stated bounds and the re-run surgery baseline above, and no statistical or "beats chance" statement is made.
