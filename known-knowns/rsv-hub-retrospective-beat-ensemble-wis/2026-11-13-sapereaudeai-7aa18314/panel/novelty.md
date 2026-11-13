# Novelty skeptic: rsv-hub-retrospective-beat-ensemble-wis (route (a), HopkinsIDD hub, season 2024-25)

context: subagent (Claude Code Agent tool, subagent_type novelty, fresh context)

Claim under test (claim/CLAIM.md): frozen as-of forecasts V3R1T4S-asofKA have season-average WIS 72.2386 against the
HopkinsIDD hub-ensemble's 99.7021 on all 3,065 scored tasks of the 14 non-empty 2024-25 hub-ensemble files
(rel -27.55%, 90% interval [-35.78%, -19.84%]), hub commit 6bf251ac3fc798e55ed95d0b7269f5f5781c0207.
Read: claim/CLAIM.md, claim/target.md, claim/scout.md, plus DISCLOSURES.md (including item 8, added
2026-11-13T02:09:50Z after the panel started, and its log attempts/evaluator/test/score_2023-24_descriptive.log),
PREREG*.md, REPRODUCE.md, baseline/. Nothing in claim/ was modified. Working files: panel/work_novelty/.

## 1. Status source (one honest request, no retry)

- URL: https://github.com/CDCgov/rsv-forecast-hub/tree/main/model-output/RSVHub-ensemble
- Time: 2026-11-13T02:06:47Z, HTTP 200, one curl with a User-Agent naming V3R1T4S; saved as
  panel/work_novelty/status_RSVHub-ensemble_tree.html (sha256 36225d25acdc63322a5b66f04e8fcc42077ba255612bbc1978ad483b36647eb3).
- Value read: 36 files listed ("totalCount":36), 2025-09-27-RSVHub-ensemble.csv ... 2026-11-07-RSVHub-ensemble.csv;
  only model-output CSVs, no scores file. Same count as the scout's fetch at 01:04:37Z. Status: OPEN.

## 2. Route (a) comparator unchanged upstream

- GitHub tree API, HopkinsIDD/rsv-forecast-hub main, recursive: 2026-11-13T02:07:03Z HTTP 200. Tree sha
  6bf251ac3fc798e55ed95d0b7269f5f5781c0207 (the pinned commit), 613 entries, not truncated. Compared with
  claim/data/hopkins/tree_main.json: no path added, removed or changed.
- Latest main commits (02:07:06Z, HTTP 200): head 6bf251ac at 2026-06-05T10:27:50Z "Update target data"; nothing after it.
- The 15 2024-25 files in model-output/hub-ensemble (2024-10-27 ... 2025-02-16, 2025-04-06) have the same git blob SHAs as the claim's tree.
- I computed git blob SHA-1s of the claim's local copies myself: all 300 model-output files and
  target-data/2026-06-05_rsvnet_hospitalization.csv match the live tree (301 of 301; only model-output/README.md not stored locally).
- Branches (02:07:56Z, HTTP 200): main plus 4 side branches; their heads (gh api, 02:08:31-02:08:41Z) are 2024-07..2025-03
  workflow fixes or a file deletion, with no scores.
- Releases: HopkinsIDD hub `[]` (02:07:09Z, HTTP 200); CDCgov hub `[]` (02:07:46Z, HTTP 200). There are no release assets.
- No score, evaluation, WIS or metric path exists in either hub's main tree:
  - HopkinsIDD: 613 entries.
  - CDCgov: tree e947ca8f, 501 entries, 02:07:42Z, HTTP 200.
  - So, as the bank says, no scores file has appeared, and the bar stays the recomputed hub-ensemble value.

## 3. Other places that might publish season scores

- HopkinsIDD dashboard https://hopkinsidd.github.io/rsv-forecast-hub_website/ (redirects to https://rsvforecasthub.org/):
  02:09:02Z, HTTP 200. The "Evaluation" section contains only commented-out scoringutils code and no numbers.
