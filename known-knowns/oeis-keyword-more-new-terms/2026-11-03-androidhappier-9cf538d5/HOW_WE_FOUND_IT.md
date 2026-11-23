# How we found it (contributor text, unverified)

The brief was a V3R1T4S run on the bank target oeis-keyword-more-new-terms: add one new term to an OEIS sequence
that carries keyword more. The shared machine was busy, so the scout looked for a cell needing little memory and an
exact count. A325786 (Gus Wiseman, 2019), complete necklace compositions, stopped at a(20) = 47049 with keyword more,
no pending draft and no later history; the entry's own Mathematica code only runs to n = 15.

The preregistration was frozen before any program was written. Three lenses then worked separately. Program A (C)
enumerated compositions recursively with a rotation-minimality test and circular block sums. Program B (Go) used cut
points in Z_n, a difference-set cover test and 1/period weighting. Program C transcribed the Mathematica literally;
its first version (all permutations) was too slow and was aborted, the second (distinct permutations) reached n = 21.
A self-break variant without the necklace test gave a(3) = 3 and failed DATA, as it should. A and B agreed on 93725
and both reproduced all 20 terms.

A first gate closed without a panel because that session could not start fresh contexts. Later three fresh skeptics
checked it: the reproduce skeptic wrote its own bitmask checker first and got the same 21 values; the novelty
skeptic re-fetched the entry, b-file, history and value searches and found no trace of the value; the criterion
skeptic checked the bank text clause by clause and the PREREG timing. The honesty gate then passed it as
CONFIRMED_SOLUTION for the one cell.
