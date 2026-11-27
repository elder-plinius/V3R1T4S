# Preregistration: `erdos-7-odd-covering-system`

- **Written (UTC):** 2026-11-27T01:23:13Z, while this package was assembled, **after** the certificates were computed and checked. Nothing in this file was written before the computation, and it is not backdated.
- **Target ID:** `erdos-7-odd-covering-system`
- **Claimed win:** partial win `p2`.

## 1. The success rule

The success rule is the bank's own text for partial win p2, fixed by the bank before this computation. It is in `bank/targets.json` on the V3R1T4S main branch since commit `1359908a` (2026-10-13), and it is unchanged in the version read on 2026-11-27:

> p2: A rigorous proof raising the lower bound on L strictly above 11,486,475 (Egeozturk, forum Aug 2026), rechecked by independent code.

No threshold, statistic or novelty bar of our own was frozen before the computation. The comparison with later public bounds (README.md, Compared to) is made after the fact and is not part of the success rule.

## 2. How the rule is applied

1. **Rigorous proof:** `object/PROOF.md`, every lemma stated and proved, together with the finite computations listed in its Section 9.4, all in exact rational arithmetic.
2. **Raising the bound strictly above 11,486,475:** the proved bound is L >= 6,557,114,959,770,375.
3. **Rechecked by independent code:** two separately written checkers (`verify-it-yourself/check.py`, and `verify-it-yourself/alternate/` with its own arithmetic and its own geometric kernel) recompute every certificate from the files and print `PASS` or `FAIL`; `sh verify-it-yourself/run_checks.sh` runs both and prints `PASS` only if both pass.

## 3. Null model declaration

null_test: not needed, because the claim is a deterministic mathematical theorem with exact integer and rational certificates checked exhaustively, with no statistical or heuristic scoring.
