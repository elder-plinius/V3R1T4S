# Skeptic 3 (CRITERION) Audit Report — `etp-finite-magma-677-255` (`p2`)

context: subagent (fresh CRITERION skeptic)
run: `runs/2026-11-01-1637`
target: `etp-finite-magma-677-255`
claim_level: `partial_win_claim` (`p2`)

## 1. Scope & Files Inspected

In accordance with strict scope rules, only the files inside `runs/2026-11-01-1637/claim/` were inspected:
- `claim/target.md`
- `claim/claim.md`
- `claim/REPRODUCE.md`
- `claim/Equation677.lean` (SHA-256 `dcc89550b0e5ce6d4e15f6e283a0401ccdaf9831289189929e67fa48cfebbe7f`, 399 lines)
- `claim/separation_models.json`
- `claim/check_p2.py`
- `claim/status_snapshot.md`
- `claim/lean_build.log`

## 2. Line-by-Line Verification Against Target `p2` Criterion

Verbatim `p2` requirement from `claim/target.md` (line 19):
> `p2`: A Lean proof of the implication under an additional natural hypothesis (e.g. the magma is a quasigroup, or left-cancellative) that is neither implied by nor equivalent to a hypothesis already proved in the ETP issues (e.g. the translation-conjugacy closure of issue #1517), stated as a separate theorem.

### 2.1 Exact ETP Definitions (`equational_theories.Equations.All` and `equational_theories.ManuallyProved.Equation677`)
- **Check**: Does `claim/Equation677.lean` use the exact ETP definitions of `Magma`, `Equation677`, `Equation255`, `Equation2910`, `Equation47`, and `[Finite G]` from `equational_theories.Equations.All` without modifying any existing definition or theorem?
- **Audit**:
  - Lines 1–4 import `equational_theories.Equations.All`, `equational_theories.ManuallyProved.Equation677`, `Mathlib.Data.Fintype.Card`, and `Mathlib.Data.Finite.Prod` directly without duplicating or modifying any upstream lemma.
  - None of `Magma`, `Equation677`, `Equation255`, `Equation2910`, `Equation47`, or `Finite` are redefined, shadowed, or altered anywhere in `claim/Equation677.lean` (verified both by manual inspection and by the regex check in `claim/check_p2.py` line 209).
  - All theorems in `namespace Eq677` (lines 27–132) and `namespace Eq2910` (lines 138–218) are quantified over `variable {G : Type*} [Magma G] [Finite G]` using the upstream ETP definitions and upstream lemmas (`eq677_fixer_unique`, `eq255_from_fixer_exists`, `eq677_leftMul_inj`, `eq677_leftMul_surj`, `eq677_star_eq`, `eq677_left_cancel`).
- **Verdict**: PASS.

### 2.2 Separate Conditional Implication Theorems Under Natural Hypotheses
- **Check**: Are the conditional implications stated as separate theorems under natural hypotheses (`EveryLeftMulHasFixedPoint`, `EveryRightMulHasFixedPoint`, `RightCancellative`, `LeftCancellative`, `IsQuasigroup`, `UniformLeftMul`)?
- **Audit**:
  - Natural algebraic hypotheses are cleanly defined on `(G : Type*) [Magma G]` at lines 32–62 of `claim/Equation677.lean`:
    - `RightCancellative G`: `∀ x : G, Function.Injective (fun y => y ◇ x)` (lines 32–33)
    - `LeftCancellative G`: `∀ x : G, Function.Injective (fun y => x ◇ y)` (lines 36–37)
    - `IsQuasigroup G`: `(∀ x : G, Function.Bijective (fun y => x ◇ y)) ∧ (∀ x : G, Function.Bijective (fun y => y ◇ x))` (lines 40–42)
    - `EveryLeftMulHasFixedPoint G`: `∀ y : G, ∃ x : G, y ◇ x = x` (lines 45–46)
    - `EveryRightMulHasFixedPoint G`: `∀ y : G, ∃ x : G, x ◇ y = x` (lines 49–50)
    - `LeftMulConjugacyClosed G`: `∀ y₁ y₂ : G, ∃ z : G, ∀ x : G, y₂ ◇ (y₁ ◇ x) = y₁ ◇ (z ◇ x)` (lines 55–56)
    - `UniformLeftMul G`: `∀ a b x : G, a ◇ x = b ◇ x → ∀ z : G, a ◇ z = b ◇ z` (lines 61–62)
  - Primary `p2` conditional implication theorem for `Equation677 G → Equation255 G` (under `[Magma G] [Finite G]`):
    - `Eq677.eq255_of_eq677_leftMul_has_fixed_point` (lines 73–85), proved via pairwise disjointness of left-translation fixed-point sets (`Eq677.eq677_leftMul_fixed_disjoint`, lines 66–68) and `Finite.injective_iff_surjective`.
  - Additional conditional implication theorems for `Equation677 G → Equation255 G`:
    - `Eq677.eq255_of_eq677_right_cancel` (lines 89–94)
    - `Eq677.eq255_of_eq677_quasigroup` (lines 107–109, via `eq677_quasigroup_iff_right_cancel` at lines 97–104)
    - `Eq677.eq255_of_eq677_uniform_leftMul` (lines 128–130, via `eq677_leftMul_faithful` at lines 113–118 and `eq677_right_cancel_of_uniform_leftMul` at lines 121–124)
  - Dual conditional implication theorems for `Equation2910 G → Equation47 G` (under `[Magma G] [Finite G]`):
    - `Eq2910.eq47_of_eq2910_rightMul_has_fixed_point` (lines 189–201)
    - `Eq2910.eq47_of_eq2910_left_cancel` (lines 205–210)
    - `Eq2910.eq47_of_eq2910_quasigroup` (lines 214–216)
- **Verdict**: PASS.

### 2.3 Formal Two-Sided Separation Against ETP Issue `#1517` (`LeftMulConjugacyClosed`)
- **Check**: Does the proof formally establish that the natural hypothesis of the primary `p2` claim (`EveryLeftMulHasFixedPoint`) is neither implied by nor equivalent to the translation-conjugacy closure hypothesis (`LeftMulConjugacyClosed`) already proved in ETP Issue `#1517`?
- **Audit**:
  - Because `L_{y₁}` is bijective in any finite `Equation677` magma (`eq677_leftMul_inj`, `eq677_leftMul_surj`), `LeftMulConjugacyClosed G` (`∀ y₁ y₂ : G, ∃ z : G, ∀ x : G, y₂ ◇ (y₁ ◇ x) = y₁ ◇ (z ◇ x)`, lines 55–56) is the exact inverse-free formulation of `L_{y₁}⁻¹ ∘ L_{y₂} ∘ L_{y₁} = L_z` from ETP Issue `#1517` / PR `#1518`.
  - **Witness 1 (`Sep7`, lines 240–265)**: `Fin 7` with `x ◇ y = (4 * x.val + y.val) % 7`.
    - Theorem `Eq677.Separation.not_leftMulHasFixedPoint_of_conjClosed` (lines 260–265) proves by `decide`:
      `∃ (G : Type) (_ : Magma G) (_ : Finite G), Equation677 G ∧ Equation255 G ∧ RightCancellative G ∧ LeftMulConjugacyClosed G ∧ ¬ EveryLeftMulHasFixedPoint G`.
    - This formally proves the **non-implication direction**: `EveryLeftMulHasFixedPoint` is **not implied by** `LeftMulConjugacyClosed` (nor by `RightCancellative` or `Equation255`).
  - **Witness 2 (`Sep25`, lines 268–323)**: `Fin 25` (`5 × 5` diagonal-split quasigroup).
    - Theorem `Eq677.Separation.not_conjClosed_of_rightCancel_and_leftMulHasFixedPoint` (lines 318–323) proves by `decide`:
      `∃ (G : Type) (_ : Magma G) (_ : Finite G), Equation677 G ∧ Equation255 G ∧ RightCancellative G ∧ EveryLeftMulHasFixedPoint G ∧ ¬ LeftMulConjugacyClosed G`.
    - This formally proves the **converse non-implication / non-equivalence direction**: neither `EveryLeftMulHasFixedPoint` nor `RightCancellative` (nor `IsQuasigroup`) implies `LeftMulConjugacyClosed`.
  - **Witness 3 (`Sep55`, lines 326–384)**: `Fin 55` (`11 × 5` quadratic-residue twisted fiber bundle).
    - Theorem `Eq677.Separation.not_rightCancel_and_not_conjClosed_of_leftMulHasFixedPoint` (lines 378–384) proves by `decide`:
      `∃ (G : Type) (_ : Magma G) (_ : Finite G), Equation677 G ∧ Equation255 G ∧ EveryLeftMulHasFixedPoint G ∧ ¬ RightCancellative G ∧ ¬ LeftMulConjugacyClosed G`.
    - Combined with `Sep7`, this establishes unconditional **two-sided logical independence** of `EveryLeftMulHasFixedPoint` from both `LeftMulConjugacyClosed` (Issue `#1517`) and `RightCancellative`: neither implies `EveryLeftMulHasFixedPoint` (`Sep7`), and `EveryLeftMulHasFixedPoint` implies neither (`Sep55`).
  - **Scoping of `RightCancellative` / `IsQuasigroup` / `UniformLeftMul`**: `claim/claim.md` (lines 5–6, 23–43) accurately scopes the primary `p2` claim to `EveryLeftMulHasFixedPoint` (where both non-implication and non-equivalence against `LeftMulConjugacyClosed` and `RightCancellative` are unconditionally proved) and explicitly notes that for the additional conditional implication theorems under `RightCancellative` / `IsQuasigroup`, `Sep25` proves non-implication in one direction (`RightCancellative` does not imply `LeftMulConjugacyClosed`, hence non-equivalence), while whether `LeftMulConjugacyClosed` implies `RightCancellative` on finite `Equation677` magmas remains open.
  - Running `python3 runs/2026-11-01-1637/claim/check_p2.py` independently verified all Cayley tables in `claim/separation_models.json`, their exact cell-by-cell agreement with `Sep7`, `Sep25`, and `Sep55` in `claim/Equation677.lean`, all separation properties for both `Equation677 => Equation255` and the opposite dual `Equation2910 => Equation47`, and all exact Lean snippets.
- **Verdict**: PASS.

### 2.4 Soundness, Forbidden Tactics, and Axiom Audit
- **Check**: Are there any `sorry`, `admit`, `native_decide`, or non-standard axioms beyond `[propext, Classical.choice, Quot.sound]`?
- **Audit**:
  - Full inspection of `claim/Equation677.lean` (lines 1–399) and automated verification via `claim/check_p2.py` confirm zero occurrences of `sorry`, `admit`, `native_decide`, or custom `axiom` declarations. All finite decidability proofs (`Sep7`, `Sep25`, `Sep55`) use standard kernel-checked `decide`.
  - `claim/lean_build.log` records clean compilation of all 12 `#print axioms` declarations at lines 388–399 of `claim/Equation677.lean`, with every theorem depending exclusively on `[propext, Classical.choice, Quot.sound]`.
- **Verdict**: PASS.

## 3. Conclusion

All criteria for partial win `p2` of `etp-finite-magma-677-255` in `claim/target.md` are rigorously satisfied.

pass: true
