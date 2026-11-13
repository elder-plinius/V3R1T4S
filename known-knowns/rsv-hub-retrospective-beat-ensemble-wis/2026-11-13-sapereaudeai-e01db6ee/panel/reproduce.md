# REPRODUCE skeptic: rsv-hub-retrospective-beat-ensemble-wis, partial win p3 (run 2026-11-13-0523)

context: subagent (Claude Code Agent tool, subagent_type reproduce)

Started 2026-11-13T05:34:14Z, finished 2026-11-13T05:45Z (times from `date -u`). All work was done on a copy of
claim/ in the panel work folder (work_reproduce/claim). Python: the venv interpreter run with `-I`, 2 threads.
My own scripts: work_reproduce/my_score.py (scorer), work_reproduce/my_checks.py (claim numbers and third-party
reconciliations), work_reproduce/google_abs.py, work_reproduce/extra.py, work_reproduce/cmp_table.py. I wrote
my_score.py and my_checks.py before reading claim/code/ or claim/code_reconcile/. I ran the author's scripts only
as REPRODUCE.md says, and looked at claim/code/p3_recompute.py only after my table matched (to see its file filter).

## Definition used by my checker (quoted in my_score.py)

Bracher et al. 2021 (PLoS Comput Biol 17(2):e1008618), eq. 3, which is what scoringutils::wis() computes by default
(weigh = TRUE, count_median_twice = FALSE) and what hubEvals calls:
"WIS_{alpha_{0:K}}(F, y) = 1/(K + 1/2) * ( w_0 * |y - m| + sum_{k=1..K} w_k * IS_{alpha_k}(F, y) )", with w_0 = 1/2 and
w_k = alpha_k/2, and "IS_alpha(F, y) = (u - l) + 2/alpha * (l - y) * 1(y < l) + 2/alpha * (y - u) * 1(y > u)".
On the hub's 23 levels this gives K = 11 central intervals (alpha 0.02, 0.05, 0.1, 0.2, ..., 0.9). I used the interval
form (not the pinball form). ae_median = |y - m|; 50%/95% coverage = 1(q0.25 <= y <= q0.75) and
1(q0.025 <= y <= q0.975). Pairwise relative WIS (scoringutils): ratio = mean WIS of A / mean WIS of B on the tasks both
have (full task id: reference_date, location, horizon, target_end_date; per target); relative skill = geometric mean
of A's ratios against all models including itself (ratio 1), divided by RSVHub-baseline's. The 5-level WIS used for
EpiBenchmark is the same formula on 0.025, 0.25, 0.5, 0.75, 0.975 (K = 2).

## 1. The object, recomputed independently

my_score.py read every file in claim data/hub/model-output (reference date 2025-09-20..2026-05-30 by file name), kept
quantile rows, pivoted to 23 levels per (model, target, reference_date, location, horizon, target_end_date), joined
the oracle-output quantile rows on (target, location, target_end_date), and aggregated. Output:

    in-season files read: 247; model dirs: 9
    duplicate (model,target,task,level) rows: 0
    levels outside the 23: []
    oracle quantile rows 5145, non-missing 5140, dup keys 0
    oracle quantile vs sample rows: 5145 keys, identical value 5145
    wk inc rsv hosp: tasks 38728, complete 23-level tasks 38728
    wk inc rsv hosp: tasks without oracle 0
    wk inc rsv prop ed visits: tasks 26103, complete 23-level tasks 26103
    wk inc rsv prop ed visits: tasks without oracle 0

Comparison with object/p3_table.csv (13 rows x 16 columns; every row and column):

    rows obj 13 mine 13 join {'both': 13, 'left_only': 0, 'right_only': 0}
    n_tasks, n_dates, n_locations: max rel diff 0; first_date, last_date, horizons: 0 string mismatches
    mean_wis 2.4e-10, mae 3.8e-10, cov50 9.5e-11, cov95 5.4e-11, share_of_ens_tasks 8.7e-11,
    mean_wis_on_ens_tasks 2.4e-10, ens_mean_wis_same_tasks 2.2e-10, rel_wis_pairwise_vs_baseline 2.7e-10 (max rel diff)
    object cells compared as %.10g strings: 182, differing: 0

So all 182 numeric and text cells of the table equal my values printed to the object's 10 significant digits.

## 2. Every number and rule in the claim sentence and the disclosures (my_checks.py, extra.py, google_abs.py)

- 247 files (219 .csv, 28 .parquet, all 28 parquet are UGA_flucast-INFLAenza) in 9 directories; 8 hosp and 5 ED
  directories; 38,728 hosp and 26,103 ED tasks. Confirmed.
- Mis-dated rows: the only tasks whose target_end_date is not reference_date + 7 x horizon are
  `('RSVHub-ensemble', ED, 2025-09-27 file, -1 week): 250` and `('UGA_flucast-INFLAenza', ED, 2025-09-27 file, -1 week): 250`
  (500 in total). Ensemble ED 2025-09-27: 344 tasks, 184 share a (reference_date, location, horizon) with another task.
  Confirmed.
