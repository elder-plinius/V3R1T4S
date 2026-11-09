# REPRODUCE skeptic verdict: physlib-clifford-dirac-iso

context: subagent (fresh Agent-tool context; saw only claim/)
scope note: outside claim/ I read only what the brief allows. That is the built Physlib/Mathlib sources and the toolchain: Physlib/Relativity/CliffordAlgebra.lean, Physlib/Relativity/Fermions/Dirac/Basic.lean and GammaMatrices.lean, the toolchain's src/lean/LeanChecker.lean, physlib's .git/HEAD and lake-manifest.json. I also read the two wrapper scripts every Lean call had to go through (tools/lean_env.sh sets env vars; tools/lean_slot.sh does flock + nice and passes the exit code through). I did not read attempts/, notes, reports, briefs or other runs. WS below means the workspace root.

(Saved by the run's main session from the skeptic's final message, verbatim apart from de-indentation; the skeptic
was told to return its verdict as text. Its scratch work is in runs/2026-10-14-0615/panel_work/reproduce/.)

## 0. Inputs (hashed 07:03:35 UTC; re-hashed unchanged 07:28:39 UTC)
Every sha256 matches CLAIM.md:
- object/OfCliffordAlgebraInjective.lean: 13837a7e226a97b9fef5bd04d6f362c0db869627cfa3a7239d4f54343cde5c8b
- checker/spec_ofCliffordAlgebra_injective.lean: e57fc5fa63bde2b1b045dde255be28fd07f26d7fd1da9a7845011f0dbd1b37e8
- checker/lean_claim_check.py: fe7aaf99a0b13f23a3c232a5a5fbfa8d33750e5f809cc0bf36e3c87ef9a828de
- source/status_page_CliffordAlgebra.lean: 70ca93d773d8a8f2c2fe43e607125ae1d3042d7530bace4371cd5eba5bf8de0d. This is byte-identical (`cmp`, 07:00:44 UTC) to Physlib/Relativity/CliffordAlgebra.lean in the local build.

Other provenance checks:
- Physlib .git/HEAD is `be0f21e5002d6d73b87f2055530c1e8bf7151546`.
- `lean --version` (07:01:57 UTC) gives `Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)`.
- The Mathlib checkout HEAD is d13f23b723b8a846827a245b89c10fc7d3f11612, which equals the lake-manifest pin.

## 1. Definitions, TODO, and my own statement (written before opening the object or spec)
From source/status_page_CliffordAlgebra.lean:
- l.34: `- Complete the isomorphism by proving injectivity of `ofCliffordAlgebra` (requires dimension theory)`
- l.40: `TODO "Prove injectivity of ofCliffordAlgebra and construct the full isomorphism."`
- l.111-112: `def γSet : Set (Matrix (Fin 4) (Fin 4) ℂ) := {endEquivMatrix (gamma i) | i : Fin 1 ⊕ Fin 3}`
- l.117-118: `def diracAlgebra : Subalgebra ℝ (Matrix (Fin 4) (Fin 4) ℂ) := Algebra.adjoin ℝ γSet`
- l.128-132: `def diracForm : QuadraticForm ℝ (Fin 4 → ℝ) := QuadraticMap.sq.comp (LinearMap.proj 0) - QuadraticMap.sq.comp (LinearMap.proj 1) - QuadraticMap.sq.comp (LinearMap.proj 2) - QuadraticMap.sq.comp (LinearMap.proj 3)`
- l.136-139: `def ofCliffordAlgebra : CliffordAlgebra diracForm →ₐ[ℝ] diracAlgebra := CliffordAlgebra.lift _ ⟨∑ i, (LinearMap.proj i).smulRight ⟨endEquivMatrix (gamma (finSumFinEquiv.symm i)), γ_in_diracAlgebra _⟩, fun v => by ... module⟩`

