# REPRODUCE skeptic verdict - flip-gb1-plmfit-scoreboard-spearman, partial win p2

context: subagent

Everything in `CLAIM.md` that I was asked to check reproduces, to the last printed decimal, from code I
wrote myself before opening the author's scorer or kernel module. Below, every number is pasted command
output. File names are relative to `claim/`.

## 1. My own scorer, written from the criterion before reading `code/boot_mean.py`

Criterion quoted from `README.md`:

> The Spearman correlation, recomputed by the skeptic with `scipy.stats.spearmanr` against the split's
> target/score column, must be strictly higher (direction: max) by at least 0.02 than the value listed for
> that split on the PLMFit scoreboard [...] Report the mean and standard deviation over at least three
> seeds, with a bootstrap 95% interval over test sequences that excludes the published bar.

and p2:

> p2. A three-seed mean strictly above the `three_vs_rest` scoreboard value of 0.8791, with a bootstrap 95%
> interval that excludes it, from a reproducible pipeline whose split file and seeds are named.

My scorer joins each prediction file to the released file's own `score` column on `aa_seq` over the rows
whose `three_vs_rest` is `test`, in its own key order (sorted, not file order), and calls
`scipy.stats.spearmanr`. Config A:

```
released file      : claim/data/gb1_data_full.csv
sha256             : 93588112a14fe5ad1789fbfd16d63549c3d24f2d9a68ae96967c801a23a529de
data rows          : 8733  split counts: {'train': 2691, 'validation': 299, 'test': 5743}
test rows (truth)  : 5743

pred file          : pred_configA_all_seed1.csv
  sha256           : 30ad1d2601a2f3edaa8d1b7950988f1627f514ea0d7c2edcf3943e7a553221f2
  rows (unique)    : 5743  duplicate keys: 0
  missing test rows: 0  extra non-test rows: 0
  SPEARMAN         : 0.902852
[seed2 and seed3: same sha256, same coverage, SPEARMAN 0.902852 each]

per-seed spearman  : ['0.902852', '0.902852', '0.902852']
mean               : 0.902852
sd(ddof=0)         : 0.000000
sd(ddof=1)         : 0.000000
bootstrap 95% CI of mean: [0.898044, 0.907247]
mean > bar  0.8791        : 0.902852 -> True
CI lo > bar 0.8791        : 0.898044 -> True
p2 MET                  : True
margin over bar         : +0.023752
full gate mean >= 0.8991 : True
```

Config B:

```
pred file          : pred_configB_trainonly_seed1.csv
  sha256           : e323a6a3d9c60d95fbdd2ffd348a8bb0653411399a482a751d15ebc015ebc490
  rows (unique)    : 5743  duplicate keys: 0
  missing test rows: 0  extra non-test rows: 0
  SPEARMAN         : 0.897451
[seed2 and seed3: same sha256, same coverage, SPEARMAN 0.897451 each]

per-seed spearman  : ['0.897451', '0.897451', '0.897451']
mean               : 0.897451
sd(ddof=0)         : 0.000000
bootstrap 95% CI of mean: [0.892649, 0.901823]
p2 MET                  : True
margin over bar         : +0.018351
full gate mean >= 0.8991 : False
```

Claimed 0.902852 / 0.897451 and `[0.898044, 0.907247]` / `[0.892649, 0.901823]`: **exact match on all six
files and all four interval endpoints.** Not a sample - all 5,743 test rows, all six files.

## 2. The bootstrap, and why my percentiles matched exactly

My independent bootstrap (10,000 resamples, `numpy.random.default_rng(0)`, each resample scored under all
three seeds and averaged) reproduced both intervals to 6 dp. That exactness is explained, not lucky: the
released file's test rows are already in sorted `aa_seq` order, so my key order coincided with the author's
file order and the resample index streams coincide.

```
test rows in released file are already in sorted aa_seq order: True
file order, rng(0)       CI [0.898044, 0.907247]  lo-bar=+0.018944  lo>0.8791: True
shuffled order, rng(0)   CI [0.898077, 0.907213]  lo-bar=+0.018977  lo>0.8791: True
file order, rng(12345)   CI [0.898141, 0.907251]  lo-bar=+0.019041  lo>0.8791: True
```

So the published interval is not an artefact of a lucky ordering: under a shuffled row order or a different
bootstrap seed the endpoints move by at most about 1e-4, and the lower end stays about 0.019 above the bar.
The conclusion "interval entirely above 0.8791" is unaffected.

## 3. Independent rebuild from the model spec

