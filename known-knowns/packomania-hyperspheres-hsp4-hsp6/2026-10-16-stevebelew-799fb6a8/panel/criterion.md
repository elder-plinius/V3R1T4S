# CRITERION verdict for claim N79 (d=4, N=79)

context: subagent (Claude Code Agent tool, fresh context for this one claim)

Method: read CLAIM.md, REPRODUCE.md, hsp4-79-candidate.txt, hsp4-79-posted.txt, hsp4_radius_as_fetched.txt. Did NOT run the REPRODUCE.md script; wrote an independent checker (strict parser: candidate must be one comment line then exactly 4 numeric tokens per line; posted file must be a radius line then 79 lines of index plus 4 coords with contiguous indices 1..79) and ran it with the project venv python, -I, mpmath mp.dps = 50. Default stance: fail unless confirmed.

## Clause 1: object is N=79 centres in R^4, N listed in radius.txt

Output:
    candidate raw line count: 80 ; comment lines: 1 ; blank lines: 0
    candidate N = 79
    posted N = 79 ; indices 1..79 contiguous: True ; posted header radius = 0.256468324828
    table rows: 299 ; N values unique: True ; first/last N: 2 300
    table rows for N=79: [['79', '0.256468324828']]
Every candidate line has exactly 4 coordinate tokens (asserted). N=79 is a listed row, the row is unique, and the value carries exactly 12 decimals (asserted). Neighbouring rows 78 = 0.256958022526 and 80 = 0.255463163131 bracket the candidate r*, so the N label is not mismatched with a neighbouring cell. Verdict: met.

## Clause 2: container convention (unit ball centred at origin, radius 1) and r* computed exactly as the clause says, no tolerance, 50 digits

Output:
    CANDIDATE: half-min-dist = 0.2565657831346274069640324  1-maxnorm = 0.256565783134456313275697  maxnorm = 0.74343421686554368672
    CANDIDATE r* (50 dps)  = 0.256565783134456313275696976757
    CANDIDATE r* 15 sig    = 0.256565783134456
    all candidate centres satisfy |c| at most 1 - r*: True
    binding constraint: wall
r* = min(min over pairs i,j of|c_i-c_j|/2, 1-max_i|c_i|) evaluated directly from the 17-digit coordinates in hsp4-79-candidate.txt, no tolerance, container radius 1 centred at the origin. The wall term binds (1-maxnorm is smaller than half the minimum pair distance by about 1.7e-13), so the feasible radius is 0.256565783134456 (15 sig). Every centre lies within 1 - r* of the origin, so all 79 balls of radius r* are inside the unit ball and pairwise non-overlapping. The candidate's header value r_float=0.25656578313445633 matches an independent float64 evaluation exactly (float64 r* = 0.2565657831344563, match: True), so the mpmath number is not a rounding artefact of the header. Parser sanity on the posted file: POSTED r* = 0.256468324826589348918066102502, |r*posted - table| = 1.4107e-12 (the posted coordinates carry only 12 decimals), which confirms the posted file and the table row describe the same packing and the reader is correct. Verdict: met.

## Clause 3: strictly greater than the 12-decimal table value by at least 1e-10

Output:
    TABLE value            = 0.256468324828
    GAIN r*cand - table    = 9.74583064563133e-5
    gain at least 1e-10 (exact mpf compare): True
    strictly greater: True
    gain / 1e-10 = 974583.06
Gain stated to 15 significant digits: 9.74583064563133e-5, about 9.7e5 times the required 1e-10 margin and far beyond any 12-decimal rounding effect. CLAIM.md's "about 9.75e-05" is consistent. Verdict: met, against the snapshot hsp4_radius_as_fetched.txt (the live re-fetch is the NOVELTY skeptic's job; see "Not verified here").

## Clause 4: not isometric to the posted hsp4-79.txt configuration (sorted pairwise-distance multisets differ by more than 1e-8 somewhere)

Output:
    pair count: 3081 3081 (expect 3081)
    max |sorted-dist diff| = 0.01576311991 ; count of diffs above 1e-8: 3081
    min pair distance cand/posted: 0.513131566269255 0.512936649653858
    max |sorted-norm diff| = 0.00650049093
The sorted multiset of the 3081 pairwise distances is invariant under every isometry of R^4; all 3081 entries differ by more than 1e-8 (max 1.58e-2), and already the minimum pair distance differs by 1.9e-4. The sorted norm multiset (invariant under origin-fixing isometries, which are the only ones that preserve the container) also differs by up to 6.5e-3. Verdict: met; the candidate is not an isometric copy of the posted packing.

## Clause 5: (d, N) not in a History-of-updates entry on the live hsp4.html newer than the scout's fetch

As recorded in CLAIM.md and REPRODUCE.md: expected "Last update: 06-Jul-2025"; the table snapshot fetched 2026-10-16 16:29:32 UTC was byte-identical to the 2026-10-14 fetches. No file in the claim folder contains the live hsp4.html, so I cannot verify this clause from the folder. Not counted as failed; the pass below depends on the NOVELTY skeptic's live re-fetch confirming no newer N=79 history entry.

## Clause 6: QUEUE RULE (N=79 not inside any hsp4 range on pending-requests.html at verification time)

As recorded in CLAIM.md: no hsp4 entry on the pending page at 2026-10-16 16:29:32 UTC. Mandatory caveat, stated here as the criterion requires: the 26-Sep-2026 "Moki & Julio *many* 4666 candidates" bundle is category-unspecified and cannot be resolved; N=79 must be re-checked against the live table once that bundle disappears from the pending list. Not verifiable from the folder; depends on the NOVELTY skeptic's live re-fetch.

## Hidden quantifiers, stretched definitions, null model

- Rounding artefact: excluded; the gain is 9.7e-5, the table carries 12 decimals, and the binding wall term is computed at 50 digits from the raw coordinates.
- Wrong container radius: excluded; container radius 1 is used both in the r* formula (1 - maxnorm) and in the explicit per-centre check |c| at most 1 - r*, and the posted packing re-derives to the table value under the same convention.
- Mislabelled N: excluded; 79 coordinate lines, 79 posted lines, and the candidate r* lies strictly between the table's N=78 and N=80 values.
- More than one cell: the claim is for the single cell (d=4, N=79); the note about N in (68, 69, 74, 75, 76) concerns other cells and is not relied on here. Only one cell is being claimed and only one is confirmed.
- Partial-win language: none invoked; the claim is judged against the full criterion.
- Null model: not needed and I agree with the brief; this is an explicit, deterministic object evaluated by a deterministic checker, and the question is whether the number exceeds a fixed threshold, not whether it is unlikely under chance.
- Submission: none is claimed or required (criterion says no email is ever made).

## Not verified here

Clauses 5 and 6 (live hsp4.html history, live pending-requests page) and the "re-fetched live immediately before claiming" part of clause 3 rest on the records in CLAIM.md and on the NOVELTY skeptic's live re-fetch. Everything computable from the files in the claim folder was recomputed independently and holds.

confirmed_scope: In d=4 with N=79, the 79 centres in hsp4-79-candidate.txt lie in the unit ball centred at the origin with feasible radius r* = 0.256565783134456 (mpmath 50 digits, no tolerance), exceeding the snapshot table value 0.256468324828 by 9.74583064563133e-5 and not isometric to the posted hsp4-79 packing, conditional on the live history and queue checks recorded in CLAIM.md.

pass: true
