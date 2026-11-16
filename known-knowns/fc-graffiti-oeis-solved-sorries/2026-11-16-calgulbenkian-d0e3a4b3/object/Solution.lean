/-
Copyright 2025 The Formal Conjectures Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-/

module

public import FormalConjecturesUtil

/-!
# Written on the Wall II - Conjecture 25

**Verbatim statement (WOWII #25, status F):**
> If G is a simple connected graph, then b(G) ≥ 2 CEIL[(1 + minimum of dist_even(v))/3]

**Source:** http://cms.uhd.edu/faculty/delavinae/research/wowII/all.html#conj25

The WOWII page records this conjecture as disproved (status F), with the same
counterexample as Conjecture 24.

*Reference:*
[E. DeLaVina, Written on the Wall II, Conjectures of Graffiti.pc](http://cms.dt.uh.edu/faculty/delavinae/research/wowII/)
-/

@[expose] public section

namespace WrittenOnTheWallII.GraphConjecture25

open SimpleGraph

/-- Recursive boolean check that `p k = true` for all `k < n`. -/
def allBelow (p : ℕ → Bool) : ℕ → Bool
  | 0 => true
  | n + 1 => p n && allBelow p n

@[category API, AMS 5]
lemma allBelow_sound (p : ℕ → Bool) (n : ℕ) (h : allBelow p n = true) :
    ∀ k < n, p k = true := by
  induction n with
  | zero =>
    intro k hk
    omega
  | succ n ih =>
    intro k hk
    simp only [allBelow, Bool.and_eq_true] at h
    rcases Nat.lt_succ_iff_lt_or_eq.mp hk with hlt | rfl
    · exact ih h.2 k hlt
    · exact h.1

/-- Structural list filter whose equation lemmas are exposed inside a module. -/
def filterList {α : Type*} (p : α → Bool) : List α → List α
  | [] => []
  | x :: xs => if p x then x :: filterList p xs else filterList p xs

@[category API, AMS 5]
lemma mem_filterList_iff {α : Type*} (p : α → Bool) (L : List α) (z : α) :
    z ∈ filterList p L ↔ z ∈ L ∧ p z = true := by
  induction L with
  | nil => simp [filterList]
  | cons x xs ih =>
    simp only [filterList]
    split_ifs with hpx
    · simp only [List.mem_cons, ih]
      constructor
      · rintro (rfl | ⟨hm, hp⟩)
        · exact ⟨Or.inl rfl, hpx⟩
        · exact ⟨Or.inr hm, hp⟩
      · rintro ⟨rfl | hm, hp⟩
        · exact Or.inl rfl
        · exact Or.inr ⟨hm, hp⟩
    · simp only [List.mem_cons, ih]
      constructor
      · rintro ⟨hm, hp⟩
        exact ⟨Or.inr hm, hp⟩
      · rintro ⟨rfl | hm, hp⟩
        · exact absurd hp hpx
        · exact ⟨hm, hp⟩

/-- Structural boolean membership check on `List ℕ`. -/
def memNat (x : ℕ) : List ℕ → Bool
  | [] => false
  | y :: ys => (x == y) || memNat x ys

@[category API, AMS 5]
lemma memNat_iff (x : ℕ) (L : List ℕ) : memNat x L = true ↔ x ∈ L := by
  induction L with
  | nil => simp [memNat]
  | cons y ys ih =>
    simp only [memNat, Bool.or_eq_true, beq_iff_eq, List.mem_cons, ih]

/-- Structural duplicate-freeness check on `List ℕ`. -/
def nodupNat : List ℕ → Bool
  | [] => true
  | x :: xs => !memNat x xs && nodupNat xs

@[category API, AMS 5]
lemma nodupNat_sound (L : List ℕ) (h : nodupNat L = true) : L.Nodup := by
  induction L with
  | nil => exact List.nodup_nil
  | cons x xs ih =>
    simp only [nodupNat, Bool.and_eq_true, Bool.not_eq_true'] at h
    refine List.nodup_cons.mpr ⟨?_, ih h.2⟩
    intro hx
    have hm := (memNat_iff x xs).mpr hx
    rw [h.1] at hm
    cases hm

/-- Inner structural recursion over `List α` (avoids `WellFounded.fix` in the kernel). -/
def noCliqueAux {α : Type*} (R : α → α → Bool) (sub : List α → Bool) : List α → Bool
  | [] => true
  | x :: xs => sub (filterList (R x) xs) && noCliqueAux R sub xs

/-- Recursive boolean check that `L` contains no `k`-clique with respect to `R`. -/
def noClique {α : Type*} (R : α → α → Bool) : ℕ → List α → Bool
  | 0 => fun _ ↦ false
  | k + 1 => noCliqueAux R (noClique R k)

@[category API, AMS 5]
lemma noClique_sound {α : Type*} [DecidableEq α] (R : α → α → Bool)
    (k : ℕ) : ∀ (L : List α) (s : Finset α),
      noClique R k L = true →
      (∀ z ∈ s, z ∈ L) →
      (∀ u ∈ s, ∀ v ∈ s, u ≠ v → R u v = true) →
      s.card = k → False := by
  induction k with
  | zero =>
    intro L s h _ _ _
    simp [noClique] at h
  | succ k ih_k =>
    intro L
    induction L with
    | nil =>
      intro s _ hsub _ hcard
      obtain ⟨z, hz⟩ := Finset.card_pos.mp (by omega : 0 < s.card)
      exact List.not_mem_nil (hsub z hz)
    | cons x xs ih_L =>
      intro s h hsub hclq hcard
      simp only [noClique, noCliqueAux, Bool.and_eq_true] at h
      by_cases hx : x ∈ s
      · refine ih_k (filterList (R x) xs) (s.erase x) h.1 ?_ ?_ ?_
        · intro z hz
          have hzx : z ≠ x := (Finset.mem_erase.mp hz).1
          have hzs : z ∈ s := (Finset.mem_erase.mp hz).2
          have hz_mem : z ∈ xs := by
            rcases List.mem_cons.mp (hsub z hzs) with rfl | hmem
            · exact absurd rfl hzx
            · exact hmem
          exact (mem_filterList_iff (R x) xs z).mpr ⟨hz_mem, hclq x hx z hzs hzx.symm⟩
        · intro u hu v hv huv
          exact hclq u (Finset.erase_subset x s hu) v (Finset.erase_subset x s hv) huv
        · have := Finset.card_erase_of_mem hx
          omega
      · refine ih_L s h.2 ?_ hclq hcard
        intro z hz
        rcases List.mem_cons.mp (hsub z hz) with rfl | hmem
        · exact absurd hz hx
        · exact hmem

/-- Boolean adjacency for the 15-vertex graph $\overline{C_5[\overline{K_3}]}$. -/
def adj15Nat (u v : ℕ) : Bool :=
  (u != v) && ((u % 5 + 1) % 5 != v % 5) && ((v % 5 + 1) % 5 != u % 5)

/-- Explicit midpoint witness for non-adjacent distinct vertices in `g15`. -/
def mid15 (u v : ℕ) : ℕ :=
  if adj15Nat u ((u + 2) % 5) && adj15Nat ((u + 2) % 5) v then (u + 2) % 5 else (u + 3) % 5

/-- Vertex list `0..14`. -/
def verts15Nat : List ℕ :=
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

/-- Non-neighbors (including `u` itself) of `u` among `0..14`. -/
def nonNbrs15 (u : ℕ) : List ℕ :=
  filterList (fun w ↦ !adj15Nat u w) verts15Nat

@[category API, AMS 5]
lemma adj15Nat_irrefl_check :
    allBelow (fun u ↦ !adj15Nat u u) 15 = true := by
  decide

@[category API, AMS 5]
lemma adj15Nat_symm_check :
    allBelow (fun u ↦ allBelow (fun v ↦ adj15Nat u v == adj15Nat v u) 15) 15 = true := by
  decide

@[category API, AMS 5]
lemma diam2_15_check :
    allBelow (fun u ↦ allBelow (fun v ↦
      (u == v) || adj15Nat u v ||
        ((mid15 u v < 15) && adj15Nat u (mid15 u v) && adj15Nat (mid15 u v) v)) 15) 15 = true := by
  decide

@[category API, AMS 5]
lemma verts15Nat_mem_check :
    allBelow (fun k ↦ memNat k verts15Nat) 15 = true := by
  decide

@[category API, AMS 5]
lemma nonNbrs15_card_check :
    allBelow (fun u ↦ nodupNat (nonNbrs15 u) && ((nonNbrs15 u).length == 7)) 15 = true := by
  decide

@[category API, AMS 5]
lemma noIndep3_15_check :
    noClique (fun u v ↦ !adj15Nat u v) 3 verts15Nat = true := by
  decide

@[category API, AMS 5]
lemma mem_verts15Nat_iff (k : ℕ) : k ∈ verts15Nat ↔ k < 15 := by
  constructor
  · intro hk
    simp only [verts15Nat, List.mem_cons, List.not_mem_nil, or_false] at hk
    omega
  · intro hk
    exact (memNat_iff k verts15Nat).mp (allBelow_sound _ 15 verts15Nat_mem_check k hk)

/-- Universe-polymorphic 15-vertex counterexample graph $\overline{C_5[\overline{K_3}]}$. -/
def g15.{u} : SimpleGraph (ULift.{u} (Fin 15)) where
  Adj x y := adj15Nat x.down.val y.down.val = true
  symm.symm x y h := by
    have hsym := allBelow_sound _ 15
      (allBelow_sound _ 15 adj15Nat_symm_check x.down.val x.down.isLt) y.down.val y.down.isLt
    rw [beq_iff_eq] at hsym
    exact hsym ▸ h
  loopless.irrefl x h := by
    have hirr := allBelow_sound _ 15 adj15Nat_irrefl_check x.down.val x.down.isLt
    rw [Bool.not_eq_true'] at hirr
    rw [hirr] at h
    cases h

@[category API, AMS 5]
lemma g15_diam2.{u} (x y : ULift.{u} (Fin 15)) :
    x = y ∨ g15.Adj x y ∨ ∃ z : ULift.{u} (Fin 15), g15.Adj x z ∧ g15.Adj z y := by
  have hd := allBelow_sound _ 15
    (allBelow_sound _ 15 diam2_15_check x.down.val x.down.isLt) y.down.val y.down.isLt
  simp only [Bool.or_eq_true, beq_iff_eq, Bool.and_eq_true, decide_eq_true_eq] at hd
  rcases hd with (hxy | hadj) | ⟨⟨hlt, h1⟩, h2⟩
  · exact Or.inl (ULift.ext _ _ (Fin.ext hxy))
  · exact Or.inr (Or.inl hadj)
  · exact Or.inr (Or.inr ⟨ULift.up ⟨mid15 x.down.val y.down.val, hlt⟩, h1, h2⟩)

@[category API, AMS 5]
lemma g15_connected.{u} : (g15.{u}).Connected := by
  have : Nonempty (ULift.{u} (Fin 15)) := ⟨ULift.up 0⟩
  refine ⟨fun x y ↦ ?_⟩
  rcases g15_diam2 x y with rfl | hadj | ⟨z, hxz, hzy⟩
  · exact Reachable.refl x
  · exact hadj.reachable
  · exact hxz.reachable.trans hzy.reachable

@[category API, AMS 5]
lemma g15_even_dist_iff.{u} (x w : ULift.{u} (Fin 15)) :
    Even ((g15.{u}).dist x w) ↔ adj15Nat x.down.val w.down.val = false := by
  by_cases hxw : x = w
  · subst hxw
    have hirr := allBelow_sound _ 15 adj15Nat_irrefl_check x.down.val x.down.isLt
    rw [Bool.not_eq_true'] at hirr
    simp [SimpleGraph.dist_self, hirr]
  · by_cases hadj : (g15.{u}).Adj x w
    · have hd_le : (g15.{u}).dist x w ≤ 1 := by
        simpa using (g15.{u}).dist_le (Walk.cons hadj Walk.nil)
      have hd_pos : 0 < (g15.{u}).dist x w := hadj.reachable.pos_dist_of_ne hxw
      have hd1 : (g15.{u}).dist x w = 1 := by omega
      have hadj_true : adj15Nat x.down.val w.down.val = true := hadj
      rw [hd1, hadj_true]
      decide
    · have hadj_false : adj15Nat x.down.val w.down.val = false := by
        cases hb : adj15Nat x.down.val w.down.val
        · rfl
        · exact absurd hb hadj
      rcases g15_diam2 x w with rfl | h1 | ⟨z, hxz, hzw⟩
      · exact absurd rfl hxw
      · exact absurd h1 hadj
      · have hd_le : (g15.{u}).dist x w ≤ 2 := by
          simpa using (g15.{u}).dist_le (Walk.cons hxz (Walk.cons hzw Walk.nil))
        have hd_pos : 0 < (g15.{u}).dist x w :=
          (hxz.reachable.trans hzw.reachable).pos_dist_of_ne hxw
        have hd_ne1 : (g15.{u}).dist x w ≠ 1 := by
          intro hd1
          obtain ⟨p, hp⟩ := (g15.{u}).exists_walk_of_dist_ne_zero (by omega : (g15.{u}).dist x w ≠ 0)
          rw [hd1] at hp
          cases p with
          | nil => simp at hp
          | cons h rest =>
            cases rest with
            | nil => exact hadj h
            | cons _ _ => simp at hp
        have hd2 : (g15.{u}).dist x w = 2 := by omega
        rw [hd2, hadj_false]
        exact ⟨fun _ ↦ rfl, fun _ ↦ ⟨1, rfl⟩⟩

@[category API, AMS 5]
lemma distEven_g15.{u} (x : ULift.{u} (Fin 15)) : distEven (g15.{u}) x = 7 := by
  unfold distEven
  let valEmb : ULift.{u} (Fin 15) ↪ ℕ :=
    ⟨fun y ↦ y.down.val, fun y₁ y₂ h ↦ ULift.ext _ _ (Fin.ext h)⟩
  have hmap_card :
      (Finset.univ.filter fun w : ULift.{u} (Fin 15) ↦ Even ((g15.{u}).dist x w)).card =
        ((Finset.univ.filter fun w : ULift.{u} (Fin 15) ↦
          Even ((g15.{u}).dist x w)).map valEmb).card :=
    (Finset.card_map valEmb).symm
  rw [hmap_card]
  have hset :
      ((Finset.univ.filter fun w : ULift.{u} (Fin 15) ↦
        Even ((g15.{u}).dist x w)).map valEmb) =
        (nonNbrs15 x.down.val).toFinset := by
    ext k
    simp only [Finset.mem_map, Finset.mem_filter, Finset.mem_univ, true_and,
      List.mem_toFinset, nonNbrs15, mem_filterList_iff, mem_verts15Nat_iff,
      Bool.not_eq_true', g15_even_dist_iff]
    constructor
    · rintro ⟨w, hw, rfl⟩
      exact ⟨w.down.isLt, hw⟩
    · rintro ⟨hk, hw⟩
      exact ⟨ULift.up ⟨k, hk⟩, hw, rfl⟩
  rw [hset]
  have hc := allBelow_sound _ 15 nonNbrs15_card_check x.down.val x.down.isLt
  simp only [Bool.and_eq_true, beq_iff_eq] at hc
  rw [List.toFinset_card_of_nodup (nodupNat_sound _ hc.1)]
  exact hc.2

@[category API, AMS 5]
lemma g15_indep_card_le_two.{u} (t : Finset (ULift.{u} (Fin 15)))
    (hind : ∀ x ∈ t, ∀ y ∈ t, x ≠ y → ¬ (g15.{u}).Adj x y) : t.card ≤ 2 := by
  by_contra hlt
  have ht3 : 3 ≤ t.card := by omega
  obtain ⟨t', ht'sub, ht'card⟩ := Finset.exists_subset_card_eq ht3
  let valEmb : ULift.{u} (Fin 15) ↪ ℕ :=
    ⟨fun y ↦ y.down.val, fun y₁ y₂ h ↦ ULift.ext _ _ (Fin.ext h)⟩
  let tNat : Finset ℕ := t'.map valEmb
  have htNat_card : tNat.card = 3 := by simpa [tNat] using ht'card
  have htNat_sub : ∀ z ∈ tNat, z ∈ verts15Nat := by
    intro z hz
    rcases Finset.mem_map.mp hz with ⟨zf, _, rfl⟩
    exact (mem_verts15Nat_iff zf.down.val).mpr zf.down.isLt
  have htNat_clq : ∀ x ∈ tNat, ∀ y ∈ tNat, x ≠ y → (!adj15Nat x y) = true := by
    intro x hx y hy hxy
    rcases Finset.mem_map.mp hx with ⟨xf, hxf, rfl⟩
    rcases Finset.mem_map.mp hy with ⟨yf, hyf, rfl⟩
    have hxyf : xf ≠ yf := fun h ↦ hxy (congrArg valEmb h)
    have hnadj := hind xf (ht'sub hxf) yf (ht'sub hyf) hxyf
    rw [Bool.not_eq_true']
    cases hb : adj15Nat xf.down.val yf.down.val
    · rfl
    · exact absurd hb hnadj
  exact noClique_sound (fun x y ↦ !adj15Nat x y) 3 verts15Nat tNat noIndep3_15_check
    htNat_sub htNat_clq htNat_card

@[category API, AMS 5]
lemma g15_b_le_four.{u} : b (g15.{u}) ≤ 4 := by
  unfold b
  suffices h : (g15.{u}).largestInducedBipartiteSubgraphSize ≤ 4 by
    exact_mod_cast h
  unfold largestInducedBipartiteSubgraphSize
  apply csSup_le
  · refine ⟨0, ∅, ?_, rfl⟩
    rw [induce_isBipartite_iff_exists_coloring]
    exact ⟨fun _ ↦ 0, by simp⟩
  · rintro n ⟨s, hs, rfl⟩
    obtain ⟨c, hc⟩ := (induce_isBipartite_iff_exists_coloring (g15.{u}) s).mp hs
    let s₀ := s.filter (fun x ↦ c x = 0)
    let s₁ := s.filter (fun x ↦ ¬ c x = 0)
    have hsub : s ⊆ s₀ ∪ s₁ := by
      intro x hx
      by_cases hcx : c x = 0
      · exact Finset.mem_union_left s₁ (Finset.mem_filter.mpr ⟨hx, hcx⟩)
      · exact Finset.mem_union_right s₀ (Finset.mem_filter.mpr ⟨hx, hcx⟩)
    have hcard_le : s.card ≤ s₀.card + s₁.card :=
      le_trans (Finset.card_le_card hsub) (Finset.card_union_le s₀ s₁)
    have hs₀ : s₀.card ≤ 2 := by
      refine g15_indep_card_le_two s₀ ?_
      intro x hx y hy _ hadj
      have cx := (Finset.mem_filter.mp hx).2
      have cy := (Finset.mem_filter.mp hy).2
      exact hc x (Finset.mem_filter.mp hx).1 y (Finset.mem_filter.mp hy).1 hadj (cx.trans cy.symm)
    have hs₁ : s₁.card ≤ 2 := by
      refine g15_indep_card_le_two s₁ ?_
      intro x hx y hy _ hadj
      have cx : c x ≠ 0 := (Finset.mem_filter.mp hx).2
      have cy : c y ≠ 0 := (Finset.mem_filter.mp hy).2
      have hc_eq : c x = c y := by
        ext
        have hx_lt := (c x).isLt
        have hy_lt := (c y).isLt
        have hx0 : (c x).val ≠ 0 := fun h ↦ cx (Fin.ext h)
        have hy0 : (c y).val ≠ 0 := fun h ↦ cy (Fin.ext h)
        omega
      exact hc x (Finset.mem_filter.mp hx).1 y (Finset.mem_filter.mp hy).1 hadj hc_eq
    omega

/--
WOWII [Conjecture 25](http://cms.uhd.edu/faculty/delavinae/research/wowII/all.html#conj25)
(status F, disproved):

For every finite simple connected graph $G$,
$b(G) ≥ 2⌈(1 + \min_v \operatorname{dist}_{\mathrm{even}}(v))/3⌉$,
where $b(G)$ is the size of a largest induced bipartite subgraph and
$\operatorname{dist}_{\mathrm{even}}(v)$ counts the vertices at even distance from $v$.

The nontrivial vertex type excludes graphs with fewer than two vertices.
The source gives the same counterexample as for Conjecture 24.
-/
@[category research solved, AMS 5]
theorem conjecture25 :
    ¬ ∀ {α : Type*} [Fintype α] [DecidableEq α] [Nontrivial α],
      ∀ (G : SimpleGraph α) (_ : G.Connected),
        let minDistEven := (Finset.univ.image (distEven G)).min' (by simp)
        2 * ⌈(1 + (minDistEven : ℝ)) / 3⌉ ≤ (b G : ℝ) := by
  intro hAll
  have : Nontrivial (ULift (Fin 15)) := ⟨ULift.up 0, ULift.up 1, fun h ↦ by cases h⟩
  have h := hAll g15 g15_connected
  dsimp only at h
  set m := (Finset.univ.image (distEven g15)).min' (by simp)
  have hm : m = 7 := by
    apply le_antisymm
    · exact Finset.min'_le _ 7
        (Finset.mem_image.mpr ⟨ULift.up 0, Finset.mem_univ _, distEven_g15 (ULift.up 0)⟩)
    · refine Finset.le_min' _ _ 7 (fun y hy ↦ ?_)
      rcases Finset.mem_image.mp hy with ⟨x, _, rfl⟩
      rw [distEven_g15 x]
  rw [hm] at h
  have hceil : (3 : ℤ) ≤ ⌈(1 + (7 : ℝ)) / 3⌉ := by
    have hlt : (2 : ℤ) < ⌈(1 + (7 : ℝ)) / 3⌉ :=
      Int.lt_ceil.mpr (by norm_num : ((2 : ℤ) : ℝ) < (1 + (7 : ℝ)) / 3)
    omega
  have hlhs : (6 : ℝ) ≤ 2 * ⌈(1 + (7 : ℝ)) / 3⌉ := by
    have hceilR : (3 : ℝ) ≤ (⌈(1 + (7 : ℝ)) / 3⌉ : ℝ) := by exact_mod_cast hceil
    linarith
  have hb4 : (b g15 : ℝ) ≤ 4 := g15_b_le_four
  linarith

-- Sanity checks

/-- The invariant `b G` is nonneg. -/
@[category test, AMS 5]
example (G : SimpleGraph (Fin 3)) : 0 ≤ b G := Nat.cast_nonneg _

/-- In $K_3$, only the vertex itself is at even distance. -/
@[category test, AMS 5]
theorem distEven_complete_three (v : Fin 3) : distEven (⊤ : SimpleGraph (Fin 3)) v = 1 := by
  simp [distEven, SimpleGraph.dist_top, apply_ite, Finset.filter_eq]

end WrittenOnTheWallII.GraphConjecture25
