# CRITERION review: matsp-lb2 (partial win 'matsp-optimality-certificate')

context: fresh subagent started for this claim only

Inputs read: CLAIM.md, target.md, PREREG.md, REPRODUCE.md, code/check_certificates.py, code/check_table.py, object/certificates.csv, data/ProblemDefinition.txt, data/matsp.html, data/changes.html, data/fetched-utc.txt, data/instances1_225.zip. `sha256sum -c SHA256SUMS` passes for every file, and so does PREREG.sha256. object/certificates.csv is byte-identical to data/certificates.csv and matches the hash frozen in PREREG.md.

## (1) Is the argument correct and complete against ProblemDefinition?
I find it correct. I re-derived it from the definition text.
- Constraint 4 gives b_e <= 15 * sum_d n_ed with n_ed an integer number of intervals. So sum_d n_ed >= ceil(b_e/15).
- On-duty intervals are distinct. A shift lasts at most 10 h, so a day-d shift cannot reach day d+2's earliest start (00:00). Constraint 3 (14 h rest) stops day d and day d+1 from overlapping. Shifts start at interval indexes in I and finish by h*96 (constraint 2), so every on-duty interval lies in I. Each employee therefore has at least ceil(b_e/15) distinct on-duty intervals in I.
- Constraint 7: an on-duty interval carries an activity. Only sum_a x_eia >= 1 is needed, so the bound does not depend on the "at most one" part. Summed cover over I x A is therefore >= W.
- Constraint 8 gives y_ia >= cover_ia - w_ia, and y_ia is a non-negative integer (Z*). Summing over I x A gives sum y >= W - M. y^2 >= y holds for integers, so the objective is >= W - M.
- Gaps I hunted for, and what I found:
  - (a) Does SECTION_COVER list every (i,a) pair exactly once? Yes, for all 94 rows I checked. Each file has exactly h*96*|A| cover rows with unique keys, running from day 1 06:00 to day h+1 05:45, and every max >= 0. If pairs were missing, M would understate the sum of w.
  - (b) The file's horizon, staff count and task count match the stem, and b_e <= c_e for every employee.
  - (c) The index range in constraint 7 (d up to h) is slightly sloppy. This does not affect the bound.
  - (d) The XML .ros files encode the minimum workload as a weighted soft constraint (weight 100000). The PDF, which the criterion names as the definition, makes it hard. One spot check (instance 9, employee 1: 1140 minutes) agrees with the TXT file. Under the PDF the argument stands. Under a soft reading it would need a separate weight argument, which I did not make. I adopt the PDF reading, as the target text does.
- Falsification check: over all 225 table rows, no best known value lies below W - M. Exactly 99 rows have best known = W - M > 0, which is the 94 claimed plus 1, 3, 4, 77 and 78. Instance 5 has best known 0.

## (2) Does this count as "a VIPR-style certificate checked by an independent checker"?
The wording has two alternatives. The first (MIP/CP model, solver log and seed, with a matching bound re-run) does not apply. On the second, I adopt the substantive reading. A VIPR certificate is a machine-checkable derivation of a dual bound: a non-negative aggregation of model constraints plus integer rounding, checked without trusting a solver. This certificate is exactly such a derivation. It aggregates constraints 4, 7 and 8 with unit multipliers and applies integer rounding (the ceiling and y^2 >= y). The derivation is four lines, so a human can check it, and the instance-specific arithmetic (W, M) is checked by code.

It does not use the literal VIPR file format, and the shipped checker was written by the claimant. I wrote my own recomputation from the TXT files, and it agrees on all 94 rows; that recomputation serves as the independent check. "-style" plainly allows a non-VIPR format, and the criterion's purpose ("proof of optimality ... new information") is fully met. I judge the fit as substantive, not stretched.

## (3) Is each row positive and equal to the bound?
- code/check_certificates.py: 94 checked, 0 failed, PASS.
- code/check_table.py: 225 table rows, no mismatches, PASS.
- My own code-independent recomputation (a fresh parser that also validates the cover structure) and a row-wise table parse both agree on all 94 rows, and every row credits TRA26. Spot checks: instance 2 (856 - 724 = 132), 9 (1824 - 1506 = 318), 225 (66736 - 55870 = 10866), all matching the table.
- No duplicate rows. None of 1, 3, 4, 5, 77 or 78 appears.

## (4) Does bundling 94 instances stretch the claim?
No. Each row is a separate deductive certificate, checked separately. One row alone meets the partial win, and a row that fails would only drop that row. The 94 rows are selected from an exploratory screen of all 225 instances, but that selection does not bias a deductive proof. No null model applies to an exact inequality; the 225-row falsification check above stands in for one.

## (5) Does version 2's removal of five instances matter?
It matters for the "new information" clause of the criterion. Instances 1, 3, 4, 77 and 78 are already proven optimal in TRA26 (per PREREG.md), so including them would not have been new. Removing them is correct and changes nothing else. For the remaining 94, the claim that TRA26's bounds are weaker is a NOVELTY question that I cannot verify from claim/. My pass covers the criterion, conditional on the novelty review. Whether anyone has published this trivial bound elsewhere is likewise for NOVELTY.

## (6) What must happen at filing?
The table was fetched at 2026-11-22T08:26:45Z (data/fetched-utc.txt). At filing:
- Re-fetch https://www.schedulingbenchmarks.org/matsp/ and changes.html.
- Re-run both checkers against the fresh table.
- Drop any row whose best known value changed. A new value below W - M on any instance would contradict the argument and should withdraw the whole claim.
- Confirm that the site still lists no lower bounds.
- Confirm that the instance archive's hash is unchanged.

confirmed_scope: For each of the 94 instances listed in object/certificates.csv, the best known penalty on the schedulingbenchmarks.org matsp table fetched 2026-11-22T08:26:45Z is positive and equals W - M computed from the instance's TXT file, which by constraints 2, 3, 4, 7 and 8 and the non-negative-integer quadratic objective of ProblemDefinition.pdf is a lower bound on every feasible roster's penalty, so those best known values are optimal (subject to the filing-time re-fetch dropping any changed row).
pass: true
