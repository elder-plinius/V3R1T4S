# How we found it (contributor text, unverified)

The brief was a V3R1T4S run on the bank target oeis-keyword-more-new-terms: add one new term to an OEIS sequence
that carries keyword more. The scout looked for a cell with an exact count that needs little memory. A326336 (Gus
Wiseman, 2019), set partitions whose capturing graph is connected, stopped at a(10) = 12270 with keyword more, no
pending draft and no later history.

The preregistration was frozen before any program was written. Program A (C) enumerated restricted-growth strings
and tested element quadruples per block pair; Program B (Go) used a bitmask generator and a min/max interval
popcount test; both also printed four sibling Wiseman sequences as a cross-check, and every DATA term of all five
matched. A self-break pass transcribed the Mathematica patterns literally in Python (Program C) and ran
wrong-definition fixtures (crossing edges in place of capturing), which failed DATA as they should. All three
programs agreed on 70472.

A first gate closed without a panel because that session could not start fresh contexts. Later three fresh skeptics
checked it: the reproduce skeptic wrote its own checker first and got the same 12 values; the novelty skeptic
re-fetched the entry, b-file, history and value searches and found no trace of the value outside this
contributor's own unpublished sibling package; the criterion skeptic checked the bank text clause by clause, the
definition match and the PREREG timing. The honesty gate then passed it as CONFIRMED_SOLUTION for the one cell.
