/-
Copyright (c) 2026 Joris van Winden. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Joris van Winden
-/

module

public import BrownianMotion.Gaussian.BrownianMotion

import Mathlib.Analysis.Calculus.LHopital
import Mathlib.Analysis.PSeries
import Mathlib.Probability.BorelCantelli

/-!
This file proves the **law of the iterated logarithm** for Brownian motion, which provides sharp
asymptotics for the limsup of B_t as t tends to infinity.

The main theorem is `IsBrownianReal.ae_limsup_div_sqrt_log_log_eq_one`, which proves that if $B_t$
is a Brownian motion, it holds almost surely that
$\limsup_{t → ∞} \frac{B_t}{\sqrt{2 \log \log t}} = 1$.
-/

@[expose] public section

open Filter MeasureTheory ProbabilityTheory Real
open scoped ENNReal NNReal

namespace ProbabilityTheory

section ReflectionAux

open scoped Topology

private noncomputable def brownianGrid (t : ℝ≥0) (N k : ℕ) : ℝ≥0 :=
  (k : ℝ≥0) * (t / (N : ℝ≥0))

private lemma brownianGrid_zero (t : ℝ≥0) (N : ℕ) : brownianGrid t N 0 = 0 := by
  simp [brownianGrid]

private lemma brownianGrid_self (t : ℝ≥0) {N : ℕ} (hN : N ≠ 0) :
    brownianGrid t N N = t := by
  unfold brownianGrid
  have hN' : (N : ℝ≥0) ≠ 0 := Nat.cast_ne_zero.mpr hN
  exact mul_div_cancel₀ t hN'

private lemma brownianGrid_mono (t : ℝ≥0) (N : ℕ) {j k : ℕ} (hjk : j ≤ k) :
    brownianGrid t N j ≤ brownianGrid t N k := by
  unfold brownianGrid
  gcongr

private lemma brownianGrid_le (t : ℝ≥0) {N k : ℕ} (hN : N ≠ 0) (hk : k ≤ N) :
    brownianGrid t N k ≤ t :=
  (brownianGrid_mono t N hk).trans_eq (brownianGrid_self t hN)

