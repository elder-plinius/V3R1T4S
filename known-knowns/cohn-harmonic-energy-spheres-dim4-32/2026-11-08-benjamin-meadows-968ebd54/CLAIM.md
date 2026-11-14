# Claim: cohn-harmonic-energy-spheres-dim4-32, cell 64-20

Object: `object/64-20.txt` (sha256 968ebd541209b17fcf58284178aa4a81b6e3562ef520328e8520e250625e9c71).

Claimed: N = 64 unit vectors in R^20 whose harmonic energy sum_{i<j} |x_i - x_j|^-(n-2) (n = 20) is lower than the smallest table energy for (N, n) = (64, 20). Claimed value about 6.68546368135722; the table value read 2026-11-07 is 6.7232495038.

Success criterion (V3R1T4S bank target cohn-harmonic-energy-spheres-dim4-32, quoted verbatim):

> Success means N unit vectors in R^n (n in 4..32; >= 20 significant digits) for an (N, n) pair listed at https://cohn.mit.edu/harmonic-energy (re-fetched immediately before claiming), whose energy E* = sum_{i < j} |x_i - x_j|^{-(n-2)}, computed in mpmath at 40 digits after normalisation, is STRICTLY LOWER (direction: min) than the SMALLEST table energy for that (N, n) by at least max(1e-9, 1e-12 * E). The (N, n) must not be a proven optimum: not a simplex (N = n+1), not a cross polytope (N = 2n), not a universal optimum listed on https://cohn.mit.edu/harmonic-optima, and not proven optimal for harmonic energy in any paper found in an arXiv check. It must be a different basin: polishing the 2021 data set's coordinates for (N, n) with the same routine stays above E* + max(1e-9, 1e-12 * E). And no lower published value is found in an arXiv search.

The bank's verification method:

> Checker (seconds to minutes): normalise in mpmath, compute E* exactly, and compare with the live table minimum for (N, n). Polish the data-set configuration and the claim with the same L-BFGS plus mpmath Newton routine, and compare the basins. Check the harmonic-optima page for proven rows.

Live sources (fetch them yourself):

- https://cohn.mit.edu/harmonic-energy (the table)
- https://cohn.mit.edu/harmonic-optima (the universal-optima page named in the criterion)
- the 2021 data set with the posted configurations, https://hdl.handle.net/1721.1/130937 (data.txt, about 78 MB)
- arXiv search for "harmonic energy" / "universal optimality" / "Riesz energy"
- Prior claims: open, merged and closed pull requests at https://github.com/elder-plinius/V3R1T4S for target cohn-harmonic-energy-spheres-dim4-32, and TROPHY_CASE.md on its main branch.
- If DSpace refuses the download (it answered HTTP 429 to curl on 2026-11-07), a copy of data.txt fetched by the claimant on 2026-11-06 was given to the panel as a local file, not included here (sha256 792eebd56d1178f6a7fef559b8d30159cac11299bcdd60ef4679d626ae7f5c8e); say which copy you used.
- Note: https://cohn.mit.edu/harmonic-optima returned HTTP 404 on 2026-11-08 and is no longer linked from https://cohn.mit.edu/data/; it was readable on 2026-11-03. Check what you can and say what you could not.
