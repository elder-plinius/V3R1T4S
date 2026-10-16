context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty panel review, claim q200-5 ([[200,5,65]] does not exist)

## Live table fetch (single attempt, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=200&k=5
- Time: 2026-10-16T21:03:27Z (date -u, immediately before/after the request)
- HTTP status: 200 (no challenge page)
- Value quoted from the page: "Bounds on [[200,5]] lower bound: 38 upper bound: 67". Matches CLAIM.md. The page also states that for n>100 the upper bounds are weak.
- The claim lowers 67 to 64 (strictly lower, not a tie).

## Propagation
- check/propagation_check.txt: live (200,5) = [38, 67]; closure of all live cells at (200,5) = 67; neighbours (200,4), (201,5), (199,6) are all [38, 67]. So 64 is not implied by propagating other live cells.

## Certificates
- Re-ran check/check_cert.py (standard library, integer arithmetic): result/cert_200_5_65_sh.json prints "VERIFIED [[200,5,65]] shadow=True ... max column coefficient <= 0"; result/cert_200_5_67_sh.json prints "VERIFIED [[200,5,67]] shadow=True". This is a correctness check only; correctness belongs to another panelist, I only confirm the checker accepts them.

## Open pull requests (elder-plinius/V3R1T4S, read-only, GitHub API list, 77 open)
- Open codetables-qubit-upper-bounds-n101-256 claims cover only [[132,1]], [[139,1]], [[145,1]], [[150,1]], [[152,1]], [[154,1]], [[158,1]], [[164,1]] (PRs 257-262, 266, 267). None mentions [[200,5]]. No duplicate found.

## TROPHY_CASE.md
- data/TROPHY_CASE_pinned_9b1d444.md (pinned copy in the claim folder, 100 lines; I did not re-fetch the live file): no qubit/codetables entry and no [[200,5]] entry.

## Literature (last 24 months)
- arXiv API query (quantum, stabilizer, bound, distance, newest first, 40 results, HTTP 200 after a 301 redirect to https) shows nothing on LP/shadow upper bounds for [[200,5]] or n in 101..256; closest items concern constructions or other topics. Search was keyword-limited, so absence is not proof, but nothing contradicts novelty. The live table (maintained by Grassl) is the authoritative record of the best known bound, and it says 67.

## Verdict
Result strictly improves the live upper bound (67 to 64), is not implied by propagation, and no open PR, trophy entry or found paper already has it.

pass: true
