# V3R1T4S Skeptic 3 (CRITERION) Audit Report — `moore-graph-57` (`p2`)

> **Dated Scope Note (`2026-10-29`):** Per `@elder-plinius`'s review on PR `#770`, this standalone package extracts strictly the **Partial Win `p2`** exact computational verification of `arXiv:2606.29183v2` (`object/certificate.json`, `sha256: d13344783df1b7cf33f19e9b3408bad1bbe96939c5e087b02460113f03dc9c07`), with all unformalized `p1` written group-action arguments removed.

- context: fresh subagent (bac313c7-40c1-4b96-a9d3-3a3c5d4f73c1) invoked via invoke_subagent for independent V3R1T4S panel review
- **Verdict:** PASS
- **Target ID:** `moore-graph-57`

---

## 1. Audit Against `target.md` Clauses (`p2`)
- **Main Success Criterion Boundary Respected:** `target.md` states that `CONFIRMED` (`CONFIRMED_SOLUTION`) is reserved for an explicit adjacency list on `3250` vertices with $A^2 + A - 56I = J$ or a formal Lean/Isabelle non-existence proof. `README.md`, `panel/gate.md`, and `object/certificate.json` strictly claim `CONFIRMED_PARTIAL` (`p2`) and do not claim a full solution or unformalized group exclusions.
- **Partial Win `p2` Clause Verification:**
  - *Requirement:* An independent machine-checked (Lean/Isabelle) or fully reproducible exact-computation verification of the `arXiv:2606.29183` theorem that a Moore graph of degree 57 has no involutory automorphisms.
  - *Audit:* **SATISFIED.** `verify-it-yourself/verify.py` (standard library only, exact `int`, `fractions.Fraction`, and $\mathbb{F}_p$ row-echelon arithmetic; exits `0` and prints `PASS` on its last line) and `object/certificate.json` independently verify from first principles in exact arithmetic:
    - Spectral idempotents $E_{57} = \frac{1}{3250}J$, $E_7 = \frac{400I + 50A - J}{750}$ ($\mathrm{denom} = 750 = 2 \cdot 3 \cdot 5^3$, $m_7 = 1729$), $E_{-8} = \frac{455I - 65A + J}{975}$ ($\mathrm{denom} = 975 = 3 \cdot 5^2 \cdot 13$, $m_{-8} = 1520$).
    - Brauer trace–rank identity $\mathrm{tr}(T_g E_\theta) = \mathrm{rank}_{\mathbb{F}_p}(E_\theta[\mathrm{Fix}(g)] \bmod p)$ on $C_5$, Petersen $\mathrm{srg}(10,3,0,1)$, and Hoffman–Singleton $\mathrm{srg}(50,7,0,1)$ ($5/5$ exact matches).
    - Theorem 1.1 & Corollary 6.1 ($p=2$): $\mathrm{Fix}(t) \cong K_{1,55}$ ($a_0(t) = 56$), combinatorial $a_1(t) = 112$ ($\chi_{-8}(t) = 22$, $\chi_7(t) = 33$, and $a_1(t) = 0$ impossible across all closed subgraphs), and $\mathrm{rank}_{\mathbb{F}_2}(975 E_{-8}[F] \bmod 2) = 54 \implies a_1(t) = -368 < 0$ (no involutions; $|\mathrm{Aut}(\Gamma)|$ is odd).
    - Theorem 1.2 ($p \in \{7, 11, 13, 19\}$) and all $11$ rows of Section 8 Table 1 across 5 open SRG families (including Remark 8.5 on $\mathrm{srg}(352,26,0,2)$).

## 2. Preregistration Freeze & `null_test` Audit
- **Timestamp Ordering:** `how-we-built-it/PREREG.md` records `frozen_utc: 2026-10-26T03:31:15Z`, which strictly precedes all claim files.
- **`null_test` Justification:** `PREREG.md` specifies `null_test: not needed because exact deterministic integer/rational and finite-field linear algebra verification has zero stochastic variance`.

## 3. Digit-for-Digit (`K12`) Consistency Audit
- `object/certificate.json` SHA-256 is `d13344783df1b7cf33f19e9b3408bad1bbe96939c5e087b02460113f03dc9c07`, matching `README.md`, `panel/gate.md`, and `INDEX.csv` character-for-character.
- Every integer, rank, multiplicity, and parameter tuple across `README.md`, `panel/gate.md`, and `object/certificate.json` matches digit-for-digit (`0` discrepancies).

pass: true
