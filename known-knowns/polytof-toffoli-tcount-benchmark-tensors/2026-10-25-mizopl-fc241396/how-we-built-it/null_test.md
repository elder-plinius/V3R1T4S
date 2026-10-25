# Null Test & Calibration Gate (`null_test.md`) — `polytof-toffoli-tcount-benchmark-tensors`

- **Run ID:** `2026-10-25-1935`
- **Target ID:** `polytof-toffoli-tcount-benchmark-tensors`
- controls: 400
- best_control: 539 symmetric triple Hamming distance on 0732 (mean 630.06 +- 29.87, 0/400 exact matches; deterministic single-scheme baseline Waring = 147 on 0732 and 173 on 0733)
- real: 0 symmetric triple Hamming distance at Waring = 139 on 0732 (-8 vs table 147) and Waring = 161 on 0733 (-12 vs table 173), plus 4 repaired posted schemes (0105 41->39, 0108 77->73, 0115 55->51, 0817 63->59) and 7 p2 optimality certificates
- real_beats_all_controls: yes
- command: python3 claim/verify.py

## 1. Calibration & Negative Controls (Law `M5`)

1. **Exact Calibration on `ZIB-IOL/polytof` Reference Suite (`88` Tensors):**
   - Independent zero-dependency verification of all 88 `data/paper/transform/*.npy`, `data/paper/cpd/topp/*.npy`, and `data/paper/waring/*.npy` files against `data/tensors/*.npy`:
     - All `88 / 88` CP files and `88 / 88` Waring files satisfy exact cubic monomial equality `upper_triples(T_rec) == upper_triples(T_ref)` over $\mathbb{F}_2$.
     - Reproduces exact optimal $T$-count `17` on `0725` ($\mathrm{GF}(2^2)$ multiplication) and `7` on `0812`/`0112` (`Mod 5_4`).
2. **Corrupted-Object Negative Control:**
   - Perturbing any single bit in any factor vector $(u_t, v_t, w_t)$ of a claimed CP decomposition or any single bit in a parity vector $a_t$ of a claimed Waring decomposition causes `upper_triples(T_rec) != upper_triples(T_ref)` and is immediately rejected (`PASS` $\to$ `FAIL`) by `verify.py`.
3. **400-Sample Naive Single-Path Control (`M5` Null Distribution):**
   - On `0732` ($\mathrm{GF}(2^9)$ multiplication, $n=27$) and `0733` ($\mathrm{GF}(2^{10})$ multiplication, $n=30$), 400 random variable-order / standard-basis greedy decompositions without `M7` Stage-1 CP fiber diversity yield strictly higher Waring counts than our `M7` fiber-optimized schemes.
