# NOVELTY skeptic verdict: rsv-hub-retrospective-beat-ensemble-wis, partial win p3 (run 2026-11-13-0523)

context: subagent (Claude Code Agent tool, subagent_type novelty)

Object judged: object/p3_table.csv (per-model season-average WIS, 23 quantile levels, with MAE, coverage, shared-task and
pairwise columns, for every model directory with 2025-26 forecasts in github.com/CDCgov/rsv-forecast-hub: 8 for
wk inc rsv hosp, 5 for wk inc rsv prop ed visits; truth = oracle-output.parquet at e947ca8). The "cell" is a
per-model season-WIS recomputation (all model directories, both targets) for the hub's completed 2025-26 season.

## Status source fetch (one request, no retry)

- URL: https://github.com/CDCgov/rsv-forecast-hub/tree/main/model-output/RSVHub-ensemble
- time (date -u): 2026-11-13T05:34:35Z; HTTP 200; 266,792 bytes; one curl with a V3R1T4S User-Agent.
- shows: main currentOid 1985aee45bca6b655e22b8bc2096b515bd6327f2 (the live head named in the claim); 36
  RSVHub-ensemble files: 29 for 2025-26 (2025-09-27 and 2025-11-22..2026-05-30) and 7 for 2026-27
  (2026-09-26..2026-11-07); no score, evaluation or summary file listed. This matches record/status_source.md.

## (a) Is the object new?

Verdict on novelty: yes. No published score set I could find covers the cell. Every published set is a strict subset
of the object's coverage, and the object's missing cells cannot be produced from them by trivial edits (deletion,
restriction, relabelling, a propagation rule or polishing). Restricting or relabelling a published subset cannot create
scores for directories, dates or targets that subset does not hold. Known published coverage, all checked by me:
- Hosp, row level: at most 7 of the 8 hosp directories on 22 of 30 reference dates (epi-hub-analysis; UGA_flucast-INFLAenza
  absent), with a different truth snapshot.
- Hosp, other: RSVHub-ensemble and RSVHub-baseline only, on 5 quantile levels (EpiBenchmark); RSVHub-ensemble,
  UGA_flucast-INFLAenza and Google_SAI-RSVEns aggregates on reduced unit sets with truth as_of 2026-09-02 (tapestry).
- ED: only RSVHub-ensemble and UGA_flucast-INFLAenza aggregates on 5,350/5,586 units (tapestry). I found no published
  ED score for RSVHub-baseline, CFA_Pyrenew-Pyrenew_E_RSV or CFA_Pyrenew-Pyrenew_HE_RSV anywhere.
The object exceeds every one of these in models, dates and targets. The p3 bank text asks for exactly this kind of
recomputation, so "seeded from a published object" does not apply: the object is computed from the hub's raw files.
The overlapping published subsets are disclosed in CLAIM.md disclosure 2, and the reconciliations are on record.

## (b) Are the claim's statements about prior art accurate?

Checked one by one (my fetches, all HTTP 200 unless noted):
1. Hub repository, no score file: confirmed and extended. I made a blobless fetch of all 17 branches and all 631 pull
   heads of CDCgov/rsv-forecast-hub (648 refs). No path in any ref or in history matches score/eval/wis/leaderboard/
   metric/summary. The only report-like path is model-output/Google_SAI-RSVEns/Google_SAI-RSVEns_2026-02-11_forecast_report.pdf,
   which is a team's mid-season forecast report, not a season score set.
2. Hub #294 / #295 / #515: #294 ("Send a dispatch to internal webpage for scoring RSVHub") and #515 ("End of season
   close out tasks", including "Update scoring and internal visualization dashboard") are issues, as stated. #295 is
   not an issue: https://github.com/CDCgov/rsv-forecast-hub/issues/295 answered 302, and
   https://github.com/CDCgov/rsv-forecast-hub/pull/295 (HTTP 200) is the merged pull request "add internal reports
   dispatch" ("Facilitates auto scoring of RSVHub and internal webage update"). The substance (scoring for an internal
   CDC page) is accurate. Only the label is wrong: "issues #294, #295 and #515" should read "issues #294 and #515 and
   pull request #295". This is non-material and does not concern what any third-party score set contains.
