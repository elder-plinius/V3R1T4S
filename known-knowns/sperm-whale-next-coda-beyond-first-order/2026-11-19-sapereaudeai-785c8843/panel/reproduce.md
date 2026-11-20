# REPRODUCE skeptic - partial win p3 (DominicaCodas.csv), sperm-whale-next-coda-beyond-first-order

context: subagent (Claude Code Agent tool, reproduce type)

Scope: the claim package only (CLAIM.md, REPRODUCE.md, PREREG.md, PREREG.v2.md, baseline/, code/, data/, result/).
All paths below are relative to the claim folder. My own work is in ../panel_work/reproduce/ (scripts/, out/, and the
fetched data in its own directory fetched/). All Python was run with the run's venv interpreter in isolated mode
(-I), single-threaded, one job at a time, with the data path given as an argument. Nothing was installed, nothing was
unpickled, and no outward action was taken. No credential was requested or handled.

## 1. Data

- One plain GET of the pinned raw URL (commit 7228c8e...), with a V3R1T4S User-Agent and a 60 s timeout:
  HTTP 200, 747,518 bytes, fetched 2026-11-19T10:28:23Z.
- sha256 of the fetched file = 53dd44fbfb0040da93656aa44883954f3abe18dd6539e90c625af86a96db6b45, the same as
  data/DominicaCodas.csv and the hash in CLAIM.md and PREREG.md. **PASS**

## 2. My independent checker (written from the definition before I read code/)

Definition implemented (bank p3, quoted in CLAIM.md): "tokens are CodaType; each Date is first rewritten with every
hyphen replaced by a slash ...; streams are rows sharing that rewritten Date and Unit, ordered by codaNUM2018; folds
are the distinct rewritten Date strings sorted as text, with the i-th in fold i mod 5", plus the main criterion's
"Scored: every coda with at least 2 earlier codas in its stream" and "a bigram over tokens with additive smoothing
chosen from 0.01, 0.03, 0.1, 0.3 and 1 by inner cross-validation on the training folds".

The checker is ../panel_work/reproduce/scripts/checker.py. It uses the stdlib csv module (utf-8-sig) and numpy only,
not pandas and not dompipe. It does the following:
- vocabulary = the sorted distinct CodaType strings;
- Date: '-' replaced by '/';
- stream = rewritten Date + '|' + Unit, sorted by integer codaNUM2018 with ties in file order;
- folds = the sorted distinct rewritten Dates, i-th date in fold i mod 5;
- scored = positions t >= 2;
- bigram reference: P(b|a) = (n(a,b)+alpha)/(n(a)+35 alpha), with counts over all consecutive pairs of the training
  streams. alpha is chosen by leave-one-training-fold-out inner CV (total held-out log-loss on the scored positions,
  ties to the first grid value), then refit on all 4 training folds;
- all cross-entropies come from the saved per-position vectors, and the bootstrap is my own loop.

Output: ../panel_work/reproduce/out/checker_stdout.txt and checker_out.json.

| check | my value | claim / saved | result |
|---|---|---|---|
| rows | 8719 | 8,719 | PASS |
| distinct CodaType (vocab) | 35, identical order to result/p3_vocab.csv | 35 | PASS |
| raw Dates -> rewritten Dates | 101 -> 97 (four days merged) | 97 | PASS |
| dates per fold | [20, 20, 19, 19, 19] | 20/20/19/19/19 | PASS |
| result/p3_folds.csv (order, dates, folds) | identical (97 rows) | - | PASS |
| streams | 109 (codaNUM2018 unique: 8719 of 8719, no ties) | 109 | PASS |
| rows per fold | [1367, 1964, 2041, 1612, 1735] | dev folds 0, 3 = 1,367, 1,612 | PASS |
| scored positions | 8501; per fold [1327, 1914, 2003, 1568, 1689] | 8,501; same per fold | PASS |
| (stream,pos) keys of both p3_probs files | equal to my scored set, no duplicates | - | PASS |
| fold label and y_token in every row | match mine in all 8501 rows (both files) | - | PASS |
| bigram alpha per fold (inner CV) | 0.3 in all 5 folds | 0.3 in all 5 | PASS |
| my bigram vectors vs result/p3_probs_bigram.csv | max abs diff 0.0 (bit-identical) | - | PASS |

