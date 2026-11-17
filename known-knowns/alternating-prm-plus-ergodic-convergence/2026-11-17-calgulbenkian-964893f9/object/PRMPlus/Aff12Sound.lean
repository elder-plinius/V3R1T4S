import PRMPlus.Defs

/-!
# Verified `SInt` and 12-Symbol Affine Arithmetic (`Aff12N`) for Reachability (`t = 0 .. T₀`)

All arithmetic operations and soundness proofs are parameterized by an abstract positive scale
`(B : Nat) (hB : 0 < B)` so tactics (`ring`, `linarith`, `field_simp`) and the Lean kernel treat
`(B : ℝ)` as an atomic variable.
-/

namespace PRMPlus

open scoped BigOperators

structure SInt where
  p : Nat
  n : Nat
  deriving DecidableEq

noncomputable def SInt.toReal (x : SInt) : ℝ := (x.p : ℝ) - (x.n : ℝ)

@[inline] def sZero : SInt := ⟨0, 0⟩
@[inline] def sOfNat (k : Nat) : SInt := ⟨k, 0⟩
@[inline] def sNegOfNat (k : Nat) : SInt := ⟨0, k⟩
@[inline] def sNeg (x : SInt) : SInt := ⟨x.n, x.p⟩

@[inline] def sNorm (x : SInt) : SInt :=
  if Nat.ble x.n x.p then ⟨Nat.sub x.p x.n, 0⟩ else ⟨0, Nat.sub x.n x.p⟩

@[inline] def sAbs (x : SInt) : Nat :=
  if Nat.ble x.n x.p then Nat.sub x.p x.n else Nat.sub x.n x.p

@[inline] def sAdd (x y : SInt) : SInt := sNorm ⟨Nat.add x.p y.p, Nat.add x.n y.n⟩
@[inline] def sSub (x y : SInt) : SInt := sNorm ⟨Nat.add x.p y.n, Nat.add x.n y.p⟩
@[inline] def sMul (x y : SInt) : SInt :=
  sNorm ⟨Nat.add (Nat.mul x.p y.p) (Nat.mul x.n y.n), Nat.add (Nat.mul x.p y.n) (Nat.mul x.n y.p)⟩
@[inline] def sMulNat (k : Nat) (x : SInt) : SInt := sNorm ⟨Nat.mul k x.p, Nat.mul k x.n⟩

@[inline] def sDivRem (x : SInt) (d : Nat) : SInt × Nat :=
  let xn := sNorm x
  (⟨Nat.div xn.p d, Nat.div xn.n d⟩, Nat.add (Nat.mod xn.p d) (Nat.mod xn.n d))

@[inline] def cdivOver (num d : Nat) : Nat := Nat.add (Nat.div num d) 1

@[inline] def sStrict (x : SInt) : Bool := Nat.beq x.p x.p && Nat.beq x.n x.n
@[inline] def sNonneg (x : SInt) : Bool := Nat.ble x.n x.p
@[inline] def sNonpos (x : SInt) : Bool := Nat.ble x.p x.n
@[inline] def sPosNat (x : SInt) : Option Nat :=
  if Nat.ble (x.n + 1) x.p then some (x.p - x.n) else none

lemma sZero_toReal : sZero.toReal = 0 := by unfold sZero SInt.toReal; simp
lemma sOfNat_toReal (k : Nat) : (sOfNat k).toReal = (k : ℝ) := by unfold sOfNat SInt.toReal; simp
lemma sNegOfNat_toReal (k : Nat) : (sNegOfNat k).toReal = -(k : ℝ) := by unfold sNegOfNat SInt.toReal; simp
lemma sNeg_toReal (x : SInt) : (sNeg x).toReal = -x.toReal := by unfold sNeg SInt.toReal; ring

private lemma nat_add_eq (a b : Nat) : Nat.add a b = a + b := rfl
private lemma nat_sub_eq (a b : Nat) : Nat.sub a b = a - b := rfl
private lemma nat_mul_eq (a b : Nat) : Nat.mul a b = a * b := rfl
private lemma nat_div_eq (a b : Nat) : Nat.div a b = a / b := rfl
private lemma nat_mod_eq (a b : Nat) : Nat.mod a b = a % b := rfl

lemma sNorm_toReal (x : SInt) : (sNorm x).toReal = x.toReal := by
  unfold sNorm SInt.toReal
  simp only [nat_sub_eq]
  split_ifs with h
  · have hle : x.n ≤ x.p := Nat.ble_eq.mp h
    simp [Nat.cast_sub hle]
  · have hlt : x.p < x.n := Nat.not_le.mp (fun hle => h (Nat.ble_eq.mpr hle))
    have hle : x.p ≤ x.n := Nat.le_of_lt hlt
    simp [Nat.cast_sub hle]

lemma sAbs_toReal (x : SInt) : (sAbs x : ℝ) = |x.toReal| := by
  unfold sAbs SInt.toReal
  simp only [nat_sub_eq]
  split_ifs with h
  · have hle : x.n ≤ x.p := Nat.ble_eq.mp h
    have hcast : (x.n : ℝ) ≤ (x.p : ℝ) := Nat.cast_le.mpr hle
    rw [Nat.cast_sub hle, abs_of_nonneg (by linarith)]
  · have hlt : x.p < x.n := Nat.not_le.mp (fun hle => h (Nat.ble_eq.mpr hle))
    have hle : x.p ≤ x.n := Nat.le_of_lt hlt
    have hcast : (x.p : ℝ) ≤ (x.n : ℝ) := Nat.cast_le.mpr hle
    rw [Nat.cast_sub hle, abs_of_nonpos (by linarith)]
    ring

lemma sAdd_toReal (x y : SInt) : (sAdd x y).toReal = x.toReal + y.toReal := by
  unfold sAdd; rw [sNorm_toReal]; unfold SInt.toReal; simp only [nat_add_eq]; push_cast; ring

lemma sSub_toReal (x y : SInt) : (sSub x y).toReal = x.toReal - y.toReal := by
  unfold sSub; rw [sNorm_toReal]; unfold SInt.toReal; simp only [nat_add_eq]; push_cast; ring

lemma sMul_toReal (x y : SInt) : (sMul x y).toReal = x.toReal * y.toReal := by
  unfold sMul; rw [sNorm_toReal]; unfold SInt.toReal; simp only [nat_add_eq, nat_mul_eq]; push_cast; ring

lemma sMulNat_toReal (k : Nat) (x : SInt) : (sMulNat k x).toReal = (k : ℝ) * x.toReal := by
  unfold sMulNat; rw [sNorm_toReal]; unfold SInt.toReal; simp only [nat_mul_eq]; push_cast; ring

