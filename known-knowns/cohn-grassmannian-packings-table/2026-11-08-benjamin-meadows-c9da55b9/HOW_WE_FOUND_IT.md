# How we found it (contributor text, unverified)

An unattended search lane (a series of AI coding sessions in a Docker sandbox) worked through the live Grassmannian packing table at https://cohn.mit.edu/grassmannian/, with the table values as targets. The lane downloaded Sloane's posted Grassmannian files from https://neilsloane.com/grass/ and repolished each row with a sequential-LP polish. For (11, 1, 62) the only seed was Sloane's file grassc.11.1.62, at 0.8891150780, which is 1.66e-7 below today's table entry (credited "Henry Cohn, 2026"). One run of `refix5.py 11 1 62 120` (a sequential-LP polish with step tolerance 5e-4, 40 LP iterations, 25 accepted) reached 0.8891705545505, 5.53e-5 above the table (how-we-built-it/src/hit.log, lane log q11w.log line 54).

This is a re-polish of a posted configuration: every one of the 62 result lines stays nearest to the seed line with the same index, and moves by squared chordal distance at most 4.5e-4. Cohn's 2026 configuration was never in the lane, so whether it lies in the same basin is unknown.

What failed: basin hopping on posted configurations found only worse optima. Early sessions called n = 1 rows dead because their LP tolerance (2e-5 or less) was too narrow, and a wider tolerance reopened them. Polishing weaker seeds on rows whose record seed was rigid gave 0 of 9 or more.
