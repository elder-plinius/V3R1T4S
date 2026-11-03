# How we found it (contributor text, unverified)

The brief was a V3R1T4S run on the bank target oeis-keyword-more-new-terms: add one new term to an OEIS sequence
that carries keyword more. The scout looked for a cell with an exact count that runs in seconds. A155520 (Emeric
Deutsch, 2009), ordered trees by number of drawings, had stopped at row 5 for seventeen years with keyword more, no
pending draft, and a tiny row 6 (Catalan(6) = 132 trees), with two built-in checks: row sums are Catalan numbers and
the weighted row sums are Klazar's total drawing counts A014307.

The preregistration was frozen before any program was written. Program A (Python) counted drawings backward on Dyck
words, deleting one "UD" leaf at a time and summing over distinct results. Program B (C) built the same counts
forward, inserting a leaf at every position of bit-encoded words and deduplicating per word. Both reproduced all 21
DATA terms and printed identical rows up to n = 8. A self-break pass checked the entry's worked example and showed that
counting deletion sequences with leaves distinguished does not give DATA, so the distinct-tree reading is the right one.
Row 6 has interior zeros, which rows 1..5 never show; that convention was disclosed rather than guessed.

Three fresh skeptics then checked it: the reproduce skeptic wrote its own nested-tuple checker before reading the
claim and got the same row; the novelty skeptic re-fetched the entry, b-file, history and value searches and read
Klazar's paper and addendum (totals only, no by-k table); the criterion skeptic checked the bank text clause by clause,
ran a third checker and judged the zero convention. The honesty gate re-fetched the entry once more and passed it as
CONFIRMED_SOLUTION for the whole row.
