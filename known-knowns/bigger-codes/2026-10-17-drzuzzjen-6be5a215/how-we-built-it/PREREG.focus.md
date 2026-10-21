# PREREG: constant-weight-codes, FOCUSED stage on A(26,6,9) (Windows campaign, T0 2026-10-16T19:20:27Z)

frozen_utc: 2026-10-16T20:44:52Z
(frozen before any measurement of this run; the pilot run pilot-code and its PREREG v1-v2 stay unchanged)

## Selection (pilot rule (1), PREREG.md of pilot-code, unchanged)
The only cell with a valid code above its live lower bound is A(26,6,9): 5988 (panel + gates, delivered in PR #22),
then 5991 from two independent 40-min walks starting at 5988 (two distinct codes, both checkers valid; a panel on the
seed-21 code is running). Pilot cells A(24,6,12), A(22,6,9), A(21,6,9): no gain in about 1,000 method-1 rounds each.
Value to beat: the best known value is 5986 (V3R1T4S) / our own 5991; the target of this stage is any valid code
larger than the current best of this campaign.

## Caps
Focused-stage cap 36 h inside the campaign window (deadline 2026-10-18T19:20:27Z); this run is a sequence of finite
batches of 60 min, each frozen in its job file; decision after each batch. Resources: <= 24 own threads, memory
enforced by tools/supervise.py (job 8 GiB, reserve 14 GiB, every ~5 s).

## Methods (two lenses on the same cell, cooperative: each batch starts from the best valid code so far)
- plateau-walk: lb_lns_gen.py (V3R1T4S, unchanged), default neighbourhood (rmax 8, KB 3), different random seeds.
- deep-neighbourhood: the same engine family with deeper moves (lb_lns_gen.py with --rmax 12 --kb 4, as documented by
  V3R1T4S for lb_lns_deep), measured against plateau-walk at equal threads and time.
Batch 1 (60 min) also measures thread scaling: plateau-walk jobs with 2, 4 and 8 numba threads from the same start
(best_5991_s21) and different seeds; the rest of the threads go to 2-thread jobs of both lenses from both 5991 starts.

## Statistic and decisions
Per job: best valid size; per lens: max gain per batch. Any code above the current best is frozen at once, checked by
both checkers and sent to a three-skeptic panel (as a new linked version; earlier claims are never rewritten).
Stop or change method when two consecutive batches give no gain in either lens; then report the plateau (sizes,
rounds, neighbourhood) as the negative result of this cell.
null_test: not needed because the claim is an explicit object checked by two deterministic exact checkers against published values
