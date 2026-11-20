# Composition-preserving null controls (post-hoc diagnostic)

The null test this claim rests on (`../null_test.md`) resimulates each stream from pooled first-order transitions,
which destroys differences between recordings as well as order. That rules out "one pooled homogeneous first-order
process" and nothing narrower. These 800 further controls answer the sharper question: **how much of the model's
advantage survives when the order inside each recording is destroyed but that recording's composition is kept?**

It is the control that a same-cell attempt (V3R1T4S draft PR #1159, on the Dominica file) reported its own p3
figure failing, which is why it was run.

## Status

**A diagnostic, not a gate.** It was designed after this run's three gates were written and after every number in
the claim was known. The run's CRITERION panellist judged that requiring this control for the criterion's condition
(2) would be a self-invented stricter gate, and that judgement stands; nothing here tightens a threshold or
retracts a gate. What it does is decide how the result is described. `panel/gate.md` and `panel/criterion.md` were
not edited on the strength of it.

## Files

| file | what it is |
|---|---|
| `PREREG.N5.md` | the design, frozen 2026-11-19T13:53:43Z, before any control ran |
| `PREREG.N5.v2.md` | correction of the *statistic*, frozen 14:00:12Z, after 2 of 800 controls and before the other 798 |
| `RESULT.md` | the result, the integrity checks on the control set, and the disclosures |
| `n5_controls.csv` | all 400 dialogues controls: `control, gain_full_vs_twin, gain_full_vs_local` |
| `n6_controls.csv` | all 400 Dominica controls: `control, gain_full_vs_bigram, gain_full_vs_local` |
| `nulls_n5.py` | the control code, unmodified since freeze |

## The headline, and the mistake behind it

The statistic originally pre-registered was wrong, and `PREREG.N5.v2.md` says so in its own words before the bulk
of the data existed. A shuffle that destroys order damages the *reference* as well as the model: the twin and the
bigram earn their predictive power from real token-to-token transitions, which the shuffle removes, while the full
model keeps the stream cache, whose information is composition and survives intact. The gain over a wrecked
reference inflates instead of collapsing.

The valid statistic is `full` vs `local` - both refit on the same shuffled data, both reading the same order-free
bag of the stream's earlier codas, differing only in the ordered and recency features.

| design | statistic | real | 400 controls: mean | max | controls >= real |
|---|---|---|---|---|---|
| N5 dialogues | **full vs local** (valid) | **+0.211238** | +0.023049 | +0.039591 | **0 of 400** |
| N5 dialogues | full vs twin (invalid as a null) | +0.531062 | +0.496911 | +0.536340 | 4 of 400 |
| N6 Dominica | **full vs local** (valid) | **+0.025465** | +0.009387 | +0.016931 | **0 of 400** |
| N6 Dominica | full vs bigram (invalid as a null) | +0.128423 | +0.574094 | +0.605964 | 400 of 400 |

So the ordered and recency component of this claim's margin, +0.2112 bits per coda, is **not** explainable by
per-recording composition: destroying the order within each recording removes essentially all of it, leaving
+0.023. The two invalid rows are reported because their behaviour is the evidence that they are invalid - on the
Dominica file the control gain over a wrecked bigram is 4.5 times the real gain.

Nothing here extends to the other components of the margin. The +0.2302 bits attributed to an order-free bag of the
stream's earlier codas is, by construction, composition - that is what it was labelled in `../CLAIM.md` and this
control does not change it. Read with `README.md`'s "Not claimed" section, which this result sharpens rather than
overturns.

## Reproducing it

`nulls_n5.py` takes five positional arguments: the design (`N5` or `N6`), the source csv, the first control index,
the index to stop before, and the output csv. It appends one line per control, and re-reads every sibling output
file before starting each one, so it can be stopped and restarted and split across workers freely. Section 4 of
`RUN_IT_YOURSELF.md` gives the two exact commands. It needs the frozen pipeline modules, which this package
ships in `../code/`; note the pre-existing path defect recorded in the run's dossier, that the frozen code adds a
`code/../../evaluator/code` entry to `sys.path` which does not exist inside a package, so reproducing these
controls inside the package layout needs the import paths adjusted. The frozen files were not edited to fix it.
Cost on 16 threads: about 150 s per N5 control and 58 s per N6 control at nine concurrent single-threaded workers,
so roughly 2.6 hours of wall clock for all 800.
