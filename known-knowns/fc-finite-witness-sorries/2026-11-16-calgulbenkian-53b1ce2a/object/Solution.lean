/-
Copyright 2026 The Formal Conjectures Authors.

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
# Lower bound $102 \le R(6,6)$ via the Paley graph $P(101)$

Kernel-checked proof of `RamseyNumbers.ramsey_number_six_six_lower_bound` using the Paley graph on
`Fin 101`, $AGL_1(\mathbb{F}_{101})$ two-point symmetry reduction, self-complementarity via
multiplication by $2$, and a proved-sound reflected clique-freeness checker over the $24$-vertex
common neighborhood of $0$ and $1$.
-/

@[expose] public section

namespace RamseyNumbers

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
lemma mem_filterList {α : Type*} (p : α → Bool) (L : List α) (z : α) :
    p z = true → z ∈ L → z ∈ filterList p L := by
  intro hp hz
  induction L with
  | nil => cases hz
  | cons x xs ih =>
    simp only [filterList]
    rcases List.mem_cons.mp hz with rfl | hmem
    · rw [if_pos hp]
      exact List.mem_cons_self
    · split_ifs
      · exact List.mem_cons_of_mem x (ih hmem)
      · exact ih hmem

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
          exact mem_filterList (R x) xs z (hclq x hx z hzs hzx.symm) hz_mem
        · intro u hu v hv huv
          exact hclq u (Finset.erase_subset x s hu) v (Finset.erase_subset x s hv) huv
        · have := Finset.card_erase_of_mem hx
          omega
      · refine ih_L s h.2 ?_ hclq hcard
        intro z hz
        rcases List.mem_cons.mp (hsub z hz) with rfl | hmem
        · exact absurd hz hx
        · exact hmem

/-- 101-bit mask of nonzero quadratic residues modulo 101. -/
def qrMask101 : ℕ := 1550432784880709368503235994226

/-- Test whether `d < 101` is a nonzero quadratic residue modulo 101. -/
def qrBit101 (d : ℕ) : Bool :=
  (qrMask101 >>> d) % 2 == 1

/-- Boolean adjacency on naturals modulo 101. -/
def paley101AdjNat (u v : ℕ) : Bool :=
  qrBit101 ((u + 101 - v) % 101)

/-- Lookup table of multiplicative inverses modulo 101. -/
def invTable101 : List ℕ :=
  [0, 1, 51, 34, 76, 81, 17, 29, 38, 45, 91, 46, 59, 70, 65, 27, 19, 6, 73, 16, 96,
   77, 23, 22, 80, 97, 35, 15, 83, 7, 64, 88, 60, 49, 3, 26, 87, 71, 8, 57, 48,
   69, 89, 47, 62, 9, 11, 43, 40, 33, 99, 2, 68, 61, 58, 90, 92, 39, 54, 12, 32,
   53, 44, 93, 30, 14, 75, 98, 52, 41, 13, 37, 94, 18, 86, 66, 4, 21, 79, 78, 24,
   5, 85, 28, 95, 82, 74, 36, 31, 42, 55, 10, 56, 63, 72, 84, 20, 25, 67, 50, 100]

/-- Multiplicative inverse modulo 101 via `invTable101`. -/
def invMod101 (b : ℕ) : ℕ :=
  invTable101.getD b 0

@[category API, AMS 5]
lemma qrBit101_zero : qrBit101 0 = false := by
  decide

@[category API, AMS 5]
lemma qrBit101_symm_check :
    allBelow (fun d ↦ qrBit101 d == qrBit101 ((101 - d) % 101)) 101 = true := by
  decide

@[category API, AMS 5]
lemma qrBit101_nonres_mul2_check :
    allBelow (fun d ↦ (d == 0) || qrBit101 d || qrBit101 ((2 * d) % 101)) 101 = true := by
  decide

@[category API, AMS 5]
lemma invMod101_check :
    allBelow (fun b ↦ (b == 0) ||
      ((invMod101 b < 101) && ((invMod101 b * b) % 101 == 1))) 101 = true := by
  decide

@[category API, AMS 5]
lemma qrBit101_mul_inv_check :
    allBelow (fun b ↦ !qrBit101 b ||
      allBelow (fun d ↦ !qrBit101 d || qrBit101 ((invMod101 b * d) % 101)) 101) 101 = true := by
  decide

