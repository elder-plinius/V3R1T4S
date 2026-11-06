# How we found it (contributor text, unverified)

The brief was a V3R1T4S run on the bank target oeis-keyword-more-new-terms: add one new term to an OEIS sequence
that carries keyword more. The scout looked for an exact count that a laptop can finish. A214570 (Emeric Deutsch,
2012) asks, among all rooted trees with n vertices, for the largest number of ordered (plane) trees that collapse to
the same rooted tree. It stopped at a(16) = 1680 in 2012, with keyword hard,more and no pending draft. At n = 17 there
are only 634847 rooted trees and 35357670 ordered trees, so both a direct and a formula-based count are feasible.

The preregistration was frozen before any program existed. Program A took the definition literally: generate every
ordered tree as a Dyck word, intern each node's sorted list of child classes, and count trees per class. Program B
enumerated rooted trees by canonical level sequences and used c(t) = prod deg! / prod (multiplicity)!. Both reproduced
all 16 DATA terms, gave a(17) = 3360 with a single maximizer, and agreed on the number of maximizers at every n. A
self-break pass tried to make it fail: a third nested-tuple method matched DATA to n = 12, and forgetting the
multiplicity division broke DATA at n = 4. The query 420,840,1680,3360 failed with a connection error at claim time;
the novelty skeptic and the gate re-ran it (4 unrelated hits).

Three fresh skeptics then checked it: the reproduce skeptic wrote its own Python checker before reading the claim
programs; the novelty skeptic re-fetched the entry, b-file, history, the companion triangles and several value
searches; the criterion skeptic checked the bank text clause by clause and judged it a full solution, not a partial
win. The honesty gate re-fetched the entry once more, re-ran both programs from a fresh copy, and passed it as
CONFIRMED_SOLUTION for the whole scoped statement.
