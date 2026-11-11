# Skeptic 3 — Target Criterion & Hygiene Audit (`criterion.md`)

- `context`: `fresh independent skeptic review initialized from clean package directory`
- `target_id`: `hadamard-maxdet-records`
- `criterion_checked`: `bank/targets.json (id: hadamard-maxdet-records)`

## Audit Findings

1. **Exact Match to Target Win Rule:** For each claimed order `n in {81, 89, 93, 97, 101, 105, 109, 117}` (`n` not divisible by 4), `object/M<nnn>.txt` provides an explicit `n x n` matrix with entries strictly in `{-1, +1}`, exact integer `|det(X)|` divisible by `2^(n-1)` verified via fraction-free Bareiss elimination on Python `int` and cross-checked with `sympy.Matrix(...).det(method='bareiss')` (plus 14-prime CRT), strictly exceeding the live maximum across Orrick's archived MaxDet database, `arXiv:2608.22518v3` / `Math-AI-Caltech/hadamard-maxdet`, and `elder-plinius/V3R1T4S`.
2. **Residue-Class Upper Bound Check:** All eight orders satisfy `n = 1 (mod 4)`, and `verify-it-yourself/verify.py` confirms by exact integer arithmetic that `|det(X)|^2 < (2n - 1) * (n - 1)^(n - 1)` (Barba's 1933 bound), with ratios ranging from `0.756779` (`n = 117`) to `0.860635` (`n = 101`).
3. **Package Isolation & Scope Honesty:** Zero third-party files are copied into `object/` or `the-record-we-beat/`; all files are well under 1 MB; `README.md` quotes `confirmed_scope` from `panel/gate.md` verbatim under `## What`; and no optimality claim is made on any of the eight orders.

pass: true
