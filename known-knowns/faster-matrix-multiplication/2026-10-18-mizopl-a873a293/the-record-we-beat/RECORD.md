# The Record We Beat: Format `9x12x14` in `ZT = {-1, 0, 1}` (`fmm-ternary-integer-ring-upgrade`)

## Summary Comparison

| Source | Format | Coefficient Ring | Rank Listed on 2026-10-18 | Our Rank | Improvement |
|---|---|---|---|---|---|
| Perminov FMM Table (`dronperminov/FastMatrixMultiplication`, `README.md` / `docs/ranks.md`) | `9x12x14` | `ZT = {-1, 0, 1}` | `960` (listed on 2026-10-18 (`ZT 960, Z 960`)) | **`954`** | **`-6` multiplications** |
| Perminov FMM Table (`dronperminov/FastMatrixMultiplication`, `README.md` / `docs/ranks.md`) | `9x12x14` | `Z` (integers) | `960` (listed on 2026-10-18 (`ZT 960, Z 960`)) | **`954`** (`ZT`) | **`-6` multiplications** |
| Perminov FMM Table / `fmm_sota.json` / Lille FMM Table | `9x12x14` | `Q` (rationals) | `940` | `954` (`ZT`) | Within target scope (`954 >= 940`) |

- **Dated Upstream Note:** Also published upstream by the contributor on 2026-10-19 (`schemes/known/mizopl/9x12x14_m954_ZT.json`); `docs/ranks.md` now lists `ZT 954 / Z 954`.

## Primary Table Fetches (UTC Time, URL, HTTP Status, SHA-256)

1. **Perminov FastMatrixMultiplication `README.md` (at filing on 2026-10-18) & `docs/ranks.md` (current table location)**
   - **URL (at filing):** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md`
   - **UTC fetch time:** `2026-10-18T12:35:49Z`
   - **HTTP status:** `200`
   - **SHA-256:** `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341`
   - **Exact row for `9x12x14` as listed on 2026-10-18 (`ZT 960, Z 960`, line 1350):**
     ```text
     | `9x12x14`  |   960 (?)   |   960 (?)    |  940 (945)   | **2.805232985** |
     ```
   - **Current `docs/ranks.md` URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md` (`sha256: 77203a718e82fec693578d193c9ccbb2332edcf41f086088a8405cd403666c5a`, fetched `2026-10-25T18:29:40Z`, HTTP `200`). Also published upstream by the contributor on 2026-10-19 (`schemes/known/mizopl/9x12x14_m954_ZT.json`); `docs/ranks.md` now lists `ZT 954 / Z 954`.

2. **Perminov FastMatrixMultiplication `schemes/status.json` (at filing on 2026-10-18)**
   - **URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/status.json`
   - **UTC fetch time:** `2026-10-18T12:35:49Z`
   - **HTTP status:** `200`
   - **SHA-256:** `b9b86c506ef4826220e5479569c6a84eaa720b703f73b705c043a3c90b463311`
   - **Exact entry for `9x12x14` as listed on 2026-10-18 (`ZT 960, Z 960`):** `ranks: {"Q": 940, "ZT": 960, "Z": 960}`, with only `schemes/results/ZT/9x12x14_m960_ZT.json` in `ZT` and no `Z` scheme.

3. **Sedoglavic `fmm_sota.json` & Lille FMM Catalogue (`9x12x14.html`)**
   - **URL:** `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`
   - **UTC fetch time:** `2026-10-18T12:35:50Z`
   - **HTTP status:** `200`
   - **SHA-256:** `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1`
   - **Exact entry:** `{"format": [9, 12, 14], "rank": 940, "exponent": 2.805233}` (rational `Q` scheme).
