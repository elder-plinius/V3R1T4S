# How we found it (contributor text, unverified)

For plain domination, a class of a partition can be shrunk to a minimal dominating set, so a 21-partition of Q_12 is
governed by a count: with a classes of 6 squares and b classes of 7 squares, 6a + 7b + 8(21 - a - b) <= 144 forces
2a + b >= 24. Q_12 has only eight dominating 6-sets and at most 4 of them are pairwise disjoint, so a 21-partition must
be one of two shapes: 4 six-sets, 16 seven-sets and 8 remaining squares that dominate, or 3 six-sets and 18 seven-sets
covering the board exactly. We enumerated the minimal dominating 7-sets (6,712, with an enumerator that branches on an
undominated square, about 100 times faster than our earlier index-ordered one). A linear-programming bound did not
exclude either shape, and an integer-programming solver found nothing in five minutes per shape. An exact-cover style
depth-first search, branching on the scarcest square, found a partition of the second shape in about a minute, and one
of the first shape as well (not part of this package).
