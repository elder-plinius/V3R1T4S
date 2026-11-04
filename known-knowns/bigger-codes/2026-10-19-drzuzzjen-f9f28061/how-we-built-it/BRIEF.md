Written post-hoc on 2026-10-19T10:54:45Z for kit layout; content transcribed from PREREG.md / REPORT_K.md / logs; no measurement added.

# BRIEF: Stage K, finite seed evaluation of the plateau walk from the immutable 8,732, cell A(25,6,11) (run 2026-10-19-0955-k-a25-6-11-seeds)

Every statement is transcribed from PREREG.md, REPORT_K.md or the files named; this brief decides nothing. Bank criterion: see target.md.

## What this stage is (PREREG.md)
Question: does the operator still reach M > 8,732 from the immutable 8,732 in short independent runs, and how often? Not a record attempt; any M >= 8,733 is a CANDIDATE PENDING LIVE COMPARISON; nothing is published for beating 8,732. Authority: Manager 6263866201 (09:18:23Z), conditional pre-authorisation, conditions met (live channel, wrapper corrected and controlled in Stage W: j7 0c012a49..., micro-tests T1-T5 AS_DESIGNED, resources measured at launch). T0 = 2026-10-19T09:53:19Z; useful cut 11:05:19Z; everything done by T0+90 = 11:23:19Z.
Runs (sequential, one at a time under ONE pte-eval supervisor): R0 CONTROL seed 105, --seconds 120, --stop-at-M 8733 (recovery control only, its object is not a new hit); R1..R5 new seeds 201, 202, 203, 204, 205 (fixed in advance, never used before), --seconds 600 each, full length. Same operator and parameters as F/G/H/J (lb_lns_gen.py, --rounds 1000000), wrapper j7_run.py 0c012a4941108e1ea12a9c271408fb06e0cdf80e41c34600d7a8700ed3ad56be, bar 8,733, 4 numba threads. Input sha256 0f9c84b8... verified at launch.
Decision rule (Manager 6263866201): control not recovered -> stop K for diagnosis; control OK: 0/5 new -> practical NO-GO of this sampling; 1/5 -> inconclusive; >= 2/5 -> evidence to present for a decision, never an automatic next stage. Report counts, times to first hit (censored at 600 s), final bests and the uncertainty of only five trials.
Infrastructure: only pte-eval tools/supervise.py + winjob.py, --mem-gib 8 --job-rss-gib 4 --sys-floor-gib 12 --checkpoint-min 1 --threads-cap 4 --deadline-utc 2026-10-19T11:06:19Z; checkers single-threaded with the engine suspended; 0 GET.
Hypotheses before any run: K1 control recovers 8,733 within 120 s (0.9); K2 at least one of 5 new seeds reaches >= 8,733 within 600 s (0.45); K3 >= 2/5 (0.2); K4 any run reaches >= 8,735 (0.05).

## Outcome
See REPORT_K.md (closed 2026-10-19T10:44:41Z): K1 TRUE, K2 TRUE, K3 TRUE (3/5: seeds 201, 202, 204), K4 FALSE; best object M = 8,734 (f9f28061..., seed 201) = CANDIDATE PENDING LIVE COMPARISON, not a record. Declared gap: no effective barrier conditioned R1-R5 on R0's result.
