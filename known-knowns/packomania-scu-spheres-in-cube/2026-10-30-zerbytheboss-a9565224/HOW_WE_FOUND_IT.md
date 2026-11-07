# How We Found It

contributor text, unverified

We investigated Eckard Specht's Packomania portal (`packomania.com`) for spheres in a cube (`scu`).
Running a global audit over all $N \le 1000$ coordinate files revealed local non-monotonicities in the live table where $r(N) < r(N+1)$. Specifically, at $N = 344$, the published table record by Lu Peng was $r = 0.075110834623$, whereas $N = 345$ had $r = 0.075110834635$.
By deleting sphere 186 from the $N = 345$ configuration and running Active-Set Sequential Quadratic Programming (SQP) contact-network optimization, we relaxed internal jamming and expanded the remaining 344 spheres to achieve a certified feasible radius of $r^* = 0.0751108346348785...$.
The resulting packing was verified in 50-digit `mpmath` arithmetic, confirming zero wall penetrations, zero pairwise collisions, a strict improvement margin of $+1.187854 \times 10^{-11}$, and complete non-isometry to the published packing.
