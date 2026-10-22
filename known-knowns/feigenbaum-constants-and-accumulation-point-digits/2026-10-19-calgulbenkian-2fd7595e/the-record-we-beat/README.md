# The record we beat (metadata only)

No third-party page is copied here. Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries) made by the builder's triage agent on 2026-10-19; the panel's novelty skeptic fetched OEIS A195102 again at 2026-10-19T05:37:36Z (HTTP 200, same sha256 5761a679e8ccdb464615f6a89348ca1701337e8f8c8c82fc27acba951931db13) and did not refetch the thesis (details in `panel/novelty.md`).

| Source | URL | UTC fetch time | HTTP | sha256 of the fetched file | Extracted cell |
|---|---|---|---|---|---|
| OEIS A195102 (json) | https://oeis.org/search?q=id:A195102&fmt=json | 2026-10-19T04:47:07Z | 200 | 5761a679e8ccdb464615f6a89348ca1701337e8f8c8c82fc27acba951931db13 | data field: 49 digits 1.6903029714052448533437801503241613482282780597095619666824 (leading digits); saved in oeis_A195102_data.txt |
| Thurlby thesis (PDF) | https://pure.port.ac.uk/ws/portalfiles/portal/43264172/Thesis_Final_Judi_Thurlby_September_2021.pdf | 2026-10-19T04:50:22Z | 200 | 65e64ebfa43a5384b652df6fe9e5eeda9a47958515fa42d8342baed1cae68173 | page 86, Table 4.6: alpha_4 331 digits, delta_4 325 digits proven; excerpt saved in thurlby_table_4_6_excerpt.txt (text extracted from the PDF by the triage agent) |

Extracted cells, saved here so that `verify-it-yourself/run_checks.sh` can compare digit by digit:

- `oeis_A195102_data.txt`: the name, offset and data field of the OEIS record (49 digits of alpha_4).
- `thurlby_table_4_6_excerpt.txt`: the digit tables for alpha_4 and delta_4 and their caption, as extracted from the thesis PDF text (page 86, Table 4.6): 331 digits of alpha_4 and 325 of delta_4, proven correct in the thesis.

The values compared are: OEIS A195102 (49 decimal digits in its data field) and the thesis (331 digits of alpha_4 and 325 of delta_4, from a proof with truncation degree N = 640). The bank text quotes OEIS as 50 digits and the thesis as about 330.

Other digit counts found by the panel's novelty skeptic (not table cells we compare against, listed for completeness): arXiv 2409.20457 (validated enclosures for the quartic case, order m=2: the eigenvalue to 41 digits, in the novelty report's reading); no OEIS sequence for delta_4 exists.
