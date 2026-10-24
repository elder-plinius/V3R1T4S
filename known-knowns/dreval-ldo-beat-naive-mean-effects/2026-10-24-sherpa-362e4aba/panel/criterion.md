# Panel verdict — CRITERION skeptic

context: subagent
target: `dreval-ldo-beat-naive-mean-effects`
seat: decide literally whether the result meets the full success criterion or one named enumerated partial
win; hunt hidden quantifiers and stretched definitions; check null models; pass only for a genuine,
non-subsumed win.
read: the claim package only, plus the two other panel verdicts, the pinned bank entry, the installed
drevalpy 1.3.5 source, the pinned dataset and the raw drevalpy result directories (both outside the run
tree), and the live status page. I did not open `attempts/`, `scout.md`, `BRIEF.md`, `target.md` or any
`REPORT.md`/`LOG.md`/`dossiers/`.

Every number below is from real command output in my own scratchpad, computed by me unless I say otherwise.

**This verdict has been revised three times**, as the package was remediated under it: the coordinator
fixed shortfalls it named, that round introduced two regressions which I caught, those were repaired, and a
submission leak rule then forced a further path sanitisation. Section 7 records every pass. Sections 1–6 are
as first written except where a statement became false, which I have corrected in place and marked. Only the
`confirmed_scope` sentence below should be quoted; earlier versions of it are superseded.

---

## 1. The criterion, quoted from the pinned bank, clause by clause

From `bank/targets.json`, id `dreval-ldo-beat-naive-mean-effects`, field `success_criterion`, verbatim:

> Success means a drevalpy model class, run through drevalpy's own pipeline on the same dataset and test
> mode as the public report (CTRPv2, test_mode=LDO, same number of CV splits, lnIC50 response,
> package-generated splits), whose mean normalized R^2 computed by drevalpy's own evaluation code is
> STRICTLY HIGHER (direction: max) than the maximum normalized R^2 over ALL models in
> https://dilis-lab.github.io/drevalpy-report/heatmaps/heatmap_algorithms_LDO_normalized.html, re-fetched
> and re-decoded live immediately before claiming, by at least 0.02 absolute AND by at least 2x the
> across-split standard error of the attacker's result, with the attacker's own same-environment
> same-splits re-run of BOTH the NaiveMeanEffectsPredictor and the published LDO leader
> (MultiOmicsNeuralNetwork) included, and the attacker's value beating both. Deliverables: pinned drevalpy
> version/commit, model source, exact invocation, per-split prediction and ground-truth CSVs, the generated
> report directory, and a seed-repeat run showing the gain survives a second independent split generation.
> Chemical features for held-out drugs must be derived from structure/target annotations only; no
> information computed from the test drugs' responses (including per-drug means, ranks, or any statistic of
> the held-out fold) may enter the model.

I also read the entry's `partial_wins` (p1, p2, p3), `verification_method` and all six `pitfalls` myself
rather than relying on the package's quotation of them. The package's quotation in
`how-we-built-it/PREREG.md` §1 is faithful word for word.

### 1.1 "a drevalpy model class" — MET

`how-we-built-it/potency_transfer_model.py` defines `class PotencyTransfer(DRPModel)` with
`cell_line_views`/`drug_views`, `train()`, `predict()`, `load_*_features()`, and is registered into
`MODEL_FACTORY` and `MULTI_DRUG_MODEL_FACTORY`. Its sha256 is
`e647a5cac3a85051c7905993225044ee8306fe8d24e56aba401b6ca0d129fc8d`, byte-identical to the hash frozen in
`how-we-built-it/PREREG.v4.md` §1. I verified all six frozen hashes in that table that are shipped
(`potency_core.py`, `potency_transfer_model.py`, `potency_core_fast.py`, `h10_build_teacher.py`,
`h10_teacher_threshold.py`, `teacher_pred.csv`) — all match. I also verified the pre-registration chain's
own hashes: `PREREG.md` = `e5adc0f5…bcff5131` exactly as `PREREG.v2.md` records, and `PREREG.v2.md` =
`29260e18…3126d5d2` exactly as `PREREG.v3.md` records.

### 1.2 "run through drevalpy's own pipeline" — MET

`how-we-built-it/run_confirmatory.py` calls the package's own entry point, `drevalpy.utils.get_parser()` and
`drevalpy.utils.main(args)`; the only deviation from stock is inserting the class into the model factories.
The raw outputs sit in drevalpy's own layout (`RUN_ID/CTRPv2/LDO/PotencyTransfer/{predictions,best_hpams}`,
`.../splits/`), which I inspected directly. `best_hpams_split_*.json` are all `{}`, consistent with
`get_hyperparameter_set()` returning `[{}]` — so drevalpy's outer tuning loop never sees a test fold.

### 1.3 "same dataset and test mode … (CTRPv2, test_mode=LDO, same number of CV splits, lnIC50 response, package-generated splits)" — MET

- **CTRPv2** — the pinned October-2025 record. One honest wrinkle, which the package raises before I could:
  the status page itself names neither its dataset nor its setting. I confirmed that on my own fetch: the
  4,665,771-byte page contains **0** occurrences of `LDO` and **0** of `CTRP`, and its HTML title element is
  `plotly-logomark`. The CTRPv2/LDO identification rests on the URL, the parent report's cross-study tables
  and the DrEval paper. `the-record-we-beat/RECORD.md` states this explicitly. Accepted.
- **test_mode=LDO** — `--test_mode LDO`, and I verified the leave-drug-out property exhaustively rather than
  by sampling: in all 20 splits of both generations, test ∩ (train ∪ validation) = ∅, no predicted drug lies
  outside its test fold, every test drug has predictions, and each of the 545 drugs is a test drug in
  **exactly one** split (10 folds partition all 545).
- **same number of CV splits** — 10. The leader's heatmap text cell is `0.023 ± 0.032`, consistent with the
  across-split SD of 0.1060 that the claim decodes from the companion violin plot at n = 10.
- **lnIC50 response** — verified at source, not taken on trust. The ground truth in `object/` equals the
  pinned dataset's `LN_IC50_curvecurator` column on every key: 235,974 non-NaN rows on both sides, 0 keys
  present on only one side, max absolute difference `4.999979e-07` (the documented 6-decimal rounding).
- **package-generated splits** — for the official generation, yes and by the package's own default:
  drevalpy 1.3.5 `experiment.py` line 135 hard-codes `random_state=42`. The *second* generation is not
  unmodified package code; see §1.8.

### 1.4 "mean normalized R^2 computed by drevalpy's own evaluation code" — MET; I ran that code myself

I read `drevalpy/visualization/utils.py::_normalize_metrics_by_mean_effects` and
`drevalpy/evaluation.py` in the pinned install: the statistic is, per CV split, `sklearn.metrics.r2_score`
of `(y_true − y_pred_naive)` against `(y_pred − y_pred_naive)`, after a **left merge** of the
NaiveMeanEffectsPredictor's predictions on `(drug_name, cell_line_name, CV_split)`.

I then ran the package's own `parse_results` → `prep_results` chain (the sequence drevalpy-report runs) on
the raw result directories, with my own script rather than the shipped one:

```
PotencyTransfer              splits 10  normR2 +0.224884  SD 0.1119  SE 0.0354  normPearson +0.4896  normSpearman +0.4504  rawR2 +0.2753  pairs 235974
NaiveMeanEffectsPredictor    splits 10  normR2 -0.024736  SD 0.0273  SE 0.0086  normPearson +0.0000  normSpearman +0.0000  rawR2 +0.0422  pairs 235974
MultiOmicsNeuralNetwork      splits 10  normR2 -0.027535  SD 0.1234  SE 0.0390  normPearson +0.2252  normSpearman +0.2195  rawR2 +0.0396  pairs 128344
```
```
(independent generation)
PotencyTransfer              splits 10  normR2 +0.226820  SD 0.1523  SE 0.0482  normPearson +0.4878  normSpearman +0.4487  rawR2 +0.2771  pairs 235974
NaiveMeanEffectsPredictor    splits 10  normR2 -0.018514  SD 0.0214  SE 0.0068                                                           pairs 235974
```