lemma sDivRem_spec (x : SInt) (d : Nat) :
    |x.toReal - (d : ℝ) * (sDivRem x d).1.toReal| ≤ ((sDivRem x d).2 : ℝ) := by
  unfold sDivRem
  simp only [nat_div_eq, nat_mod_eq, nat_add_eq]
  set xn := sNorm x
  have h1 : d * (xn.p / d) + xn.p % d = xn.p := Nat.div_add_mod xn.p d
  have h2 : d * (xn.n / d) + xn.n % d = xn.n := Nat.div_add_mod xn.n d
  have h1r : (d : ℝ) * ((xn.p / d : Nat) : ℝ) + ((xn.p % d : Nat) : ℝ) = (xn.p : ℝ) := by
    exact_mod_cast h1
  have h2r : (d : ℝ) * ((xn.n / d : Nat) : ℝ) + ((xn.n % d : Nat) : ℝ) = (xn.n : ℝ) := by
    exact_mod_cast h2
  rw [(sNorm_toReal x).symm]
  unfold SInt.toReal
  dsimp only
  have hdiff :
      (xn.p : ℝ) - (xn.n : ℝ) - (d : ℝ) * (((xn.p / d : Nat) : ℝ) - ((xn.n / d : Nat) : ℝ)) =
      ((xn.p % d : Nat) : ℝ) - ((xn.n % d : Nat) : ℝ) := by linarith
  rw [hdiff]
  have hp0 : (0 : ℝ) ≤ ((xn.p % d : Nat) : ℝ) := Nat.cast_nonneg _
  have hn0 : (0 : ℝ) ≤ ((xn.n % d : Nat) : ℝ) := Nat.cast_nonneg _
  push_cast
  rw [abs_le]
  constructor <;> linarith

lemma cdivOver_spec (num d : Nat) (hd : 0 < d) :
    (num : ℝ) ≤ (cdivOver num d : ℝ) * (d : ℝ) := by
  unfold cdivOver
  simp only [nat_div_eq, nat_add_eq]
  have h1 : d * (num / d) + num % d = num := Nat.div_add_mod num d
  have h2 : num % d < d := Nat.mod_lt num hd
  have hle : num ≤ (num / d + 1) * d := by
    have : (num / d + 1) * d = d * (num / d) + d := by ring
    omega
  exact_mod_cast hle

lemma sNonneg_spec (x : SInt) (h : sNonneg x = true) : 0 ≤ x.toReal := by
  unfold sNonneg at h
  have hcast : (x.n : ℝ) ≤ (x.p : ℝ) := Nat.cast_le.mpr (Nat.ble_eq.mp h)
  unfold SInt.toReal; linarith

lemma sNonpos_spec (x : SInt) (h : sNonpos x = true) : x.toReal ≤ 0 := by
  unfold sNonpos at h
  have hcast : (x.p : ℝ) ≤ (x.n : ℝ) := Nat.cast_le.mpr (Nat.ble_eq.mp h)
  unfold SInt.toReal; linarith

lemma sPosNat_spec (x : SInt) (m : Nat) (h : sPosNat x = some m) :
    0 < m ∧ x.toReal = (m : ℝ) := by
  unfold sPosNat at h
  split_ifs at h with hble
  · injection h with hm
    have hlt : x.n + 1 ≤ x.p := Nat.ble_eq.mp hble
    have hpos : 0 < x.p - x.n := by omega
    rw [← hm]
    refine ⟨hpos, ?_⟩
    unfold SInt.toReal
    have hle : x.n ≤ x.p := by omega
    rw [Nat.cast_sub hle]

lemma sStrict_true (x : SInt) : sStrict x = true := by unfold sStrict; simp

lemma abs_mul_le_of_abs_le_one (a y : ℝ) (hy : |y| ≤ 1) : |a * y| ≤ |a| := by
  rw [abs_mul]; nlinarith [abs_nonneg a, abs_nonneg y]

lemma abs_div_rem_term (x : SInt) (d : Nat) (ej : ℝ) (hej : |ej| ≤ 1) :
    |(x.toReal - (d : ℝ) * (sDivRem x d).1.toReal) * ej| ≤ ((sDivRem x d).2 : ℝ) :=
  le_trans (abs_mul_le_of_abs_le_one _ ej hej) (sDivRem_spec x d)

structure Aff12N where
  c   : SInt
  a0  : SInt
  a1  : SInt
  a2  : SInt
  a3  : SInt
  a4  : SInt
  a5  : SInt
  a6  : SInt
  a7  : SInt
  a8  : SInt
  a9  : SInt
  a10 : SInt
  a11 : SInt
  err : Nat
  deriving DecidableEq

def ValidEnv12 (e : Fin 12 → ℝ) : Prop := ∀ j : Fin 12, |e j| ≤ 1

noncomputable def Aff12N.linEval (x : Aff12N) (e : Fin 12 → ℝ) : ℝ :=
  x.a0.toReal * e 0 + x.a1.toReal * e 1 + x.a2.toReal * e 2 + x.a3.toReal * e 3 +
  x.a4.toReal * e 4 + x.a5.toReal * e 5 + x.a6.toReal * e 6 + x.a7.toReal * e 7 +
  x.a8.toReal * e 8 + x.a9.toReal * e 9 + x.a10.toReal * e 10 + x.a11.toReal * e 11

def Aff12N.Enc (B : Nat) (x : Aff12N) (e : Fin 12 → ℝ) (v : ℝ) : Prop :=
  |(B : ℝ) * v - (x.c.toReal + x.linEval e)| ≤ (x.err : ℝ)

@[inline] def Aff12N.radSum (x : Aff12N) : Nat :=
  sAbs x.a0 + sAbs x.a1 + sAbs x.a2 + sAbs x.a3 + sAbs x.a4 + sAbs x.a5 +
  sAbs x.a6 + sAbs x.a7 + sAbs x.a8 + sAbs x.a9 + sAbs x.a10 + sAbs x.a11

@[inline] def Aff12N.rad (x : Aff12N) : Nat := x.radSum + x.err
@[inline] def Aff12N.lo (x : Aff12N) : SInt := sSub x.c (sOfNat x.rad)
@[inline] def Aff12N.hi (x : Aff12N) : SInt := sAdd x.c (sOfNat x.rad)

@[inline] def Aff12N.strictB (x : Aff12N) : Bool :=
  sStrict x.c && sStrict x.a0 && sStrict x.a1 && sStrict x.a2 && sStrict x.a3 &&
  sStrict x.a4 && sStrict x.a5 && sStrict x.a6 && sStrict x.a7 && sStrict x.a8 &&
  sStrict x.a9 && sStrict x.a10 && sStrict x.a11 && Nat.beq x.err x.err

lemma Aff12N.strictB_true (x : Aff12N) : x.strictB = true := by
  unfold Aff12N.strictB; simp [sStrict_true]

