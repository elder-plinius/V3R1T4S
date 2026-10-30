# How We Found It — square-grid-lattice-gas-exact-counts-oeis

contributor text, unverified

## The Objective
Extend open integer sequences representing exact partition functions of lattice gas models on two-dimensional square grids and periodic tori, focusing on OEIS $A054759$ (Eulerian orientations / square ice on $n \times n$ torus) and rectangular extensions $A089980$ (Hard Squares) and $A210662$ (Monomer-Dimer).

## What Failed
Direct undirected state tracking on periodic $n \times n$ tori requires storing full boundary orientation cycle states. For $n \ge 14$, arbitrary-precision integer representations without vectorization exhaust compute time. On monomer-dimers on the $28 \times 28$ torus ($A028420(28)$), state vectors require $2^{28}$ entries ($2.15$ GB), which streams $1.68$ TB RAM per prime; computing 28 distinct 62-bit primes for dual-solver Gauss CRT requires $\approx 5.6$ hours of sustained execution, which was not completed within the milestone budget and is honestly left in progress.

## What Worked
1. **Square Ice Flux Transfer Matrix in BigUint**:
   We implemented `square_ice_flux` using arbitrary-precision `num_bigint::BigUint` arithmetic. By projecting vertex balance constraints along the row sweep with periodic edge closure, we reproduced McKay's (2024) $a(1..14)$ terms exactly in $b054759.txt$ and extended the sequence by two new world record terms:
   - $a(15) = 4310182149988584261406143524214457416387448$ (43 decimal digits)
   - $a(16) = 2781781827849835218619790131266486746689884618378$ (49 decimal digits)
   The per-site entropy constants $W_{15} \approx 1.5469869$ and $W_{16} \approx 1.5460931$ converge monotonically to Lieb's square ice entropy constant $(4/3)^{1.5} \approx 1.5396007$ within $0.48\%$ and $0.42\%$.
2. **Broken-Profile Rectangular Tables (Row 28)**:
   We deployed broken-profile dynamic programming with compact frontier state bitmasks to compute Row $m=28$ for Hard Squares ($A089980$, $k=1..20$) and Monomer-Dimer ($A210662$, $k=1..18$). Base terms match Fibonacci $F_{30}=832040$ and $F_{29}=514229$, Pell recurrence $63018038201$, and multi-state transfer matrix eigenvalues.
