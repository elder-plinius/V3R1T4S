# V3R1T4S Skeptic 2 (NOVELTY) Audit Report — `moore-graph-57`

- context: fresh subagent (7f8aad36-be8f-424e-aaba-456aae1540d3) invoked via invoke_subagent for independent V3R1T4S panel review
- **Verdict:** PASS
- **Target ID:** `moore-graph-57`
- **Run Directory:** `runs/2026-10-26-0351`

---

## 1. Scope Audited
1. Target specification: `repo/known-unknowns/graphs-games-automata/moore-graph-57.md`
2. Stage 1 Scout: `runs/2026-10-26-0351/scout.md`
3. Track `p2` attempt & code: `runs/2026-10-26-0351/attempts/lens1_p2_brauer_trace_rank_verification/report.md`, `verify_lens1_p2.py`, `lens1_output.json`
4. Track `p1` attempt & code: `runs/2026-10-26-0351/attempts/lens2_p1_automorphism_group_order_exclusions/report.md`, `verify_lens2_p1.py`, `lens2_output.json`
5. Postdiction & literature comparison: `runs/2026-10-26-0351/POSTDICTION.md`

---

## 2. Novelty & Literature Audit Findings

### 2.1 Track `p2`: Independent Executable Verification of `arXiv:2606.29183v2`
- **Prior Literature State:** Yawara Ishida's preprint *"No involutions in the missing Moore graph"* (`arXiv:2606.29183v2`, 8 July 2026) is a pure-mathematics paper with no accompanying computational artifact or verification script.
- **Verification Assessment:** `verify_lens1_p2.py` provides a genuine, independent, self-contained executable verification in 100% exact arithmetic (`fractions.Fraction` and exact $\mathbb{F}_p$ row-echelon elimination):
  - Independently constructs the Bose–Mesner algebra $\mathbb{Q}[I, A, J]$ and verifies $p$-integrality of $E_7 = (400I + 50A - J)/750$ and $E_{-8} = (455I - 65A + J)/975$.
  - Tests the Brauer-quotient trace–rank identity $\mathrm{tr}(T_g E_\theta) = \mathrm{rank}_{\mathbb{F}_p}(E_\theta[\mathrm{Fix}(g)] \bmod p)$ on explicit prime-order automorphisms of existing diameter-2 Moore graphs ($C_5$, Petersen $\mathrm{srg}(10,3,0,1)$, and Robertson's construction of Hoffman–Singleton $\mathrm{srg}(50,7,0,1)$).
  - Verifies Theorem 1.1 ($\mathrm{Fix}(t) \cong K_{1,55}$, $\mathrm{rank}_{\mathbb{F}_2}(975 E_{-8}[F] \bmod 2) = 54 \implies a_1(t) = -368 < 0$, ruling out all involutions), Theorem 1.2 ($p \in \{7, 11, 13, 19\}$), and all 11 rows of Section 8 Table 1 (including Remark 8.5 correcting Makhnev–Nosov 2004 on $\mathrm{srg}(352,26,0,2)$).
- **Verdict on `p2`:** Meets the `p2` criterion with genuine computational novelty.

### 2.2 Track `p1`: Novel Automorphism-Group Order & Composite Action Exclusions
- **Prior Literature State:**
  - **Makhnev & Paduchikh (2009, Theorem 1):** Left open 5 even-order families in Theorem 1(1), $|\mathrm{Aut}(\Gamma)| \in \{11, 55, 275\}$ ($G = C_{11} \times U$, $|U| \mid 25$) in Theorem 1(2)(iii) & Lemma 4.4, and $|\mathrm{Aut}(\Gamma)| \in \{7, 35, 175\}$ ($G \le C_7 \times U$, $|U| \mid 25$) or $F_{21}$ in Theorem 1(2)(iv) & Lemma 4.5.
  - **Mačaj & Širáň (2010):** Bounded $|\mathrm{Aut}(\Gamma)| \le 375$ (odd order) and $\le 110$ (even order), with candidate displacement tables in Lemma 12.
  - **Kováčiková (2015/2018, `arXiv:1812.05353`):** Refined $p=7$ to $49 \mid a_1(x)$ ($a_0(x) \in \{2,9,16,23,30,37\}$) via induced subgraphs of order $\le 10$, while explicitly leaving $|\mathrm{Aut}(\Gamma)| \in \{11, 55, 275\}$ open on p. 39.
  - **Ishida (2026, `arXiv:2606.29183v2`):** Proved Theorem 1.1 ($p=2$ excluded) and Theorem 1.2 (exact $a_1(x)$ for prime orders $p \in \{7, 11, 13, 19\}$), but did **not** analyze composite-order elements ($C_{55}, C_{65}, C_{35}$) or eliminate the odd group orders $275$ and $175$ from Makhnev–Paduchikh's classification.
- **Novel Contributions Verified in `lens2_p1`:**
  1. **Unconditional Exclusion of $|\mathrm{Aut}(\Gamma)| = 275$ ($C_{11} \times C_5^2$):** Proved independently of `arXiv:2606.29183` via two distinct exact arguments: (i) $\mathrm{HoSi}$ admits no automorphism of order $11$ ($50 \equiv 6 \pmod{11}$ and degree $7 < 11$ forces $\mathrm{Fix}_{\mathrm{HoSi}}(x)$ to be a union of connected components), so $G$ acts freely on $V(\Gamma) \setminus C_5$, contradicting $3245 \equiv 220 \not\equiv 0 \pmod{275}$; and (ii) character integrality plus $275 \mid a_1(x^k)$ forces $a_1(x^k) \ge 550 > 500$, contradicting Mačaj–Širáň Lemma 12 and the Abelian Orbit Chord Lemma ($3030$ disjoint vertices leave $220 < 275$).
  2. **Unconditional Exclusion of $|\mathrm{Aut}(\Gamma)| = 175$ ($C_7 \times C_5^2$):** Proved independently of `arXiv:2606.29183` by showing that free action of $U \cong C_5^2$ outside $\Omega = \mathrm{Fix}(U) \cong \mathrm{HoSi}$ forces $a_0(x) = 51$, $a_1^\Omega(x^k) = 7$, and $a_1(x^k) \equiv 7 \pmod{175}$ with $a_1(x^k) \equiv 2 \pmod{15} \implies a_1(x^k) \ge 182$, which requires $51 + 50 \times 56 + 3 \times 182 = 3397 > 3250$ pairwise-disjoint vertices.
  3. **Equivariant Galois–Brauer Rank Obstruction (Conditional on `arXiv:2606.29183` Theorem 4.1):** Generalizes Ishida's prime-order Brauer trace–rank identity to commuting automorphisms of distinct prime orders $(p, q)$ over $\mathbb{Z}_p[\zeta_q]$, proving $(q-1) \mid (\mathrm{rank}_{\mathbb{F}_p}(E_\theta[F]) - \mathrm{rank}_{\mathbb{F}_p}(E_\theta[F]\Pi_0[F]))$ and $\mathrm{tr}(T_{xf^j}E_\theta) = \hat{c}_0 - \hat{c}_1$. This excludes Case A ($\mathrm{Fix}(f) = \emptyset$) of $C_{55}$ ($4 \nmid (2 - 0)$, Fourier mode ranks $(0,0,1,1,0)$ over $\mathbb{F}_{11}$), pins down Case B of $C_{55}$ ($a_1(x^k f^j) = 55$, $a_1(f) = a_1(f^2) = 385$), rules out the $a_0(x) = 51$ branch of $C_{35}$, pins down $a_1(x^k f^j) = 42$ on the $a_0(x) = 16$ branch of $C_{35}$ (while correcting Makhnev–Paduchikh's congruence misprint $105u+35 \to 105u+70$), and pins down $a_1(x^k f^j) = 65$ and $a_0(f) = 0$ for $C_{65}$.
  4. **Explicit Separation of Dependencies:** Both `lens2_p1/report.md` and `verify_lens2_p1.py` cleanly separate Part I (100% unconditional, independent of `arXiv:2606.29183`) from Part II (conditional on `arXiv:2606.29183`), satisfying the `moore-graph-57` `p1` rule and Trap 3.

pass: true
