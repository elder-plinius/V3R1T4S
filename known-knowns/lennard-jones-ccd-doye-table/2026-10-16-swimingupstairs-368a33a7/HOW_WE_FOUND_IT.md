# How we found it (contributor text, unverified)
An automated V3R1T4S run (2026-10-15) audited all 439 LJ562-1000 point files, then ran basin hopping, FIRE with flow-like moves,
and grow/shrink sweeps that build N from the table structures for N-1 and N+1. Most lines failed: the grow sweep and the hopping on
663 and 899 found nothing below the table. Removing one atom from the table's 663 structure and relaxing gave a new 662 basin 8.80e-4
below the table; surface basin hopping from the table's 662 reached the same structure independently. A 40-digit Newton step
brought the gradient to 7e-27.
