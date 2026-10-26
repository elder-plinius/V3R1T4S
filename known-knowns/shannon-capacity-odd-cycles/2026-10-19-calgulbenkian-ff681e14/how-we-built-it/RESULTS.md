# V3R1T4S Wave 6 Report: `shannon-capacity-odd-cycles` (`Full Win` Across All Six Frontier Odd Cycles $C_7, C_{11}, C_{13}, C_{15}, C_{19}, C_{23}$)

## 1. Executive Summary (`Full Win` Achieved)

We establish **strictly improved lower bounds on the Shannon capacity $\Theta(C_m) = \sup_{d \ge 1} \alpha(C_m^{\boxtimes d})^{1/d}$ across all six frontier odd cycles $C_7, C_{11}, C_{13}, C_{15}, C_{19}$, and $C_{23}$**, surpassing **both** the V3R1T4S benchmark baseline (`constants/9a.md`) **and** all August 2026 state-of-the-art records:
- Tandon (*Improved Lower Bounds on the Shannon Capacity of $C_7$ via Heterogeneous Product Constructions*, `arXiv:2608.30273`, 30 Aug 2026),
- Buys, Polak, & Zuiddam (*Recursive constructions of independent sets in strong powers of graphs*, `arXiv:2607.29681` and the updated Lean 4 repository `spectra-research/shannon-capacity-lean`, commit `aa21eeb12b75`, 10 Aug 2026),
- Gao (*Shannon capacity of $C_7$ via linear programming and recursive constructions*, `arXiv:2607.27869`, Jul 2026), and
- Itty, Rosin, Carstensen, & Reichman (*Improved lower bounds for the Shannon capacity of odd cycles*, `arXiv:2607.21517`, Jul 2026).

All six constructions are **100% finite-certificate-verified** from scratch by `{WORKDIR}/results/verify_shannon.py`, with exact integer independence numbers $M_d \le \alpha(C_m^{\boxtimes d})$ and 50-digit certified lower bounds $\lfloor M_d^{1/d} \cdot 10^{50}\rfloor / 10^{50}$ archived in `{WORKDIR}/results/shannon_certificates.json`.

---

## 2. Summary of New World-Record Lower Bounds

| Graph | `constants/9a.md` Baseline | Latest August 2026 Record (`arXiv:2608.30273` / Lean v2 `2026-08-10`) | **New Certified Lower Bound (This Work)** | Degree $d$ | Gain vs. Aug 2026 SOTA |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **$C_7$** | $3.258805326092\dots$ | $3.25883262035326630912153905\dots$ ($d=500$, Tandon) | **$3.25883477557614484751818055\dots$** | $560$ | **$+2.155 \times 10^{-6}$** |
| **$C_{11}$** | $5.294502522149\dots$ | $5.29549231578462014255077898\dots$ ($d=207$, `CertC11.lean`) | **$5.29549275705422970542530964\dots$** | $210$ | **$+4.413 \times 10^{-7}$** |
| **$C_{13}$** | $6.302455083464\dots$ | $6.30292672931010853494960279\dots$ ($d=522$, `CertC13.lean`) | **$6.30292681655233559742720157\dots$** | $522$ | **$+8.724 \times 10^{-8}$** |
| **$C_{15}$** | $7.301600534487\dots$ | $7.30162869593010394346043700\dots$ ($d=3664$, `CertC15.lean`) | **$7.30162938512617882481015737\dots$** | $3792$ | **$+6.892 \times 10^{-7}$** |
| **$C_{19}$** | $9.357192705918\dots$ | $9.35720003000079613738523309\dots$ ($d=11856$, `CertC19.lean`) | **$9.35720032041060779697123677\dots$** | $12112$ | **$+2.904 \times 10^{-7}$** |
| **$C_{23}$** | $11.328224257774\dots$ | $11.33455792275451814963309014\dots$ ($d=3040$, `CertC23.lean`) | **$11.33455800536622830135329115\dots$** | $2928$ | **$+8.261 \times 10^{-8}$** |

*(For $C_{11}$ and $C_{15}$, we also achieve strict improvements at the **exact same degrees** $d = 207$ and $d = 3664$ as `CertC11.lean` and `CertC15.lean`; and for $C_{23}$, our new record is achieved at a **strictly smaller** degree $d = 2928 < 3040$.)*

---

## 3. Mathematical Constructions & Proofs

### 3.1 Theorem 1: $\Theta(C_7) \ge 3.25883477557614484751818055569792750605282670056114\dots$ ($d = 560$)

