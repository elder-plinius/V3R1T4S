# Novelty skeptic: massbalancemachine-norway-test-glaciers-rmse, partial win p2 (object LW1)

context: subagent (Claude Code Agent tool, fresh context, model claude-opus-5-5)

## Bottom line

I found no source that reports a model with at most 20 fitted parameters on the 14 Norway test glaciers' full winter set (999 points), at any Bw RMSE. Every published winter RMSE for these glaciers is above LW1's 0.5239:
- MBM: 0.59 on the full set (0.5881 reproduced).
- GloGEM 0.65, OGGM 0.82, PyGEM 0.87 and MBM 0.55, all on the 517-point 1980-2019 subset.

LW1 is not seeded from any published object, and no trivial edit of one gives it. The supplied van der Meer et al. 2026 text has no Norway experiment. The minimal-ML paper (The Cryosphere 19, 805, 2025) covers Swiss annual balances only. This verdict covers novelty for p2 only.

## 1. Status fetch (once, no retries)

- URL: https://github.com/khsjursen/ML_MB_Norway
- Time: 2026-11-07T20:54:46Z (UTC). HTTP 200, 218567 bytes, page sha256 417d7effdba9b8a84542654f74cafed4c6ec7339dd7c4b39a830deed97b77e5b.
- Value: `"commitCount":"403"`. This matches the two fetches in table/record.md.
- The README text in the page's article body is identical to the copy in table/status_ML_MB_Norway.html: same 1456 characters, text sha256 prefix adc92b89daf3e062. The whole-page hash differs from the saved copy, as GitHub pages carry per-request tokens.
- No newer result is posted. The README still points to ODINN-SciML/MassBalanceMachine as the current code.
- Corroboration: I fetched src/3.3_model_comparison_point.ipynb raw at 21:04:20Z (HTTP 200). Its sha256 is 8d4ffd4fbebc1e4cac2d1b41a92c81ea23a81b793978d4d2541438dd147b91ec, the same as in table/record.md. Output of cell 51 (index 51), verbatim:
  - "Mass Balance Machine - Bw: RMSE=0.55, MSE=0.30, MAE=0.43, Bias=-0.05, R²=0.68, Count=517"
  - "GloGEM - Bw: RMSE=0.65, MSE=0.42, MAE=0.51, Bias=-0.35, R²=0.55, Count=517"
  - "OGGM - Bw: RMSE=0.82, MSE=0.68, MAE=0.63, Bias=0.26, R²=0.26, Count=517"
  - "PyGEM - Bw: RMSE=0.87, MSE=0.76, MAE=0.69, Bias=0.59, R²=0.17, Count=517"

## 2. The object as compared

- object/frozen_LW1.json holds 3 coefficients for ["one", "solid", "solid_dz"]: 0.08075556306273535, 0.02986353396715234 and -0.03973234239283245.
- I wrote my own scorer, using csv and math only and not the claim's scorer. On data/…_test_svf.csv it finds 999 winter points (ids with exactly the 7 monthly rows Oct to Apr) on 14 glaciers, with **RMSE 0.523911** and bias +0.0808.
- The 14 test RGI ids equal the bank list. The training CSV has 18 glaciers, with no overlap.
- Form: f = b0 + b1·solid·(1 + (b2/b1)·dz/1000), with b2/b1 = -1.3305 per km of (climate-cell minus stake) altitude.
  - This is the textbook accumulation term of a temperature-index model: precipitation factor × solid precipitation, with a precipitation gradient and a rain/snow threshold, plus a monthly constant.
  - The bank's p2 text names "a calibrated temperature-index or linear model" as the expected kind of model. So the novelty question is about the result in this cell, not about the form.

## 3. Searches

The window is 2024-11-07 to 2026-11-07, computed with a tool.

