# CRITERION skeptic: run 2026-11-10-1136, target cryptic-tb-resistance-beat-who-catalogue, claimed partial win p2

context: subagent (Agent tool, subagent_type criterion)

Read: claim/ only (CLAIM.md, PREREG.md, PREREG.v2.md, PREREG.v3.md, null_test.md, REPRODUCE.md, EXTERNAL_INPUTS.md,
output/, result/, split/, code/, baseline/) and the bank entry (partial_wins, success_criterion, pitfalls) in
repo/bank/targets.json. Nothing else in the run folder. Own scratch code and log: work/panel_criterion/crit_check.py,
crit_check_output.txt, crit_check.csv (written by this skeptic; peak working set 262 MB, 4 threads, distance matrix read
in row blocks through short-lived memory maps). Nothing here is clinical advice.

## Bank text judged (p2, verbatim)

"A reproducible leakage demonstration: show that a random (non-cluster-aware) split inflates held-out performance for
the same model and drug by a quantified margin versus the cluster-aware split, with the split files and code released -
the standard trap in this dataset, reported as a methodology result."

## Inputs verified by this skeptic

- sha256 split/split.csv 3b4ed122...0a56, reuse table f785ae87...1c1b (12,287 rows), labels 611512d7...e61, distance
  matrix 02d7cd46...def5dd (int16 15,228 x 15,228): all equal to the values in PREREG.md / CLAIM.md / EXTERNAL_INPUTS.md.
- ETH HIGH-quality R/S isolates: 8,251 (1,189 R), as in the author's log.

## Clause-by-clause reading

1. "a random (non-cluster-aware) split": MET. 400 isolate-level splits, numpy default_rng(seed).choice(12287, 3073,
   replace=False), seeds 1..400, no grouping. result/random_control_splits_test_rows.npz equals the regenerated index
   sets for all 400 seeds (checked). My own kNN/metric code reproduces seeds 1, 2, 3 exactly (0.6026, 0.6331, 0.5980).

2. "the cluster-aware split", by the bank's own words (success_criterion: "isolates grouped by genomic cluster so no
   cluster spans train and test"; pitfall: "the skeptic must recompute the clusters"): MET, with one caveat.
   I recomputed 12-SNP single-linkage components over all 12,287 reuse isolates from the released distance matrix with
   independent code: 7,420 components, 6,399 singletons, largest 2,539; the partition is identical to split.csv CLUSTER;
   0 components span TRAIN and TEST; minimum TRAIN-TEST distance 13 SNPs in both directions (TEST rows and TRAIN rows);
   0 negative entries; the stated rule (giant component > 614 to TRAIN, salted sha256 order, stop at >= 3,072) re-derives
   exactly the split.csv TEST set (3,073). Caveat: clusters were recomputed from CRyPTIC's released GPI SNP-distance
   matrix, not from the joint-genotyped VCFs that the bank's verification_method names; and 12-SNP clusters are
   transmission-scale, not lineage-scale (671 TEST isolates still have a TRAIN isolate within 20 SNPs). Residual
   relatedness can only shrink the measured gap, so this does not weaken the p2 direction.

3. "inflates held-out performance": MET. Real (split v2) sensitivity at 95% test specificity 0.3496 (TP 93, FN 173,
   FP 91, TN 1739 on 2,096 TEST isolates, 266 R; reproduced exactly by my code; the released per-isolate prediction
   file gives the same table and every row is a split-v2 TEST isolate with nearest TRAIN distance >= 13). All 400 random
   splits are strictly higher (min 0.5135, mean 0.6003, max 0.6678); AP 0.4170 vs random mean 0.6699.

4. "for the same model and drug": MET. ETH in every arm; the model is a fixed distance-weighted 10-NN (w = 1/(1+d),
   ties by matrix index) with no fitted or tuned parameter, the same code path and the same HIGH R/S filter in the real,
   random and alternative arms (checked in code/p2_knn.py). Only the training pool changes, which is inherent to any
   split comparison. Not a stretch of "same model".

5. "by a quantified margin": MET. mean(random) - real = 0.2507; min(random) - real = 0.1639. Against the 100 alternative
   cluster-aware splits by the same rule (0.1799-0.4662, mean 0.3259; all below the lowest random split), the frozen
   split sits mid-distribution (67 of 100 alternatives are lower), so the frozen split is not a cherry-picked low; the
   distribution-level gap is 0.6003 - 0.3259 = 0.2744, the worst-case edge gap 0.5135 - 0.4662 = 0.0473.

6. "with the split files and code released": MET within the claim package (split/split.csv with sha256, the 400 random
   splits as an index file verified against their seeds, the per-isolate prediction file, and all four scripts; the
   alternative splits are defined by salts in code/p2_knn.py rather than shipped as files; the 463 MB distance matrix is
   a public CRyPTIC file pinned by sha256). "Released" becomes literal only when the package is published.

7. "reproducible": MET for the numbers I re-computed (real value, three random seeds, released index file, prediction
   file); the full 400/100 rerun is the REPRODUCE skeptic's task.

8. "reported as a methodology result": MET. No clinical or treatment interpretation is attached.

## Null / control rule frozen before measurement

