import PRMPlus.ReachSound

/-!
# Verified 15-Symbol Chebyshev-Bilinear Affine Arithmetic (`Aff15N`)

Tracks 15 basis functions on `(v₀..v₅, e₆) ∈ [-1, 1]⁷`:
- `0..5`:  `v₀ .. v₅`
- `6`:     `T₁(e₆) = e₆`
- `7..12`: `e₆ v₀ .. e₆ v₅` (exact bilinear cross-terms)
- `13`:    `T₂(e₆) = 2 e₆² - 1`
- `14`:    `T₃(e₆) = 4 e₆³ - 3 e₆`
-/

namespace PRMPlus

open scoped BigOperators

structure TubeEnv where
  v0 : ℝ
  v1 : ℝ
  v2 : ℝ
  v3 : ℝ
  v4 : ℝ
  v5 : ℝ
  e6 : ℝ

def TubeEnv.Valid (te : TubeEnv) : Prop :=
  |te.v0| ≤ 1 ∧ |te.v1| ≤ 1 ∧ |te.v2| ≤ 1 ∧
  |te.v3| ≤ 1 ∧ |te.v4| ≤ 1 ∧ |te.v5| ≤ 1 ∧ |te.e6| ≤ 1

lemma cheb_T2_abs_le_one (x : ℝ) (hx : |x| ≤ 1) : |2 * x * x - 1| ≤ 1 := by
  have hx2 : x * x ≤ 1 := by
    have := mul_le_mul hx hx (abs_nonneg x) (by norm_num)
    rwa [← abs_mul, abs_mul_self, mul_one] at this
  have hx0 : 0 ≤ x * x := mul_self_nonneg x
  rw [abs_le]; constructor <;> linarith

lemma cheb_T2_sq_shift_abs_le_one (x : ℝ) (hx : |x| ≤ 1) :
    |2 * (2 * x * x - 1) * (2 * x * x - 1) - 1| ≤ 1 := by
  exact cheb_T2_abs_le_one (2 * x * x - 1) (cheb_T2_abs_le_one x hx)

lemma cheb_T3_abs_le_one (x : ℝ) (hx : |x| ≤ 1) : |4 * x * x * x - 3 * x| ≤ 1 := by
  have hx2 : x * x ≤ 1 := by
    have := mul_le_mul hx hx (abs_nonneg x) (by norm_num)
    rwa [← abs_mul, abs_mul_self, mul_one] at this
  have h_sos : 1 - (4 * x * x * x - 3 * x) * (4 * x * x * x - 3 * x) =
      (1 - x * x) * ((1 - 4 * x * x) * (1 - 4 * x * x)) := by ring
  have h_nn : 0 ≤ (1 - x * x) * ((1 - 4 * x * x) * (1 - 4 * x * x)) :=
    mul_nonneg (by linarith) (mul_self_nonneg _)
  have hsq : (4 * x * x * x - 3 * x) * (4 * x * x * x - 3 * x) ≤ 1 := by linarith
  rw [abs_le]
  constructor
  · nlinarith [sq_nonneg (4 * x * x * x - 3 * x + 1)]
  · nlinarith [sq_nonneg (4 * x * x * x - 3 * x - 1)]

lemma prod_abs_le_one (a b : ℝ) (ha : |a| ≤ 1) (hb : |b| ≤ 1) : |a * b| ≤ 1 := by
  rw [abs_mul]; nlinarith [abs_nonneg a, abs_nonneg b]

structure Aff15N where
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
  a12 : SInt
  a13 : SInt
  a14 : SInt
  err : Nat
  deriving DecidableEq

noncomputable def Aff15N.linEval (x : Aff15N) (te : TubeEnv) : ℝ :=
  x.a0.toReal * te.v0 + x.a1.toReal * te.v1 + x.a2.toReal * te.v2 +
  x.a3.toReal * te.v3 + x.a4.toReal * te.v4 + x.a5.toReal * te.v5 +
  x.a6.toReal * te.e6 +
  x.a7.toReal * (te.e6 * te.v0) + x.a8.toReal * (te.e6 * te.v1) +
  x.a9.toReal * (te.e6 * te.v2) + x.a10.toReal * (te.e6 * te.v3) +
  x.a11.toReal * (te.e6 * te.v4) + x.a12.toReal * (te.e6 * te.v5) +
  x.a13.toReal * (2 * te.e6 * te.e6 - 1) +
  x.a14.toReal * (4 * te.e6 * te.e6 * te.e6 - 3 * te.e6)

def Aff15N.Enc (B : Nat) (x : Aff15N) (te : TubeEnv) (v : ℝ) : Prop :=
  |(B : ℝ) * v - (x.c.toReal + x.linEval te)| ≤ (x.err : ℝ)

@[inline] def Aff15N.rv (x : Aff15N) : Nat :=
  sAbs x.a0 + sAbs x.a1 + sAbs x.a2 + sAbs x.a3 + sAbs x.a4 + sAbs x.a5

@[inline] def Aff15N.rve (x : Aff15N) : Nat :=
  sAbs x.a7 + sAbs x.a8 + sAbs x.a9 + sAbs x.a10 + sAbs x.a11 + sAbs x.a12 + sAbs x.a14

@[inline] def Aff15N.radSum (x : Aff15N) : Nat :=
  x.rv + sAbs x.a6 + x.rve + sAbs x.a13

@[inline] def Aff15N.rad (x : Aff15N) : Nat := x.radSum + x.err
@[inline] def Aff15N.lo (x : Aff15N) : SInt := sSub x.c (sOfNat x.rad)
@[inline] def Aff15N.hi (x : Aff15N) : SInt := sAdd x.c (sOfNat x.rad)

@[inline] def Aff15N.strictB (x : Aff15N) : Bool :=
  sStrict x.c && sStrict x.a0 && sStrict x.a1 && sStrict x.a2 && sStrict x.a3 &&
  sStrict x.a4 && sStrict x.a5 && sStrict x.a6 && sStrict x.a7 && sStrict x.a8 &&
  sStrict x.a9 && sStrict x.a10 && sStrict x.a11 && sStrict x.a12 &&
  sStrict x.a13 && sStrict x.a14 && Nat.beq x.err x.err

lemma Aff15N.strictB_true (x : Aff15N) : x.strictB = true := by
  unfold Aff15N.strictB; simp [sStrict_true]

lemma TubeEnv.basis_bounds (te : TubeEnv) (hte : te.Valid) :
    |te.v0| ≤ 1 ∧ |te.v1| ≤ 1 ∧ |te.v2| ≤ 1 ∧ |te.v3| ≤ 1 ∧ |te.v4| ≤ 1 ∧ |te.v5| ≤ 1 ∧
    |te.e6| ≤ 1 ∧
    |te.e6 * te.v0| ≤ 1 ∧ |te.e6 * te.v1| ≤ 1 ∧ |te.e6 * te.v2| ≤ 1 ∧
    |te.e6 * te.v3| ≤ 1 ∧ |te.e6 * te.v4| ≤ 1 ∧ |te.e6 * te.v5| ≤ 1 ∧
    |2 * te.e6 * te.e6 - 1| ≤ 1 ∧ |4 * te.e6 * te.e6 * te.e6 - 3 * te.e6| ≤ 1 := by
  rcases hte with ⟨h0, h1, h2, h3, h4, h5, he6⟩
  exact ⟨h0, h1, h2, h3, h4, h5, he6,
    prod_abs_le_one _ _ he6 h0, prod_abs_le_one _ _ he6 h1, prod_abs_le_one _ _ he6 h2,
    prod_abs_le_one _ _ he6 h3, prod_abs_le_one _ _ he6 h4, prod_abs_le_one _ _ he6 h5,
    cheb_T2_abs_le_one _ he6, cheb_T3_abs_le_one _ he6⟩

lemma Aff15N.abs_linEval_le (x : Aff15N) (te : TubeEnv) (hte : te.Valid) :
    |x.linEval te| ≤ (x.radSum : ℝ) := by
  rcases te.basis_bounds hte with
    ⟨b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14⟩
  unfold Aff15N.linEval Aff15N.radSum Aff15N.rv Aff15N.rve
  push_cast; simp only [sAbs_toReal]
  have h0 := abs_mul_le_of_abs_le_one x.a0.toReal _ b0
  have h1 := abs_mul_le_of_abs_le_one x.a1.toReal _ b1
  have h2 := abs_mul_le_of_abs_le_one x.a2.toReal _ b2
  have h3 := abs_mul_le_of_abs_le_one x.a3.toReal _ b3
  have h4 := abs_mul_le_of_abs_le_one x.a4.toReal _ b4
  have h5 := abs_mul_le_of_abs_le_one x.a5.toReal _ b5
  have h6 := abs_mul_le_of_abs_le_one x.a6.toReal _ b6
  have h7 := abs_mul_le_of_abs_le_one x.a7.toReal _ b7
  have h8 := abs_mul_le_of_abs_le_one x.a8.toReal _ b8
  have h9 := abs_mul_le_of_abs_le_one x.a9.toReal _ b9
  have h10 := abs_mul_le_of_abs_le_one x.a10.toReal _ b10
  have h11 := abs_mul_le_of_abs_le_one x.a11.toReal _ b11
  have h12 := abs_mul_le_of_abs_le_one x.a12.toReal _ b12
  have h13 := abs_mul_le_of_abs_le_one x.a13.toReal _ b13
  have h14 := abs_mul_le_of_abs_le_one x.a14.toReal _ b14
  rw [abs_le] at h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11 h12 h13 h14 ⊢
  constructor <;> linarith

lemma Aff15N.bounds_of_enc (B : Nat) (x : Aff15N) (te : TubeEnv) (v : ℝ)
    (hte : te.Valid) (hx : x.Enc B te v) :
    |(B : ℝ) * v - x.c.toReal| ≤ (x.rad : ℝ) ∧
    x.lo.toReal ≤ (B : ℝ) * v ∧ (B : ℝ) * v ≤ x.hi.toReal := by
  have hlin := x.abs_linEval_le te hte
  unfold Aff15N.Enc at hx
  unfold Aff15N.lo Aff15N.hi Aff15N.rad
  rw [sSub_toReal, sAdd_toReal, sOfNat_toReal]
  push_cast
  rw [abs_le] at hx hlin ⊢
  refine ⟨⟨by linarith, by linarith⟩, by linarith, by linarith⟩

