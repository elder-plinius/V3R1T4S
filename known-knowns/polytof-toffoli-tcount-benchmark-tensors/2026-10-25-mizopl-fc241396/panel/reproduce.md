context: isolated Antigravity subagent 2c016a51-8957-4d4d-abe3-067d0cb6ef92 (V3R1T4S Skeptic REPRODUCE)
target_id: polytof-toffoli-tcount-benchmark-tensors
run_id: 2026-10-25-1935

# Adversarial Skeptic Report: `REPRODUCE`

- **Run ID:** `2026-10-25-1935`
- **Target ID:** `polytof-toffoli-tcount-benchmark-tensors`
- **Skeptic Role:** `REPRODUCE` (Independent Bit-Exact Reproduction of Tensors, Decompositions, Circuit Syntheses, Optimality Certificates, and 88-Tensor Audit)
- **Timestamp (UTC):** `2026-10-25T19:49:00Z`

---

## 1. Executive Summary

I independently executed `python3 claim/verify.py`, `python3 claim/synthesize_and_verify_circuits.py`, `ZIB-IOL/polytof`'s `scripts/verify_paper_schemes.py`, and an independent clean-room Python verification script against the unmodified upstream repository `ZIB-IOL/polytof` (`commit 0dcac107d15adc34dc646242d222f21ae7d32699`).

Every claimed decomposition, tensor reconstruction, circuit equivalence check, optimality certificate (`p2`), and 88-tensor audit result (`p3`) reproduced with **zero discrepancies**:

1. **Sub-Table Record 1 (`0732`, $\mathrm{GF}(2^9)$ Multiplication, $n=27$, $\mathrm{nnz}=123$, `07xx` variant):**
   - `claim/waring/0732-00139.npy` (SHA-256 `fc241396f7286a7ce735432937b1af57acc14a7af5e3dfee58598e3b53fc536a`) has shape `(139, 27)` over $\{0,1\}$, with 139 distinct nonzero parity rows, **8 fewer terms** ($-5.44\%$) than the live `docs/tensors.md` Waring record (`147`), found in **`0.17 s` single-thread CPU time** via Law `M7` full-nullspace `tohpe()` + 4-symmetry fiber scan (matching the `arXiv:2603.29894` rank `139` with `0 / 139` overlapping rows).
   - `claim/waring/0732-00141.npy` (SHA-256 `6d0b3549d2d391faeb3375c4924354ac923f597662bbce3877d0b0b7de4c5576`) has shape `(141, 27)` over $\{0,1\}$, with 141 distinct nonzero parity rows, **6 fewer terms** ($-4.08\%$) than `147`.
   - `claim/waring/0732-00143.npy` (SHA-256 `2dad2e86180c2214fae71f82ca1b85043cd58f57bca33a7976bf23ff2d717b98`) has shape `(143, 27)` over $\{0,1\}$, **4 fewer terms** than `147`.
   - All three reconstruct the exact unmodified tensor `data/tensors/0732.npy` (`123` strict upper-triangular triples $i < j < k$, with `data/paper/transform/0732.npy` verified equal to $I_{27}$) and pass `ZIB-IOL/polytof`'s `verify_waring` in `scripts/verify_paper_schemes.py`.

2. **Sub-Table Record 2 (`0733`, $\mathrm{GF}(2^{10})$ Multiplication, $n=30$, $\mathrm{nnz}=148$, `07xx` variant):**
   - `claim/waring/0733-00161.npy` (SHA-256 `ca804f7397e3d1c9bf8b4cc41f8b63c71f5bb4f6ef8e5a9680c40e4bce02cc8d`) has shape `(161, 30)` over $\{0,1\}$, with 161 distinct nonzero parity rows, **12 fewer terms** ($-6.94\%$) than the live `docs/tensors.md` Waring record (`173`), found in **`1.42 s` single-thread CPU time**.
   - It reconstructs the exact unmodified tensor `data/tensors/0733.npy` (`148` strict upper-triangular triples $i < j < k$, with `data/paper/transform/0733.npy` verified equal to $I_{30}$) and passes `ZIB-IOL/polytof`'s `verify_waring`.

3. **Repaired Posted Waring Decompositions (`0105`, `0108`, `0115`, `0817`):**
   - `claim/waring/0105-00039.npy` (`(39, 21)`, vs posted `0105-00041.npy` at `41`),
   - `claim/waring/0108-00073.npy` (`(73, 42)`, vs posted `0108-00077.npy` at `77`),
   - `claim/waring/0115-00051.npy` (`(51, 28)`, vs posted `0115-00055.npy` at `55`), and
   - `claim/waring/0817-00059.npy` (`(59, 42)`, vs posted `0817-00063.npy` at `63`)
   all reconstruct their exact BCO-transformed benchmark tensors and pass `ZIB-IOL/polytof`'s `verify_waring`.

