# The Record We Beat: Format `14x15x15` in `ZT = {-1, 0, 1}` and `Z` (`fmm-ternary-integer-ring-upgrade`)

## Summary Comparison

| Source | Format | Coefficient Ring | Rank Listed at Filing (`2026-10-18`) | Our Rank | Improvement |
|---|---|---|---|---|---|
| Perminov FMM Table (`dronperminov/FastMatrixMultiplication`, `README.md` / `docs/ranks.md`) | `14x15x15` | `ZT = {-1, 0, 1}` | `1,905` (`2026-10-18: ZT 1,905, Z 1,895`) | **`1,894`** | **`-11` multiplications** |
| Perminov FMM Table (`dronperminov/FastMatrixMultiplication`, `README.md` / `docs/ranks.md`) | `14x15x15` | `Z` (integers) | `1,895` (`2026-10-18: ZT 1,905, Z 1,895`) | **`1,894`** (`ZT`) | **`-1` multiplication** |
| Perminov FMM Table / `fmm_sota.json` / Lille FMM Table | `14x15x15` | `Q` (rationals) | `1,848` (`1,842` over `Q` merged in `V3R1T4S`) | `1,894` (`ZT`) | Within target scope (`1894 >= 1848 > 1842`) |

- **Dated Upstream Note:** Also published upstream by the contributor (`@mizopl`) on 2026-10-19 (`schemes/known/mizopl/14x15x15_m1894_ZT.json`); `docs/ranks.md` now lists `ZT 1,894 / Z 1,894`.
- **Overall Best (`Q`) Rank Note:** `1,848` is the rational rank listed in Perminov / `fmm_sota.json`, but `1,848` is not the overall best: a rational rank-`1,842` scheme for `14x15x15` is already merged here in `V3R1T4S` (`TROPHY_CASE.md`).

## Primary Table Fetches (UTC Time, URL, HTTP Status, SHA-256)

1. **Perminov FastMatrixMultiplication `README.md` (at filing on 2026-10-18) & `docs/ranks.md` (current table location)**
   - **URL (at filing):** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md`
   - **UTC fetch time:** `2026-10-18T17:19:53Z`
   - **HTTP status:** `200`
   - **SHA-256:** `0dc78efcb144382ef7b703d37563722f5d328b83a42eddc17c0018e9bd628ca8`
   - **Exact row for `14x15x15` as of filing (`2026-10-18: ZT 1,905, Z 1,895`, line 2011):**
     ```text
     | `14x15x15` |  1905 (32)  |  1895 (33)   |  1848 (99)   | **2.811404586** |
     ```
   - **Current `docs/ranks.md` URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md` (`sha256: 77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a`, fetched `2026-10-25T18:29:40Z`, HTTP `200`). Also published upstream by the contributor on 2026-10-19 (`schemes/known/mizopl/14x15x15_m1894_ZT.json`); `docs/ranks.md` now lists `ZT 1,894 / Z 1,894`.

2. **Perminov FastMatrixMultiplication `schemes/status.json` (at filing on 2026-10-18)**
   - **URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/status.json`
   - **UTC fetch time:** `2026-10-18T17:19:54Z`
   - **HTTP status:** `200`
   - **SHA-256:** `809a1e34183516c33c84cccd6484b49ca5682a43b5e36bd9739c2b6eb4ebaf31`
   - **Exact entry for `14x15x15` as of filing (`2026-10-18: ZT 1,905, Z 1,895`):** `ranks: {"Q": 1848, "Z": 1895, "ZT": 1905}`.

3. **Sedoglavic `fmm_sota.json`, Lille FMM Catalogue (`14x15x15.html`), & `V3R1T4S` `TROPHY_CASE.md`**
   - **URL:** `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`
   - **UTC fetch time:** `2026-10-18T17:19:55Z`
   - **HTTP status:** `200`
   - **SHA-256:** `256d5753d1ff2640c11b3b1e5a1faaf21dc22c98055e1429a319f89e4e2a3c24`
   - **Exact entry:** `{"format": [14, 15, 15], "rank": 1848, "exponent": 2.811405}` (rational `Q` scheme; note that `1,848` is not the overall best because a rational rank-`1,842` scheme is already merged in `V3R1T4S` `TROPHY_CASE.md`).
