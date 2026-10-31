# Skeptic Panel Report — Role: REPRODUCE

role: REPRODUCE
context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
problem_id: ghr-sum-difference-c3a
partial_win_id: p1

## 1. Quoted Mathematical Definitions (Used to Build the Independent Checker Before Reading Author Code)

Before inspecting `claim/author_checker_c3a_check.py`, an independent checker (`indep_c3a_check.py`) was written from scratch directly from the mathematical definitions in `claim/3a.md` and `claim/CLAIM.md`:

1. **Gyarmati–Hennecart–Ruzsa (GHR) Lemma (`claim/3a.md`, lines 40–41):**
   "A lemma from [GHR2007] states that a finite set $U$ of non-negative integers containing zero and satisfying $\lvert U-U\rvert \lt 2\max(U)+1$ yields $C_{3a} \geq 1 + \log( \lvert U-U \rvert /\lvert U+U \rvert )/\log(2 \max(U)+1)$."

2. **Controlled-Carry Masked-Digit Construction $V = 2U$ in Odd Base $q$ (`claim/CLAIM.md`, §2.2):**
   - Given positive integer generators $G = \{1518, 1524, 1587, 2024, 2032, 2116\} = \{3, 4\} \times \{506, 508, 529\}$ and mask bound $B \ge 1$, the digit mask is $M = \operatorname{span}_{\mathbb{N}_0}(G) \cap [0, B]$ and the sum support is $S = M + M \subseteq [0, 2B]$.
   - For each $d \in [0, B]$, the minimal digit-sum cost is $\kappa(d) = \min\{2b + d : b \in M, \ b + d \in M\}$ (with $\kappa(d) = +\infty$ if $d \notin M - M$), realized by the minimal witness pair $(\alpha_d, \beta_d) = (b^* + d, b^*) \in M^2$.
   - For an odd base $q$ satisfying $B + 1 \le q \le 2B + 1$, partition the non-zero residues $\{1, \dots, q - 1\} \pmod{q}$ into $(q - 1)/2$ disjoint complementary pairs $\{r, q - r\}$ ($1 \le r \le (q - 1)/2$). Since $q$ is odd, $r \not\equiv q - r \pmod{q}$. For each $r$ with $\min(\kappa(r), \kappa(q - r)) \lt \infty$, select
     $$d(r) = \begin{cases} r & \text{if } \kappa(r) \le \kappa(q - r), \\ q - r & \text{if } \kappa(q - r) \lt \kappa(r). \end{cases}$$
     Set $\widetilde{D}_+ = \{d(r) : 1 \le r \le (q - 1)/2, \ \min(\kappa(r), \kappa(q - r)) \lt \infty\}$ and $\widetilde{D} = \{0\} \cup \{\pm d : d \in \widetilde{D}_+\} \subseteq M - M$.
   - **Theorem 1 (Injective Base-$q$ Evaluation):** Every pair $\{+d(r) \bmod q, -d(r) \bmod q\} = \{r, q - r\}$ is disjoint across $1 \le r \le (q - 1)/2$ and excludes $0$, so all $1 + 2\lvert\widetilde{D}_+\rvert$ elements of $\widetilde{D}$ have pairwise distinct residues modulo $q$. By induction on $N$ (reducing modulo $q$ at the lowest digit, subtracting, and dividing by $q$), the base-$q$ evaluation map $\operatorname{eval}_q(d_0, \dots, d_{N-1}) = \sum_{i=0}^{N-1} d_i q^i$ is injective on $\widetilde{D}^N$.
   - **Theorem 2 (Exact Multinomial Difference Lower Bound):** Given integer counts $n_d \ge 1$ ($d \in \widetilde{D}_+$) with $n_0 := N - 2\sum_{d \in \widetilde{D}_+} n_d \gt 0$ and digit-sum cap $L := \sum_{d \in \widetilde{D}_+} n_d \kappa(d)$, define
     $$U = \left\{\sum_{i=0}^{N-1} a_i q^i : a_i \in M, \ \sum_{i=0}^{N-1} a_i \le L\right\}, \qquad V = 2U = \{2u : u \in U\}.$$
     Replacing $0 \mapsto (0, 0)$, $+d \mapsto (\alpha_d, \beta_d)$, and $-d \mapsto (\beta_d, \alpha_d)$ maps every word $w \in \mathcal{W} \subseteq \widetilde{D}^N$ with symbol frequencies $(n_0, (n_d, n_d)_{d \in \widetilde{D}_+})$ to a pair $(u(w), v(w)) \in U^2$ with $\sum a_i(w) = \sum b_i(w) = L$ and $u(w) - v(w) = \operatorname{eval}_q(w)$. By injectivity of $\operatorname{eval}_q$ on $\widetilde{D}^N$,
     $$\lvert V - V\rvert = \lvert U - U\rvert \ge \lvert\mathcal{W}\rvert = D_N := \frac{N!}{n_0! \prod_{d \in \widetilde{D}_+} (n_d!)^2}.$$
   - **Theorem 3 (Saddle-Point Sumset Upper Bound):** Every element of $U + U$ has digits $s_i \in S = M + M$ with $\sum_{i=0}^{N-1} s_i \le 2L$. For any $x_f \in (0, 1)$, since $x_f^m \ge x_f^{2L}$ for $0 \le m \le 2L$ and all coefficients of $(P_+(x_f))^N$ ($P_+(x) := \sum_{s \in S} x^s$) are non-negative,
     $$\lvert V + V\rvert = \lvert U + U\rvert \le \frac{(P_+(x_f))^N}{x_f^{2L}} =: S_N(x_f).$$
   - **Theorem 4 (GHR Lemma Hypotheses on $V = 2U$):**
     1. $0 \in V$ since $0 \in M$ and $L \ge 0$.
     2. $V \subset \mathbb{Z}_{\ge 0}$ is finite and $\max V = 2\max U \ge 2 B q^{N-1} \gt 0$ since $B \in M$ and $L \ge B$.
     3. Since $U \subseteq [0, \max U] \cap \mathbb{Z}$, $\lvert V - V\rvert = \lvert U - U\rvert \le 2\max U + 1 \lt 4\max U + 1 = 2\max V + 1$.
     4. Since $a_i \le B \le q - 1$, $\max U \le B(q^N - 1)/(q - 1) \le q^N - 1$, so $2\max V + 1 = 4\max U + 1 \le 4 q^N - 3 \lt 5 q^N$ for $B + 1 \le q \lt 2B + 1$ (and for $q = 2B + 1$, $\max U \le (q^N - 1)/2$, so $2\max V + 1 = 4\max U + 1 \le 2 q^N - 1 \lt 2 q^N$).

