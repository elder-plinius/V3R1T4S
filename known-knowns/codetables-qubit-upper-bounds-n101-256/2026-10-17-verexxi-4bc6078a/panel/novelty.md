# Novelty panel: [[110,5]] qubit upper bound claim (35 vs live 37)

context: subagent (Claude Code headless on the owner's PC, fresh context)

## What I did and real output

1. Read CLAIM.md and REPRODUCE.md. Claim: no [[110,5,36]] stabilizer code exists, so upper bound <= 35; live bound said to be 37.
2. Primary table fetch, exactly once (after sleep 120), in the folder:
   curl -s -A "V3R1T4S-verexxi" -o novelty_fetch.html -w '%{http_code}' "https://codetables.de/QECC.php?q=4&n=110&k=5"
   - URL: https://codetables.de/QECC.php?q=4&n=110&k=5
   - HTTP status: 200
   - UTC time: 2026-10-17T05:45:50Z (before) / 2026-10-17T05:45:51Z (after)
   - sha256 of novelty_fetch.html: 22454f4e6b49c2cdb38e5734342607b33a49b92c6c638dd802e6b45fc071767c (identical to the claim-time file in the claim package)
   - Value on page: "Bounds on [[110,5]]  lower bound: 23  upper bound: 37". Not a challenge page (49157 bytes, normal table page).
3. Propagation: check/propagation_check.txt reports closure of the live table at (110,5) = 36, neighbours (110,4)=37, (111,5)=37, (109,6)=37. So 35 is not implied by live cells.
4. TROPHY_CASE.md (raw file from github.com/elder-plinius/V3R1T4S main, saved as tc.md, 30936 bytes): grep for "110" and "qubit" found no entry for any qubit cell, nothing for [[110,5]] (the only "110" hit is an unrelated constant-weight-code row).
5. Open pull requests: one request to https://github.com/elder-plinius/V3R1T4S/pulls?q=is%3Apr+codetables-qubit (HTTP 200), plus pages 2 and 3 of the same listing (page 3 empty). 34 claim PRs for codetables-qubit-upper-bounds-n101-256 in total (saved as prs.txt, prs2.txt). Cells claimed include [[110,2]] 37->36, [[105,4]] 35->34, [[200,5]] 67->64, [[230,5]] 77->73, and others at k=1,2. None for [[110,5]], and none for [[109..111, k]] other than [[110,2]]. Consequence of [[110,2]]=36: by d(n,k) <= d(n,k-1) this gives only d(110,5) <= 36, which is weaker than the claimed 35. So the PR set does not preempt 35. (The PRs are by the same effort; they are not prior art that ties the claim.)
6. Literature (last 24 months): web search on arXiv for LP/shadow-enumerator bounds for qubit codes; looked at arXiv 2601.15446 (check-weight-constrained codes, LP bounds) via fetch: no bound stated for [[110,5]] or n in 101-256 tables. Other hits (2402.06481 Monte Carlo/BP distance bound, 2601.19848 low-weight codes, 2502.09514 CV MacWilliams) concern different settings. Nothing found that gives d <= 35 for [[110,5]]. Caveat: search is not exhaustive.

## Reasoning

Live value 37 (fetched just now, unchanged from the claim-time page by hash). The claimed bound 35 is strictly below 37, below the table-closure value 36, below anything the open PRs imply (36 via [[110,2]]), and I found no trophy-case or literature entry equal to or better than it. The claim therefore strictly beats everything known to me. Validity of the certificate itself is outside this novelty role; this verdict is on novelty only.

pass: true
