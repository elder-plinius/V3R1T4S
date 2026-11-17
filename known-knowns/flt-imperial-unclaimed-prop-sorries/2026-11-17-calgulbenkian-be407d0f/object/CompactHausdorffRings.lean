/-
Copyright (c) 2026 Thomas Browning. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Thomas Browning, Kevin Buzzard
-/
module

public import Mathlib.GroupTheory.Divisible
public import Mathlib.Topology.Algebra.Group.CompactOpen
public import Mathlib.Data.Nat.Prime.Defs
import Mathlib.Analysis.Complex.Polynomial.Basic
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Data.Nat.Factorization.Induction
import Mathlib.LinearAlgebra.Eigenspace.Triangularizable
import Mathlib.MeasureTheory.Group.Integral
import Mathlib.MeasureTheory.Integral.Bochner.Set
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.MeasureTheory.Measure.Haar.Basic
import Mathlib.Topology.Algebra.Group.SubmonoidClosure
import Mathlib.Topology.Algebra.Ring.Ideal
import Mathlib.Topology.ContinuousMap.Bounded.ArzelaAscoli
import Mathlib.Topology.ContinuousMap.Compact
import Mathlib.Topology.UrysohnsLemma

/-!
# Compact Hausdorff rings

Structure results for compact Hausdorff topological groups / rings:
in particular, a compact Hausdorff `𝔽_p`-vector space is totally
disconnected, and a connected compact Hausdorff abelian group is divisible.
-/

section SubsingletonAux

open MeasureTheory ComplexConjugate

private lemma geom_sum_mul_sub_one (z : ℂ) (n : ℕ) :
    (∑ j ∈ Finset.range n, z ^ j) * (z - 1) = z ^ n - 1 := by
  induction n with
  | zero => simp
  | succ k ih =>
    rw [Finset.sum_range_succ, add_mul, ih]
    ring

private lemma complex_norm_sub_ofReal_mul_sq (z₁ z₂ : ℂ) (c : ℝ) :
    ‖z₁ - (c : ℂ) * z₂‖ ^ 2 =
      ‖z₁‖ ^ 2 - 2 * c * (conj z₂ * z₁).re + c ^ 2 * ‖z₂‖ ^ 2 := by
  simp only [← Complex.normSq_eq_norm_sq, Complex.normSq_apply, Complex.sub_re, Complex.sub_im,
    Complex.mul_re, Complex.mul_im, Complex.ofReal_re, Complex.ofReal_im, Complex.conj_re,
    Complex.conj_im]
  ring

