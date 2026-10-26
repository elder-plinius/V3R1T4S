# V3R1T4S Skeptic 1 (REPRODUCE) Audit Report — `moore-graph-57`

- context: fresh subagent (5fcf977c-02ef-47f1-89ef-19892ee2e49a) invoked via invoke_subagent for independent V3R1T4S panel review
- **Verdict:** PASS
- **Target ID:** `moore-graph-57`
- **Run Directory:** `runs/2026-10-26-0351`
- **Verification Script Audited:** `runs/2026-10-26-0351/claim/verify.py`
- **Certificate Audited:** `runs/2026-10-26-0351/claim/certificate.json` (`sha256: 659ce5b9f841936bf9b859ab527ab00183adad85edb7371ae2cddd035019b2a6`)

---

## 1. Executive Summary
I have read, executed, and audited all four target files:
1. `runs/2026-10-26-0351/claim/verify.py`
2. `runs/2026-10-26-0351/claim/certificate.json`
3. `runs/2026-10-26-0351/attempts/lens1_p2_brauer_trace_rank_verification/verify_lens1_p2.py`
4. `runs/2026-10-26-0351/attempts/lens2_p1_automorphism_group_order_exclusions/verify_lens2_p1.py`

Running `python3 runs/2026-10-26-0351/claim/verify.py` exited with code `0` (`PASS`), confirming a digit-for-digit match between the recomputed values and `claim/certificate.json`, as well as complete agreement with `lens1_output.json` and `lens2_output.json`.

---

## 2. Exact Arithmetic & Zero-Approximation Audit
- **Zero Floating-Point Usage:** Every calculation in `verify.py`, `verify_lens1_p2.py`, and `verify_lens2_p1.py` uses Python exact `int` arithmetic, `fractions.Fraction` for rational Bose–Mesner algebra and character-multiplicity calculations, and exact modular inverse `pow(x, -1, p)` Gaussian elimination (`rank_mod_p`) over $\mathbb{F}_p$. No `float`, `/`, `math.sqrt`, or numerical tolerances exist anywhere in the codebase.

---

## 3. Track `p2` Mathematical & Computational Audit (`arXiv:2606.29183v2`)
- **Bose–Mesner Idempotents:** Verified exact SRG feasibility, eigenvalues, multiplicities, idempotency ($E_i^2 = E_i$), orthogonality ($E_i E_j = 0$), completeness ($\sum E_i = I$), and primitive integer coefficients (`gcd = 1`) for $\mathrm{srg}(3250, 57, 0, 1)$ ($E_7 = \frac{1}{750}(400I + 50A - J)$, $E_{-8} = \frac{1}{975}(455I - 65A + J)$) and all auxiliary SRG families.
- **Existing Moore Graphs:** Verified $\mathrm{tr}(T_g E_\theta) = \mathrm{rank}_{\mathbb{F}_p}(E_\theta[\mathrm{Fix}(g)])$ on $C_5$ ($p=2$, $\mathrm{rk}=0$), Petersen $\mathrm{srg}(10,3,0,1)$ ($p=2$ transposition $\mathrm{rk}=2$, $p=2$ double transposition $\mathrm{rk}=0$, $p=5$ 5-cycle $\mathrm{rk}=0$), and Hoffman–Singleton $\mathrm{srg}(50,7,0,1)$ ($p=2$ involution with $\mathrm{Fix}=K_{1,5}$, $\mathrm{rk}=4$).
- **Theorem 1.1 (No Involutions, $p=2$):** Verified that an involution $t$ on $\mathrm{srg}(3250, 57, 0, 1)$ combinatorially requires $a_0(t)=56$, $\mathrm{Fix}(t)=K_{1,55}$, $a_1(t)=112$, and $\chi_{E_{-8}}(t)=22$ (with $a_1(t)=0$ ruled out across all closed subgraphs), whereas $\mathrm{rank}_{\mathbb{F}_2}(975 E_{-8}[K_{1,55}]) = 54$, forcing $a_1(t) = -368 < 0$.
- **Theorem 1.2 (Odd Primes $p \in \{7, 11, 13, 19\}$):**
  - $p=7$: Verified $\mathrm{rank}_{\mathbb{F}_7}(975 E_{-8}[K_{1,a_0-1}]) = 1$ and $\mathrm{rank}_{\mathbb{F}_7}(750 E_7[K_{1,a_0-1}]) = a_0 - 2$ for all $a_0 \equiv 2 \pmod 7$, forcing $a_1(g) = 7a_0 + 35$ and disjoint vertex bound $78a_0 + 49 \le 3250 \implies a_0 \in \{2,9,16,23,30,37\}$ (excluding $a_0 \in \{44, 51\}$).
  - $p=11$: Verified $\mathrm{Fix}(g)=C_5$, $\mathrm{rk}_{\mathbb{F}_{11}}(E_{-8}[C_5]) = \mathrm{rk}_{\mathbb{F}_{11}}(E_7[C_5]) = 2$, forcing $a_1(g)=55$ (excluding $220, 385$).
  - $p=13$: Verified $\mathrm{Fix}(g)=\emptyset$, $\mathrm{rk}_{\mathbb{F}_{13}}(E_7[\emptyset]) = 0$, forcing $a_1(g)=65$ (excluding $260, 455$), and confirmed $E_{-8}$ is non-$13$-integral with trace $-1$.
  - $p=19$: Verified $\mathrm{Fix}(g)=K_1$, $\mathrm{rk}_{\mathbb{F}_{19}}(E_{-8}[K_1]) = \mathrm{rk}_{\mathbb{F}_{19}}(E_7[K_1]) = 0$, forcing $a_1(g)=57$ (excluding $342$).
