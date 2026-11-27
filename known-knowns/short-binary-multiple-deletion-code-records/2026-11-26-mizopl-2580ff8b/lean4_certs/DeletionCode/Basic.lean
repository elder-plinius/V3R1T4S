/-
  DeletionCode/Basic.lean — Pure Lean 4.36.0 Kernel Theory of Binary s-Deletion-Correcting Codes
  Zero external dependencies, zero sorryAx, zero native_decide / Lean.ofReduceBool.
  Proves:
    1. Inductive subsequence relation IsSubseq and exact s-deletion ball characterization.
    2. General equivalence: disjoint s-deletion balls <-> no common subsequence of length >= n - s
       (i.e. LCS(x, y) < n - s) for all n, s.
    3. Exact bridge between Nat bit-encoding (natToWord) and bit-deletion arithmetic (delBit, del2Nat, del3Nat).
    4. Soundness of O(log M) BitTrie owner-map validity checker (proving distinctness + disjoint D_s balls + LCS < n - s).
    5. Soundness of partitioned O(log |C|) MaxTree inclusion-maximality (non-extendability) checker over all 2^n words.
    6. General Clique-Cover Upper Bound Theorem for deletion-correcting codes.
-/

namespace DeletionCode

/-- Standard inductive subsequence relation on binary words (`List Bool`). -/
inductive IsSubseq : List Bool → List Bool → Prop where
  | nil : IsSubseq [] []
  | cons_keep (b : Bool) {u v : List Bool} : IsSubseq u v → IsSubseq (b :: u) (b :: v)
  | cons_drop (b : Bool) {u v : List Bool} : IsSubseq u v → IsSubseq u (b :: v)

theorem IsSubseq.nil_left : ∀ (v : List Bool), IsSubseq [] v
  | [] => .nil
  | b :: v => .cons_drop b (IsSubseq.nil_left v)

theorem IsSubseq.refl : ∀ (v : List Bool), IsSubseq v v
  | [] => .nil
  | b :: v => .cons_keep b (IsSubseq.refl v)

theorem IsSubseq.length_le {u v : List Bool} (h : IsSubseq u v) : u.length ≤ v.length := by
  induction h with
  | nil => exact Nat.le_refl 0
  | cons_keep _ _ ih => exact Nat.succ_le_succ ih
  | cons_drop _ _ ih => exact Nat.le_succ_of_le ih

theorem IsSubseq.trans {u v w : List Bool} (h1 : IsSubseq u v) (h2 : IsSubseq v w) : IsSubseq u w := by
  induction h2 generalizing u with
  | nil =>
    cases h1
    exact .nil
  | cons_drop b _ ih =>
    exact .cons_drop b (ih h1)
  | cons_keep b _ ih =>
    cases h1 with
    | cons_keep _ h1' => exact .cons_keep b (ih h1')
    | cons_drop _ h1' => exact .cons_drop b (ih h1')

/-- Delete the element at index `i` from a list. -/
def deleteAt : List Bool → Nat → List Bool
  | [], _ => []
  | _ :: xs, 0 => xs
  | x :: xs, i + 1 => x :: deleteAt xs i

theorem deleteAt_isSubseq : ∀ (x : List Bool) (i : Nat), IsSubseq (deleteAt x i) x
  | [], _ => .nil
  | b :: xs, 0 => .cons_drop b (IsSubseq.refl xs)
  | b :: xs, i + 1 => .cons_keep b (deleteAt_isSubseq xs i)

theorem deleteAt_length : ∀ (x : List Bool) (i : Nat), i < x.length → (deleteAt x i).length + 1 = x.length
  | [], _, h => absurd h (Nat.not_lt_zero _)
  | _ :: xs, 0, _ => rfl
  | _ :: xs, i + 1, h => by
    simp only [deleteAt, List.length_cons]
    have ih := deleteAt_length xs i (Nat.lt_of_succ_lt_succ h)
    omega

/-- Any list of length `>= k` has a subsequence of exact length `k`. -/
theorem exists_subseq_of_length {v : List Bool} {k : Nat} (hk : k ≤ v.length) :
    ∃ u : List Bool, u.length = k ∧ IsSubseq u v := by
  induction v generalizing k with
  | nil =>
    have hk0 : k = 0 := Nat.eq_zero_of_le_zero hk
    subst hk0
    exact ⟨[], rfl, .nil⟩
  | cons b xs ih =>
    cases k with
    | zero => exact ⟨[], rfl, IsSubseq.nil_left _⟩
    | succ k' =>
      have hle : k' ≤ xs.length := Nat.le_of_succ_le_succ hk
      obtain ⟨u, hu_len, hu_sub⟩ := ih hle
      exact ⟨b :: u, by simp [hu_len], .cons_keep b hu_sub⟩

/-- A word `d` is in the `s`-deletion ball `D_s(x)` iff `d` is a subsequence of `x` of length `x.length - s`. -/
def InDelBall (s : Nat) (x d : List Bool) : Prop :=
  IsSubseq d x ∧ d.length + s = x.length

/-- Existence of a common subsequence of length at least `k` (`LCS(x, y) >= k`). -/
def HasCommonSubseqAtLeast (k : Nat) (x y : List Bool) : Prop :=
  ∃ d : List Bool, k ≤ d.length ∧ IsSubseq d x ∧ IsSubseq d y

/--
  Fundamental Equivalence Theorem (100% general for all `n`, `s <= n`):
  Two binary words `x, y` of length `n` have disjoint `s`-deletion balls
  if and only if they have no common subsequence of length `>= n - s` (i.e. `LCS(x, y) < n - s`).
-/
theorem disjoint_delBall_iff_no_common_subseq
    {n s : Nat} (hs : s ≤ n) {x y : List Bool} (hx : x.length = n) (hy : y.length = n) :
    (∀ d, ¬ (InDelBall s x d ∧ InDelBall s y d)) ↔ ¬ HasCommonSubseqAtLeast (n - s) x y := by
  constructor
  · intro hdisj ⟨d, hd_len, hdx, hdy⟩
    obtain ⟨d', hd'_len, hd'_sub⟩ := exists_subseq_of_length hd_len
    have hx' : InDelBall s x d' := ⟨hd'_sub.trans hdx, by omega⟩
    have hy' : InDelBall s y d' := ⟨hd'_sub.trans hdy, by omega⟩
    exact hdisj d' ⟨hx', hy'⟩
  · intro hno d ⟨⟨hdx, hdlen⟩, ⟨hdy, _⟩⟩
    exact hno ⟨d, by omega, hdx, hdy⟩

