# REPRODUCE skeptic report: p3, reproducing the published Hospitalization Nowcast Hub evaluation

context: subagent (fresh context, Claude Code Agent tool)

Scope: I read only claim/CLAIM.md, claim/REPRODUCE.md, claim/data/, claim/baseline/, claim/reference_outputs/, and the claim/code/ scripts. I wrote my own checker before reading claim/code/p3_reproduce.py. My code and outputs are in panel/work_reproduce/ (relative to the run folder): mywis.py (the checker), truth_frozen.py, defcheck.py, rowcmp.py, fetch5.py, fetch_pub.py, scan.py, memwatch.py, and their logs.

## 1. Definition (quoted from the paper, fetched once from Europe PMC fullTextXML, HTTP 200, 162,139 bytes)

Wolffram et al. 2023, PLoS Comput Biol 19:e1011394, section 2.5, as given in the MathML of the XML:

> "For an interval [l, u] at the level (1 − α), α ∈ (0, 1), reaching from the α/2- to the (1−α/2)-quantile of the predictive distribution F, it is defined as
> (1) IS_α(F,y) = (u − l) + 2/α × (l − y) × 1(y < l) + 2/α × (y − u) × 1(y > u),
> where 1 is the indicator function and y is the realized value. [...] For N nested prediction intervals it is defined as
> (2) WIS(F,y) = 1/(2N+1) × ( |y − m| + Σ_{k=1}^{N} α_k × IS_{α_k}(F,y) ),
> where m is the predictive median and in our setting N = 3 and α1 = 0.5, α2 = 0.2, α3 = 0.05. We note that it is equivalent to the mean pinball loss across the respective quantile levels"

Published aggregation and rules (claim/data/evalrepo/, R code, used as documentation only):
- `qs <- function(q, y, alpha) { 2 * (as.numeric(y < q) - alpha) * (q - y) }`; `compute_wis` filters `type == "quantile"`, left-joins the 0.5-quantile value as `med` (`spread = score(value, med, ...)`, `overprediction = ifelse(med > truth, score - spread, 0)`, `underprediction = ifelse(med < truth, score - spread, 0)`), then `group_by(model) %>% summarize(... score = mean(score))`. So each cell is the mean over all quantile rows of the model at that level.
- Levels (`filter_data`): national is `location == "DE", age_group == "00+"`; states is `location != "DE", model != "ILM"`; age is `location == "DE", age_group != "00+", model != "RKI"`.
- `load_data(add_baseline=TRUE, shorten_names=TRUE, fix_data=TRUE, add_truth=TRUE, exclude_missing=TRUE, eval_date="2022-08-08")`: bind the KIT-frozen_baseline file; map `sort(unique(model))` onto SHORT_NAMES; then `fix_RKI`, `fix_epiforecasts`, `fix_ILM`, `fix_LMU`; then `anti_join` with the four `submission_check/fixed/*-missing.csv` lists; then left-join truth on (location, age_group, target_end_date = date).
- `load_truth`: `rowSums(across(starts_with("value")), na.rm = TRUE)`, then `sum_run(value, 7, na_pad = TRUE)` per (location, age_group), then `drop_na()`.

My implementation (panel/work_reproduce/mywis.py) re-implements this from the R text: the per-row score is 2(1{y<q} − τ)(q − y). Medians are joined as the R left_join would, so a key with several medians would weight its rows by the number of medians (none occurred). The cell is the row mean per level and model. `fix_RKI` replaces RKI rows with value > 1e6 or NA by the min over the same key's 0-day and −1-day rows, and the target becomes the max. `fix_epiforecasts` fills the 0.1 quantile from a normal through the sorted 0.025 and 0.25 values. I used a closed-form two-point fit because R is not available; the R code uses `get.norm.par`. `fix_ILM` and `fix_LMU` left-join the listed keys to claim/data/hub/updated_models/ files (ILM on location, age_group, target_end_date, target, type, quantile; LMU also on forecast_date). The exclusion is an anti-join on location, age_group, forecast_date, target_end_date, target, type, quantile. Only quantile rows are kept, because mean rows never enter `compute_wis` and every rule is keyed on `type`.

