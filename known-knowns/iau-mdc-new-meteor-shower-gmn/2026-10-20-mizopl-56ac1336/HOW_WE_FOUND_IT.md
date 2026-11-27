# How We Found It (`HOW_WE_FOUND_IT.md`)

*(Contributor text, unverified.)*

## 1. Upstream Data Ingestion (`2018–2026` GMN + `2026-11-03` Live IAU MDC)

1. **Global Meteor Network (GMN) Yearly Trajectory Tables (`2018–2026`):**
   - Streamed all 9 yearly public trajectory summary archives (`traj_summary_yearly_2018.txt` through `traj_summary_yearly_2026.txt`, cited by URL and SHA-256 in `object/gmn_yearly_manifest.json`), containing **`3,599,504` total trajectories**:
     - `1,772,720` trajectories with `num_stat >= 3`,
     - `1,263,849` unassigned (`IAU No == -1`) trajectories with `num_stat >= 3`,
     - `288,532` unassigned trajectories satisfying both `num_stat >= 3` and `n_countries >= 2` per meteor,
     - `173,358` high-quality unassigned multi-country trajectories passing quality filters (`Q_c >= 15.0 deg`, `sigma_Vg <= 2.0 km/s`, `0 < e < 1.05`, `q > 0.02 AU`).
2. **IAU Meteor Data Center (MDC) Catalog (`streamfulldata2026.txt`):**
   - Retrieved both the initial `2026-10-20` release (`2,192` rows, `sha256: 08409111125e83ef2f033b27e215fb4383e0f15f6e6a3d202f7dda3a27f027fe`) and the live `2026-11-03` release (`2,197` rows, `sha256: ae1a84a546be1c72ee0cf74835bc5b928a0d1d4c4e01a18a7f17bdaee299e100`), augmenting the `172` radiant-only rows with approximate Keplerian orbits `(q, e, i, Omega, omega)` so that all `2,176` rows with valid orbital or radiant parameters (`2,004` explicit + `172` radiant-derived) participate in the Southworth–Hawkins $D_{\text{SH}}$ isolation screen.
   - Out of the `173,358` high-quality unassigned multi-country trajectories, **`43,228` trajectories** survive strict per-meteor MDC isolation ($D_{\text{SH}} \ge 0.22$ and radiant separation $\Delta\theta > 10.0^\circ$).

## 2. Per-Meteor Multi-Country Filtering, Deduplication & Seam Pruning

1. **Per-Meteor Station & Country Clause:**
   - Every candidate member must individually satisfy `IAU No == -1`, `num_stat >= 3` (`len(stations) == num_stat >= 3`), and `n_countries >= 2` (`len(countries) == n_countries >= 2`, where each station code matches `^[A-Z]{2}[0-9A-Z]{4}$`).
   - Applying this strict per-meteor filter to the September Cepheus stream (`M1_Cepheus`) removes all 8 single-country trajectories of the earlier `M1_Cepheus_Core` slice (including `20250904204409_BKOSN`) while retaining the 2 genuine multi-country trajectories from that slice (`20260904215007_GPg1D` [4 stations in `BA, HR`] and `20260905002604_C1nyH` [4 stations in `BG, RO`]).
2. **Pairwise Time Deduplication (Counting Each Meteor Strictly Once):**
   - Independent camera subgroups occasionally solve the same physical meteor within `< 2 s` (`20260907031956_h3OXu` solved `0.105 s` after `20260907031956_faRoT`).
   - Enforcing $\Delta t \ge 60\text{ s}$ between consecutive members removes `20260907031956_h3OXu` and yields **`N = 16` unique multi-country trajectories** with minimum pairwise time separation **`1,332.405 s` (`22.21 minutes`)**.
3. **Orbital Cohesion & MDC Isolation Verification:**
   - Across all 16 deduplicated multi-country members of `GMN_NEW_SHOWER_M1_CEPHEUS_MC_163`:
     - $\max D_{\text{SH,exact}}(\text{mean}, \text{member}) = 0.073001 < 0.10$ ($\text{planar} = 0.071959 < 0.10$),
     - $\max D_{\text{SH,exact}}(\text{median}, \text{member}) = 0.079486 < 0.10$ ($\text{planar} = 0.083053 < 0.10$),
     - $\min D_{\text{SH}}(\text{mean}, \text{MDC}_{2197}) = 0.281872 \ge 0.20$ (`LP = 02584`, `53-Draconids / FDR #01206`),
     - $\min D_{\text{SH}}(\text{member}, \text{MDC}_{2197}) = 0.251127 \ge 0.20$ (`20260905002604_C1nyH` vs `FDR #01206`),
     - $\min \Delta\theta = 19.5245^\circ > 5.0^\circ$ within $|\Delta\lambda_\odot| \le 5.0^\circ$ (`LP = 00731`, `nu-Draconids / NDR #00220`).

## 3. Background Significance & Look-Elsewhere Correction

- **Cross-year baseline (`2018–2022`) & 20 sideband windows:** `0` trajectories in the same $3.5^\circ$ solar-longitude and $D_{\text{SH}} < 0.075$ window in all 5 prior years (`2018–2022`) and `0` in all 20 shifted sideband windows.
- **400-control shuffle/permutation test:** `real = 16` vs `best_control = 7`, $\mu_{\text{ctrl}} = 1.0925$, $\sigma_{\text{eff}} = 1.0452$, single-window Gaussian $Z = 14.26\sigma$, single-window Poisson tail $p = 7.0533 \times 10^{-14}$ ($Z_{\text{Pois}} = 7.66\sigma$).
- **Look-elsewhere corrected global significance:** $7.03\sigma$ across `103` ecliptic $3.5^\circ$ windows, $6.85\sigma$ across `360` $1^\circ$ bins, $6.11\sigma$ across `43,228` MDC-isolated multi-country seeds, and $5.88\sigma$ across all `173,358` unassigned multi-country HQ trajectories.
