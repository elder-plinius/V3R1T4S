# null_test - partial win p4, sperm-whale-next-coda-beyond-first-order (run 2026-11-19-0936)

Design N4 of the run's PREREG.md: the whale labels of every stream are resimulated from the pooled first-order
same-or-switch chain fitted on the training folds, so each control keeps the stream lengths, the timing grid and
the overall switch rate, and destroys any structure in *who* speaks next beyond first order. The whole frozen
pipeline is rerun per control, all five folds and all inner cross-validation, and the statistic is the pooled gain
of the model over the smoothed first-order reference - the same quantity the claim reports.

controls: 400
best_control: 0.000946956774339432
real: 0.08720554077302466
real_beats_all_controls: yes
command: python -I how-we-built-it/null/nulls.py N4 data/csv/sperm-whale-dialogues.csv 0 400 nulls/N4_worker.csv

N4 control gains: mean -0.00592, sd 0.00257, min -0.01557, max 0.00095, indices 0..399, distinct 400.
All 400 gains are in `how-we-built-it/null/N4_controls.csv`. The real gain is 92.1 times the best control and no
control came within two orders of magnitude of it. Control gains are mostly negative, which is what a fair null
should look like here: with the label structure resimulated, the extra features can only cost the model the
parameters it spends on them.

## What this null does and does not rule out

It rules out the possibility that the gain is an artefact of fitting a richer model to label sequences whose only
real structure is first order. It does **not** preserve each recording's own switch pattern: like designs N2 and
N3 in this run, N4 resimulates from pooled transitions, so differences between recordings are destroyed along with
the higher-order structure.

The composition-preserving control that this run ran afterwards (designs N5 and N6, 800 controls, in the full
criterion's package `2026-11-19-sapereaudeai-0b4a7cb4` under `how-we-built-it/composition-null/`) was run on the
**content** model and on the Dominica file, **not on p4**. So for p4 the sharper control is untested, and
README.md's "Not claimed" says so. What is reported instead, and is checked by `verify-it-yourself/`, is the
switch-pattern-only diagnostic: a model that sees only the stream's earlier same-or-switch values gains 0.059453
of the 0.087206, so about two thirds of p4's margin is reachable from the switch pattern alone and the remainder
comes from the timing, overlap and speaker-share features.

## Speed shims used by the null runner only (the frozen files were not modified)

N4 ran with no speed shim: the p4 pipeline is cheap enough that all 400 controls finished without one. The shims
used by the other designs in this run (`scipy.special.ndtr` for `scipy.stats.norm.cdf`, a vectorised feature path,
an einsum gradient and a warm-started fit) are documented in the full criterion's package and were each asserted
bit-identical to the frozen code on all 3,418 real scored positions before use.
