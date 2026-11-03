# Novelty skeptic: A357953(10) = 624

context: subagent (executor Task)
Inputs read: claim copy only (claim.md, table_record.md, VALUE.txt, data/). REPORT.md, WATCH_STATUS, attempts/ and other runs were not read.
Fetches: one plain GET per page, User-Agent "V3R1T4S-novelty-skeptic/1.0 (+https://github.com/elder-plinius/V3R1T4S)", no retries. Times are UTC (06:54 EST = 11:54Z).

## Live status (fetched now, by this skeptic)
| URL | time (UTC) | HTTP | what it says |
|---|---|---|---|
| https://oeis.org/search?q=id:A357953&fmt=text (cell, https://oeis.org/A357953) | 2026-11-03T11:54:38Z | 200 | `%I A357953 #13 Oct 24 2022 14:14:10`; `%S A357953 1,2,2,6,7,18,38,96` (n=1..8). No a(9), no a(10). sha256 prefix e217d9de2d829e26, same bytes as the claim's data/A357953_claimtime.txt |
| https://oeis.org/search?q=id:A384209&fmt=text (family status_source, https://oeis.org/A384209) | 2026-11-03T11:54:38Z | 200 | `%I A384209 #8 May 22 2025`; `%S 1,1,1,1,2,4,8,14,27` (Game of Life sequence, a different sequence; it says nothing about A357953) |
| https://oeis.org/draft/A357953 | 2026-11-03T11:54:39Z | 200 | "No pending changes for A357953" |
| https://oeis.org/search?q=2,6,7,18,38,96&fmt=text | 2026-11-03T11:54:39Z | 200 | 1 hit, A357953 only (no duplicate or extended sequence anywhere) |
| https://oeis.org/search?q=1,2,2,6,7,18,38,96,180&fmt=text | 2026-11-03T11:54:39Z | 200 | "No results." (nobody has published a(9)=180 on OEIS) |
| https://oeis.org/search?q=38,96,180,624&fmt=text | 2026-11-03T11:54:47Z | 200 | "No results." |

Best known value for this cell: none. a(10) is absent everywhere I checked. The last published term is a(8) = 96. a(9) = 180 shows up only in the contributor's own unsubmitted work (claim.md), not in any public source. Even if it counted, a(9) is a different cell.

## Repo: elder-plinius/V3R1T4S
- GitHub search issues/PRs "A357953 repo:elder-plinius/V3R1T4S" (api.github.com, 2026-11-03T11:54:48Z, HTTP 200): total_count 1, #904 (open, draft) "[claim] graph-automata-max-period: A384209(10) = 46". I read the #904 body through the GitHub connector (get_pull_request). Its "Not claimed" section says: "A384209(11) and the related sequences A357951, A357952 and A357953 are not claimed." It mentions A357953 only in its credits. No conflict.
- Search "graph-automata-max-period repo:elder-plinius/V3R1T4S" (11:54:48Z, HTTP 200): 4 hits (#904, #859, #699, #534). None is about A357953. Connector search for PRs (open and closed) with "totalistic": 0 hits.
- Live TROPHY_CASE.md (raw.githubusercontent.com main, 11:54:55Z, HTTP 200): 0 matches for A357953/totalistic.
- Live known-knowns/ listing (api.github.com contents, 11:54:55Z, HTTP 200): 27 entries. None is about graph automata, totalistic CA or A357953. The local clone (../../../repo, HEAD f3b19b47 2026-10-30) also gives 0 grep hits in TROPHY_CASE.md, known-knowns/ and news/.
- Two later GETs (api issues/904 and code search) got HTTP 403 from the rate limit. I did not retry them. #904 is covered by the connector read above. Code search was not done, but the issue/PR search and the TROPHY_CASE/known-knowns checks above cover the same ground.

## Literature and code, last 24 months
Two web searches, run 2026-11-03 ("A357953 maximum period totalistic cellular automaton connected graph 10 nodes"; "totalistic cellular automaton graph maximum period von Brömssen 2025 OR 2026"). They return only the OEIS entries A357951/2/3 (2022, DATA unchanged), the OEIS wiki page for Pontus von Brömssen, and Wolfram NKS (which covers cyclic 1D CA, not this). I found no paper, preprint or code with a term of A357953 beyond n = 8.

## Sanity check on the witness (not a reproduce review)
My own ~15-line Python decoder of graph6 `I?AAD@oIg` gives 10 nodes and 11 edges. Rule: ON next step iff the count of ON neighbours (node itself not counted) is in {0,2}; start 2. Result: preperiod 0, cycle length 624. This matches VALUE.txt. 624 is below the trivial bound 2^10 = 1024. The claim that 624 is the maximum (exhaustive search) belongs to the reproduce skeptic, not this review.

## Verdict
The cell A357953(10) has no known value: OEIS DATA stops at a(8) = 96, there are no draft changes, no other OEIS sequence holds these terms, and no repo PR/issue, trophy or known-known covers it. The claimed 624 is therefore strictly new for this cell. It is not a tie. The status is readable and unchanged from the claim-time snapshot (same sha256). This is a new exact term, provided the exhaustiveness holds (judged by the other panelists).
Caveat: if the package also cites a(9) = 180, that term is likewise absent from OEIS (searched above). This verdict covers only a(10).

pass: true
