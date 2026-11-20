# CRITERION skeptic - flip-gb1-plmfit-scoreboard-spearman, run 2026-11-20-0535

context: subagent

Read: `README.md`, `CLAIM.md`, `REPRODUCE.md`, `UNSCORED-PREDICTION-as-sealed.md`, `result/scores.out`,
`result/score_selftest.out`, `result/leak_test.out`, `status/plmfit_README_2026-11-20-0535_preclaim.md`,
`code/fit_sealed.py`, `code/boot_mean.py`, `code/gb1k.py`, `the-earlier-runs/related_work.md`,
`the-earlier-runs/extrap_select.out`, `the-earlier-runs/noise_floor.out`,
`the-earlier-runs/p2_all_scores.out`, `the-earlier-runs/criterion_compare-this-run.out`.
I also recomputed the claim's gating numbers myself with `scipy.stats.spearmanr` from `data/gb1_data_full.csv`
and the six frozen prediction files, and ran a permutation null the bundle does not contain.

## My own recomputation (independent of the bundle's scorer)

- `data/gb1_data_full.csv`: 8,733 rows, `three_vs_rest` = 2,691 train / 299 validation / 5,743 test; the 5,743
  test rows carry 5,743 distinct `aa_seq` (so no row can be double-counted through the join key) and 4,683
  distinct `score` values.
- `result/pred_configA_all_seed{1,2,3}.csv`: 5,743 rows each, every test `aa_seq` present exactly once, no
  extras, no missing. Spearman against the `score` column: 0.902852, 0.902852, 0.902852.
- Three-seed mean 0.902852, sd(ddof=0) 0.000000; the three prediction arrays are element-identical.
- My own bootstrap of the mean (2,000 resamples of the 5,743 test sequences, `default_rng(777)`):
  [0.898234, 0.907383], against the bundle's [0.898044, 0.907247]. Both lie entirely above 0.8791.
- `result/pred_configB_trainonly_seed1.csv`: 0.897451, reproduced.
- Permutation null (predictions shuffled against targets, 200 draws): mean rho 0.00179, sd 0.01355, largest
  |rho| 0.03978. The measured 0.902852 is nowhere near what this metric returns by chance on this test set.
- The scoreboard value: line 209 of the saved status page reads
  `| GB1 - three-vs-rest | 0.8791 | Spearman's | ProGen2-M | Adapters | 50% | CLS | Linear |`, so the bar is
  0.8791 as used.

## 1. p2 read literally - which reading of "a bootstrap 95% interval" I apply

p2: "A three-seed mean strictly above the `three_vs_rest` scoreboard value of 0.8791, with a bootstrap 95%
interval that excludes it, from a reproducible pipeline whose split file and seeds are named."

I apply the interval **of the mean**. Grammatically the subject of p2's sentence is the three-seed mean and
"with a bootstrap 95% interval that excludes it" is a modifier of that mean; nothing in p2 says "per seed", and
the full criterion's own wording ("a bootstrap 95% interval over test sequences") likewise names one interval.
The house rule is to commit only to what the bank requires on the most favourable fair reading, so a per-seed
gate would be a gate I invented.
The point is moot on these numbers in any case: because the three seeds' predictions are element-identical, each
per-seed interval printed in `result/scores.out` is [0.898044, 0.907247], the same as the mean's, and each one
excludes 0.8791 with about 0.019 to spare. Both readings give the same answer here.

p2's three literal requirements, checked:
- three-seed mean strictly above 0.8791: 0.902852 > 0.8791, margin +0.023752 - verified by my own recomputation.
- a bootstrap 95% interval excluding it: lower end 0.898044 (mine 0.898234) > 0.8791 - verified.
- reproducible pipeline whose split file and seeds are named: split file named with sha256 and its row counts
  reproduced; seeds named as 1, 2, 3; `REPRODUCE.md` gives commands that rebuild the predictions, and the
  per-file sha256s in `result/fit_configA.json` make the identity checkable.

## 2. The zero standard deviation - satisfied in letter, informationless in substance, not vacuous enough to void

