# Honesty gate — run 2026-11-10-0600

status: CONFIRMED_SOLUTION
confirmed_scope: A fixed-form symbolic regression procedure on PMLB dataset 1028_SWD returns one 12-term closed-form expression per split for the 30 listed splits, with median test R^2 0.3911 (strictly above the PS-Tree table leader's 0.3800) and median SRBench complexity 75.5 (at or below the leader's median model_size 3270).

## Panel read (all three pass: true, fresh subagent contexts)
- reproduce.md: independent checker written from the definition before reading the author's code; median R2 recomputed 0.391051, complexity 75.5, bar recomputed 0.380003/3270; 108 checks, 0 failures.
- novelty.md: live table re-fetched 2026-11-10 06:20:59 UTC (LFS pointer oid matches — table unchanged); leader confirmed; 24-month literature search clean; expressions not trivial edits of any published model.
- criterion.md: bar recomputed over all 28 algorithms; all 30 expressions re-scored independently; closed forms genuine; null (train-mean) median R2 -0.0027; no stretched definitions, no subsumption.

## Downgrade review (step 7)
- No hedging panelist; no reproduction mismatch (0.3910 stated vs 0.3911 re-scored is the disclosed 4-decimal coefficient rounding; both clear the bar).
- Value strictly better than the live table (panel fetch < 6 h old); no table evasion (one honest GET per fetch).
- No stretched criterion or hidden quantifier found; scope is exactly the scored outcome; all 30 splits scored (no sample-as-complete); one cell, one procedure.
- "Fixed procedure / no per-split hand edits": the panel could not audit this from claim/ alone. Main-session attestation: both lens scripts were written before their scoring runs, hyperparameters are fixed in code, and each script loops over the 30 seeds with no per-split edits. The only post-hoc change was the PREREG.v2 split correction (numpy permutation -> sklearn train_test_split), validated against recorded table values to +-0.0001 and applied by re-running both lenses in full — not tuned to any result.
- Narrow-margin note (from criterion.md, not a downgrade): +0.0111 on the median, 18/30 splits above 0.3800, per-split range 0.229-0.466. A real win under the literal criterion, not a wide one.
- The constructor lens's p1 partial win (0.3776, 67) was independently recomputed but NOT panelled; it is not confirmed and not packaged. Only the smuggler full win is confirmed here.