---

## 2. File Integrity Verification (`claim/`)

All 8 files in `claim/` were checked via `wc -c` and `shasum -a 256`:

| File | Expected Bytes | Actual Bytes | SHA-256 Digest | Match |
|---|---:|---:|---|---|
| `claim/finite_certificate_17086_27995.json` | `1,204` | `1,204` | `b1230dd40bb7fcb2ae877bee31547f50dd52657d99c6e19e483271a871c1fe21` | PASS |
| `claim/finite_certificate_17032_27995.json` | `1,204` | `1,204` | `db1517d0d4b32ad27df910162aa55d283fa9e6a4fa0374bff651b6ae655de04b` | PASS |
| `claim/kleinwaks_finite_certificate_17032_34065.json` | `1,204` | `1,204` | `5c85a63a7a8a8d7b596c3d375239ecd91e45fdf991feb44500a922deeb9d8239` | PASS |
| `claim/mask_17086.txt` | `18,450` | `18,450` | `3f9c0909410adb97e55c5ae7ab5a1a5dd54a11c415fa4513bbb8c2c06f29b358` | PASS |
| `claim/sum_support_17086.txt` | `112,542` | `112,542` | `7815e2fa41072d923eaeb99c46b3282f837093b6075ff5e4491d3aa89da58acc` | PASS |
| `claim/pruned_differences_17086_27995.tsv` | `662,028` | `662,028` | `32e129199434a9122f0beab45dd69309921e4e389117f1fbdc00fa94580f3c0c` | PASS |
| `claim/3a.md` | `9,559` | `9,559` | `7fcaf2453bc29c26452b9421152df4111ec3aa459d40de653fa0fabd5d439adf` | PASS |
| `claim/author_checker_c3a_check.py` | `14,634` | `14,634` | `bd9a411489eae68b8a06cde78024c85d5e839954bbf976d316e2bd8b58ceb246` | PASS |

---

## 3. Toy Brute-Force Verification & Negative Controls

Before running on $N = 10^{13}$, `indep_c3a_check.py` executed an exhaustive finite-depth set enumeration on the controlled-carry toy instance $B = 2, q = 3 \lt 2B + 1 = 5, M = \{0, 2\}, N = 3, L = 2$:
- Pruned difference alphabet: for $r = 1, q - r = 2$, $\kappa(1) = +\infty$ and $\kappa(2) = 2$ with witness $(\alpha_2, \beta_2) = (2, 0)$, giving $\widetilde{D}_+ = \{2\}$ and $\widetilde{D} = \{-2, 0, 2\}$ with pairwise distinct mod-$3$ residues $\{1, 0, 2\}$.
- Multinomial counts $n_2 = 1, n_0 = 1, L = 2$: explicit enumeration gives $\lvert U\rvert = 4$ ($U = \{0, 2, 6, 18\}$), $V = 2U = \{0, 4, 12, 36\}$, $\lvert V - V\rvert = 13 \ge D_N = \frac{3!}{1!(1!)^2} = 6$, $\lvert V + V\rvert = 10 \le S_N(0.5) = 60.75$, and $\lvert V - V\rvert = 13 \lt 2\max V + 1 = 73 \lt 5 \cdot 3^3 = 135$.
- Three negative controls were also executed and verified to fail as required:
  1. **Corrupted witness** ($\alpha_d - \beta_d \ne d$): rejected by `check_pruned_alphabet_injectivity`.
  2. **Duplicate residue modulo $q$** (including both $r = 1$ and $q - r = 2$ in $\widetilde{D}_+$ for $q = 3$): rejected by `check_pruned_alphabet_injectivity`.
  3. **Ambiguous fixed-point floor count** (non-dyadic $x_f = 1/3$ with coarse `shift_bits = 4` so `cnt_lo != cnt_hi`): rejected with `cfFloorOK == False`.

