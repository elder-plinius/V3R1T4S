# Novelty check for the claim: no [[128,5,42]] qubit stabilizer code, so the [[128,5]] upper bound is at most 41
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: CONFIRMED NEW as checked 2026-10-17: the claimed bound 41 is strictly below the live table bound 43 and below the propagation closure 42, and no pull request, trophy-case row or paper at or below 41 was found (arXiv refused, so OpenAlex and web search were used)

Time note: every time below is the PC clock (date -u). GitHub's own created_at stamps show that clock runs behind GitHub's by about 40 seconds or more (PR 317 was already listed by my page-1 fetch stamped 05:59:37Z, yet GitHub records it as created 06:00:18Z).

## 1. Status source, fetched once (no retry)
- URL: https://codetables.de/QECC.php?q=4&n=128&k=5
- Command: curl -s -A "V3R1T4S-verexxi" -o work/cell.html -w '%{http_code}' on that URL; one request, no retry.
- UTC time (PC clock): 2026-10-17T05:59:24Z, read before and after the request (both 05:59:24Z). HTTP status: 200. Size: 1548 bytes.
- sha256 of work/cell.html: 8c721d4d79ff6172421d20ce629c1eee19f20b1f4093e65bd21d06c4d0ad24e7
- Values on the page: heading Bounds on [[128,5]], lower bound 24, upper bound 43, footer Last change: 10.06.2024. The page notes say that for n above 100 the upper bounds on qubit codes are weak (and not necessarily monotone in k).
- The page is byte-identical to the claim-time copy data/QECC_q4_n128_k5_claimtime.html (same sha256, empty diff). CLAIM.md says that copy was fetched 2026-10-17T05:35:11Z with HTTP 200.
- Result: live bounds 24 to 43. The claim (upper bound 41) lowers 43 by 2.

## 2. Propagation: is 41 implied by other live cells?
- I did not fetch the complete qubit table again (the status source was fetched once, per the rule). I used the claimant's saved copy data/qubit_table_full_n1-256.html. Its sha256 is 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, equal to the hash recorded in CLAIM.md. My own live fetch of the one cell (128,5) matches the claimant's copy byte for byte. The other cells are taken on the claimant's word.
- Rules: R1 d(n,k) at most d(n,k-1) for k at least 2; R2 d(n,k) at most d(n+1,k); R3 d(n,k) at most d(n-1,k+1)+1. check/parse_table.py read 33152 cells (n 1 to 256). check/propagate.py gives a closure of 42 at (128,5) (live cell says 43). Witness chain: live (125,7)=39 plus three R3 steps gives (128,4) at most 42, then R1 gives (128,5) at most 42.
- Independent direct formula (minimum over every live cell (n2,k2) with k2 at least 1 of live upper bound + max(0, 128-n2, k2-5)): the minimum is 42, reached by 7 live cells: (124,9)=38+4, (125,7)=39+3, (125,8)=39+3, (126,7)=40+2, (126,8)=39+3, (127,7)=40+2, (128,7)=40+2. Cells implying 41 or lower: 0.
- So the best bound derivable from the live table is 42. The claim (41) beats it by 1.
- Note: the d = 43 certificate alone would give upper bound 42, which only ties the closure. Only the d = 42 certificate (upper bound 41) is a record. The claim is stated for d = 42.

