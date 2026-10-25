# How We Found It (`contributor text, unverified`)

*Note: contributor text, unverified.*

## 1. Open-Source Engine: `we*` (`https://github.com/mizopl/we-star`, Law `M7`)

All experiments were executed single-threaded on a **16 GB M1 MacBook Air** (`35 minutes` total end-to-end session wall-clock time) using our open-source **`we*` (`we-star`)** methodology (`https://github.com/mizopl/we-star`, **Law `M7`: Interface Gauge Freedom & Solution-Fiber Scan**).

In two-stage non-Clifford gate synthesis (`circuit -> cubic phase tensor T -> Stage-1 CP decomposition -> Stage-2 TOHPE + FastTODD Waring reduction`), the upstream `ZIB-IOL/polytof` pipeline stores a single canonical CP decomposition per tensor in `data/paper/cpd/topp/*.npy` and inside `tohpe()` (`src/waring/todd.h`) extracts only a single pivot column from the $\mathbb{F}_2$-nullspace (`kernel()`). By **Law `M7`**, the Stage-1 CP decomposition of a symmetric cubic tensor $T$ (and the local 7-to-6 TOHPE nullspace reduction of each Toffoli triple) has a massive internal gauge fiber under which Stage-1 Toffoli count is invariant (`CP = 30` for `0732` $\mathrm{GF}(2^9)$, `CP = 33` for `0733` $\mathrm{GF}(2^{10})$), but the downstream Stage-2 `FastTODD` Waring rank varies by $8$ to $12$ $T$-gates.

## 2. Two-Stage Law `M7` Fiber Scan & Single-Thread Runtimes

1. **Stage-1 4-Symmetry Gauge Fiber (`how-we-built-it/hunt_gf_4sym_m7.py` & `generate_m7_gf_fiber.py`):**
   - Starting from the optimal bilinear multiplication decompositions of $\mathrm{GF}(2^9)$ ($r = 30$) and $\mathrm{GF}(2^{10})$ ($r = 33$), we generated distinct minimal-rank symmetric cubic CP decompositions in `07xx` coordinates via:
     - $\mathbb{F}_{2^k}$-linear automorphisms and invertible field multipliers $(\lambda, \mu, (\lambda\mu)^{-1}) \in (\mathbb{F}_{2^k}^\times)^3$ (`(511)^2` and `(1023)^2` exact bilinear-preserving gauges),
     - Frobenius automorphisms $x \mapsto x^{2^s}$,
     - factor triple permutations, and
     - rank-preserving flip-graph plateau walks (`--fgs`).
2. **Stage-2 Full-Nullspace `tohpe()` (`kernel_all`) + `FastTODD`:**
   - Upgrading `tohpe()` to scan all basis vectors $z_a$ and pairwise XOR combinations $z_a \oplus z_b$ of $\ker_{\mathbb{F}_2}(P)$ for each triple pair reduced the post-TOHPE starting rank on `0732` from `179` to `169` before a single step of TODD ran.
   - Running single-thread `FastTODD` across the Law `M7` CP fiber found **`0732-00139.npy` (`139` $T$-gates, `-8` vs `docs/tensors.md` `147`) in `0.17 s` single-thread CPU time** (`0.221 s` mean per scheme; `0 / 139` row overlap with `arXiv:2603.29894`'s LLM-evolutionary scheme), and **`0733-00161.npy` (`161` $T$-gates, `-12` vs `docs/tensors.md` `173`) in `1.42 s` single-thread CPU time**.
3. **Complete 88-Tensor `p3` Audit, `4` Repaired Schemes, and `7` `p2` Optimality Proofs:**
   - Auditing all 88 tensors in `data/paper/` uncovered 5 posted Waring rank discrepancies (`0105`, `0108`, `0115`, `0817`, `0728`) and 2 qubit-dimension discrepancies (`0108`, `0114`). Multi-seed `FastTODD` (`how-we-built-it/hunt_all_benchmarks.py`) repaired all 4 circuit discrepancies (`0105-00039.npy`, `0108-00073.npy`, `0115-00051.npy`, `0817-00059.npy`), and mode-1 flattening $\mathbb{F}_2$-rank + exhaustive subset/pair checks certified optimality (`p2`) for 7 benchmark rows in `< 0.15 s` single-thread CPU time.