---

## 4. Independent Full Reproduction of All 3 Certificates & Determinism Check

`indep_c3a_check.py` was executed twice (`run1.txt` and `run2.txt`, completing in `4.182s` and `4.206s`) and compared via `diff -u` (`0` differences). Both independent numerical engines in `indep_c3a_check.py`—(A) 60-digit `mpmath.iv` interval arithmetic with Robbins–Stirling bounds and (B) 100% pure Python $2^{160}$-scaled integer-interval `atanh` Taylor series with Lean `StirlingBounds.lean` bounds—reproduced every value in all three certificate JSON files and all three saved tables (`claim/mask_17086.txt`, `claim/sum_support_17086.txt`, `claim/pruned_differences_17086_27995.tsv`) with 100% exact agreement:

| Quantity | Baseline (`claim/kleinwaks_finite_certificate_17032_34065.json`) | Primary (`claim/finite_certificate_17086_27995.json`) | Secondary (`claim/finite_certificate_17032_27995.json`) |
|---|---:|---:|---:|
| $(B, q, N)$ | $(17032, 34065, 10^{13})$ | $(17086, 27995, 10^{13})$ | $(17032, 27995, 10^{13})$ |
| $\lvert M\rvert$ ($0 \in M, \max M = B$) | `3,121` | `3,153` | `3,121` |
| $\lvert S\rvert = \lvert M + M\rvert$ ($\max S = 2B$) | `18,730` | `18,835` | `18,730` |
| $\lvert\widetilde{D}_+\rvert$ | `16,184` | `13,997` | `13,997` |
| Distinct residues of $\widetilde{D} \pmod{q}$ | `32,369 / 34,065` | `27,995 / 27,995` | `27,995 / 27,995` |
| $2^{-128}$ fixed-point `cfFloorOK` | `True` | `True` | `True` |
| $n_0 = N - 2\sum_{d \in \widetilde{D}_+} n_d$ | `14,962,802,398` | `17,074,745,018` | `17,075,622,128` |
| $L = \sum_{d \in \widetilde{D}_+} n_d \kappa(d)$ | `51,500,691,976,683,641` | `50,031,092,045,455,301` | `50,029,864,065,809,249` |
| $\log D_N$ lower bound | `98126619915169.794476954336516` | `96923036440531.526834740961877` | `96921708022122.256726912720788` |
| $\log S_N(x_f)$ upper bound | `78190878820128.091449996713221` | `77231677026799.530090891209173` | `77230706212341.331842730307794` |
| $\log(\text{factor} \cdot q^N)$ upper bound | `104360257432078.37848391631573` | `102397812017831.54605288810177` | `102397812017831.54605288810177` |
| Certified $\theta_{\text{mp60}}$ (20 dp floor) | `1.19102809427254087548` | **`1.19230254070568368329`** | **`1.19229904840497896133`** |
| Certified $\theta_{\text{int}}$ (20 dp floor) | `1.19102809424738956213` | **`1.19230254068351294895`** | **`1.19229904838280822699`** |
| Certified 8 dp lower bound | `1.19102809` | **`1.19230254`** | **`1.19229904`** |
| Margin over published `1.19102809` | `0.00000000` (baseline) | **`+0.00127445`** ($\ge 10^{-7}$) | **`+0.00127095`** ($\ge 10^{-7}$) |

---

## 5. Inspection and Execution of `claim/author_checker_c3a_check.py`

After completing independent verification, `claim/author_checker_c3a_check.py` was inspected and executed twice as specified in `claim/REPRODUCE.md`:
- Both runs exited with code `0` in `~3.5s` per run and produced byte-identical output (`diff -u` empty).
- Every count, intermediate bound, and 20-decimal-place certified lower bound from `claim/author_checker_c3a_check.py` agreed 100% with `indep_c3a_check.py`.
- The temporary directory `panel/reproduce_work` was removed after verification.

pass: true
