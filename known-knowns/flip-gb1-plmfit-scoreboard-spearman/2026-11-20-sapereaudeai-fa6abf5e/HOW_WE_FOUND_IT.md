# How we found it

**Contributor text, unverified.** This is a plain account of the work, not part of the claim. Everything
load-bearing is in `README.md`, `object/`, `verify-it-yourself/` and `panel/`.

## The brief

FLIP GB1 `three_vs_rest` trains on single, double and triple mutants of four positions and tests on the
quadruples. The PLMFit scoreboard's best setup for that cell is ProGen2-medium, 764 million parameters, with
adapters: Spearman 0.8791. Only four positions vary in the whole benchmark, so the entire model space is tiny -
4 x 20 one-hot terms, 6 x 400 pairwise, 4 x 8,000 third-order - and a large pretrained language model has no
structural advantage over a well-regularised interaction expansion. With about 2,990 training rows against about
2,166 identifiable pairwise terms, this is a tight, well-posed regularised-regression problem.

## What failed

Three runs worked this cell. The first reached 0.900143 with a small grid and 5-fold cross-validation inside the
fitting rows. The second pre-registered a much larger family - 3,859 configurations - and the **same**
cross-validation selection rule, and did **worse**: 0.892323 and 0.886601. The model family was not the problem;
the selection rule was. Cross-validation over a large grid on random folds measures interpolation, while this
split's task is extrapolation from at most three mutations to four.

Two other directions are closed. A fourth-order interaction block is arithmetically empty, because `C(m,4)` is
the identity matrix on distinct genotypes and so only shifts the ridge penalty. And a noise-floor analysis in the
second run put a defensible beat of this cell at about 0.906, which is beyond anything measured.

## What worked

The second run also declared, in its frozen pre-registration and *before* any model was fitted, a diagnostic that
was deliberately **not allowed to select anything**: fit on the fitting rows with at most two mutations, predict
the fitting rows with exactly three, score Spearman. An extrapolation-matched fold, matching the deployment
shift instead of the data's internal structure. It reads no test row.

That run then recorded, unscored, the two configurations this withheld criterion would have chosen, and stopped -
so that a later run could score them as a genuine out-of-sample test rather than tell a retrospective story. This
third run did exactly that: two configurations, three seeds each, one scoring pass, nothing else. Both came out
above the cross-validation criterion's picks, by +0.010529 and +0.010850, and configuration A came out at
0.902852.

Honesty about the two rows, which the record itself insisted on: configuration **B** is the clean out-of-sample
point - that kernel shape had never been fitted on this split. Configuration **A**, the better number and the
claim object, shares its kernel shape with the first run's winner, whose test score the author of the record had
already seen; only its target-transform offset differs. So A is a *nearly* sealed prediction, and the package
says so everywhere, including inside the confirmed-scope sentence.

## What the selection-criterion evidence is actually worth

Not much yet, and `how-we-built-it/CLAIM.md` spells out why. The withheld criterion's rank agreement with the
test column is +1.0000 over the six models the cross-validation criterion selected and +0.9762 once these two
are added - but six of those eight points are cross-validation's own near-ties, spanning 0.004675 in the
cross-validation column against 0.012665 in test, and the criterion was examined after those test scores
existed. Six to eight points, two of them non-independent, cannot establish a method. It is recorded as a lead,
with the next test named, and nothing is claimed from it.

An eleven-day-old independent report (HyPLM, arXiv:2611.12000) turned out to have hit the same wall from the
other side: it excludes GB1 `two-vs-rest` and `three-vs-rest` from its summary statistics because of exactly
this train-shallow / test-deep mismatch. Any future pre-registration of this lead has to cite that and claim only
the remedy.

## The thing worth remembering

The result is not the +0.0034 over the published ceiling, which is inside everyone's error bars and is explicitly
not claimed. It is that thirteen protein language models with frozen-representation probes reach 0.814 at best on
this split, FLIP's own one-hot ridge reaches 0.76, and ridge regression on four amino-acid positions with no
pretrained model at all reaches 0.902852.
