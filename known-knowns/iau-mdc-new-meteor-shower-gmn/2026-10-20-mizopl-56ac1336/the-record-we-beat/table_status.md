# Baseline & Literature Status (`the-record-we-beat/table_status.md`)

## 1. Target Benchmark & Single-Claim Summary

- **Target ID:** `iau-mdc-new-meteor-shower-gmn`
- **Single Claim Filed:** `GMN_NEW_SHOWER_M1_CEPHEUS_MC_163` (`M1_Cepheus_MC`, provisional designation *September $\xi$-Cepheids*)
- **Baseline Compared Against:**
  1. **Live 3 November 2026 IAU Meteor Data Center (MDC) `streamfulldata2026.txt` (`2,197` rows):**
     - URL: `https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt`
     - Header: `Last update: Nov 03, 20:00:00 UTC, 2026` (retrieved `2026-11-07T15:14:00Z`)
     - Size: `1,558,558` bytes (`2,197` shower rows `LP = 00001..02650`: `2,004` explicit orbits + `172` radiant-derived Keplerian orbits)
     - SHA-256: `ae1a84a546be1c72ee0cf74835bc5b928a0d1d4c4e01a18a7f17bdaee299e100`
     - (Initial filing snapshot on `2026-10-20T18:54:36Z` had `2,192` rows, `1,555,028` bytes, `sha256: 08409111125e83ef2f033b27e215fb4383e0f15f6e6a3d202f7dda3a27f027fe`.)
  2. **IAU MDC Working List (`roje_lista.php`) & 2023–2026 New Reports (`new_reports.php`):**
     - `https://www.ta3.sk/IAUC22DB/MDC2022/Roje/roje_lista.php` (`370,300` bytes, `sha256: 3d25556bdd5cc627acab13c4baca7d9df85a30afed0ee5e29e93e80e4724c2ef`, retrieved `2026-11-07T15:13:59Z`)
     - `https://www.ta3.sk/IAUC22DB/MDC2022/Dokumenty/new_reports.php` (`9,216` bytes, `sha256: f59617319b97414766b119e0abe5922dcb6a11521855d4ee643de9a031336d93`, retrieved `2026-11-07T15:14:00Z`)
  3. **9 Public GMN Yearly Trajectory Summary Archives (`2018–2026`):**
     - `3,599,504` total trajectories (`1,772,720` with `num_stat >= 3`; `1,263,849` unassigned `IAU No == -1` with `num_stat >= 3`; `288,532` unassigned multi-country trajectories with `num_stat >= 3` and `n_countries >= 2`), cited by URL and SHA-256 in `object/gmn_yearly_manifest.json`.

---

## 2. Quantitative Comparison vs. Target Thresholds