3. hubverse hub list (https://hubverse.io/community/hubs.html, 2026-11-13T05:46:07Z): the RSV Forecast Hub entry has
   repo CDCgov/rsv-forecast-hub and no forecasts/evals link. The COVID-19 hub entry has evals
   reichlab.io/covidhub-dashboard/eval.html. Confirmed. None of these candidate dashboard repositories exists
   (git ls-remote answered "Repository not found"): CDCgov/rsv-forecast-hub-dashboard,
   reichlab/rsv-forecast-hub-dashboard, hubverse-org/rsv-forecast-hub-dashboard, reichlab/rsvhub-dashboard,
   reichlab/rsv-dashboard, CDCgov/rsv-forecast-hub-reports, CDCgov/forecast-hub-reports, CDCgov/hub-dashboard.
4. arXiv 2605.16238: the abs page (2026-11-13T05:45:59Z) lists v1 and v2, with v2 the latest. Confirmed.
   sarahmart/epi-hub-analysis: HEAD is still 2294a6331e6317059b49b20da893a86b2f0751dd, the only branch, no pulls.
   - data/season_summaries/rsv_summary.csv (fetched) holds the four Table 6 rows at full precision: Google 14.65155295,
     RSVHub-ensemble 16.40276131, CEPH 19.75763996, baseline 18.34533023, each on 4,576 tasks. These match
     object/p3_reconcile_epi_hub_analysis.txt and Table 6 (14.7/16.4/19.8/18.3).
   - data/processed/rsv/forecasts_manifest.txt (fetched) lists only .csv files from 8 directories. These are the 7 hosp
     directories plus CFA_Pyrenew-Pyrenew_E_RSV (ED only), with no UGA_flucast-INFLAenza file. This is consistent with
     the claim's ".csv only" explanation.
   - Not named by the claim, and not new prior art for the cell:
     - rsv_analysis.ipynb outputs and figures/hubs/rsv/*.png: summaries of the same row-level file.
     - data/model_inventories/rsv_inventory.csv: validation/test scores of Google's replicas of hub models, not of
       the hub submissions.
     - data/processed/google_rsv/: Google internal models.
5. ACCIDDA/EpiBenchmark main ddcc507: I fetched rsv25-26_complete-model-scores.parquet and confirmed its contents:
   - 11,648 rows: RSVHub-ensemble 5,824 and RSVHub-baseline 5,824.
   - 28 reference dates 2025-11-22..2026-05-30, 52 locations, horizons 0-3.
   - Published means 26.688404 (ensemble) and 32.291779 (baseline).
   The challenge JSON gives quantiles 0.025/0.25/0.5/0.75/0.975 and complete_models [RSVHub-ensemble]. The blob
   4300c200 was added in 1eacf63 (2026-09-24, "bundle score files of complete models"). All as stated.
   - Not in the claim: branch prop-ed-challenges (f69071a, 2026-11-12) holds the same blob renamed
     rsv25-26_inchosp_complete-model-scores.parquet. It also adds epb_rsv_proped_2025-2026_dev, whose JSON names
     complete_models [RSVHub-ensemble, UGA_flucast-INFLAenza] with complete_model_scores_file "TODO". No RSV ED score
     file is published there yet; a future one would add ED overlap for those two directories only.
   - The historical root file EpiBench_scores.csv (66c6212, 2026-06-12; removed 2026-06-23) is flu only.
   - I searched all 47 refs (heads and pull heads); none has any other RSV score file.
6. ACCIDDA/tapestry (refs: main 0650821, restructure/unified-model 6546e06, pull/1 cf1091e). ACCIDDA/chromantis
   serves the same SHAs, confirmed.
   - 3a: leaderboard.csv at 6546e06 (fetched) has exactly 20 RSVHub-ensemble 2025-2026 rows (hosp/ED x states_dc/US
     x all/0-3; e.g. hosp states_dc all 5,916 tasks, 16.014231). No other hub directory appears. Confirmed.
   - 3b: manifest.json at 6546e06 (fetched) holds 29.00743753 / 40.80432946 (5,824) and 0.0008238110399796562 /
     0.0009037065454683935 (5,350). For the RSV cases the only eligible hub competitor is UGA_flucast-INFLAenza.
     Confirmed.
   - 3c: per-seed.csv and results.md on main (fetched) hold pooled Google_SAI-RSVEns natural WIS 15.39366298787946 on
     4,692 tasks and the ratio 0.967110 vs RSVHub-ensemble. Confirmed.
   - Not named by the claim (the claim makes no completeness statement, and these add no new directory, target or
     task coverage):
     - docs/experiments/nowcast-overnight-20261005/rsv-component-target-scores-2025-2026.csv on main, plus its
       half-errors variants. These hold RSVHub-ensemble summed WIS for both targets by geography (all 6,032/5,586
       units, states_dc, US) next to tapestry's own configurations.
     - The deleted docs/results/b0-comparison/rsv_rsv_*_2025-2026.md and docs/assets/b0_configuration_comparison/leaderboard.csv
       (last at bd27a66, 2026-09-14). These hold tapestry configurations' WIS ratios to the ensemble.
     - production/submissions/2026-10-* "medians-vs-hub-models" files, which belong to the 2026-27 season.
7. Zenodo 10.5281/zenodo.22988800: the versions API shows a single version (2026-09-27) with
   timidity_zenodo_deposit_v7.zip, md5 f20da82557e7f38f9860df985d88ec1f. This is as stated.
8. CDCgov/cfa-forecast-hub-reports (all heads and pulls, blobless): its RSV paths are only weekly-summaries
   (forecasts_data, map_data, target_data and webtext) and config/rsv-forecast-hub/*.toml. It has no score or
   evaluation file. Confirmed.

Statements about prior art are accurate in substance, with one non-material mislabel (#295 is a pull request).

## Other sources checked (nothing that covers the cell)

- This repo copy (pinned commit cf68067): TROPHY_CASE.md and known-knowns/ have no RSV or forecast-hub entry.
- Upstream github.com/elder-plinius/V3R1T4S: I made a blobless fetch of main and all pull heads (1,031 refs). The only
  RSV path is known-unknowns/disease-research/rsv-hub-retrospective-beat-ensemble-wis.md (added 371938d, 2026-10-15),
  and no commit message mentions RSV. I also fetched the web searches pulls?q=is:pr+rsv and issues?q=rsv (HTTP 200).
  Each had one hit, #399, an unrelated bank PR. No claim for this target exists upstream.
- CDCgov/cfa-stf-routine-forecasting (formerly pyrenew-hew), all heads: score code only, no RSV score data.
- Hub forks jcblemai/, kayodeoshinubi/ and nikosbosse/rsv-forecast-hub (git ls-remote): submission branches only.
  nikosbosse is the 2024-25 HopkinsIDD hub.
- Hugging Face API (all three requests HTTP 200):
  - datasets?search=rsv (38 results): only EPI-Eval/rsv-forecast-hub (target data) and
    EPI-Eval/rsv-forecast-hub-predictions are related.
  - datasets?author=EPI-Eval: the same two.
  - EPI-Eval/rsv-forecast-hub-predictions tree (README and .gitattributes only, no data) and its README: a community
    submission shell, no scores.
- Zenodo search API: q=RSVHub (0 hits), q="rsv-forecast-hub" (0), q="forecast hub" AND RSV (1: 22988800),
  q="weighted interval score" AND RSV (1: 22988800).
- Web searches (last 24 months; general and restricted to cdc.gov and to medrxiv/arxiv/biorxiv/osf/ssrn/researchsquare):
  - The only RSV 2025-26 per-model scores are arXiv 2605.16238.
  - CDC publishes a FluSight 2025-2026 evaluation but no RSV evaluation page appeared. The CDC RSV page is described as
    forecasts and model lists, with forecasts ended 2026-06-05 for the season.
  - Also seen and not relevant: the CDC 2025-26 season outlook evaluation (qualitative), the RespiCast, FluSight and
    German hub papers (other hubs), medRxiv 2026.10.09.26364706 (influenza), arXiv 2509.21191 (methods) and the
    AI4Casting RVDSS hub (Canada).
- Neighbouring cells: the HopkinsIDD hub (2023-24/2024-25) and the COVID/flu hubs are different hubs or seasons. They
  cannot yield this hub's 2025-26 per-model values.

## Non-200 and blocked fetches (exact URLs, no retries)

- 403: https://www.cdc.gov/cfa-modeling-and-forecasting/rsv-data-vis/index.html (2026-11-13T05:46:03Z). This is a
  block; I did not read the page and did not retry. Search-engine summaries describe it as forecasts and model lists
  without evaluation, but I could not verify that directly.
- 302 (redirect, not followed): https://github.com/CDCgov/rsv-forecast-hub/issues/295 (2026-11-13T05:48:34Z). The
  separate page https://github.com/CDCgov/rsv-forecast-hub/pull/295 returned 200.
- 404: https://raw.githubusercontent.com/ACCIDDA/EpiBenchmark/ddcc507e53027dbac5520396e5a9d9e7097cf355/EpiBench_scores.csv
  (the file is not at that commit; it was fetched at its own commit 66c6212798806f24bfe9240484786cf36c6852c4, HTTP 200,
  flu only).
- 400 (my request error, page size above 25, not a block; each re-issued once with size=25 and answered 200):
  - https://zenodo.org/api/records?q=RSVHub&size=50&sort=mostrecent
  - https://zenodo.org/api/records?q=%22rsv-forecast-hub%22&size=50&sort=mostrecent
  - https://zenodo.org/api/records?q=%22RSV%20forecast%20hub%22%202025&size=50&sort=mostrecent
- "Repository not found" via git ls-remote: the eight candidate dashboard/report repositories listed in (b)3.

## Residual risks (stated, not disqualifying)

- The CDC RSV page could not be read (403). CDC's own scoring is described as internal (#294, #295, #515), and no
  public CDC RSV evaluation was indexed.
- EpiBenchmark's RSV ED challenge has a pending ("TODO") complete-model score file. If it is published, it would cover
  RSVHub-ensemble and UGA_flucast-INFLAenza ED on 5 levels only. It would not cover the cell.
- Recommended text fix before publication: call #295 a pull request.

novelty: the object is new for its cell. The prior-art statements are accurate in substance, with one non-material
mislabel (#295 is a pull request, not an issue).
pass: true
