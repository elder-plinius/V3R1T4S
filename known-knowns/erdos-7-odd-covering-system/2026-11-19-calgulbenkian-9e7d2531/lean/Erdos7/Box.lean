/-
Stage 4 core: the box theorem.  A family of "boxes" indexed by distinct exponent vectors, whose
side on coordinate `m` has at most `p_m^(e_m - t_m)` points, cannot cover the product of the
coordinate spaces when the profile passes the certificate check.

Proof: `check_sound` (the check means the rational bound is `< 1`), `fibre_kernel` (Lemma 4)
for every fibre, and `abstract_no_cover` (Lemma 5 iterated plus counting).
-/
import Erdos7.Defs
import Erdos7.Abstract
import Erdos7.Fibre

namespace Erdos7
open Finset
open scoped Classical

/-- Turn a nested prefix into a function of the coordinate index (default `d` beyond the prefix). -/
def Space.toFun {X : ℕ → Type} (d : ∀ m, X m) : ∀ i, Space X i → ∀ m, X m
  | 0, _ => d
  | i + 1, y => Function.update (Space.toFun d i y.1) i y.2

lemma inBox_of_toFun {X : ℕ → Type} (d : ∀ m, X m) (side : ∀ m, Finset (X m)) :
    ∀ (i : ℕ) (y : Space X i), (∀ m, m < i → Space.toFun d i y m ∈ side m) → InBox side i y
  | 0, _, _ => trivial
  | i + 1, y, h => by
    refine ⟨inBox_of_toFun d side i y.1 (fun m hm => ?_), ?_⟩
    · have := h m (Nat.lt_succ_of_lt hm)
      simpa [Space.toFun, Function.update_of_ne (Nat.ne_of_lt hm)] using this
    · have := h i (Nat.lt_succ_self i)
      simpa [Space.toFun] using this

/-- Sides are irrelevant on coordinates where the exponent is `0`: replace them by everything. -/
noncomputable def relax {X : ℕ → Type} [∀ m, Fintype (X m)] {ι : Type} (lev : ι → ℕ → ℕ)
    (side : ι → ∀ m, Finset (X m)) : ι → ∀ m, Finset (X m) :=
  fun j m => if lev j m = 0 then univ else side j m

lemma Pset_card_le {X : ℕ → Type} [∀ m, Fintype (X m)] {ι : Type} (J : Finset ι)
    (lev : ι → ℕ → ℕ) (side : ι → ∀ m, Finset (X m)) (i : ℕ) :
    (Pset J lev side i).card ≤ ∑ j ∈ J.filter (fun j => IsPureAt lev j i), (side j i).card :=
  card_biUnion_le

lemma den_pos_zero (p cap : ℕ) : 0 < den p 0 cap := by
  unfold den; split_ifs <;> simp [geom]

