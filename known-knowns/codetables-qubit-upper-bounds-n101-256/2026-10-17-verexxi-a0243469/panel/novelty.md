# Novelty skeptic verdict: [[173,2]] upper bound 59 -> 56

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I did
1. Read CLAIM.md and REPRODUCE.md. Claim: no [[173,2,57]] qubit stabilizer code, so upper bound <= 56 (live table says 59).
2. Fetched the status page once, no retries, as instructed (sleep 80; curl -s -A "V3R1T4S-verexxi" -o novelty_fetch.html -w '%{http_code}'):
   - URL: https://codetables.de/QECC.php?q=4&n=173&k=2
   - HTTP status: 200
   - UTC time: 2026-10-17T05:43:02Z
   - sha256 of novelty_fetch.html: 19e8a7b675dd86211a013ee68b646d28f4710b3c694d39490baa9bc02069a02f (1523 bytes; identical to the claim-time capture)
   - Page text: "Bounds on [[173,2]]  lower bound: 34  upper bound: 59" (page footer: Last change 10.06.2024). Not a challenge page.
3. Pinned TROPHY_CASE (data/TROPHY_CASE_pinned_9b1d444.md): grep for 173 matches only unrelated constant-weight-code rows. The raw TROPHY_CASE.md on the main branch of the V3R1T4S repo lists only non-quantum families (degree-diameter, constant-weight, matrix multiplication, Lehmer, VNN-COMP, RobustBench). No qubit entry for [[173,2]].
4. Pull requests: fetched the web search page https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit (pages 1 and 2, the full result list, 2 pages) and git ls-remote on refs/pull/*/head (307 refs). The PR titles list codetables-qubit claims for [[225,2]], [[219,2]], [[213,2]], [[207,2]], [[177,1]], [[171,1]], [[164,1]], [[158,1]], [[154,1]], [[152,1]], [[150,1]], [[145,1]], [[139,1]], [[135,1]], [[132,1]], [[129,2]], [[127,2]], [[123,2]], [[122,1]], [[105,4]] and others. None is for [[173,2]] (string "173,2" occurs 0 times on both pages). None of them is a neighbour that would imply a bound at (173,2) via the propagation rules (nearest are k=1 cells and k=2 cells at n>=207 or n<=129).
5. Literature search (web search, recent 24 months): found SDP bounds on quantum codes (arXiv 2408.10323), puncturing stabilizer codes (2410.17754), low-weight quantum codes (2601.19848) and others. Nothing I found claims a nonexistence result or upper bound for [[173,2]], or a table-wide improvement for n>100 at k=2. The search is not exhaustive, but turned up no prior or competing result.
6. Propagation: check/propagation_check.txt reports live (173,2) = [34, 59], closure of live table = 58, neighbours R1 (173,1) [34,59], R2 (174,2)-equivalent [34,59], R3 (172,3) [33,58]. So 56 is not implied by other live cells (the best implied bound is 58, and the claimed 56 is strictly below it). I also ran python3 -I check/check_cert.py result/cert_173_2_57_sh.json; output: "VERIFIED [[173,2,57]] shadow=True: value=1415 digits, max column coefficient <= 0, 56+2+56 multipliers". (Certificate soundness is for the other skeptics; I only note it runs.)

## Reasoning
- Live upper bound is 59 (fetched now, same bytes as at claim time). The claim, 56 (no d=57), is strictly lower than 59 and also strictly lower than the propagation closure 58, so it is not a tie and not implied.
- No TROPHY_CASE entry, no open PR for this exact cell, and no literature found that already gives <= 56.
- Caveat noted: the success criterion literally says "proof for d equal to the live upper bound (59)"; the package supplies a derived d=59 certificate as well, and the d=57 certificate gives a stronger bound. This is a soundness/format matter for the other skeptics, not a novelty problem. Novelty-wise the result strictly beats everything known that I could find.

pass: true
