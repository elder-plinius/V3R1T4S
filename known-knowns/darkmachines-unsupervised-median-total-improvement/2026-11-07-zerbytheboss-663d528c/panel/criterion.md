# Skeptic 3: Target Criterion & Protocol Compliance Audit

- Context: Fresh independent audit of `how-we-built-it/dm_featurize.c`, `how-we-built-it/run_darkmachines_pot.py`, and `object/` against the `darkmachines-unsupervised-median-total-improvement` specification in `bank/targets.json`.
- Question: Does the submission strictly obey the odd/even `event_ID` background split, zero signal leakage, tie-aware FPR thresholding, 2-decimal `eps_S` rounding, and `p1` partial-win criteria?

## Audit Summary

1. **Odd/Even Background Split & Zero Signal Leakage**: Inspected `how-we-built-it/run_darkmachines_pot.py` and `how-we-built-it/dm_featurize.c`; confirmed that detector training and feature weighting use only SM background events with `event_ID % 2 == 1`, and that signal files are never opened or read prior to evaluation scoring.
2. **Tie-Aware Thresholding & 2-Decimal `eps_S` Rounding**: Confirmed in `compute_exact_threshold` that at each working point $\epsilon_B \in \{10^{-2}, 10^{-3}, 10^{-4}\}$, the threshold $\tau$ leaves at most $\lfloor \epsilon_B N_{\text{bg,even}} \rfloor$ background events with $s_{\text{bg}} \ge \tau$ (counting ties as passing), and that each $\epsilon_S$ is rounded to two decimal places before computing $\text{SI} = \epsilon_S / \sqrt{\epsilon_B}$.
3. **Partial Win `p1`**: Confirmed that both `chaneut_cha300_neut100` (`TI = 1.4000` / `1.6000 > 1.1000`) and `chaneut_cha400_neut200` (`TI = 1.6000` / `1.7000 > 1.0000`) strictly exceed the best of the 1,040 challenge detectors under the full-win protocol.

pass: true
