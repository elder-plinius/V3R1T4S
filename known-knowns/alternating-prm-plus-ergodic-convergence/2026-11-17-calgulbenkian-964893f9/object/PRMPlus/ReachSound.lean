import PRMPlus.Aff12Sound

/-!
# Soundness of Algorithm 2 Step (`alg2StepA12`) and Unit-`L` Lohner Re-Wrapping (`rewrapWithL`)
-/

namespace PRMPlus

open scoped BigOperators

@[inline] def isExactZero12 (x : Aff12N) : Bool := (x.c == sZero) && (x.rad == 0)
@[inline] def isExactOne12 (B : Nat) (x : Aff12N) : Bool := (x.c == sOfNat B) && (x.rad == 0)

lemma isExactZero12_enc (B : Nat) (hB : 0 < B) (x : Aff12N) (e : Fin 12 → ℝ) (v : ℝ)
    (he : ValidEnv12 e) (hx : x.Enc B e v) (hz : isExactZero12 x = true) :
    v = 0 := by
  unfold isExactZero12 at hz
  simp only [Bool.and_eq_true, beq_iff_eq] at hz
  rcases (x.bounds_of_enc B e v he hx) with ⟨hb, _, _⟩
  rw [hz.1, hz.2, sZero_toReal] at hb
  simp only [sub_zero, Nat.cast_zero, abs_nonpos_iff] at hb
  have hBr : (B : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hB)
  exact (mul_eq_zero.mp hb).resolve_left hBr

lemma isExactOne12_enc (B : Nat) (hB : 0 < B) (x : Aff12N) (e : Fin 12 → ℝ) (v : ℝ)
    (he : ValidEnv12 e) (hx : x.Enc B e v) (ho : isExactOne12 B x = true) :
    v = 1 := by
  unfold isExactOne12 at ho
  simp only [Bool.and_eq_true, beq_iff_eq] at ho
  rcases (x.bounds_of_enc B e v he hx) with ⟨hb, _, _⟩
  rw [ho.1, ho.2, sOfNat_toReal] at hb
  simp only [Nat.cast_zero, abs_nonpos_iff] at hb
  have hBr : (B : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hB)
  have hmul : (B : ℝ) * v = (B : ℝ) * 1 := by linarith
  exact mul_left_cancel₀ hBr hmul

def a12Basis (j : Fin 12) (r : Nat) : Aff12N :=
  let sr := sOfNat r
  ⟨sZero,
   if j.val == 0 then sr else sZero,
   if j.val == 1 then sr else sZero,
   if j.val == 2 then sr else sZero,
   if j.val == 3 then sr else sZero,
   if j.val == 4 then sr else sZero,
   if j.val == 5 then sr else sZero,
   if j.val == 6 then sr else sZero,
   if j.val == 7 then sr else sZero,
   if j.val == 8 then sr else sZero,
   if j.val == 9 then sr else sZero,
   if j.val == 10 then sr else sZero,
   if j.val == 11 then sr else sZero, 0⟩

lemma a12Basis_linEval (j : Fin 12) (r : Nat) (e : Fin 12 → ℝ) :
    (a12Basis j r).linEval e = (r : ℝ) * e j := by
  unfold a12Basis Aff12N.linEval
  rcases j with ⟨jv, hjv⟩
  have hcases : jv = 0 ∨ jv = 1 ∨ jv = 2 ∨ jv = 3 ∨ jv = 4 ∨ jv = 5 ∨
                jv = 6 ∨ jv = 7 ∨ jv = 8 ∨ jv = 9 ∨ jv = 10 ∨ jv = 11 := by omega
  rcases hcases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    · simp [sOfNat_toReal, sZero_toReal]

noncomputable def makeEnvCoord (B : Nat) (r : Nat) (w : ℝ) : ℝ :=
  if r = 0 then 0 else ((B : ℝ) * w) / (r : ℝ)

lemma abs_makeEnvCoord_le_one (B r : Nat) (w : ℝ) (hw : |(B : ℝ) * w| ≤ (r : ℝ)) :
    |makeEnvCoord B r w| ≤ 1 := by
  unfold makeEnvCoord
  split_ifs with hr
  · norm_num
  · have hr_pos : (0 : ℝ) < (r : ℝ) := Nat.cast_pos.mpr (Nat.pos_of_ne_zero hr)
    rw [abs_div, abs_of_pos hr_pos, div_le_one hr_pos]
    exact hw

