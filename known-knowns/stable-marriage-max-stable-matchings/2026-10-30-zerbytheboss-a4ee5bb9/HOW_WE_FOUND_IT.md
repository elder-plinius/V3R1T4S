# How we found it (contributor text, unverified)

We investigated the stable marriage problem to strictly exceed the composition-closure record at order n = 17. Because 17 is a prime integer, no non-trivial lexicographic composition A[B] of smaller instances exists, leaving Thurber's 2002 G17 construction (the 17x17 submatrix of bitwise XOR i ^ j, yielding 200,832 stable matchings) as the exact composition closure bar.

We initialized an adaptive kick-step local hill-climbing search seeded directly from Thurber's G17 profile. Candidate preference modifications were evaluated by computing the Irving-Leather rotation poset and enumerating down-sets via memoized bitset representations. The search explored adjacent swaps in preference rankings, accepting strictly improving and neutral moves, supplemented by 2-transposition kicks upon reaching search plateaus.

At evaluation 2,302, the search broke through to an explicit preference profile of order 17 with 121 exposed rotations and 32,886 memoized states, achieving exactly 206,728 stable matchings (+5,896 over the 200,832 record). The count was verified independently by Gusfield's stable matching lattice walk with per-matching stability re-checking.