p2 asks for a three-seed *mean* and for named *seeds*. It does not ask for a standard deviation at all (that is
the full criterion's wording), and it does not ask for any seed-to-seed spread. Three seeds were run, the seeds
are named, and the mean over them is the claimed number, so p2's text is satisfied as written.
What the three seeds demonstrate is nothing: a mean over three byte-identical fits carries exactly the
information of one fit, and the reported sd = 0 bounds no uncertainty whatsoever. I accept that as honest rather
than as evasion, for three reasons that are checkable inside the bundle: the determinism was pre-registered
(`CLAIM.md` cites `PREREG.md` section 4 and the program prints `DETERMINISM CHECK: 1 distinct prediction-file
sha256 over 3 seeds`), the claim states the zero plainly instead of manufacturing spread, and the identity is
verifiable from the sha256s and from my own element-wise comparison of the three arrays.
One stretch to record. `CLAIM.md` says "the seeds were passed to `numpy.random.default_rng` and
`KFold(shuffle=True, random_state=seed)`". In `code/fit_sealed.py` those two draws are made and then discarded:
`_ = list(KFold(n_splits=5, shuffle=True, random_state=seed).split(Ctr))` and `_ = rng.integers(0, 1000)`, with
a comment saying nothing below consumes the streams. That is disclosed in the code and consistent with the
claim's surrounding text, but the sentence as written suggests the seeds reach the fit, and they do not; it
should read that the seeds are consumed by draws the deterministic fit does not use. This is a wording
correction, not a defect in the measurement.
The real uncertainty this bundle leaves unquantified is not seed noise but configuration-selection noise: the
configuration was chosen in another run, and the only interval here is over test-sequence sampling. My
`confirmed_scope` is written so that it claims no more than that.

## 3. Subsumption and bundling

Not subsumed. A = 0.902852 is strictly above every measurement this operator has made on this split column:
0.900143 and 0.897626 (run 2026-11-19-2355), 0.892323 and 0.886601 (run 2026-11-20-0215). It is the project's
best number on this cell, and it clears the 0.900143 that cost run 2026-11-20-0215 its claim.
Two qualifications I put on the record rather than hide.
(a) The improvement over the project's own 0.900143 is +0.002709, which is smaller than the claim's bootstrap
half-width (about 0.0046) on an unpaired comparison. The bundle's own `the-earlier-runs/noise_floor.out` shows
that the right test is paired over test rows, where the smallest separable difference on this test set is about
0.001561 - so +0.002709 would plausibly separate - but that paired comparison was run for the 0215-vs-2355 pair
and **not** for A against 0.900143. So "higher by +0.002709" is established; "separably higher" is not measured
here. p2 does not ask for it, so it does not gate my verdict.
(b) Whether p2 has already been awarded to this project is not stated anywhere in the bundle. Run
2026-11-19-2355's `the-earlier-runs/p2_all_scores.out` shows 0.900143 already clearing both of p2's gates
(interval [0.896589, 0.905584], margin +0.022207). If the panel's own records show that run's p2 was accepted,
then this filing is an incremental re-measurement of a partial win already held, and the operator should be told
that rather than credited twice; that is a bookkeeping question I cannot settle from `claim/` alone. On the
evidence inside `claim/`, the claim object itself is new and is not subsumed.
Not bundling. One claim object is named (A); B is labelled "supporting, not the claim object" in the table and
in the prose, and `CLAIM.md` says explicitly that no claim rests on the selection-criterion observation that B
serves. `result/scores.out` prints p2 gates for B too, but the claim asserts p2 once, for A. No downgrade
trigger fires.
Worth noting in the claim's favour: B is the fully sealed configuration and it also clears p2's arithmetic
(0.897451 > 0.8791; interval [0.892649, 0.901823], reproduced by me at 0.897451), so the p2 threshold is cleared
in this bundle even by a configuration with no test-informed history at all - though B on its own would be
subsumed by the earlier 0.897626 and so could not be the claim object.

## 4. The full criterion, read literally

Clause by clause against A:
1. predictions for every test row of one named FLIP GB1 split that has a scoreboard value - met (5,743 rows,
   each exactly once, verified by me);
2. produced by a model that reads no test label - met for the fitting procedure (see section 6);
3. training code and the exact released split file named - met;
4. Spearman recomputed by the skeptic with `scipy.stats.spearmanr` against the split's score column - I did
   recompute it and I get 0.902852;
5. strictly higher by at least 0.02 than the scoreboard value - 0.902852 >= 0.8991, met;
6. strictly higher than any published value for the same split found by the novelty check - on the bundle's own
   survey (`the-earlier-runs/related_work.md`) the highest is 0.8995 +- 0.0058 (ProtEGNN(t6)) and 0.902852 is
   strictly above it, so the clause reads as met on this bundle's evidence;
7. mean and sd over at least three seeds plus a bootstrap 95% interval over test sequences excluding the
   published bar - met, reading "the published bar" as the scoreboard value 0.8791 being beaten, which is the
   fair reading of the criterion's own antecedent. Note that the interval does **not** exclude 0.8995; if "the
   published bar" were read as the highest published value instead, clause 7 would fail.

So, literally: the full criterion's arithmetic is satisfied by A on these numbers, and the claim is right that
its own three numbers meet it. I nevertheless do not certify the full win in this bundle, for two reasons that
are not noise-margin gates of my own invention.
First, clause 6 is explicitly "found by the novelty check", so it is the panel's NOVELTY skeptic's return and
not mine; if NOVELTY surfaces any published `three_vs_rest` value at or above 0.902852, clause 6 fails and the
full criterion fails with it. I can confirm clause 6 only against the survey the claimant supplied, which is
the claimant's own evidence.
Second, the claim does not assert the full criterion, and a skeptic should not award a level the claimant has
withdrawn, particularly when the claimant's reason touches the criterion's purpose: the claim object's kernel
shape was chosen with sight of a test score on this exact test set (section 5).
On the claim's self-restraint: it is understating relative to the literal text, and it says so itself. I judge
the restraint correct as scientific practice and correct in its three reasons (+0.0034 inside ProtEGNN's own
+-0.0058 and inside the claim's own half-width; the ~0.906 noise-floor figure in `noise_floor.out`; the
informed kernel shape). The right route to the full win is a re-filing whose claim object is either a
fully sealed configuration or a mean above about 0.906 - not a re-reading of these same numbers.

## 5. The "nearly sealed" disclosure - leakage by selection, narrowing but not voiding

What happened, from `UNSCORED-PREDICTION-as-sealed.md` and `CLAIM.md`: A's kernel shape (s2, s3) = (0.5, 0.25)
is the shape run 2026-11-19-2355 had already scored at 0.900143 / 0.901307 on this test set, and the author knew
that when the withheld extrapolation-matched criterion was applied to the 3,859-configuration grid. A differs
from that earlier configuration only in the target-transform offset. B is free of this.
My reading. This is selection-informed, not label-informed: nothing in A's fit touches a test score, which I
accept on the strength of the nan refit (section 6). What it means is that A's 0.902852 is drawn from a
neighbourhood that was already known to score high on this test set, so A's number carries an optimistic bias
of unknown size, and the bias channel is exactly as wide as the differences between near neighbours of that
shape - which `the-earlier-runs/extrap_select.out` shows to be small in the selection metric, and which the
project's own spread on this cell (0.886601 to 0.902852) shows need not be small on test.
Consequence. This does not void p2. p2's gate is 0.8791 and the bias channel is two orders of magnitude smaller
than the +0.0238 margin; even B, with no such history, clears p2. It would, in my judgement, void a record-grade
or full-criterion award, where the live margin is +0.0034 over the published maximum and the bias channel is of
that same order.
The disclosure is adequate, and more than adequate: it is stated in the claim's own voice, unsoftened ("A's
kernel shape was informed by a test score an earlier run had seen"), it is traceable to the earlier run's
verbatim record in the bundle with that record's sha256, and the cleaner configuration is identified as such. I
required no narrowing of the claim's own wording on this point; my `confirmed_scope` carries the caveat so that
the confirmed sentence cannot be quoted without it.

## 6. Hidden quantifiers and stretched definitions elsewhere

- "every test row (5,743), covered exactly once" - verified independently: 5,743 test rows, 5,743 distinct join
  keys, each predicted once, zero duplicates, extras or missing. Not wider than the evidence.
- "reads no test label" - supported, and by the strongest available means. `code/fit_sealed.py` reads `score`
  once, at `ytr = G.scores(tr)` over fitting rows only; the train-train Gram, the double-centring constants and
  the ridge solve all come from fitting rows, so there is no transductive use of test features either, only the
  cross-kernel needed to predict. `result/leak_test.out` refits both configurations on a copy with all 5,743
  test scores set to `nan` and gets six byte-identical prediction files. The scorer passes a known positive
  (rho = 1) and a known negative (rho = -1). I did not find a path by which a test label could reach the fit.
- "the exact released split file named" - the file is named with its sha256 and I reproduced its row and split
  counts, and the scored predictions join to it exactly. I cannot verify from `claim/` that this file is
  byte-identical to the upstream plmfit release; that is a provenance check for NOVELTY or REPRODUCE, and the
  claim's wording ("used unchanged") is an assertion I did not confirm.
- "no pretrained protein language model at all" - supported. `code/gb1k.py` is 224 lines whose only imports are
  csv, hashlib, numpy and scipy; features are one-hot indicators of four sites and their pairs and triples via
  match counts; a recursive grep of `code/` for esm, torch, transformers, embed, pretrain, `.pt` and `.npz`
  returns nothing. No embedding file is shipped or read.
- the selection-criterion section - appropriately hedged, not wider than its evidence: it calls the +1.0000 a
  selection effect, reports that the agreement degrades to +0.9762 once the two new points are added, notes the
  two out-of-sample points share a test set and that one of them is only nearly sealed, and states that no claim
  rests on it. One naming slip: it cites `../attempts/criterion-test/criterion_compare.out`, a path outside the
  bundle; the corresponding file inside the bundle is `the-earlier-runs/criterion_compare-this-run.out`, which
  does contain the arithmetic and ends "VERDICT ON THE EVIDENCE: suggestive, not established."
- the bar's own provenance - `result/scores.out` prints the bar as "carried over, PENDING STATUS CHECK" while
  the status page was fetched at 05:42:28Z; the claim states the page is byte-identical to three earlier
  fetches, so the carried-over 0.8791 and the fetched 0.8791 agree. I read 0.8791 off the saved page myself.
- one comparability wrinkle the claim raises itself and does not bury: two `three_vs_rest` test sets are in
  circulation (5,765 rows in the PLMFit paper's table, 5,743 in the released file used here), so the scoreboard
  0.8791 may not be on the same 5,743 rows this claim scores. The bank's instruction is to name the file and its
  counts, which is done. It matters more for the full criterion than for p2.

## 7. Null models

No null model is required for a claim of this shape, and I did not need `PREREG.md` to decide that. The claim
is a point measurement of a fixed metric on a fixed test set compared with a fixed published table value, with
two fully specified configurations given as inputs; there is no search whose yield needs a null, and no
detection count whose false-alarm rate needs calibrating. What such a claim does need, and what this bundle
has, is a coverage gate, a scorer validated on a known positive and a known negative, a refit with the test
labels destroyed, and a resampling interval on the quantity being compared.
For completeness I ran the null that was absent - 200 permutations of A's predictions against the targets -
and got mean rho 0.00179, sd 0.01355, largest |rho| 0.03978, so the metric returns nothing like 0.879 by chance
here. If I had needed the pre-registration for anything it would be two items only: that p2's gates and the
+0.02 arithmetic were fixed before `result/scores.out` was produced, and that the two configurations in
`code/fit_sealed.py` (`SEALED`) match the frozen text; the bundle makes the second checkable against
`UNSCORED-PREDICTION-as-sealed.md` and against the two `WOULD SELECT:` lines of
`the-earlier-runs/extrap_select.out`, and I confirmed that match by hand.

## Verdict

p2 is met, by configuration A, on my own recomputation of every number that gates it.
The full criterion's arithmetic is also satisfied by A as the criterion is written, but I do not certify it
here: its "any published value found by the novelty check" clause belongs to the NOVELTY skeptic, and the claim
does not assert the level.
The three-seed requirement is satisfied in letter and carries no information, which I record as a narrowing
rather than as grounds for refusal.
The selection-leakage disclosure narrows what the number means and is itself adequate and unsoftened.

confirmed_scope: Partial win p2 is met by configuration A of this bundle - on the `three_vs_rest` column of the released file `data/gb1_data_full.csv` (8,733 rows; 2,691 train / 299 validation / 5,743 test), a kernel ridge regression on the one-hot third-order expansion of the four varying sites, using no pretrained protein language model, fitted only on the 2,990 non-test rows, predicts all 5,743 test rows exactly once with a three-seed (1, 2, 3) mean Spearman of 0.902852, seed-to-seed standard deviation exactly 0 because the fit is deterministic, whose 10,000-resample bootstrap 95% interval over test sequences [0.898044, 0.907247] lies entirely above the PLMFit scoreboard value 0.8791 for that split, with the disclosed caveat that this configuration's kernel shape was chosen with knowledge of a score it had obtained on this same test set in an earlier run.

pass: true
