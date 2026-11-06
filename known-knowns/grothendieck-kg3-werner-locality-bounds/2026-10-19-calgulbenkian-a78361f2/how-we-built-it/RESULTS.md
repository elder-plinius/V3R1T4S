# Certified Lower Bounds on Grothendieck Constants $K_G(8)$ and $K_G(9)$ via Exact $E_8$ Weyl-Chamber Reduction

## Summary of Achievements
- **Target**: `grothendieck-kg3-werner-locality-bounds`
- **Partial Win `p2` Achieved**: Exact certification of the local bound $\mathrm{SDP}_1(A) = 6104$ for the $120 \times 120$ symmetric $E_8$ root-system instance (`d8_n1_120x120.mat`, $d = 8, m = 120$) listed as an uncertified heuristic (`1.51376*`) in Table 1 and Table 2a of Designolle, Vértesi & Pokutta ([arXiv:2409.03739v3](https://arxiv.org/abs/2409.03739)). Our independent exact method certifies $\mathrm{SDP}_1(A) = 6104$ in **0.10 seconds** (well under the 1-hour verification budget).
- **Partial Win `p1` Achieved**: Certified improvement of the lower bound on $K_G(d)$ for $d \in \{8, 9\}$ over Table 2 of [arXiv:2409.03739v3](https://arxiv.org/abs/2409.03739):
  $$K_G(9) \ge K_G(8) \ge \frac{\mathrm{SDP}_8(A)}{\mathrm{SDP}_1(A)} = \frac{9240}{6104} = \frac{165}{109} \approx 1.5137614678899083,$$
  improving the best certified bound in Table 2 of `arXiv:2409.03739v3` ($1.49339$, inherited from $d=5$ by monotonicity) by **$+0.0203757$** (more than $2000\times$ the $10^{-5}$ minimum margin).
- **Additional Certification**: The same Weyl-chamber parity reduction certifies the $63 \times 63$ symmetric $E_7$ positive-root instance (`d7_n1_63x63.mat`, $d = 7, m = 63$, $A = 3 G_{E_7} - 7 I_{63}$), proving $\mathrm{SDP}_1(A) = 1991$ and $\mathrm{SDP}_7(A) = 2961$ in **0.02 seconds**.

| Dimension $d$ | Instance | Size $m_1 \times m_2$ | $\mathrm{SDP}_d(A)$ (Exact) | $\mathrm{SDP}_1(A)$ (Certified Exact) | Certified Lower Bound on $K_G(d)$ | Previous Certified Bound (`2409.03739` Table 2) | Improvement | Verification Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| $d = 8$ | `d8_n1_120x120.mat` ($E_8$) | $120 \times 120$ | $9240$ | $6104$ | $\mathbf{165/109 \approx 1.51376147}$ | $1.49339$ | **$+0.0203757$** | $0.10\text{ s}$ |
| $d = 9$ | Monotonicity from $d = 8$ | $120 \times 120$ | $9240$ | $6104$ | $\mathbf{165/109 \approx 1.51376147}$ | $1.49339$ | **$+0.0203757$** | $0.10\text{ s}$ |
| $d = 7$ | `d7_n1_63x63.mat` ($E_7$) | $63 \times 63$ | $2961$ | $1991$ | $2961/1991 \approx 1.48719237$ | $1.49339$ | (Confirming Table 2a) | $0.02\text{ s}$ |

---

## Mathematical Proof of the Exact Certificate for $E_8$ ($120 \times 120$)

### 1. Exact Integer Structure and Quantum Value $\mathrm{SDP}_8(A) = 9240$
Let $\Phi^+(E_8) = \{v_1, \dots, v_{120}\} \subset \mathbb{R}^8$ be the 120 positive roots of the $E_8$ root lattice, each of squared Euclidean norm $\|v_x\|_2^2 = 2$, and let $V \in \mathbb{R}^{120 \times 8}$ be the matrix with rows $v_1, \dots, v_{120}$. Its Gram matrix
$$G = V V^T \in \mathbb{Z}^{120 \times 120}$$
has diagonal entries $G_{xx} = 2$ and off-diagonal entries $G_{xy} = \langle v_x, v_y \rangle \in \{-1, 0, +1\}$. Because $\Phi^+(E_8)$ forms a spherical $2$-design (tight frame) in $\mathbb{R}^8$, $G$ satisfies the exact polynomial identity
$$G^2 = 30 G, \qquad \operatorname{Tr}(G) = 240, \qquad \operatorname{rank}(G) = 8.$$
The matrix $P = \frac{1}{2} G \succeq 0$ has unit diagonal ($\operatorname{diag}(P) = \mathbf{1}_{120}$) and rank $8$.

In `d8_n1_120x120.mat`, the Bell/Grothendieck matrix is the exact integer matrix
$$A = 3 G - 13 I_{120} = 6 P - 13 I_{120} \in \mathbb{Z}^{120 \times 120},$$
with diagonal entries $-7$ and off-diagonal entries in $\{-3, 0, +3\}$. Since $G$ has eigenvalue $30$ with multiplicity $8$ and eigenvalue $0$ with multiplicity $112$, $A$ has maximum eigenvalue $\lambda_{\max}(A) = 3(30) - 13 = 77$ with multiplicity $8$. Thus, for any positive semidefinite matrix $X \succeq 0$ with $\operatorname{diag}(X) = \mathbf{1}_{120}$,
$$\langle A, X \rangle \le \lambda_{\max}(A) \operatorname{Tr}(X) = 77 \times 120 = 9240,$$
with equality attained at the rank-$8$ Gram matrix $X = P = \frac{1}{2} G$:
$$\mathrm{SDP}_8(A) = \mathrm{SDP}_\infty(A) = \langle A, P \rangle = \frac{3 \operatorname{Tr}(G^2) - 13 \operatorname{Tr}(G)}{2} = \frac{3(7200) - 13(240)}{2} = 9240.$$

---

### 2. Exact Reduction of the $2^{120}$ QUBO to the $E_8$ Fundamental Weyl Chamber
For any sign vector $a \in \{\pm 1\}^{120}$, let
$$X = V^T a = \sum_{x=1}^{120} a_x v_x \in E_8 \subset \mathbb{R}^8.$$
Then for each $y \in \{1, \dots, 120\}$, $(A a)_y = 3 \langle v_y, X \rangle - 13 a_y$, so maximizing over $b \in \{\pm 1\}^{120}$ gives
$$\max_{b \in \{\pm 1\}^{120}} a^T A b = \sum_{y=1}^{120} \left| 3 \langle v_y, X \rangle - 13 a_y \right| = \sum_{y=1}^{120} \left| 3 a_y \langle v_y, X \rangle - 13 \right|.$$
Using the identity $|t - 13| = (13 - t) + 2 \max(0, t - 13)$ for $t = 3 a_y \langle v_y, X \rangle$ and summing over $y = 1, \dots, 120$ (noting that $\sum_{y=1}^{120} a_y \langle v_y, X \rangle = \|X\|_2^2$) yields the **exact identity**:
$$\max_{b \in \{\pm 1\}^{120}} a^T A b = 1560 - 3 \|X\|_2^2 + 2 \sum_{y=1}^{120} \max\left(0, 3 a_y \langle v_y, X \rangle - 13\right) \le \Phi(X),$$
where
$$\Phi(X) := 1560 - 3 \|X\|_2^2 + 2 \sum_{y=1}^{120} \max\left(0, 3 |\langle v_y, X \rangle| - 13\right).$$

### 3. The $2 E_8$ Parity Invariant and Closed-Form Quadratic Decomposition on $C(E_8)$
Let $\alpha_1, \dots, \alpha_8$ be the simple roots of $E_8$ with Cartan matrix $C = C_{E_8}$ ($\det C = 1$), and let $\omega_1, \dots, \omega_8$ be the fundamental weights ($\langle \alpha_i, \omega_j \rangle = \delta_{ij}$, so $\omega_i$ also form a $\mathbb{Z}$-basis of $E_8$).
1. **Parity Invariant ($X \in 2 E_8$)**:
   The sum of all 120 positive roots is $2 \rho = 2 \sum_{i=1}^8 \omega_i \in 2 E_8$. For every $a \in \{\pm 1\}^{120}$, since $a_y = 1 - 2 \mathbb{I}(a_y = -1)$, we have
   $$X = \sum_{y=1}^{120} a_y v_y = 2 \rho - 2 \sum_{y : a_y = -1} v_y \in 2 E_8.$$
2. **Reduction to the Fundamental Weyl Chamber $C(E_8) \cap 2 E_8$**:
   Since the Weyl group $W(E_8)$ preserves $2 E_8$, the Euclidean norm $\|\cdot\|_2$, and the full root system $\pm \Phi^+(E_8)$, $\Phi(X)$ is $W(E_8)$-invariant. Every orbit of $W(E_8)$ on $2 E_8$ intersects the fundamental Weyl chamber $C(E_8) = \{X \in \mathbb{R}^8 : \langle \alpha_i, X \rangle \ge 0 \ \forall i\}$ in a unique dominant vector
   $$X = \sum_{i=1}^8 c_i \omega_i = 2 \sum_{i=1}^8 d_i \omega_i, \qquad d = (d_1, \dots, d_8) \in \mathbb{Z}_{\ge 0}^8 \quad (c = 2d).$$
3. **Completing the Square on $C(E_8)$**:
   On $C(E_8)$, every positive root $v_y = \sum_{i=1}^8 N_{y, i} \alpha_i \in \Phi^+(E_8)$ ($N_{y, i} \in \mathbb{Z}_{\ge 0}$) has non-negative inner product $\langle v_y, X \rangle = (N c)_y = 2 (N d)_y \ge 0$. Using $|3\langle v_y, X\rangle - 13| = (3\langle v_y, X\rangle - 13) + 2\max(0, 13 - 3\langle v_y, X\rangle)$ and $\sum_{y=1}^{120} v_y = 2\rho = 2\sum_{i=1}^8 \omega_i$ with $\|\rho\|_2^2 = \mathbf{1}^T C^{-1} \mathbf{1} = 620$, we complete the square:
   $$\Phi(2d) = 5880 - 12 (d - \mathbf{1})^T C^{-1} (d - \mathbf{1}) + R(2d), \qquad R(2d) := 2 \sum_{y=1}^{120} \max\left(0, 13 - 6 (N d)_y\right).$$

### 4. Finite $4^8 = 65,536$ Verification and Global Maximum $6104$
Because $N_{y, i} \in \mathbb{Z}_{\ge 0}$, we have $13 - 6(Nd)_y \le 0$ whenever $(Nd)_y \ge 3$. Consequently, $R(2d) = R(2\bar{d})$ depends **only** on the truncated tuple
$$\bar{d} = \min(3, d) \in \{0, 1, 2, 3\}^8 \qquad (4^8 = 65,536 \text{ tuples}).$$
For each of the $65,536$ tuples $\bar{d} \in \{0, 1, 2, 3\}^8$:
- $\Phi(2d) \ge 6090$ requires $12 (d - \mathbf{1})^T C^{-1} (d - \mathbf{1}) \le R(2\bar{d}) - 210$.
- Only $6,315$ tuples $\bar{d}$ satisfy $R(2\bar{d}) \ge 210$ (and $5,989$ satisfy $R(2\bar{d}) \ge 224$).
- Because $C^{-1}$ is strictly positive definite, for each such $\bar{d}$ the positive-definite quadratic bound on any coordinates with $d_i \ge 3$ restricts $d$ to a small finite box checked in exact integer arithmetic via Schur complements.

Executing this exhaustive check in `results/verify_grothendieck.py` takes **0.10 seconds** and proves that over the **entire** infinite cone $d \in \mathbb{Z}_{\ge 0}^8$:
$$\max_{d \in \mathbb{Z}_{\ge 0}^8} \Phi(2d) = 6104,$$
attained uniquely at the 4 dominant vectors $c = 2d \in (2\mathbb{Z}_{\ge 0})^8$:
1. $c = (2, 0, 12, 0, 0, 0, 0, 0)$ ($\Phi(c) = 6104$, $12(d-\mathbf{1})^T C^{-1}(d-\mathbf{1}) = 336$, $R(c) = 560$)
2. $c = (2, 0, 0, 0, 10, 0, 0, 0)$ ($\Phi(c) = 6104$, $12(d-\mathbf{1})^T C^{-1}(d-\mathbf{1}) = 144$, $R(c) = 368$)
3. $c = (0, 2, 0, 0, 10, 0, 0, 0)$ ($\Phi(c) = 6104$, $12(d-\mathbf{1})^T C^{-1}(d-\mathbf{1}) = 144$, $R(c) = 368$)
4. $c = (0, 0, 0, 0, 10, 0, 2, 0)$ ($\Phi(c) = 6104$, $12(d-\mathbf{1})^T C^{-1}(d-\mathbf{1}) = 144$, $R(c) = 368$),
with the next largest value of $\Phi(2d)$ on $d \in \mathbb{Z}_{\ge 0}^8$ being $6094$ at $c = (0, 0, 0, 0, 0, 14, 0, 0)$.

Combined with the explicit sign vectors $a^*, b^* \in \{\pm 1\}^{120}$ achieving $(a^*)^T A b^* = 6104$ (where $V^T a^*$ lies in the $W(E_8)$-orbit of $c = (0, 0, 0, 0, 10, 0, 2, 0)$ with $\|V^T a^*\|_2^2 = 2424$), this completes the exact proof that
$$\mathrm{SDP}_1(A) = 6104 \implies K_G(9) \ge K_G(8) \ge \frac{9240}{6104} = \frac{165}{109} \approx 1.5137614678899083.$$

---

## Reproduction Instructions
Run the self-contained exact verification script:
```bash
python3 results/verify_grothendieck.py
```
The script verifies the exact integer matrices, explicit lower-bound vectors, quantum values, and exhaustive Weyl-chamber certificates for both `d8_n1_120x120.mat` ($d=8, m=120$) and `d7_n1_63x63.mat` ($d=7, m=63$) in under $0.2$ seconds, saving the full certificate data to `results/e8_120x120_certificate.json`.
