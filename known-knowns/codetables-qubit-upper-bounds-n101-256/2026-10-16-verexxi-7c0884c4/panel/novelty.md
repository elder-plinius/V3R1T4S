context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty panel: [[183,1]] qubit upper bound 61 -> 59 (claim q183-1)

## Primary table fetch (once, no retry)
- URL: https://codetables.de/QECC.php?q=4&n=183&k=1
- Time (UTC): 2026-10-16T21:06:41Z (after sleep 35), HTTP status 200, no challenge page
- File: novelty_fetch.html
- sha256 (real output of sha256sum): 5dc930c084ce6566ab47d2af41b6f0275a0854c06a1118cc6cde873efc10d2c0
  (identical to the claimant's data/QECC_q4_n183_k1_claimtime.html hash)
- Value on page: "Bounds on [[183,1]]: lower bound 36, upper bound 61". Page notes that for n>100 upper bounds are weak.

## Comparison with known results
- Claimed new bound: d <= 59, i.e. strictly below the live 61 (improvement by 2, not a tie).
- Propagation: check/propagation_check.txt and REPRODUCE.md state the closure of all live cells at (183,1) is 61, so 59 is not implied by R1/R2/R3 on other live cells.
- Re-ran python3 -I check/check_cert.py on result/cert_183_1_60_sh.json: "VERIFIED [[183,1,60]] shadow=True ... max column coefficient <= 0"; also cert_183_1_61_sh.json VERIFIED.
- TROPHY_CASE.md (raw main, 30936 bytes; identical to data/TROPHY_CASE_pinned_9b1d444.md): no entry for quantum / qubit codes / codetables / 183.
- Open pull requests (GitHub API, per_page=100, page 1 returned 77 entries, fewer than 100, so that is the full set; page 2 request was rate limited but not needed): 77 open PRs. The matching ones are #257-#262, #266, #267 for codetables-qubit-upper-bounds-n101-256, covering cells [[132,1]], [[139,1]], [[145,1]], [[150,1]], [[152,1]], [[154,1]], [[158,1]], [[164,1]] only. None touches [[183,1]]. No other PR title/body mentions 183 or this cell. (No file-path listing per PR was fetched; titles/bodies only.)
- Literature (arXiv API, last 24 months, queries on quantum/stabilizer/linear programming/bounds/shadow): no paper found on [[183,1]] bounds. Search was limited to a few keyword queries, so absence is likely but not exhaustively proven. Table itself (live, today) is the authoritative state and shows 61.

## Verdict
Live table upper bound 61; claim gives 59 with a verified exact certificate, not implied by propagation, not in TROPHY_CASE, not in any open PR. Strictly beats known.

pass: true
