import Physlib
import V3R1T4SSpec
import V3R1T4SClaim

/-! Bonus (not part of the claim): Physlib's next informal definition `GeorgiGlashow.embedSMℤ₆`
(tag 6V2XA), "the group embedding from `StandardModel.GaugeGroupℤ₆` to `GaugeGroupI` [= SU(5)] induced by
`inclSM` by quotienting by the kernel `inclSM_ker`", built from the proved kernel equality. -/

/-- The map on the quotient `GaugeGroupI ⧸ gaugeGroupℤ₆SubGroup` (= `GaugeGroupℤ₆` by definition). -/
noncomputable def V3R1T4S.KF.embedSMℤ₆' :
    StandardModel.GaugeGroupI ⧸ StandardModel.gaugeGroupℤ₆SubGroup →* V3R1T4S.GaugeGroupGG :=
  QuotientGroup.lift StandardModel.gaugeGroupℤ₆SubGroup V3R1T4S.KF.inclSMHom
    (le_of_eq V3R1T4S.KF.ker_eq.symm)

theorem V3R1T4S.KF.embedSMℤ₆'_injective : Function.Injective V3R1T4S.KF.embedSMℤ₆' := by
  rw [injective_iff_map_eq_one]
  intro a ha
  obtain ⟨x, rfl⟩ := QuotientGroup.mk_surjective a
  rw [V3R1T4S.KF.embedSMℤ₆', QuotientGroup.lift_mk] at ha
  rw [QuotientGroup.eq_one_iff, ← V3R1T4S.KF.ker_eq]
  exact MonoidHom.mem_ker.mpr ha

/-- The same map with domain Physlib's `StandardModel.GaugeGroupℤ₆`. -/
noncomputable def V3R1T4S.KF.embedSMℤ₆ : StandardModel.GaugeGroupℤ₆ →* V3R1T4S.GaugeGroupGG :=
  V3R1T4S.KF.embedSMℤ₆'

theorem V3R1T4S.KF.embedSMℤ₆_injective : Function.Injective V3R1T4S.KF.embedSMℤ₆ :=
  V3R1T4S.KF.embedSMℤ₆'_injective

theorem V3R1T4S.KF.embedSMℤ₆_mk (x : StandardModel.GaugeGroupI) :
    V3R1T4S.KF.embedSMℤ₆ (StandardModel.GaugeGroupℤ₆.mk x) = V3R1T4S.KF.inclSMHom x := rfl

#print axioms V3R1T4S.KF.embedSMℤ₆_injective
#print axioms V3R1T4S.KF.embedSMℤ₆_mk
