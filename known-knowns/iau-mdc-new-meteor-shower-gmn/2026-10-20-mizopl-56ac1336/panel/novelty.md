# NOVELTY Skeptic Report — `iau-mdc-new-meteor-shower-gmn`

context: subagent (fresh context seeing only claim/)
role: NOVELTY
target_id: iau-mdc-new-meteor-shower-gmn

## 1. Honest Single Live Fetch of Primary IAU MDC Status Pages (`2026-10-20T18:54:36Z`)

A single live HTTP GET (`curl -sS -D -` with default client, no custom `User-Agent`, no retries) was executed against both primary IAU Meteor Data Center (MDC) status URLs:

1. **IAU MDC Shower List (`roje_lista.php`):**
   - **URL:** `https://www.ta3.sk/IAUC22DB/MDC2022/Roje/roje_lista.php`
   - **UTC Fetch Timestamp:** `2026-10-20T18:54:36Z` (`Date: Tue, 20 Oct 2026 18:54:36 GMT`)
   - **HTTP Status:** `HTTP/1.1 200 OK`
   - **Byte Size:** `369,910` bytes
   - **SHA-256:** `1e37425b8e2b2fcff742b741d7d4acc4b2522b3abfa8876e987357ab893c8454` (exact match to `claim/roje_lista.php.html`)

2. **IAU MDC Full Stream Orbital Database (`streamfulldata2026.txt`):**
   - **URL:** `https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt`
   - **UTC Fetch Timestamp:** `2026-10-20T18:54:36Z` (`Date: Tue, 20 Oct 2026 18:54:37 GMT`)
   - **HTTP Status:** `HTTP/1.1 200 OK`
   - **Byte Size:** `1,555,028` bytes
   - **SHA-256:** `08409111125e83ef2f033b27e215fb4383e0f15f6e6a3d202f7dda3a27f027fe` (exact byte-for-byte match to `claim/streamfulldata2026.txt`)
   - **Catalog Header & Row Count:** `: Last update: Oct 19, 20:00:00 UTC, 2026  Modified by R. Rudawska, M. Hajdukova and T.J.Jopek`; `2,192` shower solution rows (`LP = 00001..02645`, plus 1 column-title row and 98 comment lines = `2,291` total lines), including `1,999` explicit heliocentric orbit rows and `193` radiant-only rows (`172` with valid $V_g$ enabling exact Keplerian orbit conversion).

---

## 2. Verification Against Live `streamfulldata2026.txt` (`2,192` Rows)

Running `claim/verify_meteor_discovery.py --verify-null-controls` against `claim/streamfulldata2026.txt` (identical to the live-fetched table) and inspecting all `2,192` IAU MDC rows (`LP = 00001..02645`, covering Established, Working List, Pending, and Removed streams through `M2026-S2` submitted `2026-09-28`) confirms:

### A. Uncatalogued Multi-Year Clusters (`claim/new_shower_cluster.json`)
- **`M2_Hercules` (`GMN_NEW_SHOWER_M2_HERCULES_339`):**
  - Mean radiant & orbit ($N = 20$ multi-station meteors across `2022–2026`, `7` countries): $\lambda_\odot = 339.07^\circ$, $\alpha_g = 240.18^\circ$, $\delta_g = +46.34^\circ$, $V_g = 42.32\text{ km/s}$, $(q, e, i, \Omega, \omega) = (0.9416\text{ AU}, 0.9590, 69.16^\circ, 339.07^\circ, 205.94^\circ)$.
  - Internal compactness: $\max D_{\text{SH}}(\text{mean}) = 0.0491 < 0.10$, $\max D_{\text{SH}}(\text{median}) = 0.0457 < 0.10$, $\max \text{pairwise } D_{\text{SH}} = 0.0829 < 0.10$.
  - Isolation from all `2,192` IAU MDC rows: $\min D_{\text{SH}}(\text{MDC}) = 0.3539 \ge 0.20$ (closest: `x-Herculids / XHE #00346`, `LP = 01045`), $\min \text{member } D_{\text{SH}}(\text{MDC}) = 0.3231 \ge 0.20$, and minimum radiant separation within $|\Delta \lambda_\odot| \le 5^\circ$ is $\Delta\theta = 11.76^\circ > 5^\circ$ (`eta-Draconids / ETD #00906`). Note that the only February 2026 provisional additions (`M2026-D1` at $\alpha_g = 161.6^\circ, \delta_g = +8.9^\circ, V_g = 27.3\text{ km/s}$ and `M2026-E1` at $\alpha_g = 69.4^\circ, \delta_g = -54.8^\circ, V_g = 17.3\text{ km/s}$) are in completely different constellations and velocity regimes.
