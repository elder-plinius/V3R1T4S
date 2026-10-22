# Panelist Report: CRITERION (`ghr-sum-difference-c3a`)

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
problem_id: ghr-sum-difference-c3a
target_win_level: partial_win p1

## 1. Classification Against Full `success_criterion` vs Named Partial Win `p1`

- **Why this does NOT meet the full `success_criterion`:**
  The benchmark's full `success_criterion` requires a finite-depth certified construction whose value under the `constants/3a.md` formula exceeds the best lower bound listed on `constants/3a.md` **including asterisked limit values** (`1.19519192*` in [K2026b] as of `claim/3a.md`, `9,559` bytes, `sha256: 7fcaf2453bc29c26452b9421152df4111ec3aa459d40de653fa0fabd5d439adf`) by at least `1e-7`. The primary certified value here is `1.19230254070568368329`, which is below `1.19519192*` by `0.00288938`.
- **Why this literally satisfies named partial win `p1`:**
  The benchmark defines partial win `p1` verbatim as:
  > *"A finite-certified construction whose value lies strictly above the best finite-certified value on the 3a page (1.19102809 as of 2026-10-03) but does not beat the limit record, verified with directed rounding and the formula's hypotheses checked."*
  And under *"How a win is checked"*:
  > *"For digit constructions: re-derive the counting formula independently, recompute the counts with separate code, and reproduce Kleinwaks's 1.19102809 with the same pipeline first."*

---

## 2. Clause-by-Clause Verification of `p1` and "How a Win Is Checked"

### Clause 1: Explicit Finite-Certified Construction ($V = 2U$ at Finite Depth $N = 10^{13}$)
- **Primary certificate (`claim/finite_certificate_17086_27995.json`, `1,204` bytes, `sha256: b1230dd40bb7fcb2ae877bee31547f50dd52657d99c6e19e483271a871c1fe21`):**
  - Semigroup generators: $G = \{1518, 1524, 1587, 2024, 2032, 2116\} = \{3, 4\} \times \{506, 508, 529\}$.
  - Digit mask: $M = \operatorname{span}_{\mathbb{N}_0}(G) \cap [0, 17086]$ (`claim/mask_17086.txt`, `18,450` bytes, `sha256: 3f9c0909410adb97e55c5ae7ab5a1a5dd54a11c415fa4513bbb8c2c06f29b358`), independently reconstructed via dynamic programming with $|M| = 3,153$, $\min M = 0$, $\max M = 17,086 = B$.
  - Sum support: $S = M + M \subseteq [0, 34172]$ (`claim/sum_support_17086.txt`, `112,542` bytes, `sha256: 7815e2fa41072d923eaeb99c46b3282f837093b6075ff5e4491d3aa89da58acc`), independently reconstructed with $|S| = 18,835$, $\min S = 0$, $\max S = 34,172 = 2B$.
  - Controlled-carry odd base: $q = 27,995$ (odd, satisfying $B + 1 = 17,087 \le q \le 2B + 1 = 34,173$).
  - Finite depth $N = 10^{13}$, saddle parameter $x_f = 9996683050229444 / 10^{16} = 0.9996683050229444$, zero-difference count $n_0 = 17,074,745,018$, digit-sum cap $L = 50,031,092,045,455,301$, and explicit finite integer set
    $$V = 2U \subset \mathbb{Z}_{\ge 0}, \qquad U = \left\{\sum_{i=0}^{N-1} a_i \cdot 27995^i : a_i \in M, \ \sum_{i=0}^{N-1} a_i \le L\right\}.$$
- **Secondary certificate (`claim/finite_certificate_17032_27995.json`, `1,204` bytes, `sha256: db1517d0d4b32ad27df910162aa55d283fa9e6a4fa0374bff651b6ae655de04b`):**
  - Uses Kleinwaks's exact published mask $B = 17,032$ ($|M| = 3,121, |S| = 18,730$) in controlled-carry odd base $q = 27,995$ at $N = 10^{13}$ with $x_f = 0.9996683050229444$, $n_0 = 17,075,622,128$, and $L = 50,029,864,065,809,249$.

