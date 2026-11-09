# The record we compared against: OEIS A357952

Status source for this cell: https://oeis.org/A357952 (the bank target graph-automata-max-period lists A357952(9)
in its success criterion; its own status_source is the sibling entry https://oeis.org/A384209).

## Extracted cell
| quantity | OEIS value | this package |
|---|---|---|
| A357952(9) | absent: DATA is 2,2,4,6,8,18,42,112 (n = 1..8, offset 1), %I A357952 #12 Oct 23 2022, keyword nonn,more,hard; b-file synthesized from the entry, ends at a(8); draft page "No pending changes for A357952" | 200 |

## Fetches (one plain curl GET each, no cookies, no retries)
| when (UTC) | by | URL | HTTP | sha256 of the bytes received |
|---|---|---|---|---|
| 2026-11-02T21:05:02Z | run scout | https://oeis.org/search?q=id:A357952&fmt=text | 200 | 760308c0b91d85ea8aa5ba802ed5fd374f0d1fef38c7d56b023ff5892d94bb9b |
| 2026-11-02T21:05:02Z | run scout | https://oeis.org/A357952 | 200 | 3b4695ba6e587eae680c6c4c74836e3e2ebbde84cd0dde8fe527700212150b2a |
| 2026-11-02T21:05:02Z | run scout | https://oeis.org/A357952/b357952.txt | 200 | 4a2d446453bff516c3abc164fbb389d044fb23b420fcf58718a80009520259c0 |
| 2026-11-02T21:05:03Z | run scout | https://oeis.org/history?seq=A357952 | 200 | 70cf624474a72734d095c5e3869a9e40832fe783cbe74238534e157e54d7e634 |
| 2026-11-02T21:35:11Z | claim-time re-fetch | https://oeis.org/search?q=id:A357952&fmt=text | 200 | 760308c0b91d85ea8aa5ba802ed5fd374f0d1fef38c7d56b023ff5892d94bb9b (byte-identical to the scout fetch) |
| 2026-11-02T21:35:11Z | claim-time re-fetch | https://oeis.org/draft/A357952 | 200 | fe32b51ab7ae5f7812c741b3aff4c9474ece6bccfbd7ac26eaa1a8b9f59bee53 |
| 2026-11-02T21:50:44Z | novelty skeptic | https://oeis.org/search?q=id:A357952&fmt=text | 200 | 760308c0b91d85ea8aa5ba802ed5fd374f0d1fef38c7d56b023ff5892d94bb9b (same bytes; "200" absent from the entry) |

The honesty gate (2026-11-02T21:56:04Z) did not re-fetch: the novelty fetch was less than 6 hours old
(panel/gate.md). Selected response headers were not recorded. The pages themselves are not shipped (third-party
content).
