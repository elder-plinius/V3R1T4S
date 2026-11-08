# PREREG: cohn-harmonic-energy-spheres-dim4-32, cell 64-20

written_utc: 2026-11-08T02:31Z

## Timing, stated plainly

The object was found by an unattended search lane on 2026-11-06 or 2026-11-07, checked against the table as it read on 2026-11-07 and released in packing-records version 1.3 (https://doi.org/10.5281/zenodo.24046261) on 2026-11-08. This file was written after that and before any panel ran. It freezes the judging, not the search; it is not a pre-registration of the search. The criterion is quoted from the public bank, `bank/targets.json` on the main branch of https://github.com/elder-plinius/V3R1T4S (read 2026-11-08). No threshold or margin below was chosen by us.

## Criterion: cohn-harmonic-energy-spheres-dim4-32

> Success means N unit vectors in R^n (n in 4..32; >= 20 significant digits) for an (N, n) pair listed at https://cohn.mit.edu/harmonic-energy (re-fetched immediately before claiming), whose energy E* = sum_{i < j} |x_i - x_j|^{-(n-2)}, computed in mpmath at 40 digits after normalisation, is STRICTLY LOWER (direction: min) than the SMALLEST table energy for that (N, n) by at least max(1e-9, 1e-12 * E). The (N, n) must not be a proven optimum: not a simplex (N = n+1), not a cross polytope (N = 2n), not a universal optimum listed on https://cohn.mit.edu/harmonic-optima, and not proven optimal for harmonic energy in any paper found in an arXiv check. It must be a different basin: polishing the 2021 data set's coordinates for (N, n) with the same routine stays above E* + max(1e-9, 1e-12 * E). And no lower published value is found in an arXiv search.

Cell: 64-20.

## Statistic and thresholds

Exactly as in the criterion above. The table is re-fetched by the panel. Null test: not applicable; a deterministic construction checked against a definition.

## Panel

Three fresh skeptics (REPRODUCE, NOVELTY, CRITERION), new subagents, each seeing only the claim folder and writing its own code; none sees the search code or our checker. The cell is dropped unless all three write `pass: true`.
