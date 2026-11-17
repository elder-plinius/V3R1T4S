# Honesty gate (kit/RUN.md step 7), run 2026-11-13-0104

date: 2026-11-13
gate written: 2026-11-13T02:26:54Z (date -u; rewritten after the CRITERION skeptic reworded one placeholder-like token in its own file at 2026-11-13T02:26:21Z, no change of substance), by the run's main session after reading reproduce.md, novelty.md and criterion.md
status: CONFIRMED_SOLUTION
confirmed_scope: On route (a), 2024-25 season of HopkinsIDD/rsv-forecast-hub at commit 6bf251ac (unchanged live at 2026-11-13T02:13Z), the frozen as-of forecasts of V3R1T4S-asofKA (hub-format copies in attempts/forecaster/result/submission/) have season-average WIS 72.24 against the hub-ensemble's own files' 99.70 on the 3,065 hub-ensemble tasks that have truth in target-data/2026-06-05_rsvnet_hospitalization.csv (0-0.99, 1-4 and 5-64 as exact sums of its finer groups; the 695 65-130 tasks have no truth there and are unscored for both, our forecasts for 370 of them being all-zero placeholders), a relative difference of -27.6% with paired stationary-bootstrap 90% interval about [-36%, -20%] over the 14 reference dates, the whole gain coming from the 265 national (US) tasks while our state-level forecasts score worse than the ensemble's.

## Panel
- reproduce.md: pass: true (own scorer, truth and bootstrap reproduce 3,065 tasks, 72.2386 vs 99.7021, rel -0.2755;
  31/31 forecasts regenerate byte-identically; own minimal-tree look-ahead check identical on 4 origins).
- novelty.md: pass: true (status source fetched 2026-11-13T02:06:47Z, HTTP 200; no scores file in either hub; no
  published 2024-25 HopkinsIDD season scores or competing forecaster; nothing in the V3R1T4S repo for this target).
- criterion.md: pass: true, with the narrow confirmed_scope above and required disclosures (65-130 all-zero
  placeholders on 370 of 695 tasks and the two 65+ re-scorings that erase the margin; state-level splits; the asymmetry
  between the 65-130 input derivation and PREREG R4; the dev record; cite result/submission/ as the hub-format files).

## Gate checks
- Hedging panelist: no; CRITERION's conditions are disclosure requirements, met in the package (README "Not claimed",
  DISCLOSURES), not doubts about the verdict.
- Reproduction mismatch: none. Scope wider than reproduced: no (the scope sentence is CRITERION's, limited to the 3,065
  scored tasks, naming the placeholders and the US-only gain).
- Value strictly better than the comparator: yes (-27.6%, interval far below 0); comparator re-fetched live at
  2026-11-13T02:23:01Z (tree API 200, 300 model-output blobs unchanged, truth unchanged, 15/15 2024-25 hub-ensemble files
  byte-identical; attempts/contrarian/out/refetch_2/refetch_check.txt). Panel fetches are < 6 h old.
- Evasion: none (honest single requests; no retries after refusals; no block encountered on route (a) sources).
- Bundling: p2 (met by the same scoring) and p1 (not met) are not part of this claim.
- Benchmark baseline (step 3c): no published score exists; recomputation recorded in baseline/; CRITERION checked it.
- Main-session judgement recorded for the human: the pass depends on 65-130 having no truth in the hub's current target
  file (pre-registered PREREG R4, before any forecast existed); our 65-130 forecasts are partly all-zero placeholders.
  This is flagged under "Needs you" in REPORT.md for the human's decision before any filing.
