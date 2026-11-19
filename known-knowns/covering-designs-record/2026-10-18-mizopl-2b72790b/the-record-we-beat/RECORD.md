# The Record We Beat: `C(68, 14, 5)`

## Summary Comparison

| Source | $(v, k, t)$ | Best Known Upper Bound $b$ | Our Upper Bound $b$ | Improvement |
|---|---|---|---|---|
| Covering Repository (`coveringrepository.com`, current live cell — Wynand van Staden, `2026-10-22`) | $(68, 14, 5)$ | $16,001$ | **$15,675$** | **$-326$ blocks ($-2.04\%$)** |
| Covering Repository (`coveringrepository.com`, dated `2026-10-18` reading at initial filing) | $(68, 14, 5)$ | $16,004$ | $15,675$ | ($-329$ blocks vs 18 Oct reading) |
| La Jolla Covering Repository v1.2 (`dmgordon.org/covering-designs/`, Zenodo `19735294`) | $(68, 14, 5)$ | $16,004$ | $15,675$ | ($-329$ blocks vs LJCR v1.2; **$-326$ blocks** vs current best $16,001$) |
| Schonheim Lower Bound $L(68, 14, 5)$ | $(68, 14, 5)$ | $5,785$ (lower bound) | $15,675$ | — |

## Primary Table Fetches (UTC Time, URL, HTTP Status, SHA-256)

1. **Covering Repository (`coveringrepository.com`)**
   - **Current live cell for $(68, 14, 5)$ (confirmed in browser, `2026-11-17`):** `16,001` blocks (Wynand van Staden, `22 October 2026`, posted after our initial `18 October 2026` filing), giving a margin of **`326` blocks** (`16,001 -> 15,675`, `-2.04%`).
   - **Dated `18 October 2026` plain $(v,k,t)$ archive fetch at initial filing:**
     - **URL:** `https://coveringrepository.com/download_archive_vkt.aspx`
     - **UTC fetch time:** `2026-10-18T10:33:16Z`
     - **HTTP status:** `200`
     - **SHA-256 of fetched archive:** `f02f5fc233aa66ca835b8f0b1b4d751fd35ad721c5264043ceb515ee95da9277`
     - **Exact line for $(68, 14, 5)$ on `2026-10-18`:**
       ```
       68	14	05	05		16004
       ```

2. **La Jolla Covering Repository (`dmgordon.org/covering-designs/`)**
   - **URL:** `https://dmgordon.org/covering-designs/`
   - **UTC fetch time:** `2026-10-18T10:33:20Z`
   - **HTTP status:** `200`
   - **SHA-256 of fetched status page:** `a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3`
   - **Zenodo archive (`https://zenodo.org/api/records/19472830` / LJCR v1.2 `19735294`):** `16004` blocks for `(68, 14, 5)`.
