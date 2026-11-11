# CRITERION skeptic, run 2026-11-10-1136, claim p2 (ETH leakage, 10-NN on SNP distances)

context: subagent (Agent tool, subagent_type criterion, round 2)

Read: claim/CLAIM.md, REPAIR.md, PREREG.md, PREREG.v2.md, PREREG.v3.md, null_test.md, output/, result/, split/, code/,
baseline/, and the bank entry cryptic-tb-resistance-beat-who-catalogue (partial_wins, success_criterion, pitfalls) in
repo/bank/targets.json. Nothing else of the run folder was opened. Own checks: work/panel2_criterion/crit_check.py
(independent code; distance matrix read by memory map in reopened row blocks, ETH rows only kept, 4 threads, 30 s),
log work/panel2_criterion/crit_check_output.txt. Nothing here is clinical advice; these are prediction metrics on public
isolates and no clinical interpretation is attached.

## p2, read literally, clause by clause

Bank text: "A reproducible leakage demonstration: show that a random (non-cluster-aware) split inflates held-out
performance for the same model and drug by a quantified margin versus the cluster-aware split, with the split files and
code released - the standard trap in this dataset, reported as a methodology result."

1. "random (non-cluster-aware) split": MET. 400 isolate-level random splits, TEST size 3,073 of 12,287 (same as split v2),
   numpy default_rng seeds 1..400. I regenerated all 400 TEST row sets from their seeds; 400 of 400 equal the released
   result/random_control_splits_test_rows.npz. Nothing in them looks at clusters.
2. "the cluster-aware split": MET in the bank's words ("isolates grouped by genomic cluster so no cluster spans train
   and test"). I recomputed the clusters from the released SNP distances with my own code (edges at <= 12 SNPs among the
   12,287 reuse isolates, scipy connected components): 7,420 components, 6,399 singletons, largest 2,539, the same
   partition as split/split.csv CLUSTER (7,420 distinct pairs = 7,420 clusters, one to one), 0 negative entries,
   0 of my components span TRAIN/TEST, 0 edges at <= 12 SNPs cross the split. The split is cluster-aware, not
   lineage-stratified (lineages 1-4 occur on both sides); p2 asks for cluster-aware, so this is no stretch. Residual
   relatedness at 13-20 SNPs (671 TEST isolates) can only raise the cluster-aware value, i.e. shrink the margin.
3. "the same model": MET, not stretched. One fixed algorithm with no fitted or tuned parameters: k = 10 nearest
   training isolates with a HIGH-quality R/S ETH phenotype, weights 1/(1+d), ties by matrix order; the only thing that
   changes between arms is which isolates are TRAIN, which is what a split comparison means. Caveat for scope: a
   genome-distance kNN is the model most exposed to near-duplicate leakage, and it was chosen after run 1's gene-based
   L1 model showed no leakage (0.8348 frozen vs 0.8032 random mean). The p2 wording is existential in the model, so
   this is allowed, but the result says nothing about gene-based or catalogue-based models.
