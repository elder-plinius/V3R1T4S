# The record we compared against: OEIS A214570

Status source for this cell: https://oeis.org/A214570 (bank target oeis-keyword-more-new-terms, status_source
https://oeis.org/search?q=keyword:more).

## Extracted cell
| quantity | OEIS value | this package |
|---|---|---|
| a(17), first index missing | absent: DATA 1,1,1,2,3,4,6,12,24,40,60,120,240,420,840,1680 (a(1..16), offset 1,4), %K nonn,hard,more, %I #29 May 28 2015, %E "a(12)-a(16) from Alois P. Heinz, Sep 06 2012"; b-file (synthesized from the entry) ends "16 1680"; history newest revision #29 (Alois P. Heinz, May 28 2015, proposed -> approved), no pending draft; A214569 (row n has A214570(n) entries) has rows 1..16 only; full-prefix value search: No results | 3360 |

## Claim-time fetches (one plain curl GET each, User-Agent naming V3R1T4S research, no cookies, no retries)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T21:36:24Z | https://oeis.org/search?q=3360&fmt=text | 200 | 1d7f92d234ede1fd7b72d2206881e7c75642d815ca226fea455bfdda1a58c960 |
| 2026-11-03T21:36:24Z | https://oeis.org/search?q=1680,3360&fmt=text | 200 | b3fbd15cadb8d5ef88043d306ce5358c78676228e65434f4a9919479f131f23c |
| 2026-11-03T21:36:39Z | https://oeis.org/search?q=420,840,1680,3360&fmt=text | 000 (connection failure) | - |
| 2026-11-03T21:36:40Z | https://oeis.org/search?q=1,1,1,2,3,4,6,12,24,40,60,120,240,420,840,1680,3360&fmt=text | 200 | c0ee7a9b9258e37391d0a0cdcde3535a2f34a8bca8dc373dfe5070c0e1b00435 |
| 2026-11-03T21:36:40Z | https://oeis.org/search?q=id:A214570&fmt=text | 200 | 01439a4fa1cf899471a8162720f7f6416b55844665b938189a7539645b177991 |
| 2026-11-03T21:36:40Z | https://oeis.org/A214570/b214570.txt | 200 | 1990f8783a5b76c374ab6f8acc0c1eeb4e635546884e1ec13b255421788ebb64 |
| 2026-11-03T21:36:40Z | https://oeis.org/history?seq=A214570 | 200 | 09e14acfa6f915c8a4181c0f309bd0c439ffa9934e44404a8ca0eaaaea7c0c27 |
| 2026-11-03T21:36:40Z | https://oeis.org/search?q=id:A214569&fmt=text | 200 | 5cc11a046f0fa1b9784c9a74d524ac0ccc01e7247a618e11cd7ff503ce024e9f |
| 2026-11-03T21:38:01Z | https://oeis.org/search?q=1680,3360&fmt=text&start=10 | 200 | d6ff5cc80a57d5237feb5db01a954b23fb5af24b7fccc48a4fb5eb42e27bebfc |
| 2026-11-03T21:38:03Z | https://oeis.org/search?q=1680,3360&fmt=text&start=20 | 200 | 527bafd007a816d8bafb579106ea9c2c41971425132398f8693ad872676f3b59 |

The novelty skeptic made its own fetches of the entry, b-file, history, A214569/A214571/A206487/A215703 and several
value searches at 2026-11-03T22:15:56Z-22:16:08Z (panel/novelty.md).

## Gate re-fetch (one plain curl GET each)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T22:23:33Z | https://oeis.org/search?q=id:A214570&fmt=text | 200 | 01439a4fa1cf899471a8162720f7f6416b55844665b938189a7539645b177991 |
| 2026-11-03T22:23:34Z | https://oeis.org/A214570 | 200 | f01619000f7e1dcca8c97de72b77c2e2406ebb7fac1e749c0822957717805021 |
| 2026-11-03T22:23:34Z | https://oeis.org/A214570/b214570.txt | 200 | 1990f8783a5b76c374ab6f8acc0c1eeb4e635546884e1ec13b255421788ebb64 |
| 2026-11-03T22:23:34Z | https://oeis.org/history?seq=A214570 | 200 | 527993fcec307651759c3c07e41e8e9ad8330a9a2e78108a47009d3ce0e70a67 |
| 2026-11-03T22:23:34Z | https://oeis.org/search?q=1,1,1,2,3,4,6,12,24,40,60,120,240,420,840,1680,3360&fmt=text | 200 | c0ee7a9b9258e37391d0a0cdcde3535a2f34a8bca8dc373dfe5070c0e1b00435 |
| 2026-11-03T22:23:34Z | https://oeis.org/search?q=1680,3360&fmt=text | 200 | b3fbd15cadb8d5ef88043d306ce5358c78676228e65434f4a9919479f131f23c |
| 2026-11-03T22:23:34Z | https://oeis.org/search?q=420,840,1680,3360&fmt=text | 200 | b8d6cad90fa38bfb40b3d809250d11213891bcb2d8fd85aaa5535fd8e26d0a16 |
| 2026-11-03T22:23:34Z | https://oeis.org/search?q=id:A214569&fmt=text | 200 | 5cc11a046f0fa1b9784c9a74d524ac0ccc01e7247a618e11cd7ff503ce024e9f |

Result: entry text (fmt=text) and b-file byte-identical to claim time (DATA ends a(16) = 1680); history still
revisions up to #29, newest approved, no draft (tag-stripped text identical to the pre-claim fetch except the site
footer); "3360" occurs in neither the entry text, the entry page, the b-file nor the history; full-prefix search "No
results." and 1680,3360 search (22 hits, all unrelated) byte-identical to claim time; 420,840,1680,3360: 4 unrelated
hits (A085988, A361937, A363692, A378630); A214569 text byte-identical.

Response headers were not recorded for these fetches. The pages themselves are not shipped (third-party content).
