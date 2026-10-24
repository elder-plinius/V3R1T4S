# The record this claim beats

No third-party page, dataset or archive is copied into this package. Below is the snapshot metadata and the
extracted cell, so anyone can re-fetch and compare.

## The status table

| field | value |
|---|---|
| what | DrEval public report, leave-drug-out (LDO), normalized metrics heatmap, CTRPv2 |
| URL | `https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LDO_normalized.html` |
| first fetched (UTC) | 2026-10-23T21:30:20Z — HTTP 200, 4,665,771 bytes |
| re-fetched immediately before claiming (UTC) | 2026-10-23T23:49:53Z — HTTP 200, 4,665,771 bytes, **same sha256** |
| sha256 | `b7dd9273b4a9efbf36d5d8718a4163c73d1132f7fe8580c9dfd246e55d2c4364` |
| last-modified | Fri, 17 Oct 2025 14:20:41 GMT (unchanged for a year) |
| etag | `"68f250b9-4731ab"` |

**The page does not name its dataset or its setting.** It contains zero occurrences of `LDO` and zero of
`CTRP`, and its `<title>` is `plotly-logomark`; the identification comes from its URL and its context. That
it is CTRPv2 was established independently two ways: the parent report's `LDO.html` carries cross-study
tables for CCLE, CTRPv1, GDSC1 and GDSC2 but **not** CTRPv2, which is what one expects if CTRPv2 is the
training set; and the DrEval paper states it trains "on the largest dataset, CTRPv2" and names this exact
report URL. Stated here because the claim asserts the dataset where the source itself does not.

**Cell extracted.** Decoded from the page's embedded Plotly binary arrays (base64 `bdata`, little-endian
float64) by `../../attempts/literature/code/live_table_check.py`, not transcribed:

| model | normalized R² |
|---|---:|
| **MultiOmicsNeuralNetwork** | **+0.0235**  <- the maximum over all models |
| GradientBoosting | +0.0108 |
| SimpleNeuralNetwork | −0.0105 |
| NaiveMeanEffectsPredictor | −0.0169 |
| DIPK | −0.0181 |
| ElasticNet | −0.0305 |
| ProteomicsRandomForest | −0.0401 |
| MultiOmicsRandomForest | −0.0416 |
| NaiveTissueMeanPredictor | −0.0605 |
| NaivePredictor | −0.0892 |
| RandomForest | −0.1186 |

An independent verifier decoding the same page got `last-modified 14:20:40` and etag `"68f250b8-4731ab"`,
one second earlier than recorded above. The etag encodes mtime in hex, so the two differ only in which CDN
edge node served the request; the content sha256 is identical, which is what the comparison rests on.

The companion violin plot
(`https://dilis-lab.github.io/drevalpy-report/violin_plots/violin_algorithms_LDO_normalized.html`, fetched
2026-10-23T21:32:05Z, HTTP 200, sha256 `fba9429719d73ee493629cc281dca0c2112bafea82d3d8888810867f97c357d5`)
decodes to **10 values per model per metric**, which is where the 10 CV splits and the leader's across-split
SD of 0.1060 come from. The rank leaders are DIPK at normalized Pearson 0.3538 and Spearman 0.3559.

## Is there anything newer?

The dataset's Zenodo concept record (10.5281/zenodo.12633909) has **48 versions**. The newest,
record 23159774 (2026-10-05), ships `leaderboard_Oct26.zip` (342,432,130 bytes,
md5 `2c39020eaec28ad89e603c054ec61603`, matching the record's published checksum; downloaded once
2026-10-23T21:53:21Z, HTTP 200) — an October 2026 leaderboard of **27 distinct algorithms**, several newer
than those above.

**It contains no leave-drug-out results.** No path in the archive contains `LDO`, and its
`evaluation_results.csv` has `test_mode` values `['LCO']` only, across 270 rows. Verified programmatically
in `../../attempts/literature/output/live_table_check.txt`. An independent literature search
(`../../attempts/literature/literature-findings.md`) found no published DrEval LDO result above 0.0235 from
any group, on any dataset.

## How strong is the published record, really?

Two things a reader should know before reading any ratio against 0.0235.