- ED ensemble sensitivity: `all 6382 0.000887532; consistent 6132 0.000918589; drop file 2025-09-27 6038 0.000931546`.
  Matches disclosure 6 and object/p3_exclusions.txt.
- Ensemble: 29 files per target, horizon -1 on 12 reference dates; RSVHub-baseline's only date without an ensemble
  file is 2025-09-20. Confirmed.
- Table 6 subset (52 jurisdictions without US, horizons 0-3, 2026-01-03..2026-05-30): all 8 lines of
  object/p3_era_subset.txt reproduce (e.g. RSVHub-ensemble 4576 tasks, 22 dates, 16.422 / 25.29 / 0.874;
  Google_SAI-RSVEns 14.635 / 21.15 / 0.849; UGA_flucast-INFLAenza 22.657). The published Table 6 values quoted there
  (14.7, 21.2, 85%; 16.4, 25.3, 87%; 19.8, 28.4, 78%; 18.3, 27.8, 93%) match the arXiv 2605.16238 v2 HTML I fetched.
- UGA_flucast-INFLAenza and RSVHub-ensemble hosp units at horizons 0-3: `5936 PR: 112 non-PR: 5824`. Confirmed.
- Truth vintage (disclosure 3): `oracle non-missing quantile rows 5140 found in 2026-11-12 vintage 5140 equal 5140`;
  2026-11-04 vs 2026-11-12, target_end_date 2025-09-13..2026-06-20: 4305 rows, 50 changed (43 hosp, 7 ED), changed
  range 2025-11-29..2026-06-20; largest vs 11-04 value: hosp, 48, 2026-06-13, 41 -> 46, 0.1220 (0.1087 of the 11-12
  value); largest vs 11-12 value: ED, 19, 2026-06-06, 0.1373. All confirmed.
- Self-ratio convention (disclosure 7): dropping the self-ratio changes the scaled relative WIS by up to 4.07%
  (UGA_flucast-INFLAenza, ED); "up to about 4%" is right. baseline/wis.py is byte-identical to code/wis.py (cmp).
- data/ext/load_hub.py (third-party loader) has `if not path.endswith(".csv"): return False` in keep_forecast_file,
  which explains UGA_flucast-INFLAenza's absence from the epi-hub-analysis rows. Confirmed.

## 3. Third-party reconciliations, recomputed with my scorer

(i) epi-hub-analysis data/ext/scores.parquet: 26,248 rows, 7 models, 22 dates 2026-01-03..2026-05-30, 0 rows without a
hub forecast; `max |my WIS(their truth) - their wis| = 9.095e-13 over 26248 rows`; their truth differs from the
pinned oracle on 171 of 1,378 (location, target_end_date) pairs. Per model on the summary set (52 jurisdictions,
horizons 0-3), their mean WIS equals data/ext/rsv_summary.csv for the four Table 6 rows (19.75763996, 14.65155295,
18.34533023, 16.40276131); pinned-oracle minus their-truth differences: max 0.1008 (CFA_Pyrenew-Pyrenew_H_RSV), max
0.0463 over the four Table 6 rows. Matches the claim ("at most 0.101"; "at most 0.046").

(ii) EpiBenchmark: 11,648 rows (5,824 per model), 28 dates, 52 locations, horizons 0-3; 5-level WIS with truth =
time-series as_of 2026-09-16: `max |diff| = 9.095e-13`. Means: ensemble published 26.688404, mine 26.688404, 5-level
pinned 26.743111, 23-level pinned 29.194413 (disclosure 2: 26.688 / 26.743 / 29.194). Confirmed.

(iii-a) tapestry leaderboard, 20 RSVHub-ensemble 2025-2026 rows, truth as_of 2026-09-02, horizons 0-3, date-consistent
rows only, states_dc = without US and 72: all 20 n values equal, `max rel diff 1.232e-13` (max abs 2.3e-13).

(iii-b) tapestry hub-evaluation (manifest.json): common units without location 72, date-consistent, horizons 0-3:
hosp 5824 units, ensemble 29.007437532995738, UGA 40.804329461299567 (manifest 29.007437532995738,
40.80432946129957); ED 5350 units, 0.00082381103997968832 / 0.00090370654546843734 (manifest 0.0008238110399796562,
0.0009037065454683935). Equal to the last digit.

(iii-c) tapestry Google comparison: 4,692 common hosp tasks (51 states+DC, horizons 0-3, 23 dates from 2025-12-27);
pooled Google_SAI-RSVEns 15.393662987879464 (published 15.39366298787946); all 51 per-location sums of both models
match for every scope/seed block of native-location-scores.csv: max abs diff 9.1e-13 (google) and 9.1e-13
(ensemble), max rel diff 2.1e-16 / 1.9e-16.

