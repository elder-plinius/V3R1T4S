# Reproduce Skeptic Report (`panel/reproduce.md`)

role: reproduce
context: fresh review session inspecting object/ and verify-it-yourself/
target_id: iau-mdc-new-meteor-shower-gmn
verdict: PASS

## 1. Standalone Verification Command

From the package root (`known-knowns/iau-mdc-new-meteor-shower-gmn/2026-10-20-mizopl-56ac1336/`):

```sh
sh verify-it-yourself/run_checks.sh
```

### Observed Output (`~0.15 s`, Exit Code `0`)

```text
[1/4] GMN & IAU MDC Manifest Verified: 9 GMN yearly files (3,599,504 trajectories) + live Nov 03, 2026 IAU MDC streamfulldata2026.txt (2,197 rows, sha256=ae1a84a546be...)
[2/4] Single-Claim Cluster Verified (M1_Cepheus_MC): N=16 deduplicated meteors across 4 years [2023, 2024, 2025, 2026], 16/16 with num_stat>=3 (3..8) & n_countries>=2 (2..3), 15 countries, 62 distinct stations, min_dt=1332.4s
[3/4] Orbital D_SH & 2,197-Row MDC Isolation Verified: max_D_SH(mean)=0.0730<0.10, max_D_SH(median)=0.0795<0.10, medoid=20260907031956_faRoT (mean=0.0538, max=0.0707), min_MDC_D_SH=0.2819>=0.20, min_rad_sep=19.52 deg>5.0 deg
[4/4] Significance & Look-Elsewhere Verified: real=16 vs best_control=7 (400 controls, mu=1.0925), single-window Z=14.26 sigma (Poisson 7.66 sigma), global Z=7.03 sigma (103 windows) / 6.11 sigma (43,228 seeds) > 5.0 sigma
PASS
```

## 2. Independent Checks Executed by `verify-it-yourself/check_meteor_claim.py`

1. **Manifest & Citation Integrity (`object/gmn_yearly_manifest.json`):**
   - Verifies URL, byte size, row count, and SHA-256 citations for all 9 GMN yearly files (`traj_summary_yearly_2018.txt` through `traj_summary_yearly_2026.txt`, `3,599,504` total trajectories) and the live 3 November 2026 IAU MDC `streamfulldata2026.txt` (`2,197` rows, `sha256: ae1a84a546be1c72ee0cf74835bc5b928a0d1d4c4e01a18a7f17bdaee299e100`), `roje_lista.php`, and `new_reports.php`.
   - Verifies that `member_lines_sha256` matches the live SHA-256 of `object/m1_cepheus_mc_gmn_lines.txt` (`4f0bf9a2e5e1c56ac61f582a63923c4af28d6536a00bd1df7bf6203796b5212d`).
2. **Per-Meteor Station & Country Split + Deduplication (`object/m1_cepheus_mc_gmn_lines.txt` vs `object/new_shower_cluster.json`):**
   - Parses all 16 verbatim GMN trajectory rows, splits station codes on commas, verifies every station matches `^[A-Z]{2}[0-9A-Z]{4}$`, and checks `len(stations) == num_stat >= 3` and `len(countries) == n_countries >= 2` for every one of the 16 members (`16/16 = 100%`).
   - Checks that all 16 trajectory IDs are unique and sorted chronologically with minimum pairwise time separation $\Delta t = 1,332.405\text{ s} > 60\text{ s}$.
   - Cross-checks every orbital, radiant, coordinate, and station field between `object/m1_cepheus_mc_gmn_lines.txt` and `object/new_shower_cluster.json`.
3. **Exact Orbital $D_{\text{SH}}$ Recomputation & Single-Linkage Connectedness:**
   - Recomputes the exact spherical ($\Pi_{AB}$) and planar ($\Delta\varpi$) Southworth–Hawkins $D_{\text{SH}}$ directly from $(q, e, i, \Omega, \omega)$ for the $16 \times 16$ pairwise matrix, the mean orbit, the median orbit, and the medoid (`20260907031956_faRoT`), verifying $\max D_{\text{SH,exact}}(\text{mean}) = 0.073001 < 0.10$, $\max D_{\text{SH,exact}}(\text{median}) = 0.079486 < 0.10$, and single-linkage connectedness at $D_{\text{SH}} \le 0.10$.
   - Recomputes $D_{\text{SH}}$ and radiant separation $\Delta\theta$ across all 156 reference/neighbor IAU MDC rows (including `LP = 02646..02650` from the 3 November 2026 update), confirming $\min D_{\text{SH}} = 0.281872 \ge 0.20$ and $\min \Delta\theta = 19.5245^\circ > 5.0^\circ$.
4. **400-Control Null Test, Live Bootstrap & Look-Elsewhere Verification (`object/null_test_400_controls.json`):**
   - Recomputes the control mean (`1.0925`), control standard deviation (`1.0132`), single-window Gaussian $Z$ (`14.26 sigma`), single-window Poisson tail $p = 7.0533 \times 10^{-14}$ (`7.66 sigma`), look-elsewhere corrected $Z$-scores across `103` ecliptic $3.5^\circ$ windows (`7.03 sigma`), `360` $1^\circ$ bins (`6.85 sigma`), `43,228` isolated multi-country seeds (`6.11 sigma`), and `173,358` unassigned multi-country HQ trajectories (`5.88 sigma`), and runs a live 1,000-trial shuffled-solar-longitude bootstrap over the 166 external multi-country reference orbits.

## 3. Corrupt-Object Rejection Test

Mutating any orbital element, station code, trajectory ID, manifest byte/hash field, or null-test count in `object/new_shower_cluster.json`, `object/m1_cepheus_mc_gmn_lines.txt`, `object/null_test_400_controls.json`, or `object/gmn_yearly_manifest.json` causes `sh verify-it-yourself/run_checks.sh` to print `ERROR: ...` and `FAIL` and exit with status `1`.

pass: true
