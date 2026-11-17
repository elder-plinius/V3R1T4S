# Criterion skeptic verdict: physlib-clifford-dirac-iso (run 2026-10-14-0615)

context: subagent (fresh Agent-tool context; saw only claim/)

(Saved by the run's main session from the skeptic's final message, verbatim apart from de-indentation; the skeptic
was told to return its verdict as text. Its scratch work is in runs/2026-10-14-0615/panel_work/criterion/.)

**What I read**
- **Claim files:** CLAIM.md, REPRODUCE.md, checker/spec_ofCliffordAlgebra_injective.lean, checker/lean_claim_check.py, object/OfCliffordAlgebraInjective.lean, source/status_page_CliffordAlgebra.lean.
- **Also, as permitted:** the built Physlib and Mathlib sources under lean/physlib (read-only), and the slot-gate wrappers tools/lean_env.sh and tools/lean_slot.sh that I was told to run. These only set PATH and caches and limit how many Lean processes run at once.
- **Nothing else.** A `ps` listing showed other agents' command lines by accident; I opened none of their files.

## 1. Criterion vs. published source vs. frozen statement

Published source: source/status_page_CliffordAlgebra.lean, lines 32-40. It is byte-identical to Physlib/Relativity/CliffordAlgebra.lean at be0f21e5 (`cmp` reports identical; sha256 is 70ca93d7…de0d for both):
```
## TODO

- Complete the isomorphism by proving injectivity of `ofCliffordAlgebra` (requires dimension theory)
- Construct the `AlgEquiv` between `CliffordAlgebra diracForm` and `diracAlgebra`

-/

@[expose] public section
TODO "Prove injectivity of ofCliffordAlgebra and construct the full isomorphism."
```
Frozen statement, compiled on its own with only `import Physlib`: `def V3R1T4S.spec : Prop := Function.Injective spaceTime.γ.ofCliffordAlgebra`.

**Literal reading**
- **(a) Injectivity.** The TODO asks for two things: (a) injectivity and (b) the AlgEquiv. The frozen statement is exactly (a). It is a closed proposition about one named Physlib constant: no hypotheses, no free parameters, and no instances the prover can choose (the spec is elaborated before the object is loaded). There are no hidden quantifiers.
- **(b) The AlgEquiv.** The object does not state it. Given (a) and Physlib's proved `ofCliffordAlgebra_surjective`, it takes one line, and the source itself says proving injectivity is what will "Complete the isomorphism". I compiled `AlgEquiv.ofBijective spaceTime.γ.ofCliffordAlgebra ⟨V3R1T4S.claim, spaceTime.γ.ofCliffordAlgebra_surjective⟩ : CliffordAlgebra diracForm ≃ₐ[ℝ] diracAlgebra` (panel_work/criterion/build/CriterionProbe.lean). Its underlying function equals `ofCliffordAlgebra` by `rfl`, and it depends only on [propext, Classical.choice, Quot.sound].
- **The criterion is a faithful reading.** CLAIM.md asks for a kernel-checked injectivity proof at be0f21e5, with no `sorry` and only the three standard axioms. That matches the source, provided the AlgEquiv is described as a corollary checked by the panel, not as content of the object.
- **No stretched definitions.** `diracForm` (the (+,-,-,-) form on Fin 4 → ℝ), `diracAlgebra` (`Algebra.adjoin ℝ γSet` inside the 4×4 complex matrices) and `ofCliffordAlgebra` (`CliffordAlgebra.lift`) are all Physlib's own.
- **Partial wins.** The source lists none. None are needed, because the full criterion is met.
- **Minor and not material.** CLAIM.md line 23 says the copy is saved in `data/status_page_CliffordAlgebra.lean`. It is actually source/status_page_CliffordAlgebra.lean (line 16 says so), and the hash matches.

## 2. Does the object prove the frozen statement?

