context: subagent

p1, judged literally from CLAIM.md: a certified exhaustion, at length 70, of one precisely stated family, re-run to the same empty result, not Lebedev's reversible queue, and not already killed by a short necessary condition.

Family. (Z/70Z)* has order 24 and exactly three subgroups of order 12. Exactly two omit -1 = 69, and they are the named tuples
H1 = (1, 3, 9, 11, 13, 17, 27, 29, 33, 39, 47, 51) and
H2 = (1, 9, 11, 23, 29, 37, 39, 43, 51, 53, 57, 67).
Both are closed. The claim's "either" is the union of these two same-group families, not mixed invariance and not every multiplier subgroup. That is the scope below.

Enumeration. Invariance is constancy on multiplication orbits. H1 has 10 orbits (space 4^10 = 1048576) and H2 has 12 (space 4^12 = 16777216). search_two_groups.py, re-run from claim/, printed TOTAL_HITS 0, with H1 norm0 2304, norm1 0, norm2 6528, hits 0, and H2 norm0 36864, norm1 0, norm2 99840, hits 0. An independent Gaussian-integer autocorrelation, calibrated on the length-42 pair and a one-digit mutation, reproduced those counts and INDEPENDENT_HITS 0. norm 1 is impossible because each group has an even number of odd-sized orbits, so the two sum coordinates always have the same parity; the (1, 1) case is empty, not skipped. Sequences outside norms 0 and 2 cannot meet |sum A|^2 + |sum B|^2 = 2. Thousands of assignments survive that filter, so the zero-frequency identity does not empty the family.

Not a short kill. Half-integer centre symmetry is not forced: the orbit of 0 is {0}, and the orbit of 1 is not the orbit of 69. The midpoint identity does not reduce to "71 is not a sum of two squares" here. Attainable midpoint norms in the two sum classes are compatible with summing to 142 through modulus 64; the miss is an enumerated gap (nearest H2 sums 134 and 150), not a one-line obstruction.

Not Lebedev's queue. arXiv:2609.04589 exhausts the reversible four-block queue at length 70 and says a non-reversible pair is not ruled out. Neither named group contains -1, and x[1] is not tied to x[69], so the family is not that queue.

confirmed_scope: There is no quaternary Legendre pair of length 70 in which both sequences are constant on the orbits of (1, 3, 9, 11, 13, 17, 27, 29, 33, 39, 47, 51) or both are constant on the orbits of (1, 9, 11, 23, 29, 37, 39, 43, 51, 53, 57, 67), the two order-12 subgroups of (Z/70Z)* that do not contain -1.
pass: true
