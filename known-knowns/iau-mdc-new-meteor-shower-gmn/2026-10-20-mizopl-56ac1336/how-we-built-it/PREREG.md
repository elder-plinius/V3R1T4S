# Preregistered Verification Plan — `iau-mdc-new-meteor-shower-gmn`

target_id: iau-mdc-new-meteor-shower-gmn
frozen_utc: 2026-10-20T01:57:00Z
null_test: required
ratchet_budget: 35
predictions: P0066 (target), P0067 (lens1_orbital_clss_discovery), P0068 (lens2_mdc_recurrence_and_null_audit)

## 1. Success Criterion & Enumerated Partial Wins (Verbatim from `bank/targets.json`)

- **Full `success_criterion`:**
  > A saved list of >= 15 GMN trajectory IDs (from traj_summary_yearly_*.txt) forming a cluster whose mean orbit has D_SH < 0.10 to each member's median-orbit and whose mean orbit has D_SH >= 0.20 (and radiant separation > 5 deg at matched solar longitude +/- 5 deg) from EVERY entry of streamfulldata2026.txt re-fetched live immediately before claiming; cluster significance must exceed 5 sigma against a sporadic background estimated from the same solar-longitude window in other years (or shuffled-solar-longitude bootstrap); meteors observed by >= 3 independent stations in >= 2 countries; and no eMeteorNews / WGN / arXiv report (last 24 months) of a shower with that radiant, solar longitude and velocity.

- **Enumerated Partial Wins:**
  - **`p1`:** A confirmed new one-year outburst (>= 10 meteors within 6 h, D_SH < 0.08, >= 5 sigma over sporadic background) not in the MDC list nor in eMeteorNews, even if not recurring.
  - **`p2`:** An annual recurrence of a working-list shower in >= 3 GMN years where the MDC entry rests on a single-year detection, with mean orbit consistent (D_SH < 0.1); non-trivial because it moves evidence toward establishment.
  - **`p3`:** A parent-body association: a candidate cluster whose mean orbit has D_SH < 0.15 to a JPL SBDB comet/NEO orbit with a successful meteoroid-stream integration (e.g. via REBOUND) placing ejecta at the observed node.

## 2. Frozen Statistics, Thresholds, and Deterministic Checker

All candidate claims are judged by the deterministic verifier `code/check_meteor_cluster.py` (and the standalone claim verifier `claim/verify_meteor_discovery.py`) enforcing:

1. **Cluster Size & Trajectory Provenance:**
   - Main win: `N_members >= 15` distinct GMN trajectory IDs extracted verbatim from public `traj_summary_yearly_*.txt` files, all unassigned in GMN (`IAU No == -1`).
   - Partial win `p1`: `N_members >= 10` distinct GMN trajectory IDs within a single 6-hour interval ($\max(\text{JD}) - \min(\text{JD}) \le 0.2500\text{ days}$).
   - Partial win `p2`: `>= 3` distinct GMN years each having well-converged multi-station trajectories matching a working-list (`status == 0`) shower in `streamfulldata2026.txt` whose MDC record rests on a single-year detection (only 1 year in `activity` and no multi-year solution in `streamfulldata2026.txt`), with yearly and overall mean orbits having $D_{\text{SH}} < 0.10$ to the MDC entry.
2. **Station & Country Diversity Gate:**
   - Every member trajectory has `Num stat >= 3` independent stations (`min_num_stat >= 3`), and participating station codes span `>= 2` distinct 2-letter country prefixes (`len(countries) >= 2`).
3. **Internal Orbital Compactness Gate ($D_{\text{SH}}$):**
   - For the cluster's mean orbit $\bar{O} = (\bar{q}, \bar{e}, \bar{i}, \bar{\Omega}, \bar{\omega})$, every member $j$ satisfies $D_{\text{SH}}(\bar{O}, O_j) < 0.10$ for the main criterion (and $< 0.08$ for `p1`), verified under both the exact Southworth & Hawkins (1963) spherical $\Pi_{AB}$ formula and the planar $\Delta\varpi$ formula.
4. **Complete IAU MDC Exclusion Gate (`streamfulldata2026.txt` + Recent Literature):**
   - Across all `2,192` rows of `streamfulldata2026.txt` (re-fetched live before claiming), the cluster mean orbit (and every individual member orbit) satisfies:
     - $D_{\text{SH}}(\bar{O}, O_{\text{MDC}}) \ge 0.20$ for every MDC entry with orbital elements (and for Keplerian elements derived from `(LoS, Ra, De, Vg)` on the 193 radiant-only rows),
     - Radiant angular separation $\Delta\theta > 5.0^\circ$ from every MDC entry whose solar longitude `LoS` is within $\pm 5.0^\circ$ of $\bar{\lambda}_\odot$ (or whose `[LoSb - 5^\circ, LoSe + 5^\circ]` interval covers $\bar{\lambda}_\odot$),
     - Also separated by $D_{\text{SH}} \ge 0.20$ and $\Delta\theta > 5.0^\circ$ from any 2024–2026 *eMeteorNews* / *WGN* / arXiv provisional shower not yet in `streamfulldata2026.txt` (such as `M2025-V1`).
5. **Null Test & $\ge 5\sigma$ Significance Protocol (`null_test: required`):**
   - In the solar-longitude window surrounding the candidate cluster, we run `controls = 400` independent Monte Carlo background controls:
     - 200 controls that circularly/randomly shuffle solar longitudes $\lambda_\odot$ (and adjust $\Omega$ consistently with $\lambda_\odot$ while preserving $(q, e, i, \omega - \Omega_{\text{rel}})$) across the sporadic multi-station background pool, and
     - 200 controls that independently permute the orbital element tuples $(q, e, i, \omega)$ against $(\lambda_\odot, \Omega)$ in the local solar-longitude band / cross-year sporadic background.
   - For each of the 400 controls, we compute the maximum cluster count within a $D_{\text{SH}} < 0.10$ ball around the target orbit (and the maximum compact cluster density in the window).
   - Required to pass: `real_beats_all_controls: yes` (`real > best_control` across all 400 controls) AND significance $Z = (N_{\text{obs}} - \mu_{\text{bg}}) / \sigma_{\text{bg}} > 5.0\sigma$ (plus Poisson tail $p$-value corresponding to $> 5\sigma$).
