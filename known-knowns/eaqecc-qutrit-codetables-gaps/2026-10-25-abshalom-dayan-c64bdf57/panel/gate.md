# Honesty gate (main session), run folder 2026-10-25-0948

status: CONFIRMED_SOLUTION
confirmed_scope: The GF(3) stabilizer matrix S in claim/object/eaqecc_23_4_12_9.json defines a non-catalytic EAQECC [[23,4,12;9]]_3 (s = 28, rank(SJS^T) = 18, exact minimum distance 12 by full enumeration of span(S)^perp), which exceeds the d_lower 11 and is within the d_upper 18 of the listed cell [[23,4,11-18;9]]_3 on https://eaqecc.codetables.de/qutrit.php as fetched 2026-10-25T13:58:02Z (sha256 37bbf731...936c), and is not obtained by the page's propagation rules applied to its non-teleportation cells.

Claim: [[23,4,12;9]]_3, full success criterion of target eaqecc-qutrit-codetables-gaps at the listed cell (23,4,9)
(listed [[23,4,11-18;9]]_3), object claim/object/eaqecc_23_4_12_9.json (sha256
c64bdf57a5280892b8d4e085ea565c865d5584de5198baa9763cb516318f06f4).

Claim folder unchanged since it was frozen (panel/claim.sha256, 10:55:04Z): every file's sha256 matches (28 of 28
files OK, checked at the gate, 2026-10-25T14:04:18Z). Self-break (self_break/verdict.md, from the run): SURVIVES.

How the panel was run: the run ended before its panel ran. The supervising session ran the run's three skeptics
as fresh subagents (claude-opus-5-5), each given only its own copy
of claim/ (panel/work-*/claim/), one after another, never in parallel. Verdict files written 11:26:24Z (REPRODUCE),
11:36:16Z (NOVELTY), 14:03:58Z (CRITERION) UTC by file time; the CRITERION skeptic was held back between 11:50Z and
13:58Z by a usage pause and then run unchanged.

- reproduce.md: own checker written before reading the author's code; exhaustive enumeration of all 3^18 - 1 =
  387420488 nonzero vectors of span(S)^perp: s = 28, c = 9, k = 4, d = 12; author's REPRODUCE.md steps 1-7 match;
  no-search proof premises re-derived, including d(E_11) = 17. pass: true.
- novelty.md: one GET of the live table 2026-10-25T11:27:14Z; (23,4,9) reads [[23,4,11-18;9]]; the page's six rules
  seeded with every listed non-teleportation cell plus 328 extra codes (open PRs for this target, closed #331, the
  files of PR #739, literature tables) give 11 there; the only routes to 12 or more at c <= 9 seed teleportation
  cells, which are invalid sources. pass: true.
- criterion.md: own exact code from S (s = 28, rank 18, c = 9, k = 4; full enumeration, d = 12; 8 isotropic and 2608
  non-isotropic weight-12 vectors); own GET 2026-10-25T13:58:02Z, HTTP 200, byte-identical (sha256 37bbf731...);
  11 < 12 <= 18; the page's six rules over its non-teleportation cells give 11; the one route to 12 starts from the
  teleportation cell (23,3,3) and is rejected (it breaks 626 of the page's own upper bounds). pass: true.

Disclosures to carry into the package and the pull request description:
- The panel was run by the supervising session after the run ended, with a pause before CRITERION, as above.
- The teleportation-cell point, with the correct reason (their isotropic part is Z-only, so the rules that need pure
  codes do not apply to them; propagating them breaks the page's own upper bounds).
- NOVELTY ran at 11:27Z, before draft PR #758 ([[24,4,13;10]]_3, same contributor, same construction family) was filed
  at 13:06Z; whether #758's code reaches (23,4,c <= 9) by the page's rules is to be checked before filing
  and stated in the PR.

Verdict: CONFIRMED_SOLUTION. Gate written 2026-10-25T14:04Z.
