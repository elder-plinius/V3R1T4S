import PRMPlus.Aff15Arith

/-!
# Soundness of the Contracting 6-Step Poincaré Tube (`InTube`, `checkSlab`, `checkT0InTube`)
-/

namespace PRMPlus

open scoped BigOperators

structure TubeSpec where
  B        : Nat
  halfB    : Nat
  ys0      : Nat
  ys1      : Nat
  ys2      : Nat
  gapLB    : Nat
  slabHalf : Nat
  rInt     : Nat
  nCheb    : Nat
  uToRow   : List (Fin 6)
  rowToU   : List (Fin 6)
  Z_c      : List (List SInt)
  D_c      : List (List SInt)
  L_c      : List (List (List SInt))
  U_c      : List (List (List SInt))

def checkPerm6 (uToRow rowToU : List (Fin 6)) : Bool :=
  (uToRow.getD (rowToU.getD 0 0).val 0 == 0) &&
  (uToRow.getD (rowToU.getD 1 0).val 0 == 1) &&
  (uToRow.getD (rowToU.getD 2 0).val 0 == 2) &&
  (uToRow.getD (rowToU.getD 3 0).val 0 == 3) &&
  (uToRow.getD (rowToU.getD 4 0).val 0 == 4) &&
  (uToRow.getD (rowToU.getD 5 0).val 0 == 5) &&
  (rowToU.getD (uToRow.getD 0 0).val 0 == 0) &&
  (rowToU.getD (uToRow.getD 1 0).val 0 == 1) &&
  (rowToU.getD (uToRow.getD 2 0).val 0 == 2) &&
  (rowToU.getD (uToRow.getD 3 0).val 0 == 3) &&
  (rowToU.getD (uToRow.getD 4 0).val 0 == 4) &&
  (rowToU.getD (uToRow.getD 5 0).val 0 == 5)

lemma checkPerm6_u_row (uToRow rowToU : List (Fin 6)) (h : checkPerm6 uToRow rowToU = true)
    (orig : Fin 6) : uToRow.getD (rowToU.getD orig.val 0).val 0 = orig := by
  unfold checkPerm6 at h
  simp only [Bool.and_eq_true, beq_iff_eq] at h
  rcases orig with ⟨ov, hov⟩
  have hc : ov = 0 ∨ ov = 1 ∨ ov = 2 ∨ ov = 3 ∨ ov = 4 ∨ ov = 5 := by omega
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl
  · exact h.1.1.1.1.1.1.1.1.1.1.1
  · exact h.1.1.1.1.1.1.1.1.1.1.2
  · exact h.1.1.1.1.1.1.1.1.1.2
  · exact h.1.1.1.1.1.1.1.1.2
  · exact h.1.1.1.1.1.1.1.2
  · exact h.1.1.1.1.1.1.2

def checkTubeSpec (P : TubeSpec) : Bool :=
  Nat.ble 1 P.B &&
  (P.B == 2 * P.halfB) &&
  (P.ys0 + P.ys1 + P.ys2 == P.B) &&
  (3 * P.ys0 == 4 * P.ys2) &&
  (3 * P.ys1 == 5 * P.ys2) &&
  (20 * P.gapLB == P.B) &&
  (12288 * P.slabHalf == P.B) &&
  Nat.ble 1 P.rInt &&
  checkPerm6 P.uToRow P.rowToU &&
  (List.range 6).all (fun i =>
    Nat.ble (P.Z_c.getD i []).length P.nCheb &&
    Nat.ble (P.D_c.getD i []).length P.nCheb &&
    (List.range 6).all (fun j =>
      Nat.ble ((P.L_c.getD i []).getD j []).length P.nCheb &&
      Nat.ble ((P.U_c.getD i []).getD j []).length P.nCheb))

def TubeSpec.Valid (P : TubeSpec) : Prop :=
  0 < P.B ∧ P.B = 2 * P.halfB ∧
  P.ys0 + P.ys1 + P.ys2 = P.B ∧
  3 * P.ys0 = 4 * P.ys2 ∧ 3 * P.ys1 = 5 * P.ys2 ∧
  20 * P.gapLB = P.B ∧
  12288 * P.slabHalf = P.B ∧
  0 < P.rInt ∧
  checkPerm6 P.uToRow P.rowToU = true ∧
  (∀ i < 6, (P.Z_c.getD i []).length ≤ P.nCheb ∧ (P.D_c.getD i []).length ≤ P.nCheb) ∧
  (∀ i < 6, ∀ j < 6,
    ((P.L_c.getD i []).getD j []).length ≤ P.nCheb ∧
    ((P.U_c.getD i []).getD j []).length ≤ P.nCheb)

lemma checkTubeSpec_sound (P : TubeSpec) (h : checkTubeSpec P = true) : P.Valid := by
  unfold checkTubeSpec at h
  simp only [Bool.and_eq_true, beq_iff_eq, List.all_eq_true, List.mem_range] at h
  refine ⟨Nat.ble_eq.mp h.1.1.1.1.1.1.1.1.1, h.1.1.1.1.1.1.1.1.2,
          h.1.1.1.1.1.1.1.2, h.1.1.1.1.1.1.2, h.1.1.1.1.1.2,
          h.1.1.1.1.2, h.1.1.1.2, Nat.ble_eq.mp h.1.1.2, h.1.2, ?_, ?_⟩
  · intro i hi
    have hi' := h.2 i hi
    exact ⟨Nat.ble_eq.mp hi'.1.1, Nat.ble_eq.mp hi'.1.2⟩
  · intro i hi j hj
    have hij := (h.2 i hi).2 j hj
    exact ⟨Nat.ble_eq.mp hij.1, Nat.ble_eq.mp hij.2⟩

def ysNat (P : TubeSpec) (j : Fin 3) : Nat :=
  match j.val with
  | 0 => P.ys0 | 1 => P.ys1 | _ => P.ys2

noncomputable def ysReal (P : TubeSpec) (j : Fin 3) : ℝ :=
  (ysNat P j : ℝ) / (P.B : ℝ)

lemma ysReal_zero (P : TubeSpec) : ysReal P 0 = (P.ys0 : ℝ) / (P.B : ℝ) := rfl
lemma ysReal_one  (P : TubeSpec) : ysReal P 1 = (P.ys1 : ℝ) / (P.B : ℝ) := rfl
lemma ysReal_two  (P : TubeSpec) : ysReal P 2 = (P.ys2 : ℝ) / (P.B : ℝ) := rfl

lemma ysReal_props (P : TubeSpec) (hP : P.Valid) :
    ysReal P 0 + ysReal P 1 + ysReal P 2 = 1 ∧
    3 * ysReal P 0 - 3 * ysReal P 2 = ysReal P 2 ∧
    3 * ysReal P 1 - 4 * ysReal P 2 = ysReal P 2 := by
  have hB : (P.B : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hP.1)
  have hsum : (P.ys0 : ℝ) + (P.ys1 : ℝ) + (P.ys2 : ℝ) = (P.B : ℝ) := by
    exact_mod_cast hP.2.2.1
  have h0 : 3 * (P.ys0 : ℝ) = 4 * (P.ys2 : ℝ) := by exact_mod_cast hP.2.2.2.1
  have h1 : 3 * (P.ys1 : ℝ) = 5 * (P.ys2 : ℝ) := by exact_mod_cast hP.2.2.2.2.1
  rw [ysReal_zero, ysReal_one, ysReal_two]
  refine ⟨?_, ?_, ?_⟩ <;> (field_simp [hB]; linarith)

/-! ### 6-Vector Real & `Aff15N` Unit-LDU Transforms (`pack` and `unpack`) -/

structure Vec6R where
  v0 : ℝ
  v1 : ℝ
  v2 : ℝ
  v3 : ℝ
  v4 : ℝ
  v5 : ℝ

def Vec6R.get (x : Vec6R) (i : Fin 6) : ℝ :=
  match i.val with
  | 0 => x.v0 | 1 => x.v1 | 2 => x.v2 | 3 => x.v3 | 4 => x.v4 | _ => x.v5

def Vec6R.ofFn (f : Fin 6 → ℝ) : Vec6R := ⟨f 0, f 1, f 2, f 3, f 4, f 5⟩

lemma Vec6R.get_ofFn (f : Fin 6 → ℝ) (i : Fin 6) : (Vec6R.ofFn f).get i = f i := by
  rcases i with ⟨iv, hiv⟩
  have hc : iv = 0 ∨ iv = 1 ∨ iv = 2 ∨ iv = 3 ∨ iv = 4 ∨ iv = 5 := by omega
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl <;> rfl

lemma Vec6R.ext_get (a b : Vec6R) (h : ∀ i : Fin 6, a.get i = b.get i) : a = b := by
  rcases a with ⟨a0, a1, a2, a3, a4, a5⟩
  rcases b with ⟨b0, b1, b2, b3, b4, b5⟩
  have h0 := h 0; have h1 := h 1; have h2 := h 2
  have h3 := h 3; have h4 := h 4; have h5 := h 5
  dsimp only [Vec6R.get] at h0 h1 h2 h3 h4 h5
  subst h0; subst h1; subst h2; subst h3; subst h4; subst h5
  rfl

structure Vec6N where
  v0 : Aff15N
  v1 : Aff15N
  v2 : Aff15N
  v3 : Aff15N
  v4 : Aff15N
  v5 : Aff15N

def Vec6N.get (x : Vec6N) (i : Fin 6) : Aff15N :=
  match i.val with
  | 0 => x.v0 | 1 => x.v1 | 2 => x.v2 | 3 => x.v3 | 4 => x.v4 | _ => x.v5

def Vec6N.ofFn (f : Fin 6 → Aff15N) : Vec6N := ⟨f 0, f 1, f 2, f 3, f 4, f 5⟩

lemma Vec6N.get_ofFn (f : Fin 6 → Aff15N) (i : Fin 6) : (Vec6N.ofFn f).get i = f i := by
  rcases i with ⟨iv, hiv⟩
  have hc : iv = 0 ∨ iv = 1 ∨ iv = 2 ∨ iv = 3 ∨ iv = 4 ∨ iv = 5 := by omega
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl <;> rfl

def Vec6N.Enc (B : Nat) (x : Vec6N) (te : TubeEnv) (vr : Vec6R) : Prop :=
  x.v0.Enc B te vr.v0 ∧ x.v1.Enc B te vr.v1 ∧ x.v2.Enc B te vr.v2 ∧
  x.v3.Enc B te vr.v3 ∧ x.v4.Enc B te vr.v4 ∧ x.v5.Enc B te vr.v5

lemma Vec6N.enc_get (B : Nat) (x : Vec6N) (te : TubeEnv) (vr : Vec6R)
    (h : x.Enc B te vr) (i : Fin 6) : (x.get i).Enc B te (vr.get i) := by
  rcases i with ⟨iv, hiv⟩
  have hc : iv = 0 ∨ iv = 1 ∨ iv = 2 ∨ iv = 3 ∨ iv = 4 ∨ iv = 5 := by omega
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl
  · exact h.1
  · exact h.2.1
  · exact h.2.2.1
  · exact h.2.2.2.1
  · exact h.2.2.2.2.1
  · exact h.2.2.2.2.2

lemma Vec6N.enc_ofFn (B : Nat) (f : Fin 6 → Aff15N) (te : TubeEnv) (g : Fin 6 → ℝ)
    (h : ∀ i : Fin 6, (f i).Enc B te (g i)) : (Vec6N.ofFn f).Enc B te (Vec6R.ofFn g) :=
  ⟨h 0, h 1, h 2, h 3, h 4, h 5⟩

noncomputable def zVecReal (P : TubeSpec) (eps : ℝ) : Vec6R :=
  Vec6R.ofFn (fun i => evalChebReal P.B eps (P.Z_c.getD i.val []))

noncomputable def dVecReal (P : TubeSpec) (eps : ℝ) : Vec6R :=
  Vec6R.ofFn (fun i => evalChebReal P.B eps (P.D_c.getD i.val []))

noncomputable def lValReal (P : TubeSpec) (eps : ℝ) (i j : Nat) : ℝ :=
  evalChebReal P.B eps ((P.L_c.getD i []).getD j [])

noncomputable def uValReal (P : TubeSpec) (eps : ℝ) (i j : Nat) : ℝ :=
  evalChebReal P.B eps ((P.U_c.getD i []).getD j [])

noncomputable def solveLower6R (l : Nat → Nat → ℝ) (y3 : Vec6R) : Vec6R :=
  let y2_0 := y3.v0
  let y2_1 := y3.v1 - l 1 0 * y2_0
  let y2_2 := (y3.v2 - l 2 0 * y2_0) - l 2 1 * y2_1
  let y2_3 := ((y3.v3 - l 3 0 * y2_0) - l 3 1 * y2_1) - l 3 2 * y2_2
  let y2_4 := (((y3.v4 - l 4 0 * y2_0) - l 4 1 * y2_1) - l 4 2 * y2_2) - l 4 3 * y2_3
  let y2_5 := ((((y3.v5 - l 5 0 * y2_0) - l 5 1 * y2_1) - l 5 2 * y2_2) - l 5 3 * y2_3) - l 5 4 * y2_4
  ⟨y2_0, y2_1, y2_2, y2_3, y2_4, y2_5⟩

noncomputable def mulLower6R (l : Nat → Nat → ℝ) (y2 : Vec6R) : Vec6R :=
  ⟨y2.v0,
   y2.v1 + l 1 0 * y2.v0,
   (y2.v2 + l 2 0 * y2.v0) + l 2 1 * y2.v1,
   ((y2.v3 + l 3 0 * y2.v0) + l 3 1 * y2.v1) + l 3 2 * y2.v2,
   (((y2.v4 + l 4 0 * y2.v0) + l 4 1 * y2.v1) + l 4 2 * y2.v2) + l 4 3 * y2.v3,
   ((((y2.v5 + l 5 0 * y2.v0) + l 5 1 * y2.v1) + l 5 2 * y2.v2) + l 5 3 * y2.v3) + l 5 4 * y2.v4⟩

lemma mulLower6R_solveLower6R (l : Nat → Nat → ℝ) (y3 : Vec6R) :
    mulLower6R l (solveLower6R l y3) = y3 := by
  rcases y3 with ⟨v0, v1, v2, v3, v4, v5⟩
  unfold mulLower6R solveLower6R
  dsimp only
  congr 1 <;> ring

noncomputable def solveUpper6R (u : Nat → Nat → ℝ) (y1 : Vec6R) : Vec6R :=
  let vn_5 := y1.v5
  let vn_4 := y1.v4 - u 4 5 * vn_5
  let vn_3 := (y1.v3 - u 3 4 * vn_4) - u 3 5 * vn_5
  let vn_2 := ((y1.v2 - u 2 3 * vn_3) - u 2 4 * vn_4) - u 2 5 * vn_5
  let vn_1 := (((y1.v1 - u 1 2 * vn_2) - u 1 3 * vn_3) - u 1 4 * vn_4) - u 1 5 * vn_5
  let vn_0 := ((((y1.v0 - u 0 1 * vn_1) - u 0 2 * vn_2) - u 0 3 * vn_3) - u 0 4 * vn_4) - u 0 5 * vn_5
  ⟨vn_0, vn_1, vn_2, vn_3, vn_4, vn_5⟩

noncomputable def mulUpper6R (u : Nat → Nat → ℝ) (v : Vec6R) : Vec6R :=
  ⟨((((v.v0 + u 0 1 * v.v1) + u 0 2 * v.v2) + u 0 3 * v.v3) + u 0 4 * v.v4) + u 0 5 * v.v5,
   (((v.v1 + u 1 2 * v.v2) + u 1 3 * v.v3) + u 1 4 * v.v4) + u 1 5 * v.v5,
   ((v.v2 + u 2 3 * v.v3) + u 2 4 * v.v4) + u 2 5 * v.v5,
   (v.v3 + u 3 4 * v.v4) + u 3 5 * v.v5,
   v.v4 + u 4 5 * v.v5,
   v.v5⟩

lemma mulUpper6R_solveUpper6R (u : Nat → Nat → ℝ) (y1 : Vec6R) :
    mulUpper6R u (solveUpper6R u y1) = y1 := by
  rcases y1 with ⟨v0, v1, v2, v3, v4, v5⟩
  unfold mulUpper6R solveUpper6R
  dsimp only
  congr 1 <;> ring

noncomputable def divDiag6R (y2 d : Vec6R) : Vec6R :=
  ⟨y2.v0 / d.v0, y2.v1 / d.v1, y2.v2 / d.v2, y2.v3 / d.v3, y2.v4 / d.v4, y2.v5 / d.v5⟩

noncomputable def mulDiag6R (d y1 : Vec6R) : Vec6R :=
  ⟨d.v0 * y1.v0, d.v1 * y1.v1, d.v2 * y1.v2, d.v3 * y1.v3, d.v4 * y1.v4, d.v5 * y1.v5⟩

def Vec6R.NonZero (d : Vec6R) : Prop :=
  d.v0 ≠ 0 ∧ d.v1 ≠ 0 ∧ d.v2 ≠ 0 ∧ d.v3 ≠ 0 ∧ d.v4 ≠ 0 ∧ d.v5 ≠ 0

lemma mulDiag6R_divDiag6R (y2 d : Vec6R) (hd : d.NonZero) :
    mulDiag6R d (divDiag6R y2 d) = y2 := by
  rcases y2 with ⟨a0, a1, a2, a3, a4, a5⟩
  rcases d with ⟨d0, d1, d2, d3, d4, d5⟩
  rcases hd with ⟨h0, h1, h2, h3, h4, h5⟩
  unfold mulDiag6R divDiag6R
  dsimp only
  congr 1
  · exact mul_div_cancel₀ _ h0
  · exact mul_div_cancel₀ _ h1
  · exact mul_div_cancel₀ _ h2
  · exact mul_div_cancel₀ _ h3
  · exact mul_div_cancel₀ _ h4
  · exact mul_div_cancel₀ _ h5

noncomputable def permDiff6R (uToRow : List (Fin 6)) (z zc : Vec6R) : Vec6R :=
  Vec6R.ofFn (fun k => z.get (uToRow.getD k.val 0) - zc.get (uToRow.getD k.val 0))

