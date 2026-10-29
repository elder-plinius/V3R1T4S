# How We Found It (`contributor text, unverified`)

> **Note:** This narrative is contributor text, unverified; only the rank file `object/w12_k4_improved.gm` (`object/w12_k4_improved.csv`) and its mechanical verification in `verify-it-yourself/` constitute the verified claim.

## 1. Diagnosing the Binary-to-DNA Tie-Breaking Seam in `GreedyMini`

In `OrensteinLab/GreedyMini` (Golan, Tziony, Kraus, Orenstein, and Shur, *Bioinformatics* 2025) and `OrensteinLab/10-minimizers` (Shur, Tziony, and Orenstein, *WABI* 2026), the 199 precomputed `.gm` minimizer orders (`w{w}_k{k}.gm`) are constructed by `ecogreed` (`code/functions.cpp`) and refined by `swapper_f` / `swapper_f_v2` (`code/swapper.cpp`).

Inspecting `code/swapper.cpp` alongside `code/density_and_gc.cpp` revealed a structural mismatch:
1. `swapper.cpp` optimizes only **binary** expected density `prob_gc(w, k, order)` (under leftmost tie-breaking) and resets all non-UHS $k$-mers to the tied sentinel rank $2^k$, never evaluating the DNA tie-breaking term `get_special_case_expected_gc` in `prob_gc_dna(w, k, order)`.
2. Under binary leftmost tie-breaking (`prob_gc`), a window where the minimum binary $k$-mer repeats at an interior position $j \in \{1,\dots,w-1\}$ and the suffix position $w$ costs **`0.0` gamechangers** (interior $j$ wins leftmost tie-break), so `swapper.cpp` treats $(j, w)$ ties as free. Under DNA tie-breaking (`prob_gc_dna`), the secondary $k$-bit DNA string breaks the tie and makes $(j, w)$ a suffix gamechanger **$\approx 50\%$ of the time**.
3. Conversely, a window where the minimum binary $k$-mer repeats at prefix position $0$ and interior position $j \in \{1,\dots,w-1\}$ costs **`1.0` gamechanger** in binary (`prob_gc`), but only **$\approx 0.5$ gamechangers** in DNA (`prob_gc_dna`).

## 2. Sum-Over-Subsets (SOS) Fast Zeta Transform for $O(1)$ DNA Tie Evaluation (`how-we-built-it/sos_dna_optimizer.cpp`)

In `GreedyMini/code/density_and_gc.cpp`, `get_special_case_expected_gc` scans all $2^{w+k}$ secondary sequences for each window-type mask `wt`, costing $O(\#\text{window\_types} \cdot 2^{w+k})$ per order evaluation. Observing that `(ruin & wt) == 0` if and only if the interior bits of `ruin` (`ruin >> 1`) are a bitwise submask of the complement of the interior bits of `wt`, a single Sum-Over-Subsets (SOS) Fast Zeta Transform pass in $O(w \cdot 2^{w-1})$ precomputes the exact integer survival counts `lut[wt]` for all $2^{w+1}$ window-type masks in milliseconds. Each leaf of `gc_dfs_dna` then resolves in a single L1-cached array lookup `lut[min_indices]`, accelerating exact `prob_gc_dna` evaluation by $>10,000\times$.

## 3. Unverified Exploratory Sweep Across 17 `(w, k)` Cells and Verified Flagship Cell `(w = 12, k = 4)`

*(Unverified exploratory remark on other cells)* Running `how-we-built-it/sos_dna_optimizer.cpp` over strict permutations of `0..2^k-1` improved 17 precomputed `.gm` cells by $\ge 0.5\%$ relative in our unverified exploratory sweep (up to `-4.274%` at $w=8, k=3$). On the verified cell $(w = 12, k = 4)$, `object/w12_k4_improved.gm` (`[15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]`, `136` bytes) lowers exact expected DNA density from `584,312,429 / 2^32 = 0.1360458389` to `573,933,439 / 2^32 = 0.1336292920` (`-1.776274%` relative).
