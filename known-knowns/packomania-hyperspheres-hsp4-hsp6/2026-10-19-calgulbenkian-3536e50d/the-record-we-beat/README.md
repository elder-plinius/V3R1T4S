# The record we beat (metadata only)

No third-party page is copied here. Every row below is one honest GET (curl, User-Agent naming V3R1T4S, no retries). Two sets of fetches are recorded: the first made by the builder's triage agent before the panel (HTTP 200 each), and a second, later set made independently by the panel's novelty skeptic (times and hashes in `panel/novelty.md`). The Packomania radius table and pages had the same sha256 both times. The Cohn table has a different sha256 in the second fetch (the page may have changed in between); the converted values the panel used are in `panel/novelty.md`.

## First fetches (triage, 2026-10-19)

| Source | URL | UTC fetch time | HTTP | sha256 of the fetched file | Extracted cell |
|---|---|---|---|---|---|
| radius.txt (hsp4) | https://packomania.com/hsp4/txt/radius.txt | 2026-10-19T04:32:03Z | 200 | f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f | N=170 row 0.215589695168 |
| hsp4.html | https://packomania.com/hsp4/hsp4.html | 2026-10-19T04:32:08Z | 200 | 1c3a30644ba8ff73955547ff94e769a1983c146f4d2b14989eab3e0060a3feb3 | History of updates: entries of 04, 05, 06 Jul 2025 only |
| pending-requests.html | https://packomania.com/pending-requests.html | 2026-10-19T04:32:12Z | 200 | 92ce2e3dd9802a85edda90ace95a1e7d81dac08297c3903bba46289cdb2a14ae | no hsp4 entry; *many* bundle present |
| hsp4-170.txt (posted) | https://packomania.com/hsp4/txt/hsp4-170.txt | 2026-10-19T04:37:21Z | 200 | ee9afeb72586d7237e9abe52f458f3ef629ba93b7466f5fb18c598560d6062d8 | posted configuration, saved as table-record/posted_hsp4-170.txt |
| spherical-codes.org/plain (Cohn table) | https://spherical-codes.org/plain | 2026-10-19T04:36:21Z | 200 | d6374eb4ace2af690082ab9b49ba7739be1ad2df87d8cc3851dad9b1e1da1162 | rows for dimension 4 saved in cohn_rows.txt |
| Zenodo record (latest version) | https://zenodo.org/api/records/22981305/versions/latest | 2026-10-19T04:37:15Z | 200 | 62935b6b5f6f418f78bf09d4573d046ce405c98c23fddd5efcda6f23afcf0f66 | Moki and Julio v2.7 record metadata |

## Later fetches by the novelty skeptic (the values used in README.md, 'Compared to')

| Source | URL | UTC | HTTP | sha256 |
|---|---|---|---|---|
| Packomania pending requests | https://packomania.com/pending-requests.html | 05:37:25 | 200 | 92ce2e3dd9802a85edda90ace95a1e7d81dac08297c3903bba46289cdb2a14ae |
| Packomania hsp4 radius.txt | https://packomania.com/hsp4/txt/radius.txt | 05:37:26 | 200 | f3ddaa944aac014718bc9f5438700698abedac0189266198df8bb60772ac569f |
| Packomania hsp4.html | https://packomania.com/hsp4/hsp4.html | 05:37:27 | 200 | 1c3a30644ba8ff73955547ff94e769a1983c146f4d2b14989eab3e0060a3feb3 |
| V3R1T4S TROPHY_CASE.md | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 05:37:22 | 200 | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 |
| known-knowns hsp folder | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/packomania-hyperspheres-hsp4-hsp6 | 05:38:50 | 200 | 129aa0cf10c6aad0df9bb54da21fb0f607ebb7ffdeebcc675385698a1a591144 |
| Zenodo Moki and Julio, latest version (record 22986800, v2.7, published 2026-09-27); the first request to record 22981305 versions/latest answered 301 and was followed once | https://zenodo.org/api/records/22986800 | 05:37:46 | 200 | 62935b6b5f6f418f78bf09d4573d046ce405c98c23fddd5efcda6f23afcf0f66 |
| Same record, the zip file (581877889 bytes; md5 matches Zenodo's 24462e98...); I read MANIFEST.csv inside it (sha256 b7a042ef6a29ce8b219660691212111262e4091c14b941721dd1d3f491eec568, identical to the claim folder's snapshot copy; the 455 scu, 220 hsp4 and 169 hsp5 rows in mj_rows.csv match it with zero differences). The zip itself was deleted after extraction; its sha256 was f2dc44bd0b2800fae918268fb97eeb21560aa889d6369a4e4877444339da3da7 | https://zenodo.org/api/records/22986800/files/Hashirama1337s/moki-julio-circle-packing-v2.7.zip/content | 05:38:21 to 05:48:07 | 200 | see left |
| Cohn spherical-codes table | https://spherical-codes.org/plain | 05:42:49 | 200 | b99df04be3cbcc783533027be54eb903ca462c00591caaccfaa0a0bdb8a3e577 |

