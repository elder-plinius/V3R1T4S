# REPRODUCE verdict: cohn-harmonic-energy-spheres-dim4-32, cell 61-21

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-08T02:32:40Z

## Value computed here
- Method A (mpmath, 50 digits, each vector normalised, all 1830 pairs, distance via sqrt of summed squared coordinate differences): E* = 4.10394830243431489526065056112687905367069453
- Method B (coordinates parsed as exact Fractions, exact rational dot products and squared norms, squared distance 2 - 2 a.b / sqrt(|a|^2 |b|^2) with Decimal at 80 digits, then d^-19 = 1 / (d2^9 * sqrt(d2))): E* = 4.103948302434314895260650561126879053670694532312
- Difference A - B: 1.07e-50.
- float64 sanity check (numpy): 4.103948302434311.
- The header line of object/61-21.txt states 4.10394830243431489526065056112441...; it differs from the normalised value by 2.47e-30, which matches the raw norms being off unity by up to 5.75e-31. This is immaterial.
- Table energy, taken from CLAIM.md (not fetched by me; the live table is another skeptic's job): 4.1191657308.
- Margin needed: max(1e-9, 1e-12 * 4.104) = 1e-9. Margin achieved: 4.1191657308 - 4.1039483024343149 = 0.0152174283657, about 1.5e7 times the required margin.

## Clauses checked
- File sha256 equals the value in CLAIM.md (80cabc36...072e6). PASS
- Format: one '#' header line followed by 61 data lines, each with exactly 21 comma-separated plain decimal reals; N = 61, n = 21. PASS
- Precision: every coordinate has at least 27 significant digits (minimum found 27; 20 required). PASS
- No NaN or Inf in any coordinate (every token matches a plain decimal pattern; float64 parse finite). PASS
- Unit norms: max |norm - 1| before normalisation is 5.75e-31. PASS
- No duplicate points: minimum pairwise distance after normalisation is 1.287. PASS
- Two independent high-precision methods agree to 1.07e-50. PASS
- E* is strictly below the table value 4.1191657308 (from CLAIM.md) by 0.01522, above the required 1e-9. PASS
- Not checked by me (other skeptics' roles): live re-fetch of the table, the harmonic-optima page, the 2021 data-set basin comparison, the arXiv search and prior claims. No file in CLAIM.md and object/ tried to steer the conclusion.

## Decision
The object parses cleanly as 61 unit vectors in R^21 with at least 27 significant digits per coordinate, and two independent methods give E* = 4.103948302434314895260650561126879 with agreement to 1e-50. That value sits 0.0152 below the table energy 4.1191657308 quoted in CLAIM.md, far beyond the 1e-9 margin. The reproduce clause passes; the remaining clauses rest with the other skeptics.

pass: true