Definition self-check (defcheck.py, my own code): eq (2) implemented literally with eq (1) vs the row mean of qs over the 7 quantiles:
```
max |eq2 - row-mean qs| over 200000 random cases: 4.547473508864641e-13
hand example y=80: 25.857142857142858 25.857142857142858 25.857142857142858
```
(hand example: quantiles 10..70, y = 80: (40 + 0.5·140 + 0.2·240 + 0.05·460)/7 = 181/7.)

## 2. The 31 published cells (S2 = repair rules, then exclusion): mine vs claimed vs published

Published = claim/data/evalrepo/data_scores_wis_*.csv. I re-fetched these three files from raw.githubusercontent.com (dwolffram/hospitalization-nowcast-hub-evaluation, main), and their sha256 are identical (section 4). Claimed = claim/baseline/p3_S2_vs_published.csv. Mine = panel/work_reproduce/run3/my_ladder.csv. Relative differences in this table come from my CSV, which stores 12 significant digits, so they have a floor of about 1e-12. At full precision, inside the script, the 28 non-Epiforecasts cells have max |mine/published − 1| = 1.178e-13.

| level | model | published | claimed S2 | mine S2 | mine vs published | mine vs claimed | rows mine/claimed |
|---|---|---|---|---|---|---|---|
| national | Epiforecasts | 423.087782483 | 423.131410459 | 423.131410459 | +1.031e-04 | -2.847e-13 | 32137/32137 |
| national | ILM | 142.629049071 | 142.629049071 | 142.629049071 | -1.150e-12 | -1.150e-12 | 32137/32137 |
| national | KIT | 256.110167408 | 256.110167408 | 256.110167408 | -1.106e-12 | -1.106e-12 | 32137/32137 |
| national | KIT-frozen_baseline | 1572.717272925 | 1572.717272925 | 1572.717272930 | +2.996e-12 | +2.996e-12 | 32137/32137 |
| national | LMU | 465.845662787 | 465.845662787 | 465.845662787 | -9.472e-13 | -9.474e-13 | 32137/32137 |
| national | MeanEnsemble | 259.594450322 | 259.594450322 | 259.594450322 | -2.262e-13 | -2.259e-13 | 32137/32137 |
| national | MedianEnsemble | 319.914816255 | 319.914816255 | 319.914816255 | -1.271e-12 | -1.271e-12 | 32137/32137 |
| national | RIVM | 289.050643612 | 289.050643612 | 289.050643612 | +9.519e-13 | +9.519e-13 | 32137/32137 |
| national | RKI | 382.935129290 | 382.935129290 | 382.935129290 | -5.906e-13 | -5.906e-13 | 32137/32137 |
| national | SU | 382.449574867 | 382.449574867 | 382.449574867 | +6.350e-14 | +6.328e-14 | 32137/32137 |
| national | SZ | 521.690717304 | 521.690717304 | 521.690717304 | -9.992e-15 | -9.992e-15 | 32137/32137 |
| states | Epiforecasts | 26.436121062 | 26.436459179 | 26.436459179 | +1.279e-05 | -1.303e-12 | 513583/513583 |
| states | KIT | 21.966840316 | 21.966840316 | 21.966840316 | +1.084e-12 | +1.084e-12 | 513583/513583 |
| states | KIT-frozen_baseline | 98.412408510 | 98.412408510 | 98.412408510 | -6.406e-14 | -6.406e-14 | 513583/513583 |
| states | LMU | 29.401141255 | 29.401141255 | 29.401141255 | -1.352e-12 | -1.352e-12 | 513583/513583 |
| states | MeanEnsemble | 22.186471028 | 22.186471028 | 22.186471028 | +2.166e-12 | +2.166e-12 | 513583/513583 |
| states | MedianEnsemble | 23.762139421 | 23.762139421 | 23.762139420 | -1.104e-13 | -1.107e-13 | 513583/513583 |
| states | RIVM | 24.336784456 | 24.336784456 | 24.336784456 | +1.268e-12 | +1.268e-12 | 513583/513583 |
| states | RKI | 30.707846151 | 30.707846151 | 30.707846152 | +1.637e-12 | +1.637e-12 | 513583/513583 |
| states | SU | 25.438784620 | 25.438784620 | 25.438784620 | -1.020e-12 | -1.020e-12 | 513583/513583 |
| states | SZ | 36.505417928 | 36.505417928 | 36.505417928 | -9.763e-13 | -9.766e-13 | 513583/513583 |
| age | Epiforecasts | 64.845978394 | 64.846022052 | 64.846022052 | +6.733e-07 | -1.354e-13 | 192822/192822 |
| age | ILM | 29.299157254 | 29.299157254 | 29.299157254 | -1.376e-12 | -1.376e-12 | 192822/192822 |
| age | KIT | 44.002534462 | 44.002534462 | 44.002534462 | -8.014e-13 | -8.012e-13 | 192822/192822 |
| age | KIT-frozen_baseline | 262.370652726 | 262.370652726 | 262.370652726 | -1.329e-12 | -1.329e-12 | 192822/192822 |
| age | LMU | 76.780345189 | 76.780345189 | 76.780345189 | -3.516e-13 | -3.518e-13 | 192822/192822 |
| age | MeanEnsemble | 41.484004419 | 41.484004419 | 41.484004419 | +4.114e-13 | +4.112e-13 | 192822/192822 |
| age | MedianEnsemble | 50.372454388 | 50.372454388 | 50.372454388 | +3.022e-13 | +3.020e-13 | 192822/192822 |
| age | RIVM | 46.283498252 | 46.283498252 | 46.283498252 | +5.593e-13 | +5.593e-13 | 192822/192822 |
| age | SU | 59.509584798 | 59.509584798 | 59.509584798 | -2.544e-13 | -2.541e-13 | 192822/192822 |
| age | SZ | 87.425626359 | 87.425626359 | 87.425626359 | +2.247e-13 | +2.249e-13 | 192822/192822 |