/-- Common neighbors of `0` and `1` in $P(101)$. -/
def paley101Common01 : List ℕ :=
  [5, 6, 14, 17, 20, 21, 22, 23, 24, 25, 31, 37,
   65, 71, 77, 78, 79, 80, 81, 82, 85, 88, 96, 97]

@[category API, AMS 5]
lemma mem_paley101Common01_check :
    allBelow (fun z ↦ !(paley101AdjNat z 0 && paley101AdjNat z 1) ||
      decide (z ∈ paley101Common01)) 101 = true := by
  decide

@[category API, AMS 5]
lemma noClique4_paley101Common01 :
    noClique paley101AdjNat 4 paley101Common01 = true := by
  decide

/-- The Paley graph $P(101)$ on `Fin 101`. -/
def paley101 : SimpleGraph (Fin 101) where
  Adj u v := paley101AdjNat u.val v.val = true
  symm.symm u v h := by
    change qrBit101 ((v.val + 101 - u.val) % 101) = true
    change qrBit101 ((u.val + 101 - v.val) % 101) = true at h
    let d := (u.val + 101 - v.val) % 101
    have hd : d < 101 := Nat.mod_lt _ (by decide)
    have hsym := allBelow_sound _ 101 qrBit101_symm_check d hd
    have heq : (v.val + 101 - u.val) % 101 = (101 - d) % 101 := by omega
    rw [heq]
    have hbeq : (qrBit101 d == qrBit101 ((101 - d) % 101)) = true := hsym
    rw [beq_iff_eq] at hbeq
    exact hbeq ▸ h
  loopless.irrefl u h := by
    change qrBit101 ((u.val + 101 - u.val) % 101) = true at h
    have heq : (u.val + 101 - u.val) % 101 = 0 := by omega
    rw [heq, qrBit101_zero] at h
    cases h

