# Novelty verdict: a(28) of OEIS A028420 (matchings of 28x28 grid)

## Live b-file fetch (one honest fetch, no retries)

- URL: https://oeis.org/A028420/b028420.txt
- fetched: 2026-10-29T07:51:57Z
- HTTP status: 200 (2060 bytes, fetch completed in 0.10s)
- content: 28 rows, n = 0..27, largest index present: 27
- a(28) ABSENT: zero rows at n = 28; last row is n = 27 starting 1024636791282269170268039922912717806990700...
- sha256 af5ce6dc09ce376f103af901dc3706517b8fe9cb92b978335e9f402ab19cf6c6 — byte-identical to the fetch
  recorded in the claim's table_record (2026-10-29T07:33:30Z), and the a(27) baseline matches.

## Sequence page (one fetch)

- https://oeis.org/A028420 (2026-10-29): DATA shows a(0)..a(13); the b-file link credits "Table of n, a(n)
  for n = 0..27" (inner terms 0..21 credited separately). No comment, extension or reference mentions any
  term at n >= 28. Only extension lines on the page are a 2009 link repair and a 2020 a(0) prepend.
  Nothing newer than n = 27 exists on the entry.

## Prior / equal results

- Trophy case (repo TROPHY_CASE.md): grepped for A028420, monomer, dimer, matching, Hosoya, lattice gas —
  no entry for this sequence or problem; the only substring hit is an unrelated degree-diameter graph claim.
- Open PRs (elder-plinius/V3R1T4S, fetched once): 358 open; none mention A028420, A006506, A063443 or
  grid-graph matching counts. PR #818 is a monomer-dimer ENTROPY CONSTANT digit claim (a different
  quantity: digits of the infinite-lattice constant, not an exact finite-grid count) — not a tie. Our
  earlier PR #782 is a different sequence and does not affect this claim.
- Literature (two searches, 2026-10-29): (1) exact-integer tie check on the claimed value's first 30 digits
  503599703482028949174093021835 — zero matches anywhere on the indexed web; (2) search for 2025-2026
  extensions of A028420 / exact 28x28 monomer-dimer counts — nothing; only method papers (state-matrix
  recursion 2019, Pfaffian 2015) with no values at n = 28.

## Tie-check outcome

No prior, equal or simultaneous publication of a(28) of A028420 was found: not in the live b-file, not on
the sequence page, not in the trophy case, not in open PRs, not in the indexed literature. The claimed
value is the first unknown term (N = 28 = largest live index 27 + 1, matching the success criterion) and
is absent from the primary table at verification time. Strictly beats everything known; no tie.

context: zcode Agent-tool subagent, fresh context
pass: true
