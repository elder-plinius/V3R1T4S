# Receipts — real output of `sh verify-it-yourself/run_checks.sh`

Run from this package folder with plain `python3`. **Python standard library only** — no numpy, no
pandas, no drevalpy, no network, no dataset download, no environment variables. A couple of minutes
(about 20 s on a native filesystem; slower on a Windows-mounted one). Exits 0 on PASS, 1 on FAIL.

```
interpreter: 3.10.12  (standard library only -- no numpy, no pandas, no network)

==============================================================================
0. object integrity: every shipped file must match object/MANIFEST.sha256
   43 files listed, 43 verified, 0 mismatched, 0 missing, 0 unlisted
   ok: the object is byte-for-byte as shipped

1. leave-drug-out property: no test drug may appear in train or validation
   seed42       ok, all 10 splits drug-disjoint and complete
   independent  ok, all 10 splits drug-disjoint and complete

2. ruler authenticity: regress the shipped ruler on a replay built from the object
   seed42       worst |slope-1| = 0.00000   worst |intercept| = 0.00000
   independent  worst |slope-1| = 0.00000   worst |intercept| = 0.00000

3. tamper check: the model's predictions must actually differ from the ruler's
   seed42       splits whose predictions equal the ruler's: 0/10   <- ok
   independent  splits whose predictions equal the ruler's: 0/10   <- ok

4. the benchmark statistic, recomputed from the shipped predictions
   seed42       PotencyTransfer  normalized R^2 = +0.2244  (SE 0.0352, 10 splits, 10/10 positive, worst +0.0913)
   seed42       ruler            normalized R^2 = -0.0245  (SE 0.0086)   <- published -0.0169
   independent  PotencyTransfer  normalized R^2 = +0.2263  (SE 0.0478, 10 splits, 10/10 positive, worst +0.0252)
   independent  ruler            normalized R^2 = -0.0185  (SE 0.0068)   <- published -0.0169

5. margin over the published maximum (+0.0235)
   seed42       > max+0.02 (+0.0435): yes   > max+2SE (+0.0938): yes
   independent  > max+0.02 (+0.0435): yes   > max+2SE (+0.1191): yes

6. the published leader's own same-splits re-run, from the shipped predictions
   seed42       leader re-run -0.0268 (SE 0.0387)   claim - leader +0.2512   claim wins 10/10 splits
   independent  leader re-run -0.0928 (SE 0.0536)   claim - leader +0.3191   claim wins 10/10 splits

7. the gain is not carried by the drug-combination leak (drevalpy issue #300)
   seed42       single agents +0.2031 (SE 0.0406) | combinations +0.2030 (SE 0.0471)
   independent  single agents +0.2023 (SE 0.0523) | combinations +0.1639 (SE 0.0496)

==============================================================================
PASS

=== corrupted objects must be rejected, and the checker must survive to say so ===
   -> ok: 'model predictions replaced by the ruler's in ALL splits' rejected (9 assertions fired)
   -> ok: 'model predictions replaced by the ruler's in ONE split only' rejected (4 assertions fired)
   -> ok: 'ruler cell-line effects rescaled by 3x (model untouched)' rejected (7 assertions fired)
   -> ok: 'the 5 worst test drugs silently dropped from every split' rejected (9 assertions fired)
   -> ok: 'a test drug also placed in training' rejected (3 assertions fired)
   -> ok: 'one digit of one prediction altered' rejected (2 assertions fired)

PASS
```
## The eight checks

0. **Object integrity** — every file in `object/` is hashed and compared with `object/MANIFEST.sha256`, and
   the directory is checked for unlisted or missing files. This is what makes the rest meaningful: an
   aggregate mean over 10 splits cannot notice one altered digit, so the object is pinned by hash first.
1. **Leave-drug-out property** — in every split, no test drug appears in train or validation, every predicted
   drug is in the test fold, and every test drug is predicted. Catches leakage and silent abstention.
2. **Ruler authenticity** — the reference baseline's shipped predictions are regressed on a replay
   reconstructed from the object itself; slope must be 1 and intercept 0. Rescaling the ruler inflates the
   statistic *without touching the model*, and a margin test alone cannot see that. The replay is tried for
   each k from 1 to 12 because of a drevalpy defect that reweights validation rows (`../DIAGNOSTICS.md`);
   rescaling changes the slope for every k, so it is still rejected.
3. **Tamper check** — the model's predictions must actually differ from the ruler's in every split.
4. **The statistic** — normalized R² per split and its mean, for both split generations, with the ruler's own
   value checked against its published behaviour.
5. **Both margin conditions** — above the published maximum by ≥ 0.02 absolute *and* ≥ 2 × across-split SE.
6. **The published leader's own same-splits re-run**, from predictions shipped in `object/`: the claim must
   beat it on every split of both generations.
7. **Single agents alone must still clear the bar**, so the known drug-combination leak cannot be carrying it.

## The six corruption tests

A checker that cannot fail proves nothing. Each test builds a corrupted copy of `object/` and requires the
checker to **run to completion and print `FAIL`** — a crash counts as a failure of the test, not a pass.

Three of these six exist because something else caught a weakness in this checker rather than the author:

- *ruler rescaled 3x* and *five worst test drugs dropped* were written by the verification panel after it
  found an earlier version of this checker **accepted** both (reporting +0.4088 and +0.2961 and passing);
- *one digit of one prediction altered* was added after the kit's own package checker warned that the
  suite still passed when it changed a single digit of the object. Check 0 is the answer to it.

Replacing the model's predictions with the ruler's in **one** split of ten does not break the margin on its
own — nine untouched splits keep the mean above the bar. That is a property of the result, not a flaw, and
it is why checks 0 and 3 exist.

## Two numbers that differ, and why

This checker reports **+0.2244** for seed 42 while drevalpy's own evaluation reports **+0.2249** for the same
predictions. drevalpy attaches the ruler with a left merge on (drug, cell line, split), and CTRPv2 has
**4,118 duplicated (cell line, drug) keys**, so that merge expands 235,974 predictions into 245,122 scored
rows. This checker aligns the two models' predictions row for row instead. The criterion's words are
"drevalpy's own evaluation code", so +0.2249 is the benchmark's quantity and is what the claim states; this
checker quotes the smaller, row-aligned figure. Neither is hidden.