1. **The published LDO differences are not statistically significant.** The DrEval paper's own LDO Friedman
   test over all 11 models gives **p = 0.742** — no model on that page differs significantly from any other,
   the naive baselines included. So 0.0235 is a maximum over a set of statistically indistinguishable, near-zero
   values, not a hard-won record. The defensible statements about this claim are its absolute value, its
   across-split spread, and its margin over the author's own same-splits re-runs — not a multiple of 0.0235.
2. **The comparison is not like-for-like on training data.** All 11 leaderboard models learn from CTRPv2's
   545 compounds. This claim's method adds about 53,500 external compounds from a public cytotoxicity screen.
   No model on that page uses an external response screen. The demonstrated finding is therefore that **the
   training distribution was the binding constraint**, which is a real result but a different one from
   "better modelling of the same data".

## The software and data this claim was produced with

| field | value |
|---|---|
| package | drevalpy **1.3.5** (PyPI, uploaded 2025-07-01) — the last release before the report's last-modified date, and the last that contains `MultiOmicsNeuralNetwork` |
| data | Zenodo record **17343165** (2025-10-13), `CTRPv2.zip` md5 `e015a6753c820bdb4ffb3f972df1faac` and `meta.zip` md5 `39aa43dd152806ab58a35065bb268ba5`, both matching the record's published checksums |
| why these versions | drevalpy 1.6.0 no longer contains the published leader, and the current data record's methylation view is too narrow for that leader's own hyperparameters. See `../../PREREG.v2.md` and `../../PREREG.v3.md` |
| response | `LN_IC50_curvecurator` (the package default) |
| external screen used by the method | NCI DTP public NCI-60: `GI50.zip` sha256 `65212008012e0fc4648709f5f081c18e577986a40a8ba45ea271f8c3bb81f728`, `nsc_smiles.csv` sha256 `1e5cb58713d0a22b8cbb8865687d357bce3bda2caa2b1b0a2e7b20c58ddd75d3`, `nsc_sid_cid.csv` sha256 `ad07b3019dca04d2b014f7786c81129b07517e64b0a0fbd2a6a74be16570c1e7`, fetched 2026-10-23T22:31Z |

## Prior work this method builds on

- **Lavelle, Zhu, Marlor, Brettin, Stevens**, *Large-scale AI-Ready Data for Anti-Cancer Drug Response
  Modeling*, arXiv:2608.11444 (11 Aug 2026). Its Table 3 reports drug-blind UNO improving from **0.03 to
  0.22** after the training set is expanded, and its Table 1 shows that expansion is dominated by NCI-60
  (53,323 of 53,949 compounds). **The idea of using NCI-60 to improve unseen-drug prediction is theirs, not
  this work's.** What is added here is a checkable exclusion rule — salt-stripped skeleton matching plus a
  Tanimoto cutoff — with a monotone sensitivity curve over the cutoff, where that work excluded held-out
  identities only.
- **Cortés-Ciriano, Bender and co-workers**, NCI-60 panel QSAR, `10.1093/bioinformatics/btv529` (17,142
  compounds across 59 NCI-60 lines, explicitly testing extrapolation to dissimilar compounds), and
  **Martorana et al.**, IJMS 2022, `10.3390/ijms232214374`. Predicting NCI-60 potency from structure is an
  established problem with established accuracy; the external prior here is a plain instance of it, not a
  new modelling idea.

## A defect found in the benchmark's tooling, reported as a duty

In drevalpy 1.3.5, **changing the split seed does not change the LDO test folds.**
`datasets/dataset.py::_leave_group_out_cv` shuffles rows with the seed and then calls `GroupKFold`, whose
fold assignment depends on group labels and sizes, not row order. Verified directly: `random_state=42` and
`random_state=20261023` give **identical test drug sets in all 10 folds**; only the validation drugs differ.

Anyone who requests a second LDO split generation by changing the seed therefore receives the same held-out
drugs, and a "seed repeat" built that way is not a repeat. This bears directly on the bank's partial win p3
(ordering stability across split generations). This claim's second generation was built instead by giving
the package's own `GroupKFold` call `shuffle=True` and the seed — the minimal change that makes its stated
intent take effect — and was accepted only after a pre-committed independence check (0/10 folds shared with
seed 42, mean best-match Jaccard 0.089).
