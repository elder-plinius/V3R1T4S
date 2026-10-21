# Novelty skeptic verdict: [[155,6]] upper bound

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I did and real output

1. Single fetch (after sleep 30) of https://codetables.de/QECC.php?q=4&n=155&k=6 with User-Agent V3R1T4S-verexxi, saved as novelty_fetch.html.
   - HTTP status: 200
   - UTC time: 2026-10-17T05:39:55Z
   - sha256: e0ff2386821f97a34869e168505b4c44ad81d206438f980d66468f9660a105e6 (identical to data/QECC_q4_n155_k6_claimtime.html)
   - Page text: "Bounds on [[155,6]] ... lower bound: 29 upper bound: 53", "Last change: 10.06.2024". No challenge page.
   - Live value: upper bound 53. The claim (no [[155,6,50]] code, so upper bound at most 49) strictly lowers it.
2. Propagation (check/propagation_check.txt): live (155,6) = [29, 53]; neighbour (154,7) = [29, 49], so rule R3 gives 50. The closure of the live table at (155,6) is 50. The claimed bound 49 is strictly below what the other live cells imply. R1 and R2 neighbours give 53.
3. Re-ran `python3 -I check/check_cert.py result/cert_155_6_50_sh.json`: "VERIFIED [[155,6,50]] shadow=True: value=1240 digits, max column coefficient <= 0, 49+2+50 multipliers".
4. TROPHY_CASE.md (data/TROPHY_CASE_pinned_9b1d444.md, and the raw file on the main branch fetched via WebFetch): no quantum or qubit entries and no codetables entries. It covers graphs, constant-weight codes, matrix multiplication, totient, VNN-COMP and RobustBench only.
5. Pull requests: one request to https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit (34 results, pages 1 and 2 scanned). The titles are "codetables-qubit-upper-bounds-n101-256: [[n,k]] upper bound lowered ..." for other cells (for example [[110,2]], [[120,2]], [[122,1]] ... [[165,2]]). No title mentions [[155,6]]. git ls-remote of refs/pull/*/head returned 307 refs, with no titles, so it is not informative for this cell.
6. Literature (web search for recent arXiv work on [[155,6]] and LP bounds): no paper found that gives an upper bound at or below 49 for [[155,6]]. The search is not exhaustive. The table itself says its upper bounds for n>100 are weak, and the page was last changed 2024-06-10.

## Reasoning

The live upper bound is 53. The claim gives 49. The closure of other live cells gives 50, so 49 is not implied by propagation. I found no record in the literature, TROPHY_CASE or open pull requests of a bound this low for this exact cell. The certificate verifies on my re-run. I did not check the correctness of the LP formulation beyond running the checker. The result strictly beats everything I could find, and it is not a tie.

pass: true