Output of my checker (run3):
```
S0 (mine): cells 31, within 1%: 25, outside 1% or undefined: 6, undefined: 2, |rel|<1e-9: 0, max |rel| 0.111
S1 (mine): cells 31, within 1%: 25, outside 1% or undefined: 6, undefined: 2, |rel|<1e-9: 23, max |rel| 0.1141
S2 (mine): cells 31, within 1%: 31, outside 1% or undefined: 0, undefined: 0, |rel|<1e-9: 28, max |rel| 0.0001031
S2 (mine) non-Epiforecasts cells: 28 max |rel| 1.178e-13
mine vs author p3_ladder.csv over all 93 stage cells: max |mine/author-1| = 2.996e-12 ; NaN pattern equal: True ; row counts equal: True
```
Epiforecasts S2 components (mine vs published). The underprediction matches exactly. Spread and overprediction differ, which is what a different 0.1-quantile interpolation would cause: underprediction does not depend on the 0.1 quantile when median < truth.
```
   level      score  pub_score    spread  pub_spread      over  pub_over      under  pub_under
     age  64.846022  64.845978  5.505226    5.505238  2.182822  2.182767  57.157973  57.157973
national 423.131410 423.087782 23.098539   23.161424 14.149163 14.042650 385.883709 385.883709
  states  26.436459  26.436121  3.549817    3.549855  2.543513  2.543138  20.343129  20.343129
```

## 3. The effect of each rule (stages S0 / S1 / S2), mine vs claimed (claim/reference_outputs/p3_ladder.csv)

Rel = cell / published − 1. "undef" means the cell mean is NaN.

