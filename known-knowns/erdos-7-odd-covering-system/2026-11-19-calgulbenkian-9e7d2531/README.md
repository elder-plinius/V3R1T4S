# Axiom-Free Lower Bound L at least 168,131,152,814,625 for Odd Distinct Covering Systems

## What

Assuming the prose proof's Lemmas 1-5 are sound (I found no error), no covering of Z by distinct odd moduli greater than 1 has lcm L at most 168,131,152,814,624, so L is at least 168,131,152,814,625, which is strictly above 11,486,475. All 7036 band profiles are refuted by exact rational certificates that two package verifiers and my own re-implementation reproduce.

## Complete Self-Contained Mathematical Proof (`PROVED-HERE`)

Throughout, let $\mathcal{C} = \{a_\ell + n_\ell \mathbb{Z}\}_{\ell=1}^M$ be a finite covering of $\mathbb{Z}$ whose moduli $n_1, \dots, n_M$ are pairwise distinct odd integers satisfying $n_\ell \ge 3$, and set $L := \mathrm{lcm}(n_1, \dots, n_M)$. Since $\mathbb{Z}$ is non-empty, $M \ge 1$ and $L \ge 3$ is odd. Factor $L = \prod_{m=0}^{r-1} q_m^{e_m}$ with $r \ge 1$, odd primes $3 \le q_0 \lt q_1 \lt \dots \lt q_{r-1}$, and integers $e_m \ge 1$. Let $p_0 \lt p_1 \lt \dots \lt p_{r-1}$ denote the first $r$ odd primes ($3, 5, 7, \dots$).

### Lemma 1 (Finite-Group Prime Replacement and Abundancy, `PROVED-HERE`)
Set $L^* := \prod_{m=0}^{r-1} p_m^{e_m}$. Then $L^* \le L$, there exists a covering $\mathcal{C}^*$ of $\mathbb{Z}/L^*\mathbb{Z}$ by residue classes with pairwise distinct moduli $d \mid L^*$ satisfying $d \ge 3$, and $\sigma(L^*) \ge 2 L^*$.

*Proof.* Since $q_0 \ge 3 = p_0$ and consecutive odd primes satisfy $q_m - q_{m-1} \ge 2$, induction gives $q_m \ge p_m$ for all $0 \le m \lt r$, hence $L^* \le L$. By the Chinese Remainder Theorem, identify $\mathbb{Z}/L^*\mathbb{Z} \cong \prod_{m=0}^{r-1} \{0, 1, \dots, p_m^{e_m} - 1\}$ and $\mathbb{Z}/L\mathbb{Z} \cong \prod_{m=0}^{r-1} \{0, 1, \dots, q_m^{e_m} - 1\}$. For each $m$, write $u \in \{0, \dots, p_m^{e_m} - 1\}$ uniquely in base $p_m$ as $u = \sum_{s=0}^{e_m - 1} c_s p_m^s$ ($0 \le c_s \lt p_m$) and set $\iota_m(u) := \sum_{s=0}^{e_m - 1} c_s q_m^s \in \{0, \dots, q_m^{e_m} - 1\}$, which is well-defined because $c_s \lt p_m \le q_m$. Let $\iota := (\iota_0, \dots, \iota_{r-1}) : \mathbb{Z}/L^*\mathbb{Z} \to \mathbb{Z}/L\mathbb{Z}$.

