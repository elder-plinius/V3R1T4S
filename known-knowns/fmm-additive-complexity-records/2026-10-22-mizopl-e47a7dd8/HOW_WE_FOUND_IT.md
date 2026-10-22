# How We Found It (`contributor text, unverified`)

*Note: contributor text, unverified.*

## 1. Algorithmic Discovery (`how-we-built-it/clss_cl1_tellegen_reducer.cpp`)

Our initial hypothesis (`L-FACR-001`) tested whether purely syntactic disjoint common-subexpression elimination (CSE) over pairs and triples could beat Perminov's October 19, 2026 (`048b64987b`) `addition_reduced_ZT` records. Inspecting the DAG structure of the live `048b64987b` files revealed that Perminov's `ternary_addition_reducer` already uses algebraic cancellations (`fresh_cancellations` + `el_cancellations`, where a target row $t_p$ is written as $\pm t_q \pm e_j$ even when $j \notin \operatorname{supp}(t_p)$).

To strictly surpass `ternary_addition_reducer`, we designed and implemented **`clss_cl1_tellegen_reducer.cpp`** (`24,238` bytes, `sha256: c4dbcec6ab78e5a335bb993689806e4672509c42e8e8a5f3dbe39b4629ad1c66`), combining four mechanisms:
1. **Matroid-Optimal Distance-1 Target Closure ($\text{Cl}_1$):**
   Every distinct non-unit target vector $t_p$ is pre-loaded into the dictionary. Any target $t_p$ at $L_1$ distance $1$ from another target $t_q$ ($t_p = s_1 t_q + s_2 e_j$) or equal to a binary sum of two dictionary vectors ($t_p = s_1 d_a + s_2 d_b$) is synthesized directly in `1` addition without creating a dead-end intermediate gate.
2. **Exact Residual-Reduction Lookahead & Distance-2 Stepping-Stone Cascade:**
   Each candidate binary sum $c = e_i \pm e_j$ is scored by its Distance-1 target hits (`d1_hits`), Distance-2 target hits (`d2_hits`), and exact total $L_1$ reduction $\sum_t (\|r(t)\|_1 - \|r'(t)\|_1)$ across all remaining target residuals $r(t) = t - s^* b^*(t)$. Whenever a new node brings a target $t$ to $L_1$ distance $1$, $t$ is immediately synthesized in a cascading closure loop.
3. **Tellegen Transposition Duality on $W^T$:**
   By Tellegen's transposition theorem for linear circuits, any straight-line program for $W \in \{-1, 0, +1\}^{m \times (n_1 n_3)}$ with reduced addition count $\text{cr}(W)$ transposes into an exact straight-line program for $W^T \in \{-1, 0, +1\}^{(n_1 n_3) \times m}$ with reduced addition count
   $$\text{cr}(W^T) = \text{cr}(W) + \text{nz\_rows}(W) - \text{nz\_cols}(W).$$
   Because $m \gg n_1 n_3$, running our $\text{Cl}_1$ stepping-stone synthesizer on the $m \times (n_1 n_3)$ matrix $W$ (which has $m$ rows in a small $(n_1 n_3)$-dimensional space, creating high target-closure density) and transposing via `transpose_circuit_to_gates` yields strictly smaller $c_w$ than direct synthesis on $7$ of our $9$ exact-SOTA wins (`2x4x7`, `2x5x5`, `4x6x7`, `5x5x6`, `5x6x6`, `5x6x7`, `5x7x7`).
4. **Cross-Pool Tensor Mining (`naive_addition_reduced_ZT`, `ZT`, and `serendipitous_base`):**
   Applying our $\text{Cl}_1$ + Tellegen synthesizer across all rank-equal ternary tensors in Perminov's repository yielded 48 verified `.json` schemes, including **9 distinct exact-SOTA formats** strictly beating the live minimum `cr` (`-19` on `4x5x8`, `-14` on `5x7x7`, `-11` on `2x4x7`, `-7` on `5x5x8` and `5x6x6`, `-5` on `5x5x6`, `-4` on `4x6x7` and `5x6x7`, `-2` on `2x5x5`), **2 $\mathbb{Z}_T$-best formats** (`4x4x8` and `3x3x6`), and **21 newly addition-reduced SOTA-rank $\mathbb{Z}_T$ formats**.
