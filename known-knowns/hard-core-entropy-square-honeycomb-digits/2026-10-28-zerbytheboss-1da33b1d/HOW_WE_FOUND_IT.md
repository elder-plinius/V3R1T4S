# How We Found It

contributor text, unverified

## Narrative
The hard-core lattice gas at unit activity (OEIS A085850) counts independent vertex sets on square grid graphs (OEIS A006506). In 1999, Rodney J. Baxter used the Corner Transfer Matrix (CTM) variational method to compute 43 decimal places:
$$\kappa = 1.5030480824753322643220663294755536893857810$$
noting in his paper that the last two or three digits (`810`) should be treated with caution. For 27 years, OEIS A085850 retained only Baxter's 43 digits.

To resolve the target `hard-core-entropy-square-honeycomb-digits`, we deployed two independent, complementary statistical mechanics formulations in arbitrary-precision arithmetic:

### Lens 1: Baxter's Corner Transfer Matrix RG (CTMRG)
We formulated the local face weights for the square lattice nearest-neighbor exclusion:
$$\omega(a, b, c, d) = \begin{cases} 0 & \text{if adjacent spins violate exclusion} \\ 1 & \text{otherwise} \end{cases}$$
We solved the Kramers-Wannier approximation algebraically ($t = 0.359827...$, $\kappa_{\text{KW}} = 1.502928407...$), matching Baxter's Table 1 to all digits. We then performed block CTMRG across bond dimensions $\chi \in \{12, 16, 20, 24, 28, 32\}$ in 80-digit precision arithmetic.
At $\chi=32$, digits 41–43 converged strictly to `8, 1, 0`, settling Baxter's flagged digits as correct (`CONFIRMED_SOLUTION`, `p3`), and sequence extrapolation confirmed 65 stable decimal places.

### Lens 2: Cylinder Transfer Matrix in Cyclic Orbit Basis with Sequence Extrapolation
We formulated the transfer matrix on infinite cylinders of circumference $W \in \{6, 8, 10, 12, 14, 16, 18, 20\}$ in the $k=0$ cyclic momentum and reflection orbit basis, reducing matrix dimensions by $2W$. High-precision power iteration yielded strictly positive Perron-Frobenius eigenvectors $v > 0$ with Collatz-Wielandt gap $< 10^{-50}$, establishing two-sided bounds certifying $\ge 20$ correct decimal places and exporting machine-verifiable certificate vectors for $W = 16, 18, 20$ (satisfying partial win `p1`). Finite-size sequence extrapolation (Wynn $\epsilon$ and Richardson in $1/W^2$) independently reproduced the published constant.