| Source | Fetched (UTC), status | Relevant content |
|---|---|---|
| Sjursen et al., The Cryosphere 19, 5801, 2025, PDF | 20:57:18Z, 200, sha256 fecf987f…bdfd1 | Full set: MBM Bw 0.59 (n=999). Table E1, 1980-2019 point set: winter n=517, MBM 0.55, GloGEM 0.65, OGGM 0.82, PyGEM 0.87. These glacier evolution models calibrate 3 to 4 free parameters per glacier against 2000-2019 geodetic balances, test glaciers included. No linear or small regional baseline. |
| Sjursen preprint review files AR1, AC1 and AC2 supplements (egusphere-2025-1206) | 21:02:24-27Z, 200 | No linear or regression baseline was requested or reported. Hits were "collinearity" and "too linear gradients" only. |
| van der Meer et al., The Cryosphere 19, 805, 2025 (minimal ML), Copernicus PDF | 20:57:18Z, 200, sha256 a487307f…b23b8 | miniML-MB: XGBoost on 28 Swiss GLAMOS sites, annual point balance only, compared with a degree-day model. No Norway, no winter test set. The TU Delft record was not fetched. |
| Maslov et al., GlaUnTI, The Cryosphere 20, 6045, 2026, PDF | 21:02:40Z, 200, sha256 b3c58d6f…a858a | Different test set: 13 pan-European glaciers, 756 winter points, 1995-2024. Its temperature-index baseline has winter RMSE 0.610 / 0.613. For Norway it only cites Sjursen's numbers. |
| van der Meer et al. 2026 LSTM (local copy, table/related/vandermeer2026_paper.txt) | not fetched | See section 4. |
| EGU26-11039 and EGU26-20051 (search snippets) | not opened | 20051 is the Swiss LSTM study. 11039 is a neural network with a geodetic loss term. Neither is a small model. |
| egusphere-2025-5302 (Avzalshoev and Chun) | WebFetch, abstract page | Transformer for Central Asia, geodetic data. Not relevant. |
| ODINN-SciML/MassBalanceMachine: releases, tree, 11 notebooks and 2 scripts fetched raw | 21:00:52Z to 21:01:43Z, all 200 | Releases v0.1.0 and v0.2.0, no assets. The regions/RGI_08_Norway notebooks run XGBoost, NN, DANN and LSTM models on Sjursen's test list (`norway_kamilla_glacierlist`). The regions/TF_Europe notebooks run Transformer and LSTM, within and across regions, including NOR. All 11 notebooks have **no stored outputs**. No sklearn linear model or LinearRegression anywhere in them. |
| khsjursen/ML_MB_Norway: releases, forks, tree | 21:03:51Z to 21:04:20Z, 200 | One release, v.1.0.0 (2025-03-13), no assets. Two forks with no pushes after upstream (pushed_at 2025-06-10T13:58:29Z). model_classes.py holds XGBoost classes only. No linear-model notebook. |
| Zenodo records 23394429 and 21553824 (marvande/MassBalanceMachine "Transfer Learning paper" releases, 2026-10-15 and 2026-07-25) | 20:58:43-45Z, 200, metadata only | These are the code for "Towards a global data-driven glacier mass balance model using Transformers" (van der Meer et al., submitted to JGR MLC). Per search snippets: about 64,000 points from 180 glaciers in six RGI regions. Zip files not downloaded (see section 6). |
| V3R1T4S pull requests, pulls API, state=all, pages 1 to 10 (sequential) | 20:55:23Z to 20:55:50Z, all 200 | 959 PRs, numbers 1 to 1007, 428 open and 531 closed. None mentions glacier, mass balance, ML_MB, Norway, Sjursen or Bw in title, body or branch. |
| Repository copy: TROPHY_CASE.md and known-knowns/ (30 entries) | local read | No glacier or mass-balance entry. The only mention of this target is a quarry line in the charter file of one entry, known-knowns/iea37-cs1-circular-wind-farm-layout/. That entry is a wind-farm result. |
| Web searches (about 10 queries: Norway point or winter balance, small models, MBM successors, code reproductions, arXiv, EGU26) | 20:56Z to 21:06Z | No other report on this split. |

## 4. Check of the contributor's summary of van der Meer et al. 2026 (local text)

