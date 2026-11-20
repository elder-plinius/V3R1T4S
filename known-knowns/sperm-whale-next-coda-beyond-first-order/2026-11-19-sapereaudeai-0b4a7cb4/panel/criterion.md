# CRITERION skeptic - sperm-whale-next-coda-beyond-first-order (claim: FULL success criterion)

context: subagent (Claude Code Agent tool, criterion type)

I read only the claim package (claim/CLAIM.md, PREREG.md, PREREG.v2.md, REPRODUCE.md, baseline/, code/, result/,
posthoc/, null/) and the bank entry in bank/targets.json. The bank wording quoted in CLAIM.md and PREREG.md matches
targets.json word for word (success criterion, verification method, pitfalls). My scripts and their outputs are in
panel_work/criterion/ (check1.py, check1_output.txt, check2.py, check2_output.txt). All were run with the venv
interpreter in isolated mode, single-threaded, one job at a time. Nothing was downloaded or unpickled.

## Literal reading, clause by clause

1. **Data.** claim/data/sperm-whale-dialogues.csv: sha256 1856c8bf915cc5ae6f928aaa2036cbbc6ad8840bb6e4f6a96aaeb96953215da2,
   500,380 bytes (the bank's size), 3,840 rows, 219 REC. Met.
2. **Streams.** My own parser (csv module, Python's stable sort on TsTo within each REC) finds 7 tie rows, the bank's
   count, kept in file order. Ordering by (REC, pos) and the true token at every scored position equal the saved files
   exactly, in the same order. Met.
3. **Folds.** Distinct REC strings sorted as text, i-th REC in fold i mod 5. My folds equal result/folds.csv (219/219).
   Codas per fold are 598, 1387, 593, 779 and 483, matching the bank's "483 to 1,387". Each fold is held out once. Met.
4. **Token and bin edges.** Token = (min(nClicks,10), duration bin) over a 50-token vocabulary with id (c-1)*5+b.
   The bin edges are numpy quantiles at 0.2/0.4/0.6/0.8 of the four training folds' durations only, and my edges equal
   result/bin_edges.csv bit for bit in all 5 folds. Edges come only from the training folds, and the code
   (seqpipe.run_fold) computes them from the training folds only. The 8 one-click, zero-duration codas fall into click
   class 1, bin 0. Met.
5. **Scored set.** Every coda with at least 2 earlier codas (positions >= 2): 3,418 positions, as the bank says, owned
   by 188 RECs. Met.
6. **Reference R1.** This is the bank's R1: a 50-token bigram, P = (n(a,b)+alpha)/(n(a)+50 alpha), with alpha from the
   bank's grid. The saved probs_R1.csv equals my independent alpha=0.3 bigram exactly (max abs difference 0.0). The
   bank does not define "inner cross-validation on the training folds" in detail, so I recomputed R1 under every
   convention I could think of:
   - **Claim's convention** (leave one training fold out, the outer fold's edges, loss summed over scored positions):
     alpha 0.3 in every fold, R1 = 2.780154.
   - **Recut edges, or score every transition:** recutting the bin edges on the inner training folds, or scoring all
     transitions (positions >= 1), selects alphas [0.3, 0.1, 0.1, 0.3, 0.3] and gives R1 = 2.794781. This exactly
     reproduces the other public claim's value, so that claim used one of these conventions.
   - **Other splits and averaging:** averaging the per-fold mean losses, or leaving one REC out, gives 2.787390.
   - **Fixed alpha:** every fixed grid alpha gives R1 between 2.7802 and 2.9552.
   - **Oracle:** the best alpha per outer fold chosen on the test data gives 2.774694.

   Neither 2.7802 nor 2.7948 is a stretch. Both are fair readings of the bank's words, and the claim's reading gives
   the *stronger* (lower) reference, which is the harder one for the claim. A vocabulary of only the observed tokens
   (37 or 38) is not a fair reading: it puts zero probability on 2 scored positions, so it is not a full
   distribution. Even then the gain on the other 3,416 positions is about 0.6 bits.
7. **The model.** The model is frozen and trained on the training folds only. Training rows are positions >= 2 of the
   training-fold streams. Count tables are cross-fitted for training rows and use all 4 training folds for held-out
   rows. The penalty lambda is chosen by inner CV on the training folds.
   - **Inputs.** I read code/swlib.py (History slices every field to rows [:t] before any feature code runs),
     code/seqlib.py (feats reads only H.a, H.tok, H.t, the training-fold edges and the training-fold tables) and
     code/seqpipe.py (the batch and single-position paths both go through History.of). No field of the predicted coda
     or of any later coda is read. Its token is used only as the label.
   - **Leakage self-test.** The frozen run (result/run_output.txt) shows 0 changed vectors out of 3,418 for R1, twin,
     rep, local and full when every field of the predicted coda and all later codas is altered. The leaky positive
     control was flagged at 3,418 of 3,418, and single-position recomputation equals the batch exactly.
   - **Allowed inputs.** The model uses earlier codas' click counts, durations and whale labels. The bank's
     parenthesis lists allowed inputs; it does not require all of them.

   Met.
8. **Full distributions.** All three files are 3,418 x 50 with no zero entry. The minimum probability is 5.26e-06
   (full), 1.24e-05 (twin) and 5.46e-04 (R1); the maximum |sum-1| is 6.7e-16. Met.
9. **Condition (1)** (pooled cross-entropy at least 0.10 bits below R1). Full = 2.123847 pooled (my recomputation
   from probs_full.csv), so the gain is +0.6563 against the claim's R1 and +0.6709 against R1 = 2.794781. Against any
   fixed grid alpha it is at least +0.6563, and against the test-set oracle R1 it is +0.6508. Every fold is positive
   (0.79, 0.67, 0.77, 0.56, 0.47). **Met under both inner-CV readings and under every R1 on the grid.**
10. **Condition (2)** (at least 0.05 bits below the same model retrained with input cut to the single previous coda,
    with a 95% paired REC bootstrap of 10,000 resamples excluding 0).
    - **Pre-registered twin.** This is the same log-linear family restricted to the 7 features computable from coda
      t-1, plus the training-fold unigram. It is retrained on the same rows with the same lambda search and scores
      2.654909, a gain of +0.5311. The claim's interval is [0.4571, 0.6325]. My fresh-seed intervals are
      [0.4575, 0.6299] (seed 424242) and [0.4578, 0.6340] (seed 9). Resampling all 219 RECs instead of the 188 gives
      [0.4580, 0.6348]. The post hoc deployment-level interval is [0.4479, 0.6350]. Every fold is positive.
    - **Literal twin.** The most literal reading is the frozen `full` feature map applied to a history of coda t-1
      alone (t = 1), retrained with the same lambda search on the same rows. The post hoc file gives 2.646412. I
      re-ran it with my own harness on the frozen code and got exactly 2.646412, a gain of +0.5226 with interval
      [0.4460, 0.6273] (fresh seed 271828).
    - **Twin comparison.** The pre-registered twin is only 0.0085 bits worse than the literal one, interval
      [-0.0074, 0.0223]. So the pre-registered twin is not a weakened strawman.

    **Met under both twin readings.**
11. **Bank pitfalls.**
    - **Repetition runs.** 45.0% of scored codas repeat the previous token. On the 1,881 non-repeat positions the
      full-vs-twin gain is +0.874 bits, interval [0.769, 1.031] (seed 5); on the repeat positions it is +0.111. The
      gain does not come from runs of one token. The repetition-aware `rep` comparison still leaves +0.4415
      [0.3716, 0.5370].
    - **Whale labels.** The model uses whale labels only as same-or-switch between codas t-1 and t-2 inside one REC,
      which treats them as speaker turns within a recording, as the pitfall asks.
12. **Deliverables.** The bank's list is present: code (code/), folds (result/folds.csv), bin edges
    (result/bin_edges.csv), and per-position probabilities for the model, its cut twin and R1 (result/probs_full.csv,
    probs_twin.csv, probs_R1.csv). The literal twin's per-position probabilities are not saved, only its summary and
    code. That is not required, but adding them would help the bank's skeptic, who fits the truncated twin themselves.
13. **Pre-registration.**
    - **Code hashes.** All five code files in claim/code/ have the sha256 values listed in PREREG.md.
    - **Gates and fixes.** The gates are the bank thresholds with no self-invented tightening, and they were applied
      as written (score_content.py). PREREG.v2 concerns only p3 and changes nothing here.
    - **Timing.** The freeze is stamped 09:55:11Z, 16 minutes after the data fetch (09:39:08Z). The package attests
      that no held-out score preceded it, but I cannot verify that from the package itself, because the development
      outputs are outside it and I did not read them. The honesty gate should confirm the timeline.
    - **Dev-fold effect.** On the pristine folds 0, 1 and 3 the result is the same (+0.5212 vs twin, +0.6634 vs R1),
      so design choices made on dev folds 2 and 4 do not drive the result.
14. **N2 null design.** N2 is a fair test of condition (2) as the bank words it.
    - **What it tests.** Under N2 each stream is a first-order Markov chain over records, keyed on a token that is a
      function of coda t-1's own fields. So any history beyond coda t-1 carries no information about the next coda.
    - **Same pipeline.** The controls run the same pipeline end to end: all 5 folds, all inner CV, the same twin and
      the same full model. The null distribution therefore absorbs overfitting, the full model's extra first-order
      capacity, small folds and the fold layout.
    - **What it removes.** N2 deliberately destroys recording-level heterogeneity. Beating it shows that the next coda
      depends on earlier codas of the same stream, whether through order or through stream context. That is what
      condition (2) asks; a stream-specific null would be a self-invented stricter gate.
    - **Speed shims.** The feature-code shims were verified bit-identical. The einsum gradient with warm starts
      reproduces the frozen probabilities within 3.1e-9, which is acceptable and disclosed.
    - **Status.** The null is a kit gate, not a bank clause, and it is NOT yet complete: 105 of 400 controls are done,
      the best control is 0.0084 against a real gain of 0.5311, and the summary is marked PROVISIONAL. The honesty gate
      must confirm that all 400 finish below the real gain. Under PREREG.md's own escape hatch, the claim is PROMISING
      at most until they do.
15. **Is the claim text wider than the evidence?** The one-sentence claim is accurate and within the evidence. Three
    items should be corrected before filing:
    - **Missing file.** CLAIM.md lists `null_test.md`, which is not in the package (only null/null_test_PROVISIONAL.md
      exists). Replace it with the final 400-control file.
    - **Decomposition sentence.** CLAIM.md says "0.3198 bits (local vs twin) is matched by stream-level context with
      no order". That figure includes 0.0896 bits from the REP features (run length and repeat rate, which depend on
      order). Only 0.2302 bits (local vs rep) is the order-free bag. The wording should say so. This does not affect
      either condition.
    - **R1 convention.** The R1 value 2.7802 depends on the inner-CV convention; R1 = 2.7948 if the edges are recut
      inside the inner CV. Say which convention gives which value, so the two public numbers for this cell are not
      read as a discrepancy.

