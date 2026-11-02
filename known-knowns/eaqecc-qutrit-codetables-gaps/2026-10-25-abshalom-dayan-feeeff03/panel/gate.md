# Honesty gate (main session), run folder 2026-10-25-0931

status: CONFIRMED_SOLUTION
confirmed_scope: The 30 x 48 GF(3) stabilizer matrix S in claim/object/eaqecc_24_4_13_10.json (sha256 feeeff03749ecfd57a5b84b8778a2ffe2111723da17f31a3f197d02d048c1794) has s = 30 independent rows and rank(S J S^T) = 20, so c = 10 and k = 4, and an exhaustive enumeration of all 3^18 - 1 nonzero vectors of span(S)^perp gives exactly 13 as the minimum symplectic weight outside span(S) ∩ span(S)^perp, so it is a non-catalytic EAQECC [[24,4,13;10]]_3 whose d = 13 is strictly greater than d_lower 12 and at most d_upper 19 of the listed cell [[24,4,12-19;10]]_3 of https://eaqecc.codetables.de/qutrit.php as re-fetched 2026-10-25T11:22:04Z (sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c), a value the page's six propagation rules applied to its listed non-teleportation cells do not reach (they give 12 there).

Claim: [[24,4,13;10]]_3, full success criterion of target eaqecc-qutrit-codetables-gaps at the listed cell (24,4,10)
(listed [[24,4,12-19;10]]_3), object claim/object/eaqecc_24_4_13_10.json (sha256
feeeff03749ecfd57a5b84b8778a2ffe2111723da17f31a3f197d02d048c1794).

Claim folder unchanged since it was frozen (panel/claim.sha256, 09:47:24Z): every file's sha256 matches (28 of 28
files OK, checked at the gate, 2026-10-25T11:30:55Z). Self-break (self_break/verdict.md, from the run): SURVIVES.

How the panel was run: the run ended at 10:43:58Z before its panel finished (its background skeptics were stopped by
the headless background-wait limit); its one unfinished NOVELTY attempt is kept as
panel/attempt1-novelty-stopped-at-run-end and was not used. The supervising session then ran the run's three skeptics
as fresh subagents (claude-opus-5-5), each given only its own copy
of claim/ (panel/work-*/claim/), one after another, never in parallel. Verdict files written 11:04:12Z (REPRODUCE),
11:21:08Z (NOVELTY), 11:30:16Z (CRITERION) UTC by file time. The NOVELTY and CRITERION skeptics both checked draft PR #739
([[25,5,12;8]]_3, same contributor, filed at 11:02Z) and whether the page's teleportation cells are valid sources for
its propagation rules.

- reproduce.md: own checker written before reading the author's code; s = 30, rank(S J S^T) = 20, c = 10, k = 4;
  span(S)^perp of dimension 18, isotropic part of dimension 10. Exhaustive enumeration of all 3^18 - 1 = 387420488
  nonzero vectors of span(S)^perp: minimum weight 13, 5000 weight-13 vectors, none in the isotropic part (two
  independent membership tests). Tested on 150 random brute-force cases and three corrupted versions of S (all
  caught); reruns byte-identical. Author's REPRODUCE.md steps 1-7 run in a copy: every printed value matches. No-search
  proof premises re-derived; d(E_11) = 17 computed exactly. Step 8 (network) left to the other skeptics. pass: true.
- novelty.md: one GET of https://eaqecc.codetables.de/qutrit.php 2026-10-25T11:05:08Z, HTTP 200, sha256 37bbf731...,
  byte-identical to the claim's copy; (24,4,10) reads [[24,4,12-19;10]]. The page's rules with their purity side
  conditions, seeded with the listed non-teleportation cells plus every code named in the 15 open V3R1T4S PRs for
  this target (including #739), the merged [[14,3,8;5]], arXiv:2607.02170 Tables V and VII and the arXiv:2105.02166
  Hermitian family, give 12 at this cell. Teleportation seeds shown unsound (they break the page's own upper bounds).
  Closest: a hypothetical hull-8 variant of C_13 would tie; PR #363's k = 1 rule reaches 14 only through impure
  codes. Not read: journal-only papers beyond 2607.02170's comparison columns; PR file lists other than #739's.
  pass: true.
- criterion.md: own exact code from S (s = 30, c = 10, k = 4; exhaustive enumeration, d = 13; the code is pure);
  own GET 2026-10-25T11:22:04Z, HTTP 200, byte-identical; (24,4,10) is a listed cell, 12 < 13 <= 19; the page's six
  rules over its 3764 listed non-teleportation cells give 12 there. Teleportation cells, if propagated, would give 13
  here (for example from [[24,3,13;3]]), but propagating them pushes 2700 listed cells above their own upper bounds and
  the page itself does not do it. Non-catalytic; c = 10 >= 1. pass: true.

Disclosures to carry into the package and the pull request description:
- CLAIM.md says no open PR title or body names a code of length 23, 24 or 25; since 11:02Z, draft PR #739 names
  [[25,5,12;8]]_3 and its derived codes. None reaches past 12 at (24,4,c <= 10) (NOVELTY and CRITERION, independently).
- The teleportation-cell point above, with the correct reason (their isotropic part is Z-only, so the rules that need
  pure codes do not apply to them).
- The panel was run by the supervising session after the run ended, as described above.

Verdict: CONFIRMED_SOLUTION. Gate written 2026-10-25T11:31Z.
