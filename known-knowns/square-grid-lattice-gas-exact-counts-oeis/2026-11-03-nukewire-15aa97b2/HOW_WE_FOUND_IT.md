# HOW WE FOUND IT (contributor text, unverified)

The bank entry for this target lists, as partial win p2, "a new row of an
associated rectangular table (A210662 monomer-dimer m x n, A089980 hard squares
m x n)". We came to it from the a(28) arc: while computing a(28) of A028420
(the table's diagonal; open PR #849) we noticed the triangular b-file and its
frontier row 27.

The useful observation: a row-by-row broken-profile sweep over the 28 x k board
with a k-wide frontier empties at every row boundary, so ONE sweep at width k
records the entire column T(1..28, k) mod p — the new row's cell AND every
published cell in that column for free. That made Run A both the claim
computation and the full 378-cell reproduction gate in a single pass (13 proven
primes just above 2^61, ~21 min each).

Run B, the independent second computation, was planned as the a(28)-style
column sweep at width 28 — but its 4.3 GB monolithic arrays were blocked by the
RAM guard three nights running on a busy 64 GB machine. The fix was a two-half
in-place layout (3.2 GB peak): every step of the transfer keeps its reshape
blocks inside one half except two precisely-derived cross-half moments (the
within-column domino add at i = w-2 and the final base pass at i = w-1), each
executed as ordered phases reading the still-intact other half — no extra
buffers. Two gate crashes caught my first two wrong claims about which steps
straddle; the exact and modular gates then passed, a width-20 cross-check
against Run A's saved residues matched, and a full-width probe reproduced all
28 of Run A's column residues before the production run started.

Honest bumps, all before any result existed or all disclosed: a prime
generator with an inverted parity test looped on even numbers forever
(masquerading as machine hangs); an exact gate that "failed" at n >= 9 was
really int64 overflow of the true counts; PREREG v1's growth constant was
mis-transcribed from memory (1.33851 is the domino constant; the package's
actual reference is Finch's 1.9402139258 — corrected in PREREG.v3 before the
panel sat, verified by the CRITERION panelist); and the machine slept ~4 h
mid-run twice, surviving on checkpoints.