| level | model | S0 mine | S0 claimed | S1 mine | S1 claimed | S0 rows mine/claimed | S1 rows mine/claimed |
|---|---|---|---|---|---|---|---|
| national | Epiforecasts | +2.796e-02 | +2.796e-02 | +2.991e-02 | +2.991e-02 | 31001/31001 | 30881/30881 |
| national | ILM | -2.749e-03 | -2.749e-03 | -4.131e-04 | -4.131e-04 | 32151/32151 | 32046/32046 |
| national | KIT | +1.463e-04 | +1.463e-04 | -1.106e-12 | +0.000e+00 | 32277/32277 | 32137/32137 |
| national | KIT-frozen_baseline | -2.165e-03 | -2.165e-03 | +2.996e-12 | +0.000e+00 | 32277/32277 | 32137/32137 |
| national | LMU | -2.226e-03 | -2.226e-03 | -9.472e-13 | +2.220e-16 | 32277/32277 | 32137/32137 |
| national | MeanEnsemble | -2.819e-03 | -2.819e-03 | -2.262e-13 | -2.220e-16 | 32263/32263 | 32137/32137 |
| national | MedianEnsemble | -2.496e-03 | -2.496e-03 | -1.271e-12 | -2.220e-16 | 32263/32263 | 32137/32137 |
| national | RIVM | -2.721e-03 | -2.721e-03 | +9.519e-13 | +2.220e-16 | 32277/32277 | 32137/32137 |
| national | RKI | undef | undef | undef | undef | 32277/32277 | 32137/32137 |
| national | SU | -2.618e-03 | -2.618e-03 | +6.350e-14 | +2.220e-16 | 32277/32277 | 32137/32137 |
| national | SZ | +1.354e-03 | +1.354e-03 | -9.992e-15 | +0.000e+00 | 32151/32151 | 32137/32137 |
| states | Epiforecasts | +1.994e-02 | +1.994e-02 | +2.217e-02 | +2.217e-02 | 495407/495407 | 493487/493487 |
| states | KIT | +3.322e-05 | +3.322e-05 | +1.084e-12 | +0.000e+00 | 516432/516432 | 513583/513583 |
| states | KIT-frozen_baseline | -2.293e-03 | -2.293e-03 | -6.406e-14 | +0.000e+00 | 516432/516432 | 513583/513583 |
| states | LMU | +1.110e-01 | +1.110e-01 | +1.141e-01 | +1.141e-01 | 456141/456141 | 453432/453432 |
| states | MeanEnsemble | -2.132e-03 | -2.132e-03 | +2.166e-12 | +0.000e+00 | 516208/516208 | 513583/513583 |
| states | MedianEnsemble | -2.108e-03 | -2.108e-03 | -1.104e-13 | +2.220e-16 | 516208/516208 | 513583/513583 |
| states | RIVM | -1.147e-03 | -1.147e-03 | +1.268e-12 | +0.000e+00 | 516432/516432 | 513583/513583 |
| states | RKI | undef | undef | undef | undef | 516432/516432 | 513583/513583 |
| states | SU | -2.200e-03 | -2.200e-03 | -1.020e-12 | +0.000e+00 | 516432/516432 | 513583/513583 |
| states | SZ | +1.533e-03 | +1.533e-03 | -9.763e-13 | +2.220e-16 | 514416/514416 | 513583/513583 |
| age | Epiforecasts | +2.602e-02 | +2.602e-02 | +2.800e-02 | +2.800e-02 | 186006/186006 | 185286/185286 |
| age | ILM | -2.725e-03 | -2.725e-03 | -7.472e-04 | -7.472e-04 | 192906/192906 | 192276/192276 |
| age | KIT | +4.511e-05 | +4.511e-05 | -8.014e-13 | -1.110e-16 | 193662/193662 | 192822/192822 |
| age | KIT-frozen_baseline | -2.168e-03 | -2.168e-03 | -1.329e-12 | +2.220e-16 | 193662/193662 | 192822/192822 |
| age | LMU | -2.257e-03 | -2.257e-03 | -3.516e-13 | +2.220e-16 | 193662/193662 | 192822/192822 |
| age | MeanEnsemble | -2.946e-03 | -2.946e-03 | +4.114e-13 | +2.220e-16 | 193578/193578 | 192822/192822 |
| age | MedianEnsemble | -2.610e-03 | -2.610e-03 | +3.022e-13 | +2.220e-16 | 193578/193578 | 192822/192822 |
| age | RIVM | -2.250e-03 | -2.250e-03 | +5.593e-13 | +0.000e+00 | 193662/193662 | 192822/192822 |
| age | SU | -2.395e-03 | -2.395e-03 | -2.544e-13 | -2.220e-16 | 193662/193662 | 192822/192822 |
| age | SZ | +1.399e-03 | +1.399e-03 | +2.247e-13 | -1.110e-16 | 192906/192906 | 192822/192822 |

