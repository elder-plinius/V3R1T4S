# Pre-registration — dreval-ldo-beat-naive-mean-effects

Frozen: 2026-10-23T21:37:05Z, before any model output on this target has been scored. Nothing in this file
may be edited after results are seen; a changed plan is a new, timestamped `PREREG.v2.md`.

## 1. The criterion, verbatim from the pinned bank

> Success means a drevalpy model class, run through drevalpy's own pipeline on the same dataset
> and test mode as the public report (CTRPv2, test_mode=LDO, same number of CV splits, lnIC50
> response, package-generated splits), whose mean normalized R^2 computed by drevalpy's own
> evaluation code is STRICTLY HIGHER (direction: max) than the maximum normalized R^2 over ALL
> models in https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LDO_normalized.html,
> re-fetched and re-decoded live immediately before claiming, by at least 0.02 absolute AND by at
> least 2x the across-split standard error of the attacker's result, with the attacker's own
> same-environment same-splits re-run of BOTH the NaiveMeanEffectsPredictor and the published LDO
> leader (MultiOmicsNeuralNetwork) included, and the attacker's value beating both. Deliverables:
> pinned drevalpy version/commit, model source, exact invocation, per-split prediction and
> ground-truth CSVs, the generated report directory, and a seed-repeat run showing the gain
> survives a second independent split generation. Chemical features for held-out drugs must be
> derived from structure/target annotations only; no information computed from the test drugs'
> responses (including per-drug means, ranks, or any statistic of the held-out fold) may enter the
> model.

## 2. The statistic and the protocol

- Package: **drevalpy 1.6.0** (PyPI), Python 3.12, in a dedicated environment.
- Data: CTRPv2 as served by drevalpy's loader, **Zenodo record 23159774** (the latest version of
  concept DOI 10.5281/zenodo.12633909 at fetch time). The bank cites record 18302237; the public
  report dates from October 2025 and may have used an earlier version. Recorded, not hidden.
  `CTRPv2.csv` sha256 `14488de3ecff0a7499eddbc10d22cdec389549c8506a93516a547e619f90b412`.
- Response: `LN_IC50_curvecurator` (drevalpy default; nf-core `curve_curator=false` uses this
  precomputed column).
- Test mode **LDO**, **n_cv_splits = 10** (read off the public violin plot: n = 10 per model),
  split seed **42** (drevalpy default; the nf-core pipeline sets none), hyperparameter tuning on
  drevalpy's drug-disjoint validation split optimising RMSE, `response_transformation=None`.
- Statistic: mean over the 10 splits of **"R^2: normalized"** exactly as computed by
  `drevalpy.visualization.utils._normalize_metrics_by_mean_effects`, i.e. R^2 after subtracting the
  NaiveMeanEffectsPredictor's prediction from both truth and prediction, global over all test pairs
  of the split. SE = sample SD across the 10 splits / sqrt(10).

## 3. Thresholds

Published maximum (decoded by this run, 2026-10-23T21:30:20Z): **0.0235** (MultiOmicsNeuralNetwork).

**Full success** requires all of, on the official split generation (seed 42):
1. mean normalized R^2 > 0.0235 + 0.02 = **0.0435**;
2. mean normalized R^2 > 0.0235 + 2*SE(mine);
3. mean normalized R^2 > my same-environment re-run of NaiveMeanEffectsPredictor **and** of
   MultiOmicsNeuralNetwork on the same splits;
4. **seed repeat**: on a second split generation (seed **20261023**), conditions 1-3 hold again
   against baselines re-run on that generation;
5. the live page re-fetched immediately before claiming still shows a maximum the result beats;
6. the null test in section 6 passes.

**Partial win p1** if, on seed 42: normalized Spearman > 0.3659 and Pearson > 0.3638 and normalized
R^2 >= 0.0135.
**Partial win p3** (ordering stability) is measured as a by-product of re-running baselines on both
split generations, and reported whichever way it falls.
**Partial win p2** (documented impossibility) is the declared fallback if full success fails: at
least 20 logged model/feature configurations, none exceeding normalized R^2 0.02, with a per-drug
analysis. It will be reported as a negative benchmark result.

## 4. Development protocol — how outcome-informed design is contained

1. **Vault.** 82 of 545 drugs (15%) were drawn at 2026-10-23T21:35:45Z from a seed fixed in
   advance, before any response value was read. List: `data/vault_drugs.txt`, sha256
   `fd91cf6913afe54e641a8a0719e2856adfdf20f6749c9d2258d0cb80b0ef0cb9`. **Every development experiment excludes the vault drugs entirely**, from training and
   from testing. They enter only at confirmation.
2. **Development splits** use drevalpy's own LDO split generator on the 463 non-vault drugs with
   development seed **7**, which is neither confirmatory seed.
3. **Every development configuration is logged** to `attempts/*/output`, including failures, so the
   number of things tried is on the record.
4. **Freeze before confirmation.** The final model source, its hash, its hyperparameter search space
   and all fixed choices are frozen in `PREREG.v2.md` before the first confirmatory run.
5. **Confirmation** is the full drevalpy pipeline on all 545 drugs, seeds 42 and 20261023, with
   NaiveMeanEffectsPredictor and MultiOmicsNeuralNetwork re-run alongside. In addition, normalized
   R^2 restricted to the 82 vault drugs is reported as a **diagnostic only** — not the claim, since
   evaluating on a subset is a named pitfall — to show whether performance on never-examined drugs
   matches performance on developed-on drugs.

## 5. What is forbidden as a model input for any drug

Allowed: features computed from the drug's **SMILES / chemical structure** (Morgan fingerprints,
ChemBERTa or similar embeddings computed from SMILES, descriptors), and **target-gene annotations**
(`meta/gene_lists/drug_target_genes_*.csv`). Cell-line omics as drevalpy provides them.

Forbidden:
- `min_dose_M`, `max_dose_M` and any tested-concentration metadata. IC50 values are partly an
  artefact of the tested range, so this would "predict" potency without any chemistry. It is
  experimental-design metadata, not structure or target annotation.
- `meta/gcmf_drug_relations/drug_bioassay.csv.gz` and any other external *experimental activity*
  data. Not structure, not target annotation.
- Any column of `CTRPv2.csv` other than identifiers and the response (EC50, AUC, fit statistics,
  curve parameters are all response-derived).
- Any statistic of a held-out drug's responses, and any drug-level quantity (mean, rank, embedding,
  PCA, similarity matrix, scaler) **fitted on data that includes held-out drugs**. Everything
  learned is learned inside the model's `train()` from the training drugs it is given.

## 6. Null test

`null_test: required`

The claim is that drug structure carries transferable signal for unseen drugs beyond the
mean-effects baseline. Control: the **identical full pipeline** (same splits, same tuning, same
evaluation) with the drug-identifier -> drug-feature mapping **randomly permuted across drugs**,
breaking the link between a drug's structure and its responses while preserving the feature
distribution. **400 permutations.** The real result must exceed the normalized R^2 of **every**
control. Results to `null_test.md` with `controls`, `best_control`, `real`,
`real_beats_all_controls`, `command`.

## 7. Pre-committed failure handling

If the confirmatory run misses any condition in section 3, the outcome is recorded as such and the
stronger claim is not made. No re-running with a different seed, split count, response column,
dataset version or drug subset after seeing a miss. A miss on the official seed with a hit on the
repeat seed is a miss. Over-claiming is a named pitfall: any positive result will be described as a
benchmark result on a public cell-line screen, not as guidance about which drug to give a patient.