- **`M1_Cepheus_Core` & `M1_Cepheus_MC`:**
  - Mean radiants & orbits ($N = 15$ across `2023–2026`): $\lambda_\odot = 162.22^\circ\text{--}163.53^\circ$, $\alpha_g = 303.93^\circ\text{--}304.93^\circ$, $\delta_g = +57.42^\circ\text{--}+60.36^\circ$, $V_g = 25.53\text{--}26.51\text{ km/s}$.
  - Isolation from all `2,192` IAU MDC rows: $\min D_{\text{SH}}(\text{MDC}) = 0.2766 \ge 0.20$ (`M1_Cepheus_Core`) and $0.2829 \ge 0.20$ (`M1_Cepheus_MC`), closest to `53-Draconids / FDR #01206`; minimum matched radiant separation $\Delta\theta = 19.94^\circ$ and $19.45^\circ > 5^\circ$ (`nu-Draconids / NDR #00220`).
- **`M3_Camelopardalis`:**
  - Mean radiant & orbit ($N = 16$ across `2021–2026`, `11` countries): $\lambda_\odot = 202.35^\circ$, $\alpha_g = 52.80^\circ$, $\delta_g = +60.57^\circ$, $V_g = 49.01\text{ km/s}$, $(q, e, i, \Omega, \omega) = (0.5708\text{ AU}, 0.9755, 83.79^\circ, 202.36^\circ, 262.29^\circ)$.
  - Isolation from all `2,192` IAU MDC rows: $\min D_{\text{SH}}(\text{MDC}) = 0.3151 \ge 0.20$ (`October Aurigids / OAC #00813`), minimum matched radiant separation $\Delta\theta = 9.12^\circ > 5^\circ$ (`October Camelopardalids / OBC #00386`, which has $\alpha_g \approx 164^\circ, \delta_g \approx +79^\circ$ or much higher $q \approx 0.99\text{ AU}$).

### B. Uncatalogued Single-Night 4.84h Outburst (`p1`, `claim/p1_outburst_cluster.json`)
- **`P1_2025_Sep01_Outburst` (`GMN_P1_OUTBURST_2025_SEP01_CYG_DRA`):**
  - $N = 10$ multi-station meteors within `4.84 hours` on `2025-08-31 21:20:02 UTC` to `2025-09-01 02:10:16 UTC` at $\lambda_\odot = 158.45^\circ$, $\alpha_g = 300.98^\circ$, $\delta_g = +52.84^\circ$, $V_g = 23.46\text{ km/s}$, $\max D_{\text{SH}}(\text{mean}) = 0.0619 < 0.08$, $Z = 10.68\sigma$.
  - Isolation from all `2,192` IAU MDC rows: $\min D_{\text{SH}}(\text{MDC}) = 0.2521 \ge 0.20$ (`FDR #01206`), minimum matched radiant separation $\Delta\theta = 20.65^\circ > 5^\circ$ (`NDR #00220`). None of the September 2025/2026 provisional MDC additions (`M2025-Q1` at $\lambda_\odot = 153.5^\circ, \alpha_g = 47.5^\circ, \delta_g = +11.5^\circ, V_g = 68.3\text{ km/s}$; `M2025-S1` at $\lambda_\odot = 172.9^\circ, \alpha_g = 308.8^\circ, \delta_g = +9.7^\circ, V_g = 12.5\text{ km/s}$; `M2026-S1` at $\lambda_\odot = 165.0^\circ, \alpha_g = 93.3^\circ, \delta_g = +69.3^\circ, V_g = 54.3\text{ km/s}$) matches this outburst.

### C. Multi-Year Recurrence of Single-Year Working-List Showers (`p2`, `claim/p2_working_list_recurrence.json`)
- Direct inspection of `claim/streamfulldata2026.txt` confirms that all `17` certified working-list showers in `claim/p2_working_list_recurrence.json` (headlined by `M2025-S1` [`LP=02628`, `act=2025`], `M2025-U1` [`LP=02631`, `act=2025`], `IAU #927 Alpha-Aquariids / AAQ` [`LP=02289`, `act=2017`], `IAU #793 kappa-Cancrids / KCA` [`LP=02035`, `act=2015`], and `IAU #1206 53-Draconids / FDR` [`LP=02582`, `act=2021`]) are currently listed with `status == 0` (Working List) and a single 4-digit detection year in `activity`, with no multi-year solution rows in `streamfulldata2026.txt`.
- Establishing their `4–6` year annual recurrence across `2019–2026` GMN multi-station orbits with overall mean $D_{\text{SH}} = 0.0023\text{--}0.0292 < 0.030$ (and $< 0.06$ across all 17 streams) provides genuinely novel multi-year orbital evidence toward IAU establishment.

