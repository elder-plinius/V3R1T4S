# Preregistration: shift-scheduling record, instance 80

Frozen by the lead agent (Andy) before claim/ is built. The roster was found by the scout pilot of 2026-11-21 (code/cpsat_matsp.py, 300 s, 4 workers, seed 1; out/pilot.log; OPTIMAL after 81 s), which was not preregistered; this file fixes the claim, not the search.

null_test: not needed because the claimed result is one exact, checker-verified roster compared with a published best known value; no statistic or chance enters the decision.

## Object
- data/selected_solution.xml (sha256 a1398787321182386dce0ebb184a02ed062de9aea0dc25a30956c1277a1ad972): one roster for instance 80_14_10_2 in the site's solution format.

## Checks (all must hold)
1. An independent evaluator written from ProblemDefinition.pdf, which first reproduces penalty 889 on the site's example 8_7_20_2.Solution.889.xml, reports every hard constraint satisfied (code/verify_claim.py).
2. Its penalty is strictly below the instance's best known value 6 in the table fetched 2026-11-22T08:03:12Z (data/matsp.html).
3. The table and the changes page are re-fetched before any filing; if the best known value has dropped to or below the claimed penalty, the claim is withdrawn.