private lemma brownianGrid_pow_two_succ (t : ℝ≥0) (n k : ℕ) :
    brownianGrid t (2 ^ (n + 1)) (2 * k) = brownianGrid t (2 ^ n) k := by
  unfold brownianGrid
  rw [pow_succ', Nat.cast_mul, Nat.cast_mul, Nat.cast_ofNat]
  ext
  push_cast
  field_simp

private lemma gaussianReal_zero_measureReal_Ioi_zero {v : ℝ≥0} (hv : v ≠ 0) :
    (gaussianReal 0 v).real (Set.Ioi 0) = 1 / 2 := by
  have : NullSingletonClass (gaussianReal 0 v) := nullSingletonClass_gaussianReal hv
  have hsym : (gaussianReal 0 v).real (Set.Iio 0) = (gaussianReal 0 v).real (Set.Ioi 0) := by
    have hmap : (gaussianReal 0 v).map (fun x : ℝ ↦ -x) = gaussianReal 0 v := by
      simpa using gaussianReal_map_neg (μ := 0) (v := v)
    have hmeas_eq : gaussianReal 0 v (Set.Iio 0) = gaussianReal 0 v (Set.Ioi 0) := calc
      gaussianReal 0 v (Set.Iio 0)
          = gaussianReal 0 v ((fun x : ℝ ↦ -x) ⁻¹' Set.Ioi 0) := by
              congr 1; ext x; simp
      _ = (gaussianReal 0 v).map (fun x : ℝ ↦ -x) (Set.Ioi 0) :=
            (Measure.map_apply measurable_neg measurableSet_Ioi).symm
      _ = gaussianReal 0 v (Set.Ioi 0) := by rw [hmap]
    exact congrArg ENNReal.toReal hmeas_eq
  have huniv : Set.Iio (0 : ℝ) ∪ ({0} ∪ Set.Ioi 0) = Set.univ := by
    ext x
    simp only [Set.mem_union, Set.mem_Iio, Set.mem_singleton_iff, Set.mem_Ioi, Set.mem_univ,
      iff_true]
    rcases lt_trichotomy x 0 with h | h | h
    · exact Or.inl h
    · exact Or.inr (Or.inl h)
    · exact Or.inr (Or.inr h)
  have hdisj1 : Disjoint (Set.Iio (0 : ℝ)) ({0} ∪ Set.Ioi 0) := by
    rw [Set.disjoint_left]
    rintro x (hx : x < 0) (rfl | hx')
    · exact lt_irrefl 0 hx
    · exact lt_asymm hx hx'
  have hdisj2 : Disjoint ({(0 : ℝ)} : Set ℝ) (Set.Ioi 0) := by
    rw [Set.disjoint_singleton_left]
    simp
  have h0 : (gaussianReal 0 v).real {(0 : ℝ)} = 0 := by
    simp [Measure.real, measure_singleton (μ := gaussianReal 0 v) (0 : ℝ)]
  have h1 : (1 : ℝ) = (gaussianReal 0 v).real (Set.Iio 0) +
      ((gaussianReal 0 v).real {(0 : ℝ)} + (gaussianReal 0 v).real (Set.Ioi 0)) := by
    calc
      (1 : ℝ) = (gaussianReal 0 v).real Set.univ := by simp
      _ = (gaussianReal 0 v).real (Set.Iio 0 ∪ ({0} ∪ Set.Ioi 0)) := by rw [huniv]
      _ = (gaussianReal 0 v).real (Set.Iio 0) + (gaussianReal 0 v).real ({0} ∪ Set.Ioi 0) :=
            measureReal_union hdisj1 ((MeasurableSet.singleton 0).union measurableSet_Ioi)
      _ = (gaussianReal 0 v).real (Set.Iio 0) +
            ((gaussianReal 0 v).real {(0 : ℝ)} + (gaussianReal 0 v).real (Set.Ioi 0)) := by
            rw [measureReal_union hdisj2 measurableSet_Ioi]
  linarith

private lemma hasLaw_gaussianReal_prob_nonneg_ge_half {Ω : Type*} {mΩ : MeasurableSpace Ω}
    {P : Measure Ω} {Z : Ω → ℝ} {v : ℝ≥0} (hZ : HasLaw Z (gaussianReal 0 v) P) :
    (1 / 2 : ℝ) ≤ P.real {ω | 0 ≤ Z ω} := by
  have hmap : P.real (Z ⁻¹' Set.Ici 0) = (gaussianReal 0 v).real (Set.Ici 0) := by
    simp [Measure.real, ← Measure.map_apply_of_aemeasurable hZ.aemeasurable measurableSet_Ici,
      hZ.map_eq]
  change (1 / 2 : ℝ) ≤ P.real (Z ⁻¹' Set.Ici 0)
  rw [hmap]
  by_cases hv : v = 0
  · subst hv
    have hdir : (gaussianReal 0 0).real (Set.Ici (0 : ℝ)) = 1 := by simp [Measure.real]
    linarith
  · have hmono : (gaussianReal 0 v).real (Set.Ioi 0) ≤ (gaussianReal 0 v).real (Set.Ici 0) :=
      measureReal_mono Set.Ioi_subset_Ici_self
    linarith [gaussianReal_zero_measureReal_Ioi_zero hv]

private lemma hasLaw_gaussianReal_prob_pos_le_half {Ω : Type*} {mΩ : MeasurableSpace Ω}
    {P : Measure Ω} {Z : Ω → ℝ} {v : ℝ≥0} (hZ : HasLaw Z (gaussianReal 0 v) P) :
    P.real {ω | 0 < Z ω} ≤ 1 / 2 := by
  have hmap : P.real (Z ⁻¹' Set.Ioi 0) = (gaussianReal 0 v).real (Set.Ioi 0) := by
    simp [Measure.real, ← Measure.map_apply_of_aemeasurable hZ.aemeasurable measurableSet_Ioi,
      hZ.map_eq]
  change P.real (Z ⁻¹' Set.Ioi 0) ≤ 1 / 2
  rw [hmap]
  by_cases hv : v = 0
  · subst hv
    have hdir : (gaussianReal 0 0).real (Set.Ioi (0 : ℝ)) = 0 := by simp [Measure.real]
    linarith
  · linarith [gaussianReal_zero_measureReal_Ioi_zero hv]

private lemma hasLaw_gaussianReal_prob_ge_eq_gt {Ω : Type*} {mΩ : MeasurableSpace Ω}
    {P : Measure Ω} {Z : Ω → ℝ} {v : ℝ≥0} (hv : v ≠ 0) (hZ : HasLaw Z (gaussianReal 0 v) P)
    (c : ℝ) :
    P.real {ω | c ≤ Z ω} = P.real {ω | c < Z ω} := by
  have : NullSingletonClass (gaussianReal 0 v) := nullSingletonClass_gaussianReal hv
  have h1 : P (Z ⁻¹' Set.Ici c) = gaussianReal 0 v (Set.Ici c) := by
    rw [← Measure.map_apply_of_aemeasurable hZ.aemeasurable measurableSet_Ici, hZ.map_eq]
  have h2 : P (Z ⁻¹' Set.Ioi c) = gaussianReal 0 v (Set.Ioi c) := by
    rw [← Measure.map_apply_of_aemeasurable hZ.aemeasurable measurableSet_Ioi, hZ.map_eq]
  have hs : gaussianReal 0 v {c} = 0 := measure_singleton (μ := gaussianReal 0 v) c
  have hmeas : gaussianReal 0 v (Set.Ici c) = gaussianReal 0 v (Set.Ioi c) := by
    rw [← Set.Ioi_union_left]
    exact le_antisymm
      ((measure_union_le _ _).trans (by simp [hs]))
      (measure_mono Set.subset_union_left)
  change (P (Z ⁻¹' Set.Ici c)).toReal = (P (Z ⁻¹' Set.Ioi c)).toReal
  rw [h1, h2, hmeas]

private def firstPassageSet {Ω : Type*} (Y : ℝ≥0 → Ω → ℝ) (t : ℝ≥0) (a : ℝ) (N k : ℕ) : Set Ω :=
  {ω | a < Y (brownianGrid t N k) ω ∧ ∀ j < k, Y (brownianGrid t N j) ω ≤ a}

private lemma measurableSet_firstPassageSet {Ω : Type*} {mΩ : MeasurableSpace Ω}
    {Y : ℝ≥0 → Ω → ℝ} (hYm : ∀ s, Measurable (Y s)) (t : ℝ≥0) (a : ℝ) (N k : ℕ) :
    MeasurableSet (firstPassageSet Y t a N k) := by
  have heq : firstPassageSet Y t a N k =
      {ω | a < Y (brownianGrid t N k) ω} ∩
        ⋂ j : Fin k, {ω | Y (brownianGrid t N j.1) ω ≤ a} := by
    ext ω
    simp only [firstPassageSet, Set.mem_inter_iff, Set.mem_ofPred_eq, Set.mem_iInter]
    exact ⟨fun ⟨h1, h2⟩ ↦ ⟨h1, fun j ↦ h2 j.1 j.2⟩, fun ⟨h1, h2⟩ ↦ ⟨h1, fun j hj ↦ h2 ⟨j, hj⟩⟩⟩
  rw [heq]
  refine (measurableSet_lt measurable_const (hYm _)).inter ?_
  exact MeasurableSet.iInter fun j ↦ measurableSet_le (hYm _) measurable_const

private lemma pairwiseDisjoint_firstPassageSet {Ω : Type*} (Y : ℝ≥0 → Ω → ℝ) (t : ℝ≥0) (a : ℝ)
    (N : ℕ) :
    (Set.univ : Set ℕ).PairwiseDisjoint (firstPassageSet Y t a N) := by
  intro i _ j _ hij
  change Disjoint (firstPassageSet Y t a N i) (firstPassageSet Y t a N j)
  rw [Set.disjoint_left]
  intro ω hωi hωj
  rcases lt_or_gt_of_ne hij with hlt | hlt
  · exact lt_irrefl a (hωi.1.trans_le (hωj.2 i hlt))
  · exact lt_irrefl a (hωj.1.trans_le (hωi.2 j hlt))

private lemma biUnion_firstPassageSet_eq {Ω : Type*} (Y : ℝ≥0 → Ω → ℝ) (t : ℝ≥0) (a : ℝ)
    (N : ℕ) :
    (⋃ k ∈ Finset.range (N + 1), firstPassageSet Y t a N k) =
      {ω | ∃ k ≤ N, a < Y (brownianGrid t N k) ω} := by
  classical
  ext ω
  simp only [Set.mem_iUnion, Finset.mem_range, Nat.lt_succ_iff, Set.mem_ofPred_eq]
  constructor
  · rintro ⟨k, hk, hω⟩
    exact ⟨k, hk, hω.1⟩
  · intro h
    refine ⟨Nat.find h, (Nat.find_spec h).1, (Nat.find_spec h).2, fun j hj ↦ ?_⟩
    have hjN : j ≤ N := hj.le.trans (Nat.find_spec h).1
    exact not_lt.mp fun hgt ↦ Nat.find_min h hj ⟨hjN, hgt⟩

private lemma measureReal_firstPassageSet_inter_sub {Ω : Type*} {mΩ : MeasurableSpace Ω}
    {P : Measure Ω} {Y : ℝ≥0 → Ω → ℝ} (hY : IsPreBrownianReal Y P) (t : ℝ≥0) (a : ℝ)
    {N k : ℕ} (hN : N ≠ 0) (hk : k ≤ N) {U : Set ℝ} (hU : MeasurableSet U) :
    P.real (firstPassageSet Y t a N k ∩ {ω | Y t ω - Y (brownianGrid t N k) ω ∈ U}) =
      P.real (firstPassageSet Y t a N k) *
        P.real {ω | Y t ω - Y (brownianGrid t N k) ω ∈ U} := by
  set s := brownianGrid t N k
  have hst : s ≤ t := brownianGrid_le t hN hk
  let Z : Ω → ℝ := fun ω ↦ Y t ω - Y s ω
  let restrictPath : Ω → (Set.Iic s → ℝ) := fun ω u ↦ Y u.1 ω
  have hind : IndepFun Z restrictPath P := by
    have hcomp := (hY.indepFun_shift s).comp (measurable_pi_apply (t - s)) measurable_id
    convert hcomp using 1
    · ext ω
      simp [Z, add_tsub_cancel_of_le hst]
    · rfl
  let B : Set (Set.Iic s → ℝ) :=
    {f | a < f ⟨s, Set.mem_Iic.mpr le_rfl⟩} ∩
      ⋂ j : Fin k,
        {f | f ⟨brownianGrid t N j.1, Set.mem_Iic.mpr (brownianGrid_mono t N j.2.le)⟩ ≤ a}
  have hB : MeasurableSet B := by
    refine (measurableSet_lt measurable_const (measurable_pi_apply _)).inter ?_
    exact MeasurableSet.iInter fun j ↦ measurableSet_le (measurable_pi_apply _) measurable_const
  have hpre : restrictPath ⁻¹' B = firstPassageSet Y t a N k := by
    ext ω
    simp only [B, restrictPath, firstPassageSet, s, Set.mem_preimage, Set.mem_inter_iff,
      Set.mem_ofPred_eq, Set.mem_iInter]
    exact ⟨fun ⟨h1, h2⟩ ↦ ⟨h1, fun j hj ↦ h2 ⟨j, hj⟩⟩, fun ⟨h1, h2⟩ ↦ ⟨h1, fun j ↦ h2 j.1 j.2⟩⟩
  have hmul : P (Z ⁻¹' U ∩ restrictPath ⁻¹' B) = P (Z ⁻¹' U) * P (restrictPath ⁻¹' B) :=
    (indepFun_iff_measure_inter_preimage_eq_mul.1 hind) U B hU hB
  rw [hpre, Set.inter_comm] at hmul
  calc
    P.real (firstPassageSet Y t a N k ∩ {ω | Y t ω - Y s ω ∈ U})
        = (P (firstPassageSet Y t a N k ∩ (Z ⁻¹' U))).toReal := rfl
    _ = (P (Z ⁻¹' U) * P (firstPassageSet Y t a N k)).toReal := by rw [hmul]
    _ = P.real (firstPassageSet Y t a N k) * P.real {ω | Y t ω - Y s ω ∈ U} := by
          rw [ENNReal.toReal_mul, mul_comm]; rfl

private lemma measureReal_dyadic_exceed_le {Ω : Type*} {mΩ : MeasurableSpace Ω}
    {P : Measure Ω} {Y : ℝ≥0 → Ω → ℝ} (hY : IsPreBrownianReal Y P)
    (hYm : ∀ r, Measurable (Y r)) (t : ℝ≥0) (a : ℝ) {N : ℕ} (hN : N ≠ 0) :
    P.real {ω | ∃ k ≤ N, a < Y (brownianGrid t N k) ω} ≤ 2 * P.real {ω | a < Y t ω} := by
  have : IsProbabilityMeasure P := (hY.hasLaw ∅).isProbabilityMeasure
  let F : ℕ → Set Ω := fun k ↦
    firstPassageSet Y t a N k ∩ {ω | 0 ≤ Y t ω - Y (brownianGrid t N k) ω}
  have hF_meas : ∀ k ∈ Finset.range (N + 1), MeasurableSet (F k) := fun k _ ↦
    (measurableSet_firstPassageSet hYm t a N k).inter
      (measurableSet_le measurable_const ((hYm t).sub (hYm _)))
  have hF_disj : (↑(Finset.range (N + 1)) : Set ℕ).PairwiseDisjoint F := by
    intro i _ j _ hij
    exact ((pairwiseDisjoint_firstPassageSet Y t a N) (Set.mem_univ i) (Set.mem_univ j) hij).mono
      Set.inter_subset_left Set.inter_subset_left
  have hF_sub : (⋃ k ∈ Finset.range (N + 1), F k) ⊆ {ω | a < Y t ω} := by
    intro ω hω
    simp only [Set.mem_iUnion, F, Set.mem_inter_iff, firstPassageSet, Set.mem_ofPred_eq] at hω
    rcases hω with ⟨k, _, ⟨hgt, _⟩, hinc⟩
    change a < Y t ω
    linarith
  have hsum_le : ∑ k ∈ Finset.range (N + 1), P.real (F k) ≤ P.real {ω | a < Y t ω} := by
    rw [← measureReal_biUnion_finset hF_disj hF_meas]
    exact measureReal_mono hF_sub
  have hterm : ∀ k ∈ Finset.range (N + 1),
      (1 / 2 : ℝ) * P.real (firstPassageSet Y t a N k) ≤ P.real (F k) := by
    intro k hk
    have hkN : k ≤ N := Nat.lt_succ_iff.mp (Finset.mem_range.mp hk)
    have hfac := measureReal_firstPassageSet_inter_sub hY t a hN hkN (measurableSet_Ici (a := 0))
    change _ ≤ P.real (firstPassageSet Y t a N k ∩
      {ω | Y t ω - Y (brownianGrid t N k) ω ∈ Set.Ici 0})
    rw [hfac]
    have hhalf : (1 / 2 : ℝ) ≤ P.real {ω | Y t ω - Y (brownianGrid t N k) ω ∈ Set.Ici 0} :=
      hasLaw_gaussianReal_prob_nonneg_ge_half (hY.hasLaw_sub t (brownianGrid t N k))
    have hnonneg : 0 ≤ P.real (firstPassageSet Y t a N k) := measureReal_nonneg
    nlinarith
  have h1 : (1 / 2 : ℝ) * ∑ k ∈ Finset.range (N + 1), P.real (firstPassageSet Y t a N k) ≤
      P.real {ω | a < Y t ω} := by
    calc
      (1 / 2 : ℝ) * ∑ k ∈ Finset.range (N + 1), P.real (firstPassageSet Y t a N k)
          = ∑ k ∈ Finset.range (N + 1), (1 / 2 : ℝ) * P.real (firstPassageSet Y t a N k) := by
              rw [Finset.mul_sum]
      _ ≤ ∑ k ∈ Finset.range (N + 1), P.real (F k) := Finset.sum_le_sum hterm
      _ ≤ P.real {ω | a < Y t ω} := hsum_le
  have hpart : P.real {ω | ∃ k ≤ N, a < Y (brownianGrid t N k) ω} =
      ∑ k ∈ Finset.range (N + 1), P.real (firstPassageSet Y t a N k) := by
    rw [← biUnion_firstPassageSet_eq Y t a N]
    exact measureReal_biUnion_finset
      ((pairwiseDisjoint_firstPassageSet Y t a N).subset (Set.subset_univ _))
      (fun k _ ↦ measurableSet_firstPassageSet hYm t a N k)
  linarith

private lemma dyadic_exceed_iUnion_eq {Ω : Type*} {Y : ℝ≥0 → Ω → ℝ}
    (hYc : ∀ ω, Continuous (Y · ω)) {t : ℝ≥0} (ht : 0 < t) (a : ℝ) :
    (⋃ n : ℕ, {ω | ∃ k ≤ 2 ^ n, a < Y (brownianGrid t (2 ^ n) k) ω}) =
      {ω | (a : EReal) < ⨆ s ≤ t, (Y s ω).toEReal} := by
  ext ω
  simp only [Set.mem_iUnion, Set.mem_ofPred_eq]
  constructor
  · rintro ⟨n, k, hk, hgt⟩
    have hs : brownianGrid t (2 ^ n) k ≤ t := brownianGrid_le t (by positivity) hk
    exact lt_of_lt_of_le (EReal.coe_lt_coe_iff.mpr hgt)
      (le_iSup₂_of_le (brownianGrid t (2 ^ n) k) hs le_rfl)
  · intro hlt
    rw [lt_iSup_iff] at hlt
    rcases hlt with ⟨s, hlt⟩
    rw [lt_iSup_iff] at hlt
    rcases hlt with ⟨hs, hgtE⟩
    have hgt : a < Y s ω := EReal.coe_lt_coe_iff.mp hgtE
    have hnhds : {u : ℝ≥0 | a < Y u ω} ∈ 𝓝 s :=
      (isOpen_lt continuous_const (hYc ω)).mem_nhds hgt
    rcases Metric.mem_nhds_iff.mp hnhds with ⟨ε, hε, hball⟩
    have htend : Tendsto (fun n : ℕ ↦ (t : ℝ) / (2 : ℝ) ^ n) atTop (𝓝 0) :=
      tendsto_const_nhds.div_atTop (tendsto_pow_atTop_atTop_of_one_lt one_lt_two)
    rcases (htend.eventually (gt_mem_nhds hε)).exists with ⟨n, hn⟩
    let h : ℝ := (t : ℝ) / (2 : ℝ) ^ n
    have hh_pos : 0 < h := by
      have htR : 0 < (t : ℝ) := ht
      positivity
    let k : ℕ := ⌊(s : ℝ) / h⌋₊
    have hk_le : k ≤ 2 ^ n := by
      refine Nat.floor_le_of_le ?_
      have hstR : (s : ℝ) ≤ (t : ℝ) := hs
      calc
        (s : ℝ) / h ≤ (t : ℝ) / h := div_le_div_of_nonneg_right hstR hh_pos.le
        _ = (2 : ℝ) ^ n := by
              dsimp [h]
              field_simp [ne_of_gt (show 0 < (t : ℝ) from ht)]
        _ = ((2 ^ n : ℕ) : ℝ) := by push_cast; rfl
    have hgrid_val : ((brownianGrid t (2 ^ n) k : ℝ≥0) : ℝ) = (k : ℝ) * h := by
      simp [brownianGrid, h]
    have hlo : (k : ℝ) * h ≤ (s : ℝ) := by
      have hs_div : 0 ≤ (s : ℝ) / h := div_nonneg s.coe_nonneg hh_pos.le
      exact (le_div_iff₀ hh_pos).mp (Nat.floor_le hs_div)
    have hhi : (s : ℝ) < ((k : ℝ) + 1) * h :=
      (div_lt_iff₀ hh_pos).mp (Nat.lt_floor_add_one ((s : ℝ) / h))
    have hdist : dist (brownianGrid t (2 ^ n) k) s < ε := by
      rw [NNReal.dist_eq, hgrid_val, abs_sub_lt_iff]
      constructor <;> linarith
    exact ⟨n, k, hk_le, hball hdist⟩

private lemma real_le_iff_forall_sub_inv_lt (c x : ℝ) :
    c ≤ x ↔ ∀ m : ℕ, c - 1 / ((m : ℝ) + 1) < x := by
  constructor
  · intro hcx m
    have hpos : (0 : ℝ) < 1 / ((m : ℝ) + 1) := by positivity
    linarith
  · intro h
    by_contra! hlt
    rcases exists_nat_one_div_lt (sub_pos.mpr hlt) with ⟨m, hm⟩
    have hm' := h m
    linarith

private lemma ereal_coe_le_iff_forall_sub_inv_lt (c : ℝ) (z : EReal) :
    (c : EReal) ≤ z ↔ ∀ m : ℕ, (c - 1 / ((m : ℝ) + 1)).toEReal < z := by
  induction z with
  | bot =>
    simp only [le_bot_iff, EReal.coe_ne_bot, not_lt_bot, false_iff, not_forall]
    exact ⟨0, id⟩
  | top =>
    simp only [le_top, EReal.coe_lt_top, implies_true]
  | coe x =>
    simp only [EReal.coe_le_coe_iff, EReal.coe_lt_coe_iff]
    exact real_le_iff_forall_sub_inv_lt c x

private lemma measureReal_sup_le_two_mul {Ω : Type*} {mΩ : MeasurableSpace Ω}
    {P : Measure Ω} {Y : ℝ≥0 → Ω → ℝ} (hY : IsPreBrownianReal Y P)
    (hYm : ∀ r, Measurable (Y r)) (hYc : ∀ ω, Continuous (Y · ω)) {t : ℝ≥0} (ht : 0 < t)
    (c : ℝ) :
    P.real {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal} ≤ 2 * P.real {ω | c ≤ Y t ω} := by
  have : IsProbabilityMeasure P := (hY.hasLaw ∅).isProbabilityMeasure
  have hstrict : ∀ a : ℝ, MeasurableSet {ω | (a : EReal) < ⨆ s ≤ t, (Y s ω).toEReal} ∧
      P.real {ω | (a : EReal) < ⨆ s ≤ t, (Y s ω).toEReal} ≤ 2 * P.real {ω | a < Y t ω} := by
    intro a
    let A : ℕ → Set Ω := fun n ↦ {ω | ∃ k ≤ 2 ^ n, a < Y (brownianGrid t (2 ^ n) k) ω}
    have hA_meas : ∀ n, MeasurableSet (A n) := fun n ↦ by
      dsimp only [A]
      rw [← biUnion_firstPassageSet_eq Y t a (2 ^ n)]
      exact Finset.measurableSet_biUnion _ fun k _ ↦ measurableSet_firstPassageSet hYm t a (2 ^ n) k
    have hA_mono : Monotone A := monotone_nat_of_le_succ fun n ω ⟨k, hk, hgt⟩ ↦ by
      refine ⟨2 * k, ?_, ?_⟩
      · rw [pow_succ']
        exact Nat.mul_le_mul_left 2 hk
      · rwa [brownianGrid_pow_two_succ]
    have hA_union : (⋃ n, A n) = {ω | (a : EReal) < ⨆ s ≤ t, (Y s ω).toEReal} :=
      dyadic_exceed_iUnion_eq hYc ht a
    have hmeas_sup : MeasurableSet {ω | (a : EReal) < ⨆ s ≤ t, (Y s ω).toEReal} := by
      rw [← hA_union]
      exact MeasurableSet.iUnion hA_meas
    have htendP : Tendsto (fun n ↦ P (A n)) atTop
        (𝓝 (P {ω | (a : EReal) < ⨆ s ≤ t, (Y s ω).toEReal})) := by
      rw [← hA_union]
      exact tendsto_measure_iUnion_atTop hA_mono
    have htendR : Tendsto (fun n ↦ P.real (A n)) atTop
        (𝓝 (P.real {ω | (a : EReal) < ⨆ s ≤ t, (Y s ω).toEReal})) :=
      (ENNReal.continuousAt_toReal (measure_ne_top P _)).tendsto.comp htendP
    refine ⟨hmeas_sup, le_of_tendsto' htendR fun n ↦ ?_⟩
    exact measureReal_dyadic_exceed_le hY hYm t a (by positivity)
  let D : ℕ → Set Ω := fun m ↦
    {ω | (c - 1 / ((m : ℝ) + 1)).toEReal < ⨆ s ≤ t, (Y s ω).toEReal}
  let R : ℕ → Set Ω := fun m ↦ {ω | c - 1 / ((m : ℝ) + 1) < Y t ω}
  have hstep : ∀ m : ℕ, c - 1 / (((m + 1 : ℕ) : ℝ) + 1) ≥ c - 1 / ((m : ℝ) + 1) := by
    intro m
    have h1 : (0 : ℝ) < (m : ℝ) + 1 := by positivity
    have h2 : (m : ℝ) + 1 ≤ ((m + 1 : ℕ) : ℝ) + 1 := by push_cast; linarith
    have hinv : 1 / (((m + 1 : ℕ) : ℝ) + 1) ≤ 1 / ((m : ℝ) + 1) :=
      one_div_le_one_div_of_le h1 h2
    linarith
  have hD_anti : Antitone D := antitone_nat_of_succ_le fun m ω hω ↦
    lt_of_le_of_lt (EReal.coe_le_coe_iff.mpr (hstep m)) hω
  have hR_anti : Antitone R := antitone_nat_of_succ_le fun m ω hω ↦
    lt_of_le_of_lt (hstep m) hω
  have hD_inter : (⋂ m, D m) = {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal} := by
    ext ω
    simp only [D, Set.mem_iInter, Set.mem_ofPred_eq, ← ereal_coe_le_iff_forall_sub_inv_lt]
  have hR_inter : (⋂ m, R m) = {ω | c ≤ Y t ω} := by
    ext ω
    simp only [R, Set.mem_iInter, Set.mem_ofPred_eq, ← real_le_iff_forall_sub_inv_lt]
  have hD_tend : Tendsto (fun m ↦ P.real (D m)) atTop
      (𝓝 (P.real {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal})) := by
    have htP : Tendsto (fun m ↦ P (D m)) atTop
        (𝓝 (P {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal})) := by
      rw [← hD_inter]
      exact tendsto_measure_iInter_atTop
        (fun m ↦ (hstrict _).1.nullMeasurableSet) hD_anti ⟨0, measure_ne_top P _⟩
    exact (ENNReal.continuousAt_toReal (measure_ne_top P _)).tendsto.comp htP
  have hR_tend : Tendsto (fun m ↦ 2 * P.real (R m)) atTop (𝓝 (2 * P.real {ω | c ≤ Y t ω})) := by
    refine Tendsto.const_mul 2 ?_
    have htP : Tendsto (fun m ↦ P (R m)) atTop (𝓝 (P {ω | c ≤ Y t ω})) := by
      rw [← hR_inter]
      exact tendsto_measure_iInter_atTop
        (fun m ↦ (measurableSet_lt measurable_const (hYm t)).nullMeasurableSet)
        hR_anti ⟨0, measure_ne_top P _⟩
    exact (ENNReal.continuousAt_toReal (measure_ne_top P _)).tendsto.comp htP
  exact le_of_tendsto_of_tendsto hD_tend hR_tend (Eventually.of_forall fun m ↦ (hstrict _).2)

private lemma tendsto_measureReal_grid_oscillation_zero {Ω : Type*} {mΩ : MeasurableSpace Ω}
    {P : Measure Ω} [IsProbabilityMeasure P] {Y : ℝ≥0 → Ω → ℝ}
    (hYm : ∀ r, Measurable (Y r)) (hYc : ∀ ω, Continuous (Y · ω)) (t : ℝ≥0) {δ : ℝ}
    (hδ : 0 < δ) :
    Tendsto (fun N : ℕ ↦ P.real (⋃ j ∈ Finset.range N,
      {ω | δ < Y (brownianGrid t N (j + 1)) ω - Y (brownianGrid t N j) ω})) atTop (𝓝 0) := by
  let B : ℕ → Set Ω := fun N ↦
    ⋃ j ∈ Finset.range N, {ω | δ < Y (brownianGrid t N (j + 1)) ω - Y (brownianGrid t N j) ω}
  have hB_meas : ∀ N, MeasurableSet (B N) := fun N ↦
    Finset.measurableSet_biUnion _ fun j _ ↦
      measurableSet_lt measurable_const ((hYm _).sub (hYm _))
  let F : ℕ → Ω → ℝ := fun N ↦ (B N).indicator 1
  have hF_meas : ∀ N, AEStronglyMeasurable (F N) P := fun N ↦
    (stronglyMeasurable_const.indicator (hB_meas N)).aestronglyMeasurable
  have hF_bdd : ∀ N, ∀ᵐ ω ∂P, ‖F N ω‖ ≤ (1 : ℝ) := fun N ↦
    ae_of_all P fun ω ↦ by
      by_cases hω : ω ∈ B N <;> simp [F, hω]
  have hF_lim : ∀ᵐ ω ∂P, Tendsto (fun N ↦ F N ω) atTop (𝓝 (0 : ℝ)) := by
    refine ae_of_all P fun ω ↦ ?_
    have huc : UniformContinuousOn (Y · ω) (Set.Icc 0 t) :=
      isCompact_Icc.uniformContinuousOn_of_continuous (hYc ω).continuousOn
    rcases Metric.uniformContinuousOn_iff.mp huc δ hδ with ⟨η, hη, hmod⟩
    have htend : Tendsto (fun N : ℕ ↦ (t : ℝ) / (N : ℝ)) atTop (𝓝 0) :=
      tendsto_const_nhds.div_atTop tendsto_natCast_atTop_atTop
    have hev : ∀ᶠ N : ℕ in atTop, F N ω = 0 := by
      filter_upwards [eventually_ge_atTop 1, htend.eventually (gt_mem_nhds hη)] with N hN1 hNη
      have hnot : ω ∉ B N := by
        intro hmem
        simp only [B, Set.mem_iUnion, Finset.mem_range, Set.mem_ofPred_eq] at hmem
        rcases hmem with ⟨j, hjN, hbig⟩
        have hN0 : N ≠ 0 := by omega
        have hu : brownianGrid t N (j + 1) ∈ Set.Icc 0 t :=
          ⟨zero_le, brownianGrid_le t hN0 (by omega)⟩
        have hv : brownianGrid t N j ∈ Set.Icc 0 t :=
          ⟨zero_le, brownianGrid_le t hN0 (by omega)⟩
        have hdist : dist (brownianGrid t N (j + 1)) (brownianGrid t N j) < η := by
          have hdiff : ((brownianGrid t N (j + 1) : ℝ≥0) : ℝ) -
              ((brownianGrid t N j : ℝ≥0) : ℝ) = (t : ℝ) / (N : ℝ) := by
            unfold brownianGrid
            push_cast
            ring
          have hnn : (0 : ℝ) ≤ (t : ℝ) / (N : ℝ) := by positivity
          rw [NNReal.dist_eq, hdiff, abs_of_nonneg hnn]
          exact hNη
        have hlt := hmod (brownianGrid t N (j + 1)) hu (brownianGrid t N j) hv hdist
        rw [Real.dist_eq] at hlt
        linarith [le_abs_self (Y (brownianGrid t N (j + 1)) ω - Y (brownianGrid t N j) ω)]
      simp [F, hnot]
    exact tendsto_const_nhds.congr' (hev.mono fun _ h ↦ h.symm)
  have hint := tendsto_integral_of_dominated_convergence (fun _ ↦ (1 : ℝ)) hF_meas
    (integrable_const 1) hF_bdd hF_lim
  simp only [integral_zero] at hint
  refine hint.congr fun N ↦ ?_
  exact integral_indicator_one (hB_meas N)

private lemma two_mul_measureReal_le_sup {Ω : Type*} {mΩ : MeasurableSpace Ω}
    {P : Measure Ω} {Y : ℝ≥0 → Ω → ℝ} (hY : IsPreBrownianReal Y P)
    (hYm : ∀ r, Measurable (Y r)) (hYc : ∀ ω, Continuous (Y · ω)) {t : ℝ≥0} (ht : 0 < t)
    {c : ℝ} (hc : 0 ≤ c) :
    2 * P.real {ω | c ≤ Y t ω} ≤ P.real {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal} := by
  have : IsProbabilityMeasure P := (hY.hasLaw ∅).isProbabilityMeasure
  have hdelta : ∀ δ : ℝ, 0 < δ →
      P.real {ω | c + δ < Y t ω} ≤
        (1 / 2 : ℝ) * P.real {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal} := by
    intro δ hδ
    let B : ℕ → Set Ω := fun N ↦
      ⋃ j ∈ Finset.range N, {ω | δ < Y (brownianGrid t N (j + 1)) ω - Y (brownianGrid t N j) ω}
    have hN_bound : ∀ N : ℕ, 1 ≤ N →
        P.real {ω | c + δ < Y t ω} ≤
          (1 / 2 : ℝ) * P.real {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal} + P.real (B N) := by
      intro N hN1
      have hN0 : N ≠ 0 := by omega
      let Z0 : Set Ω := {ω | Y 0 ω ≠ 0}
      let Gk : ℕ → Set Ω := fun k ↦
        firstPassageSet Y t c N k ∩ {ω | 0 < Y t ω - Y (brownianGrid t N k) ω}
      let G : Set Ω := ⋃ k ∈ Finset.range (N + 1), Gk k
      have hGk_meas : ∀ k ∈ Finset.range (N + 1), MeasurableSet (Gk k) := fun k _ ↦
        (measurableSet_firstPassageSet hYm t c N k).inter
          (measurableSet_lt measurable_const ((hYm t).sub (hYm _)))
      have hGk_disj : (↑(Finset.range (N + 1)) : Set ℕ).PairwiseDisjoint Gk := by
        intro i _ j _ hij
        exact ((pairwiseDisjoint_firstPassageSet Y t c N) (Set.mem_univ i) (Set.mem_univ j)
          hij).mono Set.inter_subset_left Set.inter_subset_left
      have hsub : {ω | c + δ < Y t ω} ⊆ Z0 ∪ (G ∪ B N) := by
        intro ω hω
        simp only [Set.mem_ofPred_eq] at hω
        by_cases h0 : Y 0 ω = 0
        · right
          have hex : ω ∈ {ω' | ∃ k ≤ N, c < Y (brownianGrid t N k) ω'} := by
            refine ⟨N, le_rfl, ?_⟩
            rw [brownianGrid_self t hN0]
            linarith
          rw [← biUnion_firstPassageSet_eq Y t c N] at hex
          simp only [Set.mem_iUnion, Finset.mem_range, Nat.lt_succ_iff] at hex
          rcases hex with ⟨k, hkN, hfp⟩
          have hk_pos : 0 < k := by
            rcases Nat.eq_zero_or_pos k with rfl | hpos
            · exfalso
              have hcgt := hfp.1
              rw [brownianGrid_zero, h0] at hcgt
              linarith
            · exact hpos
          by_cases hle : Y (brownianGrid t N k) ω ≤ c + δ
          · left
            simp only [G, Set.mem_iUnion, Finset.mem_range, Nat.lt_succ_iff, Gk,
              Set.mem_inter_iff, Set.mem_ofPred_eq]
            exact ⟨k, hkN, hfp, by linarith⟩
          · right
            simp only [B, Set.mem_iUnion, Finset.mem_range, Set.mem_ofPred_eq]
            refine ⟨k - 1, by omega, ?_⟩
            have hk_prev : Y (brownianGrid t N (k - 1)) ω ≤ c := hfp.2 (k - 1) (by omega)
            have hk_eq : k - 1 + 1 = k := by omega
            rw [hk_eq]
            linarith
        · exact Or.inl h0
      have hZ0_null : P Z0 = 0 := by
        have hae := hY.eval_zero_ae_eq_zero
        rwa [ae_iff] at hae
      have hP_le : P.real {ω | c + δ < Y t ω} ≤ P.real G + P.real (B N) := by
        have h1 : P.real {ω | c + δ < Y t ω} ≤ P.real (Z0 ∪ (G ∪ B N)) := measureReal_mono hsub
        have h2 : P.real (Z0 ∪ (G ∪ B N)) = P.real (G ∪ B N) :=
          congrArg ENNReal.toReal <| le_antisymm
            ((measure_union_le _ _).trans (by simp [hZ0_null]))
            (measure_mono Set.subset_union_right)
        have h3 : P.real (G ∪ B N) ≤ P.real G + P.real (B N) :=
          measureReal_union_le G (B N)
        linarith
      have hG_le : P.real G ≤
          (1 / 2 : ℝ) * P.real {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal} := by
        have hsum : P.real G = ∑ k ∈ Finset.range (N + 1), P.real (Gk k) :=
          measureReal_biUnion_finset hGk_disj hGk_meas
        have hterm : ∀ k ∈ Finset.range (N + 1),
            P.real (Gk k) ≤ (1 / 2 : ℝ) * P.real (firstPassageSet Y t c N k) := by
          intro k hk
          have hkN : k ≤ N := Nat.lt_succ_iff.mp (Finset.mem_range.mp hk)
          have hfac :=
            measureReal_firstPassageSet_inter_sub hY t c hN0 hkN (measurableSet_Ioi (a := 0))
          change P.real (firstPassageSet Y t c N k ∩
            {ω | Y t ω - Y (brownianGrid t N k) ω ∈ Set.Ioi 0}) ≤ _
          rw [hfac]
          have hhalf : P.real {ω | Y t ω - Y (brownianGrid t N k) ω ∈ Set.Ioi 0} ≤ 1 / 2 :=
            hasLaw_gaussianReal_prob_pos_le_half (hY.hasLaw_sub t (brownianGrid t N k))
          have hnonneg : 0 ≤ P.real (firstPassageSet Y t c N k) := measureReal_nonneg
          nlinarith
        have hpart : ∑ k ∈ Finset.range (N + 1), P.real (firstPassageSet Y t c N k) =
            P.real {ω | ∃ k ≤ N, c < Y (brownianGrid t N k) ω} := by
          rw [← biUnion_firstPassageSet_eq Y t c N]
          exact (measureReal_biUnion_finset
            ((pairwiseDisjoint_firstPassageSet Y t c N).subset (Set.subset_univ _))
            (fun k _ ↦ measurableSet_firstPassageSet hYm t c N k)).symm
        have hex_sub : {ω | ∃ k ≤ N, c < Y (brownianGrid t N k) ω} ⊆
            {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal} := by
          rintro ω ⟨k, hkN, hgt⟩
          have hs : brownianGrid t N k ≤ t := brownianGrid_le t hN0 hkN
          exact (EReal.coe_le_coe_iff.mpr hgt.le).trans
            (le_iSup₂_of_le (brownianGrid t N k) hs le_rfl)
        have hmono : P.real {ω | ∃ k ≤ N, c < Y (brownianGrid t N k) ω} ≤
            P.real {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal} :=
          measureReal_mono hex_sub
        calc
          P.real G = ∑ k ∈ Finset.range (N + 1), P.real (Gk k) := hsum
          _ ≤ ∑ k ∈ Finset.range (N + 1), (1 / 2 : ℝ) * P.real (firstPassageSet Y t c N k) :=
                Finset.sum_le_sum hterm
          _ = (1 / 2 : ℝ) * P.real {ω | ∃ k ≤ N, c < Y (brownianGrid t N k) ω} := by
                rw [← Finset.mul_sum, hpart]
          _ ≤ (1 / 2 : ℝ) * P.real {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal} := by linarith
      linarith
    have htendB := tendsto_measureReal_grid_oscillation_zero (P := P) hYm hYc t hδ
    have htendRHS : Tendsto
        (fun N : ℕ ↦ (1 / 2 : ℝ) * P.real {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal} +
          P.real (B N)) atTop
        (𝓝 ((1 / 2 : ℝ) * P.real {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal} + 0)) :=
      tendsto_const_nhds.add htendB
    rw [add_zero] at htendRHS
    exact le_of_tendsto_of_tendsto tendsto_const_nhds htendRHS
      ((eventually_ge_atTop 1).mono hN_bound)
  let U : ℕ → Set Ω := fun m ↦ {ω | c + 1 / ((m : ℝ) + 1) < Y t ω}
  have hU_mono : Monotone U := monotone_nat_of_le_succ fun m ω hω ↦ by
    dsimp only [U] at hω ⊢
    simp only [Set.mem_ofPred_eq] at hω ⊢
    have h1 : (0 : ℝ) < (m : ℝ) + 1 := by positivity
    have h2 : (m : ℝ) + 1 ≤ ((m + 1 : ℕ) : ℝ) + 1 := by push_cast; linarith
    have hinv : 1 / (((m + 1 : ℕ) : ℝ) + 1) ≤ 1 / ((m : ℝ) + 1) :=
      one_div_le_one_div_of_le h1 h2
    linarith
  have hU_union : (⋃ m, U m) = {ω | c < Y t ω} := by
    ext ω
    simp only [U, Set.mem_iUnion, Set.mem_ofPred_eq]
    constructor
    · rintro ⟨m, hm⟩
      have hpos : (0 : ℝ) < 1 / ((m : ℝ) + 1) := by positivity
      linarith
    · intro hlt
      rcases exists_nat_one_div_lt (sub_pos.mpr hlt) with ⟨m, hm⟩
      exact ⟨m, by linarith⟩
  have hU_tend : Tendsto (fun m ↦ P.real (U m)) atTop (𝓝 (P.real {ω | c < Y t ω})) := by
    have htP : Tendsto (fun m ↦ P (U m)) atTop (𝓝 (P {ω | c < Y t ω})) := by
      rw [← hU_union]
      exact tendsto_measure_iUnion_atTop hU_mono
    exact (ENNReal.continuousAt_toReal (measure_ne_top P _)).tendsto.comp htP
  have hgt_le : P.real {ω | c < Y t ω} ≤
      (1 / 2 : ℝ) * P.real {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal} :=
    le_of_tendsto' hU_tend fun m ↦ hdelta (1 / ((m : ℝ) + 1)) (by positivity)
  have hge_eq : P.real {ω | c ≤ Y t ω} = P.real {ω | c < Y t ω} :=
    hasLaw_gaussianReal_prob_ge_eq_gt ht.ne' (hY.hasLaw_eval t) c
  linarith

end ReflectionAux

variable {Ω : Type*} {mΩ : MeasurableSpace Ω} {P : Measure Ω}
variable {X}

lemma IsBrownianReal.reflection (hX : IsBrownianReal X P) {t : ℝ≥0} {c : ℝ}
    (ht : 0 < t) (hc : 0 ≤ c) :
    P.real {ω | c ≤ ⨆ s ≤ t, (X s ω).toEReal} = 2 * P.real {ω | c ≤ X t ω} := by
  let Y := hX.toIsPreBrownianReal.mk X
  have hY : IsPreBrownianReal Y P := hX.isBrownianReal_mk.toIsPreBrownianReal
  have hYm : ∀ r, Measurable (Y r) := hX.measurable_mk
  have hYc : ∀ ω, Continuous (Y · ω) := hX.continuous_mk
  have h_ae := hX.mk_ae_forall_eq
  have hcongr1 : ({ω | (c : EReal) ≤ ⨆ s ≤ t, (X s ω).toEReal} : Set Ω) =ᵐ[P]
      {ω | (c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal} := by
    filter_upwards [h_ae] with ω hω
    change ((c : EReal) ≤ ⨆ s ≤ t, (X s ω).toEReal) = ((c : EReal) ≤ ⨆ s ≤ t, (Y s ω).toEReal)
    simp_rw [Y, hω]
  have hcongr2 : ({ω | c ≤ X t ω} : Set Ω) =ᵐ[P] {ω | c ≤ Y t ω} := by
    filter_upwards [h_ae] with ω hω
    dsimp only [Y]
    rw [hω t]
  rw [measureReal_congr hcongr1, measureReal_congr hcongr2]
  exact le_antisymm
    (measureReal_sup_le_two_mul hY hYm hYc ht c)
    (two_mul_measureReal_le_sup hY hYm hYc ht hc)

lemma IsStandardGaussian.tail (hX : HasLaw X (gaussianReal 0 1) P) :
    Asymptotics.IsEquivalent atTop (fun x ↦ P.real {ω | x ≤ X ω})
    (fun x ↦ 1 / x * exp (-1/2 * x ^ 2)) :=
  sorry -- exponential asymptotics of standard Gaussian CDF

private lemma IsBrownianReal.ae_limsup_div_sqrt_log_log_le_one (hX : IsBrownianReal X P) :
    ∀ᵐ ω ∂P, limsup (fun t ↦ ((X t ω) / √(2 * t * log (log t))).toEReal) atTop ≤ 1 := by
  -- Introduce notation
  have := (hX.hasLaw ∅).isProbabilityMeasure
  let M := fun t ω ↦ (⨆ s ≤ t, (X s ω : EReal))
  let f := fun (t : ℝ≥0) ↦ √(2 * t * log (log t))
  have fmono : MonotoneOn f (Set.Ici (⟨(exp 1),by positivity⟩)) := by
    intro x hx y hy hxy
    have hx0 : (0 < x) := by apply lt_of_lt_of_le (exp_pos _) hx
    have hx1 : (1 ≤ log x) := by
      rwa [← exp_le_exp, exp_log (by positivity)]
    apply sqrt_le_sqrt
    apply mul_le_mul (by bound) _ (log_nonneg hx1) (by bound)
    apply log_le_log (by positivity)
    apply log_le_log hx0 hxy
  -- Rewrite limsup inequality in terms of quantifiers which do not depend on `ω`
  simp_rw [ae_le_const_iff_forall_gt_measure_zero, ← not_lt, ← ae_iff]
  suffices h : ∀ c : ℝ≥0, 1 < c → ∀ᵐ (ω : Ω) ∂P, ∀ᶠ (t : ℝ≥0) in atTop,
      X t ω < c * f t by
    intro _ hc
    rcases EReal.lt_iff_exists_real_btwn.mp hc with ⟨b,hb⟩
    lift b to ℝ≥0 using by positivity [by exact_mod_cast hb.1]
    filter_upwards [h b <| by exact_mod_cast hb.1] with _ hω
    apply lt_of_le_of_lt _ hb.2
    apply limsup_le_of_le (hf := by isBoundedDefault)
    filter_upwards [hω] with t ht
    apply EReal.coe_le_coe <| div_le_of_le_mul₀ (by positivity) (by positivity) _
    exact le_of_lt ht
  intro c hc
  -- Prepare for application of Borel-Cantellli
  suffices h : ∀ᵐ ω ∂P, ∀ᶠ n : ℕ in atTop, ω ∉ {ω | (c : ℝ) * f (c ^ n) ≤ M (c ^ (n + 1)) ω} by
    filter_upwards [h] with ω hω
    -- Make a function which relates t to n
    choose n htn1 htn2 using
      fun t ↦ exists_nat_pow_near (x := max 1 t) (y := c) (by bound) (by bound)
    have h_tt1 : Tendsto (fun t ↦ n t) atTop atTop := by
      apply Tendsto.atTop_of_add_const 1
      rw [tendsto_atTop]
      intro m
      filter_upwards [eventually_ge_atTop 1, eventually_ge_atTop (c ^ m)] with t ht1 ht2
      specialize htn2 t
      rw [max_eq_right ht1] at htn2
      rw [← pow_le_pow_iff_right₀ (hc)]
      apply le_of_lt <| lt_of_le_of_lt ht2 htn2
    have h_tt2 := (tendsto_pow_atTop_atTop_of_one_lt hc).comp h_tt1
    filter_upwards [h_tt1.eventually hω, eventually_ge_atTop 1,
      h_tt2.eventually_ge_atTop ⟨(exp 1),by positivity⟩] with t ht ht1 htn3
    specialize htn1 t
    specialize htn2 t
    rw [max_eq_right ht1] at htn1 htn2
    exact_mod_cast calc
      X t ω ≤ M (c ^ (n t + 1)) ω := le_iSup_of_le t <| le_iSup_of_le (by bound) (by rfl)
      _ < (c * f (c ^ (n t))) := lt_of_not_ge ht
      _ ≤ (c : ℝ) * (f t) := by
        apply mul_le_mul_of_nonneg_left _ <| le_of_lt <| by positivity
        apply EReal.coe_le_coe <| fmono htn3 (le_trans htn3 htn1) htn1
  apply ae_eventually_notMem
  conv in P _ => rw [← ofReal_measureReal]
  conv in P.real _ => rw [← EReal.coe_mul, hX.reflection (by positivity) (by positivity)]
  apply Summable.tsum_ofReal_ne_top
  rw [summable_mul_left_iff (by norm_num)]
  -- introduce auxiliary function g and show limit at infinity
  let g := fun n : ℕ ↦ √(2 * c * log (log (c ^ n)))
  have hg_tt : Tendsto g atTop atTop := by
    apply tendsto_sqrt_atTop.comp
    apply Tendsto.const_mul_atTop (by positivity)
    repeat apply tendsto_log_atTop.comp
    exact tendsto_pow_atTop_atTop_of_one_lt hc
  -- convert to standard Gaussian
  apply Summable.congr (f := fun n ↦ P.real {ω | g n ≤ X 1 ω}); swap
  · intro n
    simp_rw [Measure.real_def]
    rw [ENNReal.toReal_eq_toReal_iff' (by finiteness) (by finiteness)]
    have h : IdentDistrib (fun ω ↦ √(c ^ (n + 1)) * X 1 ω) (X (c ^ (n + 1))) P P := by
      apply IdentDistrib.symm
      apply (hX.hasLaw_eval _).identDistrib
      convert gaussianReal_const_mul (hX.hasLaw_eval _) _
      · norm_num
      · aesop
    convert h.measure_mem_eq (s := {x | c * f (c ^ n) ≤ (x : ℝ)}) _
    · simp_rw [Set.preimage_ofPred_eq]
      rw [← mul_le_mul_iff_of_pos_left (by positivity : 0 < √(c ^ (n + 1)))]
      congr! 1
      rw [← sqrt_sq (by positivity : 0 ≤ (c : ℝ))]
      repeat rw [← sqrt_mul (by positivity)]
      rw [sqrt_sq (by positivity), pow_add]
      push_cast
      field_simp
    · rfl
    · measurability
  apply summable_of_isBigO_nat <| summable_nat_rpow_inv.2 hc
  -- apply Gaussian tail estimate
  have h := (IsStandardGaussian.tail (hX.hasLaw_eval 1)).comp_tendsto hg_tt
  apply Asymptotics.IsEquivalent.trans_isBigO h _
  -- reduce to concrete bound
  apply Asymptotics.IsBigO.of_bound <| 1 * ((log c) ^ (c : ℝ))⁻¹
  filter_upwards [hg_tt.eventually_ge_atTop 1, eventually_ge_atTop 1] with n hg1 hn
  simp_rw [Function.comp_def]
  repeat rw [norm_of_nonneg (by positivity)]
  conv_rhs => rw [mul_assoc]
  apply mul_le_mul _ _ (by positivity) (by norm_num)
  · rw [one_div_le _ (by norm_num)]; swap
    · bound
    · bound
  · rw [sq_sqrt]; swap
    · positivity [one_le_sqrt.mp hg1]
    field_simp
    conv in exp _ => rw [mul_comm]
    rw [exp_neg, exp_mul, exp_log, log_pow]; swap
    · rw [log_pow]
      exact mul_pos (by exact_mod_cast hn) (log_pos (by exact_mod_cast hc))
    rw [mul_rpow (by positivity) _]; swap
    · exact (log_pos (by exact_mod_cast hc)).le
    field_simp
    rfl

private lemma IsBrownianReal.ae_one_le_limsup_div_sqrt_log_log (hX : IsBrownianReal X P)
    (h_meas : ∀ t, Measurable (X t)) :
    ∀ᵐ ω ∂P, 1 ≤ limsup (fun t ↦ X t ω / √(2 * t * log (log t)) : ℝ≥0 → EReal) atTop := by
  have := (hX.hasLaw ∅).isProbabilityMeasure
  let f := fun (t : ℝ≥0) ↦ √(2 * t * log (log t))
  -- Rewrite the inequality into a nice form with the quantifier outside
  suffices h : ∀ (c : ℝ), 1 < c → 1 < log c → ∀ᵐ ω ∂P, √(1 - 1 / c) - (1 / √c : ℝ) ≤
      limsup (fun t ↦ (X t ω) / (f t) : ℝ≥0 → EReal) atTop by
    simp_rw [ae_const_le_iff_forall_lt_measure_zero, ← not_lt, ← ae_iff]
    have h' : Tendsto (fun (r : ℝ) ↦ √(1 - 1 / r) - (1 / √r)) atTop (nhds 1) := by
      rw [(by simp : nhds (1 : ℝ) = nhds (sqrt (1 - 0) - 0))]
      apply Tendsto.sub
      · apply Tendsto.sqrt
        apply Tendsto.sub (by aesop)
        apply Tendsto.const_div_atTop <| tendsto_id
      · apply Tendsto.const_div_atTop <| tendsto_sqrt_atTop
    intro c hc1
    wlog! hc0 : (0 < c) generalizing c with h
    · replace h := fun (c : ℝ) ↦ h c
      specialize h (1/2) (?_) (by norm_num)
      · apply EReal.coe_lt_coe; bound
      exact h.mono fun _ hω ↦ lt_trans (lt_of_le_of_lt hc0 (by norm_num)) hω
    · lift c to ℝ using by aesop;; norm_cast at hc0 hc1
      apply (eventually_const (f := atTop (α := ℝ))).1
      filter_upwards [eventually_gt_atTop 1, tendsto_log_atTop.eventually_gt_atTop 1,
      Eventually.of_forall h, h'.eventually <| lt_mem_nhds <| hc1] with r hr1 hlogr hrimp hrc
      filter_upwards [hrimp hr1 hlogr] with ω hω
      exact lt_of_lt_of_le (by exact_mod_cast hrc) hω
  intro c hc1 hlogc
  have hloglogc := log_pos hlogc
  lift c to ℝ≥0 using by positivity
  have hc0 : (0 < c) := by positivity [by exact_mod_cast hc1]
  -- Rewrite in terms of limsup of difference
  suffices h1 : ∀ᵐ ω ∂P, √(1 - 1 / c) ≤
      limsup (fun t ↦ ((X t ω - X (t / c) ω) / f t).toEReal) atTop by
    have h2 : ∀ᵐ ω ∂P,
        limsup (fun t ↦ (-X (t / c) ω / f (t)).toEReal) atTop
          ≤ (1 / √c).toEReal := by
      convert IsBrownianReal.ae_limsup_div_sqrt_log_log_le_one
        (X := fun t ω ↦ √c * (-X (t / c) ω)) _ using 1
      · funext ω
        simp_rw [← mul_div, EReal.coe_mul]
        rw [EReal.limsup_const_mul_of_nonneg_of_ne_top (by positivity) (by aesop)]
        rw [mul_comm, ← EReal.le_div_iff_mul_le (by positivity) (by aesop)]
        rfl
      · convert hX.neg.smul (c := (1 / c)) (by positivity) using 3 with t
        simp [div_eq_inv_mul]
    filter_upwards [h1, h2] with ω hω hω'
    simp_rw [neg_div, EReal.coe_neg, ← Pi.neg_def, EReal.limsup_neg, EReal.neg_le] at hω'
    grw [sub_eq_add_neg, (add_le_add hω hω'), EReal.le_limsup_add]
    apply le_of_eq
    simp_rw [← EReal.coe_div, ← div_sub_div_same,
      EReal.coe_sub, Pi.add_def]
    norm_cast
    aesop
  -- auxiliary definitions
  let g := fun (n : ℕ) ↦ √(2 * log (log (c ^ n)))
  let A := fun n ↦ {ω | sqrt (c ^ (n + 1) - c ^ n) * g (n + 1) ≤
    (X (c ^ (n + 1)) ω - X (c ^ n) ω)}
  -- prepare for application of Borel-Cantelli
  suffices h : P (limsup A atTop) = 1 by
    rw [← mem_ae_iff_prob_eq_one <| by measurability] at h
    filter_upwards [h] with ω hω
    rw [mem_limsup_iff_frequently_mem] at hω
    apply le_limsup_of_frequently_le'
    apply Tendsto.frequently_map _ (_ : Tendsto (fun n ↦ c ^ (n + 1)) atTop atTop) _ hω
    · simp_rw [pow_add]
      apply Tendsto.atTop_mul_const (by positivity)
      exact tendsto_pow_atTop_atTop_of_one_lt hc1
    intro n hn
    replace hn := hn.out
    unfold f A g at *
    push_cast at *
    -- simple rewrite
    simp_rw [log_pow, pow_add] at *
    push_cast at *
    rw [EReal.coe_le_coe_iff, le_div_iff₀ <| sqrt_pos_of_pos <| by bound]
    refine (le_of_eq ?_).trans (hn.trans (le_of_eq ?_))
    · rw [← sqrt_mul (by bound), ← sqrt_mul' _ (by bound)]
      field_simp
    · field_simp
  apply ProbabilityTheory.measure_limsup_eq_one (by measurability)
  all_goals unfold A
  · -- show independence
    rw [iIndepSet_iff_iIndep]
    have h' := hX.hasIndepIncrements
    rw [hasIndepIncrements_iff_nat] at h'
    specialize h' (fun n ↦ c ^ n) _
    · apply pow_right_monotone <| le_of_lt <| by exact_mod_cast hc1
    rw [iIndepFun_iff_iIndep] at h'
    apply iIndep_of_iIndep_of_le h' fun n ↦ ?_
    apply MeasurableSpace.generateFrom_singleton_le <| measurableSet_le (by measurability) _
    apply Measurable.of_comap_le (by rfl)
  -- convert to sum of reals
  conv in P _ => rw [← ofReal_measureReal]
  simp_rw [← ENNReal.ofNNReal_toNNReal, ENNReal.tsum_coe_eq_top_iff_not_summable_coe,
    coe_toNNReal (r := P.real _) (by positivity)]
  -- rewrite in terms of standard Gaussian
  suffices h : ¬(Summable (fun n ↦ P.real {ω | g n ≤ X 1 ω})) by
    rw [← summable_nat_add_iff 1 (G := ℝ)] at h
    refine fun h' ↦ h (h'.congr fun n ↦ ?_)
    -- remove .real
    simp_rw [Measure.real_def]
    rw [ENNReal.toReal_eq_toReal_iff' (by finiteness) (by finiteness)]
    have h_idd : IdentDistrib
        (fun ω ↦ X (c ^ (n + 1)) ω - X (c ^ n) ω)
        (fun ω ↦ sqrt (c ^ (n + 1) - c ^ n) * X 1 ω) P P := by
      apply (hX.hasLaw_sub _ _).identDistrib
      convert gaussianReal_const_mul (hX.hasLaw_eval 1) _ using 2
      · norm_num
      rw [NNReal.eq_iff]
      have h_le : (c : ℝ) ^ n ≤ c ^ (n + 1) := by bound
      simp [Real.dist_eq, abs_of_nonneg (sub_nonneg.2 h_le), sq_sqrt (sub_nonneg.2 h_le)]
    -- use identical distribution to show probabilites are equal
    convert h_idd.measure_mem_eq
      (s := {x | sqrt (c ^ (n + 1) - c ^ n) * g (n + 1) ≤ (x : ℝ)}) _
    · rfl
    · simp_rw [Set.preimage_ofPred_eq]
      rw [← mul_le_mul_iff_of_pos_left _]
      rw [sqrt_pos, sub_pos, pow_add]
      apply lt_mul_of_one_lt_right (by positivity) (by bound)
    · measurability
  -- apply limit comparison test
  rw [Asymptotics.IsEquivalent.summable_iff_nat
      (g := fun n ↦ (1 / (g n)) * ((1 / n) * (1 / log c)))]; swap
  · -- show asymptotic equivalence
    apply ((IsStandardGaussian.tail <| hX.hasLaw_eval 1).comp_tendsto _).trans_eventuallyEq
    · unfold g
      simp_rw [Function.comp_def]
      filter_upwards [eventually_ge_atTop 1] with n hn; congr 1
      rw [log_pow, sq_sqrt (by bound)]
      field_simp
      rw [exp_neg, exp_log (by positivity)]
      field_simp
    · apply tendsto_sqrt_atTop.comp
      apply Tendsto.const_mul_atTop (by norm_num)
      repeat apply tendsto_log_atTop.comp
      apply tendsto_pow_atTop_atTop_of_one_lt hc1
  -- show non-summability of elementary series
  -- get rid of constant
  simp_rw [← mul_assoc]
  rw [summable_mul_right_iff (by positivity)]
  -- apply Cauchy condensation test
  rw [← summable_condensed_iff_of_eventually_nonneg]
  rotate_left
  · exact Eventually.of_forall (fun _ ↦ by positivity)
  · -- antitone side condition
    filter_upwards [eventually_gt_atTop 1] with n hn1
    apply mul_le_mul _ (by bound) (by positivity) (by positivity)
    unfold g
    simp_rw [log_pow]
    repeat rw [log_mul (by positivity) (by positivity)]
    gcongr
    lia
  unfold g
  push_cast
  field_simp
  -- apply limit comparison test again
  rw [Asymptotics.IsEquivalent.summable_iff_nat
    (g := fun k : ℕ ↦ 1 / √(2 * log 2) * (1 / √k))]
  · -- non-summability of p-series
    rw [summable_mul_left_iff (by positivity)]
    simp_rw [sqrt_eq_rpow]
    rw [summable_one_div_nat_rpow]
    norm_num
  -- asymptotic equivalence
  simp_rw [one_div_mul_one_div, log_pow]
  apply Asymptotics.IsEquivalent.div (by rfl)
  apply Asymptotics.isEquivalent_of_tendsto_one
  rw [Pi.div_def]
  conv in _ / _ => rw [← sqrt_mul (by positivity), ← sqrt_div (by bound),
    log_mul (by positivity) (by positivity)]
  push_cast
  simp_rw [log_pow]
  ring_nf
  simp_rw [(by simp : nhds 1 = nhds (sqrt (1 + 0)))]
  apply Tendsto.sqrt
  apply Tendsto.add
  · apply Tendsto.congr' (f₁ := fun x ↦ 1) _ (by aesop)
    filter_upwards [eventually_gt_atTop 0] with n hn using by field_simp
  · field_simp
    apply Tendsto.const_div_atTop
    rw [tendsto_mul_const_atTop_iff_pos (tendsto_natCast_atTop_atTop)]
    positivity

/-- **Law of the iterated logarithm** for Brownian motion. -/
theorem IsBrownianReal.ae_limsup_div_sqrt_log_log_eq_one (hX : IsBrownianReal X P) :
    ∀ᵐ ω ∂P, limsup (fun t ↦ (X t ω) / √(2 * t * log (log t)) : ℝ≥0 → EReal) atTop = 1 := by
  have := (hX.hasLaw ∅).isProbabilityMeasure
  have h_up := IsBrownianReal.ae_limsup_div_sqrt_log_log_le_one hX.isBrownianReal_mk
  have h_low := IsBrownianReal.ae_one_le_limsup_div_sqrt_log_log hX.isBrownianReal_mk
    hX.measurable_mk
  have h_ae := hX.mk_ae_forall_eq
  filter_upwards [h_up, h_low, h_ae] with ω hω_up hω_low hω_ae
  convert eq_of_le_of_ge hω_up hω_low
  simp_rw [hω_ae]
  rfl

end ProbabilityTheory
