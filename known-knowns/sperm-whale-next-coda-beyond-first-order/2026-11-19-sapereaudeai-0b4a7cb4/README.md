# Predicting a sperm whale's next coda beyond first order: the full success criterion met (bank target sperm-whale-next-coda-beyond-first-order)

## What

> On sperm-whale-dialogues.csv (sha256 1856c8bf...5da2), with the bank's REC streams, tokens, folds, training-fold bin edges and 3,418 scored codas, the frozen log-linear model `full` of code/seqlib.py, reading only earlier codas of the same REC stream, scores 2.1238 bits per coda pooled over the 5 held-out folds, which is 0.6563 bits below R1 (2.7802 under the claim's inner-CV convention, and at least 0.65 bits below R1 at every alpha of the grid) and 0.5311 bits below its pre-registered single-previous-coda twin with a 95% paired REC bootstrap interval (10,000 resamples) of [0.4571, 0.6325] (0.5226, [0.4463, 0.6273], against the post hoc literal truncated-input twin), so conditions (1) and (2) of the full success criterion are met.

That sentence is the CRITERION panellist's, quoted word for word from `panel/gate.md`.

Both thresholds are cleared by a wide margin: condition (1) asks for 0.10 bits and gets 0.6563; condition (2)
asks for 0.05 bits with a bootstrap interval excluding 0, and gets 0.5311 with a lower bound of 0.4571.

