import Physlib
import V3R1T4SSpec

/-! Fidelity witnesses for the frozen spec (not part of the candidate):
1. `inclSMMatrix x` written out as an explicit 5 × 5 matrix: `blockdiag (α ^ 3 g, α ^ (-2) h)` with the
   `2 × 2` block on indices 0, 1 and the `3 × 3` block on indices 2, 3, 4; `α⁻¹ ^ 2 = α ^ (-2 : ℤ)`.
2. The kernel subgroup is nontrivial: `gaugeGroupℤ₆OfRoot (-1) ≠ 1` (so the statement is not about `⊥`). -/

open Matrix

example (x : StandardModel.GaugeGroupI) :
    let a : ℂ := (x.2.2 : ℂ)
    let g : Matrix (Fin 2) (Fin 2) ℂ := x.2.1
    let h : Matrix (Fin 3) (Fin 3) ℂ := x.1
    V3R1T4S.inclSMMatrix x =
      !![a ^ 3 * g 0 0, a ^ 3 * g 0 1, 0, 0, 0;
         a ^ 3 * g 1 0, a ^ 3 * g 1 1, 0, 0, 0;
         0, 0, a ^ (-2 : ℤ) * h 0 0, a ^ (-2 : ℤ) * h 0 1, a ^ (-2 : ℤ) * h 0 2;
         0, 0, a ^ (-2 : ℤ) * h 1 0, a ^ (-2 : ℤ) * h 1 1, a ^ (-2 : ℤ) * h 1 2;
         0, 0, a ^ (-2 : ℤ) * h 2 0, a ^ (-2 : ℤ) * h 2 1, a ^ (-2 : ℤ) * h 2 2] := by
  intro a g h
  have hz : a ^ (-2 : ℤ) = a⁻¹ ^ 2 := by
    rw [_root_.zpow_neg, zpow_ofNat, inv_pow]
  rw [hz]
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

/-- `-1` as a sixth root of unity. -/
noncomputable def negOneRoot : rootsOfUnity 6 ℂ := rootsOfUnity.mkOfPowEq (-1 : ℂ) (by norm_num)

example : StandardModel.gaugeGroupℤ₆OfRoot negOneRoot ≠ 1 := by
  intro h
  have h3 := congrArg (fun y : StandardModel.GaugeGroupI => ((y.2.2 : unitary ℂ) : ℂ)) h
  simp [StandardModel.gaugeGroupℤ₆OfRoot, negOneRoot] at h3
  norm_num at h3
