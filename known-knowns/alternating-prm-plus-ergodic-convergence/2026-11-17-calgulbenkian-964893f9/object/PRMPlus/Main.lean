import Mathlib.Topology.Instances.Real.Lemmas
import PRMPlus.Reach01
import PRMPlus.Reach02
import PRMPlus.Reach03
import PRMPlus.Reach04
import PRMPlus.Reach05
import PRMPlus.Reach06
import PRMPlus.Reach07
import PRMPlus.Reach08
import PRMPlus.Reach09
import PRMPlus.Reach10
import PRMPlus.Reach11
import PRMPlus.Reach12
import PRMPlus.Reach13
import PRMPlus.Reach14
import PRMPlus.Reach15
import PRMPlus.Reach16
import PRMPlus.Reach17
import PRMPlus.Reach18
import PRMPlus.Reach19
import PRMPlus.Reach20
import PRMPlus.Reach21
import PRMPlus.Reach22
import PRMPlus.Reach23
import PRMPlus.Reach24
import PRMPlus.Reach25
import PRMPlus.Reach26
import PRMPlus.Reach27
import PRMPlus.Reach28
import PRMPlus.Reach29
import PRMPlus.Reach30
import PRMPlus.Reach31
import PRMPlus.Reach32
import PRMPlus.Reach33
import PRMPlus.Reach34
import PRMPlus.Reach35
import PRMPlus.Reach36
import PRMPlus.Reach37
import PRMPlus.Reach38
import PRMPlus.Reach39
import PRMPlus.Reach40
import PRMPlus.Reach41
import PRMPlus.Reach42
import PRMPlus.Reach43
import PRMPlus.Reach44
import PRMPlus.Reach45
import PRMPlus.Reach46
import PRMPlus.Reach47
import PRMPlus.Reach48
import PRMPlus.Tube01
import PRMPlus.Tube02
import PRMPlus.Tube03
import PRMPlus.Tube04
import PRMPlus.Tube05
import PRMPlus.Tube06
import PRMPlus.Tube07
import PRMPlus.Tube08
import PRMPlus.Tube09
import PRMPlus.Tube10
import PRMPlus.Tube11
import PRMPlus.Tube12
import PRMPlus.Tube13
import PRMPlus.Tube14
import PRMPlus.Tube15
import PRMPlus.Tube16
import PRMPlus.Tube17
import PRMPlus.Tube18
import PRMPlus.Tube19
import PRMPlus.Tube20
import PRMPlus.Tube21
import PRMPlus.Tube22
import PRMPlus.Tube23
import PRMPlus.Tube24
import PRMPlus.Tube25
import PRMPlus.Tube26
import PRMPlus.Tube27
import PRMPlus.Tube28
import PRMPlus.Tube29
import PRMPlus.Tube30
import PRMPlus.Tube31
import PRMPlus.Tube32
import PRMPlus.Tube33
import PRMPlus.Tube34
import PRMPlus.Tube35
import PRMPlus.Tube36
import PRMPlus.Tube37
import PRMPlus.Tube38
import PRMPlus.Tube39
import PRMPlus.Tube40
import PRMPlus.Tube41
import PRMPlus.Tube42
import PRMPlus.Tube43
import PRMPlus.Tube44
import PRMPlus.Tube45
import PRMPlus.Tube46
import PRMPlus.Tube47
import PRMPlus.Tube48
import PRMPlus.Tube49
import PRMPlus.Tube50
import PRMPlus.Tube51
import PRMPlus.Tube52
import PRMPlus.Tube53
import PRMPlus.Tube54
import PRMPlus.Tube55
import PRMPlus.Tube56
import PRMPlus.Tube57
import PRMPlus.Tube58
import PRMPlus.Tube59
import PRMPlus.Tube60
import PRMPlus.Tube61
import PRMPlus.Tube62
import PRMPlus.Tube63
import PRMPlus.Tube64

/-!
# Main Theorems: Last-Iterate Non-Convergence of Simultaneous Predictive RM⁺ (Algorithm 2)

