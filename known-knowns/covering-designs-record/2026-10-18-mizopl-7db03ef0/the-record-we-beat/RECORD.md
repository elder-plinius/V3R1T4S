# The Record We Beat: `C(40, 16, 7)`

## Summary Comparison

| Source | $(v, k, t)$ | Best Known Upper Bound $b$ | Our Upper Bound $b$ | Improvement |
|---|---|---|---|---|
| Covering Repository (`coveringrepository.com`) | $(40, 16, 7)$ | $7,470$ | **$7,251$** | **$-219$ blocks ($-2.932\%$)** |
| La Jolla Covering Repository (`dmgordon.org/covering-designs/`) | $(40, 16, 7)$ | $7,470$ | **$7,251$** | **$-219$ blocks ($-2.932\%$)** |
| Schonheim Lower Bound $L(40, 16, 7)$ | $(40, 16, 7)$ | $1,965$ (lower bound) | $7,251$ | — |

## Primary Table Fetches (UTC Time, URL, HTTP Status, SHA-256)

1. **Covering Repository plain $(v,k,t)$ archive (`coveringrepository.com`)**
   - **URL:** `https://coveringrepository.com/download_archive_vkt.aspx`
   - **UTC fetch time:** `2026-10-18T17:27:33Z`
   - **HTTP status:** `200`
   - **SHA-256 of fetched archive (`cr_archive_vkt.txt`):** `6d317b207c4f582d7e913c4c7d6ebd0305407fdcd2dbb6de1901adf4f13a2704`
   - **Exact line for $(40, 16, 7)$ (line 5135):**
     ```
     40	16	07	07		7470
     ```

2. **La Jolla Covering Repository (`dmgordon.org/covering-designs/`)**
   - **URL:** `https://dmgordon.org/covering-designs/`
   - **UTC fetch time:** `2026-10-18T17:27:34Z`
   - **HTTP status:** `200`
   - **SHA-256 of fetched status page (`ljcr_home.html`):** `a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3`
   - **Zenodo archive (`https://zenodo.org/api/records/19472830` / v1.2 `19735294`, `coverdata.json`, `sha256: 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87`):** `7470` blocks for `(40, 16, 7)` (`low_bd: 1965`).
