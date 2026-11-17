# CRITERION skeptic: rsv-hub-retrospective-beat-ensemble-wis (route (a), season 2024-25)

context: subagent (Claude Code Agent tool, subagent_type criterion, fresh context)

Read: claim/CLAIM.md, claim/target.md, claim/PREREG.md (+ v2, v3, v4), claim/attempts/forecaster/METHOD_FREEZE.md,
claim/DISCLOSURES.md (including item 8, added 02:09:50Z, and claim/attempts/evaluator/test/score_2023-24_descriptive.log),
claim/baseline/README.md and the files they cite (score logs, scorer code, as-of code, read log, contrarian outputs, hub
READMEs, hub-config tasks.json, hub-ensemble files, truth file, archive vintages).

## What I recomputed myself (own code, panel/work_criterion/)

- Own loaders, own WIS (scoringutils interval form: weights alpha/2, median weight 1/2, divided by K + 1/2), own truth
  derivation, own stationary bootstrap (different RNG stream). Result on the claim's task set: 3,065 scored
  hub-ensemble tasks, 14 reference dates, ours 72.239, hub-ensemble 99.702, rel -0.2755; paired 90% interval
  [-0.3620, -0.1992] (seed 7), [-0.3593, -0.1981] (seed 99), [-0.3596, -0.1989] (B 20000). Matches
  claim/attempts/evaluator/test/score_test_2024-25.log within Monte Carlo noise.
- Coverage: all 3,760 tasks of the 14 non-empty 2024-25 hub-ensemble files are present in both
  claim/attempts/forecaster/result/forecasts/ and claim/attempts/forecaster/result/submission/ (identical values on
  every shared row); 23 levels, no negative values, no crossing quantiles. Forecast files match
  forecasts_sha256.txt; code and parameters match freeze_hashes_v4.txt and the frozen evaluator hashes.
- As-of: claim/attempts/forecaster/result/forecasts/read_log.csv has 44 reads, 0 violations of "vintage label <= origin
  and last week read <= origin - 8 days". One GitHub API request (commits touching target-data/archive, 02:13:44Z, HTTP
  200) shows the archive was committed weekly on the Friday of each label from 2024-11-08 on ("Update target data" followed by the label date),
  so labels track real availability for the vintages it covers; the Saturday-family vintages used for 2025-02-09 and
  2025-02-16 show the normal first-report backfill pattern (e.g. US week 2025-02-01: 6644 in the 2025-02-08 vintage vs
  8969 a week later and 10298 final), not later-revised values.
- Live re-check (one request, GitHub recursive tree API, 2026-11-13T02:13:19Z, HTTP 200): main is still commit
  6bf251ac; all 300 local model-output files have the live git blob SHA; the truth file is unchanged; no scores,
  evaluation or oracle file exists. One request for hub-config/admin.json at the pinned commit (HTTP 200):
  file_format ["csv", "parquet"], so CSV submissions are the hub's format.

## Clause by clause (full success criterion, route (a))

1. "saved quantile forecasts in that hub's submission format": MET by claim/attempts/forecaster/result/submission/
   (8 columns, "inc hosp", 23 levels of tasks.json, horizons 0..5 inside tasks.json, allowed age groups and locations,
   valid team-model name, CSV accepted by admin.json). The folder named in the CLAIM sentence (result/forecasts/) also
   carries horizon -1 rows, which tasks.json does not allow; the claim should cite submission/ as the hub-format files.
2. "released deterministic pipeline": code and parameters are in claim/ and hash-pinned; the look-ahead audit reran 17
   origins with identical output. MET (determinism is the REPRODUCE skeptic's to confirm in full).
3. "reads only data available on that date (as-of vintages; no final revised series, no other team's forecasts, no
   parameter tuned on later weeks of the same season)": MET for the pipeline (reads only target-data/archive; read log
   clean; archive commit dates consistent). Parameters were selected on 2023-24 only (METHOD_FREEZE), which the
   criterion allows. Weak points, not failures: the freeze is evidenced only by self-recorded date -u stamps and
   sha256 (no git commit or third-party timestamp, which the hindsight pitfall asks for), and the 40-configuration
   dev record cited by METHOD_FREEZE (work/dev/dev_results.jsonl, out/batch1-5.tsv) is not in claim/. Dev truth for
   2023-24 was the 2026 final file (earlier season; allowed by the text).
4. "season-average WIS computed with the public hubverse scoring code": the scorer is a Python reimplementation, not
   hubEvals/scoringutils (R not installed; disclosed, item 5). The formula is the scoringutils WIS (weigh = TRUE,
   median once) and my independent implementation gives the same numbers, so the value is the hubverse value.
   Accepted as met in substance; the literal deviation must stay disclosed.
