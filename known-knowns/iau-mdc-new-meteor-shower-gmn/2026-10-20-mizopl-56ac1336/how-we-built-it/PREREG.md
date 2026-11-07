# Preregistration Protocol (`how-we-built-it/PREREG.md`)

- **Target ID:** `iau-mdc-new-meteor-shower-gmn`
- **Single Claim Filed:** `GMN_NEW_SHOWER_M1_CEPHEUS_MC_163` (`M1_Cepheus_MC`, $N = 16$)

## 1. Data Sources Fixed Before Search

1. **Global Meteor Network (GMN) Yearly Trajectory Summary Archives (`2018–2026`):**
   - `traj_summary_yearly_2018.txt` through `traj_summary_yearly_2026.txt` (`3,599,504` total trajectories; `288,532` unassigned multi-country trajectories with `IAU No == -1`, `num_stat >= 3`, and `n_countries >= 2`; cited by URL and SHA-256 in `object/gmn_yearly_manifest.json`).
2. **IAU Meteor Data Center (MDC) Catalog (`streamfulldata2026.txt`):**
   - `https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt` (`2,197` rows on `2026-11-03`, `sha256: ae1a84a546be1c72ee0cf74835bc5b928a0d1d4c4e01a18a7f17bdaee299e100`; `2,192` rows on `2026-10-20`, `sha256: 08409111125e83ef2f033b27e215fb4383e0f15f6e6a3d202f7dda3a27f027fe`), plus `roje_lista.php` and `new_reports.php`.

## 2. Selection, Deduplication & Isolation Gates

1. **Per-Meteor Quality & Multi-Country Gate:**
   - `IAU No == -1` (unassigned in GMN),
   - `num_stat >= 3` independent stations (`len(stations) == num_stat >= 3`, valid station codes `^[A-Z]{2}[0-9A-Z]{4}$`),
   - `n_countries >= 2` distinct countries (`len(countries) == n_countries >= 2`) **for every member trajectory counted**,
   - $Q_c \ge 15.0^\circ$, $\sigma_{V_g} \le 2.0\text{ km/s}$, $0 < e < 1.05$, $q > 0.02\text{ AU}$.
2. **Pairwise Time Deduplication Gate:**
   - Count each physical meteor strictly once: reject any trajectory solved within $\Delta t < 60\text{ s}$ of an already-accepted trajectory (removing `< 2 s` split-camera duplicate solutions such as `20260907031956_h3OXu`).
3. **Cluster Size & Multi-Year Gate:**
   - $N \ge 15$ deduplicated multi-country trajectories observed across $\ge 3$ distinct calendar years.
4. **Internal Orbital Cohesion Gate:**
   - Exact spherical and planar Southworth–Hawkins $D_{\text{SH}}(\text{mean}, m) < 0.10$ and $D_{\text{SH}}(\text{median}, m) < 0.10$ for every member $m$.
5. **IAU MDC Isolation Gate:**
   - $D_{\text{SH}} \ge 0.20$ against every row of `streamfulldata2026.txt` (`2,197` rows on `2026-11-03`) and radiant separation $\Delta\theta > 5.0^\circ$ at matched solar longitude ($|\Delta\lambda_\odot| \le 5.0^\circ$ and active intervals $[\lambda_{\odot,b}-5^\circ, \lambda_{\odot,e}+5^\circ]$).
6. **Background Excess ($> 5\sigma$) & Look-Elsewhere Gate:**
   - Evaluate local sporadic background both in the same solar-longitude window across prior years (`2018–2022`) / 20 adjacent sideband windows and via 400 Monte Carlo controls (`200` solar-longitude shuffle controls + `200` orbital-tuple permutation controls), and require $> 5.0\sigma$ excess both single-window and after look-elsewhere correction across `103` ecliptic $3.5^\circ$ windows, `360` $1^\circ$ bins, `43,228` MDC-isolated multi-country seeds, and `173,358` unassigned multi-country HQ trajectories.
