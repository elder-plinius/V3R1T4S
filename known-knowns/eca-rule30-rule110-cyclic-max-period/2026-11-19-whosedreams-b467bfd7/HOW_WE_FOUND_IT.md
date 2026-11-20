# How we found it (contributor text, unverified)

Brief: compute the exact maximum eventual period of elementary CA Rule 30 (A334497) or Rule 110 (A204371) on a ring of 37 cells, by an exhaustive search with two independent programs that agree.

What was prepared first: two C programs were written and self-tested on 2026-11-03. impl1 walks the functional graph and marks each rotation orbit once, converting an orbit return into a state period with the rotation-offset formula and then checking the witness by direct iteration. impl2 is a 3-colour (white/grey/black) walk that does not fold rotations at all; a hit on a grey state gives the period as the distance along the stack. Both use the Wolfram bit-order convention and do not reduce by reflection (Rules 30 and 110 are chiral). On that self-test, both programs reproduced A334497(1..30) and A204371(1..30) exactly and reported A334497(25..30) equal to the listed terms. Width 37 was not run on the small packaging machine: impl1 needs a 16 GiB bitset and impl2 a 32 GiB colour array.

What worked: the same programs were run for Rule 110 at n=37 on a Ryzen 9900X machine with about 53 GB of memory under WSL2. impl1 finished in 1699.3565 seconds with max_period=4403 and witness=0x1c7dbbb23e; impl2 finished in 11946.5399 seconds with the same period and the same witness. A self-test log shipped back with that run again shows both programs matching A334497(1..24) and A204371(1..30) exactly (120 OK lines, no BUG or MISMATCH lines) and reporting A334497(25..30) as 588425, 312156, 240300, 249165, 1466066, 374265.

The plan file how-we-built-it/PREREG.md was written after that run, when this claim was packaged; it says so.

A later local check, not part of the original search, re-iterated the witness and also started from a single live cell: the witness is the first state of the single-cell cycle (transient 192, period 4403). So the maximum is the single-cell floor, and the exhaustive census is the evidence that no longer cycle exists.