So **+0.2249 and +0.2268 are the benchmark package's own numbers**, not a variant and not the claimant's
reimplementation. No metric swap: the quoted figure is the normalized metric, and the raw R² (+0.2753,
which is higher and which the named pitfall warns about) is nowhere used as the headline.

**Is quoting +0.2249 rather than +0.2244 legitimate? Yes.** I reproduced both from `object/` alone and
confirmed the stated cause: 4,118 duplicated `(cell_line, drug)` keys expand 235,974 predictions into
245,122 scored rows under drevalpy's left merge (I counted `keys with >1 row: 4118`, `extra rows: 9148`,
`merged rows total: 245122`). The criterion's words are "computed by drevalpy's own evaluation code", so
+0.2249 *is* the criterion's quantity; +0.2244 is the stricter row-aligned cross-check, and the package
quotes the smaller one in its own checker. Both appear in `RUN_IT_YOURSELF.md`, `DIAGNOSTICS.md` and
`verify-it-yourself/RECEIPTS.md`. Nothing is hidden and the direction of the disclosure is against the
claimant.

### 1.5 "STRICTLY HIGHER than the maximum over ALL models … re-fetched and re-decoded live immediately before claiming" — MET; I re-fetched and re-decoded it

My own fetch, `2026-10-24T02:41:09Z`: HTTP 200, 4,665,771 bytes, sha256
`b7dd9273b4a9efbf36d5d8718a4163c73d1132f7fe8580c9dfd246e55d2c4364` — byte-identical to the hash recorded in
`the-record-we-beat/RECORD.md` and to the one the novelty seat got. `last-modified` came back
`Fri, 17 Oct 2025 14:20:42 GMT` where the package recorded `:41` and the novelty seat got `:40`; the etag
encodes mtime, the byte count field is identical, and the content hash is identical, so this is edge-node
clock skew, exactly as the package already says. Not held against the claim.

Decoded by me from the page's own base64 `"dtype":"f8"` little-endian arrays, `"shape":"11, 1"`:

```
RandomForest -0.118614 | NaivePredictor -0.089200 | NaiveTissueMeanPredictor -0.060534
MultiOmicsRandomForest -0.041560 | ProteomicsRandomForest -0.040085 | ElasticNet -0.030473
DIPK -0.018102 | NaiveMeanEffectsPredictor -0.016911 | SimpleNeuralNetwork -0.010500
GradientBoosting +0.010826 | MultiOmicsNeuralNetwork +0.023466
LIVE MAX over all models: +0.023466 = MultiOmicsNeuralNetwork
```

All eleven values agree with the package's table. The rank panel decodes to DIPK leading at Pearson
+0.3538 and Spearman +0.3559, also as recorded.

### 1.6 "by at least 0.02 absolute AND by at least 2x the across-split standard error" — MET, with room, on every variant I tried