Note: codaNUM2018 is unique and already ascending in file order. Sorting it as text would reorder 3 streams, so the
numeric order is the only order used here, by me and by the author.

### Vector validity (saved per-position files)

| file | rows | min entry | entries <= 0 | non-finite | max abs(sum - 1) | result |
|---|---|---|---|---|---|---|
| result/p3_probs_bigram.csv | 8501 | 9.525e-05 | 0 | 0 | 2.22e-16 | PASS |
| result/p3_probs_full.csv | 8501 | 3.919e-05 | 0 | 0 | 6.66e-16 | PASS |

### Cross-entropies (bits per coda, -log2 p[y] recomputed from the saved vectors, with my own token for y)

| fold | n | my bigram | saved bigram | full (from saved vectors) |
|---|---|---|---|---|
| 0 | 1327 | 1.5076728991683102 | 1.5076728991683102 | 1.3644132446381125 |
| 1 | 1914 | 1.7059448503082546 | 1.7059448503082546 | 1.593230309749782 |
| 2 | 2003 | 1.8709033775374908 | 1.8709033775374908 | 1.7213395987276943 |
| 3 | 1568 | 1.848437756811054 | 1.848437756811054 | 1.6977884796549743 |
| 4 | 1689 | 1.5940547568399608 | 1.5940547568399608 | 1.505193740527712 |
| pooled | 8501 | 1.7179142139602834 | 1.7179142139602834 | 1.589491467897628 |

- Gain (my bigram minus full) = 0.12842274606265539 bits per coda, which is >= 0.05. **PASS** (claim: 0.1284)
- Diagnostic on folds 1, 2, 4: n = 5606, gain 0.1186939236775468 (claim: +0.1187 on 5,606). PASS

### Date-group bootstrap

- Fresh seed 58213467, 10,000 resamples over the 96 rewritten-Date groups that own at least one scored position.
  The statistic is sum of gains / number of positions. 95% percentile interval [0.08893699415313196,
  0.16334850867599818]. The fraction of resamples <= 0 is 0.0. The lower bound is > 0. **PASS**
- With the author's seed 20261119, my independent loop gives [0.08793142691897533, 0.16299376323756604]. The claim
  has [0.08793142691897537, 0.16299376323756598]; the difference is at summation-order rounding level. PASS

## 3. Frozen pipeline rerun (REPRODUCE.md step 2)

I copied code/ into my work folder, so nothing was written into the claim folder. The sha256 of code/dompipe.py is
63f94f42..., equal to the PREREG freeze hash. The sha256 of code/score_p3.py is 1c4bbd2f..., which differs from the
PREREG hash 303337.... That is consistent with the harness-only fix disclosed in PREREG.v2.md; I cannot see the
pre-fix file.

Command: `score_p3.py <fetched csv> <my out/rerun>`. Exit 0, about 200 s. sha256 of rerun vs saved:

| file | result |
|---|---|
| p3_probs_full.csv | IDENTICAL (e0bb563b...) |
| p3_probs_bigram.csv | IDENTICAL (140f905c...) |
| p3_summary.json | IDENTICAL (3aff05e8...) |
| p3_folds.csv | IDENTICAL (6c410700...) |
| p3_vocab.csv | IDENTICAL (1ac39697...) |
| stdout vs result/run_output.txt | identical apart from the elapsed-seconds stamps |

No non-determinism was observed. **PASS**

## 4. My own leakage test against the author's fitted model

The script is ../panel_work/reproduce/scripts/leak_check.py, a separate harness that does not use score_p3.py. It
imports the frozen dompipe and fits each fold with run_fold_full. Output: ../panel_work/reproduce/out/leak_check.json.

- T1, train-only: every field (CodaType token, IDN, nClicks, Duration) of every coda of the held-out fold was replaced
  with random values, then the fold was refit. In all 5 folds the bigram alpha and table, lambda, theta of `full` and
  the count tables are bit-identical. **PASS**
