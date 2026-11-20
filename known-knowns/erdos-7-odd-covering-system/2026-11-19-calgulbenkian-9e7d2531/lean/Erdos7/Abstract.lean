/-
Stage 4: the abstract non-covering theorem for boxes with distinct exponent vectors,
given fibre kernels with the properties established in Lemma 4.
-/
import Erdos7.Sequential

namespace Erdos7
open Finset
open scoped Classical

section counting
variable {e : ℕ → ℕ} {β : Type}

/-- Vectors that are pairwise distinct on the first `i` coordinates: at most `mult i T` of them
lie below `T`. -/
lemma card_le_mult (v : β → ℕ → ℕ) : ∀ (i : ℕ) (T : TVec e i) (K : Finset β),
    (∀ a ∈ K, ∀ b ∈ K, (∀ m, m < i → v a m = v b m) → a = b) →
    (K.filter (fun a => LeT (v a) i T)).card ≤ mult i T := by
  intro i
  induction i with
  | zero =>
    intro T K hK
    refine (card_le_card (filter_subset _ _)).trans ?_
    exact card_le_one.2 fun a ha b hb => hK a ha b hb (fun m hm => absurd hm (Nat.not_lt_zero m))
  | succ i ih =>
    intro T K hK
    set F := K.filter (fun a => LeT (v a) (i + 1) T) with hF
    have hmaps : ∀ a ∈ F, v a i ∈ range (T.2.val + 1) := by
      intro a ha
      have := (mem_filter.1 ha).2
      exact mem_range.2 (Nat.lt_succ_of_le this.2)
    rw [card_eq_sum_card_fiberwise hmaps]
    have hfib : ∀ s ∈ range (T.2.val + 1), (F.filter (fun a => v a i = s)).card ≤ mult i T.1 := by
      intro s _
      refine le_trans (card_le_card ?_) (ih T.1 (K.filter (fun a => v a i = s)) ?_)
      · intro a ha
        simp only [hF, mem_filter] at ha ⊢
        exact ⟨⟨ha.1.1, ha.2⟩, ha.1.2.1⟩
      · intro a ha b hb hab
        simp only [mem_filter] at ha hb
        refine hK a ha.1 b hb.1 fun m hm => ?_
        rcases Nat.lt_succ_iff_lt_or_eq.1 hm with h | h
        · exact hab m h
        · rw [h, ha.2, hb.2]
    calc ∑ s ∈ range (T.2.val + 1), (F.filter (fun a => v a i = s)).card
        ≤ ∑ _s ∈ range (T.2.val + 1), mult i T.1 := sum_le_sum hfib
      _ = mult (i + 1) T := by simp [mult]; ring

