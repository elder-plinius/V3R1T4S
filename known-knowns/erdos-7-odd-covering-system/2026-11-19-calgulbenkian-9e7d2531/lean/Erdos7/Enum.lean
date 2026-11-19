/-
Stage 3: completeness of the enumeration of abundant band profiles.

`walk` is a fuel-based, structurally recursive depth-first search over all profiles
`[e_0, e_1, ...]` (exponent `e_m ≥ 1` on `oddP m`) of value `≤ B0`, in lexicographic order.
Whenever it meets a profile that is in the band (`B0 < 3 * val`) and abundant
(`2 * val ≤ sig`), it requires that profile to be the head of the expected list and consumes it.
It is evaluated by the kernel (`decide +kernel`, no `native_decide`) against
`Cert.table.map Prod.fst`.
-/
import Erdos7.Defs

namespace Erdos7

/-- If `need`, the head of `l` must be `key` and is consumed. -/
def mark (need : Bool) (key : List ℕ) (l : List (List ℕ)) : Option (List (List ℕ)) :=
  if need then
    match l with
    | h :: tl => if h = key then some tl else none
    | [] => none
  else some l

/-- Depth-first search.  State: coordinate `i`, exponent `e` under consideration at coordinate
`i`, `pe = oddP i ^ e`, `base` = value of the earlier coordinates, `sn` = their sigma-product,
`pre` = their exponents (reversed), `l` = the profiles still expected. -/
def walk : ℕ → ℕ → ℕ → ℕ → ℕ → List ℕ → ℕ → List (List ℕ) → Option (List (List ℕ))
  | 0, _, _, _, _, _, _, _ => none
  | fuel + 1, i, base, pe, sn, pre, e, l =>
    if oddP i = 0 then none
    else if B0 < base * pe then some l
    else
      (mark (decide (B0 < 3 * (base * pe) ∧ 2 * (base * pe) ≤ sn * geom (oddP i) (e + 1)))
        (e :: pre).reverse l).bind fun l1 =>
      (walk fuel (i + 1) (base * pe) (oddP (i + 1)) (sn * geom (oddP i) (e + 1))
        (e :: pre) 1 l1).bind fun l2 =>
      walk fuel i base (pe * oddP i) sn pre (e + 1) l2

theorem mark_spec {need : Bool} {key : List ℕ} {l l1 : List (List ℕ)}
    (h : mark need key l = some l1) :
    ∃ c, l = c ++ l1 ∧ (need = true → key ∈ c) := by
  unfold mark at h
  cases need with
  | false =>
    simp at h
    exact ⟨[], by simp [h], by simp⟩
  | true =>
    cases l with
    | nil => simp at h
    | cons a tl =>
      simp only [ite_true] at h
      by_cases ha : a = key
      · simp [ha] at h
        exact ⟨[a], by simp [h], fun _ => by simp [ha]⟩
      · simp [ha] at h

