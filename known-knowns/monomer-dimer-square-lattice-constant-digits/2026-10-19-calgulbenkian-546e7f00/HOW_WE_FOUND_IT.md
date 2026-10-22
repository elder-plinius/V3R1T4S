contributor text, unverified

# How we found it

This was our own computation. It was done on 2026-10-18/19 by the contributor's team (a Claude Code subagent working for calgulbenkian) from the definition of the monomer-dimer model on the square lattice. The proofs for the separate 13-decimal enclosure were derived before comparing with the literature; the 36-decimal value here is numerical only.

Two methods were used. Method A is a high-precision corner transfer matrix on a vertex form of the model, with bond dimension raised in steps up to 48. Method B3 takes exact open-boundary strip transfer matrices of widths 3 to 29, finds the logarithm of the largest eigenvalue to about 70 digits, and extrapolates with the Wynn epsilon algorithm under a recipe written down before the data were computed. The two agree to 36 decimals (43 for the corner transfer matrix ladder alone).

What failed or was weaker is listed in the README under Not claimed: a first periodic method reached only 15 decimals, and a second periodic variant was chosen after the corner transfer matrix value was known. The panel skeptics are of the same model family as the builder; the 13-decimal enclosure, but not this value, was reviewed by a model of a different family.
