# Criterion skeptic verdict: physlib-restricted-lorentz-connected

context: subagent (fresh Agent-tool context; saw only claim/)

(Saved by the run's main session from the skeptic's final message, verbatim apart from de-indentation; the skeptic
was told to return its verdict as text. Its scratch work is in runs/2026-10-14-0608/panel_work/criterion/.)

Besides claim/, I read only what my brief allowed. That was the Physlib, Mathlib and Lean toolchain sources under lean/, read-only. It included lean/physlib/.git/HEAD and lean/physlib/.git/index, read as plain files; I ran no git commands. A process listing and a directory listing showed me the names of sibling panel_work folders and of other agents' scratch files. I opened none of them.

## The criterion (CLAIM.md)
Success needs a kernel-checked proof of exactly Physlib's `semiformal_result "FXNL5" restricted_isConnected {d : ℕ} : IsConnected (restricted d : Set (LorentzGroup d))`, for every `d : ℕ`. The proof must be against Physlib be0f21e5002d6d73b87f2055530c1e8bf7151546, with no `sorry` and no axioms beyond `propext`, `Classical.choice` and `Quot.sound`. A counterexample would also count. The source lists no partial wins, so only the full criterion can pass.

## 1. Literal comparison of the statements
- **Published statement.** Lines 61-63 of `source/status_page_Restricted_Basic.lean` read:
  ```
  /-- The restricted Lorentz group is connected. -/
  semiformal_result "FXNL5" restricted_isConnected {d : ℕ} :
    IsConnected (restricted d : Set (LorentzGroup d))
  ```
  Its sha256 matches CLAIM.md. It is byte-identical to the local Physlib file `Physlib/Relativity/LorentzGroup/Restricted/Basic.lean` (`panel_work/criterion/env_integrity.log` records the diff as `identical`).