theorem walk_spec : ∀ (fuel i base pe sn : ℕ) (pre : List ℕ) (e : ℕ) (l l' : List (List ℕ)),
    walk fuel i base pe sn pre e l = some l' →
    ∃ c, l = c ++ l' ∧ ∀ (e' : ℕ) (rest : List ℕ), e ≤ e' → (∀ x ∈ rest, 1 ≤ x) →
      base * (pe * oddP i ^ (e' - e)) * valFrom (i + 1) rest ≤ B0 →
      B0 < 3 * (base * (pe * oddP i ^ (e' - e)) * valFrom (i + 1) rest) →
      2 * (base * (pe * oddP i ^ (e' - e)) * valFrom (i + 1) rest)
        ≤ sn * geom (oddP i) (e' + 1) * sigFrom (i + 1) rest →
      pre.reverse ++ e' :: rest ∈ c := by
  intro fuel
  induction fuel with
  | zero => intro i base pe sn pre e l l' h; simp [walk] at h
  | succ n ih =>
    intro i base pe sn pre e l l' h
    simp only [walk] at h
    split_ifs at h with h0 hB
    · -- pruned: every extension exceeds B0
      obtain rfl : l = l' := by simpa using h
      refine ⟨[], rfl, ?_⟩
      intro e' rest _ _ hle hlo _
      exfalso
      have hvk : base * (pe * oddP i ^ (e' - e)) * valFrom (i + 1) rest
          = base * pe * (oddP i ^ (e' - e) * valFrom (i + 1) rest) := by ring
      rw [hvk] at hle hlo
      have hk : 0 < oddP i ^ (e' - e) * valFrom (i + 1) rest := by
        rcases Nat.eq_zero_or_pos (oddP i ^ (e' - e) * valFrom (i + 1) rest) with h | h
        · rw [h] at hlo; simp at hlo
        · exact h
      have : base * pe ≤ base * pe * (oddP i ^ (e' - e) * valFrom (i + 1) rest) :=
        Nat.le_mul_of_pos_right _ hk
      omega
    · rw [Option.bind_eq_some_iff] at h
      obtain ⟨l1, hm, h⟩ := h
      rw [Option.bind_eq_some_iff] at h
      obtain ⟨l2, hc, hs⟩ := h
      obtain ⟨c0, rfl, hc0⟩ := mark_spec hm
      obtain ⟨c1, rfl, hc1⟩ := ih _ _ _ _ _ _ _ _ hc
      obtain ⟨c2, rfl, hc2⟩ := ih _ _ _ _ _ _ _ _ hs
      refine ⟨c0 ++ c1 ++ c2, by simp, ?_⟩
      intro e' rest hee hpos hle hlo hab
      rcases Nat.eq_or_lt_of_le hee with rfl | hlt
      · cases rest with
        | nil =>
          simp only [Nat.sub_self, pow_zero, mul_one, valFrom, sigFrom] at hle hlo hab
          have : (e :: pre).reverse ∈ c0 := hc0 (by simpa using ⟨hlo, hab⟩)
          simp only [List.reverse_cons] at this
          simp [this]
        | cons e2 rest' =>
          have h2 : 1 ≤ e2 := hpos e2 (by simp)
          have hp : oddP (i + 1) * oddP (i + 1) ^ (e2 - 1) = oddP (i + 1) ^ e2 := by
            rw [← pow_succ', Nat.sub_add_cancel h2]
          have E : base * pe * (oddP (i + 1) ^ e2) * valFrom (i + 1 + 1) rest'
              = base * (pe * oddP i ^ (e - e)) * valFrom (i + 1) (e2 :: rest') := by
            simp [valFrom]; ring
          have E2 : sn * geom (oddP i) (e + 1) * geom (oddP (i + 1)) (e2 + 1)
                * sigFrom (i + 1 + 1) rest'
              = sn * geom (oddP i) (e + 1) * sigFrom (i + 1) (e2 :: rest') := by
            simp [sigFrom]; ring
          have := hc1 e2 rest' h2 (fun x hx => hpos x (by simp [hx]))
            (by rw [hp, E]; exact hle) (by rw [hp, E]; exact hlo)
            (by rw [hp, E, E2]; exact hab)
          simp only [List.reverse_cons, List.append_assoc, List.singleton_append] at this
          simp [this]
      · have hp : oddP i * oddP i ^ (e' - (e + 1)) = oddP i ^ (e' - e) := by
          rw [← pow_succ']; congr 1; omega
        have E : base * (pe * oddP i * oddP i ^ (e' - (e + 1)))
            = base * (pe * oddP i ^ (e' - e)) := by rw [mul_assoc pe, hp]
        have := hc2 e' rest hlt hpos (by rw [E]; exact hle) (by rw [E]; exact hlo)
          (by rw [E]; exact hab)
        simp [this]

/-- The top-level search result (fuel 40). -/
def walkRes : Option (List (List ℕ)) := walk 40 0 1 3 1 [] 1 (Cert.table.map Prod.fst)

/-- The search succeeded and consumed the whole expected list. -/
def isDone (o : Option (List (List ℕ))) : Bool :=
  match o with
  | some [] => true
  | _ => false

theorem isDone_spec {o : Option (List (List ℕ))} (h : isDone o = true) : o = some [] := by
  unfold isDone at h
  split at h
  · rfl
  · exact absurd h (by simp)

/-- Kernel-evaluated (`decide +kernel`, no `native_decide`). -/
theorem walkTop_ok : isDone walkRes = true := by decide +kernel

/-- Every abundant profile in the band `(B0/3, B0]` is one of the 7,036 table profiles. -/
theorem band_complete (es : List ℕ) (hpos : ∀ e ∈ es, 1 ≤ e) (hne : es ≠ [])
    (hlo : B0 < 3 * valFrom 0 es) (hhi : valFrom 0 es ≤ B0)
    (hab : 2 * valFrom 0 es ≤ sigFrom 0 es) :
    es ∈ Cert.table.map Prod.fst := by
  have hw : walkRes = some [] := isDone_spec walkTop_ok
  obtain ⟨c, hc, hspec⟩ := walk_spec 40 0 1 3 1 [] 1 (Cert.table.map Prod.fst) [] hw
  generalize Cert.table.map Prod.fst = tbl at hc ⊢
  rw [List.append_nil] at hc
  subst hc
  cases es with
  | nil => exact absurd rfl hne
  | cons e0 rest =>
    have h1 : 1 ≤ e0 := hpos e0 (by simp)
    have hp : (3 : ℕ) * oddP 0 ^ (e0 - 1) = oddP 0 ^ e0 := by
      show oddP 0 * oddP 0 ^ (e0 - 1) = oddP 0 ^ e0
      rw [← pow_succ', Nat.sub_add_cancel h1]
    have E : 1 * (3 * oddP 0 ^ (e0 - 1)) * valFrom (0 + 1) rest = valFrom 0 (e0 :: rest) := by
      rw [hp]; simp [valFrom]
    have E2 : 1 * geom (oddP 0) (e0 + 1) * sigFrom (0 + 1) rest = sigFrom 0 (e0 :: rest) := by
      simp [sigFrom]
    have := hspec e0 rest h1 (fun x hx => hpos x (by simp [hx]))
      (by rw [E]; exact hhi) (by rw [E]; exact hlo) (by rw [E, E2]; exact hab)
    simpa using this

#print axioms band_complete

end Erdos7
