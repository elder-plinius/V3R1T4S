# Pre-registration (frozen before any scored attack output)

frozen_utc: 2026-10-30T23:29Z (see `date -u` in run log; written before the annealer's scored runs)

## Criterion (verbatim, from target.md)
A solution JSON for one instance from ihtc2024_competition_instances.zip (i01-i30) or ihtc2024_final_instances.zip
(m01-m30) that the official IHTP_Validator.cc (compiled from the organisers' repository) reports with ZERO
hard-constraint violations and a total cost STRICTLY LOWER (direction: min) than the cost listed for that instance on
https://ihtc2024.github.io/ihtp/index.html, re-fetched live immediately before claiming, and lower than any value for
that instance found by the NOVELTY check in the 2025-2026 special issue on the IHTP (Operations Research, Data
Analytics and Logistics) and other papers. Any strict improvement counts; ties do not.

## Statistic and checker
- Per instance: total cost and total violations as printed by the official IHTP_Validator.
- Our port (ihtp_eval.py) and the annealer's internal cost are search aids only. A candidate is a candidate only if
  ihtp_eval.py reports 0 violations and cost < table value (scout.md snapshot). A claim needs the official validator.
- Threshold: strictly lower than the live table value; ties are not improvements.
- Method (for p2 accounting): anneal.cc, fixed settings (30 s cycles, T0=6, T1=0.2, restart from best), one seed
  per instance (seed 1), warm start = the organisers' published solution, wall-clock per instance stated in the report.

null_test: not needed because each claim is an explicit solution object checked by a deterministic validator against a table value.

## Baseline (step 3c)
Not an empirical benchmark score; the "baseline" is the published solution itself, re-evaluated: 60/60 reproduce the
listed cost with 0 violations under our port (attempts/contrarian/table_audit_output.txt).
