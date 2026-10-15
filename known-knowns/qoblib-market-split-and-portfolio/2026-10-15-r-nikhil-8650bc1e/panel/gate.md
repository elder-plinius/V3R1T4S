# Honesty gate (kit/RUN.md step 7), run 2026-10-15-0312, lane C

Written by the run's main session at Thu Oct 15 09:11:13 UTC 2026 after reading all three panel files in full: `reproduce.md`,
`novelty.md`, `criterion.md`. Each was written by a fresh subagent that saw only its own copy of `claim/` (plus,
for NOVELTY, the web and this repo's TROPHY_CASE.md). Each has a `context:` line and ends with `pass: true`.

## Downgrade checks

- Hedging panelist: none. Each states what is outside its own scope (NOVELTY did not re-evaluate the object; CRITERION
  relied on STATUS_RECORD.md for the public-value search), and those gaps are covered by the other two panelists.
- Reproduction mismatch: none. REPRODUCE's own exact evaluator (literal binary point + count cross-check) gives
  −644342 / −401535 / −192428, equal term by term to the claimant's checker; 5 corrupted copies rejected by both;
  byte-identical reruns; all 14 sha256 values match.
- Strictly better than the live bar: yes. NOVELTY fetched the table and the open PR list at 09:03 UTC (under 6 hours
  old at this gate): best posted value −401535 (PR #87); no table row; no third-party, website, literature or
  V3R1T4S value at or below it. Margin 242807; not a tie.
- Stretched criterion or hidden quantifier: none found. The cell (instance, B, lambda) is how the library's own table
  keys entries. The claim says plainly that the table has no row, so this beats posted values, not a curated entry.
- Convention dependence: the value assumes ZIMPL's round-half-away-from-zero (200 exact 5/2 ties at t = 0); under four
  other tie rules the claim and the bar both shift by 23, so the comparison is unchanged (REPRODUCE, CRITERION and
  the self-check agree).
- Scope wider than reproduced: no; the scope below is CRITERION's sentence, exactly.
- Sample presented as complete, capped search used as exclusion, probable prime: not applicable (explicit object).
- Table access by evasion: none (one plain request per URL, honest User-Agents, no retries; the self-check audited
  the code folders).
- Bundling: one cell, one object. Other cells found this run (a400_t10_orig lambda 1e-2) are leads only.

status: CONFIRMED_SOLUTION
confirmed_scope: The frozen solution file (sha256 8650bc1e...efe62) is feasible for QOBLIB class 06 instance po_a200_t10_s00 with B = 50 and lambda = 0.01 under the reference model bqp_u3_c10.zpl and has exact minimised objective −644342, strictly below the best value posted in the open-PR files supplied for this cell (PR #87, −401535; PR #64, −192428), a cell for which the official best-known table has no row.
