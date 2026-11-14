# Verification Receipts (`verify-it-yourself/RECEIPTS.md`)

## 1. Command & Runtime

- **Command:** `sh verify-it-yourself/run_checks.sh`
- **Interpreter:** `/opt/homebrew/bin/python3 -B verify-it-yourself/check_meteor_claim.py`
- **Elapsed Time:** `0.15 s`
- **Exit Code:** `0` (`PASS`)

## 2. Exact Stdout Transcript

```text
[1/4] GMN & IAU MDC Manifest Verified: 9 GMN yearly files (3,599,504 trajectories) + live Nov 03, 2026 IAU MDC streamfulldata2026.txt (2,197 rows, sha256=ae1a84a546be...)
[2/4] Single-Claim Cluster Verified (M1_Cepheus_MC): N=16 deduplicated meteors across 4 years [2023, 2024, 2025, 2026], 16/16 with num_stat>=3 (3..8) & n_countries>=2 (2..3), 15 countries, 62 distinct stations, min_dt=1332.4s
[3/4] Orbital D_SH & 2,197-Row MDC Isolation Verified: max_D_SH(mean)=0.0730<0.10, max_D_SH(median)=0.0795<0.10, medoid=20260907031956_faRoT (mean=0.0538, max=0.0707), min_MDC_D_SH=0.2819>=0.20, min_rad_sep=19.52 deg>5.0 deg
[4/4] Significance & Look-Elsewhere Verified: real=16 vs best_control=7 (400 controls, mu=1.0925), single-window Z=14.26 sigma (Poisson 7.66 sigma), global Z=7.03 sigma (103 windows) / 6.11 sigma (43,228 seeds) > 5.0 sigma
PASS
```

## 3. Artifact Digests Checked

| Artifact | Purpose | SHA-256 Digest |
| :--- | :--- | :--- |
| `object/m1_cepheus_mc_gmn_lines.txt` | 16 verbatim GMN trajectory rows of `GMN_NEW_SHOWER_M1_CEPHEUS_MC_163` (`IAU No == -1`, `num_stat >= 3`, `n_countries >= 2`) | `4f0bf9a2e5e1c56ac61f582a63923c4af28d6536a00bd1df7bf6203796b5212d` |
| `object/gmn_yearly_manifest.json` | URL, byte size, row count, and SHA-256 citations for the 9 GMN yearly files (`2018–2026`) and the live 3 November 2026 IAU MDC `streamfulldata2026.txt` (`2,197` rows) | Verified by `verify-it-yourself/check_meteor_claim.py` |
| `object/new_shower_cluster.json` | Single-claim certificate: 16 member records, mean/median/medoid orbits, $16 \times 16$ pairwise $D_{\text{SH}}$ matrices, and 156 reference/neighbor IAU MDC rows (`LP = 00001..02650`) | Verified by `verify-it-yourself/check_meteor_claim.py` |
| `object/null_test_400_controls.json` | 400-control shuffle/permutation null test, cross-year baseline counts (`2018–2022`), look-elsewhere corrections (`103`, `360`, `43,228`, `173,358` windows), and 166 external multi-country reference orbits | Verified by `verify-it-yourself/check_meteor_claim.py` |
