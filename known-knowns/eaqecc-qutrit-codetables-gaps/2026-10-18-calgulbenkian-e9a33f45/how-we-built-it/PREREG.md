# Preregistration: `eaqecc-qutrit-codetables-gaps`

## 1. Target & Success Criterion
- **Target ID:** `eaqecc-qutrit-codetables-gaps`
- **Category:** `physics` (Tractability 3.5)
- **Status Source:** `https://eaqecc.codetables.de/qutrit.php` (saved locally at `data/qutrit.php.html`, fetched at `2026-10-18T04:25:43Z`, HTTP 200, SHA-256 `37bbf731030c113e2e2e75fe7b5ed0b1d11829cfc4a5f1ad948a38b1ac7c936c`).
- **Direction:** `max` (strictly improve $d > d_{\text{lower}}$ with $d \le d_{\text{upper}}$ for explicit gap cells $(n, k, c)$ with $c \ge 1, k \ge 1$, excluding $(14,3,5)$ and $(33,1,24)$).
- **Success Criterion:** An explicit entanglement-assisted qutrit quantum error-correcting code (EAQECC) with parameters $[[n, k, d; c]]_3$, $c \ge 1$, given by an exact $s \times 2n$ generator matrix $S$ over $\mathrm{GF}(3)$ (symplectic form), such that:
  1. $\mathrm{rank}_{\mathrm{GF}(3)}(S) = s$.
  2. Symplectic commutation matrix $\Omega = S J S^T \pmod 3$, where $J = \begin{pmatrix} 0 & I_n \\ -I_n & 0 \end{pmatrix}$, satisfies $c = \mathrm{rank}_{\mathrm{GF}(3)}(\Omega) / 2 \ge 1$ and $k = n - s + c$.
  3. The exact minimum distance $d = d_{\text{ea}} = \min_{v \in \mathrm{span}(S)^\perp \setminus I} \mathrm{wt}_{\text{symp}}(v)$, where $I = \mathrm{span}(S) \cap \mathrm{span}(S)^\perp$ is the isotropic subgroup (of $\mathrm{GF}(3)$-dimension $r = s - 2c = n - k - c$) and $\mathrm{span}(S)^\perp = \{v \in \mathrm{GF}(3)^{2n} : S J v^T = 0 \pmod 3\}$ (of $\mathrm{GF}(3)$-dimension $m = 2n - s = n + k - c$), is computed by **exhaustive enumeration of all $3^{2n-s} - 1$ nonzero vectors in $\mathrm{span}(S)^\perp$** and satisfies $d_{\text{lower}}(n,k,c) < d \le d_{\text{upper}}(n,k,c)$.
- **Null Test:** `not needed because explicit algebraic code checked deterministically by exact enumeration over GF(3)`.

## 2. Structural Exploits & Algebraic Attack Plan
1. **Dual-Subspace Parameterization ($m = 2n - s = n + k - c \le 16$):**
   Instead of searching over large $s \times 2n$ stabilizer matrices $S$, we parameterize the symplectic dual $W = \mathrm{span}(S)^\perp = \mathrm{span}(H)$ directly via an $m \times 2n$ basis matrix $H$ over $\mathrm{GF}(3)$ where $m = 2n - s = n + k - c$ is small ($m \le 16$, so $3^m \le 4.3 \times 10^7$, or $m \le 14$ where $3^m \le 4.78 \times 10^6$). Any $m \times 2n$ matrix $H$ of rank $m$ with $\mathrm{rank}_{\mathrm{GF}(3)}(H J H^T) = 2k$ uniquely determines $S = \ker(H J)$ of rank $s = 2n - m = n + c - k$ with $\mathrm{rank}_{\mathrm{GF}(3)}(S J S^T) = 2c$ and $\mathrm{span}(S)^\perp = \mathrm{span}(H)$.
2. **Hermitian Hull Tuning via Diagonal Sign Scalings ($W \in \{1, 2\}^n$) on $\mathrm{GF}(9)$ AG & Quasi-Cyclic Codes:**
   A classical $[n, K, d]_9$ linear code $D \subset \mathrm{GF}(9)^n$ with Hermitian hull dimension $h = \dim_{\mathrm{GF}(9)}(D \cap D^{\perp_h})$ yields a pure $[[n, k = K - h, d; c = n - K - h]]_3$ EAQECC with $m = 2K$ and $r = 2h$. Multiplying column $j$ of $D$'s generator matrix by $\alpha_j \in \mathrm{GF}(9)^*$ preserves $[n, K, d]_9$ while scaling the $j$-th term of the Hermitian Gram matrix $G W G^\dagger$ by $w_j = \alpha_j^4 \in \{1, 2\} = \mathrm{GF}(3)^*$. In `qutrit.php.html`, the propagation rule `increasing dimension` ($[[n, k+1, d; c+1]]_3$) only propagates to smaller hull dimensions $h' < h_0$, leaving gaps at larger hull dimensions $h > h_0$ (the non-catalytic direction $[[n, k-1, d; c-1]]_3$) and along classical shortenings $[n-1, K-1, d]_9$ ($[[n-1, k-1, d; c]]_3$, which is absent from the table's 8 propagation rules).
3. **Odd-$m$ $\mathrm{GF}(3)$-Additive Extensions and Shortened/Quasi-Cyclic Search (`eaqecc_search.c`):**
   - Elliptic curve codes on $y^3 + y = x^2$ over $\mathrm{GF}(9)$ ($n = 16, d = 16 - K$) with full $2^{15}$ Gray-code sign scaling search and divisor/subcode selection.
   - Shortened, punctured, and quasi-cyclic/constacyclic/Toeplitz $[n, K, d]_9$ codes and $\mathrm{GF}(3)$-additive $m \times 2n$ codes for $n \in [12, 24]$ and $m = n + k - c \in [6, 16]$.
   - Exact verification of every candidate via `verify_eaqecc.py`.
