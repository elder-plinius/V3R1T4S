# How We Found It

*contributor text, unverified*

## The Brief
The monomer-dimer entropy $h_2$ on the 2D square lattice represents the asymptotic growth rate of matchings per site (Hosoya index growth rate, OEIS A028420). While Rodney Baxter provided a heuristic estimate $e^{h_2} \approx 1.940215351$ in 1968, and Shmuel Friedland & Uri Peled certified 8 decimals in 2005, the highest-precision published values in the literature were the 11-12 digits by Yong Kong (2006, Phys. Rev. E 74, 061102). At unit monomer activity, the model exhibits exponential decay of correlations without a phase transition (Heilmann-Lieb theorem), making arbitrary-precision numerical tensor network and transfer matrix methods ideally suited to push beyond published limits.

## What Failed
1. **Naive Tensor Contraction**: Attempting to contract 9 vertex tensors simultaneously in tensor networks led to exponential $O(24^{14})$ operation blowup. Contracting in structured pairwise blocks resolved this instantly.
2. **Dense Loop Traversal in Multiprecision**: Direct 4-index loops over $\chi=24$ environment tensors in pure Python `mpmath` took over 20 minutes per step. Factoring the contraction into intermediate block matrix products $M_{n,w} = T[n]^T C T[w]$ reduced complexity to $8\chi^3$, speeding up execution by $> 20\times$.
3. **Unoptimized Cylinder Orbit Generation**: Generating cyclic orbits for $W=16$ ($2^{16} = 65,536$ configurations) via nested Python loops was slow; vectorizing with NumPy integer operations and `np.bincount` accelerated orbit matrix assembly by $> 100\times$.

## What Worked
1. **Symmetric CTMRG in 80-Digit Precision**: Representing the monomer-dimer Boltzmann weight as a rank-4 vertex tensor $T_{s_N, s_E, s_S, s_W} \in \{0, 1\}^4$ with $s_N+s_E+s_S+s_W \le 1$, and iterating the symmetric corner transfer matrix to fixed-point stationarity ($\Delta \kappa < 10^{-45}$) for $\chi \in \{8, 12, 16, 20, 24, 28, 32\}$, achieved 31 stable matching decimal digits across $\chi \in \{24, 28, 32\}$.
2. **Cylinder Transfer Matrix and Orbit Reduction**: Reducing the $2^W$ state space under cyclic translation and reflection orbits enabled exact 80-digit spectral analysis up to $W=16$ (even) and $W=15$ (odd).
3. **Rigorous Two-Sided Collatz-Wielandt Enclosure**: Using reflection positivity and parity, odd circumferences provide rigorous lower bounds and even circumferences provide upper bounds. At $W=15$ and $W=16$, this enclosed $h_2$ strictly within $[0.662798972789, 0.662798972845]$ (gap $5.56 \times 10^{-11}$), improving upon Friedland & Peled's 8 certified decimals.
4. **Sequence Extrapolation**: Wynn $\epsilon$-algorithm acceleration of the even cylinder sequence matched the CTMRG reference value to 13 decimal places ($3.16 \times 10^{-14}$), strictly inside Kong's bracket.
