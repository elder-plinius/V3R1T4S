context: subagent

Independent verification of the Shapley network design and GSP Price of Anarchy instances:

1. Shapley 3-player network design instance:
   - Undirected graph with 5 vertices (0, 1, 2, 3, 4) and 7 edges:
     c(0,1) = 2928, c(0,2) = 599, c(1,3) = 1692, c(1,4) = 3545, c(2,3) = 2967, c(2,4) = 1483, c(3,4) = 2226.
   - Commodity pairs: P1 (0, 1), P2 (2, 3), P3 (4, 1).
   - Each player has 5 simple paths, yielding exactly 125 strategy profiles.
   - Full enumeration in exact rational arithmetic verifies:
     - Profile (0, 2, 0) corresponding to direct paths is the UNIQUE pure Nash equilibrium with social cost 9440.
     - Profile (4, 4, 3) is the UNIQUE social optimum with social cost 6000.
     - Price of Stability PoS = 9440 / 6000 = 118/75 = 1.57333333... > 1769/1126 = 1.57104796... (+193/84450).
     - Verified independently by two separate scripts (verify_improved_pos_instance.py and independent_checker.py) with 100% agreement.

2. GSP pure Nash calibrations and certification:
   - 2-slot calibration: v = (1, 1/2), alpha = (1, 1/2), b = (0, 1/2) yields exact ratio 5/4 = 1.25.
   - 3-slot calibration: v = (1, 0.5296, 0.14583), alpha = (1, 0.55071, 0.4704), b = (0, 0.5296, 0.14583) yields ratio 1.2591334.
   - Exhaustive certification of all 24 rankings in S_4 confirms pure Nash PoA <= 1.259134 with overall worst-case ranking [1, 2, 0, 3] at 1.2591334.
   - Multi-slot search for n in {4, 5, 6, 7, 8} across cyclic shifts, generalized Ding permutations, two-block shifts, full reversals, and derangements confirms pure Nash ratio <= 1.259134.

pass: true