Machine-checked proof in Lean 4 (using only standard axioms `[propext, Classical.choice, Quot.sound]`,
with zero `sorry` and zero `native_decide`) that Simultaneous Predictive Regret Matching⁺
(Algorithm 2 of Cai et al., ICLR 2025, `arXiv:2311.00676v2`), initialized at `R = 0` and uniform
strategies `(1/3, 1/3, 1/3)`, does not converge in the last iterate on the 3×3 matrix game
`A = [[3, 0, -3], [0, 3, -4], [0, 0, 1]]`: for every iteration `t ≥ 13203`,
`DualGap A x^t y^t ≥ 1/20`, hence `liminf_{t → ∞} DualGap A x^t y^t ≥ 1/20 > 0`.
-/

namespace PRMPlus

lemma reach_iter1000 : ∃ e : Fin 12 → ℝ, ValidEnv12 e ∧ ckpt_04.Enc B_nat e (alg2Iter caiGameA 1000) :=
  reach_04 (reach_03 (reach_02 (reach_01 reach_00)))

lemma reach_iter13203 : ∃ e : Fin 12 → ℝ, ValidEnv12 e ∧ ckpt_48.Enc B_nat e (alg2Iter caiGameA 13203) :=
  reach_48 (reach_47 (reach_46 (reach_45 (reach_44 (reach_43 (reach_42 (reach_41 (reach_40 (reach_39 (reach_38 (reach_37 (reach_36 (reach_35 (reach_34 (reach_33 (reach_32 (reach_31 (reach_30 (reach_29 (reach_28 (reach_27 (reach_26 (reach_25 (reach_24 (reach_23 (reach_22 (reach_21 (reach_20 (reach_19 (reach_18 (reach_17 (reach_16 (reach_15 (reach_14 (reach_13 (reach_12 (reach_11 (reach_10 (reach_09 (reach_08 (reach_07 (reach_06 (reach_05 reach_iter1000)))))))))))))))))))))))))))))))))))))))))))

lemma entry_iter13203 : checkT0InTube tubeParams ckpt_48 = true := by decide +kernel

