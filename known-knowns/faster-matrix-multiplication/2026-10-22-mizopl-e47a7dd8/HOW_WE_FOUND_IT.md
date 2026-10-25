# How We Found It (`contributor text, unverified`)

*Note: contributor text, unverified.*

## 1. Algorithmic Discovery (`how-we-built-it/clss_cl1_tellegen_reducer.cpp`)

Our initial hypothesis (`L-FACR-001`) tested whether purely syntactic disjoint common-subexpression elimination (CSE) over pairs and triples could beat Perminov's October 19, 2026 (`048b64987b`) `addition_reduced_ZT` records. Inspecting the DAG structure of the live `048b64987b` files revealed that Perminov's `ternary_addition_reducer` already uses algebraic cancellations (`fresh_cancellations` + `el_cancellations`, where a target row $t_p$ is written as $\pm t_q \pm e_j$ even when $j \notin \operatorname{supp}(t_p)$).

To synthesize strictly smaller straight-line programs on exact-SOTA-rank ternary tensors, we designed and implemented **`how-we-built-it/clss_cl1_tellegen_reducer.cpp`** (`24,238` bytes, `sha256: c4dbcec6ab78e5a335bb993689806e4672509c42e8e8a5f3dbe39b4629ad1c66`), combining four mechanisms:
1. **Matroid-Optimal Distance-1 Target Closure ($\text{Cl}_1$):**
   Every distinct non-unit target vector $t_p$ is pre-loaded into the dictionary. Any target $t_p$ at $L_1$ distance $1$ from another target $t_q$ ($t_p = s_1 t_q + s_2 e_j$) or equal to a binary sum of two dictionary vectors ($t_p = s_1 d_a + s_2 d_b$) is synthesized directly in `1` addition without creating a dead-end intermediate gate.
2. **Exact Residual-Reduction Lookahead & Distance-2 Stepping-Stone Cascade:**
   Each candidate binary sum $c = e_i \pm e_j$ is scored by its Distance-1 target hits (`d1_hits`), Distance-2 target hits (`d2_hits`), and exact total $L_1$ reduction $\sum_t (\|r(t)\|_1 - \|r'(t)\|_1)$ across all remaining target residuals $r(t) = t - s^* b^*(t)$. Whenever a new node brings a target $t$ to $L_1$ distance $1$, $t$ is immediately synthesized in a cascading closure loop.
3. **Tellegen Transposition Duality on $W^T$:**
   By Tellegen's transposition theorem for linear circuits, any straight-line program for $W \in \{-1, 0, +1\}^{m \times (n_1 n_3)}$ with reduced addition count $\text{cr}(W)$ transposes into an exact straight-line program for $W^T \in \{-1, 0, +1\}^{(n_1 n_3) \times m}$ with reduced addition count
   $$\text{cr}(W^T) = \text{cr}(W) + \text{nz\_rows}(W) - \text{nz\_cols}(W).$$
   Because $m \gg n_1 n_3$, running our $\text{Cl}_1$ stepping-stone synthesizer on the $m \times (n_1 n_3)$ matrix $W$ (which has $m$ rows in a small $(n_1 n_3)$-dimensional space, creating high target-closure density) and transposing via `transpose_circuit_to_gates` yields strictly smaller $c_w$ than direct synthesis on `5x6x6` ($m = 130$, where $c_w = 225$).
4. **Source Tensors Credited (`dronperminov/FastMatrixMultiplication`):**
   Applying `how-we-built-it/clss_cl1_tellegen_reducer.cpp` to four unreduced/naive ternary source schemes from Alexander Perminov's (`@dronperminov`) `FastMatrixMultiplication` repository produced the 4 verified ternary straight-line programs in `object/schemes/`:
   - `schemes/results/ZT/3x3x7_m49_ZT.json` (`sha256: 52147707b318e29596e6faf0d66102911dd9e3f86d9bd0094b0e6b1896070fff`) $\to$ `object/schemes/3x3x7_m49_cr167_cn404_ZT_reduced.json` (`cr = 167`, `cu = 33, cv = 53, cw = 81`, `cn = 404`)
   - `schemes/results/ZT/3x5x6_m68_ZT.json` (`sha256: 9675decf7533fae8ac643c4cf6fccff63f9ef76f41fc781888a7b806cd6e8cac`) $\to$ `object/schemes/3x5x6_m68_cr245_cn494_ZT_reduced.json` (`cr = 245`, `cu = 56, cv = 78, cw = 111`, `cn = 494`)
   - `schemes/results/ZT/3x5x7_m79_ZT.json` (`sha256: 9f94da6729e900a0ee525b97935d03d35306159626459768a553abf852cff0c6`) $\to$ `object/schemes/3x5x7_m79_cr294_cn520_ZT_reduced.json` (`cr = 294`, `cu = 66, cv = 97, cw = 131`, `cn = 520`)
   - `schemes/results/naive_addition_reduced_ZT/5x6x6_m130_c1697_ZT.json` (`sha256: 125bdb24d3c3303130fc9be98c98f9421ddd197b27894dada481a8d23ab4b0c7`) $\to$ `object/schemes/5x6x6_m130_cr492_cn1697_ZT_reduced.json` (`cr = 492`, `cu = 128, cv = 139, cw = 225`, `cn = 1697`).
