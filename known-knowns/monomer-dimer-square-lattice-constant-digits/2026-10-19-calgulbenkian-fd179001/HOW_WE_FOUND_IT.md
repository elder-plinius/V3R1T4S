contributor text, unverified

# How we found it

This was our own computation, not copied from anyone's search. It was done on 2026-10-18/19 by the contributor's team (a Claude Code subagent working for calgulbenkian) from the definitions of the monomer-dimer model. The proofs of the two inequalities (an upper bound from a cylinder of circumference M, a lower bound from circumferences 2q and 2q + p) were derived before comparing with the literature, and they turned out to agree with the two inequalities of Friedland and Peled. The proofs and the checker were reviewed before the panel by a model of a different family (read-only, verdict clean with three display and wording fixes, which were applied).

What worked: the largest eigenvalue of the cylinder transfer matrix was approximated in floating point by power iteration, refined in exact 128-bit integers, and turned into a positive integer vector. The Collatz-Wielandt ratios of that vector, computed in exact integers, bound the eigenvalue from both sides. Widths 22 and 24 gave the enclosure of 13 decimals. A wider 15-decimal enclosure (widths up to 28) was also computed, but its vectors are not shipped and it is not claimed.

The panel (three fresh skeptics of the same model family, disclosed in `panel/gate.md`) rebuilt the width 22 and width 24 checks with its own code and got the same enclosure digit for digit.
