# Skeptic Panel Report: CRITERION

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target_id: ame-states-open-cells-huber-table
confirmed_scope: Exact closed-form algebraic constructions in Q(zeta_5) for two open cells of the Huber-Wyderka table, AME(9, 10) in claim/ame_9_10_certificate.json (55,497 bytes, sha256 9a17cd1e6d7fb1017aaa7880fac09cac1515ec3a2b4f55677b95317ed7ecd47c, coupling the 4-dimensional [[9, 2, 3]]_2 binary stabilizer code of dual distance d_perp = 5 with four Z_5-shifted states of the [[9, 0, 5]]_5 graph state along c_9 = (0,0,0,1,4,4,3,1,1) in F_5^9, verified across all 126/126 four-party cuts in exact Gaussian-integer and F_5 arithmetic and to 2.82e-18 elementwise / 2.40e-17 Frobenius error via dense 5^9-vector contraction) and AME(11, 10) in claim/ame_11_10_certificate.json (168,341 bytes, sha256 2939f47d71d26b1844bfac1b67d12503eec5e801e5c82a7e73b556b3a2938f9c, coupling the 2-dimensional [[11, 1, 5]]_2 binary stabilizer code of dual distance d_perp = 6 with two Z_5-shifted states of an explicit pure [[11, 1, 6]]_5 quantum MDS code along c_11 = (2,0,2,2,3,1,1,4,4,1,2) in F_5^11, verified across all 462/462 five-party cuts and 923/923 F_25 minors), together with a complete 1,008-cell Huber-Wyderka table-maintenance and purity audit in claim/huber_wyderka_settled_blanks_audit.json (18,153 bytes, sha256 8d75d681f48af24ac4ca02704243da3bb9228c7b5f50180770d6b67544b8ffe4) certifying 22 settled blank cells and proving that codetables.de [[15, 0, 8]]_5 (w_pure = 7, 190/6,435 bad cuts) and [[15, 0, 8]]_7 (w_pure = 1, 3,003/6,435 bad cuts) are impure false positives (subsuming p2).

---

## 1. Clause-by-Clause Audit Against Verbatim Bank Criteria

### 1.1 File Integrity and Checksums in `claim/`

All saved artifacts in `claim/` were hashed and inspected independently:

| Relative File Path | Size (Bytes) | Verified SHA-256 Digest |
|---|---:|---|
| `claim/ame_9_10_certificate.json` | `55,497` | `9a17cd1e6d7fb1017aaa7880fac09cac1515ec3a2b4f55677b95317ed7ecd47c` |
| `claim/ame_11_10_certificate.json` | `168,341` | `2939f47d71d26b1844bfac1b67d12503eec5e801e5c82a7e73b556b3a2938f9c` |
| `claim/huber_wyderka_settled_blanks_audit.json` | `18,153` | `8d75d681f48af24ac4ca02704243da3bb9228c7b5f50180770d6b67544b8ffe4` |
| `claim/huber_wyderka_settled_blanks_audit.tsv` | `6,022` | `297ec1409f5fc41301db4dcc1dbdf0ef76719659fff8130906fdea8c25f79353` |
| `claim/ame_table_live.html` | `230,252` | `e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082` |
| `claim/author_checker_ame.py` | `24,238` | `278f8e9d225ea0a60bf1f02efed27f688bae9077cb9fa506420fe98c949bdf16` |

### 1.2 Full `success_criterion` Clause (a) Verification

The target `success_criterion` Clause (a) requires:
1. An explicit tensor $T \in (\mathbb{C}^D)^{\otimes n}$ in algebraic closed form or rational/cyclotomic entries (or stabilizer generator matrix over $\mathbb{F}_D$ / $\mathbb{Z}_D$);
2. For a cell $(n, D)$ that is currently blank or labeled `Unknown` in `https://tp.nt.uni-siegen.de/ame/table.html` and not already settled in Markus Grassl's `codetables.de` or the literature;
3. Such that for all $\binom{n}{\lfloor n/2 \rfloor}$ subsets $S$ of size $k = \lfloor n/2 \rfloor$, the reduced density matrix $\rho_S = \operatorname{Tr}_{S^c}(\lvert\psi\rangle\langle\psi\rvert)$ equals $I_{D^k}/D^k$ exactly (or to Frobenius error below $10^{-12}$ if numerical, accompanied by an exact algebraic rounding).

