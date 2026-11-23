# Pre-Registration: `alternating-prm-plus-ergodic-convergence`

frozen_utc: 2026-11-16T14:40:00Z
target_id: alternating-prm-plus-ergodic-convergence
null_test: not needed because kernel-checked formal proof in Lean 4

## Verbatim Gates

1. Formalize Algorithms 1, 2, 7, and 8 and `caiGameA = [[3,0,-3],[0,3,-4],[0,0,1]]` verbatim from `arXiv:2311.00676v2` (`PRMPlus/Defs.lean`), cross-checked against IEEE-754 `float64` and 80-digit `Decimal` at `t = 1000`.
2. Prove in Lean 4 (`0` `sorry`, `0` `admit`, `0` `native_decide`, `#print axioms` subset of `{propext, Classical.choice, Quot.sound}`) that Simultaneous PRM+ (`alg2Iter`) from `R = 0` and uniform `(1/3, 1/3, 1/3)` has `0 < liminf_{t -> inf} DualGap caiGameA x^t y^t` (`p2`).
