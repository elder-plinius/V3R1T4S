# Commands used to build and check the object

Original certificate (Codex-based run, 2026-10-15): the raw payoff table was generated with
`python3 rectangle_check.py` (sympy 1.14.0), the polynomial certificates with `python3 universal_check.py --make
universal.json`, and checked with the stdlib checkers now in verify-it-yourself/. Its preregistrations are in
original-run/PREREG.md and original-run/PREREG.v2.md (the all-b extension).

Independent re-derivation and panel (Claude-based run 2026-10-15-1311): PREREG.md here was frozen at
13:14:30 UTC before any of that run's results were scored.
`python3 code/independent_certify_sympy.py` (sympy 1.14.0) and `python3 ../verify-it-yourself/independent_check.py`
(standard library). Both printed their checks without failure (the stdlib one ends with PASS).
No search or statistical score is involved, so no null test applies (PREREG.md: null_test not needed).
