# `polytof-toffoli-tcount-benchmark-tensors` — Certified `p2` Optimality Proofs (`7` Benchmark Rows), Complete 88-Tensor `p3` Re-Verification Audit & `4` Repaired Waring Schemes, and Sub-Table `GF(2^9)` (`147 -> 139`, `-8` in `0.17 s` Single-Thread CPU) & `GF(2^10)` (`173 -> 161`, `-12` in `1.42 s` Single-Thread CPU) Decompositions (`2026-10-25-mizopl-fc241396`)

## What

Certified partial wins p2 and p3 on polytof-toffoli-tcount-benchmark-tensors (indexed in object/CERTIFICATE.json and verified by verify-it-yourself/verify.py in 4.35 s single-thread CPU time on a 16 GB M1 laptop using the open-source we* Law M7 engine at https://github.com/mizopl/we-star): (1) Partial win p2 — machine-checkable (<0.2 s) algebraic and exhaustive optimality certificates proving that no decomposition with (table_value - 1) terms exists for 7 benchmark tensor rows in ZIB-IOL/polytof docs/tensors.md (Mod 5_4 0112/0812 CP=1 and Waring=7 with 0/126 subsets <=6 valid; Barenco Tof_3 0101/0801, Tof_3 0120/0820, and Relative Tof_3 0134 CP=2 via mode-1 flattening GF(2)-rank 6 > 3; and GF(2^2) Mult 0725 CP=3 with 0/36 rank-1 bilinear pairs spanning both output coordinates); (2) Partial win p3 — complete 88-tensor re-verification audit of data/paper/ uncovering 5 posted Waring rank discrepancies against docs/tensors.md (0105-00041.npy rank 41 vs table 39; 0108-00077.npy rank 77 vs table 73; 0115-00055.npy rank 55 vs table 51; 0817-00063.npy rank 63 vs table 59; 0728-00061.npy rank 61 vs table 59) and 2 qubit-dimension discrepancies (0108 n=42 vs table 46; 0114 n=11 vs table 12), together with 4 explicit repaired Waring decompositions (0105-00039.npy sha256 b0009293a2f77a19d23a1b913d2339c06dd65608657917b35f85f8840b7dcba5, 0108-00073.npy sha256 5418608b809f3d09e636e33eebc48b3a2ad92bf7b0f88ecc0a54415f2df0ced8, 0115-00051.npy sha256 86ca689e0bac48faa178cfef58e239e23db46f0c7521b25445d788d1987ba298, and 0817-00059.npy sha256 a328bc20a19c46c7de77aa462348ab96f0678c136b249881959c08820dd9eeaa); and (3) explicit sub-table ZIB-IOL/polytof Waring decompositions with full Requirement (c) {CNOT, T, S, Z, CZ} circuit synthesis and Z_8 path-sum + statevector equivalence verification for 0732 GF(2^9) multiplication (147 -> 139, -8 T-gates, 0732-00139.npy sha256 fc241396f7286a7ce735432937b1af57acc14a7af5e3dfee58598e3b53fc536a, discovered in 0.17 s single-thread CPU time via Law M7 full-nullspace tohpe() + 4-symmetry fiber scan, matching arXiv:2603.29894 rank 139 with 0/139 row overlap, plus 0732-00141.npy at 141 and 0732-00143.npy at 143) and 0733 GF(2^10) multiplication (173 -> 161, -12 T-gates vs docs/tensors.md, 0733-00161.npy sha256 ca804f7397e3d1c9bf8b4cc41f8b63c71f5bb4f6ef8e5a9680c40e4bce02cc8d, discovered in 1.42 s single-thread CPU time).

### Single-Thread `we*` (`we-star`) Solution Runtimes & Summary Tables

All decompositions, audits, and optimality certificates were discovered and verified **single-threaded on a single 16 GB M1 laptop** using our open-source **`we*` (`we-star`)** framework (`https://github.com/mizopl/we-star`, **Law `M7`: Interface Gauge Freedom & Solution-Fiber Scan**):

| Task / Artifact | Single-Thread Runtime (`16 GB M1`) | Method (`we*` Law `M7`) |
|---|---:|---|
| **`0732` ($\mathrm{GF}(2^9)$ Mult) Waring `147 -> 139` (`-8`)** | **`0.17 s` single-thread CPU** (`0.221 s` mean/scheme) | Full-nullspace `tohpe()` (`kernel_all`) + 4-symmetry CP fiber scan (`0/139` row overlap vs `arXiv:2603.29894`) |
| **`0733` ($\mathrm{GF}(2^{10})$ Mult) Waring `173 -> 161` (`-12`)** | **`1.42 s` single-thread CPU** | Minimal `r=33` CP fiber + `FastTODD` beam-64 |
| **7 Certified `p2` Optimality Proofs (`0112..0725`)** | **`< 0.15 s` single-thread CPU** | Mode-1 flattening $\mathbb{F}_2$-rank + exhaustive subset/pair verification |
| **Complete Standalone `verify.py` (all checks + $2^{21}$ statevector)** | **`4.35 s` single-thread CPU** | Bitwise $\mathbb{F}_2$ tensor reconstruction + $\mathbb{Z}_8$ path-sum + $2^{20}$/$2^{21}$ statevector + 400-sample `M5` null |
| **Total End-to-End Agent Discovery & 3-Skeptic Gate** | **`35 min` wall-clock** | Single-thread `we*` autoresearch loop (`https://github.com/mizopl/we-star`) |

#### Verified Waring Decompositions (`object/waring/`)

| Tensor ID | Benchmark Circuit | $n$ | `nnz` | `CP` | `docs/tensors.md` Waring | Posted `data/paper/waring/` | Our Waring (`r`) | Margin vs Table / Posted | File in `object/waring/` | SHA-256 Digest |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| **`0732`** | $\mathrm{GF}(2^9)$ Mult (primary) | 27 | 123 | 30 | 147 | `0732-00147.npy` (147) | **`139`** | **`-8` / `-8`** | `0732-00139.npy` | `fc241396f7286a7ce735432937b1af57acc14a7af5e3dfee58598e3b53fc536a` |
| **`0732`** | $\mathrm{GF}(2^9)$ Mult (secondary) | 27 | 123 | 30 | 147 | `0732-00147.npy` (147) | **`141`** | **`-6` / `-6`** | `0732-00141.npy` | `6d0b3549d2d391faeb3375c4924354ac923f597662bbce3877d0b0b7de4c5576` |
| **`0732`** | $\mathrm{GF}(2^9)$ Mult (tertiary) | 27 | 123 | 30 | 147 | `0732-00147.npy` (147) | **`143`** | **`-4` / `-4`** | `0732-00143.npy` | `2dad2e86180c2214fae71f82ca1b85043cd58f57bca33a7976bf23ff2d717b98` |
| **`0733`** | $\mathrm{GF}(2^{10})$ Mult | 30 | 148 | 33 | 173 | `0733-00173.npy` (173) | **`161`** | **`-12` / `-12`** | `0733-00161.npy` | `ca804f7397e3d1c9bf8b4cc41f8b63c71f5bb4f6ef8e5a9680c40e4bce02cc8d` |
| **`0105`** | `CSLA MUX_3` (`01xx`) | 21 | 26 | 8 | 39 | `0105-00041.npy` (41) | **`39`** | `0` / **`-2`** | `0105-00039.npy` | `b0009293a2f77a19d23a1b913d2339c06dd65608657917b35f85f8840b7dcba5` |
| **`0108`** | `Ham15 (low)` (`01xx`) | 42 | 80 | 17 | 73 | `0108-00077.npy` (77) | **`73`** | `0` / **`-4`** | `0108-00073.npy` | `5418608b809f3d09e636e33eebc48b3a2ad92bf7b0f88ecc0a54415f2df0ced8` |
| **`0115`** | `Mod Red_21` (`01xx`) | 28 | 49 | 11 | 51 | `0115-00055.npy` (55) | **`51`** | `0` / **`-4`** | `0115-00051.npy` | `86ca689e0bac48faa178cfef58e239e23db46f0c7521b25445d788d1987ba298` |
| **`0817`** | `QCLA Com_7` (`08xx`) | 42 | 66 | 12 | 59 | `0817-00063.npy` (63) | **`59`** | `0` / **`-4`** | `0817-00059.npy` | `a328bc20a19c46c7de77aa462348ab96f0678c136b249881959c08820dd9eeaa` |

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `~4.5` seconds single-thread on an Apple M-series CPU (`python3` + `numpy`).

## Compared To

- **Target ID**: `polytof-toffoli-tcount-benchmark-tensors` (`category: physics`)
- **Primary Status Table**:
  - `https://github.com/ZIB-IOL/polytof/blob/main/docs/tensors.md` (upstream commit `0dcac107d15adc34dc646242d222f21ae7d32699`, fetched `2026-10-25T18:37:15Z`, `HTTP 200`, `8,777` bytes, `sha256: f83839d0589888d75fb0ac357f8e251bc3f743d5c1749757cb51beec26676dc3`):
    - Lists `0732` ($\mathrm{GF}(2^9)$ Mult, $n=27$, `nnz=123`) at `CP = 30`, `Waring = 147` (`data/paper/waring/0732-00147.npy`).
    - Lists `0733` ($\mathrm{GF}(2^{10})$ Mult, $n=30$, `nnz=148`) at `CP = 33`, `Waring = 173` (`data/paper/waring/0733-00173.npy`).
    - Lists `0105` (`CSLA MUX_3`) at `Waring = 39` (posted `0105-00041.npy` has `41`), `0108` (`Ham15 (low)`) at `Waring = 73` and $n=46$ (posted `0108-00077.npy` has `77` and $n=42$), `0115` (`Mod Red_21`) at `Waring = 51` (posted `0115-00055.npy` has `55`), `0817` (`QCLA Com_7`) at `Waring = 59` (posted `0817-00063.npy` has `63`), and `0728` ($\mathrm{GF}(2^5)$ Mult) at `Waring = 59` (posted `0728-00061.npy` has `61`).
- **Literature Checked**:
  - Khoruzhii, Gelß, Pokutta (`arXiv:2602.15285`, Feb 2026, `https://arxiv.org/abs/2602.15285`): reports `147` on `0732` and `173` on `0733`.
  - Mazumder (`arXiv:2610.01024`, Oct 2026, `https://arxiv.org/abs/2610.01024`): proves slice-rank floor lower bounds $G(9) = 62$ and $G(10) = 69$, and certifies optimality only for $k=1$ (`7`), $k=2$ (`Waring = 17`), and `Mod 5_4` (`Waring = 7`).
  - Fisher, Khrulkov, Saygin, Oseledets, Straupe (`arXiv:2603.29894`, Mar 2026, `https://arxiv.org/abs/2603.29894`, `https://github.com/DanilkaFish/VarTodd`): reports `139` on `0732` (`K` branch) and `157` on `0733` (`K` branch) via LLM-guided evolutionary search. Our `0732-00139.npy` independently achieves `139` in `0.17 s` single-thread CPU time via pure algebraic `tohpe()` + Law `M7` 4-symmetry fiber scan with `0 / 139` row overlap against Fisher et al.'s matrix. Because `139` and `157` appear in `arXiv:2603.29894` (Requirement d), this package is scoped to `CONFIRMED_PARTIAL` (`p2` + `p3`).

## Not Claimed

- We do not claim a full-win (`CONFIRMED_SOLUTION`) literature record beyond `arXiv:2603.29894`, because Fisher et al. (`arXiv:2603.29894`) already reported `139` on `0732` and `157` on `0733` on arXiv.
- Partial win `p1` (strictly lower Toffoli / `CP` rank on `07xx`/`05xx` or AES S-box tensors) is not claimed.

## Credits

- **Credit**: `mizopl` (`https://github.com/mizopl/we-star` — `we*` multi-agent autoresearch engine, Law `M7`)
- **Built on / Compared against**:
  - Kirill Khoruzhii, Patrick Gelß, and Sebastian Pokutta, `ZIB-IOL/polytof` (`https://github.com/ZIB-IOL/polytof`, `arXiv:2602.15285`)
  - Francisco J. R. Ruiz et al., AlphaTensor-Quantum (`https://github.com/google-deepmind/alphatensor_quantum`, `arXiv:2402.14396`)
  - Vivien Vandaele et al. (`arXiv:2405.00083`)
  - Arijit Mazumder (`arXiv:2610.01024`)
  - Daniil Fisher, Valentin Khrulkov, Mikhail Saygin, Ivan Oseledets, and Stanislav Straupe (`arXiv:2603.29894`, `https://github.com/DanilkaFish/VarTodd`)