lemma all_256_slabs : ∀ k < 256, checkSlab tubeParams k = true := by
  intro k hk
  if h_1_64 : k < 128 then
    if h_1_32 : k < 64 then
      if h_1_16 : k < 32 then
        if h_1_8 : k < 16 then
          if h_1_4 : k < 8 then
            if h_1_2 : k < 4 then
              exact tube_slabs_01 k (by omega) (by omega)
            else
              exact tube_slabs_02 k (by omega) (by omega)
          else
            if h_3_4 : k < 12 then
              exact tube_slabs_03 k (by omega) (by omega)
            else
              exact tube_slabs_04 k (by omega) (by omega)
        else
          if h_5_8 : k < 24 then
            if h_5_6 : k < 20 then
              exact tube_slabs_05 k (by omega) (by omega)
            else
              exact tube_slabs_06 k (by omega) (by omega)
          else
            if h_7_8 : k < 28 then
              exact tube_slabs_07 k (by omega) (by omega)
            else
              exact tube_slabs_08 k (by omega) (by omega)
      else
        if h_9_16 : k < 48 then
          if h_9_12 : k < 40 then
            if h_9_10 : k < 36 then
              exact tube_slabs_09 k (by omega) (by omega)
            else
              exact tube_slabs_10 k (by omega) (by omega)
          else
            if h_11_12 : k < 44 then
              exact tube_slabs_11 k (by omega) (by omega)
            else
              exact tube_slabs_12 k (by omega) (by omega)
        else
          if h_13_16 : k < 56 then
            if h_13_14 : k < 52 then
              exact tube_slabs_13 k (by omega) (by omega)
            else
              exact tube_slabs_14 k (by omega) (by omega)
          else
            if h_15_16 : k < 60 then
              exact tube_slabs_15 k (by omega) (by omega)
            else
              exact tube_slabs_16 k (by omega) (by omega)
    else
      if h_17_32 : k < 96 then
        if h_17_24 : k < 80 then
          if h_17_20 : k < 72 then
            if h_17_18 : k < 68 then
              exact tube_slabs_17 k (by omega) (by omega)
            else
              exact tube_slabs_18 k (by omega) (by omega)
          else
            if h_19_20 : k < 76 then
              exact tube_slabs_19 k (by omega) (by omega)
            else
              exact tube_slabs_20 k (by omega) (by omega)
        else
          if h_21_24 : k < 88 then
            if h_21_22 : k < 84 then
              exact tube_slabs_21 k (by omega) (by omega)
            else
              exact tube_slabs_22 k (by omega) (by omega)
          else
            if h_23_24 : k < 92 then
              exact tube_slabs_23 k (by omega) (by omega)
            else
              exact tube_slabs_24 k (by omega) (by omega)
      else
        if h_25_32 : k < 112 then
          if h_25_28 : k < 104 then
            if h_25_26 : k < 100 then
              exact tube_slabs_25 k (by omega) (by omega)
            else
              exact tube_slabs_26 k (by omega) (by omega)
          else
            if h_27_28 : k < 108 then
              exact tube_slabs_27 k (by omega) (by omega)
            else
              exact tube_slabs_28 k (by omega) (by omega)
        else
          if h_29_32 : k < 120 then
            if h_29_30 : k < 116 then
              exact tube_slabs_29 k (by omega) (by omega)
            else
              exact tube_slabs_30 k (by omega) (by omega)
          else
            if h_31_32 : k < 124 then
              exact tube_slabs_31 k (by omega) (by omega)
            else
              exact tube_slabs_32 k (by omega) (by omega)
  else
    if h_33_64 : k < 192 then
      if h_33_48 : k < 160 then
        if h_33_40 : k < 144 then
          if h_33_36 : k < 136 then
            if h_33_34 : k < 132 then
              exact tube_slabs_33 k (by omega) (by omega)
            else
              exact tube_slabs_34 k (by omega) (by omega)
          else
            if h_35_36 : k < 140 then
              exact tube_slabs_35 k (by omega) (by omega)
            else
              exact tube_slabs_36 k (by omega) (by omega)
        else
          if h_37_40 : k < 152 then
            if h_37_38 : k < 148 then
              exact tube_slabs_37 k (by omega) (by omega)
            else
              exact tube_slabs_38 k (by omega) (by omega)
          else
            if h_39_40 : k < 156 then
              exact tube_slabs_39 k (by omega) (by omega)
            else
              exact tube_slabs_40 k (by omega) (by omega)
      else
        if h_41_48 : k < 176 then
          if h_41_44 : k < 168 then
            if h_41_42 : k < 164 then
              exact tube_slabs_41 k (by omega) (by omega)
            else
              exact tube_slabs_42 k (by omega) (by omega)
          else
            if h_43_44 : k < 172 then
              exact tube_slabs_43 k (by omega) (by omega)
            else
              exact tube_slabs_44 k (by omega) (by omega)
        else
          if h_45_48 : k < 184 then
            if h_45_46 : k < 180 then
              exact tube_slabs_45 k (by omega) (by omega)
            else
              exact tube_slabs_46 k (by omega) (by omega)
          else
            if h_47_48 : k < 188 then
              exact tube_slabs_47 k (by omega) (by omega)
            else
              exact tube_slabs_48 k (by omega) (by omega)
    else
      if h_49_64 : k < 224 then
        if h_49_56 : k < 208 then
          if h_49_52 : k < 200 then
            if h_49_50 : k < 196 then
              exact tube_slabs_49 k (by omega) (by omega)
            else
              exact tube_slabs_50 k (by omega) (by omega)
          else
            if h_51_52 : k < 204 then
              exact tube_slabs_51 k (by omega) (by omega)
            else
              exact tube_slabs_52 k (by omega) (by omega)
        else
          if h_53_56 : k < 216 then
            if h_53_54 : k < 212 then
              exact tube_slabs_53 k (by omega) (by omega)
            else
              exact tube_slabs_54 k (by omega) (by omega)
          else
            if h_55_56 : k < 220 then
              exact tube_slabs_55 k (by omega) (by omega)
            else
              exact tube_slabs_56 k (by omega) (by omega)
      else
        if h_57_64 : k < 240 then
          if h_57_60 : k < 232 then
            if h_57_58 : k < 228 then
              exact tube_slabs_57 k (by omega) (by omega)
            else
              exact tube_slabs_58 k (by omega) (by omega)
          else
            if h_59_60 : k < 236 then
              exact tube_slabs_59 k (by omega) (by omega)
            else
              exact tube_slabs_60 k (by omega) (by omega)
        else
          if h_61_64 : k < 248 then
            if h_61_62 : k < 244 then
              exact tube_slabs_61 k (by omega) (by omega)
            else
              exact tube_slabs_62 k (by omega) (by omega)
          else
            if h_63_64 : k < 252 then
              exact tube_slabs_63 k (by omega) (by omega)
            else
              exact tube_slabs_64 k (by omega) (by omega)