## 3. Pull requests (every page)
Search used: https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit&page=N, plain requests, User-Agent V3R1T4S-verexxi. The HTML is parseable (the list sits in embedded JSON), so the REST API was only a cross-check.
- page=1: 2026-10-17T05:59:37Z, HTTP 200, 347081 bytes, sha256 96f15a2fda763393d0c37a662c5fbb1f56ca338b5e40f854bfdfffeee0de4d64. 25 PRs listed (PR 317 down to PR 272). Header: totalCount 36 (35 open, 1 closed), totalPages 2.
- page=2: 2026-10-17T06:00:19Z, HTTP 200, 300265 bytes, sha256 18f43c5d07bd5b3b59e8c0e1b4020db8cee628cd03e3609256073ffd75d6ea8d. 13 PRs listed (PR 273 down to PR 257); PR 273 and PR 272 repeat from page 1 because two new PRs were opened between my two requests. Header: totalCount 38 (37 open, 1 closed), totalPages 2.
- page=3: 2026-10-17T06:00:27Z, HTTP 200, 240316 bytes, sha256 7b1ac1d214dec25c23874b708366f063ad0c7ee1100a61a476266f2231b434aa. No results array, zero PRs listed, so I stopped there. HTML pages read: 3 (2 with PRs, 1 empty). Distinct PRs seen through HTML: 36 (PR 257 to PR 317).
- Because the total moved from 36 to 38 during the read, I used the REST fallback as a cross-check (2 of the allowed 4 calls): https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100&page=1
  - 2026-10-17T06:00:56Z, HTTP 200, sha256 8fa8406821878dd8e185e45724e1e99985507435043c0479b18f7f4b285558c9: 100 PRs (PR 214 to PR 319); 38 mention codetables-qubit, which is the 36 from HTML plus PR 318 and PR 319 (GitHub created_at 06:00:24Z and 06:00:29Z).
  - 2026-10-17T06:11:00Z, HTTP 200, sha256 194814f44dd3f8b04d18b53017ee1536fcb94aba6e1b8342338f23d70f2fd946: 100 PRs (PR 223 to PR 328); 47 mention codetables-qubit, nine more than before (PR 320 to PR 328, created_at 06:01:47Z to 06:03:05Z). No PR newer than PR 328 existed at that read.
- Total read: 47 distinct PRs (46 open, 1 closed, 0 merged), all authored by the GitHub account verexxi. A regex scan for 128,5 / n=128 / 128_5 over the title and body of all 100 PRs in each REST read found 0 matches (first read) and 0 matches (second read).
- Cells claimed in titles, each with the bound it would imply for [[128,5]] through R1/R2/R3 (new bound + max(0, 128-n2, k2-5)):
```
PR 257 open: [[132,1]] 45 to 43 (implies [[128,5]] at most 43)
PR 258 open: [[139,1]] 47 to 45 (implies [[128,5]] at most 45)
PR 259 open: [[145,1]] 49 to 47 (implies [[128,5]] at most 47)
PR 260 closed: [[150,1]] 51 to 49 (implies [[128,5]] at most 49)
PR 261 open: [[152,1]] 51 to 49 (implies [[128,5]] at most 49)
PR 262 open: [[154,1]] 52 to 50 (implies [[128,5]] at most 50)
PR 266 open: [[158,1]] 53 to 51 (implies [[128,5]] at most 51)
PR 267 open: [[164,1]] 55 to 53 (implies [[128,5]] at most 53)
PR 269 open: [[105,4]] 35 to 34 (implies [[128,5]] at most 57)
PR 270 open: [[133,2]] 45 to 43 (implies [[128,5]] at most 43)
PR 271 open: [[140,2]] 47 to 45 (implies [[128,5]] at most 45)
PR 272 open: [[142,2]] 48 to 46 (implies [[128,5]] at most 46)
PR 273 open: [[146,2]] 49 to 47 (implies [[128,5]] at most 47)
PR 274 open: [[148,2]] 50 to 48 (implies [[128,5]] at most 48)
PR 275 open: [[159,2]] 53 to 51 (implies [[128,5]] at most 51)
PR 276 open: [[165,2]] 55 to 53 (implies [[128,5]] at most 53)
PR 277 open: [[177,1]] 59 to 57 (implies [[128,5]] at most 57)
PR 278 open: [[183,1]] 61 to 59 (implies [[128,5]] at most 59)
PR 279 open: [[200,2]] 67 to 65 (implies [[128,5]] at most 65)
PR 280 open: [[200,5]] 67 to 64 (implies [[128,5]] at most 64)
PR 281 open: [[230,3]] 77 to 74 (implies [[128,5]] at most 74)
PR 282 open: [[230,5]] 77 to 73 (implies [[128,5]] at most 73)
PR 296 open: [[110,2]] 37 to 36 (implies [[128,5]] at most 54)
PR 297 open: [[120,2]] 40 to 39 (implies [[128,5]] at most 47)
PR 298 open: [[122,1]] 41 to 40 (implies [[128,5]] at most 46)
PR 299 open: [[123,2]] 41 to 40 (implies [[128,5]] at most 45)
PR 300 open: [[127,2]] 42 to 41 (implies [[128,5]] at most 42)
PR 301 open: [[129,2]] 43 to 42 (implies [[128,5]] at most 42)
PR 302 open: [[135,1]] 45 to 44 (implies [[128,5]] at most 44)
PR 303 open: [[171,1]] 57 to 55 (implies [[128,5]] at most 55)
PR 304 open: [[207,2]] 69 to 68 (implies [[128,5]] at most 68)
PR 305 open: [[213,2]] 71 to 70 (implies [[128,5]] at most 70)
PR 306 open: [[219,2]] 73 to 72 (implies [[128,5]] at most 72)
PR 307 open: [[225,2]] 75 to 74 (implies [[128,5]] at most 74)
PR 316 open: [[110,5]] 37 to 35 (implies [[128,5]] at most 53)
PR 317 open: [[155,6]] 53 to 49 (implies [[128,5]] at most 50)
PR 318 open: [[161,2]] 55 to 52 (implies [[128,5]] at most 52)
PR 319 open: [[173,2]] 59 to 56 (implies [[128,5]] at most 56)
PR 320 open: [[185,3]] 63 to 60 (implies [[128,5]] at most 60)
PR 321 open: [[200,10]] 67 to 62 (implies [[128,5]] at most 67)
PR 322 open: [[215,6]] 73 to 71 (implies [[128,5]] at most 72)
PR 323 open: [[230,10]] 77 to 72 (implies [[128,5]] at most 77)
PR 324 open: [[115,2]] 39 to 38 (implies [[128,5]] at most 51)
PR 325 open: [[125,4]] 41 to 40 (implies [[128,5]] at most 43)
PR 326 open: [[135,8]] 43 to 42 (implies [[128,5]] at most 45)
PR 327 open: [[165,6]] 53 to 52 (implies [[128,5]] at most 53)
PR 328 open: [[195,2]] 65 to 64 (implies [[128,5]] at most 64)
```
- Is [[128,5]] among the claimed cells: no. Smallest bound any single PR implies for [[128,5]]: 42 (PR 300 [[127,2]] 42 to 41; PR 301 [[129,2]] 43 to 42). Closure at (128,5) after applying all 47 PR claims as overrides to the live table (check/propagate.py with an overrides file): 42.
- So no PR equals [[128,5]] and none implies 41 or lower. The best they give is 42, a tie with the live-table closure and still above 41.

