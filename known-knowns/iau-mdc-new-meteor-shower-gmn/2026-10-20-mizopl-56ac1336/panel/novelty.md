# Novelty Skeptic Report (`panel/novelty.md`)

role: novelty
context: fresh review session inspecting object/ and verify-it-yourself/
target_id: iau-mdc-new-meteor-shower-gmn
verdict: PASS

## 1. Comparison Against Live 3 November 2026 IAU Meteor Data Center Catalog (`2,197` Rows)

On `2026-11-07T15:14:00Z` (re-filing check, extending our initial `2026-10-20T18:54:36Z` snapshot), we queried all three authoritative IAU Meteor Data Center (MDC) endpoints:

| IAU MDC Source | URL | Snapshot / Header Date | Size & Row Count | SHA-256 Digest |
| :--- | :--- | :--- | :--- | :--- |
| **`streamfulldata2026.txt` (live at re-filing)** | `https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt` | Header: `Nov 03, 20:00:00 UTC, 2026` (retrieved `2026-11-07T15:14:00Z`) | `1,558,558` bytes (`2,197` shower rows, `LP = 00001..02650`; `2,004` explicit orbits + `172` radiant-derived Keplerian orbits) | `ae1a84a546be1c72ee0cf74835bc5b928a0d1d4c4e01a18a7f17bdaee299e100` |
| **`streamfulldata2026.txt` (initial filing)** | `https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt` | Retrieved `2026-10-20T18:54:36Z` | `1,555,028` bytes (`2,192` shower rows, `LP = 00001..02645`) | `08409111125e83ef2f033b27e215fb4383e0f15f6e6a3d202f7dda3a27f027fe` |
| **`roje_lista.php` (Working List HTML)** | `https://www.ta3.sk/IAUC22DB/MDC2022/Roje/roje_lista.php` | Retrieved `2026-11-07T15:13:59Z` | `370,300` bytes | `3d25556bdd5cc627acab13c4baca7d9df85a30afed0ee5e29e93e80e4724c2ef` |
| **`new_reports.php` (2023–2026 Reports)** | `https://www.ta3.sk/IAUC22DB/MDC2022/Dokumenty/new_reports.php` | Retrieved `2026-11-07T15:14:00Z` | `9,216` bytes | `f59617319b97414766b119e0abe5922dcb6a11521855d4ee643de9a031336d93` |

### Audit of the 5 New Rows Added in the 3 November 2026 IAU MDC Update (`LP = 02646..02650`)

Between `2026-10-20` (`2,192` rows) and `2026-11-03` (`2,197` rows), exactly 5 new shower rows (`LP = 02646..02650`, submitted `2026-10-28` from CBET 5592 / 5599 / 5603 / 5616) were added to `streamfulldata2026.txt`. All 5 are included in `object/new_shower_cluster.json` (`mdc_reference_neighbors`) and verified by `verify-it-yourself/check_meteor_claim.py`:

| `LP` | `IAU No` | Code | Shower Name | Sub Date | $\lambda_\odot$ ($^\circ$) | $\alpha_g$ ($^\circ$) | $\delta_g$ ($^\circ$) | $V_g$ (km/s) | $q$ (AU) | $e$ | $i$ ($^\circ$) | $D_{\text{SH,exact}}$ to `M1_Cepheus_MC` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `02646` | `01247` | `RTR` | `M2026-R1` | `2026-10-28` | `159.4` | `31.6` | `+34.2` | `66.15` | `0.941` | `0.996` | `141.63` | **`1.448801`** |
| `02647` | `01248` | `ust` | `M2026-S1` | `2026-10-28` | `164.6` | `348.7` | `+63.9` | `54.88` | `0.971` | `0.970` | `100.39` | **`0.946958`** |
| `02648` | `01248` | `ust` | `M2026-S1` | `2026-10-28` | `164.65` | `347.9` | `+64.1` | `54.30` | `0.967` | `0.963` | `99.41` | **`0.933349`** |
| `02649` | `01249` | `dsd` | `M2026-S2` | `2026-10-28` | `172.0` | `278.4` | `+59.3` | `24.16` | `1.005` | `0.785` | `38.68` | **`0.299155`** |
| `02650` | `01250` | `nsc` | `M2026-U1` | `2026-10-28` | `202.9` | `21.2` | `-26.2` | `11.67` | `0.955` | `0.585` | `12.69` | **`0.892624`** |

None of the 5 newly added rows collides with `GMN_NEW_SHOWER_M1_CEPHEUS_MC_163` ($\min D_{\text{SH}} = 0.2992 \ge 0.20$; note that `M2026-S1` is a retrograde shower at $i \approx 100^\circ, V_g \approx 54.6\text{ km/s}$, and `M2026-S2` peaks $8.7^\circ$ later in solar longitude at $\lambda_\odot = 172.0^\circ, \alpha_g = 278.4^\circ$ with $D_{\text{SH}} = 0.2992 \ge 0.20$).

### Full-Catalog Closest Neighbors Across All `2,197` Rows (`2026-11-03`)

- **Minimum mean-orbit $D_{\text{SH}}$ across all `2,197` rows (`2,004` explicit + `172` radiant-derived):**
  $$\min_{\text{MDC}} D_{\text{SH}}(\text{mean}, \text{MDC}) = 0.281872 \ge 0.20$$
  (closest: `LP = 02584`, `IAU #01206`, `FDR` / `53-Draconids` at $\lambda_\odot = 152.9^\circ, \alpha_g = 290.9^\circ, \delta_g = +57.18^\circ, V_g = 26.86\text{ km/s}, q = 0.9967\text{ AU}, e = 0.722, i = 43.39^\circ, \Omega = 152.9^\circ, \omega = 194.28^\circ$: $D_{\text{SH,exact}} = 0.281872, D_{\text{SH,planar}} = 0.315712$).
