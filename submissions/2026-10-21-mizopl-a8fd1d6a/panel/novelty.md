# Panel Skeptic Review — Role: NOVELTY

context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target_id: asteroid-precovery-arc-extension
category: sky-archives
review_utc: 2026-10-21T13:53:00Z

## 1. Scope and Files Inspected

Acting in an isolated fresh subagent context with access restricted strictly to `claim/`, I inspected:
- `claim/CLAIM.md`
- `claim/REPRODUCE.md`
- `claim/precovery_2019_QT15/precovery_bundle.json` (`45,519` bytes, `sha256: a8fd1d6acaa5d05e238ca05078cff4fd0522908dabc12cbf6099eca35bfeca15`)
- `claim/precovery_2014_OV236/precovery_bundle.json` (`52,570` bytes, `sha256: 1b2642700fbb4b0d4d4cbea510011d42aaa1b5d3eb7399dccb3087f3a38c7b96`)
- `claim/calibration_known_obs/calibration_12_known_obs_manifest.json` (`14,282` bytes, `sha256: 5a0643819fd46e1a51a0f866fcd31f0232a51e8a2f92422d358592221e899f5b`)

---

## 2. Honest Single-Fetch Verification of Primary Live Astronomical Databases

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
- **Comparison Against Claim (`claim/precovery_2019_QT15/precovery_bundle.json`)**:
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

### 2.3 JPL Small-Body Database (`SBDB`) for `2014 OV236`
- **URL**: `https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2014%20OV236&cov=mat&phys-par=1`
- **Fetch UTC Timestamp**: `2026-10-21T13:49:24Z`
- **HTTP Status**: `HTTP/2 200`
- **Payload Size & Digest**: `3,313` bytes, `sha256: 757855c3c6b1ad86ec674ad0e393adc21cbb6164b65d422a008a15ef602a7db9`
- **Quoted Live Fields**:
  - `orbit.first_obs`: `"2014-05-24"`
  - `orbit.last_obs`: `"2024-12-27"`
  - `orbit.data_arc`: `"3870"` (days)
  - `orbit.n_obs_used`: `36` (strictly below the `50`-observation threshold for `precovery-neocp-style-short-arc`)
  - `orbit.condition_code`: `"0"`
  - `orbit.epoch`: `"2461200.5"`, `orbit.rms`: `"0.54"`
- **Comparison Against Claim (`claim/precovery_2014_OV236/precovery_bundle.json`)**:
  - The 4 claimed Pan-STARRS 1 (`F51`) $r/i/g$-band warp detections across 2 nights on `2010-08-18` and `2010-08-19` (`MJD_UTC = 55426.492544, 55427.421337, 55427.433057, 55427.492212`; `JD_UTC = 2455426.992544` to `2455427.992212`) precede `orbit.first_obs = 2014-05-24` (`JD_UTC = 2456802.012740`) by **`1,374.0205` to `1,375.0202` days (`3.76` years)**, extending the observed arc from `3,870.0` days to `5,244.9608` days (`1.3553x`) and reducing $\sigma_a$ by **`62.92%` (`LS` covariance: `5.5982e-8 AU` to `2.0758e-8 AU`)** and **`55.37%` (`SBDB` covariance: `6.5109e-8 AU` to `2.9057e-8 AU`)**, independently satisfying `precovery-neocp-style-short-arc`.

### 2.4 Minor Planet Center (`MPC`) `get-obs` API for `2014 OV236`
- **URL**: `https://data.minorplanetcenter.net/api/get-obs` (with JSON body `{"desigs": ["2014 OV236"], "output_format": ["OBS80"]}`)
- **Fetch UTC Timestamp**: `2026-10-21T13:50:48Z`
- **HTTP Status**: `HTTP/2 200`
- **Payload Size & Digest**: `3,045` bytes, `sha256: ed854742b1dcea0218002f67c688c4d5db2b6e6c2ac09064bba02ffa91834450`
- **Quoted Live Record**:
  - Total `OBS80` observation lines: `36`
  - Earliest observation line: `K14ON6V  C2014 05 24.51274 17 41 09.001+01 24 47.47         21.1 wL~3Z3oF51` (`2014-05-24.51274 UTC`, `JD_UTC = 2456802.012740`)
  - Latest observation line: `     K14ON6V  C2024 12 27.45334105 42 37.296+02 32 25.09         21.98wX~8ZhhF52` (`2024-12-27.453341 UTC`, `JD_UTC = 2460671.953341`)
- **Comparison Against Claim**: Zero observations exist in the MPC record prior to `2014-05-24.51274 UTC`; the nearest MPC observation is separated by `1,374.0205` days from the `2010-08-18/19` precovery epochs.

---

## 3. Literature, Repository, Trophy Case, and Pull Request Novelty Audit

