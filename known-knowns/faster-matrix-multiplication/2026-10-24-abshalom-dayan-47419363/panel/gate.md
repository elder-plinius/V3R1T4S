# Honesty gate (run's main session)

claim: the scheme in claim/object/ is an exact rank-3424 bilinear scheme over Q for <18,19,19> (partial win p1).

status: CONFIRMED_PARTIAL
confirmed_scope: The files in object/ define a bilinear scheme over Q for <18,19,19> (A 18x19 times B 19x19) with 3424 rank-one terms, each with three nonzero factors, satisfying all 42224004 Brent equations in exact arithmetic, and 3424 is strictly below the rank 3633 for (18,19,19) in the live fmm_sota.json and the rank 3816 on the live Lille page 18x19x19.html (both fetched for the claim at 2026-10-24T17:37:57Z and re-fetched unchanged at 2026-10-24T18:18:21Z) and below the 3633 of the only listed Lille construction Proj([[19, 0], [0]], <19x19x19:3633>) (index fetched 2026-10-24T15:58:56Z), so it meets partial win p1 of fmm-catalogue-small-format-rank and not the main criterion.

What the gate read:
- self_break.md (step 5, fresh subagent, claude-opus-5-5): verdict SURVIVES. Two own exact checkers, 42,224,004 Brent
  equations, 0 wrong; byte-identical rebuild from LITA's 19x19x19 rank-3633 scheme; lowest value in any saved source
  3595 (matmulcatalog); table-access audit clean.
- panel/reproduce.md (fresh subagent, claude-sonnet-5-5): pass: true. Own checker from the definition, all
  42,224,004 equations exact, 0 wrong; six negative controls fail; shipped checker output identical to REPRODUCE.md;
  rebuild run twice, SAME both times.
- panel/novelty.md (fresh subagent, claude-opus-5-5): pass: true. Live fetches at 18:05:46-47Z, all HTTP 200 and
  byte-identical to the claim-time fetches: Lille index 3633 (construction Proj of <19x19x19:3633>), per-format page
  3816, fmm_sota.json 3633. matmulcatalog 3595 is the lowest public value; no format containing <18,19,19> is listed
  at or below 3424; best block split 3697; all 32 pull requests for the target (open and closed) and a search for
  18x19x19 (0 hits) show nothing for this cell; TROPHY_CASE and known-knowns stop at 15x16x16; literature from
  2024-10 to 2026-10 has no such rank.
- panel/criterion.md (fresh subagent, claude-opus-5-5): pass: true. Every p1 clause holds literally; re-fetched
  fmm_sota.json and the per-format page at 18:18:21Z (unchanged); the composition clause excludes only listed
  constructions or listed values, and 3424 is neither; the main criterion is not claimed.

Downgrade checks: no hedging verdict (the panelists' caveats are the usual limits of a web search and of the
construction column's fetch time, both covered by NOVELTY's 18:05:46Z index fetch); no reproduction mismatch; 3424 is
strictly below every live table value (3633, 3816) and every other known value (3595); no stretched criterion or
hidden quantifier found; the scope sentence is exactly what was reproduced; no sample presented as complete (all
equations checked); no capped search used as an exclusion; no probable prime used as a proof (CRT and mod-p checks by
the panel were backed by an exact integer check in the shipped checker and the self-break); table access honest; one
object, one cell. The panel's table fetches (18:05Z, 18:18Z) are under 6 hours old.

Not adopted, noted: upstream commit 1ebdef4 (fetched 18:00Z, not merged) adds kit/POLICY.md with FMM rules; under
its rules 1-4 this claim still stands (no equal or better value public before today, none in the comparators).

Round 1 of this run (<16,16,17> rank 2392, status NOTHING, a tie with closed pull request #44) is kept intact in
rounds/r1-16x16x17/.