noncomputable def unpermAdd6R (rowToU : List (Fin 6)) (zc y3 : Vec6R) : Vec6R :=
  Vec6R.ofFn (fun orig => zc.get orig + y3.get (rowToU.getD orig.val 0))

lemma unpermAdd6R_permDiff6R (uToRow rowToU : List (Fin 6)) (hp : checkPerm6 uToRow rowToU = true)
    (z zc : Vec6R) :
    unpermAdd6R rowToU zc (permDiff6R uToRow z zc) = z := by
  apply Vec6R.ext_get
  intro orig
  unfold unpermAdd6R permDiff6R
  rw [Vec6R.get_ofFn, Vec6R.get_ofFn, checkPerm6_u_row uToRow rowToU hp orig]
  ring

noncomputable def packReal (P : TubeSpec) (eps : ℝ) (z : Vec6R) : Vec6R :=
  let y3 := permDiff6R P.uToRow z (zVecReal P eps)
  let y2 := solveLower6R (lValReal P eps) y3
  let y1 := divDiag6R y2 (dVecReal P eps)
  solveUpper6R (uValReal P eps) y1

noncomputable def unpackReal (P : TubeSpec) (eps : ℝ) (v : Vec6R) : Vec6R :=
  let y1 := mulUpper6R (uValReal P eps) v
  let y2 := mulDiag6R (dVecReal P eps) y1
  let y3 := mulLower6R (lValReal P eps) y2
  unpermAdd6R P.rowToU (zVecReal P eps) y3

lemma unpackReal_packReal (P : TubeSpec) (hp : checkPerm6 P.uToRow P.rowToU = true)
    (eps : ℝ) (z : Vec6R) (hD : (dVecReal P eps).NonZero) :
    unpackReal P eps (packReal P eps z) = z := by
  unfold unpackReal packReal
  dsimp only
  rw [mulUpper6R_solveUpper6R, mulDiag6R_divDiag6R _ _ hD, mulLower6R_solveLower6R]
  exact unpermAdd6R_permDiff6R P.uToRow P.rowToU hp z (zVecReal P eps)

/-! ### Verified `Aff15N` Interval/Sign Checkers & Unit-LDU Routines -/

def isPos15 (x : Aff15N) : Bool := (sPosNat x.lo).isSome
def isNeg15 (x : Aff15N) : Bool := (sPosNat (sNeg x.hi)).isSome
def nonZero15 (x : Aff15N) : Bool := isPos15 x || isNeg15 x
def loGeSInt15 (lb : SInt) (x : Aff15N) : Bool := sNonneg (sSub x.lo lb)
def absLe15 (r : Nat) (x : Aff15N) : Bool := Nat.ble (sAbs x.c + x.rad) r
def vec6AbsLe15 (r : Nat) (v : Vec6N) : Bool :=
  absLe15 r v.v0 && absLe15 r v.v1 && absLe15 r v.v2 &&
  absLe15 r v.v3 && absLe15 r v.v4 && absLe15 r v.v5

lemma isPos15_spec (B : Nat) (hB : 0 < B) (x : Aff15N) (te : TubeEnv) (v : ℝ)
    (hte : te.Valid) (hx : x.Enc B te v) (h : isPos15 x = true) : 0 < v := by
  have hBr_pos : (0 : ℝ) < (B : ℝ) := Nat.cast_pos.mpr hB
  have hlo := (x.bounds_of_enc B te v hte hx).2.1
  unfold isPos15 at h
  rcases Option.isSome_iff_exists.mp h with ⟨m, hm⟩
  rcases sPosNat_spec x.lo m hm with ⟨hm_pos, hval⟩
  rw [hval] at hlo
  exact pos_of_mul_pos_right (lt_of_lt_of_le (Nat.cast_pos.mpr hm_pos) hlo) (le_of_lt hBr_pos)

lemma isNeg15_spec (B : Nat) (hB : 0 < B) (x : Aff15N) (te : TubeEnv) (v : ℝ)
    (hte : te.Valid) (hx : x.Enc B te v) (h : isNeg15 x = true) : v < 0 := by
  have hBr_pos : (0 : ℝ) < (B : ℝ) := Nat.cast_pos.mpr hB
  have hhi := (x.bounds_of_enc B te v hte hx).2.2
  unfold isNeg15 at h
  rcases Option.isSome_iff_exists.mp h with ⟨m, hm⟩
  rcases sPosNat_spec (sNeg x.hi) m hm with ⟨hm_pos, hval⟩
  rw [sNeg_toReal] at hval
  have hm_r : (0 : ℝ) < (m : ℝ) := Nat.cast_pos.mpr hm_pos
  have hBv_neg : (B : ℝ) * v < 0 := by linarith
  by_contra hge
  have hge' : 0 ≤ v := le_of_not_gt hge
  have hnn : 0 ≤ (B : ℝ) * v := mul_nonneg (le_of_lt hBr_pos) hge'
  linarith

lemma nonZero15_spec (B : Nat) (hB : 0 < B) (x : Aff15N) (te : TubeEnv) (v : ℝ)
    (hte : te.Valid) (hx : x.Enc B te v) (h : nonZero15 x = true) : v ≠ 0 := by
  unfold nonZero15 at h
  simp only [Bool.or_eq_true] at h
  rcases h with hp | hn
  · exact ne_of_gt (isPos15_spec B hB x te v hte hx hp)
  · exact ne_of_lt (isNeg15_spec B hB x te v hte hx hn)

lemma loGeSInt15_spec (B : Nat) (lb : SInt) (x : Aff15N) (te : TubeEnv) (v : ℝ)
    (hte : te.Valid) (hx : x.Enc B te v) (h : loGeSInt15 lb x = true) :
    lb.toReal ≤ (B : ℝ) * v := by
  have hlo := (x.bounds_of_enc B te v hte hx).2.1
  have hnn := sNonneg_spec _ h
  rw [sSub_toReal] at hnn
  linarith

lemma absLe15_spec (B r : Nat) (x : Aff15N) (te : TubeEnv) (v : ℝ)
    (hte : te.Valid) (hx : x.Enc B te v) (h : absLe15 r x = true) :
    |(B : ℝ) * v| ≤ (r : ℝ) := by
  have hb := (x.bounds_of_enc B te v hte hx).1
  have hc : (sAbs x.c : ℝ) = |x.c.toReal| := sAbs_toReal x.c
  have hr : (sAbs x.c : ℝ) + (x.rad : ℝ) ≤ (r : ℝ) := by
    exact_mod_cast (Nat.ble_eq.mp h)
  have hcc1 : x.c.toReal ≤ |x.c.toReal| := le_abs_self x.c.toReal
  have hcc2 : -x.c.toReal ≤ |x.c.toReal| := neg_le_abs x.c.toReal
  rw [← hc] at hcc1 hcc2
  rw [abs_le] at hb ⊢
  constructor <;> linarith

def Vec6R.Bounded (B r : Nat) (v : Vec6R) : Prop :=
  |(B : ℝ) * v.v0| ≤ (r : ℝ) ∧ |(B : ℝ) * v.v1| ≤ (r : ℝ) ∧ |(B : ℝ) * v.v2| ≤ (r : ℝ) ∧
  |(B : ℝ) * v.v3| ≤ (r : ℝ) ∧ |(B : ℝ) * v.v4| ≤ (r : ℝ) ∧ |(B : ℝ) * v.v5| ≤ (r : ℝ)

lemma vec6AbsLe15_spec (B r : Nat) (va : Vec6N) (te : TubeEnv) (vr : Vec6R)
    (hte : te.Valid) (hva : va.Enc B te vr) (h : vec6AbsLe15 r va = true) :
    vr.Bounded B r := by
  unfold vec6AbsLe15 at h
  simp only [Bool.and_eq_true] at h
  exact ⟨absLe15_spec B r _ te _ hte hva.1 h.1.1.1.1.1,
         absLe15_spec B r _ te _ hte hva.2.1 h.1.1.1.1.2,
         absLe15_spec B r _ te _ hte hva.2.2.1 h.1.1.1.2,
         absLe15_spec B r _ te _ hte hva.2.2.2.1 h.1.1.2,
         absLe15_spec B r _ te _ hte hva.2.2.2.2.1 h.1.2,
         absLe15_spec B r _ te _ hte hva.2.2.2.2.2 h.2⟩

def solveLower6A (B : Nat) (lA : Nat → Nat → Aff15N) (y3 : Vec6N) : Vec6N :=
  let y2_0 := y3.v0
  let y2_1 := a15Sub y3.v1 (a15Mul B (lA 1 0) y2_0)
  let y2_2 := a15Sub (a15Sub y3.v2 (a15Mul B (lA 2 0) y2_0)) (a15Mul B (lA 2 1) y2_1)
  let y2_3 := a15Sub (a15Sub (a15Sub y3.v3 (a15Mul B (lA 3 0) y2_0)) (a15Mul B (lA 3 1) y2_1)) (a15Mul B (lA 3 2) y2_2)
  let y2_4 := a15Sub (a15Sub (a15Sub (a15Sub y3.v4 (a15Mul B (lA 4 0) y2_0)) (a15Mul B (lA 4 1) y2_1)) (a15Mul B (lA 4 2) y2_2)) (a15Mul B (lA 4 3) y2_3)
  let y2_5 := a15Sub (a15Sub (a15Sub (a15Sub (a15Sub y3.v5 (a15Mul B (lA 5 0) y2_0)) (a15Mul B (lA 5 1) y2_1)) (a15Mul B (lA 5 2) y2_2)) (a15Mul B (lA 5 3) y2_3)) (a15Mul B (lA 5 4) y2_4)
  ⟨y2_0, y2_1, y2_2, y2_3, y2_4, y2_5⟩

lemma solveLower6A_enc (B : Nat) (hB : 0 < B) (lA : Nat → Nat → Aff15N) (lR : Nat → Nat → ℝ)
    (y3A : Vec6N) (y3R : Vec6R) (te : TubeEnv) (hte : te.Valid)
    (hl : ∀ i < 6, ∀ j < 6, (lA i j).Enc B te (lR i j))
    (hy3 : y3A.Enc B te y3R) :
    (solveLower6A B lA y3A).Enc B te (solveLower6R lR y3R) := by
  rcases hy3 with ⟨h0, h1, h2, h3, h4, h5⟩
  unfold solveLower6A solveLower6R Vec6N.Enc
  dsimp only
  have q0 := h0
  have q1 := a15Sub_enc B _ _ te _ _ h1 (a15Mul_enc B hB _ _ te _ _ hte (hl 1 (by decide) 0 (by decide)) q0)
  have q2 := a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ h2 (a15Mul_enc B hB _ _ te _ _ hte (hl 2 (by decide) 0 (by decide)) q0)) (a15Mul_enc B hB _ _ te _ _ hte (hl 2 (by decide) 1 (by decide)) q1)
  have q3 := a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ h3 (a15Mul_enc B hB _ _ te _ _ hte (hl 3 (by decide) 0 (by decide)) q0)) (a15Mul_enc B hB _ _ te _ _ hte (hl 3 (by decide) 1 (by decide)) q1)) (a15Mul_enc B hB _ _ te _ _ hte (hl 3 (by decide) 2 (by decide)) q2)
  have q4 := a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ h4 (a15Mul_enc B hB _ _ te _ _ hte (hl 4 (by decide) 0 (by decide)) q0)) (a15Mul_enc B hB _ _ te _ _ hte (hl 4 (by decide) 1 (by decide)) q1)) (a15Mul_enc B hB _ _ te _ _ hte (hl 4 (by decide) 2 (by decide)) q2)) (a15Mul_enc B hB _ _ te _ _ hte (hl 4 (by decide) 3 (by decide)) q3)
  have q5 := a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ h5 (a15Mul_enc B hB _ _ te _ _ hte (hl 5 (by decide) 0 (by decide)) q0)) (a15Mul_enc B hB _ _ te _ _ hte (hl 5 (by decide) 1 (by decide)) q1)) (a15Mul_enc B hB _ _ te _ _ hte (hl 5 (by decide) 2 (by decide)) q2)) (a15Mul_enc B hB _ _ te _ _ hte (hl 5 (by decide) 3 (by decide)) q3)) (a15Mul_enc B hB _ _ te _ _ hte (hl 5 (by decide) 4 (by decide)) q4)
  exact ⟨q0, q1, q2, q3, q4, q5⟩

def mulLower6A (B : Nat) (lA : Nat → Nat → Aff15N) (y2 : Vec6N) : Vec6N :=
  ⟨y2.v0,
   a15Add y2.v1 (a15Mul B (lA 1 0) y2.v0),
   a15Add (a15Add y2.v2 (a15Mul B (lA 2 0) y2.v0)) (a15Mul B (lA 2 1) y2.v1),
   a15Add (a15Add (a15Add y2.v3 (a15Mul B (lA 3 0) y2.v0)) (a15Mul B (lA 3 1) y2.v1)) (a15Mul B (lA 3 2) y2.v2),
   a15Add (a15Add (a15Add (a15Add y2.v4 (a15Mul B (lA 4 0) y2.v0)) (a15Mul B (lA 4 1) y2.v1)) (a15Mul B (lA 4 2) y2.v2)) (a15Mul B (lA 4 3) y2.v3),
   a15Add (a15Add (a15Add (a15Add (a15Add y2.v5 (a15Mul B (lA 5 0) y2.v0)) (a15Mul B (lA 5 1) y2.v1)) (a15Mul B (lA 5 2) y2.v2)) (a15Mul B (lA 5 3) y2.v3)) (a15Mul B (lA 5 4) y2.v4)⟩

lemma mulLower6A_enc (B : Nat) (hB : 0 < B) (lA : Nat → Nat → Aff15N) (lR : Nat → Nat → ℝ)
    (y2A : Vec6N) (y2R : Vec6R) (te : TubeEnv) (hte : te.Valid)
    (hl : ∀ i < 6, ∀ j < 6, (lA i j).Enc B te (lR i j))
    (hy2 : y2A.Enc B te y2R) :
    (mulLower6A B lA y2A).Enc B te (mulLower6R lR y2R) := by
  rcases hy2 with ⟨h0, h1, h2, h3, h4, h5⟩
  unfold mulLower6A mulLower6R Vec6N.Enc
  dsimp only
  refine ⟨h0,
    a15Add_enc B _ _ te _ _ h1 (a15Mul_enc B hB _ _ te _ _ hte (hl 1 (by decide) 0 (by decide)) h0),
    a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ h2 (a15Mul_enc B hB _ _ te _ _ hte (hl 2 (by decide) 0 (by decide)) h0)) (a15Mul_enc B hB _ _ te _ _ hte (hl 2 (by decide) 1 (by decide)) h1),
    a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ h3 (a15Mul_enc B hB _ _ te _ _ hte (hl 3 (by decide) 0 (by decide)) h0)) (a15Mul_enc B hB _ _ te _ _ hte (hl 3 (by decide) 1 (by decide)) h1)) (a15Mul_enc B hB _ _ te _ _ hte (hl 3 (by decide) 2 (by decide)) h2),
    a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ h4 (a15Mul_enc B hB _ _ te _ _ hte (hl 4 (by decide) 0 (by decide)) h0)) (a15Mul_enc B hB _ _ te _ _ hte (hl 4 (by decide) 1 (by decide)) h1)) (a15Mul_enc B hB _ _ te _ _ hte (hl 4 (by decide) 2 (by decide)) h2)) (a15Mul_enc B hB _ _ te _ _ hte (hl 4 (by decide) 3 (by decide)) h3),
    a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ h5 (a15Mul_enc B hB _ _ te _ _ hte (hl 5 (by decide) 0 (by decide)) h0)) (a15Mul_enc B hB _ _ te _ _ hte (hl 5 (by decide) 1 (by decide)) h1)) (a15Mul_enc B hB _ _ te _ _ hte (hl 5 (by decide) 2 (by decide)) h2)) (a15Mul_enc B hB _ _ te _ _ hte (hl 5 (by decide) 3 (by decide)) h3)) (a15Mul_enc B hB _ _ te _ _ hte (hl 5 (by decide) 4 (by decide)) h4)⟩

def solveUpper6A (B : Nat) (uA : Nat → Nat → Aff15N) (y1 : Vec6N) : Vec6N :=
  let vn_5 := y1.v5
  let vn_4 := a15Sub y1.v4 (a15Mul B (uA 4 5) vn_5)
  let vn_3 := a15Sub (a15Sub y1.v3 (a15Mul B (uA 3 4) vn_4)) (a15Mul B (uA 3 5) vn_5)
  let vn_2 := a15Sub (a15Sub (a15Sub y1.v2 (a15Mul B (uA 2 3) vn_3)) (a15Mul B (uA 2 4) vn_4)) (a15Mul B (uA 2 5) vn_5)
  let vn_1 := a15Sub (a15Sub (a15Sub (a15Sub y1.v1 (a15Mul B (uA 1 2) vn_2)) (a15Mul B (uA 1 3) vn_3)) (a15Mul B (uA 1 4) vn_4)) (a15Mul B (uA 1 5) vn_5)
  let vn_0 := a15Sub (a15Sub (a15Sub (a15Sub (a15Sub y1.v0 (a15Mul B (uA 0 1) vn_1)) (a15Mul B (uA 0 2) vn_2)) (a15Mul B (uA 0 3) vn_3)) (a15Mul B (uA 0 4) vn_4)) (a15Mul B (uA 0 5) vn_5)
  ⟨vn_0, vn_1, vn_2, vn_3, vn_4, vn_5⟩

