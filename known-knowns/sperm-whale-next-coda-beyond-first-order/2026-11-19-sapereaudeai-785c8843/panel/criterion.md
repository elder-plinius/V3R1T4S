# CRITERION skeptic - sperm-whale-next-coda-beyond-first-order, partial win p3 (DominicaCodas.csv)

context: subagent (Claude Code Agent tool, criterion type)

Read: claim/CLAIM.md, PREREG.md, PREREG.v2.md, REPRODUCE.md, baseline/README.md, code/, result/, null/ (including
null_test_PROVISIONAL.md), and the bank entry. I did not read any other panel file or any other part of the run
folder. My own scripts and their outputs are in panel_work/criterion/ (check_p3.py, check_p3_b.py, *_output.txt).
They read the CSV with the csv module and rebuild every definition from the bank text, not from dompipe.py.

## Literal reading of p3, clause by clause

1. **"DominicaCodas.csv, all 8,719 rows of both clans"**: MET. sha256 53dd44fb...b45 and 747,518 bytes, as the
   bank says. 8,719 rows: EC1 7,770, EC2 949. No row has an empty Date, Unit, CodaType, codaNUM2018 or IDN. All 8,719
   rows sit in the 109 streams, so pandas' groupby dropped none. No clan filter is applied, and no stream mixes
   clans.
2. **"tokens are CodaType"**: MET. 35 distinct CodaType strings, including the N-NOISE types, are used as is. The list
   is identical to result/p3_vocab.csv, and the model and the bigram share it ("over the same tokens").
3. **Date rewrite**: MET. 101 raw Date strings become 97 after the hyphen-to-slash rewrite. 13 raw dates use hyphens,
   and exactly 4 of them also appear with slashes: 02-03-2015, 12-05-2016, 19-03-2015 and 31-03-2015. That matches
   the bank's "four days both ways".
4. **Streams = rewritten Date + Unit, ordered by codaNUM2018**: MET. There are 109 streams. codaNUM2018 is unique and
   integer-valued across the file, with no ties inside any stream, and the order within each stream equals file
   order.
5. **Folds = distinct rewritten Dates sorted as text, i mod 5**: MET. Folds hold 20/20/19/19/19 dates, and my fold
   map is identical to result/p3_folds.csv.
6. **Scored set ("the same test": >= 2 earlier codas in the stream)**: MET. My scored set has 8,501 positions. The
   (stream, position) to (true token, fold) map is identical to both probability files, with no duplicates or
   omissions.
7. **"a smoothed bigram over the same tokens"**: MET, and the reading is fair. "The same test" carries R1 over:
   additive alpha from {0.01, 0.03, 0.1, 0.3, 1}, chosen by inner leave-one-training-fold-out CV on the scored
   positions and refit on the 4 training folds. I wrote the bigram independently. It picks alpha 0.3 in every fold
   and reproduces result/p3_probs_bigram.csv with a maximum absolute difference of 0.0.
   - Stronger readings do not close the gap. An oracle bigram, with alpha tuned on the held-out fold itself over 40
     values from 0.001 to 3, improves the bigram by only 0.0010 bits, and the model still beats it by 0.1274. An
     oracle-tuned bigram/unigram interpolation is worse than the bigram (1.7502 bits).
8. **Full distribution, strictly positive**: MET. Both files have 35 columns. The minimum entry is 3.9e-05 for the
   model and 9.5e-05 for the bigram, and every row sums to 1 within 7e-16.
9. **"beats ... by at least 0.05 bits per coda" (pooled over the 5 folds)**: MET. My recomputation gives bigram
   1.717914 and model 1.589491, so the gain is +0.128423. The gain is positive in every fold: 0.143, 0.113, 0.150,
   0.151 and 0.089.
10. **"bootstrap interval over Date groups excluding 0"**: MET. The bootstrap is paired, per position, over the 96
    rewritten-Date groups that own scored positions (one of the 97 dates has no stream of 3 or more codas). It uses
    10,000 resamples, statistic sum of gains / count, and a 95% percentile interval.
    - Seed 20261119 reproduces [0.0879, 0.1630]. Fresh seeds give [0.0873, 0.1638] (seed 77) and [0.0878, 0.1638]
      (seed 4242).
    - Leave-one-date-out, the smallest pooled gain is 0.1158. Dropping the 5 dates that contribute most still leaves
      0.0839. 27 of the 96 dates have a negative net gain, so the gain is not carried by a handful of dates.
11. **"a model using two or more previous codas"**: MET literally, and with a specific character.
    - dompipe.feats reads codas t-2 and earlier: skip-bigram, same-as-t-2, the order-free cache of all earlier
      tokens, run length, stream repeat rate, same-whale-last and echo-after-switch.
    - The pre-declared `one` diagnostic (previous coda only, same family and pipeline) gains just +0.0059 over the
      bigram. So the gain does come from codas before the previous one.
    - Most of it is order-free: the stream cache (rep minus local) is 0.0855 bits. The model beats its order-free
      stream-local diagnostic `local` by only +0.0255 [0.0147, 0.0356].
    - p3's words require only that the model uses two or more previous codas and beats the pooled bigram. They do
      not require that the gain come from coda order, so this is not a stretched definition. CLAIM.md states the
      decomposition plainly.
    - Caveat: `one`, `rep` and `local` have no per-position probabilities in result/, so I could not recompute them
      from the shipped files. The decomposition rests on the author's run (run_output.txt and p3_summary.json are
      consistent with the table). It is a diagnostic, not a gate.
    - Clan check (mine, not a gate): within EC1 alone the gain is +0.1046 [0.0645, 0.1394] over 90 dates, and within
      EC2 it is +0.3203. The pass therefore does not rest only on the cache recognising the smaller clan's
      repertoire.
