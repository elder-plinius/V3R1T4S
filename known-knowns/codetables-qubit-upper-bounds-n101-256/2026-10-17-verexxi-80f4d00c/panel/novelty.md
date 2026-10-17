context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty skeptic verdict for [[200,10]] (claim: no [[200,10,63]], upper bound 67 -> 62)

## What I ran and real output

1. Read CLAIM.md and REPRODUCE.md in the claim folder. The claim lowers the upper bound of [[200,10]] from 67 to at most 62 via an LP/shadow Farkas certificate. The claim states the propagation closure from other live cells is 63.

2. Single live fetch (in the folder, after sleep 10):
   curl -s -A "V3R1T4S-verexxi" -o novelty_fetch.html -w '%{http_code}' https://codetables.de/QECC.php?q=4&n=200&k=10
   - URL: https://codetables.de/QECC.php?q=4&n=200&k=10
   - HTTP status: 200
   - UTC time (date -u): Sat Oct 17 05:38:58 UTC 2026
   - sha256 (novelty_fetch.html): 4e64d7790b52b60bebfc7662ee57891a4e46cfe968b6696bd1feaf3a7cf5de56
   - Page content: "Bounds on [[200,10]]  lower bound: 37  upper bound: 67"; page footer "Last change: 10.06.2024". Not a challenge page. The hash is identical to the claim-time fetch recorded in CLAIM.md, so the live value is unchanged: upper bound 67.

3. TROPHY_CASE.md (raw file from the repository's main branch, HTTP 200, 89 lines): grep for qubit, codetables, quantum and [[200 returned nothing. No entry for this cell. (The pinned copy in data/TROPHY_CASE_pinned_9b1d444.md was not needed for this.)

4. Pull requests: git ls-remote refs/pull/*/head listed 307 refs (up to #99+ and beyond; used only for counting). The web page https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit (pages 1 and 2) lists the open "[claim] codetables-qubit-upper-bounds-n101-256: [[n,k]] ..." draft PRs, all for other cells (e.g. [[105,4]], [[110,2]], [[164,1]], and so on). Searching both pages for "[[200,10]]" gave 0 matches. No open PR for this exact cell.

5. Literature (web search, last 24 months, queries on LP/shadow bounds for qubit stabilizer codes at n=200, k=10): found only general LP-bound papers and unrelated recent work (for example Monte Carlo distance upper-bound estimation, check-weight-constrained codes). No result gives an upper bound below 67 for [[200,10]], and none disproves the [[200,10,63]] parameters. Caveat: the search is not exhaustive and the table notes say upper bounds for n>100 are weak.

## Reasoning

- Live value is 67. The claim is 62, strictly below the live value, and strictly below the 63 that propagation from other live cells gives (per the claim's own propagation check; I did not re-run it, that is another skeptic's job).
- Nothing in the TROPHY_CASE, open PRs or recent literature that I could find already reaches 62 or lower for this cell, so the result is not a tie.
- I did not evaluate the certificate's correctness (outside my role).
- Residual risk: the literature search is limited to what the search tool surfaced.

pass: true
