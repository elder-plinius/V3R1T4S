# Run It Yourself

## 1. Quick Self-Contained Verification (`< 3` seconds)
From the package root directory, run:
```bash
sh verify-it-yourself/run_checks.sh
```
This script:
1. Loads the 27-invariant Channel `2a` training background (`verify-it-yourself/data/chan2a_bg_odd.npz`, `11,628` odd-`event_ID` events), evaluation background (`chan2a_bg_even.npz`, `8,377` even-`event_ID` events), and all 7 Channel `2a` BSM signal sets (`chan2a_signals.npz`).
2. Trains `PotHull_Hybrid_Lp3`, `PotStrataZ_Lp3`, and `PotHull_L1_L2_Hull` from scratch on the odd-`event_ID` background only, verifies that exact tie-aware thresholds satisfy $\text{FPR} \le \epsilon_B$ at $10^{-2}, 10^{-3}, 10^{-4}$, and verifies that `chaneut_cha300_neut100` achieves `TI = 1.40 / 1.60 > 1.10` (`p1`) and `chaneut_cha400_neut200` achieves `TI = 1.60 / 1.70 > 1.00` (`p1`).
3. Audits every cell of `object/darkmachines_27invariant_pot_results.csv` (`102` rows) and `object/darkmachines_19signals_summary.tsv` (`19` rows), printing `PASS` at exit code `0`.

## 2. Full End-to-End Reproduction From Raw Zenodo 3961917 CSVs
To re-run all 4 channels (`chan1`, `chan2a`, `chan2b`, `chan3`, 8.5M background events total) from the raw Zenodo 3961917 archive (`Unsupervised_DarkMachines.tar.gz`):
```bash
cc -O3 how-we-built-it/dm_featurize.c -lm -o dm_featurize
# Featurize each CSV into binary cache per channel, then run:
python3 how-we-built-it/run_darkmachines_pot.py --cache-dir /path/to/cache
```
