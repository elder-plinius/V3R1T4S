# PREREG: `hard-square-critical-activity-digits`

target_id: hard-square-critical-activity-digits
frozen_utc: 2026-10-29T04:46:50Z
null_test: not needed because deterministic high-precision numerical linear algebra and conformal field theory scaling with exact mathematical eigenvalue bounds and zero empirical noise

## Evaluation Bar
We evaluate the critical activities of the hard-square lattice gas under two independent statistical physics methodologies:
1. **Lens 1 (Cylinder Transfer Matrix Phenomenological RG)**:
   - Row-to-row cylinder transfer matrix in cyclic ($C_L$) and reflection ($D_L$) orbit basis.
   - Exact-to-60-digits Newton-Raphson eigensolver in `mpmath` for leading eigenvalues $\lambda_0(z), \lambda_1(z)$.
   - Phenomenological RG crossing equations:
     - For $z < 0$: $L g_L(z^*_L) = (L+1) g_{L+1}(z^*_L)$ across widths $L = 2, \dots, 20$.
     - For $z > 0$: $L g_L(z^*_L) = (L+2) g_{L+2}(z^*_L)$ for even widths $L = 4, 6, 8, 10, 12, 14, 16$.
2. **Lens 2 (Diagonal-to-Diagonal Transfer Matrix & CTMRG / CFT Scaling)**:
   - Diagonal-to-diagonal transfer matrix (rotated by $\pi/4$) with independent geometry and state basis.
   - Solving diagonal RG crossing $L g_L = (L+1) g_{L+1}$ and extracting central charge $c_L$ and scaling dimension $x_{\sigma, L}$.
   - Corner Transfer Matrix scaling at activity $z$.

## Thresholds for Claim Levels
- **CONFIRMED_SOLUTION**:
  - $z_c^-$ determined with stated uncertainty $\le 10^{-12}$ (or $z_c^+$ to $\le 4 \times 10^{-16}$).
  - Two independent finite-size estimators agree within their combined uncertainties.
  - Raw strip eigenvalue data published to $\ge 30$ digits for verification.
  - Published value $z_c^- = -0.11933888188(1)$ (Todo 1999) matched within combined uncertainty.
- **Partial Win p1**:
  - Exact-to-30-digits transfer-matrix eigenvalue data released as files with generating code for widths strictly beyond prior studies.
- **Partial Win p2**:
  - Reproduction of $z_c^+ = 3.79625517391234(4)$ to at least 13 significant digits with independently written code and documented corrections-to-scaling form.

## Stopping Rule
Calculations stop when:
1. Leading transfer matrix eigenvalues are computed to 60+ decimal digits for all widths $L \le 20$ (row-to-row) and $L \le 16$ (diagonal).
2. All crossing roots $z^*_L$ are certified to 30+ digits.
3. Extrapolations from both independent lenses agree on $z_c^-$ to within $10^{-12}$.
4. $z_c^+$ is reproduced to $\ge 13$ digits.