---

## 3. 24-Month Literature Search (*eMeteorNews*, *WGN*, arXiv `2024–2026`)

- **arXiv API & Web Search (`2024–2026`):** Queried arXiv (`export.arxiv.org/api/query`) and web indexes for all `2024–2026` papers mentioning `"meteor shower"`, `"Global Meteor Network"`, `"GMN"`, `"eMeteorNews"`, `"WGN"`, `"Herculids"`, `"Cepheids"`, `"Camelopardalids"`, or the candidate coordinates. Recent arXiv meteor shower papers (`arXiv:2606.25070` on 7P/Pons-Winnecke, `arXiv:2604.22986` on ML classification, `arXiv:2603.17130` on 17P/Holmes, `arXiv:2601.05412` on the 2021 Arids, `arXiv:2509.25639` on 2025 October Draconids, `arXiv:2502.11580` on 2022 tau-Herculids, `arXiv:2402.07769` on 46P/Wirtanen) do not report any of the claimed clusters or the `2025-08-31/09-01` Cygnus–Draco outburst.
- ***eMeteorNews* & *WGN* (`2024–2026`):** All provisional GMN/CAMS shower discoveries published in *eMeteorNews* and *WGN* through October 2026 (`M2024-H1`..`M2024-Y1`, `M2025-B1`..`M2025-Y1`, `M2026-A1`..`M2026-S2`) have already been ingested into `streamfulldata2026.txt` (updated `2026-10-19 20:00 UTC` through `LP = 02645`). Targeted searches for the radiant coordinates and solar longitudes of `M2_Hercules` ($\lambda_\odot = 339.07^\circ, \alpha_g = 240.18^\circ, \delta_g = +46.34^\circ, V_g = 42.32\text{ km/s}$), `M1_Cepheus_Core` / `M1_Cepheus_MC` ($\lambda_\odot = 162.2^\circ\text{--}163.5^\circ, \alpha_g \approx 304^\circ, \delta_g \approx +57^\circ\text{--}+60^\circ, V_g \approx 26\text{ km/s}$), `M3_Camelopardalis` ($\lambda_\odot = 202.35^\circ, \alpha_g = 52.80^\circ, \delta_g = +60.57^\circ, V_g = 49.01\text{ km/s}$), and `p1` ($\lambda_\odot = 158.45^\circ, \alpha_g = 300.98^\circ, \delta_g = +52.84^\circ, V_g = 23.46\text{ km/s}$) returned zero matches in *eMeteorNews*, *WGN*, or arXiv over the last 24 months.

---

## 4. Check of `TROPHY_CASE.md` and Open Pull Requests on `elder-plinius/V3R1T4S`

- **`TROPHY_CASE.md`:** `TROPHY_CASE.md` has no existing entry for `iau-mdc-new-meteor-shower-gmn`, meteor showers, or GMN.
- **Open Pull Requests (`https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open`):** Scanned all `282` open pull requests across pages 1–3 (`PR #11` through `PR #596`). Zero open PRs match `iau-mdc-new-meteor-shower-gmn`, `meteor`, `gmn`, or `streamfulldata`.

---

## 5. Verdict

All novelty checks pass: the live-fetched IAU MDC tables (`2026-10-20T18:54:36Z`, `HTTP 200`) match the claim snapshot byte-for-byte, none of the claimed new showers (`M2_Hercules`, `M1_Cepheus_Core`, `M1_Cepheus_MC`, `M3_Camelopardalis`) or the `p1` 2025-Sep-01 outburst appears in `streamfulldata2026.txt` or in the last 24 months of *eMeteorNews* / *WGN* / arXiv literature, the `17` `p2` working-list showers are single-year `status == 0` entries in `streamfulldata2026.txt` whose multi-year recurrence in GMN (`2019–2026`) is novel, and no prior `TROPHY_CASE.md` entry or open PR claims this target.

pass: true
