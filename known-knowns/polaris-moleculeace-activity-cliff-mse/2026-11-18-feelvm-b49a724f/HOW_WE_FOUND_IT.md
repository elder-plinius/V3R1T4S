# HOW WE FOUND IT — contributor text, unverified

The target (bank id `polaris-moleculeace-activity-cliff-mse`) is a field of 30 Polaris
leaderboards over the MoleculeACE activity-cliff benchmark: one single-task pKi/pEC50
regression per ChEMBL target, with a frozen cliff-stratified split, metric
mean_squared_error. Nearly every leaderboard cell held a single auto-generated entry.

**Scouting first.** A live survey of all 30 leaderboard pages (one honest GET each) showed 28
single-entry cells. Comparing each cell's listed MSE against the benchmark paper's own
corrected per-target results (the repo ships them as a CSV) produced a headroom table: on 27 of
30 targets the auto-generated entry already beat the paper's best single model, but on
CHEMBL2835 (JAK1) the listed best (0.16617) was 9.6% WORSE than the paper's own RF/ECFP
(0.15024) — so the first attack went there. Along the way the scout proved the official test
set is byte-identical to the public CSV's split=='test' rows (the Polaris API exposes the
explicit index lists; they match exactly), and caught two traps: the label column convention
('y', an exact +9 shift of the pKi column), and the fact that cliff_mol flags are
label-derived and must never be used as input features.

**The JAK1 attack failed, honestly.** The paper's baseline was reproduced first (RF/ECFP
0.3927 vs expected 0.3876; SVM/ECFP exactly 0.41980). A kitchen-sink sweep (54
descriptor×model members, out-of-fold on train only) reached OOF 0.1505 with hill-climbed
weights; the single declared test read landed at 0.1728 — worse than the listed best. A
preregistered power analysis explained why before any more reads were burned: with 126 test
molecules, the criterion's ≥95% bootstrap bar demands test MSE ≈ 0.12, a ~20% improvement
over anything published on that split; the member pool's true ceiling was ~0.16. The two
unused candidate reads were cancelled rather than spent. Negative result, recorded.

**The pivot.** The bank's partial win p2 asks for something different: beat the repo's own best
model for a target ON THE CLIFF MOLECULES ONLY, with at least 40 cliff test molecules, while
not being worse on the rest. Scoping across all 30 targets picked CHEMBL244 (coagulation factor
X): 296 cliff test molecules, and its best model (SVM/ECFP) was reproduced to within 0.0002
RMSE of the paper's value — the bar was exact and undeniable. A fresh prereg (PREREG.v2)
froze the protocol before any CHEMBL244 test read.

**What worked.** A 44-member out-of-fold sweep on the 2476 train rows, selected by a greedy
pass that minimized OOF CLIFF-subset MSE subject to not losing non-cliff OOF (the combiner
frozen to non-negative ridge — the JAK1 failure had taught us that hill-climbed weights
overfit small-sample OOF). The winner was a 6-member SVR ensemble whose biggest single
contributor (weight 0.47) was an SVR on hashed COUNT Morgan fingerprints (radius 3):
substructure multiplicity, not just presence, is what separated cliff compounds here. The
single declared test read: cliff-subset MSE 0.550194 vs the baseline's 0.634574 (−13.3%),
non-cliff better by 16.5%. A 400-control label-shuffle null test (the recipe retrained on
shuffled train labels 400 times) put every control at train-mean level (3.02–4.05) against the
real 0.4368. A from-scratch verifier re-derived every number from the CSV alone; the
self-break attempt survived.

**Also checked and not claimed.** The same frozen predictions evaluated against the
leaderboard cell: overall MSE 0.4368 vs the listed 0.4750 (−8.05%) — but the p1 criterion's
bootstrap bar (≥95% of resamples below the listed best) came out at 87.4%, so p1 is NOT
claimed for this cell either. The claim is exactly p2, one target, one bar, nothing wider.
