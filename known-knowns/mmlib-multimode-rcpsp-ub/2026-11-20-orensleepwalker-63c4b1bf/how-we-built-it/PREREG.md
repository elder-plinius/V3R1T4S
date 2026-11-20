# Preregistration: MMLIB+ claim run 2026-11-20-1014

Frozen by the lead agent (Andy) BEFORE claim/ is built. The search that found the schedules (scans/2026-11-19-mmlib-solver, phases A-C) was exploratory and is NOT covered by a preregistration; that is disclosed, not hidden. What this file fixes is the claim: which object is claimed and how it is judged.

null_test: not needed because every claimed result is an exact, checker-verified schedule compared with a published best-known value; no statistic, sample or chance enters the decision.

## Object
- For each MMLIB+ instance with at least one win file in scans/2026-11-19-mmlib-solver/phaseB/wins/ (33 files, 30 instances as of 2026-11-20T10:14Z), the shortest checker-valid schedule (modes for all jobs, starts for all jobs). The selection is data/selected_wins.json (sha256 dbbd3edc71c04edcb34d6d2d2eb66634b396c57a45863324ca966ac8d4e9fefc): 30 schedules. No schedule found after this freeze is added to this claim.

## Checks (each instance, all must hold)
1. code/mm.py check() returns VALID with the stated makespan (one mode per job, non-renewable totals, precedences, renewable capacity in every period). mm.py reproduces all 2,570 posted MMLIB+ best-known schedules exactly (scans/2026-11-19-mmlib-scout/code/validate_bks.output.txt).
2. The instance is open (LB < UB) in data/MMplus_2.csv, re-fetched 2026-11-20T10:14:46Z.
3. Makespan strictly below the UB in data/MMplus_2.csv, the value in data/MMplus_2_BKS.csv and the UB-lit in the release Excel (data/MMLIB_v2_1.zip), and not below the LB.
4. Warm starts are named: for the 8 instances whose search started from the posted best-known schedule, the claim names that schedule as the seed and reports how many modes changed and whether re-timing the posted modes alone can reach the claimed makespan (lead-agent-checks/warm_start_edits*.py).
Before any filing, data/MMplus_2.csv, data/MMplus_2_BKS.csv and the release are re-fetched; an instance whose UB has dropped to or below our makespan is removed.
