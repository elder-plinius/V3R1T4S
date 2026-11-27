# How the numbers were produced (exact commands)

Run A (left-to-right row sweeps, 22 set-A29 primes > 2^61 + 3e6, sliced DP
for k=27/28, checkpointed per (prime,width)):
    python runA29.py gate            # exact n=1..12 vs the A028420 diagonal
    python runA29.py gate-sliced     # sliced layout == plain, exact
    python runA29.py work <resfile> <deadlineUTC> 27|28

Run B (independently written; right-to-left row sweeps, 22 disjoint set-B29
primes > 2^61 + 103e6; five cross-gated implementations incl. a two-half
sliced fast form):
    python runb29_r2l.py gate | gate-mod | gate-sliced | gate-fast
    python runb29_r2l.py work <resfile> <deadlineUTC> 27|28

Gates on the collected residues (this package's evidence):
    python final_gate.py --full      # two-run CRT equality, 28/28 required
    python spot_fresh.py 21 24 27 28 # fresh prime in neither set
    python growth_row29.py <object.json>  # frozen growth test

Anchors: T(29,k) <= 3^(29k) (scan move set; largest bound 3^812 = 1287 bits
< 22 x 61 = 1342); the j=28 column vs the row-28 object (PR #960); the
published 378 cells. PREREG chain: v1 (frozen 2026-11-04, measuring design),
v2/v3 (claim narrowings after panel novelty findings; no threshold moved).
Requirements: Python 3.8+; numpy for the growth script only.
