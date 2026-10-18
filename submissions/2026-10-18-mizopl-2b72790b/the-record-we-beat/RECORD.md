# The Record We Beat: `C(68, 14, 5)`

## Summary Comparison

| Source | $(v, k, t)$ | Best Known Upper Bound $b$ | Our Upper Bound $b$ | Improvement |
|---|---|---|---|---|
| Covering Repository (`coveringrepository.com`) | $(68, 14, 5)$ | $16,004$ | **$15,675$** | **$-329$ blocks ($-2.06\%$)** |
| La Jolla Covering Repository (`dmgordon.org/covering-designs/`) | $(68, 14, 5)$ | $16,004$ | **$15,675$** | **$-329$ blocks ($-2.06\%$)** |
| Schonheim Lower Bound $L(68, 14, 5)$ | $(68, 14, 5)$ | $5,785$ (lower bound) | $15,675$ | — |

## Primary Table Fetches (UTC Time, URL, HTTP Status, SHA-256)

1. **Covering Repository plain $(v,k,t)$ archive (`coveringrepository.com`)**
   - **URL:** `https://coveringrepository.com/download_archive_vkt.aspx`
   - **UTC fetch time:** `2026-10-18T10:33:16Z`
   - **HTTP status:** `200`
   - **SHA-256 of fetched archive (`cr_archive_vkt.txt`):** `f02f5fc233aa66ca835b8f0b1b4d751fd35ad721c5264043ceb515ee95da9277`
   - **Exact line for $(68, 14, 5)$:**
     ```
     68	14	05	05		16004
     ```

2. **La Jolla Covering Repository (`dmgordon.org/covering-designs/`)**
   - **URL:** `https://dmgordon.org/covering-designs/`
   - **UTC fetch time:** `2026-10-18T10:33:20Z`
   - **HTTP status:** `200`
   - **SHA-256 of fetched status page (`ljcr_home.html`):** `a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3`
   - **Zenodo archive (`https://zenodo.org/api/records/19472830` / v1.2 `19735294`, `covers.json`):** `16004` blocks for `(68, 14, 5)`.