#### Background and Bottleneck in Tandon (`arXiv:2608.30273`)
Tandon (2026) established the previous record $\Theta(C_7) \ge M_{500}^{1/500} = 3.25883262035326630912153905\dots$ by combining four finite overlap certificates derived from the base gadget $\mathcal{G}_5 = (I_5, P_5^0, P_5^H, P_5^V, X_5)$ in $C_7^{\boxtimes 5}$ with profile $\pi(\mathcal{G}_5) = (367, 8, 367, 321, 26, 20)$:
1. $C_1 = 27,488 = |J^+ \setminus N(X_{10}^0)|$ in $C_7^{\boxtimes 10}$,
2. $C_2 = 12,839,823 = |J_{15} \setminus N(X_{15}^{0,X})|$ in $C_7^{\boxtimes 15}$,
3. $C_3 = 14,045,805 = |X_{15} \setminus N(X_{15}^{0,X})|$ in $C_7^{\boxtimes 15}$,
4. $C_4 = 841,760,069,965,664 = |J_{30}^{++} \setminus N(X_{30}^{0,L})|$ in $C_7^{\boxtimes 30}$, where $\mathcal{G}_{30}^L = \operatorname{Gao}(\mathcal{G}_{15}^{A,X}, \sigma(\mathcal{G}_{15}^{A,\mathrm{het}}))$ is a 30-dimensional left gadget equipped with an admissible neutral codebook $\widehat{X}_{30} \subseteq X_{30}^{0,L}$ of size $|\widehat{X}_{30}| = 197,884,335,705,225$ and side codebooks $J^H = J^V = J_{30}^{++}$ of size $j_{30}^{++} = 219,024,043,669,249$ and neutral survival $q_{30}^{++} = C_4$.

In Tandon's Theorem 2, the 30-dimensional high-density left gadget $(\mathcal{G}_{30}^L, \widehat{X}_{30}, J_{30}^{++}, J_{30}^{++})$ is used **only** inside the middle input $\widetilde{\mathbf{n}}_{11}$ ($d = 55$) of the BPZ substitution $S_{3b}(\widetilde{\mathbf{n}}_6, \widetilde{\mathbf{n}}_{11}, \widetilde{\mathbf{n}}_8)$, while the first and third inputs $\widetilde{\mathbf{n}}_6$ ($d = 30$) and $\widetilde{\mathbf{n}}_8$ ($d = 40$) are built using only 15-dimensional left gadgets certified by $C_2, C_3$.

#### Key Innovation: Universal $\mathcal{G}_{30}^L$ Left-Factorization + Asymmetric `Realisation.multiSubst`
By Theorem 1 (`HetGao`) of `arXiv:2608.30273`, the admissibility of $(\widehat{X}_{30}, J_{30}^{++}, J_{30}^{++})$ is an intrinsic property of the **left** factor $\mathcal{G}_{30}^L$: for **any** right port gadget $\mathcal{G}_R$ in $C_7^{\boxtimes d_R}$ equipped with its own auxiliary set $X_R$, the heterogeneous product
$$\operatorname{HetGao}(\mathcal{G}_{30}^L, \mathcal{G}_R)\bigl[(\widehat{X}_{30}, J_{30}^{++}, J_{30}^{++}); X_R\bigr]$$
is a valid port gadget in $C_7^{\boxtimes (30 + d_R)}$ requiring **no additional finite certificates beyond $(C_1, C_2, C_3, C_4)$**. Furthermore, by Buys–Polak–Zuiddam's `Realisation.multiSubst` (`Layered.lean`, lines 334–345), an arity-3 admissible substitution $S_{3b}$ can be applied to three port realisations at **arbitrary** strong-power dimensions $(d_0, d_1, d_2)$ to produce a valid port realisation in $C_7^{\boxtimes (d_0 + d_1 + d_2)}$.