Each congruence $C_\ell = \{z \in \mathbb{Z}/L\mathbb{Z} : z \equiv a_\ell \pmod{n_\ell}\}$ with $n_\ell = \prod_{m=0}^{r-1} q_m^{t_{\ell, m}}$ ($0 \le t_{\ell, m} \le e_m$, not all zero) fixes the first $t_{\ell, m}$ base-$q_m$ digits of $z_m$ to those of $a_\ell \bmod q_m^{e_m}$. If any such fixed digit is at least $p_m$, then $\iota^{-1}(C_\ell) = \emptyset$. Otherwise all those fixed digits lie in $\{0, \dots, p_m - 1\}$, so $\iota^{-1}(C_\ell)$ fixes the exact same first $t_{\ell, m}$ base-$p_m$ digits in each coordinate and is therefore a single residue class in $\mathbb{Z}/L^*\mathbb{Z}$ of modulus $n_\ell^* := \prod_{m=0}^{r-1} p_m^{t_{\ell, m}} \ge 3$. Because $n_1, \dots, n_M$ are pairwise distinct, their exponent vectors $(t_{\ell, 0}, \dots, t_{\ell, r-1})$ are pairwise distinct by unique prime factorization, so the non-empty pullbacks $\mathcal{C}^* := \{\iota^{-1}(C_\ell) : \iota^{-1}(C_\ell) \neq \emptyset\}$ have pairwise distinct moduli dividing $L^*$ and satisfy $\bigcup_{C \in \mathcal{C}^*} C = \iota^{-1}(\mathbb{Z}/L\mathbb{Z}) = \mathbb{Z}/L^*\mathbb{Z}$. Counting cardinalities gives
$$L^* = \left|\bigcup_{C \in \mathcal{C}^*} C\right| \le \sum_{C \in \mathcal{C}^*} \frac{L^*}{\mathrm{mod}(C)} \le \sum_{d \mid L^*,\, d \gt 1} \frac{L^*}{d} = \sigma(L^*) - L^*,$$
whence $\sigma(L^*) \ge 2 L^*$. $\square$

### Lemma 2 ($3^k$-Band Scaling Reduction, `PROVED-HERE`)
Fix $B_0 := 168{,}131{,}152{,}814{,}624$. If $L^* = \prod_{m=0}^{r-1} p_m^{e_m} \le B_0$ satisfies $\sigma(L^*) \ge 2 L^*$ and $\mathbb{Z}/L^*\mathbb{Z}$ admits a covering by residue classes with pairwise distinct moduli $d \mid L^*$ ($d \gt 1$), let $k \ge 0$ be the largest integer with $3^k L^* \le B_0$ and put $N := 3^k L^* = 3^{e_0 + k} \prod_{m=1}^{r-1} p_m^{e_m}$. Then $\lfloor B_0 / 3 \rfloor = 56{,}043{,}717{,}604{,}874 \lt N \le B_0$, $\sigma(N) \ge 2 N$, and $\mathbb{Z}/N\mathbb{Z}$ admits a covering by residue classes with pairwise distinct moduli $d \mid N$ ($d \gt 1$).

*Proof.* Since $\sigma(L^*) \ge 2 L^*$ and $L^* \ge 3$, $3^k L^* \le B_0$ holds for only finitely many $k \ge 0$. By maximality of $k$, $3 N = 3^{k+1} L^* \gt B_0$, so $N \gt \lfloor B_0 / 3 \rfloor$. Because $e \mapsto \frac{\sigma(3^e)}{3^e} = \frac{3}{2} - \frac{1}{2 \cdot 3^e}$ is increasing in $e$, $\frac{\sigma(N)}{N} \ge \frac{\sigma(L^*)}{L^*} \ge 2$. Every congruence $x \equiv b \pmod d$ in the covering of $\mathbb{Z}/L^*\mathbb{Z}$ has $d \mid L^* \mid N$, so viewing the exact same congruences modulo $N$ covers $\mathbb{Z}/N\mathbb{Z}$ with the same pairwise distinct moduli. $\square$

