# Honesty gate: run 2026-10-27-1709, life-smaller-orphan (bank target), partial win p1
gate written: 2026-11-02T18:20:07Z (date -u) by the run's orchestrating session (scheduled afternoon shift), after reading all three panel files in full.
status: CONFIRMED_PARTIAL
confirmed_scope: verified encoding soundness (UNSAT <=> no (h+2)x(w+2) predecessor of an h x w target, B3/S23 masks 8/12), independence, 32-cube cover and all 5x8 `.res` `c_VERIFIED` rows, and rebuilt CaDiCaL+lrat-check on 3x3/4x4 plus SAT/UNSAT polarity on tiny brute-forced sizes; did not re-solve 5x8, run kissat, or perform the human LifeWiki novelty gate.
partial win: p1 ("a DRAT/LRAT-certified proof, two independent encodings, that no orphan exists in some h x w box with h >= 5 not already ruled out in the literature"). Box: 5 x 8 (and with it every 5 x w, w <= 8). The full success criterion (an orphan smaller than Eker's 12 x 8, area 96) is NOT met, and p2 is not claimed.

## Panel record (plain)
Each reviewer was a fresh headless Grok Build CLI session (grok --prompt-file, no prior conversation), started in its own copy of claim/, nice -n 19.
- CRITERION (criterion.md, 2026-11-01): pass. Encoding soundness, independence of tcnf and mcnf, 32-cube cover, all 5x8 .res rows c_VERIFIED; rebuilt CaDiCaL+lrat-check on tiny sizes with polarity controls. Caveat: did not re-solve 5x8 or run kissat.
- NOVELTY (novelty.md, 2026-11-01): pass. Beer 2023 covers 7x7 only, Wade 2023 height <= 4; nothing published covers 5x8.
- REPRODUCE (reproduce.md, 2026-11-02, fourth session; attempts 1 and 3 timed out without a verdict, attempt 2 was inconclusive only because of a memory cap, all kept under work/): pass. Rebuilt mcnf, re-solved 5x7 mcnf cube c4 v23 UNSAT, lrat-check c VERIFIED, clause count and proof size match the stored row; own predecessor DP; subseq on two small tcnf cubes; polarity controls. Caveat: no 5x8 cube re-solved in that session.
- Human novelty gate (bank criterion (4) / p1 "human LifeWiki/forum check required"): done by the user. 2026-10-26: ConwayLife forums and LifeWiki searched for "5x8 orphan", "5 x 8 orphan", "5x8", "5 x 8", nothing relevant. 2026-11-01 ~21:17 ET: the user read LifeWiki's Garden of Eden page in a browser: Eker (no GoE of height <= 3), Wade 2023 (no height-4 orphans), nothing in 7x7, no symmetric one in 8x8 or 9x9, Eker's 45x5 as the shortest known; nothing about 5x8.
- Gate-side checks (orchestrating session, not independent; gatecheck/): fresh rebuild and re-solve of 5x8 cubes c4 v21 in BOTH encodings, compared with the stored rows (see gatecheck/*.log and the lines below).
  - mcnf 5x8 c4 v21: 16793861 clauses (= stored), CaDiCaL exit 20 in 320 s, proof 168580 kB (= stored), lrat-check c VERIFIED (gatecheck/resolve_c4v21.log).
  - tcnf 5x8 c4 v21: 14721762 clauses (= stored), CaDiCaL exit 20 in 409 s, proof 346980 kB (= stored), lrat-check c VERIFIED (gatecheck/resolve_tcnf_c4v21.log).

## Downgrade check (kit/RUN.md step 7)
- Hedging panelist: no. All three pass outright and state their caveats.
- Reproduction mismatch: none. Reviewer 5x7 re-solve and gate-side 5x8 re-solves match the stored rows (clause counts, UNSAT, proof size, c VERIFIED).
- Value vs live table: p1 asks for a box not already ruled out; novelty panelist and the human LifeWiki check found 5x8 not ruled out (literature stops at height 4 and 7x7).
- Stretched criterion or hidden quantifier: p1 requires two independent encodings, checked proofs (drat-trim family lrat-check, from the drat-trim repository), and a human check; all present. kissat (main criterion (2)) is not required for p1 and is not claimed.
- Scope wider than reproduced: the 5x8 claim rests on 64 cube proofs (32 per encoding), each mechanically checked by lrat-check at run time; a fresh reviewer re-solved a representative 5x7 cube and audited all rows, and the gate re-solved one 5x8 cube per encoding. Every individual proof was machine-checked, so no unchecked extrapolation is used.
- Sample presented as complete / capped search as exclusion: no. Coverage: the 32 cubes fix target column 4 to each of its 32 values (exhaustive); subset checks SUBSET_OK; no solver time cap counts as UNSAT (only exit 20 with a verified proof).
- Several objects bundled: one box (5 x 8); smaller widths follow from it and are certified separately anyway.
- Benchmark baseline (step 3c): not applicable (exact certificate, no score).
Result: no downgrade. Final status CONFIRMED_PARTIAL (p1), subject to CHECK_RUN: PASS and a package in outbox/ (kit/RUN.md step 8).