def a15Const (c : SInt) : Aff15N :=
  ⟨c, sZero, sZero, sZero, sZero, sZero, sZero, sZero,
   sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, 0⟩

def a15FromA12Iv (x : Aff12N) : Aff15N :=
  ⟨x.c, sZero, sZero, sZero, sZero, sZero, sZero, sZero,
   sZero, sZero, sZero, sZero, sZero, sZero, sZero, sZero, x.rad⟩

lemma a15FromA12Iv_enc (B : Nat) (x : Aff12N) (e12 : Fin 12 → ℝ) (te : TubeEnv) (v : ℝ)
    (he12 : ValidEnv12 e12) (hx : x.Enc B e12 v) :
    (a15FromA12Iv x).Enc B te v := by
  have hb := (x.bounds_of_enc B e12 v he12 hx).1
  unfold Aff15N.Enc a15FromA12Iv Aff15N.linEval
  dsimp only; simp only [sZero_toReal, zero_mul, add_zero]
  exact hb

def a15Add (x y : Aff15N) : Aff15N :=
  ⟨sAdd x.c y.c,
   sAdd x.a0 y.a0, sAdd x.a1 y.a1, sAdd x.a2 y.a2, sAdd x.a3 y.a3, sAdd x.a4 y.a4, sAdd x.a5 y.a5,
   sAdd x.a6 y.a6, sAdd x.a7 y.a7, sAdd x.a8 y.a8, sAdd x.a9 y.a9, sAdd x.a10 y.a10, sAdd x.a11 y.a11,
   sAdd x.a12 y.a12, sAdd x.a13 y.a13, sAdd x.a14 y.a14, x.err + y.err⟩

def a15Sub (x y : Aff15N) : Aff15N :=
  ⟨sSub x.c y.c,
   sSub x.a0 y.a0, sSub x.a1 y.a1, sSub x.a2 y.a2, sSub x.a3 y.a3, sSub x.a4 y.a4, sSub x.a5 y.a5,
   sSub x.a6 y.a6, sSub x.a7 y.a7, sSub x.a8 y.a8, sSub x.a9 y.a9, sSub x.a10 y.a10, sSub x.a11 y.a11,
   sSub x.a12 y.a12, sSub x.a13 y.a13, sSub x.a14 y.a14, x.err + y.err⟩

def a15Neg (x : Aff15N) : Aff15N :=
  ⟨sNeg x.c,
   sNeg x.a0, sNeg x.a1, sNeg x.a2, sNeg x.a3, sNeg x.a4, sNeg x.a5,
   sNeg x.a6, sNeg x.a7, sNeg x.a8, sNeg x.a9, sNeg x.a10, sNeg x.a11,
   sNeg x.a12, sNeg x.a13, sNeg x.a14, x.err⟩

def a15ScaleSInt (k : SInt) (x : Aff15N) : Aff15N :=
  ⟨sMul k x.c,
   sMul k x.a0, sMul k x.a1, sMul k x.a2, sMul k x.a3, sMul k x.a4, sMul k x.a5,
   sMul k x.a6, sMul k x.a7, sMul k x.a8, sMul k x.a9, sMul k x.a10, sMul k x.a11,
   sMul k x.a12, sMul k x.a13, sMul k x.a14, sAbs k * x.err⟩

def a15ScaleFixed (k : SInt) (x : Aff15N) (denom : Nat) : Aff15N :=
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
  let (q12, r12) := sDivRem (sMul k x.a12) denom
  let (q13, r13) := sDivRem (sMul k x.a13) denom
  let (q14, r14) := sDivRem (sMul k x.a14) denom
  let rem := rc + r0 + r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9 + r10 + r11 + r12 + r13 + r14 + sAbs k * x.err
  ⟨qc, q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, cdivOver rem denom⟩

def a15Mul (B : Nat) (x y : Aff15N) : Aff15N :=
  let twoB := 2 * B
  let c1 := x.c; let c2 := y.c
  let b1 := x.a6; let b2 := y.a6
  let q1 := x.a13; let q2 := y.a13
  let rv1 := x.rv; let rv2 := y.rv
  let rb1 := sAbs b1; let rb2 := sAbs b2
  let rq1 := sAbs q1; let rq2 := sAbs q2
  let rem1 := x.rve + x.err
  let rem2 := y.rve + y.err
  let bb := sMul b1 b2
  let qq := sMul q1 q2
  let bq := sAdd (sMul b1 q2) (sMul q1 b2)
  let (qc, rc)   := sDivRem (sAdd (sMulNat 2 (sMul c1 c2)) (sAdd bb qq)) twoB
  let (q0, r0)   := sDivRem (sMulNat 2 (sAdd (sMul c1 y.a0) (sMul c2 x.a0))) twoB
  let (q1_, r1)  := sDivRem (sMulNat 2 (sAdd (sMul c1 y.a1) (sMul c2 x.a1))) twoB
  let (q2_, r2)  := sDivRem (sMulNat 2 (sAdd (sMul c1 y.a2) (sMul c2 x.a2))) twoB
  let (q3, r3)   := sDivRem (sMulNat 2 (sAdd (sMul c1 y.a3) (sMul c2 x.a3))) twoB
  let (q4, r4)   := sDivRem (sMulNat 2 (sAdd (sMul c1 y.a4) (sMul c2 x.a4))) twoB
  let (q5, r5)   := sDivRem (sMulNat 2 (sAdd (sMul c1 y.a5) (sMul c2 x.a5))) twoB
  let (q6, r6)   := sDivRem (sAdd (sMulNat 2 (sAdd (sMul c1 y.a6) (sMul c2 x.a6))) bq) twoB
  let (q7, r7)   := sDivRem (sMulNat 2 (sAdd (sAdd (sMul c1 y.a7) (sMul c2 x.a7)) (sAdd (sMul b1 y.a0) (sMul b2 x.a0)))) twoB
  let (q8, r8)   := sDivRem (sMulNat 2 (sAdd (sAdd (sMul c1 y.a8) (sMul c2 x.a8)) (sAdd (sMul b1 y.a1) (sMul b2 x.a1)))) twoB
  let (q9, r9)   := sDivRem (sMulNat 2 (sAdd (sAdd (sMul c1 y.a9) (sMul c2 x.a9)) (sAdd (sMul b1 y.a2) (sMul b2 x.a2)))) twoB
  let (q10, r10) := sDivRem (sMulNat 2 (sAdd (sAdd (sMul c1 y.a10) (sMul c2 x.a10)) (sAdd (sMul b1 y.a3) (sMul b2 x.a3)))) twoB
  let (q11, r11) := sDivRem (sMulNat 2 (sAdd (sAdd (sMul c1 y.a11) (sMul c2 x.a11)) (sAdd (sMul b1 y.a4) (sMul b2 x.a4)))) twoB
  let (q12, r12) := sDivRem (sMulNat 2 (sAdd (sAdd (sMul c1 y.a12) (sMul c2 x.a12)) (sAdd (sMul b1 y.a5) (sMul b2 x.a5)))) twoB
  let (q13, r13) := sDivRem (sAdd (sMulNat 2 (sAdd (sMul c1 y.a13) (sMul c2 x.a13))) bb) twoB
  let (q14, r14) := sDivRem (sAdd (sMulNat 2 (sAdd (sMul c1 y.a14) (sMul c2 x.a14))) bq) twoB
  let trunc := rc + r0 + r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9 + r10 + r11 + r12 + r13 + r14
  let cross :=
    2 * (sAbs c1 * y.err + sAbs c2 * x.err) + rq1 * rq2 +
    2 * (rv1 * (rv2 + rq2 + rem2) + rv2 * (rq1 + rem1)) +
    2 * (rb1 * rem2 + rb2 * rem1) + 2 * (rq1 * rem2 + rq2 * rem1) + 2 * rem1 * rem2
  ⟨qc, q0, q1_, q2_, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, cdivOver (trunc + cross) twoB⟩

def a15InvPos (B : Nat) (y : Aff15N) : Option Aff15N :=
  match sPosNat y.lo, sPosNat y.c with
  | some m, some c =>
    let d : Aff15N := ⟨sZero, y.a0, y.a1, y.a2, y.a3, y.a4, y.a5, y.a6, y.a7, y.a8,
                       y.a9, y.a10, y.a11, y.a12, y.a13, y.a14, y.err⟩
    let u1 := a15ScaleFixed (sOfNat B) d c
    let u2 := a15Mul B u1 u1
    let u3 := a15Mul B u2 u1
    let poly := a15Sub (a15Add (a15Sub (a15Const (sOfNat B)) u1) u2) u3
    let base := a15ScaleFixed (sOfNat B) poly c
    let rd := y.rad
    let rd2 := rd * rd
    let c2 := c * c
    let rem4 := cdivOver ((B * B) * (rd2 * rd2)) ((c2 * c2) * m)
    let out : Aff15N := ⟨base.c, base.a0, base.a1, base.a2, base.a3, base.a4, base.a5, base.a6,
                         base.a7, base.a8, base.a9, base.a10, base.a11, base.a12, base.a13, base.a14,
                         base.err + rem4⟩
    if out.strictB then some out else none
  | _, _ => none

def a15DivPos (B : Nat) (x y : Aff15N) : Option Aff15N :=
  match sPosNat y.c, a15InvPos B y with
  | some c, some invY =>
    let (q0, _) := sDivRem (sMulNat B x.c) c
    let rem_x := a15Sub x (a15ScaleFixed q0 y B)
    let qr := a15Mul B rem_x invY
    let out : Aff15N := ⟨sAdd q0 qr.c, qr.a0, qr.a1, qr.a2, qr.a3, qr.a4, qr.a5, qr.a6,
                         qr.a7, qr.a8, qr.a9, qr.a10, qr.a11, qr.a12, qr.a13, qr.a14, qr.err⟩
    if out.strictB then some out else none
  | _, _ => none

