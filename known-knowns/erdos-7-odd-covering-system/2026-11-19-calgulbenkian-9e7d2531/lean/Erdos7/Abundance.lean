/-
The counting half of Lemma 1: a family of boxes with distinct non-zero exponent vectors that covers
the product of the cells forces the profile to be abundant, `2 * val ≤ σ(val)`.
-/
import Erdos7.Defs

namespace Erdos7

theorem valFrom_eq_prod (es : List ℕ) : ∀ i, valFrom i es =
    ∏ k ∈ Finset.range es.length, oddP (i + k) ^ es.getD k 0 := by
  induction es with
  | nil => intro i; simp [valFrom]
  | cons e es ih =>
    intro i
    rw [valFrom, ih, List.length_cons, Finset.prod_range_succ']
    simp only [List.getD_cons_succ, List.getD_cons_zero, Nat.add_zero]
    rw [mul_comm]
    congr 1
    apply Finset.prod_congr rfl
    intro k _
    congr 2
    omega

theorem sigFrom_eq_prod (es : List ℕ) : ∀ i, sigFrom i es =
    ∏ k ∈ Finset.range es.length, geom (oddP (i + k)) (es.getD k 0 + 1) := by
  induction es with
  | nil => intro i; simp [sigFrom]
  | cons e es ih =>
    intro i
    rw [sigFrom, ih, List.length_cons, Finset.prod_range_succ']
    simp only [List.getD_cons_succ, List.getD_cons_zero, Nat.add_zero]
    rw [mul_comm]
    congr 1
    apply Finset.prod_congr rfl
    intro k _
    congr 2
    omega

theorem geom_eq_sum (p : ℕ) : ∀ e, geom p e = ∑ k ∈ Finset.range e, p ^ k := by
  intro e
  induction e with
  | zero => simp [geom]
  | succ e ih =>
    rw [geom, ih, Finset.sum_range_succ', Finset.mul_sum]
    simp [pow_succ']

theorem geom_succ_eq_sum_sub (p e : ℕ) :
    geom p (e + 1) = ∑ t ∈ Finset.range (e + 1), p ^ (e - t) := by
  rw [geom_eq_sum, ← Finset.sum_range_reflect]
  apply Finset.sum_congr rfl
  intro t ht
  rw [Finset.mem_range] at ht
  congr 1

theorem box_cover_abundant (es : List ℕ) {ι : Type} [DecidableEq ι] (J : Finset ι)
    (lev : ι → ℕ → ℕ) (side : ι → (m : ℕ) → Finset (Cell es m))
    (hlev0 : ∀ j ∈ J, ∀ m, es.length ≤ m → lev j m = 0)
    (hlevle : ∀ j ∈ J, ∀ m, lev j m ≤ es.getD m 0)
    (hnz : ∀ j ∈ J, ∃ m, lev j m ≠ 0)
    (hinj : ∀ j ∈ J, ∀ j' ∈ J, lev j = lev j' → j = j')
    (hsize : ∀ j ∈ J, ∀ m, m < es.length →
      (side j m).card * oddP m ^ lev j m ≤ oddP m ^ es.getD m 0)
    (hpos : ∀ m, m < es.length → 0 < oddP m)
    (hcover : ∀ x : (m : ℕ) → Cell es m, ∃ j ∈ J, ∀ m, m < es.length → lev j m ≠ 0 → x m ∈ side j m) :
    2 * valFrom 0 es ≤ sigFrom 0 es := by
  classical
  set r := es.length with hr
  -- positivity of every cell size, hence a default point
  have hcell : ∀ m, 0 < oddP m ^ es.getD m 0 := by
    intro m
    by_cases h : m < r
    · exact pow_pos (hpos m h) _
    · have : es.getD m 0 = 0 := by
        rw [List.getD_eq_getElem?_getD, List.getElem?_eq_none (by omega)]; rfl
      rw [this]; simp
  let d : (m : ℕ) → Cell es m := fun m => ⟨0, hcell m⟩
  -- the boxes on the first `r` coordinates
  let box : ι → Finset ((m : Fin r) → Cell es m) := fun j =>
    Fintype.piFinset (fun m : Fin r => if lev j m = 0 then Finset.univ else side j m)
  have hsub : (Finset.univ : Finset ((m : Fin r) → Cell es m)) ⊆ J.biUnion box := by
    intro y _
    obtain ⟨j, hj, hjx⟩ := hcover (fun m => if h : m < r then y ⟨m, h⟩ else d m)
    rw [Finset.mem_biUnion]
    refine ⟨j, hj, ?_⟩
    rw [Fintype.mem_piFinset]
    intro m
    by_cases h0 : lev j m = 0
    · simp [h0]
    · have := hjx m m.isLt h0
      simp only [m.isLt, ↓reduceDIte] at this
      simpa [h0] using this
  -- size of the whole space
  have hcardU : (Finset.univ : Finset ((m : Fin r) → Cell es m)).card = valFrom 0 es := by
    rw [Finset.card_univ, Fintype.card_pi, valFrom_eq_prod]
    simp only [Fintype.card_fin, Nat.zero_add]
    rw [← hr, Fin.prod_univ_eq_prod_range (fun m => oddP m ^ es.getD m 0) r]
  -- size of a box
  let g : ((m : Fin r) → ℕ) → ℕ := fun τ => ∏ m : Fin r, oddP m ^ (es.getD m 0 - τ m)
  have hbox : ∀ j ∈ J, (box j).card ≤ g (fun m => lev j m) := by
    intro j hj
    rw [Fintype.card_piFinset]
    apply Finset.prod_le_prod
    intro m _
    by_cases h0 : lev j m = 0
    · simp [h0]
    · simp only [h0, ↓reduceIte]
      have h1 := hsize j hj m m.isLt
      have h2 : oddP m ^ es.getD m 0 = oddP m ^ (es.getD m 0 - lev j m) * oddP m ^ lev j m := by
        rw [← pow_add, Nat.sub_add_cancel (hlevle j hj m)]
      rw [h2] at h1
      exact Nat.le_of_mul_le_mul_right h1 (pow_pos (hpos m m.isLt) _)
  -- all exponent vectors
  let V : Finset ((m : Fin r) → ℕ) :=
    Fintype.piFinset (fun m : Fin r => Finset.range (es.getD m 0 + 1))
  have hV : ∑ τ ∈ V, g τ = sigFrom 0 es := by
    rw [sigFrom_eq_prod]
    simp only [Nat.zero_add]
    rw [← hr, ← Fin.prod_univ_eq_prod_range (fun m => geom (oddP m) (es.getD m 0 + 1)) r]
    simp only [geom_succ_eq_sum_sub]
    rw [Finset.prod_univ_sum]
  have h0V : (0 : (m : Fin r) → ℕ) ∈ V := by
    rw [Fintype.mem_piFinset]; intro m; simp
  have hg0 : g 0 = valFrom 0 es := by
    rw [valFrom_eq_prod]
    simp only [Nat.zero_add, g, Pi.zero_apply, Nat.sub_zero]
    rw [← hr, Fin.prod_univ_eq_prod_range (fun m => oddP m ^ es.getD m 0) r]
  let vec : ι → ((m : Fin r) → ℕ) := fun j m => lev j m
  have hvinj : Set.InjOn vec (J : Set ι) := by
    intro j hj j' hj' h
    apply hinj j hj j' hj'
    funext m
    by_cases hm : m < r
    · exact congrFun h ⟨m, hm⟩
    · rw [hlev0 j hj m (by omega), hlev0 j' hj' m (by omega)]
  have himg : J.image vec ⊆ V.erase 0 := by
    intro τ hτ
    rw [Finset.mem_image] at hτ
    obtain ⟨j, hj, rfl⟩ := hτ
    rw [Finset.mem_erase]
    constructor
    · intro h
      obtain ⟨m, hm⟩ := hnz j hj
      by_cases hmr : m < r
      · exact hm (congrFun h ⟨m, hmr⟩)
      · exact hm (hlev0 j hj m (by omega))
    · rw [Fintype.mem_piFinset]
      intro m
      rw [Finset.mem_range]
      have := hlevle j hj m
      show lev j m < _
      omega
  have hsum : ∑ j ∈ J, g (vec j) ≤ ∑ τ ∈ V.erase 0, g τ := by
    rw [← Finset.sum_image hvinj]
    exact Finset.sum_le_sum_of_subset himg
  have hmain : valFrom 0 es ≤ ∑ τ ∈ V.erase 0, g τ := by
    calc valFrom 0 es = (Finset.univ : Finset ((m : Fin r) → Cell es m)).card := hcardU.symm
      _ ≤ (J.biUnion box).card := Finset.card_le_card hsub
      _ ≤ ∑ j ∈ J, (box j).card := Finset.card_biUnion_le
      _ ≤ ∑ j ∈ J, g (vec j) := Finset.sum_le_sum hbox
      _ ≤ _ := hsum
  have hsplit := Finset.add_sum_erase V g h0V
  rw [hV, hg0] at hsplit
  omega

end Erdos7