lemma a12Basis_enc_makeEnv (B : Nat) (r : Fin 12 → Nat) (w : Fin 12 → ℝ)
    (hw : ∀ j : Fin 12, |(B : ℝ) * w j| ≤ (r j : ℝ)) (j : Fin 12) :
    (a12Basis j (r j)).Enc B (fun k => makeEnvCoord B (r k) (w k)) (w j) := by
  unfold Aff12N.Enc
  rw [a12Basis_linEval]
  have hc : (a12Basis j (r j)).c.toReal = 0 := sZero_toReal
  have herr : ((a12Basis j (r j)).err : ℝ) = 0 := by unfold a12Basis; simp
  rw [hc, herr, zero_add]
  unfold makeEnvCoord
  split_ifs with hr
  · have h0 := hw j
    rw [hr, Nat.cast_zero, abs_nonpos_iff] at h0
    simp [h0]
  · have hr_ne : (r j : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hr
    have hmul : (r j : ℝ) * (((B : ℝ) * w j) / (r j : ℝ)) = (B : ℝ) * w j :=
      mul_div_cancel₀ _ hr_ne
    rw [hmul]; simp

/-! ### 12-Component State `State12` -/

structure State12 where
  rx0 : Aff12N
  rx1 : Aff12N
  rx2 : Aff12N
  ry0 : Aff12N
  ry1 : Aff12N
  ry2 : Aff12N
  x0  : Aff12N
  x1  : Aff12N
  x2  : Aff12N
  y0  : Aff12N
  y1  : Aff12N
  y2  : Aff12N
  deriving DecidableEq

@[inline] def State12.strictB (s : State12) : Bool :=
  s.rx0.strictB && s.rx1.strictB && s.rx2.strictB &&
  s.ry0.strictB && s.ry1.strictB && s.ry2.strictB &&
  s.x0.strictB && s.x1.strictB && s.x2.strictB &&
  s.y0.strictB && s.y1.strictB && s.y2.strictB

lemma State12.strictB_true (s : State12) : s.strictB = true := by
  unfold State12.strictB; simp [Aff12N.strictB_true]

def State12.get (s : State12) (i : Fin 12) : Aff12N :=
  match i.val with
  | 0  => s.rx0 | 1  => s.rx1 | 2  => s.rx2
  | 3  => s.ry0 | 4  => s.ry1 | 5  => s.ry2
  | 6  => s.x0  | 7  => s.x1  | 8  => s.x2
  | 9  => s.y0  | 10 => s.y1  | _  => s.y2

def State12.ofFn (f : Fin 12 → Aff12N) : State12 :=
  ⟨f 0, f 1, f 2, f 3, f 4, f 5, f 6, f 7, f 8, f 9, f 10, f 11⟩

lemma State12.get_ofFn (f : Fin 12 → Aff12N) (i : Fin 12) :
    (State12.ofFn f).get i = f i := by
  rcases i with ⟨iv, hiv⟩
  have hcases : iv = 0 ∨ iv = 1 ∨ iv = 2 ∨ iv = 3 ∨ iv = 4 ∨ iv = 5 ∨
                iv = 6 ∨ iv = 7 ∨ iv = 8 ∨ iv = 9 ∨ iv = 10 ∨ iv = 11 := by omega
  rcases hcases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> rfl

noncomputable def rmStateCoord (st : RMState 3 3) (i : Fin 12) : ℝ :=
  match i.val with
  | 0  => st.Rx 0 | 1  => st.Rx 1 | 2  => st.Rx 2
  | 3  => st.Ry 0 | 4  => st.Ry 1 | 5  => st.Ry 2
  | 6  => st.x 0  | 7  => st.x 1  | 8  => st.x 2
  | 9  => st.y 0  | 10 => st.y 1  | _  => st.y 2

def State12.Enc (B : Nat) (s : State12) (e : Fin 12 → ℝ) (st : RMState 3 3) : Prop :=
  ∀ i : Fin 12, (s.get i).Enc B e (rmStateCoord st i)

def initState12 (u0 : Nat) : State12 :=
  let z := a12Const sZero
  let u := a12Const (sOfNat u0)
  ⟨z, z, z, z, z, z, u, u, u, u, u, u⟩

lemma initState12_enc (B u0 : Nat) (hB : 0 < B) (h3 : B = 3 * u0) :
    ∃ e : Fin 12 → ℝ, ValidEnv12 e ∧ (initState12 u0).Enc B e (initState 3 3) := by
  refine ⟨fun _ => 0, fun _ => by norm_num, ?_⟩
  have hu_div : (sOfNat u0).toReal / (B : ℝ) = (1 : ℝ) / ((3 : ℕ) : ℝ) := by
    rw [sOfNat_toReal]
    have hBr : (B : ℝ) = 3 * (u0 : ℝ) := by exact_mod_cast h3
    have hBne : (B : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hB)
    norm_num; field_simp [hBne]; linarith
  have hu_enc : (a12Const (sOfNat u0)).Enc B (fun _ => 0) ((1 : ℝ) / ((3 : ℕ) : ℝ)) := by
    rw [← hu_div]; exact a12Const_enc B hB _ _
  intro ⟨iv, hiv⟩
  have hcases : iv = 0 ∨ iv = 1 ∨ iv = 2 ∨ iv = 3 ∨ iv = 4 ∨ iv = 5 ∨
                iv = 6 ∨ iv = 7 ∨ iv = 8 ∨ iv = 9 ∨ iv = 10 ∨ iv = 11 := by omega
  rcases hcases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact a12Zero_enc B _
  · exact a12Zero_enc B _
  · exact a12Zero_enc B _
  · exact a12Zero_enc B _
  · exact a12Zero_enc B _
  · exact a12Zero_enc B _
  · exact hu_enc
  · exact hu_enc
  · exact hu_enc
  · exact hu_enc
  · exact hu_enc
  · exact hu_enc

/-! ### Simplex Normalization & One Step of Algorithm 2 in `Aff12N` -/

def divOrZero12 (B : Nat) (p sp : Aff12N) : Option Aff12N :=
  if isExactZero12 p then some (a12Const sZero) else a12DivPos B p sp

def normSimplexA12 (B : Nat) (p0 p1 p2 : Aff12N) : Option (Aff12N × Aff12N × Aff12N) :=
  let sp := a12Add (a12Add p0 p1) p2
  match sPosNat sp.lo with
  | none => none
  | some _ =>
    if isExactZero12 p0 && isExactZero12 p1 then
      match sPosNat p2.lo with
      | none => none
      | some _ => some (a12Const sZero, a12Const sZero, a12Const (sOfNat B))
    else
      match divOrZero12 B p0 sp, divOrZero12 B p1 sp, divOrZero12 B p2 sp with
      | some q0, some q1, some q2 => some (q0, q1, q2)
      | _, _, _ => none

lemma normSimplexA12_enc (B : Nat) (hB : 0 < B) (p0 p1 p2 q0 q1 q2 : Aff12N)
    (e : Fin 12 → ℝ) (z : Fin 3 → ℝ)
    (he : ValidEnv12 e) (hz : ∀ i, 0 ≤ z i)
    (hp0 : p0.Enc B e (z 0)) (hp1 : p1.Enc B e (z 1)) (hp2 : p2.Enc B e (z 2))
    (h : normSimplexA12 B p0 p1 p2 = some (q0, q1, q2)) :
    q0.Enc B e (normalize z 0) ∧ q1.Enc B e (normalize z 1) ∧ q2.Enc B e (normalize z 2) := by
  have hBr_pos : (0 : ℝ) < (B : ℝ) := Nat.cast_pos.mpr hB
  unfold normSimplexA12 at h
  set sp := a12Add (a12Add p0 p1) p2
  have hsp_enc : sp.Enc B e (z 0 + z 1 + z 2) :=
    a12Add_enc B _ p2 e (z 0 + z 1) (z 2) (a12Add_enc B p0 p1 e (z 0) (z 1) hp0 hp1) hp2
  rcases hsp_pos_eq : sPosNat sp.lo with _ | m_sp
  · simp [hsp_pos_eq] at h
  simp only [hsp_pos_eq] at h
  rcases sPosNat_spec sp.lo m_sp hsp_pos_eq with ⟨hm_sp_pos, hsp_lo_val⟩
  have hsp_lo_le := (sp.bounds_of_enc B e _ he hsp_enc).2.1
  rw [hsp_lo_val] at hsp_lo_le
  have hBsum_pos : 0 < (B : ℝ) * (z 0 + z 1 + z 2) :=
    lt_of_lt_of_le (Nat.cast_pos.mpr hm_sp_pos) hsp_lo_le
  have hsum_pos : 0 < z 0 + z 1 + z 2 := pos_of_mul_pos_right hBsum_pos (le_of_lt hBr_pos)
  rw [normalize_fin3_of_pos z hz hsum_pos]; dsimp only
  split_ifs at h with hzz
  · rcases hp2_pos_eq : sPosNat p2.lo with _ | m2
    · simp [hp2_pos_eq] at h
    simp [hp2_pos_eq] at h
    rcases h with ⟨rfl, rfl, rfl⟩
    simp only [Bool.and_eq_true] at hzz
    have hz0 : z 0 = 0 := isExactZero12_enc B hB p0 e (z 0) he hp0 hzz.1
    have hz1 : z 1 = 0 := isExactZero12_enc B hB p1 e (z 1) he hp1 hzz.2
    have hz2_ne : z 2 ≠ 0 := by linarith
    have hdiv0 : z 0 / (z 0 + z 1 + z 2) = 0 := by rw [hz0]; simp
    have hdiv1 : z 1 / (z 0 + z 1 + z 2) = 0 := by rw [hz1]; simp
    have hdiv2 : z 2 / (z 0 + z 1 + z 2) = (sOfNat B).toReal / (B : ℝ) := by
      rw [hz0, hz1, zero_add, zero_add, div_self hz2_ne, sOfNat_toReal, div_self (ne_of_gt hBr_pos)]
    rw [hdiv0, hdiv1, hdiv2]
    exact ⟨a12Zero_enc B e, a12Zero_enc B e, a12Const_enc B hB (sOfNat B) e⟩
  · have step_coord (pi qi : Aff12N) (vi : ℝ) (hpi : pi.Enc B e vi)
        (hi_opt : divOrZero12 B pi sp = some qi) :
        qi.Enc B e (vi / (z 0 + z 1 + z 2)) := by
      unfold divOrZero12 at hi_opt
      split_ifs at hi_opt with hzi
      · injection hi_opt with hqi
        rw [← hqi, isExactZero12_enc B hB pi e vi he hpi hzi, zero_div]
        exact a12Zero_enc B e
      · exact (a12DivPos_enc B hB pi sp qi e vi _ he hpi hsp_enc hi_opt).2
    rcases hq0_eq : divOrZero12 B p0 sp with _ | r0
    · simp [hq0_eq] at h
    rcases hq1_eq : divOrZero12 B p1 sp with _ | r1
    · simp [hq0_eq, hq1_eq] at h
    rcases hq2_eq : divOrZero12 B p2 sp with _ | r2
    · simp [hq0_eq, hq1_eq, hq2_eq] at h
    simp [hq0_eq, hq1_eq, hq2_eq] at h
    rcases h with ⟨rfl, rfl, rfl⟩
    exact ⟨step_coord p0 r0 (z 0) hp0 hq0_eq,
           step_coord p1 r1 (z 1) hp1 hq1_eq,
           step_coord p2 r2 (z 2) hp2 hq2_eq⟩

structure Alg2Pre12 where
  rx0' : Aff12N
  rx1' : Aff12N
  rx2' : Aff12N
  ry0' : Aff12N
  ry1' : Aff12N
  ry2' : Aff12N
  px0  : Aff12N
  px1  : Aff12N
  px2  : Aff12N
  py0  : Aff12N
  py1  : Aff12N
  py2  : Aff12N

def alg2PreA12 (B : Nat) (s : State12) : Alg2Pre12 :=
  let s3 := sOfNat 3
  let s4 := sOfNat 4
  let sm3 := sNegOfNat 3
  let ay0 := a12Sub (a12ScaleSInt s3 s.y0) (a12ScaleSInt s3 s.y2)
  let ay1 := a12Sub (a12ScaleSInt s3 s.y1) (a12ScaleSInt s4 s.y2)
  let ay2 := s.y2
  let xAy := a12Add (a12Add (a12Mul B s.x0 ay0) (a12Mul B s.x1 ay1)) (a12Mul B s.x2 ay2)
  let fx0 := a12Sub ay0 xAy
  let fx1 := a12Sub ay1 xAy
  let fx2 := a12Sub ay2 xAy
  let atx0 := a12ScaleSInt s3 s.x0
  let atx1 := a12ScaleSInt s3 s.x1
  let atx2 := a12Add (a12Sub (a12ScaleSInt sm3 s.x0) (a12ScaleSInt s4 s.x1)) s.x2
  let yATx := a12Add (a12Add (a12Mul B s.y0 atx0) (a12Mul B s.y1 atx1)) (a12Mul B s.y2 atx2)
  let fy0 := a12Sub atx0 yATx
  let fy1 := a12Sub atx1 yATx
  let fy2 := a12Sub atx2 yATx
  let rx0' := a12Max0 (a12Sub s.rx0 fx0)
  let rx1' := a12Max0 (a12Sub s.rx1 fx1)
  let rx2' := a12Max0 (a12Sub s.rx2 fx2)
  let ry0' := a12Max0 (a12Add s.ry0 fy0)
  let ry1' := a12Max0 (a12Add s.ry1 fy1)
  let ry2' := a12Max0 (a12Add s.ry2 fy2)
  let px0 := a12Max0 (a12Sub rx0' fx0)
  let px1 := a12Max0 (a12Sub rx1' fx1)
  let px2 := a12Max0 (a12Sub rx2' fx2)
  let py0 := a12Max0 (a12Add ry0' fy0)
  let py1 := a12Max0 (a12Add ry1' fy1)
  let py2 := a12Max0 (a12Add ry2' fy2)
  ⟨rx0', rx1', rx2', ry0', ry1', ry2', px0, px1, px2, py0, py1, py2⟩

def alg2StepA12 (B : Nat) (s : State12) : Option State12 :=
  let pre := alg2PreA12 B s
  match normSimplexA12 B pre.px0 pre.px1 pre.px2, normSimplexA12 B pre.py0 pre.py1 pre.py2 with
  | some (x0', x1', x2'), some (y0', y1', y2') =>
    let out : State12 := ⟨pre.rx0', pre.rx1', pre.rx2', pre.ry0', pre.ry1', pre.ry2', x0', x1', x2', y0', y1', y2'⟩
    if out.strictB then some out else none
  | _, _ => none

lemma alg2PreA12_enc (B : Nat) (hB : 0 < B) (s : State12) (e : Fin 12 → ℝ) (st : RMState 3 3)
    (he : ValidEnv12 e) (hs : s.Enc B e st) :
    let pre := alg2PreA12 B s
    let px_real := vecPosPart (fun i => (alg2Step caiGameA st).Rx i - negInstRegret st.x (matMulVec caiGameA st.y) i)
    let py_real := vecPosPart (fun j => (alg2Step caiGameA st).Ry j + negInstRegret st.y (matTMulVec caiGameA st.x) j)
    pre.rx0'.Enc B e ((alg2Step caiGameA st).Rx 0) ∧
    pre.rx1'.Enc B e ((alg2Step caiGameA st).Rx 1) ∧
    pre.rx2'.Enc B e ((alg2Step caiGameA st).Rx 2) ∧
    pre.ry0'.Enc B e ((alg2Step caiGameA st).Ry 0) ∧
    pre.ry1'.Enc B e ((alg2Step caiGameA st).Ry 1) ∧
    pre.ry2'.Enc B e ((alg2Step caiGameA st).Ry 2) ∧
    pre.px0.Enc B e (px_real 0) ∧
    pre.px1.Enc B e (px_real 1) ∧
    pre.px2.Enc B e (px_real 2) ∧
    pre.py0.Enc B e (py_real 0) ∧
    pre.py1.Enc B e (py_real 1) ∧
    pre.py2.Enc B e (py_real 2) := by
  dsimp only [alg2PreA12]
  have h0 := hs 0; have h1 := hs 1; have h2 := hs 2
  have h3 := hs 3; have h4 := hs 4; have h5 := hs 5
  have h6 := hs 6; have h7 := hs 7; have h8 := hs 8
  have h9 := hs 9; have h10 := hs 10; have h11 := hs 11
  dsimp only [State12.get, rmStateCoord] at h0 h1 h2 h3 h4 h5 h6 h7 h8 h9 h10 h11
  rcases matMulVec_caiGameA st.y with ⟨hmy0, hmy1, hmy2⟩
  rcases matTMulVec_caiGameA st.x with ⟨htx0, htx1, htx2⟩
  have hs3 : (sOfNat 3).toReal = 3 := by simp [sOfNat_toReal]
  have hs4 : (sOfNat 4).toReal = 4 := by simp [sOfNat_toReal]
  have hsm3 : (sNegOfNat 3).toReal = -3 := by simp [sNegOfNat_toReal]
  have hay0 : (a12Sub (a12ScaleSInt (sOfNat 3) s.y0) (a12ScaleSInt (sOfNat 3) s.y2)).Enc B e
      (matMulVec caiGameA st.y 0) := by
    rw [hmy0]
    have t1 := a12ScaleSInt_enc B (sOfNat 3) s.y0 e (st.y 0) h9; rw [hs3] at t1
    have t2 := a12ScaleSInt_enc B (sOfNat 3) s.y2 e (st.y 2) h11; rw [hs3] at t2
    exact a12Sub_enc B _ _ e _ _ t1 t2
  have hay1 : (a12Sub (a12ScaleSInt (sOfNat 3) s.y1) (a12ScaleSInt (sOfNat 4) s.y2)).Enc B e
      (matMulVec caiGameA st.y 1) := by
    rw [hmy1]
    have t1 := a12ScaleSInt_enc B (sOfNat 3) s.y1 e (st.y 1) h10; rw [hs3] at t1
    have t2 := a12ScaleSInt_enc B (sOfNat 4) s.y2 e (st.y 2) h11; rw [hs4] at t2
    exact a12Sub_enc B _ _ e _ _ t1 t2
  have hay2 : s.y2.Enc B e (matMulVec caiGameA st.y 2) := by rw [hmy2]; exact h11
  set ay0 := a12Sub (a12ScaleSInt (sOfNat 3) s.y0) (a12ScaleSInt (sOfNat 3) s.y2)
  set ay1 := a12Sub (a12ScaleSInt (sOfNat 3) s.y1) (a12ScaleSInt (sOfNat 4) s.y2)
  set xAy := a12Add (a12Add (a12Mul B s.x0 ay0) (a12Mul B s.x1 ay1)) (a12Mul B s.x2 s.y2)
  have hxAy : xAy.Enc B e (∑ j : Fin 3, st.x j * matMulVec caiGameA st.y j) := by
    rw [sum_fin3]
    exact a12Add_enc B _ _ e _ _
      (a12Add_enc B _ _ e _ _ (a12Mul_enc B hB _ _ e _ _ he h6 hay0) (a12Mul_enc B hB _ _ e _ _ he h7 hay1))
      (a12Mul_enc B hB _ _ e _ _ he h8 hay2)
  set fx0 := a12Sub ay0 xAy
  set fx1 := a12Sub ay1 xAy
  set fx2 := a12Sub s.y2 xAy
  have hfx0 : fx0.Enc B e (negInstRegret st.x (matMulVec caiGameA st.y) 0) := a12Sub_enc B _ _ e _ _ hay0 hxAy
  have hfx1 : fx1.Enc B e (negInstRegret st.x (matMulVec caiGameA st.y) 1) := a12Sub_enc B _ _ e _ _ hay1 hxAy
  have hfx2 : fx2.Enc B e (negInstRegret st.x (matMulVec caiGameA st.y) 2) := a12Sub_enc B _ _ e _ _ hay2 hxAy
  set atx0 := a12ScaleSInt (sOfNat 3) s.x0
  set atx1 := a12ScaleSInt (sOfNat 3) s.x1
  set atx2 := a12Add (a12Sub (a12ScaleSInt (sNegOfNat 3) s.x0) (a12ScaleSInt (sOfNat 4) s.x1)) s.x2
  have hatx0 : atx0.Enc B e (matTMulVec caiGameA st.x 0) := by
    rw [htx0]; have t := a12ScaleSInt_enc B (sOfNat 3) s.x0 e (st.x 0) h6; rwa [hs3] at t
  have hatx1 : atx1.Enc B e (matTMulVec caiGameA st.x 1) := by
    rw [htx1]; have t := a12ScaleSInt_enc B (sOfNat 3) s.x1 e (st.x 1) h7; rwa [hs3] at t
  have hatx2 : atx2.Enc B e (matTMulVec caiGameA st.x 2) := by
    rw [htx2]
    have t1 := a12ScaleSInt_enc B (sNegOfNat 3) s.x0 e (st.x 0) h6; rw [hsm3] at t1
    have t2 := a12ScaleSInt_enc B (sOfNat 4) s.x1 e (st.x 1) h7; rw [hs4] at t2
    exact a12Add_enc B _ _ e _ _ (a12Sub_enc B _ _ e _ _ t1 t2) h8
  set yATx := a12Add (a12Add (a12Mul B s.y0 atx0) (a12Mul B s.y1 atx1)) (a12Mul B s.y2 atx2)
  have hyATx : yATx.Enc B e (∑ j : Fin 3, st.y j * matTMulVec caiGameA st.x j) := by
    rw [sum_fin3]
    exact a12Add_enc B _ _ e _ _
      (a12Add_enc B _ _ e _ _ (a12Mul_enc B hB _ _ e _ _ he h9 hatx0) (a12Mul_enc B hB _ _ e _ _ he h10 hatx1))
      (a12Mul_enc B hB _ _ e _ _ he h11 hatx2)
  set fy0 := a12Sub atx0 yATx
  set fy1 := a12Sub atx1 yATx
  set fy2 := a12Sub atx2 yATx
  have hfy0 : fy0.Enc B e (negInstRegret st.y (matTMulVec caiGameA st.x) 0) := a12Sub_enc B _ _ e _ _ hatx0 hyATx
  have hfy1 : fy1.Enc B e (negInstRegret st.y (matTMulVec caiGameA st.x) 1) := a12Sub_enc B _ _ e _ _ hatx1 hyATx
  have hfy2 : fy2.Enc B e (negInstRegret st.y (matTMulVec caiGameA st.x) 2) := a12Sub_enc B _ _ e _ _ hatx2 hyATx
  have hrx0' : (a12Max0 (a12Sub s.rx0 fx0)).Enc B e ((alg2Step caiGameA st).Rx 0) := a12Max0_enc B hB _ e _ he (a12Sub_enc B _ _ e _ _ h0 hfx0)
  have hrx1' : (a12Max0 (a12Sub s.rx1 fx1)).Enc B e ((alg2Step caiGameA st).Rx 1) := a12Max0_enc B hB _ e _ he (a12Sub_enc B _ _ e _ _ h1 hfx1)
  have hrx2' : (a12Max0 (a12Sub s.rx2 fx2)).Enc B e ((alg2Step caiGameA st).Rx 2) := a12Max0_enc B hB _ e _ he (a12Sub_enc B _ _ e _ _ h2 hfx2)
  have hry0' : (a12Max0 (a12Add s.ry0 fy0)).Enc B e ((alg2Step caiGameA st).Ry 0) := a12Max0_enc B hB _ e _ he (a12Add_enc B _ _ e _ _ h3 hfy0)
  have hry1' : (a12Max0 (a12Add s.ry1 fy1)).Enc B e ((alg2Step caiGameA st).Ry 1) := a12Max0_enc B hB _ e _ he (a12Add_enc B _ _ e _ _ h4 hfy1)
  have hry2' : (a12Max0 (a12Add s.ry2 fy2)).Enc B e ((alg2Step caiGameA st).Ry 2) := a12Max0_enc B hB _ e _ he (a12Add_enc B _ _ e _ _ h5 hfy2)
  exact ⟨hrx0', hrx1', hrx2', hry0', hry1', hry2',
    a12Max0_enc B hB _ e _ he (a12Sub_enc B _ _ e _ _ hrx0' hfx0),
    a12Max0_enc B hB _ e _ he (a12Sub_enc B _ _ e _ _ hrx1' hfx1),
    a12Max0_enc B hB _ e _ he (a12Sub_enc B _ _ e _ _ hrx2' hfx2),
    a12Max0_enc B hB _ e _ he (a12Add_enc B _ _ e _ _ hry0' hfy0),
    a12Max0_enc B hB _ e _ he (a12Add_enc B _ _ e _ _ hry1' hfy1),
    a12Max0_enc B hB _ e _ he (a12Add_enc B _ _ e _ _ hry2' hfy2)⟩

lemma alg2StepA12_enc (B : Nat) (hB : 0 < B) (s res : State12)
    (e : Fin 12 → ℝ) (st : RMState 3 3)
    (he : ValidEnv12 e) (hs : s.Enc B e st)
    (h : alg2StepA12 B s = some res) :
    res.Enc B e (alg2Step caiGameA st) := by
  have hpre_all := alg2PreA12_enc B hB s e st he hs
  dsimp only at hpre_all
  unfold alg2StepA12 at h
  dsimp only at h
  generalize hpre_eq : alg2PreA12 B s = pre at h hpre_all
  rcases hpre_all with ⟨hrx0', hrx1', hrx2', hry0', hry1', hry2', hpx0, hpx1, hpx2, hpy0, hpy1, hpy2⟩
  rcases hnx : normSimplexA12 B pre.px0 pre.px1 pre.px2 with _ | ⟨x0', x1', x2'⟩
  · simp [hnx] at h
  rcases hny : normSimplexA12 B pre.py0 pre.py1 pre.py2 with _ | ⟨y0', y1', y2'⟩
  · simp [hnx, hny] at h
  rw [hnx, hny] at h; dsimp only at h; rw [State12.strictB_true] at h; simp only [↓reduceIte, Option.some.injEq] at h
  let px_real := vecPosPart (fun i => (alg2Step caiGameA st).Rx i - negInstRegret st.x (matMulVec caiGameA st.y) i)
  let py_real := vecPosPart (fun j => (alg2Step caiGameA st).Ry j + negInstRegret st.y (matTMulVec caiGameA st.x) j)
  rcases normSimplexA12_enc B hB pre.px0 pre.px1 pre.px2 x0' x1' x2' e px_real he (fun i => le_max_left 0 _) hpx0 hpx1 hpx2 hnx with
    ⟨hx0', hx1', hx2'⟩
  rcases normSimplexA12_enc B hB pre.py0 pre.py1 pre.py2 y0' y1' y2' e py_real he (fun j => le_max_left 0 _) hpy0 hpy1 hpy2 hny with
    ⟨hy0', hy1', hy2'⟩
  rw [← h]
  intro ⟨iv, hiv⟩
  have hcases : iv = 0 ∨ iv = 1 ∨ iv = 2 ∨ iv = 3 ∨ iv = 4 ∨ iv = 5 ∨
                iv = 6 ∨ iv = 7 ∨ iv = 8 ∨ iv = 9 ∨ iv = 10 ∨ iv = 11 := by omega
  rcases hcases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> dsimp only [State12.get, rmStateCoord]
  · exact hrx0'
  · exact hrx1'
  · exact hrx2'
  · exact hry0'
  · exact hry1'
  · exact hry2'
  · exact hx0'
  · exact hx1'
  · exact hx2'
  · exact hy0'
  · exact hy1'
  · exact hy2'

/-! ### Unit-`L` Lohner Re-Wrapping (`rewrapWithL`) and Hint Execution -/

def sumScalePrev (B_LU : Nat) (row : List SInt) : Nat → (Nat → Aff12N) → Aff12N
  | 0, _ => a12Const sZero
  | j + 1, f =>
    let prev := sumScalePrev B_LU row j f
    let cij := row.getD j sZero
    if cij == sZero then prev
    else a12Add prev (a12ScaleFixed cij (f j) B_LU)

noncomputable def sumRealPrev (B_LU : Nat) (row : List SInt) : Nat → (Nat → ℝ) → ℝ
  | 0, _ => 0
  | j + 1, vf => sumRealPrev B_LU row j vf + ((row.getD j sZero).toReal / (B_LU : ℝ)) * vf j

lemma sumScalePrev_enc (B B_LU : Nat) (hBLU : 0 < B_LU) (row : List SInt)
    (e : Fin 12 → ℝ) (he : ValidEnv12 e)
    (f : Nat → Aff12N) (vf : Nat → ℝ) (n : Nat)
    (hf : ∀ j < n, (f j).Enc B e (vf j)) :
    (sumScalePrev B_LU row n f).Enc B e (sumRealPrev B_LU row n vf) := by
  induction n with
  | zero => exact a12Zero_enc B e
  | succ j ih =>
    unfold sumScalePrev sumRealPrev
    dsimp only
    have hprev := ih (fun k hk => hf k (Nat.lt_succ_of_lt hk))
    split_ifs with hcz
    · simp only [beq_iff_eq] at hcz
      rw [hcz, sZero_toReal, zero_div, zero_mul, add_zero]
      exact hprev
    · exact a12Add_enc B _ _ e _ _ hprev
        (a12ScaleFixed_enc B (row.getD j sZero) (f j) B_LU hBLU e (vf j) he (hf j (Nat.lt_succ_self j)))

def checkPerm12 (uToRow rowToU : List (Fin 12)) : Bool :=
  (uToRow.getD (rowToU.getD 0 0).val 0 == 0) &&
  (uToRow.getD (rowToU.getD 1 0).val 0 == 1) &&
  (uToRow.getD (rowToU.getD 2 0).val 0 == 2) &&
  (uToRow.getD (rowToU.getD 3 0).val 0 == 3) &&
  (uToRow.getD (rowToU.getD 4 0).val 0 == 4) &&
  (uToRow.getD (rowToU.getD 5 0).val 0 == 5) &&
  (uToRow.getD (rowToU.getD 6 0).val 0 == 6) &&
  (uToRow.getD (rowToU.getD 7 0).val 0 == 7) &&
  (uToRow.getD (rowToU.getD 8 0).val 0 == 8) &&
  (uToRow.getD (rowToU.getD 9 0).val 0 == 9) &&
  (uToRow.getD (rowToU.getD 10 0).val 0 == 10) &&
  (uToRow.getD (rowToU.getD 11 0).val 0 == 11)

lemma checkPerm12_spec (uToRow rowToU : List (Fin 12)) (h : checkPerm12 uToRow rowToU = true)
    (orig : Fin 12) :
    uToRow.getD (rowToU.getD orig.val 0).val 0 = orig := by
  unfold checkPerm12 at h
  simp only [Bool.and_eq_true, beq_iff_eq] at h
  rcases orig with ⟨ov, hov⟩
  have hcases : ov = 0 ∨ ov = 1 ∨ ov = 2 ∨ ov = 3 ∨ ov = 4 ∨ ov = 5 ∨
                ov = 6 ∨ ov = 7 ∨ ov = 8 ∨ ov = 9 ∨ ov = 10 ∨ ov = 11 := by omega
  rcases hcases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact h.1.1.1.1.1.1.1.1.1.1.1
  · exact h.1.1.1.1.1.1.1.1.1.1.2
  · exact h.1.1.1.1.1.1.1.1.1.2
  · exact h.1.1.1.1.1.1.1.1.2
  · exact h.1.1.1.1.1.1.1.2
  · exact h.1.1.1.1.1.1.2
  · exact h.1.1.1.1.1.2
  · exact h.1.1.1.1.2
  · exact h.1.1.1.2
  · exact h.1.1.2
  · exact h.1.2
  · exact h.2

def zeroCenter12 (x : Aff12N) : Aff12N :=
  ⟨sZero, x.a0, x.a1, x.a2, x.a3, x.a4, x.a5, x.a6, x.a7, x.a8, x.a9, x.a10, x.a11, x.err⟩

lemma zeroCenter12_enc (B : Nat) (hB : 0 < B) (x : Aff12N) (e : Fin 12 → ℝ) (v : ℝ)
    (hx : x.Enc B e v) :
    (zeroCenter12 x).Enc B e (v - x.c.toReal / (B : ℝ)) := by
  unfold Aff12N.Enc at hx ⊢
  unfold zeroCenter12
  have hBr : (B : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hB)
  have hlin :
      ({ c := sZero, a0 := x.a0, a1 := x.a1, a2 := x.a2, a3 := x.a3, a4 := x.a4,
         a5 := x.a5, a6 := x.a6, a7 := x.a7, a8 := x.a8, a9 := x.a9, a10 := x.a10,
         a11 := x.a11, err := x.err } : Aff12N).linEval e = x.linEval e := rfl
  rw [hlin]; dsimp only; rw [sZero_toReal]
  have hid : (B : ℝ) * (v - x.c.toReal / (B : ℝ)) - (0 + x.linEval e) =
      (B : ℝ) * v - (x.c.toReal + x.linEval e) := by field_simp [hBr]; ring
  rw [hid]; exact hx

def addCenter12 (c0 : SInt) (x : Aff12N) : Aff12N :=
  ⟨sAdd c0 x.c, x.a0, x.a1, x.a2, x.a3, x.a4, x.a5, x.a6, x.a7, x.a8, x.a9, x.a10, x.a11, x.err⟩

lemma addCenter12_enc (B : Nat) (hB : 0 < B) (c0 : SInt) (x : Aff12N) (e : Fin 12 → ℝ) (v : ℝ)
    (hx : x.Enc B e (v - c0.toReal / (B : ℝ))) :
    (addCenter12 c0 x).Enc B e v := by
  unfold Aff12N.Enc at hx ⊢
  unfold addCenter12
  have hBr : (B : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hB)
  have hlin :
      ({ c := sAdd c0 x.c, a0 := x.a0, a1 := x.a1, a2 := x.a2, a3 := x.a3, a4 := x.a4,
         a5 := x.a5, a6 := x.a6, a7 := x.a7, a8 := x.a8, a9 := x.a9, a10 := x.a10,
         a11 := x.a11, err := x.err } : Aff12N).linEval e = x.linEval e := rfl
  rw [hlin]; dsimp only; rw [sAdd_toReal]
  have hid : (B : ℝ) * v - (c0.toReal + x.c.toReal + x.linEval e) =
      (B : ℝ) * (v - c0.toReal / (B : ℝ)) - (x.c.toReal + x.linEval e) := by field_simp [hBr]; ring
  rw [hid]; exact hx

def solveLowerNat (B_LU : Nat) (L : List (List SInt)) (d : Nat → Aff12N) : Nat → Aff12N
  | 0 => d 0
  | i + 1 =>
    a12Sub (d (i + 1))
      (sumScalePrev B_LU (L.getD (i + 1) []) (i + 1)
        (fun j => if _ : j < i + 1 then solveLowerNat B_LU L d j else a12Const sZero))
termination_by i => i

noncomputable def solveLowerReal (B_LU : Nat) (L : List (List SInt)) (dr : Nat → ℝ) : Nat → ℝ
  | 0 => dr 0
  | i + 1 =>
    dr (i + 1) -
      sumRealPrev B_LU (L.getD (i + 1) []) (i + 1)
        (fun j => if _ : j < i + 1 then solveLowerReal B_LU L dr j else 0)
termination_by i => i

lemma solveLowerNat_enc (B B_LU : Nat) (hBLU : 0 < B_LU) (L : List (List SInt))
    (e : Fin 12 → ℝ) (he : ValidEnv12 e)
    (d : Nat → Aff12N) (dr : Nat → ℝ)
    (hd : ∀ i < 12, (d i).Enc B e (dr i)) :
    ∀ i < 12, (solveLowerNat B_LU L d i).Enc B e (solveLowerReal B_LU L dr i) := by
  intro i hi12
  induction i using Nat.strong_induction_on with
  | ind k ih =>
    cases k with
    | zero =>
      rw [solveLowerNat, solveLowerReal]
      exact hd 0 hi12
    | succ m =>
      rw [solveLowerNat, solveLowerReal]
      apply a12Sub_enc B _ _ e _ _ (hd (m + 1) hi12)
      apply sumScalePrev_enc B B_LU hBLU (L.getD (m + 1) []) e he
      intro j hj
      simp only [hj, ↓reduceDIte]
      exact ih j hj (Nat.lt_trans hj hi12)

def unpackLowerNat (B_LU : Nat) (L : List (List SInt)) (b : Nat → Aff12N) (i : Nat) : Aff12N :=
  a12Add (b i) (sumScalePrev B_LU (L.getD i []) i b)

lemma unpackLowerNat_enc (B B_LU : Nat) (hBLU : 0 < B_LU) (L : List (List SInt))
    (e' : Fin 12 → ℝ) (he' : ValidEnv12 e')
    (b : Nat → Aff12N) (dr : Nat → ℝ)
    (hb : ∀ j < 12, (b j).Enc B e' (solveLowerReal B_LU L dr j)) :
    ∀ i < 12, (unpackLowerNat B_LU L b i).Enc B e' (dr i) := by
  intro i hi12
  unfold unpackLowerNat
  cases i with
  | zero =>
    unfold sumScalePrev
    have h0 := a12Add_enc B _ _ e' _ _ (hb 0 hi12) (a12Zero_enc B e')
    rw [solveLowerReal, add_zero] at h0
    exact h0
  | succ m =>
    have hsum_eq :
        sumRealPrev B_LU (L.getD (m + 1) []) (m + 1)
          (fun j => if _ : j < m + 1 then solveLowerReal B_LU L dr j else 0) =
        sumRealPrev B_LU (L.getD (m + 1) []) (m + 1) (solveLowerReal B_LU L dr) := by
      clear hb
      have hgen : ∀ k ≤ m + 1,
          sumRealPrev B_LU (L.getD (m + 1) []) k
            (fun j => if _ : j < m + 1 then solveLowerReal B_LU L dr j else 0) =
          sumRealPrev B_LU (L.getD (m + 1) []) k (solveLowerReal B_LU L dr) := by
        intro k hk
        induction k with
        | zero => rfl
        | succ q ihq =>
          unfold sumRealPrev
          have hql : q < m + 1 := Nat.lt_of_succ_le hk
          rw [ihq (Nat.le_of_succ_le hk)]
          simp only [hql, ↓reduceDIte]
      exact hgen (m + 1) (le_refl _)
    have hsum_enc :=
      sumScalePrev_enc B B_LU hBLU (L.getD (m + 1) []) e' he' b (solveLowerReal B_LU L dr) (m + 1)
        (fun j hj => hb j (Nat.lt_trans hj hi12))
    have hadd := a12Add_enc B _ _ e' _ _ (hb (m + 1) hi12) hsum_enc
    have hid : solveLowerReal B_LU L dr (m + 1) +
        sumRealPrev B_LU (L.getD (m + 1) []) (m + 1) (solveLowerReal B_LU L dr) = dr (m + 1) := by
      rw [solveLowerReal, hsum_eq]; ring
    rwa [hid] at hadd

structure Hint12 where
  steps  : Nat
  uToRow : List (Fin 12)
  rowToU : List (Fin 12)
  L      : List (List SInt)

@[inline] def Aff12N.absBound (x : Aff12N) : Nat := sAbs x.c + x.rad

lemma Aff12N.absBound_spec (B : Nat) (x : Aff12N) (e : Fin 12 → ℝ) (v : ℝ)
    (he : ValidEnv12 e) (hx : x.Enc B e v) :
    |(B : ℝ) * v| ≤ (x.absBound : ℝ) := by
  have hb := (x.bounds_of_enc B e v he hx).1
  unfold Aff12N.absBound
  push_cast; rw [sAbs_toReal]
  have hc := le_abs_self x.c.toReal
  have hmc := neg_le_abs x.c.toReal
  rw [abs_le] at hb ⊢
  constructor <;> linarith

def rewrapWithL (B B_LU : Nat) (h : Hint12) (s : State12) : Option State12 :=
  if checkPerm12 h.uToRow h.rowToU then
    let d : Nat → Aff12N := fun i => zeroCenter12 (s.get (h.uToRow.getD i 0))
    let w0  := solveLowerNat B_LU h.L d 0
    let w1  := solveLowerNat B_LU h.L d 1
    let w2  := solveLowerNat B_LU h.L d 2
    let w3  := solveLowerNat B_LU h.L d 3
    let w4  := solveLowerNat B_LU h.L d 4
    let w5  := solveLowerNat B_LU h.L d 5
    let w6  := solveLowerNat B_LU h.L d 6
    let w7  := solveLowerNat B_LU h.L d 7
    let w8  := solveLowerNat B_LU h.L d 8
    let w9  := solveLowerNat B_LU h.L d 9
    let w10 := solveLowerNat B_LU h.L d 10
    let w11 := solveLowerNat B_LU h.L d 11
    let rFn : Fin 12 → Nat := fun j =>
      match j.val with
      | 0 => w0.absBound | 1 => w1.absBound | 2 => w2.absBound | 3 => w3.absBound
      | 4 => w4.absBound | 5 => w5.absBound | 6 => w6.absBound | 7 => w7.absBound
      | 8 => w8.absBound | 9 => w9.absBound | 10 => w10.absBound | _ => w11.absBound
    let bFn : Nat → Aff12N := fun j =>
      if hj : j < 12 then a12Basis ⟨j, hj⟩ (rFn ⟨j, hj⟩) else a12Const sZero
    let mkOrig (orig : Fin 12) : Aff12N :=
      let sOrig := s.get orig
      if isExactZero12 sOrig then a12Const sZero
      else if isExactOne12 B sOrig then a12Const (sOfNat B)
      else
        let ui := (h.rowToU.getD orig.val 0).val
        addCenter12 sOrig.c (unpackLowerNat B_LU h.L bFn ui)
    let out := State12.ofFn mkOrig
    if out.strictB then some out else none
  else none

lemma rewrapWithL_enc (B B_LU : Nat) (hB : 0 < B) (hBLU : 0 < B_LU)
    (hint : Hint12) (s res : State12) (st : RMState 3 3)
    (hex : ∃ e : Fin 12 → ℝ, ValidEnv12 e ∧ s.Enc B e st)
    (h : rewrapWithL B B_LU hint s = some res) :
    ∃ e' : Fin 12 → ℝ, ValidEnv12 e' ∧ res.Enc B e' st := by
  rcases hex with ⟨e, he, hs⟩
  unfold rewrapWithL at h
  split_ifs at h with hp
  · simp only [State12.strictB_true, ↓reduceIte, Option.some.injEq] at h
    let d : Nat → Aff12N := fun i => zeroCenter12 (s.get (hint.uToRow.getD i 0))
    let dr : Nat → ℝ := fun i =>
      let row := hint.uToRow.getD i 0
      rmStateCoord st row - (s.get row).c.toReal / (B : ℝ)
    have hd_enc : ∀ i < 12, (d i).Enc B e (dr i) := by
      intro i _
      exact zeroCenter12_enc B hB _ e _ (hs (hint.uToRow.getD i 0))
    have hw_enc := solveLowerNat_enc B B_LU hBLU hint.L e he d dr hd_enc
    let rFn : Fin 12 → Nat := fun j =>
      match j.val with
      | 0 => (solveLowerNat B_LU hint.L d 0).absBound
      | 1 => (solveLowerNat B_LU hint.L d 1).absBound
      | 2 => (solveLowerNat B_LU hint.L d 2).absBound
      | 3 => (solveLowerNat B_LU hint.L d 3).absBound
      | 4 => (solveLowerNat B_LU hint.L d 4).absBound
      | 5 => (solveLowerNat B_LU hint.L d 5).absBound
      | 6 => (solveLowerNat B_LU hint.L d 6).absBound
      | 7 => (solveLowerNat B_LU hint.L d 7).absBound
      | 8 => (solveLowerNat B_LU hint.L d 8).absBound
      | 9 => (solveLowerNat B_LU hint.L d 9).absBound
      | 10 => (solveLowerNat B_LU hint.L d 10).absBound
      | _ => (solveLowerNat B_LU hint.L d 11).absBound
    have hrFn_eq : ∀ j : Fin 12, rFn j = (solveLowerNat B_LU hint.L d j.val).absBound := by
      intro ⟨jv, hjv⟩
      have hcases : jv = 0 ∨ jv = 1 ∨ jv = 2 ∨ jv = 3 ∨ jv = 4 ∨ jv = 5 ∨
                    jv = 6 ∨ jv = 7 ∨ jv = 8 ∨ jv = 9 ∨ jv = 10 ∨ jv = 11 := by omega
      rcases hcases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> rfl
    let wReal : Fin 12 → ℝ := fun j => solveLowerReal B_LU hint.L dr j.val
    have hw_bound : ∀ j : Fin 12, |(B : ℝ) * wReal j| ≤ (rFn j : ℝ) := by
      intro j
      rw [hrFn_eq j]
      exact Aff12N.absBound_spec B _ e (wReal j) he (hw_enc j.val j.isLt)
    let e' : Fin 12 → ℝ := fun k => makeEnvCoord B (rFn k) (wReal k)
    have he' : ValidEnv12 e' := fun k => abs_makeEnvCoord_le_one B (rFn k) (wReal k) (hw_bound k)
    let bFn : Nat → Aff12N := fun j =>
      if hj : j < 12 then a12Basis ⟨j, hj⟩ (rFn ⟨j, hj⟩) else a12Const sZero
    have hb_enc : ∀ j < 12, (bFn j).Enc B e' (solveLowerReal B_LU hint.L dr j) := by
      intro j hj
      simp only [bFn, hj, ↓reduceDIte]
      exact a12Basis_enc_makeEnv B rFn wReal hw_bound ⟨j, hj⟩
    have hunpack := unpackLowerNat_enc B B_LU hBLU hint.L e' he' bFn dr hb_enc
    refine ⟨e', he', ?_⟩
    rw [← h]
    intro orig
    rw [State12.get_ofFn]
    split_ifs with hz ho
    · rw [isExactZero12_enc B hB (s.get orig) e _ he (hs orig) hz]
      exact a12Zero_enc B e'
    · rw [isExactOne12_enc B hB (s.get orig) e _ he (hs orig) ho]
      have hc1 := a12Const_enc B hB (sOfNat B) e'
      rwa [sOfNat_toReal, div_self (ne_of_gt (Nat.cast_pos.mpr hB))] at hc1
    · set ui := hint.rowToU.getD orig.val 0
      have hu_orig : hint.uToRow.getD ui.val 0 = orig := checkPerm12_spec hint.uToRow hint.rowToU hp orig
      have hun_i := hunpack ui.val ui.isLt
      have hdr_ui : dr ui.val = rmStateCoord st orig - (s.get orig).c.toReal / (B : ℝ) := by
        dsimp only [dr]; rw [hu_orig]
      rw [hdr_ui] at hun_i
      exact addCenter12_enc B hB (s.get orig).c _ e' _ hun_i

/-! ### Iterating Steps and Hints -/

noncomputable def alg2IterFrom (st : RMState 3 3) : ℕ → RMState 3 3
  | 0     => st
  | k + 1 => alg2Step caiGameA (alg2IterFrom st k)

lemma alg2IterFrom_add (st : RMState 3 3) (m n : ℕ) :
    alg2IterFrom st (m + n) = alg2IterFrom (alg2IterFrom st m) n := by
  induction n with
  | zero => rfl
  | succ k ih => simp [alg2IterFrom, ih]

lemma alg2Iter_eq_from (t m : ℕ) :
    alg2Iter caiGameA (t + m) = alg2IterFrom (alg2Iter caiGameA t) m := by
  induction m with
  | zero => rfl
  | succ k ih => simp [alg2Iter, alg2IterFrom, ih]

def iterStepsA12 (B : Nat) : Nat → State12 → Option State12
  | 0, s     => some s
  | k + 1, s =>
    match alg2StepA12 B s with
    | none    => none
    | some s1 => iterStepsA12 B k s1

lemma iterStepsA12_enc (B : Nat) (hB : 0 < B) :
    ∀ (n : Nat) (s res : State12) (e : Fin 12 → ℝ) (st : RMState 3 3),
      ValidEnv12 e → s.Enc B e st → iterStepsA12 B n s = some res →
      res.Enc B e (alg2IterFrom st n)
  | 0, s, res, _, st, _, hs, h => by
    injection h with hEq; rw [← hEq]; exact hs
  | k + 1, s, res, e, st, he, hs, h => by
    unfold iterStepsA12 at h
    rcases hs1 : alg2StepA12 B s with _ | s1
    · simp [hs1] at h
    simp only [hs1] at h
    have henc1 := alg2StepA12_enc B hB s s1 e st he hs hs1
    have hrec := iterStepsA12_enc B hB k s1 res e (alg2Step caiGameA st) he henc1 h
    have hcomm : alg2IterFrom (alg2Step caiGameA st) k = alg2IterFrom st (k + 1) := by
      have := alg2IterFrom_add st 1 k
      simpa [Nat.add_comm 1 k, alg2IterFrom] using this.symm
    rwa [hcomm] at hrec

def runHint12 (B B_LU : Nat) (h : Hint12) (s : State12) : Option State12 :=
  match iterStepsA12 B h.steps s with
  | none        => none
  | some sAfter => rewrapWithL B B_LU h sAfter

def totalHintSteps : List Hint12 → Nat
  | []      => 0
  | h :: hs => h.steps + totalHintSteps hs

def runHints12 (B B_LU : Nat) : List Hint12 → State12 → Option State12
  | [], s      => some s
  | h :: hs, s =>
    match runHint12 B B_LU h s with
    | none    => none
    | some s1 => runHints12 B B_LU hs s1

lemma runHints12_enc (B B_LU : Nat) (hB : 0 < B) (hBLU : 0 < B_LU) :
    ∀ (hs : List Hint12) (s res : State12) (st : RMState 3 3),
      (∃ e : Fin 12 → ℝ, ValidEnv12 e ∧ s.Enc B e st) →
      runHints12 B B_LU hs s = some res →
      ∃ e' : Fin 12 → ℝ, ValidEnv12 e' ∧ res.Enc B e' (alg2IterFrom st (totalHintSteps hs))
  | [], s, res, _, hex, h => by
    injection h with hEq; rw [← hEq]; exact hex
  | hint :: rest, s, res, st, hex, h => by
    unfold runHints12 runHint12 at h
    rcases hstep : iterStepsA12 B hint.steps s with _ | sAfter
    · simp [hstep] at h
    rcases hrew : rewrapWithL B B_LU hint sAfter with _ | s1
    · simp [hstep, hrew] at h
    simp only [hstep, hrew] at h
    rcases hex with ⟨e, he, hs_enc⟩
    have hAfter := iterStepsA12_enc B hB hint.steps s sAfter e st he hs_enc hstep
    have hex1 := rewrapWithL_enc B B_LU hB hBLU hint sAfter s1 (alg2IterFrom st hint.steps) ⟨e, he, hAfter⟩ hrew
    rcases runHints12_enc B B_LU hB hBLU rest s1 res (alg2IterFrom st hint.steps) hex1 h with ⟨e', he', hfinal⟩
    refine ⟨e', he', ?_⟩
    unfold totalHintSteps
    rw [alg2IterFrom_add]
    exact hfinal


/-! ### Linear-Time Memoized Kernel Evaluator `runHintsFast12` -/

@[inline] def strictId12 (x : Aff12N) : Aff12N :=
  if x.strictB then x else x

lemma strictId12_eq (x : Aff12N) : strictId12 x = x := by
  unfold strictId12; split_ifs <;> rfl

def extendFn12 (k : Nat) (wk : Aff12N) (f : Nat → Aff12N) (j : Nat) : Aff12N :=
  if j == k then wk else f j

lemma extendFn12_enc (B : Nat) (e : Fin 12 → ℝ) (vr : Nat → ℝ)
    (k : Nat) (wk : Aff12N) (f : Nat → Aff12N)
    (hf : ∀ j < k, (f j).Enc B e (vr j)) (hwk : wk.Enc B e (vr k)) :
    ∀ j < k + 1, (extendFn12 k wk f j).Enc B e (vr j) := by
  intro j hj
  unfold extendFn12
  by_cases hjk : j = k
  · subst hjk; simp [hwk]
  · have hne : (j == k) = false := beq_eq_false_iff_ne.mpr hjk
    rw [hne]
    exact hf j (by omega)

def rewrapFast12 (B B_LU : Nat) (h : Hint12) (s : State12) : Option State12 :=
  if checkPerm12 h.uToRow h.rowToU then
    let d : Nat → Aff12N := fun i => zeroCenter12 (s.get (h.uToRow.getD i 0))
    let f0  : Nat → Aff12N := fun _ => a12Const sZero
    let w0  := strictId12 (d 0)
    let f1  := extendFn12 0 w0 f0
    let w1  := strictId12 (a12Sub (d 1) (sumScalePrev B_LU (h.L.getD 1 []) 1 f1))
    let f2  := extendFn12 1 w1 f1
    let w2  := strictId12 (a12Sub (d 2) (sumScalePrev B_LU (h.L.getD 2 []) 2 f2))
    let f3  := extendFn12 2 w2 f2
    let w3  := strictId12 (a12Sub (d 3) (sumScalePrev B_LU (h.L.getD 3 []) 3 f3))
    let f4  := extendFn12 3 w3 f3
    let w4  := strictId12 (a12Sub (d 4) (sumScalePrev B_LU (h.L.getD 4 []) 4 f4))
    let f5  := extendFn12 4 w4 f4
    let w5  := strictId12 (a12Sub (d 5) (sumScalePrev B_LU (h.L.getD 5 []) 5 f5))
    let f6  := extendFn12 5 w5 f5
    let w6  := strictId12 (a12Sub (d 6) (sumScalePrev B_LU (h.L.getD 6 []) 6 f6))
    let f7  := extendFn12 6 w6 f6
    let w7  := strictId12 (a12Sub (d 7) (sumScalePrev B_LU (h.L.getD 7 []) 7 f7))
    let f8  := extendFn12 7 w7 f7
    let w8  := strictId12 (a12Sub (d 8) (sumScalePrev B_LU (h.L.getD 8 []) 8 f8))
    let f9  := extendFn12 8 w8 f8
    let w9  := strictId12 (a12Sub (d 9) (sumScalePrev B_LU (h.L.getD 9 []) 9 f9))
    let f10 := extendFn12 9 w9 f9
    let w10 := strictId12 (a12Sub (d 10) (sumScalePrev B_LU (h.L.getD 10 []) 10 f10))
    let f11 := extendFn12 10 w10 f10
    let w11 := strictId12 (a12Sub (d 11) (sumScalePrev B_LU (h.L.getD 11 []) 11 f11))
    let f12 := extendFn12 11 w11 f11
    let rFn : Fin 12 → Nat := fun j => (f12 j.val).absBound
    let bFn : Nat → Aff12N := fun j =>
      if hj : j < 12 then a12Basis ⟨j, hj⟩ (rFn ⟨j, hj⟩) else a12Const sZero
    let mkOrig (orig : Fin 12) : Aff12N :=
      let sOrig := s.get orig
      if isExactZero12 sOrig then a12Const sZero
      else if isExactOne12 B sOrig then a12Const (sOfNat B)
      else
        let ui := (h.rowToU.getD orig.val 0).val
        addCenter12 sOrig.c (unpackLowerNat B_LU h.L bFn ui)
    let out := State12.ofFn mkOrig
    if out.strictB then some out else none
  else none

lemma rewrapFast12_enc (B B_LU : Nat) (hB : 0 < B) (hBLU : 0 < B_LU)
    (hint : Hint12) (s res : State12) (st : RMState 3 3)
    (hex : ∃ e : Fin 12 → ℝ, ValidEnv12 e ∧ s.Enc B e st)
    (h : rewrapFast12 B B_LU hint s = some res) :
    ∃ e' : Fin 12 → ℝ, ValidEnv12 e' ∧ res.Enc B e' st := by
  rcases hex with ⟨e, he, hs⟩
  unfold rewrapFast12 at h
  split_ifs at h with hp
  simp only [State12.strictB_true, ↓reduceIte, Option.some.injEq] at h
  let d : Nat → Aff12N := fun i => zeroCenter12 (s.get (hint.uToRow.getD i 0))
  let dr : Nat → ℝ := fun i =>
    let row := hint.uToRow.getD i 0
    rmStateCoord st row - (s.get row).c.toReal / (B : ℝ)
  have hd_enc : ∀ i < 12, (d i).Enc B e (dr i) := fun i _ =>
    zeroCenter12_enc B hB _ e _ (hs (hint.uToRow.getD i 0))
  let vr := solveLowerReal B_LU hint.L dr
  have step_enc (m : Nat) (hm : m + 1 < 12) (f : Nat → Aff12N)
      (hf : ∀ j < m + 1, (f j).Enc B e (vr j)) :
      (strictId12 (a12Sub (d (m + 1)) (sumScalePrev B_LU (hint.L.getD (m + 1) []) (m + 1) f))).Enc B e (vr (m + 1)) := by
    dsimp only [vr]
    rw [strictId12_eq, solveLowerReal]
    apply a12Sub_enc B _ _ e _ _ (hd_enc (m + 1) hm)
    apply sumScalePrev_enc B B_LU hBLU (hint.L.getD (m + 1) []) e he
    intro j hj
    simp only [hj, ↓reduceDIte]
    exact hf j hj
  let f0  : Nat → Aff12N := fun _ => a12Const sZero
  let w0  := strictId12 (d 0)
  have hw0 : w0.Enc B e (vr 0) := by dsimp only [w0, vr]; rw [strictId12_eq, solveLowerReal]; exact hd_enc 0 (by decide)
  let f1  := extendFn12 0 w0 f0
  have hf1 := extendFn12_enc B e vr 0 w0 f0 (fun _ hj => by omega) hw0
  let w1  := strictId12 (a12Sub (d 1) (sumScalePrev B_LU (hint.L.getD 1 []) 1 f1))
  have hw1 := step_enc 0 (by decide) f1 hf1
  let f2  := extendFn12 1 w1 f1
  have hf2 := extendFn12_enc B e vr 1 w1 f1 hf1 hw1
  let w2  := strictId12 (a12Sub (d 2) (sumScalePrev B_LU (hint.L.getD 2 []) 2 f2))
  have hw2 := step_enc 1 (by decide) f2 hf2
  let f3  := extendFn12 2 w2 f2
  have hf3 := extendFn12_enc B e vr 2 w2 f2 hf2 hw2
  let w3  := strictId12 (a12Sub (d 3) (sumScalePrev B_LU (hint.L.getD 3 []) 3 f3))
  have hw3 := step_enc 2 (by decide) f3 hf3
  let f4  := extendFn12 3 w3 f3
  have hf4 := extendFn12_enc B e vr 3 w3 f3 hf3 hw3
  let w4  := strictId12 (a12Sub (d 4) (sumScalePrev B_LU (hint.L.getD 4 []) 4 f4))
  have hw4 := step_enc 3 (by decide) f4 hf4
  let f5  := extendFn12 4 w4 f4
  have hf5 := extendFn12_enc B e vr 4 w4 f4 hf4 hw4
  let w5  := strictId12 (a12Sub (d 5) (sumScalePrev B_LU (hint.L.getD 5 []) 5 f5))
  have hw5 := step_enc 4 (by decide) f5 hf5
  let f6  := extendFn12 5 w5 f5
  have hf6 := extendFn12_enc B e vr 5 w5 f5 hf5 hw5
  let w6  := strictId12 (a12Sub (d 6) (sumScalePrev B_LU (hint.L.getD 6 []) 6 f6))
  have hw6 := step_enc 5 (by decide) f6 hf6
  let f7  := extendFn12 6 w6 f6
  have hf7 := extendFn12_enc B e vr 6 w6 f6 hf6 hw6
  let w7  := strictId12 (a12Sub (d 7) (sumScalePrev B_LU (hint.L.getD 7 []) 7 f7))
  have hw7 := step_enc 6 (by decide) f7 hf7
  let f8  := extendFn12 7 w7 f7
  have hf8 := extendFn12_enc B e vr 7 w7 f7 hf7 hw7
  let w8  := strictId12 (a12Sub (d 8) (sumScalePrev B_LU (hint.L.getD 8 []) 8 f8))
  have hw8 := step_enc 7 (by decide) f8 hf8
  let f9  := extendFn12 8 w8 f8
  have hf9 := extendFn12_enc B e vr 8 w8 f8 hf8 hw8
  let w9  := strictId12 (a12Sub (d 9) (sumScalePrev B_LU (hint.L.getD 9 []) 9 f9))
  have hw9 := step_enc 8 (by decide) f9 hf9
  let f10 := extendFn12 9 w9 f9
  have hf10 := extendFn12_enc B e vr 9 w9 f9 hf9 hw9
  let w10 := strictId12 (a12Sub (d 10) (sumScalePrev B_LU (hint.L.getD 10 []) 10 f10))
  have hw10 := step_enc 9 (by decide) f10 hf10
  let f11 := extendFn12 10 w10 f10
  have hf11 := extendFn12_enc B e vr 10 w10 f10 hf10 hw10
  let w11 := strictId12 (a12Sub (d 11) (sumScalePrev B_LU (hint.L.getD 11 []) 11 f11))
  have hw11 := step_enc 10 (by decide) f11 hf11
  let f12 := extendFn12 11 w11 f11
  have hf12 := extendFn12_enc B e vr 11 w11 f11 hf11 hw11
  let rFn : Fin 12 → Nat := fun j => (f12 j.val).absBound
  let wReal : Fin 12 → ℝ := fun j => vr j.val
  have hw_bound : ∀ j : Fin 12, |(B : ℝ) * wReal j| ≤ (rFn j : ℝ) := fun j =>
    Aff12N.absBound_spec B (f12 j.val) e (wReal j) he (hf12 j.val j.isLt)
  let e' : Fin 12 → ℝ := fun k => makeEnvCoord B (rFn k) (wReal k)
  have he' : ValidEnv12 e' := fun k => abs_makeEnvCoord_le_one B (rFn k) (wReal k) (hw_bound k)
  let bFn : Nat → Aff12N := fun j =>
    if hj : j < 12 then a12Basis ⟨j, hj⟩ (rFn ⟨j, hj⟩) else a12Const sZero
  have hb_enc : ∀ j < 12, (bFn j).Enc B e' (solveLowerReal B_LU hint.L dr j) := by
    intro j hj
    simp only [bFn, hj, ↓reduceDIte]
    exact a12Basis_enc_makeEnv B rFn wReal hw_bound ⟨j, hj⟩
  have hunpack := unpackLowerNat_enc B B_LU hBLU hint.L e' he' bFn dr hb_enc
  refine ⟨e', he', ?_⟩
  rw [← h]
  intro orig
  rw [State12.get_ofFn]
  split_ifs with hz ho
  · rw [isExactZero12_enc B hB (s.get orig) e _ he (hs orig) hz]
    exact a12Zero_enc B e'
  · rw [isExactOne12_enc B hB (s.get orig) e _ he (hs orig) ho]
    have hc1 := a12Const_enc B hB (sOfNat B) e'
    rwa [sOfNat_toReal, div_self (ne_of_gt (Nat.cast_pos.mpr hB))] at hc1
  · set ui := hint.rowToU.getD orig.val 0
    have hu_orig : hint.uToRow.getD ui.val 0 = orig := checkPerm12_spec hint.uToRow hint.rowToU hp orig
    have hun_i := hunpack ui.val ui.isLt
    have hdr_ui : dr ui.val = rmStateCoord st orig - (s.get orig).c.toReal / (B : ℝ) := by
      dsimp only [dr]; rw [hu_orig]
    rw [hdr_ui] at hun_i
    exact addCenter12_enc B hB (s.get orig).c _ e' _ hun_i

def runHintFast12 (B B_LU : Nat) (h : Hint12) (s : State12) : Option State12 :=
  match iterStepsA12 B h.steps s with
  | none        => none
  | some sAfter => rewrapFast12 B B_LU h sAfter

def runHintsFast12 (B B_LU : Nat) : List Hint12 → State12 → Option State12
  | [], s      => some s
  | h :: hs, s =>
    match runHintFast12 B B_LU h s with
    | none    => none
    | some s1 => runHintsFast12 B B_LU hs s1

lemma runHintsFast12_enc (B B_LU : Nat) (hB : 0 < B) (hBLU : 0 < B_LU) :
    ∀ (hs : List Hint12) (s res : State12) (st : RMState 3 3),
      (∃ e : Fin 12 → ℝ, ValidEnv12 e ∧ s.Enc B e st) →
      runHintsFast12 B B_LU hs s = some res →
      ∃ e' : Fin 12 → ℝ, ValidEnv12 e' ∧ res.Enc B e' (alg2IterFrom st (totalHintSteps hs))
  | [], s, res, _, hex, h => by
    injection h with hEq; rw [← hEq]; exact hex
  | hint :: rest, s, res, st, hex, h => by
    unfold runHintsFast12 runHintFast12 at h
    rcases hstep : iterStepsA12 B hint.steps s with _ | sAfter
    · simp [hstep] at h
    rcases hrew : rewrapFast12 B B_LU hint sAfter with _ | s1
    · simp [hstep, hrew] at h
    simp only [hstep, hrew] at h
    rcases hex with ⟨e, he, hs_enc⟩
    have hAfter := iterStepsA12_enc B hB hint.steps s sAfter e st he hs_enc hstep
    have hex1 := rewrapFast12_enc B B_LU hB hBLU hint sAfter s1 (alg2IterFrom st hint.steps) ⟨e, he, hAfter⟩ hrew
    rcases runHintsFast12_enc B B_LU hB hBLU rest s1 res (alg2IterFrom st hint.steps) hex1 h with ⟨e', he', hfinal⟩
    refine ⟨e', he', ?_⟩
    unfold totalHintSteps
    rw [alg2IterFrom_add]
    exact hfinal

end PRMPlus