My statements are in panel_work/reproduce/ReproStmt.lean. I wrote the file at 07:01 UTC and compiled it 07:03:11→07:03:30 UTC (exit 0) as module ReproStmt, importing only Physlib.Relativity.CliffordAlgebra, so nothing from the object can affect how they elaborate:
- StmtA := `Function.Injective (spaceTime.γ.ofCliffordAlgebra : CliffordAlgebra spaceTime.γ.diracForm → spaceTime.γ.diracAlgebra)`
- StmtB := `∀ x y, ofCliffordAlgebra x = ofCliffordAlgebra y → x = y`
- StmtC := `∀ x, ((ofCliffordAlgebra x : diracAlgebra) : Matrix (Fin 4) (Fin 4) ℂ) = 0 → x = 0`
- StmtD := `∃ e : CliffordAlgebra diracForm ≃ₐ[ℝ] diracAlgebra, ∀ x, e x = ofCliffordAlgebra x` (the TODO's full isomorphism)

The `#print` output of that compile, taken from the built oleans, matches the source text:
```
def spaceTime.γ.diracForm : QuadraticForm ℝ (Fin 4 → ℝ) :=
QuadraticMap.sq.comp (LinearMap.proj 0) - QuadraticMap.sq.comp (LinearMap.proj 1) -
    QuadraticMap.sq.comp (LinearMap.proj 2) -
  QuadraticMap.sq.comp (LinearMap.proj 3)
def spaceTime.γ.diracAlgebra : Subalgebra ℝ (Matrix (Fin 4) (Fin 4) ℂ) :=
Algebra.adjoin ℝ spaceTime.γ.γSet
def spaceTime.γ.γSet : Set (Matrix (Fin 4) (Fin 4) ℂ) :=
{x | ∃ i, Fermion.Dirac.endEquivMatrix (Fermion.Dirac.gamma i) = x}
def spaceTime.γ.ofCliffordAlgebra : CliffordAlgebra spaceTime.γ.diracForm →ₐ[ℝ] ↥spaceTime.γ.diracAlgebra :=
(CliffordAlgebra.lift spaceTime.γ.diracForm)
  ⟨∑ i, (LinearMap.proj i).smulRight ⟨Fermion.Dirac.endEquivMatrix (Fermion.Dirac.gamma (finSumFinEquiv.symm i)), ⋯⟩, ⋯⟩
```

I read the frozen spec only after that (07:03:35). It is `import Physlib` followed by `def V3R1T4S.spec : Prop := Function.Injective spaceTime.γ.ofCliffordAlgebra`. This is exactly the TODO's injectivity, and it is definitionally my StmtA: `theorem spec_iff_A : V3R1T4S.spec ↔ StmtA := Iff.rfl` type-checks.

The TODO's second half (the AlgEquiv) is not in the spec. It follows in one line from the claim plus Physlib's surjectivity; my repro_D builds it below.

## 2. My own compile and check
Each Lean call ran as `. $WS/tools/lean_env.sh; export ELAN_NO_OVERRIDE_NOTICE=1; cd $WS/lean/physlib && sh $WS/tools/lean_slot.sh lake env sh -c "LEAN_PATH=$B:$LEAN_PATH; export LEAN_PATH; exec lean --root=$B -o $B/<M>.olean $B/<M>.lean"`, with B = panel_work/reproduce/build. M was V3R1T4SSpec (a copy of the frozen spec) and then V3R1T4SClaim (a copy of the object, same sha256).
- 07:04:25→07:05:25 UTC: spec compile exit 0, no messages.
- 07:05:30→07:06:11 UTC: object compile exit 0. There were only three linter warnings: `V3R1T4SClaim.lean:34:2: warning: Try this: haveI̵ ... The goal is a proposition, so `have` is preferred over `haveI`.`, and at 109:33 and 109:51 `This simp argument is unused: Matrix.mul_apply` / `Fin.sum_univ_four`. There was no error and no "declaration uses 'sorry'".
- 07:07:11→07:07:53 UTC: panel_work/reproduce/ReproCheck.lean, which imports ReproStmt and V3R1T4SClaim, exit 0. It contains `theorem repro_A : StmtA := V3R1T4S.claim`, plus B, C and D proved from the claim, and `clifford_nontrivial : (1 : CliffordAlgebra diracForm) ≠ 0` to show the statement is not vacuous. Output:
```
V3R1T4S.claim : V3R1T4S.spec
def V3R1T4S.spec : Prop :=
Function.Injective ⇑spaceTime.γ.ofCliffordAlgebra
'V3R1T4S.claim' depends on axioms: [propext, Classical.choice, Quot.sound]
'ReproSkeptic.repro_A' depends on axioms: [propext, Classical.choice, Quot.sound]
'ReproSkeptic.repro_B' depends on axioms: [propext, Classical.choice, Quot.sound]
'ReproSkeptic.repro_C' depends on axioms: [propext, Classical.choice, Quot.sound]
'ReproSkeptic.repro_D' depends on axioms: [propext, Classical.choice, Quot.sound]
'ReproSkeptic.spec_iff_A' depends on axioms: [propext, Classical.choice, Quot.sound]
'ReproSkeptic.clifford_nontrivial' depends on axioms: [propext, Classical.choice, Quot.sound]
```
The only other messages were two unused-variable lints in my own repro_B.

## 3. Provided checker, run exactly as REPRODUCE.md says
From claim/, after `. $WS/tools/lean_env.sh; export ELAN_NO_OVERRIDE_NOTICE=1`:
`sh $WS/tools/lean_slot.sh python3 -I checker/lean_claim_check.py --physlib $WS/lean/physlib --spec checker/spec_ofCliffordAlgebra_injective.lean --candidate object/OfCliffordAlgebraInjective.lean`

Run 1 (panel_work/reproduce/log_provided_checker.txt):
```
Wed Oct 14 07:08:14 UTC 2026
spec compile: exit 0
candidate compile: exit 0
check file: exit 0
'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]
axioms: ['Classical.choice', 'Quot.sound', 'propext']
PASS
checker exit=0
Wed Oct 14 07:09:15 UTC 2026
```
Run 2 (07:15:04→07:16:17 UTC, panel_work/reproduce/log_provided_checker_run2.txt) produced identical lines; the diff is empty except for the dates. The last line is again `PASS`.

## 4. Audit of the object and re-derivation
**Source audit.** I grepped the full text at 07:04:17 UTC and then read it in full.
- Imports: Physlib, Mathlib.LinearAlgebra.ExteriorAlgebra.Basis, Mathlib.LinearAlgebra.CliffordAlgebra.Contraction, V3R1T4SSpec.
- The only scoping command is `open spaceTime spaceTime.γ Fermion.Dirac`.
- None of the following appear: set_option, instance, attribute, macro/syntax/notation, axiom, sorry/admit, native_decide, implemented_by/extern, unsafe, opaque, #eval/run_cmd/elab.
- `V3R1T4S.spec` is not redefined. The last line is `theorem V3R1T4S.claim : V3R1T4S.spec := KF.injective_ofCliffordAlgebra`.

**Olean contents.** panel_work/reproduce/OleanDump.lean writes panel_work/reproduce/dump_build1.txt. The object's olean has 43 constants: the KF.* defs and theorems, V3R1T4S.claim, and private match-equation lemmas plus a splitter that Lean generated for a match in Fermion.Dirac.gammaMatrix_basis_toMatrix. There are no axiom constants and no instance-extension entries.

**Kernel replay.** I ran `lake env sh -c "LEAN_PATH=$B:$LEAN_PATH; export LEAN_PATH; exec leanchecker -v V3R1T4SClaim"` from 07:13:53 to 07:14:36 UTC. It exited 0 with the single line `replaying V3R1T4SClaim`. This re-checks all of the module's constants in the kernel, on top of its imports.

**Independent axiom walk.** panel_work/reproduce/AxiomWalk.lean walks types, values, constructors and recursor rules from each target. It does not use `#print axioms` or its cached per-constant data. It ran 07:24:25→07:25:53 UTC, exit 0, where walkA is `theorem walkA : StmtA := V3R1T4S.claim`:
```
V3R1T4S.claim: reached 38449 constants; axioms = [Classical.choice, Quot.sound, propext]; unavailable = []
walkA: reached 38451 constants; axioms = [Classical.choice, Quot.sound, propext]; unavailable = []
spaceTime.γ.ofCliffordAlgebra_surjective: reached 31590 constants; axioms = [Classical.choice, Quot.sound, propext]; unavailable = []
```

**Re-derivation, step by step.**
- (i) dim_ℝ Cl(ℝ⁴, diracForm) = 16. Because 2 is invertible in ℝ, `CliffordAlgebra.equivExterior` is an ℝ-linear isomorphism to Λ(ℝ⁴). Λ(ℝ⁴) has a basis indexed by `Finset (Fin 4)`, with 2⁴ = 16 elements (KF.clBasis, KF.finrank_cl). This is correct. Independently, the 16 ordered monomials span Cl, and (ii) shows their images are independent, so they form a basis.
- (ii) 16 ≤ dim_ℝ diracAlgebra. ofCliffordAlgebra is an algebra hom, and ofCliffordAlgebra_ι_single gives e_i ↦ endEquivMatrix (gamma (finSumFinEquiv.symm i)), so the images of the 16 ordered monomials are the 16 ordered products of the Dirac matrices.
  - The object composes with toChiral, which is conjugation back to the chiral basis. It is an injective ℂ-algebra automorphism, so `LinearIndependent.of_comp` transfers independence back.
  - Its matrices `KF.C` equal Physlib's `gamma_toMatrix` (GammaMatrices.lean l.165-168) entry by entry. I checked this by reading, and the kernel's `rfl` confirms it.
  - It then solves Σ g_k W_k = 0 from the real and imaginary parts of eight entries, using linarith.
  - This is correct. The 16 products are even ℂ-independent: they are the classical basis of M₄(ℂ).
- (iii) Physlib's `ofCliffordAlgebra_surjective` gives dim diracAlgebra ≤ 16. So the dimensions are equal (16 = dim Cl), and a surjective linear map between finite-dimensional spaces of equal dimension is injective by rank–nullity (`LinearMap.injective_iff_surjective_of_finrank_eq_finrank`). This is correct.

**Exact numeric check.** panel_work/reproduce/numeric_check.py uses Fractions only, no floats. It rebuilds the matrices from Physlib's `gamma_toMatrix` and `endEquivMatrix_apply` as D_μ = S·C_μ·S⁻¹. Run at 07:26:16 UTC:
```
gamma0 (Dirac rep) = [1 0 0 0; 0 1 0 0; 0 0 -1 0; 0 0 0 -1]
gamma1 (Dirac rep) = [0 0 0 1; 0 0 1 0; 0 -1 0 0; -1 0 0 0]
gamma2 (Dirac rep) = [0 0 0 -i; 0 0 i 0; 0 i 0 0; -i 0 0 0]
gamma3 (Dirac rep) = [0 0 1 0; 0 0 0 -1; -1 0 0 0; 0 1 0 0]
Clifford relations {g_i,g_j} = 2 eta_ij (eta = diag(1,-1,-1,-1)): True
number of ordered monomials: 16
R-rank of the 16 Dirac-rep products (as vectors in R^32): 16
R-rank of the 16 chiral products W (object's W): 16
R-rank of {A, iA : A among the 16} (=32 iff C-independent): 32
R-dimension of the real algebra generated by gamma0..gamma3: 16
S^-1 * D_i * S == C_i for all i: True
rank of the 16x16 system from the eight entries (16 = nonsingular): 16
```
So diracAlgebra has ℝ-dimension exactly 16, the same as dim Cl. The signature matches diracForm. The eight-entry system used in linInd_W is nonsingular.

## 5. Determinism
- The provided checker gave identical output and `PASS` on both runs.
- I compiled the object three times:
  - build/ at 07:05:30.
  - build2/, 07:16:23→07:21:33 UTC.
  - A same-path rebuild, 07:26:52→07:28:33 UTC. It is bit-identical to build/: sha256 `d68f2f77fe039726322919b7b5d955a9628fddc92b33716fda55bfd1d0a78333` for both, and `cmp` prints `BITWISE IDENTICAL`.
- build2/'s olean differs in 22 bytes. The cause is the embedded source path: 'reproduce/build/' and 'reproduce/build2/' each occur once in their own olean. Its constant dump (43 names, kinds, type/value hashes, extension entry counts) is identical to build/'s (diff empty).
- The compile messages are identical across all three compiles.
- I found no non-determinism.

## 6. Notes (none of them block the result)
- CLAIM.md's success-criterion paragraph says the page copy is "saved in `data/status_page_CliffordAlgebra.lean`". There is no data/ folder in claim/. The copy is source/status_page_CliffordAlgebra.lean, which the status record names correctly and whose hash I verified. This is a wrong path in the prose; the author should fix it.
- The object proves injectivity only and does not declare the AlgEquiv. My repro_D builds it as `AlgEquiv.ofBijective ofCliffordAlgebra ⟨V3R1T4S.claim, ofCliffordAlgebra_surjective⟩`, as CLAIM.md says.
- Trust base: I trusted the local cache-built Physlib/Mathlib oleans at be0f21e. I verified the target file's source and the definitions printed from the oleans. leanchecker ran without --fresh, so upstream oleans were not replayed.
- Memory incident: at 07:11:12 I ran `leanchecker --help`. leanchecker ignores unknown flags (see its source), so this defaulted to replaying all of Physlib. It reached 8.3 GB RSS inside my slot. I killed only my own three processes at 07:13:25 UTC, then ran the correct `leanchecker -v V3R1T4SClaim`.

pass: true
