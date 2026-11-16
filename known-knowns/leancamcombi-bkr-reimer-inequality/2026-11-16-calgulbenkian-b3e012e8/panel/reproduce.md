context: Claude Code subagent, fresh context [Sonnet 5.5]

# REPRODUCE panel report: leancamcombi-bkr-reimer-inequality

All checks were run on a clean checkout of LeanCamCombi at 0a42535 (HEAD confirmed 0a42535119073f677dd60a28acbbdcda11b87f60; `git status --short` empty before and after, so the checkout was not touched). The author's scripts were NOT run. Scratch work is in a working folder that is not shipped in this package.

## 0. Manifest warnings
lake prints "manifest out of date: git revision of dependency 'AddCombi' changed" and the same for 'mathlib'. I compared `git rev-parse HEAD` of every dependency under .lake/packages with the rev in the lake manifest:
- AddCombi 6495ac1f0d3dedb7f767e011d98f68f3455b40ec = manifest
- mathlib dc2a600cfb9d99eb348ee7cb84b28167ad205265 = manifest
- plausible, LeanSearchClient, importGraph, proofwidgets, aesop, Qq, batteries, Cli: all equal the manifest rev.
So the checked-out revisions equal the manifest's. The warning looks like a stale-manifest-field warning on the repository side (cause not diagnosed; revisions are not the issue). Toolchain file: leanprover/lean4:v4.36.0-rc2.

## 1. Diff against upstream
sha256 of object/VanDenBergKesten.lean = b3e012e83c4ef62cb15af4da57291f28795c40447c4696345a8bb07199f4f4d8 (matches the claim). `diff` of upstream (107 lines) vs object (1070 lines) gives exactly four hunks and nothing is removed except the one sorry line:
- `10a11,23`: 13 added `import` lines (Mathlib BigOperators, Fintype.*, Order.Minimal, Tactic.Linarith, Tactic.Ring). Upstream's three `public import` lines are intact.
- `97a111,379`: new `section ReimerAuxiliary` (private defs and lemmas: toggle, reimerSpan, vecUR/vecUY/vecVB, zdot, ...), placed after `end BooleanAlgebra`.
- `98a381,844`: more private auxiliary lemmas and `end ReimerAuxiliary`.
- `105c851,1068`: the one changed upstream line, `lemma card_certificator_le : ... := sorry`, replaced by the same statement text with `:= by ...` (proof).
Upstream lines 1-97 (header, docstring, certificator, all lemmas to `end BooleanAlgebra`) are byte-identical, and the statement line of card_certificator_le is verbatim `lemma card_certificator_le : 2 ^ Fintype.card α * #(𝒜 □ ℬ) ≤ #𝒜 * #ℬ := ...` with the same preceding `variable [DecidableEq α] [Fintype α] {𝒜 ℬ 𝒞 : Finset (Finset α)}` and docstring.

Upstream declarations (all in namespace Finset) and status:
- certificator (noncomputable def, with `scoped[FinsetFamily] infixl:70 " □ "`): unchanged
- mem_certificator (@[simp]): unchanged
- certificator_subset_inter: unchanged
- certificator_subset_disjSups: unchanged
- certificator_comm: unchanged
- IsUpperSet.certificator_eq_inter: unchanged
- IsLowerSet.certificator_eq_inter: unchanged
- IsUpperSet.certificator_eq_disjSups: unchanged
- card_certificator_le: statement unchanged, proof changed from sorry to a real proof
No upstream declaration was dropped or reordered. Added declarations are all `private`. No new `@[simp]`/attribute/instance/notation/set_option/macro: grep of the object for `@[` finds only `@[expose] public section` and `@[simp] lemma mem_certificator`, both upstream.

## 2. Compile, sorry, axioms
`lake env lean` on a copy of object/VanDenBergKesten.lean with `#print axioms Finset.card_certificator_le` appended: no errors, no warnings except the two manifest warnings. Exact output:

`'Finset.card_certificator_le' depends on axioms: [propext, Classical.choice, Quot.sound]`

Compile time about 3 s (the file is fast to elaborate; the checkout's Mathlib cache was used). Second run gave identical output (deterministic). Control: the upstream file via `import CamCombi.PlainCombi.VanDenBergKesten` prints `[propext, sorryAx, Classical.choice, Quot.sound]`, so the check does detect sorry.
Every other declaration: I appended a `#eval` that runs `collectAxioms` on all 105 constants added by the file. Result: "constants in this file: 105; using sorryAx: []; axioms overall: [propext, Classical.choice, Quot.sound]". No `sorry` text in the file (grep).

## 3. Elaborated type
`set_option pp.all true in #check @Finset.card_certificator_le` after the object copy vs. in a file that imports the upstream (sorry) module. The printed types are character-for-character identical after renaming the universe variable (u_2 in mine vs u_1 upstream-import file). Nothing else differs (same instance arguments inst/inst_1, same Finset.certificator with Finset.booleanAlgebra instance, same HPow/HMul/LE terms).

## 4. Forbidden constructs
grep for sorry, admit, native_decide, ofReduceBool, implemented_by, extern, axiom, skipKernelTC, unsafe, opaque, set_option, macro, elab, syntax, notation, attribute, local, instance: no hits (only the two upstream `@[...]` lines above). Plus the kernel-level check in 2 (only the three standard axioms across all 105 constants, which also excludes ofReduceBool/native_decide and new axioms).

## 5. Independent exhaustive check
Own program (not shipped in this package, python -I), written from the definition: a in cert(A,B) iff a in A and a in B and exists x with y = complement of x such that every b with b&x = a&x is in A and every b with b&y = a&y is in B (subsets as bitmasks). Checked 2^n * |cert| <= |A| * |B| for ALL pairs of families:
- n=0: 4 pairs, no violation
- n=1: 16 pairs, no violation
- n=2: 256 pairs, no violation (37 non-trivial equality cases)
- n=3: 65536 pairs, no violation (653 non-trivial equality cases)
This is a spot check of the mathematics, not a substitute for the kernel.

## Limits
I did not check issue #34 status, upstream master freshness, or lake build of the whole repository (my task scope was items 1-5; the checkout's build state was as given). The compile was done with `lake env lean` as instructed, not `lake build`.

All five items confirmed with no mismatch, missing object or non-determinism.

pass: true