def a15Div (B : Nat) (x y : Aff15N) : Option Aff15N :=
  if sNonneg (sSub sZero (sAdd y.hi (sOfNat 1))) then
    a15DivPos B (a15Neg x) (a15Neg y)
  else
    a15DivPos B x y

/-! ### Soundness Proofs for `Aff15N` Operations -/

lemma a15Const_enc (B : Nat) (hB : 0 < B) (c : SInt) (te : TubeEnv) :
    (a15Const c).Enc B te (c.toReal / (B : ℝ)) := by
  unfold Aff15N.Enc a15Const Aff15N.linEval
  have hBr : (B : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hB)
  rw [mul_div_cancel₀ _ hBr, sZero_toReal]; norm_num

lemma a15Zero_enc (B : Nat) (te : TubeEnv) : (a15Const sZero).Enc B te 0 := by
  unfold Aff15N.Enc a15Const Aff15N.linEval; simp [sZero_toReal]

lemma a15Add_enc (B : Nat) (x y : Aff15N) (te : TubeEnv) (vx vy : ℝ)
    (hx : x.Enc B te vx) (hy : y.Enc B te vy) :
    (a15Add x y).Enc B te (vx + vy) := by
  unfold Aff15N.Enc at hx hy ⊢
  unfold a15Add Aff15N.linEval
  simp only [sAdd_toReal]; push_cast
  rw [abs_le] at hx hy ⊢
  unfold Aff15N.linEval at hx hy
  constructor <;> linarith

lemma a15Sub_enc (B : Nat) (x y : Aff15N) (te : TubeEnv) (vx vy : ℝ)
    (hx : x.Enc B te vx) (hy : y.Enc B te vy) :
    (a15Sub x y).Enc B te (vx - vy) := by
  unfold Aff15N.Enc at hx hy ⊢
  unfold a15Sub Aff15N.linEval
  simp only [sSub_toReal]; push_cast
  rw [abs_le] at hx hy ⊢
  unfold Aff15N.linEval at hx hy
  constructor <;> linarith

lemma a15Neg_enc (B : Nat) (x : Aff15N) (te : TubeEnv) (vx : ℝ)
    (hx : x.Enc B te vx) :
    (a15Neg x).Enc B te (-vx) := by
  unfold Aff15N.Enc at hx ⊢
  unfold a15Neg Aff15N.linEval
  simp only [sNeg_toReal]
  rw [abs_le] at hx ⊢
  unfold Aff15N.linEval at hx
  constructor <;> linarith

lemma a15ScaleSInt_enc (B : Nat) (k : SInt) (x : Aff15N) (te : TubeEnv) (vx : ℝ)
    (hx : x.Enc B te vx) :
    (a15ScaleSInt k x).Enc B te (k.toReal * vx) := by
  unfold Aff15N.Enc at hx ⊢
  unfold a15ScaleSInt Aff15N.linEval
  simp only [sMul_toReal]
  have hid :
      (B : ℝ) * (k.toReal * vx) -
        (k.toReal * x.c.toReal +
          (k.toReal * x.a0.toReal * te.v0 + k.toReal * x.a1.toReal * te.v1 +
           k.toReal * x.a2.toReal * te.v2 + k.toReal * x.a3.toReal * te.v3 +
           k.toReal * x.a4.toReal * te.v4 + k.toReal * x.a5.toReal * te.v5 +
           k.toReal * x.a6.toReal * te.e6 +
           k.toReal * x.a7.toReal * (te.e6 * te.v0) + k.toReal * x.a8.toReal * (te.e6 * te.v1) +
           k.toReal * x.a9.toReal * (te.e6 * te.v2) + k.toReal * x.a10.toReal * (te.e6 * te.v3) +
           k.toReal * x.a11.toReal * (te.e6 * te.v4) + k.toReal * x.a12.toReal * (te.e6 * te.v5) +
           k.toReal * x.a13.toReal * (2 * te.e6 * te.e6 - 1) +
           k.toReal * x.a14.toReal * (4 * te.e6 * te.e6 * te.e6 - 3 * te.e6))) =
      k.toReal * ((B : ℝ) * vx - (x.c.toReal + x.linEval te)) := by
    unfold Aff15N.linEval; ring
  rw [hid, abs_mul]; push_cast; rw [sAbs_toReal]
  exact mul_le_mul_of_nonneg_left hx (abs_nonneg _)

lemma a15ScaleFixed_enc (B : Nat) (k : SInt) (x : Aff15N) (denom : Nat) (hd : 0 < denom)
    (te : TubeEnv) (vx : ℝ) (hte : te.Valid) (hx : x.Enc B te vx) :
    (a15ScaleFixed k x denom).Enc B te ((k.toReal / (denom : ℝ)) * vx) := by
  rcases te.basis_bounds hte with
    ⟨b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14⟩
  have hd_real : (0 : ℝ) < (denom : ℝ) := Nat.cast_pos.mpr hd
  have h_scaled := a15ScaleSInt_enc B k x te vx hx
  unfold Aff15N.Enc a15ScaleSInt Aff15N.linEval at h_scaled
  simp only [sMul_toReal] at h_scaled; push_cast at h_scaled; rw [sAbs_toReal] at h_scaled
  unfold a15ScaleFixed Aff15N.Enc Aff15N.linEval; dsimp only
  have hc  := sDivRem_spec (sMul k x.c) denom
  have h0  := abs_div_rem_term (sMul k x.a0) denom _ b0
  have h1  := abs_div_rem_term (sMul k x.a1) denom _ b1
  have h2  := abs_div_rem_term (sMul k x.a2) denom _ b2
  have h3  := abs_div_rem_term (sMul k x.a3) denom _ b3
  have h4  := abs_div_rem_term (sMul k x.a4) denom _ b4
  have h5  := abs_div_rem_term (sMul k x.a5) denom _ b5
  have h6  := abs_div_rem_term (sMul k x.a6) denom _ b6
  have h7  := abs_div_rem_term (sMul k x.a7) denom _ b7
  have h8  := abs_div_rem_term (sMul k x.a8) denom _ b8
  have h9  := abs_div_rem_term (sMul k x.a9) denom _ b9
  have h10 := abs_div_rem_term (sMul k x.a10) denom _ b10
  have h11 := abs_div_rem_term (sMul k x.a11) denom _ b11
  have h12 := abs_div_rem_term (sMul k x.a12) denom _ b12
  have h13 := abs_div_rem_term (sMul k x.a13) denom _ b13
  have h14 := abs_div_rem_term (sMul k x.a14) denom _ b14
  simp only [sMul_toReal] at hc h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11 h12 h13 h14
  set rem :=
    (sDivRem (sMul k x.c) denom).2 + (sDivRem (sMul k x.a0) denom).2 +
    (sDivRem (sMul k x.a1) denom).2 + (sDivRem (sMul k x.a2) denom).2 +
    (sDivRem (sMul k x.a3) denom).2 + (sDivRem (sMul k x.a4) denom).2 +
    (sDivRem (sMul k x.a5) denom).2 + (sDivRem (sMul k x.a6) denom).2 +
    (sDivRem (sMul k x.a7) denom).2 + (sDivRem (sMul k x.a8) denom).2 +
    (sDivRem (sMul k x.a9) denom).2 + (sDivRem (sMul k x.a10) denom).2 +
    (sDivRem (sMul k x.a11) denom).2 + (sDivRem (sMul k x.a12) denom).2 +
    (sDivRem (sMul k x.a13) denom).2 + (sDivRem (sMul k x.a14) denom).2 + sAbs k * x.err
  have hcdiv := cdivOver_spec rem denom hd
  have hd_ne : (denom : ℝ) ≠ 0 := ne_of_gt hd_real
  have hmul_eq : (denom : ℝ) * ((B : ℝ) * ((k.toReal / (denom : ℝ)) * vx)) = (B : ℝ) * (k.toReal * vx) := by
    field_simp [hd_ne]
  suffices hmul :
      |(denom : ℝ) * ((B : ℝ) * (k.toReal / (denom : ℝ) * vx) -
        ((sDivRem (sMul k x.c) denom).1.toReal +
          ((sDivRem (sMul k x.a0) denom).1.toReal * te.v0 +
           (sDivRem (sMul k x.a1) denom).1.toReal * te.v1 +
           (sDivRem (sMul k x.a2) denom).1.toReal * te.v2 +
           (sDivRem (sMul k x.a3) denom).1.toReal * te.v3 +
           (sDivRem (sMul k x.a4) denom).1.toReal * te.v4 +
           (sDivRem (sMul k x.a5) denom).1.toReal * te.v5 +
           (sDivRem (sMul k x.a6) denom).1.toReal * te.e6 +
           (sDivRem (sMul k x.a7) denom).1.toReal * (te.e6 * te.v0) +
           (sDivRem (sMul k x.a8) denom).1.toReal * (te.e6 * te.v1) +
           (sDivRem (sMul k x.a9) denom).1.toReal * (te.e6 * te.v2) +
           (sDivRem (sMul k x.a10) denom).1.toReal * (te.e6 * te.v3) +
           (sDivRem (sMul k x.a11) denom).1.toReal * (te.e6 * te.v4) +
           (sDivRem (sMul k x.a12) denom).1.toReal * (te.e6 * te.v5) +
           (sDivRem (sMul k x.a13) denom).1.toReal * (2 * te.e6 * te.e6 - 1) +
           (sDivRem (sMul k x.a14) denom).1.toReal * (4 * te.e6 * te.e6 * te.e6 - 3 * te.e6))))| ≤
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
      ((sDivRem (sMul k x.a11) denom).2 : ℝ) + ((sDivRem (sMul k x.a12) denom).2 : ℝ) +
      ((sDivRem (sMul k x.a13) denom).2 : ℝ) + ((sDivRem (sMul k x.a14) denom).2 : ℝ) +
      |k.toReal| * (x.err : ℝ) := by
    unfold rem; push_cast; rw [sAbs_toReal]
  rw [abs_le] at hc h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11 h12 h13 h14 h_scaled ⊢
  constructor <;> linarith