The claimed rule effects are confirmed. Without the rules, 6 of 31 cells miss: Epiforecasts by +2.0% to +3.0%, LMU states by +11.1% (+11.4% at S1), and RKI national and states are undefined because of 3 NaN RKI values each. The exclusion alone (S1) makes 23 cells exact. The repairs then fix Epiforecasts, ILM, LMU states and RKI. Rule counts from my checker and from a separate scan (scan.py) of the assembly:
```
fix_RKI: error rows by horizon {0: 42}          (scan: RKI rows with value > 1e6 or NA, by type: {'quantile': 42, 'mean': 6} total 48)
fix_epiforecasts: targets without 0.1 29348
fix_ILM: list rows 1008 (quantile 882), files 6, joined 882, NaN after join 0;  filled keys already present in assembly: 0
fix_LMU: list rows 60291 (quantile 60291), files 158, joined 60291, NaN after join 0;  filled keys already present in assembly: 0
exclusion list rows 4744 quantile 4151 unique 7-col keys 4376 unique target keys 547
forecast dates with retrospective files per model: {'Epiforecasts-independent': 2, 'ILM-prop': 19, 'RIVM-KEW': 2, 'RKI-weekly_report': 159, 'SU-hier_bayes': 3}
forecast dates per model: 159 for each of the 10 models, range 2021-11-22 2022-04-29
S2 duplicate (model,key) quantile rows 0; keys with duplicate medians 0 and rows without median 0 at every stage and model
sorted full names -> short: Epiforecasts-independent->Epiforecasts, ILM-prop->ILM, KIT-frozen_baseline, KIT-simple_nowcast->KIT, LMU_StaBLab-GAM_nowcast->LMU, NowcastHub-MeanEnsemble->MeanEnsemble, NowcastHub-MedianEnsemble->MedianEnsemble, RIVM-KEW->RIVM, RKI-weekly_report->RKI, SU-hier_bayes->SU, SZ-hosp_nowcast->SZ
```
All the counts match CLAIM.md: 48 RKI rows, 29,348 Epiforecasts targets, 1,008 ILM and 60,291 LMU rows, and retrospective replacements for RKI 159, ILM 19, SU 3, Epiforecasts 2 and RIVM 2. One wording point: the "4,376 target keys" in CLAIM.md rule 1 are 4,376 distinct seven-column (target, type, quantile) keys, which cover 547 distinct targets. The number is right and only the word "target" is loose.

## 4. Provenance and fetches (each a single plain request, User-Agent naming V3R1T4S, at least 2.5 s apart, no retries)

