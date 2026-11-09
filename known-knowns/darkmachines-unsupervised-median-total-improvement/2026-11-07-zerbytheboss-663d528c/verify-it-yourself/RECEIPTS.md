# Verification Receipts — `darkmachines-unsupervised-median-total-improvement`

## Command Executed
```bash
sh verify-it-yourself/run_checks.sh
```

## Exact Console Output
```text
Verified 102 signal-channel evaluations and live Channel 2a retraining: cha300 TI = 1.40 / 1.60 (> 1.10), cha400 TI = 1.60 / 1.70 (> 1.00), Min_TI = 1.00 (>= 0.90).
PASS
```

## What Was Verified
1. **All 102 Signal-Channel Evaluations (`object/darkmachines_27invariant_pot_results.csv`)**: Every row (`34` channel-signal pairs across Channels `1`, `2a`, `2b`, `3` $\times$ `3` unsupervised POT detectors `PotHull_Hybrid_Lp3`, `PotStrataZ_Lp3`, `PotHull_L1_L2_Hull`) matches the exact signal passing counts, 2-decimal rounded signal efficiencies $\epsilon_S$, and Significance Improvements $\text{SI}(\epsilon_B) = \epsilon_S / \sqrt{\epsilon_B}$ at $\epsilon_B \in \{10^{-2}, 10^{-3}, 10^{-4}\}$.
2. **Live Unsupervised Training & Threshold Calibration on Channel 2a (`verify-it-yourself/data/chan2a_*.npz`)**:
   - Retrained all 3 detectors from scratch on the `11,628` odd-`event_ID` Standard Model background events in Channel `2a`.
   - Calibrated exact tie-aware background thresholds $\tau(\epsilon_B)$ on the `8,377` even-`event_ID` SM background events, confirming empirical false-positive rates $\text{mean}(s_{\text{bg}} \ge \tau) \le \epsilon_B$ at all three working points.
   - Scored all 7 BSM signals in Channel `2a` (`chaneut_cha200_neut50`, `chaneut_cha250_neut150`, `chaneut_cha300_neut100`, `chaneut_cha400_neut200`, `gluino_1000.0_neutralino_1.0`, `pp23mt_50`, `pp24mt_50`).
3. **Partial Win `p1` & Minimum-TI Floor (`object/darkmachines_19signals_summary.tsv`)**:
   - `chaneut_cha300_neut100`: **`TI = 1.4000`** (`PotHull_Hybrid_Lp3`), **`TI = 1.6000`** (`PotStrataZ_Lp3`), and **`TI = 1.2000`** (`PotHull_L1_L2_Hull`), all strictly beating `1.1000` (the maximum across all 1,040 challenge detectors).
   - `chaneut_cha400_neut200`: **`TI = 1.6000`** (`PotHull_Hybrid_Lp3`), **`TI = 1.7000`** (`PotStrataZ_Lp3`), and **`TI = 1.6000`** (`PotHull_L1_L2_Hull`), all strictly beating `1.0000` (the maximum across all 1,040 challenge detectors; `Flow-Efficient_Likelihood` is `0.9000`).
   - Minimum TI across all 19 BSM signals: **`Min_TI = 1.0000 >= 0.9000`** (`PotHull_Hybrid_Lp3` and `PotHull_L1_L2_Hull`).
