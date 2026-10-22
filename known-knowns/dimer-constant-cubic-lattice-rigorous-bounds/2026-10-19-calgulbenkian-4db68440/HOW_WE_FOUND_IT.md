contributor text, unverified

# How it was found

He's argument bounds the dimer count by the spectral radius of a diagonal-layer matrix. The contributor's team asked whether the same inequality works for all matchings (monomers allowed) at unit activity, since the 2-lift inequality used by He has a version for matching polynomials. They wrote the extension down, built the monomer-dimer layer matrix, and first found a positive integer vector at the (3,3) cross-section whose Collatz-Wielandt ratio gives h3 <= 0.7860441 (filed earlier in this PR, #537). The same program run at the larger cross-section (5,4), where the matrix has 1048576 states, gave the smaller figure h3 <= 0.7859681 that this package claims. The package builder re-applied the full matrix with an independent program, checked it against brute-force matching counts on small cases and against the (3,3) result, and recomputed the ratio exactly; the panel's skeptics then did the same with their own programs.