lemma Aff12N.abs_linEval_le (x : Aff12N) (e : Fin 12 → ℝ) (he : ValidEnv12 e) :
    |x.linEval e| ≤ (x.radSum : ℝ) := by
  unfold Aff12N.linEval Aff12N.radSum
  push_cast; simp only [sAbs_toReal]
  have h0 := abs_mul_le_of_abs_le_one x.a0.toReal (e 0) (he 0)
  have h1 := abs_mul_le_of_abs_le_one x.a1.toReal (e 1) (he 1)
  have h2 := abs_mul_le_of_abs_le_one x.a2.toReal (e 2) (he 2)
  have h3 := abs_mul_le_of_abs_le_one x.a3.toReal (e 3) (he 3)
  have h4 := abs_mul_le_of_abs_le_one x.a4.toReal (e 4) (he 4)
  have h5 := abs_mul_le_of_abs_le_one x.a5.toReal (e 5) (he 5)
  have h6 := abs_mul_le_of_abs_le_one x.a6.toReal (e 6) (he 6)
  have h7 := abs_mul_le_of_abs_le_one x.a7.toReal (e 7) (he 7)
  have h8 := abs_mul_le_of_abs_le_one x.a8.toReal (e 8) (he 8)
  have h9 := abs_mul_le_of_abs_le_one x.a9.toReal (e 9) (he 9)
  have h10 := abs_mul_le_of_abs_le_one x.a10.toReal (e 10) (he 10)
  have h11 := abs_mul_le_of_abs_le_one x.a11.toReal (e 11) (he 11)
  rw [abs_le] at h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11 ⊢
  constructor <;> linarith

lemma Aff12N.bounds_of_enc (B : Nat) (x : Aff12N) (e : Fin 12 → ℝ) (v : ℝ)
    (he : ValidEnv12 e) (hx : x.Enc B e v) :
    |(B : ℝ) * v - x.c.toReal| ≤ (x.rad : ℝ) ∧
    x.lo.toReal ≤ (B : ℝ) * v ∧ (B : ℝ) * v ≤ x.hi.toReal := by
  have hlin := x.abs_linEval_le e he
  unfold Aff12N.Enc at hx
  unfold Aff12N.lo Aff12N.hi Aff12N.rad
  rw [sSub_toReal, sAdd_toReal, sOfNat_toReal]
  push_cast
  rw [abs_le] at hx hlin ⊢
  refine ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩

def a12Const (c : SInt) : Aff12N :=
  ⟨c, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, 0⟩

def a12Add (x y : Aff12N) : Aff12N :=
  ⟨sAdd x.c y.c,
   sAdd x.a0 y.a0, sAdd x.a1 y.a1, sAdd x.a2 y.a2, sAdd x.a3 y.a3,
   sAdd x.a4 y.a4, sAdd x.a5 y.a5, sAdd x.a6 y.a6, sAdd x.a7 y.a7,
   sAdd x.a8 y.a8, sAdd x.a9 y.a9, sAdd x.a10 y.a10, sAdd x.a11 y.a11,
   x.err + y.err⟩

def a12Sub (x y : Aff12N) : Aff12N :=
  ⟨sSub x.c y.c,
   sSub x.a0 y.a0, sSub x.a1 y.a1, sSub x.a2 y.a2, sSub x.a3 y.a3,
   sSub x.a4 y.a4, sSub x.a5 y.a5, sSub x.a6 y.a6, sSub x.a7 y.a7,
   sSub x.a8 y.a8, sSub x.a9 y.a9, sSub x.a10 y.a10, sSub x.a11 y.a11,
   x.err + y.err⟩

def a12ScaleSInt (k : SInt) (x : Aff12N) : Aff12N :=
  ⟨sMul k x.c,
   sMul k x.a0, sMul k x.a1, sMul k x.a2, sMul k x.a3,
   sMul k x.a4, sMul k x.a5, sMul k x.a6, sMul k x.a7,
   sMul k x.a8, sMul k x.a9, sMul k x.a10, sMul k x.a11,
   sAbs k * x.err⟩

def a12ScaleFixed (k : SInt) (x : Aff12N) (denom : Nat) : Aff12N :=
  let (qc, rc)   := sDivRem (sMul k x.c) denom
  let (q0, r0)   := sDivRem (sMul k x.a0) denom
  let (q1, r1)   := sDivRem (sMul k x.a1) denom
  let (q2, r2)   := sDivRem (sMul k x.a2) denom
  let (q3, r3)   := sDivRem (sMul k x.a3) denom
  let (q4, r4)   := sDivRem (sMul k x.a4) denom
  let (q5, r5)   := sDivRem (sMul k x.a5) denom
  let (q6, r6)   := sDivRem (sMul k x.a6) denom
  let (q7, r7)   := sDivRem (sMul k x.a7) denom
  let (q8, r8)   := sDivRem (sMul k x.a8) denom
  let (q9, r9)   := sDivRem (sMul k x.a9) denom
  let (q10, r10) := sDivRem (sMul k x.a10) denom
  let (q11, r11) := sDivRem (sMul k x.a11) denom
  let rem := rc + r0 + r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9 + r10 + r11 + sAbs k * x.err
  ⟨qc, q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, cdivOver rem denom⟩

def a12Mul (B : Nat) (x y : Aff12N) : Aff12N :=
  let (qc, rc)   := sDivRem (sMul x.c y.c) B
  let (q0, r0)   := sDivRem (sAdd (sMul x.c y.a0) (sMul y.c x.a0)) B
  let (q1, r1)   := sDivRem (sAdd (sMul x.c y.a1) (sMul y.c x.a1)) B
  let (q2, r2)   := sDivRem (sAdd (sMul x.c y.a2) (sMul y.c x.a2)) B
  let (q3, r3)   := sDivRem (sAdd (sMul x.c y.a3) (sMul y.c x.a3)) B
  let (q4, r4)   := sDivRem (sAdd (sMul x.c y.a4) (sMul y.c x.a4)) B
  let (q5, r5)   := sDivRem (sAdd (sMul x.c y.a5) (sMul y.c x.a5)) B
  let (q6, r6)   := sDivRem (sAdd (sMul x.c y.a6) (sMul y.c x.a6)) B
  let (q7, r7)   := sDivRem (sAdd (sMul x.c y.a7) (sMul y.c x.a7)) B
  let (q8, r8)   := sDivRem (sAdd (sMul x.c y.a8) (sMul y.c x.a8)) B
  let (q9, r9)   := sDivRem (sAdd (sMul x.c y.a9) (sMul y.c x.a9)) B
  let (q10, r10) := sDivRem (sAdd (sMul x.c y.a10) (sMul y.c x.a10)) B
  let (q11, r11) := sDivRem (sAdd (sMul x.c y.a11) (sMul y.c x.a11)) B
  let trunc := rc + r0 + r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9 + r10 + r11
  let err_num := trunc + sAbs x.c * y.err + sAbs y.c * x.err + x.rad * y.rad
  ⟨qc, q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, cdivOver err_num B⟩

def a12InvPos (B : Nat) (y : Aff12N) : Option Aff12N := do
  let m ← sPosNat y.lo
  let c ← sPosNat y.c
  let d : Aff12N := ⟨sZero, y.a0, y.a1, y.a2, y.a3, y.a4, y.a5, y.a6, y.a7, y.a8, y.a9, y.a10, y.a11, y.err⟩
  let u1 := a12ScaleFixed (sOfNat B) d c
  let poly := a12Sub (a12Const (sOfNat B)) u1
  let base := a12ScaleFixed (sOfNat B) poly c
  let rd := y.rad
  let rem2 := cdivOver (rd * rd * (B * B)) (c * c * m)
  pure ⟨base.c, base.a0, base.a1, base.a2, base.a3, base.a4, base.a5,
        base.a6, base.a7, base.a8, base.a9, base.a10, base.a11, base.err + rem2⟩

