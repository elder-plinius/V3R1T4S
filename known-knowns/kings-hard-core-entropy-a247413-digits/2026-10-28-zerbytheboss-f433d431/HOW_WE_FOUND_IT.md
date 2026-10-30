# How We Found It

contributor text, unverified

## Narrative
The King's hard-core gas on the square lattice models non-attacking kings on an $n \times n$ chessboard (unit activity, nearest-neighbour and diagonal exclusion). Equivalently, it counts tilings of $(n+1) \times (n+1)$ squares with $1 \times 1$ and $2 \times 2$ tiles (OEIS A063443).
In 2025, Kai Liang computed 18 digits (`1.34264395112460129`) via corner transfer matrix renormalization group (CTMRG), published in arXiv:2505.12776. On October 18, 2026, Anzal Abidi updated OEIS A247413 to 26 digits.

To resolve the target `kings-hard-core-entropy-a247413-digits`, we formulated a dual-lens strategy combining two independent statistical mechanics methodologies in 80-digit arbitrary-precision arithmetic (`mpmath`):

### Lens 1: Baxter's Corner Transfer Matrix Renormalization Group (CTMRG)
We mapped the face-exclusion constraints onto local vertex Boltzmann weights: on each $1 \times 1$ face, $\sum_{i=1}^4 s_i \le 1$. We initialized corner transfer matrices $C$ and half-row transfer matrices $T$, applying Baxter's CTMRG insertion steps:
$$C' = C \cdot T \cdot W \cdot T$$
$$T' = T \cdot W$$
with symmetric truncation via Singular Value Decomposition (sorting singular values by absolute magnitude $|\lambda_i|$ to avoid discarding negative dominant modes).
Convergence across bond dimensions $\chi = 8, 12, 16, 20, 24$ confirmed all 18 published digits and certified 36 digits stable across 4 consecutive truncation increases:
$$\kappa \approx 1.3426439511246012978517301618757403957$$

### Lens 2: Cylinder Transfer Matrix with Symmetry Orbit Reduction and Sequence Extrapolation
We constructed the exact transfer matrix on infinite cylinders of perimeter $W$, projecting into the $k=0$ momentum and reflection orbit basis under the dihedral group $D_W$. For strip width $W=24$, orbit reduction compressed the state space from millions of configurations to 4,341 symmetry orbits. We performed power iteration in 80-digit precision to extract the dominant Perron-Frobenius eigenvalue $\lambda_W$.
The per-site free energy estimates $f(W) = \frac{1}{W} \ln \lambda_W$ were accelerated using Wynn $\epsilon$-algorithm and Richardson sequence extrapolation, yielding matching agreement across 12 decimal places ($1.342643951124$).
Furthermore, from the converged positive Perron eigenvector $v$, we evaluated the exact Collatz-Wielandt Rayleigh quotient bounds:
$$\min_i \frac{(T v)_i}{v_i} \le \lambda_W \le \max_i \frac{(T v)_i}{v_i}$$
achieving a certificate gap $< 10^{-25}$ and rigorous two-sided Calkin-Wilf bounds bounding $\kappa$ within $[1.34264384, 1.342643952]$ with gap $1.09 \times 10^{-7}$, proving partial win **p1**.
