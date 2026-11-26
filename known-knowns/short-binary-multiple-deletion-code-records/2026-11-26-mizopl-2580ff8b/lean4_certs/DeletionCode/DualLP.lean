/-
  DeletionCode/DualLP.lean — Pure-Kernel Weak LP Duality Upper Bounds, Exact Global Optimality
  Theorems (M_2(7) = 5 and M_3(9) = 5), and Klein-4 <c,r> Symmetry Certificate for (16,3) = 44.
  Zero external dependencies, zero sorryAx, zero native_decide / Lean.ofReduceBool.
-/
import DeletionCode.Basic
import DeletionCode.Cert_16_3

set_option maxRecDepth 16384

namespace DeletionCode.DualLP

/-- Binary tree storing a minimal list of packed deletion witnesses per `x < 2^n`. -/
inductive DualTree where
  | leaf (ps : List Nat) : DualTree
  | node (l r : DualTree) : DualTree

private abbrev DN := DualTree.node
private abbrev DL := DualTree.leaf

def DualTree.lookup : Nat → DualTree → Nat → List Nat
  | 0, .leaf ps, _ => ps
  | d + 1, .node l r, x =>
      if x < 2 ^ d then l.lookup d x else r.lookup d (x - 2 ^ d)
  | _, _, _ => []

/-- Strictly increasing Nat list checker (implies `Nodup` in O(len) instead of O(len^2)!). -/
def isStrictAsc : List Nat → Bool
  | [] => true
  | [_] => true
  | a :: b :: rest => (a < b) && isStrictAsc (b :: rest)

theorem strictAsc_gt_all {a : Nat} {L : List Nat} :
    isStrictAsc (a :: L) = true → ∀ b ∈ L, a < b := by
  induction L generalizing a with
  | nil => intro _ _ h; cases h
  | cons c cs ih =>
    intro h b hb
    simp only [isStrictAsc, Bool.and_eq_true, decide_eq_true_eq] at h
    rcases List.mem_cons.mp hb with rfl | hcs
    · exact h.1
    · exact Nat.lt_trans h.1 (ih h.2 b hcs)

theorem strictAsc_nodup : ∀ {L : List Nat}, isStrictAsc L = true → L.Nodup
  | [], _ => List.nodup_nil
  | [_], _ => by simp
  | a :: b :: rest, h => by
    have hall := strictAsc_gt_all h
    simp only [isStrictAsc, Bool.and_eq_true, decide_eq_true_eq] at h
    rw [List.nodup_cons]
    refine ⟨fun hmem => Nat.lt_irrefl a (hall a hmem), strictAsc_nodup h.2⟩

private theorem delBit_lt_pub (m p y : Nat) (hy : y < 2 ^ m) (hp : p < m) :
    delBit y p < 2 ^ (m - 1) := by
  unfold delBit
  have hpos_p : 0 < 2 ^ p := Nat.two_pow_pos p
  have h1 : 2 ^ m = (2 * 2 ^ p) * 2 ^ (m - 1 - p) := by
    have hm : m = (1 + p) + (m - 1 - p) := by omega
    calc
      2 ^ m = 2 ^ ((1 + p) + (m - 1 - p)) := congrArg (2 ^ ·) hm
      _ = 2 ^ (1 + p) * 2 ^ (m - 1 - p) := Nat.pow_add 2 (1 + p) (m - 1 - p)
      _ = (2 * 2 ^ p) * 2 ^ (m - 1 - p) := by rw [Nat.pow_add, Nat.pow_one]
  have h2 : 2 ^ (m - 1) = 2 ^ (m - 1 - p) * 2 ^ p := by
    have hm : m - 1 = (m - 1 - p) + p := by omega
    calc
      2 ^ (m - 1) = 2 ^ ((m - 1 - p) + p) := congrArg (2 ^ ·) hm
      _ = 2 ^ (m - 1 - p) * 2 ^ p := Nat.pow_add 2 (m - 1 - p) p
  have hdiv_lt : y / (2 * 2 ^ p) < 2 ^ (m - 1 - p) := by
    rw [Nat.div_lt_iff_lt_mul (show 0 < 2 * 2 ^ p by omega)]
    rw [Nat.mul_comm] at h1
    omega
  have hmod_lt : y % 2 ^ p < 2 ^ p := Nat.mod_lt y hpos_p
  have hmul : (y / (2 * 2 ^ p) + 1) * 2 ^ p ≤ 2 ^ (m - 1 - p) * 2 ^ p :=
    Nat.mul_le_mul_right (2 ^ p) hdiv_lt
  rw [Nat.add_mul, Nat.one_mul] at hmul
  omega

/-- Key Weak LP Duality Sum Lemma (zero Mathlib). -/
theorem sum_map_le_of_nodup_subset (y : Nat → Nat) :
    ∀ (L S : List Nat), L.Nodup → (∀ a ∈ L, a ∈ S) → (L.map y).sum ≤ (S.map y).sum := by
  intro L
  induction L with
  | nil => intro S _ _; exact Nat.zero_le _
  | cons a as ih =>
    intro S hnd hsub
    rw [List.nodup_cons] at hnd
    have haS : a ∈ S := hsub a (List.mem_cons_self ..)
    have herase : ∀ (T : List Nat), a ∈ T →
        (T.map y).sum = y a + ((T.erase a).map y).sum ∧ ∀ b ∈ T, b ≠ a → b ∈ T.erase a := by
      intro T
      induction T with
      | nil => intro h; cases h
      | cons t ts iht =>
        intro hmem
        by_cases hta : t = a
        · subst hta
          simp only [List.erase_cons_head, List.map_cons, List.sum_cons]
          refine ⟨trivial, fun b hb hne => ?_⟩
          rcases List.mem_cons.mp hb with rfl | hbts
          · exact absurd rfl hne
          · exact hbts
        · have hbe : (t == a) = false := beq_false_of_ne hta
          have hats : a ∈ ts := by
            rcases List.mem_cons.mp hmem with rfl | h
            · exact absurd rfl hta
            · exact h
          obtain ⟨hsum, hkeep⟩ := iht hats
          simp only [List.erase_cons, hbe, Bool.false_eq_true, ↓reduceIte, List.map_cons, List.sum_cons]
          refine ⟨by omega, fun b hb hne => ?_⟩
          rcases List.mem_cons.mp hb with rfl | hbts
          · exact List.mem_cons_self ..
          · exact List.mem_cons_of_mem t (hkeep b hbts hne)
    obtain ⟨hsumS, hkeepS⟩ := herase S haS
    have hsub' : ∀ b ∈ as, b ∈ S.erase a := fun b hb =>
      hkeepS b (hsub b (List.mem_cons_of_mem a hb)) (fun hba => hnd.1 (hba ▸ hb))
    have hle := ih (S.erase a) hnd.2 hsub'
    simp only [List.map_cons, List.sum_cons]
    omega

