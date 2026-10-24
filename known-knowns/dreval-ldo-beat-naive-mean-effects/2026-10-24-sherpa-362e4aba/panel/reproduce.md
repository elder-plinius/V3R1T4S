# REPRODUCE skeptic — `dreval-ldo-beat-naive-mean-effects`

context: subagent

Fresh context. I wrote my own checker from the definition before opening `verify-it-yourself/check_claim.py`,
and I did not read anything in the run directory outside `claim/`. Environment: python 3.12.15, numpy 2.4.6,
pandas 2.3.3, scikit-learn 1.9.1, drevalpy 1.3.5 installed (read-only, used to establish the definition).

---

## 1. The criterion, quoted, and what has to beat what

From `bank/targets.json`, id `dreval-ldo-beat-naive-mean-effects`, `success_criterion` (verbatim):

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

In my own words: the number that must be beaten is **0.0235**, the live-decoded maximum normalized R² over
all 11 models in the LDO normalized heatmap (MultiOmicsNeuralNetwork). The attacker's number is the mean,
over the 10 LDO CV splits, of the R² of `(truth − NaiveMeanEffects)` against `(prediction − NaiveMeanEffects)`.
It must exceed `0.0235 + 0.02 = 0.0435` **and** `0.0235 + 2·SE`. The same must hold on a second, genuinely
independent split generation, and the model may use no statistic of the held-out drugs' responses.

I confirmed the metric definition independently from the benchmark package rather than from the claim:
drevalpy 1.3.5 `visualization/utils.py::_normalize_metrics_by_mean_effects` subtracts the
NaiveMeanEffectsPredictor's `y_pred` from both `y_true` and `y_pred` after a **left merge on
(drug_name, cell_line_name, CV_split)**, then calls `evaluation.py::evaluate` per CV split, where
`"R^2"` is `sklearn.metrics.r2_score(y_true=…, y_pred=…)`. My checker implements `1 − SSres/SStot` by hand
and asserts agreement with `sklearn.metrics.r2_score` to 1e-12 on every split.

## 2. My own checker, run on `object/` only

Real output (abridged; full per-split lines were printed for all 20 splits):

```
[meta] drug_names rows=545 unique pubchem=545 unique names=545 mol-mol combos=49
[seed42] split 0: rows=23599 train_drugs=441 val_drugs=49 test_drugs=55 pred_drugs=55
         test∩train=0 test∩val=0 pred_outside_test=0 test_drugs_with_no_pred=0
   ... identical pattern for all 10 seed42 and all 10 independent splits ...

[seed42] normR2 PotencyTransfer (row-aligned): per-split=+0.1804 +0.0913 +0.2823 +0.1813 +0.4639
                                                        +0.2922 +0.2458 +0.1110 +0.1283 +0.2674
[seed42] normR2 PotencyTransfer (row-aligned): mean=+0.224402 sd=0.111158 se=0.035151 n=10
[seed42] normR2 PotencyTransfer (drevalpy left-merge): mean=+0.224884 sd=0.111931 se=0.035396
[seed42] normR2 PotencyTransfer (single agents only):  mean=+0.203123 sd=0.128541 se=0.040648
[seed42] normR2 NaiveMeanEffects (row-aligned):        mean=-0.024510 se=0.008569
[seed42] normR2 NaiveMeanEffects (drevalpy left-merge):mean=-0.024736 se=0.008639
[seed42] total shipped rows=235974  total after left-merge=245122  extra=9148
[seed42] rows with any NaN: 0
[seed42] LDO property holds for all 10 splits: True
[seed42] drugs appearing in test of exactly 1 split: 545 / 545; max appearances=1; union=545

[independent] normR2 PotencyTransfer (row-aligned):           mean=+0.226308 se=0.047807
[independent] normR2 PotencyTransfer (drevalpy left-merge):   mean=+0.226820 se=0.048150
[independent] normR2 PotencyTransfer (single agents only):    mean=+0.202317 se=0.052342
[independent] normR2 NaiveMeanEffects (row-aligned):          mean=-0.018454 se=0.006755
[independent] total shipped rows=235974  total after left-merge=245122  extra=9148
[independent] LDO property holds for all 10 splits: True

[seed42] MARGIN row-aligned:   mean=+0.224402 > 0.0435 -> True ; > 0.0235+2*SE=0.093802 -> True
[seed42] MARGIN left-merge:    mean=+0.224884 > 0.0435 -> True ; > 0.0235+2*SE=0.094291 -> True
[seed42] MARGIN single-agents: mean=+0.203123 > 0.0435 -> True ; > 0.0235+2*SE=0.104796 -> True
[independent] MARGIN row-aligned:   mean=+0.226308 > 0.0435 -> True ; > 0.119114 -> True
[independent] MARGIN left-merge:    mean=+0.226820 > 0.0435 -> True ; > 0.119800 -> True
[independent] MARGIN single-agents: mean=+0.202317 > 0.0435 -> True ; > 0.128183 -> True
```

