# How we found it

**Contributor text, unverified.** This is a plain account of how partial win p3 was reached, not a checked part of
the claim. Every number that matters is in `README.md` and is recomputed by `verify-it-yourself/`.

## The lens

DominicaCodas.csv is a second corpus for the same target: coda types recorded from the Dominica units, with a
different token set and different stream definitions from the dialogues file the main criterion uses. The bank's
partial win p3 asks for the same thing there - a next-coda model beating a smoothed bigram by 0.05 bits with an
interval excluding zero - and the stream definition it specifies is coarse: a rewritten date plus a unit, ordered
by coda number.

The model is the same family used for the main criterion, cut down to what this file offers: features of the
stream's earlier codas' `CodaType` and `IDN` only. No timing, because the columns are different. The reference is
the bank's bigram over `CodaType`, its additive smoothing chosen by inner cross-validation on the training folds,
which came out at alpha = 0.3 on all five folds.

## Why the gain is big and the interesting part is small

The pooled gain is 0.128 bits, which clears the 0.05 threshold comfortably. Almost all of it comes from knowing
*which coda types this stream has been using* rather than from any sequential pattern. The decomposition, declared
before the held-out scores existed, makes that explicit: a stream-local reference that sees an unordered bag of
the stream's earlier codas already captures 0.103 of the 0.128, leaving 0.025 for everything about order and
recency.

That is why the claim's scope sentence - written by the run's CRITERION panellist, not by us - carries the
limitation inside it. The bank's p3 wording is cleared by stream-level composition alone, and saying otherwise
would be the easiest way to overclaim on this target.

## What failed or had to be corrected

- **The harness crashed on fold 0 of the first scoring run.** Its leakage self-test tried to perturb `IDN` by
  adding an integer, and `IDN` is a string column. The crash came after fold 0's model fit and before any
  held-out score existed, so it cost nothing but time. The fix changed the harness to perturb the string instead,
  and is recorded in `how-we-built-it/PREREG.v2.md` under the pre-registration's declared escape hatch. The
  frozen model file was not touched.
- **Fixing it exposed a quirk in the frozen model, which we left in.** `IDN` holds `'0'` for 5,705 unidentified
  rows, and two of the model's features compare it against the integer `0`, which is never equal for a string. So
  the model treats "unidentified" as a whale identity rather than as missing, which is not what the code comment
  intended. It reads only earlier codas, so it is not leakage - it is the model being slightly different from
  what its author meant. We reported it and did not change it, because changing a model after its freeze is worse
  than shipping it as frozen.
- **The composition-preserving control nearly withheld this claim.** Another contributor's draft PR had computed a
  Dominica figure on this same file, found it failed a within-stream payload shuffle, and declined to claim p3.
  That was the single most useful thing we read all day. We ran the same family of control after our gate was
  written, with a pre-registered rule saying that if the real gain fell inside the control distribution we would
  withhold p3 the same way.
- **And our own version of that control was wrong the first time.** We pre-registered the gain over the *bigram*
  as the statistic and predicted it would fall under the shuffle. It rose - to four and a half times the real
  value, with all 400 controls above the real gain. The shuffle wrecks the bigram, which lives on real
  token-to-token transitions, while leaving the model's stream-level composition intact, so the gain over it
  inflates. We wrote the correction down with timestamps after two controls and before the remaining 798, and
  switched to comparing two models refit on the same shuffled data differing only in the ordered features. On
  that statistic the ordered component beats all 400 controls - but by 1.50 times, the narrowest margin anywhere
  in this run.

## What we think is actually true

On the Dominica file, knowing what a unit has been saying tells you a lot about what it will say next, and knowing
the order it said it in tells you a little more. The little more is real: it survives a control that keeps each
stream's exact composition and destroys only order. But it is a fifth of the margin, and the margin is what clears
the bank's threshold.

If someone wants to argue from this file that Dominica sperm whales have sequential structure in their coda
production, the honest version of that argument rests on 0.025 bits with a 1.5x margin over its best control, not
on 0.128 bits with a 111x margin. Both numbers are in this package and the first one is the one that is about
order.

## One thing worth passing on

The contributor who identified this control withheld a result because of it. Our numbers suggest - without
establishing, since we have not seen their code - that the version of the control that failed for them may have
been the invalid one, measuring damage to the bigram rather than absence of order. If so, they withheld a claim
they did not have to. That possibility is the reason this package explains the trap at length instead of just
reporting a pass.