- Website repo HopkinsIDD/rsv-forecast-hub_website, tree via gh api at 02:08:51Z: 115 paths. They are archived forecast
  HTML pages, with no score or eval file.
- hubverse hub list https://hubverse.io/community/hubs.html: 02:14:11Z, HTTP 200. It lists "Archival US RSV Forecast Hub
  2024-2025" (HopkinsIDD) and "RSV Forecast Hub" (CDCgov), and gives no Evaluations link for either.
- HopkinsIDD org repositories (02:08:02Z, HTTP 200): only rsv-forecast-hub and rsv-forecast-hub_website relate to RSV.
- CDCgov/cfa-forecast-hub-reports (gh api tree, 02:18:58Z): RSV weekly summaries start at 2025-09-27 and cover the CDCgov
  hub only. Nothing covers HopkinsIDD or RSV-NET.
- CDCgov/hubhelpr (02:19:00Z): no RSV files.
- Forks and related repositories checked (gh api trees, 02:13:41-02:19:11Z): none publishes 2024-25 HopkinsIDD season scores.
  - paulocv/rsv-forecast-hub-legacy: data copies, no scores.
  - predsci/rsv-forecast-hub: the 2023-24 hub.
  - Metaculus/rsv-forecast-hub and Metaculus/respiratory-diseases: no score or eval files.
  - xairu23/sentinel: CDCgov hubs.
  - seabbs/MultiHubForecastExperiments: RSV excluded, with no RSV results in its reports.
  - ACCIDDA/chromantis: its RSV scores are 2025-2026 CDCgov targets (wk inc rsv hosp, wk inc rsv prop ed visits), and RSV-NET is used only as a covariate.
- sarahmart/epi-hub-analysis (gh api, 02:13:43-02:13:58Z): data/season_summaries/rsv_summary.csv covers the CDCgov
  RSVHub, 2025-26 season, 4,576 tasks. Google_SAI-RSVEns has mean WIS 14.65 against RSVHub-ensemble's 16.40 (relative WIS 0.86).
  This is route (b)'s hub, target (NHSN) and season, a neighbouring cell and not this one. It is a prospective submission.
- GitHub searches:
  - `gh search repos "rsv-forecast-hub"` (02:14:34Z) returned 7 repositories, all listed above or test copies.
  - `gh search code "rsvnet_hospitalization hub-ensemble"` and `"rsvnet_hospitalization wis"` returned no hits.
  - `gh search code "HopkinsIDD/rsv-forecast-hub"` (02:14:56Z) found only hub-list, registry and catalogue references (checked above).

## 4. Literature, last 24 months

Searches ran with the WebSearch and WebFetch tools at about 02:11-02:18Z. The tool reports no exact times; every fetch
returned page content.

- WebSearch queries:
  - "US RSV Forecast Hub 2024-2025 season evaluation ensemble weighted interval score"
  - "\"RSV Forecast Hub\" Hopkins collaborative forecasting RSV-NET hospitalizations paper"
  - "retrospective RSV hospitalization forecast RSV-NET age groups outperforms ensemble WIS 2025"
  - "Columbia SVIRS RSV forecast ... 2024-25 forecast accuracy WIS"
  - "medRxiv 2025 RSV forecasting United States RSV-NET probabilistic forecasts evaluation hub ensemble"
  - "\"rsv-forecast-hub\" scores OR evaluation OR \"relative WIS\" github"
  - "Google \"AI system\" empirical software RSV forecasting hub ensemble retrospective WIS"
  - "\"RSV\" forecast hub retrospective model beats hub ensemble 2024-2025 ... preprint 2026"
  - "Roosa Truelove Lessler RSV forecast hub multi-model forecasts evaluation 2023-2025"
  - "Metaculus RSV forecast hub 2024-25 performance compared hub ensemble WIS"
  - "age-stratified RSV hospitalization forecasts RSV-NET 2024-25 ... weighted interval score nowcast reporting delay"
- Result: no paper, preprint, dashboard or CDC page gives season WIS for the HopkinsIDD RSV hub's 2024-25 season. None
  reports a forecaster, retrospective or real-time, that beats its hub-ensemble on its task set.
