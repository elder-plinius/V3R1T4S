# How we found it (contributor text, unverified)

The brief was a V3R1T4S run on the bank target oeis-keyword-more-new-terms: add one new term to an OEIS sequence
that carries keyword more. The scout looked for a cell with an exact count that runs in seconds. A331783 (Gus
Wiseman, 2020), locally disjoint rooted semi-identity trees, stopped at a(20) = 4242226 with keyword more, no
pending draft and no later history; a sibling run was working on the identity-tree version (A316471).

The preregistration was frozen before any program was written. Program A (C) built trees size by size as sets of
distinct non-leaf subtrees with pairwise disjoint branch-type sets, checked with a mark array. Program B (Go) was a
literal transcription of the entry's Mathematica code: every multiset of smaller trees over every integer partition,
tested with disjunsQ. Both reproduced all 20 DATA terms and gave 10950456 at n = 21. A self-break pass counted the
trees a third way via Matula-Goebel numbers and the A331682 rule (agreeing up to n = 11), and removed the
disjointness test, which gave the semi-identity counts (18 at n = 6 instead of 17), as it should.

Three fresh skeptics then checked it: the reproduce skeptic wrote its own checker before reading the claim and got
the same 21 values; the novelty skeptic re-fetched the entry, b-file, history, value searches and the related
entries A316471 and A316473 and found no trace of the value; the criterion skeptic checked the bank text clause by
clause, wrote its own literal transcription of the Mathematica code, and checked the PREREG timing. The honesty gate
re-fetched the entry once more and passed it as CONFIRMED_SOLUTION for the one cell.
