# Run It Yourself (`2026-10-26-mizopl-659ce5b9` — `moore-graph-57`)

1. Ensure `python3` (`>= 3.8`, standard library only — zero external packages required) is installed.
2. From the root of this package directory, execute:
   ```sh
   sh verify-it-yourself/run_checks.sh
   ```
3. The script runs `verify-it-yourself/verify.py`, performing in **`< 0.1` seconds** using 100% exact integer, `fractions.Fraction`, and finite-field ($\mathbb{F}_p$ Gaussian elimination) arithmetic:
   - **Track `p2` (Independent Exact Computational Verification of `arXiv:2606.29183v2`):**
     - Verifies the Bose–Mesner algebra $\mathbb{Q}[I, A, J]$ of $\mathrm{srg}(3250, 57, 0, 1)$, orthogonal idempotents $E_7 = \frac{400I + 50A - J}{750}$ ($\mathrm{denom} = 2 \cdot 3 \cdot 5^3$) and $E_{-8} = \frac{455I - 65A + J}{975}$ ($\mathrm{denom} = 3 \cdot 5^2 \cdot 13$), and $p$-integrality sharpness.
     - Verifies the Brauer-quotient trace–rank identity $\mathrm{tr}(T_g E_\theta) = \mathrm{rank}_{\mathbb{F}_p}(E_\theta[\mathrm{Fix}(g)] \bmod p)$ across prime-order automorphisms of $C_5 = \mathrm{srg}(5, 2, 0, 1)$, the Petersen graph $\mathrm{srg}(10, 3, 0, 1)$, and the Hoffman–Singleton graph $\mathrm{srg}(50, 7, 0, 1)$.
     - Verifies Theorem 1.1 & Corollary 6.1 ($\mathrm{Fix}(t) \cong K_{1,55}$, $\mathrm{rank}_{\mathbb{F}_2}(975 E_{-8}[F] \bmod 2) = 54 \implies a_1(t) = -368 < 0$, ruling out all involutions and all even group orders), Theorem 1.2 ($p \in \{7, 11, 13, 19\}$), and all 11 rows of Section 8 Table 1 across 5 open SRG families (including Remark 8.5 correcting Makhnev–Nosov 2004 Lemmas 2.2 and 2.3(1)).
   - **Track `p1` (Computer-Verified Automorphism-Group Order & Composite Action Exclusions):**
     - **Part I (Unconditional, independent of `arXiv:2606.29183`):** Verifies the Abelian Orbit Chord Lemma on $C_{11} \times C_5^2$ and $C_7 \times C_5^2$, the unconditional exclusion of $|\mathrm{Aut}(\Gamma)| = 275$ ($C_{11} \times C_5^2$, Makhnev–Paduchikh 2009 Theorem 1(2)(iii) & Lemma 4.4(2); Kováčiková 2018 p. 39), and the unconditional exclusion of $|\mathrm{Aut}(\Gamma)| = 175$ ($C_7 \times C_5^2$, Makhnev–Paduchikh 2009 Theorem 1(2)(iv) & Lemma 4.5(1)).
     - **Part II (Conditional, building on `arXiv:2606.29183`):** Verifies the Equivariant Galois–Brauer Rank Obstruction excluding Case A ($\mathrm{Fix}(f) = \emptyset$) of $C_{55}$ ($4 \nmid (2 - 0)$, Fourier mode ranks $[0, 0, 1, 1, 0]$ over $\mathbb{F}_{11}$) and uniquely pinning Case B of $C_{55}$ ($a_1(x^k f^j) = 55$, $a_1(f) = a_1(f^2) = 385$), excluding the $a_0(x) = 51$ branch of $C_{35}$ and pinning the $a_0(x) = 16$ branch ($a_1(x) = 147$, $a_1(x^k f^j) = 42$, correcting Makhnev–Paduchikh's congruence misprint $105u+35 \to 105u+70$), pinning $C_{65}$ ($a_0(f) = 0$, $a_1(x^k f^j) = 65$, $\{a_1(f), a_1(f^2)\} = \{65, 260\}$), and excluding all 11 even orders $\le 110$, printing `PASS` as its final line.
