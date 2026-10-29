# Panel Skeptic Review — Role: NOVELTY

context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target_id: asteroid-precovery-arc-extension
category: sky-archives
review_utc: 2026-10-21T13:53:00Z

## 1. Scope and Files Inspected

Acting in an isolated fresh subagent context, I inspected:
- `object/precovery_2014_OV236/precovery_bundle.json` (`52,570` bytes, `sha256: 1b2642700fbb4b0d4d4cbea510011d42aaa1b5d3eb7399dccb3087f3a38c7b96`)
- `object/precovery_2014_OV236/sbdb_orbit_cov.json` (`6,103` bytes, `sha256: b6ede1b0d29fcc75693ce8e657f0d00a61083ef5e3177ae9885e5f03382f52d9`)
- `object/precovery_2014_OV236/mpc_obs80.txt` (`2,916` bytes, `sha256: 9b77ee37684d110b0a4f0e737f4e95d55337b915cb5da8acbca13dffcc586c03`)

---

## 2. Honest Single-Fetch Verification of Primary Live Astronomical Databases (`2014 OV236`)

Each live astronomical database endpoint was queried using `curl -4 -sS -A "V3R1T4S-research-agent (honest single fetch)"`, recording exact UTC timestamp, HTTP status code, payload byte size, SHA-256 checksum, and parsed database fields:

### 2.1 JPL Small-Body Database (`SBDB`) for `2014 OV236`
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
- **Comparison Against Claim (`object/precovery_2014_OV236/precovery_bundle.json`)**:
  - The 4 claimed Pan-STARRS 1 (`F51`) $r/i/g$-band warp detections across 2 nights on `2010-08-18` and `2010-08-19` (`MJD_UTC = 55426.492544, 55427.421337, 55427.433057, 55427.492212`; `JD_UTC = 2455426.992544` to `2455427.992212`) precede `orbit.first_obs = 2014-05-24` (`JD_UTC = 2456802.012740`) by **`1,374.0205` to `1,375.0202` days (`3.76` years)**, extending the observed arc from `3,870.0` days to `5,244.9608` days (`1.3553x`) and reducing $\sigma_a$ by **`62.92%` (`LS` covariance: `5.5982e-8 AU` to `2.0758e-8 AU`)** and **`55.37%` (`SBDB` covariance: `6.5109e-8 AU` to `2.9057e-8 AU`)**, satisfying `precovery-neocp-style-short-arc`.

### 2.2 Minor Planet Center (`MPC`) `get-obs` API for `2014 OV236`
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
   - **URL 1**: `https://export.arxiv.org/api/query?search_query=all:precovery+AND+all:asteroid&sortBy=submittedDate&sortOrder=descending&max_results=20` (`2026-10-21T13:49:33Z`, `HTTP/2 200`, `45,186` bytes, `sha256: 26fba695f27f4af6d493086cfcb3f9d7f8e8ce18467c465458e133d9a821d880`)
   - **URL 2**: `https://export.arxiv.org/api/query?id_list=2510.07588` (`2026-10-21T13:52:14Z`, `HTTP/2 200`, `3,211` bytes, `sha256: a4d131e6f999ed32e3adeaa0f7fd0677a01da362ed9b722221d34912cf422646`)
   - **Findings**: Zero mentions of `2014 OV236`.

2. **OpenAlex Works API**:
   - **URL**: `https://api.openalex.org/works?search=%222014+OV236%22+OR+%22asteroid+precovery%22&per-page=20` (`2026-10-21T13:49:34Z`, `HTTP/2 200`, `283,446` bytes, `sha256: c18c017cf7bed8372f0eb907f5c44f3bebb282e0b59edf95899140d8171b0cfd`)
   - **Findings**: Zero works mentioning `"2014 OV236"`.

3. **Benchmark `TROPHY_CASE.md`**:
   - **URL**: `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` (`2026-10-21T13:49:36Z`, `HTTP/2 200`, `31,235` bytes, `sha256: b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`)
   - **Findings**: Zero entries match `2014 OV236`.

---

## 4. Verdict

The `2014 OV236` precovery bundle on `2010-08-18/19` strictly precedes the live-fetched JPL SBDB `orbit.first_obs` date (`2014-05-24`) by `1,374.02` days (`3.76` years), has zero observations within `1,374+` days in the live-fetched MPC `get-obs` record, and is completely absent from the literature and `TROPHY_CASE.md`.

pass: true
