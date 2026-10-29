# Skeptic Panel Report — Role: REPRODUCE

role: REPRODUCE
context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)

## 1. Quoted Mathematical Definition

Before reading `verify-it-yourself/author_checker_minimizer_check.py`, the mathematical definition of a binary-to-DNA minimizer order and its exact expected DNA density was extracted from the target specification and `OrensteinLab/GreedyMini` / `OrensteinLab/10-minimizers`:

1. Each DNA nucleotide $c \in \{A, C, G, T\}$ is encoded as a 2-bit integer $c \in \{0, 1, 2, 3\}$ (`00, 01, 10, 11`), where the high bit maps $\{A, C\} \to 0$ and $\{G, T\} \to 1$, and the low bit $e = c \bmod 2$ distinguishes within each pair.
2. A `.gm` binary-projected minimizer order for parameter $k$ is an array `order[0..2^k-1]` of $2^k$ `uint64_t` integers stored on disk as an 8-byte `size_t` length header ($2^k$) followed by $2^k$ 8-byte `uint64_t` values (`load_vector_from_file`).
3. Given a DNA $k$-mer $x \in \{0, \dots, 4^k - 1\}$ with high-bit $k$-mer $\text{bin}(x) \in \{0, \dots, 2^k - 1\}$ (read most-significant base first) and low-bit $k$-mer $\text{even}(x) \in \{0, \dots, 2^k - 1\}$, its primary rank is $\text{order}[\text{bin}(x)]$. When two $k$-mers in a window have the same primary rank, ties are broken lexicographically by the secondary bits $\text{even}(x)$ (or full $2k$-bit integer $x$).
4. Because `order = [15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]` is a strict permutation of `0..15`, two DNA 4-mers tie on primary rank if and only if $\text{bin}(x_1) = \text{bin}(x_2)$, in which case comparing full $2k$-bit integers $x_1$ vs $x_2$ and comparing secondary $k$-mers $\text{even}(x_1)$ vs $\text{even}(x_2)$ are mathematically identical.
5. Over all $4^{w+k} = 4^{16} = 2^{32} = 4,294,967,296$ equiprobable DNA contexts of length $w + k = 16$ ($w + 1 = 13$ consecutive 4-mers $x_0, x_1, \dots, x_{12}$), a context is a **gamechanger** (transition window where the selected minimizer changes between window $x_0 \dots x_{w-1}$ and window $x_1 \dots x_w$, under leftmost tie-breaking for identical DNA 4-mers) if and only if either:
   - **Prefix gamechanger:** $\text{rank}(x_0) \le \text{rank}(x_j)$ for all $j \in \{1, \dots, w\}$, or
   - **Suffix gamechanger:** $\text{rank}(x_w) \lt \text{rank}(x_j)$ for all $j \in \{0, \dots, w-1\}$.
6. The **expected DNA density** is the exact fraction of gamechanger contexts among all $4^{w+k} = 2^{2(w+k)}$ DNA contexts of length $w+k$:
   $$\text{density\_expected\_dna}(w, k, \text{order}) = \frac{\text{prob\_gc\_dna}(w, k, \text{order})}{2^{2(w+k)}}.$$

---

## 2. Independent Verification Written Prior to Reading Author Code

From the quoted definition alone, we implemented three independent exact algorithms prior to reading `verify-it-yourself/author_checker_minimizer_check.py`:
1. **`brute_force_gc_dna(w, k, order)`:** Naive cartesian-product enumeration over all $4^{w+k}$ DNA sequences for small $(w, k)$, extracting the $w+1$ consecutive DNA $k$-mers and testing the prefix and suffix gamechanger inequalities directly.
2. **`bitplane_exact_gc_dna(w, k, order)`:** Exact enumeration over all $2^{w+k} = 65,536$ high-bit binary strings $B \in \{0, 1\}^{w+k}$ and all $2^{w+k} = 65,536$ low-bit binary strings $E \in \{0, 1\}^{w+k}$. For each $B$, it identifies the subset mask $M(B) \subseteq \{0, \dots, w\}$ of positions achieving $\min_{0 \le j \le w} \text{order}[b_j]$; for each active mask $M(B)$ containing position $0$ or $w$, it counts how many $E \in \{0, \dots, 65535\}$ satisfy $e_0 \le e_j$ ($\forall j \in M(B) \setminus \{0\}$) or $e_w \lt e_j$ ($\forall j \in M(B) \setminus \{w\}$).
3. **`dp_4ary_exact_gc_dna(w, k, order, tie_mode)`:** Direct 4-ary de Bruijn graph dynamic programming over steps $j = 0, 1, \dots, w$, tracking the state `(running_min_rank, x0_is_running_min, suffix_3mer)` across all $4^{w+k}$ DNA strings without decomposing into $(B, E)$, implemented for both `tie_mode = "even"` (secondary-bit tie-breaking) and `tie_mode = "full"` (full $2k$-bit integer tie-breaking).

### 2.1 Small-Case Brute-Force & Negative Self-Tests

Running our independent checker executed the following self-tests (completed in `0.147s` on Run 1, `0.150s` on Run 2):
- **Small case `(w=2, k=2)` ($4^4 = 256$ DNA windows of length 4):**
  - `order = [0, 1, 2, 3]`: `brute_force == bitplane == dp_4ary == 184 / 256 (0.718750)`
  - `order = [3, 1, 0, 2]`: `brute_force == bitplane == dp_4ary == 168 / 256 (0.656250)`
  - `order = [1, 0, 1, 2]` (with tied primary ranks): `brute_force == bitplane == dp_4ary == 170 / 256 (0.664062)`
  - `order = [4, 4, 0, 1]` (with sentinel ties): `brute_force == bitplane == dp_4ary == 170 / 256 (0.664062)`