private noncomputable def trCLM {A : Type*} [CommGroup A] [TopologicalSpace A]
    [IsTopologicalGroup A] [CompactSpace A] (b : A) : C(A, ℂ) →L[ℂ] C(A, ℂ) :=
  LinearMap.mkContinuous
    { toFun := fun u ↦ ⟨fun x ↦ u (b * x), u.continuous.comp (continuous_const_mul b)⟩
      map_add' := fun _ _ ↦ by ext; rfl
      map_smul' := fun _ _ ↦ by ext; rfl }
    1
    (fun u ↦ by
      rw [one_mul, ContinuousMap.norm_le _ (norm_nonneg u)]
      intro x
      exact u.norm_coe_le_norm (b * x))

@[simp]
private lemma trCLM_apply {A : Type*} [CommGroup A] [TopologicalSpace A]
    [IsTopologicalGroup A] [CompactSpace A] (b : A) (u : C(A, ℂ)) (x : A) :
    trCLM b u x = u (b * x) :=
  rfl

private lemma trCLM_comm {A : Type*} [CommGroup A] [TopologicalSpace A]
    [IsTopologicalGroup A] [CompactSpace A] (b c : A) (u : C(A, ℂ)) :
    trCLM b (trCLM c u) = trCLM c (trCLM b u) := by
  ext x
  simp only [trCLM_apply, mul_left_comm]

private lemma continuous_integral_curry {A : Type*} [TopologicalSpace A] [CompactSpace A]
    [MeasurableSpace A] [OpensMeasurableSpace A] (μ : Measure A) [IsProbabilityMeasure μ]
    (H : C(A × A, ℂ)) : Continuous (fun x ↦ ∫ y, H (x, y) ∂μ) := by
  have hLip : LipschitzWith 1 (fun u : C(A, ℂ) ↦ ∫ y, u y ∂μ) := by
    refine LipschitzWith.of_dist_le_mul fun u v ↦ ?_
    rw [NNReal.coe_one, one_mul, dist_eq_norm, dist_eq_norm]
    have hu : Integrable u μ := u.continuous.integrable_of_hasCompactSupport (.of_compactSpace u)
    have hv : Integrable v μ := v.continuous.integrable_of_hasCompactSupport (.of_compactSpace v)
    rw [← integral_sub hu hv]
    calc
      ‖∫ y, u y - v y ∂μ‖ ≤ ∫ y, ‖u y - v y‖ ∂μ := norm_integral_le_integral_norm _
      _ ≤ ∫ _ : A, ‖u - v‖ ∂μ := by
        refine integral_mono ((hu.sub hv).norm) (integrable_const _) fun y ↦ ?_
        exact (u - v).norm_coe_le_norm y
      _ = ‖u - v‖ := by simp
  exact hLip.continuous.comp H.curry.continuous

private theorem mul_subsingleton_of_pow_prime_eq_one_aux
    (A : Type*) [CommGroup A] [TopologicalSpace A] [IsTopologicalGroup A]
    [ConnectedSpace A] [CompactSpace A] [T2Space A]
    (p : ℕ) (hp : p.Prime) (hAp : ∀ a : A, a ^ p = 1) :
    Subsingleton A := by
  refine subsingleton_iff.mpr fun x₁ x₂ ↦ ?_
  suffices h1 : ∀ a₀ : A, a₀ = 1 by rw [h1 x₁, h1 x₂]
  intro a₀
  by_contra ha₀
  borelize A
  let K₀ : TopologicalSpace.PositiveCompacts A := ⟨⟨Set.univ, isCompact_univ⟩, by simp⟩
  let μ : Measure A := Measure.haarMeasure K₀
  have hμ_univ : μ Set.univ = 1 := Measure.haarMeasure_self
  have : IsProbabilityMeasure μ := ⟨hμ_univ⟩
  have int_cont : ∀ {E : Type} [NormedAddCommGroup E] {f : A → E},
      Continuous f → Integrable f μ :=
    fun hf ↦ hf.integrable_of_hasCompactSupport (.of_compactSpace _)
  -- Step 1: Closed A-invariant subspace V where the <a₀>-orbit sum vanishes.
  let P_op : C(A, ℂ) →L[ℂ] C(A, ℂ) := ∑ j ∈ Finset.range p, trCLM (a₀ ^ j)
  let V : Submodule ℂ C(A, ℂ) := LinearMap.ker P_op.toLinearMap
  have hV_mem : ∀ {u : C(A, ℂ)}, u ∈ V ↔ ∀ x : A, ∑ j ∈ Finset.range p, u (a₀ ^ j * x) = 0 := by
    intro u
    simp only [V, LinearMap.mem_ker, ContinuousLinearMap.coe_coe, P_op,
      sum_apply, ContinuousMap.ext_iff, ContinuousMap.sum_apply,
      trCLM_apply, ContinuousMap.zero_apply]
  have hV_closed : IsClosed (V : Set C(A, ℂ)) := P_op.isClosed_ker
  have hV_tr : ∀ (b : A) {u : C(A, ℂ)}, u ∈ V → trCLM b u ∈ V := by
    intro b u hu
    rw [hV_mem] at hu ⊢
    intro x
    simpa only [trCLM_apply, mul_left_comm] using hu (b * x)
  -- Step 2: Separate a₀ and 1 by Urysohn to build g₀ ∈ V with g₀ 1 = -1.
  obtain ⟨fR, hfR_a₀, hfR_one, -⟩ := exists_continuous_zero_one_of_isClosed
    (isClosed_singleton : IsClosed ({a₀} : Set A)) isClosed_singleton
    (Set.disjoint_singleton.mpr ha₀)
  let fC : C(A, ℂ) := ⟨fun x ↦ (fR x : ℂ), Complex.continuous_ofReal.comp fR.continuous⟩
  let g₀ : C(A, ℂ) := trCLM a₀ fC - fC
  have hg₀_one : g₀ 1 = -1 := by
    have h0 : fR a₀ = 0 := hfR_a₀ rfl
    have h1 : fR 1 = 1 := hfR_one rfl
    simp [g₀, fC, h0, h1]
  have hg₀_mem : g₀ ∈ V := by
    rw [hV_mem]
    intro x
    have hstep : ∀ j : ℕ, g₀ (a₀ ^ j * x) = fC (a₀ ^ (j + 1) * x) - fC (a₀ ^ j * x) := by
      intro j
      simp only [g₀, ContinuousMap.sub_apply, trCLM_apply, ← mul_assoc, ← pow_succ']
    simp_rw [hstep]
    rw [Finset.sum_range_sub (fun j ↦ fC (a₀ ^ j * x)) p, hAp a₀, pow_zero, sub_self]
  -- Step 3: Hermitian continuous convolution kernel k and operator T.
  let H_k : C(A × A, ℂ) :=
    ⟨fun q ↦ conj (g₀ q.2) * g₀ (q.2 * q.1), by fun_prop⟩
  let k : C(A, ℂ) := ⟨fun z ↦ ∫ w, H_k (z, w) ∂μ, continuous_integral_curry μ H_k⟩
  have hk_apply : ∀ z : A, k z = ∫ w, conj (g₀ w) * g₀ (w * z) ∂μ := fun _ ↦ rfl
  have hk_one_ne : k 1 ≠ 0 := by
    intro hk0
    have hre : (k 1).re = ∫ w, ‖g₀ w‖ ^ 2 ∂μ := by
      rw [hk_apply]
      have hInt : Integrable (fun w ↦ conj (g₀ w) * g₀ (w * 1)) μ :=
        int_cont (by fun_prop)
      rw [← Complex.reCLM_apply, ← Complex.reCLM.integral_comp_comm hInt]
      refine integral_congr_ae (Filter.Eventually.of_forall fun w ↦ ?_)
      simp only [mul_one, Complex.reCLM_apply, Complex.conj_mul', ← Complex.ofReal_pow,
        Complex.ofReal_re]
    have hpos : 0 < ∫ w, ‖g₀ w‖ ^ 2 ∂μ := by
      refine Continuous.integral_pos_of_hasCompactSupport_nonneg_nonzero (x := 1)
        (by fun_prop) (.of_compactSpace _) (fun w ↦ sq_nonneg _) ?_
      rw [hg₀_one]
      norm_num
    rw [hk0, Complex.zero_re] at hre
    linarith
  have hk_symm : ∀ z : A, k z⁻¹ = conj (k z) := by
    intro z
    rw [hk_apply, hk_apply, ← integral_conj]
    rw [← integral_mul_left_eq_self (fun w ↦ conj (g₀ w) * g₀ (w * z⁻¹)) z]
    refine integral_congr_ae (Filter.Eventually.of_forall fun w ↦ ?_)
    dsimp only
    have hw : z * w * z⁻¹ = w := by rw [mul_comm z w, mul_inv_cancel_right]
    rw [hw, mul_comm z w]
    simp only [map_mul, RingHomCompTriple.comp_apply, RingHom.id_apply]
    ring
  have hstark_mem : star k ∈ V := by
    rw [hV_mem]
    intro x
    have hsum : ∀ j ∈ Finset.range p,
        Integrable (fun w ↦ g₀ w * conj (g₀ (w * (a₀ ^ j * x)))) μ :=
      fun _ _ ↦ int_cont (by fun_prop)
    have hterm : ∀ j : ℕ, (star k) (a₀ ^ j * x) =
        ∫ w, g₀ w * conj (g₀ (w * (a₀ ^ j * x))) ∂μ := by
      intro j
      change conj (k (a₀ ^ j * x)) = _
      rw [hk_apply, ← integral_conj]
      refine integral_congr_ae (Filter.Eventually.of_forall fun w ↦ ?_)
      dsimp only
      rw [map_mul, RingHomCompTriple.comp_apply, RingHom.id_apply]
    simp_rw [hterm]
    rw [← integral_finsetSum (Finset.range p) hsum]
    have hzero : ∀ w : A, ∑ j ∈ Finset.range p, g₀ w * conj (g₀ (w * (a₀ ^ j * x))) = 0 := by
      intro w
      rw [← Finset.mul_sum, ← map_sum]
      have hw : ∑ j ∈ Finset.range p, g₀ (w * (a₀ ^ j * x)) = 0 := by
        simpa only [mul_left_comm w] using hV_mem.mp hg₀_mem (w * x)
      rw [hw, map_zero, mul_zero]
    simp_rw [hzero, integral_zero]
  let T_map : C(A, ℂ) →ₗ[ℂ] C(A, ℂ) :=
    { toFun := fun u ↦
        ⟨fun x ↦ ∫ y, k (x⁻¹ * y) * u y ∂μ,
          continuous_integral_curry μ ⟨fun q ↦ k (q.1⁻¹ * q.2) * u q.2, by fun_prop⟩⟩
      map_add' := fun u v ↦ by
        ext x
        simp only [ContinuousMap.coe_mk, ContinuousMap.add_apply, mul_add]
        exact integral_add (int_cont (by fun_prop)) (int_cont (by fun_prop))
      map_smul' := fun c u ↦ by
        ext x
        simp only [ContinuousMap.coe_mk, ContinuousMap.smul_apply, smul_eq_mul, RingHom.id_apply,
          mul_left_comm _ c]
        exact integral_const_mul c _ }
  let T : C(A, ℂ) →L[ℂ] C(A, ℂ) :=
    LinearMap.mkContinuous T_map ‖k‖ fun u ↦ by
      rw [ContinuousMap.norm_le _ (mul_nonneg (norm_nonneg k) (norm_nonneg u))]
      intro x
      change ‖∫ y, k (x⁻¹ * y) * u y ∂μ‖ ≤ ‖k‖ * ‖u‖
      calc
        ‖∫ y, k (x⁻¹ * y) * u y ∂μ‖ ≤ ∫ y, ‖k (x⁻¹ * y) * u y‖ ∂μ :=
          norm_integral_le_integral_norm _
        _ ≤ ∫ _ : A, ‖k‖ * ‖u‖ ∂μ := by
          refine integral_mono (int_cont (by fun_prop)) (integrable_const _) fun y ↦ ?_
          rw [norm_mul]
          exact mul_le_mul (k.norm_coe_le_norm _) (u.norm_coe_le_norm _)
            (norm_nonneg _) (norm_nonneg k)
        _ = ‖k‖ * ‖u‖ := by simp
  have hT_apply : ∀ (u : C(A, ℂ)) (x : A), T u x = ∫ y, k (x⁻¹ * y) * u y ∂μ := fun _ _ ↦ rfl
  have hT_comm : ∀ (b : A) (u : C(A, ℂ)), T (trCLM b u) = trCLM b (T u) := by
    intro b u
    ext x
    rw [hT_apply, trCLM_apply, hT_apply]
    rw [← integral_mul_left_eq_self (fun y ↦ k (x⁻¹ * y) * trCLM b u y) b⁻¹]
    refine integral_congr_ae (Filter.Eventually.of_forall fun y ↦ ?_)
    dsimp only
    have hy : x⁻¹ * (b⁻¹ * y) = (b * x)⁻¹ * y := by rw [mul_inv_rev, mul_assoc]
    simp only [trCLM_apply, mul_inv_cancel_left, hy]
  have hT_V : ∀ {u : C(A, ℂ)}, u ∈ V → T u ∈ V := by
    intro u hu
    rw [hV_mem] at hu ⊢
    intro x
    have h1 : ∀ j : ℕ, T u (a₀ ^ j * x) = T (trCLM (a₀ ^ j) u) x := by
      intro j
      rw [hT_comm, trCLM_apply]
    simp_rw [h1]
    rw [← ContinuousMap.sum_apply, ← map_sum]
    have h2 : ∑ j ∈ Finset.range p, trCLM (a₀ ^ j) u = 0 := by
      ext y
      simpa only [ContinuousMap.sum_apply, trCLM_apply, ContinuousMap.zero_apply] using hu y
    rw [h2, map_zero, ContinuousMap.zero_apply]
  have hT_stark_ne : T (star k) ≠ 0 := by
    intro h0
    have hre : (T (star k) 1).re = ∫ y, ‖k y‖ ^ 2 ∂μ := by
      rw [hT_apply]
      have hInt : Integrable (fun y ↦ k (1⁻¹ * y) * (star k) y) μ :=
        int_cont (by fun_prop)
      rw [← Complex.reCLM_apply, ← Complex.reCLM.integral_comp_comm hInt]
      refine integral_congr_ae (Filter.Eventually.of_forall fun y ↦ ?_)
      change (k (1⁻¹ * y) * conj (k y)).re = ‖k y‖ ^ 2
      simp only [inv_one, one_mul, Complex.mul_conj', ← Complex.ofReal_pow, Complex.ofReal_re]
    have hpos : 0 < ∫ y, ‖k y‖ ^ 2 ∂μ :=
      Continuous.integral_pos_of_hasCompactSupport_nonneg_nonzero (x := 1)
        (by fun_prop) (.of_compactSpace _) (fun y ↦ sq_nonneg _)
        (pow_ne_zero 2 (norm_ne_zero_iff.mpr hk_one_ne))
    rw [h0, ContinuousMap.zero_apply, Complex.zero_re] at hre
    linarith
  -- Step 4: L2 norm & Hermitian symmetry on C(A, ℂ).
  let l2sq : C(A, ℂ) → ℝ := fun u ↦ ∫ x, ‖u x‖ ^ 2 ∂μ
  let l2 : C(A, ℂ) → ℝ := fun u ↦ Real.sqrt (l2sq u)
  let ip : C(A, ℂ) → C(A, ℂ) → ℂ := fun u v ↦ ∫ x, conj (u x) * v x ∂μ
  have hl2sq_nonneg : ∀ u : C(A, ℂ), 0 ≤ l2sq u :=
    fun u ↦ integral_nonneg fun _ ↦ sq_nonneg _
  have hl2_nonneg : ∀ u : C(A, ℂ), 0 ≤ l2 u := fun u ↦ Real.sqrt_nonneg _
  have hl2_sq : ∀ u : C(A, ℂ), l2 u ^ 2 = l2sq u :=
    fun u ↦ Real.sq_sqrt (hl2sq_nonneg u)
  have hl2_eq_zero : ∀ {u : C(A, ℂ)}, l2 u = 0 ↔ u = 0 := by
    intro u
    constructor
    · intro h0
      have hsq : l2sq u = 0 := by rw [← hl2_sq u, h0, sq, mul_zero]
      by_contra hu0
      have ⟨x₀, hx₀⟩ : ∃ x₀ : A, u x₀ ≠ 0 := by
        by_contra! hall
        apply hu0
        ext x
        exact hall x
      have hpos : 0 < l2sq u :=
        Continuous.integral_pos_of_hasCompactSupport_nonneg_nonzero (x := x₀)
          (by fun_prop) (.of_compactSpace _) (fun _ ↦ sq_nonneg _)
          (pow_ne_zero 2 (norm_ne_zero_iff.mpr hx₀))
      linarith
    · rintro rfl
      simp [l2, l2sq]
  have hl2_le_norm : ∀ u : C(A, ℂ), l2 u ≤ ‖u‖ := by
    intro u
    rw [← Real.sqrt_sq (norm_nonneg u)]
    refine Real.sqrt_le_sqrt ?_
    calc
      l2sq u ≤ ∫ _ : A, ‖u‖ ^ 2 ∂μ := by
        refine integral_mono (int_cont (by fun_prop)) (integrable_const _) fun x ↦ ?_
        exact pow_le_pow_left₀ (norm_nonneg _) (u.norm_coe_le_norm x) 2
      _ = ‖u‖ ^ 2 := by simp
  have hl2_cont : Continuous l2 := by
    suffices Continuous l2sq from Real.continuous_sqrt.comp this
    rw [Metric.continuous_iff]
    intro u ε hε
    refine ⟨min 1 (ε / (2 * ‖u‖ + 2)), by positivity, fun v hvu ↦ ?_⟩
    have hlt1 : ‖v - u‖ < 1 :=
      lt_of_lt_of_le (by simpa [dist_eq_norm] using hvu) (min_le_left _ _)
    have hlt2 : ‖v - u‖ < ε / (2 * ‖u‖ + 2) :=
      lt_of_lt_of_le (by simpa [dist_eq_norm] using hvu) (min_le_right _ _)
    have hv_norm : ‖v‖ ≤ ‖u‖ + 1 := by
      have := norm_sub_norm_le v u
      linarith
    rw [Real.dist_eq]
    have hdiff : l2sq v - l2sq u = ∫ x, (‖v x‖ ^ 2 - ‖u x‖ ^ 2) ∂μ :=
      (integral_sub (int_cont (by fun_prop)) (int_cont (by fun_prop))).symm
    rw [hdiff]
    calc
      |∫ x, (‖v x‖ ^ 2 - ‖u x‖ ^ 2) ∂μ|
        ≤ ∫ x, |‖v x‖ ^ 2 - ‖u x‖ ^ 2| ∂μ := by
          simpa only [Real.norm_eq_abs] using
            norm_integral_le_integral_norm (fun x ↦ ‖v x‖ ^ 2 - ‖u x‖ ^ 2)
      _ ≤ ∫ _ : A, ‖v - u‖ * (2 * ‖u‖ + 1) ∂μ := by
        refine integral_mono (int_cont (by fun_prop)) (integrable_const _) fun x ↦ ?_
        have h1 : |‖v x‖ - ‖u x‖| ≤ ‖(v - u) x‖ := abs_norm_sub_norm_le (v x) (u x)
        have h2 : ‖(v - u) x‖ ≤ ‖v - u‖ := (v - u).norm_coe_le_norm x
        have h3 : ‖v x‖ + ‖u x‖ ≤ 2 * ‖u‖ + 1 := by
          have := v.norm_coe_le_norm x
          have := u.norm_coe_le_norm x
          linarith
        have h4 : |‖v x‖ ^ 2 - ‖u x‖ ^ 2| = |‖v x‖ - ‖u x‖| * (‖v x‖ + ‖u x‖) := by
          rw [sq_sub_sq, abs_mul, abs_of_nonneg (by positivity), mul_comm]
        rw [h4]
        exact mul_le_mul (h1.trans h2) h3 (by positivity) (norm_nonneg _)
      _ = ‖v - u‖ * (2 * ‖u‖ + 1) := by simp
      _ < (ε / (2 * ‖u‖ + 2)) * (2 * ‖u‖ + 2) := by
        refine mul_lt_mul'' hlt2 ?_ (norm_nonneg _) (by positivity)
        linarith
      _ = ε := div_mul_cancel₀ ε (by positivity)
  have hip_self_re : ∀ u : C(A, ℂ), (ip u u).re = l2sq u := by
    intro u
    have hInt : Integrable (fun x ↦ conj (u x) * u x) μ := int_cont (by fun_prop)
    change (∫ x, conj (u x) * u x ∂μ).re = ∫ x, ‖u x‖ ^ 2 ∂μ
    rw [← Complex.reCLM_apply, ← Complex.reCLM.integral_comp_comm hInt]
    refine integral_congr_ae (Filter.Eventually.of_forall fun x ↦ ?_)
    simp only [Complex.reCLM_apply, Complex.conj_mul', ← Complex.ofReal_pow, Complex.ofReal_re]
  have hip_symm : ∀ u v : C(A, ℂ), ip u (T v) = ip (T u) v := by
    intro u v
    dsimp only [ip]
    have hL : ∀ x : A, conj (u x) * T v x = ∫ y, conj (u x) * (k (x⁻¹ * y) * v y) ∂μ := by
      intro x
      rw [hT_apply, integral_const_mul]
    simp_rw [hL]
    let F : A → A → ℂ := fun x y ↦ conj (u x) * (k (x⁻¹ * y) * v y)
    have hF_cont : Continuous F.uncurry := by
      change Continuous (fun q : A × A ↦ conj (u q.1) * (k (q.1⁻¹ * q.2) * v q.2))
      fun_prop
    rw [integral_integral_swap_of_hasCompactSupport hF_cont (.of_compactSpace _)]
    refine integral_congr_ae (Filter.Eventually.of_forall fun y ↦ ?_)
    have hR : conj (T u y) * v y = ∫ x, F x y ∂μ := by
      rw [hT_apply, ← integral_conj, ← integral_mul_const]
      refine integral_congr_ae (Filter.Eventually.of_forall fun x ↦ ?_)
      have hk_yx : conj (k (y⁻¹ * x)) = k (x⁻¹ * y) := by
        have := hk_symm (y⁻¹ * x)
        simp only [mul_inv_rev, inv_inv] at this
        exact this.symm
      dsimp only
      simp only [F, map_mul, hk_yx]
      ring
    exact hR.symm
  have hip_cs : ∀ u v : C(A, ℂ), ‖ip u v‖ ≤ l2 u * l2 v := by
    intro u v
    by_cases hu : l2 u = 0
    · rw [hl2_eq_zero.mp hu]
      simp [ip, l2, l2sq]
    by_cases hv : l2 v = 0
    · rw [hl2_eq_zero.mp hv]
      simp [ip, l2, l2sq]
    have hu_pos : 0 < l2 u := lt_of_le_of_ne (hl2_nonneg u) (Ne.symm hu)
    have hv_pos : 0 < l2 v := lt_of_le_of_ne (hl2_nonneg v) (Ne.symm hv)
    have hprod_pos : 0 < l2 u * l2 v := mul_pos hu_pos hv_pos
    have hstep1 : ‖ip u v‖ ≤ ∫ x, ‖u x‖ * ‖v x‖ ∂μ := by
      calc
        ‖ip u v‖ ≤ ∫ x, ‖conj (u x) * v x‖ ∂μ := norm_integral_le_integral_norm _
        _ = ∫ x, ‖u x‖ * ‖v x‖ ∂μ := by simp_rw [norm_mul, RingHomIsometric.norm_map]
    refine hstep1.trans ?_
    rw [← div_le_one hprod_pos, ← integral_div]
    have hpt : ∀ x : A, (‖u x‖ * ‖v x‖) / (l2 u * l2 v) ≤
        (‖u x‖ ^ 2 / l2 u ^ 2 + ‖v x‖ ^ 2 / l2 v ^ 2) / 2 := by
      intro x
      have hsq : 0 ≤ (‖u x‖ / l2 u - ‖v x‖ / l2 v) ^ 2 := sq_nonneg _
      have hmul : (‖u x‖ / l2 u) * (‖v x‖ / l2 v) = (‖u x‖ * ‖v x‖) / (l2 u * l2 v) :=
        div_mul_div_comm _ _ _ _
      have hpow1 : (‖u x‖ / l2 u) ^ 2 = ‖u x‖ ^ 2 / l2 u ^ 2 := div_pow _ _ 2
      have hpow2 : (‖v x‖ / l2 v) ^ 2 = ‖v x‖ ^ 2 / l2 v ^ 2 := div_pow _ _ 2
      linarith
    have hi_u : Integrable (fun x ↦ ‖u x‖ ^ 2 / l2 u ^ 2) μ := int_cont (by fun_prop)
    have hi_v : Integrable (fun x ↦ ‖v x‖ ^ 2 / l2 v ^ 2) μ := int_cont (by fun_prop)
    calc
      ∫ x, (‖u x‖ * ‖v x‖) / (l2 u * l2 v) ∂μ
        ≤ ∫ x, (‖u x‖ ^ 2 / l2 u ^ 2 + ‖v x‖ ^ 2 / l2 v ^ 2) / 2 ∂μ :=
          integral_mono (int_cont (by fun_prop)) (int_cont (by fun_prop)) hpt
      _ = (l2sq u / l2 u ^ 2 + l2sq v / l2 v ^ 2) / 2 := by
        rw [integral_div, integral_add hi_u hi_v, integral_div, integral_div]
      _ = 1 := by
        rw [← hl2_sq u, ← hl2_sq v, div_self (pow_ne_zero 2 hu_pos.ne'),
          div_self (pow_ne_zero 2 hv_pos.ne')]
        norm_num
  -- Step 5: Compactness of K_V = closure (T '' B_V) via Arzelà-Ascoli.
  let B_V : Set C(A, ℂ) := {u | u ∈ V ∧ l2 u ≤ 1}
  let S : Set C(A, ℂ) := T '' B_V
  let K_V : Set C(A, ℂ) := closure S
  have hl1_of_BV : ∀ {u : C(A, ℂ)}, u ∈ B_V → ∫ y, ‖u y‖ ∂μ ≤ 2 := by
    rintro u ⟨-, hu⟩
    have hsq1 : l2sq u ≤ 1 := by
      have := mul_self_le_mul_self (hl2_nonneg u) hu
      rwa [← sq, hl2_sq u, mul_one] at this
    have hi_sq : Integrable (fun y ↦ ‖u y‖ ^ 2) μ := int_cont (by fun_prop)
    calc
      ∫ y, ‖u y‖ ∂μ ≤ ∫ y, (‖u y‖ ^ 2 + 1) ∂μ :=
        integral_mono (int_cont (by fun_prop)) (int_cont (by fun_prop)) fun y ↦ by nlinarith
      _ = l2sq u + 1 := by
        rw [integral_add hi_sq (integrable_const _)]
        simp [l2sq]
      _ ≤ 2 := by linarith
  have hS_bound : ∀ f ∈ S, ∀ x : A, ‖f x‖ ≤ 2 * ‖k‖ := by
    rintro _ ⟨u, hu, rfl⟩ x
    rw [hT_apply]
    calc
      ‖∫ y, k (x⁻¹ * y) * u y ∂μ‖ ≤ ∫ y, ‖k (x⁻¹ * y) * u y‖ ∂μ :=
        norm_integral_le_integral_norm _
      _ ≤ ∫ y, ‖k‖ * ‖u y‖ ∂μ := by
        refine integral_mono (int_cont (by fun_prop)) (int_cont (by fun_prop)) fun y ↦ ?_
        rw [norm_mul]
        exact mul_le_mul_of_nonneg_right (k.norm_coe_le_norm _) (norm_nonneg _)
      _ = ‖k‖ * ∫ y, ‖u y‖ ∂μ := integral_const_mul _ _
      _ ≤ 2 * ‖k‖ := by
        have := hl1_of_BV hu
        nlinarith [norm_nonneg k]
  have hKV_compact : IsCompact K_V := by
    let e := ContinuousMap.linearIsometryBoundedOfCompact A ℂ ℂ
    let S' : Set (BoundedContinuousFunction A ℂ) := e '' S
    have hS'_comp : IsCompact (closure S') := by
      refine BoundedContinuousFunction.arzela_ascoli
        (Metric.closedBall (0 : ℂ) (2 * ‖k‖)) (isCompact_closedBall _ _) S' ?_ ?_
      · rintro _ x ⟨f, hf, rfl⟩
        simp only [e, ContinuousMap.linearIsometryBoundedOfCompact_apply_apply,
          Metric.mem_closedBall, dist_zero_right]
        exact hS_bound f hf x
      · intro x₀
        rw [Metric.equicontinuousAt_iff_right]
        intro ε hε
        let Ψ : C(A, C(A, ℂ)) :=
          ContinuousMap.curry ⟨fun q : A × A ↦ k (q.1⁻¹ * q.2), by fun_prop⟩
        have hΨ : ∀ᶠ x in nhds x₀, dist (Ψ x) (Ψ x₀) < ε / 3 :=
          Metric.tendsto_nhds.mp Ψ.continuous.continuousAt (ε / 3) (by positivity)
        filter_upwards [hΨ] with x hx
        rintro ⟨_, f, ⟨u, hu, rfl⟩, rfl⟩
        simp only [e, ContinuousMap.linearIsometryBoundedOfCompact_apply_apply]
        have hi0 : Integrable (fun y ↦ k (x₀⁻¹ * y) * u y) μ := int_cont (by fun_prop)
        have hi1 : Integrable (fun y ↦ k (x⁻¹ * y) * u y) μ := int_cont (by fun_prop)
        rw [dist_eq_norm, hT_apply, hT_apply, ← integral_sub hi0 hi1]
        calc
          ‖∫ y, (k (x₀⁻¹ * y) * u y - k (x⁻¹ * y) * u y) ∂μ‖
            ≤ ∫ y, ‖k (x₀⁻¹ * y) * u y - k (x⁻¹ * y) * u y‖ ∂μ :=
              norm_integral_le_integral_norm _
          _ ≤ ∫ y, ‖Ψ x₀ - Ψ x‖ * ‖u y‖ ∂μ := by
            refine integral_mono (int_cont (by fun_prop)) (int_cont (by fun_prop)) fun y ↦ ?_
            rw [← sub_mul, norm_mul]
            exact mul_le_mul_of_nonneg_right ((Ψ x₀ - Ψ x).norm_coe_le_norm y) (norm_nonneg _)
          _ = ‖Ψ x₀ - Ψ x‖ * ∫ y, ‖u y‖ ∂μ := integral_const_mul _ _
          _ ≤ ‖Ψ x₀ - Ψ x‖ * 2 :=
            mul_le_mul_of_nonneg_left (hl1_of_BV hu) (norm_nonneg _)
          _ < (ε / 3) * 2 := by
            rw [dist_comm, dist_eq_norm] at hx
            linarith
          _ < ε := by linarith
    have heq : K_V = e.toHomeomorph.symm '' closure S' := by
      dsimp only [K_V]
      rw [Homeomorph.image_closure e.toHomeomorph.symm S']
      dsimp only [S']
      rw [← Set.image_comp]
      simp [Function.comp_def]
    rw [heq]
    exact hS'_comp.image e.toHomeomorph.symm.continuous
  have hKV_sub_V : K_V ⊆ (V : Set C(A, ℂ)) := by
    refine closure_minimal ?_ hV_closed
    rintro _ ⟨u, ⟨hu, -⟩, rfl⟩
    exact hT_V hu
  -- Step 6: Rayleigh quotient maximization on K_V -> nonzero eigenvector of T^2 in V.
  let Rset : Set ℝ := (fun u ↦ l2 (T u)) '' B_V
  have hR_bdd : BddAbove Rset := by
    refine ⟨2 * ‖k‖, ?_⟩
    rintro _ ⟨u, hu, rfl⟩
    refine (hl2_le_norm (T u)).trans ?_
    rw [ContinuousMap.norm_le _ (mul_nonneg zero_le_two (norm_nonneg k))]
    exact hS_bound (T u) ⟨u, hu, rfl⟩
  let lam : ℝ := sSup Rset
  have hl2_smul : ∀ (r : ℝ) (u : C(A, ℂ)), 0 ≤ r → l2 ((r : ℂ) • u) = r * l2 u := by
    intro r u hr
    have hsq : l2sq ((r : ℂ) • u) = r ^ 2 * l2sq u := by
      dsimp only [l2sq]
      rw [← integral_const_mul]
      refine integral_congr_ae (Filter.Eventually.of_forall fun x ↦ ?_)
      simp only [ContinuousMap.smul_apply, smul_eq_mul, norm_mul, Complex.norm_real,
        Real.norm_of_nonneg hr, mul_pow]
    dsimp only [l2]
    rw [hsq, Real.sqrt_mul (sq_nonneg r), Real.sqrt_sq hr]
  have hlam_bound : ∀ {u : C(A, ℂ)}, u ∈ V → l2 (T u) ≤ lam * l2 u := by
    intro u hu
    by_cases h0 : l2 u = 0
    · simp [hl2_eq_zero.mp h0, l2, l2sq]
    have hpos : 0 < l2 u := lt_of_le_of_ne (hl2_nonneg u) (Ne.symm h0)
    let u₁ : C(A, ℂ) := ((l2 u)⁻¹ : ℂ) • u
    have hu₁_BV : u₁ ∈ B_V := by
      refine ⟨V.smul_mem _ hu, ?_⟩
      have h1 : u₁ = (((l2 u)⁻¹ : ℝ) : ℂ) • u := by simp [u₁]
      rw [h1, hl2_smul (l2 u)⁻¹ u (inv_nonneg.mpr hpos.le), inv_mul_cancel₀ hpos.ne']
    have hmem : l2 (T u₁) ∈ Rset := ⟨u₁, hu₁_BV, rfl⟩
    have hle : l2 (T u₁) ≤ lam := le_csSup hR_bdd hmem
    have hTu₁ : l2 (T u₁) = (l2 u)⁻¹ * l2 (T u) := by
      have h1 : T u₁ = (((l2 u)⁻¹ : ℝ) : ℂ) • T u := by simp [u₁, map_smul]
      rw [h1, hl2_smul (l2 u)⁻¹ (T u) (inv_nonneg.mpr hpos.le)]
    rw [hTu₁, inv_mul_le_iff₀ hpos] at hle
    rwa [mul_comm]
  have hlam_pos : 0 < lam := by
    have h1 : 0 < l2 (T (star k)) :=
      lt_of_le_of_ne (hl2_nonneg _) (Ne.symm (mt hl2_eq_zero.mp hT_stark_ne))
    have h2 : l2 (T (star k)) ≤ lam * l2 (star k) := hlam_bound hstark_mem
    have h3 : 0 ≤ l2 (star k) := hl2_nonneg _
    nlinarith
  have hKV_l2 : ∀ w ∈ K_V, l2 w ≤ lam := by
    have hS_l2 : S ⊆ {w | l2 w ≤ lam} := by
      rintro _ ⟨u, ⟨huV, hu1⟩, rfl⟩
      exact (hlam_bound huV).trans (mul_le_of_le_one_right hlam_pos.le hu1)
    exact closure_minimal hS_l2 (isClosed_le hl2_cont continuous_const)
  have h0_KV : (0 : C(A, ℂ)) ∈ K_V :=
    subset_closure ⟨0, ⟨V.zero_mem, by simp [l2, l2sq]⟩, map_zero T⟩
  obtain ⟨w0, hw0_KV, hw0_max⟩ :=
    hKV_compact.exists_isMaxOn ⟨0, h0_KV⟩ (hl2_cont.comp T.continuous).continuousOn
  have hw0_V : w0 ∈ V := hKV_sub_V hw0_KV
  have hlam_sq_le : lam ^ 2 ≤ l2 (T w0) := by
    have hle_sqrt : lam ≤ Real.sqrt (l2 (T w0)) := by
      refine csSup_le ⟨0, ⟨0, ⟨V.zero_mem, by simp [l2, l2sq]⟩, by simp [l2, l2sq]⟩⟩ ?_
      rintro _ ⟨u, hu, rfl⟩
      have hTu_KV : T u ∈ K_V := subset_closure ⟨u, hu, rfl⟩
      have hmax : l2 (T (T u)) ≤ l2 (T w0) := hw0_max hTu_KV
      have hsq_u : l2 (T u) ^ 2 ≤ l2 (T w0) := by
        calc
          l2 (T u) ^ 2 = l2sq (T u) := hl2_sq (T u)
          _ = (ip (T u) (T u)).re := (hip_self_re (T u)).symm
          _ = (ip u (T (T u))).re := by rw [hip_symm u (T u)]
          _ ≤ ‖ip u (T (T u))‖ := Complex.re_le_norm _
          _ ≤ l2 u * l2 (T (T u)) := hip_cs u (T (T u))
          _ ≤ 1 * l2 (T w0) := mul_le_mul hu.2 hmax (hl2_nonneg _) zero_le_one
          _ = l2 (T w0) := one_mul _
      dsimp only
      rw [← Real.sqrt_sq (hl2_nonneg (T u))]
      exact Real.sqrt_le_sqrt hsq_u
    have := mul_self_le_mul_self hlam_pos.le hle_sqrt
    rwa [← sq, Real.mul_self_sqrt (hl2_nonneg (T w0))] at this
  have hw0_l2_le : l2 w0 ≤ lam := hKV_l2 w0 hw0_KV
  have hTw0_le : l2 (T w0) ≤ lam * l2 w0 := hlam_bound hw0_V
  have hw0_l2_eq : l2 w0 = lam := by nlinarith
  have hTw0_l2_eq : l2 (T w0) = lam ^ 2 := by nlinarith
  have hw0_ne : w0 ≠ 0 := by
    intro h0
    rw [h0, hl2_eq_zero.mpr rfl] at hw0_l2_eq
    linarith
  have hw0_eig : T (T w0) = ((lam ^ 2 : ℝ) : ℂ) • w0 := by
    suffices l2 (T (T w0) - ((lam ^ 2 : ℝ) : ℂ) • w0) = 0 by
      exact sub_eq_zero.mp (hl2_eq_zero.mp this)
    have hsq0 : l2sq (T (T w0) - ((lam ^ 2 : ℝ) : ℂ) • w0) ≤ 0 := by
      have hexp : l2sq (T (T w0) - ((lam ^ 2 : ℝ) : ℂ) • w0) =
          l2sq (T (T w0)) - 2 * lam ^ 2 * (ip w0 (T (T w0))).re +
            (lam ^ 2) ^ 2 * l2sq w0 := by
        dsimp only [l2sq]
        have hpt : ∀ x : A, ‖(T (T w0) - ((lam ^ 2 : ℝ) : ℂ) • w0) x‖ ^ 2 =
            ‖T (T w0) x‖ ^ 2 - 2 * lam ^ 2 * (conj (w0 x) * T (T w0) x).re +
              (lam ^ 2) ^ 2 * ‖w0 x‖ ^ 2 := by
          intro x
          exact complex_norm_sub_ofReal_mul_sq (T (T w0) x) (w0 x) (lam ^ 2)
        simp_rw [hpt]
        have hi1 : Integrable (fun x ↦ ‖T (T w0) x‖ ^ 2) μ := int_cont (by fun_prop)
        have hi2 : Integrable (fun x ↦ 2 * lam ^ 2 * (conj (w0 x) * T (T w0) x).re) μ :=
          int_cont (by fun_prop)
        have hi3 : Integrable (fun x ↦ (lam ^ 2) ^ 2 * ‖w0 x‖ ^ 2) μ :=
          int_cont (by fun_prop)
        have hi12 : Integrable (fun x ↦ ‖T (T w0) x‖ ^ 2 -
            2 * lam ^ 2 * (conj (w0 x) * T (T w0) x).re) μ := hi1.sub hi2
        rw [integral_add hi12 hi3, integral_sub hi1 hi2, integral_const_mul,
          integral_const_mul]
        have hre : ∫ x, (conj (w0 x) * T (T w0) x).re ∂μ = (ip w0 (T (T w0))).re := by
          have hInt : Integrable (fun x ↦ conj (w0 x) * T (T w0) x) μ :=
            int_cont (by fun_prop)
          rw [← Complex.reCLM_apply, ← Complex.reCLM.integral_comp_comm hInt]
          rfl
        rw [hre]
      have hip_val : (ip w0 (T (T w0))).re = lam ^ 4 := by
        rw [hip_symm w0 (T w0), hip_self_re, ← hl2_sq, hTw0_l2_eq]
        ring
      have hl2sq_w : l2sq w0 = lam ^ 2 := by rw [← hl2_sq, hw0_l2_eq]
      have hTT_le : l2sq (T (T w0)) ≤ lam ^ 6 := by
        have h1 : l2 (T (T w0)) ≤ lam ^ 3 := by
          calc
            l2 (T (T w0)) ≤ lam * l2 (T w0) := hlam_bound (hT_V hw0_V)
            _ = lam ^ 3 := by rw [hTw0_l2_eq]; ring
        have := mul_self_le_mul_self (hl2_nonneg _) h1
        rw [← sq, hl2_sq] at this
        linarith [show lam ^ 3 * lam ^ 3 = lam ^ 6 by ring]
      rw [hexp, hip_val, hl2sq_w]
      linarith
    have hsq_eq : l2sq (T (T w0) - ((lam ^ 2 : ℝ) : ℂ) • w0) = 0 :=
      le_antisymm hsq0 (hl2sq_nonneg _)
    simp only [l2, hsq_eq, Real.sqrt_zero]
  -- Step 7: Finite-dimensionality of the A-invariant eigenspace E_V.
  let L_op : C(A, ℂ) →L[ℂ] C(A, ℂ) :=
    T.comp T - ((lam ^ 2 : ℝ) : ℂ) • ContinuousLinearMap.id ℂ C(A, ℂ)
  let E_V : Submodule ℂ C(A, ℂ) := V ⊓ LinearMap.ker L_op.toLinearMap
  have hEV_mem : ∀ {u : C(A, ℂ)}, u ∈ E_V ↔ u ∈ V ∧ T (T u) = ((lam ^ 2 : ℝ) : ℂ) • u := by
    intro u
    simp only [E_V, Submodule.mem_inf, LinearMap.mem_ker, ContinuousLinearMap.coe_coe, L_op,
      sub_apply, ContinuousLinearMap.comp_apply,
      smul_apply, ContinuousLinearMap.id_apply, sub_eq_zero]
  have hEV_closed : IsClosed (E_V : Set C(A, ℂ)) := hV_closed.inter L_op.isClosed_ker
  have : FiniteDimensional ℂ E_V := by
    refine FiniteDimensional.of_isCompact_closedBall₀ ℂ zero_lt_one ?_
    have hEmb : Topology.IsClosedEmbedding (Subtype.val : E_V → C(A, ℂ)) :=
      { toIsEmbedding := Isometry.isEmbedding fun _ _ ↦ rfl
        isClosed_range := by
          simpa only [Subtype.range_coe_subtype, SetLike.setOfPred_mem_eq] using hEV_closed }
    let c₀ : ℂ := ((lam⁻¹ : ℝ) : ℂ)
    have hK_scaled : IsCompact ((fun z : C(A, ℂ) ↦ c₀ • z) '' K_V) :=
      hKV_compact.image (continuous_const_smul c₀)
    have hTarget_comp : IsCompact ((E_V : Set C(A, ℂ)) ∩ Metric.closedBall 0 1) := by
      refine IsCompact.of_isClosed_subset hK_scaled
        (hEV_closed.inter Metric.isClosed_closedBall) ?_
      rintro u ⟨huEV, hu_ball⟩
      obtain ⟨huV, huTT⟩ := hEV_mem.mp huEV
      have hu_norm : ‖u‖ ≤ 1 := by
        simpa only [Metric.mem_closedBall, dist_zero_right] using hu_ball
      let u₁ : C(A, ℂ) := c₀ • T u
      have hu₁_BV : u₁ ∈ B_V := by
        refine ⟨V.smul_mem c₀ (hT_V huV), ?_⟩
        rw [hl2_smul lam⁻¹ (T u) (inv_nonneg.mpr hlam_pos.le)]
        have h1 : l2 (T u) ≤ lam * l2 u := hlam_bound huV
        have h2 : l2 u ≤ 1 := (hl2_le_norm u).trans hu_norm
        rw [inv_mul_le_iff₀ hlam_pos, mul_one]
        nlinarith
      refine ⟨T u₁, subset_closure ⟨u₁, hu₁_BV, rfl⟩, ?_⟩
      change c₀ • T (c₀ • T u) = u
      rw [map_smul, smul_smul, huTT, smul_smul]
      have hc : c₀ * c₀ * ((lam ^ 2 : ℝ) : ℂ) = 1 := by
        have hne : (lam : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr hlam_pos.ne'
        simp only [c₀, Complex.ofReal_inv, Complex.ofReal_pow]
        field_simp [hne]
      rw [hc, one_smul]
    have hpre : (Subtype.val : E_V → C(A, ℂ)) ⁻¹'
        ((E_V : Set C(A, ℂ)) ∩ Metric.closedBall 0 1) = Metric.closedBall (0 : E_V) 1 := by
      ext v
      refine ⟨fun h ↦ ?_, fun h ↦ ⟨v.2, ?_⟩⟩
      · simpa only [Metric.mem_closedBall, dist_zero_right, Submodule.norm_coe] using h.2
      · simpa only [Metric.mem_closedBall, dist_zero_right, Submodule.norm_coe] using h
    rw [← hpre]
    exact hEmb.isCompact_preimage hTarget_comp
  -- Step 8: Minimal A-invariant positive-dimensional subspace W <= E_V -> character.
  have hEV_tr : ∀ (b : A) {u : C(A, ℂ)}, u ∈ E_V → trCLM b u ∈ E_V := by
    intro b u hu
    obtain ⟨huV, huTT⟩ := hEV_mem.mp hu
    refine hEV_mem.mpr ⟨hV_tr b huV, ?_⟩
    rw [hT_comm, hT_comm, huTT, map_smul]
  let tr_E : A → Module.End ℂ E_V := fun b ↦
    (trCLM b).toLinearMap.restrict (fun u hu ↦ hEV_tr b hu)
  have htr_E_comm : ∀ (b c : A) (v : E_V), tr_E b (tr_E c v) = tr_E c (tr_E b v) := by
    intro b c v
    ext x
    exact congr_fun (congr_arg DFunLike.coe (trCLM_comm b c v.1)) x
  let w0_E : E_V := ⟨w0, hEV_mem.mpr ⟨hw0_V, hw0_eig⟩⟩
  have hw0_E_ne : w0_E ≠ 0 := fun h ↦ hw0_ne (congr_arg Subtype.val h)
  have : Nontrivial E_V := ⟨⟨w0_E, 0, hw0_E_ne⟩⟩
  let P_dim : ℕ → Prop := fun n ↦
    ∃ W : Submodule ℂ E_V, (∀ b : A, ∀ v ∈ W, tr_E b v ∈ W) ∧
      0 < Module.finrank ℂ W ∧ Module.finrank ℂ W = n
  have hP_ex : ∃ n : ℕ, P_dim n := by
    refine ⟨Module.finrank ℂ (⊤ : Submodule ℂ E_V), ⊤, fun _ _ _ ↦ Submodule.mem_top, ?_, rfl⟩
    have : Nontrivial (⊤ : Submodule ℂ E_V) :=
      ⟨⟨⟨w0_E, Submodule.mem_top⟩, 0, fun h ↦ hw0_E_ne (congr_arg Subtype.val h)⟩⟩
    exact Module.finrank_pos (R := ℂ) (M := (⊤ : Submodule ℂ E_V))
  classical
  let n₀ : ℕ := Nat.find hP_ex
  obtain ⟨W, hW_inv, hW_pos, hW_dim⟩ : P_dim n₀ := Nat.find_spec hP_ex
  have hW_scalar : ∀ b : A, ∃ c : ℂ, ∀ v ∈ W, tr_E b v = c • v := by
    intro b
    have : Nontrivial W := Module.finrank_pos_iff.mp hW_pos
    let f_b : Module.End ℂ W := (tr_E b).restrict (hW_inv b)
    obtain ⟨c, hc⟩ := Module.End.exists_eigenvalue (K := ℂ) (V := W) f_b
    refine ⟨c, ?_⟩
    let W'_sub : Submodule ℂ W := f_b.eigenspace c
    let W' : Submodule ℂ E_V := W'_sub.map W.subtype
    have hW'_le : W' ≤ W := Submodule.map_subtype_le W W'_sub
    have hW'_inv : ∀ d : A, ∀ v ∈ W', tr_E d v ∈ W' := by
      rintro d _ ⟨y, hy, rfl⟩
      change y ∈ f_b.eigenspace c at hy
      rw [Module.End.mem_eigenspace_iff] at hy
      refine ⟨⟨tr_E d y.1, hW_inv d y.1 y.2⟩, ?_, rfl⟩
      change (⟨tr_E d y.1, hW_inv d y.1 y.2⟩ : W) ∈ f_b.eigenspace c
      rw [Module.End.mem_eigenspace_iff]
      ext1
      change tr_E b (tr_E d y.1) = c • tr_E d y.1
      have hy_val : tr_E b y.1 = c • y.1 := congr_arg Subtype.val hy
      rw [htr_E_comm, hy_val, map_smul]
    have hW'_pos : 0 < Module.finrank ℂ W' := by
      obtain ⟨y, hy_mem, hy_ne⟩ := Submodule.exists_mem_ne_zero_of_ne_bot
        (Module.End.hasEigenvalue_iff.mp hc)
      have : Nontrivial W' :=
        ⟨⟨⟨W.subtype y, ⟨y, hy_mem, rfl⟩⟩, 0,
          fun h ↦ hy_ne (W.subtype_injective (congr_arg Subtype.val h))⟩⟩
      exact Module.finrank_pos (R := ℂ) (M := W')
    have hW'_eq : W' = W := by
      by_contra hne
      have hlt : W' < W := lt_of_le_of_ne hW'_le hne
      have hdim_lt : Module.finrank ℂ W' < n₀ :=
        hW_dim ▸ Submodule.finrank_lt_finrank_of_lt hlt
      exact Nat.find_min hP_ex hdim_lt ⟨W', hW'_inv, hW'_pos, rfl⟩
    intro v hv
    have hv' : v ∈ W' := hW'_eq.symm ▸ hv
    rcases hv' with ⟨y, hy, rfl⟩
    change y ∈ f_b.eigenspace c at hy
    rw [Module.End.mem_eigenspace_iff] at hy
    exact congr_arg Subtype.val hy
  have : Nontrivial W := Module.finrank_pos_iff.mp hW_pos
  obtain ⟨z₀, hz₀_ne⟩ := exists_ne (0 : W)
  have hz₀_fun_ne : (z₀.1.1 : C(A, ℂ)) ≠ 0 := by
    intro h0
    apply hz₀_ne
    ext1
    ext1
    exact h0
  obtain ⟨x₀, hx₀⟩ : ∃ x₀ : A, z₀.1.1 x₀ ≠ 0 := by
    by_contra! hall
    apply hz₀_fun_ne
    ext x
    exact hall x
  let z₁ : E_V := tr_E x₀ z₀.1
  have hz₁_W : z₁ ∈ W := hW_inv x₀ z₀.1 z₀.2
  have hz₁_one : z₁.1 1 ≠ 0 := by
    change z₀.1.1 (x₀ * 1) ≠ 0
    rwa [mul_one]
  let w_E : E_V := (z₁.1 1)⁻¹ • z₁
  have hw_E_W : w_E ∈ W := W.smul_mem _ hz₁_W
  let w : C(A, ℂ) := w_E.1
  have hw_V : w ∈ V := (hEV_mem.mp w_E.2).1
  have hw_one : w 1 = 1 := by
    change (z₁.1 1)⁻¹ * z₁.1 1 = 1
    exact inv_mul_cancel₀ hz₁_one
  have hw_mul : ∀ b x : A, w (b * x) = w b * w x := by
    intro b x
    obtain ⟨c, hc⟩ := hW_scalar b
    have hbw : tr_E b w_E = c • w_E := hc w_E hw_E_W
    have hpt : ∀ y : A, w (b * y) = c * w y :=
      fun y ↦ congr_fun (congr_arg DFunLike.coe (congr_arg Subtype.val hbw)) y
    have hc_eq : c = w b := by
      have h1 := hpt 1
      rw [mul_one, hw_one, mul_one] at h1
      exact h1.symm
    rw [← hc_eq, hpt x]
  have hw_pow : ∀ (b : A) (j : ℕ), w (b ^ j) = w b ^ j := by
    intro b j
    induction j with
    | zero => simp [hw_one]
    | succ m ih => rw [pow_succ', pow_succ', hw_mul, ih]
  have hw_pow_p : ∀ b : A, w b ^ p = 1 := by
    intro b
    rw [← hw_pow b p, hAp b, hw_one]
  -- Clopen decomposition of ConnectedSpace A -> final contradiction!
  let F₁ : Set A := {b | w b = 1}
  let F₂ : Set A := {b | ∑ j ∈ Finset.range p, w b ^ j = 0}
  have hF₁_closed : IsClosed F₁ := isClosed_eq w.continuous continuous_const
  have hF₂_closed : IsClosed F₂ :=
    isClosed_eq (continuous_finsetSum _ fun j _ ↦ w.continuous.pow j) continuous_const
  have huniv : ∀ b : A, b ∈ F₁ ∨ b ∈ F₂ := by
    intro b
    have hprod : (∑ j ∈ Finset.range p, w b ^ j) * (w b - 1) = 0 := by
      rw [geom_sum_mul_sub_one, hw_pow_p b, sub_self]
    rcases mul_eq_zero.mp hprod with hsum | hsub
    · exact Or.inr hsum
    · exact Or.inl (sub_eq_zero.mp hsub)
  have hdisj : ∀ b : A, ¬ (b ∈ F₁ ∧ b ∈ F₂) := by
    rintro b ⟨hb1, hb2⟩
    change w b = 1 at hb1
    change ∑ j ∈ Finset.range p, w b ^ j = 0 at hb2
    rw [hb1] at hb2
    simp only [one_pow, Finset.sum_const, Finset.card_range, nsmul_eq_mul, mul_one] at hb2
    exact (Nat.cast_ne_zero.mpr hp.ne_zero) hb2
  have hF₁_compl : F₁ᶜ = F₂ := by
    ext b
    exact ⟨fun hb ↦ (huniv b).resolve_left hb, fun hb hb1 ↦ hdisj b ⟨hb1, hb⟩⟩
  have hF₁_clopen : IsClopen F₁ :=
    ⟨hF₁_closed, isClosed_compl_iff.mp (by rwa [hF₁_compl])⟩
  have ha₀_F₂ : a₀ ∈ F₂ := by
    change ∑ j ∈ Finset.range p, w a₀ ^ j = 0
    have hv := hV_mem.mp hw_V 1
    simpa only [mul_one, hw_pow a₀] using hv
  rcases isClopen_iff.mp hF₁_clopen with hF₁_empty | hF₁_univ
  · have h1_mem : (1 : A) ∈ F₁ := hw_one
    rw [hF₁_empty] at h1_mem
    exact h1_mem
  · have ha₀_F₁ : a₀ ∈ F₁ := hF₁_univ ▸ Set.mem_univ a₀
    exact hdisj a₀ ⟨ha₀_F₁, ha₀_F₂⟩

private theorem add_subsingleton_of_nsmul_prime_eq_zero_aux
    (A : Type*) [AddCommGroup A] [TopologicalSpace A] [IsTopologicalAddGroup A]
    [ConnectedSpace A] [CompactSpace A] [T2Space A]
    (p : ℕ) (hp : p.Prime) (hAp : ∀ a : A, p • a = 0) :
    Subsingleton A := by
  have : ConnectedSpace (Multiplicative A) := ‹ConnectedSpace A›
  have : T2Space (Multiplicative A) := ‹T2Space A›
  have : Subsingleton (Multiplicative A) :=
    mul_subsingleton_of_pow_prime_eq_one_aux (Multiplicative A) p hp fun a ↦ by
      rw [← ofAdd_toAdd a, ← ofAdd_nsmul, hAp (Multiplicative.toAdd a), ofAdd_zero]
  exact Function.Injective.subsingleton Multiplicative.ofAdd.injective

attribute [to_additive existing] mul_subsingleton_of_pow_prime_eq_one_aux

end SubsingletonAux

@[expose] public section

section CompactHausdorff

/-- A connected compact Hausdorff vector space over `𝔽_p` is trivial. This might sound easy, but it
seems to require the fact that every nontrivial compact hausdorff group has a nontrivial continuous
character. This fact is a special case of Pontryagin duality, and also a consequence of the
Peter-Weyl theorem. This fact is being worked on at `YaelDillies/mean-fourier`.

Here's a proof of the theorem, using this fact that nontrivial groups have nontrivial characters:
If `χ : A → circle` is a continuous character, then the image of `χ` is connected but is a
subgroup of the `p`th roots of unity, hence must be trivial. Thus, `A` has no nontrivial continuous
characters, so `A` must be trivial. -/
@[to_additive]
theorem Group.subsingleton_of_pow_prime_eq_one
    (A : Type*) [CommGroup A] [TopologicalSpace A] [IsTopologicalGroup A]
    [ConnectedSpace A] [CompactSpace A] [T2Space A]
    (p : ℕ) (hp : p.Prime) (hAp : ∀ a : A, a ^ p = 1) :
    Subsingleton A := by
  exact mul_subsingleton_of_pow_prime_eq_one_aux A p hp hAp

/-- A compact Hausdorff vector space over `𝔽_p` is totally disconnected. -/
@[to_additive]
theorem Group.totallyDisconnected_of_pow_prime_eq_one
    (A : Type*) [CommGroup A] [TopologicalSpace A] [IsTopologicalGroup A]
    [T2Space A] [CompactSpace A] (p : ℕ) (hp : p.Prime) (hA : ∀ a : A, a ^ p = 1) :
    TotallyDisconnectedSpace A := by
  have : ConnectedSpace (Subgroup.connectedComponentOfOne A) :=
    Subtype.connectedSpace isConnected_connectedComponent
  have : CompactSpace (Subgroup.connectedComponentOfOne A) :=
    isCompact_iff_compactSpace.mp (isClosed_connectedComponent.isCompact)
  have := subsingleton_of_pow_prime_eq_one (Subgroup.connectedComponentOfOne A) p hp
    fun a ↦ Subtype.ext (hA a)
  rw [totallyDisconnectedSpace_iff_connectedComponent_one]
  exact ((Set.subsingleton_coe _).mp this).eq_singleton_of_mem mem_connectedComponent

/-- A connected compact Hausdorff abelian topological group is divisible. -/
@[to_additive /-- A connected compact Hausdorff abelian topological group is divisible. -/,
  implicit_reducible]
noncomputable def Group.rootable
    (A : Type*) [CommGroup A] [TopologicalSpace A] [IsTopologicalGroup A]
    [ConnectedSpace A] [CompactSpace A] [T2Space A] : RootableBy A ℕ := by
  apply rootableByOfPowLeftSurj
  suffices ∀ p : ℕ, p.Prime → Function.Surjective fun a : A ↦ a ^ p by
    apply Nat.prime_composite_induction
    · simp
    · simpa using! Function.surjective_id
    · grind
    · intro a _ ha b _ hb _
      simp only [pow_mul]
      exact (hb (by grind)).comp (ha (by grind))
  intro p hp
  let f : A →* A := powMonoidHom p
  change Function.Surjective f
  have hf : ∀ a : A ⧸ f.range, a ^ p = 1 := by
    intro a
    obtain ⟨a, rfl⟩ := QuotientGroup.mk_surjective a
    rw [← QuotientGroup.mk_pow, QuotientGroup.eq_one_iff]
    exact ⟨a, rfl⟩
  have : IsClosed (f.range : Set A) := (isCompact_range (continuous_pow p)).isClosed
  have := totallyDisconnected_of_pow_prime_eq_one (A ⧸ f.range) p hp hf
  have : ConnectedSpace (A ⧸ f.range) :=
    QuotientGroup.mk_surjective.connectedSpace QuotientGroup.continuous_mk
  rw [← MonoidHom.range_eq_top, ← QuotientGroup.subsingleton_iff]
  exact subsingleton_of_preconnected_totallyDisconnected

/-- A connected compact Hausdorff abelian topological group does not admit a nontrivial compact
group of automorphisms. -/
@[to_additive]
theorem CommGroup.no_compact_automorphisms
    {A : Type*} [CommGroup A] [TopologicalSpace A] [IsTopologicalGroup A]
    [ConnectedSpace A] [CompactSpace A] [T2Space A] (K : Subgroup (ContinuousMonoidHom A A))
    (hK : IsCompact (K : Set (ContinuousMonoidHom A A))) :
    K = ⊥ := by
  have A_rootable : RootableBy A ℕ := Group.rootable A
  rw [eq_bot_iff]
  intro f hf
  ext a
  rw [ContinuousMonoidHom.one_toFun]
  by_contra! ha
  let U : Set A := {f a}ᶜ
  have hU : IsOpen U := isOpen_compl_singleton
  have hU1 : 1 ∈ U := ha.symm
  let W : Set (A →ₜ* A) := {f | Set.MapsTo f Set.univ U}
  have hW : IsOpen W :=
    (ContinuousMonoidHom.isInducing_toContinuousMap A A).continuous.isOpen_preimage _
      (ContinuousMap.isOpen_setOfPred_mapsTo isCompact_univ hU)
  have hW1 : 1 ∈ W := by simpa [W]
  replace hW1 : W ∈ nhds 1 := hW.mem_nhds hW1
  have : CompactSpace K := isCompact_iff_compactSpace.mp hK
  obtain ⟨n, hn0, hnf⟩ :=
    (mapClusterPt_iff_frequently.mp (mapClusterPt_one_atTop_pow ⟨f, hf⟩) (Subtype.val ⁻¹' W)
    (continuousAt_subtype_val.preimage_mem_nhds (by exact hW1))).forall_exists_of_atTop 1
  replace hn0 : n ≠ 0 := by grind
  rw [Set.mem_preimage, Subgroup.coe_pow, Subtype.coe_mk,
    Set.mem_ofPred_eq, Set.mapsTo_univ_iff, ← Set.range_subset_iff] at hnf
  change (f ^ n).range ≤ U at hnf
  suffices f.range ≤ (f ^ n).range by
    exact (Set.Subset.trans this hnf) ⟨a, rfl⟩ rfl
  rintro - ⟨b, rfl⟩
  use RootableBy.root b n
  simp [ContinuousMonoidHom.pow_apply, ← map_pow, RootableBy.root_cancel b hn0]

/-- A compact Hausdorff ring is totally disconnected. -/
instance {R : Type*} [Ring R] [TopologicalSpace R] [IsTopologicalRing R]
    [CompactSpace R] [T2Space R] : TotallyDisconnectedSpace R := by
  let C₀ : Ideal R := Ideal.connectedComponentOfZero R
  suffices C₀ = ⊥ from
    totallyDisconnectedSpace_iff_connectedComponent_zero.mpr (SetLike.ext'_iff.mp this)
  have C₀_isClosed : IsClosed (C₀ : Set R) := isClosed_connectedComponent
  have C₀_isCompact : IsCompact (C₀ : Set R) := C₀_isClosed.isCompact
  have : CompactSpace C₀ := isCompact_iff_compactSpace.mp C₀_isCompact
  have C₀_isConnected : IsConnected (C₀ : Set R) := isConnected_connectedComponent
  have : ConnectedSpace C₀ := isConnected_iff_connectedSpace.mp C₀_isConnected
  let f : ContinuousAddMonoidHom R (ContinuousAddMonoidHom C₀ C₀) :=
  { toFun r :=
    { toFun := fun c ↦ r • c
      map_zero' := by simp
      map_add' := by simp [smul_add]
      continuous_toFun := by fun_prop }
    map_zero' := by apply DFunLike.ext; intros; apply zero_smul
    map_add' := by intros; apply DFunLike.ext; intros; apply add_smul
    continuous_toFun := ContinuousAddMonoidHom.continuous_of_continuous_uncurry _ continuous_smul }
  have key := AddCommGroup.no_compact_automorphisms f.range (isCompact_range f.continuous)
  refine eq_bot_iff.mpr fun c hc ↦ ?_
  replace key : f.toAddMonoidHom 1 ⟨c, hc⟩ = (0 : ContinuousAddMonoidHom C₀ C₀) ⟨c, hc⟩ := by
    rw [AddMonoidHom.range_eq_bot_iff.mp key, AddMonoidHom.zero_apply]
  exact (one_smul R c).symm.trans (Subtype.ext_iff.mp key)

end CompactHausdorff