lemma abs_mul_bound (a b A B_ : ℝ) (ha : |a| ≤ A) (hb : |b| ≤ B_) (_hB : 0 ≤ B_) :
    |a * b| ≤ A * B_ := by
  rw [abs_mul]
  have hA : 0 ≤ A := le_trans (abs_nonneg a) ha
  exact mul_le_mul ha hb (abs_nonneg b) hA

lemma a15Mul_enc (B : Nat) (hB : 0 < B) (x y : Aff15N) (te : TubeEnv) (vx vy : ℝ)
    (hte : te.Valid) (hx : x.Enc B te vx) (hy : y.Enc B te vy) :
    (a15Mul B x y).Enc B te (vx * vy) := by
  rcases te.basis_bounds hte with
    ⟨b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14⟩
  have h2B_pos : 0 < 2 * B := Nat.mul_pos (by decide) hB
  have h2Br_pos : (0 : ℝ) < ((2 * B : Nat) : ℝ) := Nat.cast_pos.mpr h2B_pos
  set ux := (B : ℝ) * vx - (x.c.toReal + x.linEval te)
  set uy := (B : ℝ) * vy - (y.c.toReal + y.linEval te)
  set Lv1 := x.a0.toReal * te.v0 + x.a1.toReal * te.v1 + x.a2.toReal * te.v2 +
             x.a3.toReal * te.v3 + x.a4.toReal * te.v4 + x.a5.toReal * te.v5
  set Lv2 := y.a0.toReal * te.v0 + y.a1.toReal * te.v1 + y.a2.toReal * te.v2 +
             y.a3.toReal * te.v3 + y.a4.toReal * te.v4 + y.a5.toReal * te.v5
  set R1 := x.a7.toReal * (te.e6 * te.v0) + x.a8.toReal * (te.e6 * te.v1) +
            x.a9.toReal * (te.e6 * te.v2) + x.a10.toReal * (te.e6 * te.v3) +
            x.a11.toReal * (te.e6 * te.v4) + x.a12.toReal * (te.e6 * te.v5) +
            x.a14.toReal * (4 * te.e6 * te.e6 * te.e6 - 3 * te.e6) + ux
  set R2 := y.a7.toReal * (te.e6 * te.v0) + y.a8.toReal * (te.e6 * te.v1) +
            y.a9.toReal * (te.e6 * te.v2) + y.a10.toReal * (te.e6 * te.v3) +
            y.a11.toReal * (te.e6 * te.v4) + y.a12.toReal * (te.e6 * te.v5) +
            y.a14.toReal * (4 * te.e6 * te.e6 * te.e6 - 3 * te.e6) + uy
  set T2 := 2 * te.e6 * te.e6 - 1
  set T3 := 4 * te.e6 * te.e6 * te.e6 - 3 * te.e6
  have hLv1 : |Lv1| ≤ (x.rv : ℝ) := by
    dsimp only [Lv1]; unfold Aff15N.rv; push_cast; simp only [sAbs_toReal]
    have t0 := abs_mul_le_of_abs_le_one x.a0.toReal _ b0
    have t1 := abs_mul_le_of_abs_le_one x.a1.toReal _ b1
    have t2 := abs_mul_le_of_abs_le_one x.a2.toReal _ b2
    have t3 := abs_mul_le_of_abs_le_one x.a3.toReal _ b3
    have t4 := abs_mul_le_of_abs_le_one x.a4.toReal _ b4
    have t5 := abs_mul_le_of_abs_le_one x.a5.toReal _ b5
    rw [abs_le] at t0 t1 t2 t3 t4 t5 ⊢; constructor <;> linarith
  have hLv2 : |Lv2| ≤ (y.rv : ℝ) := by
    dsimp only [Lv2]; unfold Aff15N.rv; push_cast; simp only [sAbs_toReal]
    have t0 := abs_mul_le_of_abs_le_one y.a0.toReal _ b0
    have t1 := abs_mul_le_of_abs_le_one y.a1.toReal _ b1
    have t2 := abs_mul_le_of_abs_le_one y.a2.toReal _ b2
    have t3 := abs_mul_le_of_abs_le_one y.a3.toReal _ b3
    have t4 := abs_mul_le_of_abs_le_one y.a4.toReal _ b4
    have t5 := abs_mul_le_of_abs_le_one y.a5.toReal _ b5
    rw [abs_le] at t0 t1 t2 t3 t4 t5 ⊢; constructor <;> linarith
  have hR1 : |R1| ≤ ((x.rve + x.err : Nat) : ℝ) := by
    dsimp only [R1]; unfold Aff15N.rve; push_cast; simp only [sAbs_toReal]
    have hux : |ux| ≤ (x.err : ℝ) := hx
    have t7 := abs_mul_le_of_abs_le_one x.a7.toReal _ b7
    have t8 := abs_mul_le_of_abs_le_one x.a8.toReal _ b8
    have t9 := abs_mul_le_of_abs_le_one x.a9.toReal _ b9
    have t10 := abs_mul_le_of_abs_le_one x.a10.toReal _ b10
    have t11 := abs_mul_le_of_abs_le_one x.a11.toReal _ b11
    have t12 := abs_mul_le_of_abs_le_one x.a12.toReal _ b12
    have t14 := abs_mul_le_of_abs_le_one x.a14.toReal _ b14
    rw [abs_le] at t7 t8 t9 t10 t11 t12 t14 hux ⊢; constructor <;> linarith
  have hR2 : |R2| ≤ ((y.rve + y.err : Nat) : ℝ) := by
    dsimp only [R2]; unfold Aff15N.rve; push_cast; simp only [sAbs_toReal]
    have huy : |uy| ≤ (y.err : ℝ) := hy
    have t7 := abs_mul_le_of_abs_le_one y.a7.toReal _ b7
    have t8 := abs_mul_le_of_abs_le_one y.a8.toReal _ b8
    have t9 := abs_mul_le_of_abs_le_one y.a9.toReal _ b9
    have t10 := abs_mul_le_of_abs_le_one y.a10.toReal _ b10
    have t11 := abs_mul_le_of_abs_le_one y.a11.toReal _ b11
    have t12 := abs_mul_le_of_abs_le_one y.a12.toReal _ b12
    have t14 := abs_mul_le_of_abs_le_one y.a14.toReal _ b14
    rw [abs_le] at t7 t8 t9 t10 t11 t12 t14 huy ⊢; constructor <;> linarith
  have hid :
      ((2 * B : Nat) : ℝ) * ((B : ℝ) * (vx * vy)) =
      (2 * (x.c.toReal * y.c.toReal) + (x.a6.toReal * y.a6.toReal + x.a13.toReal * y.a13.toReal)) +
      (2 * (x.c.toReal * y.a0.toReal + y.c.toReal * x.a0.toReal) * te.v0 +
       2 * (x.c.toReal * y.a1.toReal + y.c.toReal * x.a1.toReal) * te.v1 +
       2 * (x.c.toReal * y.a2.toReal + y.c.toReal * x.a2.toReal) * te.v2 +
       2 * (x.c.toReal * y.a3.toReal + y.c.toReal * x.a3.toReal) * te.v3 +
       2 * (x.c.toReal * y.a4.toReal + y.c.toReal * x.a4.toReal) * te.v4 +
       2 * (x.c.toReal * y.a5.toReal + y.c.toReal * x.a5.toReal) * te.v5 +
       (2 * (x.c.toReal * y.a6.toReal + y.c.toReal * x.a6.toReal) +
        (x.a6.toReal * y.a13.toReal + x.a13.toReal * y.a6.toReal)) * te.e6 +
       2 * ((x.c.toReal * y.a7.toReal + y.c.toReal * x.a7.toReal) +
            (x.a6.toReal * y.a0.toReal + y.a6.toReal * x.a0.toReal)) * (te.e6 * te.v0) +
       2 * ((x.c.toReal * y.a8.toReal + y.c.toReal * x.a8.toReal) +
            (x.a6.toReal * y.a1.toReal + y.a6.toReal * x.a1.toReal)) * (te.e6 * te.v1) +
       2 * ((x.c.toReal * y.a9.toReal + y.c.toReal * x.a9.toReal) +
            (x.a6.toReal * y.a2.toReal + y.a6.toReal * x.a2.toReal)) * (te.e6 * te.v2) +
       2 * ((x.c.toReal * y.a10.toReal + y.c.toReal * x.a10.toReal) +
            (x.a6.toReal * y.a3.toReal + y.a6.toReal * x.a3.toReal)) * (te.e6 * te.v3) +
       2 * ((x.c.toReal * y.a11.toReal + y.c.toReal * x.a11.toReal) +
            (x.a6.toReal * y.a4.toReal + y.a6.toReal * x.a4.toReal)) * (te.e6 * te.v4) +
       2 * ((x.c.toReal * y.a12.toReal + y.c.toReal * x.a12.toReal) +
            (x.a6.toReal * y.a5.toReal + y.a6.toReal * x.a5.toReal)) * (te.e6 * te.v5) +
       (2 * (x.c.toReal * y.a13.toReal + y.c.toReal * x.a13.toReal) + x.a6.toReal * y.a6.toReal) * T2 +
       (2 * (x.c.toReal * y.a14.toReal + y.c.toReal * x.a14.toReal) +
        (x.a6.toReal * y.a13.toReal + x.a13.toReal * y.a6.toReal)) * T3) +
      (2 * (x.c.toReal * uy + y.c.toReal * ux) +
       (x.a13.toReal * y.a13.toReal) * (2 * T2 * T2 - 1) +
       2 * (Lv1 * (Lv2 + y.a13.toReal * T2 + R2) +
            Lv2 * (x.a13.toReal * T2 + R1) +
            (x.a6.toReal * te.e6) * R2 + (y.a6.toReal * te.e6) * R1 +
            (x.a13.toReal * T2) * R2 + (y.a13.toReal * T2) * R1 + R1 * R2)) := by
    push_cast
    dsimp only [ux, uy, Lv1, Lv2, R1, R2, T2, T3, Aff15N.linEval]
    ring
  have hT2_sh := cheb_T2_sq_shift_abs_le_one te.e6 b6
  have hb6_1 := abs_mul_le_of_abs_le_one x.a6.toReal te.e6 b6
  have hb6_2 := abs_mul_le_of_abs_le_one y.a6.toReal te.e6 b6
  have hq1_T2 := abs_mul_le_of_abs_le_one x.a13.toReal T2 b13
  have hq2_T2 := abs_mul_le_of_abs_le_one y.a13.toReal T2 b13
  have hc1_uy := abs_mul_bound x.c.toReal uy |x.c.toReal| (y.err : ℝ) (le_refl _) hy (Nat.cast_nonneg _)
  have hc2_ux := abs_mul_bound y.c.toReal ux |y.c.toReal| (x.err : ℝ) (le_refl _) hx (Nat.cast_nonneg _)
  have hqq_sh : |(x.a13.toReal * y.a13.toReal) * (2 * T2 * T2 - 1)| ≤ |x.a13.toReal| * |y.a13.toReal| := by
    calc
      |(x.a13.toReal * y.a13.toReal) * (2 * T2 * T2 - 1)|
          ≤ |x.a13.toReal * y.a13.toReal| := abs_mul_le_of_abs_le_one _ _ hT2_sh
      _ = |x.a13.toReal| * |y.a13.toReal| := abs_mul _ _
  have hm_lv1 : |Lv1 * (Lv2 + y.a13.toReal * T2 + R2)| ≤
      (x.rv : ℝ) * ((y.rv : ℝ) + |y.a13.toReal| + ((y.rve + y.err : Nat) : ℝ)) := by
    apply abs_mul_bound _ _ _ _ hLv1
    · rw [abs_le] at hLv2 hq2_T2 hR2 ⊢; constructor <;> linarith
    · positivity
  have hm_lv2 : |Lv2 * (x.a13.toReal * T2 + R1)| ≤
      (y.rv : ℝ) * (|x.a13.toReal| + ((x.rve + x.err : Nat) : ℝ)) := by
    apply abs_mul_bound _ _ _ _ hLv2
    · rw [abs_le] at hq1_T2 hR1 ⊢; constructor <;> linarith
    · positivity
  have hm_b1 : |(x.a6.toReal * te.e6) * R2| ≤ |x.a6.toReal| * ((y.rve + y.err : Nat) : ℝ) :=
    abs_mul_bound _ _ _ _ hb6_1 hR2 (Nat.cast_nonneg _)
  have hm_b2 : |(y.a6.toReal * te.e6) * R1| ≤ |y.a6.toReal| * ((x.rve + x.err : Nat) : ℝ) :=
    abs_mul_bound _ _ _ _ hb6_2 hR1 (Nat.cast_nonneg _)
  have hm_q1 : |(x.a13.toReal * T2) * R2| ≤ |x.a13.toReal| * ((y.rve + y.err : Nat) : ℝ) :=
    abs_mul_bound _ _ _ _ hq1_T2 hR2 (Nat.cast_nonneg _)
  have hm_q2 : |(y.a13.toReal * T2) * R1| ≤ |y.a13.toReal| * ((x.rve + x.err : Nat) : ℝ) :=
    abs_mul_bound _ _ _ _ hq2_T2 hR1 (Nat.cast_nonneg _)
  have hm_rr : |R1 * R2| ≤ ((x.rve + x.err : Nat) : ℝ) * ((y.rve + y.err : Nat) : ℝ) :=
    abs_mul_bound _ _ _ _ hR1 hR2 (Nat.cast_nonneg _)
  set twoB := 2 * B
  set bb := sMul x.a6 y.a6
  set qq := sMul x.a13 y.a13
  set bq := sAdd (sMul x.a6 y.a13) (sMul x.a13 y.a6)
  have hc  := sDivRem_spec (sAdd (sMulNat 2 (sMul x.c y.c)) (sAdd bb qq)) twoB
  have h0  := abs_div_rem_term (sMulNat 2 (sAdd (sMul x.c y.a0) (sMul y.c x.a0))) twoB _ b0
  have h1  := abs_div_rem_term (sMulNat 2 (sAdd (sMul x.c y.a1) (sMul y.c x.a1))) twoB _ b1
  have h2  := abs_div_rem_term (sMulNat 2 (sAdd (sMul x.c y.a2) (sMul y.c x.a2))) twoB _ b2
  have h3  := abs_div_rem_term (sMulNat 2 (sAdd (sMul x.c y.a3) (sMul y.c x.a3))) twoB _ b3
  have h4  := abs_div_rem_term (sMulNat 2 (sAdd (sMul x.c y.a4) (sMul y.c x.a4))) twoB _ b4
  have h5  := abs_div_rem_term (sMulNat 2 (sAdd (sMul x.c y.a5) (sMul y.c x.a5))) twoB _ b5
  have h6  := abs_div_rem_term (sAdd (sMulNat 2 (sAdd (sMul x.c y.a6) (sMul y.c x.a6))) bq) twoB _ b6
  have h7  := abs_div_rem_term (sMulNat 2 (sAdd (sAdd (sMul x.c y.a7) (sMul y.c x.a7)) (sAdd (sMul x.a6 y.a0) (sMul y.a6 x.a0)))) twoB _ b7
  have h8  := abs_div_rem_term (sMulNat 2 (sAdd (sAdd (sMul x.c y.a8) (sMul y.c x.a8)) (sAdd (sMul x.a6 y.a1) (sMul y.a6 x.a1)))) twoB _ b8
  have h9  := abs_div_rem_term (sMulNat 2 (sAdd (sAdd (sMul x.c y.a9) (sMul y.c x.a9)) (sAdd (sMul x.a6 y.a2) (sMul y.a6 x.a2)))) twoB _ b9
  have h10 := abs_div_rem_term (sMulNat 2 (sAdd (sAdd (sMul x.c y.a10) (sMul y.c x.a10)) (sAdd (sMul x.a6 y.a3) (sMul y.a6 x.a3)))) twoB _ b10
  have h11 := abs_div_rem_term (sMulNat 2 (sAdd (sAdd (sMul x.c y.a11) (sMul y.c x.a11)) (sAdd (sMul x.a6 y.a4) (sMul y.a6 x.a4)))) twoB _ b11
  have h12 := abs_div_rem_term (sMulNat 2 (sAdd (sAdd (sMul x.c y.a12) (sMul y.c x.a12)) (sAdd (sMul x.a6 y.a5) (sMul y.a6 x.a5)))) twoB _ b12
  have h13 := abs_div_rem_term (sAdd (sMulNat 2 (sAdd (sMul x.c y.a13) (sMul y.c x.a13))) bb) twoB _ b13
  have h14 := abs_div_rem_term (sAdd (sMulNat 2 (sAdd (sMul x.c y.a14) (sMul y.c x.a14))) bq) twoB _ b14
  simp only [bb, qq, bq, sAdd_toReal, sMul_toReal, sMulNat_toReal, Nat.cast_ofNat] at hc h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11 h12 h13 h14
  unfold a15Mul Aff15N.Enc Aff15N.linEval
  dsimp only
  set err_num :=
    (sDivRem (sAdd (sMulNat 2 (sMul x.c y.c)) (sAdd bb qq)) twoB).2 +
    (sDivRem (sMulNat 2 (sAdd (sMul x.c y.a0) (sMul y.c x.a0))) twoB).2 +
    (sDivRem (sMulNat 2 (sAdd (sMul x.c y.a1) (sMul y.c x.a1))) twoB).2 +
    (sDivRem (sMulNat 2 (sAdd (sMul x.c y.a2) (sMul y.c x.a2))) twoB).2 +
    (sDivRem (sMulNat 2 (sAdd (sMul x.c y.a3) (sMul y.c x.a3))) twoB).2 +
    (sDivRem (sMulNat 2 (sAdd (sMul x.c y.a4) (sMul y.c x.a4))) twoB).2 +
    (sDivRem (sMulNat 2 (sAdd (sMul x.c y.a5) (sMul y.c x.a5))) twoB).2 +
    (sDivRem (sAdd (sMulNat 2 (sAdd (sMul x.c y.a6) (sMul y.c x.a6))) bq) twoB).2 +
    (sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a7) (sMul y.c x.a7)) (sAdd (sMul x.a6 y.a0) (sMul y.a6 x.a0)))) twoB).2 +
    (sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a8) (sMul y.c x.a8)) (sAdd (sMul x.a6 y.a1) (sMul y.a6 x.a1)))) twoB).2 +
    (sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a9) (sMul y.c x.a9)) (sAdd (sMul x.a6 y.a2) (sMul y.a6 x.a2)))) twoB).2 +
    (sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a10) (sMul y.c x.a10)) (sAdd (sMul x.a6 y.a3) (sMul y.a6 x.a3)))) twoB).2 +
    (sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a11) (sMul y.c x.a11)) (sAdd (sMul x.a6 y.a4) (sMul y.a6 x.a4)))) twoB).2 +
    (sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a12) (sMul y.c x.a12)) (sAdd (sMul x.a6 y.a5) (sMul y.a6 x.a5)))) twoB).2 +
    (sDivRem (sAdd (sMulNat 2 (sAdd (sMul x.c y.a13) (sMul y.c x.a13))) bb) twoB).2 +
    (sDivRem (sAdd (sMulNat 2 (sAdd (sMul x.c y.a14) (sMul y.c x.a14))) bq) twoB).2 +
    (2 * (sAbs x.c * y.err + sAbs y.c * x.err) + sAbs x.a13 * sAbs y.a13 +
     2 * (x.rv * (y.rv + sAbs y.a13 + (y.rve + y.err)) + y.rv * (sAbs x.a13 + (x.rve + x.err))) +
     2 * (sAbs x.a6 * (y.rve + y.err) + sAbs y.a6 * (x.rve + x.err)) +
     2 * (sAbs x.a13 * (y.rve + y.err) + sAbs y.a13 * (x.rve + x.err)) +
     2 * (x.rve + x.err) * (y.rve + y.err))
  have hcdiv := cdivOver_spec err_num twoB h2B_pos
  suffices hmul :
      |(twoB : ℝ) * ((B : ℝ) * (vx * vy) -
        ((sDivRem (sAdd (sMulNat 2 (sMul x.c y.c)) (sAdd bb qq)) twoB).1.toReal +
          ((sDivRem (sMulNat 2 (sAdd (sMul x.c y.a0) (sMul y.c x.a0))) twoB).1.toReal * te.v0 +
           (sDivRem (sMulNat 2 (sAdd (sMul x.c y.a1) (sMul y.c x.a1))) twoB).1.toReal * te.v1 +
           (sDivRem (sMulNat 2 (sAdd (sMul x.c y.a2) (sMul y.c x.a2))) twoB).1.toReal * te.v2 +
           (sDivRem (sMulNat 2 (sAdd (sMul x.c y.a3) (sMul y.c x.a3))) twoB).1.toReal * te.v3 +
           (sDivRem (sMulNat 2 (sAdd (sMul x.c y.a4) (sMul y.c x.a4))) twoB).1.toReal * te.v4 +
           (sDivRem (sMulNat 2 (sAdd (sMul x.c y.a5) (sMul y.c x.a5))) twoB).1.toReal * te.v5 +
           (sDivRem (sAdd (sMulNat 2 (sAdd (sMul x.c y.a6) (sMul y.c x.a6))) bq) twoB).1.toReal * te.e6 +
           (sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a7) (sMul y.c x.a7)) (sAdd (sMul x.a6 y.a0) (sMul y.a6 x.a0)))) twoB).1.toReal * (te.e6 * te.v0) +
           (sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a8) (sMul y.c x.a8)) (sAdd (sMul x.a6 y.a1) (sMul y.a6 x.a1)))) twoB).1.toReal * (te.e6 * te.v1) +
           (sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a9) (sMul y.c x.a9)) (sAdd (sMul x.a6 y.a2) (sMul y.a6 x.a2)))) twoB).1.toReal * (te.e6 * te.v2) +
           (sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a10) (sMul y.c x.a10)) (sAdd (sMul x.a6 y.a3) (sMul y.a6 x.a3)))) twoB).1.toReal * (te.e6 * te.v3) +
           (sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a11) (sMul y.c x.a11)) (sAdd (sMul x.a6 y.a4) (sMul y.a6 x.a4)))) twoB).1.toReal * (te.e6 * te.v4) +
           (sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a12) (sMul y.c x.a12)) (sAdd (sMul x.a6 y.a5) (sMul y.a6 x.a5)))) twoB).1.toReal * (te.e6 * te.v5) +
           (sDivRem (sAdd (sMulNat 2 (sAdd (sMul x.c y.a13) (sMul y.c x.a13))) bb) twoB).1.toReal * T2 +
           (sDivRem (sAdd (sMulNat 2 (sAdd (sMul x.c y.a14) (sMul y.c x.a14))) bq) twoB).1.toReal * T3)))| ≤
      (cdivOver err_num twoB : ℝ) * (twoB : ℝ) by
    rw [abs_mul, abs_of_pos h2Br_pos, mul_comm (cdivOver err_num twoB : ℝ)] at hmul
    exact le_of_mul_le_mul_left hmul h2Br_pos
  have herr_cast :
      (err_num : ℝ) =
      ((sDivRem (sAdd (sMulNat 2 (sMul x.c y.c)) (sAdd bb qq)) twoB).2 : ℝ) +
      ((sDivRem (sMulNat 2 (sAdd (sMul x.c y.a0) (sMul y.c x.a0))) twoB).2 : ℝ) +
      ((sDivRem (sMulNat 2 (sAdd (sMul x.c y.a1) (sMul y.c x.a1))) twoB).2 : ℝ) +
      ((sDivRem (sMulNat 2 (sAdd (sMul x.c y.a2) (sMul y.c x.a2))) twoB).2 : ℝ) +
      ((sDivRem (sMulNat 2 (sAdd (sMul x.c y.a3) (sMul y.c x.a3))) twoB).2 : ℝ) +
      ((sDivRem (sMulNat 2 (sAdd (sMul x.c y.a4) (sMul y.c x.a4))) twoB).2 : ℝ) +
      ((sDivRem (sMulNat 2 (sAdd (sMul x.c y.a5) (sMul y.c x.a5))) twoB).2 : ℝ) +
      ((sDivRem (sAdd (sMulNat 2 (sAdd (sMul x.c y.a6) (sMul y.c x.a6))) bq) twoB).2 : ℝ) +
      ((sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a7) (sMul y.c x.a7)) (sAdd (sMul x.a6 y.a0) (sMul y.a6 x.a0)))) twoB).2 : ℝ) +
      ((sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a8) (sMul y.c x.a8)) (sAdd (sMul x.a6 y.a1) (sMul y.a6 x.a1)))) twoB).2 : ℝ) +
      ((sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a9) (sMul y.c x.a9)) (sAdd (sMul x.a6 y.a2) (sMul y.a6 x.a2)))) twoB).2 : ℝ) +
      ((sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a10) (sMul y.c x.a10)) (sAdd (sMul x.a6 y.a3) (sMul y.a6 x.a3)))) twoB).2 : ℝ) +
      ((sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a11) (sMul y.c x.a11)) (sAdd (sMul x.a6 y.a4) (sMul y.a6 x.a4)))) twoB).2 : ℝ) +
      ((sDivRem (sMulNat 2 (sAdd (sAdd (sMul x.c y.a12) (sMul y.c x.a12)) (sAdd (sMul x.a6 y.a5) (sMul y.a6 x.a5)))) twoB).2 : ℝ) +
      ((sDivRem (sAdd (sMulNat 2 (sAdd (sMul x.c y.a13) (sMul y.c x.a13))) bb) twoB).2 : ℝ) +
      ((sDivRem (sAdd (sMulNat 2 (sAdd (sMul x.c y.a14) (sMul y.c x.a14))) bq) twoB).2 : ℝ) +
      (2 * (|x.c.toReal| * (y.err : ℝ) + |y.c.toReal| * (x.err : ℝ)) +
       |x.a13.toReal| * |y.a13.toReal| +
       2 * ((x.rv : ℝ) * ((y.rv : ℝ) + |y.a13.toReal| + ((y.rve + y.err : Nat) : ℝ)) +
            (y.rv : ℝ) * (|x.a13.toReal| + ((x.rve + x.err : Nat) : ℝ))) +
       2 * (|x.a6.toReal| * ((y.rve + y.err : Nat) : ℝ) + |y.a6.toReal| * ((x.rve + x.err : Nat) : ℝ)) +
       2 * (|x.a13.toReal| * ((y.rve + y.err : Nat) : ℝ) + |y.a13.toReal| * ((x.rve + x.err : Nat) : ℝ)) +
       2 * ((x.rve + x.err : Nat) : ℝ) * ((y.rve + y.err : Nat) : ℝ)) := by
    unfold err_num
    push_cast
    simp only [sAbs_toReal]
  rw [abs_le] at hc h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11 h12 h13 h14 hc1_uy hc2_ux hqq_sh hm_lv1 hm_lv2 hm_b1 hm_b2 hm_q1 hm_q2 hm_rr ⊢
  constructor <;> linarith

