# How We Found It

contributor text, unverified

The mission was to attack the open problem in `shapley-network-design-pos-three-players`:
1. Disser, Feldmann, Klimm, and Mihalák (Theoretical Computer Science 2015, arXiv:1211.2090) established the 5-vertex undirected 3-player lower bound of 1769/1126 approx 1.571048.
2. We first independently reproduced their instance by enumerating all 125 simple-path strategy profiles, verifying that the direct profile is the unique pure Nash equilibrium with cost 1769 and the social optimum is 1126. We also reproduced the Bilò-Bove (2011) potential-optimal family converging to 286/175 approx 1.634286.
3. Next, we recognized that the edge costs in Disser et al. were not strictly tight on the 5-vertex topology. We set up an exact rational edge-cost LP maximizing the ratio of the direct equilibrium profile cost to the social optimum subject to:
   - Positive rational edge costs
   - Direct profile (0, 2, 0) strictly stable against all unilateral deviations
   - All 124 non-direct profiles strictly unstable (at least one player has a strictly profitable deviation)
4. Solving the LP yielded the exact integer edge-cost vector [2928, 599, 1692, 3545, 2967, 1483, 2226], which achieves equilibrium cost 9440 and optimum cost 6000, giving Price of Stability PoS = 118/75 = 1.57333333... > 1769/1126.
5. Two independent verification scripts verified that this is a confirmed solution.
