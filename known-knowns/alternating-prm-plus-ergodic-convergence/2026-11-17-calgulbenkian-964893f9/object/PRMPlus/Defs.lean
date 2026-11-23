import Mathlib.Topology.Order.Real
import Mathlib.Topology.Order.LiminfLimsup
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# Regret Matching⁺ and Predictive Regret Matching⁺ in Matrix Games

Formal definitions of Regret Matching⁺ (Algorithm 1), Predictive Regret Matching⁺ (Algorithm 2),
Alternating Regret Matching⁺ (Algorithm 7), and Alternating Predictive Regret Matching⁺
(Algorithm 8), together with the 3×3 counterexample game `A = [[3,0,-3],[0,3,-4],[0,0,1]]`,
matching Cai, Farina, Grand-Clément, Kroer, Lee, Luo, and Zheng (*Last-Iterate Convergence
Properties of Regret-Matching Algorithms in Games*, ICLR 2025, `arXiv:2311.00676v2`),
Section 2 (`preliminaries.tex`), Section 3 (`small_counterexamples.tex`), and Appendix A
(`appendix.tex`).
-/

namespace PRMPlus

open scoped BigOperators

/-- The probability simplex `Δ^d = { x ∈ ℝ^d_+ | ⟨x, 1_d⟩ = 1 }`. -/
def Simplex (d : ℕ) (x : Fin d → ℝ) : Prop :=
  (∀ i : Fin d, 0 ≤ x i) ∧ (∑ i : Fin d, x i) = 1

/-- Componentwise positive part `[v]^+ = max(0, v)`. -/
def vecPosPart {d : ℕ} (v : Fin d → ℝ) : Fin d → ℝ :=
  fun i => max 0 (v i)

/-- `ℓ₁`-norm `‖z‖₁ = ∑_i |z_i|`. -/
def l1Norm {d : ℕ} (z : Fin d → ℝ) : ℝ :=
  ∑ i : Fin d, |z i|

/-- Simplex normalization `z / ‖z‖₁` with the paper's convention `0 / 0 = (1/d) 1_d`
(`preliminaries.tex`, lines 3 and 16). -/
noncomputable def normalize {d : ℕ} (z : Fin d → ℝ) : Fin d → ℝ :=
  if l1Norm z = 0 then fun _ => (1 : ℝ) / (d : ℝ)
  else fun i => z i / l1Norm z

/-- Joint normalization operator `g(z₁, z₂) = (z₁ / ‖z₁‖₁, z₂ / ‖z₂‖₁)` (`preliminaries.tex`, Eq. 2). -/
noncomputable def opG {d₁ d₂ : ℕ} (z₁ : Fin d₁ → ℝ) (z₂ : Fin d₂ → ℝ) :
    (Fin d₁ → ℝ) × (Fin d₂ → ℝ) :=
  (normalize z₁, normalize z₂)

/-- Matrix-vector product `(A y)_i = ∑_j A_{i,j} y_j`. -/
def matMulVec {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ) (y : Fin d₂ → ℝ) : Fin d₁ → ℝ :=
  fun i => ∑ j : Fin d₂, A i j * y j

/-- Transposed matrix-vector product `(Aᵀ x)_j = ∑_i A_{i,j} x_i`. -/
def matTMulVec {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ) (x : Fin d₁ → ℝ) : Fin d₂ → ℝ :=
  fun j => ∑ i : Fin d₁, A i j * x i

/-- Bilinear payoff `xᵀ A y = ∑_i ∑_j x_i A_{i,j} y_j`. -/
def bilinearPayoff {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ)
    (x : Fin d₁ → ℝ) (y : Fin d₂ → ℝ) : ℝ :=
  ∑ i : Fin d₁, x i * matMulVec A y i

/-- Negative instantaneous regret vector `f(x, ℓ) = ℓ - (xᵀ ℓ) 1_d` (`preliminaries.tex`, line 14). -/
def negInstRegret {d : ℕ} (x ℓ : Fin d → ℝ) : Fin d → ℝ :=
  let dot := ∑ j : Fin d, x j * ℓ j
  fun i => ℓ i - dot

