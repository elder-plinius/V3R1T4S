# Composition-preserving null control for p3 (design N6)

This is the control that decided whether p3 was filed at all.

The null test p3's gate rests on (design N3, `../null_test.md`) resimulates each stream's CodaType sequence from
pooled first-order transitions, which destroys differences between streams as well as order. The contributor
behind V3R1T4S draft PR #1159 reported their own Dominica figure failing a different control - a within-stream
payload shuffle, keeping each stream's composition and destroying only order - and **declined to claim p3 because
of it**. So this run ran that control as well, after the gate was written, as design N6.

## Status

**A diagnostic, not a gate.** Designed after p3's gate was written and after every number in the claim was known.
Under the operator's standing "fair, not strictest" rule it cannot tighten a bank threshold or retract a gate the
bank's wording grants. What it decided was whether to file p3 at all: had the real gain fallen inside the control
distribution, the pre-registered recommendation was to withhold p3 exactly as #1159 withheld theirs.

## Files

| file | what it is |
|---|---|
| `PREREG.N5.md` | the design of N5 and N6, frozen 2026-11-19T13:53:43Z, before any control ran |
| `PREREG.N5.v2.md` | correction of the *statistic*, frozen 14:00:12Z, after 2 of 800 controls and before the other 798 |
| `RESULT.md` | the result for both designs, the integrity checks, and a correction to two mis-transcribed figures |
| `n6_controls.csv` | all 400 Dominica controls: `control, gain_full_vs_bigram, gain_full_vs_local` |
| `nulls_n5.py` | the control code, unmodified since freeze; the `N6` branch is the one that applies here |

`PREREG.N5.md`, `PREREG.N5.v2.md`, `RESULT.md` and `nulls_n5.py` also cover design N5, which ran the same control
on the dialogues file for this target's full criterion. That result lives in the full criterion's package; it is
not part of this claim, and the N5 control gains are not shipped here.

## The result

| statistic | real | 400 controls: mean | sd | max | controls >= real |
|---|---|---|---|---|---|
| **full vs stream-local reference** (valid) | **+0.02546528** | +0.009387 | 0.002052 | +0.016931 | **0 of 400** |
| full vs bigram (invalid as a null) | +0.12842275 | +0.574094 | 0.010884 | +0.605964 | 400 of 400 |

**p3 survives**, so it was filed. But the margin is 1.50 times the largest control, the narrowest figure in this
run, against 111.3 times for the N3 null. `../../README.md` says so in "Not claimed" and so does the claim's
scope sentence.

## Why the second row is not a verdict

A shuffle that destroys order damages the *reference* as well as the model. The bigram earns its predictive power
from real token-to-token transitions, which the shuffle removes; the full model keeps the stream-level
composition, whose information survives intact. So the gain over a wrecked bigram inflates rather than collapses -
here to 4.5 times the real value, with the real gain sitting 40.95 sd **below** the control mean. A control that
makes the measured quantity larger than reality is not a null for it in either direction.

The statistic originally pre-registered in `PREREG.N5.md` was that gain over the bigram, and the prediction
written there was that it would fall. It rose. `PREREG.N5.v2.md` records the correction - the valid comparison is
between two models refit on the same shuffled data that differ only in the ordered features - and was frozen after
2 of the 800 controls had run, before the other 798. Both statistics are reported for all 400 controls here
rather than the invalid one being quietly dropped.

**What this implies about #1159, carefully.** If their control measured the gain over the bigram, then their
failure was the artefact above rather than an absence of order, and the figure they withheld may have been
claimable. We have not seen their code, so this is a reading of the evidence and not a finding about their work.
It is recorded because they identified the right control, and because the same trap caught us.

## Reproducing it

`nulls_n5.py` takes five positional arguments: the design (`N6` here), the source csv, the first control index,
the index to stop before, and the output csv. It appends one line per control and re-reads every sibling output
file before starting each one, so it can be stopped, restarted and split across workers. Section 4 of
`../../RUN_IT_YOURSELF.md` gives the exact command. Each control reruns the frozen p3 pipeline end to end, all
five folds and all inner cross-validation; steady-state cost was 58 seconds per control with nine concurrent
single-threaded workers on 16 threads, so about 2 hours 10 minutes for all 400.

One honest obstacle: `nulls_n5.py` reaches the frozen pipeline through `sys.path` entries shaped for the run
folder, not for this package layout, so the import paths need adjusting before it will run from here. The frozen
files were not edited to fix that.
