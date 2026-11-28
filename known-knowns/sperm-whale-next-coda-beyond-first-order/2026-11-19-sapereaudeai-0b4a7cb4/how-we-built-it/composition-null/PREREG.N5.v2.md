# PREREG.N5.v2 - correction to the N5/N6 statistic, written after 2 of 800 controls

frozen: 2026-11-19T14:00:12Z (date -u), after control index 0 of N5 and of N6 had run and before any of the
remaining 798 controls ran. PREREG.N5.md was frozen at 2026-11-19T13:53:43Z and is not edited; this file
supersedes its choice of statistic and its predictions, and says why.

## What went wrong in PREREG.N5.md

PREREG.N5.md named two statistics per control and predicted the first one would **fall** under a
composition-preserving shuffle:

- prediction 1: N5 `full` vs `twin` controls near +0.18 to +0.34, against a real +0.5311
- prediction 3: N6 `full` vs bigram controls near +0.103, against a real +0.1284

Both predictions are wrong, and wrong for the same reason, which is a flaw in my reasoning and not in the code:

| control | statistic | predicted | observed (index 0) | real |
|---|---|---|---|---|
| N5 | full vs twin | +0.18 to +0.34 | **+0.50193** | +0.531062 |
| N5 | full vs local | -0.02 to +0.03 | +0.02298 | +0.211240 |
| N6 | full vs bigram | about +0.103 | **+0.57839** | +0.128423 |
| N6 | full vs local | about 0 | +0.01039 | +0.025500 |

**The reason.** A shuffle that destroys order damages the *reference* as well as the model. The twin and the
bigram both earn their predictive power from real token-to-token transitions, which the shuffle removes, while
the full model keeps the stream cache, whose information is composition and survives intact. So the *gain* over
a degraded reference inflates instead of collapsing. On the Dominica file the control gain (+0.578) is four
times the real gain (+0.128).

**Consequence.** `full` vs `twin` and `full` vs bigram are **not valid nulls** for the question this diagnostic
exists to answer. A control that makes the measured quantity *larger* than reality cannot be used as a null for
it; "the real gain beats all 400 controls" would be a meaningless test in that direction, and so would its
failure. Any statement of the form "the real gain does not beat the composition-preserving controls, so the
criterion is explained by composition" would be an error if based on these two statistics.

## The valid statistic

`full` vs `local`. Both models are refit on the same shuffled data, both see the same order-free bag of the
stream's earlier codas (`local` = twin + repetition features + token cache + click-class cache), and the only
thing separating them is the ordered and recency features: skip-bigram, coda t-2 identity, tempo trend, last
same-click-class duration, whale-switch echoes. The reference is therefore damaged by the shuffle in exactly the
same way as the model, and what remains is the ordered component alone. Overfitting, the extra parameters and
the fold layout are all absorbed, because every control reruns the whole pipeline including the inner
cross-validation.

**Decision rule, fixed now, before the remaining controls run:**

- **N5 (dialogues).** The real `full` vs `local` gain is +0.211240. If it exceeds all 400 controls, the ordered
  and recency component of the content result is not explainable by per-recording composition, and its size is
  +0.2112 bits per coda. If it does not, the write-up must say that no sequential structure was demonstrated.
- **N6 (Dominica).** The real `full` vs `local` gain is +0.025500. If it exceeds all 400 controls, p3's small
  ordered component survives. **If it does not, the recommendation is to withhold p3 from any filing**, which is
  what V3R1T4S draft PR #1159 did with its own Dominica figure for this same reason.

**Revised predictions, from the two observed controls:** N5 control mean near +0.02 with the real at +0.2112, so
the real should beat all 400 comfortably. N6 control mean near +0.01 with the real at +0.0255, a factor of about
2.5, so **N6 is genuinely at risk**: 400 draws of a quantity centred near +0.01 may well reach +0.0255.

## Still binding from PREREG.N5.md

- This remains a **post-hoc diagnostic, not a gate.** It cannot tighten a bank threshold or retract a gate the
  bank's wording grants. The three gates of this run stand on N2, N3 and N4, which the CRITERION skeptic judged
  fair for the criterion as worded.
- Both statistics are still recorded for all 400 controls of each design and both will be reported, including
  the two that this file has just declared invalid as nulls. They are reported as what they are: evidence that
  the shuffle damages the reference, which is itself worth knowing and is the reason the valid test had to
  change.
- 400 controls per design, seeds `default_rng(5000 + i)`, the frozen pipeline end to end, speed shims asserted
  bit-identical at every worker start (both assertions passed on all 3,418 real scored positions).
- Controls 0 of N5 and of N6 are kept, not discarded. They are part of the 400 and they are the two that
  informed this correction; that is disclosed here and in the report.
