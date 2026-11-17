import Physlib

/-! Frozen statement for physlib-gut-kernel-z6: Physlib's informal lemma `GeorgiGlashow.inclSM_ker` (tag 6V2W2),
"The kernel of the map `inclSM` is equal to the subgroup `StandardModel.gaugeGroupℤ₆SubGroup`", with the informal
definitions it depends on made formal exactly as their docstrings say
(Physlib/Particles/BeyondTheStandardModel/GeorgiGlashow/Basic.lean, status page fetched 2026-10-14T06:16:29Z):
- `GaugeGroupI` (tag 6V2WM): "The gauge group of the Georgi-Glashow model, i.e., `SU(5)`."
- `inclSM` (tag 6V2WS): "the group homomorphism `SU(3) × SU(2) × U(1) → SU(5)` taking `(h, g, α)` to
  `blockdiag (α ^ 3 g, α ^ (-2) h)`."
Physlib's `StandardModel.GaugeGroupI` is `SU(3) × SU(2) × U(1)` in that order, so for `x = (h, g, α)`:
`x.1 = h ∈ SU(3)`, `x.2.1 = g ∈ SU(2)`, `x.2.2 = α ∈ U(1)`. The block-diagonal matrix puts the `2 × 2` block
`α³ g` on indices `0, 1` and the `3 × 3` block `α⁻² h` on indices `2, 3, 4` (via `finSumFinEquiv`).
The claim: some group homomorphism `StandardModel.GaugeGroupI →* SU(5)` has exactly these matrices as values,
and its kernel is `StandardModel.gaugeGroupℤ₆SubGroup`. -/

/-- `SU(5)`, the Georgi-Glashow gauge group. -/
abbrev V3R1T4S.GaugeGroupGG : Type := Matrix.specialUnitaryGroup (Fin 5) ℂ

/-- The matrix `blockdiag (α ^ 3 g, α ^ (-2) h)` for `x = (h, g, α)`. -/
noncomputable def V3R1T4S.inclSMMatrix (x : StandardModel.GaugeGroupI) : Matrix (Fin 5) (Fin 5) ℂ :=
  Matrix.reindex finSumFinEquiv finSumFinEquiv
    (Matrix.fromBlocks (((x.2.2 : ℂ) ^ 3) • (x.2.1 : Matrix (Fin 2) (Fin 2) ℂ)) 0 0
      (((x.2.2 : ℂ)⁻¹ ^ 2) • (x.1 : Matrix (Fin 3) (Fin 3) ℂ)))

def V3R1T4S.spec : Prop :=
  ∃ f : StandardModel.GaugeGroupI →* V3R1T4S.GaugeGroupGG,
    (∀ x, (f x : Matrix (Fin 5) (Fin 5) ℂ) = V3R1T4S.inclSMMatrix x) ∧
    f.ker = StandardModel.gaugeGroupℤ₆SubGroup