lemma a15InvPos_enc (B : Nat) (hB : 0 < B) (y res : Aff15N) (te : TubeEnv) (vy : ℝ)
    (hte : te.Valid) (hy : y.Enc B te vy) (h : a15InvPos B y = some res) :
    0 < vy ∧ res.Enc B te (1 / vy) := by
  have hBr_pos : (0 : ℝ) < (B : ℝ) := Nat.cast_pos.mpr hB
  unfold a15InvPos at h
  rcases hm_eq : sPosNat y.lo with _ | m
  · simp [hm_eq] at h
  rcases hc_eq : sPosNat y.c with _ | c
  · simp [hm_eq, hc_eq] at h
  rw [hm_eq, hc_eq] at h; dsimp only at h
  rw [Aff15N.strictB_true] at h
  simp only [↓reduceIte, Option.some.injEq] at h
  rcases sPosNat_spec y.lo m hm_eq with ⟨hm_pos, hlo_eq⟩
  rcases sPosNat_spec y.c c hc_eq with ⟨hc_pos, hc_val⟩
  rcases y.bounds_of_enc B te vy hte hy with ⟨hdy, hlo_le, _⟩
  rw [hlo_eq] at hlo_le
  have hm_real : (0 : ℝ) < (m : ℝ) := Nat.cast_pos.mpr hm_pos
  have hc_real : (0 : ℝ) < (c : ℝ) := Nat.cast_pos.mpr hc_pos
  have hBv_pos : 0 < (B : ℝ) * vy := lt_of_lt_of_le hm_real hlo_le
  have hvy_pos : 0 < vy := pos_of_mul_pos_right hBv_pos (le_of_lt hBr_pos)
  refine ⟨hvy_pos, ?_⟩
  let d : Aff15N := ⟨sZero, y.a0, y.a1, y.a2, y.a3, y.a4, y.a5, y.a6, y.a7, y.a8,
                     y.a9, y.a10, y.a11, y.a12, y.a13, y.a14, y.err⟩
  have hd_enc : d.Enc B te (vy - (c : ℝ) / (B : ℝ)) := by
    unfold Aff15N.Enc at hy ⊢
    have hB_ne : (B : ℝ) ≠ 0 := ne_of_gt hBr_pos
    have hid : (B : ℝ) * (vy - (c : ℝ) / (B : ℝ)) - (d.c.toReal + d.linEval te) =
        (B : ℝ) * vy - (y.c.toReal + y.linEval te) := by
      have hlin : d.linEval te = y.linEval te := rfl
      have hdc : d.c.toReal = 0 := sZero_toReal
      rw [hlin, hdc, hc_val]; field_simp [hB_ne]; ring
    rw [hid]; exact hy
  let u_real := ((B : ℝ) / (c : ℝ)) * (vy - (c : ℝ) / (B : ℝ))
  let u1 := a15ScaleFixed (sOfNat B) d c
  have hu1_enc : u1.Enc B te u_real := by
    have h1 := a15ScaleFixed_enc B (sOfNat B) d c hc_pos te _ hte hd_enc
    rwa [sOfNat_toReal] at h1
  let u2 := a15Mul B u1 u1
  have hu2_enc : u2.Enc B te (u_real * u_real) := a15Mul_enc B hB u1 u1 te _ _ hte hu1_enc hu1_enc
  let u3 := a15Mul B u2 u1
  have hu3_enc : u3.Enc B te (u_real * u_real * u_real) := a15Mul_enc B hB u2 u1 te _ _ hte hu2_enc hu1_enc
  let poly := a15Sub (a15Add (a15Sub (a15Const (sOfNat B)) u1) u2) u3
  have hpoly_enc : poly.Enc B te (1 - u_real + u_real * u_real - u_real * u_real * u_real) := by
    have hc1 := a15Const_enc B hB (sOfNat B) te
    rw [sOfNat_toReal, div_self (ne_of_gt hBr_pos)] at hc1
    exact a15Sub_enc B _ _ te _ _
      (a15Add_enc B _ _ te _ _ (a15Sub_enc B _ _ te _ _ hc1 hu1_enc) hu2_enc) hu3_enc
  let base := a15ScaleFixed (sOfNat B) poly c
  have hbase_enc : base.Enc B te (((B : ℝ) / (c : ℝ)) * (1 - u_real + u_real * u_real - u_real * u_real * u_real)) := by
    have h1 := a15ScaleFixed_enc B (sOfNat B) poly c hc_pos te _ hte hpoly_enc
    rwa [sOfNat_toReal] at h1
  have h_rem_alg :
      (B : ℝ) * (1 / vy) -
        (B : ℝ) * (((B : ℝ) / (c : ℝ)) * (1 - u_real + u_real * u_real - u_real * u_real * u_real)) =
      (((B : ℝ) * (B : ℝ)) *
        ((((B : ℝ) * vy - (c : ℝ)) * ((B : ℝ) * vy - (c : ℝ))) *
         (((B : ℝ) * vy - (c : ℝ)) * ((B : ℝ) * vy - (c : ℝ))))) /
      ((((c : ℝ) * (c : ℝ)) * ((c : ℝ) * (c : ℝ))) * ((B : ℝ) * vy)) := by
    have hc_ne : (c : ℝ) ≠ 0 := ne_of_gt hc_real
    have hB_ne : (B : ℝ) ≠ 0 := ne_of_gt hBr_pos
    have hv_ne : vy ≠ 0 := ne_of_gt hvy_pos
    dsimp only [u_real]; field_simp [hc_ne, hB_ne, hv_ne]; ring
  set rd := y.rad
  set rd2 := rd * rd
  set c2 := c * c
  have hc4m_pos : 0 < (c2 * c2) * m :=
    Nat.mul_pos (Nat.mul_pos (Nat.mul_pos hc_pos hc_pos) (Nat.mul_pos hc_pos hc_pos)) hm_pos
  have hcdiv := cdivOver_spec ((B * B) * (rd2 * rd2)) ((c2 * c2) * m) hc4m_pos
  have hdy_c : |(B : ℝ) * vy - (c : ℝ)| ≤ (rd : ℝ) := by rw [← hc_val]; exact hdy
  have hdy_sq : ((B : ℝ) * vy - (c : ℝ)) * ((B : ℝ) * vy - (c : ℝ)) ≤ (rd2 : ℝ) := by
    have := mul_le_mul hdy_c hdy_c (abs_nonneg _) (Nat.cast_nonneg _)
    rw [← abs_mul, abs_mul_self] at this
    dsimp only [rd2]; push_cast; exact this
  have hdy_4 :
      (((B : ℝ) * vy - (c : ℝ)) * ((B : ℝ) * vy - (c : ℝ))) *
      (((B : ℝ) * vy - (c : ℝ)) * ((B : ℝ) * vy - (c : ℝ))) ≤
      (rd2 : ℝ) * (rd2 : ℝ) :=
    mul_le_mul hdy_sq hdy_sq (mul_self_nonneg _) (Nat.cast_nonneg _)
  have hrem_bound :
      |(B : ℝ) * (1 / vy) -
        (B : ℝ) * (((B : ℝ) / (c : ℝ)) * (1 - u_real + u_real * u_real - u_real * u_real * u_real))| ≤
      (cdivOver ((B * B) * (rd2 * rd2)) ((c2 * c2) * m) : ℝ) := by
    rw [h_rem_alg]
    have hBB_nn : 0 ≤ (B : ℝ) * (B : ℝ) := mul_nonneg (le_of_lt hBr_pos) (le_of_lt hBr_pos)
    have hnum_nn :
        0 ≤ ((B : ℝ) * (B : ℝ)) *
          ((((B : ℝ) * vy - (c : ℝ)) * ((B : ℝ) * vy - (c : ℝ))) *
           (((B : ℝ) * vy - (c : ℝ)) * ((B : ℝ) * vy - (c : ℝ)))) :=
      mul_nonneg hBB_nn (mul_nonneg (mul_self_nonneg _) (mul_self_nonneg _))
    have hc4_pos : 0 < ((c : ℝ) * (c : ℝ)) * ((c : ℝ) * (c : ℝ)) :=
      mul_pos (mul_pos hc_real hc_real) (mul_pos hc_real hc_real)
    have hden_pos : 0 < (((c : ℝ) * (c : ℝ)) * ((c : ℝ) * (c : ℝ))) * ((B : ℝ) * vy) :=
      mul_pos hc4_pos hBv_pos
    rw [abs_of_nonneg (div_nonneg hnum_nn (le_of_lt hden_pos)), div_le_iff₀ hden_pos]
    have hs1 := mul_le_mul_of_nonneg_left hdy_4 hBB_nn
    have hc2_cast : (c2 : ℝ) = (c : ℝ) * (c : ℝ) := by dsimp only [c2]; push_cast; rfl
    push_cast at hcdiv
    rw [hc2_cast] at hcdiv
    have hs2 :
        (cdivOver ((B * B) * (rd2 * rd2)) ((c2 * c2) * m) : ℝ) *
          ((((c : ℝ) * (c : ℝ)) * ((c : ℝ) * (c : ℝ))) * (m : ℝ)) ≤
        (cdivOver ((B * B) * (rd2 * rd2)) ((c2 * c2) * m) : ℝ) *
          ((((c : ℝ) * (c : ℝ)) * ((c : ℝ) * (c : ℝ))) * ((B : ℝ) * vy)) := by
      apply mul_le_mul_of_nonneg_left _ (Nat.cast_nonneg _)
      exact mul_le_mul_of_nonneg_left hlo_le (le_of_lt hc4_pos)
    linarith
  rw [← h]
  unfold Aff15N.Enc at hbase_enc ⊢
  have hlin_eq :
      ({ c := base.c, a0 := base.a0, a1 := base.a1, a2 := base.a2, a3 := base.a3, a4 := base.a4,
         a5 := base.a5, a6 := base.a6, a7 := base.a7, a8 := base.a8, a9 := base.a9,
         a10 := base.a10, a11 := base.a11, a12 := base.a12, a13 := base.a13, a14 := base.a14,
         err := base.err + cdivOver ((B * B) * (rd2 * rd2)) ((c2 * c2) * m) } : Aff15N).linEval te =
      base.linEval te := rfl
  rw [hlin_eq]; dsimp only; push_cast
  rw [abs_le] at hbase_enc hrem_bound ⊢
  constructor <;> linarith

