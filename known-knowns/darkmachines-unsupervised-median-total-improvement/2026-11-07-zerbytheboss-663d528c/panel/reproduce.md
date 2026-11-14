# Skeptic 1: Reproducibility & Independent Computation Audit

- Context: Fresh independent verification from the package root (`sh verify-it-yourself/run_checks.sh`).
- Question: Does `verify-it-yourself/run_checks.sh` retrain the unsupervised 27-invariant POT detectors from scratch on Channel 2a odd-event_ID background events, verify tie-aware thresholds on even-event_ID background events, recompute all 102 signal-channel rows and 19 signal summaries, and reject corrupted object files?

## Audit Summary

1. Executed `sh verify-it-yourself/run_checks.sh` from a clean copy of the package.
2. Confirmed that `verify-it-yourself/check_darkmachines.py` imports `how-we-built-it/run_darkmachines_pot.py`, fits `PotHull_Hybrid_Lp3`, `PotStrataZ_Lp3`, and `PotHull_L1_L2_Hull` live from scratch on the `11,628` odd-`event_ID` SM background events of Channel `2a` (`verify-it-yourself/data/chan2a_bg_odd.npz`), calibrates exact tie-aware thresholds on the `8,377` even-`event_ID` SM background events (`chan2a_bg_even.npz`), scores all 7 Channel `2a` BSM signals (`chan2a_signals.npz`), and independently verifies all 102 rows of `object/darkmachines_27invariant_pot_results.csv` and all 19 rows of `object/darkmachines_19signals_summary.tsv`.
3. Confirmed that mutating a single character in `object/darkmachines_27invariant_pot_results.csv` or `object/darkmachines_19signals_summary.tsv` causes `run_checks.sh` to exit with code 1 and print `FAIL`.

pass: true