**Verification of Open Status (`(9, 10)` and `(11, 10)`):**
- Parsing the Bokeh `ColumnDataSource` in `claim/ame_table_live.html` across the full `1,008`-cell grid ($n = 2..113, D = 2..10$) confirms `485` populated entries (`73` `Yes`, `379` `No (Scott)`, `30` `No (Shadow)`, `1` `No`, `2` `Unknown` at `(11, 3)` and `(8, 6)`) and `523` blank cells. Both `(9, 10)` and `(11, 10)` are blank in `claim/ame_table_live.html`.
- Markus Grassl's `codetables.de` covers only prime-power dimensions $D \in \{2, 3, 4, 5, 7, 8, 9\}$ and has no tables for composite dimension $D = 10$.
- Recent 2026 preprints (`arXiv:2608.01011`, `arXiv:2608.05781`, `arXiv:2609.11796`) settle `(7, 6)`, `(7, 10)`, `(11, 6)`, `(12, 10)`, and prime-power cells, leaving `(9, 10)` and `(11, 10)` open prior to this work.

**Verification of Exact $\operatorname{AME}(9, 10)$ (`claim/ame_9_10_certificate.json`):**
- **Algebraic Closed Form in $\mathbb{Q}(\zeta_5)$:** The state $\lvert\Psi_{9,10}\rangle = \frac{1}{2}\sum_{\alpha=0}^{3} \lvert\psi_\alpha\rangle \otimes Z_5(\alpha c_9)\lvert G_5^{(9)}\rangle$ has exact cyclotomic coefficients in $\mathbb{Q}(\zeta_5)$ ($\zeta_5 = e^{2\pi i / 5}$) with overall normalization $10^{-9/2}$.
- **Binary Factor (`[[9, 2, 3]]_2`, $d^\perp = 5 = k + 1$):** All `7` binary stabilizer generators have $\mathbb{F}_2$-rank `7` and commute pairwise alongside the `2` logical operators $\bar{Z}_1, \bar{Z}_2$. Exhaustive enumeration of all $2^7 = 128$ stabilizer group elements confirms weight distribution $A_0 = 1, A_1 = A_2 = A_3 = A_4 = 0, A_5 = 18, A_6 = 36, A_7 = 36, A_8 = 27, A_9 = 10$ ($d^\perp = 5$). Exhaustive enumeration of all $2^{11} = 2,048$ normalizer elements confirms dual weight distribution $A_0^\perp = 1, A_3^\perp = 12, A_4^\perp = 90, A_5^\perp = 252, A_6^\perp = 456, A_7^\perp = 612, A_8^\perp = 477, A_9^\perp = 148$ (minimum non-stabilizer weight $d = 3$). The four integer basis vectors $s_0, s_1, s_2, s_3 \in \{-1, 0, +1\}^{512}$ satisfy $s_\alpha \cdot s_\beta = 128\,\delta_{\alpha\beta}$, are $+1$ eigenstates of all 7 generators, and satisfy $\sum_{\alpha=0}^3 \operatorname{Tr}_{S^c}(\lvert\tilde{\psi}_\alpha\rangle\langle\tilde{\psi}_\alpha\rvert) = 32 \cdot I_{16}$ in exact integer arithmetic on all $\binom{9}{4} = 126 / 126$ cuts, with off-diagonal blocks $\operatorname{Tr}_{S^c}(\lvert\tilde{\psi}_\alpha\rangle\langle\tilde{\psi}_\beta\rvert)$ ($\alpha \neq \beta$) vanishing identically on `54 / 126` cuts and nonzero on `72 / 126` active cuts.
- **Quinary Shifted Graph Factor (`[[9, 0, 5]]_5` + $c_9 \to$ Pure `[[9, 1, 5]]_5$):** The symmetric zero-diagonal adjacency matrix $\Gamma_9 \in \mathbb{F}_5^{9 \times 9}$ is verified to be locally Clifford equivalent (via Fourier transform on $\{0, 1, 2\}$) to the `codetables.de` `[[9, 0, 5]]_5` stabilizer code. With shift vector $c_9 = (0, 0, 0, 1, 4, 4, 3, 1, 1) \in \mathbb{F}_5^9$, every $5 \times 5$ augmented matrix $\begin{pmatrix} (\Gamma_9)_{S^c, S} & (c_9)_{S^c} \end{pmatrix}$ over $\mathbb{F}_5$ has nonzero determinant $\det_{\mathbb{F}_5} \in \{1, 2, 3, 4\}$ across all `126 / 126` four-party cuts (including all `72 / 72` active cuts). By Theorem 1, $T_{\alpha,\beta}^S = 0$ identically for all $\alpha \neq \beta$ and $\rho_S = 10^{-4} I_{10^4}$ with `0` algebraic error across all `126 / 126` cuts.
- **Independent Dense $5^9 = 1,953,125$-Vector Contraction:** Contracting the explicit $5^9$-component state vector across all `126 / 126` cuts in `complex128` (`16.58s` total runtime) confirms maximum elementwise error $2.82 \times 10^{-18}$, maximum quinary block Frobenius error $\lVert T_{\alpha,\alpha}^S - 5^{-4} I_{625}\rVert_F = 9.59 \times 10^{-17}$ and $\lVert T_{\alpha,\beta}^S\rVert_F = 6.72 \times 10^{-17}$, and maximum full $10^4 \times 10^4$ coupled reduced density matrix Frobenius error $\max_S \lVert \rho_S - 10^{-4} I_{10000}\rVert_F = 2.40 \times 10^{-17} \ll 10^{-12}$.

**Verification of Exact $\operatorname{AME}(11, 10)$ and Pure `[[11, 1, 6]]_5` (`claim/ame_11_10_certificate.json`):**
- **Parent `[12, 6, 7]_{25}` Hermitian Self-Dual MDS Code:** The $6 \times 6$ matrix $A_5$ over $\mathbb{F}_{25} = \mathbb{F}_5[\alpha]/(\alpha^2 + \alpha + 2)$ satisfies $A_5 A_5^\dagger = -I_6 \pmod 5$ and has nonzero determinant across all $\sum_{j=1}^6 \binom{6}{j}^2 = 923 / 923$ square submatrices over $\mathbb{F}_{25}$.
- **Punctured Pure `[[11, 1, 6]]_5` Quantum MDS Code:** The 10 shortened stabilizer generators over $\mathbb{F}_5$ are verified to lie in the parent `[[12, 0, 7]]_5` stabilizer space, commute pairwise, and have full symplectic rank `10` on $S^c$ across all $\binom{11}{5} = 462 / 462$ five-party cuts. In canonical graph-plus-shift form with $\Gamma_{11} \in \mathbb{F}_5^{11 \times 11}$ and $c_{11} = (2, 0, 2, 2, 3, 1, 1, 4, 4, 1, 2) \in \mathbb{F}_5^{11}$, every $6 \times 6$ augmented matrix $\begin{pmatrix} (\Gamma_{11})_{S^c, S} & (c_{11})_{S^c} \end{pmatrix}$ has $\det_{\mathbb{F}_5} \in \{1, 2, 3, 4\} \not\equiv 0 \pmod 5$ across all `462 / 462` five-party cuts, strictly improving the `codetables.de` lower bound `[[11, 1, 5]]_5` ($d = 5 \to 6$).
- **Binary Factor (`[[11, 1, 5]]_2`, $d^\perp = 6 = k + 1$) and Coupling:** Exhaustive enumeration of all $2^{10} = 1,024$ elements of $\mathcal{S}_{11}$ confirms $A_0 = 1, A_6 = 198, A_8 = 495, A_{10} = 330$ ($d^\perp = 6$), and the $\bar{Z}_{11}$ logical coset has minimum weight $d = 5$. The two integer basis vectors $t_0, t_1 \in \{-1, 0, +1\}^{2048}$ satisfy $\operatorname{Tr}_{S^c}(\lvert\tilde{\psi}_0\rangle\langle\tilde{\psi}_0\rvert + \lvert\tilde{\psi}_1\rangle\langle\tilde{\psi}_1\rvert) = 64 \cdot I_{32}$ across all `462 / 462` cuts, with off-diagonal block $\operatorname{Tr}_{S^c}(\lvert\tilde{\psi}_0\rangle\langle\tilde{\psi}_1\rvert)$ vanishing on `333 / 462` cuts and nonzero on `129 / 462` active cuts — all `462 / 462` of which are annihilated by $T_{0,1}^S = 0$ via $\det_{\mathbb{F}_5} \neq 0$, yielding $\rho_S = 10^{-5} I_{10^5}$ with `0` algebraic error across all `462 / 462` cuts.

### 1.3 Enumerated Partial Win `p2` Verification (Subsumed)

The audit in `claim/huber_wyderka_settled_blanks_audit.json` (`18,153` bytes) and `claim/huber_wyderka_settled_blanks_audit.tsv` (`6,022` bytes) covers all `1,008` cells ($n = 2..113, D = 2..10$):
- **Pure `codetables.de` $k=0$ Stabilizer States (`4` cells):** Full symplectic rank $\operatorname{rank}_{\mathbb{F}_D}(G_{S^c}) = n - k$ (`0` bad cuts) verified directly from cached generator tables across all cuts for `[[11, 0, 6]]_4` (`462 / 462` cuts over $\mathbb{F}_2$), `[[11, 0, 6]]_5` (`462 / 462` cuts over $\mathbb{F}_5$), `[[13, 0, 7]]_5` (`1,716 / 1,716` cuts over $\mathbb{F}_5$), and `[[14, 0, 8]]_5` (`3,432 / 3,432` cuts over $\mathbb{F}_5$).
- **Impure `codetables.de` $k=0$ False Positives (`2` cells, correcting Fig. 1 of `arXiv:2609.11796`):**
  - `[[15, 0, 8]]_5`: Generator row `9` (`0`-indexed) has symplectic support $\{4, 8, 9, 11, 12, 13, 14\}$ of weight $w_{\text{pure}} = 7$ (strictly below target distance $8$), causing `190 / 6,435` seven-party cuts to have rank $14$ instead of $15$.
  - `[[15, 0, 8]]_7`: Generator row `14` (`0`-indexed) has symplectic support $\{14\}$ of weight $w_{\text{pure}} = 1$ (strictly below target distance $8$), making the state a separable product $\lvert\operatorname{AME}(14, 7)\rangle \otimes \lvert +\rangle_{15}$ and causing `3,003 / 6,435` seven-party cuts to have rank $14$ instead of $15$.
- **Recent 2026 Literature (`16` cells) & New Exact States (`2` cells):** Total of `22` positively settled blank cells, plus `2` stabilizer upper-bound exclusions (`[[11, 0, 4..5]]_3` and `[[8, 0, 4]]_4`) and `0` unrecorded Scott bound violations across all `525` blank/`Unknown` cells.

---

## 2. Null Models, Perturbation Controls, and Hidden Quantifier Check

1. **Unshifted Coupling Null Control ($c = 0$):** Setting $c = 0$ leaves $T_{\alpha,\beta}^S \neq 0$ on every active cut, passing `0 / 72` active cuts for `AME(9, 10)` and `0 / 129` active cuts for `AME(11, 10)`.
2. **Uniform Random Shift Vector Null Model (`400` trials):**
   - For `AME(9, 10)` in $\mathbb{F}_5^9$: `0 / 400` random vectors pass all `72` active cuts under both `seed = 42` (mean `57.53 / 72`, max `69 / 72`) and `seed = 20261020` (mean `57.62 / 72`, max `66 / 72`), compared to `72 / 72` active cuts and `126 / 126` total cuts for $c_9 = (0, 0, 0, 1, 4, 4, 3, 1, 1)$.
   - For `AME(11, 10)` in $\mathbb{F}_5^{11}$ (`seed = 20261020`): `0 / 400` random vectors pass all `129` active cuts (mean `103.19 / 129`, max `116 / 129`), compared to `129 / 129` active cuts and `462 / 462` total cuts for $c_{11} = (2, 0, 2, 2, 3, 1, 1, 4, 4, 1, 2)$.
3. **Hidden Quantifiers & Stretched Definitions:** None found. Both states are genuine normalized pure states in $(\mathbb{C}^{10})^{\otimes 9}$ and $(\mathbb{C}^{10})^{\otimes 11}$ with exact cyclotomic amplitudes in $\mathbb{Q}(\zeta_5)$ satisfying the exact AME definition on every $k$-party subset $S$.

pass: true