- The text's sha256 is a88f20daf53f6cf2ab61681dcfbc301675ea7398f292d791e2c606d14ae3dd04. It matches table/related/README.md.
- **Confirmed:**
  - Swiss Alps study: about 30,000 observations from 30 glaciers.
  - 8 test glaciers (Forno, Tsanfleuron, Sanktanna, Plattalva, Tortin, Schwarzberg, Hohlaub, Corvatsch), with 471 annual and 1,707 winter points.
  - Test RMSE 0.35 winter and 0.78 annual.
  - No Norway experiment: every "Norw" hit is a citation or an affiliation.
  - The only Norway numbers are quoted: "both lower than those reported for Norway (0.55 and 0.97 m w.e., respectively)".
  - Its benchmarks (XGBoost, and an MLP with 128-128-64-32 hidden units) are Swiss and large.
- **Two imprecisions; neither changes the conclusion:**
  1. The quoted 0.55 and 0.97 are Sjursen's 1980-2019 subset values (Table E1, winter n=517), not the full-test-set 0.59 and 1.00.
  2. The paper does not say "transfer to Scandinavia is ongoing work". It says ongoing work includes "transfer-learning strategies that leverage existing PMB data sets from the Alps and Scandinavia to enable predictions in regions where in situ observations are scarce or absent".

## 5. Comparison with this cell and the neighbouring cells

| Model | Fitted parameters | Test set | Bw RMSE |
|---|---|---|---|
| **LW1 (this claim)** | 3 | 14 glaciers, all 999 points | **0.5239** |
| MBM, XGBoost | thousands (tree ensemble) | 14 glaciers, 999 points | 0.59 published, 0.5881 reproduced (baseline/output.txt) |
| MBM | thousands | 1980-2019 subset, 517 points | 0.55 |
| GloGEM / OGGM / PyGEM | 3 to 4 per glacier, calibrated on geodetic balances of the test glaciers | 517-point subset | 0.65 / 0.82 / 0.87 |
| GlaUnTI temperature-index baselines | small | different 13 European glaciers, 756 points | 0.610 / 0.613 |

- **The cell itself** (at most 20 parameters, full 999-point set) has no published entry. LW1 is strictly below every number above, including at 2 decimals: 0.52 against 0.55 or higher.
- **Trivial edits:** none of the following yields LW1:
  - deleting or restricting MBM's trees: each tree alone exceeds 20 parameters, and the full model scores 0.588;
  - relabelling or polishing the per-glacier GloGEM, OGGM or PyGEM parameters: these are calibrated on test-glacier geodetic data, are not published in a form LW1 could be derived from, and score 0.65 or worse on a subset;
  - any symmetry or propagation rule.
- **Seeding:** LW1 is a fresh least-squares fit on the 18 training glaciers and is not seeded from any published object. The claim says so in CLAIM.md, and object/frozen_LW1.json is consistent with it.

## 6. Not read (residual risk)

- **The Transformer preprint itself** (van der Meer et al., submitted 2026). I found no accessible full text. Its code (TF_Europe and RGI_08_Norway in the ODINN tree) includes Norway runs, but they are Transformer and LSTM models, i.e. the unrestricted cell, not the at-most-20-parameter cell. The code has no small or linear baseline and no stored outputs. If the preprint reports Norway Bw on the 14-glacier split, that would bear on p1, not on p2.
- **The Zenodo v0.1.2 archive** (MassBalanceMachine-v0.1.2.zip, 46,166,894 bytes). Not downloaded: it snapshots the same GitHub repository that hosts the LSTM paper's code, which was not fetched, and the ODINN main tree was read instead.

## 7. Other fetches

- Zenodo record 18267624 (the code archive the LSTM paper cites, marvande/MassBalanceMachine v1.0.0): metadata (title, date, file list) returned at 20:58:46Z, HTTP 200. The archive was not downloaded, and none of its content was used.
- The ODINN releases list includes the v0.2.0 release note, which names the LSTM paper. This was metadata only.

## Text addressed to reviewers: none found

I scanned claim/ and all downloaded pages, PDFs and notebooks. The only text that mentions the novelty skeptic is the contributor's summary quoted in table/related/README.md. It is labelled as such, and I checked it against the paper (section 4) rather than relying on its conclusion.

## Blocks

None. Every request returned HTTP 200. There were no tool-guard or classifier blocks, and no 401, 403 or 429 responses.

pass: true
