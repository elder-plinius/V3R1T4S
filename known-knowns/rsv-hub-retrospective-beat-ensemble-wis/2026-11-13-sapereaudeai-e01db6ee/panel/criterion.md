# CRITERION skeptic, run 2026-11-13-0523 (claimed item: partial win p3 only)

context: subagent (Claude Code Agent tool, subagent_type criterion)

Started 2026-11-13T05:34:15Z, verdict written about 05:46Z (date -u). Files are named relative to claim/. My reruns used a
copy of claim/ in this skeptic's work folder, `python -I -B` (no bytecode written), 2 threads, one job at a time.

## Binding text

bank/targets.json, id rsv-hub-retrospective-beat-ensemble-wis: the p3 statement, the success criterion, p1 and p2 are
quoted verbatim in CLAIM.md (checked character for character). Only p3 is claimed:
"An independent recomputation of per-model season WIS for a completed RSV season from the hub's raw model-output and
target data, released as a reproducible script, documenting any discrepancy with the hub's own published scores (if
any) and the exclusion rules needed to reconcile them."

## Evidence I produced (real output)

- 05:36:02-05:36:14Z `code/p3_recompute.py data/hub out_check`: exit 0. sha256 p3_table.csv e01db6ee...f804,
  p3_exclusions.txt 9fceead7...7a0a, p3_era_subset.txt 9cf68a4e...6ace. All three equal object/.
- 05:37:49-05:37:56Z `code/p3_reconcile_k2.py ...`: exit 0. sha256 74257bac...63e9, equal to object/.
- 05:38:06-05:38:53Z, all seven code_reconcile/ commands in REPRODUCE.md: each exit 0. The cmp loop printed `DONE`
  and no DIFF line.
- 05:42:19Z `cd baseline && reproduce_era_table.py ../data/hub`: exit 0. Output equals baseline/era_reproduction_rerun.txt
  except for its first header line. The four pinned-oracle lines all say WITHIN: 14.635, 16.422, 19.804 and 18.306,
  against the published 14.7, 16.4, 19.8 and 18.3.
- Hub provenance:
  - `git ls-remote` at 05:36:25Z: HEAD and refs/heads/main are both 1985aee45bca6b655e22b8bc2096b515bd6327f2.
  - I fetched e947ca8 and 1985aee blobless at depth 1 (05:36:32Z). `git diff --no-renames --name-status e947ca8 1985aee`
    printed only `A model-output/UM-DeepOutbreak/2026-11-14-UM-DeepOutbreak.csv`.
  - The e947ca8 tree has 25 model-output directories plus README.md. 247 files are dated 2025-09-01..2026-08-31, in 9
    directories: CEPH 25, CFA E 29, CFA HE 29, CFA H 29, Google 23, baseline 30, ensemble 29, UGA 28, UM 25.
  - No tree path matches score|eval|wis|summar.
  - `git hash-object --no-filters` of all 250 files under data/hub gives the e947ca8 blob ids, with 0 mismatches.
  - At the head, RSVHub-ensemble has 36 files, 29 of them in 2025-26.
- data/hub/hub-config/tasks.json: one round, both targets, quantile output_type_id with 23 required levels
  (0.01..0.99). The 247 files contain only quantile rows, plus sample rows from the three CFA directories (not scored).
  Every directory with in-season forecasts therefore has quantile rows for each of its targets, and the table's 8 hosp
  and 5 ED directories are complete.
- Pairwise relative WIS with and without the self-ratio: I re-ran p3_recompute with relative_skill wrapped, and the
  table hash was unchanged. The largest change is 4.07% (UGA_flucast-INFLAenza ED, 1.1732 -> 1.2210), so disclosure
  7's "up to about 4%" holds.
- oracle-output.parquet has 5,145 quantile rows, 5 of them NaN, so 5,140 are non-missing (disclosure 3).
- Truth revisions between the 2026-11-04 and 2026-11-12 vintages: 50 of 4,305 rows changed.
  - Largest change relative to the 2026-11-12 value: ED, location 19, 2026-06-06, 0.0058 -> 0.0051 (13.73%).
  - Largest change relative to the 2026-11-04 value: hosp, location 48, 2026-06-13, 41 -> 46 (12.20%).
  - Both match disclosure 3.
- data/ext/load_hub.py, keep_forecast_file, contains `if not path.endswith(".csv"): return False`. All 28 in-season
  files of UGA_flucast-INFLAenza are .parquet, so the cause given in clause (i) holds.
