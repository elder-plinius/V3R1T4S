# Preregistration: shift-scheduling record, instance 155

Frozen by the lead agent (Andy) before claim/ is built. The roster was found by the overnight run of 2026-11-21/22 (plan v2, frozen before launch: workhorse/plan.json, sha256 in workhorse/plan.sha256; exact CP-SAT 30 min, 4 workers, seed 1); this file fixes the claim, not the search.

null_test: not needed because the claimed result is one exact, checker-verified roster compared with a published best known value; no statistic or chance enters the decision.

## Object
- data/selected_solution.xml (sha256 ebc23f1e98aba3f30e7a272d07b650329416119c984d9ce1743e44c8d54dac9b): one roster for instance 155_28_10_2 in the site's solution format.

## Checks (all must hold)
1. An independent evaluator written from ProblemDefinition.pdf, which first reproduces penalty 889 on the site's example 8_7_20_2.Solution.889.xml, reports every hard constraint satisfied (code/verify_claim.py).
2. Its penalty is strictly below the instance's best known value 24 in the table fetched 2026-11-22T08:03:12Z (data/matsp.html).
3. The table and the changes page are re-fetched before any filing; if the best known value has dropped to or below the claimed penalty, the claim is withdrawn.