lemma solveUpper6A_enc (B : Nat) (hB : 0 < B) (uA : Nat → Nat → Aff15N) (uR : Nat → Nat → ℝ)
    (y1A : Vec6N) (y1R : Vec6R) (te : TubeEnv) (hte : te.Valid)
    (hu : ∀ i < 6, ∀ j < 6, (uA i j).Enc B te (uR i j))
    (hy1 : y1A.Enc B te y1R) :
    (solveUpper6A B uA y1A).Enc B te (solveUpper6R uR y1R) := by
  rcases hy1 with ⟨h0, h1, h2, h3, h4, h5⟩
  unfold solveUpper6A solveUpper6R Vec6N.Enc
  dsimp only
  have q5 := h5
  have q4 := a15Sub_enc B _ _ te _ _ h4 (a15Mul_enc B hB _ _ te _ _ hte (hu 4 (by decide) 5 (by decide)) q5)
  have q3 := a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ h3 (a15Mul_enc B hB _ _ te _ _ hte (hu 3 (by decide) 4 (by decide)) q4)) (a15Mul_enc B hB _ _ te _ _ hte (hu 3 (by decide) 5 (by decide)) q5)
  have q2 := a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ h2 (a15Mul_enc B hB _ _ te _ _ hte (hu 2 (by decide) 3 (by decide)) q3)) (a15Mul_enc B hB _ _ te _ _ hte (hu 2 (by decide) 4 (by decide)) q4)) (a15Mul_enc B hB _ _ te _ _ hte (hu 2 (by decide) 5 (by decide)) q5)
  have q1 := a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ h1 (a15Mul_enc B hB _ _ te _ _ hte (hu 1 (by decide) 2 (by decide)) q2)) (a15Mul_enc B hB _ _ te _ _ hte (hu 1 (by decide) 3 (by decide)) q3)) (a15Mul_enc B hB _ _ te _ _ hte (hu 1 (by decide) 4 (by decide)) q4)) (a15Mul_enc B hB _ _ te _ _ hte (hu 1 (by decide) 5 (by decide)) q5)
  have q0 := a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ h0 (a15Mul_enc B hB _ _ te _ _ hte (hu 0 (by decide) 1 (by decide)) q1)) (a15Mul_enc B hB _ _ te _ _ hte (hu 0 (by decide) 2 (by decide)) q2)) (a15Mul_enc B hB _ _ te _ _ hte (hu 0 (by decide) 3 (by decide)) q3)) (a15Mul_enc B hB _ _ te _ _ hte (hu 0 (by decide) 4 (by decide)) q4)) (a15Mul_enc B hB _ _ te _ _ hte (hu 0 (by decide) 5 (by decide)) q5)
  exact ⟨q0, q1, q2, q3, q4, q5⟩

def mulUpper6A (B : Nat) (uA : Nat → Nat → Aff15N) (v : Vec6N) : Vec6N :=
  ⟨a15Add (a15Add (a15Add (a15Add (a15Add v.v0 (a15Mul B (uA 0 1) v.v1)) (a15Mul B (uA 0 2) v.v2)) (a15Mul B (uA 0 3) v.v3)) (a15Mul B (uA 0 4) v.v4)) (a15Mul B (uA 0 5) v.v5),
   a15Add (a15Add (a15Add (a15Add v.v1 (a15Mul B (uA 1 2) v.v2)) (a15Mul B (uA 1 3) v.v3)) (a15Mul B (uA 1 4) v.v4)) (a15Mul B (uA 1 5) v.v5),
   a15Add (a15Add (a15Add v.v2 (a15Mul B (uA 2 3) v.v3)) (a15Mul B (uA 2 4) v.v4)) (a15Mul B (uA 2 5) v.v5),
   a15Add (a15Add v.v3 (a15Mul B (uA 3 4) v.v4)) (a15Mul B (uA 3 5) v.v5),
   a15Add v.v4 (a15Mul B (uA 4 5) v.v5),
   v.v5⟩

lemma mulUpper6A_enc (B : Nat) (hB : 0 < B) (uA : Nat → Nat → Aff15N) (uR : Nat → Nat → ℝ)
    (vA : Vec6N) (vR : Vec6R) (te : TubeEnv) (hte : te.Valid)
    (hu : ∀ i < 6, ∀ j < 6, (uA i j).Enc B te (uR i j))
    (hv : vA.Enc B te vR) :
    (mulUpper6A B uA vA).Enc B te (mulUpper6R uR vR) := by
  rcases hv with ⟨h0, h1, h2, h3, h4, h5⟩
  unfold mulUpper6A mulUpper6R Vec6N.Enc
  dsimp only
  refine ⟨
    a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ h0 (a15Mul_enc B hB _ _ te _ _ hte (hu 0 (by decide) 1 (by decide)) h1)) (a15Mul_enc B hB _ _ te _ _ hte (hu 0 (by decide) 2 (by decide)) h2)) (a15Mul_enc B hB _ _ te _ _ hte (hu 0 (by decide) 3 (by decide)) h3)) (a15Mul_enc B hB _ _ te _ _ hte (hu 0 (by decide) 4 (by decide)) h4)) (a15Mul_enc B hB _ _ te _ _ hte (hu 0 (by decide) 5 (by decide)) h5),
    a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ h1 (a15Mul_enc B hB _ _ te _ _ hte (hu 1 (by decide) 2 (by decide)) h2)) (a15Mul_enc B hB _ _ te _ _ hte (hu 1 (by decide) 3 (by decide)) h3)) (a15Mul_enc B hB _ _ te _ _ hte (hu 1 (by decide) 4 (by decide)) h4)) (a15Mul_enc B hB _ _ te _ _ hte (hu 1 (by decide) 5 (by decide)) h5),
    a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ h2 (a15Mul_enc B hB _ _ te _ _ hte (hu 2 (by decide) 3 (by decide)) h3)) (a15Mul_enc B hB _ _ te _ _ hte (hu 2 (by decide) 4 (by decide)) h4)) (a15Mul_enc B hB _ _ te _ _ hte (hu 2 (by decide) 5 (by decide)) h5),
    a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ h3 (a15Mul_enc B hB _ _ te _ _ hte (hu 3 (by decide) 4 (by decide)) h4)) (a15Mul_enc B hB _ _ te _ _ hte (hu 3 (by decide) 5 (by decide)) h5),
    a15Add_enc B _ _ te _ _ h4 (a15Mul_enc B hB _ _ te _ _ hte (hu 4 (by decide) 5 (by decide)) h5),
    h5⟩

def divDiag6A (B : Nat) (y2 d : Vec6N) : Option Vec6N :=
  match a15Div B y2.v0 d.v0, a15Div B y2.v1 d.v1, a15Div B y2.v2 d.v2,
        a15Div B y2.v3 d.v3, a15Div B y2.v4 d.v4, a15Div B y2.v5 d.v5 with
  | some q0, some q1, some q2, some q3, some q4, some q5 => some ⟨q0, q1, q2, q3, q4, q5⟩
  | _, _, _, _, _, _ => none

lemma divDiag6A_enc (B : Nat) (hB : 0 < B) (y2A dA res : Vec6N) (y2R dR : Vec6R)
    (te : TubeEnv) (hte : te.Valid) (hy2 : y2A.Enc B te y2R) (hd : dA.Enc B te dR)
    (h : divDiag6A B y2A dA = some res) :
    res.Enc B te (divDiag6R y2R dR) := by
  unfold divDiag6A at h
  rcases h0 : a15Div B y2A.v0 dA.v0 with _ | q0; · simp [h0] at h
  rcases h1 : a15Div B y2A.v1 dA.v1 with _ | q1; · simp [h0, h1] at h
  rcases h2 : a15Div B y2A.v2 dA.v2 with _ | q2; · simp [h0, h1, h2] at h
  rcases h3 : a15Div B y2A.v3 dA.v3 with _ | q3; · simp [h0, h1, h2, h3] at h
  rcases h4 : a15Div B y2A.v4 dA.v4 with _ | q4; · simp [h0, h1, h2, h3, h4] at h
  rcases h5 : a15Div B y2A.v5 dA.v5 with _ | q5; · simp [h0, h1, h2, h3, h4, h5] at h
  simp [h0, h1, h2, h3, h4, h5] at h
  rw [← h]
  exact ⟨(a15Div_enc B hB _ _ q0 te _ _ hte hy2.1 hd.1 h0).2,
         (a15Div_enc B hB _ _ q1 te _ _ hte hy2.2.1 hd.2.1 h1).2,
         (a15Div_enc B hB _ _ q2 te _ _ hte hy2.2.2.1 hd.2.2.1 h2).2,
         (a15Div_enc B hB _ _ q3 te _ _ hte hy2.2.2.2.1 hd.2.2.2.1 h3).2,
         (a15Div_enc B hB _ _ q4 te _ _ hte hy2.2.2.2.2.1 hd.2.2.2.2.1 h4).2,
         (a15Div_enc B hB _ _ q5 te _ _ hte hy2.2.2.2.2.2 hd.2.2.2.2.2 h5).2⟩

def mulDiag6A (B : Nat) (d y1 : Vec6N) : Vec6N :=
  ⟨a15Mul B d.v0 y1.v0, a15Mul B d.v1 y1.v1, a15Mul B d.v2 y1.v2,
   a15Mul B d.v3 y1.v3, a15Mul B d.v4 y1.v4, a15Mul B d.v5 y1.v5⟩

lemma mulDiag6A_enc (B : Nat) (hB : 0 < B) (dA y1A : Vec6N) (dR y1R : Vec6R)
    (te : TubeEnv) (hte : te.Valid) (hd : dA.Enc B te dR) (hy1 : y1A.Enc B te y1R) :
    (mulDiag6A B dA y1A).Enc B te (mulDiag6R dR y1R) :=
  ⟨a15Mul_enc B hB _ _ te _ _ hte hd.1 hy1.1,
   a15Mul_enc B hB _ _ te _ _ hte hd.2.1 hy1.2.1,
   a15Mul_enc B hB _ _ te _ _ hte hd.2.2.1 hy1.2.2.1,
   a15Mul_enc B hB _ _ te _ _ hte hd.2.2.2.1 hy1.2.2.2.1,
   a15Mul_enc B hB _ _ te _ _ hte hd.2.2.2.2.1 hy1.2.2.2.2.1,
   a15Mul_enc B hB _ _ te _ _ hte hd.2.2.2.2.2 hy1.2.2.2.2.2⟩

def unpackTubeA15 (P : TubeSpec) (eAff : Aff15N) (vAff : Vec6N) : Option Vec6N :=
  let B := P.B
  let ts := chebBasisA15 B eAff P.nCheb
  let zA := Vec6N.ofFn (fun i => evalChebFromBasis B ts (P.Z_c.getD i.val []))
  let dA := Vec6N.ofFn (fun i => evalChebFromBasis B ts (P.D_c.getD i.val []))
  let lA (i j : Nat) := evalChebFromBasis B ts ((P.L_c.getD i []).getD j [])
  let uA (i j : Nat) := evalChebFromBasis B ts ((P.U_c.getD i []).getD j [])
  if nonZero15 dA.v0 && nonZero15 dA.v1 && nonZero15 dA.v2 &&
     nonZero15 dA.v3 && nonZero15 dA.v4 && nonZero15 dA.v5 then
    let y1 := mulUpper6A B uA vAff
    let y2 := mulDiag6A B dA y1
    let y3 := mulLower6A B lA y2
    some (Vec6N.ofFn (fun orig => a15Add (zA.get orig) (y3.get (P.rowToU.getD orig.val 0))))
  else none

def finishPack6A (B : Nat) (uA : Nat → Nat → Aff15N) (y2 dA : Vec6N) : Option Vec6N :=
  match divDiag6A B y2 dA with
  | some y1 => some (solveUpper6A B uA y1)
  | none    => none

lemma finishPack6A_enc (B : Nat) (hB : 0 < B) (uA : Nat → Nat → Aff15N) (uR : Nat → Nat → ℝ)
    (y2A dA res : Vec6N) (y2R dR : Vec6R) (te : TubeEnv) (hte : te.Valid)
    (hu : ∀ i < 6, ∀ j < 6, (uA i j).Enc B te (uR i j))
    (hy2 : y2A.Enc B te y2R) (hd : dA.Enc B te dR)
    (h : finishPack6A B uA y2A dA = some res) :
    res.Enc B te (solveUpper6R uR (divDiag6R y2R dR)) := by
  unfold finishPack6A at h
  rcases hdiv : divDiag6A B y2A dA with _ | y1
  · simp [hdiv] at h
  simp [hdiv] at h
  rw [← h]
  exact solveUpper6A_enc B hB uA uR y1 _ te hte hu (divDiag6A_enc B hB y2A dA y1 y2R dR te hte hy2 hd hdiv)

def packTubeA15 (P : TubeSpec) (enAff : Aff15N) (z6 : Vec6N) : Option Vec6N :=
  let B := P.B
  let ts := chebBasisA15 B enAff P.nCheb
  let zA := Vec6N.ofFn (fun i => evalChebFromBasis B ts (P.Z_c.getD i.val []))
  let dA := Vec6N.ofFn (fun i => evalChebFromBasis B ts (P.D_c.getD i.val []))
  let lA (i j : Nat) := evalChebFromBasis B ts ((P.L_c.getD i []).getD j [])
  let uA (i j : Nat) := evalChebFromBasis B ts ((P.U_c.getD i []).getD j [])
  let y3 := Vec6N.ofFn (fun k => a15Sub (z6.get (P.uToRow.getD k.val 0)) (zA.get (P.uToRow.getD k.val 0)))
  let y2 := solveLower6A B lA y3
  finishPack6A B uA y2 dA

lemma unpackTubeA15_enc (P : TubeSpec) (hP : P.Valid)
    (eAff : Aff15N) (vAff res : Vec6N) (te : TubeEnv) (eps : ℝ) (vr : Vec6R)
    (hte : te.Valid) (heps : eAff.Enc P.B te eps) (hv : vAff.Enc P.B te vr)
    (h : unpackTubeA15 P eAff vAff = some res) :
    (dVecReal P eps).NonZero ∧ res.Enc P.B te (unpackReal P eps vr) := by
  have hB := hP.1
  have hlenZ := hP.2.2.2.2.2.2.2.2.2.1
  have hlenLU := hP.2.2.2.2.2.2.2.2.2.2
  have hbasis := chebBasisA15_enc P.B hB te hte eAff eps heps P.nCheb
  let ts := chebBasisA15 P.B eAff P.nCheb
  have hzA : (Vec6N.ofFn (fun i => evalChebFromBasis P.B ts (P.Z_c.getD i.val []))).Enc P.B te (zVecReal P eps) :=
    Vec6N.enc_ofFn P.B _ te _ (fun i => evalChebFromBasis_enc P.B hB te hte ts eps P.nCheb hbasis _ (hlenZ i.val i.isLt).1)
  have hdA : (Vec6N.ofFn (fun i => evalChebFromBasis P.B ts (P.D_c.getD i.val []))).Enc P.B te (dVecReal P eps) :=
    Vec6N.enc_ofFn P.B _ te _ (fun i => evalChebFromBasis_enc P.B hB te hte ts eps P.nCheb hbasis _ (hlenZ i.val i.isLt).2)
  have hlA (i : Nat) (hi : i < 6) (j : Nat) (hj : j < 6) :
      (evalChebFromBasis P.B ts ((P.L_c.getD i []).getD j [])).Enc P.B te (lValReal P eps i j) :=
    evalChebFromBasis_enc P.B hB te hte ts eps P.nCheb hbasis _ (hlenLU i hi j hj).1
  have huA (i : Nat) (hi : i < 6) (j : Nat) (hj : j < 6) :
      (evalChebFromBasis P.B ts ((P.U_c.getD i []).getD j [])).Enc P.B te (uValReal P eps i j) :=
    evalChebFromBasis_enc P.B hB te hte ts eps P.nCheb hbasis _ (hlenLU i hi j hj).2
  unfold unpackTubeA15 at h
  dsimp only at h
  split_ifs at h with hnz
  injection h with hres
  simp only [Bool.and_eq_true] at hnz
  have hD_nz : (dVecReal P eps).NonZero :=
    ⟨nonZero15_spec P.B hB _ te _ hte hdA.1 hnz.1.1.1.1.1,
     nonZero15_spec P.B hB _ te _ hte hdA.2.1 hnz.1.1.1.1.2,
     nonZero15_spec P.B hB _ te _ hte hdA.2.2.1 hnz.1.1.1.2,
     nonZero15_spec P.B hB _ te _ hte hdA.2.2.2.1 hnz.1.1.2,
     nonZero15_spec P.B hB _ te _ hte hdA.2.2.2.2.1 hnz.1.2,
     nonZero15_spec P.B hB _ te _ hte hdA.2.2.2.2.2 hnz.2⟩
  refine ⟨hD_nz, ?_⟩
  rw [← hres]
  have hy1 := mulUpper6A_enc P.B hB _ _ vAff vr te hte huA hv
  have hy2 := mulDiag6A_enc P.B hB _ _ _ _ te hte hdA hy1
  have hy3 := mulLower6A_enc P.B hB _ _ _ _ te hte hlA hy2
  unfold unpackReal unpermAdd6R
  exact Vec6N.enc_ofFn P.B _ te _ (fun orig =>
    a15Add_enc P.B _ _ te _ _
      (Vec6N.enc_get P.B _ te _ hzA orig)
      (Vec6N.enc_get P.B _ te _ hy3 (P.rowToU.getD orig.val 0)))

