# Skeptic Panel Report — Role: REPRODUCE

role: REPRODUCE
context: fresh skeptic review of the packaged files only

## 1. Quoted Mathematical Definition

1. Each DNA nucleotide $c \in \{A, C, G, T\}$ is encoded as a 2-bit integer $c \in \{0, 1, 2, 3\}$, and each DNA 4-mer $x \in \{0, \dots, 255\}$ is encoded most-significant base first ($x = \sum_{i=0}^3 c_i 4^{3-i}$).
2. A 4-ary DNA minimizer order for $k = 4$ is a strict permutation `rank[0..255]` of $\{0, \dots, 255\}$, stored in `object/w12_k4_4ary.gm` as an 8-byte `size_t` length prefix (`256`) followed by `256` 8-byte `uint64_t` ranks (`2,056` bytes), and in `object/w12_k4_4ary.csv` as a 256-row CSV table (`k-mer,dna_4mer,rank`, `4,518` bytes).
3. Over all $4^{w+k} = 4^{16} = 2^{32} = 4,294,967,296$ equiprobable DNA contexts of length $w + k = 16$ ($w + 1 = 13$ consecutive DNA 4-mers $u_0, u_1, \dots, u_{12}$), a context is a **gamechanger** (transition window where the selected minimizer changes between $u_0 \dots u_{w-1}$ and $u_1 \dots u_w$ under leftmost tie-breaking for identical 4-mers) if and only if either:
   - **Prefix gamechanger:** $\text{rank}(u_0) \le \text{rank}(u_j)$ for all $j \in \{1, \dots, w\}$, or
   - **Suffix gamechanger:** $\text{rank}(u_w) < \text{rank}(u_j)$ for all $j \in \{0, \dots, w-1\}$.
4. The **expected DNA density** is the exact fraction of gamechanger contexts over all $4^{w+k} = 2^{2(w+k)}$ contexts:
   $$\text{density}(w, k, \text{rank}) = \frac{\text{GC}(w, k, \text{rank})}{4^{w+k}}.$$

## 2. Independent Verification of Witness Files and Exhaustive Counts

We verified file integrity, rank representations, and exact gamechanger counts over all $4^{16} = 4,294,967,296$ DNA contexts using two independent exact 4-ary de Bruijn dynamic programming implementations in `verify-it-yourself/verify.py` (invoked by `verify-it-yourself/run_checks.sh`, output recorded in `verify-it-yourself/RECEIPTS.md`):

### 2.1 File Hashes, Sizes, and Format Checks
| File | Size (bytes) | Verified SHA-256 | Status |
| :--- | :--- | :--- | :--- |
| `object/w12_k4_4ary.gm` | `2,056` | `956170573df55e04f43e55c20d6bba0b134c9b8054a92f995428dc9df4410ddb` | Match (`size_t` header `256` + `256` `uint64_t` ranks) |
| `object/w12_k4_4ary.csv` | `4,518` | `72557c44cc3c4b10d4735faeee9d6745f40872674c54118a311e258f775431d1` | Match (exact element-by-element agreement with `.gm`) |
| Upstream `k4-w12.txt` (`OrensteinLab/Minimizers`, recorded in `the-record-we-beat/minimizer_record_snapshot.md`) | `58` | `9a8f7447e569399a594588e695a963da59078b34cf4aac23a6fd3d998d06d877` | Match (`[3, 16, 2, 16, 16, 4, 1, 0, 16, 16, 16, 16, 16, 16, 5, 6]`) |
| Upstream `w12_k4.gm` (`OrensteinLab/10-minimizers`, recorded in `the-record-we-beat/minimizer_record_snapshot.md`) | `136` | `7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131` | Match (`[6, 1, 16, 16, 16, 16, 16, 0, 16, 2, 4, 3, 16, 16, 5, 16]`) |
| Upstream `k_extension_k16_w12.csv` (`OrensteinLab/10-minimizers`, recorded in `the-record-we-beat/minimizer_record_snapshot.md`) | `1,644` | `88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa` | Match |

### 2.2 Exhaustive Gamechanger Counts Over All $4^{16} = 4,294,967,296$ Contexts
| Order & Verification Method | Gamechanger Contexts (out of $2^{32}$) | Exact Expected DNA Density |
| :--- | :--- | :--- |
| `OrensteinLab/10-minimizers` `w12_k4.gm` (bit-plane exact & 4-ary DP) | `584,312,429` | `0.1360458389` |
| `OrensteinLab/Minimizers` `k4-w12.txt` (bit-plane exact & 4-ary DP) | `574,313,157` | `0.1337177020` |
| `object/w12_k4_4ary.gm` (Active-Set Forward/Backward 4-ary DP) | `570,244,411` (`283,110,423` pref + `287,133,988` suff) | `0.1327703733` |
| `object/w12_k4_4ary.csv` (Transition-Matrix Power 4-ary DP) | `570,244,411` | `0.1327703733` |

- **Exact Gamechanger Reduction vs. `OrensteinLab/Minimizers` (`k4-w12.txt`):** `574,313,157 - 570,244,411 = 4,068,746` fewer gamechanger contexts (**`-0.7085%` relative**, clearing the `>= 0.5%` threshold `<= 571,441,591 / 2^32 = 0.1330491135`).
- **Exact Gamechanger Reduction vs. `OrensteinLab/10-minimizers` (`w12_k4.gm`):** `584,312,429 - 570,244,411 = 14,068,018` fewer gamechanger contexts (**`-2.4076%` relative**).
- **Adversarial Corruption Checks:** Corrupting any byte or digit in either `object/w12_k4_4ary.gm` or `object/w12_k4_4ary.csv` causes `sh verify-it-yourself/run_checks.sh` to exit non-zero and print `FAIL`.

pass: true