@[category API, AMS 5]
lemma mul_sub_mod101 (c u v : ℕ) (hu : u < 101) (hv : v < 101) :
    ((c * u) % 101 + 101 - (c * v) % 101) % 101 = (c * ((u + 101 - v) % 101)) % 101 := by
  rw [← ZMod.natCast_eq_natCast_iff' _ _ 101]
  have h1 : (c * v) % 101 ≤ (c * u) % 101 + 101 := by
    have : (c * v) % 101 < 101 := Nat.mod_lt _ (by decide)
    omega
  have h2 : v ≤ u + 101 := by omega
  have h101 : (101 : ZMod 101) = 0 := by exact_mod_cast ZMod.natCast_self 101
  push_cast [Nat.cast_sub h1, Nat.cast_sub h2, ZMod.natCast_mod]
  rw [h101]
  ring

@[category API, AMS 5]
lemma mul_inv_mod101_cancel (b c x : ℕ) (hx : x < 101) (hcb : (c * b) % 101 = 1) :
    (b * ((c * x) % 101)) % 101 = x := by
  have hmod : (b * ((c * x) % 101)) % 101 = x % 101 := by
    rw [← ZMod.natCast_eq_natCast_iff' _ _ 101]
    have hcbz : ((c : ZMod 101) * (b : ZMod 101)) = 1 := by
      have := (ZMod.natCast_eq_natCast_iff' (c * b) 1 101).mpr (by simpa using hcb)
      simpa using this
    push_cast [ZMod.natCast_mod]
    calc (b : ZMod 101) * ((c : ZMod 101) * (x : ZMod 101))
        = ((c : ZMod 101) * (b : ZMod 101)) * (x : ZMod 101) := by ring
      _ = 1 * (x : ZMod 101) := by rw [hcbz]
      _ = (x : ZMod 101) := one_mul _
  rwa [Nat.mod_eq_of_lt hx] at hmod

@[category API, AMS 5]
lemma paley101_cliqueFree_six : paley101.CliqueFree 6 := by
  intro s hs
  rcases hs with ⟨hs_clq, hs_card⟩
  -- Step 1: Translate an element `a ∈ s` to `0 : Fin 101`.
  obtain ⟨a, ha⟩ := Finset.card_pos.mp (by omega : 0 < s.card)
  let trFun : Fin 101 → Fin 101 := fun x ↦ ⟨(x.val + 101 - a.val) % 101, Nat.mod_lt _ (by decide)⟩
  have htr_inj : Function.Injective trFun := by
    intro x y hxy
    have hval : (x.val + 101 - a.val) % 101 = (y.val + 101 - a.val) % 101 :=
      congrArg Fin.val hxy
    ext
    have := x.isLt; have := y.isLt; have := a.isLt
    omega
  let tr : Fin 101 ↪ Fin 101 := ⟨trFun, htr_inj⟩
  let s₁ : Finset (Fin 101) := s.map tr
  have hs₁_card : s₁.card = 6 := by simpa [s₁] using hs_card
  have h0_mem : (0 : Fin 101) ∈ s₁ := by
    refine Finset.mem_map.mpr ⟨a, ha, ?_⟩
    ext
    change (a.val + 101 - a.val) % 101 = 0
    omega
  have hs₁_clq : ∀ u ∈ s₁, ∀ v ∈ s₁, u ≠ v → paley101.Adj u v := by
    intro u hu v hv huv
    rcases Finset.mem_map.mp hu with ⟨u₀, hu₀, rfl⟩
    rcases Finset.mem_map.mp hv with ⟨v₀, hv₀, rfl⟩
    have huv₀ : u₀ ≠ v₀ := fun h ↦ huv (congrArg tr h)
    have hadj : qrBit101 ((u₀.val + 101 - v₀.val) % 101) = true := hs_clq hu₀ hv₀ huv₀
    change qrBit101 (((tr u₀).val + 101 - (tr v₀).val) % 101) = true
    have hdiff : ((tr u₀).val + 101 - (tr v₀).val) % 101 = (u₀.val + 101 - v₀.val) % 101 := by
      change ((u₀.val + 101 - a.val) % 101 + 101 - (v₀.val + 101 - a.val) % 101) % 101 =
        (u₀.val + 101 - v₀.val) % 101
      have := u₀.isLt; have := v₀.isLt; have := a.isLt
      omega
    rwa [hdiff]
  -- Step 2: Pick `b ∈ s₁.erase 0` and rescale by `c = invMod101 b.val`.
  have hs₁_erase_card : (s₁.erase 0).card = 5 := by
    rw [Finset.card_erase_of_mem h0_mem, hs₁_card]
  obtain ⟨b, hb_erase⟩ := Finset.card_pos.mp (by omega : 0 < (s₁.erase 0).card)
  have hb_ne : b ≠ 0 := (Finset.mem_erase.mp hb_erase).1
  have hb_mem : b ∈ s₁ := (Finset.mem_erase.mp hb_erase).2
  have hb_qr : qrBit101 b.val = true := by
    have hadj : qrBit101 ((b.val + 101 - 0) % 101) = true := hs₁_clq b hb_mem 0 h0_mem hb_ne
    have hmod : (b.val + 101 - 0) % 101 = b.val := by have := b.isLt; omega
    rwa [hmod] at hadj
  let c : ℕ := invMod101 b.val
  have hcb_props := allBelow_sound _ 101 invMod101_check b.val b.isLt
  have hb_val_ne : b.val ≠ 0 := fun h ↦ hb_ne (Fin.ext h)
  have hcb : (c * b.val) % 101 = 1 := by
    simp only [Bool.or_eq_true, beq_iff_eq, Bool.and_eq_true, decide_eq_true_eq] at hcb_props
    rcases hcb_props with h0 | ⟨_, h1⟩
    · exact absurd h0 hb_val_ne
    · exact h1
  let scFun : Fin 101 → Fin 101 := fun x ↦ ⟨(c * x.val) % 101, Nat.mod_lt _ (by decide)⟩
  have hsc_inj : Function.Injective scFun := by
    intro x y hxy
    have hval : (c * x.val) % 101 = (c * y.val) % 101 := congrArg Fin.val hxy
    ext
    calc x.val = (b.val * ((c * x.val) % 101)) % 101 :=
          (mul_inv_mod101_cancel b.val c x.val x.isLt hcb).symm
      _ = (b.val * ((c * y.val) % 101)) % 101 := by rw [hval]
      _ = y.val := mul_inv_mod101_cancel b.val c y.val y.isLt hcb
  let sc : Fin 101 ↪ Fin 101 := ⟨scFun, hsc_inj⟩
  let s₂ : Finset (Fin 101) := s₁.map sc
  have hs₂_card : s₂.card = 6 := by simpa [s₂] using hs₁_card
  have h0_s₂ : (0 : Fin 101) ∈ s₂ := by
    refine Finset.mem_map.mpr ⟨0, h0_mem, ?_⟩
    ext
    change (c * 0) % 101 = 0
    simp
  have h1_s₂ : (1 : Fin 101) ∈ s₂ := by
    refine Finset.mem_map.mpr ⟨b, hb_mem, ?_⟩
    ext
    exact hcb
  have hs₂_clq : ∀ u ∈ s₂, ∀ v ∈ s₂, u ≠ v → paley101.Adj u v := by
    intro u hu v hv huv
    rcases Finset.mem_map.mp hu with ⟨u₁, hu₁, rfl⟩
    rcases Finset.mem_map.mp hv with ⟨v₁, hv₁, rfl⟩
    have huv₁ : u₁ ≠ v₁ := fun h ↦ huv (congrArg sc h)
    have hadj : qrBit101 ((u₁.val + 101 - v₁.val) % 101) = true := hs₁_clq u₁ hu₁ v₁ hv₁ huv₁
    change qrBit101 (((c * u₁.val) % 101 + 101 - (c * v₁.val) % 101) % 101) = true
    rw [mul_sub_mod101 c u₁.val v₁.val u₁.isLt v₁.isLt]
    let d := (u₁.val + 101 - v₁.val) % 101
    have hd : d < 101 := Nat.mod_lt _ (by decide)
    have hmul_b := allBelow_sound _ 101 qrBit101_mul_inv_check b.val b.isLt
    simp only [Bool.or_eq_true, Bool.not_eq_true'] at hmul_b
    rcases hmul_b with hnotb | hall_d
    · rw [hb_qr] at hnotb; cases hnotb
    · have hmul_d := allBelow_sound _ 101 hall_d d hd
      simp only [Bool.or_eq_true, Bool.not_eq_true'] at hmul_d
      rcases hmul_d with hnotd | hok
      · rw [hadj] at hnotd; cases hnotd
      · exact hok
  -- Step 3: Erase `0` and `1` and map by `Fin.val` to get a 4-clique in `paley101Common01`.
  let tFin : Finset (Fin 101) := (s₂.erase 0).erase 1
  have h10 : (1 : Fin 101) ≠ 0 := by decide
  have h1_erase : (1 : Fin 101) ∈ s₂.erase 0 := Finset.mem_erase.mpr ⟨h10, h1_s₂⟩
  have htFin_card : tFin.card = 4 := by
    dsimp only [tFin]
    rw [Finset.card_erase_of_mem h1_erase, Finset.card_erase_of_mem h0_s₂, hs₂_card]
  let valEmb : Fin 101 ↪ ℕ := ⟨Fin.val, Fin.val_injective⟩
  let t : Finset ℕ := tFin.map valEmb
  have ht_card : t.card = 4 := by simpa [t] using htFin_card
  have ht_sub : ∀ z ∈ t, z ∈ paley101Common01 := by
    intro z hz
    rcases Finset.mem_map.mp hz with ⟨zf, hzf, rfl⟩
    have hz1 : zf ≠ 1 := (Finset.mem_erase.mp hzf).1
    have hz_e0 : zf ∈ s₂.erase 0 := (Finset.mem_erase.mp hzf).2
    have hz0 : zf ≠ 0 := (Finset.mem_erase.mp hz_e0).1
    have hzs₂ : zf ∈ s₂ := (Finset.mem_erase.mp hz_e0).2
    have hadj0 : paley101AdjNat zf.val 0 = true := hs₂_clq zf hzs₂ 0 h0_s₂ hz0
    have hadj1 : paley101AdjNat zf.val 1 = true := hs₂_clq zf hzs₂ 1 h1_s₂ hz1
    have hmem := allBelow_sound _ 101 mem_paley101Common01_check zf.val zf.isLt
    simp only [Bool.or_eq_true, Bool.not_eq_true', Bool.and_eq_false_iff,
      decide_eq_true_eq] at hmem
    rcases hmem with (h0 | h1) | hin
    · rw [hadj0] at h0; cases h0
    · rw [hadj1] at h1; cases h1
    · exact hin
  have ht_clq : ∀ u ∈ t, ∀ v ∈ t, u ≠ v → paley101AdjNat u v = true := by
    intro u hu v hv huv
    rcases Finset.mem_map.mp hu with ⟨uf, huf, rfl⟩
    rcases Finset.mem_map.mp hv with ⟨vf, hvf, rfl⟩
    have huvf : uf ≠ vf := fun h ↦ huv (congrArg Fin.val h)
    have hus₂ : uf ∈ s₂ := Finset.erase_subset 0 s₂ (Finset.erase_subset 1 _ huf)
    have hvs₂ : vf ∈ s₂ := Finset.erase_subset 0 s₂ (Finset.erase_subset 1 _ hvf)
    exact hs₂_clq uf hus₂ vf hvs₂ huvf
  exact noClique_sound paley101AdjNat 4 paley101Common01 t noClique4_paley101Common01
    ht_sub ht_clq ht_card

@[category API, AMS 5]
lemma paley101_compl_cliqueFree_six : (paley101ᶜ).CliqueFree 6 := by
  intro s hs
  rcases hs with ⟨hs_clq, hs_card⟩
  let dblFun : Fin 101 → Fin 101 := fun x ↦ ⟨(2 * x.val) % 101, Nat.mod_lt _ (by decide)⟩
  have hdbl_inj : Function.Injective dblFun := by
    intro x y hxy
    have hval : (2 * x.val) % 101 = (2 * y.val) % 101 := congrArg Fin.val hxy
    ext
    have := x.isLt; have := y.isLt
    omega
  let dbl : Fin 101 ↪ Fin 101 := ⟨dblFun, hdbl_inj⟩
  refine paley101_cliqueFree_six (s.map dbl) ⟨?_, by simpa using hs_card⟩
  intro u hu v hv huv
  rcases Finset.mem_map.mp hu with ⟨u₀, hu₀, rfl⟩
  rcases Finset.mem_map.mp hv with ⟨v₀, hv₀, rfl⟩
  have huv₀ : u₀ ≠ v₀ := fun h ↦ huv (congrArg dbl h)
  have hcadj : (paley101ᶜ).Adj u₀ v₀ := hs_clq hu₀ hv₀ huv₀
  rw [SimpleGraph.compl_adj] at hcadj
  have hnot : qrBit101 ((u₀.val + 101 - v₀.val) % 101) = false := by
    cases hq : qrBit101 ((u₀.val + 101 - v₀.val) % 101)
    · rfl
    · exact absurd hq hcadj.2
  change qrBit101 (((2 * u₀.val) % 101 + 101 - (2 * v₀.val) % 101) % 101) = true
  rw [mul_sub_mod101 2 u₀.val v₀.val u₀.isLt v₀.isLt]
  let d := (u₀.val + 101 - v₀.val) % 101
  have hd : d < 101 := Nat.mod_lt _ (by decide)
  have hd_ne : d ≠ 0 := by
    intro hd0
    apply huv₀
    ext
    have := u₀.isLt; have := v₀.isLt
    omega
  have hnr := allBelow_sound _ 101 qrBit101_nonres_mul2_check d hd
  simp only [Bool.or_eq_true, beq_iff_eq] at hnr
  rcases hnr with (hd0 | hqd) | hq2d
  · exact absurd hd0 hd_ne
  · rw [hnot] at hqd; cases hqd
  · exact hq2d

/--
Lower bound $102 \le R(6,6)$, equivalently: there exists a graph on $101$ vertices with no
$6$-clique and no independent set of size $6$.
-/
@[category research solved, AMS 5]
theorem ramsey_number_six_six_lower_bound :
    ∃ G : SimpleGraph (Fin 101), G.CliqueFree 6 ∧ (Gᶜ).CliqueFree 6 := by
  exact ⟨paley101, paley101_cliqueFree_six, paley101_compl_cliqueFree_six⟩

end RamseyNumbers
