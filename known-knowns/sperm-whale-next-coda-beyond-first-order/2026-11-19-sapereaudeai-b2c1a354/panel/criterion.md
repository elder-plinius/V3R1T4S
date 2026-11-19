# CRITERION verdict - sperm-whale-next-coda-beyond-first-order, partial win p4 (turn-taking)

context: subagent (Claude Code Agent tool, criterion type)

Material read: claim/CLAIM.md, claim/PREREG.md, claim/PREREG.v2.md, claim/REPRODUCE.md, claim/baseline/README.md,
claim/code/{p4lib.py, swlib.py, score_p4.py, leak.py}, claim/null/{nulls.py, N4_controls.csv}, claim/result/*,
and the bank entry (bank/targets.json, id sperm-whale-next-coda-beyond-first-order). My own scripts are in
panel_work/criterion/ (check1.py, check2.py, check3.py); they read only the claim's CSV files, use csv + numpy, and
do not import the author's code.

## The criterion, quoted

The p4 wording in CLAIM.md is identical to the bank entry: "Turn-taking: on the dialogues folds, predict whether
the next coda carries the same whale label as the previous one with held-out log-loss at least 0.05 bits below a
smoothed first-order model of that same-or-switch sequence, with a bootstrap interval over REC groups excluding 0."
The success-criterion text quoted for streams, folds and scored set also matches the bank verbatim.

## Literal reading, clause by clause

1. **"on the dialogues folds"**: met. I rebuilt everything from sperm-whale-dialogues.csv (sha256 1856c8bf...215da2,
   which matches the claim). There are 3,840 rows and 219 RECs. Streams are grouped by REC and ordered by TsTo, with
   ties kept in file order; there are exactly 7 ties within RECs, as the bank says. I sorted the distinct REC strings
   and put the i-th in fold i mod 5. This agrees with result/folds.csv for all 219 RECs. Codas per fold are
   598/1387/593/779/483, matching the bank's "483 to 1,387". The scored set is every coda with at least 2 earlier
   codas: 3,418 positions (514/1305/508/692/399). The (REC, pos) set in result/p4_per_position.csv equals this set,
   with no duplicates and 0 fold mismatches. Each fold was held out once.
2. **"predict whether the next coda carries the same whale label as the previous one"**: met. y_t = [Whale_t ==
   Whale_{t-1}]. My independently computed y matches y_same at all 3,418 positions. The model outputs a probability
   strictly inside (0,1) at every position (range 0.0166 to 0.9656), so log-loss is finite and well defined.
3. **"a smoothed first-order model of that same-or-switch sequence"**: met, on a fair and natural reading. The
   reference is P(y_t | y_{t-1}), counted over all consecutive same/switch pairs in the training-fold streams. Its
   additive alpha is chosen from the bank's own R1 grid {0.01, 0.03, 0.1, 0.3, 1} by inner leave-one-training-fold-out
   CV, mirroring how the bank specifies R1. My own implementation picks the same alpha in every fold (1, 0.01, 1,
   0.01, 1) and reproduces p_same_ref exactly (max abs difference 0.0). The smoothing choice is immaterial: against
   the unsmoothed maximum-likelihood chain the gain is 0.08722 instead of 0.08721. I also tested a stricter reading
   that the bank does not require, as a diagnostic only: a stream-local adaptive first-order chain (per-stream
   transition counts from earlier codas, shrunk to the pooled chain, prior weight chosen by inner CV). The model still
   beats it by 0.0620 bits, 95% REC bootstrap [0.0424, 0.0809]. So the result does not hinge on reading the
   reference as pooled.
4. **Input rule (the success criterion: only earlier codas of the same stream, never any field of the predicted
   coda)**: met by code reading. In p4lib.py, feats() receives only _hist(s, t), which slices every field to rows
   [:t]. Its 21 features use Whale, TsTo, Duration and nClicks of rows t-1, t-2 and t-3 and stream-level summaries of
   rows [:t]. Row t is read only by target(), which is used solely as the label. The reference uses Whale[t-1] and
   Whale[t-2]. The StandardScaler and LR are fitted on training-fold rows only, and C is chosen by inner CV on the
   training folds only. The built-in leakage test perturbs every field of the predicted coda and all later codas. It
   reports 0 of 3,418 changed and flags the positive control at 3,418 of 3,418; I read this from p4_summary.json and
   did not rerun it. Class labels are used only through equality inside a stream (prev_is_mode breaks ties by label
   value, which is harmless). This honours the pitfall "treat them as speaker turns within a recording".
5. **"held-out log-loss at least 0.05 bits below"**: met. I recomputed from the per-position file. Pooled reference
   is 0.850317 bits, model 0.763112 bits, gain +0.08721 bits per coda. Every fold also clears 0.05 on its own: gains
   +0.0727, +0.0693, +0.1511, +0.0735 and +0.1070. Leaving out any one fold gives a pooled gain of 0.076 to 0.098. So
   the reading of "on the dialogues folds" does not matter: pooled and per-fold both pass.
6. **"a bootstrap interval over REC groups excluding 0"**: met. swlib.rec_bootstrap resamples, with replacement,
   the 188 RECs that own at least one scored position. It sums per-position paired gains and divides by the
   resampled position count. It uses 10,000 resamples and a 95% percentile interval. This is truly a REC-group
   bootstrap. With my own code: author seed [0.06486, 0.11662], identical to the claim. Fresh seeds 424242, 7 and 99
   give [0.0651, 0.1163], [0.0648, 0.1157] and [0.0648, 0.1161]. No resample is ever <= 0.
7. **Pre-registration frozen and followed**: consistent, as far as the package can show. PREREG.md states it was
   frozen at 2026-11-19T09:55:11Z, after data fetch (09:39:08Z), and PREREG.v2 (09:57:51Z) is about p3 only. The
   sha256 of claim/code/swlib.py, leak.py, p4lib.py and score_p4.py all equal the hashes frozen in PREREG.md. The
   model family, the 21 features, the C grid, the alpha grid, the bootstrap seed, the gate and the diagnostics are
   all as declared. The package has no independent timestamp for the scoring run itself, so "scored after the
   freeze" rests on the PREREG statement plus the hash match. Development used folds 2 and 4, and those folds carry
   the largest gains (0.1317 together). The pristine folds 0, 1 and 3 alone still give +0.0711, [0.0448, 0.1026] with
   my seed. So dev-fold selection cannot account for the pass.
8. **Null controls (null/)**: a fair test of the structure p4 claims. N4, as coded in nulls.py, matches the PREREG
   text. It keeps Whale_0 and Whale_1 per REC, then draws y_t from the pooled maximum-likelihood first-order chain,
   with new labels drawn uniformly from {1..max(K,2)} minus the current one. Other fields are kept real. The full
   5-fold pipeline with inner CV is rerun each time, with seeds 1000+i. Under this null the reference is the true
   model. The file has 400 distinct controls with the right seeds: max +0.00095, mean -0.0059, SD 0.0026. The real
   +0.0872 is above all 400. The null removes both higher-order dependence and between-stream heterogeneity, so on
   its own it does not separate the two. That separation is done by the diagnostics in item 3 (stream-local
   reference) and item 9 (the pattern-only model). nulls.py is not in the PREREG hash list, but its N4 design matches
   the frozen text.
9. **Possible artefacts named by the pitfalls**:
   - *Per-recording whale labels*: not an issue, because only within-stream equality of labels is used.
   - *Small folds*: every fold passes on its own, leave-one-fold-out passes, and dropping the 10 RECs that
     contribute the most gain leaves +0.0700.
   - *Single-label recordings*: 58 RECs with 237 positions give +0.466 bits per position, about 37% of the total
     gain. Excluding them, the 130 multi-label RECs (3,181 positions) give +0.0590 [0.0348, 0.0816]. That still
     clears 0.05, and the interval excludes 0. Positions whose history already holds at least 2 labels give +0.0738
     [0.0516, 0.0994].
   - *Pure label-sequence order*: the pre-declared "pattern" diagnostic uses only the last two same/switch states
     and A-B-A, with no timing and no stream rates. It gives +0.0595 [0.0439, 0.0790] with my seed. So there is
     genuine beyond-first-order dependence in the turn sequence itself.
10. **Is the claim text wider than the evidence?** No, in substance. The numbers in CLAIM.md (3,418; 0.7631;
    0.8503; 0.0872; [0.0649, 0.1166]; per-fold table; diagnostics) all match my recomputation. Two small precisions
    belong in the scope: the first-order reference is pooled over the training-fold streams, and the model also uses
    parameters fitted on the training folds. The claim asks for p4 only and does not suggest that the main criterion
    or p1-p3 are met.
11. **Genuine and not subsumed**: p4 is a separately enumerated partial win about a different target variable
    (same-or-switch of the speaker label, not the coda token). The claim does not lean on any other win. Whether it
    is new is NOVELTY's question, not mine.

Limits of my check: I did not rerun the author's pipeline or the 400 nulls; that is REPRODUCE's job. The model
probabilities come from result/p4_per_position.csv. Within the package, I independently reproduced the target,
folds, scored set, reference probabilities, all metrics and the bootstrap.

confirmed_scope: On the bank's five REC folds of sperm-whale-dialogues.csv (3,418 scored codas), the frozen logistic-regression model, trained on the training folds only and reading only earlier codas of the same REC stream, predicts whether each scored coda carries the same whale label as the previous coda with pooled held-out log-loss 0.7631 bits per coda, 0.0872 bits below a smoothed first-order same-or-switch chain fitted on the pooled training-fold streams (0.8503 bits; additive alpha chosen by inner CV from the R1 grid), with a 95% paired REC-group bootstrap interval of [0.065, 0.117] (10,000 resamples) excluding 0.

pass: true