lemma a15DivPos_enc (B : Nat) (hB : 0 < B) (x y res : Aff15N) (te : TubeEnv) (vx vy : ℝ)
    (hte : te.Valid) (hx : x.Enc B te vx) (hy : y.Enc B te vy)
    (h : a15DivPos B x y = some res) :
    0 < vy ∧ res.Enc B te (vx / vy) := by
  have hBr_pos : (0 : ℝ) < (B : ℝ) := Nat.cast_pos.mpr hB
  unfold a15DivPos at h
  rcases hc_eq : sPosNat y.c with _ | c
  · simp [hc_eq] at h
  rcases hinv_eq : a15InvPos B y with _ | invY
  · simp [hc_eq, hinv_eq] at h
  rw [hc_eq, hinv_eq] at h; dsimp only at h
  rw [Aff15N.strictB_true] at h
  simp only [↓reduceIte, Option.some.injEq] at h
  rcases a15InvPos_enc B hB y invY te vy hte hy hinv_eq with ⟨hvy_pos, hinv⟩
  refine ⟨hvy_pos, ?_⟩
  set q0 := (sDivRem (sMulNat B x.c) c).1
  have hrem : (a15Sub x (a15ScaleFixed q0 y B)).Enc B te (vx - (q0.toReal / (B : ℝ)) * vy) :=
    a15Sub_enc B x _ te vx _ hx (a15ScaleFixed_enc B q0 y B hB te vy hte hy)
  have hqr : (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).Enc B te
      ((vx - (q0.toReal / (B : ℝ)) * vy) * (1 / vy)) :=
    a15Mul_enc B hB _ _ te _ _ hte hrem hinv
  rw [← h]
  unfold Aff15N.Enc at hqr ⊢
  have hlin_eq :
      ({ c := sAdd q0 (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).c,
         a0 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a0,
         a1 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a1,
         a2 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a2,
         a3 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a3,
         a4 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a4,
         a5 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a5,
         a6 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a6,
         a7 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a7,
         a8 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a8,
         a9 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a9,
         a10 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a10,
         a11 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a11,
         a12 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a12,
         a13 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a13,
         a14 := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).a14,
         err := (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).err } : Aff15N).linEval te =
      (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).linEval te := rfl
  rw [hlin_eq]; dsimp only; rw [sAdd_toReal]
  have hvy_ne : vy ≠ 0 := ne_of_gt hvy_pos
  have hB_ne : (B : ℝ) ≠ 0 := ne_of_gt hBr_pos
  have hid :
      (B : ℝ) * (vx / vy) -
        (q0.toReal + (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).c.toReal +
         (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).linEval te) =
      (B : ℝ) * ((vx - (q0.toReal / (B : ℝ)) * vy) * (1 / vy)) -
        ((a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).c.toReal +
         (a15Mul B (a15Sub x (a15ScaleFixed q0 y B)) invY).linEval te) := by
    field_simp [hvy_ne, hB_ne]; ring
  rw [hid]; exact hqr