def a12DivPos (B : Nat) (x y : Aff12N) : Option Aff12N := do
  let c ← sPosNat y.c
  let invY ← a12InvPos B y
  let (q0, _) := sDivRem (sMulNat B x.c) c
  let rem_x := a12Sub x (a12ScaleFixed q0 y B)
  let qr := a12Mul B rem_x invY
  pure ⟨sAdd q0 qr.c, qr.a0, qr.a1, qr.a2, qr.a3, qr.a4, qr.a5,
        qr.a6, qr.a7, qr.a8, qr.a9, qr.a10, qr.a11, qr.err⟩

def a12Max0 (x : Aff12N) : Aff12N :=
  if sNonneg x.lo then x
  else if sNonpos x.hi then a12Const sZero
  else
    let hi_abs := sAbs x.hi
    ⟨sOfNat (hi_abs / 2), sZero, sZero, sZero, sZero, sZero, sZero,
     sZero, sZero, sZero, sZero, sZero, sZero, hi_abs / 2 + 1⟩

lemma a12Const_enc (B : Nat) (hB : 0 < B) (c : SInt) (e : Fin 12 → ℝ) :
    (a12Const c).Enc B e (c.toReal / (B : ℝ)) := by
  unfold Aff12N.Enc a12Const Aff12N.linEval
  have hBr : (B : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hB)
  rw [mul_div_cancel₀ _ hBr, sZero_toReal]
  norm_num

lemma a12Zero_enc (B : Nat) (e : Fin 12 → ℝ) : (a12Const sZero).Enc B e 0 := by
  unfold Aff12N.Enc a12Const Aff12N.linEval; simp [sZero_toReal]

lemma a12Add_enc (B : Nat) (x y : Aff12N) (e : Fin 12 → ℝ) (vx vy : ℝ)
    (hx : x.Enc B e vx) (hy : y.Enc B e vy) :
    (a12Add x y).Enc B e (vx + vy) := by
  unfold Aff12N.Enc at hx hy ⊢
  unfold a12Add Aff12N.linEval
  simp only [sAdd_toReal]; push_cast
  rw [abs_le] at hx hy ⊢
  unfold Aff12N.linEval at hx hy
  constructor <;> linarith

lemma a12Sub_enc (B : Nat) (x y : Aff12N) (e : Fin 12 → ℝ) (vx vy : ℝ)
    (hx : x.Enc B e vx) (hy : y.Enc B e vy) :
    (a12Sub x y).Enc B e (vx - vy) := by
  unfold Aff12N.Enc at hx hy ⊢
  unfold a12Sub Aff12N.linEval
  simp only [sSub_toReal]; push_cast
  rw [abs_le] at hx hy ⊢
  unfold Aff12N.linEval at hx hy
  constructor <;> linarith

lemma a12ScaleSInt_enc (B : Nat) (k : SInt) (x : Aff12N) (e : Fin 12 → ℝ) (vx : ℝ)
    (hx : x.Enc B e vx) :
    (a12ScaleSInt k x).Enc B e (k.toReal * vx) := by
  unfold Aff12N.Enc at hx ⊢
  unfold a12ScaleSInt Aff12N.linEval
  simp only [sMul_toReal]
  have hid :
      (B : ℝ) * (k.toReal * vx) -
        (k.toReal * x.c.toReal +
          (k.toReal * x.a0.toReal * e 0 + k.toReal * x.a1.toReal * e 1 +
           k.toReal * x.a2.toReal * e 2 + k.toReal * x.a3.toReal * e 3 +
           k.toReal * x.a4.toReal * e 4 + k.toReal * x.a5.toReal * e 5 +
           k.toReal * x.a6.toReal * e 6 + k.toReal * x.a7.toReal * e 7 +
           k.toReal * x.a8.toReal * e 8 + k.toReal * x.a9.toReal * e 9 +
           k.toReal * x.a10.toReal * e 10 + k.toReal * x.a11.toReal * e 11)) =
      k.toReal * ((B : ℝ) * vx - (x.c.toReal + x.linEval e)) := by
    unfold Aff12N.linEval; ring
  rw [hid, abs_mul]; push_cast; rw [sAbs_toReal]
  exact mul_le_mul_of_nonneg_left hx (abs_nonneg _)

