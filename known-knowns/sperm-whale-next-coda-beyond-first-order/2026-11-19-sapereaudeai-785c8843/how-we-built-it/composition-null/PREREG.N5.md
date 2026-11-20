# PREREG.N5 - composition-preserving null controls (post-hoc diagnostic)

frozen: 2026-11-19T13:53:43Z (date -u), before any N5 or N6 control was run.

## Status: this is a DIAGNOSTIC, not a gate

The three gates of run 2026-11-19-0936 are already written and this file cannot change them:

- `panel/gate.md` - CONFIRMED_SOLUTION, full criterion
- `attempts/turn-taking/panel/gate.md` - CONFIRMED_PARTIAL, p4
- `attempts/dominica/panel/gate.md` - CONFIRMED_PARTIAL, p3

The bank's criterion does not ask for this control, and the run's CRITERION skeptic judged that requiring it for
condition (2) would be a self-invented stricter gate. That judgement stands. Under the operator's standing
"fair, not strictest" rule, **no result of this control may be used to tighten a bank threshold or to retract a
gate that the bank's own wording grants.** What it can do is decide how the result is *described*, and whether
partial win p3 should be filed at all.

It is post hoc: it was designed after the gates were written and after every number in the claims was known.
That is disclosed here and must be disclosed in any filing.

## Why run it

The bank's criterion can be cleared by per-recording context alone. The claim's own pre-declared decomposition
of the 0.5311-bit gain over the twin is +0.0896 (run length and repeat rate), +0.2302 (an order-free bag of the
stream's earlier codas) and +0.2112 (ordered and recency features). The null designs already run (N2, N3, N4)
resimulate streams from pooled first-order transitions, which destroys *differences between recordings* as well
as order, so beating them rules out "one pooled homogeneous first-order process" and nothing narrower.

The control below instead destroys **order within a recording while preserving that recording's composition**.
It is the control that V3R1T4S draft PR #1159 reported its own Dominica result failing.

## Design N5 (dialogues file, the full criterion, p1 and p2)

- **Data:** data/csv/sperm-whale-dialogues.csv, sha256 1856c8bf...5da2, the same file the claims use.
- **Permutation:** within each REC stream independently, draw a uniform random permutation of its positions and
  apply it to the coda records, so each record moves as a unit. The permuted fields are `nClicks`, `Duration`,
  `Whale` and `ICI1`..`ICI28`.
- **`TsTo` is NOT permuted.** It stays in its slot. This is deliberate and it is what makes the control work:
  streams are ordered by `TsTo`, so permuting it as well would simply relabel the stream and restore the
  original order. Keeping the timestamps fixed and moving the payload is what destroys order while leaving the
  timing grid, the stream lengths and each stream's exact multiset of coda records intact.
- **Known artefact, accepted and disclosed:** a coda's `Duration` no longer matches the `TsTo` gap to the coda
  after it. Within a record, `Duration` and the `ICI` columns stay mutually consistent, because the whole record
  moves together. Any feature reading a between-coda interval therefore sees a shuffled pairing; that is the
  intended effect, not a bug.
- **Pipeline:** the same frozen pipeline end to end, all 5 folds, all inner cross-validation, the same bin edges
  rule (training folds only), the same lambda grid. Feature sets fitted: `twin`, `local`, `full`.
- **Statistics recorded per control:** the pooled gain of `full` over `twin`, and the pooled gain of `full` over
  `local`.
- **Controls:** 400, seeds `numpy.random.default_rng(5000 + i)` for i in 0..399. The 5000 offset keeps these
  seeds disjoint from N2, N3 and N4 (which used 1000 + i).

## Design N6 (DominicaCodas.csv, partial win p3)

- **Data:** data/csv/DominicaCodas.csv, sha256 53dd44fb...6b45.
- **Permutation:** within each rewritten-Date + Unit stream, a uniform random permutation applied to the coda
  records, moving `tok`, `IDN`, `nClicks` and `Duration` together. Stream membership, stream lengths and each
  stream's multiset of coda types are preserved exactly; order is destroyed.
- **Pipeline:** the frozen p3 pipeline end to end, all 5 folds, all inner cross-validation. Sets fitted:
  `local`, `full`; the smoothed bigram reference is refitted on each control as usual.
- **Statistics recorded per control:** the pooled gain of `full` over the bigram, and over `local`.
- **Controls:** 400, seeds `default_rng(5000 + i)`.

## Speed shims (identical to the ones N2 and N3 used)

`scipy.special.ndtr` in place of `scipy.stats.norm.cdf`, the vectorised feature path `fastfeats.feats`, an einsum
gradient and a warm-started L-BFGS-B fit. Each shim asserts bit-identity (`np.array_equal`) against the frozen
feature code on all 3,418 real scored positions at worker start, and the run aborts if any assertion fails. The
frozen files are not modified; this control lives in a new file, `attempts/evaluator/code/nulls_n5.py`.

## Predictions, recorded before any control runs

So that the interpretation cannot be fitted to the answer afterwards:

1. **N5, `full` vs `twin`:** the controls should retain most of the composition component and lose the ordered
   one. Predicted control mean in the range **+0.18 to +0.34 bits**, against a real +0.5311. Prediction: the real
   gain beats all 400.
2. **N5, `full` vs `local`:** both models see the same order-free bag, so the control should collapse to about
   zero. Predicted control mean **between -0.02 and +0.03**, against a real +0.2112. Prediction: the real gain
   beats all 400, and this is the sharper of the two tests.
3. **N6, `full` vs bigram:** predicted control mean **near +0.103** (the real +0.1284 minus the +0.0255 that the
   decomposition attributes to order), with a spread that may well reach the real value. **Prediction: this one
   may fail**, i.e. some control may match or exceed +0.1284. That is the outcome #1159 reported.
4. **N6, `full` vs `local`:** predicted control mean near zero against a real +0.0255.

## What each outcome will mean

- **Real beats all 400 on N5 (both statistics):** the ordered component of the content result is not explainable
  by stream composition alone. The full criterion's description can then say that a measurable part of the gain
  is genuinely sequential, with +0.2112 bits as its size.
- **Real inside the N5 control distribution:** the criterion still stands as the bank words it, and the gate is
  not touched, but the write-up must say plainly that the margin is explainable by per-recording composition and
  that no sequential structure was demonstrated. This would be reported prominently, in README.md's
  "Not claimed" and in the report, not buried.
- **Real beats all 400 on N6:** p3 is safe to describe as it stands, with the existing caveat that most of the
  gain is composition.
- **Real inside the N6 control distribution:** p3 should **not** be filed. The recommendation in that case is to
  withhold it exactly as #1159 withheld theirs, keep the gate file with the result recorded, and say in the
  report why. The p3 gate's status is a matter for the operator, not something this control overrides.
- **Partial completion:** if fewer than 400 controls finish, the result is reported with its actual count and
  explicitly labelled incomplete. No threshold moves either way.

## No other changes

No claim, gate, confirmed_scope, package or frozen file is edited on the strength of this control without the
operator saying so. The existing package `outbox/2026-11-19-sapereaudeai-0b4a7cb4` already discloses, in its
"Not claimed" section, that this control had not been run; if it is rebuilt to include the result, that is a
rebuild before filing, not an edit to anything already filed.

frozen: 2026-11-19T13:53:43Z (date -u), before the first N5 or N6 control was run.