### Clause 2: Strictly Above `1.19102809` by at Least `1e-7`, Below Limit Record `1.19519192*`, Verified with Directed Rounding
- **Primary certificate (`B = 17,086, q = 27,995, N = 10^{13}`):**
  - 60-digit `mpmath.iv` interval/directed-rounding lower bound: `1.19230254070568368329` (confirmed at 80-digit `mpmath.iv` interval precision as `[1.19230254070568368329168, 1.19230254070568368329168]`).
  - 100% pure integer-interval (`atanh` Taylor series + Lean `StirlingBounds.lean` bounds) lower bound: `1.19230254068351294895`.
  - Tight denominator check (using $2\max V + 1 \le \frac{4B}{q-1} q^N = 2.441380 \cdot q^N$ in place of $5 q^N$): `1.192302540705685029577834`.
  - Margin over `1.19102809`: `+0.00127445` ($12,744\times$ the `1e-7` minimum improvement threshold), while strictly below `1.19519192*`.
- **Secondary certificate (`B = 17,032, q = 27,995, N = 10^{13}`):**
  - 60-digit `mpmath.iv` lower bound: `1.19229904840497896133` (80-dps interval: `[1.192299048404978961333885, 1.192299048404978961333885]`).
  - Pure integer-interval lower bound: `1.19229904838280822699`.
  - Margin over `1.19102809`: `+0.00127095` ($12,709\times$ the `1e-7` threshold).

### Clause 3: Reproduction of Kleinwaks's `1.19102809` with the Same Pipeline First
- Evaluated on `claim/kleinwaks_finite_certificate_17032_34065.json` (`1,204` bytes, `sha256: 5c85a63a7a8a8d7b596c3d375239ecd91e45fdf991feb44500a922deeb9d8239`) with $B = 17,032, Q = 34,065 = 2B + 1, N = 10^{13}, x_f = 0.9996789017186568$:
  - Reconstructed $|M| = 3,121$, $|S| = 18,730$, $|\widetilde{D}_+| = 16,184$, $|\widetilde{D}| = 32,369$, $n_0 = 14,962,802,398$, $L = 51,500,691,976,683,641$, `cfFloorOK == True`.
  - Certified lower bound: `1.19102809427254087548` (60-dps `mpmath.iv`) and `1.19102809424738956213` (pure integer-interval), matching Kleinwaks's published `1.19102809` to all 8 published decimal places.

### Clause 4: Exact Hypotheses of the GHR Formula on `constants/3a.md` Checked
The lemma on `claim/3a.md` line 40 states that a finite set $V$ of non-negative integers containing zero and satisfying $|V - V| \le 2\max(V)$ yields $C_{3a} \ge 1 + \log(|V - V| / |V + V|) / \log(2\max(V) + 1)$:
1. **$0 \in V = 2U$:** Since $0 \in M$ and $L = 50,031,092,045,455,301 \ge 0$, the all-zero word $(0, \dots, 0)$ gives $0 \in U$ and $0 \in V$.
2. **$V \subset \mathbb{Z}_{\ge 0}$ is finite with $\max V \ge 2 B q^{N-1} \gt 0$:** Every digit $a_i \in M \subset \mathbb{Z}_{\ge 0}$ and base $q = 27,995 \gt 0$, so $V \subset \mathbb{Z}_{\ge 0}$; since $B \in M$ and $L \ge B$, the single-digit word $(0, \dots, 0, B)$ lies in $U$, so $\max V = 2\max U \ge 2 B q^{N-1} \gt 0$.
3. **Strict difference-range hypothesis $|V - V| \le 2\max V$:** Because $U \subseteq [0, \max U] \cap \mathbb{Z}$, $U - U \subseteq [-\max U, \max U] \cap \mathbb{Z}$, hence $|V - V| = |U - U| \le 2\max U + 1 \le 4\max U = 2\max V$ (strictly less than $2\max V + 1 = 4\max U + 1$).
4. **Denominator upper bound $2\max V + 1 \le 5 q^N$:** Since $a_i \le B \le q - 1$, $\max U \le B(q^N - 1)/(q - 1) \le q^N - 1$, so $2\max V + 1 = 4\max U + 1 \le 4 q^N - 3 \le 5 q^N$.
5. **Residue-bijective injectivity on $\widetilde{D}^N$:** All $13,997$ rows of `claim/pruned_differences_17086_27995.tsv` (`662,028` bytes, `sha256: 32e129199434a9122f0beab45dd69309921e4e389117f1fbdc00fa94580f3c0c`) satisfy $\alpha_d, \beta_d \in M$, $\alpha_d - \beta_d = d$, $\alpha_d + \beta_d = \kappa(d)$, and the $1 + 2(13,997) = 27,995$ elements of $\widetilde{D} = \{0\} \cup \{\pm d : d \in \widetilde{D}_+\}$ have $27,995$ pairwise distinct residues modulo $q = 27,995$ (a complete residue system mod $27,995$). Thus base-$q$ evaluation is injective on $\widetilde{D}^N$, and $|V - V| = |U - U| \ge D_N = N! / (n_0! \prod_{d \in \widetilde{D}_+} (n_d!)^2)$.
6. **Small-$N$ brute-force verification on controlled-carry instances ($q \le 2B$):**
   - Toy A ($B = 2, q = 3 \le 2B = 4, M = \{0, 2\}, N = 3, L = 2$): $|U| = 4, \max V = 36, |V - V| = 13 \ge D_N = 6, |V + V| = 10 \le S_N = 20.96, |V - V| = 13 \le 2\max V = 72 \le 5 q^N - 1 = 134$.
   - Toy B ($B = 3, q = 5 \le 2B = 6, M = \{0, 2, 3\}, N = 3, L = 5$): $|U| = 16, \max V = 170, |V - V| = 119 \ge D_N = 6, |V + V| = 91 \le S_N = 355.80, |V - V| = 119 \le 2\max V = 340 \le 5 q^N - 1 = 624$.

