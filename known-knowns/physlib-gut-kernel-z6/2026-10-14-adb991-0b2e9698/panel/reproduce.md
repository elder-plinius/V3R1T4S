# REPRODUCE skeptic verdict: physlib-gut-kernel-z6 (GeorgiGlashow.inclSM_ker)

context: subagent (fresh Agent-tool context; saw only claim/)

(Saved by the run's main session from the skeptic's final message, verbatim apart from de-indentation; the skeptic
was told to return its verdict as text. Its scratch work is in runs/2026-10-14-0616/panel_work/reproduce/.)

Scope notes (for honesty):
- Besides claim/, I read only what the instruction allows: Physlib, Mathlib and toolchain sources in the workspace's lean/physlib and the toolchain's LeanChecker.lean.
- I read the two wrapper scripts I was required to run: tools/lean_env.sh and tools/lean_slot.sh.
- I ran one read-only `git log -1` in lean/physlib (07:00:41). It printed `be0f21e5002d6d73b87f2055530c1e8bf7151546`.
- A directory listing of panel_work/ and `ps` output (while I diagnosed slot waits) showed other jobs' folder names and command lines. I opened none of their files.
- All my scratch work is in panel_work/reproduce/.

## 0. Integrity of the saved files

`date -u` = Wed Oct 14 07:00:35 UTC 2026, `sha256sum` run in claim/:
```
0b2e9698935d6a53381d1015fdac67779ff1d6b9761358e79767391d12c1663d  object/InclSMKer.lean
685fe987fb3c56f5bb42c79116e7bb5c4375fef3794a6b67e37aa953f89afcea  checker/spec_inclSM_ker.lean
fe7aaf99a0b13f23a3c232a5a5fbfa8d33750e5f809cc0bf36e3c87ef9a828de  checker/lean_claim_check.py
34f66288e28cd4f26f1d2338bf092acb6dc5cd92ecd54fa2c129e3e567152682  source/status_page_GeorgiGlashow_Basic.lean
```
All four hashes equal the ones stated in CLAIM.md. The hashes were unchanged when I re-ran this at 07:20:19.

At 07:20:31, the local Physlib file Physlib/Particles/BeyondTheStandardModel/GeorgiGlashow/Basic.lean had sha256 34f66288…2682. That is identical to source/status_page_GeorgiGlashow_Basic.lean, so in the local build `inclSM` and `inclSM_ker` are still informal.

At 07:21:02 I checked that the Lean block quoted in CLAIM.md is a verbatim substring of the source copy (source lines 28-49). Result: `True`. Toolchain: `Lean (version 4.34.1, ...)`.

## 1. My own formalisation, written before reading the spec or the object

Definitions, quoted from source/status_page_GeorgiGlashow_Basic.lean:
- `GaugeGroupI`: "The gauge group of the Georgi-Glashow model, i.e., `SU(5)`."
- `inclSM`: "The homomorphism of the Standard Model gauge group into the Georgi-Glashow gauge group, i.e., the group homomorphism `SU(3) × SU(2) × U(1) → SU(5)` taking `(h, g, α)` to `blockdiag (α ^ 3 g, α ^ (-2) h)`."
- `inclSM_ker`: "The kernel of the map `inclSM` is equal to the subgroup `StandardModel.gaugeGroupℤ₆SubGroup`."

Physlib definitions (Physlib/Particles/StandardModel/Basic.lean):
- `abbrev GaugeGroupI : Type := specialUnitaryGroup (Fin 3) ℂ × specialUnitaryGroup (Fin 2) ℂ × unitary ℂ`
- `gaugeGroupℤ₆SubGroup := gaugeGroupℤ₆Hom.range`. Its docstring: "the ℤ₆-subgroup of `GaugeGroupI` with elements `(α^2 * I₃, α^(-3) * I₂, α)`, where `α` is a sixth complex root of unity". The three components are `scalar (Fin 3) (z ^ 2)`, `scalar (Fin 2) (star ((u ^ 3 : unitary ℂ) : ℂ))` and `u`.