**Every claimed figure reproduces.** Claimed +0.2244 → I get **+0.224402**; claimed SE 0.0352 → **0.035151**;
claimed +0.2249 → **+0.224884**; claimed +0.2263 → **+0.226308**. Both margin conditions hold on both
generations, and they still hold with drug combinations removed (**+0.2031** / **+0.2023**), so the gain is
not the `mol-mol` combination leak.

**Leave-drug-out property verified exhaustively, not sampled**: in all 20 splits, `test ∩ (train ∪ validation) = ∅`,
every predicted drug is in that split's test fold, every test drug has predictions, each of the 545 drugs is
in test in exactly one split, and the 10 test folds' union is all 545 drugs. No NaN predictions (NaN would be
silent abstention, since drevalpy's `evaluate` masks NaN rows).

## 3. The two reported figures (+0.2249 vs +0.2244) — explanation checked, not taken on trust

I emulated drevalpy's merge from the object alone (left-merge the rows onto themselves on
(drug_name, cell_line_name)) and got **+0.224884 → +0.2249**, and **245,122 rows from 235,974**. Counting the
duplicate groups directly: `dup-key groups per split-sum: 4118 sizes: {2: 3890, 3: 228} extra rows: 9148`.

I then checked this at the source, against the pinned CTRPv2 dataset present on this machine (outside the
package):

```
non-nan LN_IC50_curvecurator rows 235974 drugs 545 cell lines 886
duplicated (cell,drug) keys in the raw dataset: 4118   extra rows from a self-merge: 9148
raw ids not in object: 0 ; object ids not in raw: 0 ; rows carried by raw-only ids: 0
```

So the "4,118 duplicated keys / 245,122 scored rows" account in `verify-it-yourself/RECEIPTS.md` is exactly
right, **and the object covers the complete benchmark** — 235,974 of 235,974 scorable rows, all 545 drugs,
all 886 cell lines. No subsetting (pitfall [4]) anywhere. The discrepancy is disclosed honestly: both numbers
appear in `RUN_IT_YOURSELF.md` and `RECEIPTS.md`, the cause is stated correctly, and the *smaller*
row-aligned figure is the one the checker quotes.

## 4. Is the shipped "ruler" really the NaiveMeanEffectsPredictor? (my strongest test)

In LDO the test drug is unseen, so drevalpy's `NaiveMeanEffectsPredictor` (`baselines/naive_pred.py:477`)
must predict `dataset_mean + cell_line_effect + 0` = that cell line's **training-fold mean**. Two checks:

1. Within every split the ruler column is constant per cell line: `max within-cell-line spread = 0.0` in all
   20 splits (and varies by up to 8.6 across drugs, as it must).
2. The 10 test folds partition the dataset, so I reconstructed the full response matrix and solved for which
   drugs entered the ruler's training set, as a linear system (886 equations, 104 unknowns = all non-train
   drugs). Result: coefficient **≈2 for every validation drug** and **≈0 for every test drug**
   (`max|x| = 6.3e-05` over all test drugs, all 20 splits). Replaying the ruler with that training fold:

```
seed42:      WORST max|diff| over 10 splits at val-weight=2 : 6.250e-07
independent: WORST max|diff| over 10 splits at val-weight=2 : 5.833e-07
```

i.e. an exact replay to CSV rounding. The ruler is genuine, is fitted on non-test drugs only, and the roles
file truthfully describes the partition that produced it.

