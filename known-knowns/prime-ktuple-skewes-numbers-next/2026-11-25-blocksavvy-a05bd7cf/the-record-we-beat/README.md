# The record we beat (status snapshot; pages themselves not shipped)

| URL | fetched (UTC) | HTTP | sha256 of page as fetched | extracted cell |
|---|---|---|---|---|
| https://oeis.org/A210439 | 2026-11-25T00:47:59Z | 200 | 5688cc08c05c4afbab9b4a037a3755732ade6f913ebc1b571290ef87ec766ddc | a(2..9) = 1369391, 337867, 1172531, 21432401, 251331775687, 7572964186421, 1203255673037261, 3658988336628289781; no (p, p+6) entry |
| https://en.wikipedia.org/wiki/Skewes%27s_number | 2026-11-25T00:47:59Z | 200 | 4b8321af3c3ba7e1d4817c178c0852391fe7a33cab1aade350617dcd32dcba53 | "The Skewes number (if it exists) for sexy primes (p, p+6) is still unknown." (page last edited 28 October 2026) |
| https://oeis.org/search?q=id:A080841&fmt=text | 2026-11-25T00:54:02Z | 200 | 621825e7b284d672005417d19733e93a3886970459999b6e89aae9bec53f8cd6 | a(11) = 448725003, a(12) = 3741217498 (counts by upper member q < 10^n; equal to ours) |
| https://oeis.org/A005597 | 2026-11-25T00:48:00Z | 200 | 5f9dbcbe8e89af90a15e6048cb0c2846093446073bc57a3dfb29b00947bf3934 | C2 = 0.66016181584686957392781211001455577843262336028473... |

The NOVELTY skeptic re-fetched A210439 at 2026-11-25T01:41:55Z (HTTP 200, sha256 15fb06d93f4f7dcb2c3736e766f2baa48e1c031d7bd64711903a379a6d0567e7, page updated since, same terms) and searched OEIS for 349018493647, 349018493981 and 1416008996: no results.