My formalisation is panel_work/reproduce/RepStatement.lean (written 07:02; I first opened the spec at 07:03:26 and the object at 07:03:48). It uses an explicit `Matrix.of` with index arithmetic:
```lean
noncomputable def myMat (x : StandardModel.GaugeGroupI) : Matrix (Fin 5) (Fin 5) ℂ :=
  Matrix.of fun i j =>
    if hi : i.val < 2 then
      (if hj : j.val < 2 then ((x.2.2 : ℂ) ^ (3 : ℕ)) * (x.2.1 : Matrix (Fin 2) (Fin 2) ℂ) ⟨i.val, hi⟩ ⟨j.val, hj⟩ else 0)
    else
      (if hj : j.val < 2 then 0
       else ((x.2.2 : ℂ) ^ (-2 : ℤ)) * (x.1 : Matrix (Fin 3) (Fin 3) ℂ) ⟨i.val - 2, _⟩ ⟨j.val - 2, _⟩)
def MyStatement : Prop := ∃ φ : StandardModel.GaugeGroupI →* Matrix.specialUnitaryGroup (Fin 5) ℂ,
    (∀ x, (φ x : Matrix (Fin 5) (Fin 5) ℂ) = myMat x) ∧ φ.ker = StandardModel.gaugeGroupℤ₆SubGroup
def MyKernelStatement : Prop := ∀ x, myMat x = 1 ↔ x ∈ StandardModel.gaugeGroupℤ₆SubGroup
```
It typechecked at 07:02:25 → 07:03:22 with no messages and exit=0.

Numerical sanity check: panel_work/reproduce/numcheck.py, written from the docstrings only, with a fixed seed. Run at 07:01:48 (output in panel_work/reproduce/numcheck.out):
```
[1] 2000 random pairs: values in SU(5), multiplicative, none in kernel
[2] k=1 alpha=0.5000+0.8660j: alpha^2=-0.5000+0.8660j conj(alpha)^3=-1.0000-0.0000j -> ||incl - I5|| = 3.17e-17
    (k=0..5 all give ||incl - I5|| <= 6.33e-16)
[3] circle grid of 36000 points: admissible alpha angles (deg) = [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]
[4] 1000 random alpha with alpha^6 != 1: a^2 I3 never in SU(3)
FAILURES: 0
NUMCHECK OK
```
A second run was byte-identical (`IDENTICAL`). The numbers are only a sanity check. The pass below rests on the kernel-checked proof.

## 2. My own compile of spec and object, and deriving my statement

I compiled byte-identical copies (same sha256) in panel_work/reproduce/build/, using `lake env sh -c 'LEAN_PATH="<build>:$LEAN_PATH" exec lean --root=<build> -o …'` through the slot gate:
- 07:05:03 → 07:05:36: `spec exit=0`. build/spec_compile.log is empty: no messages.
- 07:05:46 → 07:06:10: `claim exit=0`. build/claim_compile.log is empty: no warnings and no `declaration uses 'sorry'`.

panel_work/reproduce/build/RepDerive.lean imports RepStatement, V3R1T4SSpec and V3R1T4SClaim. It proves two things:
- `myMat x = V3R1T4S.inclSMMatrix x` in two independent ways. v1 checks all 25 entries on literal indices by `rfl`. v2 splits structurally on `finSumFinEquiv` (Sum.inl/inr) and uses `fromBlocks_apply₁₁/₁₂/₂₁/₂₂`.
- `spec_iff_mine : V3R1T4S.spec ↔ MyStatement`, `my_statement`, `my_kernel_statement`, and an explicit kernel description `my_kernel_explicit`: `myMat x = 1 ↔ ∃ a, a^6 = 1 ∧ h = a^2•1 ∧ g = a⁻¹^3•1 ∧ α = a`.