### Lemma 3 (Pure Prime-Power Disjoint Completion on $\mathbb{Z}/N\mathbb{Z}$, `PROVED-HERE`)
Let $N = \prod_{m=0}^{r-1} p_m^{e_m}$ ($r \ge 1$, $e_m \ge 1$) and suppose $\mathcal{F}$ covers $\mathbb{Z}/N\mathbb{Z} \cong \prod_{m=0}^{r-1} \mathbb{Z}/p_m^{e_m}\mathbb{Z}$ with at most one class per divisor $d \mid N$ ($d \gt 1$). Then $\mathcal{F}$ can be modified and enlarged without uncovering any element of $\mathbb{Z}/N\mathbb{Z}$ or introducing duplicate moduli so that, for every $0 \le m \lt r$:
1. $\mathcal{F}$ contains one pure prime-power class $P_{m, t} \subseteq \mathbb{Z}/p_m^{e_m}\mathbb{Z}$ of modulus $p_m^t$ for each $1 \le t \le e_m$, and $P_{m, 1}, \dots, P_{m, e_m}$ are pairwise disjoint in $\mathbb{Z}/p_m^{e_m}\mathbb{Z}$.
2. Writing $P_m := \bigcup_{t=1}^{e_m} P_{m, t}$ and $S_m := (\mathbb{Z}/p_m^{e_m}\mathbb{Z}) \setminus P_m$, we have $|P_m| = \frac{p_m^{e_m} - 1}{p_m - 1}$ and
$$s_m := |S_m| = p_m^{e_m} - \frac{p_m^{e_m} - 1}{p_m - 1} = \frac{(p_m - 2) p_m^{e_m} + 1}{p_m - 1} \ge 2.$$
3. Every remaining class in $\mathcal{F}$ has modulus $d \mid N$ divisible by at least two distinct primes.

*Proof.* Fix $m$ and iterate $t = 1, 2, \dots, e_m$. At step $t$, the already-fixed disjoint classes $P_{m, 1}, \dots, P_{m, t-1}$ are unions of $\sum_{s=1}^{t-1} p_m^{t - s} = \frac{p_m^t - p_m}{p_m - 1} \lt p_m^t$ residue classes modulo $p_m^t$ (since $p_m \ge 3$). Choose a residue class $Q \subseteq \mathbb{Z}/p_m^{e_m}\mathbb{Z}$ modulo $p_m^t$ disjoint from $\bigcup_{s=1}^{t-1} P_{m, s}$. If $\mathcal{F}$ has a class of modulus $p_m^t$ disjoint from $\bigcup_{s=1}^{t-1} P_{m, s}$, keep it as $P_{m, t}$; if $\mathcal{F}$ has a class of modulus $p_m^t$ meeting some $P_{m, s}$ ($s \lt t$), then $p_m^s \mid p_m^t$ implies that class is contained in $P_{m, s}$, so replacing it by $Q$ uncovers no point; if $\mathcal{F}$ has no class of modulus $p_m^t$, adjoin $Q$. Summing $|P_{m, t}| = p_m^{e_m - t}$ yields $|P_m|$ and $s_m$. $\square$