- **Section 8 Table 1:** Verified all 11 rows across $\mathrm{srg}(162, 21, 0, 3)$, $\mathrm{srg}(352, 26, 0, 2)$ (including Remark 8.5 correcting Makhnev–Nosov 2004 Lemmas 2.2 and 2.3(1)), $\mathrm{srg}(1276, 50, 0, 2)$, $\mathrm{srg}(99, 14, 1, 2)$, and $\mathrm{srg}(640, 243, 66, 108)$.

---

## 4. Track `p1` Mathematical & Computational Audit
- **Part I (Unconditional Exclusions, Independent of `arXiv:2606.29183`):**
  - **Abelian Orbit Chord Lemma:** Verified on $C_{11} \times C_5^2$ and $C_7 \times C_5^2$ that in any girth-5 graph ($\lambda=0, \mu=1$), a regular orbit of an odd-order abelian group has at most one inverse pair $\{g, g^{-1}\}$ of chords, ensuring $S_1(g)$ is pairwise disjoint across non-inverse elements on the free locus.
  - **Unconditional Exclusion of $|\mathrm{Aut}(\Gamma)| = 275$ ($C_{11} \times C_5^2$):** Verified both (1) that $\mathrm{HoSi}$ admits no order-11 automorphism ($50 \equiv 6 \pmod{11}$ and $k_{\mathrm{HoSi}}=7<11$), forcing $\mathrm{Fix}(g)=C_5$ for all $g \in G \setminus \{1\}$ and $275 \mid (3250-5)=3245$, impossible since $3245 \bmod 275 = 220 \ne 0$; and (2) that $275 \mid a_1(x^k)$ with $a_1(x^k) \equiv 10 \pmod{15}$ forces $a_1(x^k) \ge 550 > 500$ and $5 \cdot 550 + 5 + 275 = 3030$ vertices, leaving $220 < 275$.
  - **Unconditional Exclusion of $|\mathrm{Aut}(\Gamma)| = 175$ ($C_7 \times C_5^2$):** Verified that $\Omega = \mathrm{Fix}(U) = \mathrm{HoSi}$ forces $a_0(x)=51$ ($m=50$ leaves outside $\Omega$) and $a_1^\Omega(x^k)=7$, so $a_1(x^k) \equiv 7 \pmod{175}$ and $a_1(x^k) \equiv 2 \pmod{15} \implies a_1(x^k) \ge 182$ by CRT $\pmod{525}$. Disjoint vertex count $51 + 50 \cdot 56 + 3 \cdot 182 = 2851 + 546 = 3397 > 3250$ gives an unconditional contradiction.
- **Part II (Conditional Exclusions & Composite Galois–Brauer Obstructions):**
  - **$C_{55}$ ($|G|=55$):** Verified Fourier mode ranks $[0,0,1,1,0]$ over $\mathbb{F}_{11}$ in Case A ($\mathrm{Fix}(f)=\emptyset$), excluding Case A via $4 \nmid (2-0)$ (and $55 \nmid 230$), and pinning Case B ($\mathrm{Fix}(f)=C_5$) to $a_1(x^k f^j)=55$ and $a_1(f)=a_1(f^2)=385$ ($m_{0,0}=28$).
  - **$C_{65}$ ($|G|=65$):** Verified $a_0(f)=0$, $a_1(x^k f^j)=65$, and $\{a_1(f), a_1(f^2)\} = \{65, 260\}$ ($m_{0,0}=27$).
  - **$C_{35}$ ($|G|=35$):** Verified exclusion of $a_0(x)=51$, pinning of $a_0(x)=16, a_1(x)=147, a_1(x^k f^j)=42$, and correction of Makhnev–Paduchikh Lemma 2.9(2)(i) congruence from $105u+35$ to $105u+70 \in \{70, 175, 280\}$ ($m_{0,0}=46$).
  - **Even-Order Groups:** Verified exclusion of all 11 even orders $[2, 4, 6, 10, 12, 20, 22, 38, 50, 100, 110]$.

pass: true