12. **Input rule (only earlier codas of the same stream, never any field of the predicted coda)**: MET.
    - feats sees only hist(s, t), the [:t] slices of the token and IDN arrays. Unit, Date, Clan and the ICIs are not
      in the stream arrays.
    - Count tables come from the training folds, cross-fitted for training rows. No held-out token enters any table.
    - The vocabulary and the date-to-fold map use the whole file, but the bank's own definitions make them so.
    - The leakage self-test perturbs every readable field of row t and all later rows. It reports 0 of 42,505 vectors
      changed and the positive control flagged 8,501 of 8,501, and my reading of the code confirms the design.
    - Minor: inside the lambda inner CV, the training rows of the other inner folds carry features from tables that
      include the inner held-out fold. That affects only lambda selection within the training folds, never outer
      held-out data.
13. **IDN-string quirk (PREREG.v2.md item 2)**: not a criterion problem.
    - IDN values are strings, so the comparison with the integer 0 never matches, and '0' (5,705 unidentified rows)
      acts as one more whale label.
    - The features still read only the IDN of earlier codas, and the main criterion explicitly allows whale labels
      of earlier codas.
    - Keeping the frozen feature definition, instead of "fixing" it after the freeze, was correct.
    - The quirk can only affect the ordered/whale share (about 0.0255 bits). The IDN-free `local` diagnostic is
      already 0.1029 below the bigram, so the pass does not hinge on it.
14. **Harness fix (PREREG.v2.md item 1)**: within the declared escape hatch.
    - dompipe.py's sha256 equals the freeze value (63f94f42...). score_p3.py differs from its freeze value
      (1c4bbd2f... against 303337ac...), as disclosed.
    - The fix only changes how IDN is perturbed (a suffix, asserted to change every value).
    - Wording nit: in the harness, the fold-0 bits are computed in memory before the leakage loop. "Before any
      held-out score was computed" is therefore slightly loose, but nothing was printed or saved before the crash,
      so no score was seen. Not material.
15. **Pre-registration**: frozen and followed, as far as the package shows.
    - Features, grids, seed, diagnostics and gate match the code. The gate is exactly the bank's threshold, neither
      stricter nor looser.
    - Development touched date folds 0 and 3, as disclosed. The folds not used in development (1, 2 and 4; 5,606
      positions) give +0.1187 [0.0703, 0.1568] with a fresh seed, which is itself above both thresholds.
    - I cannot verify the freeze time independently: file times inside the package are copy times. It rests on the
      run record.
16. **baseline/ record**: same data, folds, scored set and metric as the claim, and I reproduced it exactly (item 7).
    Deliverables: per-position probabilities for the model and the reference are shipped. Bin edges and a cut twin do
    not apply to p3's stated condition.

## Null model (N3)

- **Design: a fair test of p3.** Each stream keeps its first coda, its length, its date, fold and Unit, and its real
  IDN, nClicks and Duration. Tokens are redrawn from the whole file's pooled first-order transitions, so the pooled
  smoothed bigram is essentially the true model. The identical pipeline then runs with all 5 folds and all inner CV,
  and the statistic is the same pooled gain.
- **Shims.** The einsum and warm-start fit is a speed shim on a convex L2-penalised objective, reported to match real
  fold 0 within 7.4e-12. The verification file is not in the package.
- **Limitation (interpretation only, not a defect for p3).** N3 also removes between-stream heterogeneity. It rejects
  "a pooled homogeneous first-order process" but cannot separate stream-level context from coda-order dependence.
  confirmed_scope below is worded accordingly.
- **Provisional results.** 78 controls have finished: mean -0.00435, sd 0.00201, maximum 0.00115, against a real gain
  of 0.1284.
- **This pass depends on the main session's honesty gate.** All 400 controls must finish and the real gain must
  exceed every one. If either fails, this pass is void.
- CLAIM.md's Null section still reads PENDING and must be filled in before any filing.

## Claim text against the evidence

The one-sentence claim in CLAIM.md is accurate and no wider than the evidence. The target's headline asks to "show
dependence beyond the previous coda". This result shows that codas before the previous one improve prediction over a
pooled bigram. By the pre-declared diagnostics, most of that improvement is order-free stream-level context, not
order. Any outward wording must keep that distinction, as CLAIM.md does.

The win is not subsumed by anything in this package: p3 is a distinct enumerated partial win on a different file
from the main criterion and from p1 and p2. Literature novelty is the NOVELTY skeptic's remit.

confirmed_scope: On DominicaCodas.csv under the bank's p3 setup (all 8,719 rows of both clans, CodaType tokens, hyphen-to-slash Date rewrite, rewritten-Date + Unit streams ordered by codaNUM2018, text-sorted date folds i mod 5, 8,501 scored codas), the frozen log-linear model, reading only the CodaType and IDN of earlier codas of the same stream, has pooled held-out cross-entropy 1.5895 bits per coda, 0.1284 bits below the inner-CV-smoothed bigram over CodaType (1.7179), with a 95% paired bootstrap interval over rewritten-Date groups of [0.0879, 0.1630] (10,000 resamples), which shows that earlier codas beyond the previous one improve prediction over a pooled bigram, not that coda order does (by the pre-declared diagnostics most of the gain is order-free stream-level context), conditional on the N3 null gate (400 controls, real gain above all).

pass: true