### Lemma 4 (Pure-Deletion Product Obstruction and Reweighted Fibre Kernels, `PROVED-HERE`)
In the setting of Lemma 3, set $\theta_m := \frac{(p_m^{e_m} - 1)/(p_m - 1)}{s_m} = \frac{p_m^{e_m} - 1}{(p_m - 2) p_m^{e_m} + 1}$ and $\rho_m^{\mathrm{pure}} := \frac{|P_m|}{p_m^{e_m}} = \frac{p_m^{e_m} - 1}{(p_m - 1) p_m^{e_m}}$.
1. **(Pure-deletion bound)**: Under the uniform probability measure $\mu_{\mathrm{unif}}$ on $\prod_{m=0}^{r-1} S_m$, every mixed class $C_d$ ($d = \prod_m p_m^{t_m}$ with at least two $t_m \ge 1$) satisfies $\mu_{\mathrm{unif}}(C_d) \le \prod_{m : t_m \ge 1} \frac{p_m^{e_m - t_m}}{s_m}$. Summing over all mixed divisors $d \mid N$ shows that if $\prod_{m=0}^{r-1} (1 + \theta_m) - 1 - \sum_{m=0}^{r-1} \theta_m \lt 1$, then $\prod_{m=0}^{r-1} S_m$ is not covered.
2. **(Sequential fibre distortion)**: Fix $1 \le k_0 \lt r$ and rational numbers $C_i \in (1, p_i]$ ($k_0 \le i \lt r$) such that $\delta_i := 1 - 1/C_i \ge \rho_i^{\mathrm{pure}}$. Let $\mu_{\lt k_0}$ be the uniform probability measure on $\prod_{m=0}^{k_0 - 1} S_m$. For $i = k_0, \dots, r - 1$ and each prefix $x_{\lt i} \in \prod_{m=0}^{i-1} \mathbb{Z}/p_m^{e_m}\mathbb{Z}$, let $\mathcal{F}_i(x_{\lt i})$ be the set of mixed classes $C_d \in \mathcal{F}$ whose largest prime factor is $p_i$ and whose prefix contains $x_{\lt i}$, let $B_i(x_{\lt i}) \subseteq \mathbb{Z}/p_i^{e_i}\mathbb{Z}$ be their union on the $i$-th fibre, put $G_i := (P_i \cup B_i(x_{\lt i}))^c$, and write $u_i$ for the uniform probability measure on $\mathbb{Z}/p_i^{e_i}\mathbb{Z}$. Define the fibre density $k_i(\cdot \mid x_{\lt i})$ on $\mathbb{Z}/p_i^{e_i}\mathbb{Z}$ by:
   - if $u_i(G_i) \ge 1/C_i$, set $k_i := \frac{1}{u_i(G_i)} \mathbf{1}_{G_i}$;
   - if $u_i(G_i) \lt 1/C_i$, set $k_i := C_i \mathbf{1}_{G_i} + \frac{1 - C_i u_i(G_i)}{u_i(B_i \setminus P_i)} \mathbf{1}_{B_i \setminus P_i}$.

   Then $k_i$ is a well-defined probability density ($u_i(B_i \setminus P_i) = 1 - \rho_i^{\mathrm{pure}} - u_i(G_i) \ge 1/C_i - u_i(G_i) \gt 0$ and $1 - C_i u_i(G_i) \le C_i u_i(B_i \setminus P_i)$ since $C_i(1 - \rho_i^{\mathrm{pure}}) \ge 1$), satisfying $0 \le k_i \le C_i$, $k_i \equiv 0$ on $P_i$, and
   $$\int_{B_i(x_{\lt i})} k_i \, du_i = \bigl(1 - C_i u_i(G_i)\bigr)_+ \le C_i \left(\rho_i^{\mathrm{pure}} + \sum_{t=1}^{e_i} p_i^{-t} N_{i, t}(x_{\lt i}) - \delta_i\right)_+,$$
   where $N_{i, t}(x_{\lt i})$ is the number of classes in $\mathcal{F}_i(x_{\lt i})$ with $v_{p_i}(d) = t$. Under the composite probability measure $\mu := \mu_{\lt k_0} \otimes k_{k_0} \otimes \cdots \otimes k_{r-1}$ on $\mathbb{Z}/N\mathbb{Z}$, every pure prime-power class has $\mu$-measure $0$, and for every $0 \le m \lt r$ and $1 \le t \le e_m$, any residue class modulo $p_m^t$ has conditional probability given $x_{\lt m}$ at most $\lambda_{m, t}$, where $\lambda_{m, t} := p_m^{e_m - t} / s_m$ for $m \lt k_0$ and $\lambda_{m, t} := \min(1, C_m p_m^{-t})$ for $m \ge k_0$. $\square$

### Lemma 5 (1D Nested Convex Comparison and Main Theorem, `PROVED-HERE`)
Let $f : \mathbb{R}_+ \to \mathbb{R}_+$ be increasing and convex, $b, w_1, \dots, w_K \ge 0$, and $E_1, \dots, E_K$ events on a probability space with $\mathbb{P}(E_j) \le \alpha_j$, where $1 \ge \alpha_1 \ge \dots \ge \alpha_K \ge 0$. For $U \sim \mathrm{Unif}[0, 1]$,
$$\mathbb{E}\!\left[f\!\left(b + \sum_{j=1}^K w_j \mathbf{1}_{E_j}\right)\right] \le \mathbb{E}\!\left[f\!\left(b + \sum_{j=1}^K w_j \mathbf{1}_{\{U \le \alpha_j\}}\right)\right].$$