- **Small case `(w=3, k=2)` ($4^5 = 1,024$ DNA windows of length 5):**
  - `order = [2, 0, 3, 1]`: `brute_force == bitplane == dp_4ary == 498 / 1024 (0.486328)`
- **Negative / Corrupted Tests:**
  - **Corrupted `.gm` byte length (`24` bytes instead of `136` bytes):** Properly rejected with `ValueError`.
  - **Perturbed CSV vs `.gm` rank vector (`13` and `5` swapped at indices `14` and `15`):** Detected mismatch against `object/w12_k4_improved.gm` and evaluated to `573,976,207 / 2^32 = 0.1336392497` (worse by `+42,768` gamechanger windows than `573,933,439`).
  - **Degraded lexicographical permutation `[0, 1, ..., 15]` at `(w=12, k=4)`:** Evaluated to `819,391,145 / 2^32 = 0.1907793677`, strictly worse than the baseline `0.1360458389`.

---

## 3. Independent Verification of Witness Files and Exhaustive Counts

We ran the independent checker twice consecutively to verify file integrity, rank representations, exact gamechanger counts over all $4^{16} = 4,294,967,296$ DNA contexts, and determinism:

### 3.1 File Hashes, Sizes, and Format Checks
| File | Size (bytes) | Verified SHA-256 | Status |
| :--- | :--- | :--- | :--- |
| `object/w12_k4_improved.gm` | `136` | `537faa127958cbb7f10b0e90c8832449b375b2fad8360bfd4c7e596eee187bc4` | Match (`size_t` header `16` + `16` `uint64_t` ranks) |
| `object/w12_k4_improved.csv` | `129` | `e542885cc0668c8fa166514faccbba226ccaa833fc352df9d5b17aaf2537078b` | Match (exact agreement with `.gm` vector) |
| Upstream `w12_k4.gm` (snapshot in `the-record-we-beat/minimizer_record_snapshot.md`) | `136` | `7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131` | Match (`size_t` header `16` + `16` `uint64_t` ranks) |
| Upstream `k_extension_k16_w12.csv` (snapshot in `the-record-we-beat/minimizer_record_snapshot.md`) | `1,644` | `88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa` | Match |

- **Decoded rank vector from `object/w12_k4_improved.gm` and `object/w12_k4_improved.csv`:**
  `[15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]` (strict permutation of `0..15`).
- **Decoded rank vector from upstream `w12_k4.gm`:**
  `[6, 1, 16, 16, 16, 16, 16, 0, 16, 2, 4, 3, 16, 16, 5, 16]`.

### 3.2 Exhaustive Gamechanger Counts and Determinism Across Two Runs
| Target Order & Method | Gamechanger Windows (out of $2^{32} = 4,294,967,296$) | Exact Expected DNA Density | Run 1 Time | Run 2 Time |
| :--- | :--- | :--- | :--- | :--- |
| Upstream `w12_k4.gm` (bit-plane exact) | `584,312,429` | `0.1360458389` | `2.529s` | `2.515s` |
| Upstream `w12_k4.gm` (4-ary DP, secondary-bit tie) | `584,312,429` | `0.1360458389` | `0.050s` | `0.049s` |
| Upstream `w12_k4.gm` (4-ary DP, full-integer tie) | `584,312,429` | `0.1360458389` | `0.056s` | `0.057s` |
| `object/w12_k4_improved.gm` (bit-plane exact) | `573,933,439` | `0.1336292920` | `2.365s` | `2.367s` |
| `object/w12_k4_improved.gm` (4-ary DP, secondary-bit tie) | `573,933,439` | `0.1336292920` | `0.053s` | `0.053s` |
| `object/w12_k4_improved.gm` (4-ary DP, full-integer tie) | `573,933,439` | `0.1336292920` | `0.054s` | `0.053s` |

- **Exact Gamechanger Difference:** `584,312,429 - 573,933,439 = 10,378,990` fewer gamechanger contexts out of $4^{16} = 4,294,967,296$.
- **Exact Absolute Density Reduction:** `-0.0024165469` (`0.1336292920` vs `0.1360458389`).
- **Exact Relative Density Reduction:** **`-1.776274%`** vs upstream `w12_k4.gm` (`0.1360458389`) and **`-1.776390%`** vs the smallest listed value in `k_extension_k16_w12.csv` (`GreedyMini = 0.136046`), exceeding the required `0.5%` relative threshold by `3.55x`.

---

## 4. Verification of Package Checker (`verify-it-yourself/run_checks.sh` & `verify-it-yourself/author_checker_minimizer_check.py`)

After completing the independent checker and its two runs, we inspected and executed `verify-it-yourself/run_checks.sh` (which runs `verify-it-yourself/author_checker_minimizer_check.py`, output saved in `verify-it-yourself/RECEIPTS.md`):

- `Published w12_k4.gm (bit-plane exact)        : 584312429 / 2^32 = 0.1360458389`
- `Improved  w12_k4_improved.gm (bit-plane)     : 573933439 / 2^32 = 0.1336292920`
- `Improved  w12_k4_improved.gm (4-ary DP)      : 573933439 / 2^32 = 0.1336292920`
- `Relative reduction      : -1.776274% (required >= 0.500000%)`
- `VERIFICATION: PASS`

All independent and package verifications agree to the exact integer (`573,933,439` vs `584,312,429` over $2^{32}$ contexts).

pass: true