- Nearest items:
  - https://arxiv.org/abs/2605.16238 and https://arxiv.org/html/2605.16238 (Martinson et al., ERA, v2 2026-10-14), read
    in two parts via offset. RSV covers only the CDCgov RSVHub, NHSN target, 2025-26 season, prospective
    (relative WIS 0.87 vs RSVHub-ensemble). Its RSV validation window 2024-10-01..2025-07-01 is on NHSN HRD data, not
    RSV-NET or the HopkinsIDD hub. The HopkinsIDD hub and RSV-NET are not mentioned.
  - https://arxiv.org/abs/2509.21191 (Dudley and Eisenberg): COVID-19 only, no RSV numbers.
  - https://arxiv.org/abs/2608.05883 (Bracher and Funk, 2026-08-06): revision leakage in retrospective forecasts,
    COVID-19 (ERA), no RSV. It is relevant to the other skeptics as a known critique of retrospective-beats-ensemble
    claims. Compare DISCLOSURES item 4: scored against the first report, ours is worse (rel +0.2627).
  - medRxiv 2025.01.08.25320187 (MPOG-Ensemble): forecasts RSV-NET for 12 states. Its RSV MAE is reported in rates, it
    states that no official RSV ensemble was available for comparison, and it uses no hub WIS (search abstract only;
    the scout recorded a 403 on the full text, not retried).
  - PLOS Comp Biol 10.1371/journal.pcbi.1014644: England, a different system.
  - medRxiv 10.64898/2026.07.20.26358471: Germany, RESPINOW.

## 5. V3R1T4S repository (read-only gh CLI)

- TROPHY_CASE.md (blob 18b731d7, 31,306 bytes, 02:09:52Z): no RSV, forecast-hub or WIS entry.
- Repository tree at HEAD fb516440 (2026-11-09T19:54:43Z; 7,438 paths, not truncated, 02:10:02Z):
  - known-knowns/ has no RSV entry. The only forecast-named entry is robust-forecast-aggregation-bounds, a different problem.
  - known-unknowns/disease-research/rsv-hub-retrospective-beat-ensemble-wis.md is the open target page: "open as of 2026-10-15", no scores file.
- bank/targets.json (02:19:20Z): the entry rsv-hub-retrospective-beat-ensemble-wis has status_checked 2026-10-15 and is
  still in the bank, disclosure open.
- Pull requests and issues:
  - `gh pr list --state all --search` for "rsv", "rsv-hub-retrospective-beat-ensemble-wis", "RSV forecast",
    "hub-ensemble" and "respiratory syncytial" (02:10:24-02:10:34Z).
  - Full title list of 1,000 PRs (02:10:44Z).
  - `search/issues` for "repo:elder-plinius/V3R1T4S rsv" (1 hit) and "\"rsv-forecast-hub\"" (0 hits).
  - The only hit is #399, a closed bank-maintenance PR whose body notes "the CDC RSV ensemble has the 33 files ...". It is not a claim.
  - #569 (immrep22) matched "hub-ensemble" only through search noise.
  - Result: no open or closed PR or issue claims this target or a competing result.

## 6. Comparison with the published objects of the cell and its neighbours

I wrote my own code: panel/work_novelty/code/novelty_compare.py and stratum_select.py, outputs out_novelty_compare.txt and out_stratum_select.txt.
- WIS: interval form, weigh = TRUE, median counted once.
- Truth: the hub's current target file, with 0-0.99, 1-4 and 5-64 as sums of their finer groups.

It reproduces the claim exactly: ensemble 99.7021, ours 72.2386, 3,065 tasks, 14 dates, ours covers 3,065 of 3,065.

Each published 2024-25 model on its overlap with the hub-ensemble task set. No published model covers the whole set.