4. "and drug": MET. ETH only, fixed in PREREG.md; same phenotype column and HIGH R/S filter in every arm.
5. "inflates held-out performance ... by a quantified margin": MET. Metric: sensitivity at >= 95% specificity on the
   TEST part (threshold from TEST negatives, integer form of the frozen <= 5% rule). My own re-implementation
   (threshold just above the (floor(n_neg/20)+1)-th highest negative score; different code path from the author's)
   gives 0.3496 on split v2 and 0.6026 / 0.6331 / 0.5980 / 0.6218 / 0.6154 on seeds 1-5, matching output/p2_knn_ETH.csv.
   Random: 0.5135-0.6678, mean 0.6003; all 400 strictly above 0.3496; margin mean 0.2507, min 0.1639.
6. "with the split files and code released": MET for the package: split/split.csv (sha256 3b4ed122...0a56, re-hashed),
   the 400 control splits (npz), per-isolate split-v2 TEST predictions (2,096 rows), code for split, audit, test and
   export. The 463 MB distance matrix is referenced by public URL and sha256 rather than copied (EXTERNAL_INPUTS.md);
   acceptable, it is a public CRyPTIC release file. "Released" becomes true only when the package is filed.
7. "reproducible": the headline value and the controls reproduce from my independent code (above).
8. "reported as a methodology result": the claim sentence is a methodology statement; no clinical reading attached.

## Control rule frozen before measurement

PREREG.md (frozen_at 11:44:57Z) fixes model (k, weights, filter, tie rule), metric (<= 5% of negatives at or above t),
drug ETH, real split v2, 400 random splits seeds 1..400 of the same TEST size, the pass rule (every control strictly
greater), the margin definition, and 100 alternative cluster-aware splits by salt. code/p2_knn.py implements exactly
these; the only unfixed detail is the generator call (default_rng(s).choice), which cannot matter with a 0.16 minimum gap.
PREREG.v3 (written after the ETH result was seen) only reduces the control count for the 12 secondary drugs, which are
not claimed. The freeze order rests on the package's own timestamps; nothing in the package contradicts it. Split v2 was
made from distances only, before any phenotype was read; the 918 run-1-TEST isolates in it do not bear on p2 (the kNN
has no parameters fitted on anything).

## Repair round 1

Does not change anything material. Diff of output/p2_knn_ETH.csv against output/round1_superseded_p2_knn_ETH.csv: 1 row
differs (random seed 333, 0.584375 -> 0.5875); real value, min, mean, max, margin and pass rule unchanged.

## Is the margin meaningful against the alternatives and against TEST make-up

- Alternative cluster-aware splits (100 salts): 0.1799-0.4662, mean 0.3259; 33 of 100 are >= 0.3496, so split v2 is
  mid-range, not a favourable salt; all 100 are below the lowest random split (0.5135).
- TEST make-up differs between the arms: the rule keeps the 2,539-isolate component in TRAIN; it holds 1,592 of the
  8,251 ETH-phenotyped isolates with R fraction 0.220 (rest 0.126); split-v2 TEST is 67.0% singletons (all ETH 54.1%);
  R fraction 0.127 (split v2) vs 0.144 (random mean). Two post hoc composition controls (mine, not pre-registered):
  (A) 50 random isolate-level splits with that component forced into TRAIN (TEST drawn from the other 9,748):
      0.4491-0.5658, mean 0.5025; all 50 still above 0.3496 (gap mean 0.153, min 0.100).
  (B) Same 2,096 split-v2 TEST isolates, scored by random isolate-level 4-fold out-of-fold kNN (10 repeats):
      0.5263-0.5714, mean 0.5556 (gap mean 0.206, min 0.177).
  So the inflation is leakage, not only composition: on identical TEST isolates it is about 0.21. About 0.10 of the
  headline 0.2507 mean gap goes with the big component sitting in random TESTs (leakage inside that component mixed with
  its higher R share). The headline figure is the literal random-vs-cluster-aware gap that p2 asks for, so it stands as
  stated, but the panel-controlled gap (0.15-0.21) is the fairer size of the leakage. Note also that under (A) the
  random range (min 0.4491) overlaps the top of the alternative cluster-aware range (max 0.4662); only the frozen v2
  comparison is claimed, and it separates under every control.

## Pitfalls

- Population structure: this is the subject of the claim; clusters recomputed (above). Not undermining.
- Phenotype filter: HIGH-quality R/S ETH, fixed in PREREG.md before p2, identical in every arm. Not undermining.
- Class imbalance: ETH R is 14.4% overall; the headline metric is sensitivity at matched (>= 95%) specificity, as the
  pitfall asks; spec at threshold is 0.950 in every arm. Average precision is prevalence-dependent and the R share differs
  (0.127 vs 0.144), so AP should not be cited as the margin; the claim does not.
- Catalogue circularity and clinical scope: no catalogue in this comparison; no clinical reading. Not applicable.

## Hidden quantifiers and stretches

- "the same model": one specific distance-based kNN; the result must not be read as "random splits inflate TB
  resistance prediction models" in general (run 1's gene-based model showed none).
- "inflates by 0.2507": mean over 400 random splits, not a guaranteed per-split gap (min 0.1639), and about 0.10 of it
  tracks the giant component's placement.
- One drug only. PREREG.md also pre-registered the same test on the other 12 drugs as secondaries; the claim package
  does not report them. They cannot be used for the claim, but they should be reported alongside it.

## Baseline record

baseline/ uses the same pinned table (sha256 f785ae87...1b, re-hashed), the same split v2 and the same HIGH R/S filter:
its ETH TEST table (WHO-2023.5 212/54/68/1762) has 2,096 isolates and 266 R, exactly the p2 real-arm TEST. Its metric
(the catalogue's own sensitivity/specificity) is not the p2 metric; it concerns the main criterion. p2's comparison is
internal (same model and metric in both arms), so no external baseline is needed and none is misused.

## Main success criterion

Not met and not claimed: this claim makes no model-versus-WHO-catalogue comparison (the kNN's 0.3496 at 95% specificity
is far below the catalogue's 0.7970 sensitivity on the same TEST isolates, at a different specificity).

## Verdict

p2 is met literally: random isolate-level splits vs a recomputed, genuinely cluster-aware split, same fixed model and
drug, quantified margin, all 400 controls above, split files and code in the package, rule frozen before measurement,
repair immaterial; the inflation survives composition controls. Not subsumed by run 1 (which found no leakage, with a
different model and split).

confirmed_scope: On the pinned 12,287-row CRyPTIC reuse table, for ethionamide (HIGH-quality R/S phenotypes) and one fixed genome-wide 10-nearest-neighbour model on the released CRyPTIC SNP distances, sensitivity at >= 95% specificity is 0.3496 on the frozen 12-SNP single-linkage cluster-aware split v2 versus 0.5135-0.6678 (mean 0.6003) on all 400 pre-registered random isolate-level splits of the same TEST size, a random-split inflation of 0.2507 on average (at least 0.1639), of which 0.15 to 0.21 remains in the panel's post hoc composition controls; this is shown for this distance-based model and this drug only.

pass: true