5. "same locations, horizons, reference dates and age groups; hub exclusion rules applied": MET. Both models are scored
   on exactly the same 3,065 tasks with the same truth. The hub publishes no exclusion rules beyond the ensemble's
   horizons 0..4.
6. "strictly lower ... by at least 3% relative": MET, -27.55%.
7. "outside a stationary-bootstrap 90% interval over reference dates": MET under every single-interval reading I can
   construct: paired relative-difference interval [-0.36, -0.20] excludes 0 (and excludes -3%); our 72.24 lies below
   the ensemble's own bootstrap 90% interval of its season-average WIS [84.6, 115.6]; the ensemble's 99.70 lies above
   ours [57.1, 87.2]. Holds for block length 1..6 (author's sensitivity) and leave-one-date-out (-0.24 to -0.32).
8. "the hub ensemble's season-average WIS recomputed identically from that hub's own ensemble model-output, re-fetched
   live immediately before claiming": MET (ensemble's own files; author re-fetch 01:58-01:59Z; my blob check 02:13Z).
   Using the files, not a recomputed mean, is correct: baseline/hub_season_wis_2024-25.txt shows the files differ from
   the mean of today's member files on 195 tasks. If the claim is filed later, refetch_check must be rerun first.
9. "covering every reference date, location, age group and horizon of the hub-ensemble": MET LITERALLY (3,760/3,760
   tasks present), BUT see the finding below: 370 of the 695 65-130 tasks are all-zero placeholder forecasts.
10. "as-of data from the hub's target-data/archive vintages": MET.
11. Scores-file override: no scores file in HopkinsIDD/rsv-forecast-hub (live tree), so the recomputed bar applies.

## Are the frozen readings fair or a stretch?

- Truth version (R4, final 2026-06-05 file): fair. It is the hub's current target data, the hubverse convention and,
  per DISCLOSURES item 3, the bank's verification method (I could not see the bank's verification text; target.md
  carries only criterion, partial wins and pitfalls). Sensitivity is real and disclosed: against first reports ours is
  worse (+26%); against the view 4 weeks later or the season-end vintage ours still wins (-26%, -25%). The gain is a
  backfill nowcast scored against revised data, which is legitimate under as-of inputs. The hub README's "no adjustment
  for reporting (=raw data from RSV-NET dataset to be projected)" reads to me as "no under-ascertainment multipliers",
  not "forecast first reports"; disclosed (item 3).
