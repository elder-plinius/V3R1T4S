# Primary Source & Literature Audit — `asteroid-precovery-arc-extension` (`2014 OV236`)

## 1. Live JPL Small-Body Database (`SBDB`) & Minor Planet Center (`MPC`) Record (`2014 OV236`)

- **JPL SBDB URL:** `https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2014%20OV236&cov=mat&phys-par=1`
- **Fetched UTC:** `2026-10-21T13:49:24Z` (`HTTP/2 200`, `3,313` bytes, `sha256: 757855c3c6b1ad86ec674ad0e393adc21cbb6164b65d422a008a15ef602a7db9`; saved full-precision bundle copy `object/precovery_2014_OV236/sbdb_orbit_cov.json`, `6,103` bytes, `sha256: b6ede1b0d29fcc75693ce8e657f0d00a61083ef5e3177ae9885e5f03382f52d9`)
- **Live SBDB Parameters:** `orbit.first_obs = "2014-05-24"`, `orbit.last_obs = "2024-12-27"`, `orbit.data_arc = "3870"` days, `orbit.n_obs_used = 36` (`< 50`), `orbit.condition_code = "0"`, $\sigma_{a,\text{LS,before}} = 5.5982 \times 10^{-8}\text{ AU}$ ($\sigma_{a,\text{SBDB,before}} = 6.5109 \times 10^{-8}\text{ AU}$).
- **MPC `get-obs` URL:** `https://data.minorplanetcenter.net/api/get-obs` (JSON body `{"desigs":["2014 OV236"],"output_format":["OBS80"]}`, fetched `2026-10-21T13:50:48Z`, `HTTP/2 200`, `3,045` bytes, `sha256: ed854742b1dcea0218002f67c688c4d5db2b6e6c2ac09064bba02ffa91834450`; saved `OBS80` lines in `object/precovery_2014_OV236/mpc_obs80.txt`, `2,916` bytes, `sha256: 9b77ee37684d110b0a4f0e737f4e95d55337b915cb5da8acbca13dffcc586c03`): `36` total observations, earliest observation `2014-05-24.51274 UTC` (`JD_UTC = 2456802.012740`). Zero observations exist prior to `2014-05-24`.
- **Public JPL Planetary Ephemeris (`DE421`):**
  - `https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de421.bsp` (`16,788,480` bytes, `sha256: a20a7139da04cbc462454634918e9a9ca69127044e2cc9d4f9c16e238d2deedc`)
  - `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp` (`16,790,528` bytes, `sha256: 08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3`)

## 2. Literature, `TROPHY_CASE.md`, and Open PR Audit (`2026-10-21T13:49:33Z–13:52:49Z`)

- **arXiv & OpenAlex:** `arXiv:2510.07588` (Oct 2025, automated ZTF NEA precovery) and all 16 arXiv / 11 OpenAlex asteroid precovery works contain zero mentions or observations of `2014 OV236`.
- **`TROPHY_CASE.md` & Open PRs:** `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` (`sha256: b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`) and all open pull requests on `elder-plinius/V3R1T4S` contain zero entries for `2014 OV236`.
