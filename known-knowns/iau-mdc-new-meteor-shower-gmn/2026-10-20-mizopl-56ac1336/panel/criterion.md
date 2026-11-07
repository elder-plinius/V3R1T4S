# Criterion Skeptic Report (`panel/criterion.md`)

role: criterion
context: fresh review session inspecting object/ and verify-it-yourself/
target_id: iau-mdc-new-meteor-shower-gmn
verdict: PASS

## 1. Single-Claim Package Audit (`kit/SUBMIT.md` §1)

- This package files **strictly one claim**: the multi-year, per-meteor multi-country September Cepheus meteor shower candidate `GMN_NEW_SHOWER_M1_CEPHEUS_MC_163` (`M1_Cepheus_MC`, $N = 16$).
- Earlier multi-claim bundles (`M2_Hercules`, `M1_Cepheus_Core` single-country members, `M3_Camelopardalis`, the `p1` 6-hour outburst, and `p2` working-list recurrences) have been removed from `object/` so that `object/` contains only the single claim's artifacts (`object/m1_cepheus_mc_gmn_lines.txt`, `object/new_shower_cluster.json`, `object/null_test_400_controls.json`, and `object/gmn_yearly_manifest.json`).

## 2. Clause-by-Clause Target Criterion Audit

| Target Clause (`target.md`) | Required Threshold | Verified Value (`object/new_shower_cluster.json` & `object/m1_cepheus_mc_gmn_lines.txt`) | Status |
| :--- | :--- | :--- | :--- |
| **1. Public GMN trajectory summary tables** | Verbatim trajectories from `traj_summary_yearly_*.txt` (`IAU No == -1`) | `16` verbatim rows in `object/m1_cepheus_mc_gmn_lines.txt` (`sha256: 4f0bf9a2e5e1c56ac61f582a63923c4af28d6536a00bd1df7bf6203796b5212d`), all with `IAU No == -1`, cited against the 9 GMN yearly files (`2018–2026`) by URL and SHA-256 in `object/gmn_yearly_manifest.json`. | **PASS** |
| **2. Count each meteor once (no duplicate solutions)** | Distinct physical meteors ($\Delta t \gg 2\text{ s}$) | `16` unique meteors; minimum pairwise time separation $\min \Delta t = 1,332.405\text{ s}$ (`22.21 minutes`). The duplicate trajectory solution `20260907031956_h3OXu` (solved `0.105 s` after `20260907031956_faRoT`) and all 8 single-country members of the earlier `M1_Cepheus_Core` slice (including `20250904204409_BKOSN`) are excluded. | **PASS** |
| **3. Cluster size & multi-year span** | $N \ge 15$ multi-station trajectories across $\ge 3$ distinct years | $N = 16 \ge 15$ trajectories across $4 \ge 3$ consecutive years: `2023` (`2`), `2024` (`3`), `2025` (`4`), `2026` (`7`). | **PASS** |
| **4. Per-meteor independent stations & countries** | $\ge 3$ independent stations in $\ge 2$ countries **for every member counted** | `16/16` (`100%`) members individually satisfy `num_stat >= 3` (`3..8` stations per meteor, matching `len(stations)`) and `n_countries >= 2` (`2..3` countries per meteor). Union spans `15` countries (`AT, BA, BE, BG, CZ, DE, DK, FR, HR, HU, IT, NL, RO, SI, UK`) and `62` distinct GMN station codes. | **PASS** |
| **5. Internal orbital cohesion ($D_{\text{SH}} < 0.10$)** | Every member satisfies $D_{\text{SH}} < 0.10$ to cluster mean/median orbit | $\max D_{\text{SH,exact}}(\text{mean}, \text{member}) = 0.073001 < 0.10$ ($\text{planar} = 0.071959 < 0.10$); $\max D_{\text{SH,exact}}(\text{median}, \text{member}) = 0.079486 < 0.10$ ($\text{planar} = 0.083053 < 0.10$); medoid `20260907031956_faRoT` has mean $D_{\text{SH}} = 0.053828$ and max $D_{\text{SH}} = 0.070696 < 0.10$; single-linkage graph is a single connected component at $D_{\text{SH}} \le 0.10$. | **PASS** |
| **6. IAU MDC orbital & radiant isolation (3 Nov 2026 live list, 2,197 rows)** | $D_{\text{SH}} \ge 0.20$ from every IAU MDC entry and radiant separation $> 5^\circ$ at matched solar longitude | Evaluated against all `2,197` rows of the live 3 November 2026 `streamfulldata2026.txt` (`sha256: ae1a84a546be1c72ee0cf74835bc5b928a0d1d4c4e01a18a7f17bdaee299e100`, including new rows `LP = 02646..02650`): $\min D_{\text{SH}}(\text{mean}, \text{MDC}) = 0.281872 \ge 0.20$ (`53-Draconids / FDR #01206`, `LP = 02584`), $\min D_{\text{SH}}(\text{member}, \text{MDC}) = 0.251127 \ge 0.20$, $\min \Delta\theta = 19.5245^\circ > 5.0^\circ$ within $|\Delta\lambda_\odot| \le 5.0^\circ$ (`nu-Draconids / NDR #00220`, `LP = 00731`), and $\min \Delta\theta = 9.4502^\circ > 5.0^\circ$ across active intervals $[\lambda_{\odot,b}-5^\circ, \lambda_{\odot,e}+5^\circ]$. | **PASS** |
| **7. Local sporadic background excess ($> 5\sigma$) with number of windows searched** | Overdensity $> 5\sigma$ above local sporadic background (same solar-longitude window in other years or shuffled-solar-longitude bootstrap), with number of windows searched | **Same window in baseline years (`2018–2022`):** `0` trajectories in all 5 prior years (`2018: 0, 2019: 0, 2020: 0, 2021: 0, 2022: 0`) and `0` in all 20 adjacent $3.5^\circ$ solar-longitude sideband windows (`sideband_mean = 0.0`).<br>**400-control shuffled-solar-longitude & orbital-permutation test:** `real = 16` vs `best_control = 7`, `control_mean = 1.0925`, `control_std = 1.0132`, `effective_bg_sigma = 1.0452`, single-window Gaussian $Z = 14.26\sigma > 5.0\sigma$, single-window Poisson tail $p = 7.0533 \times 10^{-14}$ ($\log_{10} p = -13.15$, $Z_{\text{Pois}} = 7.66\sigma > 5.0\sigma$).<br>**Look-elsewhere corrected significance across searched windows:**<br>• `103` ecliptic $3.5^\circ$ solar-longitude windows: $p_{\text{global}} = 7.2649 \times 10^{-12}$ ($Z_{\text{global}} = 7.03\sigma > 5.0\sigma$)<br>• `360` ecliptic $1^\circ$ solar-longitude bins: $p_{\text{global}} = 2.5392 \times 10^{-11}$ ($Z_{\text{global}} = 6.85\sigma > 5.0\sigma$)<br>• `43,228` MDC-isolated multi-country seed trajectories: $p_{\text{global}} = 3.0490 \times 10^{-9}$ ($Z_{\text{global}} = 6.11\sigma > 5.0\sigma$)<br>• `173,358` unassigned multi-country HQ trajectories: $p_{\text{global}} = 1.2227 \times 10^{-8}$ ($Z_{\text{global}} = 5.88\sigma > 5.0\sigma$). | **PASS** |

## Conclusion

Every requirement of `target.md` and all six review items are satisfied with margin.

pass: true