lemma a12ScaleFixed_enc (B : Nat) (k : SInt) (x : Aff12N) (denom : Nat) (hd : 0 < denom)
    (e : Fin 12 → ℝ) (vx : ℝ) (he : ValidEnv12 e) (hx : x.Enc B e vx) :
    (a12ScaleFixed k x denom).Enc B e ((k.toReal / (denom : ℝ)) * vx) := by
  have hd_real : (0 : ℝ) < (denom : ℝ) := Nat.cast_pos.mpr hd
  have h_scaled := a12ScaleSInt_enc B k x e vx hx
  unfold Aff12N.Enc a12ScaleSInt Aff12N.linEval at h_scaled
  simp only [sMul_toReal] at h_scaled; push_cast at h_scaled; rw [sAbs_toReal] at h_scaled
  unfold a12ScaleFixed Aff12N.Enc Aff12N.linEval; dsimp only
  have hc := sDivRem_spec (sMul k x.c) denom
  have h0 := abs_div_rem_term (sMul k x.a0) denom (e 0) (he 0)
  have h1 := abs_div_rem_term (sMul k x.a1) denom (e 1) (he 1)
  have h2 := abs_div_rem_term (sMul k x.a2) denom (e 2) (he 2)
  have h3 := abs_div_rem_term (sMul k x.a3) denom (e 3) (he 3)
  have h4 := abs_div_rem_term (sMul k x.a4) denom (e 4) (he 4)
  have h5 := abs_div_rem_term (sMul k x.a5) denom (e 5) (he 5)
  have h6 := abs_div_rem_term (sMul k x.a6) denom (e 6) (he 6)
  have h7 := abs_div_rem_term (sMul k x.a7) denom (e 7) (he 7)
  have h8 := abs_div_rem_term (sMul k x.a8) denom (e 8) (he 8)
  have h9 := abs_div_rem_term (sMul k x.a9) denom (e 9) (he 9)
  have h10 := abs_div_rem_term (sMul k x.a10) denom (e 10) (he 10)
  have h11 := abs_div_rem_term (sMul k x.a11) denom (e 11) (he 11)
  simp only [sMul_toReal] at hc h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11
  set rem :=
    (sDivRem (sMul k x.c) denom).2 + (sDivRem (sMul k x.a0) denom).2 +
    (sDivRem (sMul k x.a1) denom).2 + (sDivRem (sMul k x.a2) denom).2 +
    (sDivRem (sMul k x.a3) denom).2 + (sDivRem (sMul k x.a4) denom).2 +
    (sDivRem (sMul k x.a5) denom).2 + (sDivRem (sMul k x.a6) denom).2 +
    (sDivRem (sMul k x.a7) denom).2 + (sDivRem (sMul k x.a8) denom).2 +
    (sDivRem (sMul k x.a9) denom).2 + (sDivRem (sMul k x.a10) denom).2 +
    (sDivRem (sMul k x.a11) denom).2 + sAbs k * x.err
  have hcdiv := cdivOver_spec rem denom hd
  have hd_ne : (denom : ℝ) ≠ 0 := ne_of_gt hd_real
  have hmul_eq : (denom : ℝ) * ((B : ℝ) * ((k.toReal / (denom : ℝ)) * vx)) = (B : ℝ) * (k.toReal * vx) := by
    field_simp [hd_ne]
  suffices hmul :
      |(denom : ℝ) * ((B : ℝ) * (k.toReal / (denom : ℝ) * vx) -
        ((sDivRem (sMul k x.c) denom).1.toReal +
          ((sDivRem (sMul k x.a0) denom).1.toReal * e 0 +
           (sDivRem (sMul k x.a1) denom).1.toReal * e 1 +
           (sDivRem (sMul k x.a2) denom).1.toReal * e 2 +
           (sDivRem (sMul k x.a3) denom).1.toReal * e 3 +
           (sDivRem (sMul k x.a4) denom).1.toReal * e 4 +
           (sDivRem (sMul k x.a5) denom).1.toReal * e 5 +
           (sDivRem (sMul k x.a6) denom).1.toReal * e 6 +
           (sDivRem (sMul k x.a7) denom).1.toReal * e 7 +
           (sDivRem (sMul k x.a8) denom).1.toReal * e 8 +
           (sDivRem (sMul k x.a9) denom).1.toReal * e 9 +
           (sDivRem (sMul k x.a10) denom).1.toReal * e 10 +
           (sDivRem (sMul k x.a11) denom).1.toReal * e 11)))| ≤
      (cdivOver rem denom : ℝ) * (denom : ℝ) by
    rw [abs_mul, abs_of_pos hd_real, mul_comm (cdivOver rem denom : ℝ)] at hmul
    exact le_of_mul_le_mul_left hmul hd_real
  have hrem_cast :
      (rem : ℝ) =
      ((sDivRem (sMul k x.c) denom).2 : ℝ) + ((sDivRem (sMul k x.a0) denom).2 : ℝ) +
      ((sDivRem (sMul k x.a1) denom).2 : ℝ) + ((sDivRem (sMul k x.a2) denom).2 : ℝ) +
      ((sDivRem (sMul k x.a3) denom).2 : ℝ) + ((sDivRem (sMul k x.a4) denom).2 : ℝ) +
      ((sDivRem (sMul k x.a5) denom).2 : ℝ) + ((sDivRem (sMul k x.a6) denom).2 : ℝ) +
      ((sDivRem (sMul k x.a7) denom).2 : ℝ) + ((sDivRem (sMul k x.a8) denom).2 : ℝ) +
      ((sDivRem (sMul k x.a9) denom).2 : ℝ) + ((sDivRem (sMul k x.a10) denom).2 : ℝ) +
      ((sDivRem (sMul k x.a11) denom).2 : ℝ) + |k.toReal| * (x.err : ℝ) := by
    unfold rem; push_cast; rw [sAbs_toReal]
  rw [abs_le] at hc h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11 h_scaled ⊢
  constructor <;> linarith

