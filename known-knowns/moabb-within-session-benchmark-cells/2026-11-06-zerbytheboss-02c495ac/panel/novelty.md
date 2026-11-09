# Skeptic 2: Prior Art & Benchmark Novelty Audit

context: independent literature and benchmark audit started from target specification and package files only

## Audit Summary

1. Audited the live MOABB benchmark results table (`https://moabb.neurotechx.com/docs/paper_results.html`, `SSVEP (All classes)` paradigm table, SHA-256 `acba9cb52cf71de26d84b1ff00bd8a7a0a61b845ee2a017cb5531e25a2c76d4c`) and `known-unknowns/neuroscience/moabb-within-session-benchmark-cells.md`: the live best cells are `Kalunga2016 = 70.89±13.44` (`SSVEP_MDM`), `Nakanishi2015 = 87.22±15.96` (`SSVEP_TS+LR`), and `MAMEM3 = 42.10±14.33` (`SSVEP_TS+LR`).
2. Verified that the single fixed pipeline `FB_HTR_SSVEP` achieves `88.92±8.03` on `Kalunga2016` (`+18.03` points), `95.86±10.02` on `Nakanishi2015` (`+8.64` points), and `52.73±23.99` on `MAMEM3` (`+10.63` points; `50.08±23.58` on subjects `1..10`), exceeding the `+1.0` point requirement on all 3 datasets while reproducing `SSVEP_MDM` and `SSVEP_TS+LR` baselines.
3. Confirmed that both `win` (`>= 3` datasets of the same paradigm table beaten by `>= 1.0` point with one fixed pipeline) and `p1` (`1` dataset cell beaten by `>= 1.0` point) are satisfied.

pass: true
