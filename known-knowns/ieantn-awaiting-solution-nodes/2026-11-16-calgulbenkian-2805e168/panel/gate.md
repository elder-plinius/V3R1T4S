# Honesty gate (ieantn-awaiting-solution-nodes)

status: CONFIRMED_SOLUTION
confirmed_scope: As of live main d60421f, the Lake project Solutions/ZetaHadamard.v1 (the node's only conclusion, unconditional, no declared imports) passes Comparator 10dd2b33 with lean4export cacf989b on the Lean kernel using only propext, Classical.choice and Quot.sound, run with the fake sandbox and with the NanoDa replay not run here, and the node had no solution, receipt, claim or open PR when fetched.

## Gate notes
- Object: object/Solutions/ZetaHadamard.v1/Solution.lean, sha256 2805e1685be99c2dc1adc74bbcd69e74aef77bb69054393c3f842a9cf12cc228.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Lean's kernel and Comparator are the referees. On 2026-11-16 IEANTN live main was the pinned commit d60421f; in a clean checkout there the solution project builds with no warnings, the challenge and solution declare the same pp.all type, #print axioms lists only propext, Classical.choice and Quot.sound, and Comparator 10dd2b33 with lean4export cacf989b (the tools IEANTN's verification script pins) prints 'Lean default kernel accepts the solution' and 'Your solution is okay!'.
- Two limits of that Comparator run, stated in the scope sentence: macOS has no Landlock, so it ran with Comparator's own fake-landrun script instead of the landrun sandbox (the sandbox protects the machine, not the result), and the NanoDa kernel replay that IEANTN's own verification adds was not run (enable_nanoda set to false in a copy of comparator.json, because NanoDa is not built here). IEANTN's receipt-writing workflow is the maintainers' own; no IEANTN pull request is opened.
