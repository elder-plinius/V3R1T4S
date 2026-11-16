# Honesty gate (fc-graffiti-oeis-solved-sorries)

status: CONFIRMED_SOLUTION
confirmed_scope: The file object/Solution.lean, compiled against a clean checkout of formal-conjectures at e028240a (whose target file, lean-toolchain and lake-manifest are byte-identical to live main on 2026-11-15), proves the unaltered universe-polymorphic statement WrittenOnTheWallII.GraphConjecture25.conjecture25 (a research solved item that was a sorry, with no formal_proof and no open PR proving or linking it) with only propext, Classical.choice and Quot.sound and no forbidden tokens.

## Gate notes
- Object: object/Solution.lean, sha256 d0e3a4b3ef31bab45d3fb0a942cb1cb804b321d7d6e1004cdac8f5b01a85b31d.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini) is a different model family from every skeptic.
- Lean's kernel is the referee. Re-checked on 2026-11-16: formal-conjectures live main (f50ff7be) has the same FormalConjectures/WrittenOnTheWallII/GraphConjecture25.lean, lean-toolchain and a working file (not shipped) as the pinned commit e028240a; with the solution in place of that file, lake build of the module completes with no warnings and no errors, its pp.all type equals the upstream declaration's, and #print axioms lists only propext, Classical.choice and Quot.sound.
