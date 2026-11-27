# 400-Control Null Test & Look-Elsewhere Report (`how-we-built-it/null_test.md`)

controls: 400
real: 16
best_control: 7
real_beats_all_controls: yes
command: /opt/homebrew/bin/python3 how-we-built-it/discover_new_showers.py

## 1. Null-Test Summary (`object/null_test_400_controls.json`)

- `candidate_id`: `GMN_NEW_SHOWER_M1_CEPHEUS_MC_163` (`M1_Cepheus_MC`, $N = 16$ deduplicated multi-country trajectories)
- `controls`: `400` (`200` solar-longitude shuffle controls + `200` orbital-tuple permutation controls)
- `real`: `16`
- `best_control`: `7`
- `real_beats_all_controls`: `yes`

## 2. Background Estimation Methods (`target.md`)

We evaluate the local sporadic background for `GMN_NEW_SHOWER_M1_CEPHEUS_MC_163` ($\lambda_\odot \in [162.01^\circ, 165.54^\circ]$, mean orbit $q = 0.9573\text{ AU}, e = 0.7191, i = 41.84^\circ, \Omega = 163.31^\circ, \omega = 208.37^\circ$, ball radius $D_{\text{SH}} < 0.075$) using both methods specified in `target.md`:

### Method A — Background from the Same Solar-Longitude Window in Other Years & Sidebands

1. **Same solar-longitude window ($\lambda_\odot \in [161.56^\circ, 165.06^\circ]$, $D_{\text{SH}} < 0.075$) across the 5 prior GMN baseline years (`2018–2022`):**
   - `2018`: `0` trajectories
   - `2019`: `0` trajectories
   - `2020`: `0` trajectories
   - `2021`: `0` trajectories
   - `2022`: `0` trajectories
   - Active years (`2023–2026`): `2023`: `1`, `2024`: `2`, `2025`: `5`, `2026`: `8` (`16` total; note that trajectory `20230905191934_2YuSb` and `20230906022249_hhc3N` both belong to `2023` in the full $3.53^\circ$ span).
2. **20 adjacent $3.5^\circ$ solar-longitude sideband windows** ($\Delta\lambda_\odot \in \{-25^\circ, -23^\circ, \dots, -7^\circ, +6^\circ, +8^\circ, \dots, +24^\circ\}$ with $\Omega$ shifted by $\Delta\lambda_\odot$):
   - `0` trajectories in all 20 windows (`sideband_mean = 0.0000`).

### Method B — 400-Control Shuffled-Solar-Longitude & Orbital-Permutation Monte Carlo Bootstrap

Excluding the 16 signal members from the surrounding $60^\circ$ sporadic solar-longitude band $\lambda_\odot \in [133.31^\circ, 193.31^\circ]$:
1. **Control Group 1 (`200` solar-longitude shuffle controls):** Uniformly shuffle $\lambda_\odot$ across the $60^\circ$ band $[-30^\circ, +30^\circ]$ around $\lambda_\odot = 163.31^\circ$, shifting $\Omega \mapsto (\Omega + \Delta\lambda_\odot) \bmod 360^\circ$ while preserving $(q, e, i, \omega)$, and count simulated trajectories landing within the $3.5^\circ$ solar-longitude window and $D_{\text{SH}} < 0.075$.
2. **Control Group 2 (`200` orbital-tuple permutation controls):** Independently permute $(q, e, i, \omega)$ against $(\lambda_\odot, \Omega)$ within the local $3.5^\circ$ solar-longitude window and count simulated trajectories within $D_{\text{SH}} < 0.075$.
3. **Live Verification Bootstrap (`1,000` trials in `verify-it-yourself/check_meteor_claim.py`):** Shuffles the `166` external multi-country unassigned reference orbits stored in `object/null_test_400_controls.json` across $[-30^\circ, +30^\circ]$ around $\lambda_\odot = 163.31^\circ$, confirming max random count $\ll 16$.

### Control Distribution (`400` Controls)

| Control Count ($k$) | `0` | `1` | `2` | `3` | `4` | `5` | `6` | `7` | $\ge 8$ | Observed (`M1_Cepheus_MC`) |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| **Frequency (out of 400)** | `129` | `150` | `84` | `32` | `4` | `0` | `0` | `1` | `0` | **`16`** |

- `control_mean` $\mu_{\text{ctrl}} = 1.0925$
- `control_std` $\sigma_{\text{ctrl}} = 1.0132$
- `effective_bg_sigma` $\sigma_{\text{eff}} = \max(\sigma_{\text{ctrl}}, \sqrt{\mu_{\text{ctrl}}}) = 1.0452$
- `z_score_sigma` $= (16 - 1.0925) / 1.0452 = \mathbf{14.26\sigma > 5.0\sigma}$
- Exact single-window Poisson tail $P(\text{Pois}(1.0925) \ge 16) = \mathbf{7.0533 \times 10^{-14}}$ ($\log_{10} p = -13.15$, one-sided Gaussian equivalent $\mathbf{Z_{\text{Pois}} = 7.66\sigma > 5.0\sigma}$)

---

## 3. Look-Elsewhere Correction With Number of Windows Searched

| Search Space Level | Windows / Seeds Searched ($N_{\text{trials}}$) | Global $p$-Value ($1 - (1 - p_1)^{N_{\text{trials}}}$) | $\log_{10} p_{\text{global}}$ | Global Gaussian Equivalent $Z_{\text{global}}$ |
| :--- | :-: | :-: | :-: | :-: |
| **Single $3.5^\circ$ solar-longitude window** | `1` | `7.0533e-14` | `-13.15` | **`7.66 sigma`** (`14.26 sigma` linear) |
| **Full ecliptic in non-overlapping $3.5^\circ$ windows** ($360^\circ / 3.5^\circ$) | `103` | `7.2649e-12` | `-11.14` | **`7.03 sigma > 5.0 sigma`** |
| **Full ecliptic in $1^\circ$ solar-longitude bins** | `360` | `2.5392e-11` | `-10.60` | **`6.85 sigma > 5.0 sigma`** |
| **All MDC-isolated multi-country seed trajectories** ($D_{\text{SH}} \ge 0.22, \Delta\theta > 10^\circ$) | `43,228` | `3.0490e-09` | `-8.52` | **`6.11 sigma > 5.0 sigma`** |
| **All high-quality unassigned multi-country GMN trajectories** (`num_stat >= 3, n_countries >= 2`) | `173,358` | `1.2227e-08` | `-7.91` | **`5.88 sigma > 5.0 sigma`** |