theorem flatMap_nodup_and_sum (y : Nat → Nat) (f : Nat → List Nat) :
    ∀ (C : List Nat),
      (∀ x ∈ C, (f x).Nodup) →
      (∀ (i j : Nat) (hi : i < C.length) (hj : j < C.length), i ≠ j → ∀ d, ¬ (d ∈ f C[i] ∧ d ∈ f C[j])) →
      (C.flatMap f).Nodup ∧ ((C.flatMap f).map y).sum = (C.map (fun x => ((f x).map y).sum)).sum := by
  intro C
  induction C with
  | nil => intro _ _; simp
  | cons c cs ih =>
    intro hnd hdisj
    have hnd_cs : ∀ x ∈ cs, (f x).Nodup := fun x hx => hnd x (List.mem_cons_of_mem c hx)
    have hdisj_cs : ∀ (i j : Nat) (hi : i < cs.length) (hj : j < cs.length), i ≠ j →
        ∀ d, ¬ (d ∈ f cs[i] ∧ d ∈ f cs[j]) := fun i j hi hj hij d =>
      hdisj (i + 1) (j + 1) (Nat.succ_lt_succ hi) (Nat.succ_lt_succ hj) (by omega) d
    obtain ⟨hnd_tail, hsum_tail⟩ := ih hnd_cs hdisj_cs
    have hnd_head : (f c).Nodup := hnd c (List.mem_cons_self ..)
    have hdisj_head : ∀ d ∈ f c, d ∉ cs.flatMap f := by
      intro d hdc hdcs
      rw [List.mem_flatMap] at hdcs
      obtain ⟨x, hxcs, hdx⟩ := hdcs
      obtain ⟨k, hk, rfl⟩ := List.getElem_of_mem hxcs
      exact hdisj 0 (k + 1) (Nat.zero_lt_succ _) (Nat.succ_lt_succ hk) (by omega) d ⟨hdc, hdx⟩
    refine ⟨?_, ?_⟩
    · simp only [List.flatMap_cons]
      rw [List.nodup_append]
      exact ⟨hnd_head, hnd_tail, fun a ha b hb hab => hdisj_head a ha (hab ▸ hb)⟩
    · simp only [List.flatMap_cons, List.map_append, List.sum_append, List.map_cons, List.sum_cons, hsum_tail]

theorem mul_length_le_sum (D : Nat) (g : Nat → Nat) :
    ∀ (L : List Nat), (∀ x ∈ L, D ≤ g x) → D * L.length ≤ (L.map g).sum := by
  intro L
  induction L with
  | nil => intro _; simp
  | cons a as ih =>
    intro h
    have ha := h a (List.mem_cons_self ..)
    have has := ih (fun x hx => h x (List.mem_cons_of_mem a hx))
    simp only [List.length_cons, List.map_cons, List.sum_cons, Nat.mul_succ]
    omega

/-- Map packed `(i + 16*j)` witnesses to descendants of `x`. -/
def witDescs2 (x : Nat) (ps : List Nat) : List Nat :=
  ps.map fun p => del2Nat x (p % 16) (p / 16)

def witOk2 (n D : Nat) (y : Nat → Nat) (x : Nat) (ps : List Nat) : Bool :=
  ps.all (fun p => (p % 16 < p / 16) && (p / 16 < n)) &&
  isStrictAsc (witDescs2 x ps) &&
  (D ≤ ((witDescs2 x ps).map y).sum)

def checkDualTree2 (n D : Nat) (y : Nat → Nat) : Nat → Nat → DualTree → Bool
  | 0, x, .leaf ps => witOk2 n D y x ps
  | d + 1, x, .node l r =>
      checkDualTree2 n D y d (2 * x) l && checkDualTree2 n D y d (2 * x + 1) r
  | _, _, _ => false