/-- If moreover every vector is nonzero on the first `i` coordinates, the zero vector is missed. -/
lemma card_lt_mult (v : β → ℕ → ℕ) : ∀ (i : ℕ) (T : TVec e i) (K : Finset β),
    (∀ a ∈ K, ∀ b ∈ K, (∀ m, m < i → v a m = v b m) → a = b) →
    (∀ a ∈ K, ∃ m, m < i ∧ v a m ≠ 0) →
    (K.filter (fun a => LeT (v a) i T)).card + 1 ≤ mult i T := by
  intro i
  induction i with
  | zero =>
    intro T K _ hnz
    have : K = ∅ := by
      refine eq_empty_of_forall_notMem fun a ha => ?_
      obtain ⟨m, hm, _⟩ := hnz a ha
      exact Nat.not_lt_zero m hm
    simp [this, mult]
  | succ i ih =>
    intro T K hK hnz
    set F := K.filter (fun a => LeT (v a) (i + 1) T) with hF
    have hmaps : ∀ a ∈ F, v a i ∈ range (T.2.val + 1) := by
      intro a ha
      have := (mem_filter.1 ha).2
      exact mem_range.2 (Nat.lt_succ_of_le this.2)
    have hinjs : ∀ s, ∀ a ∈ K.filter (fun a => v a i = s), ∀ b ∈ K.filter (fun a => v a i = s),
        (∀ m, m < i → v a m = v b m) → a = b := by
      intro s a ha b hb hab
      simp only [mem_filter] at ha hb
      refine hK a ha.1 b hb.1 fun m hm => ?_
      rcases Nat.lt_succ_iff_lt_or_eq.1 hm with h | h
      · exact hab m h
      · rw [h, ha.2, hb.2]
    have hsub : ∀ s, F.filter (fun a => v a i = s)
        ⊆ (K.filter (fun a => v a i = s)).filter (fun a => LeT (v a) i T.1) := by
      intro s a ha
      simp only [hF, mem_filter] at ha ⊢
      exact ⟨⟨ha.1.1, ha.2⟩, ha.1.2.1⟩
    have h0 : (F.filter (fun a => v a i = 0)).card + 1 ≤ mult i T.1 := by
      refine le_trans (Nat.succ_le_succ (card_le_card (hsub 0))) (ih T.1 _ (hinjs 0) ?_)
      intro a ha
      simp only [mem_filter] at ha
      obtain ⟨m, hm, hne⟩ := hnz a ha.1
      rcases Nat.lt_succ_iff_lt_or_eq.1 hm with h | h
      · exact ⟨m, h, hne⟩
      · exact absurd (h ▸ ha.2) hne
    have hs : ∀ s ∈ range T.2.val, (F.filter (fun a => v a i = s + 1)).card ≤ mult i T.1 :=
      fun s _ => le_trans (card_le_card (hsub (s + 1))) (card_le_mult v i T.1 _ (hinjs (s + 1)))
    rw [card_eq_sum_card_fiberwise hmaps, sum_range_succ']
    calc ∑ s ∈ range T.2.val, (F.filter (fun a => v a i = s + 1)).card
          + (F.filter (fun a => v a i = 0)).card + 1
        ≤ ∑ _s ∈ range T.2.val, mult i T.1 + mult i T.1 := by
          have := sum_le_sum hs; omega
      _ = mult (i + 1) T := by simp [mult]; ring

end counting

section abstract
variable {X : ℕ → Type} [∀ m, Fintype (X m)]
variable {ι : Type} (J : Finset ι) (lev : ι → ℕ → ℕ) (side : ι → ∀ m, Finset (X m))

/-- The class `j` is a pure power of the `i`-th prime. -/
def IsPureAt (j : ι) (i : ℕ) : Prop := lev j i ≠ 0 ∧ ∀ m, m ≠ i → lev j m = 0

/-- The class `j` is mixed (at least two primes) and its largest prime is the `i`-th. -/
def IsTopMixed (j : ι) (i : ℕ) : Prop :=
  lev j i ≠ 0 ∧ (∀ m, i < m → lev j m = 0) ∧ ∃ m, m < i ∧ lev j m ≠ 0

/-- Union of the pure prime-power classes on coordinate `i`. -/
noncomputable def Pset (i : ℕ) : Finset (X i) :=
  (J.filter (fun j => IsPureAt lev j i)).biUnion (fun j => side j i)

/-- Mixed classes with top coordinate `i`. -/
noncomputable def Jtop (i : ℕ) : Finset ι := J.filter (fun j => IsTopMixed lev j i)

/-- The part of the `i`-th fibre over the prefix `y` covered by mixed classes with top `i`. -/
noncomputable def Bset (i : ℕ) (y : Space X i) : Finset (X i) :=
  ((Jtop J lev i).filter (fun j => InBox (side j) i y)).biUnion (fun j => side j i)

/-- A prefix is bad when some coordinate lies in the pure part or the mixed-covered part. -/
def Bad : ∀ i, Space X i → Prop
  | 0, _ => False
  | i + 1, y => Bad i y.1 ∨ y.2 ∈ Pset J lev side i ∪ Bset J lev side i y.1

lemma cover_bad (hnz : ∀ j ∈ J, ∃ m, lev j m ≠ 0) :
    ∀ (i : ℕ) (y : Space X i) (j : ι), j ∈ J → (∀ m, i ≤ m → lev j m = 0) →
      InBox (side j) i y → Bad J lev side i y := by
  intro i
  induction i with
  | zero =>
    intro y j hj h0 _
    obtain ⟨m, hm⟩ := hnz j hj
    exact absurd (h0 m (Nat.zero_le m)) hm
  | succ i ih =>
    intro y j hj h0 hin
    by_cases hi : lev j i = 0
    · left
      refine ih y.1 j hj (fun m hm => ?_) hin.1
      rcases Nat.eq_or_lt_of_le hm with h | h
      · rw [← h]; exact hi
      · exact h0 m h
    · right
      by_cases hmix : ∃ m, m < i ∧ lev j m ≠ 0
      · refine mem_union_right _ (mem_biUnion.2 ⟨j, ?_, hin.2⟩)
        exact mem_filter.2 ⟨mem_filter.2 ⟨hj, hi, fun m hm => h0 m hm, hmix⟩, hin.1⟩
      · refine mem_union_left _ (mem_biUnion.2 ⟨j, ?_, hin.2⟩)
        refine mem_filter.2 ⟨hj, hi, fun m hm => ?_⟩
        rcases lt_or_gt_of_ne hm with h | h
        · by_contra hne; exact hmix ⟨m, h, hne⟩
        · exact h0 m h

variable (κ : ∀ i, Space X i → X i → ℚ)

lemma Ex_bad (hκ0 : ∀ i y x, 0 ≤ κ i y x) (hκ1 : ∀ i y, ∑ x, κ i y x = 1) : ∀ i : ℕ,
    Ex κ i (fun y => if Bad J lev side i y then 1 else 0) ≤
      ∑ m ∈ range i, Ex κ m (fun y => ∑ x ∈ Pset J lev side m ∪ Bset J lev side m y, κ m y x) := by
  intro i
  induction i with
  | zero => simp [Ex, Bad]
  | succ i ih =>
    rw [sum_range_succ]
    have hpt : ∀ y : Space X i,
        ∑ x, κ i y x * (if Bad J lev side (i + 1) (y, x) then 1 else 0) ≤
          (if Bad J lev side i y then 1 else 0)
            + ∑ x ∈ Pset J lev side i ∪ Bset J lev side i y, κ i y x := by
      intro y
      have hnn : 0 ≤ ∑ x ∈ Pset J lev side i ∪ Bset J lev side i y, κ i y x :=
        sum_nonneg fun x _ => hκ0 i y x
      by_cases hb : Bad J lev side i y
      · have : ∀ x : X i, Bad J lev side (i + 1) (y, x) := fun x => Or.inl hb
        simp only [this, if_true, mul_one, hκ1, hb]
        linarith
      · have : ∀ x : X i, (if Bad J lev side (i + 1) (y, x) then (1:ℚ) else 0)
            = if x ∈ Pset J lev side i ∪ Bset J lev side i y then 1 else 0 := by
          intro x
          have : Bad J lev side (i + 1) (y, x) ↔ x ∈ Pset J lev side i ∪ Bset J lev side i y := by
            simp [Bad, hb]
          simp only [this]
        simp only [this, hb, if_false, zero_add, mul_ite, mul_one, mul_zero]
        rw [sum_ite_mem, univ_inter]
    calc Ex κ (i + 1) (fun y => if Bad J lev side (i + 1) y then 1 else 0)
        = Ex κ i (fun y => ∑ x, κ i y x * (if Bad J lev side (i + 1) (y, x) then 1 else 0)) := rfl
      _ ≤ Ex κ i (fun y => (if Bad J lev side i y then 1 else 0)
            + ∑ x ∈ Pset J lev side i ∪ Bset J lev side i y, κ i y x) := Ex_mono κ hκ0 i _ _ hpt
      _ = Ex κ i (fun y => if Bad J lev side i y then 1 else 0)
            + Ex κ i (fun y => ∑ x ∈ Pset J lev side i ∪ Bset J lev side i y, κ i y x) :=
          Ex_add κ i _ _
      _ ≤ _ := by linarith

/-- The counting step: mixed classes with top `i` below the level vector `T`. -/
lemma top_count (hinj : ∀ j ∈ J, ∀ j' ∈ J, lev j = lev j' → j = j')
    (e : ℕ → ℕ) (hlevle : ∀ j ∈ J, ∀ m, lev j m ≤ e m)
    (ω : ℕ → ℚ) (hω : ∀ t, 0 ≤ ω t) (i : ℕ) (T : TVec e i) :
    ∑ j ∈ Jtop J lev i, (if LeT (lev j) i T then ω (lev j i) else 0)
      ≤ (∑ t ∈ Icc 1 (e i), ω t) * ((mult i T : ℚ) - 1) := by
  have hmaps : ∀ j ∈ Jtop J lev i, lev j i ∈ Icc 1 (e i) := by
    intro j hj
    have hj' := mem_filter.1 hj
    exact mem_Icc.2 ⟨Nat.one_le_iff_ne_zero.2 hj'.2.1, hlevle j hj'.1 i⟩
  rw [← sum_fiberwise_of_maps_to hmaps, sum_mul]
  refine sum_le_sum fun t _ => ?_
  have hcard := card_lt_mult (e := e) lev i T ((Jtop J lev i).filter (fun j => lev j i = t))
    (by
      intro a ha b hb hab
      simp only [Jtop, mem_filter] at ha hb
      refine hinj a ha.1.1 b hb.1.1 (funext fun m => ?_)
      rcases lt_trichotomy m i with h | h | h
      · exact hab m h
      · rw [h, ha.2, hb.2]
      · rw [ha.1.2.2.1 m h, hb.1.2.2.1 m h])
    (by
      intro a ha
      simp only [Jtop, mem_filter] at ha
      exact ha.1.2.2.2)
  have hcard' : ((((Jtop J lev i).filter (fun j => lev j i = t)).filter
      (fun j => LeT (lev j) i T)).card : ℚ) ≤ (mult i T : ℚ) - 1 := by
    have : ((((Jtop J lev i).filter (fun j => lev j i = t)).filter
      (fun j => LeT (lev j) i T)).card : ℚ) + 1 ≤ (mult i T : ℚ) := by exact_mod_cast hcard
    linarith
  calc ∑ j ∈ (Jtop J lev i).filter (fun j => lev j i = t),
        (if LeT (lev j) i T then ω (lev j i) else 0)
      = ∑ j ∈ (Jtop J lev i).filter (fun j => lev j i = t),
        (if LeT (lev j) i T then ω t else 0) :=
        sum_congr rfl fun j hj => by rw [(mem_filter.1 hj).2]
    _ = ((((Jtop J lev i).filter (fun j => lev j i = t)).filter
          (fun j => LeT (lev j) i T)).card : ℚ) * ω t := by
        rw [← sum_filter, sum_const, nsmul_eq_mul]
    _ ≤ ((mult i T : ℚ) - 1) * ω t := mul_le_mul_of_nonneg_right hcard' (hω t)
    _ = ω t * ((mult i T : ℚ) - 1) := mul_comm _ _

