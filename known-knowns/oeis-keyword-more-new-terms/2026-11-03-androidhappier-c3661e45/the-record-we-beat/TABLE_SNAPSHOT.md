# The record we compared against: OEIS A131449

Status source for this cell: https://oeis.org/A131449 (bank target oeis-keyword-more-new-terms, status_source
https://oeis.org/search?q=keyword:more).

## Extracted cell
| quantity | OEIS value | this package |
|---|---|---|
| T(6,2), flattened index 66 (second entry of row 6) | absent: DATA ends ...,4,4,3,3,2,1,720 (indices 0..65, offset 0,3; rows 0..5 and T(6,1) = 720), %K nonn,more,tabf, %I #12 Aug 29 2019; b-file (synthesized from the entry) ends "65 720"; history newest revision #12 (N. J. A. Sloane, Aug 29 2019, approved), no pending draft; Lang's linked file "First 6 rows" stops at row 5; contextual value searches of the row-6 head: No results | 360 (row 6, 132 entries non-increasing: 720,360,360,360,360,360,240,240,240,240,180,...) |

## Claim-time fetches (one plain curl GET each, User-Agent naming V3R1T4S research, no cookies, no retries)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T21:53:15Z | https://oeis.org/A131449/a131449.txt | 200 | e41257bf7e708b217e4938ff83ddae931873ba716f020110921cdcef6b020f7a |
| 2026-11-03T21:53:52Z | https://oeis.org/A131449 | 200 | 26d712285cc1f57eef977f2ef108da58a6d92577ea73df398d5a85587c8e5675 |
| 2026-11-03T21:53:52Z | https://oeis.org/A131449/b131449.txt | 200 | cabf2cc627ebbd35c4f5386667d07eb726c901567cd173782f04737509e66d49 |
| 2026-11-03T21:53:52Z | https://oeis.org/history?seq=A131449 | 200 | 0e2258d6d8d3bb6ff218b4de1620d1115bc9f053e37527c773ca759d4235349d |
| 2026-11-03T21:53:52Z | https://oeis.org/search?q=id:A131449&fmt=text | 200 | a528ccf340058109f060ce2c4638e4ca6f60519a85c1a6a2d3123bec7e20d363 |
| 2026-11-03T21:54:51Z | https://oeis.org/search?q=2,1,720,360,360,360,360,360,240&fmt=text | 200 | d362dac2fe6b90660c7ad981d47ba7d36e29acd7894c077eaba44ecc95ea5647 |
| 2026-11-03T21:54:52Z | https://oeis.org/search?q=720,360,360,360,360,360,240,240,240,240,180&fmt=text | 200 | b55e1092fe2856e19ec3ce2e91cb9655169a94ef8c4e3727c9da797aaccee316 |
| 2026-11-03T21:54:53Z | https://oeis.org/A131449 | 200 | 6871202072e5bbc808287069ef786a368ae71baa845e1c692eb4f74ccdd7c9d8 |
| 2026-11-03T21:54:53Z | https://oeis.org/A131449/b131449.txt | 200 | cabf2cc627ebbd35c4f5386667d07eb726c901567cd173782f04737509e66d49 |
| 2026-11-03T21:54:53Z | https://oeis.org/history?seq=A131449 | 200 | a2acbf6f05f3ea9eb3944e48659b6934deb6920184085094ab10b264b44fdd58 |

The novelty skeptic made its own fetches of the entry, b-file, history, Lang's files and five value searches at about
2026-11-03T21:58Z (panel/novelty.md).

## Gate re-fetch (one plain curl GET each)
| when (UTC) | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|
| 2026-11-03T22:01:20Z | https://oeis.org/search?q=id:A131449&fmt=text | 200 | a528ccf340058109f060ce2c4638e4ca6f60519a85c1a6a2d3123bec7e20d363 |
| 2026-11-03T22:01:21Z | https://oeis.org/A131449 | 200 | ea4dd988d3b042b00f9a699cccaa16af729d9a6c2d4572d28b13b3cf428c55d1 |
| 2026-11-03T22:01:21Z | https://oeis.org/A131449/b131449.txt | 200 | cabf2cc627ebbd35c4f5386667d07eb726c901567cd173782f04737509e66d49 |
| 2026-11-03T22:01:21Z | https://oeis.org/history?seq=A131449 | 200 | a5b3897615982772f0c19a892322c18bd07fa35eae103a84a70734a931e21e49 |
| 2026-11-03T22:01:21Z | https://oeis.org/search?q=2,1,720,360,360,360,360,360,240&fmt=text | 200 | d362dac2fe6b90660c7ad981d47ba7d36e29acd7894c077eaba44ecc95ea5647 |
| 2026-11-03T22:01:21Z | https://oeis.org/search?q=720,360,360,360,360,360,240,240,240,240,180&fmt=text | 200 | b55e1092fe2856e19ec3ce2e91cb9655169a94ef8c4e3727c9da797aaccee316 |
| 2026-11-03T22:01:21Z | https://oeis.org/search?q=720,360,360,360,360,360,240&fmt=text | 200 | 281b37e113451b930dbe71e4de46fba0113b7327c1646cc783e35740b600f44c |

Result: entry text (fmt=text) byte-identical to claim time (%I #12 Aug 29 2019, %K nonn,more,tabf, %O 0,3, DATA ends
at index 65 = 720); b-file byte-identical (ends "65 720"); history still revisions #1-#12, newest approved, no draft
(tag-stripped text identical to the pre-claim fetch; the HTML bytes vary between fetches); "360" occurs in neither
the entry text, the entry page nor the history; all value searches "No results.", the two repeated ones byte-identical
to claim time.

Response headers were not recorded for these fetches. The pages themselves are not shipped (third-party content).
