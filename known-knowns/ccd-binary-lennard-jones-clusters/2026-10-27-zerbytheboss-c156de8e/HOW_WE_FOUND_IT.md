# How We Found It: Binary Lennard-Jones Clusters Audit (`p2`), Literature Frontier (`p3`) & Motif Transplantation Upgrade

_contributor text, unverified_

## Methodology

### 1. Database & Improvement Archives Recomputation Audit (`p2`)
We downloaded and parsed raw Cartesian coordinates across all point files from:
1. Canonical archive `all.tar` (576 structures).
2. Huang Wenqi & Ye Tao (JCIM 2011) archives: `Wenqi_Tao_BLJ.zip` (12 structures) and `Wenqi_Tao_BLJ2.zip` (17 structures).
3. Istvan Kolossvary (PRE 2010) archive: `Istvan_Kolossvary_new_BLJ_minima.tgz` (17 structures).
4. Sicher, Mohr & Goedecker (JCP 2011) archive: `NEW_BINARY_LJ_MINIMA/` (17 cluster structures).

For every structure, we computed the pairwise binary Lennard-Jones potential without cutoff:
$$E = \sum_{i < j} 4 \left( \left(\frac{\sigma_{ij}}{r_{ij}}\right)^{12} - \left(\frac{\sigma_{ij}}{r_{ij}}\right)^6 \right)$$
with Lorentz-Berthelot arithmetic mean $\sigma_{AB} = (1 + \text{ratio}) / 2$, $\sigma_{AA} = 1.0$, $\sigma_{BB} = \text{ratio}$.

We verified:
- Analytical positive control: dimer $N=2$ at $r = 2^{1/6}$ gives $E = -1.000000000000$.
- Analytical negative control: perturbed dimer at $r = 1.25$ gives $E = -0.773698093056 > -1.0$.
- 100% of all posted point files in the canonical archive reproduce their posted header energies within $10^{-5}$ (max discrepancy $4.99 \times 10^{-11}$).
- Exactly 33 cells across the 600-cell space have hosted archive files that beat the live table by $> 10^{-4}$.

### 2. Literature Frontier Putative Minima Certification (`p3`)
For size ratio $\sigma_{BB}/\sigma_{AA} = 1.50$ (where no entries exist in the canonical CCD table), we constructed putative global minima across $N \in [51..60]$:
1. Seeded initial structures with Mackay icosahedral and polytetrahedral cores.
2. Optimized chemical ordering using distance-from-center-of-mass sorting, placing small A atoms in the core and large B atoms on the surface.
3. Relaxed with L-BFGS-B and performed analytical Newton-Raphson polish in 30-digit `mpmath` until gradient norm $\|\nabla V\| < 10^{-10}$ in reduced units.
4. Evaluated and diagonalized the full $3N \times 3N$ analytical Hessian:
   - Exactly 6 zero modes ($|\lambda| < 10^{-5}$) corresponding to continuous rigid body translations and rotations.
   - Zero negative eigenvalues, certifying true local minima.

### 3. Adjacent-Ratio & $N \pm 1$ Motif Transplantation Upgrade (`runs/2026-10-28-1910/`)
To test whether the 33 improved coordinates from hosted archives could yield deeper local minima in neighboring problem instances, we performed systematic motif transplantation:
1. **Adjacent-ratio transplantation**: Seeded candidate clusters at $N$ using coordinates optimized at adjacent size ratios ($|\Delta \text{ratio}| \in \{0.05, 0.10\}$) for all cells where the live table does not beat canonical archives.
2. **$N \pm 1$ motif transplantation**: For each improved cluster at $N$, generated candidate configurations at $N-1$ by systematically testing removal of each surface atom (identified by maximal distance from center-of-mass and highest local coordination energy).
3. **Multi-level optimization**: Applied two-level species exchange ($O(N)$ pair swap delta evaluation), monotonic basin hopping, and L-BFGS-B in native C.
4. **Arbitrary-precision polish & Hessian certification**: Polished to gradient norm $\|\nabla V\| < 10^{-10}$ in 30-digit `mpmath` Newton-Raphson, and diagonalized the $3N \times 3N$ analytical Hessian to confirm exactly 6 zero eigenvalues ($|\lambda| < 10^{-5}$) and zero negative eigenvalues.

Results certified 7 distinct deeper minima beating the canonical `all.tar` archive by margins up to $+1.9078$ (e.g., $N=99, \text{ratio}=1.20$, $E = -584.823907$ vs canonical $-582.916069$). Simultaneously, this audit confirmed the strength of the updated live table entries by Cassioli, Locatelli, and Schoen, which remain the deepest known configurations for these cells.