lemma a12Mul_enc (B : Nat) (hB : 0 < B) (x y : Aff12N) (e : Fin 12 → ℝ) (vx vy : ℝ)
    (he : ValidEnv12 e) (hx : x.Enc B e vx) (hy : y.Enc B e vy) :
    (a12Mul B x y).Enc B e (vx * vy) := by
  have hBr_pos : (0 : ℝ) < (B : ℝ) := Nat.cast_pos.mpr hB
  have hdx := (x.bounds_of_enc B e vx he hx).1
  have hdy := (y.bounds_of_enc B e vy he hy).1
  set ux := (B : ℝ) * vx - (x.c.toReal + x.linEval e)
  set uy := (B : ℝ) * vy - (y.c.toReal + y.linEval e)
  have hux : |ux| ≤ (x.err : ℝ) := hx
  have huy : |uy| ≤ (y.err : ℝ) := hy
  have hid :
      (B : ℝ) * ((B : ℝ) * (vx * vy)) =
      x.c.toReal * y.c.toReal +
      ((x.c.toReal * y.a0.toReal + y.c.toReal * x.a0.toReal) * e 0 +
       (x.c.toReal * y.a1.toReal + y.c.toReal * x.a1.toReal) * e 1 +
       (x.c.toReal * y.a2.toReal + y.c.toReal * x.a2.toReal) * e 2 +
       (x.c.toReal * y.a3.toReal + y.c.toReal * x.a3.toReal) * e 3 +
       (x.c.toReal * y.a4.toReal + y.c.toReal * x.a4.toReal) * e 4 +
       (x.c.toReal * y.a5.toReal + y.c.toReal * x.a5.toReal) * e 5 +
       (x.c.toReal * y.a6.toReal + y.c.toReal * x.a6.toReal) * e 6 +
       (x.c.toReal * y.a7.toReal + y.c.toReal * x.a7.toReal) * e 7 +
       (x.c.toReal * y.a8.toReal + y.c.toReal * x.a8.toReal) * e 8 +
       (x.c.toReal * y.a9.toReal + y.c.toReal * x.a9.toReal) * e 9 +
       (x.c.toReal * y.a10.toReal + y.c.toReal * x.a10.toReal) * e 10 +
       (x.c.toReal * y.a11.toReal + y.c.toReal * x.a11.toReal) * e 11) +
      x.c.toReal * uy + y.c.toReal * ux +
      ((B : ℝ) * vx - x.c.toReal) * ((B : ℝ) * vy - y.c.toReal) := by
    dsimp only [ux, uy, Aff12N.linEval]; ring
  have hc := sDivRem_spec (sMul x.c y.c) B
  have h0 := abs_div_rem_term (sAdd (sMul x.c y.a0) (sMul y.c x.a0)) B (e 0) (he 0)
  have h1 := abs_div_rem_term (sAdd (sMul x.c y.a1) (sMul y.c x.a1)) B (e 1) (he 1)
  have h2 := abs_div_rem_term (sAdd (sMul x.c y.a2) (sMul y.c x.a2)) B (e 2) (he 2)
  have h3 := abs_div_rem_term (sAdd (sMul x.c y.a3) (sMul y.c x.a3)) B (e 3) (he 3)
  have h4 := abs_div_rem_term (sAdd (sMul x.c y.a4) (sMul y.c x.a4)) B (e 4) (he 4)
  have h5 := abs_div_rem_term (sAdd (sMul x.c y.a5) (sMul y.c x.a5)) B (e 5) (he 5)
  have h6 := abs_div_rem_term (sAdd (sMul x.c y.a6) (sMul y.c x.a6)) B (e 6) (he 6)
  have h7 := abs_div_rem_term (sAdd (sMul x.c y.a7) (sMul y.c x.a7)) B (e 7) (he 7)
  have h8 := abs_div_rem_term (sAdd (sMul x.c y.a8) (sMul y.c x.a8)) B (e 8) (he 8)
  have h9 := abs_div_rem_term (sAdd (sMul x.c y.a9) (sMul y.c x.a9)) B (e 9) (he 9)
  have h10 := abs_div_rem_term (sAdd (sMul x.c y.a10) (sMul y.c x.a10)) B (e 10) (he 10)
  have h11 := abs_div_rem_term (sAdd (sMul x.c y.a11) (sMul y.c x.a11)) B (e 11) (he 11)
  simp only [sAdd_toReal, sMul_toReal] at hc h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11
  have hcuy : |x.c.toReal * uy| ≤ |x.c.toReal| * (y.err : ℝ) := by
    rw [abs_mul]; exact mul_le_mul_of_nonneg_left huy (abs_nonneg _)
  have hcux : |y.c.toReal * ux| ≤ |y.c.toReal| * (x.err : ℝ) := by
    rw [abs_mul]; exact mul_le_mul_of_nonneg_left hux (abs_nonneg _)
  have hdxy : |((B : ℝ) * vx - x.c.toReal) * ((B : ℝ) * vy - y.c.toReal)| ≤ (x.rad : ℝ) * (y.rad : ℝ) := by
    rw [abs_mul]; exact mul_le_mul hdx hdy (abs_nonneg _) (Nat.cast_nonneg _)
  unfold a12Mul Aff12N.Enc Aff12N.linEval; dsimp only
  set err_num :=
    (sDivRem (sMul x.c y.c) B).2 +
    (sDivRem (sAdd (sMul x.c y.a0) (sMul y.c x.a0)) B).2 +
    (sDivRem (sAdd (sMul x.c y.a1) (sMul y.c x.a1)) B).2 +
    (sDivRem (sAdd (sMul x.c y.a2) (sMul y.c x.a2)) B).2 +
    (sDivRem (sAdd (sMul x.c y.a3) (sMul y.c x.a3)) B).2 +
    (sDivRem (sAdd (sMul x.c y.a4) (sMul y.c x.a4)) B).2 +
    (sDivRem (sAdd (sMul x.c y.a5) (sMul y.c x.a5)) B).2 +
    (sDivRem (sAdd (sMul x.c y.a6) (sMul y.c x.a6)) B).2 +
    (sDivRem (sAdd (sMul x.c y.a7) (sMul y.c x.a7)) B).2 +
    (sDivRem (sAdd (sMul x.c y.a8) (sMul y.c x.a8)) B).2 +
    (sDivRem (sAdd (sMul x.c y.a9) (sMul y.c x.a9)) B).2 +
    (sDivRem (sAdd (sMul x.c y.a10) (sMul y.c x.a10)) B).2 +
    (sDivRem (sAdd (sMul x.c y.a11) (sMul y.c x.a11)) B).2 +
    sAbs x.c * y.err + sAbs y.c * x.err + x.rad * y.rad
  have hcdiv := cdivOver_spec err_num B hB
  suffices hmul :
      |(B : ℝ) * ((B : ℝ) * (vx * vy) -
        ((sDivRem (sMul x.c y.c) B).1.toReal +
          ((sDivRem (sAdd (sMul x.c y.a0) (sMul y.c x.a0)) B).1.toReal * e 0 +
           (sDivRem (sAdd (sMul x.c y.a1) (sMul y.c x.a1)) B).1.toReal * e 1 +
           (sDivRem (sAdd (sMul x.c y.a2) (sMul y.c x.a2)) B).1.toReal * e 2 +
           (sDivRem (sAdd (sMul x.c y.a3) (sMul y.c x.a3)) B).1.toReal * e 3 +
           (sDivRem (sAdd (sMul x.c y.a4) (sMul y.c x.a4)) B).1.toReal * e 4 +
           (sDivRem (sAdd (sMul x.c y.a5) (sMul y.c x.a5)) B).1.toReal * e 5 +
           (sDivRem (sAdd (sMul x.c y.a6) (sMul y.c x.a6)) B).1.toReal * e 6 +
           (sDivRem (sAdd (sMul x.c y.a7) (sMul y.c x.a7)) B).1.toReal * e 7 +
           (sDivRem (sAdd (sMul x.c y.a8) (sMul y.c x.a8)) B).1.toReal * e 8 +
           (sDivRem (sAdd (sMul x.c y.a9) (sMul y.c x.a9)) B).1.toReal * e 9 +
           (sDivRem (sAdd (sMul x.c y.a10) (sMul y.c x.a10)) B).1.toReal * e 10 +
           (sDivRem (sAdd (sMul x.c y.a11) (sMul y.c x.a11)) B).1.toReal * e 11)))| ≤
      (cdivOver err_num B : ℝ) * (B : ℝ) by
    rw [abs_mul, abs_of_pos hBr_pos, mul_comm (cdivOver err_num B : ℝ)] at hmul
    exact le_of_mul_le_mul_left hmul hBr_pos
  have herr_cast :
      (err_num : ℝ) =
      ((sDivRem (sMul x.c y.c) B).2 : ℝ) +
      ((sDivRem (sAdd (sMul x.c y.a0) (sMul y.c x.a0)) B).2 : ℝ) +
      ((sDivRem (sAdd (sMul x.c y.a1) (sMul y.c x.a1)) B).2 : ℝ) +
      ((sDivRem (sAdd (sMul x.c y.a2) (sMul y.c x.a2)) B).2 : ℝ) +
      ((sDivRem (sAdd (sMul x.c y.a3) (sMul y.c x.a3)) B).2 : ℝ) +
      ((sDivRem (sAdd (sMul x.c y.a4) (sMul y.c x.a4)) B).2 : ℝ) +
      ((sDivRem (sAdd (sMul x.c y.a5) (sMul y.c x.a5)) B).2 : ℝ) +
      ((sDivRem (sAdd (sMul x.c y.a6) (sMul y.c x.a6)) B).2 : ℝ) +
      ((sDivRem (sAdd (sMul x.c y.a7) (sMul y.c x.a7)) B).2 : ℝ) +
      ((sDivRem (sAdd (sMul x.c y.a8) (sMul y.c x.a8)) B).2 : ℝ) +
      ((sDivRem (sAdd (sMul x.c y.a9) (sMul y.c x.a9)) B).2 : ℝ) +
      ((sDivRem (sAdd (sMul x.c y.a10) (sMul y.c x.a10)) B).2 : ℝ) +
      ((sDivRem (sAdd (sMul x.c y.a11) (sMul y.c x.a11)) B).2 : ℝ) +
      |x.c.toReal| * (y.err : ℝ) + |y.c.toReal| * (x.err : ℝ) + (x.rad : ℝ) * (y.rad : ℝ) := by
    unfold err_num; push_cast; rw [sAbs_toReal, sAbs_toReal]
  rw [abs_le] at hc h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11 hcuy hcux hdxy ⊢
  constructor <;> linarith

