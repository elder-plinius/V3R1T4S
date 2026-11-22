# Preregistration: 11x14x16, class ZT, rank 1547

Trimmed on 2026-10-25, at the maintainer's request, to the part of the 2026-10-17/18 plan that concerns this cell. The full
plan also covered other cells and a second target; those parts are left out. The wording below is the plan's own, minus local
file names.

## Scope
- Target `fmm-ternary-integer-ring-upgrade`: construct and verify `ZT` or `Z` schemes that strictly improve the live Perminov
  `ZT` or `Z` upper bound while remaining $\ge$ the global SOTA rank over $\mathbb{Q}$. This package is the 11x14x16 `ZT` result.
- Verify the scheme exactly over $\mathbb{Z}$: every Brent equation
  $\sum_{q=1}^r U_{q,a} V_{q,b} W_{c,q} = \delta_{a_2,b_1}\delta_{a_1,c_1}\delta_{b_2,c_2}$ (or its transpose) must hold over the integers.

## Method used for this cell
**Subspace Homomorphism Base Substitution (`Q -> Z / ZT`)**:
   Detect rational base tensor blocks `<2,4,5>` ($32 \to 33$ `ZT`), `<3,3,6>` ($40 \to 42$ `ZT`), `<4,4,4>` ($48 \to 49$ `ZT`), and `<3,4,7>` ($63 \to 64$ `ZT`, accounting for 1 leading integer triad) inside Perminov's `_Q.json` schemes, solve the exact $\mathbb{Q}$-linear transition maps $(P_U, P_V, P_W)$ via Gaussian elimination over `fractions.Fraction`, optimize over the signed permutation symmetry group of each base `ZT` scheme, and reduce via `zt_flip_reduce`.

Added on 2026-10-25, not part of the plan: for this cell the result was then split into ternary terms and reduced again with the ternary flip graph (see `../HOW_WE_FOUND_IT.md`).
