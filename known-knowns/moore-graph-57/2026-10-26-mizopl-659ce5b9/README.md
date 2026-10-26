# Unconditional & Galois–Brauer Exclusions of Automorphism Group Orders in the Missing Moore Graph (`srg(3250, 57, 0, 1)`) and Independent Exact Computational Verification of `arXiv:2606.29183v2` (`moore-graph-57`)

## What

Certified Partial Wins (p1, p2) on moore-graph-57 (srg(3250, 57, 0, 1); indexed in object/certificate.json sha256 659ce5b9f841936bf9b859ab527ab00183adad85edb7371ae2cddd035019b2a6 and verified on a 16 GB M1 laptop using the open-source we* engine at https://github.com/mizopl/we-star), verified in 100% exact integer, rational (fractions.Fraction), and finite-field (F_p Gaussian elimination) arithmetic with zero floating-point approximations: (1) Partial Win p1 (Computer-verified exclusions of automorphism-group orders and composite actions not excluded in arXiv:2606.29183v2 or Makhnev-Paduchikh 2009 / Macaj-Siran 2010 / Kovacikova 2018, explicitly separating unconditional and conditional exclusions) — (a) Part I (Unconditional, independent of arXiv:2606.29183): proved the Abelian Orbit Chord Lemma for girth-5 graphs (lambda=0, mu=1), unconditionally excluded |Aut(Gamma)| = 275 (G = C_11 x C_5^2, Makhnev-Paduchikh 2009 Theorem 1(2)(iii) & Lemma 4.4(2); Kovacikova 2018 p. 39) via both 11 not dividing |Aut(HoSi)| (50 == 6 mod 11 and degree 7 < 11 forcing Fix(g) = C_5 for all g in G \ {1} and 3245 mod 275 = 220 != 0) and 275 | a_1(x^k) with a_1(x^k) == 10 (mod 15) forcing a_1(x^k) >= 550 > 500 (consuming >= 3030 vertices and leaving 220 < 275), and unconditionally excluded |Aut(Gamma)| = 175 (G = C_7 x C_5^2, Makhnev-Paduchikh 2009 Theorem 1(2)(iv) & Lemma 4.5(1)) by proving that free action of U = C_5^2 on the leaves of Fix(x) outside Omega = Fix(U) = HoSi forces a_0(x) = 51, a_1^Omega(x^k) = 7, and CRT on a_1(x^k) == 7 (mod 175) and a_1(x^k) == 2 (mod 15) forces a_1(x^k) >= 182 (k=1,2,3), requiring 51 + 50*56 + 3*182 = 3397 > 3250 pairwise-disjoint vertices; (b) Part II (Conditional, building on arXiv:2606.29183): established the Equivariant Galois-Brauer Rank Obstruction for commuting automorphisms of distinct prime orders (p != q) over Z_p[zeta_q], proving (q-1) | (rank_{F_p}(E_theta[F]) - rank_{F_p}(E_theta[F] Pi_0[F])) and tr(T_{x f^j} E_theta) = c_0 - c_1, which excludes Case A (Fix(f) = empty) of G = C_55 (Makhnev-Paduchikh 2009 Lemma 2.9(2)(ii) & Lemma 4.4(1)) via 4 not dividing (2 - 0) (Fourier mode ranks [0,0,1,1,0] mod 11) and uniquely pins Case B (Fix(f) = C_5) to a_1(x^k f^j) = 55 and a_1(f) = a_1(f^2) = 385 (m_{0,0} = 28), excludes the a_0(x) = 51 branch of G = C_35 and pins the surviving a_0(x) = 16 branch to a_1(x) = 147 and a_1(x^k f^j) = 42 while correcting the Makhnev-Paduchikh Lemma 2.9(2)(i) congruence misprint 105u+35 to 105u+70 in {70, 175, 280} (m_{0,0} = 46), pins G = C_65 to a_0(f) = 0, a_1(x^k f^j) = 65, and {a_1(f), a_1(f^2)} = {65, 260} (m_{0,0} = 27), and eliminates all 11 even orders <= 110 in Makhnev-Paduchikh Theorem 1(1); and (2) Partial Win p2 (Independent exact computational verification of arXiv:2606.29183v2) — verified the Bose-Mesner idempotents E_7 = (400I+50A-J)/750 and E_{-8} = (455I-65A+J)/975, the Brauer trace-rank identity on C_5, Petersen srg(10,3,0,1), and Hoffman-Singleton srg(50,7,0,1), Theorem 1.1 & Corollary 6.1 (Fix(t) = K_{1,55}, rank_{F_2}(975 E_{-8}[F] mod 2) = 54 => a_1(t) = -368 < 0, ruling out all involutions), Theorem 1.2 for p in {7, 11, 13, 19}, and all 11 rows of Section 8 Table 1 across 5 open SRG families including Remark 8.5.

---

### Why This Finding Matters Beyond the Benchmark Score / Target: Methodological & Mathematical Significance (Note for @elder-plinius)

1. **Closing Two Long-Standing Odd-Order Cases ($|\mathrm{Aut}(\Gamma)| \in \{275, 175\}$) Unconditionally:**
   - In Theorem 1(2) of Makhnev & Paduchikh (*Proc. Steklov Inst. Math.* **267** (2009), S149–S163) and Kováčiková (`arXiv:1812.05353`, 2015/2018, p. 39), the odd-order classification of $\mathrm{Aut}(\Gamma)$ for $\Gamma = \mathrm{srg}(3250, 57, 0, 1)$ left open $G \cong C_{11} \times C_5^2$ ($|G| = 275$, Lemma 4.4(2)) and $G \cong C_7 \times C_5^2$ ($|G| = 175$, Lemma 4.5(1)).
   - We show that **both $|G| = 275$ and $|G| = 175$ are impossible unconditionally** (without even invoking `arXiv:2606.29183`):
     - For $|G| = 275$, the Hoffman–Singleton graph $\mathrm{HoSi} = \mathrm{srg}(50, 7, 0, 1)$ has $50 \equiv 6 \pmod{11}$ and degree $7 < 11$, so no order-$11$ automorphism can act non-trivially on $\mathrm{HoSi}$. Thus $\mathrm{Fix}(g) = \mathrm{Fix}(x) \cong C_5$ ($5$ vertices) for **every** $g \in G \setminus \{1\}$, forcing $G$ to act freely on $V(\Gamma) \setminus C_5$ ($3245$ vertices) — which fails $275 \mid 3245$ ($3245 \equiv 220 \pmod{275}$) and independently forces $a_1(x^k) \ge 550 > 500$.
     - For $|G| = 175$, free action of $U \cong C_5^2$ on the $a_0(x)-1$ leaves of $\mathrm{Fix}(x) \cong K_{1, a_0(x)-1}$ outside $\Omega = \mathrm{Fix}(U) \cong \mathrm{HoSi}$ uniquely forces $a_0(x) = 51$, and Chinese Remainder Theorem compatibility between $a_1(x^k) \equiv 7 \pmod{175}$ and $a_1(x^k) \equiv 2 \pmod{15}$ forces $a_1(x^k) \ge 182$ ($k = 1, 2, 3$), requiring $51 + 50 \times 56 + 3 \times 182 = 3397 > 3250$ pairwise-disjoint vertices.

2. **Extending the Broué–Ishida Brauer-Quotient Method from Prime Orders $p$ to Composite Orders $p \cdot q$ (The Equivariant Galois–Brauer Rank Obstruction):**
   - Ishida (`arXiv:2606.29183v2`, Theorem 4.1) applies the Brauer quotient over $\mathbb{Z}_p$ to a single automorphism $x$ of prime order $p$.
   - We show that when $x$ ($|x| = p$) commutes with an automorphism $f$ of distinct prime order $q \ne p$, working over the unramified cyclotomic discrete valuation ring $\mathcal{O} = \mathbb{Z}_p[\zeta_q]$ and applying the Brauer quotient to the $q$ orthogonal $f$-isotypic idempotents $E_\theta \Pi_r$ ($\Pi_r = \frac{1}{q}\sum_{j=0}^{q-1} \zeta_q^{-rj} T_f^j$) yields integer ranks $\hat{c}_r = \mathrm{rank}_\kappa(E_\theta[F]\Pi_r[F] \bmod p) \in \mathbb{Z}_{\ge 0}$ that must be invariant under $\mathrm{Gal}(\mathbb{Q}(\zeta_q)/\mathbb{Q})$ ($\hat{c}_1 = \hat{c}_2 = \dots = \hat{c}_{q-1}$).
   - This produces a new **mod-$(q-1)$ divisibility obstruction** on $\mathrm{Fix}(x)$, $(q - 1) \mid (\mathrm{rank}_{\mathbb{F}_p}(E_\theta[F]) - \hat{c}_0)$, which immediately eliminates Case A ($\mathrm{Fix}(f) = \emptyset$) of $C_{55}$ in Makhnev & Paduchikh (2009, Lemma 2.9(2)(ii) & Lemma 4.4(1)) via $4 \nmid (2 - 0)$, and pins down the exact composite-order displacement spectra of Case B of $C_{55}$, $C_{65}$, and $C_{35}$.

---

## Check It Yourself

Run the standalone zero-dependency checker from the package root (`< 0.1 seconds`, Python 3.8+ standard library only):
```bash
sh verify-it-yourself/run_checks.sh
```
This script executes `verify-it-yourself/verify.py`, which independently recomputes every rational Bose–Mesner idempotent, finite-field $\mathbb{F}_p$ matrix rank, Brauer trace–rank check on existing Moore graphs ($C_5$, Petersen, Hoffman–Singleton), Theorem 1.1, Theorem 1.2, all 11 rows of Section 8 Table 1, and all Track `p1` unconditional and conditional exclusions from scratch in exact arithmetic, verifies digit-for-digit agreement with `object/certificate.json`, and prints `PASS`.

To run the standalone Lens 1 (`p2`) and Lens 2 (`p1`) scripts directly:
```bash
python3 how-we-built-it/verify_lens1_p2.py
python3 how-we-built-it/verify_lens2_p1.py
```

---

## Compared To

### 1. Track `p1` — Automorphism-Group Order & Composite Action Exclusions (`srg(3250, 57, 0, 1)`)

| Candidate Group / Branch | Prior Status in Literature | Our Certified Result | Dependency on `arXiv:2606.29183` | Exact Proof Certificate |
| :--- | :--- | :---: | :---: | :--- |
| **$G \cong C_{11} \times C_5^2$ ($\|G\| = 275$)** | Open in Makhnev–Paduchikh (2009) Thm. 1(2)(iii) & Kováčiková (2018) p. 39 | **EXCLUDED** | **Unconditional** (`False`) | $11 \nmid \|\mathrm{Aut}(\mathrm{HoSi})\| \implies \mathrm{Fix}(g) \cong C_5$ ($\forall g \ne 1$) $\implies 3245 \equiv 220 \not\equiv 0 \pmod{275}$; and $a_1(x^k) \ge 550 > 500$ leaves $220 < 275$ vertices |
| **$G \cong C_7 \times C_5^2$ ($\|G\| = 175$)** | Open in Makhnev–Paduchikh (2009) Thm. 1(2)(iv) & Lem. 4.5(1) | **EXCLUDED** | **Unconditional** (`False`) | Free $C_5^2$-action on star leaves outside $\mathrm{HoSi}$ forces $a_0(x) = 51$; CRT ($a_1 \equiv 7 \pmod{175}, a_1 \equiv 2 \pmod{15}$) forces $a_1(x^k) \ge 182 \implies 2851 + 3 \cdot 182 = 3397 > 3250$ |
| **$G \cong C_{55}$ ($\|G\| = 55$), Case A ($\mathrm{Fix}(f) = \emptyset$)** | Open in Makhnev–Paduchikh (2009) Lem. 2.9(2)(ii) & Lem. 4.4(1) | **EXCLUDED** | **Conditional** (`True`, Thm. 4.1) | Equivariant Galois–Brauer at $(11,5)$: $\mathrm{rk}_{\mathbb{F}_{11}}(E_{-8}[F]) = 2$, $\hat{c}_0 = 0$ (mode ranks $[0,0,1,1,0]$), violating $4 \mid (2 - 0)$ (and $55 \nmid 230$) |
| **$G \cong C_{55}$ ($\|G\| = 55$), Case B ($\mathrm{Fix}(f) \cong C_5$)** | Open with $a_1(x), a_1(f) \in \{55, 220, 385\}$ | **UNIQUELY PINNED** | **Conditional** (`True`, Thm. 4.1) | $\hat{c}_0 = 2, \hat{c}_1 = 0 \implies a_1(x^k f^j) = 55$ ($\forall k \ne 0$), and $V_{-8}$ multiplicity integrality uniquely forces $a_1(f) = a_1(f^2) = 385$ ($m_{0,0} = 28$) |
| **$G \cong C_{35}$ ($\|G\| = 35$)** | Allowed $a_0(x) \in \{16, 51\}$; printed $\alpha_1(g) = 105u + 35$ | **$a_0 = 51$ EXCLUDED; $a_0 = 16$ PINNED** | **Conditional** (`True`, Thms. 1.2 & 4.1) | $a_0(x) = 51$ excluded by $a_0(x) \le 37$; on $a_0(x) = 16$, $a_1(x) = 147$, $a_1(x^k f^j) = 42$, and corrects $\alpha_1(g)$ to $105u + 70 \in \{70, 175, 280\}$ ($m_{0,0} = 46$) |
| **$G \cong C_{65}$ ($\|G\| = 65$)** | Open in Makhnev–Paduchikh (2009) Lem. 2.9(2)(iii) & Lem. 4.3 | **PINNED** | **Conditional** (`True`, Thm. 4.1) | $13 \mid a_0(f) \implies a_0(f) = 0$; $\hat{c}_r = 0 \implies a_1(x^k f^j) = 65$ ($\forall k \ne 0$) and $\{a_1(f), a_1(f^2)\} = \{65, 260\}$ ($m_{0,0} = 27$) |
| **Even Orders ($\|G\| \in \{2,4,6,10,12,20,22,38,50,100,110\}$)** | Listed in Makhnev–Paduchikh (2009) Thm. 1(1); Mačaj–Širáň ($\le 110$) | **EXCLUDED** | **Conditional** (`True`, Thm. 1.1) | Eliminated by $2 \nmid \|\mathrm{Aut}(\Gamma)\|$ |

### 2. Track `p2` — Independent Exact Verification of `arXiv:2606.29183v2`

| Theorem / Section | Mathematical Statement Verified | Exact Computed Result | Status |
| :--- | :--- | :--- | :---: |
| **Section 5 (Eqs. 8–9)** | $p$-integrality of $E_7$ and $E_{-8}$ in $\mathrm{srg}(3250, 57, 0, 1)$ | $E_7 = \frac{400I+50A-J}{750}$ ($\mathrm{denom} = 2 \cdot 3 \cdot 5^3$), $E_{-8} = \frac{455I-65A+J}{975}$ ($\mathrm{denom} = 3 \cdot 5^2 \cdot 13$) | **PASS** |
| **Section 4 (Thm. 4.1)** | Existing Moore graphs $C_5$, Petersen $\mathrm{srg}(10,3,0,1)$, $\mathrm{HoSi}$ $\mathrm{srg}(50,7,0,1)$ | $\mathrm{tr}(T_g E_\theta) = \mathrm{rank}_{\mathbb{F}_p}(E_\theta[\mathrm{Fix}(g)] \bmod p)$ verified across all $5$ prime-order benchmark cases | **PASS** |
| **Theorem 1.1 & Cor. 6.1** | No involutions in $\mathrm{srg}(3250, 57, 0, 1)$ ($p = 2$, $\mathrm{Fix}(t) \cong K_{1,55}$) | $\mathrm{rank}_{\mathbb{F}_2}(975 E_{-8}[K_{1,55}] \bmod 2) = 54 \implies a_1(t) = -368 < 0$ (vs combinatorial $a_1(t) = 112, \chi_{-8}(t) = 22$) | **PASS** |
| **Theorem 1.2 ($p \in \{7,11,13,19\}$)** | Exact displacements $a_1(x)$ for odd primes | $p=7$: $(a_0, a_1) \in \{(2,49),(9,98),(16,147),(23,196),(30,245),(37,294)\}$ (excludes $\{44,51\}$); $p=11$: $a_1 = 55$; $p=13$: $a_1 = 65$; $p=19$: $a_1 = 57$ | **PASS** |
| **Section 8 (Table 1 & Rem. 8.5)** | $11$ branches across $5$ open SRG families | All $11$ rows of Table 1 and Remark 8.5 (correcting Makhnev–Nosov 2004 on $\mathrm{srg}(352,26,0,2)$) verified in exact $\mathbb{F}_p$ arithmetic | **PASS** |

---

## Not Claimed

- We do not claim a Full Win (`CONFIRMED_SOLUTION`) on `moore-graph-57` (constructing a $57$-regular Moore graph on $3250$ vertices or proving its non-existence in Lean/Isabelle).
- Automorphisms of prime orders $p \in \{3, 5\}$ (where neither $E_7$ nor $E_{-8}$ is $p$-integral) and the surviving small odd group orders in Makhnev–Paduchikh (2009) remain open.

---

## Credits

- **Primary Reference Verified (`p2`):** Yawara Ishida (*"No involutions in the missing Moore graph"*, `arXiv:2606.29183v2`, 8 July 2026).
- **Discovery & Verification (`p1` & `p2`):** `@mizopl` (`we*` = `@mizopl` + Gemini-CLSS autonomous research system, `https://github.com/mizopl/we-star`).