The weight of 2 on validation rows is drevalpy's own behaviour, not the author's: `experiment.py:220`
does `train_dataset.add_rows(validation_dataset)` on the dataset object **stored in `cv_splits`**, so the
second model run in one process sees validation rows twice. The same forensics on PotencyTransfer's own
cell-line baseline matches weight **1** (`corr with observed cell-line shift = 0.9992`), i.e. PT ran first
and had *less* training data than the ruler — never more, and never any test drug. The effect on the claim
is negligible: refitting the ruler on exactly PT's own training fold gives

```
seed42:      normR2 with baseline REFIT at val-weight=1: mean=+0.224287 (vs +0.224402)
independent: normR2 with baseline REFIT at val-weight=1: mean=+0.226149 (vs +0.226308)
```

a shift of 1.1e-4. I note it because it is undisclosed, not because it matters.

## 5. Second split generation: genuinely independent, and the stated reason is real

From the two `*_split_drug_roles.csv.gz` alone:

```
identical folds: 0
best-match Jaccard per seed42 fold: [0.0784 0.0792 0.101 0.102 0.08 0.0891 0.09 0.0686 0.0891 0.102]
mean best-match Jaccard = 0.0880 ; max over all pairs = 0.1020
```

matching the package's stated 0/10 and 0.089. I also reproduced the drevalpy defect that justifies the
patched splitter, on a synthetic dataset through drevalpy's own `split_dataset`:

```
test folds identical between random_state=42 and 20261023: True
test folds identical between random_state=42 and 7       : True
validation sets identical between 42 and 20261023        : False
```

So in drevalpy 1.3.5 the LDO **test** folds genuinely do not depend on the seed, a plain seed change would
not have produced a second generation, and `how-we-built-it/make_splits_independent.py` (GroupKFold given
`shuffle=True`) is the minimal honest fix. This is disclosed in `the-record-we-beat/README.md`. Caveat for
the criterion skeptic: the second generation is therefore **not** produced by unmodified package code.

## 6. Leakage audit

**`potency_core.py`** — clean. Everything is fitted inside whatever `fit()` is handed: cell-line means and
global mean (`self.cm`, `self.global_mean`), the per-drug mean residual targets and their weights, the
teacher standardisation (`self.zm`, `self.zs` are the mean/sd over **training** drugs only), the kernel
weights β/τ, the ridge α, the intercept `c0` and the shrinkage κ (all chosen by a drug-grouped 5-fold CV
with fixed `INNER_SEED=12345` **inside the training drugs**), and `self.coef`. A held-out drug enters only
through `drug_effect()`: its fingerprint (Tanimoto to training drugs), its pathway set (Jaccard), and its
scalar teacher value. No per-drug response statistic of a test drug is computed anywhere.

