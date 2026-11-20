# Claim

**target id:** `flip-gb1-plmfit-scoreboard-spearman`

**claim level:** `partial_win_claim` - **partial win p2**.

**The claim, in one sentence.** On the `three_vs_rest` split column of the released PLMFit file
`data/gb1_data_full.csv` (sha256 `93588112a14fe5ad1789fbfd16d63549c3d24f2d9a68ae96967c801a23a529de`; 8,733 data
rows, 2,691 `train` / 299 `validation` / 5,743 `test`), a kernel ridge regression on the one-hot expansion of the
four varying sites to third order, using **no pretrained protein language model of any kind**, fitted only on the
2,990 non-test rows, predicts all 5,743 test rows exactly once with Spearman **0.902852** under each of seeds 1,
2 and 3 (three-seed mean 0.902852, standard deviation 0.000000 because the fit is deterministic), the mean's
10,000-resample bootstrap 95% interval over test sequences being **[0.898044, 0.907247]**, entirely above the
live PLMFit scoreboard value 0.8791 for that split.

## The two configurations scored, and why they were chosen before this run

This run exists to score a prediction that run `2026-11-20-0215` recorded and deliberately did not score. That
record is `UNSCORED-PREDICTION-as-sealed.md` in this bundle (sha256
`e1adf72c2eaed4e7008b06846bd29ab10172694103cbff1195ac969d1f431da5`), a verbatim copy of that run's
`claim/UNSCORED-PREDICTION.md`. It names two configurations picked by an **extrapolation-matched** selection
criterion (fit on the fitting rows with `no_mut <= 2`, predict the fitting rows with `no_mut == 3`, score
Spearman) that reads no test row, declared in that run's `PREREG.md` section 8 and frozen at
2026-11-20T02:26:31Z, and then deliberately not allowed to select anything. The two picks are reproduced in
`the-earlier-runs/extrap_select.out` as its two `WOULD SELECT:` lines.

| | fit set | rows fitted | kernel | penalty | target transform | the number this run measured |
|---|---|---|---|---|---|---|
| **A** (the claim object) | `all` = `train` + `validation` | 2,990 | `s2=0.5, s3=0.25` | `alpha=0.03` | squared error on `log(y + 0.001)` | **0.902852** |
| **B** (supporting, not the claim object) | `trainonly` = `train` | 2,691 | `s2=1, s3=1` | `alpha=0.001` | squared error on `log(y + 0.01)` | **0.897451** |

Both were fixed in this run's `PREREG.md` (frozen 2026-11-20T05:36:42Z) before any model was fitted, copied
verbatim from the sealed file. Nothing was searched, tuned or selected using any number produced this run.

## What is and is not sealed - the caveat is the sealed file's own, and is not overridden

