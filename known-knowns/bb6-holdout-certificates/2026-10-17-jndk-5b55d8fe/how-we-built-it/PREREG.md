# PREREG (second panel run; session id redacted), written 2026-10-17T17:10:45Z, before any check of this run and before claim/ is built

(Package copy: the session id and the compute server hostname were redacted for publication; otherwise verbatim.)

## Criterion (verbatim, partial win p1)
"Verified macro-rule reduction: for a machine in the newest BB(6) holdout file whose wiki/holdout notes give no accelerated rule set, an explicit set of parametric rules (e.g. A(n) -> A(f(n))) proven for ALL parameter values by a symbolic checker or Lean/Rocq (no sorry), with every rule application also matching a naive simulation for the first 1e8 steps."

## Thresholds
- lens notes: claim/code/notes_check.py on today's pages: hits=0 on holdouts_lists.html, bb6_page.html and
  sheet_gid806905077.csv; only SELF hits elsewhere; notes_empty: True.
- lens reproduce (fresh copy of claim/ on the compute server, code/remote_checks.sh): parser test pass; RESULT PROVED for all
  seven ids; all controls rejected; brute force all real pass and all mutants caught; replay TOTAL scheduled ==
  passed == 8365935, failures=0; controls passed=0; BB(5) champion 47176869 defined transitions.
- panel: three NEW fresh subagents (REPRODUCE, NOVELTY, CRITERION), each seeing only its own copy of claim/; the
  run-1618 verdicts are not reused. Gate: CONFIRMED_PARTIAL only with three pass: true, no hedge and check_run PASS;
  otherwise PROMISING.

null_test: not needed because the claim is an explicit rule set checked by deterministic symbolic and naive-simulation checkers; no search, key, period or statistical "beats chance" claim.
