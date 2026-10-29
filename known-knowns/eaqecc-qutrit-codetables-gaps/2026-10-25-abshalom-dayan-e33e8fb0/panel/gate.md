# Honesty gate (main session), run folder 2026-10-25-0856

status: CONFIRMED_SOLUTION
confirmed_scope: The 28 x 50 GF(3) matrix S in claim/object/eaqecc_25_5_12_8.json (sha256 e33e8fb04dc70d4d703e033310b6efafb1825109a93d649ecef183451ee09ec3), with 28 independent rows and rank(S J S^T) = 16, is a non-catalytic [[25,5,12;8]]_3 EAQECC whose exact distance 12 (no nonzero vector of span(S)^perp of symplectic weight <= 11 over all 4457400 11-position sets, and explicit weight-12 vectors of span(S)^perp outside span(S)) is strictly above the d_lower 11 and at most the d_upper 18 of the listed cell [[25,5,11-18;8]]_3 of https://eaqecc.codetables.de/qutrit.php as fetched at 2026-10-25T10:14:24Z (HTTP 200, sha256 37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c) and is not reached at (25,5,8) by the page's six propagation rules applied to its listed non-teleportation cells (which give 11).

Claim: [[25,5,12;8]]_3, full success criterion of target eaqecc-qutrit-codetables-gaps at the listed cell (25,5,8)
(listed [[25,5,11-18;8]]_3), object claim/object/eaqecc_25_5_12_8.json (sha256
e33e8fb04dc70d4d703e033310b6efafb1825109a93d649ecef183451ee09ec3): the extended one-point Hermitian code E_13 on
y^3 + y = x^4 over GF(9) with the three affine points of the line x = 0 deleted and 13 columns times w, a
[25,11,12]_9 code with Hermitian hull 6.

Claim folder unchanged since the panel started: every file's sha256 equals panel/claim.sha256 (26 of 26 files OK,
checked at the gate, 2026-10-25T10:28:18Z). Self-break (self_break/verdict.md, main session): SURVIVES.

Panel files read in full by the main session (each skeptic a fresh subagent, claude-opus-5-5, given only its own
copy of claim/, run one after another, never in parallel; NOVELTY started 09:34:12Z, REPRODUCE 09:59:58Z, CRITERION
10:13:48Z; verdict files written 09:57:43Z, 10:12:53Z, 10:26:39Z UTC by file time). An earlier panel attempt of the
previous session was cut off at 09:30Z before any verdict; its work folders are kept as panel/aborted-0930-*.
- reproduce.md: own checker written before reading the author's code; s = 28, rank(S J S^T) = 16, c = 8, k = 5;
  span(S)^perp, span(S) and the isotropic part are closed under w, so span(S)^perp = phi(C) for a [25,11]_9 code C.
  Two exact methods over the whole space: enumeration of all 3922632451 projective words of C (no word below
  weight 12; 1204 weight-12 classes, 12 inside the isotropic part, 1192 outside; MacWilliams transform integral and
  nonnegative) and a GF(3) subset rank test over all 4457400 11-sets (0) and 5200300 12-sets (1192, the same
  supports). Tested on 240 random brute-force cases and two seeded negatives (both caught). Author's REPRODUCE.md
  steps 1-6 run in a copy: every printed value matches; reruns byte-identical. No-search proof re-derived, with
  d(E_13) = 15 computed exactly. Step 7 (network) left to the other skeptics. pass: true.
- novelty.md: one honest GET 2026-10-25T09:35:47Z, HTTP 200, sha256 37bbf731..., byte-identical to the claim's copy.
  Best known value at (25,5,c <= 8) is 11, over the listed non-teleportation cells and 73 extra codes (open PR
  bodies, merged PR #331, known-knowns, the author's unfiled codes, arXiv:2607.02170, arXiv:2105.02166) under the
  page's rules applied generously up to n = 40; PR #363's k = 1 extension reaches 12 only through impure codes.
  Routes through teleportation cells shown unsound (they would give [[5,1,6;4]], impossible). Literature read:
  arXiv:2607.02170, 2105.02166, 2501.04921, 2206.09782, codetables [25,11]_9 (12-13), [25,12]_9 (11-12),
  [25,8]_3. Not read: the PR file lists (GitHub API 403, rate limit) and three journal papers. pass: true.
- criterion.md: own exact code from S (s = 28, c = 8, k = 5; exhaustive subset test over all 4457400 11-sets, no
  nonzero vector of span(S)^perp at weight <= 11; explicit weight-12 vectors outside span(S)); own GET
  2026-10-25T10:14:24Z, HTTP 200, byte-identical; (25,5,8) is a listed cell, 11 < 12 <= 18; the page's six rules
  over its listed non-teleportation cells give 11 there (also with the 24 extra codes named in CLAIM.md); only
  increasing dimension or length reduction applied to teleportation cells reach 12, and exactly those rules put
  626 and 143 listed cells above their own d_upper. Non-catalytic; c = 8 >= 1. pass: true.

Table fetch age: the newest panel fetch (CRITERION, 10:14:24Z) is under an hour old at the gate, so no further fetch
is required (rule: re-fetch only if older than 6 hours).

Downgrade checks (none triggered): no hedging panelist (each states a bounded residual risk and a definite
verdict); no reproduction mismatch (methods A and B, bz64, the formalist's no-search proof, the self-break's
column-dependence test and the two skeptics' own exact computations all give d = 12, with 1204 weight-12 supports
and 1192 outside the isotropic part); 12 is strictly above the live d_lower 11 and at most d_upper 18; no stretched
criterion or hidden quantifier; scope no wider than reproduced; no sample presented as complete (every search is
exhaustive); no capped search used as an exclusion; no probable prime; the table read only by honest single GETs.
One object, one cell.

The NOVELTY skeptic's unread PR file lists are covered by this folder's already-settled closure, which seeded the
225 code strings that folder 2026-10-25-0810's NOVELTY skeptic extracted from all 14 open PRs' bodies and files at
about 08:25Z (attempts/already-settled/out/novelty0810_pr_codes_notele.txt, 208 seeds after teleportation cells were
dropped), and still gives 11 at (25,5,8); the GitHub search result at 09:35:14Z was byte-identical to the one at
08:57Z, so no PR for this target changed in between.

Caveats carried into the package and report, not downgrades:
- Teleportation reading: if the page's "using teleportation" cells were fed to its increasing-dimension or
  length-reduction rules, [[25,4,12;4]] or [[28,5,12;5]] would give 12 at (25,5,8). The page never does this, and
  doing it contradicts the page's own upper bounds at hundreds of cells (CRITERION) and gives an impossible
  [[5,1,6;4]] (NOVELTY).
- Catalytic reading: with the page's catalytic remark ([[n,k,d;c]] -> [[n,k-1,d;c-1]]) the page's cells would give
  12 at (25,5,8); the page and the bank exclude the catalytic setting, and this code is non-catalytic.
- The classical [25,11]_9 parameters are codetables.de's (12-13, a shortened Hermitian AG code); what is new is a
  [25,11,12]_9 code with Hermitian hull 6. Optimality not claimed (d_upper 18).
- Literature: three journal papers (Cao-Li-Zhu, IEEE TIT 2025; Li-Li-Guan-Song, IJTP 2024; arXiv:2512.17128 in full)
  were not read; arXiv:2607.02170 compares against them and its qutrit codes from them have n <= 16 or large c.
Not part of this claim: cells that follow by the table's rules (for example [[26,5,12;8]] by lengthening).
