# Self-Contained Mathematical Proof of the 4-to-1 Qubit QRAC Bound

## Main Theorem

For every 4-to-1 quantum random access code (QRAC) over a single qubit assisted by shared classical randomness, the worst-case success probability $p(4)$ satisfies

$$\frac{1}{2} + \frac{1 + \sqrt{3}}{8\sqrt{2}} \le p(4) \le 0.7414817995596351 < 0.741481 + 10^{-6} = 0.741482.$$

In numerical decimal form, the Ambainis-Leung-Mancinska-Ozols lower bound is $0.741481456572267067\ldots$, so the Ambainis 4-to-1 construction is globally optimal within $3.43 \times 10^{-7}$.

---

## 1. Bloch-Vector Formulation

By Yao's minimax principle (proved explicitly for $n$-to-1 QRACs in Ambainis, Leung, Mancinska, and Ozols, `arXiv:0810.2937`, Lemma 2 and Theorem 3), the optimal worst-case success probability $p(n)$ of an $n$-to-1 one-qubit QRAC with shared randomness equals the optimal average success probability over a uniform input $x \in \{\pm 1\}^n$ and uniform index $i \in \{1, \dots, n\}$ without shared randomness.

Let Bob's $n$ binary projective/POVM measurements have Bloch vectors $v_1, \dots, v_n \in B^3 = \{v \in \mathbb{R}^3 : \|v\|_2 \le 1\}$, corresponding to measurement operators $M_i^{\pm} = \frac{1}{2}(I_2 \pm v_i \cdot \vec{\sigma})$ (mixing with trivial outcomes only shrinks $\|v_i\|_2$). For an input string $x \in \{\pm 1\}^n$, Bob's average success probability on state $\rho_x$ is

$$\frac{1}{n} \sum_{i=1}^n \mathrm{tr}\!\left(\rho_x \frac{I_2 + x_i v_i \cdot \vec{\sigma}}{2}\right) = \frac{1}{2} + \frac{1}{2n} \mathrm{tr}\!\left(\rho_x \left(\sum_{i=1}^n x_i v_i\right) \cdot \vec{\sigma}\right).$$

