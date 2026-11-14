# REPRODUCE verdict: cohn-harmonic-energy-spheres-dim4-32, cell 64-20

context: subagent (fresh context; one skeptic, one role, one claim; no access to the claimant's search or checker code)
verdict_utc: 2026-11-08T02:32:39Z

## Value computed here
- Method A (mpmath, 50 digits; each vector normalised, then all 2016 pairs summed with fsum): E* = 6.68546368135722749098338583853941365571
- Method B (exact rational dot products and norms from the decimal strings, one square root per pair in Decimal at 70 digits, |x-y|^-18 as (2 - 2cos)^-9): E* = 6.6854636813572274909833858385394136557102322
- Difference between the methods: 6.4e-50.
- The header line of object/64-20.txt states 6.68546368135722749098338583854041359598692198857256; it differs from the computed value by 1.0e-30, which is the size of the norm deviation and does not affect the verdict. The claimed "about 6.68546368135722" in CLAIM.md matches to all quoted digits.
- Table energy: 6.7232495038, taken from CLAIM.md (fetching the live table is another skeptic's job).
- Margin needed: max(1e-9, 1e-12 * 6.685) = 1e-9. Margin achieved: 6.7232495038 - 6.6854636814 = 0.0377858224, about 3.8e7 times the required margin.

## Clauses checked
- File identity: sha256 of object/64-20.txt is 968ebd541209b17fcf58284178aa4a81b6e3562ef520328e8520e250625e9c71, matching CLAIM.md. PASS
- Format: one '#' header line, then 64 data lines of exactly 20 comma-separated values each. PASS
- Count: N = 64 vectors, n = 20 coordinates. PASS
- Numeric validity: every token matches a plain decimal-number pattern; no NaN, Inf or non-numeric tokens; no coordinate is exactly zero. PASS
- Precision: the shortest coordinate has 27 significant digits (requirement: at least 20). PASS
- Unit norms: exact rational max |norm^2 - 1| = 1.4e-30 before normalisation. PASS
- Duplicates: no repeated rows; minimum pairwise distance after normalisation is 1.3236638778, so no near-coincident points. PASS
- Two independent energy computations over all 2016 pairs agree to 6.4e-50. PASS
- Strictly below the table value from CLAIM.md by at least max(1e-9, 1e-12 E): 0.0378 > 1e-9. PASS

## Decision
The object parses cleanly as 64 unit vectors in R^20 at 27+ significant digits, and two independent high-precision methods give the same harmonic energy E* = 6.685463681357227490983385838539 to about 49 digits. That value is below the table energy 6.7232495038 quoted in CLAIM.md by 0.0378, far more than the 1e-9 margin. This verdict covers only the reproduction of the value; the live table, the proven-optimum clauses, the 2021 data-set basin comparison and the literature search belong to the other skeptics.

pass: true
