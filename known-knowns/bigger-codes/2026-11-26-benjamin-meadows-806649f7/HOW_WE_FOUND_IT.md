# How we found it (contributor text, unverified)

Method: seeded bit-swap tabu search, the local search Echols used for 124 improved cells of this table (arXiv:2608.13906), run over many open cells of Brouwer's constant-weight table with the cell's best hosted code as the seed. For A(30,12,9) the seed was the 44-word code Brouwer hosts for the cell (https://aeb.win.tue.nl/codes/cwc/d12/a30.12.9.44, itself a polished version of Rosin's 43-word code, arXiv:2603.00174). The search adds one word to reach the target size 45 and then moves single 1s within words to remove every pair at distance below 12. The penalty is the total distance shortfall over such pairs. how-we-built-it/COMMANDS.md describes the program and the exact command.

What worked: a short tabu tenure (1 to 5 iterations) with random tie-breaking and no restarts. Seed 1008 reached penalty 0 after 19,272,004 iterations (about a minute on one core). Every one of the 45 words was moved along the way: the result shares no word with the seed code, and no 44-word subset of it has the seed's pairwise intersection counts (result: 0: 57, 1: 36, 2: 141, 3: 756 pairs; seed: 0: 57, 1: 31, 2: 98, 3: 760).

What did not: a run with seed 1009 and a longer tenure (10 to 30) stalled at penalty 2. A deterministic tie-breaking variant also stalled at penalty 2 when it restarted after every million iterations without improvement. Plain random-score greedy constructions (no seed code) reached only 38 words in short trials.

Checks done beyond the package checker, by the contributor: the bounds that the hosted codes of neighbouring cells give for this cell by shortening, puncturing or appending a coordinate (largest: 42, from A(29,12,9) >= 42), listed in the-record-we-beat/RECORD.md. One route could not be tested: the table's A(32,12,11) >= 215 code file returned 404, so the best two-coordinate shortening of that code to (30,12,9) was not computed. That route keeps the words with a 1 at both of two chosen coordinates and deletes those coordinates; on average a pair keeps 215 x (11/32) x (10/31), about 24 words, well below 45, but the best pair could keep more than the average.

## What was not established

- Not optimal: the table's upper bound is 74.
- No symmetry: the code has no claimed automorphism group, and none was searched for.
- Whether the code is maximal (no 46th word can be added) was not checked here.
