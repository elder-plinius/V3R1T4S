# How We Found It (`2026-11-02-rainrat-dcc89550`)

*Contributor text, unverified.*

## 1. The Brief

In the Equational Theories Project (`teorth/equational_theories`), out of `4694 × 4694 = 22,033,636` implications on finite magmas, only two dual implications remain open (`"unknown"`):
- `Equation677 => Equation255`: `x = y ◇ (x ◇ ((y ◇ x) ◇ y))` implies `x = ((x ◇ x) ◇ x) ◇ x`
- `Equation2910 => Equation47`: `x = ((y ◇ (x ◇ y)) ◇ x) ◇ y` implies `x = x ◇ (x ◇ (x ◇ x))`.

We attacked the target with two independent lenses:
1. **`sat-cegar` (Orbit-Case Backtracking & Fiber-Bundle Search)**: Exhaustive search for counterexamples partitioned by the right-multiplication orbit `0 -> 1 -> ... -> k -> s` of an element `0` lacking a fixer (`y ◇ 0 != 0`), plus twisted fiber-bundle search over finite fields.
2. **`formalist` (Algebraic Structure & Lean 4 Formalization)**: Structural analysis of fixed-point sets of left translations `L_y` and right translations `R_x` in finite `Equation677` and `Equation2910` magmas.

## 2. What Failed (Dead Lines)

- **Exhaustive order-11 counterexample search (`p1`)**: Our C++ orbit-case solver (`orbit_solver.cpp`) verified UNSAT for `n = 2..9`, with search nodes growing from `7,631` (`n=7`) to `256,215` (`n=8`, `0.020s`) and `28,540,760` (`n=9`, `1.624s` across 36 orbits). The `~111x` scaling per order projects to `>3.5e11` nodes (`>80` CPU-hours) and multi-hundred-GB DRAT certificates at `n=11`, exceeding both the run kill criteria and the 50 MB package limit.
- **Off-diagonal sign-system twisted bundles over `F_5, F_7, F_9`**: Attempting to build a smaller non-right-cancellative `Equation677` fiber bundle `G × M` over `G in {F_5, F_7, F_9}` using a two-sign off-diagonal partition (`s ◇^+ t = t`, `s ◇^- t = -s - t`) was proved UNSAT by Z3; `G = F_11` with `M = F_5` (order `55 = 11 × 5`) is the smallest base order supporting this construction.

## 3. What Worked

- **Disjointness of Left-Translation Fixed-Point Sets (`eq677_leftMul_fixed_disjoint`)**: Using Blueprint Lemma 13.1(ii) (`eq677_fixer_unique`: `y ◇ x = x → y = (x ◇ x) ◇ x`), if two left translations `L_{y₁}` and `L_{y₂}` fix the same point `x`, then `y₁ = (x ◇ x) ◇ x = y₂`. Thus the fixed-point sets `Fix(L_y)` of distinct left translations are pairwise disjoint!
- **Fixed-Point Conditional Implication (`eq255_of_eq677_leftMul_has_fixed_point`)**: Whenever every left translation `L_y` has at least one fixed point (`EveryLeftMulHasFixedPoint G`), choosing a fixed point `f(y)` for each `y` defines an injective function `f : G → G`, which is surjective by `[Finite G]`. Hence every `x : G` is fixed by some `L_y` and satisfies `Equation255` (and dually `EveryRightMulHasFixedPoint G` implies `Equation47 G` for `Equation2910`).
- **Right-Cancellative / Quasigroup / Left-Cancellative & Faithfulness Theorems**: We also formalized `eq255_of_eq677_right_cancel`, `eq255_of_eq677_quasigroup`, `eq677_leftMul_faithful` (the left-regular representation `y ↦ L_y` is injective in *every* finite `Equation677` magma), `eq255_of_eq677_uniform_leftMul` (Blueprint Lemma 13.3), and the dual `Equation2910 => Equation47` theorems under `LeftCancellative` and `IsQuasigroup`.
- **Two-Sided Separation Witnesses (`Sep7`, `Sep25`, `Sep55`)**:
  - `Sep7` (`Fin 7` with `x ◇ y = (4x + y) mod 7`) satisfies `Equation677`, `RightCancellative`, and Issue #1517's `LeftMulConjugacyClosed`, but violates `EveryLeftMulHasFixedPoint`.
  - `Sep25` (`Fin 25` diagonal-split bundle of two isomorphic order-5 `Equation677` quasigroups swapped on `0 ↔ 1` off the diagonal) satisfies `Equation677`, `RightCancellative` (it is a quasigroup), and `EveryLeftMulHasFixedPoint`, but violates `LeftMulConjugacyClosed`.
  - `Sep55` (`Fin 55` quadratic-residue twisted bundle over `F_11 × F_5`, nearly `9×` smaller than the order-496 example in Blueprint Section 13.1) satisfies `Equation677` and `EveryLeftMulHasFixedPoint`, but violates both `RightCancellative` and `LeftMulConjugacyClosed`.
  All three witnesses and their separation theorems are proved in Lean 4 by kernel `decide`.