lemma packTubeA15_enc (P : TubeSpec) (hP : P.Valid)
    (enAff : Aff15N) (z6 res : Vec6N) (te : TubeEnv) (en : ℝ) (zr : Vec6R)
    (hte : te.Valid) (hen : enAff.Enc P.B te en) (hz : z6.Enc P.B te zr)
    (h : packTubeA15 P enAff z6 = some res) :
    res.Enc P.B te (packReal P en zr) := by
  have hB := hP.1
  have hlenZ := hP.2.2.2.2.2.2.2.2.2.1
  have hlenLU := hP.2.2.2.2.2.2.2.2.2.2
  have hbasis := chebBasisA15_enc P.B hB te hte enAff en hen P.nCheb
  let ts := chebBasisA15 P.B enAff P.nCheb
  have hzA : (Vec6N.ofFn (fun i => evalChebFromBasis P.B ts (P.Z_c.getD i.val []))).Enc P.B te (zVecReal P en) :=
    Vec6N.enc_ofFn P.B _ te _ (fun i => evalChebFromBasis_enc P.B hB te hte ts en P.nCheb hbasis _ (hlenZ i.val i.isLt).1)
  have hdA : (Vec6N.ofFn (fun i => evalChebFromBasis P.B ts (P.D_c.getD i.val []))).Enc P.B te (dVecReal P en) :=
    Vec6N.enc_ofFn P.B _ te _ (fun i => evalChebFromBasis_enc P.B hB te hte ts en P.nCheb hbasis _ (hlenZ i.val i.isLt).2)
  have hlA (i : Nat) (hi : i < 6) (j : Nat) (hj : j < 6) :
      (evalChebFromBasis P.B ts ((P.L_c.getD i []).getD j [])).Enc P.B te (lValReal P en i j) :=
    evalChebFromBasis_enc P.B hB te hte ts en P.nCheb hbasis _ (hlenLU i hi j hj).1
  have huA (i : Nat) (hi : i < 6) (j : Nat) (hj : j < 6) :
      (evalChebFromBasis P.B ts ((P.U_c.getD i []).getD j [])).Enc P.B te (uValReal P en i j) :=
    evalChebFromBasis_enc P.B hB te hte ts en P.nCheb hbasis _ (hlenLU i hi j hj).2
  have hy3 : (Vec6N.ofFn (fun k => a15Sub (z6.get (P.uToRow.getD k.val 0))
      ((Vec6N.ofFn (fun i => evalChebFromBasis P.B ts (P.Z_c.getD i.val []))).get (P.uToRow.getD k.val 0)))).Enc P.B te
      (permDiff6R P.uToRow zr (zVecReal P en)) :=
    Vec6N.enc_ofFn P.B _ te _ (fun k =>
      a15Sub_enc P.B _ _ te _ _
        (Vec6N.enc_get P.B _ te _ hz _)
        (Vec6N.enc_get P.B _ te _ hzA _))
  have hy2 := solveLower6A_enc P.B hB _ _ _ _ te hte hlA hy3
  exact finishPack6A_enc P.B hB _ _ _ _ res _ _ te hte huA hy2 hdA h

/-! ### Rescaled 1-Step Dynamics (`rescaledStep15`) & Duality Gap Check (`checkGap9`) -/

def checkGap9 (gapLB : Nat) (atx0 atx1 atx2 ay0 ay1 ay2 : Aff15N) : Bool :=
  let lb := sOfNat gapLB
  loGeSInt15 lb (a15Sub atx0 ay0) || loGeSInt15 lb (a15Sub atx0 ay1) || loGeSInt15 lb (a15Sub atx0 ay2) ||
  loGeSInt15 lb (a15Sub atx1 ay0) || loGeSInt15 lb (a15Sub atx1 ay1) || loGeSInt15 lb (a15Sub atx1 ay2) ||
  loGeSInt15 lb (a15Sub atx2 ay0) || loGeSInt15 lb (a15Sub atx2 ay1) || loGeSInt15 lb (a15Sub atx2 ay2)