My first attempt (07:07:04) failed only inside my own bridge code: `zpow_neg` was ambiguous under `open Matrix`, and I used a wrong lemma name. The final run, 07:18:58 → 07:19:27, gave `RepDerive exit=0`. Its only messages are linter and deprecation warnings in my own file.
```
'V3R1T4S.claim' depends on axioms: [propext, Classical.choice, Quot.sound]
'RepCheck.myMat_eq_spec_v1' depends on axioms: [propext, Classical.choice, Quot.sound]
'RepCheck.myMat_eq_spec_v2' depends on axioms: [propext, Classical.choice, Quot.sound]
'RepCheck.spec_iff_mine' depends on axioms: [propext, Classical.choice, Quot.sound]
'RepCheck.my_statement' depends on axioms: [propext, Classical.choice, Quot.sound]
'RepCheck.my_kernel_statement' depends on axioms: [propext, Classical.choice, Quot.sound]
'RepCheck.my_kernel_explicit' depends on axioms: [propext, Classical.choice, Quot.sound]
```
The `rfl`/`congr` bridge succeeded against my explicitly typed exponents (`(3 : ℕ)`, `(-2 : ℤ)`). So the spec's `^ 3` and `⁻¹ ^ 2` are the ordinary monoid powers, not `cpow`.

Kernel replay of the object's compiled module (log in build/leanchecker_claim.log). I ran `leanchecker -v V3R1T4SClaim` through the slot gate; it waited for a slot from 07:15:44:
```
replaying V3R1T4SClaim
leanchecker exit=0
Wed Oct 14 07:18:48 UTC 2026
```

Does the frozen spec say what the docstrings say? Yes.
- `GaugeGroupGG` is `Matrix.specialUnitaryGroup (Fin 5) ℂ`, which is SU(5).
- The domain is Physlib's `StandardModel.GaugeGroupI`: SU(3) × SU(2) × U(1) in that order, so `x.1 = h`, `x.2.1 = g`, `x.2.2 = α`.
- `inclSMMatrix` equals my independent blockdiag(α³g on indices 0,1; α⁻²h on indices 2,3,4). This is kernel-proved above.
- `f.ker = gaugeGroupℤ₆SubGroup` is exactly the `inclSM_ker` sentence.
- The `∃ f` is not a weakening. The value condition `∀ x, ↑(f x) = inclSMMatrix x` fixes f uniquely (Subtype.ext and MonoidHom.ext), so the spec is equivalent to "the hom inclSM exists and its kernel is ℤ₆". `spec_iff_mine` confirms this.
- Block order does not affect the kernel in any case.

## 3. The provided checker, run exactly as REPRODUCE.md says

The command, with `<workspace>` standing for the workspace root:
```
. <workspace>/tools/lean_env.sh; export ELAN_NO_OVERRIDE_NOTICE=1; cd claim
sh <workspace>/tools/lean_slot.sh python3 -I checker/lean_claim_check.py --physlib <workspace>/lean/physlib \
  --spec checker/spec_inclSM_ker.lean --candidate object/InclSMKer.lean
```
Run 1, 07:11:31 → 07:12:12, exit 0 (panel_work/reproduce/checker_run.log):
```
spec compile: exit 0
candidate compile: exit 0
check file: exit 0
'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]
axioms: ['Classical.choice', 'Quot.sound', 'propext']
PASS
```
Run 2, 07:19:36 → 07:20:19, exit 0 (panel_work/reproduce/checker_run2.log): the same output. `cmp` printed `RUN1 == RUN2 (byte-identical)`. There is no non-determinism.

## 4. Referee audit of object/InclSMKer.lean

Source scan (07:12:46): I grepped for axiom, sorry, admit, macro, notation, syntax, elab, instance, attribute, `@[`, set_option, native_decide, implemented_by, extern, unsafe, opaque, partial, #eval, #exit, run_cmd, initialize, export, infix, prefix, postfix, local, scoped, private, `open … in`, decide, ofReduceBool, Lean./Meta./Elab., debug, trust, skipKernel, addDecl and Classical. Result: `(no matches)`.
- There are no string literals.
- There are no control, bidi or zero-width characters. Only ordinary math Unicode appears (ℂ, ℤ, ₆, α, ρ, ⁻¹, ⟨⟩ …).
- Declarations: `open Matrix`, `namespace V3R1T4S.KF`, ten `lemma`s, one `noncomputable def inclSMHom`, and `theorem V3R1T4S.claim : V3R1T4S.spec := ⟨inclSMHom, fun _ => rfl, ker_eq⟩`.