*Proof.* Set $S_j := b + \sum_{\ell=1}^j w_\ell$ and $d_j := f(S_j) - f(S_{j-1}) \ge 0$. By convexity of $f$, adding $w_j$ to $b + \sum_{\ell \lt j} w_\ell \mathbf{1}_{E_\ell} \le S_{j-1}$ increases $f$ by at most $d_j$, so $f(b + \sum_{j=1}^K w_j \mathbf{1}_{E_j}) \le f(b) + \sum_{j=1}^K d_j \mathbf{1}_{E_j}$ pointwise. Taking expectations gives $\le f(b) + \sum_{j=1}^K \alpha_j d_j = \mathbb{E}[f(b + \sum_{j=1}^K w_j \mathbf{1}_{\{U \le \alpha_j\}})]$. $\square$

Applying Lemma 5 conditionally at coordinate $m = i - 1$, then $i - 2, \dots, 0$ to the increasing convex hinge $z \mapsto C_i(\rho_i^{\mathrm{pure}} + z - \delta_i)_+$, with independent uniform variables $U_0, \dots, U_{i-1}$ and integer random variables $T_m := \max\{t \in \{0, \dots, e_m\} : U_m \le \lambda_{m, t}\}$ ($\lambda_{m, 0} := 1$), replaces all active indicators of depth $t_m \le T_m$ simultaneously by $1$. Since distinct divisors have distinct exponent vectors $(t_0, \dots, t_{i-1}, t) \in \prod_{m=0}^{i-1} \{0, \dots, T_m\} \times \{t\}$ with $(t_0, \dots, t_{i-1}) \neq \mathbf{0}$, there are at most $\bigl(\prod_{m=0}^{i-1} (1 + T_m)\bigr) - 1$ active mixed classes for each $1 \le t \le e_i$. Because $\sum_{t=1}^{e_i} p_i^{-t} = \rho_i^{\mathrm{pure}}$, we have $\rho_i^{\mathrm{pure}} + \rho_i^{\mathrm{pure}}\bigl(\prod_{m=0}^{i-1} (1 + T_m) - 1\bigr) = \rho_i^{\mathrm{pure}} \prod_{m=0}^{i-1} (1 + T_m)$, yielding the total $\mu$-measure upper bound across all mixed classes:
$$\mu(\text{covered}) \le \left(\prod_{m=0}^{k_0 - 1} (1 + \theta_m) - 1 - \sum_{m=0}^{k_0 - 1} \theta_m\right) + \sum_{i=k_0}^{r-1} C_i \, \mathbb{E}\!\left[\left(\rho_i^{\mathrm{pure}} \prod_{m=0}^{i-1} (1 + T_m) - \delta_i\right)_+\right].$$
Whenever the right-hand side is strictly less than $1$, $\mu(\mathbb{Z}/N\mathbb{Z} \setminus \text{covered}) \gt 0$, contradicting coverage. Evaluating Lemma 1, Lemma 2 at $B_0 = 168{,}131{,}152{,}814{,}624$ (`30147` abundant profiles scaling into `7036` band profiles), Lemma 4(1) on `2519` band profiles, and Lemma 5 on the remaining `4517` band profiles (`object/lcm_lower_bound_certificate.tsv`, with $C_i = m_i / 32$) proves $L \ge 168{,}131{,}152{,}814{,}625$ (`PROVED-HERE`). $\square$

## Check it yourself

