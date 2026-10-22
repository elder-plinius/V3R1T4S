# Honesty gate, cell C10 (proportion 0.10), run 2026-10-18-0202 (kit RUN.md step 7)

Written 2026-10-18T07:16:47Z (date -u; first written 07:05Z) by the main session (Opus 5.5, claude-opus-5-5[1m]) after reading all three panel files.

status: CONFIRMED_SOLUTION
confirmed_scope: At proportion 0.10, the frozen stage-2 minimum-Bayes-risk combination combiner/test/0.10 (seven frozen components trained only on the 10 surprise families' training-0.10 files and the development view, each masked test-0.10 row predicted in isolation, integer weights fit on validation splits cut from training-0.10) scores mean NED 0.18916240713560675 over the 10 surprise families under the pinned ST2022 scorer (left-to-right summation; the same value with compensated summation), strictly lower than this workspace's earlier confirmed 0.10 system (0.19710919181751296, bar_holder/), FeVeT's published predictions (0.2296925777970808) and Mockingbird-I1's official results-surprise-0.10.json value (0.2431316340782435), as a win on mean NED only.

## Panel (three fresh contexts, Agent tool, model opus = Opus 5.5)
- panel/reproduce.md: round-2 REPRODUCE skeptic on the round-2 package; retrained every stage-2 entry (weight 0 included)
  byte-identically, rebuilt the claimed object byte-identically with its own MBR code, sandboxed and per-partition
  isolation checks; pass: true.
- panel/criterion.md: round-2 CRITERION skeptic on the round-2 package; literal criterion met, null test reproduced;
  pass: true; its confirmed_scope is copied above exactly.
- panel/novelty.md: round-1 NOVELTY skeptic (status source https://github.com/sigtyp/ST2022 HTTP 200 at 04:56-04:57Z,
  HEAD 03094435 unchanged since 2022-05-27; literature of the last 24 months searched; best published value at 0.10:
  run 2026-10-17-1806's confirmed combiner); pass: true. Its fetch is about 2 h old at this gate (< 6 h), so no re-fetch was needed. The values it
  checked are identical in the round-2 package.
- Round 1 (round1/panel/, round1/claim/): the round-1 package omitted the code of weight-0 stage-2 entries, whose strings
  the per-item rule can still choose (C20 1 item, C30 6 items, C10 4 items), and said wrongly that they had no influence.
  The round-1 REPRODUCE skeptic failed C30 and C10 and the round-1 CRITERION skeptic failed C10 on that ground; C20 passed
  all three with the defect noted. Repair (this run's repair round 1): sealed checks of every weight-0 entry at its P
  (runs/2026-10-18-0202/out/sealed2_*.log, all PASS), a rebuilt package with every entry's code and corrected text, and
  new REPRODUCE and CRITERION skeptics on it. The claimed object, its value, the weights and the selection did not change.

- Re-issue (07:15-07:16Z): the skeptics whose texts quoted path patterns in angle brackets (which the kit's placeholder
  check rejects in published files) re-issued them with the brackets removed; the main session verified each re-issue
  against the skeptic's first text with a line diff (only those tokens differ). Verdicts and scope unchanged.

## Gate checks (downgrade on any; none applies)
- Hedging panelist: none (three plain pass: true).
- Reproduction mismatch: none (every entry and the object reproduced byte for byte; rule 12 iv in its strict case).
- Value strictly better than the live table and the PREREG bar: COMB-ALL10 0.18916240713560675 vs our own confirmed 0.19710919181751296 (FeVeT 0.2296925777970808, Mockingbird-I1 0.2431316340782435); margins far above 1e-9 in both summation modes.
- Stretched criterion or hidden quantifier: none found by CRITERION (row isolation stricter than the literal criterion).
- Scope wider than reproduced: no; the scope above is the CRITERION sentence, about one object at one proportion on mean
  NED only.
- Sample presented as complete, capped search, probable prime: not applicable.
- Table value obtained by evasion: no (one honest GET per resource through the stop-aware helper; blocks recorded in
  logs/stops-2026-10-18-0202.tsv and never retried).
- Several objects bundled: no (one cell, one object).
- PREREG rule 12: (i) met; (ii) null test passed (best_control: 0.005948936672339172; real: 0.00794678468190621; 0 of 400 controls at or above real);
  (iii) every stage-2 entry passed its lens's harness test-mode audit at 0.10 and the main session's sealed check at 0.10
  (runs/2026-10-18-0202/out/sealed_0.10.log and sealed2_0.10.log, both SEALED_CHECK 0.10 PASS); run 2026-10-17-1806's two entries by that run's own sealed check (SEALED_COMPARE PASS); (iv) REPRODUCE retrained every
  entry byte-identically.

Final status: CONFIRMED_SOLUTION, standing only if python3 repo/kit/check_run.py prints CHECK_RUN: PASS for this folder.
