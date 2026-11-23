# REPRODUCE review: 94 matsp optimality certificates (W - M bound)

context: fresh subagent started for this claim only

Scope read: claim/ only (CLAIM.md, target.md, PREREG.md, REPRODUCE.md, data/, object/, then code/). Scratch work outside the run folder; nothing in claim/ modified.

## (a) Definition quoted and bound re-derived (data/ProblemDefinition.txt)

- Intervals: "The planning horizon is split into 15-minute intervals." "The shift lengths are in 15-minute intervals i.e. {24…40}." n_ed is a length in intervals.
- Constraint 4: "b_e ≤ ∑_{d∈D} n_ed ∗ 15 ≤ c_e". Work time is 15 * (integer number of intervals), so each employee has ∑_d n_ed ≥ ceil(b_e/15). (In all 225 instances every b_e and c_e is a multiple of 15 and b_e ≤ c_e, so the ceiling is never even exercised.)
- Constraint 7: "Activities can only be assigned between shift start and end times, and an employee cannot have more than one activity during an interval", formula "∑_{a∈A} x_eia ⇔ t_e(d−1) ≤ i < u_e(d−1) ⋁ t_ed ≤ i < u_ed". With x binary and at most one activity per interval, ∑_a x_eia ∈ {0,1} and equals 1 exactly on on-duty intervals: an on-duty interval cannot be idle (the ⇔ is two-sided).
- Shifts of one employee do not overlap: constraint 3 ("at least 14 hours rest after a shift", u_ed ≤ t_e(d+1) − 56) separates consecutive days, and a shift is at most 40 intervals, so day d and day d+2 shifts cannot meet. Hence on-duty intervals of e = ∑_d n_ed, and constraint 2 keeps them inside I.
- So ∑_{i,a} cover_ia = ∑_e ∑_d n_ed ≥ W = ∑_e ceil(b_e/15).
- Constraint 8: "v_ia ≤ ∑_e x_eia − y_ia ≤ w_ia", so y_ia ≥ cover_ia − w_ia for every (i,a) in I×A. Domain "y_ia ∈ ℤ∗" (described as "total employees above the max demand").
- Objective "Minimise ∑∑ y_ia y_ia". For each term: if cover_ia − w_ia ≥ 1 then y_ia ≥ that integer ≥ 1 and y_ia² ≥ y_ia ≥ cover_ia − w_ia; otherwise y_ia² ≥ 0 ≥ cover_ia − w_ia. This holds whether ℤ∗ means non-negative or all integers, and even for real y. Summing: penalty ≥ ∑ (cover − w) = ∑cover − M ≥ W − M, with M = ∑_{i,a} w_ia over the full grid.
- The saved XML instances agree with this objective: every <Max> cover has function="quadratic" weight="1"; all other XML terms are hard constraints (large weights) and can only add penalty.

Gap search: (i) idle on-duty intervals: excluded by the two-sided ⇔ of constraint 7. One wording caveat: the formula's block indexing ("i ∈ {d∗96 … (d+1)∗96−1}" against a horizon starting at 06:00) is sloppy for 00:00 starts; read literally it would say nothing coherent about the first hours of a 00:00 shift. The prose and the ⇔ make the intended meaning (every interval of a shift carries exactly one activity) clear, and the data are consistent with it: over all 225 instances TRA26's best known is never below W − M, and it equals W − M on 100 instances, including 1, 3, 4, 77, 78 that TRA26 itself proves optimal. (ii) Work time not a multiple of 15: impossible, lengths are interval counts. (iii) y forced ≥ cover − max: yes, by the right inequality of constraint 8. (iv) negative or fractional y: does not break the bound (shown above). No gap found that invalidates the argument.

## (b) Own recomputation before reading claim/code/

Own parser of all 225 instances1_225/txt files (sections HORIZON, TASKS, STAFF, COVER; asserts: every cover line maps into I, task ids in range, v ≤ w, no duplicate (interval, task), grid complete = h*96*|A| entries, unique staff ids). W = ∑ ceil(b/15), M = ∑ w. Result: all 94 CSV rows match stem, min_work_intervals (W), max_cover_total (M), bound = W − M, and bound = best_known > 0; 0 mismatches, no duplicate rows. Cross-check from the XML instance files (instances1_225/xml): W and M identical to the text files for all 225.

## (c) Best known values vs data/matsp.html

Own HTML table parse: 225 rows (columns Instance, Days, Staff, Tasks, Best known, Reference). For all 94 rows, best_known equals the table value, the reference is TRA26, and days/staff/tasks match the file stem. None of 1, 3, 4, 5, 77, 78 is in the CSV.

Sanity check on the other 131 instances: W − M never exceeds the best known value (0 violations of 225). W − M equals best known exactly on 100 instances = the 94 rows + {1, 3, 4, 5, 77, 78}, so the CSV is exactly the set the PREREG describes. Smallest remaining gaps: instance 219 (2), 80 and 173 (6), 98 (12).

## (d) REPRODUCE.md steps 1-3

1. sha256sum -c SHA256SUMS: all 15 OK; sha256sum -c PREREG.sha256: OK; object/certificates.csv sha256 293c822d...7d17b matches PREREG and is identical to data/certificates.csv.
2. code/check_certificates.py: "94 certificates checked, 0 failed", PASS, exit 0; run twice, byte-identical output (deterministic). Its W and M agree with mine.
3. code/check_table.py: "table rows read: 225; certificate rows: 94; mismatches: none", PASS, exit 0.

The author's checker is weaker than mine (no grid completeness, duplicate or range checks), but my stricter parser confirms the same numbers, so this does not matter for the result.

## Limits

- The PDF itself could not be rendered here (no PDF tools); the review relies on data/ProblemDefinition.txt and the XML instances. The only formula-level weak point is the constraint 7 indexing noted above.
- PREREG check 4 (re-fetch the live table and changes page before filing) is for the lead and was not done live by this reviewer; only the saved data/matsp.html and data/changes.html were used.

Verdict: the derivation is sound, all 94 rows reproduce exactly from the saved files with my own code and with the author's, deterministically.

pass: true
