# Pre-registration v2 (run 3), frozen 2026-10-31T11:04:45Z before sweep 2

Why a v2: the method changes (new formulation), not the criterion. Smoke test before freezing: Hurinkrdata21 only
(hierarchical model, 30 s, 8 workers: OPTIMAL 618, checker VALID), already a sweep-1 candidate (623).
Criterion, statistic and threshold: unchanged from PREREG.md (independent checker VALID and makespan <= round(UB) - 1).
Method (fixed settings): attempts/cpsat-hier/code/solve_hier.py (machine-then-worker optional intervals, redundant
cumulative of capacity min(machines, workers), no makespan cap), 30 s per instance, 4 search workers, 2 instances in
parallel, every row that sweep 1 left UNKNOWN or FEASIBLE (357 rows), smallest file first.
One instance per claim; NOVELTY checks papers, V3R1T4S PRs and OptalCP before any panel.

null_test: not needed because each claim is an explicit schedule checked by a deterministic checker against a table value.
