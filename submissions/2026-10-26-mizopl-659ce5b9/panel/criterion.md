# V3R1T4S Skeptic 3 (CRITERION) Audit Report — `moore-graph-57`

- context: fresh subagent (bac313c7-40c1-4b96-a9d3-3a3c5d4f73c1) invoked via invoke_subagent for independent V3R1T4S panel review
- **Verdict:** PASS
- **Target ID:** `moore-graph-57`
- **Run Directory:** `runs/2026-10-26-0351`

---

## 1. Audit Against `target.md` Clauses (`p1` and `p2`)
- **Main Success Criterion Boundary Respected:** `target.md` states that `CONFIRMED` (`CONFIRMED_SOLUTION`) is reserved for an explicit adjacency list on `3250` vertices with $A^2 + A - 56I = J$ or a formal Lean/Isabelle non-existence proof. `RESULT.md`, `claim/artifact.md`, and `claim/certificate.json` strictly claim `CONFIRMED_PARTIAL` (`p1, p2`) and do not claim a full solution.
- **Partial Win `p1` Clause Verification:**
  - *Requirement:* Computer-verified exclusion (reproducible code, exact arithmetic) of automorphisms of a specific odd prime order $p$, or of a specific automorphism-group order, not already excluded in `arXiv:2606.29183` and its references; if it relies on `arXiv:2606.29183` (unrefereed), the dependency must be stated.
  - *Audit:* **SATISFIED.** `claim/verify.py` (standard library only, exact `int`, `fractions.Fraction`, and $\mathbb{F}_p$ row-echelon arithmetic; exits `0` and prints `PASS` on its last line) and `claim/certificate.json` explicitly partition `track_p1_automorphism_group_order_exclusions` into:
    1. **`part_1_unconditional_exclusions_independent_of_2606_29183` (`depends_on_arxiv_2606_29183: false`):**
       - $|\mathrm{Aut}(\Gamma)| = 275$ ($G \cong C_{11} \times C_5^2$, left open in Makhnev–Paduchikh 2009 Thm. 1(2)(iii) & Lem. 4.4(2) and Kováčiková 2018 p. 39): excluded unconditionally via two independent proofs: (i) $50 \equiv 6 \pmod{11}$ and degree $7 < 11$ in $\mathrm{HoSi}$ rules out order-$11$ automorphisms of $\mathrm{HoSi}$, forcing $\mathrm{Fix}(g) \cong C_5$ for all $g \in G \setminus \{1\}$ and $3245 \equiv 220 \not\equiv 0 \pmod{275}$; (ii) free action on $S_1(x^k)$ plus $a_1(x^k) \equiv 10 \pmod{15}$ forces $a_1(x^k) \ge 550 > 500$ (violating Mačaj–Širáň 2010 Lemma 12) and consumes $\ge 5 + 275 + 5 \times 550 = 3030$ vertices, leaving $220 < 275$.
       - $|\mathrm{Aut}(\Gamma)| = 175$ ($G \cong C_7 \times C_5^2$, left open in Makhnev–Paduchikh 2009 Thm. 1(2)(iv) & Lem. 4.5(1)): excluded unconditionally via free action of $U \cong C_5^2$ on the $a_0(x)-1$ leaves of $\mathrm{Fix}(x)$ outside $\Omega = \mathrm{Fix}(U) \cong \mathrm{HoSi}$ forcing $a_0(x) = 51$, $a_1^\Omega(x^k) = 7$, and CRT on $a_1(x^k) \equiv 7 \pmod{175}$ and $a_1(x^k) \equiv 2 \pmod{15}$ forcing $a_1(x^k) \ge 182$ ($k=1,2,3$), which requires $51 + 50 \times 56 + 3 \times 182 = 2851 + 546 = 3397 > 3250$ vertices.
    2. **`part_2_conditional_exclusions_and_composite_obstructions_from_2606_29183` (explicitly marked conditional on `arXiv:2606.29183`):**
       - Excludes Case A ($\mathrm{Fix}(f) = \emptyset$) of $G \cong C_{55}$ ($|G| = 55$, Makhnev–Paduchikh 2009 Lem. 2.9(2)(ii) & Lem. 4.4(1)) via Equivariant Galois–Brauer divisibility $(q-1)=4 \nmid (2-0)=2$ (mode ranks $(0,0,1,1,0)$ over $\mathbb{F}_{11}$), and uniquely pins Case B ($\mathrm{Fix}(f) \cong C_5$) to $a_1(x^k f^j) = 55$ and $a_1(f) = a_1(f^2) = 385$ ($m_{0,0} = 28$).
       - Excludes the $a_0(x) = 51$ branch of $G \cong C_{35}$ ($|G| = 35$, Makhnev–Paduchikh 2009 Lem. 2.9(2)(i) & Lem. 4.5), pins the surviving $a_0(x) = 16$ branch ($a_1(x) = 147$, $a_1(x^k f^j) = 42$, $m_{0,0} = 46$), and corrects the printed congruence $\alpha_1(g) = 105u + 35$ to $105u + 70 \in \{70, 175, 280\}$.
       - Pins $G \cong C_{65}$ ($|G| = 65$, Makhnev–Paduchikh 2009 Lem. 2.9(2)(iii) & Lem. 4.3) to $a_0(f) = 0$, $a_1(x^k f^j) = 65$, and $\{a_1(f), a_1(f^2)\} = \{65, 260\}$ ($m_{0,0} = 27$).
       - Eliminates all even group orders $|G| \in \{2,4,6,10,12,20,22,38,50,100,110\}$ in Makhnev–Paduchikh (2009) Thm. 1(1) and reduces the Mačaj–Širáň (2010) even-order bound $|\mathrm{Aut}(\Gamma)| \le 110$ to $0$.
