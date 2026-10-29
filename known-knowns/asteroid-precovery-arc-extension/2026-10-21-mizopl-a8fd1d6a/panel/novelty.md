# Panel Skeptic Review — Role: NOVELTY

context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target_id: asteroid-precovery-arc-extension
category: sky-archives
review_utc: 2026-10-21T13:53:00Z

## 1. Scope and Files Inspected

Acting in an isolated fresh subagent context, I inspected:
- `object/precovery_2019_QT15/precovery_bundle.json` (`45,519` bytes, `sha256: a8fd1d6acaa5d05e238ca05078cff4fd0522908dabc12cbf6099eca35bfeca15`)
- `object/precovery_2019_QT15/sbdb_orbit_cov.json` (`6,069` bytes, `sha256: 98c97fe6eabb7b58bbabfea79ca3cfc4ab3613411513307da8ad667143dfb1ba`)
- `object/precovery_2019_QT15/mpc_obs80.txt` (`3,321` bytes, `sha256: 04f0bbaf3c8191c1d533ef8c7d50efa63f41e6d69d8c652fd41efbdbde797ff5`)

---

## 2. Honest Single-Fetch Verification of Primary Live Astronomical Databases (`2019 QT15`)

Each live astronomical database endpoint was queried using `curl -4 -sS -A "V3R1T4S-research-agent (honest single fetch)"`, recording exact UTC timestamp, HTTP status code, payload byte size, SHA-256 checksum, and parsed database fields:

### 2.1 JPL Small-Body Database (`SBDB`) for `2019 QT15`
- **URL**: `https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2019%20QT15&cov=mat&phys-par=1`
- **Fetch UTC Timestamp**: `2026-10-21T13:49:08Z`
- **HTTP Status**: `HTTP/2 200`
- **Payload Size & Digest**: `3,293` bytes, `sha256: f95d64f54fb52a3423930a433a626fb1ecf0125263d7cdecef07c00bc5ab6c73`
- **Quoted Live Fields**:
  - `orbit.first_obs`: `"2019-08-31"`
  - `orbit.last_obs`: `"2019-11-27"`
  - `orbit.data_arc`: `"88"` (days; strictly below the `365`-day threshold for `precovery-arc-doubling`)
  - `orbit.n_obs_used`: `41` (strictly below the `50`-observation threshold for `precovery-neocp-style-short-arc`)
  - `orbit.condition_code`: `"3"`
  - `orbit.epoch`: `"2461200.5"`, `orbit.rms`: `"0.53"`
- **Comparison Against Claim (`object/precovery_2019_QT15/precovery_bundle.json`)**:
  - The 3 claimed Pan-STARRS 1 (`F51`) $i$-band warp detections on `2014-11-11` (`MJD_UTC = 56972.466511, 56972.480097, 56972.493696`; `JD_UTC = 2456972.966511` to `2456972.993696`) precede `orbit.first_obs = 2019-08-31` (`JD_UTC = 2458727.070780`) by **`1,754.0771` to `1,754.1043` days (`4.80` years)**, far exceeding the `60`-day one-apparition threshold.
  - Adding these 3 detections extends the observed arc from `88.0` days to **`1,841.8205` days (`20.9298x` `data_arc`)**, exceeding the `2.0x` arc-doubling threshold (`precovery-arc-doubling`) by a factor of `10.46x`, and reduces the semi-major-axis uncertainty $\sigma_a$ by **`87.38%` (`SBDB` covariance: `2.1185e-5 AU` to `2.6743e-6 AU`)** and **`83.25%` (`LS` covariance: `1.6783e-5 AU` to `2.8113e-6 AU`)**, well above the `50%` reduction threshold (`precovery-neocp-style-short-arc`).

### 2.2 Minor Planet Center (`MPC`) `get-obs` API for `2019 QT15`
- **URL**: `https://data.minorplanetcenter.net/api/get-obs` (with JSON body `{"desigs": ["2019 QT15"], "output_format": ["OBS80"]}`)
- **Fetch UTC Timestamp**: `2026-10-21T13:49:08Z`
- **HTTP Status**: `HTTP/2 200`
- **Payload Size & Digest**: `3,455` bytes, `sha256: 46ee004a37ed19915f9192d83198df86c918cd59caac143c1455e53a834612d5`
- **Quoted Live Record**:
  - Total `OBS80` observation lines: `41`
  - Earliest observation line: `K19Q15T* C2019 08 31.57078 00 26 49.326+08 15 57.25         21.4 wU~3acQF51` (`2019-08-31.57078 UTC`, `JD_UTC = 2458727.070780`)
  - Latest observation line: `     K19Q15T  C2019 11 27.28702 00 02 06.803+01 21 28.54         22.0 wU~3acQF51` (`2019-11-27.28702 UTC`, `JD_UTC = 2458814.787020`)