Hub files I picked at random from claim/reference_outputs/hub_fetch_log_part1.tsv (fetch5.py, random.SystemRandom, spread across folders). Six files, all HTTP 200, and every sha256 equals the logged one:
```
2026-11-13T04:56:37Z 200 483177  sha_match=True .../main/data-processed/NowcastHub-MeanEnsemble/2021-12-15-NowcastHub-MeanEnsemble.csv
2026-11-13T04:56:40Z 200 482462  sha_match=True .../main/data-processed/KIT-simple_nowcast/2022-01-15-KIT-simple_nowcast.csv
2026-11-13T04:56:43Z 200 461038  sha_match=True .../main/data-processed_updated_models/LMU_StaBLab-GAM_nowcast/2021-11-22-LMU_StaBLab-GAM_nowcast.csv
2026-11-13T04:56:46Z 200 435273  sha_match=True .../main/data-processed/RIVM-KEW/2022-03-31-RIVM-KEW.csv
2026-11-13T04:56:49Z 200 397836  sha_match=True .../main/data-processed/SZ-hosp_nowcast/2021-11-22-SZ-hosp_nowcast.csv
2026-11-13T04:56:52Z 200 472303  sha_match=True .../main/data-processed_updated_models/LMU_StaBLab-GAM_nowcast/2022-04-04-LMU_StaBLab-GAM_nowcast.csv
```
The rows of the four data-processed files compared with claim/data/eval_data/submissions.csv.gz (same model and forecast_date), matched on location, age_group, target_end_date, target, type and quantile (rowcmp.py):
```
NowcastHub-MeanEnsemble 2021-12-15: hub_rows=5336 asm_rows=5336 only_hub=0 only_asm=0 value_mismatch=0 dup_keys hub/asm=0/0 hub_fd_mismatch=0 asm_retrospective=['False']
KIT-simple_nowcast 2022-01-15: hub_rows=5336 asm_rows=5336 only_hub=0 only_asm=0 value_mismatch=0 dup_keys hub/asm=0/0 hub_fd_mismatch=0 asm_retrospective=['False']
RIVM-KEW 2022-03-31: hub_rows=5336 asm_rows=5336 only_hub=0 only_asm=0 value_mismatch=66 dup_keys hub/asm=0/0 hub_fd_mismatch=0 asm_retrospective=['False']
SZ-hosp_nowcast 2021-11-22: hub_rows=4232 asm_rows=4232 only_hub=0 only_asm=0 value_mismatch=508 dup_keys hub/asm=0/0 hub_fd_mismatch=0 asm_retrospective=['False']
```
The value_mismatch counts are from exact (bitwise) float equality. Every one of them is a last-digit difference from decimal printing:
```
RIVM-KEW 66 max abs diff 1.8189894035458565e-12 max rel 2.0319817283069955e-16   (e.g. 9233.974999999999 vs 9233.975)
SZ-hosp_nowcast 508 max abs diff 9.094947017729282e-13 max rel 2.2200727625137782e-16 (e.g. 901.8832350192581 vs 901.883235019258)
```
So the rows are equal: the keys match exactly and every value agrees to at most 2.2e-16 relative. The author's checker uses atol 1e-9, so it counts these as equal. Both re-fetched LMU updated-model files are byte-identical (same sha256) to the copies in claim/data/hub/updated_models/.

Truth files at hub commit 11c745322c055cfbd4f0c8f72241642a50aea399, re-fetched; both sha256 equal the logged values and the local copies in claim/data/hub/truth/:
```
2026-11-13T05:08:20Z 200 10497770 bdd34ddb...d380 sha_match=True .../11c7453.../data-truth/COVID-19/COVID-19_hospitalizations_preprocessed.csv
2026-11-13T05:08:23Z 200 10511341 2c18ca95...2ed3 sha_match=True .../11c7453.../data-truth/COVID-19/COVID-19_hospitalizations.csv
```
Published evaluation files, re-fetched from raw.githubusercontent.com/dwolffram/hospitalization-nowcast-hub-evaluation/main/. Each is byte-identical to the claim/data copy:
```
2026-11-13T05:02:10Z 200 919      78aeb28a...2f37 equal=True data/scores/wis_national.csv
2026-11-13T05:02:13Z 200 856      2cde62e4...6dd9 equal=True data/scores/wis_states.csv
2026-11-13T05:02:16Z 200 849      88936f4c...e022 equal=True data/scores/wis_age.csv
2026-11-13T05:02:19Z 200 54425741 04608675...f8e1 equal=True data/submissions.csv.gz
2026-11-13T05:02:25Z 200 1454132  8c93cdbb...ac24 equal=True data/truth_2022-08-08.csv
```
claim/reference_outputs/p3_provenance_part1.txt covers 189 files: all 159 MeanEnsemble files, 27 sampled data-processed files and 3 retrospective files. Its result line is `files_checked=189 hub_rows=989134 key_mismatches=0 value_mismatches=0`. claim/reference_outputs/p3_provenance_full.txt appeared at 05:22 UTC and I checked it; see the provenance_full status at the end of section 7.