- Exact Google-comparison differences, from my own script using code_reconcile/hubload.py:
  - Pooled: 15.393662987879464 against the published 15.39366298787946 (|diff| 3.6e-15).
  - Per-location Google_SAI-RSVEns: largest |diff| 9.09e-13, none above 1e-12.
  - Per-location RSVHub-ensemble: largest |diff| 1.82e-12, and one value is above 1e-12: location 36, summed WIS
    9077.012942330319, a relative difference of 2.0e-16 (one floating-point unit at that size).
- Hub-scores check:
  - https://github.com/CDCgov/rsv-forecast-hub/issues/515 (05:40:57Z, HTTP 200, one request) is titled "End of season
    close out tasks" and includes "Update scoring and internal visualization dashboard".
  - https://www.cdc.gov/cfa-modeling-and-forecasting/rsv-data-vis/index.html (05:41:12Z) returned HTTP 403. I did not
    retry and did not read it.
- Overlap check on tapestry (blobless fetch of main 06508218 and restructure/unified-model 6546e066 at 05:40:22Z):
  - The RSV rows of docs/legacy-v0/results/B2-screen/benchmark/leaderboard.csv hold no hub model other than
    RSVHub-ensemble.
  - main also has docs/experiments/nowcast-overnight-20261005/rsv-component-target-scores*-2025-2026.csv. These hold
    RSVHub-ensemble summed WIS columns (ensemble_wis) next to tapestry's own configurations, on the same
    ensemble-unit sets as the leaderboard: hosp 6032/5916/116, ED 5586/5475/111.
  - record/published_table.md does not name these files. It says it is not a complete list, so this falsifies nothing.

## Clause-by-clause reading of p3

1. "An independent recomputation": met. The loader, task pairing and scoring are the work's own code (code/wis.py, a
   Python form of scoringutils WIS). Pinball and interval forms agree to 1.36e-12. Values that tapestry computed with
   R scoringutils 2.1.1 on the hub's 23 levels reproduce to about 1e-12, so the scorer matches the public hubverse
   scorer on those tasks.
2. "of per-model season WIS": met for every model directory with 2025-26 quantile forecasts. That is 8 for hosp and 5
   for ED, each a mean over its own scored tasks, with paired columns on the full task id.
   - Hidden quantifier "per-model": checked against the e947ca8 tree. 9 of 25 directories have 2025-26 files, and all
     of them are in the table.
   - Hidden quantifier "season": all 247 in-season files and all 30 reference dates. Data rules drop 0 tasks (0
     incomplete quantile sets, 0 tasks without truth).
3. "for a completed RSV season": met. 2025-26 forecasting ended on 2026-05-30, and the hub has moved to 2026-27 files.
   The truth was still being revised up to 2026-11-12. That is disclosed, and the table is stated to hold for the
   pinned oracle only.
4. "from the hub's raw model-output and target data": met. Blob identity is verified against e947ca8, every input is
   unchanged at the live head 1985aee, and truth is that commit's target-data/oracle-output.parquet.
5. "released as a reproducible script": the reproducible part is met (byte-identical rerun above). "Released" is not
   met yet. It becomes true only when this package is published, as disclosure 5 says. This pass depends on that.
6. "documenting any discrepancy with the hub's own published scores (if any)": the hub's repository has no score file
   at e947ca8 or 1985aee (verified). Issue #515 points to an internal dashboard. The bank itself says "Neither hub
   currently publishes its own scores file". The clause is therefore vacuous for the hub, and disclosure 1 says so
   openly.
   - Residual unknown: the public CDC RSV page could not be read (HTTP 403).
   - The third-party discrepancies, such as the arXiv truth differences, UGA's absence from the arXiv repository's
     rows, and the mis-dated ED rows, are documented with their causes.
7. "and the exclusion rules needed to reconcile them": vacuous for the hub. For each third-party set the rules are
   stated (truth vintage, horizons 0-3, Puerto Rico, the target_end_date rule), and they reproduce.

Null model: none is needed. This is a deterministic recomputation, not a detection or better-than-chance claim. The
controls are the two WIS forms and the exact reproduction of independently computed third-party values.

Baseline record (kit step 3c):
- Data: the same as the claim's (hub files at e947ca8, blob-verified).
- Split: the published Supplementary Table 6 subset (52 states, horizons 0-3, 22 reference dates), which is a subset of
  the object's tasks.
- Metric: the same mean 23-level WIS.
- It reruns as recorded. Its wis.py is byte-identical to code/wis.py, which is disclosed. The independent WIS check is
  the third-party reconciliation, which uses the separate WIS function in code_reconcile/hubload.py.

Subsumption: not subsumed by anything named in the package or found here.
- arXiv 2605.16238 v2 and its repository: hosp only, 7 of 8 hosp directories (UGA missing), 22 of 30 dates, no ED.
- EpiBenchmark: ensemble and baseline only, hosp, 5 quantile levels.
- tapestry: the ensemble for both targets, UGA only on its common units with the ensemble, Google hosp only. Its
  committed RSV rows name no other hub directory.
