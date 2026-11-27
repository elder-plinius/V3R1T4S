# The record we compared against: OEIS A155520

Status source for this cell: https://oeis.org/A155520 (bank target oeis-keyword-more-new-terms, status_source
https://oeis.org/search?q=keyword:more).

## Extracted cell
| quantity | OEIS value | this package |
|---|---|---|
| A(6,1), flattened index 22 (start of row 6) | absent: DATA 1,2,3,2,4,2,6,1,1,5,2,6,9,1,4,4,4,2,1,2,2 (rows 1..5, offset 1,2), %K nonn,tabf,more, %I #12 Sep 24 2025; b-file (synthesized from the entry) ends "21 2"; history newest revision #12 (Andrei Zabolotskii, Sep 24 2025, approved), no pending draft; value searches of the row-6 head: No results | 6 (row 6, k = 1..42: 6,2,6,9,11,4,4,4,2,15,8,2,0,6,12,0,0,1,4,6,0,4,4,0,8,4,0,0,0,4,0,0,0,1,2,0,0,2,0,0,0,1) |

## Claim-time fetches (one plain curl GET each, User-Agent naming V3R1T4S research, no cookies, no retries)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T21:46:40Z | https://oeis.org/A155520 | 200 | bc44b8dc79a6b3830b9fbadd77e23982cc0f686bd6fd0ebbcef1ce2860acab96 |
| 2026-11-03T21:46:40Z | https://oeis.org/search?q=id:A155520&fmt=text | 200 | 09faabfe06ade0fe0cdde54d510aaedf6d165249b505098353e8ea023ad4146d |
| 2026-11-03T21:46:40Z | https://oeis.org/A155520/b155520.txt | 200 | 255b579936bb85108c7d7ed9ac42810e17d9826e957b574c386a584c7c44992d |
| 2026-11-03T21:46:40Z | https://oeis.org/history?seq=A155520 | 200 | 1cde8f3f3d6c0ef6e9e6e4525e655862499c176650ce35e4cf749aac3dad69bc |
| 2026-11-03T21:46:40Z | https://oeis.org/search?q=id:A014307&fmt=text | 200 | 02efe5aad3ff5928d739b9680e6c1f37e9318b6bf8f9e409c9b0cb656f84cdd9 |
| 2026-11-03T21:47:49Z | https://oeis.org/search?q=6,2,6,9,11,4,4,4,2,15,8,2&fmt=text | 200 | b3abb46299943a879ff2c7ec1132d06db2b6b593b5873e2a7af34df32de1e844 |
| 2026-11-03T21:47:50Z | https://oeis.org/search?q=1,2,2,6,2,6,9,11&fmt=text | 200 | 0d85230ea051968bb6078f14971cdec1f89e5e4654ede95c83d0a7a2886b234a |
| 2026-11-03T21:47:51Z | https://oeis.org/search?q=6,2,6,9,11,4&fmt=text | 200 | 28d10fd70527dba81036171f581af9190ddbf977d374d0593212e5c04f8811d2 |
| 2026-11-03T21:48:17Z | https://oeis.org/search?q=id:A155520&fmt=text | 000 (connection failure, not retried) | - |
| 2026-11-03T21:48:18Z | https://oeis.org/A155520/b155520.txt | 200 | 255b579936bb85108c7d7ed9ac42810e17d9826e957b574c386a584c7c44992d |
| 2026-11-03T21:48:18Z | https://oeis.org/history?seq=A155520 | 200 | d41ba486c6b70372d3e16e8de4eeb986d04e89d1de0e6471c669bf86eda00333 |
| 2026-11-03T21:48:25Z | https://oeis.org/A155520 | 200 | 669dde7e64cb7fcfd5b505665919ed6cf40f497cd2a10499e42f3ab00835a231 |

The novelty skeptic made its own fetches of the entry, b-file, history and value searches at about 2026-11-03T21:50Z
(panel/novelty.md).

## Gate re-fetch (one plain curl GET each)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T21:54:58Z | https://oeis.org/search?q=id:A155520&fmt=text | 200 | 09faabfe06ade0fe0cdde54d510aaedf6d165249b505098353e8ea023ad4146d |
| 2026-11-03T21:54:58Z | https://oeis.org/A155520 | 200 | ad9d92c13f05315625c0a08a7099dadb53a5cffbd510ef45f55084e22f32a156 |
| 2026-11-03T21:54:58Z | https://oeis.org/A155520/b155520.txt | 200 | 255b579936bb85108c7d7ed9ac42810e17d9826e957b574c386a584c7c44992d |
| 2026-11-03T21:54:58Z | https://oeis.org/history?seq=A155520 | 200 | 8c453d0dd0544ce00bb38648c98ea36e31f91234a20b8aec95101a7a17ec933f |
| 2026-11-03T21:54:58Z | https://oeis.org/search?q=6,2,6,9,11,4,4,4,2,15,8,2&fmt=text | 200 | b3abb46299943a879ff2c7ec1132d06db2b6b593b5873e2a7af34df32de1e844 |
| 2026-11-03T21:54:58Z | https://oeis.org/search?q=1,2,2,6,2,6,9,11&fmt=text | 200 | 0d85230ea051968bb6078f14971cdec1f89e5e4654ede95c83d0a7a2886b234a |
| 2026-11-03T21:54:58Z | https://oeis.org/search?q=6,2,6,9,11,4&fmt=text | 200 | 28d10fd70527dba81036171f581af9190ddbf977d374d0593212e5c04f8811d2 |

Result: entry text and b-file byte-identical to claim time (%I #12 Sep 24 2025, %K nonn,tabf,more, %O 1,2, DATA ends
at index 21); history still revisions #1-#12, newest approved, no draft (the HTML page bytes vary between fetches:
footer time and a script token); no row-6 value in entry text, entry page or history; all three value searches
"No results.", byte-identical to claim time.

Response headers were not recorded for these fetches. The pages themselves are not shipped (third-party content).