lemma a12InvPos_enc (B : Nat) (hB : 0 < B) (y res : Aff12N) (e : Fin 12 → ℝ) (vy : ℝ)
    (he : ValidEnv12 e) (hy : y.Enc B e vy) (h : a12InvPos B y = some res) :
    0 < vy ∧ res.Enc B e (1 / vy) := by
  have hBr_pos : (0 : ℝ) < (B : ℝ) := Nat.cast_pos.mpr hB
  unfold a12InvPos at h
  rcases hm_eq : sPosNat y.lo with _ | m
  · simp [hm_eq] at h
  rcases hc_eq : sPosNat y.c with _ | c
  · simp [hm_eq, hc_eq] at h
  simp [hm_eq, hc_eq] at h
  rcases sPosNat_spec y.lo m hm_eq with ⟨hm_pos, hlo_eq⟩
  rcases sPosNat_spec y.c c hc_eq with ⟨hc_pos, hc_val⟩
  rcases y.bounds_of_enc B e vy he hy with ⟨hdy, hlo_le, _⟩
  rw [hlo_eq] at hlo_le
  have hm_real : (0 : ℝ) < (m : ℝ) := Nat.cast_pos.mpr hm_pos
  have hc_real : (0 : ℝ) < (c : ℝ) := Nat.cast_pos.mpr hc_pos
  have hBv_pos : 0 < (B : ℝ) * vy := lt_of_lt_of_le hm_real hlo_le
  have hvy_pos : 0 < vy := pos_of_mul_pos_right hBv_pos (le_of_lt hBr_pos)
  refine ⟨hvy_pos, ?_⟩
  set d : Aff12N := ⟨sZero, y.a0, y.a1, y.a2, y.a3, y.a4, y.a5, y.a6, y.a7, y.a8, y.a9, y.a10, y.a11, y.err⟩
  have hd_enc : d.Enc B e (vy - (c : ℝ) / (B : ℝ)) := by
    unfold Aff12N.Enc at hy ⊢
    have hB_ne : (B : ℝ) ≠ 0 := ne_of_gt hBr_pos
    have hid : (B : ℝ) * (vy - (c : ℝ) / (B : ℝ)) - (d.c.toReal + d.linEval e) =
        (B : ℝ) * vy - (y.c.toReal + y.linEval e) := by
      have hlin : d.linEval e = y.linEval e := rfl
      have hdc : d.c.toReal = 0 := sZero_toReal
      rw [hlin, hdc, hc_val]; field_simp [hB_ne]; ring
    rw [hid]; exact hy
  set u_real := ((B : ℝ) / (c : ℝ)) * (vy - (c : ℝ) / (B : ℝ))
  have hu1_enc : (a12ScaleFixed (sOfNat B) d c).Enc B e u_real := by
    have h1 := a12ScaleFixed_enc B (sOfNat B) d c hc_pos e (vy - (c : ℝ) / (B : ℝ)) he hd_enc
    rw [sOfNat_toReal] at h1; exact h1
  have hpoly_enc : (a12Sub (a12Const (sOfNat B)) (a12ScaleFixed (sOfNat B) d c)).Enc B e (1 - u_real) := by
    have hc1 := a12Const_enc B hB (sOfNat B) e
    rw [sOfNat_toReal, div_self (ne_of_gt hBr_pos)] at hc1
    exact a12Sub_enc B _ _ e 1 u_real hc1 hu1_enc
  set base := a12ScaleFixed (sOfNat B) (a12Sub (a12Const (sOfNat B)) (a12ScaleFixed (sOfNat B) d c)) c
  have hbase_enc : base.Enc B e (((B : ℝ) / (c : ℝ)) * (1 - u_real)) := by
    have h1 := a12ScaleFixed_enc B (sOfNat B) _ c hc_pos e (1 - u_real) he hpoly_enc
    rw [sOfNat_toReal] at h1; exact h1
  have h_rem_alg :
      (B : ℝ) * (1 / vy) - (B : ℝ) * (((B : ℝ) / (c : ℝ)) * (1 - u_real)) =
      (((B : ℝ) * vy - (c : ℝ)) * ((B : ℝ) * vy - (c : ℝ)) * ((B : ℝ) * (B : ℝ))) /
        (((c : ℝ) * (c : ℝ)) * ((B : ℝ) * vy)) := by
    have hc_ne : (c : ℝ) ≠ 0 := ne_of_gt hc_real
    have hB_ne : (B : ℝ) ≠ 0 := ne_of_gt hBr_pos
    have hv_ne : vy ≠ 0 := ne_of_gt hvy_pos
    dsimp only [u_real]; field_simp [hc_ne, hB_ne, hv_ne]; ring
  have hc2m_pos : 0 < c * c * m := Nat.mul_pos (Nat.mul_pos hc_pos hc_pos) hm_pos
  have hcdiv := cdivOver_spec (y.rad * y.rad * (B * B)) (c * c * m) hc2m_pos
  have hdy_c : |(B : ℝ) * vy - (c : ℝ)| ≤ (y.rad : ℝ) := by rw [← hc_val]; exact hdy
  have hdy_sq : ((B : ℝ) * vy - (c : ℝ)) * ((B : ℝ) * vy - (c : ℝ)) ≤ (y.rad : ℝ) * (y.rad : ℝ) := by
    have := mul_le_mul hdy_c hdy_c (abs_nonneg _) (Nat.cast_nonneg _)
    rwa [← abs_mul, abs_mul_self] at this
  have hrem_bound :
      |(B : ℝ) * (1 / vy) - (B : ℝ) * (((B : ℝ) / (c : ℝ)) * (1 - u_real))| ≤
      (cdivOver (y.rad * y.rad * (B * B)) (c * c * m) : ℝ) := by
    rw [h_rem_alg]
    have hnum_nn : 0 ≤ ((B : ℝ) * vy - (c : ℝ)) * ((B : ℝ) * vy - (c : ℝ)) * ((B : ℝ) * (B : ℝ)) :=
      mul_nonneg (mul_self_nonneg _) (mul_nonneg (le_of_lt hBr_pos) (le_of_lt hBr_pos))
    have hden_pos : 0 < ((c : ℝ) * (c : ℝ)) * ((B : ℝ) * vy) :=
      mul_pos (mul_pos hc_real hc_real) hBv_pos
    rw [abs_of_nonneg (div_nonneg hnum_nn (le_of_lt hden_pos)), div_le_iff₀ hden_pos]
    have hBB_nn : 0 ≤ (B : ℝ) * (B : ℝ) := mul_nonneg (le_of_lt hBr_pos) (le_of_lt hBr_pos)
    have hs1 := mul_le_mul_of_nonneg_right hdy_sq hBB_nn
    push_cast at hcdiv
    have hs2 :
        (cdivOver (y.rad * y.rad * (B * B)) (c * c * m) : ℝ) * ((c : ℝ) * (c : ℝ) * (m : ℝ)) ≤
        (cdivOver (y.rad * y.rad * (B * B)) (c * c * m) : ℝ) * (((c : ℝ) * (c : ℝ)) * ((B : ℝ) * vy)) := by
      apply mul_le_mul_of_nonneg_left _ (Nat.cast_nonneg _)
      exact mul_le_mul_of_nonneg_left hlo_le (mul_nonneg (le_of_lt hc_real) (le_of_lt hc_real))
    linarith
  rw [← h]
  unfold Aff12N.Enc at hbase_enc ⊢
  have hlin_eq :
      ({ c := base.c, a0 := base.a0, a1 := base.a1, a2 := base.a2, a3 := base.a3, a4 := base.a4,
         a5 := base.a5, a6 := base.a6, a7 := base.a7, a8 := base.a8, a9 := base.a9,
         a10 := base.a10, a11 := base.a11,
         err := base.err + cdivOver (y.rad * y.rad * (B * B)) (c * c * m) } : Aff12N).linEval e =
      base.linEval e := rfl
  rw [hlin_eq]; dsimp only; push_cast
  rw [abs_le] at hbase_enc hrem_bound ⊢
  constructor <;> linarith