- Zenodo: relative WIS only.
- No named source gives per-model season WIS for all 9 directories, or any ED values for the CFA_Pyrenew E or HE
  directories or for RSVHub-baseline.
- A wider literature search is the NOVELTY skeptic's job and was not repeated here.

## Statement-by-statement check of the CLAIM.md sentence and disclosures

Verified true:
- the commit pair and the head
- the reference dates
- "247 ... files", "9 of the hub's 25 model directories"
- the 23 levels
- "8 ... 5"
- "500 ED tasks in two 2025-09-27 files" (250 + 250, offset -1 week)
- no score file in the hub's tree
- 26,248 rows reproduced (9.09e-13)
- "at most 0.101" (0.10081)
- 171 of 1,378
- the .csv-only loader
- EpiBenchmark: 11,648 rows reproduced (6.82e-13) with truth as_of 2026-09-16
- the 20 leaderboard values: hosp relative <= 4.3e-16, ED relative <= 1.2e-13 with the target_end_date rule
- the 4 hub-evaluation values: relative 0 and 4.8e-14
- the 1 + 102 Google values
- the 5,936 / 5,824 / 5,350 counts
- every number in disclosures 3, 6 and 7, except as noted in R2 below

Disclosure 9 (history of other runs) was not checked, because I was told not to read other runs.

Three statements are not literally true and must be corrected. The object does not change.

- R1 (claim sentence): "each reproduced within 1e-12" is false read as an absolute difference.
  - One of the 102 tapestry per-location values is off by more than that: RSVHub-ensemble, location 36, summed WIS
    9077.012942330319, |diff| 1.82e-12 (relative 2.0e-16).
  - Every other reconciled value is within 1e-12.
  - Fix: write "each reproduced to within 2e-12 absolute (the largest difference, 1.82e-12, is on RSVHub-ensemble's
    summed WIS of 9,077 for location 36)", or state that the 1e-12 is relative where that is meant.
- R2 (disclosure 3): two "at most" bounds are rounded down and so are false.
  - CFA_Pyrenew-Pyrenew_H_RSV: 16.901411 - 16.80060365 = 0.100807 > 0.1008.
  - CEPH-Rtrend_rsv: 19.803893 - 19.75763996 = 0.046253 > 0.046.
  - Fix: "at most 0.1009" and "at most 0.0463", or "0.101" and "0.047". The claim sentence's "at most 0.101" is
    correct.
- R3 (claim sentence, attribution): grammatically, code/p3_recompute.py is the subject of "finds no score file in the
  hub's own repository, and was reconciled with these third-party score sets".
  - That script does not search the hub tree. The search is in record/status_source.md.
  - The reconciliations are run by code/p3_reconcile_k2.py and code_reconcile/, which has its own loader and WIS
    function, not by p3_recompute.py.
  - Fix: make the subject "this work", or name those scripts and that record.

Condition: "released" is met only when exactly this package (object/, code/, code_reconcile/, data/, record/, REPRODUCE.md)
is published.

Optional disclosure (not required, because the claim makes no completeness statement): add the tapestry main files
docs/experiments/nowcast-overnight-20261005/rsv-component-target-scores*-2025-2026.csv (RSVHub-ensemble summed WIS on
the leaderboard's unit sets) to item 3d of record/published_table.md.

confirmed_scope: code/p3_recompute.py deterministically and byte-reproducibly (object/p3_table.csv sha256 e01db6ee9d55baf24c06fa801c2fdfee27d9c1f70d1d513b9e98b75bd6d2f804) recomputes, from the 247 in-season model-output files of github.com/CDCgov/rsv-forecast-hub at commit e947ca8fe8d50a581a181e6aefacfe922ba95af5 (reference dates 2025-09-20..2026-05-30, all unchanged at head 1985aee45bca6b655e22b8bc2096b515bd6327f2) and that commit's target-data/oracle-output.parquet, the per-model mean 23-level quantile WIS, MAE, 50%/95% coverage, shared-task comparisons with RSVHub-ensemble and pairwise relative WIS scaled to RSVHub-baseline of every model directory with 2025-26 quantile forecasts (8 for wk inc rsv hosp, 5 for wk inc rsv prop ed visits), with its data rules in object/p3_exclusions.txt and no hub score file to compare against, while the separate scripts code/p3_reconcile_k2.py and code_reconcile/ reproduce the named arXiv 2605.16238 v2 repository, EpiBenchmark and tapestry score sets to within 2e-12 absolute under the truth vintages and task rules the claim states, for the pinned oracle only and with p3's "released" clause met only once this package is published.

pass: true
