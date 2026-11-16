# How We Found It

_Note: contributor text, unverified._

1. **Colon-ideal & covering-sheet analysis (`algebraic-colon-and-covering`)**: Analyzing the `h = 7` covering map `Z_42 x Z_6 -> Z_6 x Z_6` onto `[[72, 12, 6]]` showed that pure covering pullbacks multiply Hamming weight by `7` (`>= 42`), whereas nontrivial minimum-weight operators arise from non-translation-invariant `Z_42` sheet cancellations projecting to higher-weight homology representatives in `[[72, 12, 6]]`.
2. **Bit-packed Stern/Dumer ISD + coset reducer (`isd-stern-logical-hunter`)**: Running Stern/Dumer collision search directly on `ker(H_X)` with online `rowspace(H_Z)` rank filtering and weight-reducing stabilizer coset sweeps (`bb_isd_hunter.cpp`) rapidly isolated a `12 + 16 = 28` qubit logical operator (`rank([H_Z; u]) = 247 > 246`), strictly below the published `d <= 30` bound.
