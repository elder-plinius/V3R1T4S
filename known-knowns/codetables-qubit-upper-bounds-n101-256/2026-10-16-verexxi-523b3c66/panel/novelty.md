context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty skeptic report, claim q142-2 ([[142,2,47]] does not exist)

## Status source (fetched once, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=142&k=2
- UTC time: 2026-10-16T21:04:41Z (start; finished 21:04:42Z), after `sleep 10`
- HTTP status: 200 (no challenge page; 82512 bytes, saved as novelty_fetch.html)
- sha256 (real output of sha256sum novelty_fetch.html): 66fef426d41383cc48140ebb8e49076880723af92cfff17e91bbc09f682bde8d
- Value on page: "Bounds on [[142,2]]  lower bound: 30  upper bound: 48"
- This hash is identical to the claim-time fetch recorded in CLAIM.md (data/QECC_q4_n142_k2_claimtime.html), so the live table is unchanged at 48.

## Propagation (check/propagation_check.txt, re-read)
- Cell (142,2): [30, 48]; closure 48.
- Neighbours: (142,1) [30,48]; (143,2) [30,49]; (141,3) [27,47], giving d(142,2) <= 47+1 = 48.
- No standard propagation rule gives anything below 48, so the claimed bound 46 is not implied by the live table.
- check/checker_output.txt reports VERIFIED for cert_142_2_47_sh.json (shadow=True) and cert_142_2_48_sh.json. I did not independently re-run the checker (novelty role only).

## Open pull requests of elder-plinius/V3R1T4S (read-only)
- Open claims for the same target: [[132,1]] 45->43, [[139,1]] 47->45, [[145,1]] 49->47, [[150,1]] 51->49, [[152,1]] 51->49, [[154,1]] 52->50, [[158,1]] 53->51, [[164,1]] 55->53 (PRs 257-262, 266, 267).
- None concerns [[142,2]]. Caveat: if the [[145,1]] claim were accepted, d(142,2) <= d(142,1) <= d(145,1) <= 47, which still does not reach 46. So the claim would strictly beat that as well.

## TROPHY_CASE.md (main branch)
- No mention of qubit/quantum stabilizer codes or codetables; nothing on [[142,2]].

## Literature, last 24 months
- One web search round plus arXiv-related results: found only general LP/shadow-enumerator work (small n, entanglement-assisted, SDP, XYZ and LDPC codes) and no result giving a bound below 48 for [[142,2]] or a table update. Search coverage is limited (search engine, not an exhaustive arXiv scan), so this is absence of evidence only.

## Verdict
- Claimed new upper bound 46 (no code with d=47) is strictly below the live table value 48, not implied by propagation, and not found in pending PRs, TROPHY_CASE.md or the literature I could reach. Correctness of the certificate is for the other panel roles.

pass: true
