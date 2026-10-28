# Reproduce Skeptic Report — `myerson-vs-anonymous-reserve-gap`

context: subagent (fresh invocation)
target_id: myerson-vs-anonymous-reserve-gap
review_utc: 2026-10-28T18:25:00Z

## Reproduction Audit
1. **Calibration Verification on Published Benchmarks**:
   - Executed `attempts/lens1_rational_interval_engine/calibrate_jltx.py`.
   - JLTX 3-buyer instance (`arXiv:1804.00480`): evaluated $\text{OPT} = 2.136098$, $\text{AR}(v_1) = 1.000000$, $\text{AR}(v_2) = 1.000000$. Ratio $= 2.1361$, matching published 2.1361.
   - JLTX 4-buyer printed instance: evaluated $\text{OPT} = 2.159605$, $\text{AR}(v_1) = 1.000010$, $\text{AR}(v_2) = 1.000003$, $\text{AR}(v_3) = 0.999978$. Ratio $= 2.1596$, matching published 2.1596.

2. **Independent Verification of 5-Buyer Regular Instance**:
   - The instance consists of Buyer 0 ($\text{Tri}(\infty)$, $F_0(p) = p/(p+1)$) and 4 triangular buyers with exact rational parameters:
     - Buyer 1: $v_1 = 19309/10000 = 1.9309$, $q_1 = 2682/10000 = 0.2682$
     - Buyer 2: $v_2 = 10153/10000 = 1.0153$, $q_2 = 5344/10000 = 0.5344$
     - Buyer 3: $v_3 = 7575/10000 = 0.7575$, $q_3 = 7410/10000 = 0.7410$
     - Buyer 4: $v_4 = 6450/10000 = 129/200 = 0.6450$, $q_4 = 1/1 = 1.0000$
   - Each buyer satisfies strict regularity: virtual valuation is constant negative on $[0, v_i)$ and jumps to non-negative values at and above $v_i$.
   - Computed Myerson OPT by JLTX Lemma 1 in exact rational arithmetic:
     $$\text{OPT} = 1 + v_1 q_1 + v_2 q_2 (1 - q_1) + v_3 q_3 (1 - q_1)(1 - q_2) + v_4 q_4 (1 - q_1)(1 - q_2)(1 - q_3) = \frac{108154841521}{50000000000} \approx 2.1630968304$$
   - Verified that the second-price payment integrand $1 - \second(x)$ has exact rational partial fraction decomposition with residues $A_j = -(-c_j)^m (-c_j + C_m) / \prod_{i \ne j}(c_i - c_j)$ where $c_j = v_j q_j / (1 - q_j)$.
   - Evaluated closed-form antiderivatives across all candidate reserves $v_i$:
     - $\text{AR}(v_1) \le 0.9999829828 < 1.0$
     - $\text{AR}(v_2) \le 0.9999837967 < 1.0$
     - $\text{AR}(v_3) \le 0.9999952705 < 1.0$
     - $\text{AR}(v_4) \le 0.9998598283 < 1.0$
   - By JLTX Lemma 9, the virtual values are constant negative on $[0, v_j)$, which guarantees $\text{AR}'(p) \ge 0$ on each open interval $(v_{k+1}, v_k)$. Therefore the supremum over all $r \ge 0$ occurs at one of the candidate cutoffs $v_i$:
     $$\sup_{r \ge 0} \text{AR}(r) = \max_i \text{AR}(v_i) \le 0.9999952705 < 1.0$$
   - The certified ratio is:
     $$\frac{\text{OPT}}{\text{AR}} \ge \frac{2.1630968304}{0.9999952705} \ge 2.16310706 \ge 2.16000000$$
   - Separation margin above the 2.1600 target threshold is $+0.00310706$.
   - Executed independent standalone verifier `object/verify_certificate.py` with zero non-standard dependencies; verification passed and printed `PASS`.

pass: true