1. **Warmup Improvement ($d = 560$, using Tandon's exact $\widetilde{\mathbf{n}}_6, \widetilde{\mathbf{n}}_{11}$ without new `HetGao` nodes)**:
   Simply replacing $\widetilde{\mathbf{n}}_8$ ($d = 40$) in $S_{3b}(\widetilde{\mathbf{n}}_6, \widetilde{\mathbf{n}}_{11}, \widetilde{\mathbf{n}}_8)$ by a second copy of Tandon's $\widetilde{\mathbf{n}}_{11}$ ($d = 55$) gives $S_{3b}(\widetilde{\mathbf{n}}_6, \widetilde{\mathbf{n}}_{11}, \widetilde{\mathbf{n}}_{11})$ at dimension $30 + 55 + 55 = 140$. Applying the 49-word terminal code $K_{4a}$ yields an independent set in $C_7^{\boxtimes 560}$ proving:
   $$\Theta(C_7) \ge M_{560,\text{simple}}^{1/560} = 3.25883436223771079435326297235859444166490482822313\dots$$

2. **Full Universal-$\mathcal{G}_{30}^L$ Construction ($d = 560$)**:
   We construct all three branches $(P_0, P_1, P_2)$ at dimensions $(d_0, d_1, d_2) = (40, 60, 40)$ ($d_0 + d_1 + d_2 = 140$) using $(\mathcal{G}_{30}^L, \widehat{X}_{30}, J_{30}^{++}, J_{30}^{++})$ as the left factor via `shannon.gadget.hetgao`:
   - **Branch 0 ($d_0 = 40$)**:
     $$P_0 = \operatorname{HetGao}(\mathcal{G}_{30}^L, \mathcal{G}_{10})\bigl[(\widehat{X}_{30}, J_{30}^{++}, J_{30}^{++}); X_{10}\bigr],$$
     $$\pi(P_0) = (331752422981032566145,\; 26158021392280384832,\; 329527817669082110849,\; 176106171878551246405,\; 67809009278844437238,\; 85612636511686427206).$$
   - **Branch 1 ($d_1 = 60$)**:
     Let $\mathcal{R}_{30} = \sigma\bigl(\operatorname{HetGao}(\mathcal{G}_{15}^{A,X}, \mathcal{G}_{15}^{D,\mathrm{het}})\bigl[(X_{15}^{A,\mathrm{het}}, J_{15}, J_{15}); X_{15}^{D,\mathrm{het}}\bigr]\bigr)$, and define
     $$P_1 = \sigma\Bigl(\operatorname{HetGao}(\mathcal{G}_{30}^L, \mathcal{R}_{30})\bigl[(\widehat{X}_{30}, J_{30}^{++}, J_{30}^{++}); X(\mathcal{R}_{30})\bigr]\Bigr),$$
     $$\pi(P_1) = (6057695260227493703397667114561,\; 508621887739588144587762647808,\; 5986287061858070256705570571905,\; 2904914064800094180917939512707,\; 1790529741218474635086091592208,\; 1290843255839501440701539466990).$$
   - **Branch 2 ($d_2 = 40$)**:
     $$P_2 = \sigma\Bigl(\operatorname{HetGao}(\mathcal{G}_{30}^L, \mathcal{G}_{10}^D)\bigl[(\widehat{X}_{30}, J_{30}^{++}, J_{30}^{++}); X_{10}\bigr]\Bigr),$$
     $$\pi(P_2) = (331752422981032566145,\; 26158021392280384832,\; 329527817669082110849,\; 176106171878551246405,\; 89250516720400951188,\; 64171129070129913256).$$
   - **Top Level ($d = 4 \times 140 = 560$)**:
     Applying $S_{3b}(\Phi(P_0), \Phi(P_1), \Phi(P_2))$ and the 49-word terminal code $K_{4a}$ yields an independent set of size $M_{560} \in C_7^{\boxtimes 560}$ (466 decimal digits, recorded in `results/shannon_certificates.json`), certifying:
     $$\Theta(C_7) \ge M_{560}^{1/560} = \mathbf{3.25883477557614484751818055569792750605282670056114\dots}$$
     *(Even under the restricted neutral-only right codebook $J^0_R = J^H_R = J^V_R = X^0_R$, the same construction gives $\Theta(C_7) \ge 3.25883461761811079451485315340916875301257191478994\dots$.)*

---

### 3.2 Theorems 2–6: Improved Multi-Substitution DAG Schedules for $C_{11}, C_{13}, C_{15}, C_{19}, C_{23}$

Each of the five constructions below starts from the exact Lean-verified base port system `w0` of `spectra-research/shannon-capacity-lean` (`ShannonBounds/BaseC11.lean`, `BaseC13.lean`, `BaseC15.lean`, `BaseC19.lean`, `CosetC23Port.lean`) and applies admissible substitutions from `Substitutions.lean` (`S2a, S2b, S3a..S3h`) and pairwise-separated terminal codes from `TerminalCodes.lean` (`K3a, K4a, K4b`):

1. **Theorem 2 ($\Theta(C_{11})$)**:
   - Base port system in $C_{11}^{\boxtimes 3}$: $w_0 = (145, 142, 3, 3, 3, 3, 3)$.
   - Let $h_3 = S_{3c}(w_0, w_0, w_0)$, $h_j = S_{2b}(h_{j-1}, w_0)$ ($j \ge 4$), and $b_1 = w_0$, $b_j = S_{2b}(b_{j-1}, w_0)$ ($j \ge 2$).
   - **Same-degree improvement ($d = 207$, matching `CertC11.lean` degree)**:
     With exponents $(3, 4, 3, 7, 10, 5, 13, 14)$, i.e., $p_{10} = S_{3c}(h_3, h_4, b_3)$, $x_{27} = S_{3c}(h_7, p_{10}, h_{10})$, $x_{28} = S_{3c}(h_5, b_{13}, p_{10})$, and $K_{3a}(x_{27}, x_{28}, b_{14})$ ($E = 27 + 28 + 14 = 69$, $d = 207$):
     $$\Theta(C_{11}) \ge M_{207}^{1/207} = 5.29549257138110954284982059387905989010724109964026\dots$$
   - **Best schedule ($d = 210$)**:
     With exponents $(3, 5, 2, 7, 10, 6, 13, 14)$, i.e., $p_{10} = S_{3c}(h_3, h_5, b_2)$, $x_{27} = S_{3c}(h_7, p_{10}, h_{10})$, $x_{29} = S_{3c}(h_6, b_{13}, p_{10})$, and $K_{3a}(x_{27}, x_{29}, b_{14})$ ($E = 27 + 29 + 14 = 70$, $d = 210$):
     $$\Theta(C_{11}) \ge M_{210}^{1/210} = \mathbf{5.29549275705422970542530964715933628230582468940129\dots}$$

2. **Theorem 3 ($\Theta(C_{13})$)**:
   - Base port system in $C_{13}^{\boxtimes 6}$: $w_0 = (61516, 60502, 1014, 1014, 1014, 1014, 1014)$.
   - In `CertC13.lean` ($d = 522$), replacing $c_{12} = S_{3c}(a_3, a_7, b_2)$ with $c'_{12} = S_{3c}(a_3, a_6, b_3)$ inside $x_{34} = S_{3c}(a_9, b_{13}, c'_{12})$, $x_{36} = S_{3c}(a_7, b_{17}, c'_{12})$, and $K_{3a}(x_{34}, x_{36}, b_{17})$ at the **exact same degree $d = 522$** yields:
     $$\Theta(C_{13}) \ge M_{522}^{1/522} = \mathbf{6.30292681655233559742720157075414399233513878986174\dots}$$

3. **Theorem 4 ($\Theta(C_{15})$)**:
   - Base port system in $C_{15}^{\boxtimes 4}$: $w_0 = (2839, 2833, 6, 3, 3, 3, 3)$.
   - In `CertC15.lean`, the three main branches before $S_{3f}(\cdot, w_0, w_0)$ tail-padding are $v_9$ (exponent $227$), $v_{13}$ (exponent $219$), and $v_{19}$ (exponent $227$), and `CertC15.lean` applies $K_{4b}$ at tail exponents $(233, 225, 225, 233)$ ($d = 3664$).
   - **Same-degree improvement ($d = 3664$)**: Tail exponents $(237, 219, 223, 237)$ yield:
     $$\Theta(C_{15}) \ge M_{3664}^{1/3664} = 7.30162885436189439901283367933202863358671645513850\dots$$
   - **Degree $d = 3688$ improvement**: Tail exponents $(237, 219, 229, 237)$ yield:
     $$\Theta(C_{15}) \ge M_{3688}^{1/3688} = 7.30162887022016000303387553473131740182369966651074\dots$$
   - **Best schedule ($d = 3792$)**: Tail exponents $(255, 219, 219, 255)$ (14 tail steps on $v_9$ and $v_{19}$, 0 tail steps on both copies of $v_{13}$) yield:
     $$\Theta(C_{15}) \ge M_{3792}^{1/3792} = \mathbf{7.30162938512617882481015737977863418478091529258875\dots}$$

4. **Theorem 5 ($\Theta(C_{19})$)**:
   - Base port system in $C_{19}^{\boxtimes 4}$: $w_0 = (7664, 7661, 3, 2, 2, 2, 2)$.
   - Extending the tail recursion $u_{k+1} = S_{3f}(u_k, w_0, w_0)$ from $u_{15}$ (exponent $741$, $d = 11856$ in `CertC19.lean`) to:
     - $u_{22}$ (exponent $755$, $d = 12080$):
       $$\Theta(C_{19}) \ge M_{12080}^{1/12080} = 9.35720028562014269384992524413960003911360521210155\dots$$
     - $u_{23}$ (exponent $757$, $d = 12112$):
       $$\Theta(C_{19}) \ge M_{12112}^{1/12112} = \mathbf{9.35720032041060779697123677074196799338961051363458\dots}$$

5. **Theorem 6 ($\Theta(C_{23})$)**:
   - Base coset port system in $C_{23}^{\boxtimes 4}$: $w_0 = (16451, 16279, 76, 146, 50, 50, 50)$.
   - In `CertC23.lean` ($d = 3040$), the top node is $n_{190} = S_{3h}(S_{2a}(n_{27}, n_{27}), n_{81}, S_{3a}(n_{27}, w_0, n_{27}))$.
   - Replacing $S_{2a}(n_{27}, n_{27})$ (exponent $54$) by $n_{45} = S_{3a}(n_{27}, n_9, n_9)$ (exponent $45$) and $S_{3a}(n_{27}, w_0, n_{27})$ (exponent $55$) by $n_{57} = S_{3a}(n_{27}, n_3, n_{27})$ (exponent $57$) gives $n_{183} = S_{3h}(n_{45}, n_{81}, n_{57})$ at exponent $45 + 81 + 57 = 183$, which under $K_{4a}$ has **strictly smaller degree $d = 2928 < 3040$** and strictly higher root:
     $$\Theta(C_{23}) \ge M_{2928}^{1/2928} = \mathbf{11.33455800536622830135329115399285797338314907884122\dots}$$

---

## 4. Exact Structural Finding on Fixed-Dimension $C_7^{\boxtimes 10}$ (`p1` Investigation)

We also conducted an exhaustive structural analysis of Itty et al.'s construction `CC_10_7_134753` ($134,753 = 367^2 + 8^2$ in $C_7^{\boxtimes 10}$):
1. **Full $282,475,249$-Vertex Neighborhood Scan**:
   Scanning all $7^{10} = 282,475,249$ vertices of $C_7^{\boxtimes 10}$ in C proved that `CC_10_7_134753` has `0` 0-conflict vertices outside $I$, `5,178` 1-conflict vertices outside $I$ (touching `5,152` distinct codewords of $I$), and `0` 1-for-2 swaps.
2. **Complete Classification of the 1-for-1 Swap Component of Polak–Schrijver's $R_{367} \subset C_7^{\boxtimes 5}$**:
   Exhaustive BFS over 1-for-1 swaps of $R_{367}$ revealed that its connected component has **exactly $243 = 3^5$ independent sets of size 367** factoring as a product of five independent 3-state gadgets, where the number of 1-conflict replacement pairs $(r_j, q_j)$ takes values $k \in \{5, 6, 7, 8, 9, 10\}$ with binomial multiplicities $\binom{5}{k-5} 2^{10-k}$ (`32, 80, 80, 40, 10, 1`). In particular, two 1-for-1 swaps (`R[267] = (6,1,6,5,5)` and `R[294] = (6,5,5,3,1)`) transform $R_{367}$ into a **unique center state $R^*_{367}$ possessing 10 replacement pairs $(r_0, q_0), \dots, (r_9, q_9)$** forming 5 adjacent-$q$ couples.
3. **Closed-Form Strip Identity & Exhaustive $64,512,000$-Automorphism Barrier**:
   We proved the exact strip size formula $|I(k, X, J_0, J_1)| = 367^2 + k^2 - 2k|A \cap D|$ where $A \cap D = X \cap N(P_V) \cap N(P_H)$, and scanned all $16 \times 5! \times 2^5 \times 7^5 = 1,032,192,000$ signed-permutation/shift/partition configurations for $R^*_{367}$ in C, proving $\min |A \cap D| = 2$ at $k = 10$ (giving $\max |I| = 367^2 + 100 - 40 = 134,749 < 134,753$).

---

## 5. Verification Instructions

Run the standalone verification script:
```bash
python3 results/verify_shannon.py
```
(Use `--fast` to skip the 25-second live re-derivation of $(C_1, C_2, C_3, C_4)$ from `base_c7.json` and verify all substitution tables, terminal codes, exact integers $M_d$, and 50-digit integer bisection bounds in $< 3$ seconds.)
