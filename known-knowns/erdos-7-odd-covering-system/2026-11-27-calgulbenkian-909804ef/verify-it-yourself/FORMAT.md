# Certificate Package Format and Verification Specification

This document specifies the plain-text certificate formats, manifest schema, and exact mathematical checks performed by `check.py` for the unconditional lower bound

$$L \ge 6{,}557{,}114{,}959{,}770{,}375 = 3^5 \cdot 5^3 \cdot 7^2 \cdot 11^2 \cdot 13^2 \cdot 17 \cdot 19 \cdot 23 \cdot 29$$

on the least common multiple $L$ of the moduli of any odd covering system of $\mathbb{Z}$ with pairwise distinct moduli greater than $1$.

All units in anchored certificates are **global cells** (Haar probability times $135$). All arithmetic in verification is exact rational (`Fraction`) or exact arbitrary-precision integer arithmetic, with zero floating-point operations.

**Cross-reference to `PROOF.md`:** In `MANIFEST.json`, `check.py` comments/messages, and this specification, *Lemma U* (format `lemma_u_v1`) refers to the scalar criterion of `PROOF.md` Proposition 4.1 (computed by Section 4.2); *Lemma A2* refers to the completion proper-divisor sum condition of `PROOF.md` Lemma 3.1 with the completion table of Section 5.2; and *Lemmas A2–A13* refers to the anchored bound of `PROOF.md` Sections 3–8 (Theorem 8.2). For the column-to-notation dictionary, see `PROOF.md` Section 9.5.

---

## 1. Directory Layout and File Size Limit

In this package, `MANIFEST.json` and `certs/` are in `object/`; this file and `check.py` are in `verify-it-yourself/`. Paths in `MANIFEST.json` are relative to `object/`.

Every certificate file under `certs/` is UTF-8 plain text with LF (`\n`) line endings and size **at most $1{,}000{,}000$ bytes** (split cleanly at line boundaries when needed, with each part under $950{,}000$ bytes).

- `MANIFEST.json` — machine-readable index giving the target bound $L_{\mathrm{target}}$, the list of all certificate files (relative path, exact byte length, SHA-256 hex digest, format, role, and mathematical meaning), and the list of logical certificates with their file parts.
- `certs/scalar_lemma_u.tsv` — 738 exact rational Lemma U (scalar distortion) certificates for $\omega(L) \in \{10, 11, 12, 13\}$.
- `certs/thmA_8p.part01.tsv`, ... — exact rational anchored certificate for Theorem A ($\omega(L) \ge 9$, excluding all finite families on the first 8 odd primes $3, 5, 7, 11, 13, 17, 19, 23$ with unrestricted exponents).
- `certs/nine_finite.tsv` — 23 exact rational Phase-1 (`basic`) anchored certificates on the first 9 odd primes $3, \dots, 29$, dominating all $5{,}028$ nine-prime exponent vectors with product strictly below $L_{\mathrm{target}}$.
- `certs/global_anchored.tsv` — 13 exact rational anchored certificates (Phases 1–2: `basic` and `mixed`) on the first 10 or 11 odd primes, dominating the 18 exponent vectors with $\omega(L) \in \{10, 11\}$ and product strictly below $L_{\mathrm{target}}$ that are not already dominated by `certs/scalar_lemma_u.tsv`.
- `check.py` — standalone verifier using only the Python 3 standard library. Prints `PASS` as its last line if and only if every check succeeds, and `FAIL` otherwise. In this package it is `verify-it-yourself/check.py`, next to this file, and it reads `MANIFEST.json` and `certs/` from the folder named by its `--dir` option, which is `object/` here (`python3 verify-it-yourself/check.py --dir object`, as `verify-it-yourself/run_checks.sh` runs it).
- The results of the tamper tests (corrupted copies of the certificate files that the checkers must reject) are in `verify-it-yourself/RECEIPTS.md`.

---

## 2. Format `lemma_u_v1` (`certs/scalar_lemma_u.tsv`)

Header lines begin with `# ` in `key: value` form, followed by tab-separated data lines:

```tsv
# format: lemma_u_v1
# L_target: 6557114959770375
# columns: id	omega	primes	exps	k0	Cs	B_exact
U001	10	3,5,7,11,13,17,19,23,29,31	1,1,1,1,1,1,1,1,1,4	1	107/64,...	2255944982454656944182508243/12740789030009889398340976640
```