## 4. REPRODUCE.md run exactly (work_reproduce/run_repro.sh, log work_reproduce/repro_log.txt)

    e01db6ee9d55baf24c06fa801c2fdfee27d9c1f70d1d513b9e98b75bd6d2f804 *out_check/p3_table.csv
    9fceead7ca155ecbb985cd6bd3a5a3b86884699098d383d4fb900443b3337a0a *out_check/p3_exclusions.txt
    9cf68a4e80e931837ba295356b044a39940539b15a4b082d8155208f154f6ace *out_check/p3_era_subset.txt
    74257bac5ab80b7053d436dcac5d6f1107d466bab72a03095ec6bfe8ef4e63e9 *out_check/p3_reconcile_epi_hub_analysis.txt
    DONE          (no DIFF line for the 7 record files)
    e65e96e9...c387 reconcile_epibenchmark, 257e8713...6fd5 reconcile_tapestry, d8db2a84...07cb5 reconcile_tapestry_ed_rule,
    2c27682e...9475 reconcile_tapestry_hubeval, 0458030c...4788 reconcile_tapestry_google, cdcf2993...86c1 truth_revisions

All four object hashes and all six stated record hashes match REPRODUCE.md and object/ / record/; every script
exited 0. The baseline console output is identical to baseline/era_reproduction_rerun.txt (diff empty; 4 WITHIN
lines). Determinism: a second run of code/p3_recompute.py into another folder gave the same three sha256 values. No
output contains a CR byte (LF only, disclosure 8). The object/ and record/ files of my copy hash the same as claim/.

## 5. Inputs

- `sha256sum -c` on data/SHA256SUMS_hub_files.txt: 250 of 250 OK, and the file list equals data/hub exactly;
  data/SHA256SUMS_ext_files.txt: 3 of 3 OK; data/SHA256SUMS_ext2_files.txt: 11 of 11 OK.
- Against the public sources, via git blob hashes (`git hash-object --no-filters` on the local files vs
  `git ls-tree -r` of blobless depth-1 fetches; no blob contents were read):
  CDCgov/rsv-forecast-hub e947ca8: 250 of 250 hub files blob-equal. `git ls-remote` (05:39:58Z): HEAD = main =
  1985aee45bca6b655e22b8bc2096b515bd6327f2; the trees of e947ca8 and 1985aee differ only by the added
  model-output/UM-DeepOutbreak/2026-11-14-UM-DeepOutbreak.csv, so every input is unchanged at the live head. 25
  model-output directories; 247 files dated 2025-09-01..2026-08-31, all inside 2025-09-20..2026-05-30, in 9
  directories with the per-directory counts of data/hub; no path matching score|eval|wis|summary.
  sarahmart/epi-hub-analysis 2294a63 (still HEAD): scores.parquet, rsv_summary.csv, src/load_hub.py MATCH.
  ACCIDDA/EpiBenchmark ddcc507 (still main): the parquet (blob 4300c200...) and the json MATCH.
  ACCIDDA/tapestry 6546e066 (still restructure/unified-model): leaderboard.csv, hub-evaluation.md, manifest.json MATCH;
  06508218 (still main): the 6 copied google-comparison files MATCH, and the folder lists the 10 files named in
  record/published_table.md.
- One plain request to https://arxiv.org/html/2605.16238v2 (05:43:28Z): HTTP 200; Table 6 RSV rows and the start of
  Supplementary Table 7 agree with object/p3_era_subset.txt and record/arxiv_supp_table7.txt.

## Mismatches

None found in any value, count, rule, hash or input.

Notes (not counted as mismatches):
1. The claim says each third-party set was "reproduced within 1e-12" without saying absolute or relative.
   record/reconcile_tapestry_google.txt reports an absolute max |diff| of 1.82e-12 for the ensemble per-location
   sums (values up to about 9,077, so about 2e-16 relative). My independent scorer reproduces those sums within
   9.1e-13 absolute, and every other set within 9.1e-13 absolute or 1.3e-13 relative, so the sentence is true as a
   statement about reproducibility. Adding "(relative)" or printing relative differences in that record would
   remove the ambiguity.
2. With `python -I`, PYTHONDONTWRITEBYTECODE is ignored, so the REPRODUCE commands write __pycache__ folders into
   code/, code_reconcile/ and baseline/. I removed them from my copy. This does not affect any output.
3. Not checked: record/zenodo_22988800_scan.txt (not fetched), the status-page byte hash in record/status_source.md
   (I used git ls-remote and trees instead), the predecessors of the CRLF -> LF change (not in the package), and the
   "Released" clause (a criterion question, disclosure 5).

No fetch was refused or blocked. The background process I started (PID logged in work_reproduce/pids.txt) has
ended.

pass: true