- **Comparison Against Claim**: Zero observations exist in the MPC record prior to `2019-08-31.57078 UTC`; the nearest MPC observation is separated by `1,754.0771` days from the `2014-11-11` precovery epoch (strictly satisfying the `1`-day separation rule).

---

## 3. Literature, Repository, Trophy Case, and Pull Request Novelty Audit

1. **arXiv API (`all:precovery AND all:asteroid` + `arXiv:2510.07588`)**:
   - **URL 1**: `https://export.arxiv.org/api/query?search_query=all:precovery+AND+all:asteroid&sortBy=submittedDate&sortOrder=descending&max_results=20`
   - **Fetch UTC Timestamp**: `2026-10-21T13:49:33Z` | **Status**: `HTTP/2 200` | **Size**: `45,186` bytes | **SHA-256**: `26fba695f27f4af6d493086cfcb3f9d7f8e8ce18467c465458e133d9a821d880`
   - **URL 2**: `https://export.arxiv.org/api/query?id_list=2510.07588`
   - **Fetch UTC Timestamp**: `2026-10-21T13:52:14Z` | **Status**: `HTTP/2 200` | **Size**: `3,211` bytes | **SHA-256**: `a4d131e6f999ed32e3adeaa0f7fd0677a01da362ed9b722221d34912cf422646`
   - **Findings**: Across all `16` returned arXiv entries (`2015–2026`) and `arXiv:2510.07588` (`2025-10-08`, *An Automated Probabilistic Asteroid Prediscovery Pipeline*, which searches ZTF 2018+ archives for near-Earth asteroids), there are **zero mentions** of `2019 QT15`, and `arXiv:2510.07588` does not search `2010–2014` Pan-STARRS 1 (`F51`) warp archives.

2. **OpenAlex Works API**:
   - **URL**: `https://api.openalex.org/works?search=%222019+QT15%22+OR+%22asteroid+precovery%22&per-page=20`
   - **Fetch UTC Timestamp**: `2026-10-21T13:49:34Z` | **Status**: `HTTP/2 200` | **Size**: `283,446` bytes | **SHA-256**: `c18c017cf7bed8372f0eb907f5c44f3bebb282e0b59edf95899140d8171b0cfd`
   - **Findings**: Returns `11` total works matching `"asteroid precovery"`, with **zero works** mentioning `"2019 QT15"` in their titles, abstracts, or metadata.

3. **GitHub Repository Search API**:
   - **URL**: `https://api.github.com/search/repositories?q=%222019+QT15%22+OR+asteroid-precovery-arc-extension`
   - **Fetch UTC Timestamp**: `2026-10-21T13:50:59Z` | **Status**: `HTTP/2 200` | **Size**: `55` bytes | **SHA-256**: `4af480b8ee5b87b369a76c49bd22c9a783908272ebffbe97898f8ab0f0772a5f`
   - **Findings**: `"total_count": 0` across all public GitHub repositories.

4. **Benchmark `TROPHY_CASE.md`**:
   - **URL**: `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
   - **Fetch UTC Timestamp**: `2026-10-21T13:49:36Z` | **Status**: `HTTP/2 200` | **Size**: `31,235` bytes | **SHA-256**: `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`
   - **Findings**: Zero entries match `asteroid-precovery-arc-extension`, `sky-archives`, `2019 QT15`, or `precovery`.

---

## 4. Verdict

The `2019 QT15` precovery bundle on `2014-11-11` strictly precedes the live-fetched JPL SBDB `orbit.first_obs` date (`2019-08-31`) by `1,754.08` days (`4.80` years), has zero observations within `1,754+` days in the live-fetched MPC `get-obs` record, and is completely absent from the literature and `TROPHY_CASE.md`.

pass: true
