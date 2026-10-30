context: isolated Antigravity subagent 2c016a51-8957-4d4d-abe3-067d0cb6ef92 (V3R1T4S Skeptic REPRODUCE)
target_id: polytof-toffoli-tcount-benchmark-tensors
run_id: 2026-10-25-1935

# Adversarial Skeptic Report: `REPRODUCE`

- **Run ID:** `2026-10-25-1935`
- **Target ID:** `polytof-toffoli-tcount-benchmark-tensors`
- **Skeptic Role:** `REPRODUCE` (Independent Bit-Exact Reproduction of the `p3` Audit of `data/paper/` and the `4` Repaired Waring Schemes)
- **Timestamp (UTC):** `2026-10-25T19:49:00Z` (Updated `2026-10-30` for `p3`-only package split `2026-10-25-mizopl-7162c3e8`)

---

## 1. Executive Summary

I independently executed `sh verify-it-yourself/run_checks.sh` (`verify-it-yourself/verify.py`) against the pinned upstream repository `ZIB-IOL/polytof` (`commit 0dcac107d15adc34dc646242d222f21ae7d32699`, `docs/tensors.md` SHA-256 `f83839d0589888d75fb0ac357f8e251bc3f743d5c1749757cb51beec26676dc3`).

Every audited decomposition file across `data/paper/` (`185` files total: `88` `cpd/topp` with `13,528` stored CP schemes, `9` `cpd/base` bilinear files, and `88` `waring` files), every identified discrepancy (`5` Waring rank discrepancies and `2` qubit-dimension discrepancies), and all `4` shipped repaired Waring schemes (`object/waring/0105-00039.npy`, `object/waring/0108-00073.npy`, `object/waring/0115-00051.npy`, `object/waring/0817-00059.npy`) reproduced from scratch with **zero discrepancies**:

1. **Complete `data/paper/` Decomposition Audit (`185` Files, `13,537` CP Schemes + `88` Waring Schemes):**
   - `data/paper/transform/*.npy`: `88 / 88` binary matrices verified invertible over $\mathbb{F}_2$.
   - `data/paper/cpd/topp/*.npy`: `88 / 88` files verified across all **`13,528` stored CP schemes** (`74` single-row files + `14` multi-row pool files containing `13 x 1,000 + 454 = 13,454` schemes); `13,528 / 13,528` reconstruct their exact BCO-transformed cubic tensors on $i < j < k$, and `88 / 88` decoded ranks match both the filename and `docs/tensors.md`.
   - `data/paper/cpd/base/*.npy`: `9 / 9` bilinear $\mathrm{GF}(2^k)$ multiplication files (`0525`..`0533`, $k = 2..10$) reconstruct `data/tensors/0525.npy` .. `0533.npy` entrywise over $\mathbb{F}_2$ and match `docs/tensors.md` (`97 / 97` total CP files match `docs/tensors.md`).
   - `data/paper/waring/*.npy`: `88 / 88` files pass the full phase-polynomial signature check (`odd_cols == 0`, `odd_pairs == 0`, and cubic triples matching both BCO and original bases) and match their filename counts; `83 / 88` match `docs/tensors.md` and `5 / 88` exceed `docs/tensors.md` (`0105-00041.npy` at `41` vs `39`, `0108-00077.npy` at `77` vs `73`, `0115-00055.npy` at `55` vs `51`, `0728-00061.npy` at `61` vs `59`, and `0817-00063.npy` at `63` vs `59`).
   - Qubit-dimension audit against `docs/tensors.md`: `0108` has actual $n = 42$ vs table $n = 46$ (`0808` has $n = 46$), and `0114` has actual $n = 11$ vs table $n = 12$ (`0814` has $n = 12$).

2. **Repaired Posted Waring Decompositions (`object/waring/`):**
   - `object/waring/0105-00039.npy` (`(39, 21)`, vs posted `0105-00041.npy` at `41`),
   - `object/waring/0108-00073.npy` (`(73, 42)`, vs posted `0108-00077.npy` at `77`),
   - `object/waring/0115-00051.npy` (`(51, 28)`, vs posted `0115-00055.npy` at `55`), and
   - `object/waring/0817-00059.npy` (`(59, 42)`, vs posted `0817-00063.npy` at `63`)
   all have distinct nonzero binary rows and pass the full-signature check (`odd_cols = 0`, `odd_pairs = 0`, exact cubic match) in both the BCO basis and the original basis.

---

## 2. Verification Table of Shipped Repaired Waring Decompositions

| Tensor ID | Benchmark Circuit | Shape `(r, n)` | `docs/tensors.md` Waring | Posted `data/paper/waring/` | Repaired Waring (`r`) | Margin vs Posted | Odd Col / Pair Sums (BCO & Orig) | Full Signature Check | SHA-256 |
|---|---|---|---:|---:|---:|---:|---|---|---|
| `0105` | CSLA MUX_3 (`01xx`) | `(39, 21)` | `39` | `41` | **`39`** | **`-2`** | `0 / 0` | `PASS` | `b0009293a2f77a19d23a1b913d2339c06dd65608657917b35f85f8840b7dcba5` |
| `0108` | Ham15 (low) (`01xx`) | `(73, 42)` | `73` | `77` | **`73`** | **`-4`** | `0 / 0` | `PASS` | `5418608b809f3d09e636e33eebc48b3a2ad92bf7b0f88ecc0a54415f2df0ced8` |
| `0115` | Mod Red_21 (`01xx`) | `(51, 28)` | `51` | `55` | **`51`** | **`-4`** | `0 / 0` | `PASS` | `86ca689e0bac48faa178cfef58e239e23db46f0c7521b25445d788d1987ba298` |
| `0817` | QCLA Com_7 (`08xx`) | `(59, 42)` | `59` | `63` | **`59`** | **`-4`** | `0 / 0` | `PASS` | `a328bc20a19c46c7de77aa462348ab96f0678c136b249881959c08820dd9eeaa` |

pass: true
