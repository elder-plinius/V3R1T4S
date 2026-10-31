# Pre-registration (run 3), frozen 2026-10-31T10:30:09Z before the scored sweep

Criterion: verbatim in target.md.
Statistic: makespan computed by attempts/cpsat/code/fjsspw_check.py (independent of the solver) on the solver's schedule,
compared with round(UB) from data/best_known.csv (fetched 2026-10-31T10:24:20Z) for the row given by data/name_map.csv.
Threshold: makespan <= round(UB) - 1 and the checker prints VALID. Ties fail.
Method (fixed settings): attempts/cpsat/code/solve.py, CP-SAT (OR-Tools 9.15), cap makespan <= UB-1, 20 s per instance,
2 search workers, 4 instances in parallel, all 371 open rows, smallest first. A follow-up pass with longer limits on
selected rows is allowed and will be logged with its own settings.
One instance per claim; each surviving cell gets its own claim/ and three-skeptic panel; NOVELTY must check papers
(arXiv:2501.16159 and later), V3R1T4S PRs and OptalCP before the panel.

null_test: not needed because each claim is an explicit schedule checked by a deterministic checker against a table value.

Baseline (step 3c): not an empirical benchmark; no published schedules to reproduce.