/-- **Theorem 1 (Eventual Pointwise Duality Gap Lower Bound):**
For every iteration `t ≥ 13203` of Simultaneous Predictive RM⁺ (Algorithm 2) from `R = 0` and
uniform strategies on `caiGameA`, the duality gap of `(x^t, y^t)` is at least `1/20`. -/
theorem alg2_caiGame_eventual_dualityGap_ge :
    ∀ t : ℕ, 13203 ≤ t →
      (1 : ℝ) / 20 ≤ DualGap caiGameA (alg2Iter caiGameA t).x (alg2Iter caiGameA t).y :=
  eventual_dualityGap_of_tube tubeParams tubeParams_valid all_256_slabs 13203 ckpt_48
    reach_iter13203 entry_iter13203

/-- **Theorem 2 (Positive Asymptotic Liminf of the Duality Gap — Partial Progress `p2`):**
Simultaneous Predictive RM⁺ (Algorithm 2) has strictly positive `liminf` duality gap on `caiGameA`. -/
theorem alg2_caiGame_liminf_dualityGap_pos :
    0 < Filter.liminf (fun t : ℕ => DualGap caiGameA (alg2Iter caiGameA t).x (alg2Iter caiGameA t).y) Filter.atTop := by
  have hle : (1 : ℝ) / 20 ≤ Filter.liminf
      (fun t : ℕ => DualGap caiGameA (alg2Iter caiGameA t).x (alg2Iter caiGameA t).y) Filter.atTop :=
    liminf_alg2_dualGap_ge 13203 ((1 : ℝ) / 20) alg2_caiGame_eventual_dualityGap_ge
  linarith

/-- **Theorem 3 (Last-Iterate Non-Convergence of Simultaneous Predictive RM⁺):**
The duality gap along the last-iterate trajectory `(x^t, y^t)` does not converge to `0`. -/
theorem alg2_caiGame_not_tendsto_zero :
    ¬ Filter.Tendsto (fun t : ℕ => DualGap caiGameA (alg2Iter caiGameA t).x (alg2Iter caiGameA t).y)
        Filter.atTop (nhds 0) := by
  intro h
  have hev : ∀ᶠ t : ℕ in Filter.atTop,
      DualGap caiGameA (alg2Iter caiGameA t).x (alg2Iter caiGameA t).y < (1 : ℝ) / 20 :=
    h.eventually (gt_mem_nhds (by norm_num))
  rw [Filter.eventually_atTop] at hev
  rcases hev with ⟨N, hN⟩
  have hlt := hN (max N 13203) (le_max_left N 13203)
  have hge := alg2_caiGame_eventual_dualityGap_ge (max N 13203) (le_max_right N 13203)
  linarith