lemma checkGap9_sound (P : TubeSpec) (hP : P.Valid) (te : TubeEnv) (hte : te.Valid)
    (x y : Fin 3 → ℝ) (hx : Simplex 3 x) (hy : Simplex 3 y)
    (atx0 atx1 atx2 ay0 ay1 ay2 : Aff15N)
    (hatx0 : atx0.Enc P.B te (matTMulVec caiGameA x 0))
    (hatx1 : atx1.Enc P.B te (matTMulVec caiGameA x 1))
    (hatx2 : atx2.Enc P.B te (matTMulVec caiGameA x 2))
    (hay0 : ay0.Enc P.B te (matMulVec caiGameA y 0))
    (hay1 : ay1.Enc P.B te (matMulVec caiGameA y 1))
    (hay2 : ay2.Enc P.B te (matMulVec caiGameA y 2))
    (h : checkGap9 P.gapLB atx0 atx1 atx2 ay0 ay1 ay2 = true) :
    (1 : ℝ) / 20 ≤ DualGap caiGameA x y := by
  have hBr_pos : (0 : ℝ) < (P.B : ℝ) := Nat.cast_pos.mpr hP.1
  have h20 : 20 * (P.gapLB : ℝ) = (P.B : ℝ) := by exact_mod_cast hP.2.2.2.2.2.1
  have pair_step (i₀ j₀ : Fin 3) (atxJ ayI : Aff15N)
      (hJ : atxJ.Enc P.B te (matTMulVec caiGameA x j₀))
      (hI : ayI.Enc P.B te (matMulVec caiGameA y i₀))
      (hpair : loGeSInt15 (sOfNat P.gapLB) (a15Sub atxJ ayI) = true) :
      (1 : ℝ) / 20 ≤ DualGap caiGameA x y := by
    have hlo := loGeSInt15_spec P.B (sOfNat P.gapLB) _ te _ hte (a15Sub_enc P.B _ _ te _ _ hJ hI) hpair
    rw [sOfNat_toReal] at hlo
    have hdiff : (1 : ℝ) / 20 ≤ matTMulVec caiGameA x j₀ - matMulVec caiGameA y i₀ := by
      have hmul : (P.B : ℝ) * ((1 : ℝ) / 20) ≤ (P.B : ℝ) * (matTMulVec caiGameA x j₀ - matMulVec caiGameA y i₀) := by linarith
      exact le_of_mul_le_mul_left hmul hBr_pos
    exact le_trans hdiff (caiGameA_dualGap_ge x y hx hy i₀ j₀)
  unfold checkGap9 at h
  simp only [Bool.or_eq_true] at h
  rcases h with (((((((h00 | h01) | h02) | h10) | h11) | h12) | h20') | h21) | h22
  · exact pair_step 0 0 atx0 ay0 hatx0 hay0 h00
  · exact pair_step 1 0 atx0 ay1 hatx0 hay1 h01
  · exact pair_step 2 0 atx0 ay2 hatx0 hay2 h02
  · exact pair_step 0 1 atx1 ay0 hatx1 hay0 h10
  · exact pair_step 1 1 atx1 ay1 hatx1 hay1 h11
  · exact pair_step 2 1 atx1 ay2 hatx1 hay2 h12
  · exact pair_step 0 2 atx2 ay0 hatx2 hay0 h20'
  · exact pair_step 1 2 atx2 ay1 hatx2 hay1 h21
  · exact pair_step 2 2 atx2 ay2 hatx2 hay2 h22

structure Rescaled15 where
  w0  : Aff15N
  w1  : Aff15N
  w2  : Aff15N
  x0  : Aff15N
  x1  : Aff15N
  x2  : Aff15N
  ry0 : Aff15N
  ry1 : Aff15N
  ry2 : Aff15N
  u0  : Aff15N
  u1  : Aff15N
  u2  : Aff15N

@[inline] def Rescaled15.strictB (r : Rescaled15) : Bool :=
  r.w0.strictB && r.w1.strictB && r.w2.strictB &&
  r.x0.strictB && r.x1.strictB && r.x2.strictB &&
  r.ry0.strictB && r.ry1.strictB && r.ry2.strictB &&
  r.u0.strictB && r.u1.strictB && r.u2.strictB

def RescaledInv (P : TubeSpec) (te : TubeEnv) (Sy eps : ℝ) (st : RMState 3 3) (r : Rescaled15) : Prop :=
  Simplex 3 st.x ∧ Simplex 3 st.y ∧
  ∃ (w0 w1 w2 ry0 ry1 ry2 u0 u1 u2 : ℝ),
    st.Rx 0 = eps * w0 ∧ st.Rx 1 = eps * w1 ∧ st.Rx 2 = eps * w2 ∧
    st.Ry 0 = Sy * ysReal P 0 + ry0 ∧
    st.Ry 1 = Sy * ysReal P 1 + ry1 ∧
    st.Ry 2 = Sy * ysReal P 2 + ry2 ∧
    st.y 0 = ysReal P 0 + eps * u0 ∧
    st.y 1 = ysReal P 1 + eps * u1 ∧
    st.y 2 = ysReal P 2 + eps * u2 ∧
    r.w0.Enc P.B te w0 ∧ r.w1.Enc P.B te w1 ∧ r.w2.Enc P.B te w2 ∧
    r.x0.Enc P.B te (st.x 0) ∧ r.x1.Enc P.B te (st.x 1) ∧ r.x2.Enc P.B te (st.x 2) ∧
    r.ry0.Enc P.B te ry0 ∧ r.ry1.Enc P.B te ry1 ∧ r.ry2.Enc P.B te ry2 ∧
    r.u0.Enc P.B te u0 ∧ r.u1.Enc P.B te u1 ∧ r.u2.Enc P.B te u2

def stepRx15 (sPhase : Nat) (urx0 urx1 urx2 : Aff15N) : Option (Aff15N × Aff15N × Aff15N) :=
  if sPhase == 5 then
    if isPos15 urx0 && isNeg15 urx1 && isPos15 urx2 then
      some (urx0, a15Const sZero, urx2)
    else none
  else
    if isPos15 urx0 && isPos15 urx1 && isPos15 urx2 then
      some (urx0, urx1, urx2)
    else none

lemma stepRx15_sound (B : Nat) (hB : 0 < B) (te : TubeEnv) (hte : te.Valid)
    (eps : ℝ) (heps : 0 < eps) (sPhase : Nat) (urx0 urx1 urx2 wn0 wn1 wn2 : Aff15N)
    (r0 r1 r2 : ℝ) (hu0 : urx0.Enc B te r0) (hu1 : urx1.Enc B te r1) (hu2 : urx2.Enc B te r2)
    (h : stepRx15 sPhase urx0 urx1 urx2 = some (wn0, wn1, wn2)) :
    ∃ (w0' w1' w2' : ℝ),
      max 0 (eps * r0) = eps * w0' ∧
      max 0 (eps * r1) = eps * w1' ∧
      max 0 (eps * r2) = eps * w2' ∧
      wn0.Enc B te w0' ∧ wn1.Enc B te w1' ∧ wn2.Enc B te w2' ∧
      (sPhase = 5 → w1' = 0) := by
  unfold stepRx15 at h
  split_ifs at h with h5 hchk hchk2
  · simp only [Bool.and_eq_true] at hchk
    rcases h with ⟨rfl, rfl, rfl⟩
    have hr0 := isPos15_spec B hB urx0 te r0 hte hu0 hchk.1.1
    have hr1 := isNeg15_spec B hB urx1 te r1 hte hu1 hchk.1.2
    have hr2 := isPos15_spec B hB urx2 te r2 hte hu2 hchk.2
    refine ⟨r0, 0, r2,
      max_eq_right (le_of_lt (mul_pos heps hr0)),
      by rw [mul_zero]; exact max_eq_left (le_of_lt (mul_neg_of_pos_of_neg heps hr1)),
      max_eq_right (le_of_lt (mul_pos heps hr2)),
      hu0, a15Zero_enc B te, hu2, fun _ => rfl⟩
  · simp only [Bool.and_eq_true] at hchk2
    rcases h with ⟨rfl, rfl, rfl⟩
    have hr0 := isPos15_spec B hB urx0 te r0 hte hu0 hchk2.1.1
    have hr1 := isPos15_spec B hB urx1 te r1 hte hu1 hchk2.1.2
    have hr2 := isPos15_spec B hB urx2 te r2 hte hu2 hchk2.2
    refine ⟨r0, r1, r2,
      max_eq_right (le_of_lt (mul_pos heps hr0)),
      max_eq_right (le_of_lt (mul_pos heps hr1)),
      max_eq_right (le_of_lt (mul_pos heps hr2)),
      hu0, hu1, hu2, fun hs5 => absurd (beq_iff_eq.mpr hs5) h5⟩

def stepPx15 (B sPhase : Nat) (upx0 upx1 upx2 : Aff15N) : Option (Aff15N × Aff15N × Aff15N) :=
  if Nat.ble (sPhase + 1) 4 then
    if isPos15 upx0 && isPos15 upx1 && isPos15 upx2 then
      let spx := a15Add (a15Add upx0 upx1) upx2
      match a15Div B upx0 spx, a15Div B upx1 spx, a15Div B upx2 spx with
      | some xn0, some xn1, some xn2 => some (xn0, xn1, xn2)
      | _, _, _ => none
    else none
  else
    if isNeg15 upx0 && isNeg15 upx1 && isPos15 upx2 then
      some (a15Const sZero, a15Const sZero, a15Const (sOfNat B))
    else none

lemma stepPx15_sound (B : Nat) (hB : 0 < B) (te : TubeEnv) (hte : te.Valid)
    (eps : ℝ) (heps : 0 < eps) (sPhase : Nat) (upx0 upx1 upx2 xn0 xn1 xn2 : Aff15N)
    (p0 p1 p2 : ℝ) (px : Fin 3 → ℝ)
    (hpx_nn : ∀ i, 0 ≤ px i)
    (hpx0 : px 0 = max 0 (eps * p0)) (hpx1 : px 1 = max 0 (eps * p1)) (hpx2 : px 2 = max 0 (eps * p2))
    (hp0 : upx0.Enc B te p0) (hp1 : upx1.Enc B te p1) (hp2 : upx2.Enc B te p2)
    (h : stepPx15 B sPhase upx0 upx1 upx2 = some (xn0, xn1, xn2)) :
    xn0.Enc B te (normalize px 0) ∧
    xn1.Enc B te (normalize px 1) ∧
    xn2.Enc B te (normalize px 2) ∧
    (sPhase = 5 → normalize px 0 = 0 ∧ normalize px 1 = 0 ∧ normalize px 2 = 1) := by
  have hBr_ne : (B : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hB)
  have heps_ne : eps ≠ 0 := ne_of_gt heps
  unfold stepPx15 at h
  split_ifs at h with hlt4 hchk hchk2
  · simp only [Bool.and_eq_true] at hchk
    have hr0 := isPos15_spec B hB upx0 te p0 hte hp0 hchk.1.1
    have hr1 := isPos15_spec B hB upx1 te p1 hte hp1 hchk.1.2
    have hr2 := isPos15_spec B hB upx2 te p2 hte hp2 hchk.2
    have hq0 : px 0 = eps * p0 := by rw [hpx0]; exact max_eq_right (le_of_lt (mul_pos heps hr0))
    have hq1 : px 1 = eps * p1 := by rw [hpx1]; exact max_eq_right (le_of_lt (mul_pos heps hr1))
    have hq2 : px 2 = eps * p2 := by rw [hpx2]; exact max_eq_right (le_of_lt (mul_pos heps hr2))
    have hsum_pos : 0 < px 0 + px 1 + px 2 := by
      have : px 0 + px 1 + px 2 = eps * (p0 + p1 + p2) := by linarith
      rw [this]; exact mul_pos heps (by linarith)
    set spx := a15Add (a15Add upx0 upx1) upx2
    have hspx : spx.Enc B te (p0 + p1 + p2) :=
      a15Add_enc B _ _ te _ _ (a15Add_enc B _ _ te _ _ hp0 hp1) hp2
    rcases hd0 : a15Div B upx0 spx with _ | q0; · simp [hd0] at h
    rcases hd1 : a15Div B upx1 spx with _ | q1; · simp [hd0, hd1] at h
    rcases hd2 : a15Div B upx2 spx with _ | q2; · simp [hd0, hd1, hd2] at h
    simp [hd0, hd1, hd2] at h
    rcases h with ⟨rfl, rfl, rfl⟩
    rw [normalize_fin3_of_pos px hpx_nn hsum_pos]; dsimp only
    have hsum_eq : px 0 + px 1 + px 2 = eps * (p0 + p1 + p2) := by linarith
    rw [hsum_eq, hq0, hq1, hq2,
        mul_div_mul_left p0 _ heps_ne,
        mul_div_mul_left p1 _ heps_ne,
        mul_div_mul_left p2 _ heps_ne]
    refine ⟨(a15Div_enc B hB _ _ q0 te _ _ hte hp0 hspx hd0).2,
            (a15Div_enc B hB _ _ q1 te _ _ hte hp1 hspx hd1).2,
            (a15Div_enc B hB _ _ q2 te _ _ hte hp2 hspx hd2).2,
            fun hs5 => by have := Nat.ble_eq.mp hlt4; omega⟩
  · simp only [Bool.and_eq_true] at hchk2
    rcases h with ⟨rfl, rfl, rfl⟩
    have hr0 := isNeg15_spec B hB upx0 te p0 hte hp0 hchk2.1.1
    have hr1 := isNeg15_spec B hB upx1 te p1 hte hp1 hchk2.1.2
    have hr2 := isPos15_spec B hB upx2 te p2 hte hp2 hchk2.2
    have hq0 : px 0 = 0 := by rw [hpx0]; exact max_eq_left (le_of_lt (mul_neg_of_pos_of_neg heps hr0))
    have hq1 : px 1 = 0 := by rw [hpx1]; exact max_eq_left (le_of_lt (mul_neg_of_pos_of_neg heps hr1))
    have hq2_pos : 0 < px 2 := by
      rw [hpx2, max_eq_right (le_of_lt (mul_pos heps hr2))]; exact mul_pos heps hr2
    have hsum_pos : 0 < px 0 + px 1 + px 2 := by linarith
    have hnorm := normalize_fin3_of_pos px hpx_nn hsum_pos
    have hn0 : normalize px 0 = 0 := by rw [hnorm]; dsimp only; rw [hq0, zero_div]
    have hn1 : normalize px 1 = 0 := by rw [hnorm]; dsimp only; rw [hq1, zero_div]
    have hn2 : normalize px 2 = 1 := by
      rw [hnorm]; dsimp only; rw [hq0, hq1, zero_add, zero_add, div_self (ne_of_gt hq2_pos)]
    have hone_enc : (a15Const (sOfNat B)).Enc B te 1 := by
      have h1 := a15Const_enc B hB (sOfNat B) te
      rwa [sOfNat_toReal, div_self hBr_ne] at h1
    rw [hn0, hn1, hn2]
    exact ⟨a15Zero_enc B te, a15Zero_enc B te, hone_enc, fun _ => ⟨rfl, rfl, rfl⟩⟩

def rescaledStep15 (P : TubeSpec) (epsAff : Aff15N) (sPhase : Nat) (r : Rescaled15) :
    Option Rescaled15 :=
  let B := P.B
  let s3 := sOfNat 3
  let s4 := sOfNat 4
  let sm3 := sNegOfNat 3
  let atx0 := a15ScaleSInt s3 r.x0
  let atx1 := a15ScaleSInt s3 r.x1
  let atx2 := a15Add (a15Sub (a15ScaleSInt sm3 r.x0) (a15ScaleSInt s4 r.x1)) r.x2
  let yc0 := a15Add (a15Const (sOfNat P.ys0)) (a15Mul B epsAff r.u0)
  let yc1 := a15Add (a15Const (sOfNat P.ys1)) (a15Mul B epsAff r.u1)
  let yc2 := a15Add (a15Const (sOfNat P.ys2)) (a15Mul B epsAff r.u2)
  let ay0 := a15Sub (a15ScaleSInt s3 yc0) (a15ScaleSInt s3 yc2)
  let ay1 := a15Sub (a15ScaleSInt s3 yc1) (a15ScaleSInt s4 yc2)
  let ay2 := yc2
  if checkGap9 P.gapLB atx0 atx1 atx2 ay0 ay1 ay2 then
    let au0 := a15Sub (a15ScaleSInt s3 r.u0) (a15ScaleSInt s3 r.u2)
    let au1 := a15Sub (a15ScaleSInt s3 r.u1) (a15ScaleSInt s4 r.u2)
    let au2 := r.u2
    let xAu := a15Add (a15Add (a15Mul B r.x0 au0) (a15Mul B r.x1 au1)) (a15Mul B r.x2 au2)
    let fxs0 := a15Sub au0 xAu
    let fxs1 := a15Sub au1 xAu
    let fxs2 := a15Sub au2 xAu
    let yATx := a15Add (a15Add (a15Mul B yc0 atx0) (a15Mul B yc1 atx1)) (a15Mul B yc2 atx2)
    let fy0 := a15Sub atx0 yATx
    let fy1 := a15Sub atx1 yATx
    let fy2 := a15Sub atx2 yATx
    match stepRx15 sPhase (a15Sub r.w0 fxs0) (a15Sub r.w1 fxs1) (a15Sub r.w2 fxs2) with
    | none => none
    | some (wn0, wn1, wn2) =>
      match stepPx15 B sPhase (a15Sub wn0 fxs0) (a15Sub wn1 fxs1) (a15Sub wn2 fxs2) with
      | none => none
      | some (xn0, xn1, xn2) =>
        let ryn0 := a15Add r.ry0 fy0
        let ryn1 := a15Add r.ry1 fy1
        let ryn2 := a15Add r.ry2 fy2
        let rpy0 := a15Add ryn0 fy0
        let rpy1 := a15Add ryn1 fy1
        let rpy2 := a15Add ryn2 fy2
        let ychk :=
          isPos15 (a15Add (a15Const (sOfNat P.ys0)) (a15Mul B epsAff ryn0)) &&
          isPos15 (a15Add (a15Const (sOfNat P.ys1)) (a15Mul B epsAff ryn1)) &&
          isPos15 (a15Add (a15Const (sOfNat P.ys2)) (a15Mul B epsAff ryn2)) &&
          isPos15 (a15Add (a15Const (sOfNat P.ys0)) (a15Mul B epsAff rpy0)) &&
          isPos15 (a15Add (a15Const (sOfNat P.ys1)) (a15Mul B epsAff rpy1)) &&
          isPos15 (a15Add (a15Const (sOfNat P.ys2)) (a15Mul B epsAff rpy2))
        if ychk then
          let srpy := a15Add (a15Add rpy0 rpy1) rpy2
          let denY := a15Add (a15Const (sOfNat B)) (a15Mul B epsAff srpy)
          match a15Div B (a15Sub rpy0 (a15ScaleFixed (sOfNat P.ys0) srpy B)) denY,
                a15Div B (a15Sub rpy1 (a15ScaleFixed (sOfNat P.ys1) srpy B)) denY,
                a15Div B (a15Sub rpy2 (a15ScaleFixed (sOfNat P.ys2) srpy B)) denY with
          | some un0, some un1, some un2 =>
            let out : Rescaled15 := ⟨wn0, wn1, wn2, xn0, xn1, xn2, ryn0, ryn1, ryn2, un0, un1, un2⟩
            if out.strictB then some out else none
          | _, _, _ => none
        else none
  else none

lemma negInstRegret_row_rescaled (P : TubeSpec) (hP : P.Valid)
    (x y : Fin 3 → ℝ) (hx : Simplex 3 x) (eps u0 u1 u2 : ℝ)
    (hy0 : y 0 = ysReal P 0 + eps * u0)
    (hy1 : y 1 = ysReal P 1 + eps * u1)
    (hy2 : y 2 = ysReal P 2 + eps * u2) :
    let au0 := 3 * u0 - 3 * u2
    let au1 := 3 * u1 - 4 * u2
    let au2 := u2
    let xAu := x 0 * au0 + x 1 * au1 + x 2 * au2
    negInstRegret x (matMulVec caiGameA y) 0 = eps * (au0 - xAu) ∧
    negInstRegret x (matMulVec caiGameA y) 1 = eps * (au1 - xAu) ∧
    negInstRegret x (matMulVec caiGameA y) 2 = eps * (au2 - xAu) := by
  rcases ysReal_props P hP with ⟨_, hys0, hys1⟩
  rcases matMulVec_caiGameA y with ⟨hmy0, hmy1, hmy2⟩
  have hxsum : x 0 + x 1 + x 2 = 1 := by
    have hs := hx.2; rwa [sum_fin3] at hs
  have hm0 : matMulVec caiGameA y 0 = ysReal P 2 + eps * (3 * u0 - 3 * u2) := by
    rw [hmy0, hy0, hy2]; linarith
  have hm1 : matMulVec caiGameA y 1 = ysReal P 2 + eps * (3 * u1 - 4 * u2) := by
    rw [hmy1, hy1, hy2]; linarith
  have hm2 : matMulVec caiGameA y 2 = ysReal P 2 + eps * u2 := by
    rw [hmy2, hy2]
  dsimp only
  unfold negInstRegret
  rw [sum_fin3, hm0, hm1, hm2]
  have hdot :
      x 0 * (ysReal P 2 + eps * (3 * u0 - 3 * u2)) +
      x 1 * (ysReal P 2 + eps * (3 * u1 - 4 * u2)) +
      x 2 * (ysReal P 2 + eps * u2) =
      ysReal P 2 + eps * (x 0 * (3 * u0 - 3 * u2) + x 1 * (3 * u1 - 4 * u2) + x 2 * u2) := by
    calc
      x 0 * (ysReal P 2 + eps * (3 * u0 - 3 * u2)) +
        x 1 * (ysReal P 2 + eps * (3 * u1 - 4 * u2)) +
        x 2 * (ysReal P 2 + eps * u2)
        = (x 0 + x 1 + x 2) * ysReal P 2 +
            eps * (x 0 * (3 * u0 - 3 * u2) + x 1 * (3 * u1 - 4 * u2) + x 2 * u2) := by ring
      _ = ysReal P 2 + eps * (x 0 * (3 * u0 - 3 * u2) + x 1 * (3 * u1 - 4 * u2) + x 2 * u2) := by
            rw [hxsum, one_mul]
  rw [hdot]
  exact ⟨by ring, by ring, by ring⟩

lemma col_norm_rescaled (Sy eps ys rpy srpy : ℝ)
    (hepsSy : eps * Sy = 1) (hsum : Sy + srpy ≠ 0) (hden : 1 + eps * srpy ≠ 0) :
    (Sy * ys + rpy) / (Sy + srpy) = ys + eps * ((rpy - ys * srpy) / (1 + eps * srpy)) := by
  have hrhs : ys + eps * ((rpy - ys * srpy) / (1 + eps * srpy)) =
      (ys * (1 + eps * srpy) + eps * (rpy - ys * srpy)) / (1 + eps * srpy) := by
    field_simp [hden]
  rw [hrhs, div_eq_div_iff hsum hden]
  have hid :
      (Sy * ys + rpy) * (1 + eps * srpy) -
      (ys * (1 + eps * srpy) + eps * (rpy - ys * srpy)) * (Sy + srpy) =
      (1 - eps * Sy) * (rpy - ys * srpy) := by ring
  have h0 : 1 - eps * Sy = 0 := by linarith
  linarith [hid, mul_eq_zero_of_left h0 (rpy - ys * srpy)]

lemma rescaledStep15_sound (P : TubeSpec) (hP : P.Valid) (te : TubeEnv) (hte : te.Valid)
    (Sy eps : ℝ) (hSy : 0 < Sy) (heps : 0 < eps) (hepsSy : eps * Sy = 1)
    (epsAff : Aff15N) (hepsAff : epsAff.Enc P.B te eps)
    (sPhase : Nat) (st : RMState 3 3) (r rNext : Rescaled15)
    (hinv : RescaledInv P te Sy eps st r)
    (h : rescaledStep15 P epsAff sPhase r = some rNext) :
    (1 : ℝ) / 20 ≤ DualGap caiGameA st.x st.y ∧
    RescaledInv P te Sy eps (alg2Step caiGameA st) rNext ∧
    (sPhase = 5 →
      (alg2Step caiGameA st).Rx 1 = 0 ∧
      (alg2Step caiGameA st).x 0 = 0 ∧
      (alg2Step caiGameA st).x 1 = 0 ∧
      (alg2Step caiGameA st).x 2 = 1) := by
  have hB := hP.1
  have hBr_ne : (P.B : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hB)
  rcases hinv with ⟨hx_simp, hy_simp, w0, w1, w2, ry0, ry1, ry2, u0, u1, u2,
    hRx0, hRx1, hRx2, hRy0, hRy1, hRy2, hy0, hy1, hy2,
    hw0, hw1, hw2, hx0, hx1, hx2, hry0, hry1, hry2, hu0, hu1, hu2⟩
  rcases matMulVec_caiGameA st.y with ⟨hmy0, hmy1, hmy2⟩
  rcases matTMulVec_caiGameA st.x with ⟨htx0, htx1, htx2⟩
  have hs3 : (sOfNat 3).toReal = 3 := by simp [sOfNat_toReal]
  have hs4 : (sOfNat 4).toReal = 4 := by simp [sOfNat_toReal]
  have hsm3 : (sNegOfNat 3).toReal = -3 := by simp [sNegOfNat_toReal]
  set atx0 := a15ScaleSInt (sOfNat 3) r.x0
  set atx1 := a15ScaleSInt (sOfNat 3) r.x1
  set atx2 := a15Add (a15Sub (a15ScaleSInt (sNegOfNat 3) r.x0) (a15ScaleSInt (sOfNat 4) r.x1)) r.x2
  have hatx0 : atx0.Enc P.B te (matTMulVec caiGameA st.x 0) := by
    rw [htx0]; have t := a15ScaleSInt_enc P.B (sOfNat 3) r.x0 te _ hx0; rwa [hs3] at t
  have hatx1 : atx1.Enc P.B te (matTMulVec caiGameA st.x 1) := by
    rw [htx1]; have t := a15ScaleSInt_enc P.B (sOfNat 3) r.x1 te _ hx1; rwa [hs3] at t
  have hatx2 : atx2.Enc P.B te (matTMulVec caiGameA st.x 2) := by
    rw [htx2]
    have t0 := a15ScaleSInt_enc P.B (sNegOfNat 3) r.x0 te _ hx0; rw [hsm3] at t0
    have t1 := a15ScaleSInt_enc P.B (sOfNat 4) r.x1 te _ hx1; rw [hs4] at t1
    exact a15Add_enc P.B _ _ te _ _ (a15Sub_enc P.B _ _ te _ _ t0 t1) hx2
  have hys0_c : (a15Const (sOfNat P.ys0)).Enc P.B te (ysReal P 0) := by
    rw [ysReal_zero]; have t := a15Const_enc P.B hB (sOfNat P.ys0) te; rwa [sOfNat_toReal] at t
  have hys1_c : (a15Const (sOfNat P.ys1)).Enc P.B te (ysReal P 1) := by
    rw [ysReal_one]; have t := a15Const_enc P.B hB (sOfNat P.ys1) te; rwa [sOfNat_toReal] at t
  have hys2_c : (a15Const (sOfNat P.ys2)).Enc P.B te (ysReal P 2) := by
    rw [ysReal_two]; have t := a15Const_enc P.B hB (sOfNat P.ys2) te; rwa [sOfNat_toReal] at t
  set yc0 := a15Add (a15Const (sOfNat P.ys0)) (a15Mul P.B epsAff r.u0)
  set yc1 := a15Add (a15Const (sOfNat P.ys1)) (a15Mul P.B epsAff r.u1)
  set yc2 := a15Add (a15Const (sOfNat P.ys2)) (a15Mul P.B epsAff r.u2)
  have hyc0 : yc0.Enc P.B te (st.y 0) := by
    rw [hy0]; exact a15Add_enc P.B _ _ te _ _ hys0_c (a15Mul_enc P.B hB _ _ te _ _ hte hepsAff hu0)
  have hyc1 : yc1.Enc P.B te (st.y 1) := by
    rw [hy1]; exact a15Add_enc P.B _ _ te _ _ hys1_c (a15Mul_enc P.B hB _ _ te _ _ hte hepsAff hu1)
  have hyc2 : yc2.Enc P.B te (st.y 2) := by
    rw [hy2]; exact a15Add_enc P.B _ _ te _ _ hys2_c (a15Mul_enc P.B hB _ _ te _ _ hte hepsAff hu2)
  set ay0 := a15Sub (a15ScaleSInt (sOfNat 3) yc0) (a15ScaleSInt (sOfNat 3) yc2)
  set ay1 := a15Sub (a15ScaleSInt (sOfNat 3) yc1) (a15ScaleSInt (sOfNat 4) yc2)
  have hay0 : ay0.Enc P.B te (matMulVec caiGameA st.y 0) := by
    rw [hmy0]
    have t0 := a15ScaleSInt_enc P.B (sOfNat 3) yc0 te _ hyc0; rw [hs3] at t0
    have t2 := a15ScaleSInt_enc P.B (sOfNat 3) yc2 te _ hyc2; rw [hs3] at t2
    exact a15Sub_enc P.B _ _ te _ _ t0 t2
  have hay1 : ay1.Enc P.B te (matMulVec caiGameA st.y 1) := by
    rw [hmy1]
    have t1 := a15ScaleSInt_enc P.B (sOfNat 3) yc1 te _ hyc1; rw [hs3] at t1
    have t2 := a15ScaleSInt_enc P.B (sOfNat 4) yc2 te _ hyc2; rw [hs4] at t2
    exact a15Sub_enc P.B _ _ te _ _ t1 t2
  have hay2 : yc2.Enc P.B te (matMulVec caiGameA st.y 2) := by rw [hmy2]; exact hyc2
  unfold rescaledStep15 at h
  dsimp only at h
  split at h
  case isFalse => nomatch h
  rename_i hgap_eq
  have hgap := checkGap9_sound P hP te hte st.x st.y hx_simp hy_simp
    atx0 atx1 atx2 ay0 ay1 yc2 hatx0 hatx1 hatx2 hay0 hay1 hay2 hgap_eq
  set au0 := a15Sub (a15ScaleSInt (sOfNat 3) r.u0) (a15ScaleSInt (sOfNat 3) r.u2)
  set au1 := a15Sub (a15ScaleSInt (sOfNat 3) r.u1) (a15ScaleSInt (sOfNat 4) r.u2)
  have hau0 : au0.Enc P.B te (3 * u0 - 3 * u2) := by
    have t0 := a15ScaleSInt_enc P.B (sOfNat 3) r.u0 te _ hu0; rw [hs3] at t0
    have t2 := a15ScaleSInt_enc P.B (sOfNat 3) r.u2 te _ hu2; rw [hs3] at t2
    exact a15Sub_enc P.B _ _ te _ _ t0 t2
  have hau1 : au1.Enc P.B te (3 * u1 - 4 * u2) := by
    have t1 := a15ScaleSInt_enc P.B (sOfNat 3) r.u1 te _ hu1; rw [hs3] at t1
    have t2 := a15ScaleSInt_enc P.B (sOfNat 4) r.u2 te _ hu2; rw [hs4] at t2
    exact a15Sub_enc P.B _ _ te _ _ t1 t2
  set xAu := a15Add (a15Add (a15Mul P.B r.x0 au0) (a15Mul P.B r.x1 au1)) (a15Mul P.B r.x2 r.u2)
  set xAu_r := st.x 0 * (3 * u0 - 3 * u2) + st.x 1 * (3 * u1 - 4 * u2) + st.x 2 * u2
  have hxAu : xAu.Enc P.B te xAu_r :=
    a15Add_enc P.B _ _ te _ _
      (a15Add_enc P.B _ _ te _ _
        (a15Mul_enc P.B hB _ _ te _ _ hte hx0 hau0)
        (a15Mul_enc P.B hB _ _ te _ _ hte hx1 hau1))
      (a15Mul_enc P.B hB _ _ te _ _ hte hx2 hu2)
  set fxs0 := a15Sub au0 xAu
  set fxs1 := a15Sub au1 xAu
  set fxs2 := a15Sub r.u2 xAu
  set fxs0_r := (3 * u0 - 3 * u2) - xAu_r
  set fxs1_r := (3 * u1 - 4 * u2) - xAu_r
  set fxs2_r := u2 - xAu_r
  have hfxs0 : fxs0.Enc P.B te fxs0_r := a15Sub_enc P.B _ _ te _ _ hau0 hxAu
  have hfxs1 : fxs1.Enc P.B te fxs1_r := a15Sub_enc P.B _ _ te _ _ hau1 hxAu
  have hfxs2 : fxs2.Enc P.B te fxs2_r := a15Sub_enc P.B _ _ te _ _ hu2 hxAu
  rcases negInstRegret_row_rescaled P hP st.x st.y hx_simp eps u0 u1 u2 hy0 hy1 hy2 with
    ⟨hfx_r0, hfx_r1, hfx_r2⟩
  set yATx := a15Add (a15Add (a15Mul P.B yc0 atx0) (a15Mul P.B yc1 atx1)) (a15Mul P.B yc2 atx2)
  have hyATx : yATx.Enc P.B te (∑ j : Fin 3, st.y j * matTMulVec caiGameA st.x j) := by
    rw [sum_fin3]
    exact a15Add_enc P.B _ _ te _ _
      (a15Add_enc P.B _ _ te _ _
        (a15Mul_enc P.B hB _ _ te _ _ hte hyc0 hatx0)
        (a15Mul_enc P.B hB _ _ te _ _ hte hyc1 hatx1))
      (a15Mul_enc P.B hB _ _ te _ _ hte hyc2 hatx2)
  set fy0 := a15Sub atx0 yATx
  set fy1 := a15Sub atx1 yATx
  set fy2 := a15Sub atx2 yATx
  set fy_r := negInstRegret st.y (matTMulVec caiGameA st.x)
  have hfy0 : fy0.Enc P.B te (fy_r 0) := a15Sub_enc P.B _ _ te _ _ hatx0 hyATx
  have hfy1 : fy1.Enc P.B te (fy_r 1) := a15Sub_enc P.B _ _ te _ _ hatx1 hyATx
  have hfy2 : fy2.Enc P.B te (fy_r 2) := a15Sub_enc P.B _ _ te _ _ hatx2 hyATx
  split at h
  · nomatch h
  rename_i wn0 wn1 wn2 hrx_opt
  rcases stepRx15_sound P.B hB te hte eps heps sPhase _ _ _ wn0 wn1 wn2
      (w0 - fxs0_r) (w1 - fxs1_r) (w2 - fxs2_r)
      (a15Sub_enc P.B _ _ te _ _ hw0 hfxs0)
      (a15Sub_enc P.B _ _ te _ _ hw1 hfxs1)
      (a15Sub_enc P.B _ _ te _ _ hw2 hfxs2) hrx_opt with
    ⟨w0', w1', w2', hw0'_eq, hw1'_eq, hw2'_eq, hwn0, hwn1, hwn2, hw1'_z⟩
  set st' := alg2Step caiGameA st
  have hst'_Rx0 : st'.Rx 0 = eps * w0' := by
    show max 0 (st.Rx 0 - negInstRegret st.x (matMulVec caiGameA st.y) 0) = eps * w0'
    rw [hRx0, hfx_r0, ← mul_sub, hw0'_eq]
  have hst'_Rx1 : st'.Rx 1 = eps * w1' := by
    show max 0 (st.Rx 1 - negInstRegret st.x (matMulVec caiGameA st.y) 1) = eps * w1'
    rw [hRx1, hfx_r1, ← mul_sub, hw1'_eq]
  have hst'_Rx2 : st'.Rx 2 = eps * w2' := by
    show max 0 (st.Rx 2 - negInstRegret st.x (matMulVec caiGameA st.y) 2) = eps * w2'
    rw [hRx2, hfx_r2, ← mul_sub, hw2'_eq]
  split at h
  · nomatch h
  rename_i xn0 xn1 xn2 hpx_opt
  set px_vec := vecPosPart (fun i => st'.Rx i - negInstRegret st.x (matMulVec caiGameA st.y) i)
  have hpx_nn : ∀ i, 0 ≤ px_vec i := fun i => le_max_left 0 _
  have hpx0_eq : px_vec 0 = max 0 (eps * (w0' - fxs0_r)) := by
    show max 0 (st'.Rx 0 - _) = _; rw [hst'_Rx0, hfx_r0, ← mul_sub]
  have hpx1_eq : px_vec 1 = max 0 (eps * (w1' - fxs1_r)) := by
    show max 0 (st'.Rx 1 - _) = _; rw [hst'_Rx1, hfx_r1, ← mul_sub]
  have hpx2_eq : px_vec 2 = max 0 (eps * (w2' - fxs2_r)) := by
    show max 0 (st'.Rx 2 - _) = _; rw [hst'_Rx2, hfx_r2, ← mul_sub]
  rcases stepPx15_sound P.B hB te hte eps heps sPhase _ _ _ xn0 xn1 xn2
      (w0' - fxs0_r) (w1' - fxs1_r) (w2' - fxs2_r) px_vec hpx_nn hpx0_eq hpx1_eq hpx2_eq
      (a15Sub_enc P.B _ _ te _ _ hwn0 hfxs0)
      (a15Sub_enc P.B _ _ te _ _ hwn1 hfxs1)
      (a15Sub_enc P.B _ _ te _ _ hwn2 hfxs2) hpx_opt with
    ⟨hxn0, hxn1, hxn2, hx_lock5⟩
  set ryn0 := a15Add r.ry0 fy0
  set ryn1 := a15Add r.ry1 fy1
  set ryn2 := a15Add r.ry2 fy2
  set rpy0 := a15Add ryn0 fy0
  set rpy1 := a15Add ryn1 fy1
  set rpy2 := a15Add ryn2 fy2
  have hryn0 : ryn0.Enc P.B te (ry0 + fy_r 0) := a15Add_enc P.B _ _ te _ _ hry0 hfy0
  have hryn1 : ryn1.Enc P.B te (ry1 + fy_r 1) := a15Add_enc P.B _ _ te _ _ hry1 hfy1
  have hryn2 : ryn2.Enc P.B te (ry2 + fy_r 2) := a15Add_enc P.B _ _ te _ _ hry2 hfy2
  have hrpy0 : rpy0.Enc P.B te (ry0 + fy_r 0 + fy_r 0) := a15Add_enc P.B _ _ te _ _ hryn0 hfy0
  have hrpy1 : rpy1.Enc P.B te (ry1 + fy_r 1 + fy_r 1) := a15Add_enc P.B _ _ te _ _ hryn1 hfy1
  have hrpy2 : rpy2.Enc P.B te (ry2 + fy_r 2 + fy_r 2) := a15Add_enc P.B _ _ te _ _ hryn2 hfy2
  split at h
  case isFalse => nomatch h
  rename_i hychk
  simp only [Bool.and_eq_true] at hychk
  have pos_from_eps (j : Fin 3) (ys_c a : Aff15N) (vr : ℝ)
      (hysc : ys_c.Enc P.B te (ysReal P j)) (ha : a.Enc P.B te vr)
      (hp : isPos15 (a15Add ys_c (a15Mul P.B epsAff a)) = true) :
      0 < Sy * ysReal P j + vr := by
    have hp' := isPos15_spec P.B hB _ te _ hte
      (a15Add_enc P.B _ _ te _ _ hysc (a15Mul_enc P.B hB _ _ te _ _ hte hepsAff ha)) hp
    have hmul := mul_pos hSy hp'
    have hid : Sy * (ysReal P j + eps * vr) = Sy * ysReal P j + (eps * Sy) * vr := by ring
    rw [hid, hepsSy, one_mul] at hmul
    exact hmul
  have hry_pos0 := pos_from_eps 0 _ ryn0 _ hys0_c hryn0 hychk.1.1.1.1.1
  have hry_pos1 := pos_from_eps 1 _ ryn1 _ hys1_c hryn1 hychk.1.1.1.1.2
  have hry_pos2 := pos_from_eps 2 _ ryn2 _ hys2_c hryn2 hychk.1.1.1.2
  have hrpy_pos0 := pos_from_eps 0 _ rpy0 _ hys0_c hrpy0 hychk.1.1.2
  have hrpy_pos1 := pos_from_eps 1 _ rpy1 _ hys1_c hrpy1 hychk.1.2
  have hrpy_pos2 := pos_from_eps 2 _ rpy2 _ hys2_c hrpy2 hychk.2
  have hst'_Ry0 : st'.Ry 0 = Sy * ysReal P 0 + (ry0 + fy_r 0) := by
    show max 0 (st.Ry 0 + fy_r 0) = _
    rw [hRy0, add_assoc]; exact max_eq_right (le_of_lt hry_pos0)
  have hst'_Ry1 : st'.Ry 1 = Sy * ysReal P 1 + (ry1 + fy_r 1) := by
    show max 0 (st.Ry 1 + fy_r 1) = _
    rw [hRy1, add_assoc]; exact max_eq_right (le_of_lt hry_pos1)
  have hst'_Ry2 : st'.Ry 2 = Sy * ysReal P 2 + (ry2 + fy_r 2) := by
    show max 0 (st.Ry 2 + fy_r 2) = _
    rw [hRy2, add_assoc]; exact max_eq_right (le_of_lt hry_pos2)
  set py_vec := vecPosPart (fun j => st'.Ry j + fy_r j)
  have hpy0 : py_vec 0 = Sy * ysReal P 0 + (ry0 + fy_r 0 + fy_r 0) := by
    show max 0 (st'.Ry 0 + fy_r 0) = _
    rw [hst'_Ry0, add_assoc]; exact max_eq_right (le_of_lt hrpy_pos0)
  have hpy1 : py_vec 1 = Sy * ysReal P 1 + (ry1 + fy_r 1 + fy_r 1) := by
    show max 0 (st'.Ry 1 + fy_r 1) = _
    rw [hst'_Ry1, add_assoc]; exact max_eq_right (le_of_lt hrpy_pos1)
  have hpy2 : py_vec 2 = Sy * ysReal P 2 + (ry2 + fy_r 2 + fy_r 2) := by
    show max 0 (st'.Ry 2 + fy_r 2) = _
    rw [hst'_Ry2, add_assoc]; exact max_eq_right (le_of_lt hrpy_pos2)
  set srpy := a15Add (a15Add rpy0 rpy1) rpy2
  set srpy_r := (ry0 + fy_r 0 + fy_r 0) + (ry1 + fy_r 1 + fy_r 1) + (ry2 + fy_r 2 + fy_r 2)
  have hsrpy : srpy.Enc P.B te srpy_r :=
    a15Add_enc P.B _ _ te _ _ (a15Add_enc P.B _ _ te _ _ hrpy0 hrpy1) hrpy2
  set denY := a15Add (a15Const (sOfNat P.B)) (a15Mul P.B epsAff srpy)
  have h1_enc : (a15Const (sOfNat P.B)).Enc P.B te 1 := by
    have t := a15Const_enc P.B hB (sOfNat P.B) te; rwa [sOfNat_toReal, div_self hBr_ne] at t
  have hdenY : denY.Enc P.B te (1 + eps * srpy_r) :=
    a15Add_enc P.B _ _ te _ _ h1_enc (a15Mul_enc P.B hB _ _ te _ _ hte hepsAff hsrpy)
  split at h
  · rename_i un0 un1 un2 hd0 hd1 hd2
    split at h
    case isFalse => nomatch h
    rename_i hstr
    injection h with hrNext
    rw [← hrNext]
    have hnum0 : (a15Sub rpy0 (a15ScaleFixed (sOfNat P.ys0) srpy P.B)).Enc P.B te
        ((ry0 + fy_r 0 + fy_r 0) - ysReal P 0 * srpy_r) := by
      have t := a15ScaleFixed_enc P.B (sOfNat P.ys0) srpy P.B hB te _ hte hsrpy
      rw [sOfNat_toReal, ← ysReal_zero] at t; exact a15Sub_enc P.B _ _ te _ _ hrpy0 t
    have hnum1 : (a15Sub rpy1 (a15ScaleFixed (sOfNat P.ys1) srpy P.B)).Enc P.B te
        ((ry1 + fy_r 1 + fy_r 1) - ysReal P 1 * srpy_r) := by
      have t := a15ScaleFixed_enc P.B (sOfNat P.ys1) srpy P.B hB te _ hte hsrpy
      rw [sOfNat_toReal, ← ysReal_one] at t; exact a15Sub_enc P.B _ _ te _ _ hrpy1 t
    have hnum2 : (a15Sub rpy2 (a15ScaleFixed (sOfNat P.ys2) srpy P.B)).Enc P.B te
        ((ry2 + fy_r 2 + fy_r 2) - ysReal P 2 * srpy_r) := by
      have t := a15ScaleFixed_enc P.B (sOfNat P.ys2) srpy P.B hB te _ hte hsrpy
      rw [sOfNat_toReal, ← ysReal_two] at t; exact a15Sub_enc P.B _ _ te _ _ hrpy2 t
    have hun0 := a15Div_enc P.B hB _ _ un0 te _ _ hte hnum0 hdenY hd0
    have hun1 := a15Div_enc P.B hB _ _ un1 te _ _ hte hnum1 hdenY hd1
    have hun2 := a15Div_enc P.B hB _ _ un2 te _ _ hte hnum2 hdenY hd2
    have hys_sum := (ysReal_props P hP).1
    have hpy_sum_eq : py_vec 0 + py_vec 1 + py_vec 2 = Sy + srpy_r := by
      rw [hpy0, hpy1, hpy2]
      calc
        (Sy * ysReal P 0 + (ry0 + fy_r 0 + fy_r 0)) +
          (Sy * ysReal P 1 + (ry1 + fy_r 1 + fy_r 1)) +
          (Sy * ysReal P 2 + (ry2 + fy_r 2 + fy_r 2))
          = Sy * (ysReal P 0 + ysReal P 1 + ysReal P 2) + srpy_r := by ring
        _ = Sy + srpy_r := by rw [hys_sum, mul_one]
    have hpy_sum_pos : 0 < py_vec 0 + py_vec 1 + py_vec 2 := by linarith
    have hSy_srpy_ne : Sy + srpy_r ≠ 0 := ne_of_gt (by linarith)
    have hpy_nn : ∀ j, 0 ≤ py_vec j := fun j => le_max_left 0 _
    have hnorm_py := normalize_fin3_of_pos py_vec hpy_nn hpy_sum_pos
    have hst'_y0 : st'.y 0 = ysReal P 0 + eps * (((ry0 + fy_r 0 + fy_r 0) - ysReal P 0 * srpy_r) / (1 + eps * srpy_r)) := by
      show normalize py_vec 0 = _; rw [hnorm_py]; dsimp only
      rw [hpy_sum_eq, hpy0]
      exact col_norm_rescaled Sy eps (ysReal P 0) _ srpy_r hepsSy hSy_srpy_ne hun0.1
    have hst'_y1 : st'.y 1 = ysReal P 1 + eps * (((ry1 + fy_r 1 + fy_r 1) - ysReal P 1 * srpy_r) / (1 + eps * srpy_r)) := by
      show normalize py_vec 1 = _; rw [hnorm_py]; dsimp only
      rw [hpy_sum_eq, hpy1]
      exact col_norm_rescaled Sy eps (ysReal P 1) _ srpy_r hepsSy hSy_srpy_ne hun1.1
    have hst'_y2 : st'.y 2 = ysReal P 2 + eps * (((ry2 + fy_r 2 + fy_r 2) - ysReal P 2 * srpy_r) / (1 + eps * srpy_r)) := by
      show normalize py_vec 2 = _; rw [hnorm_py]; dsimp only
      rw [hpy_sum_eq, hpy2]
      exact col_norm_rescaled Sy eps (ysReal P 2) _ srpy_r hepsSy hSy_srpy_ne hun2.1
    refine ⟨hgap, ⟨simplex_normalize_vecPosPart _, simplex_normalize_vecPosPart _,
      w0', w1', w2', ry0 + fy_r 0, ry1 + fy_r 1, ry2 + fy_r 2,
      ((ry0 + fy_r 0 + fy_r 0) - ysReal P 0 * srpy_r) / (1 + eps * srpy_r),
      ((ry1 + fy_r 1 + fy_r 1) - ysReal P 1 * srpy_r) / (1 + eps * srpy_r),
      ((ry2 + fy_r 2 + fy_r 2) - ysReal P 2 * srpy_r) / (1 + eps * srpy_r),
      hst'_Rx0, hst'_Rx1, hst'_Rx2, hst'_Ry0, hst'_Ry1, hst'_Ry2,
      hst'_y0, hst'_y1, hst'_y2,
      hwn0, hwn1, hwn2, hxn0, hxn1, hxn2, hryn0, hryn1, hryn2,
      hun0.2, hun1.2, hun2.2⟩, ?_⟩
    intro hs5
    have hw1z := hw1'_z hs5
    have hxl := hx_lock5 hs5
    refine ⟨?_, hxl.1, hxl.2.1, hxl.2.2⟩
    rw [hst'_Rx1, hw1z, mul_zero]
  · nomatch h

/-! ### Poincaré Tube `InTube`, Slab Verifier `checkSlab`, and Global Induction -/

noncomputable def tubeSy (st : RMState 3 3) : ℝ :=
  st.Ry 0 + st.Ry 1 + st.Ry 2

noncomputable def tubeZReal (P : TubeSpec) (st : RMState 3 3) : Vec6R :=
  let Sy := tubeSy st
  ⟨Sy * st.Rx 0,
   Sy * st.Rx 2,
   st.Ry 0 - ysReal P 0 * Sy,
   st.Ry 1 - ysReal P 1 * Sy,
   Sy * (st.y 0 - ysReal P 0),
   Sy * (st.y 1 - ysReal P 1)⟩

def InTube (P : TubeSpec) (st : RMState 3 3) : Prop :=
  Simplex 3 st.x ∧ Simplex 3 st.y ∧
  24 ≤ tubeSy st ∧
  st.Rx 1 = 0 ∧ st.x 0 = 0 ∧ st.x 1 = 0 ∧ st.x 2 = 1 ∧
  (packReal P (1 / tubeSy st) (tubeZReal P st)).Bounded P.B P.rInt

def epsSlabAff (k slabHalf : Nat) : Aff15N :=
  ⟨sOfNat ((2 * k + 1) * slabHalf),
   sZero, sZero, sZero, sZero, sZero, sZero,
   sOfNat slabHalf,
   sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, 0⟩

def vBoxAff (rInt : Nat) : Vec6N :=
  let sr := sOfNat rInt
  ⟨⟨sZero, sr, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, 0⟩,
   ⟨sZero, sZero, sr, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, 0⟩,
   ⟨sZero, sZero, sZero, sr, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, 0⟩,
   ⟨sZero, sZero, sZero, sZero, sr, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, 0⟩,
   ⟨sZero, sZero, sZero, sZero, sZero, sr, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, 0⟩,
   ⟨sZero, sZero, sZero, sZero, sZero, sZero, sr, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, 0⟩⟩

def checkSlab (P : TubeSpec) (k : Nat) : Bool :=
  let epsAff := epsSlabAff k P.slabHalf
  match unpackTubeA15 P epsAff (vBoxAff P.rInt) with
  | none => false
  | some z0 =>
    let r0 : Rescaled15 :=
      ⟨z0.v0, a15Const sZero, z0.v1,
       a15Const sZero, a15Const sZero, a15Const (sOfNat P.B),
       z0.v2, z0.v3, a15Neg (a15Add z0.v2 z0.v3),
       z0.v4, z0.v5, a15Neg (a15Add z0.v4 z0.v5)⟩
    match rescaledStep15 P epsAff 0 r0 with
    | none => false
    | some r1 =>
      match rescaledStep15 P epsAff 1 r1 with
      | none => false
      | some r2 =>
        match rescaledStep15 P epsAff 2 r2 with
        | none => false
        | some r3 =>
          match rescaledStep15 P epsAff 3 r3 with
          | none => false
          | some r4 =>
            match rescaledStep15 P epsAff 4 r4 with
            | none => false
            | some r5 =>
              match rescaledStep15 P epsAff 5 r5 with
              | none => false
              | some r6 =>
                let sry := a15Add (a15Add r6.ry0 r6.ry1) r6.ry2
                let rat := a15Add (a15Const (sOfNat P.B)) (a15Mul P.B epsAff sry)
                let zNext : Vec6N :=
                  ⟨a15Mul P.B r6.w0 rat,
                   a15Mul P.B r6.w2 rat,
                   a15Sub r6.ry0 (a15ScaleFixed (sOfNat P.ys0) sry P.B),
                   a15Sub r6.ry1 (a15ScaleFixed (sOfNat P.ys1) sry P.B),
                   a15Mul P.B r6.u0 rat,
                   a15Mul P.B r6.u1 rat⟩
                match a15Div P.B epsAff rat with
                | none => false
                | some enAff =>
                  match packTubeA15 P enAff zNext with
                  | none => false
                  | some vNext =>
                    vec6AbsLe15 P.rInt vNext &&
                    (if Nat.ble 6144 (25 * (k + 1)) then
                       isPos15 sry
                     else
                       loGeSInt15 (sNegOfNat P.halfB) sry)

lemma makeSlabEnv (P : TubeSpec) (hP : P.Valid) (k : Nat) (eps : ℝ) (vr : Vec6R)
    (heps_lo : (k : ℝ) / 6144 ≤ eps) (heps_hi : eps ≤ ((k + 1 : Nat) : ℝ) / 6144)
    (hvr : vr.Bounded P.B P.rInt) :
    ∃ te : TubeEnv, te.Valid ∧
      (epsSlabAff k P.slabHalf).Enc P.B te eps ∧
      (vBoxAff P.rInt).Enc P.B te vr := by
  have hr_pos : (0 : ℝ) < (P.rInt : ℝ) := Nat.cast_pos.mpr hP.2.2.2.2.2.2.2.1
  have hr_ne : (P.rInt : ℝ) ≠ 0 := ne_of_gt hr_pos
  have hslab : 12288 * (P.slabHalf : ℝ) = (P.B : ℝ) := by exact_mod_cast hP.2.2.2.2.2.2.1
  let te : TubeEnv :=
    ⟨((P.B : ℝ) * vr.v0) / (P.rInt : ℝ),
     ((P.B : ℝ) * vr.v1) / (P.rInt : ℝ),
     ((P.B : ℝ) * vr.v2) / (P.rInt : ℝ),
     ((P.B : ℝ) * vr.v3) / (P.rInt : ℝ),
     ((P.B : ℝ) * vr.v4) / (P.rInt : ℝ),
     ((P.B : ℝ) * vr.v5) / (P.rInt : ℝ),
     12288 * eps - (2 * (k : ℝ) + 1)⟩
  have coord_valid (v : ℝ) (hv : |(P.B : ℝ) * v| ≤ (P.rInt : ℝ)) :
      |((P.B : ℝ) * v) / (P.rInt : ℝ)| ≤ 1 := by
    rw [abs_div, abs_of_pos hr_pos, div_le_one hr_pos]; exact hv
  have he6_valid : |12288 * eps - (2 * (k : ℝ) + 1)| ≤ 1 := by
    push_cast at heps_hi
    rw [abs_le]; constructor <;> linarith
  have hte : te.Valid :=
    ⟨coord_valid vr.v0 hvr.1, coord_valid vr.v1 hvr.2.1, coord_valid vr.v2 hvr.2.2.1,
     coord_valid vr.v3 hvr.2.2.2.1, coord_valid vr.v4 hvr.2.2.2.2.1, coord_valid vr.v5 hvr.2.2.2.2.2,
     he6_valid⟩
  refine ⟨te, hte, ?_, ?_⟩
  · unfold Aff15N.Enc epsSlabAff Aff15N.linEval
    dsimp only [te]
    simp only [sOfNat_toReal, sZero_toReal, zero_mul, add_zero, zero_add]
    push_cast
    have hid : (P.B : ℝ) * eps -
        (((2 * (k : ℝ) + 1) * (P.slabHalf : ℝ)) + (P.slabHalf : ℝ) * (12288 * eps - (2 * (k : ℝ) + 1))) = 0 := by
      rw [← hslab]; ring
    rw [hid]; norm_num
  · unfold vBoxAff Vec6N.Enc Aff15N.Enc Aff15N.linEval
    dsimp only [te]
    simp only [sOfNat_toReal, sZero_toReal, zero_mul, add_zero, zero_add]
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> (rw [mul_div_cancel₀ _ hr_ne]; norm_num)

lemma checkSlab_sound (P : TubeSpec) (hP : P.Valid) (k : Nat)
    (hchk : checkSlab P k = true) (st : RMState 3 3) (htube : InTube P st)
    (heps_lo : (k : ℝ) / 6144 ≤ 1 / tubeSy st)
    (heps_hi : 1 / tubeSy st ≤ ((k + 1 : Nat) : ℝ) / 6144) :
    (∀ m < 6, (1 : ℝ) / 20 ≤ DualGap caiGameA (alg2IterFrom st m).x (alg2IterFrom st m).y) ∧
    InTube P (alg2IterFrom st 6) := by
  have hB := hP.1
  have hBr_pos : (0 : ℝ) < (P.B : ℝ) := Nat.cast_pos.mpr hB
  have hBr_ne : (P.B : ℝ) ≠ 0 := ne_of_gt hBr_pos
  rcases htube with ⟨hx_simp, hy_simp, hSy24, hRx1_0, hx0_0, hx1_0, hx2_1, hv_bdd⟩
  set Sy := tubeSy st
  set eps := 1 / Sy
  have hSy_pos : 0 < Sy := by linarith
  have hSy_ne : Sy ≠ 0 := ne_of_gt hSy_pos
  have heps_pos : 0 < eps := div_pos zero_lt_one hSy_pos
  have hepsSy : eps * Sy = 1 := one_div_mul_cancel hSy_ne
  rcases makeSlabEnv P hP k eps (packReal P eps (tubeZReal P st)) heps_lo heps_hi hv_bdd with
    ⟨te, hte, hepsAff, hvBox⟩
  unfold checkSlab at hchk
  set epsAff := epsSlabAff k P.slabHalf
  rcases hunp : unpackTubeA15 P epsAff (vBoxAff P.rInt) with _ | z0
  · simp [hunp] at hchk
  simp only [hunp] at hchk
  rcases unpackTubeA15_enc P hP epsAff (vBoxAff P.rInt) z0 te eps _ hte hepsAff hvBox hunp with
    ⟨hD_nz, hz0_enc⟩
  rw [unpackReal_packReal P hP.2.2.2.2.2.2.2.2.1 eps (tubeZReal P st) hD_nz] at hz0_enc
  set r0 : Rescaled15 :=
    ⟨z0.v0, a15Const sZero, z0.v1,
     a15Const sZero, a15Const sZero, a15Const (sOfNat P.B),
     z0.v2, z0.v3, a15Neg (a15Add z0.v2 z0.v3),
     z0.v4, z0.v5, a15Neg (a15Add z0.v4 z0.v5)⟩
  have h1_enc : (a15Const (sOfNat P.B)).Enc P.B te 1 := by
    have t := a15Const_enc P.B hB (sOfNat P.B) te; rwa [sOfNat_toReal, div_self hBr_ne] at t
  have hys_sum := (ysReal_props P hP).1
  have hy_sum : st.y 0 + st.y 1 + st.y 2 = 1 := by
    have hs := hy_simp.2; rwa [sum_fin3] at hs
  have hr0_inv : RescaledInv P te Sy eps st r0 := by
    refine ⟨hx_simp, hy_simp,
      Sy * st.Rx 0, 0, Sy * st.Rx 2,
      st.Ry 0 - ysReal P 0 * Sy, st.Ry 1 - ysReal P 1 * Sy, -((st.Ry 0 - ysReal P 0 * Sy) + (st.Ry 1 - ysReal P 1 * Sy)),
      Sy * (st.y 0 - ysReal P 0), Sy * (st.y 1 - ysReal P 1), -((Sy * (st.y 0 - ysReal P 0)) + (Sy * (st.y 1 - ysReal P 1))),
      ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_,
      hz0_enc.1, a15Zero_enc P.B te, hz0_enc.2.1,
      by rw [hx0_0]; exact a15Zero_enc P.B te,
      by rw [hx1_0]; exact a15Zero_enc P.B te,
      by rw [hx2_1]; exact h1_enc,
      hz0_enc.2.2.1, hz0_enc.2.2.2.1,
      a15Neg_enc P.B _ te _ (a15Add_enc P.B _ _ te _ _ hz0_enc.2.2.1 hz0_enc.2.2.2.1),
      hz0_enc.2.2.2.2.1, hz0_enc.2.2.2.2.2,
      a15Neg_enc P.B _ te _ (a15Add_enc P.B _ _ te _ _ hz0_enc.2.2.2.2.1 hz0_enc.2.2.2.2.2)⟩
    · calc st.Rx 0 = 1 * st.Rx 0 := (one_mul _).symm
        _ = (eps * Sy) * st.Rx 0 := by rw [hepsSy]
        _ = eps * (Sy * st.Rx 0) := mul_assoc _ _ _
    · rw [hRx1_0, mul_zero]
    · calc st.Rx 2 = 1 * st.Rx 2 := (one_mul _).symm
        _ = (eps * Sy) * st.Rx 2 := by rw [hepsSy]
        _ = eps * (Sy * st.Rx 2) := mul_assoc _ _ _
    · ring
    · ring
    · have hSy_def : st.Ry 0 + st.Ry 1 + st.Ry 2 = Sy := rfl
      calc st.Ry 2 = Sy - st.Ry 0 - st.Ry 1 := by linarith
        _ = Sy * (ysReal P 0 + ysReal P 1 + ysReal P 2) - st.Ry 0 - st.Ry 1 := by rw [hys_sum, mul_one]
        _ = Sy * ysReal P 2 + -((st.Ry 0 - ysReal P 0 * Sy) + (st.Ry 1 - ysReal P 1 * Sy)) := by ring
    · calc st.y 0 = ysReal P 0 + 1 * (st.y 0 - ysReal P 0) := by ring
        _ = ysReal P 0 + (eps * Sy) * (st.y 0 - ysReal P 0) := by rw [hepsSy]
        _ = ysReal P 0 + eps * (Sy * (st.y 0 - ysReal P 0)) := by ring
    · calc st.y 1 = ysReal P 1 + 1 * (st.y 1 - ysReal P 1) := by ring
        _ = ysReal P 1 + (eps * Sy) * (st.y 1 - ysReal P 1) := by rw [hepsSy]
        _ = ysReal P 1 + eps * (Sy * (st.y 1 - ysReal P 1)) := by ring
    · have hu2_eq : -(Sy * (st.y 0 - ysReal P 0) + Sy * (st.y 1 - ysReal P 1)) =
          Sy * (st.y 2 - ysReal P 2) := by
        have hdiff : (st.y 0 + st.y 1 + st.y 2) - (ysReal P 0 + ysReal P 1 + ysReal P 2) = 0 := by
          rw [hy_sum, hys_sum, sub_self]
        calc -(Sy * (st.y 0 - ysReal P 0) + Sy * (st.y 1 - ysReal P 1))
            = Sy * (st.y 2 - ysReal P 2) - Sy * ((st.y 0 + st.y 1 + st.y 2) - (ysReal P 0 + ysReal P 1 + ysReal P 2)) := by ring
          _ = Sy * (st.y 2 - ysReal P 2) := by rw [hdiff, mul_zero, sub_zero]
      rw [hu2_eq]
      calc st.y 2 = ysReal P 2 + 1 * (st.y 2 - ysReal P 2) := by ring
        _ = ysReal P 2 + (eps * Sy) * (st.y 2 - ysReal P 2) := by rw [hepsSy]
        _ = ysReal P 2 + eps * (Sy * (st.y 2 - ysReal P 2)) := by ring
  rcases hs0 : rescaledStep15 P epsAff 0 r0 with _ | r1; · simp [hs0] at hchk
  rcases hs1 : rescaledStep15 P epsAff 1 r1 with _ | r2; · simp [hs0, hs1] at hchk
  rcases hs2 : rescaledStep15 P epsAff 2 r2 with _ | r3; · simp [hs0, hs1, hs2] at hchk
  rcases hs3 : rescaledStep15 P epsAff 3 r3 with _ | r4; · simp [hs0, hs1, hs2, hs3] at hchk
  rcases hs4 : rescaledStep15 P epsAff 4 r4 with _ | r5; · simp [hs0, hs1, hs2, hs3, hs4] at hchk
  rcases hs5 : rescaledStep15 P epsAff 5 r5 with _ | r6; · simp [hs0, hs1, hs2, hs3, hs4, hs5] at hchk
  simp only [hs0, hs1, hs2, hs3, hs4, hs5] at hchk
  rcases rescaledStep15_sound P hP te hte Sy eps hSy_pos heps_pos hepsSy epsAff hepsAff 0 (alg2IterFrom st 0) r0 r1 hr0_inv hs0 with ⟨hg0, hr1_inv, _⟩
  rcases rescaledStep15_sound P hP te hte Sy eps hSy_pos heps_pos hepsSy epsAff hepsAff 1 (alg2IterFrom st 1) r1 r2 hr1_inv hs1 with ⟨hg1, hr2_inv, _⟩
  rcases rescaledStep15_sound P hP te hte Sy eps hSy_pos heps_pos hepsSy epsAff hepsAff 2 (alg2IterFrom st 2) r2 r3 hr2_inv hs2 with ⟨hg2, hr3_inv, _⟩
  rcases rescaledStep15_sound P hP te hte Sy eps hSy_pos heps_pos hepsSy epsAff hepsAff 3 (alg2IterFrom st 3) r3 r4 hr3_inv hs3 with ⟨hg3, hr4_inv, _⟩
  rcases rescaledStep15_sound P hP te hte Sy eps hSy_pos heps_pos hepsSy epsAff hepsAff 4 (alg2IterFrom st 4) r4 r5 hr4_inv hs4 with ⟨hg4, hr5_inv, _⟩
  rcases rescaledStep15_sound P hP te hte Sy eps hSy_pos heps_pos hepsSy epsAff hepsAff 5 (alg2IterFrom st 5) r5 r6 hr5_inv hs5 with ⟨hg5, hr6_inv, hlock6⟩
  have hlocks := hlock6 rfl
  have hgaps : ∀ m < 6, (1 : ℝ) / 20 ≤ DualGap caiGameA (alg2IterFrom st m).x (alg2IterFrom st m).y := by
    intro m hm
    have hc : m = 0 ∨ m = 1 ∨ m = 2 ∨ m = 3 ∨ m = 4 ∨ m = 5 := by omega
    rcases hc with rfl | rfl | rfl | rfl | rfl | rfl
    · exact hg0
    · exact hg1
    · exact hg2
    · exact hg3
    · exact hg4
    · exact hg5
  refine ⟨hgaps, ?_⟩
  let st6 := alg2Step caiGameA (alg2IterFrom st 5)
  rcases hr6_inv with ⟨hx6_simp, hy6_simp, w0, w1, w2, ry0, ry1, ry2, u0, u1, u2,
    hRx6_0, _, hRx6_2, hRy6_0, hRy6_1, hRy6_2, hy6_0, hy6_1, _,
    hw0, _, hw2, _, _, _, hry0, hry1, hry2, hu0, hu1, _⟩
  set sry := a15Add (a15Add r6.ry0 r6.ry1) r6.ry2
  set sry_r := ry0 + ry1 + ry2
  have hsry : sry.Enc P.B te sry_r :=
    a15Add_enc P.B _ _ te _ _ (a15Add_enc P.B _ _ te _ _ hry0 hry1) hry2
  set rat := a15Add (a15Const (sOfNat P.B)) (a15Mul P.B epsAff sry)
  set rat_r := 1 + eps * sry_r
  have hrat : rat.Enc P.B te rat_r :=
    a15Add_enc P.B _ _ te _ _ h1_enc (a15Mul_enc P.B hB _ _ te _ _ hte hepsAff hsry)
  rcases hen_opt : a15Div P.B epsAff rat with _ | enAff
  · simp [hen_opt] at hchk
  simp only [hen_opt] at hchk
  rcases hpack_opt : packTubeA15 P enAff
      ⟨a15Mul P.B r6.w0 rat,
       a15Mul P.B r6.w2 rat,
       a15Sub r6.ry0 (a15ScaleFixed (sOfNat P.ys0) sry P.B),
       a15Sub r6.ry1 (a15ScaleFixed (sOfNat P.ys1) sry P.B),
       a15Mul P.B r6.u0 rat,
       a15Mul P.B r6.u1 rat⟩ with _ | vNext
  · simp [hpack_opt] at hchk
  simp only [hpack_opt, Bool.and_eq_true] at hchk
  have hSy6_eq : tubeSy st6 = Sy + sry_r := by
    unfold tubeSy
    rw [hRy6_0, hRy6_1, hRy6_2]
    calc (Sy * ysReal P 0 + ry0) + (Sy * ysReal P 1 + ry1) + (Sy * ysReal P 2 + ry2)
        = Sy * (ysReal P 0 + ysReal P 1 + ysReal P 2) + sry_r := by ring
      _ = Sy + sry_r := by rw [hys_sum, mul_one]
  have hSy6_ge24 : 24 ≤ tubeSy st6 := by
    rw [hSy6_eq]
    have hsy_chk := hchk.2
    split_ifs at hsy_chk with htop
    · have hsry_pos := isPos15_spec P.B hB sry te sry_r hte hsry hsy_chk
      linarith
    · have hlt : 25 * (k + 1) < 6144 := Nat.not_le.mp (fun hle => htop (Nat.ble_eq.mpr hle))
      have hlt_r : (25 : ℝ) * ((k + 1 : Nat) : ℝ) < 6144 := by exact_mod_cast hlt
      have heps_lt : eps < (1 : ℝ) / 25 := by linarith
      have hSy_gt25 : 25 < Sy := by
        have hmul : 25 * eps < 1 := by linarith
        have hmul2 := mul_lt_mul_of_pos_right hmul hSy_pos
        have hid : 25 * eps * Sy = 25 * (eps * Sy) := by ring
        rw [hid, hepsSy, mul_one, one_mul] at hmul2
        exact hmul2
      have hlo := loGeSInt15_spec P.B (sNegOfNat P.halfB) sry te sry_r hte hsry hsy_chk
      rw [sNegOfNat_toReal] at hlo
      have h2half : (P.B : ℝ) = 2 * (P.halfB : ℝ) := by exact_mod_cast hP.2.1
      have hsry_ge : -((1 : ℝ) / 2) ≤ sry_r := by
        have hm : (P.B : ℝ) * (-((1 : ℝ) / 2)) ≤ (P.B : ℝ) * sry_r := by linarith
        exact le_of_mul_le_mul_left hm hBr_pos
      linarith
  have hSy6_rat : tubeSy st6 = Sy * rat_r := by
    rw [hSy6_eq]
    calc Sy + sry_r = Sy + (eps * Sy) * sry_r := by rw [hepsSy, one_mul]
      _ = Sy * (1 + eps * sry_r) := by ring
  have hen_enc : enAff.Enc P.B te (1 / tubeSy st6) := by
    have hdiv := (a15Div_enc P.B hB _ _ enAff te _ _ hte hepsAff hrat hen_opt).2
    have heq : eps / rat_r = 1 / tubeSy st6 := by
      rw [hSy6_rat]
      change (1 / Sy) / rat_r = 1 / (Sy * rat_r)
      rw [div_div]
    rwa [heq] at hdiv
  have hzNext_enc :
      (Vec6N.mk
        (a15Mul P.B r6.w0 rat)
        (a15Mul P.B r6.w2 rat)
        (a15Sub r6.ry0 (a15ScaleFixed (sOfNat P.ys0) sry P.B))
        (a15Sub r6.ry1 (a15ScaleFixed (sOfNat P.ys1) sry P.B))
        (a15Mul P.B r6.u0 rat)
        (a15Mul P.B r6.u1 rat)).Enc P.B te (tubeZReal P st6) := by
    unfold Vec6N.Enc tubeZReal
    dsimp only
    have hz0' : tubeSy st6 * st6.Rx 0 = w0 * rat_r := by
      rw [hSy6_rat, hRx6_0]
      calc (Sy * rat_r) * (eps * w0) = (eps * Sy) * (w0 * rat_r) := by ring
        _ = w0 * rat_r := by rw [hepsSy, one_mul]
    have hz1' : tubeSy st6 * st6.Rx 2 = w2 * rat_r := by
      rw [hSy6_rat, hRx6_2]
      calc (Sy * rat_r) * (eps * w2) = (eps * Sy) * (w2 * rat_r) := by ring
        _ = w2 * rat_r := by rw [hepsSy, one_mul]
    have hz2' : st6.Ry 0 - ysReal P 0 * tubeSy st6 = ry0 - ysReal P 0 * sry_r := by
      rw [hRy6_0, hSy6_eq]; ring
    have hz3' : st6.Ry 1 - ysReal P 1 * tubeSy st6 = ry1 - ysReal P 1 * sry_r := by
      rw [hRy6_1, hSy6_eq]; ring
    have hz4' : tubeSy st6 * (st6.y 0 - ysReal P 0) = u0 * rat_r := by
      rw [hSy6_rat, hy6_0]
      calc (Sy * rat_r) * (ysReal P 0 + eps * u0 - ysReal P 0) = (eps * Sy) * (u0 * rat_r) := by ring
        _ = u0 * rat_r := by rw [hepsSy, one_mul]
    have hz5' : tubeSy st6 * (st6.y 1 - ysReal P 1) = u1 * rat_r := by
      rw [hSy6_rat, hy6_1]
      calc (Sy * rat_r) * (ysReal P 1 + eps * u1 - ysReal P 1) = (eps * Sy) * (u1 * rat_r) := by ring
        _ = u1 * rat_r := by rw [hepsSy, one_mul]
    rw [hz0', hz1', hz2', hz3', hz4', hz5']
    have hs0_f := a15ScaleFixed_enc P.B (sOfNat P.ys0) sry P.B hB te _ hte hsry
    rw [sOfNat_toReal, ← ysReal_zero] at hs0_f
    have hs1_f := a15ScaleFixed_enc P.B (sOfNat P.ys1) sry P.B hB te _ hte hsry
    rw [sOfNat_toReal, ← ysReal_one] at hs1_f
    exact ⟨a15Mul_enc P.B hB _ _ te _ _ hte hw0 hrat,
           a15Mul_enc P.B hB _ _ te _ _ hte hw2 hrat,
           a15Sub_enc P.B _ _ te _ _ hry0 hs0_f,
           a15Sub_enc P.B _ _ te _ _ hry1 hs1_f,
           a15Mul_enc P.B hB _ _ te _ _ hte hu0 hrat,
           a15Mul_enc P.B hB _ _ te _ _ hte hu1 hrat⟩
  have hvNext_enc := packTubeA15_enc P hP enAff _ vNext te (1 / tubeSy st6) (tubeZReal P st6)
    hte hen_enc hzNext_enc hpack_opt
  have hvNext_bdd := vec6AbsLe15_spec P.B P.rInt vNext te _ hte hvNext_enc hchk.1
  exact ⟨hx6_simp, hy6_simp, hSy6_ge24, hlocks.1, hlocks.2.1, hlocks.2.2.1, hlocks.2.2.2, hvNext_bdd⟩

/-! ### Covering `(0, 1/24]` by `256` Slabs, `T₀` Entry Check, and Global Theorem -/

lemma exists_nat_bin_of_le : ∀ (N : Nat) (x : ℝ),
    0 < N → 0 ≤ x → x ≤ (N : ℝ) →
    ∃ k < N, (k : ℝ) ≤ x ∧ x ≤ ((k + 1 : Nat) : ℝ)
  | 0, _, hN, _, _ => by omega
  | 1, x, _, hx0, hx1 => ⟨0, by omega, by norm_num; exact hx0, by norm_num; exact hx1⟩
  | m + 2, x, _, hx0, hxN => by
    by_cases hle : x ≤ ((m + 1 : Nat) : ℝ)
    · rcases exists_nat_bin_of_le (m + 1) x (by omega) hx0 hle with ⟨k, hk, hlo, hhi⟩
      exact ⟨k, by omega, hlo, hhi⟩
    · have hgt : ((m + 1 : Nat) : ℝ) < x := lt_of_not_ge hle
      exact ⟨m + 1, by omega, le_of_lt hgt, hxN⟩

lemma tube_step6_of_all_slabs (P : TubeSpec) (hP : P.Valid)
    (hslabs : ∀ k < 256, checkSlab P k = true)
    (st : RMState 3 3) (htube : InTube P st) :
    (∀ m < 6, (1 : ℝ) / 20 ≤ DualGap caiGameA (alg2IterFrom st m).x (alg2IterFrom st m).y) ∧
    InTube P (alg2IterFrom st 6) := by
  have hSy24 := htube.2.2.1
  have hSy_pos : 0 < tubeSy st := by linarith
  set eps := 1 / tubeSy st
  have heps0 : 0 ≤ 6144 * eps := by
    have : 0 < eps := div_pos zero_lt_one hSy_pos
    linarith
  have heps256 : 6144 * eps ≤ ((256 : Nat) : ℝ) := by
    have h1 : eps ≤ (1 : ℝ) / 24 := one_div_le_one_div_of_le (by norm_num) hSy24
    norm_num; linarith
  rcases exists_nat_bin_of_le 256 (6144 * eps) (by decide) heps0 heps256 with ⟨k, hk, hlo, hhi⟩
  exact checkSlab_sound P hP k (hslabs k hk) st htube (by linarith) (by linarith)

def checkT0InTube (P : TubeSpec) (s : State12) : Bool :=
  let sy12 := a12Add (a12Add s.ry0 s.ry1) s.ry2
  if isExactZero12 s.rx1 && isExactZero12 s.x0 && isExactZero12 s.x1 &&
     isExactOne12 P.B s.x2 && sNonneg (sSub sy12.lo (sOfNat (24 * P.B))) then
    let sy15 := a15FromA12Iv sy12
    match a15InvPos P.B sy15 with
    | none => false
    | some epsT0 =>
      let rx0_15 := a15FromA12Iv s.rx0
      let rx2_15 := a15FromA12Iv s.rx2
      let ry0_15 := a15FromA12Iv s.ry0
      let ry1_15 := a15FromA12Iv s.ry1
      let y0_15  := a15FromA12Iv s.y0
      let y1_15  := a15FromA12Iv s.y1
      let zT0 : Vec6N :=
        ⟨a15Mul P.B sy15 rx0_15,
         a15Mul P.B sy15 rx2_15,
         a15Sub ry0_15 (a15ScaleFixed (sOfNat P.ys0) sy15 P.B),
         a15Sub ry1_15 (a15ScaleFixed (sOfNat P.ys1) sy15 P.B),
         a15Mul P.B sy15 (a15Sub y0_15 (a15Const (sOfNat P.ys0))),
         a15Mul P.B sy15 (a15Sub y1_15 (a15Const (sOfNat P.ys1)))⟩
      match packTubeA15 P epsT0 zT0 with
      | none => false
      | some vT0 => vec6AbsLe15 P.rInt vT0
  else false

lemma checkT0InTube_sound (P : TubeSpec) (hP : P.Valid) (s : State12) (st : RMState 3 3)
    (hsimp : Simplex 3 st.x ∧ Simplex 3 st.y)
    (henc : ∃ e : Fin 12 → ℝ, ValidEnv12 e ∧ s.Enc P.B e st)
    (h : checkT0InTube P s = true) :
    InTube P st := by
  have hB := hP.1
  have hBr_pos : (0 : ℝ) < (P.B : ℝ) := Nat.cast_pos.mpr hB
  rcases henc with ⟨e12, he12, hs⟩
  have h0 := hs 0; have h1 := hs 1; have h2 := hs 2
  have h3 := hs 3; have h4 := hs 4; have h5 := hs 5
  have h6 := hs 6; have h7 := hs 7; have h8 := hs 8
  have h9 := hs 9; have h10 := hs 10
  dsimp only [State12.get, rmStateCoord] at h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10
  unfold checkT0InTube at h
  dsimp only at h
  split_ifs at h with hpre
  simp only [Bool.and_eq_true] at hpre
  rcases hpre with ⟨⟨⟨⟨h1_z, h6_z⟩, h7_z⟩, h8_o⟩, hsy_nn⟩
  set sy12 := a12Add (a12Add s.ry0 s.ry1) s.ry2
  have hsy12 : sy12.Enc P.B e12 (tubeSy st) :=
    a12Add_enc P.B _ _ e12 _ _ (a12Add_enc P.B _ _ e12 _ _ h3 h4) h5
  split at h
  · nomatch h
  rename_i epsT0 hinv
  split at h
  · nomatch h
  rename_i vT0 hpack
  have hRx1 := isExactZero12_enc P.B hB s.rx1 e12 (st.Rx 1) he12 h1 h1_z
  have hx0 := isExactZero12_enc P.B hB s.x0 e12 (st.x 0) he12 h6 h6_z
  have hx1 := isExactZero12_enc P.B hB s.x1 e12 (st.x 1) he12 h7 h7_z
  have hx2 := isExactOne12_enc P.B hB s.x2 e12 (st.x 2) he12 h8 h8_o
  have hSy_ge24 : 24 ≤ tubeSy st := by
    have hlo := (sy12.bounds_of_enc P.B e12 (tubeSy st) he12 hsy12).2.1
    have hnn := sNonneg_spec _ hsy_nn
    rw [sSub_toReal, sOfNat_toReal] at hnn
    push_cast at hnn
    have hm : (P.B : ℝ) * 24 ≤ (P.B : ℝ) * tubeSy st := by linarith
    exact le_of_mul_le_mul_left hm hBr_pos
  let te0 : TubeEnv := ⟨0, 0, 0, 0, 0, 0, 0⟩
  have hte0 : te0.Valid := by unfold TubeEnv.Valid; dsimp only [te0]; norm_num
  have hsy15 := a15FromA12Iv_enc P.B sy12 e12 te0 (tubeSy st) he12 hsy12
  have hepsT0 := (a15InvPos_enc P.B hB _ epsT0 te0 (tubeSy st) hte0 hsy15 hinv).2
  have hrx0_15 := a15FromA12Iv_enc P.B s.rx0 e12 te0 (st.Rx 0) he12 h0
  have hrx2_15 := a15FromA12Iv_enc P.B s.rx2 e12 te0 (st.Rx 2) he12 h2
  have hry0_15 := a15FromA12Iv_enc P.B s.ry0 e12 te0 (st.Ry 0) he12 h3
  have hry1_15 := a15FromA12Iv_enc P.B s.ry1 e12 te0 (st.Ry 1) he12 h4
  have hy0_15  := a15FromA12Iv_enc P.B s.y0  e12 te0 (st.y 0)  he12 h9
  have hy1_15  := a15FromA12Iv_enc P.B s.y1  e12 te0 (st.y 1)  he12 h10
  have hys0_c : (a15Const (sOfNat P.ys0)).Enc P.B te0 (ysReal P 0) := by
    rw [ysReal_zero]; have t := a15Const_enc P.B hB (sOfNat P.ys0) te0; rwa [sOfNat_toReal] at t
  have hys1_c : (a15Const (sOfNat P.ys1)).Enc P.B te0 (ysReal P 1) := by
    rw [ysReal_one]; have t := a15Const_enc P.B hB (sOfNat P.ys1) te0; rwa [sOfNat_toReal] at t
  have hs0_f := a15ScaleFixed_enc P.B (sOfNat P.ys0) (a15FromA12Iv sy12) P.B hB te0 _ hte0 hsy15
  rw [sOfNat_toReal, ← ysReal_zero] at hs0_f
  have hs1_f := a15ScaleFixed_enc P.B (sOfNat P.ys1) (a15FromA12Iv sy12) P.B hB te0 _ hte0 hsy15
  rw [sOfNat_toReal, ← ysReal_one] at hs1_f
  have hzT0 :
      (Vec6N.mk
        (a15Mul P.B (a15FromA12Iv sy12) (a15FromA12Iv s.rx0))
        (a15Mul P.B (a15FromA12Iv sy12) (a15FromA12Iv s.rx2))
        (a15Sub (a15FromA12Iv s.ry0) (a15ScaleFixed (sOfNat P.ys0) (a15FromA12Iv sy12) P.B))
        (a15Sub (a15FromA12Iv s.ry1) (a15ScaleFixed (sOfNat P.ys1) (a15FromA12Iv sy12) P.B))
        (a15Mul P.B (a15FromA12Iv sy12) (a15Sub (a15FromA12Iv s.y0) (a15Const (sOfNat P.ys0))))
        (a15Mul P.B (a15FromA12Iv sy12) (a15Sub (a15FromA12Iv s.y1) (a15Const (sOfNat P.ys1))))).Enc P.B te0
        (tubeZReal P st) :=
    ⟨a15Mul_enc P.B hB _ _ te0 _ _ hte0 hsy15 hrx0_15,
     a15Mul_enc P.B hB _ _ te0 _ _ hte0 hsy15 hrx2_15,
     a15Sub_enc P.B _ _ te0 _ _ hry0_15 hs0_f,
     a15Sub_enc P.B _ _ te0 _ _ hry1_15 hs1_f,
     a15Mul_enc P.B hB _ _ te0 _ _ hte0 hsy15 (a15Sub_enc P.B _ _ te0 _ _ hy0_15 hys0_c),
     a15Mul_enc P.B hB _ _ te0 _ _ hte0 hsy15 (a15Sub_enc P.B _ _ te0 _ _ hy1_15 hys1_c)⟩
  have hvT0 := packTubeA15_enc P hP epsT0 _ vT0 te0 (1 / tubeSy st) (tubeZReal P st) hte0 hepsT0 hzT0 hpack
  have hv_bdd := vec6AbsLe15_spec P.B P.rInt vT0 te0 _ hte0 hvT0 h
  exact ⟨hsimp.1, hsimp.2, hSy_ge24, hRx1, hx0, hx1, hx2, hv_bdd⟩

theorem eventual_dualityGap_of_tube (P : TubeSpec) (hSpec : checkTubeSpec P = true)
    (hslabs : ∀ k < 256, checkSlab P k = true)
    (T₀ : Nat) (sT0 : State12)
    (hReach : ∃ e : Fin 12 → ℝ, ValidEnv12 e ∧ sT0.Enc P.B e (alg2Iter caiGameA T₀))
    (hEntry : checkT0InTube P sT0 = true) :
    ∀ t : Nat, T₀ ≤ t →
      (1 : ℝ) / 20 ≤ DualGap caiGameA (alg2Iter caiGameA t).x (alg2Iter caiGameA t).y := by
  have hP := checkTubeSpec_sound P hSpec
  have hTube0 : InTube P (alg2Iter caiGameA T₀) :=
    checkT0InTube_sound P hP sT0 (alg2Iter caiGameA T₀) (alg2Iter_simplex T₀) hReach hEntry
  have hBlock : ∀ q : Nat, InTube P (alg2Iter caiGameA (T₀ + 6 * q)) := by
    intro q
    induction q with
    | zero => simpa using hTube0
    | succ q ih =>
      have hidx : T₀ + 6 * (q + 1) = (T₀ + 6 * q) + 6 := by omega
      rw [hidx, alg2Iter_eq_from]
      exact (tube_step6_of_all_slabs P hP hslabs _ ih).2
  intro t ht
  let q := (t - T₀) / 6
  let r := (t - T₀) % 6
  have hr : r < 6 := Nat.mod_lt _ (by decide)
  have ht_eq : t = (T₀ + 6 * q) + r := by omega
  rw [ht_eq, alg2Iter_eq_from]
  exact (tube_step6_of_all_slabs P hP hslabs _ (hBlock q)).1 r hr

end PRMPlus