## 5. Truth recomputation and FrozenBaseline (my code, truth_frozen.py)

```
preprocessed rows 58310 value cols 82 ['value_0d', 'value_1d'] ['value_80d', 'value_>80d']
file order date-increasing within each stratum: True
date gaps inside strata 0
truth file rows 57596 my rows 57596 join: {'both': 57596, 'left_only': 0, 'right_only': 0}
TRUTH CHECK: common 57596 max |diff| 0.0 n diff>0 0
raw rows 58310 delay cols 82 max delay 81 NaN cells 395080
baseline rows 848424 targets 106053 targets with >1 distinct value over its 8 rows 0 rows per target {8: 106053}
FROZEN CHECK: baseline targets 106053 equal to my raw-truncation 7-day sums 106053 differ 0 missing raw rows 0 NaN baseline values 0
```
The first part is the published load_truth applied to the hub preprocessed triangle at the stated commit. It reproduces claim/data/eval_data/truth_2022-08-08.csv exactly, and that file is byte-identical to the evaluation repository's copy. The second part is the FrozenBaseline check. For each target I computed the sum over reference dates s in [t−6, t] of the delay columns k with s + k ≤ forecast_date (value_>80d treated as k = 81), from the hub raw triangle. This equals the KIT-frozen_baseline value on 106,053 of 106,053 targets, and all 8 rows of every target are equal. This confirms claim/reference_outputs/frozen_baseline_check.txt.

## 6. The author's REPRODUCE.md commands (run from inside claim/, outputs written outside claim/)

- Step 1, `python -I code/wis_selftest.py`: output ends `SELFTEST PASS`, and the output is byte-identical to claim/reference_outputs/wis_selftest.txt (`diff` empty).
- Step 3, `python -I code/frozen_baseline_check.py . <outside>/frozen_baseline_check.txt`: `baseline targets 106053; equal to raw-truncation 7-day sums: 106053; differ: 0; NaN: 0; max |diff| 0.0; sum |diff| 0.0`. Byte-identical to claim/reference_outputs/frozen_baseline_check.txt. Peak working set 415 MB.
- Step 2, `python -I code/p3_reproduce.py . <outside>`: **not completed.** REPRODUCE.md itself says the memory peak is about 1 GB, and this panel is capped at 700 MB. My watchdog stopped the process during loading: `pid 36736 KILLED at 723 MB (limit 690.0)`. So I could not confirm by rerunning that the author's step 2 is deterministic. What I can confirm is that its saved output (claim/reference_outputs/p3_ladder.csv and p3_log.txt) agrees with my independent checker on all 93 stage cells to 3.0e-12 relative, with the same NaN pattern and identical row counts.
- My own checker is deterministic. Two complete runs (run1 single-phase, run3 two-phase) gave byte-identical my_ladder.csv (sha256 b698680c...e363 both times) and identical extracted assembly rows.

## 7. Mismatches, caveats and process notes

- No numerical mismatch. All 31 cells reproduce within 1%. The 28 non-Epiforecasts cells agree to 1.2e-13 relative. The three Epiforecasts cells differ from the published values by +1.031e-4, +1.279e-5 and +6.73e-7, exactly as claimed. The cause is the closed-form normal fit used instead of rriskDistributions::get.norm.par: underprediction matches exactly and only spread and overprediction move. CLAIM.md documents this. Without R I cannot show that get.norm.par gives exactly the published value.
- CLAIM.md says "4,376 target keys". These are 4,376 (target, type, quantile) keys over 547 targets. Only the wording is loose; the count is right.
- Memory rule: before I added a watchdog, my first full run reached a 954 MB peak working set, above the 700 MB cap. It completed, and its numbers equal run3. Two of my later attempts were stopped by the watchdog at 695 MB and 795 MB. The compliant two-phase run3 peaked at 329 MB (encode) and 687 MB (score). The author's step 2 was stopped at 723 MB.

