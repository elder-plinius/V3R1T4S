module

public import APAP.Prereqs.Bohr.Regular
public import APAP.Prereqs.Convolution.Discrete.Defs
public import APAP.Prereqs.LpNorm.Discrete.Defs
public import APAP.Prereqs.Mu
public import Mathlib.Algebra.Field.ZMod

import AddCombi.Mathlib.Algebra.Order.GroupWithZero.Indicator
import APAP.Mathlib.Analysis.Normed.Ring.Basic
import APAP.Prereqs.Convolution.Discrete.Basic
import APAP.Prereqs.Convolution.Norm
import APAP.Prereqs.LpNorm.Discrete.Basic
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# Basic properties of regular Bohr sets, size bounds, Lipschitz weights, and Bourgain's trick
-/

@[expose] public section

open AddChar Complex Finset Function MeasureTheory Real
open scoped NNReal ENNReal BigOperators Pointwise Indicator translate mu

section ConvNonneg
variable {G R : Type*} [Fintype G] [DecidableEq G] [AddCommGroup G]

lemma ddconv_apply_nonneg' [CommSemiring R] [PartialOrder R] [IsOrderedRing R] {f g : G → R}
    (hf : 0 ≤ f) (hg : 0 ≤ g) (a : G) : 0 ≤ (f ∗ᵈ g) a := by
  rw [ddconv_eq_sum_sub']
  exact sum_nonneg fun _ _ ↦ mul_nonneg (hf _) (hg _)

lemma ddconv_nonneg' [CommSemiring R] [PartialOrder R] [IsOrderedRing R] {f g : G → R}
    (hf : 0 ≤ f) (hg : 0 ≤ g) : 0 ≤ f ∗ᵈ g :=
  fun a ↦ ddconv_apply_nonneg' hf hg a

lemma dddconv_apply_nonneg' {f g : G → ℝ} (hf : 0 ≤ f) (hg : 0 ≤ g) (a : G) :
    0 ≤ (f ○ᵈ g) a := by
  rw [← ddconv_conjneg]
  exact ddconv_apply_nonneg' hf (fun x ↦ by rw [conjneg_apply, conj_trivial]; exact hg (-x)) a

lemma dddconv_nonneg' {f g : G → ℝ} (hf : 0 ≤ f) (hg : 0 ≤ g) : 0 ≤ f ○ᵈ g :=
  fun a ↦ dddconv_apply_nonneg' hf hg a

lemma support_dddconv_subset' [CommRing R] [StarRing R] (f g : G → R) :
    support (f ○ᵈ g) ⊆ support f - support g := by
  rw [← ddconv_conjneg]
  refine (support_ddconv_subset f (conjneg g)).trans ?_
  intro x hx
  rcases hx with ⟨a, ha, b, hb, rfl⟩
  refine ⟨a, ha, -b, ?_, by abel_nf⟩
  simpa [conjneg_apply] using hb

end ConvNonneg

namespace BohrSet

section NoFiniteAPI
variable {G : Type*} [AddCommGroup G]

lemma smul_le_smul_of_le {B : BohrSet G} {ρ₁ ρ₂ : ℝ} (h₀ : 0 ≤ ρ₁) (h : ρ₁ ≤ ρ₂) :
    ρ₁ • B ≤ ρ₂ • B := by
  intro ψ
  simp only [ewidth_smul]
  split_ifs with hψ
  · gcongr
    rw [Real.nnabs_of_nonneg h₀, Real.nnabs_of_nonneg (h₀.trans h)]
    exact Real.toNNReal_mono h
  · exact le_rfl

@[simp] lemma top_chordSet : (⊤ : BohrSet G).chordSet = Set.univ := by
  ext x
  simp only [Set.mem_univ, iff_true, mem_chordSet_iff_nnnorm_ewidth]
  intro ψ
  exact le_top

@[simp] lemma top_rank : (⊤ : BohrSet G).rank = 0 := by
  change #(⊤ : BohrSet G).frequencies = 0
  simp [Top.top]

lemma smul_top (ρ : ℝ) : ρ • (⊤ : BohrSet G) = ⊤ := by
  apply ewidth_injective
  ext ψ
  simp [Top.top]


/-- All active frequencies of `B` have strictly positive width. -/
def PosWidth (B : BohrSet G) : Prop := ∀ ψ ∈ B.frequencies, 0 < B.width ψ

lemma posWidth_top : (⊤ : BohrSet G).PosWidth := fun _ h ↦ by simp [Top.top] at h

lemma PosWidth.smul {B : BohrSet G} (hB : B.PosWidth) {ρ : ℝ} (hρ : ρ ≠ 0) :
    (ρ • B).PosWidth := by
  intro ψ hψ
  rw [frequencies_smul] at hψ
  rw [width_smul_apply]
  exact mul_pos (by simpa using hρ) (hB ψ hψ)

lemma posWidth_ofWidth {Γ : Finset (AddChar G ℂ)} {δ : ℝ≥0} (hδ : 0 < δ) :
    (ofWidth (fun _ ↦ δ) Γ).PosWidth := by
  intro ψ hψ
  simp only [ofWidth, width_def] at hψ ⊢
  simp [hψ, hδ]

lemma PosWidth.inf {B₁ B₂ : BohrSet G} (h₁ : B₁.PosWidth) (h₂ : B₂.PosWidth) :
    (B₁ ⊓ B₂).PosWidth := by
  intro ψ hψ
  change ψ ∈ B₁.frequencies ∪ B₂.frequencies at hψ
  rw [width_def]
  change 0 < (B₁.ewidth ψ ⊓ B₂.ewidth ψ).toNNReal
  rcases Finset.mem_union.mp hψ with hψ₁ | hψ₂
  · by_cases hψ₂' : ψ ∈ B₂.frequencies
    · rw [← coe_width hψ₁, ← coe_width hψ₂', ← ENNReal.coe_min, ENNReal.toNNReal_coe]
      exact lt_min (h₁ ψ hψ₁) (h₂ ψ hψ₂')
    · rw [ewidth_eq_top_of_not_mem_frequencies hψ₂', inf_top_eq]
      exact h₁ ψ hψ₁
  · by_cases hψ₁' : ψ ∈ B₁.frequencies
    · rw [← coe_width hψ₁', ← coe_width hψ₂, ← ENNReal.coe_min, ENNReal.toNNReal_coe]
      exact lt_min (h₁ ψ hψ₁') (h₂ ψ hψ₂)
    · rw [ewidth_eq_top_of_not_mem_frequencies hψ₁', top_inf_eq]
      exact h₂ ψ hψ₂

lemma rank_inf_ofWidth_le (X : BohrSet G) (Γ : Finset (AddChar G ℂ)) (w : AddChar G ℂ → ℝ≥0) :
    (X ⊓ ofWidth w Γ).rank ≤ X.rank + #Γ := by
  classical
  change #(X.frequencies ∪ Γ) ≤ #X.frequencies + #Γ
  exact Finset.card_union_le _ _

/-- The Bohr gauge `sup_{ψ ∈ B.frequencies} ‖1 - ψ x‖ / B.width ψ`. -/
noncomputable def bohrNorm (B : BohrSet G) (x : G) : ℝ≥0 :=
  B.frequencies.sup fun ψ ↦ ‖1 - ψ x‖₊ / B.width ψ

@[simp] lemma bohrNorm_zero (B : BohrSet G) : B.bohrNorm 0 = 0 := by simp [bohrNorm]

/-- Smooth Lipschitz Bohr weight equal to `1` on `B` and decaying exponentially outside `B`. -/
noncomputable def bohrWeight (B : BohrSet G) (x : G) : ℝ :=
  Real.exp (-1000 * (B.rank : ℝ) ^ 2 * max 0 ((B.bohrNorm x : ℝ) - 1))

lemma bohrWeight_pos (B : BohrSet G) (x : G) : 0 < B.bohrWeight x := Real.exp_pos _

lemma bohrWeight_le_one (B : BohrSet G) (x : G) : B.bohrWeight x ≤ 1 := by
  unfold bohrWeight
  apply Real.exp_le_one_iff.mpr
  have h1 : 0 ≤ max 0 ((B.bohrNorm x : ℝ) - 1) := le_max_left _ _
  have h2 : 0 ≤ (1000 : ℝ) * (B.rank : ℝ) ^ 2 := by positivity
  nlinarith

end NoFiniteAPI

section FiniteAPI
variable {G : Type*} [AddCommGroup G] [Finite G]

/-- The `Finset G` of elements of a Bohr set `B` on a finite group. -/
noncomputable def finset (B : BohrSet G) : Finset G :=
  open scoped Classical in
  let _ : Fintype G := Fintype.ofFinite G
  B.chordSet.toFinset

@[simp] lemma mem_finset {B : BohrSet G} {x : G} : x ∈ B.finset ↔ x ∈ B.chordSet := by
  classical
  let _ : Fintype G := Fintype.ofFinite G
  unfold finset
  convert Set.mem_toFinset (s := B.chordSet)

@[simp] lemma coe_finset (B : BohrSet G) : (B.finset : Set G) = B.chordSet := by
  ext x; simp

lemma card_finset (B : BohrSet G) : #B.finset = Nat.card B := by
  classical
  let _ : Fintype G := Fintype.ofFinite G
  have hsub : B.finset = B.chordSet.toFinset := by ext x; simp
  rw [hsub, Set.toFinset_card, ← Nat.card_eq_fintype_card]

@[simp] lemma zero_mem_finset (B : BohrSet G) : (0 : G) ∈ B.finset := by simp

lemma finset_nonempty (B : BohrSet G) : B.finset.Nonempty := ⟨0, B.zero_mem_finset⟩

lemma card_finset_pos (B : BohrSet G) : 0 < #B.finset := B.finset_nonempty.card_pos

@[simp] lemma neg_mem_finset {B : BohrSet G} {x : G} : -x ∈ B.finset ↔ x ∈ B.finset := by
  simp

@[simp] lemma neg_finset [DecidableEq G] (B : BohrSet G) : -B.finset = B.finset := by
  ext x; simp

lemma finset_mono {B₁ B₂ : BohrSet G} (h : B₁ ≤ B₂) : B₁.finset ⊆ B₂.finset := by
  intro x hx
  exact mem_finset.mpr (chordSet_mono h (mem_finset.mp hx))

lemma smul_finset_mono {B : BohrSet G} {ρ₁ ρ₂ : ℝ} (h₀ : 0 ≤ ρ₁) (h : ρ₁ ≤ ρ₂) :
    (ρ₁ • B).finset ⊆ (ρ₂ • B).finset :=
  finset_mono (smul_le_smul_of_le h₀ h)

lemma smul_add_smul_finset_subset [DecidableEq G] {B : BohrSet G} {ρ₁ ρ₂ : ℝ}
    (h₁ : 0 ≤ ρ₁) (h₂ : 0 ≤ ρ₂) :
    (ρ₁ • B).finset + (ρ₂ • B).finset ⊆ ((ρ₁ + ρ₂) • B).finset := by
  rw [← coe_subset, Finset.coe_add, coe_finset, coe_finset, coe_finset]
  exact smul_add_smul_subset h₁ h₂


@[simp] lemma bohrNorm_neg (B : BohrSet G) (x : G) : B.bohrNorm (-x) = B.bohrNorm x := by
  unfold bohrNorm
  congr 1 with ψ
  have : ‖1 - ψ (-x)‖₊ = ‖1 - ψ x‖₊ := by
    rw [← RCLike.nnNorm_conj, map_sub, map_one, map_neg_eq_conj, RCLike.conj_conj]
  rw [this]

lemma bohrNorm_add_le (B : BohrSet G) (x y : G) :
    B.bohrNorm (x + y) ≤ B.bohrNorm x + B.bohrNorm y := by
  unfold bohrNorm
  refine Finset.sup_le fun ψ hψ ↦ ?_
  by_cases hw : B.width ψ = 0
  · simp [hw]
  · have htri : ‖1 - ψ (x + y)‖₊ ≤ ‖1 - ψ x‖₊ + ‖1 - ψ y‖₊ := by
      rw [map_add_eq_mul]
      exact nnnorm_one_sub_mul (by simp)
    calc
      ‖1 - ψ (x + y)‖₊ / B.width ψ
        ≤ (‖1 - ψ x‖₊ + ‖1 - ψ y‖₊) / B.width ψ := by gcongr
      _ = ‖1 - ψ x‖₊ / B.width ψ + ‖1 - ψ y‖₊ / B.width ψ := add_div _ _ _
      _ ≤ B.bohrNorm x + B.bohrNorm y :=
        add_le_add (Finset.le_sup (f := fun ψ ↦ ‖1 - ψ x‖₊ / B.width ψ) hψ)
          (Finset.le_sup (f := fun ψ ↦ ‖1 - ψ y‖₊ / B.width ψ) hψ)

lemma abs_bohrNorm_sub_le (B : BohrSet G) (u y : G) :
    |(B.bohrNorm (u - y) : ℝ) - B.bohrNorm u| ≤ B.bohrNorm y := by
  have h1 : B.bohrNorm (u - y) ≤ B.bohrNorm u + B.bohrNorm y := by
    simpa [sub_eq_add_neg] using B.bohrNorm_add_le u (-y)
  have h2 : B.bohrNorm u ≤ B.bohrNorm (u - y) + B.bohrNorm y := by
    have := B.bohrNorm_add_le (u - y) y
    simpa [sub_add_cancel] using this
  have h1' : (B.bohrNorm (u - y) : ℝ) ≤ B.bohrNorm u + B.bohrNorm y := by exact_mod_cast h1
  have h2' : (B.bohrNorm u : ℝ) ≤ B.bohrNorm (u - y) + B.bohrNorm y := by exact_mod_cast h2
  exact abs_le.mpr ⟨by linarith, by linarith⟩

lemma bohrNorm_le_iff_mem_smul {B : BohrSet G} (hB : B.PosWidth) {t : ℝ} (ht : 0 ≤ t) (x : G) :
    (B.bohrNorm x : ℝ) ≤ t ↔ x ∈ (t • B).finset := by
  let t' : ℝ≥0 := ⟨t, ht⟩
  have ht_eq : Real.nnabs t = t' := by
    rw [Real.nnabs_of_nonneg ht]
    ext
    exact Real.coe_toNNReal t ht
  rw [mem_finset, mem_chordSet_iff_nnnorm_width]
  change (B.bohrNorm x : ℝ) ≤ (t' : ℝ) ↔ _
  rw [NNReal.coe_le_coe, bohrNorm, Finset.sup_le_iff]
  refine forall_congr' fun ψ ↦ ?_
  simp only [frequencies_smul, width_smul_apply, ht_eq]
  refine imp_congr_right fun hψ ↦ ?_
  exact div_le_iff₀ (hB ψ hψ)

lemma bohrWeight_eq_one_of_mem {B : BohrSet G} (hB : B.PosWidth) {x : G} (hx : x ∈ B.finset) :
    B.bohrWeight x = 1 := by
  have hle : (B.bohrNorm x : ℝ) ≤ 1 := by
    rw [bohrNorm_le_iff_mem_smul hB zero_le_one, one_smul]
    exact hx
  have hmax : max 0 ((B.bohrNorm x : ℝ) - 1) = 0 := max_eq_left (by linarith)
  simp [bohrWeight, hmax]

lemma abs_bohrWeight_sub_le {B : BohrSet G} (hB : B.PosWidth) {ρ : ℝ} (hρ : 0 ≤ ρ)
    {y : G} (hy : y ∈ (ρ • B).finset) (u : G) :
    |B.bohrWeight (u - y) - B.bohrWeight u| ≤
      (Real.exp (1000 * (B.rank : ℝ) ^ 2 * ρ) - 1) * B.bohrWeight u := by
  have hy_norm : (B.bohrNorm y : ℝ) ≤ ρ := (bohrNorm_le_iff_mem_smul hB hρ y).mpr hy
  let m₁ : ℝ := max 0 ((B.bohrNorm (u - y) : ℝ) - 1)
  let m₂ : ℝ := max 0 ((B.bohrNorm u : ℝ) - 1)
  have hm_diff : |m₁ - m₂| ≤ ρ := by
    have hlip := abs_max_sub_max_le_max (0 : ℝ) ((B.bohrNorm (u - y) : ℝ) - 1) 0
      ((B.bohrNorm u : ℝ) - 1)
    simp only [sub_self, abs_zero, sub_sub_sub_cancel_right] at hlip
    exact hlip.trans ((max_eq_right (abs_nonneg _)).trans_le
      ((B.abs_bohrNorm_sub_le u y).trans hy_norm))
  set δ : ℝ := 1000 * (B.rank : ℝ) ^ 2 * ρ
  set a : ℝ := 1000 * (B.rank : ℝ) ^ 2 * m₁
  set b : ℝ := 1000 * (B.rank : ℝ) ^ 2 * m₂
  have ha_eq : B.bohrWeight (u - y) = Real.exp (-a) := by
    unfold bohrWeight; congr 1; dsimp [a, m₁]; ring
  have hb_eq : B.bohrWeight u = Real.exp (-b) := by
    unfold bohrWeight; congr 1; dsimp [b, m₂]; ring
  rw [ha_eq, hb_eq]
  have hab : |a - b| ≤ δ := by
    have : a - b = 1000 * (B.rank : ℝ) ^ 2 * (m₁ - m₂) := by dsimp [a, b]; ring
    rw [this, abs_mul, abs_of_nonneg (by positivity)]
    exact mul_le_mul_of_nonneg_left hm_diff (by positivity)
  rcases le_total a b with hle | hle
  · have hba : b - a ≤ δ := (le_abs_self _).trans (by rwa [abs_sub_comm])
    have hexp_le : Real.exp (-b) ≤ Real.exp (-a) := Real.exp_le_exp.mpr (by linarith)
    rw [abs_of_nonneg (sub_nonneg.mpr hexp_le)]
    have hrew : Real.exp (-a) - Real.exp (-b) = (Real.exp (b - a) - 1) * Real.exp (-b) := by
      rw [sub_mul, one_mul, ← Real.exp_add]
      ring_nf
    rw [hrew]
    exact mul_le_mul_of_nonneg_right (by linarith [Real.exp_le_exp.mpr hba])
      (Real.exp_pos _).le
  · have hab' : a - b ≤ δ := (le_abs_self _).trans hab
    have hexp_le : Real.exp (-a) ≤ Real.exp (-b) := Real.exp_le_exp.mpr (by linarith)
    rw [abs_sub_comm, abs_of_nonneg (sub_nonneg.mpr hexp_le)]
    have hrew : Real.exp (-b) - Real.exp (-a) = (1 - Real.exp (-(a - b))) * Real.exp (-b) := by
      rw [sub_mul, one_mul, ← Real.exp_add]
      ring_nf
    rw [hrew]
    refine mul_le_mul_of_nonneg_right ?_ (Real.exp_pos _).le
    have h1 : 1 - Real.exp (-(a - b)) ≤ a - b := by
      linarith [Real.add_one_le_exp (-(a - b))]
    have h2 : δ ≤ Real.exp δ - 1 := by
      linarith [Real.add_one_le_exp δ]
    linarith

lemma bohrWeight_sub_le_mul {B : BohrSet G} (hB : B.PosWidth) {ρ : ℝ} (hρ : 0 ≤ ρ)
    {y : G} (hy : y ∈ (ρ • B).finset) (u : G) :
    B.bohrWeight (u - y) ≤ Real.exp (1000 * (B.rank : ℝ) ^ 2 * ρ) * B.bohrWeight u := by
  have h := abs_bohrWeight_sub_le hB hρ hy u
  have h1 : B.bohrWeight (u - y) - B.bohrWeight u ≤
      (Real.exp (1000 * (B.rank : ℝ) ^ 2 * ρ) - 1) * B.bohrWeight u := (le_abs_self _).trans h
  linarith

private lemma norm_exp_mul_I_sub_one_sq' (t : ℝ) :
    ‖Complex.exp (t * I) - 1‖ ^ 2 = 4 * Real.sin (t / 2) ^ 2 := by
  rw [Complex.exp_mul_I, ← Complex.normSq_eq_norm_sq]
  have hre : (Complex.cos t + Complex.sin t * I - 1).re = Real.cos t - 1 := by
    simp [Complex.cos_ofReal_re, Complex.sin_ofReal_im]
  have him : (Complex.cos t + Complex.sin t * I - 1).im = Real.sin t := by
    simp [Complex.cos_ofReal_im, Complex.sin_ofReal_re]
  rw [Complex.normSq_apply, hre, him]
  have htwo : 2 * (t / 2) = t := by ring
  have h2 := Real.cos_two_mul' (t / 2)
  rw [htwo] at h2
  nlinarith [Real.cos_sq_add_sin_sq t, Real.cos_sq_add_sin_sq (t / 2)]

private lemma norm_exp_mul_I_sub_exp_mul_I_le' (a b : ℝ) :
    ‖Complex.exp (a * I) - Complex.exp (b * I)‖ ≤ |a - b| := by
  have hmul : Complex.exp (a * I) - Complex.exp (b * I) =
      Complex.exp (b * I) * (Complex.exp (((a - b : ℝ) : ℂ) * I) - 1) := by
    rw [mul_sub, mul_one, ← Complex.exp_add]
    congr 1
    rw [Complex.ofReal_sub, sub_mul, add_sub_cancel]
  rw [hmul, norm_mul, Complex.norm_exp_ofReal_mul_I, one_mul]
  have hsq : ‖Complex.exp (((a - b : ℝ) : ℂ) * I) - 1‖ ^ 2 ≤ |a - b| ^ 2 := by
    rw [norm_exp_mul_I_sub_one_sq' (a - b), ← sq_abs (Real.sin ((a - b) / 2))]
    have hsin : |Real.sin ((a - b) / 2)| ≤ |(a - b) / 2| := Real.abs_sin_le_abs
    have hpos : 0 ≤ |Real.sin ((a - b) / 2)| := abs_nonneg _
    have habs : |(a - b) / 2| = |a - b| / 2 := by simp [abs_div]
    rw [habs] at hsin
    nlinarith
  nlinarith [norm_nonneg (Complex.exp (((a - b : ℝ) : ℂ) * I) - 1), abs_nonneg (a - b)]

private lemma abs_arg_le_pi_div_two_mul_norm_one_sub' {z : ℂ} (hz : ‖z‖ = 1) :
    |z.arg| ≤ (Real.pi / 2) * ‖1 - z‖ := by
  have hzeq : Complex.exp (z.arg * I) = z := by
    simpa [hz] using Complex.norm_mul_exp_arg_mul_I z
  have hnorm : ‖1 - z‖ ^ 2 = 4 * Real.sin (|z.arg| / 2) ^ 2 := by
    calc
      ‖1 - z‖ ^ 2 = ‖Complex.exp (z.arg * I) - 1‖ ^ 2 := by rw [hzeq, norm_sub_rev]
      _ = 4 * Real.sin (z.arg / 2) ^ 2 := norm_exp_mul_I_sub_one_sq' z.arg
      _ = 4 * Real.sin (|z.arg| / 2) ^ 2 := by
        rcases le_total 0 z.arg with h0 | h0
        · rw [abs_of_nonneg h0]
        · have : |z.arg| / 2 = -(z.arg / 2) := by rw [abs_of_nonpos h0]; ring
          rw [this, Real.sin_neg, neg_sq]
  have hu0 : 0 ≤ |z.arg| / 2 := by positivity
  have hu1 : |z.arg| / 2 ≤ Real.pi / 2 := by
    have := Complex.abs_arg_le_pi z
    linarith
  have hsin := Real.mul_le_sin hu0 hu1
  have hpi : 0 < Real.pi := Real.pi_pos
  have hsq : ((2 / Real.pi) * |z.arg|) ^ 2 ≤ ‖1 - z‖ ^ 2 := by
    rw [hnorm]
    have : (2 / Real.pi) * |z.arg| = 2 * ((2 / Real.pi) * (|z.arg| / 2)) := by ring
    rw [this]
    nlinarith [show 0 ≤ (2 / Real.pi) * (|z.arg| / 2) by positivity]
  have hle : (2 / Real.pi) * |z.arg| ≤ ‖1 - z‖ := by
    nlinarith [norm_nonneg (1 - z), show 0 ≤ (2 / Real.pi) * |z.arg| by positivity]
  rw [div_mul_eq_mul_div, div_le_iff₀' hpi] at hle
  linarith

private lemma norm_addChar_apply' (ψ : AddChar G ℂ) (y : G) : ‖ψ y‖ = 1 :=
  congr_arg NNReal.toReal (AddChar.nnnorm_apply ψ y)

private lemma norm_one_sub_apply_sub' (ψ : AddChar G ℂ) (x y : G) :
    ‖1 - ψ (x - y)‖ = ‖ψ x - ψ y‖ := by
  have hy : ‖ψ y‖ = 1 := norm_addChar_apply' ψ y
  calc
    ‖1 - ψ (x - y)‖ = ‖ψ y‖ * ‖1 - ψ (x - y)‖ := by rw [hy, one_mul]
    _ = ‖ψ y * (1 - ψ (x - y))‖ := (norm_mul _ _).symm
    _ = ‖ψ y - ψ x‖ := by
      congr 1
      rw [mul_sub, mul_one, ← map_add_eq_mul, add_sub_cancel]
    _ = ‖ψ x - ψ y‖ := norm_sub_rev _ _

/-- General covering bound between dilates `R • B` and `r • B` using `M` arc-length bins. -/
lemma card_smul_le_pow_mul (B : BohrSet G) {M : ℕ} (hM : 1 ≤ M) {R r : ℝ}
    (hR : 0 < R) (hr : 0 < r) (hratio : Real.pi * R < M * r) :
    #(R • B).finset ≤ M ^ B.rank * #(r • B).finset := by
  classical
  let _ : Fintype G := Fintype.ofFinite G
  have : NeZero M := ⟨by omega⟩
  let Φ : G → (B.frequencies → Fin M) := fun x ⟨ψ, _⟩ ↦
    let w : ℝ := (B.width ψ : ℝ)
    if w = 0 then ⟨0, by omega⟩
    else
      let u : ℝ := ((ψ x).arg + (Real.pi / 2) * R * w) / (r * w)
      Fin.ofNat M ⌊u⌋₊
  have hdiff : ∀ {x y : G}, x ∈ (R • B).chordSet → y ∈ (R • B).chordSet →
      Φ x = Φ y → x - y ∈ (r • B).chordSet := by
    intro x y hx hy hxy
    rw [mem_chordSet_iff_norm_width] at hx hy ⊢
    intro ψ hψ
    simp only [frequencies_smul] at hψ
    have hR_nn : (Real.nnabs R : ℝ) = R := by simp [Real.nnabs_of_nonneg hR.le, hR.le]
    have hr_nn : (Real.nnabs r : ℝ) = r := by simp [Real.nnabs_of_nonneg hr.le, hr.le]
    have hxψ : ‖1 - ψ x‖ ≤ R * (B.width ψ : ℝ) := by
      simpa [width_smul_apply, hR_nn] using hx hψ
    have hyψ : ‖1 - ψ y‖ ≤ R * (B.width ψ : ℝ) := by
      simpa [width_smul_apply, hR_nn] using hy hψ
    rw [width_smul_apply, NNReal.coe_mul, hr_nn, norm_one_sub_apply_sub']
    set w : ℝ := (B.width ψ : ℝ)
    by_cases hw0 : w = 0
    · have hx1 : ψ x = 1 := (sub_eq_zero.mp (norm_le_zero_iff.mp (by simpa [hw0] using hxψ))).symm
      have hy1 : ψ y = 1 := (sub_eq_zero.mp (norm_le_zero_iff.mp (by simpa [hw0] using hyψ))).symm
      simp [hx1, hy1, hw0]
    · have hw_pos : 0 < w := lt_of_le_of_ne (NNReal.coe_nonneg _) (Ne.symm hw0)
      have hrw_pos : 0 < r * w := mul_pos hr hw_pos
      let ux : ℝ := ((ψ x).arg + (Real.pi / 2) * R * w) / (r * w)
      let uy : ℝ := ((ψ y).arg + (Real.pi / 2) * R * w) / (r * w)
      have hx_arg : |(ψ x).arg| ≤ (Real.pi / 2) * R * w :=
        (abs_arg_le_pi_div_two_mul_norm_one_sub' (norm_addChar_apply' ψ x)).trans
          (by nlinarith [Real.pi_pos])
      have hy_arg : |(ψ y).arg| ≤ (Real.pi / 2) * R * w :=
        (abs_arg_le_pi_div_two_mul_norm_one_sub' (norm_addChar_apply' ψ y)).trans
          (by nlinarith [Real.pi_pos])
      have hux0 : 0 ≤ ux := div_nonneg (by linarith [abs_le.mp hx_arg]) hrw_pos.le
      have huy0 : 0 ≤ uy := div_nonneg (by linarith [abs_le.mp hy_arg]) hrw_pos.le
      have huxM : ux < M := by
        rw [div_lt_iff₀ hrw_pos]
        nlinarith [(abs_le.mp hx_arg).2]
      have huyM : uy < M := by
        rw [div_lt_iff₀ hrw_pos]
        nlinarith [(abs_le.mp hy_arg).2]
      have hfx : ⌊ux⌋₊ < M := (Nat.floor_lt hux0).mpr huxM
      have hfy : ⌊uy⌋₊ < M := (Nat.floor_lt huy0).mpr huyM
      have hcoord := congr_arg Fin.val (congr_fun hxy ⟨ψ, hψ⟩)
      have hw0' : ((B.width ψ : ℝ)) ≠ 0 := hw0
      dsimp only [Φ] at hcoord
      rw [ite_eq_right hw0', ite_eq_right hw0'] at hcoord
      simp only [Fin.val_ofNat] at hcoord
      change ⌊ux⌋₊ % M = ⌊uy⌋₊ % M at hcoord
      rw [Nat.mod_eq_of_lt hfx, Nat.mod_eq_of_lt hfy] at hcoord
      have hfl_eq : (⌊ux⌋₊ : ℝ) = (⌊uy⌋₊ : ℝ) := by exact_mod_cast hcoord
      have hdiff_u : |ux - uy| ≤ 1 := abs_le.mpr
        ⟨by linarith [Nat.floor_le hux0, Nat.lt_floor_add_one uy],
         by linarith [Nat.floor_le huy0, Nat.lt_floor_add_one ux]⟩
      have harg_diff : |(ψ x).arg - (ψ y).arg| ≤ r * w := by
        have hsub : ux - uy = ((ψ x).arg - (ψ y).arg) / (r * w) := by dsimp only [ux, uy]; ring
        rwa [hsub, abs_div, abs_of_pos hrw_pos, div_le_one hrw_pos] at hdiff_u
      have hψx_exp : Complex.exp ((ψ x).arg * I) = ψ x := by
        simpa [norm_addChar_apply' ψ x] using Complex.norm_mul_exp_arg_mul_I (ψ x)
      have hψy_exp : Complex.exp ((ψ y).arg * I) = ψ y := by
        simpa [norm_addChar_apply' ψ y] using Complex.norm_mul_exp_arg_mul_I (ψ y)
      rw [← hψx_exp, ← hψy_exp]
      exact (norm_exp_mul_I_sub_exp_mul_I_le' _ _).trans harg_diff
  let SR := (R • B).finset
  let Sr := (r • B).finset
  have hpart : #SR = ∑ c : (B.frequencies → Fin M), #{x ∈ SR | Φ x = c} := by
    rw [← Finset.card_eq_sum_card_fiberwise (f := Φ) (t := Finset.univ)]
    exact fun _ _ ↦ Finset.mem_univ _
  rw [hpart]
  have hfib : ∀ c : (B.frequencies → Fin M), #{x ∈ SR | Φ x = c} ≤ #Sr := by
    intro c
    rcases ({x ∈ SR | Φ x = c}).eq_empty_or_nonempty with hemp | ⟨x₀, hx₀⟩
    · simp [hemp]
    · obtain ⟨hx₀_SR, hx₀_c⟩ := Finset.mem_filter.mp hx₀
      refine Finset.card_le_card_of_injOn (fun x ↦ x - x₀) (fun x hx ↦ ?_) (fun _ _ _ _ h ↦ ?_)
      · obtain ⟨hx_SR, hx_c⟩ := Finset.mem_filter.mp hx
        exact mem_finset.mpr (hdiff (mem_finset.mp hx_SR) (mem_finset.mp hx₀_SR)
          (hx_c.trans hx₀_c.symm))
      · exact sub_left_inj.mp h
  calc
    ∑ c : (B.frequencies → Fin M), #{x ∈ SR | Φ x = c}
      ≤ ∑ _ : (B.frequencies → Fin M), #Sr := Finset.sum_le_sum fun c _ ↦ hfib c
    _ = Fintype.card (B.frequencies → Fin M) * #Sr := by
      rw [Finset.sum_const, Finset.card_univ, smul_eq_mul]
    _ = M ^ B.rank * #Sr := by
      rw [Fintype.card_fun, Fintype.card_coe, Fintype.card_fin]
      rfl

lemma card_two_smul_le (B : BohrSet G) :
    #((2 : ℝ) • B).finset ≤ 9 ^ B.rank * #B.finset := by
  have hratio : Real.pi * 2 < (9 : ℕ) * (1 : ℝ) := by
    push_cast
    linarith [Real.pi_le_four]
  simpa [one_smul] using card_smul_le_pow_mul B (M := 9) (by omega) (by norm_num) (by norm_num)
    hratio

lemma card_pow_two_smul_le (B : BohrSet G) (k : ℕ) :
    #(((2 : ℝ) ^ k) • B).finset ≤ (9 ^ B.rank) ^ k * #B.finset := by
  induction k with
  | zero => simp [one_smul]
  | succ k ih =>
    have hmul : ((2 : ℝ) ^ (k + 1)) • B = (2 : ℝ) • (((2 : ℝ) ^ k) • B) := by
      rw [pow_succ', mul_smul]
    rw [hmul, pow_succ']
    have hstep := card_two_smul_le (((2 : ℝ) ^ k) • B)
    rw [rank_smul] at hstep
    exact hstep.trans (by rw [mul_assoc]; exact Nat.mul_le_mul_left _ ih)

/-- Size lower bound for a dilated Bohr set `ρ • B` (`0 < ρ ≤ 1`). -/
lemma le_card_smul (B : BohrSet G) {ρ : ℝ} (hρ₀ : 0 < ρ) (hρ₁ : ρ ≤ 1) :
    (ρ / 5) ^ B.rank * (#B.finset : ℝ) ≤ #(ρ • B).finset := by
  let M : ℕ := ⌊4 / ρ⌋₊ + 1
  have hM1 : 1 ≤ M := Nat.succ_le_succ (Nat.zero_le _)
  have h4lt : 4 / ρ < (M : ℝ) := by
    dsimp [M]; push_cast; exact Nat.lt_floor_add_one (4 / ρ)
  have hratio : Real.pi * 1 < M * ρ := by
    have hmul : 4 < (M : ℝ) * ρ := (div_lt_iff₀ hρ₀).mp h4lt
    linarith [Real.pi_le_four]
  have hcov := card_smul_le_pow_mul B hM1 zero_lt_one hρ₀ hratio
  rw [one_smul] at hcov
  have hcovR : (#B.finset : ℝ) ≤ (M : ℝ) ^ B.rank * #(ρ • B).finset := by exact_mod_cast hcov
  have hM_le : (M : ℝ) ≤ 5 / ρ := by
    have hfl : (⌊4 / ρ⌋₊ : ℝ) ≤ 4 / ρ := Nat.floor_le (by positivity)
    have h1 : (1 : ℝ) ≤ 1 / ρ := (le_div_iff₀ hρ₀).mpr (by linarith)
    have hsum : 4 / ρ + 1 / ρ = 5 / ρ := by ring
    dsimp [M]; push_cast; linarith
  have hM_pos : 0 < (M : ℝ) := by positivity
  have hpow : (M : ℝ) ^ B.rank ≤ (5 / ρ) ^ B.rank := pow_le_pow_left₀ hM_pos.le hM_le _
  have h5_pos : 0 < (5 / ρ) ^ B.rank := by positivity
  rw [show (ρ / 5) ^ B.rank = ((5 / ρ) ^ B.rank)⁻¹ by rw [← inv_pow, inv_div],
    inv_mul_le_iff₀ h5_pos]
  exact hcovR.trans (mul_le_mul_of_nonneg_right hpow (Nat.cast_nonneg _))

/-- Size lower bound when intersecting `X` with a new uniform-width Bohr set `ofWidth _ Γ`. -/
lemma le_card_inf_ofWidth (X : BohrSet G) (Γ : Finset (AddChar G ℂ)) {δ : ℝ}
    (hδ₀ : 0 < δ) (hδ₂ : δ ≤ 2) :
    (δ / 18) ^ #Γ * (#(((2⁻¹ : ℝ) • X).finset) : ℝ) ≤
      #(X ⊓ ofWidth (fun _ ↦ (⟨δ, hδ₀.le⟩ : ℝ≥0)) Γ).finset := by
  classical
  let _ : Fintype G := Fintype.ofFinite G
  let δ' : ℝ≥0 := ⟨δ, hδ₀.le⟩
  let M : ℕ := ⌊4 * Real.pi / δ⌋₊ + 1
  have hM1 : 1 ≤ M := Nat.succ_le_succ (Nat.zero_le _)
  have : NeZero M := ⟨by omega⟩
  let Φ : G → (Γ → Fin M) := fun x ⟨ψ, _⟩ ↦
    Fin.ofNat M ⌊((ψ x).arg + Real.pi) / (δ / 2)⌋₊
  have hhalf : (2⁻¹ : ℝ) + (2⁻¹ : ℝ) = 1 := by norm_num
  have hdiff : ∀ {x y : G}, x ∈ ((2⁻¹ : ℝ) • X).chordSet → y ∈ ((2⁻¹ : ℝ) • X).chordSet →
      Φ x = Φ y → x - y ∈ (X ⊓ ofWidth (fun _ ↦ δ') Γ).chordSet := by
    intro x y hx hy hxy
    have hxX : x - y ∈ X.chordSet := by
      have hmem : x + (-y) ∈ (((2⁻¹ : ℝ) • X).chordSet + ((2⁻¹ : ℝ) • X).chordSet) :=
        ⟨x, hx, -y, neg_mem.mpr hy, rfl⟩
      have hsub := smul_add_smul_subset (B := X) (by norm_num : (0 : ℝ) ≤ 2⁻¹)
        (by norm_num : (0 : ℝ) ≤ 2⁻¹) hmem
      rwa [hhalf, one_smul, ← sub_eq_add_neg] at hsub
    intro ψ
    change ‖1 - ψ (x - y)‖₊ ≤ X.ewidth ψ ⊓ (ofWidth (fun _ ↦ δ') Γ).ewidth ψ
    refine le_inf (hxX ψ) ?_
    change ‖1 - ψ (x - y)‖₊ ≤ if ψ ∈ Γ then (δ' : ℝ≥0∞) else ⊤
    split_ifs with hψ
    · rw [ENNReal.coe_le_coe, ← NNReal.coe_le_coe]
      change ‖1 - ψ (x - y)‖ ≤ δ
      rw [norm_one_sub_apply_sub']
      have hd2 : 0 < δ / 2 := by positivity
      let ux : ℝ := ((ψ x).arg + Real.pi) / (δ / 2)
      let uy : ℝ := ((ψ y).arg + Real.pi) / (δ / 2)
      have hux0 : 0 ≤ ux := div_nonneg (by linarith [(abs_le.mp (Complex.abs_arg_le_pi (ψ x))).1])
        hd2.le
      have huy0 : 0 ≤ uy := div_nonneg (by linarith [(abs_le.mp (Complex.abs_arg_le_pi (ψ y))).1])
        hd2.le
      have h4pi_lt : 4 * Real.pi / δ < (M : ℝ) := by
        dsimp [M]; push_cast; exact Nat.lt_floor_add_one _
      have hM_gt : 4 * Real.pi < (M : ℝ) * δ := (div_lt_iff₀ hδ₀).mp h4pi_lt
      have huxM : ux < M := by
        rw [div_lt_iff₀ hd2]
        linarith [Complex.arg_le_pi (ψ x)]
      have huyM : uy < M := by
        rw [div_lt_iff₀ hd2]
        linarith [Complex.arg_le_pi (ψ y)]
      have hfx : ⌊ux⌋₊ < M := (Nat.floor_lt hux0).mpr huxM
      have hfy : ⌊uy⌋₊ < M := (Nat.floor_lt huy0).mpr huyM
      have hcoord := congr_arg Fin.val (congr_fun hxy ⟨ψ, hψ⟩)
      simp only [Φ, Fin.val_ofNat] at hcoord
      rw [Nat.mod_eq_of_lt hfx, Nat.mod_eq_of_lt hfy] at hcoord
      have hfl_eq : (⌊ux⌋₊ : ℝ) = (⌊uy⌋₊ : ℝ) := by exact_mod_cast hcoord
      have hdiff_u : |ux - uy| ≤ 1 := abs_le.mpr
        ⟨by linarith [Nat.floor_le hux0, Nat.lt_floor_add_one uy],
         by linarith [Nat.floor_le huy0, Nat.lt_floor_add_one ux]⟩
      have harg_diff : |(ψ x).arg - (ψ y).arg| ≤ δ / 2 := by
        have hsub : ux - uy = ((ψ x).arg - (ψ y).arg) / (δ / 2) := by dsimp only [ux, uy]; ring
        rwa [hsub, abs_div, abs_of_pos hd2, div_le_one hd2] at hdiff_u
      have hψx_exp : Complex.exp ((ψ x).arg * I) = ψ x := by
        simpa [norm_addChar_apply' ψ x] using Complex.norm_mul_exp_arg_mul_I (ψ x)
      have hψy_exp : Complex.exp ((ψ y).arg * I) = ψ y := by
        simpa [norm_addChar_apply' ψ y] using Complex.norm_mul_exp_arg_mul_I (ψ y)
      rw [← hψx_exp, ← hψy_exp]
      exact (norm_exp_mul_I_sub_exp_mul_I_le' _ _).trans (harg_diff.trans (by linarith))
    · exact le_top
  let SX := ((2⁻¹ : ℝ) • X).finset
  let SY := (X ⊓ ofWidth (fun _ ↦ δ') Γ).finset
  have hpart : #SX = ∑ c : (Γ → Fin M), #{x ∈ SX | Φ x = c} := by
    rw [← Finset.card_eq_sum_card_fiberwise (f := Φ) (t := Finset.univ)]
    exact fun _ _ ↦ Finset.mem_univ _
  have hfib : ∀ c : (Γ → Fin M), #{x ∈ SX | Φ x = c} ≤ #SY := by
    intro c
    rcases ({x ∈ SX | Φ x = c}).eq_empty_or_nonempty with hemp | ⟨x₀, hx₀⟩
    · simp [hemp]
    · obtain ⟨hx₀_SX, hx₀_c⟩ := Finset.mem_filter.mp hx₀
      refine Finset.card_le_card_of_injOn (fun x ↦ x - x₀) (fun x hx ↦ ?_) (fun _ _ _ _ h ↦ ?_)
      · obtain ⟨hx_SX, hx_c⟩ := Finset.mem_filter.mp hx
        exact mem_finset.mpr (hdiff (mem_finset.mp hx_SX) (mem_finset.mp hx₀_SX)
          (hx_c.trans hx₀_c.symm))
      · exact sub_left_inj.mp h
  have hcov : #SX ≤ M ^ #Γ * #SY := by
    calc
      #SX = ∑ c : (Γ → Fin M), #{x ∈ SX | Φ x = c} := hpart
      _ ≤ ∑ _ : (Γ → Fin M), #SY := Finset.sum_le_sum fun c _ ↦ hfib c
      _ = Fintype.card (Γ → Fin M) * #SY := by
        rw [Finset.sum_const, Finset.card_univ, smul_eq_mul]
      _ = M ^ #Γ * #SY := by rw [Fintype.card_fun, Fintype.card_coe, Fintype.card_fin]
  have hcovR : (#SX : ℝ) ≤ (M : ℝ) ^ #Γ * #SY := by exact_mod_cast hcov
  have hM_le : (M : ℝ) ≤ 18 / δ := by
    have hfl : (⌊4 * Real.pi / δ⌋₊ : ℝ) ≤ 16 / δ := by
      refine (Nat.floor_le (by positivity)).trans ?_
      exact div_le_div_of_nonneg_right (by linarith [Real.pi_le_four]) hδ₀.le
    have h1 : (1 : ℝ) ≤ 2 / δ := (le_div_iff₀ hδ₀).mpr (by linarith)
    have hsum : 16 / δ + 2 / δ = 18 / δ := by ring
    dsimp [M]; push_cast; linarith
  have hM_pos : 0 < (M : ℝ) := by positivity
  have hpow : (M : ℝ) ^ #Γ ≤ (18 / δ) ^ #Γ := pow_le_pow_left₀ hM_pos.le hM_le _
  have h18_pos : 0 < (18 / δ) ^ #Γ := by positivity
  rw [show (δ / 18) ^ #Γ = ((18 / δ) ^ #Γ)⁻¹ by rw [← inv_pow, inv_div],
    inv_mul_le_iff₀ h18_pos]
  exact hcovR.trans (mul_le_mul_of_nonneg_right hpow (Nat.cast_nonneg _))

end FiniteAPI

section FintypeWeight
variable {G : Type*} [AddCommGroup G] [Fintype G]

@[simp] lemma top_finset : (⊤ : BohrSet G).finset = Finset.univ := by
  ext x; simp

lemma card_le_sum_bohrWeight {B : BohrSet G} (hB : B.PosWidth) :
    (#B.finset : ℝ) ≤ ∑ x : G, B.bohrWeight x := by
  calc
    (#B.finset : ℝ) = ∑ _x ∈ B.finset, (1 : ℝ) := by simp
    _ = ∑ x ∈ B.finset, B.bohrWeight x :=
      Finset.sum_congr rfl fun x hx ↦ (bohrWeight_eq_one_of_mem hB hx).symm
    _ ≤ ∑ x : G, B.bohrWeight x :=
      Finset.sum_le_univ_sum_of_nonneg fun x ↦ (B.bohrWeight_pos x).le

private lemma nat_add_one_le_two_pow : ∀ k : ℕ, 2 ≤ k → k + 1 ≤ 2 ^ k
  | 0, h => by omega
  | 1, h => by omega
  | 2, _ => by norm_num
  | k + 3, _ => by
    have ih := nat_add_one_le_two_pow (k + 2) (by omega)
    have hstep : 2 * 2 ^ (k + 2) = 2 ^ (k + 3) := (pow_succ' 2 (k + 2)).symm
    omega

lemma sum_bohrWeight_le {B : BohrSet G} (hreg : B.IsRegular) (hB : B.PosWidth) :
    ∑ x : G, B.bohrWeight x ≤ 4 * (#B.finset : ℝ) := by
  classical
  rcases Nat.eq_zero_or_pos B.rank with hd0 | hd_pos
  · have hfreq : B.frequencies = ∅ := Finset.card_eq_zero.mp hd0
    have hB_univ : B.finset = Finset.univ := by
      ext x
      simp [mem_finset, mem_chordSet_iff_nnnorm_width, hfreq]
    rw [hB_univ]
    calc
      ∑ x : G, B.bohrWeight x ≤ ∑ _x : G, (1 : ℝ) :=
        Finset.sum_le_sum fun x _ ↦ B.bohrWeight_le_one x
      _ = ((#(Finset.univ : Finset G) : ℕ) : ℝ) := by simp
      _ ≤ (4 : ℝ) * (#(Finset.univ : Finset G) : ℝ) := by
        linarith [Nat.cast_nonneg (α := ℝ) #(Finset.univ : Finset G)]
  · set d : ℝ := (B.rank : ℝ)
    have hd1 : 1 ≤ d := Nat.one_le_cast.mpr hd_pos
    have hd_pos' : 0 < d := by positivity
    let κ₀ : ℝ := (100 * d)⁻¹
    have hκ₀_pos : 0 < κ₀ := by positivity
    let S₀ : Finset G := ((1 + κ₀) • B).finset
    let S₁ : Finset G := ((2 : ℝ) • B).finset \ S₀
    let S₂ : Finset G := Finset.univ \ ((2 : ℝ) • B).finset
    have hunion1 : S₀ ∪ S₁ = ((2 : ℝ) • B).finset := by
      refine Finset.union_sdiff_of_subset (smul_finset_mono (by positivity) ?_)
      have : κ₀ ≤ 1 := inv_le_one_of_one_le₀ (by linarith)
      linarith
    have hdisj01 : Disjoint S₀ S₁ := disjoint_sdiff_self_right
    have hdisj12 : Disjoint (S₀ ∪ S₁) S₂ := by rw [hunion1]; exact disjoint_sdiff_self_right
    have huniv : (S₀ ∪ S₁) ∪ S₂ = Finset.univ := by
      rw [hunion1]
      exact Finset.union_sdiff_of_subset (Finset.subset_univ _)
    have hsum_split : ∑ x : G, B.bohrWeight x =
        ∑ x ∈ S₀, B.bohrWeight x + ∑ x ∈ S₁, B.bohrWeight x + ∑ x ∈ S₂, B.bohrWeight x := by
      rw [← huniv, Finset.sum_union hdisj12, Finset.sum_union hdisj01]
    rw [hsum_split]
    have hS0 : ∑ x ∈ S₀, B.bohrWeight x ≤ 2 * (#B.finset : ℝ) := by
      have hreg0 := hreg.card_smul_le κ₀ hκ₀_pos.le (by dsimp [κ₀, d]; exact le_rfl)
      rw [← card_finset, ← card_finset] at hreg0
      calc
        ∑ x ∈ S₀, B.bohrWeight x ≤ ∑ _x ∈ S₀, (1 : ℝ) :=
          Finset.sum_le_sum fun x _ ↦ B.bohrWeight_le_one x
        _ = (#S₀ : ℝ) := by simp
        _ ≤ (1 + 100 * d * κ₀) * (#B.finset : ℝ) := hreg0
        _ = 2 * (#B.finset : ℝ) := by
          have : 100 * d * κ₀ = 1 := mul_inv_cancel₀ (by positivity)
          rw [this]; ring
    have hlog9 : Real.log 9 < 3 := by
      rw [Real.log_lt_iff_lt_exp (by norm_num)]
      have he1 : (2.71 : ℝ) < Real.exp 1 := by linarith [Real.exp_one_gt_d9]
      have he3 : Real.exp 3 = Real.exp 1 * Real.exp 1 * Real.exp 1 := by
        rw [← Real.exp_add, ← Real.exp_add]; norm_num
      rw [he3]; nlinarith
    have h9pow : (9 : ℝ) ^ B.rank ≤ Real.exp (3 * d) := by
      rw [← Real.exp_log (by positivity : (0 : ℝ) < (9 : ℝ) ^ B.rank), Real.log_pow]
      exact Real.exp_le_exp.mpr (by dsimp [d]; nlinarith)
    have hS1 : ∑ x ∈ S₁, B.bohrWeight x ≤ (#B.finset : ℝ) := by
      have hx_S1 : ∀ x ∈ S₁, B.bohrWeight x ≤ Real.exp (-10 * d) := by
        intro x hx
        have hx_not : x ∉ S₀ := (Finset.mem_sdiff.mp hx).2
        have hgt : 1 + κ₀ < (B.bohrNorm x : ℝ) :=
          lt_of_not_ge fun hle ↦ hx_not ((bohrNorm_le_iff_mem_smul hB (by positivity) x).mp hle)
        have hmax : κ₀ ≤ max 0 ((B.bohrNorm x : ℝ) - 1) :=
          le_trans (by linarith) (le_max_right _ _)
        unfold bohrWeight
        apply Real.exp_le_exp.mpr
        have hcalc : 1000 * d ^ 2 * κ₀ = 10 * d := by
          dsimp [κ₀]; field_simp; ring
        nlinarith [show 0 ≤ 1000 * d ^ 2 by positivity]
      calc
        ∑ x ∈ S₁, B.bohrWeight x ≤ ∑ _x ∈ S₁, Real.exp (-10 * d) := Finset.sum_le_sum hx_S1
        _ = (#S₁ : ℝ) * Real.exp (-10 * d) := by simp
        _ ≤ (#((2 : ℝ) • B).finset : ℝ) * Real.exp (-10 * d) := by
          gcongr; exact sdiff_subset
        _ ≤ (9 : ℝ) ^ B.rank * (#B.finset : ℝ) * Real.exp (-10 * d) := by
          gcongr; exact_mod_cast card_two_smul_le B
        _ ≤ Real.exp (3 * d) * (#B.finset : ℝ) * Real.exp (-10 * d) := by gcongr
        _ = Real.exp (-7 * d) * (#B.finset : ℝ) := by
          rw [mul_right_comm, ← Real.exp_add]; ring_nf
        _ ≤ 1 * (#B.finset : ℝ) := by
          gcongr; exact Real.exp_le_one_iff.mpr (by linarith)
        _ = (#B.finset : ℝ) := one_mul _
    have hS2 : ∑ x ∈ S₂, B.bohrWeight x ≤ (#B.finset : ℝ) := by
      let M_top : ℕ := ⌊((Finset.univ.sup B.bohrNorm : ℝ≥0) : ℝ)⌋₊ + 1
      let shell (k : ℕ) : Finset G := {x ∈ S₂ | ⌊(B.bohrNorm x : ℝ)⌋₊ = k}
      have hsub_shells : S₂ ⊆ (Finset.Ico 2 M_top).biUnion shell := by
        intro x hx
        have hx_not : x ∉ ((2 : ℝ) • B).finset := (Finset.mem_sdiff.mp hx).2
        have hgt2 : 2 < (B.bohrNorm x : ℝ) :=
          lt_of_not_ge fun hle ↦ hx_not ((bohrNorm_le_iff_mem_smul hB (by norm_num) x).mp hle)
        have hge2 : 2 ≤ ⌊(B.bohrNorm x : ℝ)⌋₊ := (Nat.le_floor_iff (by positivity)).mpr hgt2.le
        have hltM : ⌊(B.bohrNorm x : ℝ)⌋₊ < M_top := by
          have hfl_le : ⌊(B.bohrNorm x : ℝ)⌋₊ ≤ ⌊((Finset.univ.sup B.bohrNorm : ℝ≥0) : ℝ)⌋₊ := by
            gcongr; exact_mod_cast Finset.le_sup (Finset.mem_univ x)
          dsimp [M_top]; omega
        exact Finset.mem_biUnion.mpr
          ⟨⌊(B.bohrNorm x : ℝ)⌋₊, Finset.mem_Ico.mpr ⟨hge2, hltM⟩, Finset.mem_filter.mpr ⟨hx, rfl⟩⟩
      have hshell_bound : ∀ k ∈ Finset.Ico 2 M_top,
          ∑ x ∈ shell k, B.bohrWeight x ≤ (2⁻¹ : ℝ) ^ k * (#B.finset : ℝ) := by
        intro k hk
        have hk2 : 2 ≤ k := (Finset.mem_Ico.mp hk).1
        have hsub_pow : shell k ⊆ (((2 : ℝ) ^ k) • B).finset := by
          intro x hx
          have hfl : ⌊(B.bohrNorm x : ℝ)⌋₊ = k := (Finset.mem_filter.mp hx).2
          have hlt : (B.bohrNorm x : ℝ) < (k : ℝ) + 1 := by
            rw [← hfl]; exact Nat.lt_floor_add_one _
          have hkpow : (k : ℝ) + 1 ≤ (2 : ℝ) ^ k := by
            exact_mod_cast nat_add_one_le_two_pow k hk2
          exact (bohrNorm_le_iff_mem_smul hB (by positivity) x).mp (hlt.le.trans hkpow)
        have hx_wt : ∀ x ∈ shell k, B.bohrWeight x ≤ Real.exp (-500 * d * k) := by
          intro x hx
          have hfl : ⌊(B.bohrNorm x : ℝ)⌋₊ = k := (Finset.mem_filter.mp hx).2
          have hge : (k : ℝ) ≤ B.bohrNorm x := by
            rw [← hfl]; exact Nat.floor_le (by positivity)
          have hk2' : (2 : ℝ) ≤ k := by exact_mod_cast hk2
          have hmax : (k : ℝ) / 2 ≤ max 0 ((B.bohrNorm x : ℝ) - 1) :=
            le_trans (by linarith) (le_max_right _ _)
          unfold bohrWeight
          apply Real.exp_le_exp.mpr
          have hd_sq : d ≤ d ^ 2 := by nlinarith
          nlinarith
        have hcard_sh : (#(shell k) : ℝ) ≤ (Real.exp (3 * d)) ^ k * (#B.finset : ℝ) := by
          calc
            (#(shell k) : ℝ) ≤ (#(((2 : ℝ) ^ k) • B).finset : ℝ) := by gcongr
            _ ≤ ((9 : ℝ) ^ B.rank) ^ k * (#B.finset : ℝ) := by
              exact_mod_cast card_pow_two_smul_le B k
            _ ≤ (Real.exp (3 * d)) ^ k * (#B.finset : ℝ) := by gcongr
        calc
          ∑ x ∈ shell k, B.bohrWeight x ≤ ∑ _x ∈ shell k, Real.exp (-500 * d * k) :=
            Finset.sum_le_sum hx_wt
          _ = (#(shell k) : ℝ) * Real.exp (-500 * d * k) := by simp
          _ ≤ (Real.exp (3 * d)) ^ k * (#B.finset : ℝ) * Real.exp (-500 * d * k) := by gcongr
          _ = (Real.exp (-497 * d)) ^ k * (#B.finset : ℝ) := by
            rw [mul_right_comm, ← Real.exp_nat_mul, ← Real.exp_nat_mul, ← Real.exp_add]
            congr 2; ring
          _ ≤ (2⁻¹ : ℝ) ^ k * (#B.finset : ℝ) := by
            gcongr
            have he_inv : Real.exp (-497 * d) ≤ Real.exp (-1) :=
              Real.exp_le_exp.mpr (by linarith)
            exact he_inv.trans (by linarith [Real.exp_neg_one_lt_d9])
      calc
        ∑ x ∈ S₂, B.bohrWeight x ≤
            ∑ x ∈ (Finset.Ico 2 M_top).biUnion shell, B.bohrWeight x :=
          Finset.sum_le_sum_of_subset_of_nonneg hsub_shells fun _ _ _ ↦ (B.bohrWeight_pos _).le
        _ = ∑ k ∈ Finset.Ico 2 M_top, ∑ x ∈ shell k, B.bohrWeight x :=
          Finset.sum_biUnion fun k₁ _ k₂ _ hne ↦ Finset.disjoint_left.mpr fun x hx₁ hx₂ ↦
            hne ((Finset.mem_filter.mp hx₁).2.symm.trans (Finset.mem_filter.mp hx₂).2)
        _ ≤ ∑ k ∈ Finset.Ico 2 M_top, (2⁻¹ : ℝ) ^ k * (#B.finset : ℝ) :=
          Finset.sum_le_sum hshell_bound
        _ = (∑ k ∈ Finset.Ico 2 M_top, (2⁻¹ : ℝ) ^ k) * (#B.finset : ℝ) :=
          (Finset.sum_mul _ _ _).symm
        _ ≤ 1 * (#B.finset : ℝ) := by
          gcongr
          rcases le_or_gt M_top 2 with hM2 | hM2
          · rw [Finset.Ico_eq_empty (by omega)]
            simp
          · have hgeom := geom_sum_eq (by norm_num : (2⁻¹ : ℝ) ≠ 1) M_top
            have hgeom' : ∑ k ∈ Finset.range M_top, (2⁻¹ : ℝ) ^ k =
                2 - 2 * (2⁻¹ : ℝ) ^ M_top := by rw [hgeom]; ring
            have hsplit := Finset.sum_range_add_sum_Ico (fun k ↦ (2⁻¹ : ℝ) ^ k) hM2.le
            have hr2 : ∑ k ∈ Finset.range 2, (2⁻¹ : ℝ) ^ k = 3 / 2 := by
              simp [Finset.sum_range_succ]; norm_num
            have hpos_pow : 0 ≤ (2⁻¹ : ℝ) ^ M_top := by positivity
            linarith
        _ = (#B.finset : ℝ) := one_mul _
    linarith

end FintypeWeight

section TwoBohr
variable {q : ℕ} [Fact q.Prime]

/-- Multiplication by `2` as an additive automorphism of `ZMod q` for prime `q ≥ 3`. -/
def twoEquiv (hq : 3 ≤ q) : ZMod q ≃+ ZMod q where
  toFun x := (2 : ZMod q) * x
  invFun y := (2 : ZMod q)⁻¹ * y
  left_inv x := by
    dsimp only
    have h2 : (2 : ZMod q) ≠ 0 := by
      intro h0
      have hdvd : q ∣ 2 := (ZMod.natCast_eq_zero_iff 2 q).mp (by simpa using h0)
      have hle : q ≤ 2 := Nat.le_of_dvd (by norm_num) hdvd
      omega
    rw [← mul_assoc, inv_mul_cancel₀ h2, one_mul]
  right_inv y := by
    dsimp only
    have h2 : (2 : ZMod q) ≠ 0 := by
      intro h0
      have hdvd : q ∣ 2 := (ZMod.natCast_eq_zero_iff 2 q).mp (by simpa using h0)
      have hle : q ≤ 2 := Nat.le_of_dvd (by norm_num) hdvd
      omega
    rw [← mul_assoc, mul_inv_cancel₀ h2, one_mul]
  map_add' x y := mul_add _ _ _

/-- Precomposition of an additive character with an additive equivalence. -/
def charCompEquiv {G H : Type*} [AddCommGroup G] [AddCommGroup H]
    (e : G ≃+ H) (ψ : AddChar H ℂ) : AddChar G ℂ where
  toFun x := ψ (e x)
  map_zero_eq_one' := by simp
  map_add_eq_mul' x y := by simp [map_add_eq_mul]

@[simp] lemma charCompEquiv_apply {G H : Type*} [AddCommGroup G] [AddCommGroup H]
    (e : G ≃+ H) (ψ : AddChar H ℂ) (x : G) : charCompEquiv e ψ x = ψ (e x) := rfl

@[simp] lemma charCompEquiv_symm_comp {G H : Type*} [AddCommGroup G] [AddCommGroup H]
    (e : G ≃+ H) (ψ : AddChar H ℂ) :
    charCompEquiv e.symm (charCompEquiv e ψ) = ψ := by
  ext x; simp

@[simp] lemma charCompEquiv_comp_symm {G H : Type*} [AddCommGroup G] [AddCommGroup H]
    (e : G ≃+ H) (φ : AddChar G ℂ) :
    charCompEquiv e (charCompEquiv e.symm φ) = φ := by
  ext x; simp

def charCompEmbedding {G H : Type*} [AddCommGroup G] [AddCommGroup H]
    (e : G ≃+ H) : AddChar H ℂ ↪ AddChar G ℂ where
  toFun := charCompEquiv e
  inj' φ₁ φ₂ h := by
    have := congr_arg (charCompEquiv e.symm) h
    simpa using this

@[simp] lemma charCompEmbedding_apply {G H : Type*} [AddCommGroup G] [AddCommGroup H]
    (e : G ≃+ H) (ψ : AddChar H ℂ) : charCompEmbedding e ψ = charCompEquiv e ψ := rfl

/-- The `2`-dilated Bohr set `2 · B = {2 x : x ∈ B}` in `ZMod q` (`q ≥ 3` prime). -/
noncomputable def twoBohr (hq : 3 ≤ q) (B : BohrSet (ZMod q)) : BohrSet (ZMod q) where
  frequencies := B.frequencies.map (charCompEmbedding (twoEquiv hq).symm)
  ewidth ψ := B.ewidth (charCompEquiv (twoEquiv hq) ψ)
  mem_frequencies ψ := by
    simp only [Finset.mem_map, charCompEmbedding_apply, ← B.mem_frequencies]
    constructor
    · rintro ⟨φ, hφ, rfl⟩
      simpa using hφ
    · intro h
      exact ⟨charCompEquiv (twoEquiv hq) ψ, h, by simp⟩

lemma mem_twoBohr_chordSet (hq : 3 ≤ q) (B : BohrSet (ZMod q)) (y : ZMod q) :
    y ∈ (twoBohr hq B).chordSet ↔ (twoEquiv hq).symm y ∈ B.chordSet := by
  simp only [mem_chordSet_iff_nnnorm_ewidth, twoBohr]
  constructor
  · intro h φ
    have h1 := h (charCompEquiv (twoEquiv hq).symm φ)
    simpa using h1
  · intro h ψ
    simpa using h (charCompEquiv (twoEquiv hq) ψ)

lemma twoBohr_finset (hq : 3 ≤ q) (B : BohrSet (ZMod q)) :
    (twoBohr hq B).finset = B.finset.image (fun x ↦ (2 : ZMod q) * x) := by
  ext y
  simp only [mem_finset, mem_twoBohr_chordSet, Finset.mem_image]
  constructor
  · intro hy
    refine ⟨(twoEquiv hq).symm y, hy, ?_⟩
    exact (twoEquiv hq).apply_symm_apply y
  · rintro ⟨x, hx, rfl⟩
    change (twoEquiv hq).symm ((twoEquiv hq) x) ∈ B.chordSet
    simpa using hx

lemma twoBohr_finset_nsmul (hq : 3 ≤ q) (B : BohrSet (ZMod q)) :
    (twoBohr hq B).finset = B.finset.image (2 • ·) := by
  rw [twoBohr_finset]
  congr 1 with x
  rw [two_smul, two_mul]

@[simp] lemma twoBohr_rank (hq : 3 ≤ q) (B : BohrSet (ZMod q)) :
    (twoBohr hq B).rank = B.rank := by
  change #(twoBohr hq B).frequencies = #B.frequencies
  simp [twoBohr]

@[simp] lemma card_twoBohr_finset (hq : 3 ≤ q) (B : BohrSet (ZMod q)) :
    #(twoBohr hq B).finset = #B.finset := by
  rw [twoBohr_finset]
  exact Finset.card_image_of_injective _ (twoEquiv hq).injective

lemma twoBohr_smul (hq : 3 ≤ q) (ρ : ℝ) (B : BohrSet (ZMod q)) :
    twoBohr hq (ρ • B) = ρ • twoBohr hq B := by
  apply ewidth_injective
  ext ψ
  have hmem : charCompEquiv (twoEquiv hq) ψ ∈ B.frequencies ↔ ψ ∈ (twoBohr hq B).frequencies := by
    rw [B.mem_frequencies, (twoBohr hq B).mem_frequencies]; rfl
  change (ρ • B).ewidth (charCompEquiv (twoEquiv hq) ψ) =
      if ψ ∈ (twoBohr hq B).frequencies then ↑(nnabs ρ) * (twoBohr hq B).ewidth ψ else ⊤
  rw [ewidth_smul]
  exact if_congr hmem rfl rfl

lemma twoBohr_isRegular (hq : 3 ≤ q) {B : BohrSet (ZMod q)} (hB : B.IsRegular) :
    (twoBohr hq B).IsRegular where
  le_card_smul κ hκ0 hκ := by
    rw [twoBohr_rank] at hκ ⊢
    rw [← twoBohr_smul, ← card_finset, ← card_finset, card_twoBohr_finset, card_twoBohr_finset,
      card_finset, card_finset]
    exact hB.le_card_smul κ hκ0 hκ
  card_smul_le κ hκ0 hκ := by
    rw [twoBohr_rank] at hκ ⊢
    rw [← twoBohr_smul, ← card_finset, ← card_finset, card_twoBohr_finset, card_twoBohr_finset,
      card_finset, card_finset]
    exact hB.card_smul_le κ hκ0 hκ

lemma twoBohr_posWidth (hq : 3 ≤ q) {B : BohrSet (ZMod q)} (hB : B.PosWidth) :
    (twoBohr hq B).PosWidth := by
  intro ψ hψ
  rw [mem_frequencies] at hψ
  change B.ewidth (charCompEquiv (twoEquiv hq) ψ) < ⊤ at hψ
  have hφ : charCompEquiv (twoEquiv hq) ψ ∈ B.frequencies := (B.mem_frequencies _).mpr hψ
  exact hB _ hφ

lemma twoBohr_finset_subset_two_smul (hq : 3 ≤ q) (B : BohrSet (ZMod q)) :
    (twoBohr hq B).finset ⊆ ((2 : ℝ) • B).finset := by
  intro y hy
  rw [twoBohr_finset, Finset.mem_image] at hy
  rcases hy with ⟨x, hx, rfl⟩
  have hadd : x + x ∈ ((1 : ℝ) • B).finset + ((1 : ℝ) • B).finset := by
    rw [one_smul]
    exact Finset.add_mem_add hx hx
  have hsub := smul_add_smul_finset_subset (B := B) zero_le_one zero_le_one hadd
  rwa [show (1 : ℝ) + 1 = 2 by norm_num, ← two_mul] at hsub

end TwoBohr

section RegularityConvAndBourgain
variable {G : Type*} [AddCommGroup G] [Fintype G] [DecidableEq G]
  [MeasurableSpace G] [DiscreteMeasurableSpace G]

omit [Fintype G] [DecidableEq G] [MeasurableSpace G] [DiscreteMeasurableSpace G] in
lemma IsRegular.card_one_add_smul_le [Finite G] {B : BohrSet G} (hreg : B.IsRegular)
    {κ : ℝ} (hκ₀ : 0 ≤ κ) (hκ : 100 * (B.rank : ℝ) * κ ≤ 1) :
    (#((1 + κ) • B).finset : ℝ) ≤ (1 + 100 * B.rank * κ) * (#B.finset : ℝ) := by
  rcases Nat.eq_zero_or_pos B.rank with hd0 | hd_pos
  · have hfreq : B.frequencies = ∅ := Finset.card_eq_zero.mp hd0
    have heq : ((1 + κ) • B).finset = B.finset := by
      ext x; simp [mem_finset, mem_chordSet_iff_nnnorm_width, hfreq]
    simp [hd0, heq]
  · have hd_pos' : 0 < (100 : ℝ) * B.rank := by positivity
    have hκ' : κ ≤ (100 * B.rank : ℝ)⁻¹ := by
      have h1 := mul_le_mul_of_nonneg_left hκ (inv_nonneg.mpr hd_pos'.le)
      rwa [inv_mul_cancel_left₀ hd_pos'.ne', mul_one] at h1
    simpa [card_finset] using hreg.card_smul_le κ hκ₀ hκ'

omit [Fintype G] [DecidableEq G] [MeasurableSpace G] [DiscreteMeasurableSpace G] in
lemma IsRegular.le_card_one_sub_smul [Finite G] {B : BohrSet G} (hreg : B.IsRegular)
    {κ : ℝ} (hκ₀ : 0 ≤ κ) (hκ : 100 * (B.rank : ℝ) * κ ≤ 1) :
    (1 - 100 * B.rank * κ) * (#B.finset : ℝ) ≤ (#((1 - κ) • B).finset : ℝ) := by
  rcases Nat.eq_zero_or_pos B.rank with hd0 | hd_pos
  · have hfreq : B.frequencies = ∅ := Finset.card_eq_zero.mp hd0
    have heq : ((1 - κ) • B).finset = B.finset := by
      ext x; simp [mem_finset, mem_chordSet_iff_nnnorm_width, hfreq]
    simp [hd0, heq]
  · have hd_pos' : 0 < (100 : ℝ) * B.rank := by positivity
    have hκ' : κ ≤ (100 * B.rank : ℝ)⁻¹ := by
      have h1 := mul_le_mul_of_nonneg_left hκ (inv_nonneg.mpr hd_pos'.le)
      rwa [inv_mul_cancel_left₀ hd_pos'.ne', mul_one] at h1
    simpa [card_finset] using hreg.le_card_smul κ hκ₀ hκ'

/-- Convolution `L^1` regularity bound (`reg-conv` in the blueprint). -/
lemma IsRegular.dL1Norm_mu_ddconv_sub_le {B : BohrSet G} (hreg : B.IsRegular)
    {κ : ℝ} (hκ₀ : 0 ≤ κ) (hκ : 100 * (B.rank : ℝ) * κ ≤ 1)
    {ν : G → ℝ} (hν₀ : 0 ≤ ν) (hν₁ : ∑ y, ν y = 1)
    (hsupp : ∀ y, ν y ≠ 0 → y ∈ (κ • B).finset) :
    ‖μ_[ℝ] B.finset ∗ᵈ ν - μ B.finset‖_[1] ≤ 200 * B.rank * κ := by
  let μB : G → ℝ := μ B.finset
  have hshift : ∀ {y : G}, y ∈ (κ • B).finset →
      ∑ x : G, |μB (x - y) - μB x| ≤ 200 * B.rank * κ := by
    intro y hy
    rcases Nat.eq_zero_or_pos B.rank with hd0 | hd_pos
    · have hfreq : B.frequencies = ∅ := Finset.card_eq_zero.mp hd0
      have hB_univ : B.finset = Finset.univ := by
        ext x; simp [mem_finset, mem_chordSet_iff_nnnorm_width, hfreq]
      simp [μB, hB_univ, hd0, mu_apply]
    · let B_in := ((1 - κ) • B).finset
      let B_out := ((1 + κ) • B).finset
      have hd1 : (1 : ℝ) ≤ B.rank := Nat.one_le_cast.mpr hd_pos
      have hκ1 : κ ≤ 1 := by nlinarith
      have hsub_in_B : B_in ⊆ B.finset := by
        simpa [B_in, one_smul] using smul_finset_mono (by linarith) (by linarith : 1 - κ ≤ 1)
      have hsub_B_out : B.finset ⊆ B_out := by
        simpa [B_out, one_smul] using smul_finset_mono zero_le_one (by linarith : (1 : ℝ) ≤ 1 + κ)
      have hsub_in_out : B_in ⊆ B_out := hsub_in_B.trans hsub_B_out
      have hzero_in : ∀ x ∈ B_in, μB (x - y) - μB x = 0 := by
        intro x hx
        have hxB : x ∈ B.finset := hsub_in_B hx
        have hxyB : x - y ∈ B.finset := by
          have hmem : x + (-y) ∈ ((1 - κ) • B).finset + (κ • B).finset :=
            Finset.add_mem_add hx (neg_mem_finset.mpr hy)
          have hsub := smul_add_smul_finset_subset (B := B) (by linarith) hκ₀ hmem
          simpa [sub_add_cancel, one_smul, ← sub_eq_add_neg] using hsub
        simp [μB, mu_apply, hxB, hxyB]
      have hzero_out : ∀ x ∉ B_out, μB (x - y) - μB x = 0 := by
        intro x hx_out
        have hxB : x ∉ B.finset := fun hx ↦ hx_out (hsub_B_out hx)
        have hxyB : x - y ∉ B.finset := by
          intro hxy
          apply hx_out
          have hmem : (x - y) + y ∈ ((1 : ℝ) • B).finset + (κ • B).finset := by
            rw [one_smul]
            exact Finset.add_mem_add hxy hy
          have hsub := smul_add_smul_finset_subset (B := B) zero_le_one hκ₀ hmem
          simpa [B_out, sub_add_cancel] using hsub
        simp [μB, mu_apply, hxB, hxyB]
      have hpoint : ∀ x : G, |μB (x - y) - μB x| ≤ (#B.finset : ℝ)⁻¹ := by
        intro x
        have hinv_nn : (0 : ℝ) ≤ (#B.finset : ℝ)⁻¹ := by positivity
        simp only [μB, mu_apply, mul_boole]
        split_ifs <;> simp [abs_of_nonneg hinv_nn]
      have hBpos : (0 : ℝ) < #B.finset := by exact_mod_cast B.card_finset_pos
      calc
        ∑ x : G, |μB (x - y) - μB x|
          = ∑ x ∈ B_out \ B_in, |μB (x - y) - μB x| := by
            symm
            refine Finset.sum_subset (Finset.subset_univ _) fun x _ hx_not ↦ ?_
            rw [Finset.mem_sdiff, not_and_or, not_not] at hx_not
            rcases hx_not with hx_out | hx_in
            · simp [hzero_out x hx_out]
            · simp [hzero_in x hx_in]
        _ ≤ ∑ _x ∈ B_out \ B_in, (#B.finset : ℝ)⁻¹ :=
          Finset.sum_le_sum fun x _ ↦ hpoint x
        _ = ((#B_out : ℝ) - (#B_in : ℝ)) / (#B.finset : ℝ) := by
          have hcs : (#(B_out \ B_in) : ℝ) + (#B_in : ℝ) = (#B_out : ℝ) := by
            exact_mod_cast Finset.card_sdiff_add_card_eq_card hsub_in_out
          have hcs' : (#(B_out \ B_in) : ℝ) = (#B_out : ℝ) - (#B_in : ℝ) := by linarith
          simp [hcs', div_eq_mul_inv]
        _ ≤ (((1 + 100 * B.rank * κ) * #B.finset) - ((1 - 100 * B.rank * κ) * #B.finset)) /
              (#B.finset : ℝ) := by
          refine div_le_div_of_nonneg_right ?_ hBpos.le
          have h1 := hreg.card_one_add_smul_le hκ₀ hκ
          have h2 := hreg.le_card_one_sub_smul hκ₀ hκ
          linarith
        _ = 200 * B.rank * κ := by field_simp [hBpos.ne']; ring
  rw [dL1Norm_eq_sum_norm]
  have hpt : ∀ x : G, ‖(μB ∗ᵈ ν - μB) x‖ ≤ ∑ y : G, ν y * |μB (x - y) - μB x| := by
    intro x
    have hrew : (μB ∗ᵈ ν - μB) x = ∑ y : G, ν y * (μB (x - y) - μB x) := by
      simp only [Pi.sub_apply, ddconv_eq_sum_sub, mul_sub, Finset.sum_sub_distrib,
        ← Finset.sum_mul, hν₁, one_mul]
      congr 1
      exact Finset.sum_congr rfl fun y _ ↦ mul_comm _ _
    rw [Real.norm_eq_abs, hrew]
    refine (Finset.abs_sum_le_sum_abs _ _).trans (le_of_eq ?_)
    refine Finset.sum_congr rfl fun y _ ↦ ?_
    rw [abs_mul, abs_of_nonneg (hν₀ y)]
  calc
    ∑ x : G, ‖(μB ∗ᵈ ν - μB) x‖
      ≤ ∑ x : G, ∑ y : G, ν y * |μB (x - y) - μB x| := Finset.sum_le_sum fun x _ ↦ hpt x
    _ = ∑ y : G, ν y * ∑ x : G, |μB (x - y) - μB x| := by
      rw [Finset.sum_comm]
      exact Finset.sum_congr rfl fun y _ ↦ (Finset.mul_sum _ _ _).symm
    _ ≤ ∑ y : G, ν y * (200 * B.rank * κ) := by
      refine Finset.sum_le_sum fun y _ ↦ ?_
      by_cases hy0 : ν y = 0
      · simp [hy0]
      · exact mul_le_mul_of_nonneg_left (hshift (hsupp y hy0)) (hν₀ y)
    _ = 200 * B.rank * κ := by rw [← Finset.sum_mul, hν₁, one_mul]

omit [MeasurableSpace G] [DiscreteMeasurableSpace G] in
/-- Pointwise majorization of `μ B` by `2 * (μ ((1 + κ) • B) ∗ᵈ ν)` (`bohr-majorise`). -/
lemma IsRegular.mu_le_two_mul_ddconv {B : BohrSet G} (hreg : B.IsRegular)
    {κ : ℝ} (hκ₀ : 0 ≤ κ) (hκ : 100 * (B.rank : ℝ) * κ ≤ 1)
    {ν : G → ℝ} (hν₀ : 0 ≤ ν) (hν₁ : ∑ y, ν y = 1)
    (hsupp : ∀ y, ν y ≠ 0 → y ∈ (κ • B).finset) (x : G) :
    μ_[ℝ] B.finset x ≤ 2 * (μ_[ℝ] ((1 + κ) • B).finset ∗ᵈ ν) x := by
  let W := ((1 + κ) • B).finset
  by_cases hxB : x ∈ B.finset
  · have hW_le : (#W : ℝ) ≤ 2 * (#B.finset : ℝ) := by
      have h1 := hreg.card_one_add_smul_le hκ₀ hκ
      nlinarith [Nat.cast_nonneg (α := ℝ) #B.finset]
    have hB_pos : (0 : ℝ) < #B.finset := by exact_mod_cast B.card_finset_pos
    have hW_pos : (0 : ℝ) < #W := by exact_mod_cast ((1 + κ) • B).card_finset_pos
    have hconv : (μ_[ℝ] W ∗ᵈ ν) x = (#W : ℝ)⁻¹ := by
      rw [ddconv_eq_sum_sub]
      have hterm : ∀ y : G, μ_[ℝ] W (x - y) * ν y = (#W : ℝ)⁻¹ * ν y := by
        intro y
        by_cases hy0 : ν y = 0
        · simp [hy0]
        · have hy : y ∈ (κ • B).finset := hsupp y hy0
          have hxy : x - y ∈ W := by
            have hmem : x + (-y) ∈ ((1 : ℝ) • B).finset + (κ • B).finset := by
              rw [one_smul]
              exact Finset.add_mem_add hxB (neg_mem_finset.mpr hy)
            have hsub := smul_add_smul_finset_subset (B := B) zero_le_one hκ₀ hmem
            simpa [W, ← sub_eq_add_neg] using hsub
          simp [mu_apply, hxy]
      simp_rw [hterm, ← Finset.mul_sum, hν₁, mul_one]
    have hmuB : μ_[ℝ] B.finset x = (#B.finset : ℝ)⁻¹ := by simp [mu_apply, hxB]
    rw [hconv, hmuB, inv_eq_one_div, inv_eq_one_div, mul_one_div, div_le_div_iff₀ hB_pos hW_pos]
    linarith
  · have hmuB : μ_[ℝ] B.finset x = 0 := by simp [mu_apply, hxB]
    rw [hmuB]
    exact mul_nonneg (by norm_num : (0 : ℝ) ≤ 2) (ddconv_apply_nonneg' (R := ℝ) mu_nonneg hν₀ x)

/-- Bourgain's density-preservation / increment dichotomy (`bourgain-trick` in the blueprint). -/
lemma bourgain_trick {B : BohrSet G} (hreg : B.IsRegular) {A B₁ B₂ : Finset G}
    (hAB : A ⊆ B.finset) (hB₁₀ : B₁.Nonempty) (hB₂₀ : B₂.Nonempty)
    (hB₁sym : -B₁ = B₁) (hB₂sym : -B₂ = B₂)
    {α_B ε κ : ℝ} (hα : α_B = (#A : ℝ) / (#B.finset : ℝ)) (_hε₀ : 0 < ε)
    (hκ₀ : 0 ≤ κ) (hκ : 100 * (B.rank : ℝ) * κ ≤ 1)
    (hκ_small : 200 * B.rank * κ ≤ ε * α_B / 8)
    (hB₁_sub : B₁ ⊆ (κ • B).finset) (hB₂_sub : B₂ ⊆ (κ • B).finset) :
    (1 + ε / 4) * α_B ≤ ‖𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₁‖_[∞] ∨
    (1 + ε / 4) * α_B ≤ ‖𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₂‖_[∞] ∨
    ∃ x : G, (1 - ε / 2) * α_B * #B₁ ≤ #((-x +ᵥ A) ∩ B₁) ∧
      (1 - ε / 2) * α_B * #B₂ ≤ #((-x +ᵥ A) ∩ B₂) := by
  by_cases h1 : (1 + ε / 4) * α_B ≤ ‖𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₁‖_[∞]
  · exact Or.inl h1
  by_cases h2 : (1 + ε / 4) * α_B ≤ ‖𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₂‖_[∞]
  · exact Or.inr (Or.inl h2)
  refine Or.inr (Or.inr ?_)
  push Not at h1 h2
  have hcard_eq : ∀ (S : Finset G), -S = S → ∀ x : G,
      (𝟭_[(A : Set G), ℝ] ∗ᵈ μ S) x = (#((-x +ᵥ A) ∩ S) : ℝ) / (#S : ℝ) := by
    intro S hSsym x
    rw [ddconv_eq_sum_sub']
    have hsum_A : ∑ y : G, (𝟭_[(A : Set G), ℝ] y) * μ_[ℝ] S (x - y) =
        ∑ y ∈ A, μ_[ℝ] S (x - y) := by
      rw [← Finset.sum_subset (Finset.subset_univ A)]
      · exact Finset.sum_congr rfl fun y hy ↦ by simp [hy]
      · intro y _ hy; simp [hy]
    rw [hsum_A]
    calc
      ∑ y ∈ A, μ_[ℝ] S (x - y)
        = ∑ y ∈ A, (#S : ℝ)⁻¹ * ite (y - x ∈ S) 1 0 := by
          refine Finset.sum_congr rfl fun y _ ↦ ?_
          rw [mu_apply]
          congr 2
          have : x - y ∈ S ↔ y - x ∈ S := by
            conv_lhs => rw [← hSsym]
            simp [neg_sub]
          exact propext this
      _ = (#S : ℝ)⁻¹ * #{y ∈ A | y - x ∈ S} := by
          rw [← Finset.mul_sum]
          simp
      _ = (#((-x +ᵥ A) ∩ S) : ℝ) / (#S : ℝ) := by
          rw [div_eq_inv_mul]
          congr 2
          apply Finset.card_bij (fun y _ ↦ -x + y)
          · intro y hy
            obtain ⟨hyA, hyS⟩ := Finset.mem_filter.mp hy
            refine Finset.mem_inter.mpr ⟨Finset.mem_vadd_finset.mpr ⟨y, hyA, rfl⟩, ?_⟩
            simpa [sub_eq_add_neg, add_comm] using hyS
          · intro y₁ _ y₂ _ h; exact add_left_cancel h
          · intro z hz
            obtain ⟨hzA, hzS⟩ := Finset.mem_inter.mp hz
            obtain ⟨y, hyA, rfl⟩ := Finset.mem_vadd_finset.mp hzA
            refine ⟨y, Finset.mem_filter.mpr ⟨hyA, ?_⟩, rfl⟩
            simpa [sub_eq_add_neg, add_comm] using hzS
  have havg_ge : ∀ (S : Finset G), S.Nonempty → -S = S → S ⊆ (κ • B).finset →
      (1 - ε / 8) * α_B ≤ ∑ x : G, μ_[ℝ] B.finset x * (𝟭_[(A : Set G), ℝ] ∗ᵈ μ S) x := by
    intro S hS₀ hSsym hS_sub
    let μB : G → ℝ := μ B.finset
    let μS : G → ℝ := μ S
    let indA : G → ℝ := 𝟭_[(A : Set G), ℝ]
    have hsym_conv : ∑ x : G, μB x * (indA ∗ᵈ μS) x = ∑ y : G, (μB ∗ᵈ μS) y * indA y := by
      have hμS_even : ∀ z : G, μS (-z) = μS z := fun z ↦ by
        have := congr_fun (conjneg_mu ℝ S) z
        simpa [μS, conjneg_apply, hSsym] using this
      simp_rw [ddconv_eq_sum_sub', Finset.mul_sum, Finset.sum_mul]
      rw [Finset.sum_comm]
      refine Finset.sum_congr rfl fun y _ ↦ ?_
      have hinner : ∑ x : G, μB x * (indA y * μS (x - y)) =
          ∑ x : G, μB x * μS (y - x) * indA y := by
        refine Finset.sum_congr rfl fun x _ ↦ ?_
        have hxy : μS (x - y) = μS (y - x) := by
          rw [← hμS_even (y - x), neg_sub]
        rw [hxy]; ring
      exact hinner
    have hbase : ∑ y : G, μB y * indA y = α_B := by
      have h1' : ∑ y : G, μB y * indA y = ∑ y ∈ A, μB y := by
        rw [← Finset.sum_subset (Finset.subset_univ A)]
        · exact Finset.sum_congr rfl fun y hy ↦ by simp [indA, hy]
        · intro y _ hy; simp [indA, hy]
      have h2' : ∑ y ∈ A, μB y = ∑ _y ∈ A, (#B.finset : ℝ)⁻¹ :=
        Finset.sum_congr rfl fun y hy ↦ by simp [μB, mu_apply, hAB hy]
      rw [h1', h2']
      simp [hα, div_eq_mul_inv]
    have herr : |∑ y : G, ((μB ∗ᵈ μS) y - μB y) * indA y| ≤ ε * α_B / 8 := by
      calc
        |∑ y : G, ((μB ∗ᵈ μS) y - μB y) * indA y|
          ≤ ∑ y : G, |((μB ∗ᵈ μS) y - μB y) * indA y| := Finset.abs_sum_le_sum_abs _ _
        _ ≤ ∑ y : G, |(μB ∗ᵈ μS) y - μB y| := by
            refine Finset.sum_le_sum fun y _ ↦ ?_
            rw [abs_mul]
            refine mul_le_of_le_one_right (abs_nonneg _) ?_
            simp only [indA, Set.indicator_apply]; split_ifs <;> norm_num
        _ = ‖μB ∗ᵈ μS - μB‖_[1] := by rw [dL1Norm_eq_sum_norm]; rfl
        _ ≤ 200 * B.rank * κ :=
            hreg.dL1Norm_mu_ddconv_sub_le hκ₀ hκ mu_nonneg (sum_mu ℝ hS₀)
              (fun y hy ↦ hS_sub (by simpa [μS] using hy))
        _ ≤ ε * α_B / 8 := hκ_small
    change (1 - ε / 8) * α_B ≤ ∑ x : G, μB x * (indA ∗ᵈ μS) x
    rw [hsym_conv]
    have hdiff_eq : ∑ y : G, (μB ∗ᵈ μS) y * indA y - ∑ y : G, μB y * indA y =
        ∑ y : G, ((μB ∗ᵈ μS) y - μB y) * indA y := by
      rw [← Finset.sum_sub_distrib]
      exact Finset.sum_congr rfl fun _ _ ↦ (sub_mul _ _ _).symm
    have hlo := (neg_le_abs _).trans herr
    linarith
  have havg1 := havg_ge B₁ hB₁₀ hB₁sym hB₁_sub
  have havg2 := havg_ge B₂ hB₂₀ hB₂sym hB₂_sub
  let F : G → ℝ := fun x ↦ (𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₁) x + (𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₂) x
  have hsum_F : (2 - ε / 4) * α_B ≤ ∑ x : G, μ_[ℝ] B.finset x * F x := by
    have : ∑ x : G, μ_[ℝ] B.finset x * F x =
        ∑ x : G, μ_[ℝ] B.finset x * (𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₁) x +
        ∑ x : G, μ_[ℝ] B.finset x * (𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₂) x := by
      rw [← Finset.sum_add_distrib]
      exact Finset.sum_congr rfl fun _ _ ↦ mul_add _ _ _
    linarith
  have hex_x : ∃ x ∈ B.finset, (2 - ε / 4) * α_B ≤ F x := by
    by_contra! hlt
    have hsum_lt : ∑ x : G, μ_[ℝ] B.finset x * F x < (2 - ε / 4) * α_B := by
      have hrestrict : ∑ x : G, μ_[ℝ] B.finset x * F x =
          ∑ x ∈ B.finset, (#B.finset : ℝ)⁻¹ * F x := by
        rw [← Finset.sum_subset (Finset.subset_univ B.finset)]
        · exact Finset.sum_congr rfl fun x hx ↦ by simp [mu_apply, hx]
        · intro x _ hx; simp [mu_apply, hx]
      rw [hrestrict]
      have hBpos : (0 : ℝ) < #B.finset := by exact_mod_cast B.card_finset_pos
      calc
        ∑ x ∈ B.finset, (#B.finset : ℝ)⁻¹ * F x
          < ∑ _x ∈ B.finset, (#B.finset : ℝ)⁻¹ * ((2 - ε / 4) * α_B) :=
            Finset.sum_lt_sum_of_nonempty B.finset_nonempty fun x hx ↦
              mul_lt_mul_of_pos_left (hlt x hx) (inv_pos.mpr hBpos)
        _ = (2 - ε / 4) * α_B := by
            simp [mul_inv_cancel_left₀ hBpos.ne']
    linarith
  obtain ⟨x, -, hxF⟩ := hex_x
  have hx1_lt : (𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₁) x < (1 + ε / 4) * α_B :=
    ((le_abs_self _).trans (norm_le_dLinftyNorm (f := 𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₁))).trans_lt h1
  have hx2_lt : (𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₂) x < (1 + ε / 4) * α_B :=
    ((le_abs_self _).trans (norm_le_dLinftyNorm (f := 𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₂))).trans_lt h2
  have hx1_ge : (1 - ε / 2) * α_B ≤ (𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₁) x := by
    dsimp [F] at hxF; linarith
  have hx2_ge : (1 - ε / 2) * α_B ≤ (𝟭_[(A : Set G), ℝ] ∗ᵈ μ B₂) x := by
    dsimp [F] at hxF; linarith
  rw [hcard_eq B₁ hB₁sym x, le_div_iff₀ (by exact_mod_cast hB₁₀.card_pos)] at hx1_ge
  rw [hcard_eq B₂ hB₂sym x, le_div_iff₀ (by exact_mod_cast hB₂₀.card_pos)] at hx2_ge
  exact ⟨x, hx1_ge, hx2_ge⟩

end RegularityConvAndBourgain

end BohrSet
