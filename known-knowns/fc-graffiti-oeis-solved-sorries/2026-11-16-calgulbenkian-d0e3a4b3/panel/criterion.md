context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report: fc-graffiti-oeis-solved-sorries (GraphConjecture25.conjecture25)

## Verdict in brief
Every literal condition of the full success criterion checked out. I found no hidden quantifier, stretched definition or subsumption.

## Condition by condition (how I checked)
1. Verbatim statement vs live FC main. I fetched the raw target file, lean-toolchain and the lake manifest from live main (live main is now at a later commit than the pin, f50ff7be, 2026-11-15T22:20Z). All three are byte-identical (cmp) to the clean checkout of formal-conjectures at e028240a. The theorem text, docstring and attributes in object/Solution.lean equal the upstream file: a line diff of the pinned file against object/Solution.lean shows exactly one removed line, `sorry`. Everything else is additions (helper lemmas before the theorem, the proof body). The statement is untouched.
2. Tagged research solved, ended in sorry, no formal_proof. Upstream has `@[category research solved, AMS 5]` and `sorry`, with no formal_proof attribute (read directly from the checked-out and live files).
3. No open FC PR proving or linking it. I paginated all 798 open PRs by title, then fetched the file lists of every PR whose title mentions WrittenOnTheWallII, WOWII, Graffiti, formal_proof or "link ... proof" (about 40 PRs, including the 22-statement link PR 7660, 7661 and 6901). A substring match flagged PRs 7366 and 7367, but those touch GraphConjecture252/253, not 25. A text search for "GraphConjecture25" in PRs returns zero open PRs. The only PR ever naming it is 3796, merged 2026-10-23, which added the statement (no proof). Limit: the file-list scan covered title-matched PRs, not all 798; an untitled PR touching the file is excluded only by the weaker text search.
4. Compiles, no forbidden tokens. Running the solution file inside the pinned checkout (`lake env lean`, toolchain v4.33.1) succeeded with no errors or warnings. Case-insensitive grep finds 0 occurrences of sorry, admit, axiom, native_decide, ofReduceBool, implemented_by, extern, skipKernelTC. There is no set_option, unsafe, opaque, macro, elab, attribute or instance line. The proof uses `decide` (kernel evaluation), which is allowed. Caveat: I ran `lake env lean` on the file, not a full `lake build` of the module, so FC's own linters were not run by me.
5. Axioms. `#print axioms` gave exactly [propext, Classical.choice, Quot.sound].
6. Universe polymorphism. `#check` shows `conjecture25.{u_1} : ¬∀ {α : Type u_1} [Fintype α] [DecidableEq α] [Nontrivial α] (G : SimpleGraph α), G.Connected → ... 2 * ⌈(1+minDistEven)/3⌉ ≤ G.b`, matching the upstream signature. The counterexample is built on `ULift.{u} (Fin 15)` for arbitrary u, with connectivity, Nontrivial, distEven = 7 at every vertex, and b <= 4 proved in-file. The proof covers the statement as stated, at every universe level.

## Null model, definitions, pitfalls
- The statement is a negation (the conjecture was known false, status F), so one counterexample proves it. This is the "FC statement should be the negation" pitfall, and the proof matches the negated form.
- distEven and b come from FC's own utility library; the solution does not redefine them.
- No bounded enumeration stands in for the universal claim (the p1 trap): the proof is a full proof of the stated theorem. The finite `decide` checks only verify properties of the one fixed 15-vertex graph.
- Subsumption rule: no merged FC proof of this item exists, and nothing merged implies it by restriction. The README correctly says the falsity was already in the literature; only the Lean formalization is claimed, which is what the criterion asks for.

## Residual limits
- My open-PR search was run on 15 Nov 2026, independent of the package's own earlier check.
- No full `lake build` by me; I did not review the Python check scripts (not needed for the kernel result).

confirmed_scope: The file object/Solution.lean, compiled against a clean checkout of formal-conjectures at e028240a (whose target file, lean-toolchain and lake-manifest are byte-identical to live main on 2026-11-15), proves the unaltered universe-polymorphic statement WrittenOnTheWallII.GraphConjecture25.conjecture25 (a research solved item that was a sorry, with no formal_proof and no open PR proving or linking it) with only propext, Classical.choice and Quot.sound and no forbidden tokens.

pass: true
