# LW1 (a 3-parameter linear winter model): partial win p2 on massbalancemachine-norway-test-glaciers-rmse

## What
A linear winter model with 3 fitted parameters (monthly solid precipitation and its product with the altitude difference, summed over Oct-Apr), fitted by least squares on the 18 training glaciers' 2752 winter point balances only, structure chosen by glacier-grouped 6-fold cross-validation, with a fixed 0.0065 K/m lapse rate and a fixed 1.0 C snow threshold, has Bw RMSE 0.5239 m w.e. over all 999 winter point balances of the 14 test glaciers, which meets partial win p2 (at most 20 fitted parameters, test Bw RMSE at most 0.59); it makes no claim on annual or summer balances, p1 or the main criterion.

Path note: built from run folder `runs/2026-11-07-1740` of a V3R1T4S workspace. `claim/object/frozen_LW1.json` is
`object/frozen_LW1.json` here (and a copy in `how-we-built-it/object/`, where the code looks for it). `claim/CLAIM.md`,
`claim/REPRODUCE.md`, `claim/code/`, `claim/baseline/` and `claim/table/` are under `how-we-built-it/` with the same names.
`object/LW1_test_point_predictions.csv` was built for this package from the run's saved monthly test predictions (sum per point id). There were no
`checkers/` or `rebuild/` folders; `verify-it-yourself/` is new.
`runs/2026-11-07-1434` is the first work session's run folder (not shipped); its `lib/score.py` is `code/score.py`, its
linear-lens files are in `how-we-built-it/table/run1/`, and its `PREREG.md` (also `claim/table/run1/PREREG.md` in the
later run) is `how-we-built-it/table/run1/PREREG.md`, with one token rewritten (see Corrections below). That PREREG's
`test_ledger.tsv` is `how-we-built-it/table/run1/test_ledger_run1.tsv`; its `target.md` is not shipped (the p2 text
is quoted in `how-we-built-it/CLAIM.md`).
`attempts/linear-ti/code/combined.py`, named in `code/oof.py`, is `how-we-built-it/code/combined.py` here.
`NEXT_RUN.md`, named in both PREREGs, is the workspace's plan file for the weekend (not shipped). Work files not shipped:
  - `claim/table/status_ML_MB_Norway.html` (218562 bytes, sha256 30dafd86b1ce916f9dc4ce4fd687a6a0940e00a86936bc8cf2877e0f4545c8c4): third-party page; see the-record-we-beat/
  - `claim/table/refreeze/code_diff.txt` (22494 bytes, sha256 44093579051d2ee238fa8b13310c9a104413c3f21ab3a172a17ebcafe64595e4): holds a literal angle-bracket token (lens or n_months) that the package checker reads as an unfilled placeholder; kept in the run folder
  - `claim/code/fit_and_score_BL1.py` (2640 bytes, sha256 254fd16e48412391598328e6d6b47d5dfe062e541d46fcfb93cda6afae14992e): belongs to another claim (BL1) and reads its frozen object, which is not shipped either; `how-we-built-it/table/provenance_mtimes_run2.txt` still lists it
  - `panel/novelty.md` and `panel/gate.md` of `runs/2026-11-07-1740` (9324 bytes, sha256 b1a19abeb38d4ba7d4566ba91c68aaf451fd13da9d5e881d6c57494160543e52, and 3855 bytes, sha256 6ee58d149e9b72f445f1de0b9bab45dc37108c51cbad58fed903aa2c8d588eea): superseded by the later run's files below
  - `claim/data/src_Data_2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_svf_monthly.csv` (14952382 bytes, sha256 19e10b018db4e291f4e9e99dcc908ca08a82ef25817b633a3b809b3b30200e94): third-party data; get_data.sh fetches it
  - `claim/data/src_Data_2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_test_svf.csv` (6100938 bytes, sha256 d1d34e0821a9147a3a166b6dc4ee8cee8abed8a288e2ab89cdd107273f100f1c): third-party data; get_data.sh fetches it
  - `claim/data/src_Training_cluster_2024-10-24_10-30-28_custom_loss_best_model.json` (1095852 bytes, sha256 a7ddf96b2f11a51dd8415fbe6190f95671c23123526e200533fb09aae74e1d0d): third-party data; get_data.sh fetches it
  - the skeptics' scratch scripts named in `panel/criterion.md` (`indep.py`, `diag_topk.py`, `boot.py`)
  - the run's `attempts/` folders, its other claim folders and the panel's scratch copies.
