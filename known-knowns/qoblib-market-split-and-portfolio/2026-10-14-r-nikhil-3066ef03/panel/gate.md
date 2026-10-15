# Honesty gate (kit/RUN.md step 7), run 2026-10-14-1518, lane C

Written by the run's main session after reading all three panel files in full: `reproduce.md`, `novelty.md`,
`criterion.md`. Each was written by a fresh subagent that saw only its own copy of `claim/` (plus, for NOVELTY, the
web and this repo's TROPHY_CASE.md). Each has a `context:` line and ends with `pass: true`.

## Downgrade checks

- Hedging panelist: none. REPRODUCE and CRITERION state caveats precisely and still pass:
  - the exact value depends on the tie rule for 25 coefficients round(5/2) at t = 0. The class states the rule (round
    half away from zero, `claim/definition/06-portfolio-check-README.md`), and both posted bar values reproduce only
    under it; the claim stays strictly below the bar under half-to-even and float rules too;
  - B = 50 for a200 rested on the parameter file and both PRs. The gate settled it: the class's own generator
    `06-portfolio/models/binary_quadratic_programming/gen_archive.sh` (fetched once, 2026-10-14T22:20:45Z, HTTP 200,
    sha256 0d491d354a7fc59921430be086d0d7b4c74f6df5509bd1a57d08af2941ecf85b) maps `200) B=50`.
- Reproduction mismatch: none. REPRODUCE's own checker, CRITERION's own evaluator, the claimant's `pf_eval.py` and the
  claimant's literal ZIMPL evaluator all give −691624, feasible, with identical breakdowns.
- Strictly better than the live bar: yes. −691624 < −551385 (PR #87), by 140239. Not a tie.
- Live table: re-read by the gate once each, 2026-10-14T22:20:58Z, HTTP 200. The official table is byte-identical
  (sha256 05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a, ETag
  "b8d113952e45aebb91be82ab051a193b5f7c92736b83c957b3470b0de433681e"; no a200 row). The open-PR list (sha256
  c26d7d62269bfbd9e2efaa2514e3e257ac10db5fc29d6589d6b71c58ca8121ea) has the same 24 PRs; the class-06 PRs #87, #64 and
  #44 have unchanged heads; the only change is PR #88's (class 04) update time. NOVELTY's own fetch was at
  17:24:41–17:28:42 UTC, under 6 hours before this gate.
- Stretched criterion or hidden quantifier: none found. The cell has no row in the official table; the bar is the
  best value posted in an open QOBLIB pull request, as the operator's clarification of the criterion defines it, and
  the scope sentence says so.
- Scope wider than reproduced: no; the scope below is CRITERION's sentence, exactly.
- Sample presented as complete, capped search used as an exclusion, probable prime: not applicable (one explicit
  object, evaluated completely).
- Table values obtained by evasion: none. Every status fetch was one plain request with a User-Agent naming
  V3R1T4S; NOVELTY's 429/503 responses were on literature endpoints, not retried.
- Bundling: one object, one cell.

Correction recorded: the claimant's step-5 self-check wrongly said the value does not depend on the tie rule
(`attempts/crossover/self_check.md`, Correction section). The panel caught it; the claimed value is unaffected under
the class's stated rule.

status: CONFIRMED_SOLUTION
confirmed_scope: The canonical count file claim/solution/a200_t10_orig_b050_l1e-02_solution.sol is feasible for QOBLIB class 06 instance po_a200_t10_orig (instance files as packaged in claim/instance/) with B = 50 and lambda = 0.01, and its exact objective under the class's minimised reference model (claim/definition/bqp_u3_c10.zpl with claim/definition/parameter_u3_c10.zpl, lambda set to 0.01, Zimpl rounding half away from zero) is -691624, strictly below (by 140239) the bar of -551385, which is the exactly re-evaluated objective of the PR #87 solution file copied in claim/bar/ and, per the claim's status record, the best value posted in an open QOBLIB pull request for cell a200_t10_orig_b050_l1e-02, a cell for which the official best-known table (copy in claim/bar/06-portfolio-solutions-README.md) has no row.