Checker weak points (none of them used here):
- The regex policy would not catch `@[default_instance]` (because of the word boundary) or code hidden after `--` inside a string.
- The checker trusts imported .olean files.

Both are covered here: the object has no attributes and no strings, I compiled it myself from the source, and leanchecker replayed it.

Re-derivation of the proof. Let x = (h, g, α), a = (α:ℂ). Since α is unitary, a·ā = 1, so a ≠ 0 and a⁻¹ = ā.
- **Membership in SU(5), unitary part.** M·M* = reindex(fromBlocks((a³g)(a³g)*, 0, 0, (a⁻²h)(a⁻²h)*)). The first block is (a·ā)³·gg* = 1. The second is (ā·a)²·hh* = 1, using a⁻¹ = ā. So M·M* = reindex(fromBlocks 1 0 0 1) = 1. The object uses `mem_unitaryGroup_iff` (M·star M = 1) and `smul_mul_smul_comm`, `scal_inv`, `← mul_pow`, `fromBlocks_one` and `submatrix_one_equiv`. This is correct.
- **Membership in SU(5), determinant.** det M = det(fromBlocks A 0 0 D) = det A · det D (`det_reindex_self`, `det_fromBlocks_zero₂₁`). det A = (a³)²·det g = a⁶ and det D = (a⁻¹)⁶·det h = a⁻⁶ (`det_smul`, with card Fin 2 = 2 and card Fin 3 = 3). Their product is 1 (`field_simp` with a ≠ 0). This is correct.
- **Multiplicativity.** (xy) = (hh′, gg′, αα′). Block multiplication with zero off-diagonal blocks (`fromBlocks_multiply`, `submatrix_mul_equiv`) gives blocks (a³a′³)gg′ = (aa′)³gg′ and (a⁻¹)²(a′⁻¹)²hh′ = ((aa′)⁻¹)²hh′ (`mul_pow`, `mul_inv`). Also M(1) = 1. This is correct.
- **Kernel criterion.** M = 1 ⟺ a³g = 1 ∧ a⁻²h = 1. This holds because reindex is an equivalence, together with `fromBlocks_inj` and `fromBlocks_one`. This is correct.
- **ker ⊆ ℤ₆.** Taking determinants of a³g = 1 gives a⁶·det g = a⁶ = 1. That is the α⁶ = 1 step, and it holds because det g = 1. Then ρ := mkOfPowEq a is a sixth root of unity with ↑ρ = a. From a⁻²h = 1 we get h = a²·1 = gaugeGroupℤ₆SU3OfRoot ρ. From a³g = 1 we get g = ā³·1 = gaugeGroupℤ₆SU2OfRoot ρ (Physlib's `star ρ ^ 3 • 1`). The U(1) component is ρ = α. This is correct.
- **ℤ₆ ⊆ ker.** For x = (ρ²·1, ρ̄³·1, ρ): a³·ρ̄³ = (ρρ̄)³ = 1 and (ρ⁻¹)²·ρ² = 1. This is correct.

The numerical check agrees: exactly the six α at 0°, 60°, …, 300° are admissible, and all six give the identity matrix.

Nits (they do not change the verdict):
- CLAIM.md line 24 says the source copy is "saved in `data/status_page_GeorgiGlashow_Basic.lean`". It actually lives in source/, as line 16 of the same file correctly states, with the matching hash.
- CLAIM.md gives "lines 28-50"; the block is lines 28-49 (line 50 is blank).

Incident: my own `leanchecker --help` call was taken by leanchecker as "check the whole project". Inside a slot it reached about 9.6 GB for about 2 minutes before I killed it (07:15:15). It had no effect on any result above.

## Verdict
- Every saved object is present and its hash matches.
- Spec and object compile cleanly. I did this myself and via the checker, twice, with identical output.
- `V3R1T4S.claim` implies my independently written statement, and my statement is equivalent to the frozen spec. All of it depends only on propext, Classical.choice and Quot.sound.
- The kernel replay of the object passes.
- The frozen spec faithfully formalises the `GaugeGroupI`, `inclSM` and `inclSM_ker` docstrings.
- Every proof step re-derives correctly.

pass: true
