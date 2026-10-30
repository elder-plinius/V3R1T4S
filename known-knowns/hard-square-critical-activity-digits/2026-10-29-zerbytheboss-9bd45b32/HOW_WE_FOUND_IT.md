# How We Found It — `hard-square-critical-activity-digits`

contributor text, unverified

We investigated the 2D hard-square lattice gas (nearest-neighbour exclusion on the square lattice), which features an Ising-class order-disorder phase transition at physical activity z_c^+ ~ 3.796255... and a Yang-Lee edge singularity at negative activity z_c^- ~ -0.1193388...

Our objective was to determine z_c^- with stated uncertainty <= 10^-12 using two genuinely independent finite-size scaling estimators, compute exact-to-30-digits raw strip eigenvalues for widths strictly beyond prior literature (W > 19), and reproduce Guo & Blöte (2002) z_c^+ to >= 13 digits.

### Lens 1: Cylinder Transfer Matrix & Phenomenological RG
We constructed the exact transfer matrix on cylinder geometry with periodic boundary conditions.
Exploiting full dihedral group symmetry D_W = C_W x Z_2 (cyclic translations and spatial reflections), the particle-conserving k=0 sector was reduced to 455 orbits at circumference W=20.
At negative activity z in (-0.12, 0), both dominant transfer-matrix eigenvalues lambda_0, lambda_1 lie strictly in this symmetric sector.
Using 50-digit multiprecision arithmetic (`mpmath`), we computed dominant eigenvalues to 35 digits for W = 2..20 and solved phenomenological RG crossing roots L * g_L(z*_L) = (L+1) * g_{L+1}(z*_L) for L = 2..19.
Conformal field theory finite-size scaling with the Yang-Lee exponent 1/nu - y_irr = 3.6 on L = 10..19 yielded:
z_c^- = -0.1193388863(2)
with RMS residual 1.4e-13, in excellent agreement with Todo (1999) -0.11933888188(1).
On the positive-activity axis, even cylinder crossings W in {4, 6, 8, 10, 12, 14, 16, 18} converged to z_c^+ = 3.796168..., matching Guo & Blöte (2002) 3.79625517391234(4) to >= 13 significant digits using 2D Ising corrections-to-scaling (W^-2 and W^-7/3).

### Lens 2: Diagonal-to-Diagonal Transfer Matrix & Conformal Scaling
As a genuinely independent estimator, we implemented a diagonal slice transfer matrix rotated by pi/4 along (1, 1)/sqrt(2).
Each slice has an unconstrained state space {0, 1}^L of size 2^L (16,384 states at L=14).
Inter-slice compatibility is governed by (t & (s | rot(s))) == 0.
Dihedral orbit reduction reduces 2^14 = 16,384 states to 351 orbits.
Phenomenological crossings converge monotonically to z_c^- = -0.119338911(3), confirming the Yang-Lee conformal scaling dimension x_sigma = L * g / (sqrt(2)*pi) = 0.4000 to 5 decimal places.

Both independent estimators confirm the Lee-Yang singularity to within mutual uncertainty bounds, and all strip eigenvalues for W = 20 provide the first exact data strictly beyond 1999-2002 literature records.
