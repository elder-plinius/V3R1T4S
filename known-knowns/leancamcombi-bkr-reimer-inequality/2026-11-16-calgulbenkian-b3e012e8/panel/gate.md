# Honesty gate (leancamcombi-bkr-reimer-inequality)

status: CONFIRMED_SOLUTION
confirmed_scope: On a clean LeanCamCombi checkout at master 0a42535 (toolchain v4.36.0-rc2, dependency revisions equal to the manifest pins), replacing only the `:= sorry` of Finset.card_certificator_le with the proof in object/VanDenBergKesten.lean (plus extra private helpers and non-public imports) yields a file that elaborates with no errors, leaves the lemma statement and certificator definition verbatim, depends only on propext, Classical.choice and Quot.sound, while issue #34 is still open with no PR proving it.

## Gate notes
- Object: object/VanDenBergKesten.lean, sha256 b3e012e83c4ef62cb15af4da57291f28795c40447c4696345a8bb07199f4f4d8.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Lean's kernel is the referee. Re-checked on 2026-11-16: LeanCamCombi live master is the pinned commit 0a42535 and issue 34 is open; with the solution in place of CamCombi/PlainCombi/VanDenBergKesten.lean, lake build of the module completes (2121 jobs) with no errors; its only warnings are lake's two manifest notices, which this commit prints with or without the solution, and the checked-out Mathlib (dc2a600) and AddCombi (6495ac1) are the manifest's pins. The pp.all type equals the upstream declaration's up to the name of the universe variable, and #print axioms lists only propext, Classical.choice and Quot.sound.
