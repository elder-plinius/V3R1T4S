# PREREG.md: robust-forecast-aggregation-bounds, run 2026-10-14-1717 (lane B)

frozen_at: Wed Oct 14 17:28:35 UTC 2026
(written before any attack program has produced output; the checker tests on published/known cases ran before this)

## Criterion (verbatim from charter.md; the target is not in the bank)

> robust forecast aggregation with two experts whose signals are conditionally independent given the state, squared
> loss, additive regret against the omniscient aggregator. First cell: the unknown-state-values variant (bounds
> 31/1326 ≈ 0.023379 and 0.025512): an explicit aggregator with an interval-certified worst-case regret below
> 0.025512, or an explicit information structure certifying more than 31/1326. Second cell: the binary-state setting
> (bounds (5√5 − 11)/8 ≈ 0.0225425 and 0.022599): an explicit finite mixture of structures certifying more than
> (5√5 − 11)/8, or an aggregator with certified regret below 0.022599.
> Shape: bound (an explicit aggregator or information structure with the regret definition copied from the source;
> the worst case certified with interval or exact arithmetic over the full reduced parameter domain).

## Cell attacked and the exact rule that will judge it

Cell 1 (unknown state values), lower-bound side.
- Object: a JSON file (code/lb_check.py input format) listing finitely many environments, each with a binary state
  space 0 <= theta_1 < theta_2 <= 1 (strict), a prior over the two states, two experts with finite signal sets and
  conditionally independent likelihoods, all parameters rational, plus rational mixing weights summing to 1. This is
  the same kind of object as Theorem 3.4 of arXiv:2604.24517v2, whose 31/1326 is certified in exactly this way.
- Statistic: LB(D) = min over aggregators f of E_D[L(f | env)], computed exactly in rationals by code/lb_check.py
  (both of its computations, the variance form and the literal loss-difference definition, must agree). By Yao's
  principle inf_f Reg[f] >= LB(D).
- Threshold: LB(D) > 31/1326 as exact rationals (strict). A tie or anything below is NOTHING. The published bar is
  exact, so there is no tolerance question on this side.
- A win would be a claim that the minimax regret of the unknown-state CI cell is at least LB(D) > 31/1326; nothing
  wider (not the minimax value, not the known-{0,1} cell).

Cell 1, upper-bound side (attacked only as far as numerics; pre-registered so that no number gets upgraded later).
- Statistic: sup over the full reduced parameter domain (Lemma 3.3: theta_1 <= theta_2 in [0,1], lambda_2 in [0,1],
  a_1, b_1, a_2, b_2 in [0,1]) of L(f | Theta, pi) for an explicit aggregator f, certified with interval arithmetic.
- Threshold: certified sup < 0.025512. A numerical (floating-point, multi-start) sup is labelled NUMERICAL and is
  never a claim at any level above "progress"; it cannot be packaged.

Cell 2 (known {0,1} states): not attacked in this run; no claim will be made on it.

## Null design

null_test: not needed because the result is an explicit object (a rational adversary distribution over explicit
environments) whose statistic is computed exactly by a deterministic checker and compared with an exact published
value (31/1326); there is no chance level, statistical test or search-versus-random component in the claim.

## What cannot change after this point

The threshold, the statistic, the object type and the checker (code/lb_check.py, tested in checker_tests/results.log
before this file was written). If any of them must change, a new timestamped PREREG.v2.md is written and the report
says so.
