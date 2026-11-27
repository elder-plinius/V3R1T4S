# Primary Source & Literature Audit — `asteroid-precovery-arc-extension` (`2019 QT15`)

## 1. Live JPL Small-Body Database (`SBDB`) & Minor Planet Center (`MPC`) Record (`2019 QT15`)

- **JPL SBDB URL:** `https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2019%20QT15&cov=mat&phys-par=1`
- **Fetched UTC:** `2026-10-21T13:49:08Z` (`HTTP/2 200`, `3,293` bytes, `sha256: f95d64f54fb52a3423930a433a626fb1ecf0125263d7cdecef07c00bc5ab6c73`; saved full-precision bundle copy `object/precovery_2019_QT15/sbdb_orbit_cov.json`, `6,069` bytes, `sha256: 98c97fe6eabb7b58bbabfea79ca3cfc4ab3613411513307da8ad667143dfb1ba`)
- **Live SBDB Parameters:** `orbit.first_obs = "2019-08-31"`, `orbit.last_obs = "2019-11-27"`, `orbit.data_arc = "88"` days (`< 365` days), `orbit.n_obs_used = 41` (`< 50`), `orbit.condition_code = "3"`, $\sigma_{a,\text{SBDB,before}} = 2.1185 \times 10^{-5}\text{ AU}$ ($\sigma_{a,\text{LS,before}} = 1.6783 \times 10^{-5}\text{ AU}$).
- **MPC `get-obs` URL:** `https://data.minorplanetcenter.net/api/get-obs` (JSON body `{"desigs":["2019 QT15"],"output_format":["OBS80"]}`, fetched `2026-10-21T13:49:08Z`, `HTTP/2 200`, `3,455` bytes, `sha256: 46ee004a37ed19915f9192d83198df86c918cd59caac143c1455e53a834612d5`; saved `OBS80` lines in `object/precovery_2019_QT15/mpc_obs80.txt`, `3,321` bytes, `sha256: 04f0bbaf3c8191c1d533ef8c7d50efa63f41e6d69d8c652fd41efbdbde797ff5`): `41` total observations, earliest observation `2019-08-31.57078 UTC` (`JD_UTC = 2458727.070780`). Zero observations exist prior to `2019-08-31`.
- **Public JPL Planetary Ephemeris (`DE421`):**
  - `https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de421.bsp` (`16,788,480` bytes, `sha256: a20a7139da04cbc462454634918e9a9ca69127044e2cc9d4f9c16e238d2deedc`)
  - `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp` (`16,790,528` bytes, `sha256: 08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3`)

## 2. Literature, `TROPHY_CASE.md`, and Open PR Audit (`2026-10-21T13:49:33Z–13:52:49Z`)

- **arXiv & OpenAlex:** `arXiv:2510.07588` (Oct 2025, automated ZTF NEA precovery) and all 16 arXiv / 11 OpenAlex asteroid precovery works contain zero mentions or observations of `2019 QT15`.
- **`TROPHY_CASE.md` & Open PRs:** `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` (`sha256: b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`) and all open pull requests on `elder-plinius/V3R1T4S` contain zero entries for `2019 QT15`.
