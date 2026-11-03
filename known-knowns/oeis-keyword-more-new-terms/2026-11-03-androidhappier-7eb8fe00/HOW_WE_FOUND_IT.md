# How we found it (contributor text, unverified)

The brief was a V3R1T4S run on the bank target oeis-keyword-more-new-terms: add one new term to an OEIS sequence that
carries keyword more. The scout looked for an exact count that needs little memory and had not been extended.
A316471 (Gus Wiseman, 2018), locally disjoint rooted identity trees, stopped at a(20) = 214490 with keyword more, a
b-file synthesized from DATA and no history after 2018, while its non-identity sibling A316473 had been extended to
n = 25 by others in 2026.

The preregistration was frozen before any program was written. Program A (C) enumerated trees as strictly increasing
sets of canonical branch ids with a mark array for the disjointness test; Program B (Go) transcribed the entry's
Mathematica algorithm literally (partitions, sorted tuples, filter). Both reproduced all 20 DATA terms and agreed on
482706; with the disjointness test removed both gave A004111, so the test is the active difference. A self-break pass
wrote Program C, a Matula-Goebel oracle based on the A316494 rule, which matched for n <= 11.

Three fresh skeptics then checked it: the reproduce skeptic wrote its own checker from the definition first and got
the same 21 values; the novelty skeptic re-fetched the entry, b-file, history, value searches and sibling entries and
found the value nowhere; the criterion skeptic checked the bank text clause by clause, the definition match and the
PREREG timing. The honesty gate re-fetched the entry once more and passed it for the one cell.
