# Dark Machines Unsupervised Anomaly Detection — 27-Invariant POT Detector (`p1`: `cha300 TI = 1.40 / 1.60 > 1.10`, `cha400 TI = 1.60 / 1.70 > 1.00`, `Min_TI = 1.00 >= 0.90`)

## What

Strictly unsupervised 27-invariant Upper-Tail Log-Survival Peaks-Over-Threshold (POT) detectors (PotHull_Hybrid_Lp3, PotStrataZ_Lp3, and PotHull_L1_L2_Hull) trained exclusively on odd-event_ID Standard Model background events per channel in the Dark Machines Anomaly Score Challenge (Zenodo 3961917, 4 channels, 34 channel-signal files, 19 BSM signals), with tie-aware thresholds calibrated on even-event_ID SM background events and signal efficiencies rounded to 2 decimals per notebooks/04-SignificanceImprovement.ipynb. Achieves partial win p1 by beating all 1,040 challenge detectors on both chargino-neutralino bottleneck signals in Channel 2a: chaneut_cha300_neut100 TI = 1.4000 (PotHull_Hybrid_Lp3) and 1.6000 (PotStrataZ_Lp3) > 1.1000 (best of 1,040 detectors), and chaneut_cha400_neut200 TI = 1.6000 (PotHull_Hybrid_Lp3) and 1.7000 (PotStrataZ_Lp3) > 1.0000 (best of 1,040 detectors; Flow-Efficient_Likelihood is 0.9000), while simultaneously achieving Min_TI = 1.0000 >= 0.9000 across all 19 BSM signals (PotHull_Hybrid_Lp3 and PotHull_L1_L2_Hull) and TI = 24.0000 > 15.0000 on gluino_1000.0_neutralino_1.0.

## Check It Yourself

Run the standalone verification script from the package root:

```bash
sh verify-it-yourself/run_checks.sh
```

This executes `verify-it-yourself/check_darkmachines.py` (`< 3` seconds runtime), which:
1. Retrains `PotHull_Hybrid_Lp3`, `PotStrataZ_Lp3`, and `PotHull_L1_L2_Hull` live from scratch on the `11,628` odd-`event_ID` SM background events of Channel `2a` (`verify-it-yourself/data/chan2a_bg_odd.npz`), calibrates exact tie-aware thresholds on the `8,377` even-`event_ID` SM background events (`chan2a_bg_even.npz`), and scores all 7 Channel `2a` BSM signals (`chan2a_signals.npz`).
2. Independently verifies all 102 signal-channel rows (`34` channel-signal pairs $\times$ `3` models) in `object/darkmachines_27invariant_pot_results.csv` and all 19 per-signal Total Improvement summaries in `object/darkmachines_19signals_summary.tsv`.
3. Confirms `p1` (`chaneut_cha300_neut100` $\text{TI} = 1.4000 / 1.6000 > 1.1000$ and `chaneut_cha400_neut200` $\text{TI} = 1.6000 / 1.7000 > 1.0000$) and $\text{Min\_TI} = 1.0000 \ge 0.9000$.

## Compared To

- **Published Challenge Benchmark (Aarrestad et al., *SciPost Phys.* 12, 043, 2022, `arXiv:2105.14027`; `bostdiek/DarkMachines-UnsupervisedChallenge`, 1,040 Detectors)**:
  - **`p1` (`chaneut_cha300_neut100` in Channel 2a)**: Best across all 1,040 detectors is **`1.1000`** (`Flow-Efficient_Likelihood`).
  - **`p1` (`chaneut_cha400_neut200` in Channel 2a)**: Best across all 1,040 detectors is **`1.0000`** (`Combined-AVG-DeepSVDD-Flow` and `Combined-PROD-DeepSVDD-Flow`; `Flow-Efficient_Likelihood` achieves `0.9000`).
  - **Minimum TI across all 19 BSM signals**: Best across all 1,040 detectors is **`0.9000`** (`Flow-Efficient_Likelihood`), followed by `0.6325` (`Combined-AVG-DeepSVDD-Flow`).
- **This Submission (`object/darkmachines_27invariant_pot_results.csv`, `object/darkmachines_19signals_summary.tsv`)**:
  - **`chaneut_cha300_neut100`**: **`1.4000`** (`PotHull_Hybrid_Lp3`, `+27.3%`), **`1.6000`** (`PotStrataZ_Lp3`, `+45.5%`), and **`1.2000`** (`PotHull_L1_L2_Hull`, `+9.1%`), all strictly above `1.1000` (`p1`).
  - **`chaneut_cha400_neut200`**: **`1.6000`** (`PotHull_Hybrid_Lp3`, `+60.0%`), **`1.7000`** (`PotStrataZ_Lp3`, `+70.0%`), and **`1.6000`** (`PotHull_L1_L2_Hull`, `+60.0%`), all strictly above `1.0000` (`p1`).
  - **Minimum TI across all 19 signals**: **`1.0000 >= 0.9000`** (`PotHull_Hybrid_Lp3` and `PotHull_L1_L2_Hull`).
  - **`gluino_1000.0_neutralino_1.0` (Channel 2b)**: **`24.0000`** (`PotHull_Hybrid_Lp3`), beating `Flow-Efficient_Likelihood` (`15.0000`).

## Not Claimed

- Full-target `win` (`Median TI > 15.0`) and partial wins `p2` (`Median TI > 10.0`) and `p3` (`beating the best of 1,040 detectors on >= 10/19 signals simultaneously`) are not claimed (`Median TI = 2.80 - 3.00` under strict non-tie evaluation); this submission claims partial win `p1`.

## Credits

- Contributor: `@HindsightWise`
- Prior work:
  - T. Aarrestad et al., "The Dark Machines Anomaly Score Challenge: Benchmark Data and Model Independent Event Classification for the Large Hadron Collider," *SciPost Phys.* 12, 043 (2022), `arXiv:2105.14027`, Zenodo `3961917` (`https://zenodo.org/records/3961917`), and `https://github.com/bostdiek/DarkMachines-UnsupervisedChallenge`.
  - C. G. Lester & D. J. Summers, "Measuring masses of semi-invisibly decaying particles pair produced at hadron colliders," *Phys. Lett. B* 463, 99-103 (1999) ($M_{T2}$ stransverse mass).
