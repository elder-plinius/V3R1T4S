# Preregistration: Hadamard Maximal Determinant Records (`hadamard-maxdet-records`)

## 1. Target Problem & Scope

For an order $n \not\equiv 0 \pmod 4$, let $X \in \{-1, +1\}^{n \times n}$ be a $\{\pm 1\}$ matrix and let
$$D_{\text{norm}}(X) = \frac{|\det X|}{2^{n-1}} \in \mathbb{Z}_{>0}$$
denote its normalized determinant. We target both:
- **Full Win**: Explicit $n \times n$ matrices $X \in \{-1, +1\}^{n \times n}$ for open orders $n \le 119$ whose exact normalized determinant $D_{\text{norm}}(X)$ strictly exceeds the best known record across Orrick's MaxDet archive (`indiana.edu/~maxdet`), Rokicki's `newrec.html`, `Math-AI-Caltech/hadamard-maxdet` (`maxdet_records.csv`), and merged V3R1T4S PR `#155`.
- **Partial Win (`p2`, Frozen Gram Target)**: Explicit $n \times n$ symmetric integer Gram matrices $G$ with $G_{ii} = n$, valid mod-4 pairwise and triple congruences, positive definiteness, $\det G > (\det R_{\text{rec}}(n))^2$, exact rational congruence to both $I_n$ and $n I_n$ ($Q I_n Q^T = G$ and $P (n I_n) P^T = G$), and an explicit $(n-1) \times n$ (or $(n-2) \times n$) $\{\pm 1\}$ submatrix $M_0$ satisfying $M_0 M_0^T = G[:k, :k]$ ($k \ge n-2$).

## 2. Mathematical Constructions

### 2.1 Standard Hadamard Excess Bordering ($n = 4k + 1$)
Given a Hadamard matrix $H_m \in \{-1, +1\}^{m \times m}$ of order $m = n - 1 = 4k$ and sign vectors $r, c \in \{-1, +1\}^m$, let $H(r, c) = \operatorname{diag}(r) H_m \operatorname{diag}(c)$ have excess $\Sigma(r, c) = \mathbf{1}_m^T H(r, c) \mathbf{1}_m \equiv 0 \pmod 4$. The bordered $n \times n$ matrix
$$X(r, c) = \begin{pmatrix} -1 & \mathbf{1}_m^T \\ \mathbf{1}_m & H(r, c) \end{pmatrix}$$
has exact normalized determinant
$$D_{\text{norm}}(X) = \left(k + \frac{\Sigma(r, c)}{4}\right) k^{2k-1}.$$

### 2.2 Orrick–Solomon 3-Normalized Construction ($n = 4k + 1$)
Given an $m \times m$ Hadamard matrix $H_m$ ($m = 4k$), choose 3 rows $(r_0, r_1, r_2)$ and relative row signs $(1, s_1, s_2) \in \{1\} \times \{-1, +1\}^2$. Negate columns of $H_m$ so the 3 chosen rows become 3-normalized: $k$ columns $K$ equal to $(-1, -1, -1)^T$, and $3k$ columns of weight $+1$. Flipping the $3 \times k$ block of $-1$'s on $\{r_0, r_1, r_2\} \times K$ to $+1$'s (a rank-1 perturbation $+2 \mathbf{e}_{\{r_0,r_1,r_2\}} \mathbf{e}_K^T$) and bordering with row $0$ having $-1$ on $K$ and $+1$ outside $K$, and column $0$ having $-1$ on $\{r_0, r_1, r_2\}$ and $+1$ on the remaining $m-3$ rows (oriented to have non-negative row sums $E_{3..m-1} = \sum_{i \notin \{r_0,r_1,r_2\}} |\sum_j N'_{ij}|$), yields exact normalized determinant (`arXiv:math/0311292`):
$$D_{\text{norm}}(X) = \left(2k + \frac{E_{3..m-1}}{4}\right) k^{2k-1}.$$

### 2.3 Constructive Frozen Gram Targets (`p2`) for Odd Squares $n = (2s+1)^2$
For $n = 4k + 1$ with a Paley Class I Hadamard matrix $H_m$ ($m = n-1$), the $(n-1) \times n$ matrix $M_0 = [\mathbf{1}_m, H_m]$ realizes $G_0 = M_0 M_0^T = m I_m + J_m$ and has an explicit integer right-kernel vector $u = [-m, (H_m^T \mathbf{1}_m)^T]^T \in \mathbb{Z}^n$ with $\|u\|^2 = 2m^2$. Bordering $G_0$ by $g \in \{5, 1, -3\}^m$ yields
$$\det G = 2^{2(n-1)} k^{2(2k-1)} \frac{2n m^2 - 2m \sum_{i=1}^m g_i^2 + (\sum_{i=1}^m g_i)^2}{16},$$
which admits an explicit rational factor $Q \in \mathbb{Q}^{n \times n}$ ($Q Q^T = G$, and $P = Q/\sqrt{n}$ satisfying $P (n I_n) P^T = G$) whenever $\operatorname{val}(g) = 2nm^2 - 2m \sum g_i^2 + (\sum g_i)^2 = r^2$ is an integer square with $4 \mid r$.

## 3. Dual Independent Verification Protocol
Every candidate matrix and Gram certificate is verified by `tools/verify_hadamard_maxdet.py` using:
1. Exact fraction-free Bareiss integer Gaussian elimination (`det_bareiss`).
2. Independent multi-prime Chinese Remainder Theorem (`det_crt`) over 30-bit primes.
3. Exact check against all standing records in `data/maxdet_table.json` and against Barba's theoretical upper bound $B(n) = \sqrt{2n-1}(n-1)^{(n-1)/2}$.