Hashes match CLAIM.md (`sha256sum`):
```
13837a7e226a97b9fef5bd04d6f362c0db869627cfa3a7239d4f54343cde5c8b  object/OfCliffordAlgebraInjective.lean
e57fc5fa63bde2b1b045dde255be28fd07f26d7fd1da9a7845011f0dbd1b37e8  checker/spec_ofCliffordAlgebra_injective.lean
fe7aaf99a0b13f23a3c232a5a5fbfa8d33750e5f809cc0bf36e3c87ef9a828de  checker/lean_claim_check.py
70ca93d773d8a8f2c2fe43e607125ae1d3042d7530bace4371cd5eba5bf8de0d  source/status_page_CliffordAlgebra.lean
```
- **Physlib checkout:** `git rev-parse HEAD` gives `be0f21e5002d6d73b87f2055530c1e8bf7151546`.
- **Clean trees:** `git status --porcelain` is empty for Physlib and for its Mathlib package.
- **Toolchain:** lean-toolchain is `leanprover/lean4:v4.34.1`.
- **TODO still open:** Physlib.lean line 416 is `public import Physlib.Relativity.CliffordAlgebra`.

**(a) Provided checker.** Run as REPRODUCE.md says, under the slot gate (log: panel_work/criterion/checker_run.log):
```
spec compile: exit 0
candidate compile: exit 0
check file: exit 0
'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]
axioms: ['Classical.choice', 'Quot.sound', 'propext']
PASS
```

**(b) Independent recompile plus my own probe.** I recompiled unmodified copies (same sha256) and ran a probe file. Files: panel_work/criterion/run_probe.sh and panel_work/criterion/build/CriterionProbe.lean; log: panel_work/criterion/probe_run.log.
- The spec, the object and the probe all exited 0, and there are no error or `sorry` lines.
- The object's only warnings are linter style warnings: one `haveI` suggestion and two unused simp arguments.
- Key output:
```
PROBE-MODULE spaceTime.γ.ofCliffordAlgebra : Physlib.Relativity.CliffordAlgebra
PROBE-MODULE spaceTime.γ.diracForm : Physlib.Relativity.CliffordAlgebra
PROBE-MODULE spaceTime.γ.diracAlgebra : Physlib.Relativity.CliffordAlgebra
PROBE-MODULE spaceTime.γ.ofCliffordAlgebra_surjective : Physlib.Relativity.CliffordAlgebra
PROBE-MODULE V3R1T4S.spec : V3R1T4SSpec
PROBE-MODULE V3R1T4S.claim : V3R1T4SClaim
def V3R1T4S.spec : Prop :=
Function.Injective ⇑spaceTime.γ.ofCliffordAlgebra
'criterion_check' depends on axioms: [propext, Classical.choice, Quot.sound]
'V3R1T4S.claim' depends on axioms: [propext, Classical.choice, Quot.sound]
'criterion_iso' depends on axioms: [propext, Classical.choice, Quot.sound]
KF.finrank_cl : Module.finrank ℝ (CliffordAlgebra spaceTime.γ.diracForm) = 16
KF.finrank_dirac_ge : 16 ≤ Module.finrank ℝ ↥spaceTime.γ.diracAlgebra
'criterion_finrank_dirac' depends on axioms: [propext, Classical.choice, Quot.sound]
probe exit 0
```
- Both of these also elaborate:
  - `example : V3R1T4S.spec = Function.Injective (⇑spaceTime.γ.ofCliffordAlgebra) := rfl`
  - `theorem criterion_check : Function.Injective (⇑spaceTime.γ.ofCliffordAlgebra) := V3R1T4S.claim`

**No redefinitions.** The probe lists every constant the object module adds (`PROBE-CLAIM-CONSTS count=43`):
- 37 under `KF.*`, including auto-generated `_proof_*`, `.eq_1` and `_simp_*` entries.
- `V3R1T4S.claim`.
- 5 private match-equation lemmas that Lean generates on demand: `_private.V3R1T4SClaim.0.Fermion.Dirac.gammaMatrix_basis_toMatrix.match_1.{eq_1..eq_4,splitter}`.

None of them is `diracForm`, `diracAlgebra`, `ofCliffordAlgebra` or `γSet`, and none is in the `spaceTime` namespace.

