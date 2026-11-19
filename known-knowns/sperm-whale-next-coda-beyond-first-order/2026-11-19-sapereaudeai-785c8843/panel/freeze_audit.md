# Freeze-timeline audit (honesty gate, main session, 2026-11-19)

The CRITERION skeptic passed the full criterion but made its pass conditional, in part, on condition (b):
the freeze must be confirmed to precede every held-out score. It could not check this itself, because the
development outputs sit outside the claim package it was allowed to read. This file is that check.

PREREG.md line 3: `frozen: 2026-11-19T09:55:11Z (date -u), before any held-out score on bank folds 0, 1 or 3
of the dialogues file or [the Dominica holdout folds]`.

## Method

Listed every file in the run folder with an mtime before the freeze instant (09:55:11Z = 10:55:11 local,
this machine runs UTC+1), excluding the fetched data and the cache. Then read all six pre-freeze output
files in full and checked, for each, whether it contains a score on an evaluation fold.

## Pre-freeze files

Six output files existed before the freeze, plus code and the two scouting notes:

| file | what it contains | a held-out score? |
|---|---|---|
| attempts/evaluator/structure_output.txt | dataset shape, column dtypes, REC sizes, tie counts, scored-coda counts per fold, Dominica stream counts | No. Descriptive statistics of the inputs only; no model is fitted and no loss is computed. |
| attempts/evaluator/smoke_dev_output.txt | leakage-harness smoke test on 269 positions, single-vs-batch agreement | No. Harness self-tests, not scores. |
| attempts/turn-taking/dev_output_round1.txt | p4 model comparison, "dev scored 907" | No. 907 is exactly folds 2+4. |
| attempts/sequence-model/dev_output_round1.txt | content models over 4 inner sub-folds of the dev set | No. Inner split of the dev folds. |
| attempts/sequence-model/dev_output_round2.txt | the same plus the `local` reference | No. Same dev set. |
| attempts/dominica/dev_output_round1.txt | p3 models, "dev folds (two smallest by rows): (0, 3)", "dev scored 2895" | No. Dev folds only. |

## Positive evidence, not just attestation

1. **The dev row counts match the dev folds exactly.** structure_output.txt records scored codas per fold as
   {0: 514, 1: 1305, 2: 508, 3: 692, 4: 399}. The p4 dev output reports `dev scored 907`, and 508 + 399 = 907,
   i.e. folds 2 and 4 and nothing else. The Dominica dev output reports `dev scored 2895` against the final
   8,501, and names its dev folds (0, 3) in the file.
2. **Every pre-freeze number differs from the corresponding final number.** If a held-out evaluation score had
   been computed before the freeze, the dev file would carry that value. It does not:

   | quantity | pre-freeze dev | final held-out |
   |---|---|---|
   | content R1 | 2.9854 | 2.7802 |
   | content twin | 2.6724 | 2.6549 |
   | content full | 2.1065 | 2.1238 |
   | content full vs twin | +0.5659 | +0.5311 |
   | p4 full | 0.7828 | 0.7631 |
   | p3 bigram | 1.8773 | 1.7179 |
   | p3 full | 1.6216 | 1.5895 |

   The model is *worse* on the evaluation folds than it was on the dev folds in every case, which is the
   expected direction when a design is fixed on one subset and then scored on unseen data. A leaked held-out
   score would not show that pattern.
3. **The code hashes in PREREG.md match the frozen code files** (checked independently by CRITERION, its
   item 13).

## Limit of this audit

mtimes show what exists now, not what was deleted or overwritten. I cannot prove by filesystem evidence alone
that no pre-freeze held-out score was computed and then removed. What I can say is that nothing on disk
contradicts the freeze, that the dev counts match the dev folds exactly, and that all seven comparable
numbers moved in the direction that genuine held-out scoring produces.

A residual caveat belongs in any filing, and is independent of this audit: dev folds 2 and 4 are included in
the pooled 5-fold score, because the bank specifies a pooled 5-fold score. On the three folds never used in
development (0, 1, 3) the result is materially the same: +0.5212 vs twin, +0.6634 vs R1.

**Condition (b): satisfied, to the extent the filesystem can show it, with the caveat above stated.**