---

## 2. Verification Table of Claimed Waring Decompositions

| Tensor ID | Benchmark Circuit | Shape `(r, n)` | Live `docs/tensors.md` Waring | Posted `data/paper/waring/` | Claimed Waring (`r`) | Margin vs Table / Posted | Odd Col / Pair Sums | Standalone Check | `polytof` `verify_waring` | SHA-256 (prefix) |
|---|---|---|---:|---:|---:|---|---:|---|---|---|
| `0732` | $\mathrm{GF}(2^9)$ Mult (primary) | `(139, 27)` | `147` | `147` | **`139`** | **`-8` / `-8`** | `0 / 0` | `PASS` | `PASS` | `fc241396f7286a7c...` |
| `0732` | $\mathrm{GF}(2^9)$ Mult (secondary) | `(141, 27)` | `147` | `147` | **`141`** | **`-6` / `-6`** | `0 / 0` | `PASS` | `PASS` | `6d0b3549d2d391fa...` |
| `0732` | $\mathrm{GF}(2^9)$ Mult (tertiary) | `(143, 27)` | `147` | `147` | **`143`** | **`-4` / `-4`** | `0 / 0` | `PASS` | `PASS` | `2dad2e86180c2214...` |
| `0733` | $\mathrm{GF}(2^{10})$ Mult | `(161, 30)` | `173` | `173` | **`161`** | **`-12` / `-12`** | `0 / 0` | `PASS` | `PASS` | `ca804f7397e3d1c9...` |
| `0105` | CSLA MUX_3 (`01xx`) | `(39, 21)` | `39` | `41` | **`39`** | `0` / **`-2`** | `0 / 0` | `PASS` | `PASS` | `b0009293a2f77a19...` |
| `0108` | Ham15 (low) (`01xx`) | `(73, 42)` | `73` | `77` | **`73`** | `0` / **`-4`** | `0 / 0` | `PASS` | `PASS` | `5418608b809f3d09...` |
| `0115` | Mod Red_21 (`01xx`) | `(51, 28)` | `51` | `55` | **`51`** | `0` / **`-4`** | `0 / 0` | `PASS` | `PASS` | `86ca689e0bac48fa...` |
| `0817` | QCLA Com_7 (`08xx`) | `(59, 42)` | `59` | `63` | **`59`** | `0` / **`-4`** | `0 / 0` | `PASS` | `PASS` | `a328bc20a19c46c7...` |

---

## 3. Requirement (c): Explicit Circuit Synthesis & Exact Path-Sum + Statevector Equivalence

I independently verified `claim/synthesize_and_verify_circuits.py`:

- **Zero Extra Non-Clifford Gates:** In all claimed Waring matrices $A \in \{0,1\}^{r \times n}$, every column sum $\sum_{q=1}^r A_{q,i}$ is even and every pair sum $\sum_{q=1}^r A_{q,i} A_{q,j}$ ($i<j$) is even. Consequently, in the multilinear expansion over $\mathbb{Z}_8[x_0, \dots, x_{n-1}]/(x_i^2 - x_i)$,
  $$\sum_{q=1}^r \left(p^{(q)}(x) \bmod 2\right) \equiv \sum_i M_i x_i - 2 \sum_{i<j} Q_{ij} x_i x_j + 4 \sum_{i<j<k} T_{ijk} x_i x_j x_k \pmod 8,$$
  all linear residuals $-M_i \bmod 8 \in \{0, 2, 4, 6\}$ are compensated purely by single-qubit Clifford $S, S^\dagger, Z$ gates (`0` $T$-gates), and all quadratic residuals $+2 Q_{ij} \bmod 8 \in \{0, 4\}$ are compensated purely by two-qubit Clifford $\mathrm{CZ}$ gates (`0` $T$-gates).