- **Minimum single-member $D_{\text{SH}}$ across all $16 \times 2,176$ pairs:**
  $$\min_{m \in \text{cluster},\,\text{MDC}} D_{\text{SH}}(m, \text{MDC}) = 0.251127 \ge 0.20$$
  (trajectory `20260905002604_C1nyH` vs `LP = 02584` `53-Draconids / FDR #01206`).
- **Minimum radiant separation within $|\Delta\lambda_\odot| \le 5.0^\circ$:**
  $$\min_{|\Delta\lambda_\odot| \le 5^\circ} \Delta\theta = 19.5245^\circ > 5.0^\circ$$
  (closest: `LP = 00731`, `IAU #00220`, `NDR` / `nu-Draconids` at $\lambda_\odot = 162.6^\circ, \alpha_g = 265.0^\circ, \delta_g = +56.3^\circ$).
- **Minimum radiant separation across active intervals $[\lambda_{\odot,b}-5^\circ, \lambda_{\odot,e}+5^\circ]$:**
  $$\min_{\text{interval}} \Delta\theta = 9.4502^\circ > 5.0^\circ$$
  (closest: `LP = 00112`, `IAU #00012`, `KCG` / `kappa-Cygnids` at $\alpha_g = 289.9^\circ, \delta_g = +53.5^\circ$, where $D_{\text{SH}} = 0.3266 \ge 0.20$).

---

## 2. Dated Literature Searches (*eMeteorNews*, *WGN*, CBET, and arXiv)

We executed systematic literature searches on **`2026-10-20`** (initial filing) and **`2026-11-07`** (re-filing verification) across all venues specified in `target.md`:

| Venue / Database | Search Dates | Exact Queries & Coordinate Cones Searched | Findings |
| :--- | :--- | :--- | :--- |
| ***eMeteorNews* (eMetN)** (`meteornews.net` & ADS bibcode `eMetN`) | `2026-10-20`, `2026-11-07` | 1. `"Cepheids" OR "Cepheus" AND ("Global Meteor Network" OR "GMN" OR "CAMS") AND ("163" OR "September")`<br>2. `"RA 304" OR "305" AND "Dec +59" OR "+60" AND "26.4"`<br>3. All *eMeteorNews* shower discovery & outburst reports (2018–Nov 2026) by Roggemans, Jenniskens, Segon, Vida, Koseki, Šegon, et al. | **0 matches.** No shower or candidate report within $10^\circ$ of $(\alpha_g = 304.77^\circ, \delta_g = +59.83^\circ)$ at $\lambda_\odot \in [158^\circ, 168^\circ]$, $V_g \in [22, 31]\text{ km/s}$, $i \in [37^\circ, 47^\circ]$. |
| ***WGN, Journal of the International Meteor Organization*** (`imo.net` & ADS bibcode `JIMO`) | `2026-10-20`, `2026-11-07` | 1. `"Cepheus" OR "Draco" OR "Cygnus" AND ("new meteor shower" OR "working list" OR "GMN")`<br>2. Coordinate cone search around $\lambda_\odot \in [158^\circ, 168^\circ], \alpha_g \in [295^\circ, 315^\circ], \delta_g \in [+54^\circ, +65^\circ]$ across WGN volumes `46–54` (`2018–2026`). | **0 matches.** Closest discussed late-August/September prograde activity is the $\kappa$-Cygnid (`#00012`) / `53-Draconid` (`#01206`) complex at $D_{\text{SH}} \ge 0.2819$. |
| **IAU Central Bureau Electronic Telegrams (CBET) & `new_reports.php`** | `2026-10-20`, `2026-11-07` | 1. Full scan of `https://www.ta3.sk/IAUC22DB/MDC2022/Dokumenty/new_reports.php` (`2023–2026` list of newly submitted showers).<br>2. Audit of October 2026 CBETs `5592, 5599, 5603, 5616` (`M2026-R1`, `M2026-S1`, `M2026-S2`, `M2026-U1`, `LP = 02646..02650`). | **0 matches.** All 2023–2026 reports in `new_reports.php` and CBET 5592–5616 have $D_{\text{SH}} \ge 0.2819$ from `GMN_NEW_SHOWER_M1_CEPHEUS_MC_163`. |
| **arXiv (`astro-ph.EP`, `astro-ph.IM`) & NASA ADS** (`arxiv.org`, `ui.adsabs.harvard.edu`) | `2026-10-20`, `2026-11-07` | 1. `abs:("Global Meteor Network" OR "meteor shower" OR "CAMS") AND abs:("Cepheus" OR "streamfulldata" OR "working list")` (2018–Nov 2026)<br>2. Author searches: `Vida, D.`, `Jenniskens, P.`, `Roggemans, P.`, `Jopek, T.`, `Neslušan, L.`, `Hajduková, M.`, `Kornoš, L.` (including Vida et al. 2021 *MNRAS* 506, 5046; Jenniskens et al. 2018–2026 CAMS surveys). | **0 matches.** No preprint or peer-reviewed paper reports a prograde stream at $(\lambda_\odot \approx 163.3^\circ, \alpha_g \approx 304.8^\circ, \delta_g \approx +59.8^\circ, V_g \approx 26.4\text{ km/s}, q \approx 0.957\text{ AU}, i \approx 41.8^\circ)$. |

## Conclusion

`GMN_NEW_SHOWER_M1_CEPHEUS_MC_163` (`M1_Cepheus_MC`, $N = 16$) is absent from the live 3 November 2026 IAU MDC catalog (`2,197` rows) and from *eMeteorNews*, *WGN*, CBET, and arXiv through 7 November 2026.

pass: true