**Source scan of the object.**
- **No banned constructs:** no set_option, attribute, `@[...]`, local/scoped, notation, macro, syntax, elab, axiom, sorry, admit, native_decide, implemented_by, extern, unsafe, opaque or #eval.
- **Imports:** only Physlib, Mathlib.LinearAlgebra.ExteriorAlgebra.Basis, Mathlib.LinearAlgebra.CliffordAlgebra.Contraction and V3R1T4SSpec.

**(c) Negative control.** panel_work/criterion/negctl/NullSurjective.lean gives the name `V3R1T4S.claim` to Physlib's already-known surjectivity. The provided checker rejects it (log: panel_work/criterion/negctl/negctl_run.log; temp path elided):
```
spec compile: exit 0
candidate compile: exit 0
check file: exit 1
<checker tmp dir>/Check.lean:4:40: error: Type mismatch
  V3R1T4S.claim
has type
  Function.Surjective ⇑spaceTime.γ.ofCliffordAlgebra
but is expected to have type
  V3R1T4S.spec
problem: V3R1T4S.claim does not prove V3R1T4S.spec
FAIL
```
So the checker discriminates, and the half that was already known does not pass.

## 3. Genuine and non-subsumed?

**Null models do not apply.** This is a deterministic, kernel-checked proof of a closed proposition. There is no sampling, benchmark or success rate to compare against a baseline. Two checks play the analogous role:
- **Non-vacuity:** the domain has dimension 16 (`KF.finrank_cl`), so injectivity is a real statement.
- **Discrimination:** the negative control above gives `FAIL`.

**Not subsumed.**
- **Physlib:** be0f21e5 (`git log -1` gives `2026-10-14T05:36:42+00:00 feat(Space/Norm): remove nonzero hypothesis from normPowerSeries_tendsto (#1788)`) is about 40 minutes older than the 06:16:28Z status fetch, whose page is identical. Physlib has only `ofCliffordAlgebra_surjective`. A grep over Physlib finds no injectivity lemma or AlgEquiv for this map, and the TODO is still open.
- **Mathlib:** the CliffordAlgebra folder has no simplicity or injectivity theorem that would make this a one-liner.
- **The proof does real work.** It counts dimensions on both sides:
  - Clifford side: dimension 16, from `CliffordAlgebra.equivExterior` and `Module.Basis.ExteriorAlgebra`.
  - Dirac side: at least 16, by showing the 16 monomials' images are linearly independent over ℝ, after the algebra automorphism `toChiral`.
- **Not checked:** upstream master after the 06:16:28Z fetch, because I stayed off the network.

**Exact-arithmetic sanity check.** panel_work/criterion/dim_crosscheck.py (log: panel_work/criterion/dim_crosscheck.log) printed:
```
monomials: 16  real rank of their span: 16
span closed under multiplication (products are +/- monomials): True
```
This agrees with `finrank ℝ diracAlgebra = 16`, which the probe also derives in Lean (`criterion_finrank_dirac`).

## 4. Verdict

The result meets the full success criterion as CLAIM.md writes it. It is not a partial win, and the source lists none. It settles the injectivity half of the Physlib TODO directly. The "construct the full isomorphism" half is covered only as a one-line corollary that the panel checked; it is not a declaration in the object, and the scope below says so.

confirmed_scope: Against Physlib commit be0f21e5002d6d73b87f2055530c1e8bf7151546 (Lean 4 v4.34.1), object/OfCliffordAlgebraInjective.lean is a kernel-checked, sorry-free proof, depending only on propext, Classical.choice and Quot.sound, of the frozen statement `Function.Injective spaceTime.γ.ofCliffordAlgebra` for Physlib's own unmodified `ofCliffordAlgebra : CliffordAlgebra diracForm →ₐ[ℝ] diracAlgebra`, from which, with Physlib's `ofCliffordAlgebra_surjective`, the ℝ-algebra isomorphism `CliffordAlgebra diracForm ≃ₐ[ℝ] diracAlgebra` follows by a one-line `AlgEquiv.ofBijective` that the panel compiled separately with the same three axioms and that the object itself does not state.

pass: true
