# Preregistered Evaluation Bar (`ccd-binary-lennard-jones-clusters`)

- Date: 2026-10-28T22:15:00Z
- Target ID: `ccd-binary-lennard-jones-clusters`
- Success Criteria:
  - Exact binary Lennard-Jones potential $E = \sum_{i < j} 4 ((\sigma_{ij}/r_{ij})^{12} - (\sigma_{ij}/r_{ij})^6)$
  - Partial win p2: Merged audit table of all 600 cells across CCD table and all 4 hosted improvement archives re-evaluated from coordinates, listing every cell where live table is beaten by > 1e-4.
  - Partial win p3: Certified putative global minimum for size ratio in 1.4..2.0 at N in 51..100, polished in mpmath (30 digits) to $\|\nabla V\| < 10^{-10}$ with 3Nx3N Hessian having exactly 6 zero modes and 0 negative eigenvalues.
- null_test: not needed because deterministic coordinate re-evaluations and analytical Hessian eigenmode calculations are exact mathematical verifications against published tables.
