# How we found it

**Contributor text, unverified.** This is a plain account of how partial win p4 was reached, not a checked part of
the claim. Every number that matters is in `README.md` and is recomputed by `verify-it-yourself/`.

## It was the lens nobody had tried

The target was picked because it looked like an easy null. Three earlier public attempts on this benchmark had
argued about coda *content* - which coda type comes next - and had got weak or vanishing results. The bank's
partial win p4 asks a different question: not what is said next, but **who speaks next**. None of those three
attempts had tried it.

That turned out to be the cheapest win of the run. Whether the next coda comes from the same whale or a different
one is strongly structured in time: whales overlap, they alternate in runs, and a recording's tempo tells you
something about whether an exchange is in progress. A first-order same-or-switch chain already captures some of
it, which is why the bank uses one as the reference, but not the part that depends on how long the current run has
gone on, how fast the codas are coming, or which whale has been dominating the recording.

## What the model is

A logistic regression on features of the stream's earlier codas only, named here as they are named in
`how-we-built-it/code/p4lib.py`: the last two same-or-switch values and the A-B-A pattern (`s1`, `s2`, `aba`); the
stream's own switch rate so far and how many transitions it rests on (`loc_rate`, `log_ntrans`); how many distinct
whales have been labelled (`log_nd`); how long the current run of one speaker has lasted (`log_run`); the previous
whale's share of the recording and whether it is the modal speaker (`share_prev`, `prev_is_mode`); the last two
inter-coda gaps, whether each overlapped the coda before it, and the gap measured from the previous coda's end
(`log_gap1`, `log_gap2`, `overlap1`, `overlap2`, `end_gap1`); how long since a *different* whale last spoke
(`log_since_other`); the previous coda's click count and duration; and two interactions (`s1_x_loc_rate`,
`s1_x_log_gap1`). Trained on the training folds, with the regularisation strength chosen by inner cross-validation
inside those folds. The reference is the bank's: a smoothed first-order same-or-switch chain, its additive alpha
chosen the same way, from the grid the bank specifies for R1.

Nothing about the predicted coda or any later coda is read. A leakage harness rewrote every field of the predicted
coda and of every coda after it and re-scored: 0 of 3,418 predictions moved, while a deliberately leaky control
feature moved every one of them.

## What failed or had to be corrected

- Development was confined to folds 2 and 4. That discipline cost something visible: the gain on fold 2 is
  0.1511, the largest of the five, so the pooled figure is flattered by a development fold. The three untouched
  folds give 0.0711, which is the number to trust if you only trust one. Both are shipped.
- 237 of the 3,418 positions sit in recordings with a single labelled whale, where the answer is always "same".
  Excluding them drops the gain from 0.0872 to 0.0590. We report the pooled figure because the bank's scored set
  is the bank's scored set, and we report the restricted one right next to it.
- One escape-hatch harness fix was recorded during the run, in `how-we-built-it/PREREG.v2.md`. It concerns the p3
  lens, not p4; p4's frozen code and gates are exactly as frozen at 09:55:11Z. It is shipped here because the
  pre-registration is shipped whole rather than filtered.
- We did not run the composition-preserving control for p4. It was run for the content model and for the Dominica
  file, after the gates, and both passed; p4 was left out because the run had already turned to packaging. So the
  sharper question - whether the gain survives destroying order inside each recording while keeping that
  recording's own switch habits - is open for p4, and `README.md` says so rather than implying the N4 null
  answered it.

## What we think is actually true

Sperm whale exchanges have turn-taking structure beyond "who spoke last", and a good part of it is in the timing
rather than in the identity sequence. That is not a surprising claim and it is not a new one qualitatively -
WhaleLM says as much - but it now has a number on this benchmark, and the number is better than the only other
public one.

The part that should temper it: about two thirds of the margin is reachable from the earlier same-or-switch values
alone, and the rest comes from timing and speaker-share features that are plausibly about recording conditions as
much as about whales deciding when to speak. Nothing here distinguishes those two readings.

## One thing worth knowing about the sequence of events

Another contributor filed a claim on this exact cell 4 minutes 42 seconds after our pre-registration freeze, with
a worse number, and found out about ours no sooner than we found out about theirs. Our packaging-stage novelty
check caught it; an attack-time check could not have, because at attack time it did not exist. Their claim came
first publicly and this package says so in three places.
