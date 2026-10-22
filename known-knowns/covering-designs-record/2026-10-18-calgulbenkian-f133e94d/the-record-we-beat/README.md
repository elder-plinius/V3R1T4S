# The record we beat (metadata only)

No third-party page is copied here. Cell: covering design C(57,14,3), the plain (v,k,t) table, section m = t = 3. Best listed value: 109. This object: 108.

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| coveringrepository.com, plain (v,k,t) table (panel novelty skeptic: form POST V=0, K=14, T=3, M=3) | https://coveringrepository.com/systems.aspx | 2026-10-18T14:24:06Z | 200 | a2e903b063e78366c55ad98ff5ed7ed93b2186845b76829bafa6fa092e81fd8d | 57 14 03 03: 109 blocks, lower bound 90; Franco Atzeni, Local Search, 14/02/2025 |
| same table, read again by the panel criterion skeptic (form POST) | https://coveringrepository.com/systems.aspx | 2026-10-18T14:34:14Z | 200 | 69c8bde5...2b76 (abbreviated in the skeptic's report; see panel/criterion.md) | same row: 109 |
| LJCR data on GitHub, coverdata.json | https://raw.githubusercontent.com/dmgordo/LJCR/master/coverings/coverdata.json | 2026-10-18T14:24:23Z | 200 | 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef | C(57,14,3): 110 (Jan de Heer and Steve Muir, 2013-09-05) |
| LJCR on Zenodo v1.2, coverdata.json | https://zenodo.org/api/records/19735294/files/coverdata.json/content | 2026-10-18T14:24:38Z | 200 | 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87 | C(57,14,3): 109 (Franco Atzeni, Local Search, 2025-02-14) |
| LJCR page | https://dmgordon.org/covering-designs/ | 2026-10-18T14:34:22Z | 200 | a5cc2312afc8dedd... (full hash in the orchestrator record below) | prose only, last updated 2026-09-03; lists no per-cell value |

The first row is the most recent fetch with a full hash. The full details (every other source read, the empty latest-improvements pages, the hobbyist repositories) are in `panel/novelty.md`, `panel/criterion.md` and the files below. The table is served only through the site's own search form, so each value was read by one GET of the page and one form POST.

The text below is the original record written before the panel. Where it says the orchestrator had no form-post fetch of its own, the panel's novelty skeptic made one afterwards (first row above), recorded in `live_refetch_2026-10-18.md`.


Cell: covering design C(57,14,3), plain (v,k,t) table, section m = t = 3 on coveringrepository.com. Object: 108 blocks.

Plainly, which values come from whom:

- Items 1, 4, 5 and 6 in the first table below come from Argon's saved files (the author's own snapshots, taken 2026-10-17 and 2026-10-18 on its laptop, not by the orchestrator). The orchestrator read the saved files and computed their sha256; the orchestrator did not fetch those URLs itself for this cell.
- Items 2 and 3 are the orchestrator's own fetches, taken on 2026-10-18 (curl, User-Agent naming V3R1T4S, one GET per URL, no retries).
- The coveringrepository.com table needs an ASP.NET form post (a plain GET of the page does not return the (57,14,3) row). The orchestrator has no form-post fetch of its own for this cell. The only direct record of the value 109 is Argon's form-post snapshot. Whoever checks novelty should re-fetch it.

## Argon's snapshots (author's files, read by the orchestrator)

| # | What | Source URL | Taken by | Time | sha256 of the saved file | Extracted value |
|---|---|---|---|---|---|---|
| 1 | coveringrepository.com, plain (14,3) section, m=3, form-post result | https://coveringrepository.com/ (systems page, form post) | Argon | 2026-10-17, about 22:41Z (the saved file's timestamp; HTTP status not recorded) | 51fa4981a6f7640f75a8a1eed403fdbf133764c0d24c1077086ff40b1ba4240a | row for v=57, k=14, t=3, m=3: size 109, lower bound 90, creator Franco Atzeni, method Local Search, date 14/02/2025. Row text saved as cr_row_57_14_3.txt |
| 4 | LJCR GitHub data, coverdata.json | https://github.com/dmgordo/LJCR | Argon | 2026-10-17 (saved file timestamp 22:38) | 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef | key C(57,14,3): size 110, low_bd 90, best improvement 110 by Jan de Heer and Steve Muir, 2013-09-05 |
| 5 | Zenodo LJCR v1.2, coverdata.json (record 10.5281/zenodo.19735294, created 2026-04-24) | https://zenodo.org/records/19735294 | Argon | 2026-10-17 (saved file timestamp 22:38) | 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87 | key C(57,14,3): size 109, low_bd 90, best improvement 109 by Franco Atzeni, Local Search, 2025-02-14 09:31:41 |
| 6 | thebrockchain/covering-designs README | https://github.com/thebrockchain/covering-designs | Argon | 2026-10-17 (saved file timestamp 22:38) | 171f9f5e88341cc90576de0f3016d0ed67569c54e33c1ed16ae729d49b066da5 | claims only C(28,13,4) <= 53 and C(32,13,4) <= 95; no (57,14,3) |

Items 4 and 5 are saved in full by Argon; the (57,14,3) entries are extracted in ljcr_zenodo_entries_57_14_3.json. The two data files are 6.5 MB and 8.3 MB and are not copied here.

## The orchestrator's own fetches (2026-10-18)

| # | What | URL | UTC fetch time | HTTP | sha256 | Extracted |
|---|---|---|---|---|---|---|
| 2 | coveringrepository.com latest-improvements, pages 1-3 | https://coveringrepository.com/systems.aspx?li=1 (and li=2, li=3) | 2026-10-18T13:47:16Z, 13:47:17Z, 13:47:18Z | 200, 200, 200 | 9c10420d6314509becc67354f7d74369225fccfaf3ae8b02d6cec38fd2b9421e ; eefd3fa0038282fa4edda0b3991318bc6b713634f40ae26676e8244ecb6cca1e ; 25552458d8bc875c3e2537c10d850a646ba974da011d4ebaa81e0c88a56a03bc | 300 rows, all dated 18/10/2026; no (57,14,3) row. See latest_pages_scan.txt |
| 3a | Wynand van Staden RECORDS.md | https://raw.githubusercontent.com/WynandVStaden/covering-design-records/HEAD/RECORDS.md | 2026-10-18T13:47:43Z | 200 | 41ffe04b8e3ce9e4e7db7c5fb5ab6864325b8ef2d5e5c5d7c65dbcf7c2ea70a3 | no (57,14,3) row; rows with v=57 are in wynand_rows_v57.txt (k = 9, 12, 16) |
| 3b | LJCR page (prose page; no table of values) | https://dmgordon.org/covering-designs/ | 2026-10-18T13:46:58Z | 200 | a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3 | site last updated 2026-09-03; it states that coveringrepository.com holds more recent improvements; it lists no (57,14,3) value |

Notes on what these do and do not show: the three latest-improvements pages cover only the 300 most recent entries, all dated 18 October 2026, so they show that no (57,14,3) entry was posted in that window and say nothing about earlier dates. The value 109 dated 14/02/2025 on the form-post row is older than that window. The LJCR value on GitHub (110) is the older snapshot; Zenodo v1.2 (109) already contains the Atzeni improvement.

Compared cell: C(57,14,3). Reference (best value among the sources above): 109. This object: 108. Schonheim lower bound L(57,14,3) = 90 (computed by verify-it-yourself/schonheim.py; both snapshots also list lower bound 90).