lemma a15Div_enc (B : Nat) (hB : 0 < B) (x y res : Aff15N) (te : TubeEnv) (vx vy : ℝ)
    (hte : te.Valid) (hx : x.Enc B te vx) (hy : y.Enc B te vy)
    (h : a15Div B x y = some res) :
    vy ≠ 0 ∧ res.Enc B te (vx / vy) := by
  unfold a15Div at h
  split_ifs at h with hneg
  · rcases a15DivPos_enc B hB (a15Neg x) (a15Neg y) res te (-vx) (-vy) hte
        (a15Neg_enc B x te vx hx) (a15Neg_enc B y te vy hy) h with ⟨h_neg_pos, hres⟩
    have hv_ne : vy ≠ 0 := by linarith
    rw [neg_div_neg_eq] at hres
    exact ⟨hv_ne, hres⟩
  · rcases a15DivPos_enc B hB x y res te vx vy hte hx hy h with ⟨hv_pos, hres⟩
    exact ⟨ne_of_gt hv_pos, hres⟩

/-! ### Shared Chebyshev Polynomial Basis & Evaluation -/

noncomputable def chebTermReal (t : ℝ) : Nat → ℝ
  | 0     => 1
  | 1     => t
  | k + 2 => 2 * t * chebTermReal t (k + 1) - chebTermReal t k

