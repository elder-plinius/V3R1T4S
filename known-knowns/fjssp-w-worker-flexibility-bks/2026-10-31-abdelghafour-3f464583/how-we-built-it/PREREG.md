> Paths updated 2026-11-07 to files in this package; the frozen text is otherwise unchanged.

# Pre-registration (run 3), frozen 2026-10-31T10:30:09Z before the scored sweep

Criterion: verbatim in the V3R1T4S target file for fjssp-w-worker-flexibility-bks (known-unknowns/).
Statistic: makespan computed by verify-it-yourself/fjsspw_check.py (independent of the solver) on the solver's schedule,
compared with round(UB) from best_known.csv (the-record-we-beat/snapshot.md) (fetched 2026-10-31T10:24:20Z) for the row given by the instance-to-row mapping in INDEX.csv.
Threshold: makespan <= round(UB) - 1 and the checker prints VALID. Ties fail.
Method (fixed settings): how-we-built-it/solve_flat.py, CP-SAT (OR-Tools 9.15), cap makespan <= UB-1, 20 s per instance,
2 search workers, 4 instances in parallel, all 371 open rows, smallest first. A follow-up pass with longer limits on
selected rows is allowed and will be logged with its own settings.
One instance per claim; each surviving cell gets its own claim folder and three-skeptic panel; NOVELTY must check papers
(arXiv:2501.16159 and later), V3R1T4S PRs and OptalCP before the panel.

null_test: not needed because each claim is an explicit schedule checked by a deterministic checker against a table value.

Baseline (step 3c): not an empirical benchmark; no published schedules to reproduce.