- **Frozen statement.** `checker/spec_restricted_isConnected.lean` (imports only Physlib) defines `def V3R1T4S.spec : Prop := ∀ {d : ℕ}, IsConnected (LorentzGroup.restricted d : Set (LorentzGroup d))`.
- **Textual comparison.** Both have the same implicit binder over all of ℕ, with no condition on `d`. The set is the same: the subgroup `restricted d` coerced to `Set (LorentzGroup d)`. The predicate is the same. The `LorentzGroup.` prefix in the spec stands in for the source's `namespace LorentzGroup`.
- **Term-level comparison.** `semiformal_result` elaborates the statement under `withoutModifyingEnv` (see Physlib's `Physlib/Meta/Informal/SemiFormal.lean`), so it leaves no declaration to compare with.
  - I re-elaborated the signature exactly as the macro does, as `noncomputable def … {d : ℕ} : IsConnected (restricted d : Set (LorentzGroup d)) := helper`. I did this in the source file's own context: importing only `Physlib.Relativity.LorentzGroup.Restricted.Basic`, inside `namespace LorentzGroup`, with `open Matrix`, `open minkowskiMatrix` and `open TopologicalSpace` (`panel_work/criterion/build/SrcCtx.lean`).
  - I then compared that with the frozen spec compiled under `import Physlib` (`panel_work/criterion/build/Compare.lean`). From `panel_work/criterion/compare_rerun.log` (0 errors, 0 warnings):
  ```
  [1] spec.value == (type of FXNL5 re-elaborated in source context): true
  [2] spec.value == srcStmt.value: true
  [3] spec.type == Prop: true; spec levelParams: []
  [4] claim.type == const V3R1T4S.spec: true; claim is a theorem: true
  [5] LorentzGroup.restricted is declared in module Physlib.Relativity.LorentzGroup.Restricted.Basic
  [5] IsConnected is declared in module Mathlib.Topology.Connected.Basic
  [5] instTopologicalSpaceElemMatrixSumFinOfNatNatRealLorentzGroup is declared in module Physlib.Relativity.LorentzGroup.Basic
  ```
  - That is structural `Expr` equality, not only definitional equality, and `example : V3R1T4S.spec = LorentzGroup.V3R1T4S_srcStmt := rfl` elaborated too. With `pp.explicit`, both statements print the same topology argument:
  ```
  def V3R1T4S.spec : Prop :=
  ∀ {d : Nat},
    @IsConnected
  ...
      (@instTopologicalSpaceElemMatrixSumFinOfNatNatRealLorentzGroup d)
  ```
  and
  ```
  @LorentzGroup.V3R1T4S_src_restricted_isConnected : ∀ {d : Nat},
    @IsConnected
  ...
      (@instTopologicalSpaceElemMatrixSumFinOfNatNatRealLorentzGroup d)
  ```
- **Topology.** The only `TopologicalSpace` instance on `LorentzGroup d` anywhere in Physlib, PhyslibAlpha or QuantumInfo is the following, at Physlib `Physlib/Relativity/LorentzGroup/Basic.lean:143` (`panel_work/criterion/subsumption_greps.log`):
  ```
  instance : TopologicalSpace (LorentzGroup d) := instTopologicalSpaceSubtype
  ```
  This is the subspace topology inherited from the matrix topology.
- **`IsConnected`.** It is Mathlib's root definition (nonempty and preconnected). No `IsConnected` definition shadows it in the `LorentzGroup`, `Matrix`, `minkowskiMatrix` or `TopologicalSpace` namespaces.
- **The set is the genuine one.** All definitions are Physlib's own:
  - `restricted d` has carrier `{Λ | IsProper Λ ∧ IsOrthochronous Λ}`.
  - `IsProper Λ := Λ.1.det = 1`.
  - `IsOrthochronous := 0 ≤ Λ.1 (Sum.inl 0) (Sum.inl 0)`.
  - `LorentzGroup d := {Λ | Λ * dual Λ = 1}`, with `dual = η * Λᵀ * η`.
- **Result.** No weakening: not only some `d`, not a different set, topology, group or `IsConnected`, and no change in name resolution.

## 2. The object proves the frozen statement
- **Hashes.** sha256 of `object/RestrictedIsConnected.lean`, `checker/spec_restricted_isConnected.lean`, `checker/lean_claim_check.py` and `source/status_page_Restricted_Basic.lean` all match CLAIM.md (8bef4eda…, fe815010…, fe7aaf99…, e41850ba…).
- **Provided checker.** I ran the command from REPRODUCE.md through the kit's slot gate. Output from `panel_work/criterion/checker_run.log`:
  ```
  spec compile: exit 0
  candidate compile: exit 0
  check file: exit 0
  'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]
  axioms: ['Classical.choice', 'Quot.sound', 'propext']
  PASS
  ```
- **Independent recompile.** I recompiled the three modules myself (`panel_work/criterion/run_compare.sh`). The object compiled with exit 0 and no warnings. From `panel_work/criterion/compare_rerun.log`:
  ```
  'V3R1T4S_check_criterion' depends on axioms: [propext, Classical.choice, Quot.sound]
  'V3R1T4S.claim' depends on axioms: [propext, Classical.choice, Quot.sound]
  'V3R1T4SConstructExplicit.SO_pathConnectedSpace' depends on axioms: [propext, Classical.choice, Quot.sound]
  'LorentzGroup.toBoostRotation' depends on axioms: [propext, Classical.choice, Quot.sound]
  'Lorentz.Velocity.isPathConnected' depends on axioms: [propext, Classical.choice, Quot.sound]
  ```
- **No redefinitions.**
  - The spec is compiled as its own module before the object is loaded, so the object cannot change what it means.
  - A grep of the object for `@[`, `attribute`, `instance`, `set_option`, `notation`, `macro`, `axiom`, `opaque`, `sorry`, `admit`, `#eval`, `run_cmd`, `elab` and `syntax` found no matches.
  - The compiled module declares only names under `V3R1T4SConstructExplicit.*` plus `V3R1T4S.claim`:
    ```
    [6] V3R1T4SClaim declares 43 constants; axioms/opaques among them: 0
    ```
  - Its only extension entry that is not bookkeeping is one automatic `backward_defeq` tag. Lean adds it to theorems proved by `rfl`, here the module's own equation lemma `hh.eq_1`. It cannot affect the already-frozen spec.
- **Proof route.** This is for the record; my verdict relies only on the kernel check. SO(n) is shown path-connected for every n, by explicit paths built from pairs of Householder reflections. Physlib's `Lorentz.Velocity.isPathConnected` and Physlib's homeomorphism `LorentzGroup.toBoostRotation : restricted d ≃ₜ Velocity d × SO(d)` then give path-connectedness of `restricted d`. `IsPathConnected.isConnected` finishes. There is no case split on `d`; `d = 0` is covered by the same term.
- **Environment.**
  - `lean/physlib/.git/HEAD` reads `be0f21e5002d6d73b87f2055530c1e8bf7151546`.
  - Working tree against the git index gives `index version 2, 1259 entries; checked 1071; modified 0; missing 0; untracked .lean 0`.
  - `lean-toolchain` is `leanprover/lean4:v4.34.1`.
  - The oleans for files changed at the 06:07 checkout were rebuilt after it. For example, `Physlib.olean` is from 06:08:15 and `Physlib.lean` from 06:07:38.
  - The `Restricted/Basic` and `FromBoostRotation` oleans were built from sources unchanged since the original 04:56 checkout.
  - Caveat: I did not resolve the index against the HEAD tree object, since I ran no git commands. "At be0f21e5" therefore rests on `.git/HEAD` plus the clean index match.

## 3. Genuine, non-subsumed win?
- **Full criterion met, literally.** The proof covers exactly this statement, for every `d`, against Physlib be0f21e5, is kernel-checked, and uses only the three standard axioms. The source offers no partial wins and the claim asks for none.
- **Not subsumed.**
  - At be0f21e5, FXNL5 exists only as a `semiformal_result`, which adds no declaration.
  - Nothing in Physlib, PhyslibAlpha or QuantumInfo proves that `restricted` is connected. The only other hit is `restricted_eq_identity_component_of_isConnected`, which takes it as hypothesis `h1`.
  - Mathlib has no connectedness or path result for `specialOrthogonalGroup` (grep: no matches), so the object's SO(n) argument does real work (`panel_work/criterion/subsumption_greps.log`).
  - The copy fetched from master at 06:07:15Z still has it as semiformal.
- **Null models.** These do not apply: this is a deterministic, kernel-checked proof, with no sampling, statistic or search rate to compare against a baseline. The nearest checks are a vacuous statement, a trivialised set or topology, and a target already proved. All three were done above and came back clean.
- **Minor discrepancy.** CLAIM.md line 23 says the copy is saved in `data/status_page_Restricted_Basic.lean`, but it is at `source/status_page_Restricted_Basic.lean`. Line 16 names it correctly and the sha256 matches, so this does not affect the result.

confirmed_scope: Against the local Physlib build at commit be0f21e5002d6d73b87f2055530c1e8bf7151546 with Lean v4.34.1, object/RestrictedIsConnected.lean kernel-checks `V3R1T4S.claim : V3R1T4S.spec` using only the axioms propext, Classical.choice and Quot.sound, where `V3R1T4S.spec` is `∀ {d : ℕ}, IsConnected (LorentzGroup.restricted d : Set (LorentzGroup d))` and is structurally identical to the statement of Physlib's `semiformal_result "FXNL5" restricted_isConnected` re-elaborated in its own source context (Physlib's subspace topology on `LorentzGroup d`).

pass: true
