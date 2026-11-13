# RECEIPTS (real output of `sh verify-it-yourself/run_checks.sh`, run 2026-11-13 ~05:24 UTC with the run's Python 3.11)

```
ok   object sha256 0d068173581343468b7a4ef6f28861c18a8fbf83a5e2aa2b8808272fe7283ee4
ok   93 stage cells (3 stages x 31) in the table: 93
ok   published value recorded for national Epiforecasts
ok   published value recorded for national ILM
ok   published value recorded for national KIT
ok   published value recorded for national KIT-frozen_baseline
ok   published value recorded for national LMU
ok   published value recorded for national MeanEnsemble
ok   published value recorded for national MedianEnsemble
ok   published value recorded for national RIVM
ok   published value recorded for national RKI
ok   published value recorded for national SU
ok   published value recorded for national SZ
ok   published value recorded for states Epiforecasts
ok   published value recorded for states KIT
ok   published value recorded for states KIT-frozen_baseline
ok   published value recorded for states LMU
ok   published value recorded for states MeanEnsemble
ok   published value recorded for states MedianEnsemble
ok   published value recorded for states RIVM
ok   published value recorded for states RKI
ok   published value recorded for states SU
ok   published value recorded for states SZ
ok   published value recorded for age Epiforecasts
ok   published value recorded for age ILM
ok   published value recorded for age KIT
ok   published value recorded for age KIT-frozen_baseline
ok   published value recorded for age LMU
ok   published value recorded for age MeanEnsemble
ok   published value recorded for age MedianEnsemble
ok   published value recorded for age RIVM
ok   published value recorded for age SU
ok   published value recorded for age SZ
ok   S2: all 31 cells within 1% (max |rel| 1.031e-04)
ok   S2: 28 cells agree to < 1e-9 relative: 28
ok   S2: the only non-exact cells are the three Epiforecasts cells
ok   S2: Epiforecasts residuals below 2e-4
ok   S0: 6 cells outside 1% or undefined without the full rules: 6
ok   S1: 6 cells outside 1% or undefined without the full rules: 6
ok   WIS pinball form = interval form (max diff 2.84e-14)
ok   known positive: a point forecast scores |y - m|
ok   known negative: a wrong normalisation differs
PASS
```

A copy of the object with one digit changed fails check 1 (`FAIL object sha256 7b911929...`), last line FAIL.