### Exact Checks on Each Row
Let $r = \texttt{omega}$, $P = (p_0, \dots, p_{r-1}) = \texttt{primes}$, $e = (e_0, \dots, e_{r-1}) = \texttt{exps}$, $k_0 = \texttt{k0}$, and $(C_{k_0}, \dots, C_{r-1}) = \texttt{Cs}$.
1. $r \ge 2$, $P$ equals the first $r$ odd primes, every $e_m$ is a positive integer, $1 \le k_0 < r$, and $|\texttt{Cs}| = r - k_0$.
2. For each $m < k_0$, put $\theta_m := (p_m^{e_m} - 1) / ((p_m - 2)p_m^{e_m} + 1)$.
3. For each $i \ge k_0$, put $\rho_i := (p_i^{e_i} - 1) / ((p_i - 1)p_i^{e_i})$ and $\delta_i := 1 - 1/C_i$. Verify the Lemma U hypotheses:
   $$1 < C_i \le p_i \qquad \text{and} \qquad \delta_i \ge \rho_i.$$
4. With independent integer-valued variables $T_m \in \{0, \dots, e_m\}$ having tail probabilities
   $$\mathbb{P}(T_m \ge t) = \begin{cases} \dfrac{(p_m - 1) p_m^{e_m - t}}{(p_m - 2)p_m^{e_m} + 1}, & m < k_0, \\[8pt] C_m p_m^{-t}, & m \ge k_0, \end{cases} \qquad (1 \le t \le e_m),$$
   and $M_i := \prod_{0 \le m < i} (1 + T_m)$, compute the exact rational
   $$B := \prod_{m < k_0}(1 + \theta_m) - 1 - \sum_{m < k_0} \theta_m + \sum_{i = k_0}^{r - 1} C_i \left(\rho_i \mathbb{E}[M_i] - \delta_i + \sum_{k < \delta_i / \rho_i} \mathbb{P}(M_i = k)\,(\delta_i - \rho_i k)\right).$$
5. Verify $B = \texttt{B\_exact}$ identically as exact rationals and $B < 1$.

---

## 3. Format `anchored_cert_v1`

An anchored certificate file contains one or more certificate blocks separated by `# --- model ---` (or split across ordered part files `*.part01.tsv`, ..., `*.partNN.tsv` sharing an identical header block except `# part: k/N`, whose data rows concatenate in order). Each block has header lines:

```tsv
# format: anchored_cert_v1
# id: <identifier>
# primes: 3,5,7,...
# exps: <comma-separated positive ints or inf>
# C7: <rational>
# taus_later: <comma-separated rationals for primes > 7>
# U_cut: <positive int>
# V_cut: <positive int>
# part: <k>/<N>
# columns: phase	key	R_exact	S_exact
```

Followed by tab-separated rows `phase \t key \t R_exact \t S_exact`:
- `phase` $\in \{\texttt{basic}, \texttt{basic75}, \texttt{mixed}, \texttt{coarse}, \texttt{spatial}, \texttt{pure3}, \texttt{fixed165}\}$.
- `key`: comma-separated integers:
  - length 9 `[a, b, c, r, j, d, k, i_e, z]` for `basic`, `basic75`, `mixed`;
  - length 13 `[a, b, c, r, j, d, k, i_e, z, x3, x5, x9, x15]` for `coarse`, `spatial`, `pure3`;
  - length 14 `[a, b, c, r, j, d, k, i_e, z, x3, x5, x9, x15, eta]` for `fixed165`.
- `R_exact`, `S_exact`: exact reduced rational strings (`"p/q"` or `"p"`).

### Exact Side Conditions and Mathematical Checks on Each Anchored Model
1. **Header hypotheses:**
   - `primes` is strictly increasing odd primes starting with `(3, 5, 7, ...)`; `len(exps) == len(primes)`; `len(taus_later) == len(primes) - 3`.
   - `v_3` is `inf` or an integer $\ge 3$; `v_5` is `inf` or an integer $\ge 2$; every `v_p` ($p \ge 7$) is `inf` or an integer $\ge 1$.
   - `U_cut >= 1` and `V_cut >= 1`. Whenever `v_3` is finite, `U_cut > v_3 - 3` (all finite $u$-atoms $1 \le u \le v_3 - 3$ are evaluated exactly with zero tail); whenever `v_5` is finite, `V_cut > v_5 - 1` (all finite $v$-atoms $1 \le v \le v_5 - 1$ are evaluated exactly with zero tail).
   - Pure densities $P_p = 1/(p-1)$ if $v_p = \infty$ else $(p^{v_p} - 1)/((p-1)p^{v_p})$, $n_p = 1/P_p$.
   - Stage 7: $1 < C_7 \le 7$, $C_7(1 - P_7) \ge 1$, $\tau_7 = n_7(1 - 1/C_7)$, $\beta_7 = n_7 - \tau_7 > 0$, $\tau_7 \ge 1 + n_7/7$ (so $\Delta_7 = (\tau_7 - 1) - n_7/7 \ge 0$), and $S_s := \min(1, C_7(6 - s)/7) \in [C_7/7, 1]$ for all $s \in \{0, 1, 2, 3, 4\}$.
   - Later stages ($p > 7$): $1 \le \tau_p < n_p$, $\beta_p = n_p - \tau_p > 0$, $C_p = n_p / \beta_p$ satisfies $1 < C_p \le p$.
   - Completion hypothesis (Lemma A2): for $D = \{p^e : 1 \le e \le v_p\} \cup \{15, 21, 35, 45, 63, 75, 105, 15 p_3\}$, every $m \in D$ satisfies $\sum_{d \in D,\, d \mid m,\, d < m} 1/d < 1$.
   - If `fixed165` occurs: $w_{15 p_3} := n_{p_3}/p_3 \le 1$, so the residual category-15 weight $m(1+v) - w_{15 p_3} \ge 0$ for all $m \ge 1, v \ge 0$.
