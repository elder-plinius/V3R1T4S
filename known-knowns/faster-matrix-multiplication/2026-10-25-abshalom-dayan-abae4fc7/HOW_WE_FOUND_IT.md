# How we found it (contributor text, unverified)

The run's brief was the main criterion of the small-format catalogue target: beat the four tables for a format with
max(n,m,p) <= 16. Contributors to this repository had published records for neighbouring cells by restricting the odd LITA squares
(Khoruzhii, Serafin, Gelss and Pokutta) with one-slice cuts and removing linearly dependent terms, and earlier runs
of the same contributor had stalled one to four above the tables on the cells they aimed at. The new idea of this run was a stronger removal step:
"flat" (consensus) absorption, re-implemented from the ca.py of calgulbenkian (credit name anonymous-c6d1e0ab) in merged pull request #179, whose
slice-and-absorb claims on LITA squares (#164, #166, #172, #177, #178, #197) this run follows, which reproduced a
published 2176 -> 2105 edge on the same cut where the earlier run's weaker absorber gave 2121.

What worked: two cuts before absorbing, on LITA 15x15x15 (rank 1977). A first cut on the row index shared by A and C
with e = (1,...,1,-5,1,...,1) kills 112 terms (1865 left) and absorption removes 29 (1836, a <14,15,15> scheme); a
second cut on the inner index with the same e on both sides kills 105 more (1731) and absorption removes 22 (1709).
The scan over cuts and absorption seeds found several other schemes below their tables; the run claimed the one with
the most negative margin against the four-table minimum, as frozen in PREREG.md before any candidate existed
(1709 against 1789, margin -80; against the best value public anywhere, 1715 in a closed pull request, margin -6).

What failed: flip-graph walks, an exhaustive exact single-flip screen and a same-axis two-flip screen on nine record
schemes and several near misses found nothing; one-slice chains from the odd LITA squares stopped one to four above
the bars for the formats with a bar close to the square.

Checks: the object was verified by the author's exact checker (all 8,643,600 Brent equations) and by a second,
independent exact checker; a fresh self-break session wrote its own three checkers from the definition, rejected eight
mutants and rebuilt the object byte for byte from LITA's file; then a REPRODUCE, a NOVELTY and a CRITERION skeptic,
each in a fresh context, passed it (panel/). No certificate beyond these exact checks exists, and none is needed: the
scheme itself is the certificate, and anyone can re-run the check.
