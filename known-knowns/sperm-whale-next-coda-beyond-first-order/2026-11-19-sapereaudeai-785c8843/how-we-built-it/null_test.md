# null_test - partial win p3, sperm-whale-next-coda-beyond-first-order (run 2026-11-19-0936)

Design N3 of the run's PREREG.md: every stream's CodaType sequence is resimulated from the pooled first-order
transitions fitted on the training folds, so each control keeps the stream lengths and the pooled transition
statistics and destroys everything above first order. The whole frozen pipeline is rerun per control, all five
folds and all inner cross-validation, and the statistic is the pooled gain of the model over the smoothed bigram -
the same quantity the claim reports.

controls: 400
best_control: 0.0011542479820425993
real: 0.1284227460626554
real_beats_all_controls: yes
command: python -I how-we-built-it/null/nulls.py N3 data/csv/DominicaCodas.csv 0 400 nulls/N3_worker.csv

N3 control gains: mean -0.00469, sd 0.00208, min -0.01019, max 0.00115, indices 0..399, distinct 400, no gaps.
All 400 are shipped in `null/N3_controls.csv`. The real gain is 111.3 times the best control. The control gains
are mostly negative, which is what a fair null looks like here: once the sequence is resimulated from pooled
first-order transitions, the extra features can only cost the model the parameters it spends on them.

## The second, sharper control: design N6 (composition-preserving)

N3, like N2 and N4 in this run, resimulates from *pooled* transitions, so it destroys differences between streams
as well as order. It therefore rules out "one pooled homogeneous first-order process" and nothing narrower. The
contributor behind V3R1T4S draft PR #1159 reported their own Dominica figure failing a control of a different
family - a within-stream payload shuffle, which keeps each stream's composition and destroys only order - and
declined to claim p3 because of it. So this run ran that control too, after the gate, as design N6.

n6_controls: 400 (indices 0..399, no duplicates, no gaps)
n6_statistic: pooled gain of the full model over a stream-local reference, both refit on the shuffled data
n6_best_control: 0.016930587044015767
n6_real: 0.02546527737158247
n6_real_beats_all_controls: yes   (control mean 0.009387, sd 0.002052; the real value is +7.85 sd)

All 400 gains are in `composition-null/n6_controls.csv`; the design is `composition-null/PREREG.N5.md`, the
correction to its statistic is `composition-null/PREREG.N5.v2.md`, and the result with its integrity checks and
one transcription correction is `composition-null/RESULT.md`.

**The margin here is 1.50x, the narrowest in this run**, against 111.3x for N3. It should be stated wherever p3
is described, and `README.md` does state it.

### Why the obvious version of that control is invalid, and what it would have said

Measured against the **bigram**, the composition-preserving shuffle does not weaken the gain, it inflates it:
across the same 400 controls the gain over the bigram averages +0.574094 against a real +0.128423, and **all 400
controls exceed the real value**, which sits 40.95 sd below the control mean. The reason is that the shuffle
destroys the real token-to-token transitions the bigram lives on, while the model keeps the stream-level
composition, whose information survives intact. A control that makes the measured quantity four and a half times
larger than reality is not a null for it in either direction, and "the real gain does not beat the controls" would
be meaningless.

That is why N6's statistic is the gain over a stream-local reference that is damaged by the shuffle in exactly the
same way as the model, leaving the ordered component alone. The error was ours first: the originally
pre-registered statistic was the gain over the bigram, and `composition-null/PREREG.N5.v2.md` records the
correction, frozen after 2 of the 800 controls had run and before the other 798. Both statistics are reported for
all 400 controls rather than the invalid one being dropped.

It also suggests, without establishing, that #1159's withheld figure may have failed a control that was measuring
damage to its reference rather than absence of order. We have not seen their code and make no claim about it.

## Speed shims used by the null runners only (the frozen files were not modified)

- N3 ran with an einsum gradient in place of the broadcast-and-sum gradient, same objective: on real fold 0 it
  reproduces the frozen p3 probabilities to within 7.4e-12.
- N6 ran with the same einsum gradient and a warm-started L-BFGS-B fit, both copied unchanged from the N3 runner.
- The vectorised feature path and `scipy.special.ndtr` shims used on the dialogues file do not apply to the p3
  pipeline and were not used here.