theorem box_no_cover (es caps : List ℕ) (hchk : checkEntry (es, caps) = true)
    {ι : Type} [DecidableEq ι] (J : Finset ι) (lev : ι → ℕ → ℕ)
    (side : ι → (m : ℕ) → Finset (Cell es m))
    (hlev0 : ∀ j ∈ J, ∀ m, es.length ≤ m → lev j m = 0)
    (hlevle : ∀ j ∈ J, ∀ m, lev j m ≤ es.getD m 0)
    (hnz : ∀ j ∈ J, ∃ m, lev j m ≠ 0)
    (hinj : ∀ j ∈ J, ∀ j' ∈ J, lev j = lev j' → j = j')
    (hsize : ∀ j ∈ J, ∀ m, m < es.length →
      (side j m).card * oddP m ^ lev j m ≤ oddP m ^ es.getD m 0) :
    ∃ x : (m : ℕ) → Cell es m, ∀ j ∈ J, ∃ m, m < es.length ∧ lev j m ≠ 0 ∧ x m ∉ side j m := by
  obtain ⟨hOK, hspec⟩ := check_sound es caps hchk
  have hE0 : ∀ m, es.length ≤ m → es.getD m 0 = 0 := fun m hm => List.getD_eq_default _ _ hm
  have hp3 : ∀ m, m < es.length → 3 ≤ oddP m := fun m hm => (coordOK_spec (hOK m hm)).1
  have hden : ∀ m, 0 < den (oddP m) (es.getD m 0) (caps.getD m 0) := by
    intro m
    by_cases hm : m < es.length
    · exact (coordOK_spec (hOK m hm)).2.2.1
    · rw [hE0 m (not_lt.1 hm)]; exact den_pos_zero _ _
  have hcardX : ∀ m, Fintype.card (Cell es m) = oddP m ^ es.getD m 0 := fun m => Fintype.card_fin _
  have hr0 : ∀ j m, lev j m = 0 → relax lev side j m = univ := fun j m h => by simp [relax, h]
  have hr1 : ∀ j m, lev j m ≠ 0 → relax lev side j m = side j m := fun j m h => by simp [relax, h]
  -- sizes of the relaxed sides
  have hsz : ∀ j ∈ J, ∀ m, m < es.length →
      (relax lev side j m).card * oddP m ^ lev j m ≤ oddP m ^ es.getD m 0 := by
    intro j hj m hm
    by_cases h : lev j m = 0
    · rw [hr0 j m h, h, card_univ, hcardX]; simp
    · rw [hr1 j m h]; exact hsize j hj m hm
  have hsc : ∀ j ∈ J, ∀ m, m < es.length →
      (relax lev side j m).card ≤ oddP m ^ (es.getD m 0 - lev j m) := by
    intro j hj m hm
    have h := hsz j hj m hm
    have hle := hlevle j hj m
    have : oddP m ^ es.getD m 0 = oddP m ^ (es.getD m 0 - lev j m) * oddP m ^ lev j m := by
      rw [← pow_add]; congr 1; omega
    rw [this] at h
    exact Nat.le_of_mul_le_mul_right h (Nat.pow_pos (by have := hp3 m hm; omega))
  -- the pure part of each coordinate is small
  have hPcard : ∀ i, i < es.length →
      (Pset J lev (relax lev side) i).card ≤ geom (oddP i) (es.getD i 0) := by
    intro i hi
    set F := J.filter (fun j => IsPureAt lev j i) with hF
    have hFJ : ∀ j ∈ F, j ∈ J := fun j hj => (mem_filter.1 hj).1
    have hinjF : Set.InjOn (fun j => lev j i) (F : Set ι) := by
      intro a ha b hb hab
      have ha' := mem_filter.1 (mem_coe.1 ha)
      have hb' := mem_filter.1 (mem_coe.1 hb)
      refine hinj a ha'.1 b hb'.1 (funext fun m => ?_)
      by_cases hm : m = i
      · rw [hm]; exact hab
      · rw [ha'.2.2 m hm, hb'.2.2 m hm]
    calc (Pset J lev (relax lev side) i).card
        ≤ ∑ j ∈ F, (relax lev side j i).card := Pset_card_le J lev _ i
      _ ≤ ∑ j ∈ F, oddP i ^ (es.getD i 0 - lev j i) :=
          sum_le_sum fun j hj => hsc j (hFJ j hj) i hi
      _ = ∑ t ∈ F.image (fun j => lev j i), oddP i ^ (es.getD i 0 - t) :=
          (sum_image (f := fun t => oddP i ^ (es.getD i 0 - t)) hinjF).symm
      _ ≤ ∑ t ∈ Icc 1 (es.getD i 0), oddP i ^ (es.getD i 0 - t) := by
          refine sum_le_sum_of_subset ?_
          intro t ht
          obtain ⟨j, hj, rfl⟩ := mem_image.1 ht
          have hj' := mem_filter.1 hj
          exact mem_Icc.2 ⟨Nat.one_le_iff_ne_zero.2 hj'.2.1, hlevle j hj'.1 i⟩
      _ = geom (oddP i) (es.getD i 0) := sum_Icc_pow _ _
  -- the fibre kernels (Lemma 4)
  have hex : ∀ (i : ℕ) (y : Space (Cell es) i), ∃ k : Cell es i → ℚ,
      (∀ x, 0 ≤ k x) ∧ ∑ x, k x = 1 ∧ (i < es.length →
        (∀ x ∈ Pset J lev (relax lev side) i, k x = 0) ∧
        (∀ j ∈ J, ∑ x ∈ relax lev side j i, k x
          ≤ Qr (oddP i) (es.getD i 0) (caps.getD i 0) (lev j i)) ∧
        ∑ x ∈ Bset J lev (relax lev side) i y, k x ≤
          fS (oddP i) (es.getD i 0) (caps.getD i 0) (∑ j ∈ Jtop J lev i,
            if InBox (relax lev side j) i y
              then ωS (oddP i) (es.getD i 0) (caps.getD i 0) (lev j i) else 0)) := by
    intro i y
    by_cases hi : i < es.length
    · obtain ⟨k, hk0, hk1, hkP, hkS, hkB⟩ := fibre_kernel (α := Cell es i) (oddP i)
        (es.getD i 0) (caps.getD i 0) (hOK i hi) (hcardX i) (Pset J lev (relax lev side) i)
        (hPcard i hi) ((Jtop J lev i).filter (fun j => InBox (relax lev side j) i y))
        (fun j => lev j i) (fun j => relax lev side j i)
        (fun j hj => by
          have hj' := mem_filter.1 (mem_filter.1 hj).1
          exact ⟨Nat.one_le_iff_ne_zero.2 hj'.2.1, hlevle j hj'.1 i⟩)
        (fun j hj => hsc j (mem_filter.1 (mem_filter.1 hj).1).1 i hi)
      refine ⟨k, hk0, hk1, fun _ => ⟨hkP, fun j hj => ?_, ?_⟩⟩
      · exact hkS _ _ (hlevle j hj i) (hsz j hj i hi)
      · rw [sum_filter] at hkB
        exact hkB
    · refine ⟨fun _ => 1, fun _ => zero_le_one, ?_, fun h => absurd h hi⟩
      rw [sum_const, card_univ, hcardX, hE0 i (not_lt.1 hi)]; simp
  choose κ hκ0 hκ1 hκ using hex
  -- the bound
  have hbound : ∑ i ∈ range es.length,
      ET (fun m => es.getD m 0)
        (fun m t => Qr (oddP m) (es.getD m 0) (caps.getD m 0) t
          - Qr (oddP m) (es.getD m 0) (caps.getD m 0) (t + 1)) i
        (fun T => fS (oddP i) (es.getD i 0) (caps.getD i 0)
          ((∑ t ∈ Icc 1 (es.getD i 0), ωS (oddP i) (es.getD i 0) (caps.getD i 0) t)
            * ((mult i T : ℚ) - 1))) < 1 := by
    have : ∑ i ∈ range es.length,
        ET (fun m => es.getD m 0)
          (fun m t => Qr (oddP m) (es.getD m 0) (caps.getD m 0) t
            - Qr (oddP m) (es.getD m 0) (caps.getD m 0) (t + 1)) i
          (fun T => fS (oddP i) (es.getD i 0) (caps.getD i 0)
            ((∑ t ∈ Icc 1 (es.getD i 0), ωS (oddP i) (es.getD i 0) (caps.getD i 0) t)
              * ((mult i T : ℚ) - 1))) = specBound es caps := by
      unfold specBound stageQ
      refine sum_congr rfl fun i hi => ?_
      congr 1
      funext T
      exact stage_eq (hOK i (mem_range.1 hi)) (mult_pos i T)
    rw [this]; exact hspec
  obtain ⟨y, hy⟩ := abstract_no_cover J lev (relax lev side) κ es.length (fun m => es.getD m 0)
    hκ0 hκ1 (fun m t => Qr (oddP m) (es.getD m 0) (caps.getD m 0) t)
    (fun m => Qr_zero (hden m)) (fun m => Qr_succ_top _ _ _)
    (by
      intro m t ht
      by_cases hm : m < es.length
      · have hanti := (coordOK_spec (hOK m hm)).2.2.2.1 t ht
        have hd : (0:ℚ) < (den (oddP m) (es.getD m 0) (caps.getD m 0) : ℚ) := by
          exact_mod_cast hden m
        unfold Qr
        apply div_le_div_of_nonneg_right _ hd.le
        exact_mod_cast hanti
      · have h0 := hE0 m (not_lt.1 hm)
        have ht0 : t = es.getD m 0 := by omega
        rw [ht0, Qr_succ_top]; exact Qr_nonneg _ _ _ _)
    (fun i => fS (oddP i) (es.getD i 0) (caps.getD i 0))
    (fun i _ => fS_convex _ _ _) (fun i _ => fS_mono _ _ _)
    (fun i t => ωS (oddP i) (es.getD i 0) (caps.getD i 0) t) (fun i t => ωS_nonneg _ _ _ _)
    hlev0 hlevle hnz hinj
    (fun i hi y => (hκ i y hi).1) (fun i hi y => (hκ i y hi).2.1) (fun i hi y => (hκ i y hi).2.2)
    hbound
  -- read off the uncovered point
  have hpos : ∀ m, 0 < oddP m ^ es.getD m 0 := by
    intro m
    by_cases hm : m < es.length
    · exact Nat.pow_pos (by have := hp3 m hm; omega)
    · rw [hE0 m (not_lt.1 hm)]; simp
  obtain ⟨d⟩ : Nonempty (∀ m, Cell es m) := ⟨fun m => ⟨0, hpos m⟩⟩
  refine ⟨Space.toFun d es.length y, fun j hj => ?_⟩
  by_contra hcon
  push Not at hcon
  refine hy j hj (inBox_of_toFun d (relax lev side j) es.length y fun m hm => ?_)
  by_cases h : lev j m = 0
  · rw [hr0 j m h]; exact mem_univ _
  · rw [hr1 j m h]; exact hcon m hm h

end Erdos7
