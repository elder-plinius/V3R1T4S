# Table record (scout, run fetches of 2026-10-26)

Every fetch was one plain GET with curl and the User-Agent "V3R1T4S-run (curl)", no cookies, no retries. Times are
UTC from `date -u`; sha256 of the saved body.

| fetched (UTC) | HTTP | URL | sha256 of body | value for sorted <14,15,15> |
|---|---|---|---|---|
| 2026-10-26T22:07:25Z | 200 | https://fmm.univ-lille.fr/ | 57e936b6aa0efe3a2e4020e14a84f5533983f66d5befd16fbb08bd448bd906a9 | row "<14x15x15:1848>" (catalogue index; the bank status_source; Last-Modified: Tue, 20 Oct 2026 08:14:45 GMT) |
| 2026-10-26T22:01:19Z | 200 | https://fmm.univ-lille.fr/14x15x15.html | 72bedfe2f8cb81f8a2b7ca2daa73561f04f2de1961c52e15dad8bf7c2fe8d465 | "Description of fast matrix multiplication algorithm: <14x15x15:1890>" (Last-Modified: Wed, 10 Jun 2026 10:43:30 GMT) |
| 2026-10-26T22:01:19Z | 200 | https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae | {"format": [14, 15, 15], "rank": 1848, "exponent": 2.801382}; createdAt 2026-10-19T20:46:33 |
| 2026-10-26T22:01:20Z | 200 | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/ranks.md | e71786dda6669d49fb1af448046cd294d7246977ba5372eeab5f536bf58dcbe4 | row "| `14x15x15` |    1894     | 1892 (1894)  | 1848 (1894)  | **2.801382482** |" under the header Format / `ZT` rank / `Z` rank / `Q` rank: minimum 1848 |
| 2026-10-26T22:01:20Z | 200 | https://raw.githubusercontent.com/MerlijnW70/fmm-schemes/main/SHA256SUMS | de848328881cf69cbe2a8d8309e04d94826cf1431b5b39e81db63f95af58a3fd | 32 lines; no 14x15x15 (or 15x14x15, 15x15x14) file |
| 2026-10-26T22:01:21Z | 200 | https://api.github.com/repos/MerlijnW70/fmm-schemes/git/trees/main?recursive=1 | f25a290fcb035c0a0b1df06f5baccbd99653698ed38b1abcc49807da335e8c37 | full repository tree, 39 paths, not truncated; none for 14x15x15 or a permutation |
| 2026-10-26T22:01:21Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 | entry 44: "<14,15,15> rank 1842 over Q (supersedes our 1843 of 2026-10-10)" |

The minimum over the four sources the criterion names is 1848 (fmm_sota.json and Perminov Q; the Lille index
row also reads 1848, the per-format page 1890). The claimed rank 1836 is 12 below it.

Values already public in this repository:
- merged known-knowns/faster-matrix-multiplication/schemes/14x15x15_r1842_Q.json, <14,15,15> rank **1842** over Q
  (TROPHY_CASE #44, row above). 1836 is 6 below it.
- Pull requests, all states, GitHub search API (one GET each):
  - `14x15x15`: 2026-10-26T22:01:49Z, HTTP 200, sha256 ccbb8c66cc8725a5bf9d9064e102599227f871811e314491d5fc92704aff9ca1, total_count 10
  - `15x15x14`: 2026-10-26T22:01:49Z, HTTP 200, sha256 840185ac69ff01c964c2bfead7f7b8a5a7764c3814155124f82ebe285189a90f, total_count 0
  - `15x14x15`: 2026-10-26T22:01:49Z, HTTP 200, sha256 840185ac69ff01c964c2bfead7f7b8a5a7764c3814155124f82ebe285189a90f, total_count 0
  - `"14,15,15"`: 2026-10-26T22:01:50Z, HTTP 200, sha256 39501d448712aab87aa20afd07f9d36eb239c295e48f10f5a5bb6b20afad8189, total_count 1
  - `"14 15 15"`: 2026-10-26T22:01:51Z, HTTP 200, sha256 5ae175c1fbc0ec076d940a9ef9c97e965da82aabc8fdad424c9133064ce647bc, total_count 24
  - `1836`: 2026-10-26T22:01:50Z, HTTP 200, sha256 39501d448712aab87aa20afd07f9d36eb239c295e48f10f5a5bb6b20afad8189, total_count 1
  - `fmm-catalogue-small-format-rank`: 2026-10-26T22:01:51Z, HTTP 200, sha256 20475ecd0ff8c55e2c39a4d9f562dc7466253e4f7416f931f856bd0ea02815a7, total_count 47
  Results for this cell: #432 (open, created 2026-10-18T18:08:23Z) "[claim] fmm-ternary-integer-ring-upgrade:
  14x15x15 ZT rank 1,894 ..." (another target; rank above 1842). #752 (open, created 2026-10-25T11:18:58Z, the same
  contributor's <14,14,15> rank 1709 claim) says in its body: "The intermediate <14,15,15> scheme. HOW_WE_FOUND_IT.md
  and how-we-built-it/COMMANDS.md name the chain's intermediate <14,15,15> scheme of rank 1836. It is not claimed here
  (...)." Its rebuild code (step 1 of its chain) regenerates this object.
  No pull request claims (14,15,15) or a permutation at a rank <= 1841.

Parent file: https://raw.githubusercontent.com/khoruzhii/lita/HEAD/schemes/15x15x15_r1977.npz
fetched 2026-10-26T22:04:33Z, HTTP 200, sha256 94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33; git blob sha1 65821484d954b4aade06cbda624932ba2a481f7b,
equal to the entry schemes/15x15x15_r1977.npz in the LITA tree (https://api.github.com/repos/khoruzhii/lita/git/trees/HEAD?recursive=1, fetched 2026-10-26T22:04:33Z, HTTP 200, sha256 d923a68888fc427aa8e9d216c6e54d45eb078afb8718ea55ae4990f443b89339).
