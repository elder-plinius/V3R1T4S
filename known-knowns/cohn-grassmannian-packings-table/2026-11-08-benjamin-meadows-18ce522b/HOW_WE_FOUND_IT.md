# How we found it (contributor text, unverified)

An unattended search lane (a series of AI coding sessions in Docker containers) worked through the live Grassmannian packing table at https://cohn.mit.edu/grassmannian/, with the table values as targets. The lane downloaded Sloane's posted Grassmannian files from https://neilsloane.com/grass/ and repolished each row with a sequential-LP polish. For (11, 4, 66) the seed was Sloane's file grassc.11.4.66, which attains the table value 2.5777278197 (reference [31]) to all ten printed digits, so it is the configuration behind the table entry. One run of `refix6.py 11 4 66 320` (the same polish with step tolerance 5e-4 and an early exit once the table is cleared by 1e-8) took 3 LP iterations with 1 accepted step and reached 2.5777695524773, 4.17e-5 above the table (how-we-built-it/src/hit.log, lane log q14_3.log line 37).

This is a re-polish of the posted configuration in its own basin: every one of the 66 subspaces stays nearest to the seed subspace with the same index and moves by squared chordal distance at most 8.2e-7.

What failed: an earlier screen with a narrow LP tolerance called this row a fixed point (gain 1e-10. Lane log q7s2.log line 16). Basin hopping on posted configurations found only worse optima, and the (11, 4) rows from N = 72 to 82 stayed rigid (0 of 11).