**`potency_transfer_model.py`** — clean. `train()` reads only `output.{cell_line_ids,drug_ids,response}`
(drevalpy's train fold); `predict()` receives identifiers only; `get_hyperparameter_set()` returns `[{}]`
so drevalpy's tuner cannot see the test fold. Views are identifiers only, which is why the model is scored
on all 235,974 rows with no feature-availability subsetting.

**Empirical confirmation from the object**, independent of the code:

| quantity | seed42 | independent |
|---|---:|---:|
| ORACLE per-drug offset taken from the test responses (leak ceiling) | +0.7112 | +0.7097 |
| PotencyTransfer | +0.2244 | +0.2263 |
| PT, drug-level part only | +0.2243 | +0.2263 |
| PT, within-drug part only | +0.0002 | +0.0002 |

PT sits at 32% of the leak ceiling, not at it. Per-drug offsets correlate with the truth at r = 0.598
(spearman 0.582) with sd 1.17 against the truth's 2.13 — a shrunken estimate, not a copy. And the model is
**not** calibrated to the held-out fold: per split, `mean(PT offset)` is far below `mean(true offset)`
(e.g. seed42 split 1: +0.333 vs +1.116) and `sd(PT)` is about half `sd(true)` in all 20 splits, which a
transductive leak of fold statistics would not look like. The same drug's PT offset correlates at **0.970**
across the two independent generations, so the prediction is a function of the drug, not of the fold.

**The external prior.** `teacher_pred.csv` is one scalar per drug (545 rows, index in the dataset
fingerprint file's exact column order). Against the benchmark's own per-drug response level:

```
pearson(teacher_logGI50, per-drug mean residual-from-baseline) = +0.4819  spearman +0.4940
pearson(teacher_logGI50, per-drug mean lnIC50)                 = +0.4733  spearman +0.4871
teacher range -7.57..-3.98 sd 0.577   vs per-drug mean lnIC50 sd 2.13
```

r = 0.48, not ~1: it is not a disguised copy of a CTRPv2 response. Its ordering is pharmacologically
sensible (most potent: triptolide, bortezomib, SN-38, BI-2536; least: temozolomide, dacarbazine,
thalidomide, oxaliplatin) and it makes large individual errors (AZD1480 predicted potent, inactive in
CTRPv2). I also re-ran the decisive test myself with the dataset's fingerprint table:

```
distinct fingerprints: 543 of 545; groups sharing a fingerprint: 2
  group ['54618795','54618771']: teacher values [-5.247958, -5.247958] (spread 0.00e+00)
        their CTRPv2 per-drug mean residuals [1.293, -1.025]
  group ['159324','9935249']:    teacher values [-5.272972, -5.272972] (spread 0.00e+00)
        their CTRPv2 per-drug mean residuals [0.596, 0.99]
```

Two pairs of drugs with byte-identical fingerprints get **identical** prior values to 0.0, although their
CTRPv2 responses differ by up to 2.3 ln units. The prior is `f(fingerprint)`; it cannot carry drug-specific
response information. This matches `verify-it-yourself/teacher_structure_only.txt`.

**Exclusion logic** (`h10_build_teacher.py`, `h10_leak_audit.py`, `h10_teacher_threshold.py`): CID-identity
exclusion first, then a Tanimoto exclusion. The important detail is that the *frozen* exclusion uses `ms`
from the **audit**, which recomputes CTRPv2 fingerprints from `drug_smiles.csv` with the same rdkit generator
after salt-stripping and takes the max over both those and the dataset's shipped deMorgan fingerprints — so
it does not depend on the two fingerprint conventions agreeing. InChIKey-14 connectivity matching caught 3
compounds under other identifiers (NSC 373989 / 721951 / 757444), which are removed explicitly. The logic is
correct as far as I can check it without the NCI-60 download. What I did **not** verify: that the shipped
`teacher_pred.csv` is the 0.60-threshold artefact rather than a looser one — nothing in the package pins it
to a hash of the 0.60 run, and the weights file is not shipped.

## 7. Trying to break it

- **Gain confined to a few splits?** No. 10/10 splits positive in both generations (worst +0.0913 and
  +0.0252); 10/10 still positive for single agents (worst +0.0099 / +0.0024).
- **Gain confined to combinations?** No: single agents +0.2031 / +0.2023, both clearing both margins.
- **Gain confined to near-duplicate drugs? Partly — this is my main substantive finding.** Pitfall [1]
  requires the skeptic to report each test drug's maximum Tanimoto to the training set. Using the dataset's
  own 2048-bit fingerprints and each split's own train+validation drugs:

```
seed42:      n=545 min=0.000 p25=0.262 median=0.352 p75=0.595 p90=0.729 max=1.000
             >=0.85: 12   >=0.7: 63   >=0.5: 194
independent: n=545 min=0.000 p25=0.262 median=0.350 p75=0.595 p90=0.737 max=1.000
             >=0.85: 11   >=0.7: 65   >=0.5: 199

   seed42 normR2 [all test drugs ] mean=+0.2244 se=0.0352
   seed42 normR2 [maxsim >= 0.50 ] mean=+0.3597 se=0.0367
   seed42 normR2 [maxsim <  0.50 ] mean=+0.1201 se=0.0519
   seed42 normR2 [maxsim <  0.40 ] mean=+0.0973 se=0.0537
   seed42 normR2 [maxsim <  0.30 ] mean=+0.1174 se=0.0626
   independent normR2 [maxsim >= 0.50 ] mean=+0.3137 se=0.0532
   independent normR2 [maxsim <  0.50 ] mean=+0.1565 se=0.0495
   independent normR2 [maxsim <  0.40 ] mean=+0.1270 se=0.0619
   independent normR2 [maxsim <  0.30 ] mean=+0.0527 se=0.0832
```

  The gain is about **3x larger** for test drugs that have a close analogue among the training drugs
  (36% of drugs have maxsim ≥ 0.5; 12 have ≥ 0.85, including one at 1.000). It is **not confined** to them —
  the `maxsim < 0.40` subsets are +0.0973 and +0.1270, still above `0.0235 + 0.02` in both generations — but
  on the hardest subset (`maxsim < 0.30`, 14–27 drugs per split) the independent generation falls to +0.0527
  (SE 0.0832), which is not separable from the bar. These subset SEs are large by construction and the
  criterion's margin is defined on the full benchmark, so this does not defeat the claim; it is the
  qualification that belongs in any write-up. The package discloses the related external-prior exclusion
  sensitivity (Level 3: 0.85→+0.227, 0.70→+0.172, 0.60→+0.163, 0.50→+0.123 on development data) but does
  **not** report this within-CTRPv2 train/test analogue analysis.
- **Where does the gain live?** Entirely at the drug level: PT = cell-line training mean + a per-drug
  constant, and the within-drug component of normalized R² is +0.0002. The model carries no cell-line-specific
  signal for unseen drugs. Legitimate for this metric, but it should be said plainly.
- **Non-determinism.** Two consecutive runs of `verify-it-yourself/check_claim.py` are byte-identical; the
  statistic is a deterministic function of the shipped files, which I hashed (sha256 of all 23 object files
  recorded in my scratchpad). The kernel model is deterministic given the data (fixed `INNER_SEED`, exact
  linear solves). The neural prior is **not** bit-reproducible: `h10_teacher_threshold.py` hardcodes
  `dev="cuda"`, uses dropout and does not set `torch.use_deterministic_algorithms`, so a Level-3 rebuild will
  give a slightly different prior, and the `.pt` weights are not shipped (only their sha256). Level 1 and
  Level 2 are fully reproducible from the shipped `teacher_pred.csv`; Level 3 reproduces the method, not the
  exact file.
- **`RUN_IT_YOURSELF.md` as printed.** Level 1 ran exactly as printed (with `PYTHON=` as the file says) and
  its output matches `RECEIPTS.md` line for line. Levels 2–4 need the 1.5 GB dataset / NCI-60 download /
  a GPU and were out of scope for this budget; I did not run them. Two files referenced by `RECEIPTS.md`
  (`verify-it-yourself/teacher_is_structure_only.py` and `.txt`) were absent from the package when I first
  listed it and present later in the same session — the package was being edited while I verified it.

## 8. The author's checker, and a corruption it misses

`sh verify-it-yourself/run_checks.sh` (with `PYTHON=`) prints `PASS`, and **every number in it matches my
independent recomputation to all printed digits** (+0.2244/0.0352, −0.0245/0.0086, +0.2263/0.0478,
−0.0185/0.0068, +0.2031, +0.2023). Its corruption harness is real: it copies `object/` into a temp
directory, mutates it, and requires the checker's stdout to contain a line starting with `FAIL (` — a crash
is explicitly counted as a failure of the test, not a pass. The three shipped corruptions all fire.

But the checker is weaker than it looks, and I found two corruption classes it accepts:

```
### ruler cell-line effects x 1.3 ###  (truth and model predictions untouched)
   seed42 PotencyTransfer +0.2334 ... NaiveMeanEffects -0.0243   -> PASS
### ruler cell-line effects x 3.0 ###
   seed42 PotencyTransfer +0.4088 ... NaiveMeanEffects -0.0188   -> PASS
### silently dropped the 5 worst test drugs per split ###
   seed42 PotencyTransfer +0.2961 ... NaiveMeanEffects -0.0421   -> PASS
```

Causes: (a) normalized R² is `1 − SS(y−PT)/SS_centred(y−ruler)`, so inflating the ruler's cell-line effects
inflates the statistic without touching the model, and the ruler's own normalized R² *moves toward* the
published −0.0169, sailing through check 3's `-0.06 < bm < 0` window — the checker reports +0.4088 and still
says PASS; (b) `leakage()` tests `pred − test` but never `test − pred`, so dropping hard test drugs
(pitfall [4], abstention) is invisible to it. My own tests reject all three:

```
shipped object              rows=235974  test drugs with no prediction=  0  max|ruler - cell-line training mean|=6.250e-07  -> OK
corruption A (ruler x1.3)   rows=235974  test drugs with no prediction=  0  max|ruler - cell-line training mean|=1.994e+00  -> REJECTED
corruption A (ruler x3.0)   rows=235974  test drugs with no prediction=  0  max|ruler - cell-line training mean|=1.329e+01  -> REJECTED
corruption B (drop 5 worst) rows=215032  test drugs with no prediction= 50  max|ruler - cell-line training mean|=4.065e+00  -> REJECTED
```

This is a weakness of the verification script, not evidence against the claim: the shipped object passes the
stronger tests exactly. Recommendation: add the ruler-authenticity replay and a `test − pred` assertion to
`check_claim.py`.

## 9. Criterion gap I could not close

The criterion requires "the attacker's own same-environment same-splits re-run of **BOTH** the
NaiveMeanEffectsPredictor **and** the published LDO leader (MultiOmicsNeuralNetwork) included, and the
attacker's value beating both." The ruler's re-run is shipped and I verified it exactly. **The
MultiOmicsNeuralNetwork re-run is not in `claim/`** — no predictions in `object/`, and no local normalized
R² for it anywhere in the package. It is only named in `how-we-built-it/PREREG*.md` and as a `--models`
argument in `how-we-built-it/repro_seed42.sh`. I was instructed not to read `attempts/`, so I can only say it
is absent from the claim package, not that it was never run. The published 0.0235 is beaten by 0.20, so the
substantive comparison is not in doubt; the deliverable is. This one is for the criterion skeptic.

## 9b. The package was edited during my verification — re-checked

`the-record-we-beat/README.md` changed on disk while I worked (and two files appeared in
`verify-it-yourself/`). I re-read it. **The bar did not move**: still
`| **MultiOmicsNeuralNetwork** | **+0.0235**  <- the maximum over all models |`, so every margin result
above stands. The added sections are self-critical, not self-serving: that the heatmap page names neither
its dataset nor its setting (identified from URL plus context); that the published LDO differences are not
statistically significant (Friedman p = 0.742 over all 11 models), so 0.0235 is a maximum over
indistinguishable near-zero values and ratios against it are not meaningful; that the comparison is not
like-for-like because this method adds ~53,500 external compounds no leaderboard model uses; and that the
NCI-60-expansion idea is prior work (arXiv:2608.11444). None of this changes what I recomputed; all of it is
the right framing for the numbers I confirmed, and I note it because candour added mid-verification is still
candour. The moving package is itself worth flagging to the panel: my checks are against the object hashes
recorded in my scratchpad, and `object/` did not change.

## 10. Verdict

What I verified: the claimed values (+0.2244 row-aligned / +0.2249 drevalpy-merge, SE 0.0352, +0.2263 on the
second generation) reproduce exactly with my own checker written from the definition; both margin conditions
hold on both generations and on single agents alone; the leave-drug-out property holds in all 20 splits
exhaustively; the object covers the complete benchmark (235,974 of 235,974 rows); the ruler is provably the
real NaiveMeanEffectsPredictor fitted on non-test drugs only (exact replay, 6e-7); the two reported figures
differ for exactly the stated reason, confirmed against the raw dataset; the second split generation is
genuinely independent and the defect motivating it is real; the external prior is a deterministic function of
chemical structure and correlates with the benchmark's per-drug response at only r = 0.48; no test-drug
response statistic enters the model in code or in the data.

What I did not verify: Levels 2–4 end to end (drevalpy's own report run, the NCI-60 rebuild, the permutation
null); that `teacher_pred.csv` is specifically the 0.60-threshold artefact; and the MultiOmicsNeuralNetwork
same-splits re-run, which is not in the package.

Qualifications that must travel with the claim: the gain is ~3x larger for test drugs with a close training
analogue (+0.36 vs +0.10 at maxsim<0.40) and on the hardest subset of the independent generation it is
+0.053 ± 0.083; all of the gain is a per-drug offset, with no cell-line-specific signal for unseen drugs; the
Level-3 prior rebuild is not bit-deterministic.

No mismatch, no missing object in `object/`, no non-determinism in the shipped result.

pass: true
