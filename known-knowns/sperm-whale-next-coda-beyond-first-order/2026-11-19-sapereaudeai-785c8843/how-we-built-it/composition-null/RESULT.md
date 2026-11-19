# N5 / N6 composition-preserving null controls - result

completed: 2026-11-19T16:37:08Z (date -u). Designs frozen in `../../../PREREG.N5.md` (13:53:43Z) and the statistic
corrected in `../../../PREREG.N5.v2.md` (14:00:12Z). Code: `../code/nulls_n5.py`, unmodified since freeze.

**This is a post-hoc diagnostic, not a gate.** Per PREREG.N5.md and the operator's standing "fair, not strictest"
rule, nothing here tightens a bank threshold or retracts a gate the bank's wording grants. What it decides is how
the result is *described*, and whether partial win p3 should be filed.

## Integrity of the control set

| design | lines | unique indices | range | missing from 0..399 | duplicated | workers at finish |
|---|---|---|---|---|---|---|
| N5 | 400 | 400 | 0..399 | none | 0 | 0 (all exited) |
| N6 | 400 | 400 | 0..399 | none | 0 | 0 (all exited) |

Six N5 workers over [1,67) [67,133) [133,200) [200,266) [266,333) [333,400) and three N6 workers over [1,134)
[134,267) [267,400), plus control index 0 of each from the smoke test. Seeds `numpy.random.default_rng(5000 + i)`.
Both speed shims asserted bit-identical against the frozen feature code on all 3,418 real scored positions at every
worker start. Steady-state cost 150 s per N5 control and 58 s per N6 control at nine concurrent workers.

## The valid statistic: `full` vs `local`

Both models refit on the same shuffled data, both reading the same order-free bag of the stream's earlier codas;
the only difference is the ordered and recency features. The reference is damaged by the shuffle exactly as much as
the model is, so what remains is the ordered component alone.

| design | real | controls | mean | sd | min | max | controls >= real | real vs control mean | real / max control |
|---|---|---|---|---|---|---|---|---|---|
| N5 dialogues | **+0.211238** | 400 | +0.023049 | 0.005585 | +0.006948 | +0.039591 | **0 of 400** | +33.70 sd | 5.34x |
| N6 Dominica | **+0.025465** | 400 | +0.009387 | 0.002052 | +0.003627 | +0.016931 | **0 of 400** | +7.85 sd | 1.50x |

**N5 passes.** Per the frozen rule: the ordered and recency component of the content result is not explainable by
per-recording composition, and its size is +0.2112 bits per coda. Destroying the order inside each recording while
keeping that recording's exact multiset of coda records removes essentially all of it - the controls retain
+0.023 of the +0.211.

**N6 passes.** Per the frozen rule: p3's small ordered component survives, so **the recommendation to withhold p3
is not triggered.** The margin is the narrowest of this run - 1.50x the largest of 400 controls against 49.9x,
92.1x and 111.3x for N2, N3 and N4 - and that should be stated wherever p3 is described. The distribution is tight
(sd 0.00205) and the real value sits 7.85 sd above the mean, so the pass does not rest on the tail being well
behaved.

This revises the expectation recorded in PREREG.N5.v2.md, which called N6 "genuinely at risk" on the strength of a
single control at +0.01039. With 400 controls the spread is small enough that the factor of 2.5 is decisive. The
prediction was wrong in the direction of pessimism; it is recorded here rather than quietly dropped.

## The invalid statistics, reported in full as PREREG.N5.v2.md requires

These are the two statistics PREREG.N5.md originally named and PREREG.N5.v2.md declared invalid as nulls, before
798 of the 800 controls had run. They are reported because their behaviour is the evidence for that declaration.

| design | statistic | real | controls mean | sd | max | controls >= real | real vs control mean |
|---|---|---|---|---|---|---|---|
| N5 | full vs twin | +0.531062 | +0.496911 | 0.013851 | +0.536340 | **4 of 400** (61, 67, 114, 376) | +2.47 sd |
| N6 | full vs bigram | +0.128423 | +0.574094 | 0.010884 | +0.605964 | **400 of 400** | **-40.95 sd** |

Had the originally pre-registered statistics been used as the nulls, the dialogues result would have "failed" with
4 exceedances of 400 and p3 would have "failed" with 400 of 400 - and both failures would have been artefacts. The
shuffle destroys the twin's and the bigram's real token-to-token transitions, which is where those references earn
their predictive power, while the full model keeps the stream cache, whose information is composition and survives
intact. On the Dominica file the control gain over a wrecked bigram (+0.574) is 4.5 times the real gain (+0.128),
and the real value sits 41 sd *below* the control mean. A control that makes the measured quantity larger than
reality is not a null for it in either direction.

## Correction: the real values quoted in PREREG.N5.v2.md are mis-transcribed

PREREG.N5.v2.md states the real `full` vs `local` gains as **+0.211240** (N5) and **+0.025500** (N6). The exact
values, read from the frozen summaries that every other number in this run comes from, are:

| design | PREREG.N5.v2.md says | frozen summary says | source | error |
|---|---|---|---|---|
| N5 | +0.211240 | **+0.21123767905720953** | `attempts/sequence-model/frozen/content_summary.json`, `comparisons.full_vs_local` | 2e-6, a bad rounding |
| N6 | +0.025500 | **+0.02546527737158247** | `attempts/dominica/frozen/p3_summary.json`, `comparisons.full_vs_local` | 3.5e-5, I rounded to +0.0255 and then wrote it back out at six decimals |

Both errors are mine, in transcription, not in any computation; the pipelines and control files were never
affected. **Neither changes the outcome**, and the margins are nowhere near tight enough for 3.5e-5 to matter: the
largest of 400 controls is +0.039591 against an N5 real of +0.2112 (5.3x) and +0.016931 against an N6 real of
+0.0255 (1.5x). The decision rule's conclusion - real beats all 400 on both designs - holds identically under
either figure.

PREREG.N5.v2.md is **not edited**, because it is the frozen pre-registration and its whole value is that it was
written before the data. This file, `null_test.md` and the package carry the exact values; the frozen file carries
the figures I actually committed to. Where the two differ, the frozen file is the record of what was promised and
this table is the record of what is true.

## Disclosures

- Post hoc: designed after the three gates were written and after every number in the claims was known.
- The real values in the frozen pre-registration are mis-transcribed by 2e-6 and 3.5e-5; see the correction
  section above. No verdict depends on the difference.
- PREREG.N5.v2.md was written after control index 0 of each design had run, and those two controls informed the
  correction of the statistic. They are kept and counted in the 400; they are not discarded.
- The permutation moves each coda record as a unit and leaves `TsTo` in place for N5, so a coda's `Duration` no
  longer matches the `TsTo` gap to the coda after it. That artefact is intended and was declared before the run.
- These controls say nothing about whether the gains reflect communication, syntax or meaning. They separate
  ordered structure from per-recording composition, and nothing more.
