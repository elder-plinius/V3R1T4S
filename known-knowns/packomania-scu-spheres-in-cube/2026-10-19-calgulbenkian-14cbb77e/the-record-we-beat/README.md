# The record we beat (metadata only)

No third-party page is copied here. Every row below is one honest GET (curl, User-Agent naming V3R1T4S, no retries). Two sets of fetches are recorded: the first made by the builder's triage agent before the panel (HTTP 200 each), and a second, later set made independently by the panel's novelty skeptic (times and hashes in `panel/novelty.md`; the radius table and the pages had the same sha256 both times).

## First fetches (triage, 2026-10-19, UTC times in the table)

| Source | URL | UTC fetch time | HTTP | sha256 of the fetched file | Extracted cell |
|---|---|---|---|---|---|
| radius.txt (scu) | https://packomania.com/scu/txt/radius.txt | 2026-10-19T04:31:56Z | 200 | 2e2af491aa08d8eba54a88cdbb6b3b007dacac59f4f12d60d00a3687d8b01791 | N=733 row 0.058531064607; N=734 row 0.058943675866 |
| scu.html | https://packomania.com/scu/scu.html | 2026-10-19T04:31:58Z | 200 | 7b77906badc3ee9ed081ee8dd6033b4897531b3a932e6fd03fe828963eb8c1de | History of updates, last entry 17-Oct-2026; page dated 17-Oct-2026 |
| pending-requests.html | https://packomania.com/pending-requests.html | 2026-10-19T04:32:12Z | 200 | 92ce2e3dd9802a85edda90ace95a1e7d81dac08297c3903bba46289cdb2a14ae | no scu entry; *many* bundle present |
| scu733.txt (posted) | https://packomania.com/scu/txt/scu733.txt | 2026-10-19T04:35:18Z | 200 | fdbff424438261147ece88e91fed84807812e207e6f55bd5887b2483ead19ec4 | posted configuration, saved as table-record/posted_scu733.txt |
| scu734.txt (posted, not saved) | https://packomania.com/scu/txt/scu734.txt | 2026-10-19T04:35:19Z | 200 | 99f0f667096abe3c5398f34d403272c9f4cdd4f3b1b32b878d0aac2cf498cafa | posted N=734 configuration, used by the contributor's derivation |
| Zenodo record (latest version) | https://zenodo.org/api/records/22981305/versions/latest | 2026-10-19T04:37:15Z | 200 | 62935b6b5f6f418f78bf09d4573d046ce405c98c23fddd5efcda6f23afcf0f66 | Moki and Julio v2.7 record metadata (publication date 2026-09-27) |

## Later fetches by the novelty skeptic (the values used in README.md, 'Compared to')

| Source | URL | UTC | HTTP | sha256 |
|---|---|---|---|---|
| Packomania scu radius.txt | https://packomania.com/scu/txt/radius.txt | 05:37:23 | 200 | 2e2af491aa08d8eba54a88cdbb6b3b007dacac59f4f12d60d00a3687d8b01791 |
| Packomania scu.html | https://packomania.com/scu/scu.html | 05:37:24 | 200 | 7b77906badc3ee9ed081ee8dd6033b4897531b3a932e6fd03fe828963eb8c1de |
| Packomania pending requests | https://packomania.com/pending-requests.html | 05:37:25 | 200 | 92ce2e3dd9802a85edda90ace95a1e7d81dac08297c3903bba46289cdb2a14ae |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 05:37:22 | 200 | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 |
| known-knowns scu folder | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/packomania-scu-spheres-in-cube | 05:38:51 | 200 | c812a1132623d5d083cc982e44551b3db93005c10b12404434cac40d00ab87e7 |
| Zenodo Moki and Julio, latest version (record 22986800, v2.7, published 2026-09-27); the first request to record 22981305 versions/latest answered 301 and was followed once | https://zenodo.org/api/records/22986800 | 05:37:46 | 200 | 62935b6b5f6f418f78bf09d4573d046ce405c98c23fddd5efcda6f23afcf0f66 |
| Same record, the zip file (581877889 bytes; md5 matches Zenodo's 24462e98...); I read MANIFEST.csv inside it (sha256 b7a042ef6a29ce8b219660691212111262e4091c14b941721dd1d3f491eec568, identical to the claim folder's snapshot copy; the 455 scu, 220 hsp4 and 169 hsp5 rows in mj_rows.csv match it with zero differences). The zip itself was deleted after extraction; its sha256 was f2dc44bd0b2800fae918268fb97eeb21560aa889d6369a4e4877444339da3da7 | https://zenodo.org/api/records/22986800/files/Hashirama1337s/moki-julio-circle-packing-v2.7.zip/content | 05:38:21 to 05:48:07 | 200 | see left |

## Extracted cells (small excerpts, so that `verify-it-yourself/run_checks.sh` can print the comparison)