private theorem mul_pow2_l (x d' y : Nat) : (2 * x) * 2 ^ d' + y = x * 2 ^ (d' + 1) + y := by
  rw [Nat.pow_succ, Nat.mul_comm 2 x, Nat.mul_assoc, Nat.mul_comm 2 (2 ^ d')]

private theorem mul_pow2_r (x d' y : Nat) (hge : ¬ y < 2 ^ d') :
    (2 * x + 1) * 2 ^ d' + (y - 2 ^ d') = x * 2 ^ (d' + 1) + y := by
  rw [Nat.add_mul, Nat.one_mul, Nat.pow_succ, Nat.mul_comm 2 x, Nat.mul_assoc, Nat.mul_comm 2 (2 ^ d')]
  omega

theorem checkDualTree2_spec (n D : Nat) (y : Nat → Nat) :
    ∀ (d x : Nat) (t : DualTree), checkDualTree2 n D y d x t = true →
      ∀ z < 2 ^ d, witOk2 n D y (x * 2 ^ d + z) (t.lookup d z) = true := by
  intro d
  induction d with
  | zero =>
    intro x t ht z hz
    have hz0 : z = 0 := by simpa using hz
    subst hz0
    cases t with
    | node _ _ => simp [checkDualTree2] at ht
    | leaf ps => simpa [DualTree.lookup, checkDualTree2] using ht
  | succ d' ih =>
    intro x t ht z hz
    cases t with
    | leaf _ => simp [checkDualTree2] at ht
    | node l r =>
      simp only [checkDualTree2, Bool.and_eq_true] at ht
      by_cases hlow : z < 2 ^ d'
      · simp only [DualTree.lookup, hlow, ↓reduceIte]
        have := ih (2 * x) l ht.1 z hlow
        rw [mul_pow2_l] at this
        exact this
      · simp only [DualTree.lookup, hlow, ↓reduceIte]
        have hhi : z - 2 ^ d' < 2 ^ d' := by rw [Nat.pow_succ] at hz; omega
        have := ih (2 * x + 1) r ht.2 (z - 2 ^ d') hhi
        rw [mul_pow2_r x d' z hlow] at this
        exact this

/-- General Weak LP Duality Upper Bound Theorem for `s = 2` via fast O(1)-checked DualTree! -/
theorem weak_duality_tree2 (n D : Nat) (hn : 2 ≤ n) (y : Nat → Nat) (t : DualTree)
    (ht : checkDualTree2 n D y n 0 t = true)
    (C : List Nat) (hval : IsValidDeletionCode n 2 C) :
    D * C.length ≤ ((List.range (2 ^ (n - 2))).map y).sum := by
  have hall : ∀ x < 2 ^ n, witOk2 n D y x (t.lookup n x) = true := fun x hx => by
    simpa using checkDualTree2_spec n D y n 0 t ht x hx
  let f : Nat → List Nat := fun x => witDescs2 x (t.lookup n x)
  have hf_spec : ∀ x < 2 ^ n, (f x).Nodup ∧ D ≤ ((f x).map y).sum ∧
      ∀ d ∈ f x, d < 2 ^ (n - 2) ∧ InDelBall 2 (natToWord n x) (natToWord (n - 2) d) := by
    intro x hx
    have hok := hall x hx
    unfold witOk2 at hok
    simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at hok
    refine ⟨strictAsc_nodup hok.1.2, hok.2, fun d hd => ?_⟩
    dsimp only [f, witDescs2] at hd
    rw [List.mem_map] at hd
    obtain ⟨p, hp, rfl⟩ := hd
    have hbounds := hok.1.1 p hp
    have ha := delBit_lt_pub n (p / 16) x hx hbounds.2
    have hb := delBit_lt_pub (n - 1) (p % 16) (delBit x (p / 16)) ha (by omega)
    have hsub2 : n - 1 - 1 = n - 2 := by omega
    refine ⟨by rw [del2Nat, ← hsub2]; exact hb,
            del2Nat_isSubseq hbounds.1 hbounds.2,
            by rw [natToWord_length, natToWord_length]; omega⟩
  have hnd_each : ∀ x ∈ C, (f x).Nodup := fun x hx => (hf_spec x (hval.1 x hx)).1
  have hdisj : ∀ (i j : Nat) (hi : i < C.length) (hj : j < C.length), i ≠ j →
      ∀ d, ¬ (d ∈ f C[i] ∧ d ∈ f C[j]) := by
    intro i j hi hj hij d ⟨hdi, hdj⟩
    have bi := ((hf_spec C[i] (hval.1 C[i] (List.getElem_mem hi))).2.2 d hdi).2
    have bj := ((hf_spec C[j] (hval.1 C[j] (List.getElem_mem hj))).2.2 d hdj).2
    exact (hval.2 i j hi hj hij).2.1 (natToWord (n - 2) d) ⟨bi, bj⟩
  obtain ⟨hnd_all, hsum_all⟩ := flatMap_nodup_and_sum y f C hnd_each hdisj
  have hsub_range : ∀ d ∈ C.flatMap f, d ∈ List.range (2 ^ (n - 2)) := by
    intro d hd
    rw [List.mem_flatMap] at hd
    obtain ⟨x, hxC, hdx⟩ := hd
    rw [List.mem_range]
    exact ((hf_spec x (hval.1 x hxC)).2.2 d hdx).1
  have hupper := sum_map_le_of_nodup_subset y (C.flatMap f) (List.range (2 ^ (n - 2))) hnd_all hsub_range
  have hlower := mul_length_le_sum D (fun x => ((f x).map y).sum) C (fun x hx => (hf_spec x (hval.1 x hx)).2.1)
  omega

/-- Map packed `(i + 16*j + 256*k)` witnesses to descendants of `x`. -/
def witDescs3 (x : Nat) (ps : List Nat) : List Nat :=
  ps.map fun p => del3Nat x (p % 16) ((p / 16) % 16) (p / 256)

def witOk3 (n D : Nat) (y : Nat → Nat) (x : Nat) (ps : List Nat) : Bool :=
  ps.all (fun p => (p % 16 < (p / 16) % 16) && ((p / 16) % 16 < p / 256) && (p / 256 < n)) &&
  isStrictAsc (witDescs3 x ps) &&
  (D ≤ ((witDescs3 x ps).map y).sum)

def checkDualTree3 (n D : Nat) (y : Nat → Nat) : Nat → Nat → DualTree → Bool
  | 0, x, .leaf ps => witOk3 n D y x ps
  | d + 1, x, .node l r =>
      checkDualTree3 n D y d (2 * x) l && checkDualTree3 n D y d (2 * x + 1) r
  | _, _, _ => false

theorem checkDualTree3_spec (n D : Nat) (y : Nat → Nat) :
    ∀ (d x : Nat) (t : DualTree), checkDualTree3 n D y d x t = true →
      ∀ z < 2 ^ d, witOk3 n D y (x * 2 ^ d + z) (t.lookup d z) = true := by
  intro d
  induction d with
  | zero =>
    intro x t ht z hz
    have hz0 : z = 0 := by simpa using hz
    subst hz0
    cases t with
    | node _ _ => simp [checkDualTree3] at ht
    | leaf ps => simpa [DualTree.lookup, checkDualTree3] using ht
  | succ d' ih =>
    intro x t ht z hz
    cases t with
    | leaf _ => simp [checkDualTree3] at ht
    | node l r =>
      simp only [checkDualTree3, Bool.and_eq_true] at ht
      by_cases hlow : z < 2 ^ d'
      · simp only [DualTree.lookup, hlow, ↓reduceIte]
        have := ih (2 * x) l ht.1 z hlow
        rw [mul_pow2_l] at this
        exact this
      · simp only [DualTree.lookup, hlow, ↓reduceIte]
        have hhi : z - 2 ^ d' < 2 ^ d' := by rw [Nat.pow_succ] at hz; omega
        have := ih (2 * x + 1) r ht.2 (z - 2 ^ d') hhi
        rw [mul_pow2_r x d' z hlow] at this
        exact this

/-- General Weak LP Duality Upper Bound Theorem for `s = 3` via fast O(1)-checked DualTree! -/
theorem weak_duality_tree3 (n D : Nat) (hn : 3 ≤ n) (y : Nat → Nat) (t : DualTree)
    (ht : checkDualTree3 n D y n 0 t = true)
    (C : List Nat) (hval : IsValidDeletionCode n 3 C) :
    D * C.length ≤ ((List.range (2 ^ (n - 3))).map y).sum := by
  have hall : ∀ x < 2 ^ n, witOk3 n D y x (t.lookup n x) = true := fun x hx => by
    simpa using checkDualTree3_spec n D y n 0 t ht x hx
  let f : Nat → List Nat := fun x => witDescs3 x (t.lookup n x)
  have hf_spec : ∀ x < 2 ^ n, (f x).Nodup ∧ D ≤ ((f x).map y).sum ∧
      ∀ d ∈ f x, d < 2 ^ (n - 3) ∧ InDelBall 3 (natToWord n x) (natToWord (n - 3) d) := by
    intro x hx
    have hok := hall x hx
    unfold witOk3 at hok
    simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true] at hok
    refine ⟨strictAsc_nodup hok.1.2, hok.2, fun d hd => ?_⟩
    dsimp only [f, witDescs3] at hd
    rw [List.mem_map] at hd
    obtain ⟨p, hp, rfl⟩ := hd
    have hbounds := hok.1.1 p hp
    have ha := delBit_lt_pub n (p / 256) x hx hbounds.2
    have hb := delBit_lt_pub (n - 1) ((p / 16) % 16) (delBit x (p / 256)) ha (by omega)
    have hc := delBit_lt_pub (n - 1 - 1) (p % 16) (delBit (delBit x (p / 256)) ((p / 16) % 16)) hb (by omega)
    have hsub3 : n - 1 - 1 - 1 = n - 3 := by omega
    refine ⟨by rw [del3Nat, ← hsub3]; exact hc,
            del3Nat_isSubseq hbounds.1.1 hbounds.1.2 hbounds.2,
            by rw [natToWord_length, natToWord_length]; omega⟩
  have hnd_each : ∀ x ∈ C, (f x).Nodup := fun x hx => (hf_spec x (hval.1 x hx)).1
  have hdisj : ∀ (i j : Nat) (hi : i < C.length) (hj : j < C.length), i ≠ j →
      ∀ d, ¬ (d ∈ f C[i] ∧ d ∈ f C[j]) := by
    intro i j hi hj hij d ⟨hdi, hdj⟩
    have bi := ((hf_spec C[i] (hval.1 C[i] (List.getElem_mem hi))).2.2 d hdi).2
    have bj := ((hf_spec C[j] (hval.1 C[j] (List.getElem_mem hj))).2.2 d hdj).2
    exact (hval.2 i j hi hj hij).2.1 (natToWord (n - 3) d) ⟨bi, bj⟩
  obtain ⟨hnd_all, hsum_all⟩ := flatMap_nodup_and_sum y f C hnd_each hdisj
  have hsub_range : ∀ d ∈ C.flatMap f, d ∈ List.range (2 ^ (n - 3)) := by
    intro d hd
    rw [List.mem_flatMap] at hd
    obtain ⟨x, hxC, hdx⟩ := hd
    rw [List.mem_range]
    exact ((hf_spec x (hval.1 x hxC)).2.2 d hdx).1
  have hupper := sum_map_le_of_nodup_subset y (C.flatMap f) (List.range (2 ^ (n - 3))) hnd_all hsub_range
  have hlower := mul_length_le_sum D (fun x => ((f x).map y).sum) C (fun x hx => (hf_spec x (hval.1 x hx)).2.1)
  omega

-- =============================================================================
-- EXACT GLOBAL OPTIMALITY #1: M_2(7) = 5 (BOTH LOWER BOUND AND DUAL UPPER BOUND!)
-- =============================================================================

def y_7_2 : Nat → Nat
  | 0 => 17 | 1 => 3 | 3 => 7 | 5 => 2 | 6 => 2 | 7 => 7 | 10 => 1 | 11 => 2
  | 12 => 2 | 14 => 3 | 15 => 3 | 16 => 3 | 17 => 3 | 19 => 2 | 20 => 2 | 21 => 1
  | 24 => 7 | 25 => 2 | 26 => 2 | 28 => 7 | 30 => 3 | 31 => 17
  | _ => 0

private def dualTree_7_2 : DualTree := (DN (DN (DN (DN (DN (DN (DN (DL [16]) (DL [16])) (DN (DL [16]) (DL [16]))) (DN (DN (DL [32]) (DL [32])) (DN (DL [33]) (DL [16, 48, 67])))) (DN (DN (DN (DL [48]) (DL [48])) (DN (DL [49]) (DL [48, 32, 66]))) (DN (DN (DL [50]) (DL [50, 16, 65])) (DN (DL [16, 64, 84]) (DL [16, 64, 84]))))) (DN (DN (DN (DN (DL [64]) (DL [64])) (DN (DL [65]) (DL [64, 66, 50]))) (DN (DN (DL [66]) (DL [66, 65, 49])) (DN (DL [64, 48, 83]) (DL [64, 48, 83])))) (DN (DN (DN (DL [67]) (DL [67, 49, 16, 33, 80, 101])) (DN (DL [48, 16, 32, 81, 82, 101]) (DL [67, 32, 82]))) (DN (DN (DL [16, 80, 101]) (DL [50, 32, 16, 80, 81])) (DN (DL [33, 16, 81, 80, 101]) (DL [101])))))) (DN (DN (DN (DN (DN (DL [80]) (DL [80])) (DN (DL [81]) (DL [80, 82, 50, 96, 98]))) (DN (DN (DL [82]) (DL [82, 81, 83, 98, 97])) (DN (DL [80, 83, 49, 48, 67, 96]) (DL [80, 83, 67])))) (DN (DN (DN (DL [83]) (DL [83, 81, 33, 64, 99, 96, 97, 100])) (DN (DL [80, 82, 16, 32, 65, 66, 97, 96, 100]) (DL [83, 82, 66]))) (DN (DN (DL [80, 16, 66, 64, 98, 100]) (DL [82, 80, 81, 64, 65])) (DN (DL [81, 80, 65, 64, 100]) (DL [100]))))) (DN (DN (DN (DN (DL [84]) (DL [84, 16, 100, 96, 97])) (DN (DL [66, 16, 50, 97, 96, 98]) (DL [84, 66, 16, 50, 100, 96]))) (DN (DN (DL [48, 98, 99]) (DL [84, 65, 32, 48, 49, 100, 98, 96])) (DN (DL [84, 64, 33, 49, 48, 97, 99]) (DL [99])))) (DN (DN (DN (DL [16, 99, 96]) (DL [48, 16, 33, 99, 96])) (DN (DL [16, 32, 99, 97, 98]) (DL [98]))) (DN (DN (DL [50, 32, 16, 98, 96]) (DL [97])) (DN (DL [96]) (DL [96]))))))) (DN (DN (DN (DN (DN (DN (DL [96]) (DL [96])) (DN (DL [97]) (DL [96, 98, 16, 32, 50]))) (DN (DN (DL [98]) (DL [98, 97, 99, 32, 16])) (DN (DL [96, 99, 33, 16, 48]) (DL [96, 99, 16])))) (DN (DN (DN (DL [99]) (DL [99, 97, 48, 49, 33, 64, 84])) (DN (DL [96, 98, 100, 49, 48, 32, 65, 84]) (DL [99, 98, 48]))) (DN (DN (DL [96, 100, 50, 16, 66, 84]) (DL [98, 96, 97, 50, 16, 66])) (DN (DL [97, 96, 100, 16, 84]) (DL [84]))))) (DN (DN (DN (DN (DL [100]) (DL [100, 64, 65, 80, 81])) (DN (DL [65, 64, 81, 80, 82]) (DL [100, 98, 64, 66, 16, 80]))) (DN (DN (DL [66, 82, 83]) (DL [100, 96, 97, 66, 65, 32, 16, 82, 80])) (DN (DL [100, 97, 96, 99, 64, 33, 81, 83]) (DL [83])))) (DN (DN (DN (DL [67, 83, 80]) (DL [96, 67, 48, 49, 83, 80])) (DN (DL [97, 98, 83, 81, 82]) (DL [82]))) (DN (DN (DL [98, 96, 50, 82, 80]) (DL [81])) (DN (DL [80]) (DL [80])))))) (DN (DN (DN (DN (DN (DL [101]) (DL [101, 80, 81, 16, 33])) (DN (DL [81, 80, 16, 32, 50]) (DL [101, 80, 16]))) (DN (DN (DL [82, 32, 67]) (DL [101, 82, 81, 32, 16, 48])) (DN (DL [101, 80, 33, 16, 49, 67]) (DL [67])))) (DN (DN (DN (DL [83, 48, 64]) (DL [83, 48, 64])) (DN (DL [49, 65, 66]) (DL [66]))) (DN (DN (DL [50, 66, 64]) (DL [65])) (DN (DL [64]) (DL [64]))))) (DN (DN (DN (DN (DL [84, 64, 16]) (DL [84, 64, 16])) (DN (DL [65, 16, 50]) (DL [50]))) (DN (DN (DL [66, 32, 48]) (DL [49])) (DN (DL [48]) (DL [48])))) (DN (DN (DN (DL [67, 48, 16]) (DL [33])) (DN (DL [32]) (DL [32]))) (DN (DN (DL [16]) (DL [16])) (DN (DL [16]) (DL [16]))))))))

theorem y_7_2_feas : checkDualTree2 7 17 y_7_2 7 0 dualTree_7_2 = true := by rfl
theorem y_7_2_sum : ((List.range (2 ^ 5)).map y_7_2).sum = 98 := by rfl

theorem upper_bound_7_2 (C : List Nat) (hval : IsValidDeletionCode 7 2 C) : C.length ≤ 5 := by
  have h := weak_duality_tree2 7 17 (by decide) y_7_2 dualTree_7_2 y_7_2_feas C hval
  rw [y_7_2_sum] at h
  omega

def BitTrie.insert : Nat → BitTrie → Nat → Nat → BitTrie
  | 0, _, _, v => .leaf v
  | k + 1, .empty, idx, v =>
      if idx % 2 == 0 then .node (BitTrie.insert k .empty (idx / 2) v) .empty
      else .node .empty (BitTrie.insert k .empty (idx / 2) v)
  | k + 1, .node l r, idx, v =>
      if idx % 2 == 0 then .node (BitTrie.insert k l (idx / 2) v) r
      else .node l (BitTrie.insert k r (idx / 2) v)
  | _, t, _, _ => t

def rawBall2 (n x : Nat) : List Nat :=
  (List.range n).flatMap fun j => (List.range j).map fun i => del2Nat x i j

def rawBall3 (n x : Nat) : List Nat :=
  (List.range n).flatMap fun k => (List.range k).flatMap fun j => (List.range j).map fun i => del3Nat x i j k

def buildOwner2 (n : Nat) (C : List Nat) : BitTrie :=
  let rec go (idx : Nat) (t : BitTrie) : List Nat → BitTrie
    | [] => t
    | x :: xs => go (idx + 1) ((rawBall2 n x).foldl (fun acc d => BitTrie.insert (n - 2) acc d (idx + 1)) t) xs
  go 0 .empty C

def buildOwner3 (n : Nat) (C : List Nat) : BitTrie :=
  let rec go (idx : Nat) (t : BitTrie) : List Nat → BitTrie
    | [] => t
    | x :: xs => go (idx + 1) ((rawBall3 n x).foldl (fun acc d => BitTrie.insert (n - 3) acc d (idx + 1)) t) xs
  go 0 .empty C

def opt_code_7_2 : List Nat := [0, 30, 41, 112, 127]

theorem opt_code_7_2_valid : IsValidDeletionCode 7 2 opt_code_7_2 :=
  checkCode2_sound 7 (by decide) (buildOwner2 7 opt_code_7_2) opt_code_7_2 (by rfl)

/-- EXACT GLOBAL OPTIMALITY: `M_2(7) = 5` (constructive lower bound + dual LP upper bound, 0 sorryAx). -/
theorem exact_opt_7_2 :
    (∃ C, C.length = 5 ∧ IsValidDeletionCode 7 2 C) ∧
    (∀ C, IsValidDeletionCode 7 2 C → C.length ≤ 5) :=
  ⟨⟨opt_code_7_2, rfl, opt_code_7_2_valid⟩, upper_bound_7_2⟩

-- =============================================================================
-- EXACT GLOBAL OPTIMALITY #2: M_3(9) = 5 (ONLY 14 NONZERO DUAL WEIGHTS, 22/4 = 5.5!)
-- =============================================================================

def y_9_3 : Nat → Nat
  | 0 => 4 | 3 => 1 | 7 => 2 | 11 => 1 | 12 => 1 | 15 => 1
  | 30 => 1 | 33 => 1 | 48 => 1 | 51 => 1 | 52 => 1 | 56 => 2 | 60 => 1 | 63 => 4
  | _ => 0

private def dw9_0 : DualTree := (DN (DN (DN (DN (DN (DN (DL [528]) (DL [528])) (DN (DL [528]) (DL [528]))) (DN (DN (DL [528]) (DL [528])) (DN (DL [528]) (DL [528])))) (DN (DN (DN (DL [784]) (DL [784])) (DN (DL [784]) (DL [784]))) (DN (DN (DL [800]) (DL [800])) (DN (DL [801]) (DL [1040, 1344, 1620]))))) (DN (DN (DN (DN (DL [1040]) (DL [1040])) (DN (DL [1040]) (DL [1040]))) (DN (DN (DL [1056]) (DL [1056])) (DN (DL [1057]) (DL [1328, 1616, 1619])))) (DN (DN (DN (DL [1072]) (DL [1072])) (DN (DL [1073]) (DL [1312, 1619, 1618]))) (DN (DN (DL [1074]) (DL [528, 1296, 1617])) (DN (DL [1296, 1616, 1893]) (DL [528, 1296, 1616])))))) (DN (DN (DN (DN (DN (DL [1296]) (DL [1296])) (DN (DL [1296]) (DL [1296]))) (DN (DN (DL [1312]) (DL [1312])) (DN (DL [1313]) (DL [1072, 1584, 1603])))) (DN (DN (DN (DL [1328]) (DL [1328])) (DN (DL [1329]) (DL [1056, 1568, 1602]))) (DN (DN (DL [1330]) (DL [1040, 1552, 1601])) (DN (DL [1040, 1600, 1892]) (DL [1040, 1552, 1600]))))) (DN (DN (DN (DN (DL [1344]) (DL [1344])) (DN (DL [1345]) (DL [800, 1602, 2166]))) (DN (DN (DL [1346]) (DL [1345, 784, 1601])) (DN (DL [784, 1569, 1891]) (DL [1344, 784, 1600])))) (DN (DN (DN (DL [1347]) (DL [528, 1584, 1569])) (DN (DL [528, 1585, 1890]) (DL [1347, 528, 1603]))) (DN (DN (DL [528, 1586, 2166]) (DL [528, 1552, 1888])) (DN (DL [528, 1552, 1889]) (DL [2166])))))))
private def dw9_1 : DualTree := (DN (DN (DN (DN (DN (DN (DL [1552]) (DL [1552])) (DN (DL [1552]) (DL [1552]))) (DN (DN (DL [1568]) (DL [1568])) (DN (DL [1569]) (DL [1584, 1603, 1347])))) (DN (DN (DN (DL [1584]) (DL [1584])) (DN (DL [1585]) (DL [1568, 1602, 1346]))) (DN (DN (DL [1586]) (DL [1552, 1601, 1345])) (DN (DL [1600, 1344, 1876]) (DL [1552, 1600, 1344]))))) (DN (DN (DN (DN (DL [1600]) (DL [1600])) (DN (DL [1601]) (DL [1602, 1586, 2165]))) (DN (DN (DL [1602]) (DL [1601, 1585, 1329])) (DN (DL [1584, 1313, 1875]) (DL [1600, 1584, 1328])))) (DN (DN (DN (DL [1603]) (DL [1569, 1328, 1313])) (DN (DL [1568, 1329, 1874]) (DL [1603, 1568, 1312]))) (DN (DN (DL [1552, 1330, 2165]) (DL [1552, 1296, 1872])) (DN (DL [1552, 1296, 1873]) (DL [2165])))))) (DN (DN (DN (DN (DN (DL [1616]) (DL [1616])) (DN (DL [1617]) (DL [1618, 1330, 1074, 2162]))) (DN (DN (DL [1618]) (DL [1617, 1329, 1073, 2161])) (DN (DL [1616, 1328, 1859, 2160]) (DL [1616, 1619, 2160])))) (DN (DN (DN (DL [1619]) (DL [1313, 784, 1057, 2160])) (DN (DL [1312, 1056, 1858, 2161]) (DL [1619, 1618, 2163]))) (DN (DN (DL [800, 1856, 2162, 2164]) (DL [1617, 800, 1856])) (DN (DL [1616, 801, 1857]) (DL [2164]))))) (DN (DN (DN (DN (DL [1620]) (DL [1040, 801, 2160])) (DN (DL [800, 1842, 2161]) (DL [1620, 1346, 800, 2164]))) (DN (DN (DL [2164, 2162, 2163]) (DL [1345, 1056, 784, 1840])) (DN (DL [1344, 1057, 784, 1841]) (DL [2163])))) (DN (DN (DN (DL [1072, 2163, 2160]) (DL [1072, 528, 1808, 2160])) (DN (DL [1073, 528, 1808, 2161]) (DL [2162]))) (DN (DN (DL [1074, 528, 1824, 2162]) (DL [2161])) (DN (DL [2160]) (DL [2160])))))))
private def dw9_2 : DualTree := (DN (DN (DN (DN (DN (DN (DL [1808]) (DL [1808])) (DN (DL [1808]) (DL [1808]))) (DN (DN (DL [1824]) (DL [1824])) (DN (DL [1825]) (DL [1840, 1859, 2064])))) (DN (DN (DN (DL [1840]) (DL [1840])) (DN (DL [1841]) (DL [1858, 1876, 2096]))) (DN (DN (DL [1842]) (DL [1808, 1857, 2098])) (DN (DL [1808, 1856, 1620]) (DL [1808, 1856, 1876]))))) (DN (DN (DN (DN (DL [1856]) (DL [1856])) (DN (DL [1857]) (DL [1842, 1874, 2149]))) (DN (DN (DL [1858]) (DL [1841, 1873, 2114])) (DN (DL [1840, 1872, 1619]) (DL [1840, 1872, 1875])))) (DN (DN (DN (DL [1859]) (DL [1825, 1872, 2115])) (DN (DL [1824, 1873, 1618]) (DL [1859, 1824, 1875]))) (DN (DN (DL [1808, 1874, 2149]) (DL [1808, 1873, 1616])) (DN (DL [1808, 1872, 1617]) (DL [2149])))))) (DN (DN (DN (DN (DN (DL [1872]) (DL [1872])) (DN (DL [1873]) (DL [1874, 1842, 2128, 2146]))) (DN (DN (DL [1874]) (DL [1873, 1841, 2130, 2145])) (DN (DL [1872, 1840, 1603, 2144]) (DL [1875, 1859, 2144])))) (DN (DN (DN (DL [1875]) (DL [1825, 1856, 2131, 2144])) (DN (DL [1824, 1857, 1602, 2145]) (DL [1875, 1874, 2147]))) (DN (DN (DL [1858, 1600, 2146, 2148]) (DL [1873, 1857, 1600])) (DN (DL [1872, 1856, 1601]) (DL [2148]))))) (DN (DN (DN (DN (DL [1876]) (DL [1808, 2132, 2144])) (DN (DL [1808, 1586, 2145]) (DL [1876, 1858, 1842, 2148]))) (DN (DN (DL [2148, 2146, 2147]) (DL [1857, 1824, 1841, 1584])) (DN (DL [1856, 1825, 1840, 1585]) (DL [2147])))) (DN (DN (DN (DL [1840, 2147, 2144]) (DL [1840, 1825, 1552, 2144])) (DN (DL [1841, 1824, 1552, 2145]) (DL [2146]))) (DN (DN (DL [1842, 1808, 1568, 2146]) (DL [2145])) (DN (DL [2144]) (DL [2144])))))))
private def dw9_3 : DualTree := (DN (DN (DN (DN (DN (DN (DL [1888]) (DL [1888])) (DN (DL [1889]) (DL [1890, 2144, 2064, 2098]))) (DN (DN (DL [1890]) (DL [1889, 2146, 2080, 2097])) (DN (DL [1888, 1347, 2081, 2096]) (DL [1888, 1891, 2096])))) (DN (DN (DN (DL [1891]) (DL [2147, 2096, 2081, 2112])) (DN (DL [1346, 2097, 2080, 2113]) (DL [1891, 1890, 1892]))) (DN (DN (DL [1892, 2098, 2114, 2132]) (DL [1889, 1344, 2064])) (DN (DL [1888, 1345, 2064]) (DL [2132]))))) (DN (DN (DN (DN (DL [1892]) (DL [2148, 2112, 2128])) (DN (DL [1330, 2113, 2129]) (DL [1892, 1890, 2114, 2064]))) (DN (DN (DL [1891, 2130, 2131]) (DL [1889, 1328, 2113, 2080])) (DN (DL [1888, 1329, 2112, 2081]) (DL [2131])))) (DN (DN (DN (DL [1888, 2115, 2131]) (DL [1888, 1296, 2096, 2128])) (DN (DL [1889, 1296, 2097, 2129]) (DL [2130]))) (DN (DN (DL [1890, 1312, 2098, 2130]) (DL [2129])) (DN (DL [2128]) (DL [2128])))))) (DN (DN (DN (DN (DN (DL [1893]) (DL [2149, 2128, 2064])) (DN (DL [1074, 2129, 2064]) (DL [1893, 2130, 2064]))) (DN (DN (DL [2131, 2080, 2115]) (DL [1072, 2129, 2080])) (DN (DL [1073, 2128, 2081]) (DL [2115])))) (DN (DN (DN (DL [2131, 2128, 2096]) (DL [2128, 2096, 2112])) (DN (DL [2129, 2097, 2113]) (DL [2114]))) (DN (DN (DL [1893, 2130, 2098]) (DL [2113])) (DN (DL [2112]) (DL [2112]))))) (DN (DN (DN (DN (DL [2132, 2112, 2064]) (DL [528, 2112, 2064])) (DN (DL [528, 2113, 2064]) (DL [2098]))) (DN (DN (DL [2132, 2114, 2080]) (DL [2097])) (DN (DL [2096]) (DL [2096])))) (DN (DN (DN (DL [784, 2115, 2096]) (DL [2081])) (DN (DL [2080]) (DL [2080]))) (DN (DN (DL [2064]) (DL [2064])) (DN (DL [2064]) (DL [2064])))))))
private def dw9_4 : DualTree := (DN (DN (DN (DN (DN (DN (DL [2064]) (DL [2064])) (DN (DL [2064]) (DL [2064]))) (DN (DN (DL [2080]) (DL [2080])) (DN (DL [2081]) (DL [2096, 2115, 784])))) (DN (DN (DN (DL [2096]) (DL [2096])) (DN (DL [2097]) (DL [2080, 2114, 2132]))) (DN (DN (DL [2098]) (DL [2064, 2113, 528])) (DN (DL [2064, 2112, 528]) (DL [2064, 2112, 2132]))))) (DN (DN (DN (DN (DL [2112]) (DL [2112])) (DN (DL [2113]) (DL [2098, 2130, 1893]))) (DN (DN (DL [2114]) (DL [2113, 2097, 2129])) (DN (DL [2112, 2096, 2128]) (DL [2096, 2128, 2131])))) (DN (DN (DN (DL [2115]) (DL [2081, 2128, 1073])) (DN (DL [2080, 2129, 1072]) (DL [2115, 2080, 2131]))) (DN (DN (DL [2064, 2130, 1893]) (DL [2064, 2129, 1074])) (DN (DL [2064, 2128, 2149]) (DL [1893])))))) (DN (DN (DN (DN (DN (DL [2128]) (DL [2128])) (DN (DL [2129]) (DL [2130, 2098, 1312, 1890]))) (DN (DN (DL [2130]) (DL [2129, 2097, 1296, 1889])) (DN (DL [2128, 2096, 1296, 1888]) (DL [2131, 2115, 1888])))) (DN (DN (DN (DL [2131]) (DL [2081, 2112, 1329, 1888])) (DN (DL [2080, 2113, 1328, 1889]) (DL [2131, 2130, 1891]))) (DN (DN (DL [2064, 2114, 1890, 1892]) (DL [2129, 2113, 1330])) (DN (DL [2128, 2112, 2148]) (DL [1892]))))) (DN (DN (DN (DN (DL [2132]) (DL [2064, 1345, 1888])) (DN (DL [2064, 1344, 1889]) (DL [2132, 2114, 2098, 1892]))) (DN (DN (DL [1892, 1890, 1891]) (DL [2113, 2080, 2097, 1346])) (DN (DL [2112, 2081, 2096, 2147]) (DL [1891])))) (DN (DN (DN (DL [2096, 1891, 1888]) (DL [2096, 2081, 1347, 1888])) (DN (DL [2097, 2080, 2146, 1889]) (DL [1890]))) (DN (DN (DL [2098, 2064, 2144, 1890]) (DL [1889])) (DN (DL [1888]) (DL [1888])))))))
private def dw9_5 : DualTree := (DN (DN (DN (DN (DN (DN (DL [2144]) (DL [2144])) (DN (DL [2145]) (DL [2146, 1568, 1808, 1842]))) (DN (DN (DL [2146]) (DL [2145, 1552, 1824, 1841])) (DN (DL [2144, 1552, 1825, 1840]) (DL [2144, 2147, 1840])))) (DN (DN (DN (DL [2147]) (DL [1585, 1840, 1825, 1856])) (DN (DL [1584, 1841, 1824, 1857]) (DL [2147, 2146, 2148]))) (DN (DN (DL [2148, 1842, 1858, 1876]) (DL [2145, 1586, 1808])) (DN (DL [2144, 2132, 1808]) (DL [1876]))))) (DN (DN (DN (DN (DL [2148]) (DL [1601, 1856, 1872])) (DN (DL [1600, 1857, 1873]) (DL [2148, 2146, 1600, 1858]))) (DN (DN (DL [2147, 1874, 1875]) (DL [2145, 1602, 1857, 1824])) (DN (DL [2144, 2131, 1856, 1825]) (DL [1875])))) (DN (DN (DN (DL [2144, 1859, 1875]) (DL [2144, 1603, 1840, 1872])) (DN (DL [2145, 2130, 1841, 1873]) (DL [1874]))) (DN (DN (DL [2146, 2128, 1842, 1874]) (DL [1873])) (DN (DL [1872]) (DL [1872])))))) (DN (DN (DN (DN (DN (DL [2149]) (DL [1617, 1872, 1808])) (DN (DL [1616, 1873, 1808]) (DL [2149, 1874, 1808]))) (DN (DN (DL [1875, 1824, 1859]) (DL [1618, 1873, 1824])) (DN (DL [2115, 1872, 1825]) (DL [1859])))) (DN (DN (DN (DL [1875, 1872, 1840]) (DL [1619, 1872, 1840])) (DN (DL [2114, 1873, 1841]) (DL [1858]))) (DN (DN (DL [2149, 1874, 1842]) (DL [1857])) (DN (DL [1856]) (DL [1856]))))) (DN (DN (DN (DN (DL [1876, 1856, 1808]) (DL [1620, 1856, 1808])) (DN (DL [2098, 1857, 1808]) (DL [1842]))) (DN (DN (DL [2096, 1876, 1858]) (DL [1841])) (DN (DL [1840]) (DL [1840])))) (DN (DN (DN (DL [2064, 1859, 1840]) (DL [1825])) (DN (DL [1824]) (DL [1824]))) (DN (DN (DL [1808]) (DL [1808])) (DN (DL [1808]) (DL [1808])))))))
private def dw9_6 : DualTree := (DN (DN (DN (DN (DN (DN (DL [2160]) (DL [2160])) (DN (DL [2161]) (DL [2162, 1824, 528, 1074]))) (DN (DN (DL [2162]) (DL [2161, 1808, 528, 1073])) (DN (DL [2160, 1808, 528, 1072]) (DL [2160, 2163, 1072])))) (DN (DN (DN (DL [2163]) (DL [1841, 784, 1057, 1344])) (DN (DL [1840, 784, 1056, 1345]) (DL [2163, 2162, 2164]))) (DN (DN (DL [2164, 800, 1346, 1620]) (DL [2161, 1842, 800])) (DN (DL [2160, 801, 1040]) (DL [1620]))))) (DN (DN (DN (DN (DL [2164]) (DL [1857, 801, 1616])) (DN (DL [1856, 800, 1617]) (DL [2164, 2162, 1856, 800]))) (DN (DN (DL [2163, 1618, 1619]) (DL [2161, 1858, 1056, 1312])) (DN (DL [2160, 1057, 784, 1313]) (DL [1619])))) (DN (DN (DN (DL [2160, 1619, 1616]) (DL [2160, 1859, 1328, 1616])) (DN (DL [2161, 1073, 1329, 1617]) (DL [1618]))) (DN (DN (DL [2162, 1074, 1330, 1618]) (DL [1617])) (DN (DL [1616]) (DL [1616])))))) (DN (DN (DN (DN (DN (DL [2165]) (DL [1873, 1296, 1552])) (DN (DL [1872, 1296, 1552]) (DL [2165, 1330, 1552]))) (DN (DN (DL [1312, 1568, 1603]) (DL [1874, 1329, 1568])) (DN (DL [1313, 1328, 1569]) (DL [1603])))) (DN (DN (DN (DL [1328, 1584, 1600]) (DL [1875, 1313, 1584])) (DN (DL [1329, 1585, 1601]) (DL [1602]))) (DN (DN (DL [2165, 1586, 1602]) (DL [1601])) (DN (DL [1600]) (DL [1600]))))) (DN (DN (DN (DN (DL [1344, 1600, 1552]) (DL [1876, 1344, 1600])) (DN (DL [1345, 1601, 1552]) (DL [1586]))) (DN (DN (DL [1346, 1602, 1568]) (DL [1585])) (DN (DL [1584]) (DL [1584])))) (DN (DN (DN (DL [1347, 1603, 1584]) (DL [1569])) (DN (DL [1568]) (DL [1568]))) (DN (DN (DL [1552]) (DL [1552])) (DN (DL [1552]) (DL [1552])))))))
private def dw9_7 : DualTree := (DN (DN (DN (DN (DN (DN (DL [2166]) (DL [1889, 1552, 528])) (DN (DL [1888, 1552, 528]) (DL [2166, 1586, 528]))) (DN (DN (DL [1603, 528, 1347]) (DL [1890, 1585, 528])) (DN (DL [1569, 1584, 528]) (DL [1347])))) (DN (DN (DN (DL [1600, 784, 1344]) (DL [1891, 1569, 784])) (DN (DL [1601, 784, 1345]) (DL [1346]))) (DN (DN (DL [2166, 1602, 800]) (DL [1345])) (DN (DL [1344]) (DL [1344]))))) (DN (DN (DN (DN (DL [1600, 1552, 1040]) (DL [1892, 1600, 1040])) (DN (DL [1601, 1552, 1040]) (DL [1330]))) (DN (DN (DL [1602, 1568, 1056]) (DL [1329])) (DN (DL [1328]) (DL [1328])))) (DN (DN (DN (DL [1603, 1584, 1072]) (DL [1313])) (DN (DL [1312]) (DL [1312]))) (DN (DN (DL [1296]) (DL [1296])) (DN (DL [1296]) (DL [1296])))))) (DN (DN (DN (DN (DN (DL [1616, 1296, 528]) (DL [1893, 1616, 1296])) (DN (DL [1617, 1296, 528]) (DL [1074]))) (DN (DN (DL [1618, 1619, 1312]) (DL [1073])) (DN (DL [1072]) (DL [1072])))) (DN (DN (DN (DL [1619, 1616, 1328]) (DL [1057])) (DN (DL [1056]) (DL [1056]))) (DN (DN (DL [1040]) (DL [1040])) (DN (DL [1040]) (DL [1040]))))) (DN (DN (DN (DN (DL [1620, 1344, 1040]) (DL [801])) (DN (DL [800]) (DL [800]))) (DN (DN (DL [784]) (DL [784])) (DN (DL [784]) (DL [784])))) (DN (DN (DN (DL [528]) (DL [528])) (DN (DL [528]) (DL [528]))) (DN (DN (DL [528]) (DL [528])) (DN (DL [528]) (DL [528])))))))
private def dualTree_9_3 : DualTree := (DN (DN (DN dw9_0 dw9_1) (DN dw9_2 dw9_3)) (DN (DN dw9_4 dw9_5) (DN dw9_6 dw9_7)))

set_option maxHeartbeats 2000000 in
theorem y_9_3_feas : checkDualTree3 9 4 y_9_3 9 0 dualTree_9_3 = true := by rfl
theorem y_9_3_sum : ((List.range (2 ^ 6)).map y_9_3).sum = 22 := by rfl

theorem upper_bound_9_3 (C : List Nat) (hval : IsValidDeletionCode 9 3 C) : C.length ≤ 5 := by
  have h := weak_duality_tree3 9 4 (by decide) y_9_3 dualTree_9_3 y_9_3_feas C hval
  rw [y_9_3_sum] at h
  omega

def opt_code_9_3 : List Nat := [0, 118, 327, 480, 511]

theorem opt_code_9_3_valid : IsValidDeletionCode 9 3 opt_code_9_3 :=
  checkCode3_sound 9 (by decide) (buildOwner3 9 opt_code_9_3) opt_code_9_3 (by rfl)

/-- EXACT GLOBAL OPTIMALITY: `M_3(9) = 5` (constructive lower bound + exact 14-weight dual LP upper bound, 0 sorryAx). -/
theorem exact_opt_9_3 :
    (∃ C, C.length = 5 ∧ IsValidDeletionCode 9 3 C) ∧
    (∀ C, IsValidDeletionCode 9 3 C → C.length ≤ 5) :=
  ⟨⟨opt_code_9_3, rfl, opt_code_9_3_valid⟩, upper_bound_9_3⟩

-- =============================================================================
-- KLEIN-4 <c, r> SYMMETRY CERTIFICATE FOR OUR RECORD (16, 3) = 44 CODEBOOK
-- =============================================================================

def bitComp (n x : Nat) : Nat := (2 ^ n - 1) - x

def bitRev (n x : Nat) : Nat :=
  let rec go : Nat → Nat → Nat → Nat
    | 0, _, acc => acc
    | k + 1, cur, acc => go k (cur / 2) (2 * acc + cur % 2)
  go n x 0

/-- Pure-kernel proof that our record `(16, 3) = 44` codebook (`Cert_16_3.code`) is strictly invariant
    under BOTH bit-complement `c` and string reversal `r` (generating the full Klein-4 group `V_4 = <c, r>`). -/
theorem cert_16_3_klein4_invariant :
    ∀ x ∈ DeletionCode.Cert_16_3.code,
      bitComp 16 x ∈ DeletionCode.Cert_16_3.code ∧
      bitRev 16 x ∈ DeletionCode.Cert_16_3.code := by
  decide

end DeletionCode.DualLP
