# Honesty gate (leanapap-kelley-meka-integer-bound)

status: CONFIRMED_SOLUTION
confirmed_scope: Against LeanAPAP master fb5cb9c (re-fetched, still live) at Lean v4.36.0-rc2, the six staged files compile in a full lake build and prove, under open Finset Real, exactly the criterion's corrected theorem int with axioms only propext, Classical.choice and Quot.sound, and BohrSet.regularity (p1) is also proved sorry-free with its statement unchanged.

## Gate notes
- Object: object/Integer.lean, sha256 e82f63b5324cb2854fa6bfe9c92ec853d49798d350068e10957738abce223240.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Lean's kernel is the referee. The target's success criterion fixes the corrected statement of int (upstream's int is false as written, since C is unused), so int's type differs from upstream's by design; it is exactly the criterion's statement (the reproduce skeptic compared the kernel terms). BohrSet.regularity (partial win p1) keeps the upstream type. In a clean checkout of LeanAPAP at fb5cb9c (live master on 2026-11-17), with the six files staged, lake build APAP.Integer completes with no errors and no warnings, and #print axioms lists only propext, Classical.choice and Quot.sound for both; APAP.Prereqs.DummyPositivity is not in the import closure.