| model | bits per coda, pooled over the 5 held-out folds |
|---|---|
| R1 (the bank's smoothed bigram reference) | 2.780154 |
| the pre-registered single-previous-coda twin | 2.654909 |
| repetition-aware twin (diagnostic) | 2.565329 |
| stream-local reference (diagnostic) | 2.335085 |
| **the claimed model** | **2.123847** |

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. About 10 seconds on a laptop, Python 3 standard library only, no network.

It verifies the sha256 of every file in `object/`, rebuilds the scored set and the fold assignment, recomputes
all five pooled cross-entropies from the per-position losses, checks both conditions against their thresholds,
runs its own 10,000-resample paired bootstrap over REC groups **with its own seed** (it gets [0.4588, 0.6322],
against the claim's [0.4571, 0.6325]), and checks the null test's 400 controls.

To refit the model from the source data instead of checking the shipped arithmetic, see `RUN_IT_YOURSELF.md`.

## Compared to

| cell | value here | value compared against | source | fetched (UTC) |
|---|---|---|---|---|
| pooled cross-entropy, full criterion | **2.123847** bits/coda | 2.564371 bits/coda (order-3 n-gram) | V3R1T4S draft PR #1159 | 2026-11-19T10:16:39Z |
| reference R1 | 2.780154 | 2.794781 | V3R1T4S draft PR #1159 | 2026-11-19T10:16:39Z |
| target status | open | no listing in TROPHY_CASE.md for this cell | V3R1T4S repository | 2026-11-19T10:16:39Z |

**Draft PR #1159 is the first public clearance of this criterion**, filed 2026-11-18, one day before this run.
This claim is a record improvement on it, by 0.4406 bits, and not first evidence of the effect. It was developed
independently and is not derived from it; the two were found by this run's NOVELTY panellist after this run's
freeze.

The two R1 values are the same quantity under two readings of a step the bank leaves open, not a disagreement.
"Inner cross-validation on the training folds" does not say whether the duration bin edges are recut inside the
inner cross-validation, nor whether all transitions or only scored positions are scored. Recutting the edges, or
scoring all transitions, gives R1 = 2.794781 (#1159's value); leave-one-training-fold-out with the outer fold's
edges over scored positions only gives 2.780154. Averaging per-fold mean losses, or leaving one REC out, gives
2.787390. This claim uses the **lowest** of them, which is the hardest reference to beat, and condition (1) holds
under every one of them and at every smoothing value on the bank's grid. The run's CRITERION panellist
reproduced #1159's 2.794781 exactly under the recut-edges reading.

`the-record-we-beat/` holds the status-source snapshot, with its URL, fetch time, HTTP status and sha256.

## Not claimed

- **Not syntax, and not grammar.** The criterion as the bank words it can be cleared by per-recording context
  alone, and #1159 showed a plain order-3 n-gram clears it. Of the 0.531062-bit margin over the twin,
  +0.0896 comes from run-length and repeat-rate features (which do depend on order), +0.2302 from an order-free
  bag of the stream's earlier codas, and +0.2112 from ordered and recency features beyond a stream-local
  reference. What is established is that the next coda depends on **more than the previous coda**. Which part of
  that is sequential structure rather than a slowly varying per-recording state is not settled here.
- **The composition-preserving control passes, but it is a diagnostic and it was run after the gate.** The null
  test this claim rests on resimulates each stream from pooled first-order transitions, which destroys differences
  between recordings as well as order, so on its own it rules out "one pooled homogeneous first-order process" and
  nothing narrower. A sharper control, shuffling codas within each recording so that the recording's exact multiset
  of coda records is kept and only the order is destroyed, was run afterwards: 400 controls, designed and frozen
  before they ran, in `how-we-built-it/composition-null/`. The ordered component of the margin, +0.211238 bits,
  beats all 400 (control mean +0.023049, largest +0.039591), so that component is not explainable by per-recording
  composition. Three caveats belong with that. It is **post hoc**: designed after this run's gates were written and
  after every number here was known, and the run's CRITERION panellist had judged that requiring it for condition
  (2) would be a self-invented stricter gate, so it did not and could not change the gate. The statistic
  originally pre-registered for it was **wrong** - a shuffle that destroys order damages the twin reference as much
  as the model, which inflates the gain instead of collapsing it; that error, and the correction to a reference
  damaged equally by the shuffle, are recorded in `PREREG.N5.v2.md` with timestamps, frozen after 2 of 800 controls
  and before the other 798. And it speaks only to the +0.2112 ordered component: the +0.2302 bits attributed to an
  order-free bag of the stream's earlier codas **is** per-recording composition by construction, and this control
  does not change that. The bullet above still stands.
- **Not a refit by this checker.** `verify-it-yourself/` checks the claim's arithmetic from the shipped
  per-position losses and runs its own bootstrap. It does not refit the model; `RUN_IT_YOURSELF.md` does that.
- **The per-position probability files are not shipped.** They are 3.6-3.8 MB each, over this repository's 1 MB
  per-file limit. `object/per_position_bits.csv` carries the per-position log-loss of every model at every scored
  position instead, which is what every number in the claim is computed from. The probability files are
  regenerable byte-for-byte by `RUN_IT_YOURSELF.md`; their names, sizes and sha256 values are listed there.
- **The freeze cannot be proved from inside this package.** `panel/freeze_audit.md` is the run's own audit of it
  and states its own limit: file timestamps show what exists, not what was deleted. Development used folds 2 and
  4 only; on the three folds never used in development the result is materially the same (+0.5212 against the
  twin, +0.6634 against R1).
- Two secondary sources could not be read (an OpenReview PDF and a phys.org page, both HTTP 403, not retried).

## Credits

- **Data.** Sharma, Gero, Payne, Gruber, Rus, Torralba and Andreas, *Contextual and combinatorial structure in
  sperm whale vocalisations*, Nature Communications 15:3617 (2024),
  https://github.com/pratyushasharma/sw-combinatoriality - the DTag recordings of the Dominica Sperm Whale
  Project. The data file is not copied into this package; it is fetched by URL and checksum.
- **The first public clearance of this criterion.** V3R1T4S draft PR #1159 by another contributor (2026-11-18),
  order-3 n-gram at 2.564371 bits. Its author also cleared partial win p4 first, in draft PR #1175.
- **Neighbouring prior work.** WhaleLM (Sharma, Gero, Rus, Torralba, Andreas; bioRxiv 2024.10.31.621071), which
  reports qualitative predictable turn-taking and plots absolute perplexities under its own tokenisation;
  whale-coda-dynamics, for stream-level run-length and repertoire gains on overlapping recordings; Bond (2026),
  for in-sample higher-order accuracy on this file; Sinha and Chavan (arXiv 2606.16084, 2609.16612, 2610.33974),
  on other corpora and other tokens.
- **The reference.** R1 is the bank's own definition; this package computes it from that definition rather than
  from any published value.
