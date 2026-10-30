context: subagent

# Skeptic Reproduction Report: Stable Marriage Maximum Stable Matchings

Independent reproduction and verification of the claimed mathematical breakthroughs:

1. **Preference Lists Verification**:
   - Parsed `object/instance_n19.txt`: verified that all 38 preference rows (19 men and 19 women) are strict complete permutations of $\{1, \dots, 19\}$.
2. **Dual Counting Verification**:
   - Method 1 (Irving-Leather rotation poset closed-set DP): 128 rotations, 95,449 memoized states, exactly 642,696 stable matchings.
   - Method 2 (Gusfield breakmarriage lattice traversal): visited 642,696 matchings from Gale-Shapley man-optimal to woman-optimal, verifying zero blocking pairs on each.
   - Exact numerical agreement: `agree: yes` (642,696 = 642,696).
3. **Composite Orders**:
   - Re-verified composite instances: $n=14$ (23,744), $n=18$ (530,528), and $n=22$ (12,277,568), all passing permutation and dual counting checks with exact agreement.

pass: true