| model | tasks | model WIS | ensemble WIS | ours WIS |
|---|---|---|---|---|
| CEPH-Rtrend_rsv (0-130 only) | 980 | **123.32** | 179.77 | 126.82 |
| CU-RSV_SVIRS | 2,780 | 110.57 | 106.65 | 74.76 |
| JHU_CSSE-RSV | 666 | 318.15 | 212.03 | 148.46 |
| Metaculus-cp | 36 | 2,004.35 | 2,139.33 | 1,292.10 |
| UGA_flucast-INFLAenza | 915 | 252.43 | 174.12 | 125.82 |
| UM-DeepOutbreak | 728 | 277.09 | 202.64 | 141.20 |
| hub-baseline | 434 | 242.37 | 178.35 | 118.35 |

Trivial edits and recombinations of published 2024-25 forecasts (restriction, relabelling, re-aggregation), all on the full 3,065-task set:

| published object | mean WIS |
|---|---|
| median of members | 102.61 |
| mean of members, recomputed | 99.02 |
| mean of members without Metaculus-cp | 100.12 |
| CU-RSV_SVIRS, with the ensemble where CU is missing | 103.26 |
| CEPH where present, else CU, else the ensemble | 81.65 |
| hindsight best published model per age group | 81.65 |
| hindsight best per age group x location | 80.44 |
| hindsight best per age group x location x horizon | 80.30 |

Even with hindsight selection on the scored season, no published forecast reaches 72.2386. The only lower number is a
per-task oracle minimum that uses the truth for every task (71.59). It is not a forecast.

Seeding check: our quantiles are not a copy, rescale or shift of any published file.
- Values identical to a published model: 0.8%-7.4%, mostly zeros at low quantiles.
- Ratio of our quantiles to a published model's, between the 5th and 95th percentiles: from about 0.2-0.5 up to about 2.4-7.7.
- A grep of the forecaster code finds reads only of target-data/archive vintages and its own cache, with no model-output/ read.

Neighbouring cells, stated so that no wider claim is read into this one:
- All-ages (0-130) sub-cell of the ensemble tasks: the published real-time CEPH-Rtrend_rsv beats ours (123.32 vs 126.82, ours +2.8%).
- p1 is not met. The claim says so itself: on CEPH's own tasks ours is 108.10 against CEPH's 106.09.
- Season 2023-24 of the same hub (DISCLOSURES item 8): the frozen pipeline is worse than the 2023-24 hub-ensemble
  (rel +0.1861, 90% [-0.0507, +0.3181]). It is in-sample and descriptive, and the replication fails there. That bears on
  the criterion's thin-pool pitfall, not on novelty: no published object beats or ties the claimed cell.
- Route (b), CDCgov hub, 2025-26, NHSN target: Google_SAI-RSVEns beat RSVHub-ensemble (relative WIS 0.86-0.87; arXiv
  2605.16238 and sarahmart/epi-hub-analysis). That is a different hub, target and season, so it is neither a competitor
  for this cell nor a prior holder of it.

## 7. Verdict

The status source answered (HTTP 200, 36 files, no scores file), and the HopkinsIDD comparator is unchanged upstream.
- Blob-identical: tree 6bf251ac, all 15 2024-25 hub-ensemble files and the truth file.
- No hub scores file, release asset, dashboard evaluation, paper, preprint or repository gives a 2024-25 season score
  for this hub, or a forecaster that beats its hub-ensemble on these tasks.
- Nothing in the V3R1T4S repository (TROPHY_CASE.md, known-knowns/, PRs, issues) holds this result or a competing claim.
- On the claimed cell (every reference date, location, age group and horizon of the 2024-25 hub-ensemble, 3,065 scored
  tasks), 72.2386 is strictly below everything known:
  - the bar: hub-ensemble 99.7021;
  - every published model where it overlaps;
  - every trivial edit or hindsight recombination of published forecasts, best 80.30.

The result is new for this cell.
- This verdict covers novelty only. Whether the look-ahead discipline, the backfill correction against raw-data
  ensemble members, and the failure to replicate on 2023-24 satisfy the criterion is for the reproduce and criterion skeptics.
- The claim must not be widened to all-ages tasks or to "best forecaster": CEPH-Rtrend_rsv is better on 0-130, and p1 fails.

pass: true
