# The record we compared against: OEIS A357951

Status source for this cell: https://oeis.org/A357951 (the bank target graph-automata-max-period lists A357951(8)
in its success criterion; its own status_source is the sibling entry https://oeis.org/A384209).

## Extracted cell
| quantity | OEIS value | this package |
|---|---|---|
| A357951(8) | absent: DATA is 2,2,4,6,16,26,66 (n = 1..7, offset 1), %I A357951 #11 Oct 23 2022 13:42:18, keyword nonn,more,hard; history shows revisions up to #11 only; draft page "No pending changes for A357951" | 150 |

## Fetches (one plain curl GET each, no cookies, no retries)
| when (UTC) | by | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|---|
| 2026-11-03T02:36:55Z | run scout | https://oeis.org/search?q=id:A357951&fmt=text | 200 | e8e8bfa7c8a4953334164e23d561e02541c275663e8a984b7640e62d5578b302 |
| 2026-11-03T02:37:42Z | run scout | https://oeis.org/A357951 | 200 | 90c2ecba8d643ffc92e158800a7660386ab9fe9802970171204cd11b30c48029 |
| 2026-11-03T02:37:42Z | run scout | https://oeis.org/draft/A357951 | 200 | 38beaa59d79420b4f9e90a2fd69d36dcbb41d79c75e7e027f97c54e3ea1fb4fa |
| 2026-11-03T02:37:42Z | run scout | https://oeis.org/history?seq=A357951 | 200 | 66a54865594f03bc64741d5a873c8a42ed3c5487f7f3aa2b081b8a97238825f2 |
| 2026-11-03T02:50:41Z | claim-time re-fetch | https://oeis.org/search?q=id:A357951&fmt=text | 200 | e8e8bfa7c8a4953334164e23d561e02541c275663e8a984b7640e62d5578b302 (byte-identical to the scout fetch) |
| 2026-11-03T02:50:41Z | claim-time re-fetch | https://oeis.org/draft/A357951 | 200 | page is dynamic, so its hash differs from the scout fetch; text still "No pending changes for A357951" |
| 2026-11-03T04:15:37Z | novelty skeptic | https://oeis.org/search?q=id:A357951&fmt=text | 200 | e8e8bfa7c8a4953334164e23d561e02541c275663e8a984b7640e62d5578b302 (same bytes; DATA still ends a(7) = 66) |
| 2026-11-03T04:15:37Z | novelty skeptic | https://oeis.org/draft/A357951 | 200 | not recorded; text "No pending changes for A357951." |

The honesty gate (2026-11-03T04:29:37Z) did not re-fetch: the novelty fetch was less than 6 hours old
(panel/gate.md). Selected response headers were not recorded. The pages themselves are not shipped (third-party
content).
