# Honesty gate (flt-imperial-unclaimed-prop-sorries)

status: CONFIRMED_SOLUTION
confirmed_scope: On FLT main a321020 (re-checked today, no open PR or issue touching it), replacing the single sorry in Group.subsingleton_of_pow_prime_eq_one (and thus its @[to_additive] twin) in FLT/Patching/Utils/CompactHausdorffRings.lean with the claimed 803-line proof leaves the statement unchanged, builds that module and its importer AdicTopology under lean v4.35.0, and shows only propext, Classical.choice and Quot.sound, without a whole-repo build run by this skeptic.

## Gate notes
- Object: object/CompactHausdorffRings.lean, sha256 be407d0f4d9d2b6bac5c1b7b64f7ac9361ad711a3c8c4bcf05d8713729bc8bbd.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Lean's kernel is the referee. On 2026-11-17, in a clean checkout of FLT at a321020 (live main), with the solution in place of FLT/Patching/Utils/CompactHausdorffRings.lean, lake build of the module completes with no warnings and no errors; Group.subsingleton_of_pow_prime_eq_one and its @[to_additive] counterpart AddGroup.subsingleton_of_nsmul_prime_eq_zero have the same pp.all types as upstream, and #print axioms lists only propext, Classical.choice and Quot.sound for both.
