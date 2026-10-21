# The Record We Beat: Format `14x15x15` in `ZT = {-1, 0, 1}` and `Z` (`fmm-ternary-integer-ring-upgrade`)

## Summary Comparison

| Source | Format | Coefficient Ring | Previous Best Rank | Our Rank | Improvement |
|---|---|---|---|---|---|
| Perminov FMM Table (`dronperminov/FastMatrixMultiplication`) | `14x15x15` | `ZT = {-1, 0, 1}` | `1,905` | **`1,894`** | **`-11` multiplications** |
| Perminov FMM Table (`dronperminov/FastMatrixMultiplication`) | `14x15x15` | `Z` (integers) | `1,895` | **`1,894`** (`ZT`) | **`-1` multiplication** |
| Perminov FMM Table / `fmm_sota.json` / Lille FMM Table | `14x15x15` | `Q` (rationals) | `1,848` | `1,894` (`ZT`) | Within target scope (`1894 >= 1848`) |

## Primary Table Fetches (UTC Time, URL, HTTP Status, SHA-256)

1. **Perminov FastMatrixMultiplication `README.md`**
   - **URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md`
   - **UTC fetch time:** `2026-10-18T17:19:53Z`
   - **HTTP status:** `200`
   - **SHA-256:** `0dc78efcb144382ef7b703d37563722f5d328b83a42eddc17c0018e9bd628ca8`
   - **Exact row for `14x15x15` (line 2011):**
     ```text
     | `14x15x15` |  1905 (32)  |  1895 (33)   |  1848 (99)   | **2.811404586** |
     ```

2. **Perminov FastMatrixMultiplication `schemes/status.json`**
   - **URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/status.json`
   - **UTC fetch time:** `2026-10-18T17:19:54Z`
   - **HTTP status:** `200`
   - **SHA-256:** `809a1e34183516c33c84cccd6484b49ca5682a43b5e36bd9739c2b6eb4ebaf31`
   - **Exact entry for `14x15x15`:** `ranks: {"Q": 1848, "Z": 1895, "ZT": 1905}`.

3. **Sedoglavic `fmm_sota.json` & Lille FMM Catalogue (`14x15x15.html`)**
   - **URL:** `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`
   - **UTC fetch time:** `2026-10-18T17:19:55Z`
   - **HTTP status:** `200`
   - **SHA-256:** `256d5753d1ff2640c11b3b1e5a1faaf21dc22c98055e1429a319f89e4e2a3c24`
   - **Exact entry:** `{"format": [14, 15, 15], "rank": 1848, "exponent": 2.811405}` (rational `Q` scheme).