- Derived age groups (0-0.99, 1-4, 5-64 as exact sums of the file's finer groups): fair; I checked 0-4 against the sum
  of its four parts in three vintages (median +0.4%). Not load-bearing: the narrowest literal reading (score only
  rows the hub file carries, i.e. 0-130 only) gives ours 126.82 vs 179.77, rel -0.2945, 90% [-0.392, -0.212], also MET.
- Unscored 65-130: literal and pre-registered before any forecast existed (PREREG R4), and it is what hubverse scoring
  of the hub's current target file does (no 65+ rows after 2016-09-24). But it is LOAD-BEARING and the claim does not
  say so (see finding). It is also internally asymmetric: attempts/forecaster/code/asof_rsv.py derives 65-130 for its
  inputs as 0-130 - (0-4 + 5-17 + 18-49 + 50-64), yet R4 declares the same quantity "no truth". I accept the reading
  as fair because the complement is not an identity in this data (0-130 differs from the sum of all five groups by a
  median -1.5%, 5th-95th percentile +-13% of 0-130 in vintages that carry 65-130; it even goes negative in New Mexico)
  and because the archive values are a different truth version; requiring either would be a gate the bank did not set.
- Bootstrap reading (R7, paired ratio, L = 3, 95th percentile < 0): fair; all alternative single-interval readings pass.
- Amendments v2-v4 before scoring: fair. v2 fixes a mislabelled vintage (2023-12-08 holds data to 2023-12-30) and the
  parallel file family; v3 is a crash fix; v4 is needed for coverage (NC missing in the 2024-11-22 vintage) and changes
  only 2024-11-24. None uses a 2024-25 score. Side effect of v3 found below.
- Development protocol: one frozen config chosen on 2023-24 by a pre-declared statistic; scored once on 2024-25. Fair,
  with the evidence-package gap noted in clause 3.
- Null test: I agree none beyond the bank's bootstrap is needed: one frozen forecaster, one held-out season, one
  pre-declared comparison, no search on the test season; the stationary bootstrap over dates is the bank's own
  uncertainty model, and ours is lower on 12 of 14 dates.

## Finding the claim must disclose (load-bearing for the full criterion)

- 370 of the 695 hub-ensemble 65-130 tasks carry ALL-ZERO forecasts (every quantile 0, all 14 locations, every horizon)
  for the six origins 2024-12-08 .. 2025-01-26, i.e. the RSV peak (US 65+ truth about 1,700-4,500 per week then). Cause:
  the Friday vintages from 2024-12-06 carry 65-130 only as rows ending in 2016; the PREREG.v3 stale-series rule marks
  them absent and the frozen fallback (0-130 x US share over 52 weeks) then has a zero share. So the 65-130 group is
  "covered" by placeholders, and the CLAIM's "65-130 ... is unscored" hides how much it matters.
- If the ensemble's 65-130 tasks are scored, the full-task-set result is gone: with 65+ truth from the hub's own archive
  (latest vintage carrying 65-130, weeks to 2025-03-08; 3,746 tasks) ours 100.81 vs 101.89, rel -0.0106, 90%
  [-0.247, +0.161]; with the complement from the final file (3,760 tasks) rel -0.0151, 90% [-0.249, +0.158]. On 65-130
  alone ours is about twice the ensemble's WIS (rel +1.05 / +1.14).
- The whole gain comes from the 265 national (US) tasks: sum of WIS differences -84,176 overall, -99,281 from US. On
  state tasks ours is worse in every cut: all states +18.2% [+8.0%, +26.2%], 0-130 states +9.4% [+1.8%, +16.8%],
  pediatric states +35.2% [+18.4%, +52.8%]. The bank's metric is the plain season-average WIS, so this is a scope fact,
  not a criterion failure.
- Not replicated on 2023-24 (DISCLOSURES item 8: frozen pipeline worse than the ensemble, +18.6%, [-5.1%, +31.8%]),
  for a structural reason (no earlier vintages for the backfill rule). The thin-pool pitfall asks for replication "if
  possible"; the criterion itself admits one completed season. Not a failure; the claim rests on one season.

Required additions to claim/DISCLOSURES.md before filing: the all-zero 65-130 count and both 65+ re-scorings above; the
state-level splits; the asymmetry between asof_rsv.py's 65-130 input derivation and R4; the dev record (or a note that
it is absent); and the CLAIM sentence should cite result/submission/ as the hub-format files.

## Pitfalls (bank list)

- Revision leakage: avoided (archive-only reads, clean read log, look-ahead audit, archive commit dates).
- Thin-pool illusion: margin 27.6% with an interval far from 0; second-season replication not achieved (item 8).
- Target/scale mismatch: same task set and truth for both; but the result depends on which age groups have truth (65+).
- Hindsight model selection: frozen on 2023-24; freeze evidence self-recorded, dev record not in claim/.
- Ensemble recomputation error: avoided (ensemble's own files).
- Mixing hubs: avoided (route (a) only).

## Baseline record

claim/baseline/hub_season_wis_2024-25.txt is the same data, split and metric as the claim (hub-ensemble 99.702 on 3,065
tasks, same truth file and derivations, same scorer); I reproduce it independently. No published score exists to
reproduce (no scores file live). The 2023-24 dev baseline is a different season and only checks the scorer.

## Verdict

Read literally, with the pre-registered readings, the full success criterion is met. It is also met under the narrowest
literal hubverse reading (0-130 rows only). The pass depends on 65-130 having no truth in the hub's current target file.
Those tasks are mostly all-zero placeholders, and if they were scored, the margin would vanish. The claim may go forward
only with the confirmed scope below and the added disclosures. It must not be described as beating the ensemble across
all of its age groups or on state-level forecasts.

edit at 2026-11-13T02:26:21Z: placeholder-like token reworded at the run's request; no change of substance

confirmed_scope: On route (a), 2024-25 season of HopkinsIDD/rsv-forecast-hub at commit 6bf251ac (unchanged live at 2026-11-13T02:13Z), the frozen as-of forecasts of V3R1T4S-asofKA (hub-format copies in attempts/forecaster/result/submission/) have season-average WIS 72.24 against the hub-ensemble's own files' 99.70 on the 3,065 hub-ensemble tasks that have truth in target-data/2026-06-05_rsvnet_hospitalization.csv (0-0.99, 1-4 and 5-64 as exact sums of its finer groups; the 695 65-130 tasks have no truth there and are unscored for both, our forecasts for 370 of them being all-zero placeholders), a relative difference of -27.6% with paired stationary-bootstrap 90% interval about [-36%, -20%] over the 14 reference dates, the whole gain coming from the 265 national (US) tasks while our state-level forecasts score worse than the ensemble's.
pass: true