- **Partial Win `p2` Clause Verification:**
  - *Requirement:* An independent machine-checked (Lean/Isabelle) or fully reproducible exact-computation verification of the `arXiv:2606.29183` theorem that a Moore graph of degree 57 has no involutory automorphisms.
  - *Audit:* **SATISFIED.** `claim/verify.py` and `claim/certificate.json` independently verify from first principles in exact arithmetic:
    - Spectral idempotents $E_{57} = \frac{1}{3250}J$, $E_7 = \frac{400I + 50A - J}{750}$ ($\mathrm{denom} = 750 = 2 \cdot 3 \cdot 5^3$, $m_7 = 1729$), $E_{-8} = \frac{455I - 65A + J}{975}$ ($\mathrm{denom} = 975 = 3 \cdot 5^2 \cdot 13$, $m_{-8} = 1520$).
    - Brauer trace–rank identity $\mathrm{tr}(T_g E_\theta) = \mathrm{rank}_{\mathbb{F}_p}(E_\theta[\mathrm{Fix}(g)] \bmod p)$ on $C_5$, Petersen $\mathrm{srg}(10,3,0,1)$, and Hoffman–Singleton $\mathrm{srg}(50,7,0,1)$ ($5/5$ exact matches).
    - Theorem 1.1 & Corollary 6.1 ($p=2$): $\mathrm{Fix}(t) \cong K_{1,55}$ ($a_0(t) = 56$), combinatorial $a_1(t) = 112$ ($\chi_{-8}(t) = 22$), and $\mathrm{rank}_{\mathbb{F}_2}(975 E_{-8}[F] \bmod 2) = 54 \implies a_1(t) = -368 < 0$ (no involutions; $|\mathrm{Aut}(\Gamma)|$ is odd).
    - Theorem 1.2 ($p \in \{7, 11, 13, 19\}$) and all $11$ rows of Section 8 Table 1 (including Remark 8.5 on $\mathrm{srg}(352,26,0,2)$).

## 2. Preregistration Freeze & `null_test` Audit
- **Timestamp Ordering:** `PREREG.md` records `frozen_utc: 2026-10-26T03:31:15Z`, which strictly precedes all files in `attempts/` and `claim/`.
- **`null_test` Justification:** `PREREG.md` specifies `null_test: not needed because exact deterministic integer/rational and finite-field linear algebra verification has zero stochastic variance`.

## 3. Digit-for-Digit (`K12`) Consistency Audit
- `claim/certificate.json` SHA-256 is `659ce5b9f841936bf9b859ab527ab00183adad85edb7371ae2cddd035019b2a6`, matching `RESULT.md` and `claim/artifact.md` character-for-character.
- Every integer, rank, multiplicity, congruence, vertex count, and parameter tuple across `RESULT.md`, `claim/artifact.md`, and `claim/certificate.json` matches digit-for-digit (`0` discrepancies).

pass: true
