# Novelty review, claim q105-4 ([[105,4,35]] nonexistence, target codetables-qubit-upper-bounds-n101-256)

context: subagent (Claude Code headless on the owner's PC, fresh context)

## Primary table fetch (one attempt, no retries)
- URL: https://codetables.de/QECC.php?q=4&n=105&k=4
- Command: curl -s -A "V3R1T4S-verexxi" -o novelty_fetch.html -w '%{http_code}' (after sleep 25)
- Fetched (date -u): 2026-10-16T21:12:28Z
- HTTP status: 200 (not a challenge page; 45415 bytes, normal table content)
- sha256 (novelty_fetch.html): 93d5fd17b2cb6c3e8fd97bf84154faa5b88c0922c31d7ea4a21ddf75e4e079b0
- Value quoted from the page: "Bounds on [[105,4]] ... lower bound: 21 upper bound: 35"
- Same hash as the claimant's fetch of 2026-10-16T21:02:04Z, so the live upper bound is still 35. The claim (no [[105,4,35]], so the bound is at most 34) would strictly lower it by 1.

## Open pull requests (one API call)
- https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=1 returned HTTP 200 and 78 open PRs (fewer than 100, so this is the whole list). Saved as pulls.json.
- Eight PRs carry the target id (#257, #258, #259, #260, #261, #262, #266, #267). They cover [[132,1]], [[139,1]], [[145,1]], [[150,1]], [[152,1]], [[154,1]], [[158,1]], [[164,1]]. All are k=1 cells. None mentions (n,k)=(105,4) or [[105,4,...]] in title or body (regex search of titles and bodies).
- No tie and no prior claim for this cell.

## TROPHY_CASE.md
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md returned HTTP 200 (30936 bytes, saved as trophy.md). It has no entry for codetables, QECC, qubit bounds or [[105,4]].

## Literature, last 24 months (arXiv API query results, abstracts only)
Closest papers and the n range each covers:
- arXiv 2603.19901 (2026-03): SDP bounds on quantum codes with rational certificates; n = 6 to 19.
- arXiv 2601.19848 (2026-01): LP on quantum weight enumerators with generator-weight constraints; exact for n <= 9, plus a 127-qubit architecture case.
- arXiv 2601.15446 (2026-01): check-weight-constrained code bounds, rate vs distance, "tens or hundreds" of qubits, with no specific n=105, k=4 result in the abstract.
- arXiv 2604.16023 (2026-04): group-equivariant SDP/MacWilliams for intrinsic and permutation-invariant codes; small dimensions.
- arXiv 2311.07111 (2023-11): SDP for entanglement-assisted codeword-stabilized codes; not qubit stabilizer tables.
- arXiv 2608.06304 (2026-08): interpretation of the shadow enumerator by time reversal; not a bound table.
- arXiv 2306.00048 (2023-05): Hamming-like bound for degenerate codes, distance 3 regime.
- None of these treats qubit stabilizer cells in 101 <= n <= 256 or [[105,4]]. The codetables page itself states that its upper bounds for n <= 100 come from Rains' MAGMA program, and the live entry for n=105 remains 35.

## Assessment
- Nothing found (live table, open PRs, trophy case, recent arXiv) ties or beats upper bound 34 for [[105,4]]. The claim would be a strict improvement over the live value 35.
- Limits: the literature search was an abstract-level arXiv search only, and not every paper's tables were read. Whether the propagation rules already imply 34 from other live cells is addressed by the claimant's check/propagation_check.txt and was not re-derived here; the live page for this cell shows 35, which is consistent with no propagated bound existing.

pass: true