- T2: only the predicted coda was altered. Its token became another token, its IDN became the IDN of coda t-1 (a value
  chosen to trigger an IDN-reading bug), and nClicks and Duration were shifted. `full` or bigram changed at 0 of 8501
  positions, max abs diff 0.0. **PASS**
- T3: the predicted coda and all later codas were altered, with IDN switched to the integer 0 (a type change). The
  prediction changed at 0 of 8501 positions. **PASS**
- T4: the single-position prediction on the untouched stream equals the saved result/p3_probs_full.csv row exactly
  (0 of 8501 mismatches). **PASS**
- Positive control: a deliberately leaky predictor (the same fitted `full` model fed rows [:t+1], so it reads coda t)
  is flagged under T2 at 8501 of 8501 positions. The author's built-in control only checks that the perturbation
  changed the token. This one actually exercises a leaky reader. **PASS**
- The other CSV columns (ICI1-9, Clan, UnitNum) are never loaded into the stream arrays: dompipe.load keeps only FIELDS
  = tok, IDN, nClicks, Duration. Date, Unit and codaNUM2018 only define stream membership and order.

## 5. Code read (code/dompipe.py)

- `feats(hist(s, t), ...)` receives rows [:t] only. It reads tok[t-1] (bigram, same1), tok[t-2] (skip, same2, echo),
  the run length, the repeat rate and the cache over all earlier codas, and the IDN of earlier codas. It never sees
  index t.
- Functional check (U2): altering only coda t-2's token changes `full` at 8501 of 8501 positions and the
  previous-coda-only `one` at 0 of 8501.
- The fitted weights on the beyond-first-order features are non-zero in every fold. For example, in fold 0: skip
  0.2578, cache 0.2583, same2 0.0295, same_whale_last 0.0849, echo2_if_switch -0.0929.
- So the model uses two or more previous codas. **PASS**
- Training uses the training folds only: Tables, ref_fit and the fit rows are built from training-fold streams, and T1
  confirms this. **PASS**

## 6. Observations (not failures)

- **IDN quirk.** In the loaded data, all 8,719 IDN values are Python str, 5,705 of them '0', and none equal the integer
  0. So the `idn != 0` guards are always true, and '0' acts as one more whale label. This confirms the disclosure in
  PREREG.v2.md. It is a feature-definition quirk, not leakage.
- **Inner CV for lambda.** The cross-fitted tables of the inner-training rows include the inner-validation fold. This
  can only affect which lambda is chosen inside the training folds (0.01 almost everywhere). It cannot affect the
  outer held-out evaluation; T1 shows the fitted model does not depend on the held-out fold.
- **Diagnostics come from the author's run.** The pooled `one`/`rep`/`local` diagnostics (1.7121, 1.7005, 1.6150) and
  their intervals come from the author's pipeline. I reproduced them only through the bit-identical rerun, not with an
  independent model. On those numbers, 0.0855 of the 0.1284-bit gain is the order-free stream cache (rep minus local),
  as CLAIM.md says. Whether that meets the spirit of "beyond first order" is for the CRITERION lens.
- **Null controls N3 are not covered.** PREREG.md says a p3 claim needs its real gain above all 400 null controls, and
  CLAIM.md marks this PENDING (null/ is empty). It is not part of the claim sentence, so this verdict does not cover
  it. The claim must not be treated as complete until null/ exists and has been checked.

## Verdict

Every check passes:
- the data checksum;
- independent regeneration of the streams, folds, scored set and vocabulary;
- the independently fitted smoothed bigram, bit-identical to the saved one;
- vector validity in both files;
- the recomputed cross-entropies and the 0.12842-bit gain;
- the fresh-seed Date bootstrap [0.0889, 0.1633], which excludes 0;
- a bit-identical frozen rerun;
- the independent leakage test with a working positive control;
- the code read.

The claimed p3 numbers reproduce exactly. I found no mismatch, no missing claimed object and no non-determinism. The
pending N3 null gate is outside this verdict's scope (section 6).

pass: true
