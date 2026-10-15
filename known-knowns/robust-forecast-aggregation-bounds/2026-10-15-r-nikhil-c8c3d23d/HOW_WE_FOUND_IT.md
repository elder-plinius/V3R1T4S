# How we found it (contributor text, unverified)

**Brief.** The research charter listed this cell of Chen, Peng and Tang's prior-agnostic robust forecast aggregation
problem (arXiv:2604.24517): two experts whose signals are conditionally independent given a binary state with unknown
values, squared loss, additive regret against the omniscient aggregator. Published bounds: 31/1326 (lower, Theorem
3.4, certified by a uniform mixture of two explicit structures through Yao's principle) and 0.025512 (upper, a
floating-point maximisation). Any explicit adversary mixture certifying strictly more than 31/1326 would count.

**What failed.** A discretised game (solver lens): every environment whose reports lie on a grid of spacing 1/12 or
1/24, with the adversary's best mixture over all of them, returned exactly 31/1326, so on those grids the paper's
construction is already optimal. On the upper-bound side (certifier lens), aggregators whose logit weight depends on
|x1 - x2| reached a floating-point worst-case regret of about 0.02415, below the published 0.025512, but that is a
multi-start maximisation (NUMERICAL), no interval certificate was attempted, and nothing is claimed about it. Two searches meant to try three and four environments ran the default two-environment
setting instead, because of a shell quoting slip, so larger mixtures were not explored.

**What worked.** Treating the lower bound as a smooth function of the construction's numbers (reports, states, prior
means, weights) and running Nelder–Mead from the paper's own point: the point is not a local maximum. The optimiser
moved the reports inward from 1/6 and 5/6 to about 0.167325 and 0.832675 and the prior means from 5/12 and 7/12 to about
0.417121 and 0.582879, and 200 random restarts found the same optimum. The gain is tiny (about 2.2e-7), so the
float point was rounded to short fractions inside the mirror-symmetric family (environment B the image of A under
x ↦ 1 − x), 11 rational points were evaluated exactly, and the best, reports 6693/40000 and 33307/40000 with prior
mean 417121/1000000, became the object. (The certifier lens, working separately on a "veto plus mirror" two-environment family, located
the same float optimum near 0.832676 and 0.417119.) Every number was then checked with exact fractions by two separately written
programs.