/-- **Abstract non-covering theorem.**  Boxes with pairwise distinct nonzero exponent vectors
cannot cover the product space when there are fibre kernels `κ` vanishing on the pure parts
(`hK2`), giving every box side of level `t` weight at most `Q i t` (`hK3`), with mixed fibre loss
bounded by a convex increasing function of the weighted number of active classes (`hK4`), and
the resulting explicit bound is `< 1`. -/
theorem abstract_no_cover (r : ℕ) (e : ℕ → ℕ)
    (hκ0 : ∀ i y x, 0 ≤ κ i y x) (hκ1 : ∀ i y, ∑ x, κ i y x = 1)
    (Q : ℕ → ℕ → ℚ) (hQ0 : ∀ m, Q m 0 = 1) (hQe : ∀ m, Q m (e m + 1) = 0)
    (hQanti : ∀ m t, t ≤ e m → Q m (t + 1) ≤ Q m t)
    (f : ℕ → ℚ → ℚ) (hf : ∀ i, i < r → ConvexOn ℚ (Set.Ici 0) (f i))
    (hm : ∀ i, i < r → MonotoneOn (f i) (Set.Ici 0))
    (ω : ℕ → ℕ → ℚ) (hω : ∀ i t, 0 ≤ ω i t)
    (hlev0 : ∀ j ∈ J, ∀ m, r ≤ m → lev j m = 0)
    (hlevle : ∀ j ∈ J, ∀ m, lev j m ≤ e m)
    (hnz : ∀ j ∈ J, ∃ m, lev j m ≠ 0)
    (hinj : ∀ j ∈ J, ∀ j' ∈ J, lev j = lev j' → j = j')
    (hK2 : ∀ i, i < r → ∀ y, ∀ x ∈ Pset J lev side i, κ i y x = 0)
    (hK3 : ∀ i, i < r → ∀ y, ∀ j ∈ J, ∑ x ∈ side j i, κ i y x ≤ Q i (lev j i))
    (hK4 : ∀ i, i < r → ∀ y, ∑ x ∈ Bset J lev side i y, κ i y x ≤
      f i (∑ j ∈ Jtop J lev i, if InBox (side j) i y then ω i (lev j i) else 0))
    (hbound : ∑ i ∈ range r, ET e (fun m t => Q m t - Q m (t + 1)) i
      (fun T => f i ((∑ t ∈ Icc 1 (e i), ω i t) * ((mult i T : ℚ) - 1))) < 1) :
    ∃ y : Space X r, ∀ j ∈ J, ¬ InBox (side j) r y := by
  by_contra hcon
  push_neg at hcon
  have hbad : ∀ y : Space X r, Bad J lev side r y := fun y => by
    obtain ⟨j, hj, hin⟩ := hcon y
    exact cover_bad J lev side hnz r y j hj (hlev0 j hj) hin
  have h1 : Ex κ r (fun y => if Bad J lev side r y then 1 else 0) = 1 := by
    simp only [hbad, if_true]; exact Ex_const κ hκ1 r 1
  have h2 := Ex_bad J lev side κ hκ0 hκ1 r
  have hq0 : ∀ (i : ℕ) (y : TVec e i) (x : Fin (e i + 1)),
      0 ≤ (fun m (t : ℕ) => Q m t - Q m (t + 1)) i x.val := fun i _ x =>
    sub_nonneg.2 (hQanti i x.val (Nat.lt_succ_iff.1 x.isLt))
  have h3 : ∀ i ∈ range r,
      Ex κ i (fun y => ∑ x ∈ Pset J lev side i ∪ Bset J lev side i y, κ i y x) ≤
        ET e (fun m t => Q m t - Q m (t + 1)) i
          (fun T => f i ((∑ t ∈ Icc 1 (e i), ω i t) * ((mult i T : ℚ) - 1))) := by
    intro i hi
    have hir := mem_range.1 hi
    calc Ex κ i (fun y => ∑ x ∈ Pset J lev side i ∪ Bset J lev side i y, κ i y x)
        ≤ Ex κ i (fun y => f i (0 + ∑ j ∈ Jtop J lev i,
            if InBox (side j) i y then ω i (lev j i) else 0)) := by
          refine Ex_mono κ hκ0 i _ _ fun y => ?_
          rw [zero_add]
          refine le_trans ?_ (hK4 i hir y)
          rw [← union_sdiff_self_eq_union, sum_union disjoint_sdiff,
            sum_eq_zero (fun x hx => hK2 i hir y x hx), zero_add]
          exact sum_le_sum_of_subset_of_nonneg sdiff_subset (fun x _ _ => hκ0 i y x)
      _ ≤ ET e (fun m t => Q m t - Q m (t + 1)) i (fun T => f i (0 + ∑ j ∈ Jtop J lev i,
            if LeT (lev j) i T then ω i (lev j i) else 0)) := by
          classical
          exact comparison κ hκ0 hκ1 e Q hQ0 hQe hQanti (f i) (hf i hir) (hm i hir) lev side i
            (Jtop J lev i) (fun j => ω i (lev j i)) (fun j _ => hω i _) 0 le_rfl
            (fun j hj m _ => hlevle j (mem_filter.1 hj).1 m)
            (fun j hj m hm' y => hK3 m (hm'.trans hir) y j (mem_filter.1 hj).1)
      _ ≤ _ := by
          refine Ex_mono _ hq0 i _ _ fun T => ?_
          rw [zero_add]
          refine hm i hir ?_ ?_ (top_count J lev hinj e hlevle (ω i) (hω i) i T)
          · exact Set.mem_Ici.2 (sum_nonneg fun j _ => by
              split_ifs <;> [exact hω i _; exact le_rfl])
          · refine Set.mem_Ici.2 (mul_nonneg (sum_nonneg fun t _ => hω i t) ?_)
            have : (1:ℚ) ≤ (mult i T : ℚ) := by exact_mod_cast mult_pos i T
            linarith
  have h4 := sum_le_sum h3
  linarith

end abstract

end Erdos7
