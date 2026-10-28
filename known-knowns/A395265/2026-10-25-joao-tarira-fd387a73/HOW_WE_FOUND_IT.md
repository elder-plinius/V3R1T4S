# How we found it

contributor text, unverified

This is a short account by the contributor. It is contributor text, unverified.

A395265(n) is the shortest 5-Golomb ruler with n marks. The published data stopped at a(19) = 50. The search places marks from 0 to a fixed diameter D, breaks mirror symmetry, and prunes with two rules: any block of marks is at least as long as the already computed shorter ruler, and the unplaced segment cannot hold its internal differences inside the remaining multiplicity budget.

a(20) = 56 was found by a left-to-right search that returned NONE for diameters 51 through 55 and a witness at 56. A separately written right-to-left search reproduced the chain from a(3) through a(20), with matching node counts on the overlapping cases. a(21) = 62 used a bidirectional search for the witness at diameter 62, and a sliced left-to-right search that returned NONE for diameters 57 through 61. The right-to-left program, extended only with an optional slice argument, repeated those NONE results. A tree-size estimate for diameter 61 matched the node count that the search actually reported.

The research rule was that the term is kept only when that independent verifier exits 0.
