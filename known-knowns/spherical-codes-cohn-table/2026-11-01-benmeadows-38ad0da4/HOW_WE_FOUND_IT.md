# How we found it (contributor text, unverified)

The brief: one search lane over Cohn's table for d = 25..32 and d+2 <= N <= 3d (193 cells not already claimed), four
cores, about 3.3 hours, with the 2026-10-31 snapshot of /plain as the target values. Posted codes were not available
offline, so every search started from random, cross-polytope or two-simplex seeds.

What failed: for N between 2d+3 and 3d, unseeded search ended 7e-4 or more above the table cosine; sequential-LP polish
was dropped because up to 1460 of 2016 pairs are near-active and one HiGHS solve took 168 s.

What worked, at N = 2d + 2 only: log-sum-exp descent (sharpness 10 to 300) followed by threshold-penalty descent on
sum max(0, <x_i, x_j> - t)^2 with t lowered step by step; about 1000 loose restarts for (31, 64), the best six fully
descended (best 0.030331458, still above the table), then monotonic basin hopping (perturb, re-descend, accept if the
maximum cosine drops) for about two hours. That reached 0.0303197334, below the table's 0.030322662292. One of 193
cells.
