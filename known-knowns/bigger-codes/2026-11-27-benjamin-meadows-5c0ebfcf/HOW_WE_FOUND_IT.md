# How we found it (contributor text, unverified)

Method: seeded bit-swap tabu search (Rosin's bit-swap tabu search, arXiv:2603.00174, started from a known code as in Echols, arXiv:2608.13906), run as a worker pool over many open cells of Brouwer's constant-weight table, each cell started from the best code Brouwer hosts for it. For A(29,10,8) the start was the 96-word code at https://aeb.win.tue.nl/codes/cwc/d10/a29.10.8.96, credited in the table to William Echols. Whenever a run found a code of the target size, the next target was one word more, started from that code. A first pass ran random seeds from 1001 upward (at most 20) with a 120 CPU-second limit per run, several at a time; as soon as one run found a code, the target moved up one word, so not every seed ran at every size; even seeds used a short tabu tenure (1 to 5) and no restarts, odd seeds tenure 5 to 15 with a restart after 10^6 iterations without improvement.

What worked: 2 run(s) of the first pass reached 98 words (149.6 CPU seconds in total); how-we-built-it/COMMANDS.md lists each run's seed and step count.

What did not: the other 4 runs at 98 words ended at penalty 2 or more. At 99 words, 40 runs (CPU limits up to 900 s) had found nothing by 2026-11-27T18:43Z; best penalty 4. (Penalty 2 means one pair at distance 8.) The pool was still running when this package was built, so the counts at one word more are a snapshot.

## What was not established

- Not optimal: see the table's upper bound in README.md.
- No symmetry: the code has no claimed automorphism group, and none was searched for.
- Whether the code is maximal (no further word can be added) was not checked here.
- Bounds implied for this cell by shortening or puncturing the hosted codes of neighbouring cells were computed by the contributor's own tooling only (none reached the table's lower bound plus one); the novelty review in panel/ reports its own check.
