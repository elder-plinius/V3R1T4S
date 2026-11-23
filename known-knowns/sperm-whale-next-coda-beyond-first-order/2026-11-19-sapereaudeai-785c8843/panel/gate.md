# Honesty gate - partial win p3 (written 2026-11-19T12:29:14Z by the run's main session)

status: CONFIRMED_PARTIAL
confirmed_scope: On DominicaCodas.csv under the bank's p3 setup (all 8,719 rows of both clans, CodaType tokens, hyphen-to-slash Date rewrite, rewritten-Date + Unit streams ordered by codaNUM2018, text-sorted date folds i mod 5, 8,501 scored codas), the frozen log-linear model, reading only the CodaType and IDN of earlier codas of the same stream, has pooled held-out cross-entropy 1.5895 bits per coda, 0.1284 bits below the inner-CV-smoothed bigram over CodaType (1.7179), with a 95% paired bootstrap interval over rewritten-Date groups of [0.0879, 0.1630] (10,000 resamples), which shows that earlier codas beyond the previous one improve prediction over a pooled bigram, not that coda order does (by the pre-declared diagnostics most of the gain is order-free stream-level context), conditional on the N3 null gate (400 controls, real gain above all).

The confirmed_scope above is the CRITERION panelist's sentence, verbatim, including its closing condition. That
condition is now discharged: see below. The sentence is deliberately left unedited, as kit/RUN.md step 7 requires.

## Panel files read in full by the main session

- **reproduce.md — pass: true.** Data checksum; independent regeneration of streams, folds, scored set and
  vocabulary; an independently fitted smoothed bigram that is bit-identical to the saved one; vector validity in
  both files; recomputed cross-entropies and the 0.12842-bit gain; a fresh-seed Date bootstrap [0.0889, 0.1633]
  excluding 0; a bit-identical frozen rerun; an independent leakage test with a working positive control (its own
  leaky predictor caught at 8,501 of 8,501).
- **novelty.md — pass: true.** The object is not derivable from PR #1159's Dominica model or any Sinha-Chavan
  model by deletion, restriction, relabelling, symmetry or numerical polish. Within the cell it strictly beats the
  only known value (0.1284 > 0.0974).
- **criterion.md — pass: true**, conditional on the N3 null, now discharged.

## The condition, discharged

**N3 null, 400 controls, real gain above every one.** DISCHARGED. 400 of 400 complete, no missing index, no
duplicate. Best control +0.001154 against a real +0.128423, a 111.3x margin; zero controls at or above the real
gain; mean -0.004687, sd 0.002081. Recorded in claim/null/null_test.md (`p3_real_beats_all_controls: yes`) and
verified independently by this session. CLAIM.md's Null section, which read PENDING when the panel saw it, is
superseded by that file.

## Downgrade checks (kit/RUN.md step 7), each considered

- **Hedging panelist:** no. All three passes are clean once the N3 condition is discharged.
- **Reproduction mismatch:** no. REPRODUCE reports the claimed numbers reproducing exactly, with a bit-identical
  frozen rerun.
- **Value not strictly better than the live table:** no table value exists for this cell. PR #1159 computed
  +0.097416 and **declined to claim it**; the bank's own reference (the smoothed bigram) is what this claim beats.
- **Stretched criterion or hidden quantifier:** no, but one is worth naming. The bank's p3 asks for a gain over a
  smoothed bigram, and that is what is claimed; it does not ask for a demonstration that *order* carries the gain.
  CRITERION's scope sentence states this limit in its own words rather than letting the headline imply more.
- **Scope wider than what was reproduced:** no. The scope sentence is CRITERION's verbatim, and it explicitly
  says what the result does not show.
- **Several objects bundled as one claim:** no. This is one enumerated partial win on a different file from the
  main criterion.
- **Unresolved benchmark baseline:** not applicable; the reference is defined by the bank and computed from that
  definition.

## The honest limit of this partial win (must survive into any filing)

This is the weakest of the three results in this run, and it should be presented that way.

- By this claim's own pre-declared decomposition, only **+0.0255 of the +0.1284 bits** is ordered structure beyond
  a stream-local reference. The rest is stream composition: which coda types a given date-and-unit stream uses at
  all.
- **The N3 null does not preserve stream composition.** It resimulates each stream from pooled first-order
  transitions, which destroys between-stream heterogeneity. Beating it therefore rules out "one pooled
  homogeneous first-order process" and nothing narrower.
- **A same-cell attempt already failed the control that does preserve composition.** PR #1159 reported its
  Dominica figure and withheld the claim because it failed a payload-shuffle control (within-stream CodaType
  swaps). That control is the strongest open test of this partial win and has not been run here.
- CRITERION judged that requiring a composition-preserving null for the bank's condition would be a
  self-invented stricter gate. That is correct as a *gating* matter and this gate follows it. It does not make
  the interpretive caveat go away, and the caveat is the reason this partial win should not be described as
  evidence of coda order or syntax.

A composition-preserving null is the first thing to run on this cell next, and it may well reduce or remove this
partial win. That is a reason to run it, not a reason to withhold the result.
