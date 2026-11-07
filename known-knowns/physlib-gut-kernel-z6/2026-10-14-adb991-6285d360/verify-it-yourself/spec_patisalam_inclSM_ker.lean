import Physlib

/-! Frozen statement for Physlib's informal lemma `PatiSalam.inclSM_ker` (tag 6V2RQ), "The kernel of the map
`inclSM` is equal to the subgroup `StandardModel.gaugeGroupℤ₃SubGroup`", with the informal definitions it depends on
made formal exactly as their docstrings say (Physlib/Particles/BeyondTheStandardModel/PatiSalam/Basic.lean):
- `GaugeGroupI` (tag 6V2Q2): "The gauge group of the Pati-Salam model (unquotiented by ℤ₂), i.e.,
  `SU(4) × SU(2) × SU(2)`."
- `inclSM` (tag 6V2RH): "the group homomorphism `SU(3) × SU(2) × U(1) → SU(4) × SU(2) × SU(2)` taking `(h, g, α)` to
  `(blockdiag (α h, α ^ (-3)), g, diag (α ^ 3, α ^(-3))`."
Physlib's `StandardModel.GaugeGroupI` is `SU(3) × SU(2) × U(1)`, so for `x = (h, g, α)`: `x.1 = h`, `x.2.1 = g`,
`x.2.2 = α`. The `4 × 4` block-diagonal matrix puts `α h` on indices `0, 1, 2` and `α⁻³` on index `3`
(via `finSumFinEquiv`). The claim: some group homomorphism with exactly these three components has kernel
`StandardModel.gaugeGroupℤ₃SubGroup`. -/

/-- `SU(4) × SU(2) × SU(2)`, the (unquotiented) Pati-Salam gauge group. -/
abbrev V3R1T4S.GaugeGroupPS : Type :=
  Matrix.specialUnitaryGroup (Fin 4) ℂ × Matrix.specialUnitaryGroup (Fin 2) ℂ ×
    Matrix.specialUnitaryGroup (Fin 2) ℂ

/-- `blockdiag (α h, α ^ (-3))` for `x = (h, g, α)`. -/
noncomputable def V3R1T4S.psMatrix4 (x : StandardModel.GaugeGroupI) : Matrix (Fin 4) (Fin 4) ℂ :=
  Matrix.reindex finSumFinEquiv finSumFinEquiv
    (Matrix.fromBlocks ((x.2.2 : ℂ) • (x.1 : Matrix (Fin 3) (Fin 3) ℂ)) 0 0
      (((x.2.2 : ℂ)⁻¹ ^ 3) • (1 : Matrix (Fin 1) (Fin 1) ℂ)))

/-- `diag (α ^ 3, α ^ (-3))` for `x = (h, g, α)`. -/
noncomputable def V3R1T4S.psMatrixR (x : StandardModel.GaugeGroupI) : Matrix (Fin 2) (Fin 2) ℂ :=
  Matrix.diagonal ![(x.2.2 : ℂ) ^ 3, (x.2.2 : ℂ)⁻¹ ^ 3]

def V3R1T4S.spec : Prop :=
  ∃ f : StandardModel.GaugeGroupI →* V3R1T4S.GaugeGroupPS,
    (∀ x, ((f x).1 : Matrix (Fin 4) (Fin 4) ℂ) = V3R1T4S.psMatrix4 x ∧
      ((f x).2.1 : Matrix (Fin 2) (Fin 2) ℂ) = (x.2.1 : Matrix (Fin 2) (Fin 2) ℂ) ∧
      ((f x).2.2 : Matrix (Fin 2) (Fin 2) ℂ) = V3R1T4S.psMatrixR x) ∧
    f.ker = StandardModel.gaugeGroupℤ₃SubGroup