lemma coord_bounds_of_enc12 (s : State12) (st : RMState 3 3) (idx : Fin 12) (loN hiN : Nat)
    (hex : ∃ e : Fin 12 → ℝ, ValidEnv12 e ∧ s.Enc B_nat e st)
    (hlo : sNonneg (sSub (s.get idx).lo (sOfNat loN)) = true)
    (hhi : sNonneg (sSub (sOfNat hiN) (s.get idx).hi) = true) :
    (loN : ℝ) / (B_nat : ℝ) ≤ rmStateCoord st idx ∧
    rmStateCoord st idx ≤ (hiN : ℝ) / (B_nat : ℝ) := by
  have hBr_pos : (0 : ℝ) < (B_nat : ℝ) := Nat.cast_pos.mpr B_nat_pos
  rcases hex with ⟨e, he, hs⟩
  rcases (s.get idx).bounds_of_enc B_nat e (rmStateCoord st idx) he (hs idx) with ⟨_, hb_lo, hb_hi⟩
  have h1 := sNonneg_spec _ hlo; rw [sSub_toReal, sOfNat_toReal] at h1
  have h2 := sNonneg_spec _ hhi; rw [sSub_toReal, sOfNat_toReal] at h2
  exact ⟨(div_le_iff₀ hBr_pos).mpr (by linarith), (le_div_iff₀ hBr_pos).mpr (by linarith)⟩

/-- **Theorem 4 (Kernel-Verified Iteration-1000 Strategy Bounds):**
Explicit rational interval bounds (width `< 10⁻¹²`) on `(x^1000, y^1000)` for independent
floating-point / arbitrary-precision cross-validation of the formal dynamics. -/
theorem alg2_caiGame_iter1000_bounds :
    ((6952364039090924642008615 : ℝ) / (B_nat : ℝ) ≤ (alg2Iter caiGameA 1000).x 0 ∧ (alg2Iter caiGameA 1000).x 0 ≤ (6952364039091115236711365 : ℝ) / (B_nat : ℝ)) ∧
    ((6672723298608839783575868 : ℝ) / (B_nat : ℝ) ≤ (alg2Iter caiGameA 1000).x 1 ∧ (alg2Iter caiGameA 1000).x 1 ≤ (6672723298608986135326508 : ℝ) / (B_nat : ℝ)) ∧
    ((58910461839177659027200214 : ℝ) / (B_nat : ℝ) ≤ (alg2Iter caiGameA 1000).x 2 ∧ (alg2Iter caiGameA 1000).x 2 ≤ (58910461839177976139918546 : ℝ) / (B_nat : ℝ)) ∧
    ((20355789547417786300043889 : ℝ) / (B_nat : ℝ) ≤ (alg2Iter caiGameA 1000).y 0 ∧ (alg2Iter caiGameA 1000).y 0 ≤ (20355789547417906371312525 : ℝ) / (B_nat : ℝ)) ∧
    ((26120265866226286103894723 : ℝ) / (B_nat : ℝ) ≤ (alg2Iter caiGameA 1000).y 1 ∧ (alg2Iter caiGameA 1000).y 1 ≤ (26120265866226368681150485 : ℝ) / (B_nat : ℝ)) ∧
    ((26059493763233478939264068 : ℝ) / (B_nat : ℝ) ≤ (alg2Iter caiGameA 1000).y 2 ∧ (alg2Iter caiGameA 1000).y 2 ≤ (26059493763233674569075426 : ℝ) / (B_nat : ℝ)) :=
  ⟨coord_bounds_of_enc12 ckpt_04 _ 6  6952364039090924642008615 6952364039091115236711365 reach_iter1000 (by decide +kernel) (by decide +kernel),
   coord_bounds_of_enc12 ckpt_04 _ 7  6672723298608839783575868 6672723298608986135326508 reach_iter1000 (by decide +kernel) (by decide +kernel),
   coord_bounds_of_enc12 ckpt_04 _ 8  58910461839177659027200214 58910461839177976139918546 reach_iter1000 (by decide +kernel) (by decide +kernel),
   coord_bounds_of_enc12 ckpt_04 _ 9  20355789547417786300043889 20355789547417906371312525 reach_iter1000 (by decide +kernel) (by decide +kernel),
   coord_bounds_of_enc12 ckpt_04 _ 10 26120265866226286103894723 26120265866226368681150485 reach_iter1000 (by decide +kernel) (by decide +kernel),
   coord_bounds_of_enc12 ckpt_04 _ 11 26059493763233478939264068 26059493763233674569075426 reach_iter1000 (by decide +kernel) (by decide +kernel)⟩

end PRMPlus