Maximizing over all single-qubit density matrices $\rho_x$ (Helstrom's bound) yields $\frac{1}{2} + \frac{1}{2n} \left\|\sum_{i=1}^n x_i v_i\right\|_2$, achieved when $\rho_x$ aligns with $\sum_{i=1}^n x_i v_i$. Averaging uniformly over the $2^n$ strings $x \in \{\pm 1\}^n$ gives

$$p(n) = \max_{v_1, \dots, v_n \in B^3} P_n(v_1, \dots, v_n), \qquad P_n(v_1, \dots, v_n) := \frac{1}{2} + \frac{1}{n 2^{n+1}} \sum_{x \in \{\pm 1\}^n} \left\| \sum_{i=1}^n x_i v_i \right\|_2.$$

Because the Euclidean norm $\|\cdot\|_2$ is convex on $\mathbb{R}^3$, $P_n$ is separately convex in each $v_i \in B^3$. Since the extreme points of the closed unit ball $B^3$ are the unit sphere $S^2$, the global maximum is attained on $(S^2)^n$. For $n = 4$, using the negation symmetry $\|-w\|_2 = \|w\|_2$ under $x \mapsto -x$ to fix $x_1 = +1$, we obtain

$$p(4) = \max_{v_1, v_2, v_3, v_4 \in S^2} p(v_1, v_2, v_3, v_4), \qquad p(v_1, v_2, v_3, v_4) = \frac{1}{2} + \frac{1}{64} \sum_{s \in \{+1\} \times \{\pm 1\}^3} \left\| v_1 + s_2 v_2 + s_3 v_3 + s_4 v_4 \right\|_2.$$

Evaluating at $v_1 = v_2 = (0, 0, 1)$, $v_3 = (1, 0, 0)$, $v_4 = (0, 1, 0)$ yields four sign tuples with $s_2 = -1$ having $\|s_3 e_1 + s_4 e_2\|_2 = \sqrt{2}$ and four sign tuples with $s_2 = +1$ having $\|2 e_3 + s_3 e_1 + s_4 e_2\|_2 = \sqrt{6}$, so

$$p(e_3, e_3, e_1, e_2) = \frac{1}{2} + \frac{4\sqrt{2} + 4\sqrt{6}}{64} = \frac{1}{2} + \frac{1 + \sqrt{3}}{8\sqrt{2}} = 0.741481456572267067\ldots$$

---

## 2. Theorem 1: Constructive Symmetry Reduction and Rational Weierstrass Parameterization

Define the rational Weierstrass map $\mathcal{W} : \mathbb{R}^2 \to S^2$ by

$$\mathcal{W}(a, b) := \left(\frac{2a}{1 + a^2 + b^2}, \frac{2b}{1 + a^2 + b^2}, \frac{1 - a^2 - b^2}{1 + a^2 + b^2}\right).$$

Note that $\|\mathcal{W}(a, b)\|_2^2 = \frac{4a^2 + 4b^2 + (1 - a^2 - b^2)^2}{(1 + a^2 + b^2)^2} = \frac{(1 + a^2 + b^2)^2}{(1 + a^2 + b^2)^2} = 1$ identically on $\mathbb{R}^2$. On the closed unit disk $a^2 + b^2 \le 1$, $\mathcal{W}$ is a bijection onto the closed upper hemisphere $S^2_+ = \{v \in S^2 : v_z \ge 0\}$ with smooth inverse $(a, b) = \left(\frac{v_x}{1 + v_z}, \frac{v_y}{1 + v_z}\right)$ (since $1 + v_z \in [1, 2]$).

For $z = (a_2, b_2, c, a_4, b_4) \in D := [-1, 1]^2 \times [0, 1] \times [-1, 1] \times [0, 1]$, set

$$v_1 = (0, 0, 1), \quad v_2(z) = \mathcal{W}(a_2, b_2), \quad v_3(z) = \mathcal{W}(c, 0), \quad v_4(z) = \mathcal{W}(a_4, b_4),$$

and define the canonical domain $F \subset D$ by the six inequalities:
- `(C4)` $a_4^2 + b_4^2 \le 1$,
- `(C5)` $a_2^2 + b_2^2 \le c^2$,
- `(C6)` $c^2 \le a_4^2 + b_4^2$,
- `(C7)` $|v_2(z) \cdot v_3(z)| \le v_{2,z}(z)$,
- `(C8)` $|v_2(z) \cdot v_4(z)| \le v_{2,z}(z)$,
- `(C9)` $|v_3(z) \cdot v_4(z)| \le v_{2,z}(z)$.

**Claim (Theorem 1).** For every $(u_1, u_2, u_3, u_4) \in (S^2)^4$, there exists $z \in F$ such that $p(u_1, u_2, u_3, u_4) = p(v_1, v_2(z), v_3(z), v_4(z))$.

**Proof.**
1. **Invariance group**: $p(u_1, u_2, u_3, u_4)$ is invariant under:
   - any permutation $\pi \in S_4$ of the four vectors (re-indexing the sum over $\{\pm 1\}^4$);
   - any sign flips $u_k \mapsto \varepsilon_k u_k$ with $\varepsilon_k \in \{\pm 1\}$ (substituting $x_k \mapsto \varepsilon_k x_k$ in $\{\pm 1\}^4$);
   - any orthogonal transformation $R \in O(3)$, including reflections ($\|\sum_i x_i (R u_i)\|_2 = \|R(\sum_i x_i u_i)\|_2 = \|\sum_i x_i u_i\|_2$).
2. **Pairwise inner-product dominance**: Choose a pair $(i^*, j^*)$ with $1 \le i^* < j^* \le 4$ maximizing $|u_i \cdot u_j|$ over all 6 pairs, and permute $\{1, 2, 3, 4\}$ so $(i^*, j^*) \mapsto (1, 2)$. Then $|u_i \cdot u_j| \le |u_1 \cdot u_2|$ for all $1 \le i < j \le 4$.
3. **Hemisphere alignment and radial ordering**: For each $k \in \{2, 3, 4\}$, if $u_1 \cdot u_k < 0$, replace $u_k \mapsto -u_k$. This preserves $|u_i \cdot u_j|$ for every pair and ensures $u_1 \cdot u_k = |u_1 \cdot u_k| \ge 0$ for $k = 2, 3, 4$. In particular, $u_1 \cdot u_2 \ge u_1 \cdot u_k \ge 0$ for $k = 3, 4$. Swap $u_3 \leftrightarrow u_4$ if $u_1 \cdot u_3 < u_1 \cdot u_4$, obtaining
   $$0 \le u_1 \cdot u_4 \le u_1 \cdot u_3 \le u_1 \cdot u_2 \le 1, \qquad |u_i \cdot u_j| \le u_1 \cdot u_2 \quad \forall \, 1 \le i < j \le 4.$$
4. **Orthogonal frame alignment**: Choose an orthonormal basis $(f_1, f_2, f_3)$ of $\mathbb{R}^3$ as follows:
   - Set $f_3 = u_1$.
   - If $u_3 \neq u_1$ (note $u_3 \neq -u_1$ because $u_1 \cdot u_3 \ge 0$), set $f_1 = \frac{u_3 - (u_3 \cdot f_3) f_3}{\|u_3 - (u_3 \cdot f_3) f_3\|_2}$; if $u_3 = u_1$, choose any unit vector $f_1 \perp f_3$.
   - Set $f_2 = f_3 \times f_1$; if $u_4 \cdot f_2 < 0$, replace $f_2 \mapsto -f_2$.
   Let $R \in O(3)$ map $(f_1, f_2, f_3)$ to the standard basis $(e_1, e_2, e_3)$, and set $w_k = R u_k$. Then $w_1 = (0, 0, 1)$, $w_{k,z} = u_1 \cdot u_k \in [0, 1]$ for $k = 2, 3, 4$, $w_3 = (w_{3,x}, 0, w_{3,z})$ with $w_{3,x} \ge 0$, and $w_{4,y} \ge 0$.
5. **Weierstrass coordinates**: Since $w_{k,z} \in [0, 1]$ ($1 + w_{k,z} \in [1, 2]$), define
   $$(a_2, b_2) = \left(\frac{w_{2,x}}{1 + w_{2,z}}, \frac{w_{2,y}}{1 + w_{2,z}}\right), \quad c = \frac{w_{3,x}}{1 + w_{3,z}}, \quad (a_4, b_4) = \left(\frac{w_{4,x}}{1 + w_{4,z}}, \frac{w_{4,y}}{1 + w_{4,z}}\right).$$
   For each $k \in \{2, 3, 4\}$, $r_k^2 := a_k^2 + b_k^2 = \frac{1 - w_{k,z}^2}{(1 + w_{k,z})^2} = \frac{1 - w_{k,z}}{1 + w_{k,z}} \in [0, 1]$. Since $w_{3,x} \ge 0, w_{3,y} = 0$, we have $c \in [0, 1]$; since $w_{4,y} \ge 0$, $b_4 \in [0, 1]$; and since $r_k^2 \le 1$, $a_2, b_2, a_4 \in [-1, 1]$. Hence $z = (a_2, b_2, c, a_4, b_4) \in D$. Finally, since $t \mapsto \frac{1 - t}{1 + t}$ is strictly decreasing on $[0, 1]$, the ordering $1 \ge w_{2,z} \ge w_{3,z} \ge w_{4,z} \ge 0$ is equivalent to $0 \le a_2^2 + b_2^2 \le c^2 \le a_4^2 + b_4^2 \le 1$, establishing `(C4)`-`(C6)`, while $|w_i \cdot w_j| \le w_{2,z}$ gives `(C7)`-`(C9)`. $\square$

**Corollary (Symmetry Exclusion Codes `S4`..`S9`).** If a box $B \subset D$ satisfies any of the strict interval inequalities
- `S4`: $\min_{z \in B} (a_4^2 + b_4^2) > 1$,
- `S5`: $\min_{z \in B} (a_2^2 + b_2^2) > \max_{z \in B} c^2$,
- `S6`: $\max_{z \in B} (a_4^2 + b_4^2) < \min_{z \in B} c^2$,
- `S7`: $\min_{z \in B} |v_2(z) \cdot v_3(z)| > \max_{z \in B} v_{2,z}(z)$,
- `S8`: $\min_{z \in B} |v_2(z) \cdot v_4(z)| > \max_{z \in B} v_{2,z}(z)$,
- `S9`: $\min_{z \in B} |v_3(z) \cdot v_4(z)| > \max_{z \in B} v_{2,z}(z)$,

then $B \cap F = \emptyset$.

---

## 3. Theorem 2: Singularity-Free AM-GM Rational Quadratic Bound (`A` Leaves)

For each $s = (1, s_2, s_3, s_4) \in \{+1\} \times \{\pm 1\}^3$, let $w_s(z) = v_1 + s_2 v_2(z) + s_3 v_3(z) + s_4 v_4(z)$ and $q_s(z) = \|w_s(z)\|_2^2 \ge 0$. Since $\|v_i(z)\|_2 = 1$,

$$q_s(z) = 4 + 2 \sum_{1 \le i < j \le 4} s_i s_j \big(v_i(z) \cdot v_j(z)\big).$$

**Claim (Theorem 2).** Let $\rho_0, \dots, \rho_7 > 0$ be any eight strictly positive real numbers. Then for all $z \in \mathbb{R}^5$,

$$p(v_1, v_2(z), v_3(z), v_4(z)) \le L(z) := C_0 + \sum_{1 \le i < j \le 4} \alpha_{ij} \big(v_i(z) \cdot v_j(z)\big),$$

where

$$C_0 = \frac{1}{2} + \frac{1}{128} \sum_{s=0}^7 \left(\rho_s + \frac{4}{\rho_s}\right), \qquad \alpha_{ij} = \frac{1}{64} \sum_{s=0}^7 \frac{s_i s_j}{\rho_s}.$$

Moreover, $L : \mathbb{R}^5 \to \mathbb{R}$ is $C^\infty$ smooth everywhere, and on any compact box $B = \{m + y : |y_i| \le r_i\}$,

$$\max_{z \in B} L(z) \le L(m) + \sum_{i=0}^4 \psi\!\left(\partial_i L(m), \max_{\xi \in B} \partial_i^2 L(\xi), r_i\right) + \sum_{0 \le i < j \le 4} \left(\max_{\xi \in B} |\partial_i \partial_j L(\xi)|\right) r_i r_j,$$

where for any $g, h \in \mathbb{R}$ and $r \ge 0$,

$$\psi(g, h, r) = \begin{cases} |g| r + \frac{1}{2} h r^2 & \text{if } h \ge 0 \text{ or } |g| \ge (-h) r, \\ \frac{g^2}{2(-h)} & \text{if } h < 0 \text{ and } |g| < (-h) r. \end{cases}$$

**Proof.** For every $q \ge 0$ and $\rho > 0$, $(\sqrt{q} - \rho)^2 \ge 0$ implies $\sqrt{q} \le \frac{\rho}{2} + \frac{q}{2\rho}$. Summing over $s = 0, \dots, 7$ and substituting $q_s(z) = 4 + 2\sum_{i<j} s_i s_j (v_i(z) \cdot v_j(z))$ yields $p \le L(z)$. Since each $v_k(z)$ is a rational function with denominator $1 + a_k^2 + b_k^2 \ge 1$, $L$ is $C^\infty$ on $\mathbb{R}^5$. By multivariate Taylor's theorem along $t \mapsto m + t y$ ($t \in [0, 1]$), for each $y \in \prod_{i=0}^4 [-r_i, r_i]$ there exists $\xi \in B$ with

$$L(m + y) = L(m) + \sum_{i=0}^4 \left(\partial_i L(m) y_i + \frac{1}{2} \partial_i^2 L(\xi) y_i^2\right) + \sum_{0 \le i < j \le 4} \partial_i \partial_j L(\xi) y_i y_j.$$

Since $y_i^2 \ge 0$, replacing $\partial_i^2 L(\xi)$ by $h_i := \max_{\zeta \in B} \partial_i^2 L(\zeta)$ only increases the quadratic form, and maximizing $g_i y_i + \frac{1}{2} h_i y_i^2$ over $y_i \in [-r_i, r_i]$ equals $\psi(g_i, h_i, r_i)$ (which is monotonically non-decreasing in $|g_i|$). Bounding the off-diagonal terms by $|\partial_i \partial_j L(\xi)| |y_i| |y_j| \le (\max_B |\partial_i \partial_j L|) r_i r_j$ completes the proof. $\square$

---

## 4. Theorem 3: Smooth Concave-Quadratic Tangent Bound (`Q` Leaves)

Suppose that on a compact box $B = \{m + y : |y_i| \le r_i\}$, every sign tuple $s \in \{0, \dots, 7\}$ satisfies $\min_{z \in B} q_s(z) > 0$. Then $p(z) := p(v_1, v_2(z), v_3(z), v_4(z))$ is $C^\infty$ smooth on $B$, with exact gradient and Hessian entries enclosed by outward-rounded interval differentiation (using the identity $|\hat{w}_{s,\alpha}| = |w_{s,\alpha}| / \|w_s\|_2 \le 1$ and Cauchy-Schwarz $\|\partial_i w_s\|_2^2 - (\hat{w}_s \cdot \partial_i w_s)^2 \ge 0$).

Let $H(B) = [H_{ij}^-, H_{ij}^+]_{i,j=0}^4$ be an interval enclosure of $\nabla^2 p(\xi)$ over all $\xi \in B$, decomposed into a symmetric scalar midpoint matrix $H_{\text{mid}}$ and non-negative error radii $H_{\text{rad}, ij} \ge \max_{\xi \in B} |\partial_i \partial_j p(\xi) - H_{\text{mid}, ij}|$.

**Claim (Theorem 3).** Suppose interval $LDL^T$ factorization of $-H_{\text{mid}}$ succeeds with all five diagonal pivots strictly positive ($D_j^- > 0$ for $j = 0, \dots, 4$). Then $-H_{\text{mid}}$ is symmetric positive definite, and for **any** reference vector $u \in \mathbb{R}^5$ and all $z = m + y \in B$:

$$p(m + y) \le p(m) + g_0 \cdot u + \frac{1}{2} u^T H_{\text{mid}} u + \sum_{i=0}^4 \left(|\eta_i| r_i - \eta_i u_i\right) + \frac{1}{2} \sum_{i=0}^4 \sum_{j=0}^4 H_{\text{rad}, ij} r_i r_j,$$

where $g_0 = \nabla p(m)$ and $\eta = g_0 + H_{\text{mid}} u$.

**Proof.** By Sylvester's law of inertia, $-H_{\text{mid}} = L D L^T$ with unit lower-triangular $L$ and strictly positive diagonal $D \succ 0$ implies $-H_{\text{mid}} \succ 0$, so the quadratic function $Q(y) := p(m) + g_0 \cdot y + \frac{1}{2} y^T H_{\text{mid}} y$ is strictly concave on $\mathbb{R}^5$. Therefore, its first-order Taylor expansion at any $u \in \mathbb{R}^5$ is a global upper bound:

$$Q(y) \le Q(u) + \nabla Q(u) \cdot (y - u) = Q(u) + \eta \cdot y - \eta \cdot u \le Q(u) + \sum_{i=0}^4 |\eta_i| r_i - \eta \cdot u \quad \forall \, y \in \prod_{i=0}^4 [-r_i, r_i].$$

Combining with Taylor's theorem $p(m + y) = Q(y) + \frac{1}{2} y^T (\nabla^2 p(\xi) - H_{\text{mid}}) y$ and $|y_i y_j (\partial_i \partial_j p(\xi) - H_{\text{mid}, ij})| \le H_{\text{rad}, ij} r_i r_j$ yields the stated bound. $\square$

---

## 5. Exact Partition Completion (`verify_qrac4.py`)

The certificate `object/certificate_qrac4.json` encodes a finite full binary bisection tree starting from the exact root box $D = [-1, 1] \times [-1, 1] \times [0, 1] \times [-1, 1] \times [0, 1]$. Each internal node `d` ($\in \{0, 1, 2, 3, 4\}$) bisects coordinate $d$ at its exact rational midpoint $m_d = (\text{lo}_d + \text{hi}_d) / 2$ into $[\text{lo}_d, m_d]$ and $[m_d, \text{hi}_d]$, tracked in `verify_qrac4.py` via exact `fractions.Fraction` arithmetic. By induction on the binary tree, the `43,476` leaf boxes partition $D$ with zero gaps:

- `10,914` leaves carry codes `S4`..`S9` and satisfy Theorem 1's strict interval exclusion ($B \cap F = \emptyset$).
- `32,152` leaves carry code `A` and satisfy Theorem 2's outward-rounded `mpmath.iv` (`40` decimal digits) upper bound $\le 0.7414818$.
- `410` leaves carry code `Q` and satisfy Theorem 3's outward-rounded `mpmath.iv` (`40` decimal digits) upper bound $\le 0.7414818$.

Across all leaves intersecting $F$, the maximum certified upper bound is `0.741481799559635048`. By Theorem 1, every $(u_1, u_2, u_3, u_4) \in (S^2)^4$ has an orbit representative in $F \subset D$, proving $p(4) \le 0.741481799559635048 < 0.741481 + 10^{-6}$. $\square$