## 4. TROPHY_CASE.md on main and the repository
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md fetched 2026-10-17T06:01:46Z, HTTP 200, 30936 bytes, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9. Main HEAD from git ls-remote in the same command: 7dd4480512cc47fe0f897164844432a2738fe649.
- Identical to the pinned copy data/TROPHY_CASE_pinned_9b1d444.md once carriage returns are stripped (pinned copy: 31036 bytes, sha256 cdfe852481ba85e35ccbc386d64ce88de92a56eb73d1ec3e44cdc9a3b86345ad; 100 lines each; the 100-byte difference is line endings).
- It lists six result families (degree-diameter graphs, constant-weight codes, matrix multiplication, the Lehmer bound, VNN-COMP counterexamples, a RobustBench attack) plus two cipher commitments. A search for codetables, qubit, QECC, quantum, stabilizer, [[ , upper bound and Farkas matches only constant-weight Delsarte LP rows; the number 128 does not appear. There is no quantum-code row.
- Repository tree on main (git/trees API, HTTP 200, 3324 entries, not truncated): no known-knowns folder for qubit codes (only codetables-binary-linear, a different table). The problem file is known-unknowns/physics/codetables-qubit-upper-bounds-n101-256.md (HTTP 200, 5583 bytes, sha256 173e4ae9e4906a622907254fe821f55ebb498592e9c3a8bef32841741aeaad32). It says that since 24 May 2024 codetables.de lists qubit bounds up to n = 256, and it suggests (as a suggestion from spot checks, not a proof) that the full quantum LP with shadow constraints has not been run above n = 100.

## 5. Literature, last 24 months (2024-10 to 2026-10)
- arXiv API (export.arxiv.org): 2 requests, 2026-10-17T06:03:26Z and 06:05:49Z, both answered HTTP 429 (refused). I stopped there and fell back, as the rules allow. This limits coverage and is stated on purpose.
- OpenAlex (api.openalex.org, plain requests, HTTP 200 each, about 06:03Z to 06:07Z): 8 distinct searches (9 requests: the first search was sent twice because my first script run crashed on console encoding after it), seven over 2024-10-01 to 2026-10-17 and one over 2015-01-01 to 2024-09-30. Queries: linear programming bound quantum stabilizer codes minimum distance (1073 hits); upper bounds minimum distance qubit quantum codes table (1319); quantum shadow enumerator weight enumerator bound (439); semidefinite programming bound quantum codes distance (1100); additive quaternary codes GF(4) quantum bounds length 128 (9); upper bound minimum distance qubit stabilizer codes Grassl table improved bounds linear programming (39); quantum weight enumerator linear programming exact arithmetic certificate nonexistence quantum code (6); quantum linear programming bound large length table upper bounds additive quantum codes, n greater than 100 (887, older window).
- Web: WebSearch, 4 queries (3 standard, 1 extended) on [[128,5]], LP/shadow bounds above n = 100, exact rational certificates and codetables.de. WebFetch of the Rains abstract (quant-ph/9611001) and of a 2017 Southampton paper on quantum coding bounds (PDF text unreadable, not assessed). The only n = 128 figure that surfaced was for half-rate codes (distance between 11 and 22), not k = 5. Zenodo records API: 3 queries, only unrelated records. GitHub-wide issue search: 2 queries, one with total_count 0 and one unrelated.
- Closest items found, and why none is a competitor:
  - Angles Munne and Huber, SDP bounds on quantum codes: rational certificates, arXiv 2603.19901 (2026-03-20): improves 18 upper bounds for n-qubit codes with n from 6 to 19. Far from n = 128. (Predecessor by Angles Munne and Nemec, 2024-08-19: title and date only.)
  - Zhang and Chen, arXiv 2606.15558 and 2606.22538 (June 2026): quantum Hamming bound for degenerate codes and for all local dimensions. For [[128,5]] the Hamming bound allows d up to 48 (my computation), so it cannot reach 41. Quantum Singleton allows 62.
  - Wei et al., arXiv 2601.19848 (2026-01-27): LP with generator-weight constraints, exact for n at most 9. Okada, arXiv 2502.14165 (2025-02-20): thesis generalizing the Shor-Laflamme-Rains LP, no tables. Ball et al. (2026): mixed-dimensional MacWilliams and shadow identities. None gives a [[128,5]] bound.
  - de Messieres, Zenodo 10.5281/zenodo.23303034 (2026-10-11): new codes (lower bounds), lengths 17 to 55. An and Yang, Zenodo 10.5281/zenodo.22998465 (2026-09-27): checkable certificates of code parameters, not upper bounds for a parameter set. Hernando, Quintana-Orti and Grassl (2026): minimum-distance computation for given codes.
  - Rains, Quantum shadow enumerators, quant-ph/9611001 (old; abstract read through WebFetch): any code of length n corrects at most floor((n+1)/6) errors. For n = 128 that is 21 errors, so d at most 44, which is above 41.
- Result: no source in the window states an upper bound for [[128,5]] at or below 41. A negative search cannot prove absence; this is what could be reached with the tools available.

## 6. Reasoning
- The strict comparison, claimed 41 against: live table 43; live-table closure 42; best single-PR implication 42; closure with all 47 PRs applied 42; trophy case, nothing; literature, nothing at or below 41. 41 is below every one of them, so it is not a tie.
- The claim package's checker (check/check_cert.py) printed VERIFIED for result/cert_128_5_42_sh.json and for result/cert_128_5_43_sh.json when I ran it once. Correctness belongs to the other reviewers; this is noted only so the novelty question is not vacuous.
- Caveats: (a) the arXiv API refused, so the literature check rests on OpenAlex and web search; (b) the closure uses the claimant's saved table, checked only against its recorded hash and one live cell; (c) the repository is active (the PR list grew from 36 to 38 to 47 during my work), so the PR list must be re-read right before anything is posted; (d) the live table can change.
- Within what could be checked, the result strictly beats everything known.
pass: true
