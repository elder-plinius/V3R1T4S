# PREREG v2: run 2026-10-15-0312, lane C

Written at: Thu Oct 15 03:21:55 UTC 2026 (from `date -u`).

Why a v2: the OPERATOR first asked for a wrap-up (03:20 UTC; both jobs were stopped by PID) and then raised this run's
budget to heavy (about 480 active minutes in total, 470 remaining): "Keep the current target, pour effort into the
most promising live line, add lenses if useful, and keep the kit's verification standards." Results seen before this
file: the contrarian lens's checks (tie rule, literal evaluation, format audit: none hurts the lead), the extender's
round-1 single-period fast-model gains (NUMERICAL, unverified, no full portfolio), the a400 relaxation value
(NUMERICAL). No new full portfolio has been judged by pf_eval in this run.

What changes: only the freeze time. The claim object is the best `checker/pf_eval.py`-verified portfolio for the cell
at the freeze time, now planned for 08:15 UTC (recorded with its sha256 in `claim/CLAIM.md`), so the panel and gate
fit before 80% of the budget.

What does not change: the cell (`po_a200_t10_s00`, B = 50, lambda = 1e-2), the bar (−401535, PR #87, best posted
anywhere public; re-read before the claim is built and in the gate if the panel's fetch is older than 6 hours), the
judge (`checker/pf_eval.py` FEASIBLE, exit 0, objective ≤ −401536, and `checker/zimpl_literal_eval.py` agreeing on the
same integer), one cell per claim, other cells are live leads only.
null_test: not needed because the claim is an explicit portfolio object checked by a deterministic exact checker
against a posted value.