lemma a12DivPos_enc (B : Nat) (hB : 0 < B) (x y res : Aff12N) (e : Fin 12 → ℝ) (vx vy : ℝ)
    (he : ValidEnv12 e) (hx : x.Enc B e vx) (hy : y.Enc B e vy)
    (h : a12DivPos B x y = some res) :
    0 < vy ∧ res.Enc B e (vx / vy) := by
  have hBr_pos : (0 : ℝ) < (B : ℝ) := Nat.cast_pos.mpr hB
  unfold a12DivPos at h
  rcases hc_eq : sPosNat y.c with _ | c
  · simp [hc_eq] at h
  rcases hinv_eq : a12InvPos B y with _ | invY
  · simp [hc_eq, hinv_eq] at h
  simp [hc_eq, hinv_eq] at h
  rcases a12InvPos_enc B hB y invY e vy he hy hinv_eq with ⟨hvy_pos, hinv⟩
  refine ⟨hvy_pos, ?_⟩
  set q0 := (sDivRem (sMulNat B x.c) c).1
  have hrem : (a12Sub x (a12ScaleFixed q0 y B)).Enc B e (vx - (q0.toReal / (B : ℝ)) * vy) :=
    a12Sub_enc B x _ e vx _ hx (a12ScaleFixed_enc B q0 y B hB e vy he hy)
  have hqr : (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).Enc B e
      ((vx - (q0.toReal / (B : ℝ)) * vy) * (1 / vy)) :=
    a12Mul_enc B hB _ _ e _ _ he hrem hinv
  rw [← h]
  unfold Aff12N.Enc at hqr ⊢
  have hlin_eq :
      ({ c := sAdd q0 (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).c,
         a0 := (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).a0,
         a1 := (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).a1,
         a2 := (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).a2,
         a3 := (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).a3,
         a4 := (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).a4,
         a5 := (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).a5,
         a6 := (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).a6,
         a7 := (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).a7,
         a8 := (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).a8,
         a9 := (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).a9,
         a10 := (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).a10,
         a11 := (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).a11,
         err := (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).err } : Aff12N).linEval e =
      (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).linEval e := rfl
  rw [hlin_eq]; dsimp only; rw [sAdd_toReal]
  have hvy_ne : vy ≠ 0 := ne_of_gt hvy_pos
  have hB_ne : (B : ℝ) ≠ 0 := ne_of_gt hBr_pos
  have hid :
      (B : ℝ) * (vx / vy) -
        (q0.toReal + (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).c.toReal +
         (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).linEval e) =
      (B : ℝ) * ((vx - (q0.toReal / (B : ℝ)) * vy) * (1 / vy)) -
        ((a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).c.toReal +
         (a12Mul B (a12Sub x (a12ScaleFixed q0 y B)) invY).linEval e) := by
    field_simp [hvy_ne, hB_ne]; ring
  rw [hid]; exact hqr

lemma a12Max0_enc (B : Nat) (hB : 0 < B) (x : Aff12N) (e : Fin 12 → ℝ) (vx : ℝ)
    (he : ValidEnv12 e) (hx : x.Enc B e vx) :
    (a12Max0 x).Enc B e (max 0 vx) := by
  have hBr_pos : (0 : ℝ) < (B : ℝ) := Nat.cast_pos.mpr hB
  rcases x.bounds_of_enc B e vx he hx with ⟨_, hlo, hhi⟩
  unfold a12Max0
  split_ifs with h1 h2
  · have hnn := sNonneg_spec x.lo h1
    have hvx : 0 ≤ vx := nonneg_of_mul_nonneg_right (by linarith) hBr_pos
    rw [max_eq_right hvx]; exact hx
  · have hnp := sNonpos_spec x.hi h2
    have hvx : vx ≤ 0 := nonpos_of_mul_nonpos_right (by linarith) hBr_pos
    rw [max_eq_left hvx]; exact a12Zero_enc B e
  · have hhi_pos : 0 < x.hi.toReal := by
      by_contra hle
      have hle' : x.hi.toReal ≤ 0 := le_of_not_gt hle
      unfold sNonpos at h2; unfold SInt.toReal at hle'
      have hnat : x.hi.p ≤ x.hi.n := Nat.cast_le.mp (by linarith : (x.hi.p : ℝ) ≤ (x.hi.n : ℝ))
      exact h2 (Nat.ble_eq.mpr hnat)
    have habs : (sAbs x.hi : ℝ) = x.hi.toReal := by rw [sAbs_toReal, abs_of_pos hhi_pos]
    have hBmax_nn : 0 ≤ (B : ℝ) * max 0 vx := mul_nonneg (le_of_lt hBr_pos) (le_max_left 0 vx)
    have hBmax_hi : (B : ℝ) * max 0 vx ≤ (sAbs x.hi : ℝ) := by
      rcases le_total vx 0 with hv0 | hv0
      · rw [max_eq_left hv0, mul_zero]; exact Nat.cast_nonneg _
      · rw [max_eq_right hv0, habs]; exact hhi
    unfold Aff12N.Enc Aff12N.linEval; dsimp only
    rw [sOfNat_toReal, sZero_toReal]
    have hdiv_r : (2 : ℝ) * ((sAbs x.hi / 2 : Nat) : ℝ) + ((sAbs x.hi % 2 : Nat) : ℝ) = (sAbs x.hi : ℝ) := by
      exact_mod_cast Nat.div_add_mod (sAbs x.hi) 2
    have hmod_lt := Nat.mod_lt (sAbs x.hi) (by decide : 0 < 2)
    have hmod_r : ((sAbs x.hi % 2 : Nat) : ℝ) ≤ 1 := by
      have : sAbs x.hi % 2 ≤ 1 := by omega
      exact_mod_cast this
    have hmod_nn : (0 : ℝ) ≤ ((sAbs x.hi % 2 : Nat) : ℝ) := Nat.cast_nonneg _
    push_cast; rw [abs_le]; constructor <;> linarith

end PRMPlus
