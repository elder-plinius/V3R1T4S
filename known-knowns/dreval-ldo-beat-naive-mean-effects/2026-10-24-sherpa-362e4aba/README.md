# DrEval leave-drug-out on CTRPv2: normalized R^2 +0.2249 against a published best of +0.0235

## What
On DrEval/drevalpy 1.3.5's own CTRPv2 leave-drug-out pipeline (pinned October-2025 data, `LN_IC50_curvecurator`, 10 CV splits, all 235,974 measured pairs scored with no subsetting, abstention or NaN masking), the drevalpy model class `PotencyTransfer` attains a mean normalized R² of **+0.2249** on the package's own default seed-42 splits (SE 0.0354, 10/10 splits positive) and **+0.2268** on a second split generation verified independent of it (SE 0.0482, 0/10 shared test folds, mean best-match Jaccard 0.088) — both computed by drevalpy's own evaluation code, both exceeding by more than 0.02 absolute and more than 2 SE the live-decoded maximum over all eleven published LDO models (+0.023466, MultiOmicsNeuralNetwork; page re-fetched 2026-10-24T02:41:09Z, sha256 `b7dd9273…4364`), and both beating the author's same-environment same-splits re-runs of NaiveMeanEffectsPredictor (−0.0247, −0.0185) and MultiOmicsNeuralNetwork (−0.0275 and −0.0931, as recomputed here) on 20/20 splits, and on all 20 again when the leader comparison is restricted to the ~54% of pairs drevalpy actually scores that model on — subject to these limits, which are part of the result: it is a benchmark result on a public cell-line screen with no clinical meaning; the model predicts one potency offset per drug and contributes nothing to the ~29% of the scored variance that is drug × cell-line interaction; it adds an external potency prior trained on ~53,500 NCI-60 compounds (every CTRPv2 compound, and everything within Tanimoto 0.60 of one, excluded from that prior's training set), which no leaderboard model uses, so the comparison is not like-for-like on training data, although a τ = 0 ablation of the frozen model — run by this skeptic and independently reproduced in the package on both generations — puts the architecture at +0.1450 and +0.1556 (SE 0.0284, 0.0333) with the prior switched off entirely, still clearing both margin conditions and still beating the leader 10/10 on seed 42, so the prior supplies about 35% of the gain rather than all of it and the record falls under the strict reading of the author's own pre-registration too; the published +0.0235 is in any case a maximum over eleven models the DrEval paper's own Friedman test cannot distinguish (p = 0.742), so ratios against it carry no effect-size meaning; the second generation required patching drevalpy's `GroupKFold` call with `shuffle=True`, because in 1.3.5 the split seed provably does not change LDO test folds, so it is independent but not unmodified-package-generated; the result survives removing the 49 drug-combination "drugs" (+0.2031, +0.2023) but is roughly three times weaker for drugs with no close training analogue (max Tanimoto < 0.30: pooled +0.1615 and +0.1114, per-split mean +0.1174 and +0.0527, 7/10 and 5/10 splits positive), i.e. not separable from the bar on the independent generation's hardest band, and that novel-scaffold band is the part that does depend on the external prior, going negative without it (−0.0186 and −0.0147 per-split); the vault diagnostics on the 82 drugs held out of all development reproduce exactly from the package's now-shipped and provably pre-registered vault list but are too noisy to establish anything (+0.1153 and +0.0868 at standard errors of 0.1404 and 0.1437, t = 0.8 and 0.6), and the package's strictest-exclusion figure (+0.1736 at a Tanimoto-0.50 exclusion) is shipped as a receipt but needs the external prior rebuilt to check and was not verified here; and two of the six artefacts whose sha256 `PREREG.v4.md` freezes no longer match it, because a path sanitisation rewrote their path literals — a disclosed and separately documented change which this skeptic verified, by diffing against the originals with paths masked, to be nothing but those literals plus one `import os` line per file, with every constant, threshold and hyperparameter intact and the other four frozen artefacts, the whole model among them, matching exactly.

(File paths are as in this package. The reviewers' sentence exactly as signed off is in panel/gate.md.)

## Check it yourself

`sh verify-it-yourself/run_checks.sh` from this folder (needs Python 3 with numpy and pandas; set
`PYTHON=...` if your `python3` lacks them). No network, no drevalpy, no dataset download. About 15 seconds.
Expected last line: `PASS`.

It recomputes the benchmark's own statistic from `object/`, which holds every test pair of all 10 CV splits
of both split generations with the ground truth, this model's prediction and the reference baseline's. It
checks the leave-drug-out property, replays the baseline to confirm it has not been doctored, verifies both
margin conditions, and confirms the result survives without drug combinations. It then corrupts the object
five ways and requires the checker to run to completion and report `FAIL` on each — a crash does not count
as a rejection. Real output: `verify-it-yourself/RECEIPTS.md`.

## Compared to

| bar | normalized R^2 | source |
|---|---:|---|
| best of all 11 published models (MultiOmicsNeuralNetwork) | **+0.0235** | status page, re-fetched 2026-10-23T23:49:53Z, HTTP 200, sha256 `b7dd9273…4364`, unchanged since 2025-10-17 |
| published reference baseline (NaiveMeanEffectsPredictor) | −0.0169 | same page |
| my same-environment, same-splits re-run of that baseline | −0.0247 | `object/` |
| my same-environment, same-splits re-run of that leader | **−0.0268** | `how-we-built-it/leader_seed42.txt` |
| **this model, official seed-42 splits** | **+0.2249** (SE 0.0354) | `object/` |
| **this model, an independent second split generation** | **+0.2268** (SE 0.0482) | `object/` |

Paired over the 10 official splits against the leader's re-run: this model wins **10/10**, mean difference
+0.2512, paired t = 7.61, p = 3.3e-05, Wilcoxon p = 0.0020.

Partial win **p1** is also met: normalized Pearson 0.4896 and Spearman 0.4504 against the published rank
leaders 0.3538 and 0.3559.

**Null test** (`how-we-built-it/null_test.md`): 400 permutations giving every drug another drug's chemistry,
consistently in training and test. Best control −0.0055 against the real +0.2243 — 53 control standard
deviations. Controls land *below* zero, because a wrong potency estimate actively hurts.

## How it works, in one paragraph

In leave-drug-out the reference baseline sets an unseen drug's effect to zero, so the residual the metric
grades is dominated by the held-out drug's **average potency across cell lines** — 69% of residual variance,
measured here. The benchmark is therefore mostly asking how potent a molecule is, from its structure. The
benchmark's own ~420 training drugs are too few to learn that, so this model adds one scalar: a prior
trained on **53,486 NCI-60 compounds** to predict panel-mean log10 GI50 from Morgan fingerprints, after
removing every compound sharing a skeleton with, or within Tanimoto 0.60 of, any CTRPv2 drug. Everything
else — the kernel weights, the ridge strength, the intercept, the shrinkage — is fitted by drug-grouped
cross-validation inside each split's training drugs.

## Not claimed

- **No clinical or treatment meaning.** This is a benchmark result on a public cell-line screen.
- **The metric is narrower than the setting's name.** Most of what it scores is average potency, not
  personalised response. This model predicts **one number per drug**, so the ~31% of scored variance that is
  drug x cell-line interaction is untouched.
- **Part of what the benchmark calls potency is assay design.** The maximum tested concentration explains
  **26.5%** of the drug-level potency variance. Dose metadata was forbidden as a model input for that reason.
- **Part of the gain is analogue knowledge**, and it is monotone in how strictly analogues are excluded from
  the external prior: 0.85 → +0.227, 0.70 → +0.172, **0.60 (used here)** → +0.163, 0.50 → +0.123 on
  development data; +0.1736 confirmatory at the strictest setting.
- **Novel scaffolds are the weakest band**, not a solved case: +0.1615 and +0.1114 pooled, but only 7/10 and
  5/10 splits positive, and not positive at all when the training set was reduced. See `DIAGNOSTICS.md`.
- **The published differences are not statistically significant.** The DrEval paper's own leave-drug-out
  Friedman test over all 11 models gives **p = 0.742**, and this work's own re-run of the leader lands 1.30
  SE from its published value. A ratio against that maximum carries no effect-size meaning; the absolute
  value, the across-split spread and the paired margin over the re-runs are the defensible statements.
- **The comparison is not like-for-like on training data.** Every leaderboard model learns from CTRPv2's 545
  compounds; this adds about 53,500 external ones. The demonstrated finding is that **the training
  distribution was the binding constraint**, not that the modelling is better on the same data.
- **No claim of methodological originality.** See Credits.

## Three defects found in the benchmark's tooling, reported as a duty

Details and evidence in `the-record-we-beat/RECORD.md` and `DIAGNOSTICS.md`.

1. **The split seed does not change the leave-drug-out test folds** in drevalpy 1.3.5: rows are shuffled
   with the seed and then handed to `GroupKFold`, whose fold assignment ignores row order. Seeds 42, 7 and
   20261023 give identical test drug sets in all 10 folds. A "seed repeat" built that way is not a repeat;
   this package's second generation was built by giving the package's own `GroupKFold` call `shuffle=True`
   and accepted only after a pre-committed independence check. This also answers partial win p3.
2. **The normalized metric double-counts duplicated pairs**: the ruler is attached by a left merge on
   (drug, cell line, split) and CTRPv2 has 4,118 duplicated keys, so 235,974 predictions become 245,122
   scored rows (+0.2249 versus +0.2244 row-aligned; both reported).
3. **Every model after the first in a run trains on the validation rows again**, because `experiment.py`
   binds `train_dataset = split["train"]` without copying and then mutates it. This claim is unaffected
   (clean-ruler re-score: +0.2243 versus +0.2244), but the published report ran 11 models in one pipeline,
   so its ruler may depend on model order. This work cannot establish that from the artefacts it has.

Separately, the leader's hyperparameter tuning is **nondeterministic**: re-running one fold selected a
different architecture and gave predictions correlating 0.75 with the first run.

## Credits

- **Judith Bernett, Pascal Iversen, Mario Picciani, Mathias Wilhelm, Katharina Baum and Markus List** —
  DrEval and `drevalpy`, Nature Communications 2026, article 4238. The benchmark, the splits, the metric,
  the baselines and the pipeline this result is produced and scored by are all theirs.
- **Lavelle, Zhu, Marlor, Brettin and Stevens**, arXiv:2608.11444 (2026) — **the idea of improving
  unseen-drug prediction by training on the public NCI-60 screen is theirs**, with drug-blind R^2 rising
  from 0.03 to 0.22 on an NCI-60-dominated expansion. This work's addition is a checkable exclusion rule and
  a sensitivity curve over its threshold.
- **Cortés-Ciriano and co-workers** (`10.1093/bioinformatics/btv529`) and **Martorana et al.**
  (`10.3390/ijms232214374`) — NCI-60 panel potency QSAR is an established problem; the external prior here
  is a plain instance of it.
- **NCI Developmental Therapeutics Program** — the public NCI-60 growth-inhibition data.
- **Codicè et al.** (J. Cheminform., 2025) — showed IC50 tracks the maximum tested concentration on GDSC;
  this work measured the same effect on CTRPv2.
- Target definition and verification discipline: the V3R1T4S bank.
- Contributor credit: **Sherpa** (github.com/shitcoinsherpa).
