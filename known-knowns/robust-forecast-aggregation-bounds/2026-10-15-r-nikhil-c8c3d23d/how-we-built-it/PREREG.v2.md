# PREREG.v2.md: addition for the second cell (known {0,1} states), lower-bound side

frozen_at: Wed Oct 14 22:30:19 UTC 2026
(written after the human extended the run to a heavy budget and before any attack program for the second cell ran;
PREREG.md is unchanged and still governs the first cell)

## Criterion for the second cell (verbatim from charter.md)

> Second cell: the binary-state setting (bounds (5√5 − 11)/8 ≈ 0.0225425 and 0.022599): an explicit finite mixture
> of structures certifying more than (5√5 − 11)/8, or an aggregator with certified regret below 0.022599.

## Exact rule

- Object: a JSON file in the code/lb_check.py format whose every environment has theta = [0, 1] (the known binary
  state space of Arieli, Babichenko and Smorodinsky 2018 and of Section 3.3 of arXiv:2604.24517), a prior, two
  experts with finite conditionally independent signal sets, rational parameters, rational weights summing to 1.
- Statistic: LB(D) = min over aggregators f of E_D[L(f | env)], exactly as in PREREG.md, computed by
  code/lb_check.py (both internal routes must agree).
- Threshold: LB(D) > (5 sqrt(5) - 11)/8, decided exactly: since 8 LB + 11 > 0, the inequality holds if and only if
  (8 LB + 11)^2 > 125 in exact rationals (code/lb_check.py --bar abs2018). A tie is impossible for a rational LB
  (the bar is irrational); anything below is NOTHING.
- Scope of a win: the minimax regret of the known-{0,1} CI cell is at least LB(D); nothing wider.

## Null design

null_test: not needed because the result is an explicit object checked by a deterministic exact checker against an
exact published value; no chance level or statistical component.
