# PREREG v3: run 2026-10-15-0312, lane C

Written at: Thu Oct 15 09:01:05 UTC 2026 (from `date -u`).

Why a v3: the session was paused by the control supervisor (usage limit; paused time does not count against the
budget) and resumed at 09:00 UTC, after PREREG.v2's planned freeze time (08:15 UTC) had passed. No freeze happened at
08:15: nobody was running the session. Results seen before this file: the extender's 60 rounds ended at 07:34 UTC
with best `attempts/extender/rounds_b/base_r53.sol`, judged at 09:00 UTC by `checker/pf_eval.py` (−644342, FEASIBLE)
and `checker/zimpl_literal_eval.py` (−644342); the a400 lead's round-12 base (−1806395, FEASIBLE; not this run's cell).

What changes: only the freeze time, now = the time this file was written. The claim object is the best
pf_eval-verified portfolio for the cell at this time, which is `base_r53.sol` (−644342). Nothing produced after this
file is written can replace it in this run.

What does not change: the cell (`po_a200_t10_s00`, B = 50, lambda = 1e-2), the bar (−401535, PR #87, best posted
anywhere public; re-read right before the claim is built), the judge (pf_eval FEASIBLE, exit 0, objective ≤ −401536;
zimpl_literal_eval agreeing), one cell per claim; other cells are live leads only.
null_test: not needed because the claim is an explicit portfolio object checked by a deterministic exact checker
against a posted value.