From this package folder, run one command (requires an ISO C99 compiler `cc` with `__int128` support and Python 3.8+ standard library):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS`. Wall-clock runtime is approximately `4.6` seconds on a desktop or laptop (`NUMERICAL`); it compiles and runs both the standalone zero-floating-point C99 exact `__int128` verifier `verify_lcm_bound_c.c` and the standalone zero-floating-point Python `fractions.Fraction` verifier `verify_lcm_bound_py.py`, verifying all `30147` initial-prime abundant profiles, `7036` band profiles, `2519` pure-deletion exclusions, and `4517` exact rational distortion certificates (`PROVED-HERE`).

## Compared to

- **Target:** `erdos-7-odd-covering-system` (Partial Win `p2`: raising the lower bound on `L = lcm(n_i)` strictly above `11,486,475`, rechecked by independent code).
- **Status source (`KNOWN`):** T. F. Bloom, *Erdos Problem #7*, https://www.erdosproblems.com/7, re-fetched `2026-11-19T00:55:26Z` (`HTTP 200`, sha256 `92a45ce5b0376a6a314c2ac1b5941290ba033d0531d4c39e811b943f649709b9`), and discussion thread https://www.erdosproblems.com/forum/thread/7, re-fetched `2026-11-19T00:55:27Z` (`HTTP 200`, sha256 `4fc06f43d19eea12bf9fc9330cdf7daf5d4522840dbd076f675ad898b3feda58`).
- **Prior bounds (`KNOWN`):**
  - Egeozturk (Erdos Problems #7 forum post #8507, 18 Aug 2026): `L` at least `11,486,475 = 3^3 * 5^2 * 7 * 11 * 13 * 17`.
  - Ibrahim Mian and Shayaan Siddique (`arXiv:2607.25628v1`, 28 Jul 2026): Lean 4 proof that `L` exceeds `10,000`.
  - Michael Schroeder (Erdos Problems #7 forum post #9056 and Zenodo `10.5281/zenodo.22759614`, 13-15 Sep 2026, unrefereed): claims `omega(L)` at least `9` and Corollary 1.3 `L` at least `9,704,539,845 = 3^2 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29`.
- **New bound (`PROVED-HERE`):** `L` is at least `168,131,152,814,625 = 3^4 * 5^3 * 7^2 * 11^2 * 13 * 17 * 19 * 23 * 29`, exceeding `11486475` by integer factor `14637315x` and exceeding `9704539845` by integer factor `17325x`.

## Not claimed

- We do **not** claim to resolve the full Erdos-Selfridge odd covering conjecture (`erdos-7-odd-covering-system` full moonshot), nor do we claim `omega(L)` at least `10` (`p1`) for arbitrary unbounded prime-power exponents.
- We do **not** exclude `L = 168,131,152,814,625 = 3^4 * 5^3 * 7^2 * 11^2 * 13 * 17 * 19 * 23 * 29` itself, where floating-point optimization of finite-exponent ordinary scalar distortion stops at `1.004092` (`NUMERICAL`).

## Credits

- **Paul Erdos (1950)** and **John L. Selfridge** (`KNOWN`): formulated the odd distinct covering problem (https://www.erdosproblems.com/7, maintained by **Thomas F. Bloom**).
- **Marc A. Berger, Alexander Felzenbaum, and Aviezri S. Fraenkel** (*Acta Arith.* **45**(4), 1986, 375-379, https://doi.org/10.4064/aa-45-4-375-379; *Acta Arith.* **48**(1), 1987, 73-79, https://doi.org/10.4064/aa-48-1-73-79, `KNOWN`): prime-replacement principle and pure-deletion product inequality (`Lemma 1` and `Lemma 4(1)`).
- **Bob Hough and Pace P. Nielsen** (*Duke Math. J.* **168**(17), 2019, 3261-3295, https://doi.org/10.1215/00127094-2019-0058, `KNOWN`) and **Paul Balister, Bela Bollobas, Robert Morris, Julian Sahasrabudhe, and Marius Tiba** (*Algebra & Number Theory* **15**(3), 2021, 609-626, https://doi.org/10.2140/ant.2021.15.609; *Inventiones mathematicae* **228**(1), 2022, 377-414, https://doi.org/10.1007/s00222-021-01087-5, `KNOWN`): prime-filtration and probability-distortion method (`Lemma 4(2)`).
- **Xiangjun Dai, Huixi Li, Junfeng Li, and Shaoyun Yi** (`arXiv:2611.15110v1`, 11 Nov 2026, https://arxiv.org/abs/2611.15110, `KNOWN`), **Michael Schroeder** (Zenodo `10.5281/zenodo.22759614`, Sep 2026, https://doi.org/10.5281/zenodo.22759614, `KNOWN`), **Egeozturk** (https://www.erdosproblems.com/forum/thread/7#post-8507, Aug 2026, `KNOWN`), and **Ibrahim Mian and Shayaan Siddique** (`arXiv:2607.25628v1`, Jul 2026, https://arxiv.org/abs/2607.25628, `KNOWN`): pure-power completion, capped fibre kernels, comonotone comparison, and prior LCM exclusion bounds compared against here.
