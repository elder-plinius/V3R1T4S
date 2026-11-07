# How we found it (contributor text, unverified)
We reused our vectorised re-implementation of the official evaluator (matching it to 3.3e-6 MWh on all 13 published
16-turbine layouts). Re-scoring the results folder showed participant 12 is best (421561.9) but 3.5 m outside the
circle; the best feasible published value is DPCRO-SL's 419935.8. What failed: 40000 random starts with wake-expansion
continuation and SLSQP (best 419835.0, never reaching participant 12's basin); 1920 structured ring starts (best
417575); basin-hopping around participant 12 repaired and polished (stuck at 421912.3). What worked: a ruin-and-recreate
large-neighbourhood search imported from vehicle routing (remove 1-4 turbines, re-insert each at the best point of a
50 m grid plus a dense boundary ring, SLSQP polish, keep if better), started from four distinct random-start optima.
One chain reached 424131.95 in 83 moves and held it for 7400 more; four larger-move chains (up to 8 turbines, 25 m
grid) found nothing higher. Warm starts from participant 12 and DPCRO-SL plateaued at 422634.9 and 422923.0. The final
layout turned out to share 14 turbine sites with participant 12's.