| generation | mean normR2 | SE | margin over +0.023466 | needs ≥ 0.02 | needs ≥ 2·SE |
|---|---:|---:|---:|---|---|
| seed 42 (drevalpy's own eval) | +0.224884 | 0.0354 | +0.201418 | yes | yes (0.0708) |
| independent (drevalpy's own eval) | +0.226820 | 0.0482 | +0.203354 | yes | yes (0.0964) |
| seed 42, row-aligned | +0.224402 | 0.0352 | +0.200936 | yes | yes |
| seed 42, single agents only | +0.2031 | 0.0406 | +0.179634 | yes | yes |
| independent, single agents only | +0.2023 | 0.0523 | +0.178834 | yes | yes |

10/10 splits positive in both generations (worst split +0.0913 and +0.0252).

### 1.7 "same-environment same-splits re-run of BOTH … included, and the attacker's value beating both" — MET; I verified both re-runs independently

- **NaiveMeanEffectsPredictor**: −0.024736 (seed 42) and −0.018514 (independent) by drevalpy's own
  evaluation. Its per-pair predictions are shipped in `object/`, so this one is checkable from the package
  alone.
- **MultiOmicsNeuralNetwork**: −0.027535 over 10 seed-42 folds by drevalpy's own evaluation. On the
  independent generation I recomputed the per-fold runner's 10 folds myself and got **−0.0931** (3/10
  positive) against the package's reported −0.0928.
- **A like-for-like row check the package does not report, which I add as supporting evidence.** drevalpy
  scores the leader on only **128,344 of 235,974** pairs (477 of 884 cell lines) because of its omics
  feature-availability filter, while PotencyTransfer, whose views are identifiers only, is scored on all
  235,974. Restricting PotencyTransfer to the leader's *own* covered pairs on seed 42:

```
mean PT on leader-covered pairs: +0.2228 (SE 0.0352)
mean leader on same pairs:       -0.0264 (SE 0.0385)
PT wins splits: 10 /10  mean diff +0.2492
```

  and on the independent generation, restricted the same way, PT +0.2244 against the leader's −0.0931,
  winning 10/10. So the asymmetry runs against the claimant (it is scored on the complete, harder set) and
  the comparison survives when corrected.
- **~~Deliverable gap~~ — RESOLVED in the second pass (§7.1).** When I first wrote this, the leader's
  per-pair predictions were not in `object/` and I could only verify its number because the raw run
  directories happen to be on this machine. They are now shipped as 20 `*_leader_predictions.csv.gz` files
  and I verified them against drevalpy's own raw output; `check_claim.py` scores the leader from them. The
  reproduce seat's open item §9 is now fully closed.

### 1.8 "a seed-repeat run showing the gain survives a second independent split generation" — MET, by a substitution I judge legitimate

The pre-registered mechanism provably cannot deliver what the criterion asks. I confirmed the defect two
ways. In the pinned install, `datasets/dataset.py::_leave_group_out_cv` shuffles rows with the seed and then
calls `GroupKFold(n_splits=n_cv_splits)` (its own comment: "shuffle, since GroupKFold does not implement
this"); and empirically, pre-shuffling with different seeds and then calling `GroupKFold` gives
**10/10 identical fold group-sets in the same order**. So "a seed repeat" and "a second *independent* split
generation" are contradictory requirements in drevalpy 1.3.5.

`PREREG.v5.md` was written **before** the replacement existed, states the defect, declares the already
completed seed-20261023 run **void as the repeat** (it had in fact passed, at 0.2250 — so the retraction
cost the claimant evidence rather than saving it), demotes it to a validation-split sensitivity observation,
and pre-commits an acceptance test. I checked the replacement from `object/` alone and it passes that test:

```
seed42 test fold sizes: [55,55,54,54,54,55,54,55,55,54] sum 545
indep  test fold sizes: [55,55,55,55,55,54,54,54,54,54] sum 545
identical folds: 0
best-match Jaccard per seed42 fold: 0.078 0.079 0.101 0.102 0.080 0.089 0.090 0.069 0.089 0.102
mean best-match Jaccard: 0.0880   (pre-committed bound < 0.25)
```

**Honest cost, which I put in the scope sentence:** the second generation is produced by drevalpy's own
`split_dataset` with one injected change — `GroupKFold(shuffle=True, random_state=seed)` — so it is *not*
unmodified package code. I accept it because the criterion's repeat clause asks for *independence*, which
only the patch can deliver, while the phrase "package-generated splits" sits with the main protocol
description, which the seed-42 generation satisfies completely and which is the generation the headline
number comes from.

### 1.9 Deliverables — met except one named item, plus packaging defects

| deliverable | status |
|---|---|
| pinned drevalpy version/commit | **met** — 1.3.5 (PyPI), version not commit, which the wording allows |
| model source | **met** — shipped and hash-verified against `PREREG.v4.md` |
| exact invocation | **met in substance** — `run_confirmatory.py` prints the full drevalpy arg dict; `repro_seed42.sh` is the baseline/leader CLI line. The absolute paths I first criticised are gone, but the substitution that removed them left this file **syntactically invalid Python** (§7.4) |
| per-split prediction and ground-truth CSVs | **met** for the model, the ruler **and now the leader** — I verified all of `object/` against drevalpy's own written `predictions_split_*.csv` row for row (max abs difference `5.00e-07` on predictions, ruler, leader and truth alike, i.e. the documented rounding) |
| the generated report directory | **met in substance** (was absent on my first pass) — `how-we-built-it/generated-report/` now holds drevalpy's own `parse_results`→`prep_results` evaluation tables for both generations, whose values match my own run of that code to six decimals. The multi-megabyte HTML tree is excluded for a stated submission-kit reason, with the regeneration command given (§7.2) |
| seed-repeat on a second independent generation | **met** — §1.8 |

I weighed the then-missing report directory as a packaging shortfall rather than a criterion failure: its
entire content for this purpose is the normalized-metric table, which I regenerated myself with the
package's own code, and the per-pair CSVs that back it are shipped. It has since been shipped (§7.2).

### 1.10 "structure/target annotations only; no information computed from the test drugs' responses" — the decisive clause. MET on the literal reading, with a reservation I record in full

What actually reaches a held-out drug, from reading `potency_core.py` and `potency_transfer_model.py` line
by line:

1. its Morgan-2048 fingerprint, from the dataset's own `drug_fingerprints/` table — **structure**;
2. its target-pathway set from `drug_pathways.csv.gz`. I inspected that file: it is literally
   `(pubchem_id, drug_name, pathway)` over 1,993 KEGG/Reactome terms (e.g. `REAC:GRB2 Events In EGFR
   Signaling R-HSA-179812`) — **target annotation**, which the criterion names as allowed;
3. one scalar `z = f(fingerprint)` from the external potency prior.

Everything the model *fits* — cell-line means, the global mean, the per-drug mean residual targets and their
weights, the prior's standardisation `zm`/`zs`, the kernel weights β and τ, the ridge α, the intercept and
the shrinkage κ (all by 5-fold drug-grouped CV with fixed `INNER_SEED=12345`) — is computed inside `fit()`
from the rows the pipeline hands it, i.e. training drugs only. No dose metadata
(`min_dose_M`/`max_dose_M`, which the claimant's own prereg forbade) and no CTRPv2 column but identifiers
and the response are read anywhere. The second half of the clause — "no information computed from the test
drugs' responses (including per-drug means, ranks, or any statistic of the held-out fold)" — is therefore
cleanly satisfied, and the exhaustive leave-drug-out check in §1.3 is its empirical confirmation.

**The hard part is the prior.** `f` was fitted on 53,486 *other* compounds' NCI-60 panel-mean log10 GI50 —
external **experimental response** data. Every CTRPv2 compound was excluded from its training set three
ways (`h10_build_teacher.py`, `h10_leak_audit.py`, `h10_teacher_threshold.py`, all shipped and
hash-verified): PubChem CID identity; salt-stripped InChIKey connectivity-block match, which caught 3
compounds the original rule had let through as salt forms (NSC 373989, 721951, 757444); and Morgan Tanimoto
≥ 0.60 to **any** CTRPv2 compound. So no held-out drug's own measured response — in CTRPv2 or in NCI-60 —
can reach the model.

The question the criterion forces is whether a response-trained QSAR output counts as "derived from
structure/target annotations only". Two readings:

- **per-drug derivation**: the feature *value* for a held-out drug must be a function of that drug's
  structure/target annotations. Satisfied exactly — `z` is `f(fingerprint)` for a fixed `f`, which the
  package's own test demonstrates (two CTRPv2 drug pairs have byte-identical fingerprints and receive
  identical prior values to 0.0 although their CTRPv2 responses differ by up to 2.3 ln units; re-running the
  saved network reproduces the shipped `teacher_pred.csv` up to one constant, max deviation 6.07e-07).
- **provenance of the whole pipeline**: every bit of information inside the feature, parameters included,
  must trace to structure/target annotations. Violated.

**I take the per-drug reading, and I think it is the criterion's own.** Four reasons, in the text rather
than in how impressive the result is. (i) The sentence's subject is "chemical features **for held-out
drugs**" — it is scoped to what may be known about *them*. (ii) Its own companion clause enumerates exactly
what is banned, and it is test-drug response statistics, not external training corpora. (iii) The bank's
`pitfalls` localise the worry to statistics "computed on the full dataset", i.e. CTRPv2. (iv) The bank's own
suggested `angles` include drug features built from cell-line dependency/expression correlations, which a
provenance reading would also forbid; and the criterion nowhere constrains training-set composition. A QSAR
prediction from a fingerprint is a structure-derived descriptor in the ordinary cheminformatics sense.

**The reservation, which the package must state and currently does not.** `how-we-built-it/PREREG.md` §5,
frozen at 21:37:05Z before anything was scored, lists as forbidden: "`meta/gcmf_drug_relations/
drug_bioassay.csv.gz` **and any other external *experimental activity* data**. Not structure, not target
annotation." The prior's training target is external experimental activity data. `H10-PRECOMMIT.md`
(22:32:51Z) introduces it and `PREREG.v4.md` (23:12:55Z) freezes it while asserting that `PREREG.md`
"stands" — and **neither addresses that clause**. I grepped all of `claim/`: the phrase "experimental
activity" occurs in exactly two places, §5 itself and a line in `RUN_IT_YOURSELF.md` defending the pathway
table. A reader of §5 alone would conclude the method was barred by its own pre-registration.

I do not fail the claim on it, for three reasons. The bank's criterion, not the attacker's prereg, is what I
am seated to judge. §5's named target is a table of the benchmark drugs' *own* measured activities — the
direct back-door that the exclusion rule is built to prevent — so the narrow reading of §5 is coherent. And
the decision was made before any of its results were scored, with its one post-hoc amendment (0.85 → 0.60)
moving against the claimant's interest. But it is a real hole in the paper trail, it is the hole a hostile
reader will find first, and the package should name it rather than leave it to be discovered.

**Addressed in the second pass.** `PREREG5-RECONCILIATION.md` now states the contradiction, gives both
readings, declines to adjudicate the author's own ambiguous text in the author's favour, and shows the claim
clears every pre-registered bar under the **strict** reading too, using the τ = 0 ablation. I checked that
arithmetic: +0.1450 (seed 42) against a strict-reading bar of max(0.0435, 0.0235 + 2·0.0284) = 0.0803, and
+0.1556 (independent) against max(0.0435, 0.0235 + 2·0.0333) = 0.0901. I also checked the clause the
reconciliation does not: pairing my own τ = 0 per-split values against the leader's re-run split by split,
the no-prior model beats the leader in **10/10** seed-42 splits as well. So the criterion's substantive
conditions are met under both readings, which is the strongest form this could have taken.

---

## 2. The pre-registration, checked honestly

| file | written | what it changes | my judgement |
|---|---|---|---|
| `PREREG.md` | 21:37:05Z | the criterion, statistic, thresholds, vault, forbidden inputs, `null_test: required` | frozen before any scoring; hash matches what v2 records |
| `PREREG.v2.md` | 21:49:20Z | 1.6.0 → **1.3.5**, because 1.6.0 does not contain the published leader | **legitimate factual correction.** I confirmed `MultiOmicsNeuralNetwork` exists in the installed 1.3.5. Without it the criterion's own leader-re-run clause is unsatisfiable. Adds an obligation (reproduce the baselines first), which is a tightening |
| `PREREG.v3.md` | 22:00:19Z | pins the October-2025 data record, because the current one's methylation view (80 PCs) is too narrow for the leader's own 100-PC hyperparameters | **legitimate.** The alternative was patching the published model's settings, which would stop it being the published model. States that responses are identical across records to 4.1e-14 |
| `PREREG.v4.md` | 23:12:55Z | freezes the model, the grids and the confirmatory protocol, with hashes; declares the diagnostics to be reported whatever they show | **legitimate, and the hashes hold** — all six shipped artefacts match. Its §2 states the number of development configurations (~15) and that development numbers are not the claim. Its one defect is silence on `PREREG.md` §5 (§1.10 above) |
| `PREREG.v5.md` | 23:25:30Z | voids the pre-registered seed repeat and defines a corrected generation | **legitimate substitution, not a loosening** — §1.8. Written before the replacement existed, with a pre-committed acceptance test I verified (0/10, 0.0880), and it discarded a run that had already passed |
| `H10-PRECOMMIT.md` | 22:32:51Z, amended 22:34:05Z and 23:02:29Z | the prior's source, target, exclusions and reporting duties | **legitimate.** Amendment 1 records a ≥30-measurement filter rather than folding it in silently. Amendment 2 replaces Tanimoto 0.85 with salt-stripped skeleton matching plus 0.60 **after** a leak audit found 3 CTRPv2 compounds inside the prior, and it is strictly *stricter* (development +0.227 → +0.163). An outcome-informed loosening moves the bar toward the claimant; this moves away from it. A later "Attribution" section was appended on 2026-10-24 and says so |

**Does the v5 substitution void the pre-registered condition?** No. The condition's operative content is
"the gain survives a second **independent** split generation"; the seed mechanism cannot produce one in this
package, which is a defect in the benchmark, not a choice by the claimant. The substitution is minimal,
pre-committed, independently checkable from the shipped object, and verified. What it does cost is the
phrase "package-generated" for that one generation, and my scope sentence says so.

One pre-committed reporting duty was unfulfilled on my first pass: `H10-PRECOMMIT.md` item 5 promises
results "with and without the teacher, whatever the outcome", and no without-teacher number appeared
anywhere in `claim/`. I ran it; it has since been run independently and shipped. See §4 and §7.

---

## 3. Hidden quantifiers and stretched definitions — what I hunted and what I found

- **Subsetting / abstention — none.** The scored set is the whole benchmark: 235,974 of 235,974 scorable
  pairs, 545/545 drugs, 886/886 cell lines, in both generations. **Zero NaN predictions** — which matters,
  because `drevalpy/evaluation.py` silently masks NaN rows, so NaN is an invisible abstention channel; there
  is none here. The shipped checker also asserts `test drugs with no prediction: 0`, and my own run of it
  confirms the corruption "drop the 5 worst test drugs per split" is now rejected.
- **Metric swap — none.** §1.4.
- **Duplicate-key arithmetic — benign and fully disclosed.** §1.4.
- **Drug combinations — a real leak the claim benefits from, but not one it rests on.** 49 of 545 CTRPv2
  "drugs" are `mol-mol` combinations whose single-agent components can sit in training (drevalpy issue
  #300). With them removed: +0.2031 (seed 42) and +0.2023 (independent), both still clearing the 0.02 and
  2·SE conditions; combinations alone score +0.2030 and +0.1639, i.e. about the same, so the gain is not
  concentrated in them. Reported in `DIAGNOSTICS.md` and enforced as a permanent assertion in
  `verify-it-yourself/check_claim.py`.
- **Analogue concentration — the genuine qualification, and the package's figures are exact.** The bank's
  dominant pitfall after leakage demands the skeptic report each test drug's maximum Tanimoto to the
  training set and show the gain is not confined to high-similarity drugs. I recomputed the pre-declared
  bands myself from the dataset's own fingerprints against each split's own train+validation set, single
  agents only, and **every figure in `DIAGNOSTICS.md` reproduces to 4 decimals**:

```
seed42 (single agents only)
  maxsim [0.00,0.30): drugs  207 pairs   85262 pooled +0.1615  per-split mean +0.1174  splits>0 7/10
  maxsim [0.30,0.45): drugs  118 pairs   52387 pooled +0.0900  per-split mean +0.0074  splits>0 7/10
  maxsim [0.45,0.60): drugs   80 pairs   33918 pooled +0.4485  per-split mean +0.3826  splits>0 10/10
  maxsim [0.60,1.01): drugs   91 pairs   34216 pooled +0.3438  per-split mean +0.2644  splits>0 7/10
independent (single agents only)
  maxsim [0.00,0.30): drugs  214 pairs   90342 pooled +0.1114  per-split mean +0.0527  splits>0 5/10
  maxsim [0.30,0.45): drugs  109 pairs   45761 pooled +0.1989  per-split mean +0.1324  splits>0 8/10
  maxsim [0.45,0.60): drugs   80 pairs   33755 pooled +0.4028  per-split mean +0.1465  splits>0 6/10
  maxsim [0.60,1.01): drugs   93 pairs   35925 pooled +0.3881  per-split mean +0.1980  splits>0 7/10
```

  The pitfall's test is passed: the gain is **not confined** to close analogues — the novel-scaffold band
  (207 and 214 drugs, ~40% of single agents) clears the 0.0435 bar pooled in both generations. But it is
  weakest and least stable there, and on the independent generation its per-split mean is +0.0527 with only
  5/10 splits positive, which is not separable from the bar. The package says precisely this, in
  `DIAGNOSTICS.md`, including that in the development setting with a smaller training set the band was not
  positive at all. That is the right disclosure and it is accurate.
- **What the metric is.** I measured the decomposition myself on the confirmatory object: the between-drug
  share of the normalized residual variance is **71.1%** (seed 42) and **71.0%** (independent), and an
  oracle that knew each held-out drug's true per-drug offset would score **+0.7112** / **+0.7097**. So this
  model sits at ~32% of the per-drug ceiling and contributes essentially nothing to the remaining ~29%
  drug × cell-line interaction. The package's "69% / ~31%" framing (measured on development data) is if
  anything conservative relative to what I measure.
- **Robustness I could not verify.** The strictest-exclusion sensitivity figures — development 0.85→+0.227,
  0.70→+0.172, 0.60→+0.163, 0.50→+0.123, and confirmatory **+0.1736** at the 0.50 threshold — and the vault
  diagnostics (+0.1153 on all 82 vault drugs, +0.0868 on the 74 never exposed) were, on my first pass, cited
  to files under `attempts/`. They are now shipped as receipts inside the package
  (`how-we-built-it/teacher050_seed42.txt`, `diagnostics_seed42_partial.txt`), which is an improvement in
  disclosure but **not** in verifiability: recomputing the 0.50 figure needs the prior rebuilt from the
  NCI-60 download, and the vault figures need the 82-drug vault list, which is still not in the package. I
  take both on the claimant's word. The two receipts I *can* check — `similarity_bands.txt` and
  `clean_ruler.txt` — match my own computations exactly (§7.3). Shipping the vault receipt also surfaced
  something the prose does not say; see §7.5.

---

## 4. The null model

`PREREG.md` §6 declares `null_test: required` and specifies the control in advance;
`how-we-built-it/null_test.md` reports it: 400 permutations of the 545-drug universe, each giving every drug
another drug's fingerprint, pathway set **and** prior value, consistently in training and test, on the
pipeline's own saved seed-42 splits, with responses, splits, cell-line effects and tuning untouched. Real
+0.224287; controls mean −0.0266, SD 0.0047, best of 400 **−0.0055**; real beats all 400.

**Is this the right control for this claim? Yes.** The claim is that a drug's chemistry carries transferable
signal beyond the mean-effects baseline, and this control destroys exactly the drug↔chemistry link while
preserving everything else, so it isolates that hypothesis from the possibility that the kernel-ridge-plus-
calibration machinery manufactures positive normalized R² from nothing. The controls land *below* zero, at
the ruler's own level, which is what a dead feature should give. I read `null_test.py`: it builds the ruler
itself per split with a proper `.copy()` (so it sidesteps drevalpy's in-place mutation bug), and its
control −1 is the unpermuted cross-check, landing at 0.2243 — consistent with the clean-ruler figure in
`DIAGNOSTICS.md`, so real and controls genuinely share one metric. The disclosure that controls used the
verified-equivalent fast core (predictions within 2e-7) is adequate.

**The control it should have run and did not.** There is no ablation isolating the external prior — the
same frozen model with the teacher channel removed (τ = 0) on the confirmatory splits. This is the control
that would answer the question the novelty seat's strongest objection turns on: how much of +0.2249 is the
external screen, as against the within-CTRPv2 structural kernel that the leaderboard models could in
principle also have built? `H10-PRECOMMIT.md` item 5 pre-committed to reporting it. The development
narrative in `HOW_WE_FOUND_IT.md` implies the answer (+0.073 fingerprints alone, +0.096 adding pathways,
+0.163 adding the prior — on development data, with 82 drugs withheld), but that is development data, is
outside the package, and is not the confirmatory ablation that was promised.

**So I ran it myself**, on the official seed-42 splits, with the frozen `potency_core.py` (hash-verified,
copied unmodified into my scratchpad) given `taus=(0.0,)` — the teacher channel removed and nothing else
touched, trained on train+validation as the pipeline does for its final fit, scored row-aligned against the
shipped ruler. My harness first reproduces the full frozen model exactly, which is what licenses the
ablation number:

```
RESULT full frozen grid     mean +0.2244 SE 0.0352 pos 10/10 worst +0.0913
  per-split: +0.1804 +0.0913 +0.2823 +0.1813 +0.4639 +0.2922 +0.2458 +0.1110 +0.1283 +0.2674
  tau chosen by the inner CV: [4.0, 4.0, 4.0, 4.0, 0.5, 4.0, 4.0, 4.0, 4.0, 4.0]   (grid max is 4.0)
RESULT NO-teacher tau=0     mean +0.1451 SE 0.0284 pos 10/10 worst +0.0386
NO-teacher all      mean +0.1451 SE 0.0284 pos 10/10
NO-teacher single   mean +0.1118 SE 0.0341 pos  9/10
NO-teacher novel    mean -0.0186 SE 0.0575 pos  6/10      (single agents, max Tanimoto < 0.30)
NO-teacher novel-scaffold POOLED normR2 +0.0504 over 85262 pairs
```

Every per-split value of the full run matches the shipped object to 4 decimals, so this is the frozen model,
not an approximation of it. Two findings, and they cut in opposite directions:

1. **The record falls even without the external screen.** At τ = 0 the within-CTRPv2 structural + target-
   pathway kernel alone reaches **+0.1451** (SE 0.0284, 10/10 splits positive), which clears both margin
   conditions (> 0.0435 and > 0.0235 + 2·SE = 0.0803) and is 6.2x the published maximum; single agents only,
   +0.1118, still clears both. So the external prior supplies about **35%** of the headline gain
   (+0.0793 of +0.2244), not all of it, and the novelty seat's "not like-for-like on training data"
   objection, while correct, does not explain the win away.
2. **But the external prior supplies essentially all of the novel-scaffold performance** — the band the
   bank's dominant pitfall cares about. Without it, drugs with no close training analogue go from a
   per-split mean of +0.1174 (7/10 positive, pooled +0.1615) to **−0.0186** (6/10 positive, pooled +0.0504,
   i.e. at the bar). The inner CV also pushes τ to the top of its allowed grid (4.0) in 9 of 10 splits.

This is the number the pre-commitment promised and it should be in the package, with both readings stated.
It is my computation, on the seed-42 generation only, row-aligned.

**Now in the package, and it replicates (second pass).** `how-we-built-it/ablate_teacher.{py,txt}` runs the
same ablation independently on **both** generations with the fast core and a clean ruler. Their figures
against mine: all drugs +0.1450 vs my +0.1451, single agents +0.1117 vs +0.1118, novel scaffolds −0.0186 vs
−0.0186 (SE 0.0574 vs 0.0575, 6/10 both). The 1e-4 offsets are explained — their "with prior" reference is
+0.2243, the clean-ruler figure, where mine is +0.2244, the shipped-ruler figure — so two different core
implementations and two ruler conventions agree. On the independent generation they add: no prior +0.1556
(SE 0.0333, 9/10), single agents +0.1213 (8/10), novel scaffolds **−0.0147** (4/10). The finding replicates
in both directions on both generations: the record falls without the external prior, and the novel-scaffold
band goes negative without it.

---

## 5. Weighing the other two seats

- **Reproduce (pass).** Every figure in it matches mine; its independent-split and ruler-replay forensics
  are stronger than mine and agree. Its one open criterion item — the leader re-run absent from `claim/` —
  is now partly closed (documented in `LEADER_COMPARISON.md` and four evidence files) and I verified the
  leader's numbers myself from the raw outputs; it is still not recomputable from the package. Its central
  substantive finding, that the gain is ~3x concentrated in drugs with a close training analogue, I
  reproduced exactly, and the package discloses it in band form.
- **Novelty (pass), with one correction from my §4 ablation.** Its first objection — the comparison is not
  like-for-like on training data, and beating the maximum "by changing the data regime" is what the result
  shows — is factually right about the method but overstates the dependence: with the external prior
  switched off the same architecture still reaches +0.1451 on CTRPv2's own 545 compounds, 6.2x the published
  maximum and clearing both margin conditions. The external screen is what makes the result hold on novel
  scaffolds, not what makes it beat the leaderboard.
  Its other three objections stand as written. All four are now carried in the package's own load-bearing
  text, which I checked: Friedman p = 0.742 and "a ratio against that maximum carries no effect-size
  meaning" (`README_BODY.md`, `the-record-we-beat/RECORD.md`, `LEADER_COMPARISON.md`); "not like-for-like on
  training data … ~53,500 external compounds" (same three files); the uncontested frontier
  (`RECORD.md`); and the metric being narrower than the setting's name (`README_BODY.md` "Not claimed",
  `DIAGNOSTICS.md` "What remains unsolved"). Its "26 models" correction is applied — `RECORD.md` now says 27
  — and the Lavelle et al. and NCI-60-QSAR citations have been carried out of the file marked unverified
  into `RECORD.md`, `how-we-built-it/README.md` and `H10-PRECOMMIT.md`.

**Are the package's own disclosures adequate, or does the headline still overstate?** Adequate, with two
limits that I carry into the scope sentence rather than treat as failures. The title —
"normalized R^2 +0.2249 against a published best of +0.0235" — is literally true and is the criterion's own
comparison, and the body qualifies it immediately and unusually candidly. But (a) the juxtaposition invites
a ratio reading that the package itself calls meaningless, and (b) nothing in the title or first screen says
the method adds ~53,500 external compounds that no leaderboard model uses. Both belong in the recorded
result, so both are in my sentence.

---

## 6. Residual defects in the package, as first written (current status in brackets)

1. **The generated report directory is not shipped** — a deliverable the criterion names (§1.9).
   **[FIXED — §7.2]**
2. **The leader's per-pair predictions are not in `object/`**, so its re-run is documented but not
   recomputable from the package (§1.7). **[FIXED — §7.1]**
3. **`PREREG.md` §5's ban on "any other external experimental activity data" is never reconciled with the
   NCI-60 prior** (§1.10). This is the most consequential omission in the paper trail.
   **[FIXED — `PREREG5-RECONCILIATION.md`, §1.10 and §7.6]**
4. **The pre-committed with/without-teacher ablation is missing** (§4). I ran it: +0.1451 without the
   teacher on all drugs, +0.1118 on single agents, but −0.0186 per-split (pooled +0.0504) on novel
   scaffolds. Both halves of that belong in the package. **[FIXED — shipped, replicated on both
   generations, §7.6]**
5. **`verify-it-yourself/RECEIPTS.md` is stale.** It shows 5 numbered checks and 3 corruption tests; the
   shipped `check_claim.py`/`run_checks.sh` now run **6** checks (including the ruler-authenticity
   regression) and **5** corruption tests. My own run of the shipped script, with the pinned interpreter:

```
2. ruler authenticity: regress the shipped ruler on a replay from the object
   seed42       worst |slope-1| = 0.00000   worst |intercept| = 0.00000   test drugs with no prediction: 0   non-constant rulers: 0
   independent  worst |slope-1| = 0.00000   worst |intercept| = 0.00000   test drugs with no prediction: 0   non-constant rulers: 0
…
PASS
   -> ok: 'model predictions replaced by the ruler's in ALL splits' rejected (2 assertions fired)
   -> ok: 'model predictions replaced by the ruler's in ONE split only' rejected (1 assertions fired)
   -> ok: 'ruler cell-line effects rescaled by 3x (model predictions untouched)' rejected (1 assertions fired)
   -> ok: 'the 5 worst test drugs silently dropped from every split' rejected (2 assertions fired)
   -> ok: 'a test drug also placed in training' rejected (1 assertions fired)
PASS
```

   The receipts under-report the package's own strength, and `README_BODY.md`'s "corrupts the object five
   ways" no longer matches the receipts it points at. Regenerate them.
   **[FIXED — regenerated; they now document 7 checks and 5 corruption tests and match my own live run
   line for line, §7.7]**
6. **`teacher_structure_only.json` in the package root records `part2_run: false`** while
   `verify-it-yourself/teacher_structure_only.txt` shows part 2 ran — a stray part-1-only artefact.
   **[FIXED — the file has been removed]**
7. **Absolute hardcoded paths** in `run_confirmatory.py`, `evaluate_with_drevalpy.py`,
   `h10_build_teacher.py`, `h10_teacher_threshold.py`, `h10_leak_audit.py`, `null_test.py`,
   `diagnostics.py`, `devharness.py` and `verify-it-yourself/build_object.py`, including a `sys.path` entry
   into `attempts/` rather than the shipped model copy, so `RUN_IT_YOURSELF.md` Levels 2–4 will not run as
   printed on another machine. Level 1 does run exactly as printed.
   **[FIXED on the third pass — all 17 shipped scripts parse, no account name or machine path remains; the
   two hash-frozen files it rewrote are disclosed in `how-we-built-it/PATH-SUBSTITUTIONS.md` and I verified
   the rewrite is path literals only, §7.7]**
8. **`run_confirmatory.py`'s docstring still names `repro_seed20261023`**, the void generation, rather than
   the accepted independent one.
9. The prior's weights are not shipped and `h10_teacher_threshold.py` hardcodes `dev="cuda"` with dropout
   and no determinism flags, so a Level-3 rebuild reproduces the method, not the exact `teacher_pred.csv`.

---

## 7. Re-verifying the remediation, pass by pass

The coordinator reported fixes to three shortfalls my scope sentence named, plus two further additions. I
re-checked all of it rather than accepting the report, starting from the question that matters most: **did
anything load-bearing change?** It did not. All 43 files in `object/` verify against the shipped
`MANIFEST.sha256` (now `362e4aba…`), the prediction, ruler and truth columns are still faithful to
drevalpy's own raw outputs (max abs difference `5.00e-07`), and every headline figure reproduces unchanged:
+0.2244 row-aligned / +0.2249 merge / −0.0245 ruler on seed 42, +0.2263 / +0.2268 / −0.0185 on the
independent generation, normPearson +0.4896, normSpearman +0.4504, zero NaN predictions.

### 7.1 Leader per-pair predictions — genuinely fixed

20 files, `pred_MultiOmicsNeuralNetwork`. I checked every one against drevalpy's own written leader
predictions (seed 42 from the sequential run, independent from the per-fold runner): **10/10 splits match in
both generations**, 128,344 rows each, max |pred diff| and |truth diff| `5.00e-07`. Critically they carry
the leader's honest coverage — 12,890 rows for seed-42 split 0, not padded to the model's 23,599 — so the
~54% pair-coverage asymmetry I found in §1.7 is preserved in the shipped evidence rather than papered over.
The new **check 6** scores the leader from these files and fails unless the claim wins every split; it
reports −0.0268 (SE 0.0387) and −0.0928 (SE 0.0536), claim − leader +0.2512 and +0.3191, 10/10 both. I
re-ran the whole suite: **7 checks, PASS, all 5 corruption tests rejected.** One note: check 6 scores the
claim on its full pair set and the leader on the leader's smaller one, which is drevalpy's own convention
and matches the published report, and which I showed in §1.7 is marginally *unfavourable* to the claim
(restricted to the leader's rows the claim is +0.2228, not +0.2244). It could be strengthened to compare
both on the leader's rows; the result holds either way.

### 7.2 Generated report directory — fixed in substance

`how-we-built-it/generated-report/` holds drevalpy's own `parse_results`→`prep_results` tables and
summaries for both generations. Their values match my own independent run of that same code **to six
decimals**: PotencyTransfer +0.224884 / +0.226820, NaiveMeanEffectsPredictor −0.024736 / −0.018514, 235,974
pairs, with the same normPearson and normSpearman. The HTML tree is excluded, with the submission-kit reason
and the regeneration command stated. Residual: the leader is not in those evaluation tables (they contain
only PotencyTransfer and the ruler), so the leader's drevalpy-eval row still has to be recomputed from the
now-shipped per-pair files.

### 7.3 Robustness receipts — now inside the package, but only two of four are checkable

`similarity_bands.txt` matches my own band computation **exactly, all eight rows**, both generations.
`clean_ruler.txt` is consistent with what I and the reproduce seat measured (shipped/replayed/clean rulers
agreeing to 0.0002, replay within 6.25e-07 and 5.83e-07). `teacher050_seed42.txt` (+0.1736 at the 0.50
exclusion) and the vault rows in `diagnostics_seed42_partial.txt` are **transcribed results, not
recomputable evidence**: the first needs the prior rebuilt from the NCI-60 download, the second needs the
82-drug vault list, which is still not shipped. Disclosure improved; verifiability did not.

### 7.4 REGRESSION: the path cleanup broke two hash-frozen artefacts and four scripts

This is mine, not reported to me, and it is the one thing in this round that needs fixing before submission.

**Two of the six artefacts whose sha256 `PREREG.v4.md` §1 freezes no longer match their frozen hashes:**

```
32e8abd941994b03350ebf76b9487d57771310b1f8cc0bdf026d27f026c6ee3f  how-we-built-it/h10_build_teacher.py
   PREREG.v4 freezes:  df368571330b4db802496f99483616e6ed166d0b88ff1681d14537ae9fa546d6
4938dbcecbe589f28d2c3b67c7b509e99aed9ad905f5dccacab464b46aa46bb0  how-we-built-it/h10_teacher_threshold.py
   PREREG.v4 freezes:  312b0a8ef06cc27d76f170fc84225aadaaf7b0b0773078bad14248978f727d51
```

The other four still match exactly (`potency_core.py`, `potency_transfer_model.py`, `potency_core_fast.py`,
`teacher_pred.csv`), as do `PREREG.md` and `PREREG.v2.md` against the hashes their successors record. The
edits are path substitutions that do not change the method — but the entire point of a hash-bound
pre-registration is that a verifier can check the artefact against the frozen hash, and a verifier doing
exactly what I did now gets two unexplained mismatches. **Fix by reverting those two files and leaving the
paths documented in `PATHS.md` only, or by recording the substitution with old→new hashes and the diff so
the frozen artefact stays checkable.** A hash-bound artefact should not be edited silently for cosmetic
reasons.

**Four shipped scripts are now syntactically invalid Python**, from the same substitution emitting nested
unescaped quotes — e.g. `DATA = "os.environ.get("DATA", "./data")"`:

```
how-we-built-it/ablate_teacher.py        SYNTAX ERROR line 16
how-we-built-it/devharness.py            SYNTAX ERROR line 16
how-we-built-it/null_test.py             SYNTAX ERROR line 12
how-we-built-it/run_confirmatory.py      SYNTAX ERROR line  6
```

Everything else parses, including the whole Level-1 verifier and the frozen model files. But
`run_confirmatory.py` is the criterion's **"exact invocation"** deliverable and `ablate_teacher.py` is this
round's newly shipped first-class result, and neither can now be run at all; before the cleanup both ran,
with author-specific paths. Seven further files carry shell-style `${DATA}`/`${RESULTS}`/`${NCI60}` inside
Python string literals, which Python never expands, and `ablate_teacher.py` and `null_test.py` still point
`sys.path` and their outputs at `attempts/`. `PATHS.md` discloses the placeholder substitution honestly and
reframes these as "the record of what was run, not a turnkey pipeline", which is a fair position — but it
does not disclose the SyntaxErrors, and "run the script through a shell that expands it" does not work for a
Python file. Net: on this axis the package moved from *needs path edits* to *needs path edits and syntax
repair*. It does not touch the claim; `run_checks.sh` and `check_claim.py` are clean and I ran them.

### 7.5 The vault receipt surfaced a prose claim that does not survive it

Shipping `diagnostics_seed42_partial.txt` disclosed, for the first time anywhere in the package, the vault
standard errors: **+0.1153 (SE 0.1404)** on all 82 vault drugs and **+0.0868 (SE 0.1437)** on the 74 never
exposed. Those are not separable from zero, let alone from the 0.0435 bar (t ≈ 0.6). `DIAGNOSTICS.md` line
49 still reads "The vault bands are the honest cost of development choices: lower than the headline, still
above the bar", and no prose anywhere gives those SEs. "Still above the bar" is not a supportable statement
at that spread and should be corrected to say the vault diagnostic is too noisy to establish anything. To
the package's credit, shipping the receipt is what made this checkable; it should now be acted on. (Line 47
also still points at `../data/VAULT-INCIDENT.md`, outside the package.)

### 7.6 The two further additions

**`PREREG5-RECONCILIATION.md`** does what it says: states the contradiction, credits the panel for finding
it, gives both readings, declines to adjudicate the author's own ambiguous text in the author's favour, and
shows the claim clears every pre-registered bar under the strict reading (arithmetic re-checked in §1.10,
plus my own finding that the no-prior model also beats the leader 10/10 on seed 42). It records the finding
that cuts against the claim — the prior supplies ~35% of the headline but essentially all of the
novel-scaffold performance — in its own voice. This is the right way to handle a hole of this kind, and it
converts my sharpest reservation from an unaddressed ambiguity into a documented, two-sided disclosure.

**The ablation** is shipped, extended to both generations, and replicates my numbers to 1e-4 with a
different core implementation and a different ruler convention (§4).

### 7.7 Third pass: the two regressions are repaired, and one item moves from unverified to verified

Re-checked after the coordinator reported fixing §7.4 and §7.5. The object is untouched: 43/43 files verify
against `object/MANIFEST.sha256` (unchanged at `362e4aba…`), every file is still faithful to drevalpy's raw
output at `5.00e-07`, and the headline figures re-derive unchanged yet again. Package: 104 files, 12 MB,
largest file 0.47 MB.

**Regression B (broken scripts) — fixed.** All **17** shipped `.py` files parse under Python 3.12, **0
errors**, including the four I named; `repro_seed42.sh` and `run_checks.sh` both pass `sh -n`. No file in the
package contains the account name, and the few remaining absolute-home-path strings are anonymised
placeholders in `PREREG.v2.md`, `null_test.md` and `PATH-SUBSTITUTIONS.md`.

**Regression A (hash-frozen artefacts) — resolved by disclosure, and I verified the disclosure is accurate
rather than taking it on trust.** The two files are still modified, so the mismatch a verifier hits is real
and permanent: `h10_build_teacher.py` is now `a6b34fa5…` and `h10_teacher_threshold.py` `fe0a1178…` against
the frozen `df368571…` and `312b0a8e…`. The other four frozen artefacts — including the entire model —
match exactly, as do `PREREG.md` and `PREREG.v2.md` against the hashes their successors record.
`PATH-SUBSTITUTIONS.md` now states all of this plainly, says which two are frozen and why a verifier will
see a mismatch, and claims nothing but path strings changed. **I checked that claim mechanically.** I
reconstructed both originals from the verbatim text I had read before any cleanup, masked the path literals
on both sides, and diffed:

```
h10_teacher_threshold.py:   2a3  > import os
h10_build_teacher.py:       3a4  > import os
```

That is the whole difference. Every substantive constant survives: the ≥30-measurement panel filter,
`radius=2, fpSize=2048`, `near = maxsim >= 0.85`, `skel = {373989, 721951, 757444}`, `torch.manual_seed(0)`,
and the 2048-1024-256-1 / Dropout(0.3) / AdamW(1e-3, wd 1e-4) / 25-epoch / batch-256 schedule. So "one line
each, path literals only, no logic, constant, hyperparameter or threshold altered" is true, with the
pedantic addition of one `import os` per file that the substitution necessarily requires. One gap remains in
that document: its table promises the as-shipped hashes ("see … listing below", "likewise") and **no such
listing exists**, so it does not actually print `a6b34fa5…` and `fe0a1178…` — the one thing a verifier needs
to confirm the file in hand is the file described. It should.

**Regression C (the vault claim) — fixed, and the fix let me verify what I previously could not.** The
corrected `DIAGNOSTICS.md` puts the standard errors in the table, states that at t ≈ 0.6–0.8 the vault
estimates are not separable from zero let alone from the 0.0435 bar, says in terms that an earlier version
of the file was wrong to call them "still above the bar", keeps only the direction while noting the
baseline's −0.1345 (SE 0.0533) *is* separable, and credits the panel. The dead link is gone.

The 82-drug vault list is now shipped, which closes one of my two "not verified here" items and produces the
strongest single piece of development-hygiene evidence in the package:

```
PREREG.md section 4 pre-registered sha256: fd91cf6913afe54e641a8a0719e2856adfdf20f6749c9d2258d0cb80b0ef0cb9
how-we-built-it/vault_drugs.txt:           fd91cf6913afe54e641a8a0719e2856adfdf20f6749c9d2258d0cb80b0ef0cb9
82 ids, all of them real CTRPv2 drugs; 8 contaminated entries, all mol-mol combinations, all in the vault; 82-8 = 74

vault_all_82:            PT +0.1153 (SE 0.1404)   ruler -0.1345 (SE 0.0533)   [receipt: identical]
vault_74_never_exposed:  PT +0.0868 (SE 0.1437)   ruler -0.1493 (SE 0.0559)   [receipt: identical]
t for PT against zero: 0.82 and 0.60    against the 0.0435 bar: 0.51 and 0.30
```

The list hashes to the value frozen before any scoring, so it provably is the pre-registered vault and
cannot have been chosen after seeing results; both figures reproduce exactly from the shipped files; and my
own t-statistics confirm the retraction is the correct call. (My first attempt reproduced the bug the
incident note describes — I split the contaminated list on whitespace, and its entries are combination
*names* containing spaces.)

**Defect 5 (stale receipts) — fixed.** `verify-it-yourself/RECEIPTS.md` now matches my own live run of the
suite **line for line**, 0 differences in either direction, documenting 7 checks and 5 corruption tests.

**The two residuals the coordinator declared, which I confirm and do not hold against the claim:** the
leader is still absent from the shipped `generated-report/` evaluation tables (recomputable from the
now-shipped per-pair files), and check 6 still scores the claim on its full pair set against the leader on
its smaller one — drevalpy's own convention, and the direction that disfavours the claim (+0.2228 restricted
versus +0.2244 full, §1.7).

### 7.8 Fourth pass: a further leak-rule sanitisation, and the verifier becomes dependency-free

A submission-kit leak check then forced another round of path sanitisation, which also flagged two strings
in this verdict file; I rewrote those myself and they carried no findings. What I re-verified afterwards:

**A third recorded hash reference is now broken, and it is in the pre-registration chain itself.**
`PREREG.v2.md` is referenced by sha256 in `PREREG.v3.md`, and the shipped copy was sanitised, so that
reference fails: recorded `29260e18…`, shipped `2153aea5…`. This matters more in kind than the two scripts,
because the chain is the mechanism by which "this amendment superseded exactly that frozen text" is
checkable. I tested it the same way: reconstructing the original from the verbatim text I had read before
any sanitisation and diffing with the one path literal masked, the shipped file is **identical** — not one
date, commitment, check or number altered. `PREREG.md` is shipped unmodified and still matches the hash
`PREREG.v2.md` records for it. `PATH-SUBSTITUTIONS.md` now discloses all three breaks with both hashes in
each case, including the two as-shipped values I asked for (`a6b34fa5…`, `fe0a1178…`), and reproduces my
masked diff and constants list verbatim. The gap I flagged in §7.7 is closed. Precision on one point: the
coordinator described four sanitised documents as recorded with before/after hashes; the table carries two
of them (`PREREG.v2.md`, `null_test.md`), and `RUN_IT_YOURSELF.md` and `generated-report/README.md` are not
individually listed — neither is referenced by hash anywhere, so nothing becomes unverifiable, but the count
is two, not four.

**The verification suite is now Python standard library only, and this is a real strengthening.**
`check_claim.py` imports `csv, gzip, math, os, sys` and nothing else. I ran the whole suite under plain
`python3` on this machine — an interpreter that has **neither numpy nor pandas installed**, which I
confirmed — with no environment variables, and it reproduces every number the numpy/pandas version gave and
every number I computed independently:

```
seed42       PotencyTransfer +0.2244 (SE 0.0352, 10/10 positive, worst +0.0913)   ruler -0.0245 (SE 0.0086)
independent  PotencyTransfer +0.2263 (SE 0.0478, 10/10 positive, worst +0.0252)   ruler -0.0185 (SE 0.0068)
margins      seed42 and independent: > max+0.02 yes, > max+2SE yes
leader       seed42 -0.0268, claim - leader +0.2512, 10/10 | independent -0.0928, +0.3191, 10/10
singles      +0.2031 | +0.2023          7 checks, PASS, all 5 corruption tests rejected
```

So Level-1 verification of this claim now needs nothing but a Python 3 interpreter — no third-party
packages, no environment variables, no dataset, no network. The one discrepancy: it took **2m07s** here, not
the ~20s reported, on a Windows-mounted filesystem; the documentation should say "a couple of minutes" to be
safe. Object untouched again: 43/43 against the unchanged manifest. All 22 shipped `.py` files parse,
`run_confirmatory.py` no longer names the void run id, and no file in the package contains the account name
or the workspace path.

---

## 8. Decision

The claim is for the **full success criterion**, not a partial win. Every clause is met on a literal
reading, on evidence I regenerated myself with the benchmark's own code: the model is a drevalpy model class
run through drevalpy's own pipeline; the dataset, test mode, split count, response column and official split
generation are the package's own; the statistic is the package's own normalized R², computed by its own
evaluation code, on the complete 235,974-pair test set with no subsetting, abstention or NaN masking; the
live maximum over all eleven published models is +0.023466 on a page whose sha256 I matched byte for byte;
both margin conditions hold on both generations and on every conservative variant I could construct; both
required re-runs were made in the same environment on the same splits and are beaten on 20 of 20 splits,
and still beaten when the comparison is restricted to the leader's own covered rows; the second generation
is genuinely independent and the defect that forced its construction is real; the null test's design is the
right one and its margin is enormous; and no statistic of the held-out drugs' responses enters the model,
in code or in data.

Two things keep the verdict from being unqualified, and both are limits on *scope* rather than grounds for
failure: the second split generation needed a one-line patch to the package's splitter to be independent at
all, and the method's most-discussed component is a prior trained on an external experimental screen, which
I judge inside the criterion's allowance on the per-drug-derivation reading while the claimant's own
`PREREG.md` §5 appears to forbid it. That second point is **stronger after the second pass, not weaker**:
the reconciliation document now states both readings without adjudicating in the author's favour, and the
τ = 0 ablation — which I ran first and which the package then ran independently on both generations —
shows the claim clears every pre-registered bar under the strict reading too (+0.1450 and +0.1556 against
strict-reading bars of 0.0803 and 0.0901, and beating the leader 10/10 on seed 42). So the win does not rest
on the external data; the novel-scaffold band does. The gain is about three times weaker, and not separable
from the bar on one generation, for drugs with no close training analogue.

The three deliverable shortfalls my first scope sentence named have been fixed and I re-verified each
(§7.1–§7.3). The two regressions those fixes introduced, and the vault over-claim the fixes exposed, have
since been repaired and re-checked (§7.7): all 17 shipped scripts parse, the vault retraction is correct by
my own arithmetic, and the one permanent residue — two path-sanitised files that no longer match the sha256
`PREREG.v4.md` freezes for them — is now disclosed, with the disclosure's central claim verified
mechanically: masking the path literals, the entire difference from the originals is one `import os` line per
file, every constant and threshold intact. Shipping the vault list also closed one of my unverified items in
the claim's favour: it hashes to the value pre-registered before any scoring, and both vault figures
reproduce exactly. Throughout all three passes the object never changed — 43/43 files against an unchanged
manifest, still faithful to drevalpy's raw output, every headline figure re-derived unchanged, and the
Level-1 suite printing PASS at 7 checks with all five corruption tests rejected.

Partial wins p1 (rank metrics: I measured normalized Pearson +0.4896 and Spearman +0.4504 against the live
leaders +0.3538 and +0.3559, clearing the +0.01 margins, with normalized R² far from 0.01 worse) and p3
(ordering stability across two generations) are also satisfied, but both are **subsumed** by the full
criterion and should not be recorded separately; the recorded result is the full success criterion.

confirmed_scope: On DrEval/drevalpy 1.3.5's own CTRPv2 leave-drug-out pipeline (pinned October-2025 data, `LN_IC50_curvecurator`, 10 CV splits, all 235,974 measured pairs scored with no subsetting, abstention or NaN masking), the drevalpy model class `PotencyTransfer` attains a mean normalized R² of **+0.2249** on the package's own default seed-42 splits (SE 0.0354, 10/10 splits positive) and **+0.2268** on a second split generation verified independent of it (SE 0.0482, 0/10 shared test folds, mean best-match Jaccard 0.088) — both computed by drevalpy's own evaluation code, both exceeding by more than 0.02 absolute and more than 2 SE the live-decoded maximum over all eleven published LDO models (+0.023466, MultiOmicsNeuralNetwork; page re-fetched 2026-10-24T02:41:09Z, sha256 `b7dd9273…4364`), and both beating the author's same-environment same-splits re-runs of NaiveMeanEffectsPredictor (−0.0247, −0.0185) and MultiOmicsNeuralNetwork (−0.0275 and −0.0931, as recomputed here) on 20/20 splits, and on all 20 again when the leader comparison is restricted to the ~54% of pairs drevalpy actually scores that model on — subject to these limits, which are part of the result: it is a benchmark result on a public cell-line screen with no clinical meaning; the model predicts one potency offset per drug and contributes nothing to the ~29% of the scored variance that is drug × cell-line interaction; it adds an external potency prior trained on ~53,500 NCI-60 compounds (every CTRPv2 compound, and everything within Tanimoto 0.60 of one, excluded from that prior's training set), which no leaderboard model uses, so the comparison is not like-for-like on training data, although a τ = 0 ablation of the frozen model — run by this skeptic and independently reproduced in the package on both generations — puts the architecture at +0.1450 and +0.1556 (SE 0.0284, 0.0333) with the prior switched off entirely, still clearing both margin conditions and still beating the leader 10/10 on seed 42, so the prior supplies about 35% of the gain rather than all of it and the record falls under the strict reading of the author's own pre-registration too; the published +0.0235 is in any case a maximum over eleven models the DrEval paper's own Friedman test cannot distinguish (p = 0.742), so ratios against it carry no effect-size meaning; the second generation required patching drevalpy's `GroupKFold` call with `shuffle=True`, because in 1.3.5 the split seed provably does not change LDO test folds, so it is independent but not unmodified-package-generated; the result survives removing the 49 drug-combination "drugs" (+0.2031, +0.2023) but is roughly three times weaker for drugs with no close training analogue (max Tanimoto < 0.30: pooled +0.1615 and +0.1114, per-split mean +0.1174 and +0.0527, 7/10 and 5/10 splits positive), i.e. not separable from the bar on the independent generation's hardest band, and that novel-scaffold band is the part that does depend on the external prior, going negative without it (−0.0186 and −0.0147 per-split); the vault diagnostics on the 82 drugs held out of all development reproduce exactly from the package's now-shipped and provably pre-registered vault list but are too noisy to establish anything (+0.1153 and +0.0868 at standard errors of 0.1404 and 0.1437, t = 0.8 and 0.6), and the package's strictest-exclusion figure (+0.1736 at a Tanimoto-0.50 exclusion) is shipped as a receipt but needs the external prior rebuilt to check and was not verified here; and a leak-rule sanitisation of absolute machine paths has left three recorded sha256 references in the package no longer matching the files they name — two of the six artefacts frozen in `PREREG.v4.md`, and `PREREG.v2.md` as referenced by `PREREG.v3.md` — each disclosed with both hashes in `how-we-built-it/PATH-SUBSTITUTIONS.md` and each verified by this skeptic, by diffing against the pre-sanitisation originals with the path literals masked, to be nothing but those literals plus one `import os` line in each of the two scripts, with every constant, threshold, hyperparameter and pre-registered commitment intact, `PREREG.md` itself shipped unmodified and matching, and the other four frozen artefacts, the whole model among them, matching exactly.

pass: true