/-- LSB-first bit-vector decoding `natToWord n x : List Bool` of exact length `n`. -/
def natToWord : Nat → Nat → List Bool
  | 0, _ => []
  | n + 1, x => (x % 2 == 1) :: natToWord n (x / 2)

theorem natToWord_length : ∀ (n x : Nat), (natToWord n x).length = n
  | 0, _ => rfl
  | n + 1, x => by simp [natToWord, natToWord_length n (x / 2)]

/-- Bit-level single deletion at index `i` (LSB = index 0). -/
def delBit (x i : Nat) : Nat :=
  (x % 2 ^ i) + (x / (2 * 2 ^ i)) * 2 ^ i

private theorem delBit_zero (x : Nat) : delBit x 0 = x / 2 := by
  simp [delBit, Nat.mod_one]

private theorem pow2_succ_eq (i : Nat) : 2 ^ (i + 1) = 2 * 2 ^ i := by
  rw [Nat.pow_succ, Nat.mul_comm]

private theorem mul_two_right (a b : Nat) : a * (2 * b) = (a * b) * 2 := by
  rw [Nat.mul_comm 2 b, ← Nat.mul_assoc]

private theorem two_mul_assoc_right (a b : Nat) : (2 * a) * b = (a * b) * 2 := by
  rw [Nat.mul_comm 2 a, Nat.mul_assoc, Nat.mul_comm 2 b, ← Nat.mul_assoc]

private theorem delBit_succ_mod2 (x i : Nat) : delBit x (i + 1) % 2 = x % 2 := by
  unfold delBit
  rw [pow2_succ_eq i, mul_two_right, Nat.add_mul_mod_self_right]
  have h1 := Nat.div_add_mod x (2 * 2 ^ i)
  have h2 : (2 * 2 ^ i) * (x / (2 * 2 ^ i)) = (2 ^ i * (x / (2 * 2 ^ i))) * 2 :=
    two_mul_assoc_right (2 ^ i) (x / (2 * 2 ^ i))
  have h3 : x = (2 ^ i * (x / (2 * 2 ^ i))) * 2 + x % (2 * 2 ^ i) := by omega
  calc
    x % (2 * 2 ^ i) % 2
      = ((2 ^ i * (x / (2 * 2 ^ i))) * 2 + x % (2 * 2 ^ i)) % 2 := (Nat.mul_add_mod_self_right _ _ _).symm
    _ = x % 2 := congrArg (· % 2) h3.symm

private theorem delBit_succ_div2 (x i : Nat) : delBit x (i + 1) / 2 = delBit (x / 2) i := by
  unfold delBit
  rw [pow2_succ_eq i, mul_two_right, Nat.add_mul_div_right _ _ (by omega : 0 < 2)]
  have hdiv_mod : (x % (2 * 2 ^ i)) / 2 = (x / 2) % 2 ^ i := by
    have hq := Nat.div_add_mod x (2 * 2 ^ i)
    have hpos : 0 < 2 ^ i := Nat.two_pow_pos i
    have hlt := Nat.mod_lt x (show 0 < 2 * 2 ^ i by omega)
    have hr := Nat.div_add_mod (x % (2 * 2 ^ i)) 2
    have hm1 : 2 * 2 ^ i * (x / (2 * 2 ^ i)) = 2 * (2 ^ i * (x / (2 * 2 ^ i))) := Nat.mul_assoc 2 _ _
    have hrem : (x % (2 * 2 ^ i)) % 2 < 2 := Nat.mod_lt _ (by omega)
    have hx2 : x / 2 = 2 ^ i * (x / (2 * 2 ^ i)) + (x % (2 * 2 ^ i)) / 2 := by
      have := Nat.div_add_mod x 2
      omega
    have hlt2 : (x % (2 * 2 ^ i)) / 2 < 2 ^ i := by omega
    rw [hx2, Nat.mul_add_mod_self_left, Nat.mod_eq_of_lt hlt2]
  have hdiv2 : x / (2 * (2 * 2 ^ i)) = (x / 2) / (2 * 2 ^ i) := by
    rw [Nat.div_div_eq_div_mul]
  rw [hdiv_mod, hdiv2]

