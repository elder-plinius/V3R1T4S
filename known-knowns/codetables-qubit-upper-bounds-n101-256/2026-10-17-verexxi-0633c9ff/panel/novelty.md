# Novelty skeptic verdict: [[110,2]] qubit upper bound 37 -> 36

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I ran
- Live table fetch (once, no retry): sleep 8; curl -s -A "V3R1T4S-verexxi" -o novelty_cell_page.html -w '%{http_code}' "https://codetables.de/QECC.php?q=4&n=110&k=2"
  - URL: https://codetables.de/QECC.php?q=4&n=110&k=2
  - HTTP status: 200
  - UTC time (date -u): Sat Oct 17 00:33:58 UTC 2026
  - sha256 of novelty_cell_page.html: 9366ddf82bcfd8cba8025060d03f553dd6a312f0bd3dd6a767cf6349119c2034 (identical to the claim-time file data/QECC_q4_n110_k2_claimtime.html)
  - Value on page: "Bounds on [[110,2]]  lower bound: 24  upper bound: 37". Not a challenge page (50569 bytes, real content).
- TROPHY_CASE.md: read data/TROPHY_CASE_pinned_9b1d444.md and the live raw TROPHY_CASE.md of the V3R1T4S repo (HTTP 200, saved as tc_live.md). Neither has any qubit/codetables entry or a [[110,2]] entry (the only "110" match is an unrelated constant-weight-code row).
- Open pull requests: one request to https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit (HTTP 200, saved as pulls.html). It lists PRs for these cells only: [[105,4]], [[132,1]], [[133,2]], [[139,1]], [[140,2]], [[142,2]], [[145,1]], [[146,2]], [[148,2]], [[150,1]], [[152,1]], [[154,1]], [[158,1]], [[159,2]], [[164,1]], [[165,2]], [[177,1]], [[183,1]], [[200,2]], [[200,5]], [[230,3]], [[230,5]]. No PR for [[110,2]]. None of those cells feeds (110,2) by the propagation rules R1 (110,1), R2 (111,2), R3 (109,3), so none implies a bound of 36 there.
- Literature (one web search of recent arXiv, shadow-enumerator LP bounds for qubit codes): nothing found that gives d <= 36 for [[110,2]]. The hits were general LP/shadow-enumerator papers and distance-finding papers, none tabulating this cell.
- Claim-package checks (read only): check/checker_output.txt reports "VERIFIED [[110,2,37]] shadow=True"; check/propagation_check.txt reports closure of the live table at (110,2) = 37, with neighbours R1 [25,37], R2 [25,37], R3 [23,37]. So 36 is not implied by other live cells.

## Reasoning
The live upper bound is 37. The claim shows no [[110,2,37]] exists, giving at most 36, which is strictly below 37. It is below the literature I could find, absent from TROPHY_CASE.md (pinned and live), not implied by propagation from the live table, and not claimed by any open PR for this exact cell. This is a strict improvement, not a tie. Limits: the literature check was one search plus the table, so it is not exhaustive. Correctness of the certificate is for the other skeptics. This verdict covers novelty only.

pass: true
