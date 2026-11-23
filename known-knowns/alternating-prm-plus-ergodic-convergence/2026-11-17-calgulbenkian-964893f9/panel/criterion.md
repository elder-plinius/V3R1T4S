context: Claude Code subagent, fresh context [Sonnet 5.5]

Verdict on partial win p2 (criterion skeptic).

What I checked, literally:
- Statement. In a fresh Lake project with the 119 modules on LeanAPAP fb5cb9c's Mathlib, I printed `alg2_caiGame_liminf_dualityGap_pos`. It reads: 0 < Filter.liminf (fun t => DualGap caiGameA (alg2Iter caiGameA t).x (alg2Iter caiGameA t).y) atTop. That is the last iterate (x_t, y_t), not averages, and a liminf over t, as p1/p2 require. #print axioms gives exactly [propext, Classical.choice, Quot.sound]. A grep of the modules finds no sorry, axiom, native_decide or ofReduceBool (only the doc comment in object/PRMPlus/Main.lean mentions them).
- Duality gap. object/PRMPlus/Defs.lean defines DualGap as sSup over y' in the simplex of x^T A y' minus sInf over x' in the simplex of x'^T A y. That is the standard variational gap; boundedness is proved in Lean (caiGameA_dualGap_le, payoff bounds), so the real-valued sSup/sInf are not junk-valued. The liminf is taken in the reals with a proven upper bound, so cobounded-ness is not a loophole.
- Algorithm. alg2Step uses simultaneous updates: both regrets are updated from the same (x_t, y_t), then both strategies come from [R' - f]^+ normalised (prediction = last loss). That is the simultaneous PRM+ shape (Algorithm 2), not alternating PRM+ (alg8Step is defined but is not what the theorem uses) and not RM+. I compared it to my reading of the paper's Algorithm 2 from memory; I did not fetch arXiv in this run (no a working file (not shipped) entries), so the match is by the definitions' own comments and standard form, not a fresh diff against the PDF.
- Matrix and start. caiGameA is [[3,0,-3],[0,3,-4],[0,0,1]] exactly. alg2Iter 0 = initState: R = 0, x = y = (1/3,1/3,1/3). 0/0 convention for normalize is uniform, as in the paper.
- Computation inside the proof. The reach/tube steps are exact or interval computations checked by `decide +kernel` inside Lean and linked to alg2Iter through the encoding lemmas (reach_iter13203, entry_iter13203, all_256_slabs, eventual_dualityGap_of_tube). The theorem alg2_caiGame_eventual_dualityGap_ge (all t >= 13203, gap >= 1/20) feeds the liminf theorem. Nothing the argument relies on sits outside the proof.
- Hidden quantifiers and stretching: none found. The result is about one game, one start, and Algorithm 2 only. The "iteration 1000 bounds" theorem is a sanity cross-check, not part of the win.

Null models / subsumption: p2 is an enumerated partial win ("simultaneous RM+ or PRM+"), so PRM+ alone qualifies. It is not subsumed by p1 (alternating RM+ is a different algorithm). The bank text says the paper only showed this numerically; no prior formal proof is cited. I did not search the 2025-2026 literature.

Not settled: the main criterion, ergodic convergence of ALTERNATING PRM+ (Algorithm 8), is not addressed at all. Nothing here proves or refutes it, and p1 (alternating RM+) is also not proved.

confirmed_scope: In Lean 4 with only propext, Classical.choice and Quot.sound, the last iterate (x_t, y_t) of simultaneous Predictive RM+ (Algorithm 2) from R = 0 and uniform strategies on A = [[3,0,-3],[0,3,-4],[0,0,1]] has duality gap at least 1/20 for every t >= 13203, so its liminf is positive; this says nothing about alternating PRM+, averaged iterates, or RM+.

pass: true