- `radius_rows_N733_to_1000.txt`: 268 rows of the fetched radius.txt, N=733 to N=1000, unchanged. The confirmed scope compares against the largest row at any N' from 733 up to 1000, which this file contains. (The full table has 1134 rows up to N=1024192; larger N' were not examined.)
- `mj_rows_extract.csv`: the 120 scu rows with N at least 733 of the Moki and Julio v2.7 MANIFEST.csv (manifest sha256 b7a042ef6a29ce8b219660691212111262e4091c14b941721dd1d3f491eec568; the panel's novelty skeptic compared the full scu, hsp4 and hsp5 rows with the real manifest from the Zenodo zip and found no difference).
- History of updates of scu.html (2026 entries) and the pending-requests excerpt, contributor names removed: below.

### History of updates excerpt
04-Oct-2026: There were very old candidates on my laptop (from July 2022) for N =94-96, 109-120, 123-125, 127, 129, 131, 132, 134-139, 145-152, 154, 155, 157-160, 174-187, 191-194, 197-200 by [contributor, ref 30]. 
05-Oct-2026: A large bundle of new records for N =202, 203, 205, 224, 228, 235-239, 257, 258, 265, 271, 281, 290, 291, 293, 295, 297, 298, 301, 305-309, 326, 328-330, 336, 338-343, 367, 377, 383, 396, 408-411, 417-427, 448, 451, 456-459, 461-463, 501-506, 508-529, 551, 553-557, 559-563, 568-576 by [contributor, ref 32]. 
06-Oct-2026: Many new records for N =102, 110, 205, 206, 208, 225, 232, 233, 259, 260, 263-265, 293-296, 300-305, 329, 331, 333, 335-337, 366, 368-371, 373, 375, 376, 378-382, 397, 411, 448, 450, 452-456 by [contributor, ref 33]. 
08-Oct-2026: A continuation of the last update for N =458-465, 469, 509, 511, 512, 518, 551, 552, 555, 558-562, 568, 571-573, 575-578, 601-629, 667-684, 727-732, 788-792, 794-798, 801-811, 865-885, 937-946 by [contributor, ref 33]. 
17-Oct-2026: A continuation of the last update for N =95, 96, 101, 102, 110, 111, 117, 118, 123-125, 130, 135, 137-139, 149, 150, 157, 181, 184-187, 192-195, 200-204, 206-213, 222-229, 231-240, 257-263, 266-268, 271-274, 282, 283, 289-302, 305-310, 321-334, 336-345, 366-378, 380-384, 396, 398, 399, 406-414, 417, 418, 420-427, 446-452, 454-463, 466-469, 501-506, 508-510, 512-529, 553-557, 563, 568-571, 573, 574, 578, 601-603, 605, 607, 608, 610, 613-617, 619-629, 667, 670, 672, 683, 684, 728, 730, 731, 734, 735, 788-795, 797, 801, 804, 806-811, 865-870, 872-874, 876, 878, 879, 881-883 by [contributor, ref 33]. 
17-Oct-2026: The next update for N =101, 210-212, 297, 366, 417, 421, 422, 459-463, 509, 513, 517, 518, 522-524, 555, 556, 573, 630, 734-737, 740-742, 745-747, 793-795, 808, 1596 by [contributor, ref 34]. 
17-Oct-2026: The table has been reorganized.

(Excerpt of the History of updates of https://packomania.com/scu/scu.html, 2026 entries; contributor names replaced by [contributor]. N=733 does not appear in any 2026 entry; N=734 and 735 appear in the first 17-Oct-2026 entry, N=734-737 and 740-742 in the second.)

### Pending-requests excerpt
Excerpt of https://packomania.com/pending-requests.html (page dated 17-Oct-2026). Submitter names are omitted.
Categories named in the list: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv, cci, ssp. No entry names scu, hsp4, hsp5 or hsp6.
Entry relevant to the bank's caveat: 26-Sep-2026, Moki & Julio, category *many*, 4666 candidates total (category not specified).
Entry for the sibling category ssp: 15-Oct-2026, 17 candidates in the range 917-100000.

## Values

- Live row N=733: 0.058531064607. Live row N=734: 0.058943675866 (the largest row at any N' >= 733 in the fetched file). Live row N=741: 0.058627036756.
- The Moki and Julio manifest (Zenodo record 22986800, version v2.7, per the saved record metadata; the manifest rows in `mj_rows.csv` are copied from the contributor's snapshot copy, file sha256 b7a042ef6a29ce8b219660691212111262e4091c14b941721dd1d3f491eec568, which the triage agent used as its bar) lists N=733 as 0.0588218693814828687141927.
- `table_compare.py` prints these numbers next to the computed radius. Its output is pasted in `verify-it-yourself/RECEIPTS.md`.
- `pending_requests_excerpt.txt` and `history_excerpt.txt` hold the queue and update-history excerpts (names omitted).

Not shipped: the posted Packomania coordinate file scu733.txt (sha256 in the first-fetch table; it is third-party data). Its comparison with the object (largest difference of the sorted pairwise distances about 7.7e-2) was done by the builder and re-done by the panel (`panel/criterion.md`).