## Observed-vocabulary R1 (tested; not a fair reading; the criterion still holds)

- **The test.** R1 built over only the tokens seen in the 4 training folds (37 or 38 tokens per fold; alpha 0.3 in
  every fold by the claim's inner CV) gives 2.735398 bits pooled over 3,416 positions.
- **Unseen tokens.** At 2 scored positions the true token (or the previous token) never occurs in the training folds,
  so this R1 gives the true token zero probability. Over all 3,418 positions its cross-entropy is therefore infinite.
  That breaks the full-distribution requirement, so this is not a fair reading of the bank's R1.
- **Gain on the 3,416 positions.** The model was not recomputed. From the saved values: full is 2.123847 over 3,418
  positions, and no position costs more than 17.54 bits (its minimum probability is 5.26e-06). So full over the 3,416
  positions lies between 2.1148 and 2.1251 bits, and its gain over this R1 lies between +0.610 and +0.621.
- **Result.** Condition (1) still holds by a wide margin, and over all 3,418 positions it holds trivially.

## Literal cut twin (what it implies)

- **Result.** The full feature map fed only coda t-1 and retrained the same way scores 2.646412 bits. I reproduced
  this independently; it equals the post hoc file. Full vs this twin is +0.5226, 95% REC bootstrap [0.4460, 0.6273]
  (seed 271828), and literal vs pre-registered twin is +0.0085 [-0.0074, 0.0223].
- **Implication 1.** Condition (2) holds under the most literal reading of "the same model retrained with its input
  cut to the single previous coda". Its margin over the 0.05 threshold is about 10 times the threshold, and the lower
  bound of its interval is far above 0.
- **Implication 2.** The pre-registered twin (a feature subset) is not a weakened strawman. It is statistically
  indistinguishable from the literal twin and at most 0.022 bits worse. So the choice of twin reading cannot change
  the verdict on condition (2) or on p2.
- **Disclosure.** The literal twin is post hoc. It can only narrow the claim, and here it does not.

## Verdict on p1 and p2 (separately)

- **p1** requires a gain of at least 0.05 bits over R1 with a REC bootstrap interval excluding 0. The gain is
  +0.6563; the claim's interval is [0.5883, 0.7465]. My intervals are [0.5862, 0.7434] (seed 424242),
  [0.5877, 0.7472] (seed 9) and [0.5891, 0.7481] (all 219 RECs). **Met.** I computed the interval only under the
  claim's inner-CV convention; under the 2.7948 convention the gain is larger (+0.6709), but I did not bootstrap it.
- **p2** requires a gain of at least 0.03 bits over the model's own single-previous-coda twin with the interval
  excluding 0. Against the pre-registered twin the gain is +0.5311 [0.4571, 0.6325]; against the literal twin it is
  +0.5226 [0.4460, 0.6273]. **Met.**
- **Subsumed.** Both p1 and p2 are subsumed by the full criterion, which is the claim being judged.

## Stretched definitions and hidden quantifiers found (including ones that did not change the verdict)

1. **R1 inner CV is underspecified by the bank.** The value depends on two choices: whether the bin edges are recut
   inside the inner CV, and whether all transitions or only scored positions are used.
   - The claim's convention gives 2.7802.
   - Averaging per-fold mean losses, or leaving one REC out, gives 2.7874.
   - Recutting the edges, or scoring all transitions, gives 2.7948 (the other public claim's value).

   The claim's reading gives the strongest reference, and condition (1) holds under all of them. **No change.**
2. **Vocabulary of R1.** 50 tokens (the claim) versus only the observed tokens. The observed-token version is not
   fair (zero probabilities, see above), and the criterion holds under it anyway. **No change.**
3. **Cut twin.** A feature subset (pre-registered) versus the full map on a truncated history (literal, post hoc).
   Both pass. **No change.**
4. **"Bootstrap over REC groups".** 188 groups that own a scored position, or all 219: the intervals are
   [0.4571, 0.6325] and [0.4580, 0.6348]. **No change.**
5. **Tag deployments are split across folds.** The bank's fold rule splits RECs from the same deployment across
   training and test folds (46 deployment prefixes). That is literal to the bank, so it is not a defect. The post hoc
   deployment-level interval [0.4479, 0.6350], which I did not recompute, still excludes 0. **No change.**
6. **"Trained on the training folds only".** It holds for the outer split. Inside the inner CV, the cross-fitted
   tables of the other training rows include the inner held-out fold's counts, and R1's inner CV uses the outer
   fold's edges. This information flow stays inside the training folds and affects only the choice of alpha or
   lambda. **No change.**
7. **"From earlier codas (their intervals, durations, whale labels, time stamps)".** The model also uses earlier
   codas' click counts. The parenthesis lists allowed inputs; it is not exhaustive, and click counts are part of
   every token, R1's included. **No change.**
8. **Dev folds 2 and 4 are in the pooled score.** They were used for development and then scored as held-out folds.
   The bank specifies a pooled 5-fold score, so this is literal. The pristine folds 0, 1 and 3 give the same result
   (+0.5212 vs twin). **No change.**
9. **N2 null design.** N2 removes differences between recordings, so beating it shows dependence on earlier codas of
   the stream through order or through stream context, without telling which. Condition (2) as worded asks for
   exactly that, and the `local` diagnostic shows +0.2112 [0.1741, 0.2445] beyond an order-free stream bag. Fair.
   **No change.**
10. **Wording in CLAIM.md (not the claim sentence).** "0.3198 bits ... stream-level context with no order" includes
    0.0896 bits of features that depend on order (run length and repeat rate). Only 0.2302 bits is order-free. The
    wording must be corrected before filing. **No change to the verdict.**
11. **Missing file.** CLAIM.md lists `null_test.md`, which is absent; only null/null_test_PROVISIONAL.md exists. This
    must be fixed before filing.
12. **Freeze timing.** I cannot verify from the package that the freeze (09:55:11Z, 16 minutes after the data fetch)
    preceded every held-out score. The code hashes match PREREG.md.
13. **Literal-twin probabilities.** The literal twin's per-position probabilities are not delivered (only its code
    and summary). This is not required, because the delivered twin is the pre-registered one.

## Verdict

**Bank literal success criterion: MET.** Both conditions are met literally and pooled:
- under every fair reading of R1 (2.7802, 2.7874 or 2.7948, and every grid alpha), and also under the unfair
  observed-vocabulary reading;
- under both readings of the cut twin.

The scored set, folds, edges and tokens are exactly the bank's. The probabilities are full distributions with no zeros.
The model reads only earlier codas of the same stream. Both bank pitfalls are addressed with large margins. p1 and p2
are each met separately and are subsumed.

**The pass is conditional.** These conditions are not yet settled:
- **(a) N2 null (kit gate, not a bank clause).** All 400 N2 controls must finish, and the real gain of 0.5311 must
  exceed every one. At my reading 105 of 400 were done; the best was 0.0084 and the mean 0.0005.
  - If any control reaches 0.5311, this is a fail.
  - If the 400 do not finish, PREREG.md's own escape hatch caps the claim at PROMISING, and this pass must not be used
    to file it.
- **(b) Freeze timeline.** The freeze must be confirmed as preceding every held-out score (the dev outputs are outside
  the package I was allowed to read).
- **(c) Package fixes before filing.** The final null_test.md must replace the provisional file, and CLAIM.md's
  decomposition sentence must be corrected (item 10).

confirmed_scope: On sperm-whale-dialogues.csv (sha256 1856c8bf...5da2), with the bank's REC streams, tokens, folds, training-fold bin edges and 3,418 scored codas, the frozen log-linear model `full` of code/seqlib.py, reading only earlier codas of the same REC stream, scores 2.1238 bits per coda pooled over the 5 held-out folds, which is 0.6563 bits below R1 (2.7802 under the claim's inner-CV convention, and at least 0.65 bits below R1 at every alpha of the grid) and 0.5311 bits below its pre-registered single-previous-coda twin with a 95% paired REC bootstrap interval (10,000 resamples) of [0.4571, 0.6325] (0.5226, [0.4463, 0.6273], against the post hoc literal truncated-input twin), so conditions (1) and (2) of the full success criterion are met.

pass: true