---

## 3. Null Model & Perturbation Controls

1. **Unmasked full-interval baseline $M_{\text{full}} = [0, 17086]$:**
   $|M_{\text{full}}| = 17,087$ and $|M_{\text{full}} + M_{\text{full}}| = 34,173$. Because any residue-distinct difference alphabet modulo $q = 27,995$ has size $|\widetilde{D}| \le 27,995$, the difference-to-sum ratio is at most $27995 / 34173 = 0.819214 \le 1$, giving an upper bound proxy $1 + \log(27995 / 34173) / \log(27995) = 0.980526 \le 1.0$.
2. **Random mask ensemble (`400` random masks $M_{\text{rand}} \subset [0, 17086]$ of size $|M_{\text{rand}}| = 3,153$ containing $\{0, 17086\}$, seed `20261019`):**
   Across all 400 random trials, the minimum sumset size is $\min |M_{\text{rand}} + M_{\text{rand}}| = 33,990$ (nearly the full interval $34,173$, vs $|S| = 18,835$ for the commutative semigroup mask $M = \operatorname{span}_{\mathbb{N}_0}(G) \cap [0, 17086]$), and the upper-bound proxy $1 + \log(\min(|M_{\text{rand}} - M_{\text{rand}}|, q) / |M_{\text{rand}} + M_{\text{rand}}|) / \log(q)$ has mean `0.980775` and maximum `0.981050` (all below `1.0`, vs `1.19230254` for the structured mask).
3. **Witness corruption & even-base perturbation controls:**
   - Perturbing row $r = 1$ of `claim/pruned_differences_17086_27995.tsv` from $\alpha_1 = 7176$ to $7177$ is immediately caught (`7177 not in M` and `7177 - 7175 != 1`).
   - Replacing odd base $q = 27,995$ by even base $q = 27,994$ causes residue collision at $r = q/2 = 13,997$ ($+13997 \equiv -13997 \equiv 13997 \pmod{27994}$), which is immediately rejected by the residue-distinctness check.

---

## 4. Confirmed Scope & Verdict

confirmed_scope: Two explicit finite-depth (N = 10^13) controlled-carry masked-digit constructions V = 2U in odd base q = 27,995 over the semigroup generated by {1518, 1524, 1587, 2024, 2032, 2116}, headlined by claim/finite_certificate_17086_27995.json (sha256 b1230dd40bb7fcb2ae877bee31547f50dd52657d99c6e19e483271a871c1fe21, B = 17,086, |M| = 3,153, |S| = 18,835, |D_+| = 13,997 with all 27,995 residues mod 27,995 pairwise distinct, n_0 = 17,074,745,018, L = 50,031,092,045,455,301) with certified GHR lower bound C_{3a}(V) > 1.19230254070568368329 in 60-digit mpmath interval arithmetic and > 1.19230254068351294895 in pure integer-interval arithmetic (along with secondary certificate claim/finite_certificate_17032_27995.json on B = 17,032 giving C_{3a}(V) > 1.19229904840497896133), after reproducing Kleinwaks's 1.19102809 baseline with the same pipeline, strictly exceeding the best finite-certified bound 1.19102809 on constants/3a.md by +0.00127445 while remaining below the asymptotic limit record 1.19519192* under partial win p1.

pass: true