/-- Variational duality gap `DualGap(x, y) = max_{y' ∈ Δ^{d₂}} xᵀ A y' - min_{x' ∈ Δ^{d₁}} x'ᵀ A y`
(`preliminaries.tex`, line 10). -/
noncomputable def DualGap {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ)
    (x : Fin d₁ → ℝ) (y : Fin d₂ → ℝ) : ℝ :=
  sSup { v : ℝ | ∃ y' : Fin d₂ → ℝ, Simplex d₂ y' ∧ v = bilinearPayoff A x y' } -
  sInf { v : ℝ | ∃ x' : Fin d₁ → ℝ, Simplex d₁ x' ∧ v = bilinearPayoff A x' y }

/-- Joint state `(R_x^t, R_y^t, x^t, y^t)` of self-play RM⁺ / PRM⁺ algorithms. -/
structure RMState (d₁ d₂ : ℕ) where
  Rx : Fin d₁ → ℝ
  Ry : Fin d₂ → ℝ
  x  : Fin d₁ → ℝ
  y  : Fin d₂ → ℝ

/-- Standard initialization `R^0 = 0` and uniform strategies `x^0 = (1/d₁) 1`, `y^0 = (1/d₂) 1`. -/
noncomputable def initState (d₁ d₂ : ℕ) : RMState d₁ d₂ :=
  { Rx := fun _ => 0
    Ry := fun _ => 0
    x  := fun _ => (1 : ℝ) / (d₁ : ℝ)
    y  := fun _ => (1 : ℝ) / (d₂ : ℝ) }

/-- **Algorithm 1** of `arXiv:2311.00676v2`: Simultaneous Regret Matching⁺ (RM⁺). -/
noncomputable def alg1Step {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ) (s : RMState d₁ d₂) :
    RMState d₁ d₂ :=
  let fx := negInstRegret s.x (matMulVec A s.y)
  let fy := negInstRegret s.y (matTMulVec A s.x)
  let Rx' := vecPosPart (fun i => s.Rx i - fx i)
  let Ry' := vecPosPart (fun j => s.Ry j + fy j)
  let xy' := opG Rx' Ry'
  { Rx := Rx', Ry := Ry', x := xy'.1, y := xy'.2 }

/-- **Algorithm 2** of `arXiv:2311.00676v2`: Simultaneous Predictive Regret Matching⁺ (PRM⁺). -/
noncomputable def alg2Step {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ) (s : RMState d₁ d₂) :
    RMState d₁ d₂ :=
  let fx := negInstRegret s.x (matMulVec A s.y)
  let fy := negInstRegret s.y (matTMulVec A s.x)
  let Rx' := vecPosPart (fun i => s.Rx i - fx i)
  let Ry' := vecPosPart (fun j => s.Ry j + fy j)
  let px := vecPosPart (fun i => Rx' i - fx i)
  let py := vecPosPart (fun j => Ry' j + fy j)
  let xy' := opG px py
  { Rx := Rx', Ry := Ry', x := xy'.1, y := xy'.2 }

/-- **Algorithm 7** of `arXiv:2311.00676v2`: Alternating Regret Matching⁺ (alt. RM⁺). -/
noncomputable def alg7Step {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ) (s : RMState d₁ d₂) :
    RMState d₁ d₂ :=
  let fx := negInstRegret s.x (matMulVec A s.y)
  let Rx' := vecPosPart (fun i => s.Rx i - fx i)
  let x' := normalize Rx'
  let fy := negInstRegret s.y (matTMulVec A x')
  let Ry' := vecPosPart (fun j => s.Ry j + fy j)
  let y' := normalize Ry'
  { Rx := Rx', Ry := Ry', x := x', y := y' }

/-- **Algorithm 8** of `arXiv:2311.00676v2`: Alternating Predictive Regret Matching⁺ (alt. PRM⁺). -/
noncomputable def alg8Step {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ) (s : RMState d₁ d₂) :
    RMState d₁ d₂ :=
  let fx := negInstRegret s.x (matMulVec A s.y)
  let Rx' := vecPosPart (fun i => s.Rx i - fx i)
  let x' := normalize (vecPosPart (fun i => Rx' i - fx i))
  let fy := negInstRegret s.y (matTMulVec A x')
  let Ry' := vecPosPart (fun j => s.Ry j + fy j)
  let y' := normalize (vecPosPart (fun j => Ry' j + fy j))
  { Rx := Rx', Ry := Ry', x := x', y := y' }

/-- Trajectory `(R_x^t, R_y^t, x^t, y^t)` of Algorithm 2 (Simultaneous PRM⁺) from `R = 0` and uniform strategies. -/
noncomputable def alg2Iter {d₁ d₂ : ℕ} (A : Fin d₁ → Fin d₂ → ℝ) : ℕ → RMState d₁ d₂
  | 0     => initState d₁ d₂
  | t + 1 => alg2Step A (alg2Iter A t)

/-- Cai et al.'s 3×3 game matrix `A = [[3, 0, -3], [0, 3, -4], [0, 0, 1]]`
(`small_counterexamples.tex`, Section 3). -/
def caiGameA : Fin 3 → Fin 3 → ℝ
  | 0, 0 =>  3 | 0, 1 => 0 | 0, 2 => -3
  | 1, 0 =>  0 | 1, 1 => 3 | 1, 2 => -4
  | 2, 0 =>  0 | 2, 1 => 0 | 2, 2 =>  1

/-! ### Basic Simplex, Normalization, and Duality Gap Lemmas on `Fin 3` -/

lemma univ_fin3 : (Finset.univ : Finset (Fin 3)) = {0, 1, 2} := by decide

lemma sum_fin3 (f : Fin 3 → ℝ) : (∑ i : Fin 3, f i) = f 0 + f 1 + f 2 := by
  rw [univ_fin3]
  have h01 : (0 : Fin 3) ∉ ({1, 2} : Finset (Fin 3)) := by decide
  have h12 : (1 : Fin 3) ∉ ({2} : Finset (Fin 3)) := by decide
  rw [Finset.sum_insert h01, Finset.sum_insert h12, Finset.sum_singleton]
  ring

lemma l1Norm_eq_sum_of_nonneg (z : Fin 3 → ℝ) (hz : ∀ i, 0 ≤ z i) :
    l1Norm z = z 0 + z 1 + z 2 := by
  unfold l1Norm
  rw [sum_fin3, abs_of_nonneg (hz 0), abs_of_nonneg (hz 1), abs_of_nonneg (hz 2)]

lemma normalize_fin3_of_pos (z : Fin 3 → ℝ) (hz : ∀ i, 0 ≤ z i)
    (hpos : 0 < z 0 + z 1 + z 2) :
    normalize z = fun i => z i / (z 0 + z 1 + z 2) := by
  unfold normalize
  rw [l1Norm_eq_sum_of_nonneg z hz]
  simp [ne_of_gt hpos]

lemma simplex_normalize_vecPosPart (v : Fin 3 → ℝ) :
    Simplex 3 (normalize (vecPosPart v)) := by
  have hz : ∀ i : Fin 3, 0 ≤ vecPosPart v i := fun i => le_max_left 0 (v i)
  have hz0 := hz 0; have hz1 := hz 1; have hz2 := hz 2
  unfold normalize
  rw [l1Norm_eq_sum_of_nonneg _ hz]
  split_ifs with h0
  · refine ⟨fun _ => by norm_num, ?_⟩
    rw [sum_fin3]
    norm_num
  · have hpos : 0 < vecPosPart v 0 + vecPosPart v 1 + vecPosPart v 2 :=
      lt_of_le_of_ne (by linarith) (Ne.symm h0)
    refine ⟨fun i => div_nonneg (hz i) (le_of_lt hpos), ?_⟩
    rw [sum_fin3]
    have hsum_eq :
        vecPosPart v 0 / (vecPosPart v 0 + vecPosPart v 1 + vecPosPart v 2) +
        vecPosPart v 1 / (vecPosPart v 0 + vecPosPart v 1 + vecPosPart v 2) +
        vecPosPart v 2 / (vecPosPart v 0 + vecPosPart v 1 + vecPosPart v 2) =
        (vecPosPart v 0 + vecPosPart v 1 + vecPosPart v 2) /
          (vecPosPart v 0 + vecPosPart v 1 + vecPosPart v 2) := by ring
    rw [hsum_eq]
    exact div_self (ne_of_gt hpos)

lemma alg2Iter_simplex (t : ℕ) :
    Simplex 3 (alg2Iter caiGameA t).x ∧ Simplex 3 (alg2Iter caiGameA t).y := by
  cases t with
  | zero =>
    unfold alg2Iter initState Simplex
    constructor <;> · refine ⟨fun _ => by norm_num, ?_⟩; rw [sum_fin3]; norm_num
  | succ k =>
    exact ⟨simplex_normalize_vecPosPart _, simplex_normalize_vecPosPart _⟩

lemma matMulVec_caiGameA (y : Fin 3 → ℝ) :
    matMulVec caiGameA y 0 = 3 * y 0 - 3 * y 2 ∧
    matMulVec caiGameA y 1 = 3 * y 1 - 4 * y 2 ∧
    matMulVec caiGameA y 2 = y 2 := by
  unfold matMulVec
  refine ⟨?_, ?_, ?_⟩ <;> · rw [sum_fin3]; unfold caiGameA; ring

lemma matTMulVec_caiGameA (x : Fin 3 → ℝ) :
    matTMulVec caiGameA x 0 = 3 * x 0 ∧
    matTMulVec caiGameA x 1 = 3 * x 1 ∧
    matTMulVec caiGameA x 2 = -3 * x 0 - 4 * x 1 + x 2 := by
  unfold matTMulVec
  refine ⟨?_, ?_, ?_⟩ <;> · rw [sum_fin3]; unfold caiGameA; ring

lemma bilinearPayoff_eq_dot_AT (x y : Fin 3 → ℝ) :
    bilinearPayoff caiGameA x y = ∑ j : Fin 3, y j * matTMulVec caiGameA x j := by
  unfold bilinearPayoff
  rw [sum_fin3, sum_fin3]
  rcases matMulVec_caiGameA y with ⟨hm0, hm1, hm2⟩
  rcases matTMulVec_caiGameA x with ⟨ht0, ht1, ht2⟩
  rw [hm0, hm1, hm2, ht0, ht1, ht2]
  ring

def stdBasis3 (k : Fin 3) : Fin 3 → ℝ := fun i => if i = k then 1 else 0

lemma simplex_stdBasis3 (k : Fin 3) : Simplex 3 (stdBasis3 k) := by
  unfold Simplex stdBasis3
  refine ⟨fun i => by split_ifs <;> norm_num, ?_⟩
  rw [sum_fin3]
  rcases k with ⟨kv, hkv⟩
  have hcases : kv = 0 ∨ kv = 1 ∨ kv = 2 := by omega
  rcases hcases with rfl | rfl | rfl <;> simp [Fin.ext_iff]

lemma caiGameA_payoff_abs_le (x y : Fin 3 → ℝ) (hx : Simplex 3 x) (hy : Simplex 3 y) :
    -12 ≤ bilinearPayoff caiGameA x y ∧ bilinearPayoff caiGameA x y ≤ 12 := by
  rcases hx with ⟨hx0, hx1⟩
  rcases hy with ⟨hy0, hy1⟩
  rw [sum_fin3] at hx1 hy1
  have hx00 := hx0 0; have hx01 := hx0 1; have hx02 := hx0 2
  have hy00 := hy0 0; have hy01 := hy0 1; have hy02 := hy0 2
  unfold bilinearPayoff
  rw [sum_fin3]
  rcases matMulVec_caiGameA y with ⟨hm0, hm1, hm2⟩
  rw [hm0, hm1, hm2]
  constructor <;> nlinarith

/-- Witness-free pure-action lower bound on `DualGap caiGameA x y`. -/
lemma caiGameA_dualGap_ge (x y : Fin 3 → ℝ) (hx : Simplex 3 x) (hy : Simplex 3 y)
    (i₀ j₀ : Fin 3) :
    matTMulVec caiGameA x j₀ - matMulVec caiGameA y i₀ ≤ DualGap caiGameA x y := by
  unfold DualGap
  have h_bdd_sup : BddAbove { v : ℝ | ∃ y' : Fin 3 → ℝ, Simplex 3 y' ∧ v = bilinearPayoff caiGameA x y' } := by
    refine ⟨12, ?_⟩
    rintro v ⟨y', hy', rfl⟩
    exact (caiGameA_payoff_abs_le x y' hx hy').2
  have h_mem_sup : matTMulVec caiGameA x j₀ ∈
      { v : ℝ | ∃ y' : Fin 3 → ℝ, Simplex 3 y' ∧ v = bilinearPayoff caiGameA x y' } := by
    refine ⟨stdBasis3 j₀, simplex_stdBasis3 j₀, ?_⟩
    rw [bilinearPayoff_eq_dot_AT, sum_fin3]
    unfold stdBasis3
    rcases j₀ with ⟨jv, hjv⟩
    have hcases : jv = 0 ∨ jv = 1 ∨ jv = 2 := by omega
    rcases hcases with rfl | rfl | rfl <;> simp [Fin.ext_iff]
  have h_bdd_inf : BddBelow { v : ℝ | ∃ x' : Fin 3 → ℝ, Simplex 3 x' ∧ v = bilinearPayoff caiGameA x' y } := by
    refine ⟨-12, ?_⟩
    rintro v ⟨x', hx', rfl⟩
    exact (caiGameA_payoff_abs_le x' y hx' hy).1
  have h_mem_inf : matMulVec caiGameA y i₀ ∈
      { v : ℝ | ∃ x' : Fin 3 → ℝ, Simplex 3 x' ∧ v = bilinearPayoff caiGameA x' y } := by
    refine ⟨stdBasis3 i₀, simplex_stdBasis3 i₀, ?_⟩
    unfold bilinearPayoff stdBasis3
    rw [sum_fin3]
    rcases i₀ with ⟨iv, hiv⟩
    have hcases : iv = 0 ∨ iv = 1 ∨ iv = 2 := by omega
    rcases hcases with rfl | rfl | rfl <;> simp [Fin.ext_iff]
  have h1 := le_csSup h_bdd_sup h_mem_sup
  have h2 := csInf_le h_bdd_inf h_mem_inf
  linarith

/-- Global upper bound `DualGap caiGameA x y ≤ 24` on `Δ³ × Δ³`. -/
lemma caiGameA_dualGap_le (x y : Fin 3 → ℝ) (hx : Simplex 3 x) (hy : Simplex 3 y) :
    DualGap caiGameA x y ≤ 24 := by
  unfold DualGap
  have h_nonempty_sup : { v : ℝ | ∃ y' : Fin 3 → ℝ, Simplex 3 y' ∧ v = bilinearPayoff caiGameA x y' }.Nonempty :=
    ⟨bilinearPayoff caiGameA x (stdBasis3 0), stdBasis3 0, simplex_stdBasis3 0, rfl⟩
  have h_sup_le : sSup { v : ℝ | ∃ y' : Fin 3 → ℝ, Simplex 3 y' ∧ v = bilinearPayoff caiGameA x y' } ≤ 12 := by
    apply csSup_le h_nonempty_sup
    rintro v ⟨y', hy', rfl⟩
    exact (caiGameA_payoff_abs_le x y' hx hy').2
  have h_nonempty_inf : { v : ℝ | ∃ x' : Fin 3 → ℝ, Simplex 3 x' ∧ v = bilinearPayoff caiGameA x' y }.Nonempty :=
    ⟨bilinearPayoff caiGameA (stdBasis3 0) y, stdBasis3 0, simplex_stdBasis3 0, rfl⟩
  have h_inf_ge : -12 ≤ sInf { v : ℝ | ∃ x' : Fin 3 → ℝ, Simplex 3 x' ∧ v = bilinearPayoff caiGameA x' y } := by
    apply le_csInf h_nonempty_inf
    rintro v ⟨x', hx', rfl⟩
    exact (caiGameA_payoff_abs_le x' y hx' hy).1
  linarith

/-- Bridge from eventual pointwise lower bound `∀ t ≥ T₀, δ ≤ DualGap ...` to `δ ≤ Filter.liminf ... atTop`. -/
lemma liminf_alg2_dualGap_ge (T₀ : ℕ) (δ : ℝ)
    (hev : ∀ t : ℕ, T₀ ≤ t → δ ≤ DualGap caiGameA (alg2Iter caiGameA t).x (alg2Iter caiGameA t).y) :
    δ ≤ Filter.liminf (fun t : ℕ => DualGap caiGameA (alg2Iter caiGameA t).x (alg2Iter caiGameA t).y) Filter.atTop := by
  apply Filter.le_liminf_of_le
  · refine Filter.isCoboundedUnder_ge_of_le Filter.atTop (x := (24 : ℝ)) (fun t => ?_)
    have hxy := alg2Iter_simplex t
    exact caiGameA_dualGap_le _ _ hxy.1 hxy.2
  · rw [Filter.eventually_atTop]
    exact ⟨T₀, hev⟩

end PRMPlus
