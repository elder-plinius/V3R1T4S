# Novelty skeptic panel file, cell [[129,2]] (qubit)

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I ran
1. Live table, exactly once, after sleep 20, inside the claim folder:
   curl -s -A "V3R1T4S-verexxi" -o novelty_cell_page.html -w '%{http_code}' "https://codetables.de/QECC.php?q=4&n=129&k=2"
   - URL: https://codetables.de/QECC.php?q=4&n=129&k=2
   - UTC time: 2026-10-17T00:42:14Z (request started), finished 2026-10-17T00:42:15Z
   - HTTP status: 200 (no challenge page; the page contains the normal bounds table)
   - sha256 of novelty_cell_page.html: 19c28eb589e7dc3562d188b951a584ff23a27b333e04fe8b07ae03a9f901e551
   - Value seen: "upper bound: 43" (lower bound 25 per the page; same hash as the claimant's own saved page, data/QECC_q4_n129_k2_claimtime.html).
2. Open and closed pull requests, one request:
   curl -s -A "V3R1T4S-verexxi" -o pulls.html "https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit"
   HTTP 200, 325452 bytes, sha256 953762832162a1bbd79cf33cb245d51ea38180c7876811659c09946aa5a01fe7, no "next page" link found.
   Every [[n,k]] cell found in the saved file: [[105,4]], [[132,1]], [[133,2]], [[139,1]], [[140,2]], [[142,2]], [[145,1]], [[146,2]], [[148,2]], [[150,1]], [[152,1]], [[154,1]], [[158,1]], [[159,2]], [[164,1]], [[165,2]], [[177,1]], [[183,1]], [[200,2]], [[200,5]], [[230,3]], [[230,5]].
   [[129,2]] is not among them.
3. TROPHY_CASE.md: curl of the raw file from github.com/elder-plinius/V3R1T4S (main), HTTP 200, 30936 bytes, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9. grep for "129" and for "q=4&n=129" found nothing, so no recorded entry for this cell.
4. Literature: one web search (arXiv-oriented) for nonexistence of [[129,2,43]] / LP bounds. Results (SDP bounds on quantum codes 2408.10323, LP bounds for EAQECC 1602.00413, etc.) mention no [[129,2,43]] result and no improvement of this cell. I found nothing in the last 24 months that already lowers the [[129,2]] upper bound to 42.

## Reasoning
- The live primary table gives upper bound 43 for [[129,2]], fetched honestly with HTTP 200. The claim is upper bound 42 (nonexistence of d = 43), which is strictly below the live value, not a tie.
- No open or closed PR for this exact cell, no TROPHY_CASE.md entry, and no literature hit contradict novelty.
- The claim package's propagation check states the closure of other live cells at (129,2) is 43, so 42 is not implied by neighbouring cells. I did not re-run it (outside my scope as the novelty skeptic; correctness of the certificate belongs to the other skeptics).
- Limits: the literature check was a single search engine query, not an exhaustive arXiv sweep; I note that residual risk, but found no evidence of prior art.

pass: true
