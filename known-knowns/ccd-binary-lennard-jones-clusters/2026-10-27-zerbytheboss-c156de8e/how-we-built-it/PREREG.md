# Preregistered Evaluation Bar (`ccd-binary-lennard-jones-clusters`)

- Date: 2026-10-28T22:15:00Z
- Target ID: `ccd-binary-lennard-jones-clusters`
- Success Criteria:
  - Exact binary Lennard-Jones potential $E = \sum_{i < j} 4 ((\sigma_{ij}/r_{ij})^{12} - (\sigma_{ij}/r_{ij})^6)$ with $\sigma_{AA}=1$, $\sigma_{BB}=\text{ratio}$, $\sigma_{AB}=(1+\text{ratio})/2$.
  - Partial win `p2`: A machine-readable merged table of all 600 cells (minimum over the CCD table and all hosted archives, each re-evaluated from coordinates), listing every cell where the live table is beaten by a hosted file by $> 10^{-4}$ and any posted point file that does not reproduce its own posted energy within $10^{-5}$.
  - Analytical Hessian zero-mode tolerance $|\lambda| < 10^{-6}$.
- null_test: not needed because deterministic coordinate re-evaluations and analytical Hessian eigenmode calculations are exact mathematical verifications against published tables.