| Metric | Target Requirement (`target.md`) | Verified Result (`GMN_NEW_SHOWER_M1_CEPHEUS_MC_163`) |
| :--- | :--- | :--- |
| **Unique multi-station meteors ($N$)** | $\ge 15$ meteors (each meteor counted once) | **`16` unique meteors** ($\min \Delta t = 1,332.405\text{ s} = 22.21\text{ min}$; duplicate `20260907031956_h3OXu` removed) |
| **Distinct years observed** | $\ge 3$ years | **`4` consecutive years (`2023`: 2, `2024`: 3, `2025`: 4, `2026`: 7)** |
| **Per-meteor stations & countries** | $\ge 3$ independent stations in $\ge 2$ countries **per meteor** | **`16/16` (`100%`)** have `num_stat >= 3` (`3..8`) and `n_countries >= 2` (`2..3`), spanning **`15` countries** and **`62` stations** |
| **Internal orbital cohesion ($D_{\text{SH}}$)** | $D_{\text{SH}} < 0.10$ for every member | **$\max D_{\text{SH,exact}}(\text{mean}) = 0.073001 < 0.10$** ($\text{planar} = 0.071959$); **$\max D_{\text{SH,exact}}(\text{median}) = 0.079486 < 0.10$** ($\text{planar} = 0.083053$) |
| **Orbital isolation vs. 2,197 IAU MDC rows (`2026-11-03`)** | $\min D_{\text{SH}} \ge 0.20$ | **$\min D_{\text{SH}}(\text{mean}, \text{MDC}) = 0.281872 \ge 0.20$** (`53-Draconids / FDR #01206`, `LP = 02584`); **$\min D_{\text{SH}}(\text{member}, \text{MDC}) = 0.251127 \ge 0.20$** |
| **Isolation vs. 5 rows added on 3 Nov 2026 (`LP = 02646..02650`)** | $\min D_{\text{SH}} \ge 0.20$ | **$\min D_{\text{SH}} = 0.299155 \ge 0.20$** (`M2026-R1`: `1.4488`, `M2026-S1`: `0.9470 / 0.9333`, `M2026-S2`: `0.2992`, `M2026-U1`: `0.8926`) |
| **Radiant separation at matched solar longitude** | $\Delta\theta > 5.0^\circ$ within $|\Delta\lambda_\odot| \le 5.0^\circ$ | **$\min \Delta\theta = 19.5245^\circ > 5.0^\circ$** (`nu-Draconids / NDR #00220`, `LP = 00731`); **$9.4502^\circ > 5.0^\circ$** across active intervals $[\lambda_{\odot,b}-5^\circ, \lambda_{\odot,e}+5^\circ]$ |
| **Background excess ($> 5\sigma$) & windows searched** | $> 5\sigma$ above local sporadic background, with number of windows searched | • **Same window in baseline years `2018–2022`:** `0` meteors (`0` in all 20 adjacent $3.5^\circ$ sideband windows)<br>• **Single-window 400-control shuffle/permutation:** $Z = 14.26\sigma$ Gaussian / $Z_{\text{Pois}} = 7.66\sigma$ Poisson ($p = 7.0533 \times 10^{-14}$)<br>• **Look-elsewhere (`103` ecliptic $3.5^\circ$ windows):** $Z_{\text{global}} = 7.03\sigma > 5.0\sigma$ ($p_{\text{global}} = 7.2649 \times 10^{-12}$)<br>• **Look-elsewhere (`360` $1^\circ$ solar-longitude bins):** $Z_{\text{global}} = 6.85\sigma > 5.0\sigma$ ($p_{\text{global}} = 2.5392 \times 10^{-11}$)<br>• **Look-elsewhere (`43,228` MDC-isolated multi-country seeds):** $Z_{\text{global}} = 6.11\sigma > 5.0\sigma$ ($p_{\text{global}} = 3.0490 \times 10^{-9}$)<br>• **Look-elsewhere (`173,358` unassigned multi-country HQ trajectories):** $Z_{\text{global}} = 5.88\sigma > 5.0\sigma$ ($p_{\text{global}} = 1.2227 \times 10^{-8}$) |

---

## 3. Dated Literature Searches (*eMeteorNews*, *WGN*, CBET, and arXiv)

| Venue | Dates Searched | Exact Queries & Coordinate Cones | Result |
| :--- | :--- | :--- | :--- |
| ***eMeteorNews* (eMetN)** (`meteornews.net` & ADS `eMetN`, 2018–Nov 2026) | `2026-10-20`, `2026-11-07` | `"Cepheids" OR "Cepheus" AND ("Global Meteor Network" OR "GMN" OR "CAMS") AND ("163" OR "September")`; radiant cone $\alpha_g \in [295^\circ, 315^\circ], \delta_g \in [+54^\circ, +65^\circ], \lambda_\odot \in [158^\circ, 168^\circ], V_g \in [22, 31]\text{ km/s}$ | **0 matches** |
| ***WGN, Journal of the IMO*** (`imo.net` & ADS `JIMO`, vols. 46–54, 2018–2026) | `2026-10-20`, `2026-11-07` | `"Cepheus" OR "Draco" OR "Cygnus" AND ("new meteor shower" OR "working list" OR "GMN")`; coordinate cone around $(\alpha_g = 304.8^\circ, \delta_g = +59.8^\circ, \lambda_\odot = 163.3^\circ)$ | **0 matches** |
| **IAU CBET (`5592, 5599, 5603, 5616`) & `new_reports.php` (2023–Nov 2026)** | `2026-10-20`, `2026-11-07` | Full inspection of `new_reports.php` (2023–2026) and October 2026 CBETs `5592, 5599, 5603, 5616` (`M2026-R1`, `M2026-S1`, `M2026-S2`, `M2026-U1`, `LP = 02646..02650`) | **0 matches** ($\min D_{\text{SH}} = 0.2992$) |
| **arXiv (`astro-ph.EP`, `astro-ph.IM`) & NASA ADS (2018–Nov 2026)** | `2026-10-20`, `2026-11-07` | `abs:("Global Meteor Network" OR "meteor shower" OR "CAMS") AND abs:("Cepheus" OR "streamfulldata" OR "working list")`; author searches (`Vida, Jenniskens, Roggemans, Jopek, Neslušan, Hajduková, Kornoš`) | **0 matches** |
