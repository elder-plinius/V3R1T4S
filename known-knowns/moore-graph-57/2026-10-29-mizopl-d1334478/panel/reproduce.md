# V3R1T4S Skeptic 1 (REPRODUCE) Audit Report — `moore-graph-57` (`p2`)

> **Dated Scope Note (`2026-10-29`):** Per `@elder-plinius`'s review on PR `#770`, this standalone package extracts strictly the **Partial Win `p2`** exact computational verification of `arXiv:2606.29183v2` (`object/certificate.json`, `sha256: d13344783df1b7cf33f19e9b3408bad1bbe96939c5e087b02460113f03dc9c07`), with all unformalized `p1` written group-action arguments removed.

- context: fresh subagent (5fcf977c-02ef-47f1-89ef-19892ee2e49a) invoked via invoke_subagent for independent V3R1T4S panel review
- **Verdict:** PASS
- **Target ID:** `moore-graph-57`
- **Verification Script Audited:** `verify-it-yourself/verify.py` and `how-we-built-it/verify_lens1_p2.py`
- **Certificate Audited:** `object/certificate.json` (`sha256: d13344783df1b7cf33f19e9b3408bad1bbe96939c5e087b02460113f03dc9c07`)

---

## 1. Executive Summary
I have read, executed, and audited:
1. `verify-it-yourself/verify.py`
2. `object/certificate.json`
3. `how-we-built-it/verify_lens1_p2.py`

Running `sh verify-it-yourself/run_checks.sh` exited with code `0` (`PASS`), confirming a digit-for-digit match between the recomputed values and `object/certificate.json`, and mutating any digit in `object/certificate.json` causes `verify.py` to print `FAIL` on its last line and exit `1`.

---

## 2. Exact Arithmetic & Zero-Approximation Audit
- **Zero Floating-Point Usage:** Every calculation in `verify.py` and `verify_lens1_p2.py` uses Python exact `int` arithmetic, `fractions.Fraction` for rational Bose–Mesner algebra calculations, and exact modular inverse `pow(x, -1, p)` Gaussian elimination (`rank_mod_p`) over $\mathbb{F}_p$. No `float`, `/`, `math.sqrt`, or numerical tolerances exist anywhere in the codebase.

---

## 3. Track `p2` Mathematical & Computational Audit (`arXiv:2606.29183v2`)
- **Bose–Mesner Idempotents:** Verified exact SRG feasibility, eigenvalues, multiplicities ($m_{57}=1, m_7=1729, m_{-8}=1520$), idempotency ($E_i^2 = E_i$), orthogonality ($E_i E_j = 0$), completeness ($\sum E_i = I$), and primitive integer coefficients (`gcd = 1`) for $\mathrm{srg}(3250, 57, 0, 1)$ ($E_7 = \frac{1}{750}(400I + 50A - J)$, $E_{-8} = \frac{1}{975}(455I - 65A + J)$) and all auxiliary SRG families.
- **Existing Moore Graphs:** Verified $\mathrm{tr}(T_g E_\theta) = \mathrm{rank}_{\mathbb{F}_p}(E_\theta[\mathrm{Fix}(g)])$ on $C_5$ ($p=2$, $\mathrm{rk}=0$), Petersen $\mathrm{srg}(10,3,0,1)$ ($p=2$ transposition $\mathrm{rk}=2$, $p=2$ double transposition $\mathrm{rk}=0$, $p=5$ 5-cycle $\mathrm{rk}=0$), and Hoffman–Singleton $\mathrm{srg}(50,7,0,1)$ ($p=2$ involution with $\mathrm{Fix}=K_{1,5}$, $\mathrm{rk}=4$).
- **Theorem 1.1 (No Involutions, $p=2$):** Verified that an involution $t$ on $\mathrm{srg}(3250, 57, 0, 1)$ combinatorially requires $a_0(t)=56$, $\mathrm{Fix}(t)=K_{1,55}$, $a_1(t)=112$, $\chi_{E_{-8}}(t)=22$, and $\chi_{E_7}(t)=33$ (with $a_1(t)=0$ ruled out across all closed subgraphs), whereas $\mathrm{rank}_{\mathbb{F}_2}(975 E_{-8}[K_{1,55}]) = 54$, forcing $a_1(t) = -368 < 0$.
- **Theorem 1.2 (Odd Primes $p \in \{7, 11, 13, 19\}$):**
  - $p=7$: Verified $\mathrm{rank}_{\mathbb{F}_7}(975 E_{-8}[K_{1,a_0-1}]) = 1$ and $\mathrm{rank}_{\mathbb{F}_7}(750 E_7[K_{1,a_0-1}]) = a_0 - 2$ for all $a_0 \equiv 2 \pmod 7$, forcing $a_1(g) = 7a_0 + 35$ and disjoint vertex bound $78a_0 + 49 \le 3250 \implies a_0 \in \{2,9,16,23,30,37\}$ (excluding $a_0 \in \{44, 51\}$).
  - $p=11$: Verified $\mathrm{Fix}(g)=C_5$, $\mathrm{rk}_{\mathbb{F}_{11}}(E_{-8}[C_5]) = \mathrm{rk}_{\mathbb{F}_{11}}(E_7[C_5]) = 2$, forcing $a_1(g)=55$ (excluding $220, 385$).
  - $p=13$: Verified $\mathrm{Fix}(g)=\emptyset$, $\mathrm{rk}_{\mathbb{F}_{13}}(E_7[\emptyset]) = 0$, forcing $a_1(g)=65$ (excluding $260, 455$), and confirmed $E_{-8}$ is non-$13$-integral with trace $-1$.
  - $p=19$: Verified $\mathrm{Fix}(g)=K_1$, $\mathrm{rk}_{\mathbb{F}_{19}}(E_{-8}[K_1]) = \mathrm{rk}_{\mathbb{F}_{19}}(E_7[K_1]) = 0$, forcing $a_1(g)=57$ (excluding $342$).
- **Section 8 Table 1:** Verified all 11 rows across $\mathrm{srg}(162, 21, 0, 3)$, $\mathrm{srg}(352, 26, 0, 2)$ (including Remark 8.5 correcting Makhnev–Nosov 2004 Lemmas 2.2 and 2.3(1)), $\mathrm{srg}(1276, 50, 0, 2)$, $\mathrm{srg}(99, 14, 1, 2)$, and $\mathrm{srg}(640, 243, 66, 108)$.

pass: true