I built my own sparse one-hot design (4x20 singles, 6x400 pairs scaled by s2, 4x8000 triples scaled by s3;
0-indexed sites 38, 39, 40, 53; 34,480 columns) and fitted `log(y + c)` two ways from that matrix: the
asked-for `sklearn.linear_model.Ridge(alpha, fit_intercept=True)` primal, and an exact Cholesky closed form.

```
=== REBUILD CONFIG A ===
fitset all: 2990 fitting rows, 5743 test rows
params : s2=0.5 s3=0.25 alpha=0.03 c=0.001
kernel identity max |X X^T - (m + s2^2 C(m,2) + s3^2 C(m,3))| over all 2990^2 pairs: 0.000e+00
SPEARMAN uncentred closed form (my design): 0.902973
SPEARMAN centred  closed form (my design): 0.902852
SPEARMAN sklearn Ridge sparse_cg          : 0.902852
max |pred_centred - pred_sklearn|         : 8.607e-12
vs released file pred_configA_all_seed1.csv
  max |centred closed form - author|  : 4.951e-09
  max |sklearn Ridge      - author|   : 4.951e-09
  spearman(centred, author)           : 1.000000000
  author file SPEARMAN vs score       : 0.902852

=== REBUILD CONFIG B ===
fitset trainonly: 2691 fitting rows, 5743 test rows
params : s2=1 s3=1 alpha=0.001 c=0.01
kernel identity max |X X^T - (m + s2^2 C(m,2) + s3^2 C(m,3))| over all 2691^2 pairs: 0.000e+00
SPEARMAN uncentred closed form (my design): 0.897216
SPEARMAN centred  closed form (my design): 0.897451
SPEARMAN sklearn Ridge sparse_cg          : 0.897451
max |pred_centred - pred_sklearn|         : 8.613e-12
vs released file pred_configB_trainonly_seed1.csv
  max |centred closed form - author|  : 4.997e-10
  max |sklearn Ridge      - author|   : 5.003e-10
  spearman(centred, author)           : 1.000000000
  author file SPEARMAN vs score       : 0.897451
```

Three things worth stating plainly.

- The author's kernel identity `K(i,j) = m + s2^2*C(m,2) + s3^2*C(m,3)` is **not** a spot check here: I
  computed `X X^T` from my own explicit design and compared it to the formula for **all** 2990^2 and 2691^2
  fitting-row pairs. Maximum absolute discrepancy 0.000e+00 in both configurations.
- The primal `Ridge(fit_intercept=True)` fit reproduces the claimed Spearman **exactly** (0.902852,
  0.897451), and agrees with the released predictions to 5e-9 (A) and 5e-10 (B) in prediction value, which
  is the 10-significant-digit rounding of the released CSV. Full rebuild, not a fallback spot check.
