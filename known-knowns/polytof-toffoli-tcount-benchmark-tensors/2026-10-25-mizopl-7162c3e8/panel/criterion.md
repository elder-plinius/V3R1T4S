context: isolated Antigravity subagent 520fd83c-45f6-4ca5-9f66-e864d73cf31e (V3R1T4S Skeptic CRITERION)
target_id: polytof-toffoli-tcount-benchmark-tensors
run_id: 2026-10-25-1935

# Adversarial Skeptic Report: `CRITERION` — Run `2026-10-25-1935`

- **Target:** `polytof-toffoli-tcount-benchmark-tensors`
- **Skeptic Role:** `CRITERION` (Strict adherence to every rule in `target.md`, `PREREG.md`, and `kit/SUBMIT.md`)
- **Timestamp (UTC):** `2026-10-25T19:49:00Z` (Updated `2026-10-30` for `p3`-only package split `2026-10-25-mizopl-7162c3e8`)

---

## 1. Executive Summary & Audit Scope

I conducted an adversarial criterion-by-criterion audit of package `2026-10-25-mizopl-7162c3e8` against the definition of **partial win `p3`** in `target.md` and the single-object packaging rules in `kit/SUBMIT.md` section 1:
> "**p3:** An independent re-verification audit of all decompositions in data/paper/ that reports any table value not reproduced by its posted decomposition."

1. **Single-Object / Single-Partial-Win Scoping (`kit/SUBMIT.md` section 1):**
   - This package holds strictly the **`p3` audit** (`object/p3_audit_certificate.json`, SHA-256 `7162c3e8cd13709302daf1b50be19ecb1f1bf75e1aa78c6b5050e188e1a42757`) together with the **`4` repaired Waring schemes** (`object/waring/0105-00039.npy`, `object/waring/0108-00073.npy`, `object/waring/0115-00051.npy`, `object/waring/0817-00059.npy`).
2. **Complete Recomputation from Pinned `polytof` Commit (`0dcac107d15adc34dc646242d222f21ae7d32699`):**
   - `verify-it-yourself/run_checks.sh` checks out `ZIB-IOL/polytof` at pinned commit `0dcac107d15adc34dc646242d222f21ae7d32699`, verifies the commit hash, and invokes `verify-it-yourself/verify.py`.
   - `verify-it-yourself/verify.py` recomputes the entire `p3` audit from scratch across all `185` decomposition files in `data/paper/`:
     - All `88` `data/paper/cpd/topp/*.npy` files covering all `13,528` stored CP schemes (`74` single-row files + `14` multi-row pool files containing `13 x 1,000 + 454 = 13,454` schemes),
     - All `9` `data/paper/cpd/base/*.npy` bilinear files (`0525`..`0533`),
     - All `88` `data/paper/waring/*.npy` files under the full signature (`odd_cols == 0`, `odd_pairs == 0`, and cubic triples matching in both BCO and original bases).
   - Identifies the `5` Waring rank discrepancies (`0105`, `0108`, `0115`, `0728`, `0817`) and `2` qubit-dimension discrepancies (`0108`, `0114`), verifies the `4` shipped repaired Waring schemes (`0105-00039.npy`, `0108-00073.npy`, `0115-00051.npy`, `0817-00059.npy`), and rejects any corrupted copy of any file in `object/`.

pass: true