- **`0732` ($\mathrm{GF}(2^9)$ Mult, $n=27$ qubits, `0732-00139.npy`):**
  - Synthesized circuit uses exactly **139 $T$-gates**, 7 $S/S^\dagger$ gates, 11 $Z$ gates, 167 $\mathrm{CZ}$ gates, and 2,710 $\mathrm{CNOT}$ gates (0 ancilla qubits).
  - Exact symbolic path-sum check over $\mathbb{Z}_8[x_0, \dots, x_{26}]/(x_i^2 - x_i)$: `linear_zero_mod8 = True`, `quadratic_zero_mod8 = True`, `cubic_exact_mod8 = True` (`123/123` triples matched).
  - Direct $2^{20} = 1,048,576$-state statevector phase evaluation against the algebraic $\mathrm{GF}(2^9) \cong \mathbb{F}_2[x]/(x^9 + x^4 + 1)$ multiplication oracle $(-1)^{\langle a \cdot b, c \rangle}$: **0 mismatches**.
- **`0733` ($\mathrm{GF}(2^{10})$ Mult, $n=30$ qubits):**
  - Synthesized circuit uses exactly **161 $T$-gates**, 18 $S/S^\dagger$ gates, 9 $Z$ gates, 231 $\mathrm{CZ}$ gates, and 4,078 $\mathrm{CNOT}$ gates (0 ancilla qubits).
  - Exact symbolic path-sum check over $\mathbb{Z}_8[x_0, \dots, x_{29}]/(x_i^2 - x_i)$: `linear_zero_mod8 = True`, `quadratic_zero_mod8 = True`, `cubic_exact_mod8 = True` (`148/148` triples matched).
  - Direct $2^{20} = 1,048,576$-state statevector phase evaluation against the algebraic $\mathrm{GF}(2^{10}) \cong \mathbb{F}_2[x]/(x^{10} + x^3 + 1)$ multiplication oracle $(-1)^{\langle a \cdot b, c \rangle}$: **0 mismatches**.
- **`0105` (`CSLA MUX_3`, $n=21$ qubits):**
  - Synthesized circuit uses **39 $T$-gates**, 4 $S/S^\dagger$ gates, 11 $Z$ gates, 24 $\mathrm{CZ}$ gates, and 248 $\mathrm{CNOT}$ gates.
  - Exact symbolic path-sum check over $\mathbb{Z}_8[x_0, \dots, x_{20}]/(x_i^2 - x_i)$: `linear_zero_mod8 = True`, `quadratic_zero_mod8 = True`, `cubic_exact_mod8 = True` (`61/61` original-basis triples matched).
  - Exhaustive $2^{21} = 2,097,152$-state full diagonal statevector equivalence check: **0 mismatches** (`fidelity = 1.0`).

---

## 4. Partial Wins `p2` and `p3` Reproduction

- **Partial Win `p2` (Certified Optimality Proofs):**
   - `Mod 5_4` (`0112` / `0812`): $\mathrm{CP} = 1$ optimal ($\mathrm{nnz} = 1 > 0$) and $\mathrm{Waring} = 7$ optimal (all $\sum_{r=1}^6 \binom{7}{r} = 126$ subsets of $\le 6$ nonzero linear forms over $\mathbb{F}_2^3$ fail to yield a pure cubic triple with zero odd linear/quadratic residuals, while $r=7$ succeeds).
   - `Barenco Tof_3` (`0101`, `0801`), `Tof_3` (`0120`, `0820`), and `Relative Tof_3` (`0134`): mode-1 flattening matrix $F_1(T) \in \mathbb{F}_2^{n \times n^2}$ has $\mathrm{rank}_{\mathbb{F}_2}(F_1(T)) = 6 > 3$, certifying $\mathrm{CP}(T) \ge \lceil 6/3 \rceil = 2$, so the table value $\mathrm{CP} = 2$ is strictly optimal.
   - `GF(2^2) Mult` (`0725` / `0525`): exhaustive check over all $\binom{9}{2} = 36$ pairs of nonzero rank-1 bilinear forms in $\mathbb{F}_2^2 \times \mathbb{F}_2^2$ finds `0` pairs spanning both output coordinates $(z_0, z_1)$ of $\mathbb{F}_4$ multiplication, certifying $\mathrm{CP} = 3$ is strictly optimal.
- **Partial Win `p3` (88-Tensor Upstream Audit):**
   - Independent execution across all 88 tensor IDs in `data/paper/` confirmed `88 PASS, 0 FAIL` on tensor reconstruction, while confirming the 5 posted Waring rank discrepancies (`0105`: posted `41` vs table `39`; `0108`: posted `77` vs table `73`; `0115`: posted `55` vs table `51`; `0817`: posted `63` vs table `59`; `0728`: posted `61` vs table `59`) and 2 dimension discrepancies (`0108`: $n=42$ vs `0808` $n=46$; `0114`: $n=11$ vs `0814` $n=12$).

pass: true
