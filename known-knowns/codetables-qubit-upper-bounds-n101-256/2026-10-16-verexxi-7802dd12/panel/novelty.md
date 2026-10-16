context: subagent (Claude Code headless on the owner's PC, fresh context)

# Novelty review, claim q230-5: no [[230,5,74]] qubit stabilizer code (upper bound 77 -> at most 73)

## Primary table (one fetch, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=230&k=5
- Fetched 2026-10-16T20:59:33Z (end 20:59:34Z), HTTP 200, no challenge page.
- sha256: not available. I piped the response straight into a text filter and did not save the body, so I have no sha256 of exactly what I fetched, and I did not re-fetch. (The claim folder's own copy, data/QECC_q4_n230_k5_claimtime.html, is the claimant's fetch, not mine.)
- Value: "Bounds on [[230,5]]  lower bound: 44, upper bound: 77". Page also states for n>100 the upper bounds are weak and not necessarily monotone in k.
- This matches the claim's own record (data/QECC_q4_n230_k5_claimtime.html, 20:56:42Z, upper bound 77). The table did not change in between.

## Propagation (are 73 or 74 implied by other live cells?)
- check/propagation_check.txt: live (230,5) = [44, 77]; neighbours (230,4) 77, (231,5) 77, (229,6) 77 (+1 rule gives 77 at best 78). Closure at (230,5) = 77, so a bound of 73 is not implied by the stated propagation rules.

## Literature, last 24 months (arXiv API, read-only; queries on quantum code + linear programming + bound, and "quantum weight enumerator", sorted by date)
- Nothing found that bounds the distance of [[230,5]] or any n>100 qubit cell by LP/shadow methods. Closest hits (Quantizing Delsarte Theory, 2026-10-07; Quantum Hamming Bound in Arbitrary Local Dimension; Degeneracy Cannot Violate the Quantum Hamming Bound; MacWilliams-identity papers for qudit/mixed-dimension/CV codes; Stabilizer codes over general phase spaces) are general theory, not a [[230,5]] bound. I did not read their full text, so a table of improved bounds inside one of them cannot be fully ruled out, but the live table (which would incorporate such results) still says 77.

## Repo state
- data/TROPHY_CASE_pinned_9b1d444.md (100 lines): no qubit-code or [[230,5]] entry.
- Open pull requests (GitHub API, read-only): qubit upper-bound claims exist only for cells [[132,1]], [[139,1]], [[145,1]], [[150,1]], [[152,1]], [[154,1]], [[158,1]], [[164,1]] (PRs 257-262, 266, 267). None touches [[230,5]]; these are different cells (k=1) and do not imply a bound on (230,5) through the propagation rules (the k=1 rows do not feed (230,5) via d(n,k)<=d(n,k-1) in the downward direction needed).
- No open PR for [[230,5]] found.

## Verdict
The claimed bound (<= 73, certificate also given for 77 = the live bound) strictly improves the live table value 77 by 4, is not implied by propagation from live cells, and I found no prior or competing record in the literature window, the trophy case or open PRs. Caveats: the literature check is a title-level API search, not exhaustive; correctness of the certificate is for the other panelists.

pass: true