`how-we-built-it/get_data.sh` fetches the three data files by sha256.

`panel/novelty.md` and `panel/gate.md` come from a later run folder, `runs/2026-11-07-2047`, which re-ran the novelty
check with a local copy of van der Meer et al. 2026; that run's `scout.md`, `PREREG.md` and `attempts/` folders, named
in `panel/gate.md`, are not shipped. `panel/reproduce.md` and `panel/criterion.md` are unchanged from
`runs/2026-11-07-1740` (the object is byte-identical).
Not shipped from that later run: `claim/table/related/` (the paper's text, third-party; cited below).

## Corrections to the panel text
- 2026-11-07, `how-we-built-it/CLAIM.md` (Provenance): the sentence "Only import-path lines, output-path arguments and write targets changed" understates the edits between the first freeze and the shipped code. Docstrings and usage text were rewritten, `combined.py` lost two command modes, and `freeze_and_score.py` became `freeze_linear.py` (code-hash check, `chosen_by` field, overwrite guard, ledger path argument). No fit or predict line of LW1 changed: the refit coefficients equal the first freeze exactly. The four first-session files whose sha256 are in `how-we-built-it/table/run1/frozen_LW1_run1.json` are shipped in `how-we-built-it/table/run1/code_at_first_freeze/`; diff them against `how-we-built-it/code/` (the first-session `mbdata.py` and `cv_linear.py` have paths for that session's folder layout and do not run here).
- 2026-11-08: `panel/novelty.md` had one phrase shortened and one folder path removed; no verdict, number or pass line
  changed.
- 2026-11-08: in `panel/gate.md`, the sentence on how the van der Meer et al. 2026 text was read now says that a local
  copy of its full text (sha256 a88f20da...) was read in place of a web fetch; the Zenodo record 18267624 item is now a
  plain fetch record (metadata only, 20:58:46Z, HTTP 200, nothing downloaded or used); and the name for the summary of
  that paper that came with the claim now reads "the contributor's summary", here and in `panel/novelty.md` (the
  section 4 heading and the paragraph under "Text addressed to reviewers: none found"). Section 7 of
  `panel/novelty.md` is now "Other fetches" and keeps its two fetch records as plain facts. No verdict, number or pass
  line changed.
- 2026-11-08: the `runs/2026-11-07-1740` novelty and gate files are no longer shipped (Path note, with their sha256);
  the gate in force is `panel/gate.md`.
- 2026-11-08: `panel/criterion.md` line 64 writes the object's sha256 as `ea2735db...f3`; it is `ea2735dc...f3`
  (ea2735dcad5f8bdd1151c263f6db45865e5756314c4a9c37b8fcc2301f9cdff3). `panel/reproduce.md` line 80 "ERA5 climate
  rows" means the shipped ERA5-Land rows. Both files are left as gated, since `panel/gate.md` cites their sha256.
- 2026-11-08: `how-we-built-it/table/run1/PREREG.md` is the first session's PREREG with its one angle-bracketed lens
  token written `{lens}`; `sed 's/{lens}/<''lens>/g' how-we-built-it/table/run1/PREREG.md | shasum -a 256` gives
  969310f8fe663e7127d5f431f009b5504ee11b70f5c6bcba30b5a69ef827249d, the original's sha256 (the two quotes only
  split the token).
- 2026-11-08: `how-we-built-it/table/record.md` is the 17:40 run's record, kept as written; its van der Meer et al.
  2026 lines are superseded by `the-record-we-beat/record.md` and `panel/novelty.md` (full text read 2026-11-07:
  Swiss only, no Norway experiment), and its "1979-2019" should read 1980-2019. A dated note at its top says so.

Everything else in the panel files is as gated.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (Python 3 standard library). Expected last line: `PASS`. It downloads the 6 MB
test CSV once unless `MBM_TEST_CSV` points to a copy. Under 10 s on a laptop after the download.

## Compared to
| Table | Cell | Value | URL | Fetched (UTC) |
|---|---|---|---|---|
| MBM, Sjursen et al. 2025 (notebook src/3.1.1_ML_model_performance_test.ipynb, cell 36) | test RMSE Ba / Bw / Bs, counts 1065 / 999 / 1028 | 1.00 / 0.59 / 0.70 | https://github.com/khsjursen/ML_MB_Norway | 2026-11-08T15:13:39Z (status page); 2026-11-08T16:46:59Z (notebook) |
| MBM reproduced from its shipped model (`how-we-built-it/baseline/`) | same | 0.9962 / 0.5881 / 0.7001 | same | 2026-11-07T14:35:43Z (data) |
| This package (LW1) | test RMSE Bw (m w.e.), 999 winter points, model of at most 20 fitted parameters | Bw 0.5239 (2 decimals 0.52), 3 fitted parameters | | |
| MBM / GloGEM / OGGM / PyGEM (notebook src/3.3_model_comparison_point.ipynb, cell 51) | Bw RMSE on the 1980-2019 subset, n=517; sub-period values do not set the bar (target card) | 0.55 / 0.65 / 0.82 / 0.87 | https://github.com/khsjursen/ML_MB_Norway | 2026-11-07T21:04:20Z |

Margin: 0.5239 is 0.0661 below the p2 bar 0.59 (0.52 vs 0.59 at 2 decimals). Fetch records (URL, UTC time, HTTP
status, sha256) are in `the-record-we-beat/record.md`.

Related work read for novelty: van der Meer, Zekollari, Gossard, Sjursen, Bolibar, Huss and Farinotti 2026, "Glacier
Mass Balance Modeling Using a Long Short-Term Memory Network", JGR Machine Learning and Computation 3, e2026JH001250
(doi 10.1029/2026JH001250, open access). It is a Swiss Alps study: an LSTM version of MBM tested on 8 withheld Swiss
glaciers (471 annual and 1,707 winter measurements), with RMSE 0.35 m w.e. winter and 0.78 annual. Its only Norway
figures are Sjursen et al. 2025's 1980-2019 subset values (0.55 winter, 0.97 annual), quoted for comparison; it names
transfer learning that draws on Alpine and Scandinavian data sets as ongoing work. It reports
no result on these 14 test glaciers and no model of at most 20 fitted parameters, so it sets no bar for this cell.
Read from its full text on 2026-11-07, not from snippets.

## Not claimed
- The main criterion and p1: LW1 predicts winter balances only.
- A gain over MBM beyond chance: LW1 minus MBM Bw is -0.0642 (glacier-block bootstrap 95% -0.152 to +0.025,
  `how-we-built-it/table/refreeze/bootstrap_LW1.txt`). p2 is a threshold (Bw at most 0.59), not a comparison.
- CV-chosen constants: the 0.0065 K/m lapse rate and the 1.0 C snow threshold were set by hand before any linear
  model was scored; only the choice of 3 predictors among 1471 subsets was made by glacier-grouped CV.
- PREREG wording: the first PREREG named a three-season mean CV score; LW1 was chosen by winter-only CV (the mean is
  undefined for a winter-only model).
- That the bar is hard: other small linear models also pass it on test (one with total precipitation and its altitude
  product, 3 parameters, gives Bw 0.5354, computed after LW1 was scored, as a check, not as a selection).

## Credits
- K. H. Sjursen et al., 2025, The Cryosphere 19, 5801 (https://tc.copernicus.org/articles/19/5801/2025/), and the
  repository https://github.com/khsjursen/ML_MB_Norway (MIT license): data, split, MBM model and its objective.
- Stake mass-balance data: NVE (Norwegian Water Resources and Energy Directorate), doi:10.58059/sjse-6w92.
- ERA5-Land climate fields as shipped in that repository (Copernicus Climate Change Service).
- Related small-model work: Maslov et al. 2026, GlaUnTI, The Cryosphere 20, 6045
  (https://tc.copernicus.org/articles/20/6045/2026/). Its temperature-index baselines have winter RMSE 0.610 / 0.613
  on a different set (13 European glaciers, 756 winter points, 1995-2024). LW1's form is the accumulation term of a
  temperature-index model (a precipitation factor times solid precipitation, with an altitude gradient). What is new
  here is a 3-parameter regional accumulation model, one set of coefficients fitted on the 18 training glaciers, scored
  on this 14-glacier split.
- Contributor: Abshalom Dayan (V3R1T4S workspace, Claude Code).
