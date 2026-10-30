# `polytof-toffoli-tcount-benchmark-tensors` — `p3` Audit of the Posted `data/paper/` Decompositions (`185` Files, `13,537` CP Schemes & `88` Waring Schemes) and `4` Repaired Waring Schemes (`2026-10-25-mizopl-7162c3e8`)

## What

Confirmed partial win p3 on polytof-toffoli-tcount-benchmark-tensors (indexed in object/p3_audit_certificate.json sha256 7162c3e8cd13709302daf1b50be19ecb1f1bf75e1aa78c6b5050e188e1a42757 and recomputed from scratch by verify-it-yourself/verify.py against ZIB-IOL/polytof pinned commit 0dcac107d15adc34dc646242d222f21ae7d32699): (1) independent re-verification audit of all 185 decomposition files in data/paper/ — all 88 files in data/paper/cpd/topp/ covering all 13,528 stored CP schemes across 74 single-row files and 14 multi-row pool files (13 x 1,000 + 454 = 13,454 pool schemes), all 9 bilinear files in data/paper/cpd/base/ (0525..0533, 9/9 valid, 97/97 total CP files matching docs/tensors.md), and all 88 files in data/paper/waring/ under the full phase-polynomial signature (linear, quadratic, and cubic parities in both BCO and original bases, 88/88 valid) — uncovering 5 posted Waring rank discrepancies against docs/tensors.md (0105-00041.npy rank 41 vs table 39; 0108-00077.npy rank 77 vs table 73; 0115-00055.npy rank 55 vs table 51; 0728-00061.npy rank 61 vs table 59; 0817-00063.npy rank 63 vs table 59) and 2 qubit-dimension discrepancies (0108 actual n=42 vs table 46; 0114 actual n=11 vs table 12); and (2) 4 explicit repaired Waring decompositions matching docs/tensors.md under the full signature in both BCO and original bases (object/waring/0105-00039.npy sha256 b0009293a2f77a19d23a1b913d2339c06dd65608657917b35f85f8840b7dcba5, object/waring/0108-00073.npy sha256 5418608b809f3d09e636e33eebc48b3a2ad92bf7b0f88ecc0a54415f2df0ced8, object/waring/0115-00051.npy sha256 86ca689e0bac48faa178cfef58e239e23db46f0c7521b25445d788d1987ba298, and object/waring/0817-00059.npy sha256 a328bc20a19c46c7de77aa462348ab96f0678c136b249881959c08820dd9eeaa).

### Summary of `p3` Audit Coverage (`ZIB-IOL/polytof` at `0dcac107d15adc34dc646242d222f21ae7d32699`)

| `data/paper/` Subset | Files Audited | Total Stored Schemes Audited | Valid Reconstruction | Rank Matches `docs/tensors.md` | Discrepancies Found |
|---|---:|---:|---:|---:|---|
| `data/paper/transform/*.npy` | `88` | `88` basis matrices | `88 / 88` invertible over $\mathbb{F}_2$ | `86 / 88` match `n` | **`2` dimension discrepancies** (`0108` $n=42$ vs $46$; `0114` $n=11$ vs $12$) |
| `data/paper/cpd/topp/*.npy` (single-row) | `74` | `74` CP schemes | `74 / 74` (`100%`) | `74 / 74` | `0` |
| `data/paper/cpd/topp/*.npy` (multi-row pools) | `14` | `13,454` CP schemes (`13 x 1,000 + 454`) | `13,454 / 13,454` (`100%`) | `14 / 14` | `0` |
| `data/paper/cpd/base/*.npy` (`0525`..`0533`) | `9` | `9` bilinear CP schemes | `9 / 9` (`100%`) | `9 / 9` | `0` |
| `data/paper/waring/*.npy` (full signature) | `88` | `88` Waring schemes | `88 / 88` (`100%` linear, quadratic & cubic) | `83 / 88` | **`5` Waring rank discrepancies** (`0105`, `0108`, `0115`, `0728`, `0817`) |
| **Total `data/paper/` Decompositions** | **`185`** | **`13,537` CP + `88` Waring** | **`100%` valid** | **`97/97` CP, `83/88` Waring** | **`5` Waring rank + `2` dimension discrepancies** |

### Five Posted Waring Rank Discrepancies & Four Shipped Repaired Schemes (`object/waring/`)

