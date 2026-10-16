context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty review: [[159,2]] upper bound 53 -> 51

## Single live fetch (no retries)
- URL: https://codetables.de/QECC.php?q=4&n=159&k=2
- UTC time: 2026-10-16T21:05:39Z (after sleep 40)
- HTTP status: 200 (no challenge page; 1523 bytes, real table page)
- File: novelty_fetch.html
- sha256 (real output of sha256sum): bf8570d740bdf2ba0d51826bb553e6604fc381be9067b1b7032690bd16267652
  (identical to the claim-time fetch data/QECC_q4_n159_k2_claimtime.html, so the page did not change)
- Value quoted from page: "Bounds on [[159,2]] ... lower bound: 31 upper bound: 53".
- Page note: "For n>100, the upper bounds on qubit codes are weak (and not necessarily monotone in k)."

## Comparison
- The claim (upper bound at most 51) is strictly below the live 53, by 2. It is not a tie.
- Propagation: check/propagation_check.txt shows neighbours (159,1): [33,53], (160,2): [31,54], (158,3): [31,53]. None gives a value below 53 for (159,2), so the standard propagation rules do not imply 51 from the live table.
- check/check_cert.py was re-run here on result/cert_159_2_52_sh.json and printed "VERIFIED [[159,2,52]] shadow=True" (exact integer arithmetic). The 53 certificate is also VERIFIED per check/checker_output.txt. I did not re-derive the LP independently, only ran the supplied checker.
  A [[159,2,53]] code would also be a [[159,2,52]] code, so ruling out d=52 rules out 53 as well and the new upper bound is 51.

## TROPHY_CASE.md
- data/TROPHY_CASE_pinned_9b1d444.md (a pinned copy, not re-fetched live): zero lines mention quantum, QECC or stabilizer codes, so no prior entry on this cell.

## Open pull requests (github.com/elder-plinius/V3R1T4S/pulls, read-only, pages 1 and 2)
- Sibling claims for the same bank entry exist for other cells: #267 [[164,1]] 55->53, #266 [[158,1]] 53->51, #262 [[154,1]] 52->50, #261 [[152,1]] 51->49, #260 [[150,1]] 51->49, plus #257-#259. None names [[159,2]]. Page 2 (#213-#239) has no codetables PRs.
- Not checked: PR pages 3 and later (older than #213; the codetables PRs are #257 and up) and closed PRs. The gh CLI was not available.

## Literature (last 24 months, arXiv search)
- Seen: arXiv 2502.14165 (quantum Delsarte LP), 2408.10323 (SDP bounds; concrete cases are only ((7,1,4)), ((8,9,3)), ((10,5,4)); no mention of codetables or n>100), 2601.15446 (check-weight-constrained bounds), 2306.00048 (Hamming-like bound). None reports an upper bound for [[159,2]] or a systematic n=101..256 table improvement. The search was not exhaustive.

## Caveats
- The method (Rains LP with shadow) is classical; the novelty is as a table entry only, which is what the success criterion asks for.
- Literature and PR coverage is partial (see above), so a prior private or unlisted result cannot be excluded.

pass: true