provenance_full status: CHECKED, no discrepancy. claim/reference_outputs/p3_provenance_full.txt appeared at 05:22 UTC. Its summary line is `files_checked=1593 hub_rows=7592953 key_mismatches=0 value_mismatches=0 files_with_any_difference=0`. I parsed it with my own code:
```
distinct (model, date) pairs: 1590   (159 for each of the 10 models)
pairs checked against a retrospective file: {'Epiforecasts-independent': 2, 'ILM-prop': 19, 'RIVM-KEW': 2, 'RKI-weekly_report': 159, 'SU-hier_bayes': 3}
pairs checked against both prospective and retrospective files: 3 (the 3 MeanEnsemble dates in both the 'ensemble' and 'sample' sets, all equal)
sum asm_rows over distinct pairs: 7577313 (assembly rows 7577313)
pairs with any difference: 0
```
So every (model, forecast_date) of the assembly is covered once, from the folder the released loader reads. The retrospective counts equal my scan of the assembly's retrospective flag, and the per-pair row counts add up exactly to the assembly's 7,577,313 rows. claim/reference_outputs/hub_fetch_log_full.tsv has 1,404 rows, all HTTP 200. I re-fetched 3 more files of my own random choice from that log, none of them in part1 and one from the retrospective folder (fetch_full3.py; one plain request each, 2.5 s apart). All sha256 match the log, and the rows equal the assembly, here bitwise:
```
2026-11-13T05:23:01Z 200 483380 sha_match=True .../main/data-processed/KIT-simple_nowcast/2022-03-26-KIT-simple_nowcast.csv
2026-11-13T05:23:04Z 200 442574 sha_match=True .../main/data-processed/SU-hier_bayes/2022-04-09-SU-hier_bayes.csv
2026-11-13T05:23:07Z 200 317400 sha_match=True .../main/data-processed_retrospective/RKI-weekly_report/2021-12-10-RKI-weekly_report.csv
KIT-simple_nowcast 2022-03-26 (retrospective file: False): hub_rows=5336 asm_rows=5336 only_hub=0 only_asm=0 value_not_bitwise_equal=0 value_mismatch_rel>1e-15=0 dup_keys hub/asm=0/0 asm_retrospective=['FALSE']
SU-hier_bayes 2022-04-09 (retrospective file: False): hub_rows=5336 asm_rows=5336 only_hub=0 only_asm=0 value_not_bitwise_equal=0 value_mismatch_rel>1e-15=0 dup_keys hub/asm=0/0 asm_retrospective=['FALSE']
RKI-weekly_report 2021-12-10 (retrospective file: True): hub_rows=3944 asm_rows=3944 only_hub=0 only_asm=0 value_not_bitwise_equal=0 value_mismatch_rel>1e-15=0 dup_keys hub/asm=0/0 asm_retrospective=['TRUE']
```
In total I re-fetched 9 hub nowcast files (7 data-processed or retrospective, 2 updated-model files) and 2 hub truth files. All sha256 match the logs, and all compared rows equal the assembly (or the local copies), up to at most 2.2e-16 relative in float printing. claim/ADDENDUM.md was added after my first pass. It is documentation only, and I checked that it changes none of the numbers I verified. I did not independently re-run its claim that the exclusion lists can be re-derived (claim/reference_outputs/rederive_exclusions.txt). I did confirm that the lists contain 4,376 keys over 547 targets.

Verdict basis: every claimed number, row count, rule count and rule effect is reproduced independently and deterministically, and so are the truth and FrozenBaseline checks. The provenance holds on my re-fetches and in the full file. The one item I could not do is the rerun of the author's step 2 under the panel's 700 MB cap (section 6). Its saved output is matched by my independent recomputation to 3e-12.

pass: true