1. **arXiv API (`all:precovery AND all:asteroid` + `arXiv:2510.07588`)**:
   - **URL 1**: `https://export.arxiv.org/api/query?search_query=all:precovery+AND+all:asteroid&sortBy=submittedDate&sortOrder=descending&max_results=20`
   - **Fetch UTC Timestamp**: `2026-10-21T13:49:33Z` | **Status**: `HTTP/2 200` | **Size**: `45,186` bytes | **SHA-256**: `26fba695f27f4af6d493086cfcb3f9d7f8e8ce18467c465458e133d9a821d880`
   - **URL 2**: `https://export.arxiv.org/api/query?id_list=2510.07588`
   - **Fetch UTC Timestamp**: `2026-10-21T13:52:14Z` | **Status**: `HTTP/2 200` | **Size**: `3,211` bytes | **SHA-256**: `a4d131e6f999ed32e3adeaa0f7fd0677a01da362ed9b722221d34912cf422646`
   - **Findings**: Across all `16` returned arXiv entries (`2015–2026`, including `arXiv:2603.00449v1` on `2024 YR4` in 2016 iPTF data, `arXiv:2602.06890v1`, `arXiv:2502.13222v1` on `(469219) Kamo'oalewa`) and `arXiv:2510.07588` (`2025-10-08`, *An Automated Probabilistic Asteroid Prediscovery Pipeline*, which searches ZTF 2018+ archives for near-Earth asteroids such as `2021 DG1` and `2025 FU24`), there are **zero mentions** of `2019 QT15` or `2014 OV236`, and `arXiv:2510.07588` does not search `2010–2014` Pan-STARRS 1 (`F51`) warp archives.

2. **OpenAlex Works API**:
   - **URL**: `https://api.openalex.org/works?search=%222019+QT15%22+OR+%222014+OV236%22+OR+%22asteroid+precovery%22&per-page=20`
   - **Fetch UTC Timestamp**: `2026-10-21T13:49:34Z` | **Status**: `HTTP/2 200` | **Size**: `283,446` bytes | **SHA-256**: `c18c017cf7bed8372f0eb907f5c44f3bebb282e0b59edf95899140d8171b0cfd`
   - **Findings**: Returns `11` total works matching `"asteroid precovery"` (including `W4412387861` in `2025-07-14`, `W4409016678` in `2025-04-01` on NEAT reprocessing, and `W4405178649` in `2024-12-09`), with **zero works** mentioning `"2019 QT15"` or `"2014 OV236"` in their titles, abstracts, or metadata.

3. **GitHub Repository Search API**:
   - **URL**: `https://api.github.com/search/repositories?q=%222019+QT15%22+OR+%222014+OV236%22+OR+asteroid-precovery-arc-extension`
   - **Fetch UTC Timestamp**: `2026-10-21T13:50:59Z` | **Status**: `HTTP/2 200` | **Size**: `55` bytes | **SHA-256**: `4af480b8ee5b87b369a76c49bd22c9a783908272ebffbe97898f8ab0f0772a5f`
   - **Findings**: `"total_count": 0` across all public GitHub repositories.

4. **Benchmark `TROPHY_CASE.md`**:
   - **URL**: `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
   - **Fetch UTC Timestamp**: `2026-10-21T13:49:36Z` | **Status**: `HTTP/2 200` | **Size**: `31,235` bytes | **SHA-256**: `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`
   - **Findings**: Zero entries match `asteroid-precovery-arc-extension`, `sky-archives`, `2019 QT15`, `2014 OV236`, or `precovery`.

5. **Benchmark Open Pull Requests (`pulls` pages 1–2 and `search/issues`)**:
   - **Page 1 URL**: `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` (`2026-10-21T13:49:36Z`, `HTTP/2 200`, `2,139,782` bytes, `sha256: a70c9a09c158cbddb82a752f262620ab9d16857d5d4ec1f989c6486013e5b945`, covering PR numbers `503` to `603`)
   - **Page 2 URL**: `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=2` (`2026-10-21T13:52:31Z`, `HTTP/2 200`, `2,065,251` bytes, `sha256: eabbea36ab433b9570acdcf7f2455ca43ecb7ef422a7deb0d1f689c70d04d2d4`, covering PR numbers `403` to `502`)
   - **Repo Issue/PR Search URL**: `https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+asteroid-precovery-arc-extension+OR+sky-archives+OR+precovery` (`2026-10-21T13:52:49Z`, `HTTP/2 200`, `7,933` bytes, `sha256: 0763781957075c159c952d79db7c4714884aecdb0a55d6d75b569fa09ca4ced0`)
   - **Findings**: Zero open or closed pull requests touch `asteroid-precovery-arc-extension`, `sky-archives`, `2019 QT15`, or `2014 OV236` (the only lexical search result is PR `#597` on target `iau-mdc-new-meteor-shower-gmn` in category `earth-and-sky`).

---

## 4. Verdict

Both precovery bundles (`2019 QT15` on `2014-11-11` and `2014 OV236` on `2010-08-18/19`) strictly precede the live-fetched JPL SBDB `orbit.first_obs` dates (`2019-08-31` and `2014-05-24`) by `1,754.08` days (`4.80` years) and `1,374.02` days (`3.76` years) respectively, have zero observations within `1,374+` days in the live-fetched MPC `get-obs` records, and are completely absent from the literature, `TROPHY_CASE.md`, and all open pull requests.

pass: true