@[inline] def strictId15 (x : Aff15N) : Aff15N := if x.strictB then x else x

lemma strictId15_eq (x : Aff15N) : strictId15 x = x := by
  unfold strictId15; split_ifs <;> rfl

def chebBasisLoop (B : Nat) (twoT tPrev tCur : Aff15N) : Nat → List Aff15N
  | 0     => []
  | m + 1 =>
    let tNxt := strictId15 (a15Sub (a15Mul B twoT tCur) tPrev)
    tNxt :: chebBasisLoop B twoT tCur tNxt m

def chebBasisA15 (B : Nat) (eAff : Aff15N) (nTerms : Nat) : List Aff15N :=
  let tAff := a15Sub (a15ScaleSInt (sOfNat 48) eAff) (a15Const (sOfNat B))
  let twoT := a15ScaleSInt (sOfNat 2) tAff
  let t0 := a15Const (sOfNat B)
  t0 :: tAff :: chebBasisLoop B twoT t0 tAff (nTerms - 2)

lemma chebBasisLoop_enc (B : Nat) (hB : 0 < B) (te : TubeEnv) (hte : te.Valid) (t : ℝ)
    (twoT : Aff15N) (hTwoT : twoT.Enc B te (2 * t)) :
    ∀ (m k : Nat) (tPrev tCur : Aff15N),
      tPrev.Enc B te (chebTermReal t k) →
      tCur.Enc B te (chebTermReal t (k + 1)) →
      ∀ j < m, ((chebBasisLoop B twoT tPrev tCur m).getD j (a15Const sZero)).Enc B te (chebTermReal t (k + 2 + j))
  | 0, _, _, _, _, _, _, hj => by omega
  | m + 1, k, tPrev, tCur, hp, hc, j, hj => by
    unfold chebBasisLoop
    simp only [strictId15_eq]
    have hnxt : (a15Sub (a15Mul B twoT tCur) tPrev).Enc B te (chebTermReal t (k + 2)) := by
      unfold chebTermReal
      exact a15Sub_enc B _ _ te _ _ (a15Mul_enc B hB _ _ te _ _ hte hTwoT hc) hp
    cases j with
    | zero =>
      simp only [List.getD_cons_zero, Nat.add_zero]
      exact hnxt
    | succ j' =>
      simp only [List.getD_cons_succ]
      have hrec := chebBasisLoop_enc B hB te hte t twoT hTwoT m (k + 1) tCur
        (a15Sub (a15Mul B twoT tCur) tPrev) hc hnxt j' (Nat.lt_of_succ_lt_succ hj)
      have hidx : k + 1 + 2 + j' = k + 2 + (j' + 1) := by omega
      rwa [hidx] at hrec

lemma chebBasisA15_enc (B : Nat) (hB : 0 < B) (te : TubeEnv) (hte : te.Valid)
    (eAff : Aff15N) (eps : ℝ) (heps : eAff.Enc B te eps) (nTerms : Nat) :
    ∀ k < nTerms,
      ((chebBasisA15 B eAff nTerms).getD k (a15Const sZero)).Enc B te (chebTermReal (48 * eps - 1) k) := by
  have hBr_ne : (B : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hB)
  unfold chebBasisA15
  set tAff := a15Sub (a15ScaleSInt (sOfNat 48) eAff) (a15Const (sOfNat B))
  have htAff : tAff.Enc B te (48 * eps - 1) := by
    have h48 := a15ScaleSInt_enc B (sOfNat 48) eAff te eps heps
    rw [sOfNat_toReal] at h48; norm_num at h48
    have h1 := a15Const_enc B hB (sOfNat B) te
    rw [sOfNat_toReal, div_self hBr_ne] at h1
    exact a15Sub_enc B _ _ te _ _ h48 h1
  set twoT := a15ScaleSInt (sOfNat 2) tAff
  have htwoT : twoT.Enc B te (2 * (48 * eps - 1)) := by
    have h2 := a15ScaleSInt_enc B (sOfNat 2) tAff te _ htAff
    rwa [sOfNat_toReal, Nat.cast_ofNat] at h2
  have ht0 : (a15Const (sOfNat B)).Enc B te (chebTermReal (48 * eps - 1) 0) := by
    unfold chebTermReal
    have h1 := a15Const_enc B hB (sOfNat B) te
    rwa [sOfNat_toReal, div_self hBr_ne] at h1
  have ht1 : tAff.Enc B te (chebTermReal (48 * eps - 1) 1) := htAff
  intro k hk
  cases k with
  | zero => exact ht0
  | succ k1 =>
    cases k1 with
    | zero => exact ht1
    | succ k2 =>
      simp only [List.getD_cons_succ]
      have hk2 : k2 < nTerms - 2 := by omega
      have hres := chebBasisLoop_enc B hB te hte (48 * eps - 1) twoT htwoT (nTerms - 2) 0
        (a15Const (sOfNat B)) tAff ht0 ht1 k2 hk2
      have hidx2 : 0 + 2 + k2 = k2 + 1 + 1 := by omega
      rwa [hidx2] at hres

def evalChebTail (B : Nat) (basis : List Aff15N) : Nat → List SInt → Aff15N → Aff15N
  | _, [], acc      => acc
  | idx, c :: cs, acc =>
    let term := a15ScaleFixed c (basis.getD idx (a15Const sZero)) B
    evalChebTail B basis (idx + 1) cs (a15Add acc term)

def evalChebFromBasis (B : Nat) (basis : List Aff15N) (coefs : List SInt) : Aff15N :=
  match coefs with
  | []      => a15Const sZero
  | c0 :: cs => evalChebTail B basis 1 cs (a15Const c0)

noncomputable def evalChebTailReal (B : Nat) (t : ℝ) : Nat → List SInt → ℝ → ℝ
  | _, [], acc      => acc
  | idx, c :: cs, acc =>
    evalChebTailReal B t (idx + 1) cs (acc + (c.toReal / (B : ℝ)) * chebTermReal t idx)

noncomputable def evalChebReal (B : Nat) (eps : ℝ) (coefs : List SInt) : ℝ :=
  match coefs with
  | []      => 0
  | c0 :: cs => evalChebTailReal B (48 * eps - 1) 1 cs (c0.toReal / (B : ℝ))

lemma evalChebTail_enc (B : Nat) (hB : 0 < B) (te : TubeEnv) (hte : te.Valid)
    (basis : List Aff15N) (t : ℝ) (nTerms : Nat)
    (hbasis : ∀ k < nTerms, (basis.getD k (a15Const sZero)).Enc B te (chebTermReal t k)) :
    ∀ (cs : List SInt) (idx : Nat) (acc : Aff15N) (vacc : ℝ),
      idx + cs.length ≤ nTerms →
      acc.Enc B te vacc →
      (evalChebTail B basis idx cs acc).Enc B te (evalChebTailReal B t idx cs vacc)
  | [], _, acc, _, _, hacc => hacc
  | c :: cs, idx, acc, vacc, hlen, hacc => by
    unfold evalChebTail evalChebTailReal
    simp only [List.length_cons] at hlen
    have hidx : idx < nTerms := by omega
    have hterm := a15ScaleFixed_enc B c (basis.getD idx (a15Const sZero)) B hB te _ hte (hbasis idx hidx)
    exact evalChebTail_enc B hB te hte basis t nTerms hbasis cs (idx + 1)
      (a15Add acc _) _ (by omega) (a15Add_enc B _ _ te _ _ hacc hterm)

lemma evalChebFromBasis_enc (B : Nat) (hB : 0 < B) (te : TubeEnv) (hte : te.Valid)
    (basis : List Aff15N) (eps : ℝ) (nTerms : Nat)
    (hbasis : ∀ k < nTerms, (basis.getD k (a15Const sZero)).Enc B te (chebTermReal (48 * eps - 1) k))
    (coefs : List SInt) (hlen : coefs.length ≤ nTerms) :
    (evalChebFromBasis B basis coefs).Enc B te (evalChebReal B eps coefs) := by
  unfold evalChebFromBasis evalChebReal
  cases coefs with
  | nil => exact a15Zero_enc B te
  | cons c0 cs =>
    simp only [List.length_cons] at hlen
    exact evalChebTail_enc B hB te hte basis (48 * eps - 1) nTerms hbasis cs 1
      (a15Const c0) (c0.toReal / (B : ℝ)) (by omega) (a15Const_enc B hB c0 te)

end PRMPlus