PREREG.md (frozen_at 11:44:57Z, before any p2 number per the file) fixes model (k = 10, w = 1/(1+d), HIGH R/S pool,
ties by matrix index), metric (smallest t with <= 5% of test negatives scoring >= t; sensitivity = positives >= t),
drug (ETH), 400 random seeds 1..400 of the same TEST size, the pass rule ("every one of the 400 random-split metrics
strictly greater than the split-v2 metric"), the margin definition, and the 100 alternative salts as secondary. The code
run matches each item (I read the code and re-implemented the metric independently; same results). PREREG.v2 (11:51:22Z)
does not touch p2; PREREG.v3 (11:53:07Z) only reduces control counts for the secondary drugs and records the ETH p2
result as already seen, which is consistent with the run happening after the freeze. The smoke run and the one-line
memory change do not alter values (smoke real 0.3496 = full run). Timing is attested by the documents only; file
times inside claim/ are copy times.

## Hidden quantifiers and stretches found

- Composition component in the margin (not disclosed in CLAIM.md). The cluster-aware rule always keeps the 2,539-isolate
  giant component in TRAIN, while random splits test about a quarter of it. My checks (20 seeds): random-split sensitivity
  with giant-component isolates excluded from scoring is 0.4495-0.5700 (mean 0.5041) versus mean 0.6056 overall for the
  same seeds, so roughly 0.10 of the 0.25 mean margin comes from random splits also scoring the giant cluster. The
  leakage effect survives without it: on the identical 2,096 split-v2 TEST isolates, scoring with random 4-fold training
  pools (similar pool size, about 6,190 vs 6,155) gives 0.5451-0.5714 (mean 0.5617, 5 seeds) versus 0.3496, an
  inflation of about 0.21 on the same isolates; and all 20 giant-excluded random values still exceed 0.3496. Mechanism check: random-split
  sensitivity on 12-SNP singletons only (0.1682-0.3727) is not above the cluster-aware singletons (0.3429), so the
  inflation is carried by isolates with close relatives, as leakage predicts. The claim's 0.2507 is therefore the
  protocol-level difference "random vs cluster-aware split", which is what p2 literally asks; it must not be read as
  pure near-relative leakage on identical isolates (that figure is about 0.21 by my check).
- Existential "the same model": p2 needs one model. The relatedness-only 10-NN was chosen in this run after run 1's p2
  with a resistance-gene L1 model on its Mykrobe split found no leakage (disclosed in CLAIM.md and PREREG.md). A
  relatedness-only model is the one most exposed to the trap, so the direction is close to expected by construction; the
  quantified size is the empirical content. The result does not show that random splits inflate every model on CRyPTIC
  (run 1 is a counter-example for a gene-based model), and the scope below is restricted to this model.
- "held-out performance" is sensitivity at 95% specificity with the threshold set on each test set's own negatives
  (same rule in every arm): a ranking-type metric, not a pre-fixed operating point. Acceptable for a like-for-like
  comparison; AP agrees.
- "same TEST size" means 3,073 of 12,287 isolates; the phenotyped ETH test counts differ slightly (random 2,007-2,136,
  split v2 2,096; R 261-348 vs 266).
- 918 of the 3,073 TEST isolates were seen in run 1; the p2 model has no fitted parameters and the split was built
  from distances only, so I see no route for that to bias this comparison, but p2 is not reported on the 2,155
  never-held-out subset.
- Secondary drugs (PREREG.v3) are said to be reported but are not in this package; they are not claimed and not judged.
- The 10-NN is a weak predictor (0.3496 at 95% specificity on split-v2 TEST; the baseline record shows the WHO-2023.5
  catalogue at sensitivity 0.7970 / specificity 0.9628 on the same 2,096 ETH isolates). p2 is a methodology result
  only; nothing about predictive merit follows.

## Pitfalls

- Population structure: the subject of the claim; clusters recomputed (above).
- Phenotype filter: HIGH-quality R/S, fixed in PREREG.md (run 1's rule), applied identically in every arm before any
  split is applied. Not chosen after results.
- Class imbalance: ETH R prevalence 14.4%; metric is sensitivity at matched specificity with AP and the real confusion
  matrix, not accuracy or AUROC.
- Catalogue circularity: not relevant to p2 (no catalogue in the comparison).
- Clinical scope: none attached.

## Baseline record

baseline/ is the step-3c record for the main criterion (engine check 13/13 PASS against released v1.2 predictions;
WHO-2023.5 confusion matrices on split-v2 TEST). Its ETH TEST population (2,096 isolates, 266 R, HIGH R/S) is the same
data and split as the claim's real arm, but its metric (the catalogue's fixed operating point) differs, and it is not
used by p2. For p2 the comparator is internal: the random-split controls use the same data, phenotype filter, model and
metric, with only the split changed, which is the contrast p2 requires. No external p2 baseline exists or is needed.

## Main success criterion

Not met by this claim: it is not claimed, the package contains no main-criterion model or per-isolate comparison against
the catalogue, and PREREG.v2 records an INH result made conditional on a robustness check whose outcome is not in this
package. I cannot confirm the main criterion.

## Verdict

p2 is met literally, clause by clause, for ETH with this fixed 10-NN model; not subsumed by run 1 (whose p2 attempt
found no leakage and claimed nothing) and not a restatement of the main criterion. Literature novelty of a quantified
CRyPTIC leakage figure is the NOVELTY skeptic's question, not judged here.

confirmed_scope: On the 12,287-row CRyPTIC_reuse_table_20240917.csv, for ethionamide with HIGH-quality R/S phenotypes, a fixed untuned distance-weighted 10-nearest-neighbour model on CRyPTIC's released GPI SNP-distance matrix has sensitivity at 95% test specificity of 0.3496 on the pre-registered 12-SNP single-linkage cluster-aware split v2 (no cluster spans TRAIN and TEST, minimum TRAIN-TEST distance 13 SNPs) versus 0.5135 to 0.6678 (mean 0.6003) on all 400 pre-registered random isolate-level splits of the same 3,073-isolate TEST size, a random-split inflation of 0.2507 on average (at least 0.1639) for this model and drug only, part of which comes from random splits also scoring the 2,539-isolate giant cluster that the cluster-aware rule keeps in TRAIN, reported as a methodology result with no clinical meaning.

pass: true