/-- Exact algebraic bridge: `delBit` on `Nat` matches `deleteAt` on `natToWord`! -/
theorem natToWord_delBit : ∀ (n i x : Nat), i < n →
    natToWord (n - 1) (delBit x i) = deleteAt (natToWord n x) i := by
  intro n
  induction n with
  | zero => intro i _ h; exact absurd h (Nat.not_lt_zero _)
  | succ n' ih =>
    intro i x hi
    cases i with
    | zero =>
      simp [natToWord, deleteAt, delBit_zero]
    | succ i' =>
      cases n' with
      | zero => omega
      | succ n'' =>
        have hi' : i' < n'' + 1 := Nat.lt_of_succ_lt_succ hi
        change natToWord (n'' + 1) (delBit x (i' + 1)) =
               (x % 2 == 1) :: deleteAt (natToWord (n'' + 1) (x / 2)) i'
        simp only [natToWord, delBit_succ_mod2, delBit_succ_div2]
        congr 1
        exact ih i' (x / 2) hi'

/-- Deleting 2 positions `i < j < n` from `x`. -/
def del2Nat (x i j : Nat) : Nat := delBit (delBit x j) i

/-- Deleting 3 positions `i < j < k < n` from `x`. -/
def del3Nat (x i j k : Nat) : Nat := delBit (delBit (delBit x k) j) i

theorem del2Nat_isSubseq {n i j x : Nat} (hij : i < j) (hjn : j < n) :
    IsSubseq (natToWord (n - 2) (del2Nat x i j)) (natToWord n x) := by
  have h1 := natToWord_delBit n j x hjn
  have hin : i < n - 1 := by omega
  have h2 := natToWord_delBit (n - 1) i (delBit x j) hin
  have hsub1 := deleteAt_isSubseq (natToWord (n - 1) (delBit x j)) i
  have hsub2 := deleteAt_isSubseq (natToWord n x) j
  have hlen : n - 2 = n - 1 - 1 := by omega
  rw [hlen, del2Nat, h2]
  exact hsub1.trans (h1 ▸ hsub2)

theorem del3Nat_isSubseq {n i j k x : Nat} (hij : i < j) (hjk : j < k) (hkn : k < n) :
    IsSubseq (natToWord (n - 3) (del3Nat x i j k)) (natToWord n x) := by
  have h1 := natToWord_delBit n k x hkn
  have hjn : j < n - 1 := by omega
  have h2 := natToWord_delBit (n - 1) j (delBit x k) hjn
  have hin : i < n - 1 - 1 := by omega
  have h3 := natToWord_delBit (n - 1 - 1) i (delBit (delBit x k) j) hin
  have hlen : n - 3 = n - 1 - 1 - 1 := by omega
  rw [hlen, del3Nat, h3]
  have s3 := deleteAt_isSubseq (natToWord (n - 1 - 1) (delBit (delBit x k) j)) i
  have s2 := deleteAt_isSubseq (natToWord (n - 1) (delBit x k)) j
  have s1 := deleteAt_isSubseq (natToWord n x) k
  exact s3.trans (h2 ▸ s2.trans (h1 ▸ s1))

private theorem natToWord_eq_mod : ∀ (m a b : Nat),
    natToWord m a = natToWord m b → a % 2 ^ m = b % 2 ^ m := by
  intro m
  induction m with
  | zero => intro a b _; simp [Nat.mod_one]
  | succ m' ihm =>
    intro a b hab
    simp only [natToWord, List.cons.injEq] at hab
    have hbit : a % 2 = b % 2 := by
      have ha2 : a % 2 < 2 := Nat.mod_lt a (by omega)
      have hb2 : b % 2 < 2 := Nat.mod_lt b (by omega)
      have heq := hab.1
      cases h1 : a % 2 <;> cases h2 : b % 2 <;> simp_all <;> omega
    have hdiv := ihm (a / 2) (b / 2) hab.2
    rw [pow2_succ_eq m']
    have hsplit : ∀ z : Nat, z % (2 * 2 ^ m') = 2 * ((z / 2) % 2 ^ m') + z % 2 := by
      intro z
      have hq := Nat.div_add_mod (z / 2) (2 ^ m')
      have hpos : 0 < 2 ^ m' := Nat.two_pow_pos m'
      have hlt := Nat.mod_lt (z / 2) hpos
      have hz := Nat.div_add_mod z 2
      have hm : (2 * 2 ^ m') * ((z / 2) / 2 ^ m') = 2 * (2 ^ m' * ((z / 2) / 2 ^ m')) := Nat.mul_assoc 2 _ _
      have hz2 : z = (2 * 2 ^ m') * ((z / 2) / 2 ^ m') + (2 * ((z / 2) % 2 ^ m') + z % 2) := by omega
      have hlt2 : 2 * ((z / 2) % 2 ^ m') + z % 2 < 2 * 2 ^ m' := by omega
      calc
        z % (2 * 2 ^ m')
          = ((2 * 2 ^ m') * ((z / 2) / 2 ^ m') + (2 * ((z / 2) % 2 ^ m') + z % 2)) % (2 * 2 ^ m') :=
            congrArg (· % (2 * 2 ^ m')) hz2
        _ = (2 * ((z / 2) % 2 ^ m') + z % 2) % (2 * 2 ^ m') := Nat.mul_add_mod_self_left _ _ _
        _ = 2 * ((z / 2) % 2 ^ m') + z % 2 := Nat.mod_eq_of_lt hlt2
    rw [hsplit a, hsplit b, hdiv, hbit]

private theorem delBit_lt (m p y : Nat) (hy : y < 2 ^ m) (hp : p < m) :
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

/-- Completeness of `delBit`: every length `n - 1` subsequence of `natToWord n x` arises from `delBit x i`. -/
theorem exists_delBit_of_subseq {n x : Nat} {d : List Bool}
    (hsub : IsSubseq d (natToWord n x)) (hlen : d.length + 1 = n) :
    ∃ i < n, d = natToWord (n - 1) (delBit x i) := by
  induction n generalizing x d with
  | zero => omega
  | succ n' ih =>
    simp only [natToWord] at hsub
    cases hsub with
    | cons_drop _ h' =>
      have aux : ∀ {a b : List Bool}, IsSubseq a b → a.length = b.length → a = b := by
        intro a b hab
        induction hab with
        | nil => intro _; rfl
        | cons_keep c _ ih' =>
          intro hl; simp only [List.length_cons] at hl; rw [ih' (Nat.succ.inj hl)]
        | cons_drop c hsub' _ =>
          intro hl; have hle := hsub'.length_le; simp only [List.length_cons] at hl; omega
      have heq : d = natToWord n' (x / 2) := aux h' (by rw [natToWord_length]; omega)
      refine ⟨0, Nat.zero_lt_succ _, ?_⟩
      simp [delBit_zero, heq]
    | cons_keep b h' =>
      cases n' with
      | zero => simp only [List.length_cons] at hlen; omega
      | succ n'' =>
        simp only [List.length_cons] at hlen
        obtain ⟨i', hi', hd'⟩ := ih h' (by omega)
        refine ⟨i' + 1, Nat.succ_lt_succ hi', ?_⟩
        rw [natToWord_delBit (n'' + 2) (i' + 1) x (Nat.succ_lt_succ hi')]
        change (x % 2 == 1) :: _ = (x % 2 == 1) :: deleteAt (natToWord (n'' + 1) (x / 2)) i'
        congr 1
        rw [hd', natToWord_delBit (n'' + 1) i' (x / 2) hi']

private theorem hdrop_subseq {u v : List Bool} (huv : IsSubseq u v) (hlt : u.length < v.length) :
    ∃ j < v.length, IsSubseq u (deleteAt v j) := by
  induction huv with
  | nil => omega
  | cons_drop b h' _ => exact ⟨0, Nat.zero_lt_succ _, h'⟩
  | cons_keep b h' ih' =>
    simp only [List.length_cons] at hlt
    obtain ⟨j, hj, hsub'⟩ := ih' (by omega)
    exact ⟨j + 1, Nat.succ_lt_succ hj, .cons_keep b hsub'⟩

private theorem deleteAt_comm : ∀ (w : List Bool) (a b : Nat), a ≤ b → b + 1 < w.length →
    deleteAt (deleteAt w a) b = deleteAt (deleteAt w (b + 1)) a := by
  intro w
  induction w with
  | nil => intro a b _ h; simp at h
  | cons c ws ihw =>
    intro a b hab hbl
    cases a with
    | zero => simp [deleteAt]
    | succ a' =>
      cases b with
      | zero => omega
      | succ b' =>
        simp only [deleteAt]; congr 1
        exact ihw a' b' (Nat.le_of_succ_le_succ hab) (by simp at hbl; omega)

/-- Completeness of `del2Nat`: every length `n - 2` subsequence arises from `del2Nat x i j` (`i < j < n`). -/
theorem exists_del2Nat_of_subseq {n x : Nat} {d : List Bool}
    (hsub : IsSubseq d (natToWord n x)) (hlen : d.length + 2 = n) :
    ∃ i j, i < j ∧ j < n ∧ d = natToWord (n - 2) (del2Nat x i j) := by
  obtain ⟨j1, hj1_len, hsub1⟩ := hdrop_subseq hsub (by rw [natToWord_length]; omega)
  rw [natToWord_length] at hj1_len
  rw [← natToWord_delBit n j1 x hj1_len] at hsub1
  obtain ⟨i1, hi1, hd⟩ := exists_delBit_of_subseq hsub1 (by omega)
  by_cases hlt : i1 < j1
  · exact ⟨i1, j1, hlt, hj1_len, by simpa [del2Nat, Nat.sub_sub] using hd⟩
  · refine ⟨j1, i1 + 1, by omega, by omega, ?_⟩
    have h1 : natToWord (n - 2) (del2Nat x j1 (i1 + 1)) =
              deleteAt (deleteAt (natToWord n x) (i1 + 1)) j1 := by
      have hlen2 : n - 2 = n - 1 - 1 := by omega
      rw [hlen2, del2Nat, natToWord_delBit (n - 1) j1 _ (by omega),
          natToWord_delBit n (i1 + 1) x (by omega)]
    have h2 : d = deleteAt (deleteAt (natToWord n x) j1) i1 := by
      rw [hd, natToWord_delBit (n - 1) i1 _ (by omega), natToWord_delBit n j1 x hj1_len]
    rw [h1, h2]
    exact deleteAt_comm (natToWord n x) j1 i1 (by omega) (by rw [natToWord_length]; omega)

/-- Completeness of `del3Nat`: every length `n - 3` subsequence arises from `del3Nat x i j k` (`i < j < k < n`). -/
theorem exists_del3Nat_of_subseq {n x : Nat} {d : List Bool}
    (hsub : IsSubseq d (natToWord n x)) (hlen : d.length + 3 = n) :
    ∃ i j k, i < j ∧ j < k ∧ k < n ∧ d = natToWord (n - 3) (del3Nat x i j k) := by
  obtain ⟨k0, hk0_len, hsub1⟩ := hdrop_subseq hsub (by rw [natToWord_length]; omega)
  rw [natToWord_length] at hk0_len
  rw [← natToWord_delBit n k0 x hk0_len] at hsub1
  obtain ⟨a, b, hab, hbn, hd⟩ := exists_del2Nat_of_subseq hsub1 (by omega)
  have hd_del : d = deleteAt (deleteAt (deleteAt (natToWord n x) k0) b) a := by
    have hlen3 : n - 1 - 2 = n - 1 - 1 - 1 := by omega
    rw [hd, hlen3, del2Nat, natToWord_delBit (n - 1 - 1) a _ (by omega),
        natToWord_delBit (n - 1) b _ hbn, natToWord_delBit n k0 x hk0_len]
  have mk_goal : ∀ i j k, i < j → j < k → k < n →
      deleteAt (deleteAt (deleteAt (natToWord n x) k) j) i = d →
      ∃ i j k, i < j ∧ j < k ∧ k < n ∧ d = natToWord (n - 3) (del3Nat x i j k) := by
    intro i j k hij hjk hkn heq
    refine ⟨i, j, k, hij, hjk, hkn, ?_⟩
    have hlen3 : n - 3 = n - 1 - 1 - 1 := by omega
    rw [← heq, hlen3, del3Nat, natToWord_delBit (n - 1 - 1) i _ (by omega),
        natToWord_delBit (n - 1) j _ (by omega), natToWord_delBit n k x hkn]
  have hwlen : (natToWord n x).length = n := natToWord_length n x
  by_cases hbk : b < k0
  · exact mk_goal a b k0 hab hbk hk0_len hd_del.symm
  · have hswap1 : deleteAt (deleteAt (natToWord n x) k0) b =
                  deleteAt (deleteAt (natToWord n x) (b + 1)) k0 :=
      deleteAt_comm (natToWord n x) k0 b (by omega) (by omega)
    by_cases hak : a < k0
    · exact mk_goal a k0 (b + 1) hak (by omega) (by omega) (by rw [hd_del, hswap1])
    · have hswap2 : deleteAt (deleteAt (deleteAt (natToWord n x) (b + 1)) k0) a =
                    deleteAt (deleteAt (deleteAt (natToWord n x) (b + 1)) (a + 1)) k0 := by
        have hlen_w1 : (deleteAt (natToWord n x) (b + 1)).length = n - 1 := by
          have := deleteAt_length (natToWord n x) (b + 1) (by omega); omega
        exact deleteAt_comm _ k0 a (by omega) (by omega)
      exact mk_goal k0 (a + 1) (b + 1) (by omega) (by omega) (by omega) (by rw [hd_del, hswap1, hswap2])

/-- Formal validity predicate for an `s`-deletion-correcting code encoded as `List Nat` of `n`-bit words. -/
def IsValidDeletionCode (n s : Nat) (C : List Nat) : Prop :=
  (∀ x ∈ C, x < 2 ^ n) ∧
  (∀ (i j : Nat) (hi : i < C.length) (hj : j < C.length), i ≠ j →
    C[i] ≠ C[j] ∧
    (∀ d, ¬ (InDelBall s (natToWord n C[i]) d ∧ InDelBall s (natToWord n C[j]) d)) ∧
    ¬ HasCommonSubseqAtLeast (n - s) (natToWord n C[i]) (natToWord n C[j]))

/-- Formal inclusion-maximality (non-extendability) predicate over all `2^n` binary words.
    NOTE (-0 Hype): Certifies inclusion-maximality (no single word can extend `C`), NOT global cardinality optimality. -/
def IsInclusionMaximal (n s : Nat) (C : List Nat) : Prop :=
  ∀ x : Nat, x < 2 ^ n →
    ∃ (i : Nat) (_ : i < C.length) (d : List Bool),
      InDelBall s (natToWord n x) d ∧ InDelBall s (natToWord n C[i]) d

/-- O(log M) bit-indexed binary trie mapping each `(n-s)`-bit descendant to `owner_idx + 1` (or `0`). -/
inductive BitTrie where
  | empty : BitTrie
  | leaf (val : Nat) : BitTrie
  | node (l r : BitTrie) : BitTrie

def BitTrie.get : Nat → BitTrie → Nat → Nat
  | _, .empty, _ => 0
  | 0, .leaf v, _ => v
  | k + 1, .node l r, idx =>
      if idx % 2 == 0 then l.get k (idx / 2) else r.get k (idx / 2)
  | _, _, _ => 0

def allLt (bound : Nat) (f : Nat → Bool) : Bool :=
  let rec go : Nat → Bool
    | 0 => true
    | k + 1 => f k && go k
  go bound

theorem allLt_spec (bound : Nat) (f : Nat → Bool) :
    allLt bound f = true → ∀ i, i < bound → f i = true := by
  unfold allLt
  induction bound with
  | zero => intro _ i hi; exact absurd hi (Nat.not_lt_zero _)
  | succ k ih =>
    intro h i hi
    simp only [allLt.go, Bool.and_eq_true] at h
    rcases Nat.lt_succ_iff_lt_or_eq.mp hi with hlt | heq
    · exact ih h.2 i hlt
    · subst heq; exact h.1

def checkWord2 (n : Nat) (owner : BitTrie) (tag x : Nat) : Bool :=
  (x < 2 ^ n) &&
  allLt n (fun j => allLt j (fun i => owner.get (n - 2) (del2Nat x i j) == tag))

theorem checkWord2_spec {n : Nat} {owner : BitTrie} {tag x : Nat}
    (h : checkWord2 n owner tag x = true) :
    x < 2 ^ n ∧ ∀ i j, i < j → j < n → owner.get (n - 2) (del2Nat x i j) = tag := by
  unfold checkWord2 at h
  simp only [Bool.and_eq_true, decide_eq_true_eq] at h
  refine ⟨h.1, fun i j hij hjn => ?_⟩
  have h1 := allLt_spec n _ h.2 j hjn
  have h2 := allLt_spec j _ h1 i hij
  exact beq_iff_eq.mp h2

def checkList2 (n : Nat) (owner : BitTrie) : Nat → List Nat → Bool
  | _, [] => true
  | idx, x :: xs => checkWord2 n owner (idx + 1) x && checkList2 n owner (idx + 1) xs

theorem checkList2_spec {n : Nat} {owner : BitTrie} :
    ∀ (base : Nat) (L : List Nat), checkList2 n owner base L = true →
      ∀ (k : Nat) (hk : k < L.length), checkWord2 n owner (base + k + 1) L[k] = true := by
  intro base L
  induction L generalizing base with
  | nil => intro _ k hk; simp at hk
  | cons x xs ih =>
    intro h k hk
    simp only [checkList2, Bool.and_eq_true] at h
    cases k with
    | zero => simpa using h.1
    | succ k' =>
      have hk' : k' < xs.length := Nat.lt_of_succ_lt_succ hk
      have := ih (base + 1) h.2 k' hk'
      simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using this

/-- Soundness of the O(log M) BitTrie 2-deletion validity checker (zero sorryAx, pure kernel!). -/
theorem checkCode2_sound (n : Nat) (hn : 2 ≤ n) (owner : BitTrie) (C : List Nat)
    (h : checkList2 n owner 0 C = true) : IsValidDeletionCode n 2 C := by
  have hall := checkList2_spec 0 C h
  constructor
  · intro x hx
    obtain ⟨k, hk, rfl⟩ := List.getElem_of_mem hx
    exact (checkWord2_spec (by simpa using hall k hk)).1
  · intro i j hi hj hij
    have hwi := checkWord2_spec (by simpa using hall i hi)
    have hwj := checkWord2_spec (by simpa using hall j hj)
    have hdisj : ∀ d, ¬ (InDelBall 2 (natToWord n C[i]) d ∧ InDelBall 2 (natToWord n C[j]) d) := by
      intro d ⟨⟨hdi, hlen⟩, ⟨hdj, _⟩⟩
      rw [natToWord_length] at hlen
      obtain ⟨i1, j1, h1, h1n, heq1⟩ := exists_del2Nat_of_subseq hdi hlen
      obtain ⟨i2, j2, h2, h2n, heq2⟩ := exists_del2Nat_of_subseq hdj hlen
      have hd1_lt : del2Nat C[i] i1 j1 < 2 ^ (n - 2) := by
        have ha := delBit_lt n j1 C[i] hwi.1 h1n
        have hb := delBit_lt (n - 1) i1 (delBit C[i] j1) ha (by omega)
        simpa [del2Nat, Nat.sub_sub] using hb
      have hd2_lt : del2Nat C[j] i2 j2 < 2 ^ (n - 2) := by
        have ha := delBit_lt n j2 C[j] hwj.1 h2n
        have hb := delBit_lt (n - 1) i2 (delBit C[j] j2) ha (by omega)
        simpa [del2Nat, Nat.sub_sub] using hb
      have hdeq : del2Nat C[i] i1 j1 = del2Nat C[j] i2 j2 := by
        have hm := natToWord_eq_mod (n - 2) _ _ (heq1.symm.trans heq2)
        rw [Nat.mod_eq_of_lt hd1_lt, Nat.mod_eq_of_lt hd2_lt] at hm
        exact hm
      have oi := hwi.2 i1 j1 h1 h1n
      have oj := hwj.2 i2 j2 h2 h2n
      rw [hdeq] at oi
      omega
    have hneq : C[i] ≠ C[j] := by
      intro heq
      have hsub := del2Nat_isSubseq (n := n) (i := 0) (j := 1) (x := C[i]) (by omega) (by omega)
      have hball : InDelBall 2 (natToWord n C[i]) (natToWord (n - 2) (del2Nat C[i] 0 1)) :=
        ⟨hsub, by rw [natToWord_length, natToWord_length]; omega⟩
      exact hdisj _ ⟨hball, heq ▸ hball⟩
    have hlcs := (disjoint_delBall_iff_no_common_subseq hn (natToWord_length n C[i]) (natToWord_length n C[j])).mp hdisj
    exact ⟨hneq, hdisj, hlcs⟩

def checkWord3 (n : Nat) (owner : BitTrie) (tag x : Nat) : Bool :=
  (x < 2 ^ n) &&
  allLt n (fun k => allLt k (fun j => allLt j (fun i => owner.get (n - 3) (del3Nat x i j k) == tag)))

theorem checkWord3_spec {n : Nat} {owner : BitTrie} {tag x : Nat}
    (h : checkWord3 n owner tag x = true) :
    x < 2 ^ n ∧ ∀ i j k, i < j → j < k → k < n → owner.get (n - 3) (del3Nat x i j k) = tag := by
  unfold checkWord3 at h
  simp only [Bool.and_eq_true, decide_eq_true_eq] at h
  refine ⟨h.1, fun i j k hij hjk hkn => ?_⟩
  have h1 := allLt_spec n _ h.2 k hkn
  have h2 := allLt_spec k _ h1 j hjk
  have h3 := allLt_spec j _ h2 i hij
  exact beq_iff_eq.mp h3

def checkList3 (n : Nat) (owner : BitTrie) : Nat → List Nat → Bool
  | _, [] => true
  | idx, x :: xs => checkWord3 n owner (idx + 1) x && checkList3 n owner (idx + 1) xs

theorem checkList3_spec {n : Nat} {owner : BitTrie} :
    ∀ (base : Nat) (L : List Nat), checkList3 n owner base L = true →
      ∀ (k : Nat) (hk : k < L.length), checkWord3 n owner (base + k + 1) L[k] = true := by
  intro base L
  induction L generalizing base with
  | nil => intro _ k hk; simp at hk
  | cons x xs ih =>
    intro h k hk
    simp only [checkList3, Bool.and_eq_true] at h
    cases k with
    | zero => simpa using h.1
    | succ k' =>
      have hk' : k' < xs.length := Nat.lt_of_succ_lt_succ hk
      have := ih (base + 1) h.2 k' hk'
      simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using this

/-- Soundness of the O(log M) BitTrie 3-deletion validity checker (zero sorryAx, pure kernel!). -/
theorem checkCode3_sound (n : Nat) (hn : 3 ≤ n) (owner : BitTrie) (C : List Nat)
    (h : checkList3 n owner 0 C = true) : IsValidDeletionCode n 3 C := by
  have hall := checkList3_spec 0 C h
  constructor
  · intro x hx
    obtain ⟨k, hk, rfl⟩ := List.getElem_of_mem hx
    exact (checkWord3_spec (by simpa using hall k hk)).1
  · intro i j hi hj hij
    have hwi := checkWord3_spec (by simpa using hall i hi)
    have hwj := checkWord3_spec (by simpa using hall j hj)
    have hdisj : ∀ d, ¬ (InDelBall 3 (natToWord n C[i]) d ∧ InDelBall 3 (natToWord n C[j]) d) := by
      intro d ⟨⟨hdi, hlen⟩, ⟨hdj, _⟩⟩
      rw [natToWord_length] at hlen
      obtain ⟨i1, j1, k1, h1a, h1b, h1n, heq1⟩ := exists_del3Nat_of_subseq hdi hlen
      obtain ⟨i2, j2, k2, h2a, h2b, h2n, heq2⟩ := exists_del3Nat_of_subseq hdj hlen
      have hd1_lt : del3Nat C[i] i1 j1 k1 < 2 ^ (n - 3) := by
        have ha := delBit_lt n k1 C[i] hwi.1 h1n
        have hb := delBit_lt (n - 1) j1 (delBit C[i] k1) ha (by omega)
        have hc := delBit_lt (n - 1 - 1) i1 (delBit (delBit C[i] k1) j1) hb (by omega)
        simpa [del3Nat, Nat.sub_sub] using hc
      have hd2_lt : del3Nat C[j] i2 j2 k2 < 2 ^ (n - 3) := by
        have ha := delBit_lt n k2 C[j] hwj.1 h2n
        have hb := delBit_lt (n - 1) j2 (delBit C[j] k2) ha (by omega)
        have hc := delBit_lt (n - 1 - 1) i2 (delBit (delBit C[j] k2) j2) hb (by omega)
        simpa [del3Nat, Nat.sub_sub] using hc
      have hdeq : del3Nat C[i] i1 j1 k1 = del3Nat C[j] i2 j2 k2 := by
        have hm := natToWord_eq_mod (n - 3) _ _ (heq1.symm.trans heq2)
        rw [Nat.mod_eq_of_lt hd1_lt, Nat.mod_eq_of_lt hd2_lt] at hm
        exact hm
      have oi := hwi.2 i1 j1 k1 h1a h1b h1n
      have oj := hwj.2 i2 j2 k2 h2a h2b h2n
      rw [hdeq] at oi
      omega
    have hneq : C[i] ≠ C[j] := by
      intro heq
      have hsub := del3Nat_isSubseq (n := n) (i := 0) (j := 1) (k := 2) (x := C[i]) (by omega) (by omega) (by omega)
      have hball : InDelBall 3 (natToWord n C[i]) (natToWord (n - 3) (del3Nat C[i] 0 1 2)) :=
        ⟨hsub, by rw [natToWord_length, natToWord_length]; omega⟩
      exact hdisj _ ⟨hball, heq ▸ hball⟩
    have hlcs := (disjoint_delBall_iff_no_common_subseq hn (natToWord_length n C[i]) (natToWord_length n C[j])).mp hdisj
    exact ⟨hneq, hdisj, hlcs⟩

/-- Binary witness tree for inclusion-maximality over all `2^n` binary words (depth `d` recursion -> O(1) stack!). -/
inductive MaxTree where
  | leaf (idx px pc : Nat) : MaxTree
  | node (l r : MaxTree) : MaxTree

def checkCodeTrie (cd : Nat) (ct : BitTrie) : Nat → List Nat → Bool
  | _, [] => true
  | idx, x :: xs => (ct.get cd idx == x) && checkCodeTrie cd ct (idx + 1) xs

theorem checkCodeTrie_spec {cd : Nat} {ct : BitTrie} :
    ∀ (base : Nat) (L : List Nat), checkCodeTrie cd ct base L = true →
      ∀ (k : Nat) (hk : k < L.length), ct.get cd (base + k) = L[k] := by
  intro base L
  induction L generalizing base with
  | nil => intro _ k hk; simp at hk
  | cons x xs ih =>
    intro h k hk
    simp only [checkCodeTrie, Bool.and_eq_true, beq_iff_eq] at h
    cases k with
    | zero => simpa using h.1
    | succ k' =>
      have hk' : k' < xs.length := Nat.lt_of_succ_lt_succ hk
      have := ih (base + 1) h.2 k' hk'
      simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using this

private theorem mul_pow2_left (x d' y : Nat) :
    (2 * x) * 2 ^ d' + y = x * 2 ^ (d' + 1) + y := by
  rw [Nat.pow_succ, Nat.mul_comm 2 x, Nat.mul_assoc, Nat.mul_comm 2 (2 ^ d')]

private theorem mul_pow2_right (x d' y : Nat) (hge : ¬ y < 2 ^ d') :
    (2 * x + 1) * 2 ^ d' + (y - 2 ^ d') = x * 2 ^ (d' + 1) + y := by
  rw [Nat.add_mul, Nat.one_mul, Nat.pow_succ, Nat.mul_comm 2 x, Nat.mul_assoc, Nat.mul_comm 2 (2 ^ d')]
  omega

def checkMax3 (n klen cd : Nat) (ct : BitTrie) : Nat → Nat → MaxTree → Bool
  | 0, x, .leaf idx px pc =>
      let i1 := px % 16; let j1 := (px / 16) % 16; let k1 := px / 256
      let i2 := pc % 16; let j2 := (pc / 16) % 16; let k2 := pc / 256
      (idx < klen) &&
      (i1 < j1) && (j1 < k1) && (k1 < n) &&
      (i2 < j2) && (j2 < k2) && (k2 < n) &&
      (del3Nat x i1 j1 k1 == del3Nat (ct.get cd idx) i2 j2 k2)
  | d + 1, x, .node l r =>
      checkMax3 n klen cd ct d (2 * x) l && checkMax3 n klen cd ct d (2 * x + 1) r
  | _, _, _ => false

theorem checkMax3_block {n cd : Nat} {C : List Nat} {ct : BitTrie}
    (hct : checkCodeTrie cd ct 0 C = true) :
    ∀ (d x : Nat) (t : MaxTree), checkMax3 n C.length cd ct d x t = true →
      ∀ (y : Nat), y < 2 ^ d →
        ∃ (idx : Nat) (_ : idx < C.length) (sub : List Bool),
          InDelBall 3 (natToWord n (x * 2 ^ d + y)) sub ∧
          InDelBall 3 (natToWord n C[idx]) sub := by
  have hget := checkCodeTrie_spec 0 C hct
  intro d
  induction d with
  | zero =>
    intro x t ht y hy
    have hy0 : y = 0 := by simpa using hy
    subst hy0
    cases t with
    | node _ _ => simp [checkMax3] at ht
    | leaf idx px pc =>
      simp only [checkMax3, Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq] at ht
      rcases ht with ⟨⟨⟨⟨⟨⟨⟨hidx, hi1⟩, hj1⟩, hk1⟩, hi2⟩, hj2⟩, hk2⟩, hdeq⟩
      have hlookup : ct.get cd idx = C[idx] := by simpa using hget idx hidx
      rw [hlookup] at hdeq
      refine ⟨idx, hidx, natToWord (n - 3) (del3Nat x (px % 16) ((px / 16) % 16) (px / 256)), ?_, ?_⟩
      · refine ⟨?_, by rw [natToWord_length, natToWord_length]; omega⟩
        simpa using del3Nat_isSubseq (n := n) (x := x) hi1 hj1 hk1
      · refine ⟨?_, by rw [natToWord_length, natToWord_length]; omega⟩
        rw [hdeq]
        exact del3Nat_isSubseq (n := n) (x := C[idx]) hi2 hj2 hk2
  | succ d' ih =>
    intro x t ht y hy
    cases t with
    | leaf _ _ _ => simp [checkMax3] at ht
    | node l r =>
      simp only [checkMax3, Bool.and_eq_true] at ht
      by_cases hlow : y < 2 ^ d'
      · have hres := ih (2 * x) l ht.1 y hlow
        rw [mul_pow2_left] at hres
        exact hres
      · have hhi : y - 2 ^ d' < 2 ^ d' := by rw [Nat.pow_succ] at hy; omega
        have hres := ih (2 * x + 1) r ht.2 (y - 2 ^ d') hhi
        rw [mul_pow2_right x d' y hlow] at hres
        exact hres

def checkMax2 (n klen cd : Nat) (ct : BitTrie) : Nat → Nat → MaxTree → Bool
  | 0, x, .leaf idx px pc =>
      let i1 := px % 16; let j1 := px / 16
      let i2 := pc % 16; let j2 := pc / 16
      (idx < klen) &&
      (i1 < j1) && (j1 < n) &&
      (i2 < j2) && (j2 < n) &&
      (del2Nat x i1 j1 == del2Nat (ct.get cd idx) i2 j2)
  | d + 1, x, .node l r =>
      checkMax2 n klen cd ct d (2 * x) l && checkMax2 n klen cd ct d (2 * x + 1) r
  | _, _, _ => false

theorem checkMax2_block {n cd : Nat} {C : List Nat} {ct : BitTrie}
    (hct : checkCodeTrie cd ct 0 C = true) :
    ∀ (d x : Nat) (t : MaxTree), checkMax2 n C.length cd ct d x t = true →
      ∀ (y : Nat), y < 2 ^ d →
        ∃ (idx : Nat) (_ : idx < C.length) (sub : List Bool),
          InDelBall 2 (natToWord n (x * 2 ^ d + y)) sub ∧
          InDelBall 2 (natToWord n C[idx]) sub := by
  have hget := checkCodeTrie_spec 0 C hct
  intro d
  induction d with
  | zero =>
    intro x t ht y hy
    have hy0 : y = 0 := by simpa using hy
    subst hy0
    cases t with
    | node _ _ => simp [checkMax2] at ht
    | leaf idx px pc =>
      simp only [checkMax2, Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq] at ht
      rcases ht with ⟨⟨⟨⟨⟨hidx, hi1⟩, hj1⟩, hi2⟩, hj2⟩, hdeq⟩
      have hlookup : ct.get cd idx = C[idx] := by simpa using hget idx hidx
      rw [hlookup] at hdeq
      refine ⟨idx, hidx, natToWord (n - 2) (del2Nat x (px % 16) (px / 16)), ?_, ?_⟩
      · refine ⟨?_, by rw [natToWord_length, natToWord_length]; omega⟩
        simpa using del2Nat_isSubseq (n := n) (x := x) hi1 hj1
      · refine ⟨?_, by rw [natToWord_length, natToWord_length]; omega⟩
        rw [hdeq]
        exact del2Nat_isSubseq (n := n) (x := C[idx]) hi2 hj2
  | succ d' ih =>
    intro x t ht y hy
    cases t with
    | leaf _ _ _ => simp [checkMax2] at ht
    | node l r =>
      simp only [checkMax2, Bool.and_eq_true] at ht
      by_cases hlow : y < 2 ^ d'
      · have hres := ih (2 * x) l ht.1 y hlow
        rw [mul_pow2_left] at hres
        exact hres
      · have hhi : y - 2 ^ d' < 2 ^ d' := by rw [Nat.pow_succ] at hy; omega
        have hres := ih (2 * x + 1) r ht.2 (y - 2 ^ d') hhi
        rw [mul_pow2_right x d' y hlow] at hres
        exact hres

theorem inclusionMaximal_of_blocks {n s b d : Nat} {C : List Nat} (hbd : b + d = n)
    (hblocks : ∀ blk < 2 ^ b, ∀ y < 2 ^ d,
      ∃ (idx : Nat) (_ : idx < C.length) (sub : List Bool),
        InDelBall s (natToWord n (blk * 2 ^ d + y)) sub ∧
        InDelBall s (natToWord n C[idx]) sub) :
    IsInclusionMaximal n s C := by
  intro x hx
  have hpos : 0 < 2 ^ d := Nat.two_pow_pos d
  have hpow : 2 ^ n = 2 ^ b * 2 ^ d := by rw [← hbd, Nat.pow_add]
  have hblk : x / 2 ^ d < 2 ^ b := by
    rw [Nat.div_lt_iff_lt_mul hpos]
    rw [← hpow]
    exact hx
  have hy : x % 2 ^ d < 2 ^ d := Nat.mod_lt x hpos
  have hdecomp : (x / 2 ^ d) * 2 ^ d + x % 2 ^ d = x := by
    have := Nat.div_add_mod x (2 ^ d)
    rw [Nat.mul_comm] at this
    exact this
  simpa [hdecomp] using hblocks (x / 2 ^ d) hblk (x % 2 ^ d) hy

/--
  General Clique-Cover Upper Bound Theorem (exact pigeonhole bound for any deletion code):
  If every `n`-bit word is assigned to one of `K` buckets (`color : Nat -> Fin K`)
  such that any two words in the same bucket share a length `(n - s)` subsequence,
  then EVERY valid `s`-deletion code `C` has cardinality `|C| <= K`.
-/
theorem card_le_of_clique_cover {n s K : Nat} {C : List Nat}
    (hval : IsValidDeletionCode n s C)
    (color : Nat → Fin K)
    (hclq : ∀ x y, x < 2 ^ n → y < 2 ^ n → color x = color y →
      ∃ d, InDelBall s (natToWord n x) d ∧ InDelBall s (natToWord n y) d) :
    C.length ≤ K := by
  have hinj : ∀ (i j : Fin C.length), color C[i.1] = color C[j.1] → i = j := by
    intro i j heq
    exact Classical.byContradiction fun hne => by
      have hij : i.1 ≠ j.1 := fun h => hne (Fin.ext h)
      have hxi : C[i.1] < 2 ^ n := hval.1 C[i.1] (List.getElem_mem i.2)
      have hxj : C[j.1] < 2 ^ n := hval.1 C[j.1] (List.getElem_mem j.2)
      obtain ⟨d, hd⟩ := hclq C[i.1] C[j.1] hxi hxj heq
      exact (hval.2 i.1 j.1 i.2 j.2 hij).2.1 d hd
  have fpig : ∀ {m k : Nat} (f : Fin m → Fin k), (∀ a b, f a = f b → a = b) → m ≤ k := by
    intro m k
    induction m generalizing k with
    | zero => intro _ _; exact Nat.zero_le _
    | succ m' ihm =>
      intro f hf
      cases k with
      | zero => exact Fin.elim0 (f ⟨0, Nat.zero_lt_succ _⟩)
      | succ k' =>
        let z := f ⟨m', Nat.lt_succ_self _⟩
        let g : Fin m' → Fin k' := fun a =>
          let y := f ⟨a.1, Nat.lt_succ_of_lt a.2⟩
          if hlt : y.1 < z.1 then ⟨y.1, by omega⟩
          else ⟨y.1 - 1, by
            have hne : y ≠ z := fun h => by
              have := hf ⟨a.1, Nat.lt_succ_of_lt a.2⟩ ⟨m', Nat.lt_succ_self _⟩ h
              have : a.1 = m' := congrArg Fin.val this
              omega
            have hnv : y.1 ≠ z.1 := fun h => hne (Fin.ext h)
            omega⟩
        have hg : ∀ a b, g a = g b → a = b := by
          intro a b hab
          have hval_eq : (g a).1 = (g b).1 := congrArg Fin.val hab
          have hnea : (f ⟨a.1, Nat.lt_succ_of_lt a.2⟩).1 ≠ z.1 := fun h => by
            have := hf ⟨a.1, Nat.lt_succ_of_lt a.2⟩ ⟨m', Nat.lt_succ_self _⟩ (Fin.ext h)
            have : a.1 = m' := congrArg Fin.val this; omega
          have hneb : (f ⟨b.1, Nat.lt_succ_of_lt b.2⟩).1 ≠ z.1 := fun h => by
            have := hf ⟨b.1, Nat.lt_succ_of_lt b.2⟩ ⟨m', Nat.lt_succ_self _⟩ (Fin.ext h)
            have : b.1 = m' := congrArg Fin.val this; omega
          have hfeq_val : (f ⟨a.1, Nat.lt_succ_of_lt a.2⟩).1 = (f ⟨b.1, Nat.lt_succ_of_lt b.2⟩).1 := by
            by_cases ha1 : (f ⟨a.1, Nat.lt_succ_of_lt a.2⟩).1 < z.1 <;>
            by_cases hb1 : (f ⟨b.1, Nat.lt_succ_of_lt b.2⟩).1 < z.1
            · simp only [g, ha1, hb1, ↓reduceDIte] at hval_eq; exact hval_eq
            · simp only [g, ha1, hb1, ↓reduceDIte] at hval_eq; omega
            · simp only [g, ha1, hb1, ↓reduceDIte] at hval_eq; omega
            · simp only [g, ha1, hb1, ↓reduceDIte] at hval_eq; omega
          have hfeq : f ⟨a.1, Nat.lt_succ_of_lt a.2⟩ = f ⟨b.1, Nat.lt_succ_of_lt b.2⟩ := Fin.ext hfeq_val
          have hfin : (⟨a.1, Nat.lt_succ_of_lt a.2⟩ : Fin (m' + 1)) = ⟨b.1, Nat.lt_succ_of_lt b.2⟩ :=
            hf _ _ hfeq
          have hv : a.1 = b.1 := congrArg (fun x : Fin (m' + 1) => x.1) hfin
          exact Fin.ext hv
        exact Nat.succ_le_succ (ihm g hg)
  exact fpig (fun i => color C[i.1]) hinj

end DeletionCode