## Extracted cells (small excerpts, so that `verify-it-yourself/run_checks.sh` can print the comparison)

- `radius_rows_N170_to_300.txt`: 131 rows of the fetched hsp4 radius.txt, N=170 to N=300 (the end of the table), unchanged.
- `mj_rows_extract.csv`: the 127 hsp4 rows with N at least 170 of the Moki and Julio v2.7 MANIFEST.csv (manifest sha256 b7a042ef6a29ce8b219660691212111262e4091c14b941721dd1d3f491eec568; the panel's novelty skeptic compared the hsp4 rows with the real manifest from the Zenodo zip and found no difference).
- `cohn_rows_extract.txt`: the rows with N at least 170 of the dimension-4 rows of the spherical-codes table (format: dimension, N, cosine, polynomial), as saved at the triage fetch.

### History of updates excerpt (hsp4.html)
History of updates Please note that the results are taken from a running search. For updates look at the list below. 
04-Jul-2025: First presentation for N =2-100 by [contributor, ref 31]. The packings for N =2-23 can be easily derived from spherical codes in [1], where maximum separation angles &phi; between points on the surface of a 4-sphere are given. The radius r of a corresponding hypersphere for our packing problem can be calculated by r = sin(&phi;/2) / (1 + sin(&phi;/2)). For the range N =24-53, 55, we can take N -1 points from the corresponding spherical code and place one central hypersphere at the origin. 
05-Jul-2025: Extension to N =200 by [contributor, ref 31]. 
06-Jul-2025: Extension to N =300 by [contributor, ref 31].

(Excerpt of the History of updates of https://packomania.com/hsp4/hsp4.html; the maintainer's name replaced where it appeared.)

### Pending-requests excerpt
Excerpt of https://packomania.com/pending-requests.html (page dated 17-Oct-2026). Submitter names are omitted.
Categories named in the list: csc, ccq, crt, csq, chx, cpt, crc, cxd, csqv, cci, ssp. No entry names scu, hsp4, hsp5 or hsp6.
Entry relevant to the bank's caveat: 26-Sep-2026, Moki & Julio, category *many*, 4666 candidates total (category not specified).
Entry for the sibling category ssp: 15-Oct-2026, 17 candidates in the range 917-100000.

## Values

- Live row N=170: 0.215589695168 (N=169: 0.215785895566, N=171: 0.215441346347; the table is monotone here).
- Moki and Julio manifest (copy from the contributor's snapshot, file sha256 b7a042ef6a29ce8b219660691212111262e4091c14b941721dd1d3f491eec568) for hsp4 N=170: 0.2155917530134953452636646.
- Cohn's table of spherical codes in 4 dimensions, converted to ball packings (r = s/(2+s), s = sqrt(2-2c)), as computed by `table_compare.py`.

Not shipped: the posted Packomania coordinate file hsp4-170.txt (third-party data). The builder and the panel compared it with the object: largest difference of the sorted pairwise distances 9.0e-3, which is more than 1e-8 (`panel/criterion.md`).
