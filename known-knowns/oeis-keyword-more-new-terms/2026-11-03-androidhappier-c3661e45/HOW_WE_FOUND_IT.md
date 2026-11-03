# How we found it (contributor text, unverified)

The brief was a V3R1T4S run on the bank target oeis-keyword-more-new-terms: add one new term to an OEIS sequence
that carries keyword more. The scout looked for a cell with an exact count that runs in seconds. A131449 (Wolfdieter
Lang, 2007), organic (increasing) labelings of rooted ordered trees, had stopped after the first entry of row 6 for
nineteen years with keyword more and no pending draft. Row 6 has only Catalan(6) = 132 trees, and the row sums are a
built-in check ((2n-1)!!, A001147).

The one real risk was the order of the trees within a row, which the entry's name does not fix. It was written down
in target.md and the preregistration before any program existed: every existing row is non-increasing, and Lang's
own file groups rows 3..5 by isomorphism class in decreasing value.

Program A (Python) applied the hook formula n!/prod h(v) to every Dyck word. Program B (C) avoided the formula and
counted, per tree, the orders in which vertices can be removed leaf by leaf with a bitmask DP. Both reproduced all 66
DATA terms and printed identical rows through n = 7. A self-break pass reproduced Lang's row-5 class grouping exactly
under the sorted order and showed two wrong readings (one entry per unordered class; dropping "increasing") fail DATA.

Three fresh skeptics then checked it: the reproduce skeptic brute-forced all label permutations with its own tree
generator and got the same row; the novelty skeptic re-fetched the entry, b-file, history, Lang's files and five value
searches (nothing published for row 6); the criterion skeptic checked the bank text clause by clause and judged that
T(6,2) = 360 holds under any order consistent with rows 0..5. The honesty gate re-fetched the entry once more and
passed it as CONFIRMED_SOLUTION for the whole scoped statement.
