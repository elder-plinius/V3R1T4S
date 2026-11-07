# Run It Yourself (`RUN_IT_YOURSELF.md`)

## One-Command Verification

From the package root (`known-knowns/iau-mdc-new-meteor-shower-gmn/2026-10-20-mizopl-56ac1336/`):

```sh
sh verify-it-yourself/run_checks.sh
```

### Expected Output (`~0.15 s`, Exit Code `0`)

```text
[1/4] GMN & IAU MDC Manifest Verified: 9 GMN yearly files (3,599,504 trajectories) + live Nov 03, 2026 IAU MDC streamfulldata2026.txt (2,197 rows, sha256=ae1a84a546be...)
[2/4] Single-Claim Cluster Verified (M1_Cepheus_MC): N=16 deduplicated meteors across 4 years [2023, 2024, 2025, 2026], 16/16 with num_stat>=3 (3..8) & n_countries>=2 (2..3), 15 countries, 62 distinct stations, min_dt=1332.4s
[3/4] Orbital D_SH & 2,197-Row MDC Isolation Verified: max_D_SH(mean)=0.0730<0.10, max_D_SH(median)=0.0795<0.10, medoid=20260907031956_faRoT (mean=0.0538, max=0.0707), min_MDC_D_SH=0.2819>=0.20, min_rad_sep=19.52 deg>5.0 deg
[4/4] Significance & Look-Elsewhere Verified: real=16 vs best_control=7 (400 controls, mu=1.0925), single-window Z=14.26 sigma (Poisson 7.66 sigma), global Z=7.03 sigma (103 windows) / 6.11 sigma (43,228 seeds) > 5.0 sigma
PASS
```

## What `verify-it-yourself/check_meteor_claim.py` Checks

1. **Manifest & Upstream Citations (`object/gmn_yearly_manifest.json`):**
   - Verifies the SHA-256 and URL citations for all 9 GMN yearly trajectory summary tables (`traj_summary_yearly_2018.txt` through `traj_summary_yearly_2026.txt`, `3,599,504` total trajectories) and the live 3 November 2026 IAU MDC `streamfulldata2026.txt` (`2,197` rows, `sha256: ae1a84a546be1c72ee0cf74835bc5b928a0d1d4c4e01a18a7f17bdaee299e100`), `roje_lista.php`, and `new_reports.php`.
2. **Per-Meteor Station & Country Split + Deduplication (`object/m1_cepheus_mc_gmn_lines.txt`):**
   - Parses all 16 verbatim GMN trajectory rows, splits `stations` on commas, verifies every station code matches `^[A-Z]{2}[0-9A-Z]{4}$`, and checks `len(stations) == num_stat >= 3` and `len(countries) == n_countries >= 2` for every one of the 16 members (`16/16 = 100%`).
   - Verifies that all 16 trajectories represent distinct meteors ($\min \Delta t = 1,332.405\text{ s} > 60\text{ s}$) across `4` consecutive years (`2023–2026`), `15` countries, and `62` distinct GMN stations.
3. **Orbital $D_{\text{SH}}$ Matrix & 3 November 2026 IAU MDC Isolation (`object/new_shower_cluster.json`):**
   - Recomputes the exact spherical ($\Pi_{AB}$) and planar ($\Delta\varpi$) Southworth–Hawkins $D_{\text{SH}}$ directly from $(q, e, i, \Omega, \omega)$ for the $16 \times 16$ pairwise matrix, mean orbit, median orbit, and medoid (`20260907031956_faRoT`), verifying $\max D_{\text{SH,exact}}(\text{mean}) = 0.073001 < 0.10$, $\max D_{\text{SH,exact}}(\text{median}) = 0.079486 < 0.10$, and single-linkage connectedness at $D_{\text{SH}} \le 0.10$.
   - Recomputes $D_{\text{SH}}$ and radiant separation $\Delta\theta$ against the 156 reference/neighbor IAU MDC rows (including all 5 rows `LP = 02646..02650` added on 3 November 2026), confirming $\min D_{\text{SH}} = 0.281872 \ge 0.20$ and $\min \Delta\theta = 19.5245^\circ > 5.0^\circ$.
4. **400-Control Null Test, Live Bootstrap & Look-Elsewhere Correction (`object/null_test_400_controls.json`):**
   - Verifies `real = 16 > best_control = 7`, `control_mean = 1.0925`, `z_score_sigma = 14.26 > 5.0`, single-window Poisson $Z_{\text{Pois}} = 7.66\sigma > 5.0\sigma$, look-elsewhere corrected $Z$-scores across `103` ecliptic $3.5^\circ$ windows (`7.03 sigma`), `360` $1^\circ$ bins (`6.85 sigma`), `43,228` MDC-isolated multi-country seeds (`6.11 sigma`), and `173,358` unassigned multi-country HQ trajectories (`5.88 sigma`), and runs a live 1,000-trial shuffled-solar-longitude bootstrap over the 166 external multi-country reference orbits.