2. **Row recomputation:** No duplicate `(phase, key)`. For every row, recompute exact rational reserve $R_{\mathrm{calc}}$ (adding $+1/5$ in `basic75`, valid only when $b = 2, r = -1, d = 0$) and exact rational stage-loss sum $S_{\mathrm{calc}} = \sum_{q \ge 7} L_q$ from the definitions, and verify
   $$R_{\mathrm{calc}} = \texttt{R\_exact}, \qquad S_{\mathrm{calc}} = \texttt{S\_exact}, \qquad R_{\mathrm{calc}} > S_{\mathrm{calc}}.$$
3. **Complete anchor-hierarchy partition:** Traverse the entire normalized anchor hierarchy:
   - All $8$ triples $(a, b, c) \in \{1, 2\} \times \{2, 4\} \times \{a, 3 - a\}$; either all $4$ basic vertices $j \in \{1, 2, 3, 4\}$ close at `basic` (or `basic75` when $b = 2$), or expand to:
   - All minimal $45$-orbit representatives $r \in \{0, \dots, 44\}$ with $3 \nmid r$, $r \not\equiv 1 \pmod 9$, $5 \nmid r$, $r \not\equiv a \pmod{15}$ indexed by $(r \bmod 3, [r \equiv b \pmod 9], [r \equiv a \pmod 5], [r \equiv c \pmod 5])$, all $7$ pairs $(d, k) \in \{1, 2\} \times \{1, 2, 3, 4\} \setminus \{(a, a)\}$, and all $5$ quinary budget vertices $(j, i_e) \in \{(1, 0), (2, 0), (3, 0), (4, 0), (k, 1)\}$; if not closed at `mixed`, expand to:
   - All $280$ tuples $\xi = (x_3, x_5, x_9, x_{15}) \in \{1, 2\} \times \{1, 2, 3, 4\} \times \{2, 4, 5, 7, 8\} \times R_{15}(a)$; if not closed at `coarse` or `spatial`, expand to:
   - All $14$ surviving ternary rows $z \in \{h \in \{0, \dots, 26\} : 3 \nmid h, h \not\equiv 1 \pmod 9, h \neq b\}$; if not closed at `pure3`, expand to:
   - All $7$ residues $\eta \in R_{15}(a)$ at `fixed165`.
   Verify **0 uncovered leaves** and **0 unused rows**.

---

## 4. Global Lower-Bound Assembly Check

After all certificate files pass SHA-256 and exact recomputation checks, `check.py` verifies:
1. Primality and consecutiveness of the first $14$ odd primes $(3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)$, and $\prod_{m=0}^{13} p_m = 307{,}444{,}891{,}294{,}245{,}705 > L_{\mathrm{target}}$ (excluding $\omega(L) \ge 14$).
2. A verified Theorem A certificate exists on $(3, 5, 7, 11, 13, 17, 19, 23)$ with all exponents unrestricted (`inf`) (excluding $\omega(L) \le 8$).
3. For each $r \in \{9, 10, 11, 12, 13\}$, enumerate all exponent vectors $f \in \mathbb{Z}_{\ge 1}^r$ with $\prod_{m=0}^{r-1} p_m^{f_m} < L_{\mathrm{target}}$ (counts: $5{,}028$, $1{,}484$, $248$, $21$, $1$; total $6{,}782$), and verify that every single vector $f$ is componentwise dominated ($f_m \le e_m$ for all $m$, with $\infty$ dominating every integer) by at least one verified certificate on $(p_0, \dots, p_{r-1})$.
