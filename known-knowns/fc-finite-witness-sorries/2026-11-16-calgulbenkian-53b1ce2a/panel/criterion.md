context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report

Target: object/Solution.lean claims the full success criterion for RamseyNumbers.ramsey_number_six_six_lower_bound (R(6,6) >= 102, Paley graph on 101 vertices).

## Condition by condition (how each was checked)

1. Verbatim restatement, diffed against live main: PASS. I fetched live main (commit f50ff7be, newer than the pinned e028240a, 2026-11-15T22:20Z) and compared the raw FormalConjectures/Wikipedia/RamseyNumbers.lean, lean-toolchain and lake-manifest.json byte for byte with a clean checkout of formal-conjectures at e028240a: all three are identical, so the pinned commit and live main do not differ for these files. The docstring, attributes and statement in object/Solution.lean (`@[category research solved, AMS 5] theorem ramsey_number_six_six_lower_bound : ∃ G : SimpleGraph (Fin 101), G.CliqueFree 6 ∧ (Gᶜ).CliqueFree 6`) diff clean against live lines 183-190; only the body (`sorry` vs the proof term) differs. Same Mathlib SimpleGraph/CliqueFree definitions, no custom FC definition involved, so the "wrong definition" pitfall does not apply.
2. Tagged research solved: PASS (live attribute line 187).
3. Outside ErdosProblems, WrittenOnTheWallII, OEIS: PASS (Wikipedia/ folder).
4. Ends in sorry upstream, no formal_proof attribute: PASS. Live file's only formal_proof is on the R(5,5) lower bound (line 106); six_six_lower_bound has body `sorry` and none.
5. No open FC PR proving or linking it: PASS. I paged all 798 open PRs by title, body and branch for ramsey/six_six/R(6/Paley (none about this theorem), read the file patches of the Ramsey-related PRs #7660, #6953, #7574 (they link only R(3,x), R(4,4), Leinster etc.; no six_six), and ran GitHub issue searches for `ramsey_number_six_six`, `Paley`, `RamseyNumbers` among open PRs (0, 0, and 6 unrelated/other-number hits). Limitation: PR file lists were not enumerated for all 798, so a PR that touches the theorem without naming it in title/body is not strictly excluded; the search hits make that unlikely.
6. Compiles at the pinned toolchain and manifest: PASS. In the clean checkout at e028240a (lean-toolchain v4.33.1) `lake env lean` on a copy of the file succeeded with no errors or warnings in about 5 s. Caveat: this is a standalone module compiled with `lake env lean`, not a `lake build` of the repo with the proof spliced into RamseyNumbers.lean. My attempt to splice it in was botched by my own script (duplicate declarations), so I did not get a clean in-tree build; this is a packaging difference, not a soundness gap, since the same kernel checks the same statement.
7. No statement edits, no new axiom/sorry/admit/native_decide/ofReduceBool/implemented_by/extern/skipKernelTC: PASS. Grep of the whole file finds none of those tokens, no set_option, no unsafe/macro/elab/syntax/opaque, and the only import is FormalConjecturesUtil.
8. `#print axioms`: PASS. Output: [propext, Classical.choice, Quot.sound]. Also `#check` shows the exact type `∃ G, G.CliqueFree 6 ∧ Gᶜ.CliqueFree 6`.
9. Computation via kernel-checked reflection, not native: PASS (structural recursion checker with proved soundness lemmas plus `decide`; ran in seconds).

Hidden quantifiers / stretched definitions / null model: none found. The statement is an existential over graphs on Fin 101, so any graph works; no hidden parameter. Not subsumed by a merged package: no merged six_six formal_proof exists on live main, and R(5,5) is a different theorem. A "tie is not a record" rule does not bite since no one else has this item. The mathematical fact is classical (Kalbfleisch 1965); the criterion asks for a Lean proof of the FC statement, which this is.

confirmed_scope: A kernel-checked Lean 4 v4.33.1 proof, compiled standalone with `lake env lean` against a clean checkout of formal-conjectures at e028240a (whose RamseyNumbers.lean, lean-toolchain and lake-manifest.json are identical to live main f50ff7be), of the verbatim, research-solved, still-`sorry`, formal_proof-free theorem RamseyNumbers.ramsey_number_six_six_lower_bound with axioms exactly propext, Classical.choice and Quot.sound, with no open PR found proving or linking it (not a spliced in-tree `lake build`, and PR file lists not enumerated for all 798 open PRs).

pass: true
