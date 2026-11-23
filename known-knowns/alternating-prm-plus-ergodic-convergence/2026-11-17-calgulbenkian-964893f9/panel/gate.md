# Honesty gate (alternating-prm-plus-ergodic-convergence)

status: CONFIRMED_PARTIAL
confirmed_scope: In Lean 4 with only propext, Classical.choice and Quot.sound, the last iterate (x_t, y_t) of simultaneous Predictive RM+ (Algorithm 2) from R = 0 and uniform strategies on A = [[3,0,-3],[0,3,-4],[0,0,1]] has duality gap at least 1/20 for every t >= 13203, so its liminf is positive; this says nothing about alternating PRM+, averaged iterates, or RM+.

## Gate notes
- Object: object/PRMPlus/Main.lean, sha256 964893f95e6fee87437002a8274f74b21ace1cd899e366e16fd40f9cb3dc598c.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Partial win p2 of the target, for PRM+ (Algorithm 2); the main criterion (ergodic convergence of alternating PRM+, Algorithm 8) is not addressed. Lean's kernel is the referee: in a fresh Lake project holding the 119 modules unchanged, on the Mathlib (2d833a6) that LeanAPAP fb5cb9c pins, lake build PRMPlus.Main completes (3489 jobs, no sorry; the only warnings advise the module system), and #print axioms lists only propext, Classical.choice and Quot.sound for the four main theorems. The exact and interval computations are checked by decide +kernel inside the proof.
- Definitions checked against the paper (arXiv:2311.00676v2, fetched 2026-11-17): alg2Step implements Algorithm 2 line for line (f(x, l) = l - x.l 1, the two clipped regret updates, the prediction step [R a working folder (not shipped)+ f]+ normalised by g), with A = [[3,0,-3],[0,3,-4],[0,0,1]], R = 0 and uniform start; normalising the zero vector gives the uniform strategy.