| Tensor ID | Benchmark Circuit | Actual $n$ (Table $n$) | Orig `nnz` (`BCO nnz`) | Table `CP` | `docs/tensors.md` Waring | Posted `data/paper/waring/` File (Rank) | Excess Over Table | Repaired File in `object/waring/` (Rank) | SHA-256 Digest |
|---|---|---:|---:|---:|---:|---|---:|---|---|
| **`0105`** | `CSLA MUX_3` (`01xx`) | `21` (`21`) | `61` (`26`) | `8` | `39` | `0105-00041.npy` (`41`) | `+2` | `object/waring/0105-00039.npy` (**`39`**) | `b0009293a2f77a19d23a1b913d2339c06dd65608657917b35f85f8840b7dcba5` |
| **`0108`** | `Ham15 (low)` (`01xx`) | **`42`** (`46`) | `891` (`80`) | `17` | `73` | `0108-00077.npy` (`77`) | `+4` | `object/waring/0108-00073.npy` (**`73`**) | `5418608b809f3d09e636e33eebc48b3a2ad92bf7b0f88ecc0a54415f2df0ced8` |
| **`0115`** | `Mod Red_21` (`01xx`) | `28` (`28`) | `365` (`49`) | `11` | `51` | `0115-00055.npy` (`55`) | `+4` | `object/waring/0115-00051.npy` (**`51`**) | `86ca689e0bac48faa178cfef58e239e23db46f0c7521b25445d788d1987ba298` |
| **`0817`** | `QCLA Com_7` (`08xx`) | `42` (`42`) | `75` (`66`) | `12` | `59` | `0817-00063.npy` (`63`) | `+4` | `object/waring/0817-00059.npy` (**`59`**) | `a328bc20a19c46c7de77aa462348ab96f0678c136b249881959c08820dd9eeaa` |
| **`0728`** | $\mathrm{GF}(2^5)$ Mult (`07xx`) | `15` (`15`) | `36` (`36`) | `13` | `59` | `0728-00061.npy` (`61`) | `+2` | *(Posted `0128-00059.npy` achieves `59` via BCO transform)* | — |

### Two Qubit-Dimension Discrepancies vs `docs/tensors.md`

| Tensor ID | Benchmark Circuit | `docs/tensors.md` $n$ | Actual `data/tensors/` $n$ | Counterpart ID (`08xx`) $n$ |
|---|---|---:|---:|---:|
| **`0108`** | `Ham15 (low)` | `46` | **`42`** | `0808` has $n = 46$ |
| **`0114`** | `Mod Mult_55` | `12` | **`11`** | `0814` has $n = 12$ |

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **What it does**: Clones `https://github.com/ZIB-IOL/polytof.git` at pinned commit `0dcac107d15adc34dc646242d222f21ae7d32699` (if `POLYTOF_DIR` is not already provided), verifies the commit SHA and `docs/tensors.md` digest, recomputes the entire `p3` audit across all `185` decomposition files (`13,528` `cpd/topp` schemes across `74` single-row and `14` pool files, `9` `cpd/base` bilinear schemes, and `88` `waring` schemes under the full signature), verifies the `4` repaired Waring `.npy` schemes in `object/waring/` in both BCO and original bases, and verifies `object/p3_audit_certificate.json` (`~4.5 s` single-thread CPU time after checkout).

## Compared To

- **Target ID**: `polytof-toffoli-tcount-benchmark-tensors` (`category: physics`)
- **Primary Status Table**:
  - `https://github.com/ZIB-IOL/polytof/blob/main/docs/tensors.md` (upstream commit `0dcac107d15adc34dc646242d222f21ae7d32699`, fetched `2026-10-25T18:37:15Z`, `HTTP 200`, `8,777` bytes, `sha256: f83839d0589888d75fb0ac357f8e251bc3f743d5c1749757cb51beec26676dc3`).
- **Literature Checked**:
  - Khoruzhii, Gelß, Pokutta (`arXiv:2602.15285`, Feb 2026, `https://arxiv.org/abs/2602.15285`, `https://github.com/ZIB-IOL/polytof`).
  - Ruiz et al., AlphaTensor-Quantum (`arXiv:2402.14396`, `https://github.com/google-deepmind/alphatensor_quantum`).
  - Vandaele et al. (`arXiv:2405.00083`).
  - Mazumder (`arXiv:2610.01024`).

## Not Claimed

- This package claims only partial win **`p3`** (the complete re-verification audit of `data/paper/` and the `4` repaired Waring schemes matching `docs/tensors.md`).
- Partial win `p2` (single-row optimality certificates) is filed in separate single-row pull requests per `kit/SUBMIT.md` section 1.
- Partial win `p1` (strictly lower Toffoli / `CP` rank) and full-win literature T-count records are not claimed here.

## Credits

- **Credit**: `mizopl` (`https://github.com/mizopl/we-star` — `we*` multi-agent autoresearch engine, Law `M7`)
- **Cross-check acknowledgment**: Thanks to `@DmitrL-dev` for independent cross-verification of the `185` decomposition files, `13,528` stored `cpd/topp` pool schemes, `9` `cpd/base` schemes, and the `4` repaired Waring matrices.
- **Built on / Compared against**:
  - Kirill Khoruzhii, Patrick Gelß, and Sebastian Pokutta, `ZIB-IOL/polytof` (`https://github.com/ZIB-IOL/polytof`, `arXiv:2602.15285`)
  - Francisco J. R. Ruiz et al., AlphaTensor-Quantum (`https://github.com/google-deepmind/alphatensor_quantum`, `arXiv:2402.14396`)
  - Vivien Vandaele et al. (`arXiv:2405.00083`)
