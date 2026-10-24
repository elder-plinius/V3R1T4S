# Null Model Control Test (`iau-mdc-new-meteor-shower-gmn`)

controls: 400
best_control: 3
real: 20
command: /opt/homebrew/bin/python3 claim/verify_meteor_discovery.py --verify-null-controls
real_beats_all_controls: yes

## Summary of 400 Monte Carlo Background Controls

- **Number of independent synthetic background controls per candidate**: `400` (`200` solar-longitude shuffle controls rotating $\lambda_\odot$ across the $\pm 30^\circ$ sporadic band and shifting $\Omega$ by $\Delta\lambda_\odot$ + `200` orbital-element tuple permutations decoupling $(q, e, i, \omega)$ from $(\lambda_\odot, \Omega)$)
- **Primary Main Cluster (`GMN_NEW_SHOWER_M2_HERCULES_339`, `new_shower_cluster.json`, `new_shower_gmn_lines.txt`)**:
  - `controls`: `400`
  - `real`: `20` (across 5 years `2022–2026`, `min_num_stat = 3`, `7` countries, $\max D_{\text{SH}} = 0.0491 < 0.10$, $\min D_{\text{SH}}(\text{MDC}) = 0.3539 \ge 0.20$)
  - `best_control`: `3` (`control_mean = 0.5275`, `control_std = 0.6822`, `sideband_mean = 0.4000`, histogram `{0: 227, 1: 140, 2: 28, 3: 5}`)
  - `real_beats_all_controls`: `yes` (`20 > 3`, Gaussian $Z = 26.81\sigma$, Poisson tail $\log_{10} p = -24.16$, equivalent $10.46\sigma$)
- **Secondary Main Cluster (`M1_Cepheus_Core`, `m1_cepheus_core_gmn_lines.txt`)**:
  - `controls`: `400`, `real`: `15`, `best_control`: `2` (`control_mean = 0.1975`), `real_beats_all_controls`: `yes` ($Z = 33.31\sigma$, Poisson equivalent $10.15\sigma$)
- **Strict Per-Meteor Multi-Country Main Cluster (`M1_Cepheus_MC`, `m1_cepheus_mc_gmn_lines.txt`, 100% per-meteor `n_countries >= 2`)**:
  - `controls`: `400`, `real`: `15`, `best_control`: `7` (`control_mean = 1.0925`), `real_beats_all_controls`: `yes` ($Z = 13.31\sigma$, Poisson equivalent $7.30\sigma$)
- **High-Inclination Main Cluster (`M3_Camelopardalis`, `m3_camelopardalis_gmn_lines.txt`)**:
  - `controls`: `400`, `real`: `16`, `best_control`: `2` (`control_mean = 0.1200`), `real_beats_all_controls`: `yes` ($Z = 45.84\sigma$, Poisson equivalent $11.30\sigma$)
- **Enumerated Partial Win `p1` 6-Hour Single-Night Outburst (`GMN_P1_OUTBURST_2025_SEP01_CYG_DRA`, `p1_outburst_cluster.json`, `p1_outburst_gmn_lines.txt`)**:
  - `controls`: `400`, `real`: `10` (within `4.84 h <= 6.0 h`, $\max D_{\text{SH}} = 0.0619 < 0.08$, $\min D_{\text{SH}}(\text{MDC}) = 0.2521 \ge 0.20$), `best_control`: `3` (`control_mean = 0.4800`, `sideband_mean = 0.7500`, cross-year counts in same $0.25^\circ$ solar-longitude window `{2019: 0, 2020: 0, 2021: 0, 2022: 1, 2023: 0, 2024: 0}`), `real_beats_all_controls`: `yes` ($Z = 10.68\sigma$, Poisson equivalent $5.96\sigma$)