- A detail the bundle gets right and a careless replicator would get wrong: the number depends on the
  intercept convention. Penalising the raw features and centring only `y` gives 0.902973 / 0.897216 - near
  but not equal. `fit_intercept=True` (equivalently the author's double-centred Gram) is the convention
  stated in `REPRODUCE.md` section 5, and that is the one that gives the claimed numbers.

## 4. Determinism, coverage, and whether a zero spread is honest

Coverage: each of the six files carries each of the 5,743 test sequences exactly once, 0 duplicates, 0
extras, 0 missing (section 1 above). Byte identity within each configuration, and the two configurations
differing from each other:

```
A: all three byte-identical
B: all three byte-identical
A and B differ, as they must
30ad1d2601a2f3edaa8d1b7950988f1627f514ea0d7c2edcf3943e7a553221f2 *result/pred_configA_all_seed1.csv
30ad1d2601a2f3edaa8d1b7950988f1627f514ea0d7c2edcf3943e7a553221f2 *result/pred_configA_all_seed2.csv
30ad1d2601a2f3edaa8d1b7950988f1627f514ea0d7c2edcf3943e7a553221f2 *result/pred_configA_all_seed3.csv
e323a6a3d9c60d95fbdd2ffd348a8bb0653411399a482a751d15ebc015ebc490 *result/pred_configB_trainonly_seed1.csv
e323a6a3d9c60d95fbdd2ffd348a8bb0653411399a482a751d15ebc015ebc490 *result/pred_configB_trainonly_seed2.csv
e323a6a3d9c60d95fbdd2ffd348a8bb0653411399a482a751d15ebc015ebc490 *result/pred_configB_trainonly_seed3.csv
```

Both sha256s are the two the claim states. I also re-ran `code/fit_sealed.py` myself, in my own scratch
directory, and compared bytes against the bundle:

```
configA_all_seed1  BYTE-IDENTICAL to bundle
configA_all_seed2  BYTE-IDENTICAL to bundle
configA_all_seed3  BYTE-IDENTICAL to bundle
configB_trainonly_seed1  BYTE-IDENTICAL to bundle
configB_trainonly_seed2  BYTE-IDENTICAL to bundle
configB_trainonly_seed3  BYTE-IDENTICAL to bundle
```

So the released predictions really are what the released code produces. No non-determinism anywhere.

**Is reporting sd = 0.000000 honest?** Yes as a statement of fact, with one caveat the panel should weigh.
I read `code/fit_sealed.py` lines 70-83: the seed is consumed by `np.random.default_rng(seed)` and
`KFold(shuffle=True, random_state=seed)` and then nothing downstream uses either stream, because the
configuration is a literal rather than a search result. The fit is a single Cholesky solve. So the zero is
real, it was pre-registered, and the claim says all of this in the open rather than manufacturing jitter -
which is the honest way to handle it. The caveat: the "at least three seeds" requirement is therefore not
exercised in any informative sense. Three identical runs measure nothing, and a consequence worth naming is
that the "mean's bootstrap interval" is mathematically identical to a single-file bootstrap interval - the
seed averaging is a no-op. Further, the earlier run that *did* let seeds select the configuration reported
`mean 0.892323 sd(ddof=0) 0.003340` (`the-earlier-runs/run-0215-scores.out` line 24), so the selection
variance that the seeds used to capture is of order 0.003-0.004 and has been removed by sealing the
configuration rather than shown to be absent. That is legitimate for a sealed out-of-sample test, but it
means 0.902852 is one deterministic point, not a point with a measured run-to-run spread. The bundle does
not overclaim here; whether "mean and standard deviation over at least three seeds" is *satisfied* by three
identical runs is a reading question for CRITERION, not a reproduction failure. Nothing is hidden.

## 5. Leakage, re-run by me and audited line by line

I wrote my own NaN copy with my own code (not `code/make_nan_copy.py`) and refitted with my own ridge code:

```
my NaN copy: test scores replaced = 5743  sha256 = c50240964016608e53869bee05e7c3071a6734cb52c6fdfae70adf5469464497
  seq/split columns unchanged: True ; every test score nan: True ; no non-test score nan: True
config A: keys identical=True  max|pred_real - pred_NaN|=0.000e+00  (my own fitting code)
config B: keys identical=True  max|pred_real - pred_NaN|=0.000e+00  (my own fitting code)
```

My independently written copy lands on the **same sha256** the claim reports for its own copy
(`c50240964016608e53869bee05e7c3071a6734cb52c6fdfae70adf5469464497`), and my own fitting code gives bitwise
identical predictions with every test target destroyed.

Line audit of `code/fit_sealed.py`. The `score` column is read exactly once, at line 64 `ytr = G.scores(tr)`,
where `tr` is built at line 54 as `[r for r in rows if r[SPLIT] in want]` with `want` being
`("train","validation")` or `("train",)`. Test rows enter only through `G.codes(te)` (line 63, the four site
letters) and `r["aa_seq"]` (line 90, the output key). `G.transform(ytr, cfg["transform"])` at line 82 takes
`ytr` alone. `alpha`, `s2`, `s3` and the transform are literals in the `SEALED` dict at lines 31-36. The
Gram matrices come from `G.kernel(m_trtr, ...)` and `G.kernel(m_tetr, ...)`; `G.centre` is computed on the
fitting-fitting Gram only, and `G.centre_cross(Kte, rm, gm)` uses `rm`/`gm` from that fitting Gram plus
`K_ev_tr.mean(axis=1)`, which is a per-test-row mean over fitting columns - a row-local quantity, not a
statistic pooled over test rows. So no test target and no cross-test statistic reaches any feature,
transform, penalty or decision. I confirmed the non-pooling empirically, by predicting test rows alone
versus inside the full 5,743-row batch:

```
transductivity check: predict each test row ALONE vs in the 5743-row batch
max |solo - batch| over 8 random test rows: 8.682e-14
also: half-batch vs full-batch for first 50 rows: 1.776e-14
```

Float noise only: the model is not transductive. `code/boot_mean.py` is the scorer and touches test targets
only after the predictions exist and are hashed; its `--selftest` known-positive/known-negative is in
`result/score_selftest.out` and gives rho 1.000000 / -1.000000.

## 6. The two configurations scored are the two that were sealed

| source | A | B |
|---|---|---|
| `UNSCORED-PREDICTION-as-sealed.md` table | `s2=0.5 s3=0.25 alpha=0.03`, ls on `log(y+0.001)`, fitset all, extrapolation rho 0.797099 | `s2=1 s3=1 alpha=0.001`, ls on `log(y+0.01)`, fitset trainonly, rho 0.777742 |
| `the-earlier-runs/extrap_select.out` line 17 / line 30 | `WOULD SELECT: s2=0.5 s3=0.25 alpha=0.03 objective=ls transform=log0.001 (extrapolation rho 0.797099)` | `WOULD SELECT: s2=1 s3=1 alpha=0.001 objective=ls transform=log0.01 (extrapolation rho 0.777742)` |
| `code/fit_sealed.py` `SEALED` literals, lines 32-35 | `fitset="all", s2=0.5, s3=0.25, alpha=0.03, objective="ls", transform="log0.001", extrapolation_rho=0.797099` | `fitset="trainonly", s2=1.0, s3=1.0, alpha=0.001, objective="ls", transform="log0.01", extrapolation_rho=0.777742` |
| `result/fit_configA.json` / `fit_configB.json` `sealed` block | same | same |

All four agree in every field, including the extrapolation rho carried along as a tag. Nothing substituted,
no third configuration scored, no quiet change of fit set (A fitted 2,990 rows, B 2,691, both printed by the
program and both confirmed by my own row counts).

## 7. Arithmetic of every derived number in `CLAIM.md`

```
A margin  0.902852 - 0.8791 = +0.023752   (claim +0.023752)
B margin  0.897451 - 0.8791 = +0.018351   (claim +0.018351)
bar+0.02 = 0.899100 ; A>=it: True ; B>=it: False
2355 all  three-seed mean from its own per-seed lines: 0.900143 (claim 0.900143)
2355 tron three-seed mean from its own per-seed lines: 0.897626 (claim 0.897626)
A - 0.900143 = +0.002709   (claim +0.002709)
B - 0.897626 = -0.000175   (claim -0.000175)
A - 0.892323 = +0.010529   (claim +0.010529)
B - 0.886601 = +0.010850   (claim +0.010850)
A - 0.8995 (highest published) = +0.003352   (claim +0.0034)
A vs noise floor 0.906063: A below it = True
bootstrap half-widths: A 0.004602  B 0.004587  (claim 'about 0.0046')
```

The two earlier three-seed means the subsumption table quotes are not stated as means in their own files, so
I re-derived them from the per-seed `spearman:` lines: `p2_all_scores.out` lines 7, 17, 27 give 0.901307,
0.899561, 0.899561, mean 0.900143; `p2_trainonly_scores.out` lines 3, 9, 15 give 0.899038, 0.896920,
0.896920, mean 0.897626. Both match the table. The 0.892323 and 0.886601 are printed directly in
`run-0215-scores.out` lines 24 and 49, and the 0.906063 noise floor in `noise_floor.out` line 13. Every
derived number in `CLAIM.md` checks out; `+0.0034` is 0.003352 rounded to 4 dp and `about 0.0046` is
0.004602/0.004587, both fairly stated.

## 8. The bar

`status/plmfit_README_2026-11-20-0535_preclaim.md` line 209 reads, verbatim:

```
| GB1 - three-vs-rest | 0.8791 | Spearman's | ProGen2-M | Adapters | 50% | CLS | Linear |
```

0.8791, as relied on. Whether that saved page is genuine is NOVELTY's question, not mine.

## Verdict

No mismatch, no missing object, no non-determinism. Both claimed Spearmans, both bootstrap intervals, both
prediction-file sha256s, the leakage-copy sha256, the two sealed configurations and every derived number in
`CLAIM.md` reproduce exactly, from code I wrote from the stated definition before reading the author's. The
full rebuild from the model spec agrees with the released predictions to 5e-9, and the kernel identity holds
exhaustively over all fitting-row pairs rather than on a sample. The leakage claim survives both my own
empirical test and a line audit, and the model is not transductive.

Two things I am flagging for the other skeptics rather than failing on, because the bundle states both
openly itself: the three seeds are three identical runs, so the seed requirement carries no information and
the "mean's" bootstrap interval equals a single-file one (reading question for CRITERION); and A's kernel
shape was informed by a test score an earlier run had seen, as `CLAIM.md` says in its own words, which makes
B the clean point and B falls below the 0.8991 full-criterion gate.

pass: true