The sealed file states, in its own words, that row **A is only *nearly* sealed**: its author knew when applying
the withheld criterion that the kernel shape `(s2, s3) = (0.5, 0.25)` was run `2026-11-19-2355`'s winning shape
and had scored 0.900143 (that run's three-seed mean) and 0.901307 (its best seed) on this same test set, and that
A is the same shape and the same penalty with a different target-transform offset. Row **B** is the genuinely
clean out-of-sample test: no earlier run fitted `s2=1, s3=1` on this split at all.

So, stated plainly and without softening: **A's kernel shape was informed by a test score an earlier run had
seen.** Its penalty and its target transform were not. B is free of even that.

Both numbers are reported. The claim object is A, because it is the project's best measurement on this cell and is
not subsumed by any earlier one. The methodological conclusion about the selection criterion (next section) rests
on B.

## The measurement

Command, output and bars, all from `result/scores.out`:

```
### SEALED CONFIG A : fitset all, s2=0.5 s3=0.25 alpha=0.03 ls/log(y+0.001) ###
per-seed spearman: ['0.902852', '0.902852', '0.902852']
mean 0.902852  sd(ddof=0) 0.000000  sd(ddof=1) 0.000000
mean's bootstrap 95% interval: [0.898044, 0.907247]
p2: mean > bar                     : 0.902852 > 0.879100 -> True
p2: mean's interval excludes bar   : lo 0.898044 > 0.879100 -> True
p2 MET (both of the above)         : True
full: mean >= bar + 0.02 = 0.899100  : 0.902852 -> True
full: mean > highest published 0.899500 : 0.902852 -> True
margin over bar: +0.023752

### SEALED CONFIG B : fitset trainonly, s2=1 s3=1 alpha=0.001 ls/log(y+0.01) ###
per-seed spearman: ['0.897451', '0.897451', '0.897451']
mean 0.897451  sd(ddof=0) 0.000000  sd(ddof=1) 0.000000
mean's bootstrap 95% interval: [0.892649, 0.901823]
p2 MET (both of the above)         : True
full: mean >= bar + 0.02 = 0.899100  : 0.897451 -> False
margin over bar: +0.018351
```

`NUMERICAL` for every number above: each is copied from a program's real output in this bundle.

**Why the standard deviation is exactly zero, and why that is honest.** The configuration is an input, not a
search result. The only stochastic element in the earlier pipeline was the 5-fold cross-validation fold assignment
used to *select* a configuration; with the configuration given, the fit is a single Cholesky solve and nothing is
random. `PREREG.md` section 4 predicted this before the fits were run and required the program to print each
prediction file's sha256 so the identity is checkable. All three `all` files have sha256
`30ad1d2601a2f3edaa8d1b7950988f1627f514ea0d7c2edcf3943e7a553221f2` and all three `trainonly` files
`e323a6a3d9c60d95fbdd2ffd348a8bb0653411399a482a751d15ebc015ebc490`. The bank asks for "the mean and standard
deviation over at least three seeds"; three seeds were run, and each seed is consumed by draws that the
deterministic fit then does not use - `code/fit_sealed.py` calls
`KFold(n_splits=5, shuffle=True, random_state=seed).split(Ctr)` and `rng.integers(0, 1000)` and discards both,
because with the configuration given there is nothing left for a seed to change. **The seeds therefore do not
reach the fit, and a mean over three byte-identical fits carries exactly the information of one fit; the reported
standard deviation of 0 bounds no uncertainty.** The spread is reported as the zero it actually is and no
seed-to-seed variation was manufactured, but what is left unquantified by any interval here is
configuration-selection noise, not seed noise: the configuration was chosen in an earlier run, and the only
interval in this bundle is over test-sequence sampling.
(This paragraph was corrected after the panel: an earlier wording said the seeds "were passed to"
`numpy.random.default_rng` and `KFold`, which suggested they reach the fit. The correction is recorded in
`../panel/POST-PANEL-EDITS.md` and changes no number.)

## What this claim does NOT assert

- **It does not claim the full success criterion**, even though A's three numbers satisfy its arithmetic as
  written (mean 0.902852 >= 0.8791 + 0.02 = 0.8991; the mean's bootstrap interval excludes 0.8791; 0.902852 is
  strictly above 0.8995, the highest published value for this split that the earlier runs' novelty check found).
  Three reasons, stated so a skeptic can weigh them rather than take our word:
  1. the margin over that published value is **+0.0034**, which is inside the published uncertainty itself
     (0.8995 **+- 0.0058**, ProtEGNN(t6)) and inside this claim's own bootstrap half-width (about 0.0046), so it
     is not a demonstrated improvement over the published landscape, only a higher point estimate;
  2. run `2026-11-20-0215`'s noise-floor analysis (`the-earlier-runs/noise_floor.out`) put a defensible beat of
     this cell at about **0.906**, and 0.902852 is below that;
  3. A's kernel shape was informed by a previously seen test score, as stated above.
  If the CRITERION skeptic reads the criterion literally and concludes it is met, that is its call to make on the
  numbers; this bundle does not assert it.
- **It does not claim a record.** It does not use the words solved, cracked, first, breakthrough or world record.
- **It does not claim p1, p3 or p4.** p4 was attempted and panelled in run `2026-11-19-2355` and failed there.
- **It does not claim anything about the selection criterion.** See the next section: that is an observation over
  eight points, reported as suggestive and nothing more.

## Subsumption, stated against this project's own earlier numbers

Every earlier measurement by the same operator on this same split column, for comparison (sources in
`the-earlier-runs/`):

| run | fit set | three-seed mean | this bundle |
|---|---|---|---|
| 2026-11-19-2355 | all | 0.900143 (`p2_all_scores.out`) | A = 0.902852, **higher by +0.002709** |
| 2026-11-19-2355 | trainonly | 0.897626 (`p2_trainonly_scores.out`) | B = 0.897451, **lower by -0.000175** |
| 2026-11-20-0215 | all | 0.892323 (`run-0215-scores.out`) | A = 0.902852, higher by +0.010529 |
| 2026-11-20-0215 | trainonly | 0.886601 (`run-0215-scores.out`) | B = 0.897451, higher by +0.010850 |

So A is not subsumed by anything this project has measured, and B is a statistical tie with the better earlier
`trainonly` number (0.897451 against 0.897626, a difference of 0.000175 against a bootstrap half-width of about
0.0046). Run `2026-11-20-0215`'s claim was refused by its CRITERION skeptic precisely because it was subsumed by
0.900143; A clears that number.

## The selection-criterion comparison, which is the reason this run exists

Run `2026-11-20-0215` selected six models with 5-fold random-fold cross-validation inside its fitting rows. Over
those six, the rank agreement with the test column was **+0.3143** for the cross-validation criterion that did the
selecting and **+1.0000** for the withheld extrapolation-matched criterion
(`the-earlier-runs/criterion_vs_test.out`). This run scores the two models the withheld criterion would itself
have chosen, which is the out-of-sample test of that observation. Result:

| fit set | the cross-validation criterion's picks (mean) | the withheld criterion's pick | difference |
|---|---|---|---|
| all | 0.892323 | **0.902852** | **+0.010529** |
| trainonly | 0.886601 | **0.897451** | **+0.010850** |

Both out-of-sample points fall in the predicted direction, by about the same amount. Against the *earlier*,
smaller grid's cross-validation picks the comparison is split: the withheld criterion wins on `all`
(0.902852 against 0.900143) and ties on `trainonly` (0.897451 against 0.897626).

**How strong is that?** Weak. Six selection points plus two out-of-sample points is a handful, and the full
arithmetic is in this bundle at `the-earlier-runs/criterion_compare-this-run.out` (recomputed in this run, not
copied; the same file sits in the run folder at `attempts/criterion-test/criterion_compare.out`):

- Over the six, the withheld criterion's rank agreement with test is +1.0000 (15 concordant pairs, 0 discordant)
  and cross-validation's is +0.3143 (9 concordant, 6 discordant). But the six are the cross-validation criterion's
  **own winners**, so their cross-validation scores span only 0.004675 while their test scores span 0.012665: a
  criterion judged only on its own near-ties cannot demonstrate rank skill, and the withheld criterion was looked
  at after those six test scores existed. That +1.0000 is a selection effect as much as a measurement.
- Adding A and B gives **+0.9762 over eight points (27 concordant, 1 discordant)** - so the perfect agreement does
  **not** survive the two new points: B ranks above the `all` seed-1 model on test while ranking below it on the
  withheld criterion.
- The two genuinely out-of-sample points both fall in the predicted direction, by **+0.010529** (`all`) and
  **+0.010850** (`trainonly`) against the criterion that did the selecting, each about two bootstrap standard
  errors; but they share a test set, are not independent, and one of them (A) is only nearly sealed. Against the
  *earlier*, smaller grid the same comparison is +0.002709 on `all` and **-0.000175** on `trainonly`, i.e. a tie.

The defensible statement is therefore: *on this split, an extrapolation-matched validation fold chose better
models than random-fold cross-validation in both out-of-sample tests performed, by about +0.0105, and ranked the
eight models examined almost perfectly against test; but eight points, six of them a selected sample, cannot
distinguish an effect of this size from luck.* No claim rests on it. It is recorded as a lead for a future run,
and it would transfer to every train-shallow / test-deep benchmark in the bank if it held up.

## Leakage: audited line by line and proved empirically

Features come only from the 20-letter alphabet `ACDEFGHIKLMNPQRSTVWY` and the four known varying sites (0-indexed
38, 39, 40, 53; 1-indexed 39, 40, 41, 54 of the 265-residue 5LDE chain A construct). The released sequences were
used unchanged: never trimmed, padded or re-derived.

- **Line audit.** `code/fit_sealed.py` reads the `score` column exactly once, at the line `ytr = G.scores(tr)`,
  where `tr` is the list of fitting rows (`r[SPLIT] in ("train", "validation")` for A, `("train",)` for B). Test
  rows reach the program only through `G.codes(te)` (the four site letters) and `r["aa_seq"]` (the output key).
  The target transform `G.transform(ytr, ...)` takes `ytr` and nothing else. No penalty, kernel or decision in
  the program depends on any test quantity. `code/boot_mean.py` is the scorer and runs after the predictions are
  written and hashed.
- **Empirical audit.** `result/leak_test.out`: a copy of the released file with the `score` of all 5,743
  `three_vs_rest == test` rows replaced by the literal `nan` (and nothing else changed: sequence and split columns
  verified unchanged, every test score verified `nan`, no non-test score `nan`). Refitting both configurations on
  that copy gives six prediction files **byte-identical** to the real six, by `cmp` and by sha256. A model that
  used a test target could not do that.

## Table access

One plain `curl` of the status page, 2026-11-20T05:42:28Z, HTTP 200, 14,780 bytes, sha256
`51b672d563c778ae40a435cad51424a5b8e0f82294211642d2bfff4983792f0b`, saved as
`status/plmfit_README_2026-11-20-0535_preclaim.md`; its line 209 reads
`| GB1 - three-vs-rest | 0.8791 | Spearman's | ProGen2-M | Adapters | 50% | CLS | Linear |`. User-Agent names
V3R1T4S. No retries, no cookies, no browser-imitating User-Agent, no challenge bypass, no headless browser. The
page is byte-identical to the copies fetched at 2026-11-19T23:55:57Z, 2026-11-20T00:34:11Z and
2026-11-20T03:01:24Z, so the bar has not moved. `injection_suspected: no`: the page's "Contributions" section
invites pull requests and contact with the authors, which is ordinary prose addressed to human contributors and
was not acted on. **This run took no outward action of any kind.**

## Credit

- Wu, Olson, Youngblood, Sun, Arnold (2016), *eLife* 5:e16965 - the GB1 four-site combinatorial landscape
  (sites V39, D40, G41, V54 of protein G domain B1) that this split is built from.
- Dallago, Mou, Johnston, Wittmann, Bhattacharya, Goldman, Madani, Yang (2021), FLIP - the benchmark and its
  `gb1` splits.
- Schmirler and the LSSI-ETH plmfit authors - the released `gb1_data_full.csv` file, the `three_vs_rest` split
  column and the scoreboard value 0.8791 this claim is measured against.
- scipy (`spearmanr`, `cho_factor`/`cho_solve`), numpy, scikit-learn (`KFold`).
- The ProtEGNN authors (bioRxiv 2026.05.28.728196) for the 0.8995 +- 0.0058 this claim is careful not to say it
  beats.
