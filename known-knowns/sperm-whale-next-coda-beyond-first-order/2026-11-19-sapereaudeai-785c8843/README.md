# Dominica sperm whale codas: partial win p3

Target `sperm-whale-next-coda-beyond-first-order`, partial win **p3**. Run `2026-11-19-0936`.

## What

The claim, exactly as this run's CRITERION panellist worded it and its honesty gate records it in
`panel/gate.md`:

> On DominicaCodas.csv under the bank's p3 setup (all 8,719 rows of both clans, CodaType tokens, hyphen-to-slash Date rewrite, rewritten-Date + Unit streams ordered by codaNUM2018, text-sorted date folds i mod 5, 8,501 scored codas), the frozen log-linear model, reading only the CodaType and IDN of earlier codas of the same stream, has pooled held-out cross-entropy 1.5895 bits per coda, 0.1284 bits below the inner-CV-smoothed bigram over CodaType (1.7179), with a 95% paired bootstrap interval over rewritten-Date groups of [0.0879, 0.1630] (10,000 resamples), which shows that earlier codas beyond the previous one improve prediction over a pooled bigram, not that coda order does (by the pre-declared diagnostics most of the gain is order-free stream-level context), conditional on the N3 null gate (400 controls, real gain above all).

To six decimals: full 1.589491 bits per coda, bigram 1.717914, gain **0.128423**, paired Date bootstrap
[0.087931, 0.162994] over 96 rewritten-Date groups. The threshold is 0.05 bits with an interval excluding zero.
The N3 null gate is discharged: 400 controls, best of them 0.001154, a margin of 111.3 times.

**Read the second half of that sentence as carefully as the first.** The panellist put the limitation inside the
scope, and it stays there: what this clears is "earlier codas beyond the previous one help", not "coda order
helps". Only 0.025465 of the 0.128423 is ordered structure. That part is now separately controlled - see
"Not claimed" - but it is a fifth of the margin, not the margin.

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Python 3 standard library only, a few seconds, no network. It hashes every file in `object/`, rebuilds the scored
set from the fold table and the vocabulary, recomputes both pooled cross-entropies from the per-position losses,
checks p3's 0.05-bit threshold, runs its own 10,000-resample paired bootstrap over rewritten-Date groups under its
own seed (`31415926`, not the claim's), and checks both null tests including all 800 shipped control gains. Last
line is `PASS` or `FAIL`. `verify-it-yourself/RECEIPTS.md` lists every check and what it cannot do.

## Compared to

The comparator is the bank's own for p3: a bigram over CodaType whose additive smoothing is chosen by inner
cross-validation on the training folds. Both sides are scored on exactly the same 8,501 positions.

| quantity | value | what it is |
|---|---|---|
| **full model** | **1.589491** | the claim |
| bigram reference | 1.717914 | the bank's comparator, gain **0.128423** |
| single-previous-coda variant of our own family | 1.712053 | gains only 0.005861 over the bigram, so the family itself is not what wins |
| repetition-aware first-order | 1.700460 | the model beats it by 0.110968 |
| stream-local reference (order-free bag of the stream's earlier codas) | 1.614957 | the model beats it by only **0.025465**, which is the ordered component |

| quantity | V3R1T4S draft PR #1159 | this claim |
|---|---|---|
| Dominica gain over the bigram | 0.097416 | **0.128423** |
| claimed? | **no - withheld** | yes |

#1159 computed a Dominica figure and declined to claim p3, because it failed a within-stream payload-shuffle
control. That PR holds the first public clearance of this target's full criterion and of p4, but **not of p3**, so
on this cell there is no prior public claim to beat. `how-we-built-it/null_test.md` reports what happened when
this run ran that same family of control, and why the obvious version of it is invalid as a null.
`the-record-we-beat/record.md` records the status source with its fetch time, HTTP status and sha256.

## Not claimed

- **Not that coda order carries the gain.** The scope sentence says so and the numbers say so: 0.025465 of
  0.128423 is ordered structure, the rest is order-free stream-level context - which coda types this unit is
  using, and how often it repeats them. Nothing here is evidence of syntax.
- **The ordered part is real, but by the narrowest margin in this run.** The composition-preserving control
  (design N6, 400 controls, shipped in `how-we-built-it/composition-null/`) shuffles the codas inside each stream
  while keeping that stream's exact multiset of coda records. The ordered component beats all 400, but the best
  control is 0.016931 against a real 0.025465 - a margin of 1.50 times, where the N3 null's margin is 111.3
  times. It was also run **after** the gate was written and cannot change it, and the statistic first
  pre-registered for it was wrong. All of that is in `how-we-built-it/composition-null/RESULT.md`.
- **The ordered component is not recomputable from this package's object.** The stream-local reference's
  per-position probabilities are not shipped, so `verify-it-yourself/` checks the 0.025465 figure against
  `object/p3_summary.json` and against the 400 N6 controls, but cannot re-derive it. `RUN_IT_YOURSELF.md`
  regenerates it from the source data.
- **A feature-definition quirk in the frozen model, found during the run and deliberately not fixed.** The `IDN`
  column of DominicaCodas.csv holds strings - `'0'` for 5,705 unidentified rows, ids such as `'5586'`, and three
  ambiguous forms such as `'6070/6068'` and `'59871?'`. Two frozen features compare `IDN` against the integer
  `0`, which is never equal for a string, so the model treats `'0'` as one more whale label rather than as
  "unidentified" as the code comment intended. This reads only earlier codas, so it is not leakage; it is the
  model being slightly different from what its author meant. It was **not** changed, because changing a model
  after its freeze is worse than shipping it as frozen. See `how-we-built-it/PREREG.v2.md`.
- **Development used folds 0 and 3.** On the three folds never touched in development the gain is 0.118694,
  interval [0.069963, 0.156394], over 5,606 positions. Lower than the pooled figure and still well clear.
- **Not a refit by this checker.** `verify-it-yourself/` checks arithmetic and runs its own bootstrap; it does not
  refit. `RUN_IT_YOURSELF.md` does, and this run's REPRODUCE panellist did it independently - including an
  independently written smoothed bigram that came out bit-identical to the shipped one.
- **The freeze cannot be proved from inside this package.** `panel/freeze_audit.md` is this run's own audit and
  states its limit: timestamps show what exists, not what was deleted.
- **Both clans are pooled, as the bank's setup specifies.** No per-clan result is claimed.

## Credits

Data: the Dominica Sperm Whale Project coda corpus as distributed in Sharma, Gero, Payne, Gruber, Rus, Torralba
and Andreas, *Nature Communications* 15:3617 (2024), https://doi.org/10.1038/s41467-024-47221-8, and the authors'
repository https://github.com/pratyushasharma/sw-combinatoriality at pinned commit 7228c8ee
(`data/csv/DominicaCodas.csv`, sha256 `53dd44fb...6b45`, 747,518 bytes).

Prior sequence modelling on sperm whale codas: WhaleLM, https://doi.org/10.1101/2024.10.31.621071.

The contributor behind V3R1T4S draft PR #1159 identified the composition-preserving control as the one that
matters on this file, and withheld their own figure because of it. That judgement is the reason design N6 exists.

Built with the V3R1T4S kit at commit 5d2d31e76fe1f4d7eb4b75c7646d06425c10640c. Submitted as SapereAudeAI.
