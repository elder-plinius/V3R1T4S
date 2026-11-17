# Panel: REPRODUCE skeptic — physlib-gut-kernel-z6 (Pati-Salam `inclSM_ker`)

context: subagent (fresh context, Claude Code Agent tool)

Checks run 2026-10-15, about 07:25 to 07:40 UTC.

- **What I read:** only `claim/` (CLAIM.md, REPRODUCE.md, MACHINE_NOTE.md, checker/, object/, source/) and the local Physlib/Mathlib sources. I read nothing else in the run folder or workspace.
- **Lean processes:** every Lean/Lake invocation went through `tools/lean_slot.sh`. I killed no processes.
- **Scratch files:** `../panel_work/reproduce/` (relative to `claim/`).

**Physlib commit checked against: 76245c854e4827a1dd7f20d1c053b61219cc8fbb.** This is not be0f21e5, which is not on this machine (see MACHINE_NOTE.md).
- I read the commit without running git: the checkout's `.git/refs/heads/master` points to it, and `.git/shallow` lists only this commit.
- Toolchain: `Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)` and `Lake version 5.0.0-src+5045d00 (Lean version 4.34.1)`.
- Mathlib: d13f23b723b8a846827a245b89c10fc7d3f11612 (inputRev v4.34.1), as pinned by the 76245c85 lake-manifest.json. The Mathlib checkout's HEAD is the same commit.

## 1. Package integrity

```
6285d360e0d0a5a396fb3a5461d732888f314b08dcef13c1eda2bcd63aa3a5bd  object/PatiSalamInclSMKer.lean
ed68095509a7bbdffd578df7ccfba3bfde49cbeb8f5173a65dc62123f24db278  checker/spec_patisalam_inclSM_ker.lean
fe7aaf99a0b13f23a3c232a5a5fbfa8d33750e5f809cc0bf36e3c87ef9a828de  checker/lean_claim_check.py
060aeb499b68cd6b526f4b746f18cf44e65abc6e97ce5ef2a9866b0e2ed627d9  source/status_page_PatiSalam_Basic.lean
```

- All four hashes equal the ones in CLAIM.md.
- `source/status_page_PatiSalam_Basic.lean` is byte-identical (`cmp`) to Physlib's `Physlib/Particles/BeyondTheStandardModel/PatiSalam/Basic.lean` at 76245c85.
- For the record, Physlib's `Physlib/Particles/StandardModel/Basic.lean` at 76245c85 has sha256 `9950098dd0c6dc6a02d0023859c78c359b38e1417dbbcc16ada7197454bc199a`. CLAIM.md gives no hash for this file, so there is nothing to compare it with.

## 2. The definition and what must be true (written before reading the object)

### Quoted informal definitions

The docstrings below are quoted verbatim from Physlib `PatiSalam/Basic.lean` (identical to the file in `source/`). Reference links are omitted.

- **`GaugeGroupI` (tag 6V2Q2):** "The gauge group of the Pati-Salam model (unquotiented by ℤ₂), i.e., `SU(4) × SU(2) × SU(2)`."
- **`inclSM` (tag 6V2RH):** "The homomorphism of the Standard Model gauge group into the Pati-Salam gauge group, i.e., the group homomorphism `SU(3) × SU(2) × U(1) → SU(4) × SU(2) × SU(2)` taking `(h, g, α)` to `(blockdiag (α h, α ^ (-3)), g, diag (α ^ 3, α ^(-3))`." Its deps are `GaugeGroupI` and `StandardModel.GaugeGroupI`.
- **`inclSM_ker` (tag 6V2RQ):** "The kernel of the map `inclSM` is equal to the subgroup `StandardModel.gaugeGroupℤ₃SubGroup`."

### Formal Physlib definitions

These are verbatim from Physlib `Particles/StandardModel/Basic.lean` at 76245c85:

```lean
abbrev GaugeGroupI : Type :=
  specialUnitaryGroup (Fin 3) ℂ × specialUnitaryGroup (Fin 2) ℂ × unitary ℂ
noncomputable def gaugeGroupℤ₃RootToℤ₆Root : rootsOfUnity 3 ℂ →* rootsOfUnity 6 ℂ :=
  Subgroup.inclusion (rootsOfUnity_le_of_dvd (by norm_num : 3 ∣ 6))
noncomputable def gaugeGroupℤ₃Hom : rootsOfUnity 3 ℂ →* GaugeGroupI :=
  gaugeGroupℤ₆Hom.comp gaugeGroupℤ₃RootToℤ₆Root
noncomputable def gaugeGroupℤ₃SubGroup : Subgroup GaugeGroupI :=
  gaugeGroupℤ₃Hom.range
```

How the ℤ₆ map is built:
- `gaugeGroupℤ₆Hom` sends α to `(gaugeGroupℤ₆SU3OfRoot α, gaugeGroupℤ₆SU2OfRoot α, gaugeGroupℤ₆UnitaryOfRoot α)`.
- The three parts are `scalar (Fin 3) (z ^ 2)`, `scalar (Fin 2) (star ((u ^ 3 : unitary ℂ) : ℂ))` and `u`, where z is α as a complex number and u is z as a unitary.
- Physlib's own lemmas state this: `gaugeGroupℤ₆SU3OfRoot_eq_mul_id` and `gaugeGroupℤ₆SU2OfRoot_eq_mul_id`.

So for z³ = 1 the elements are (z²I₃, star(z³)I₂, z) = (z²I₃, I₂, z).

### What must be true

Write Φ(h, g, α) = (blockdiag(αh, α⁻³), g, diag(α³, α⁻³)) on SU(3) × SU(2) × U(1).

- **(T1) Φ lands in SU(4) × SU(2) × SU(2).** Because |α| = 1, the blocks αh, α⁻³ and α³ are unitary. Also det blockdiag(αh, α⁻³) = α³·det h·α⁻³ = 1, and det diag(α³, α⁻³) = 1.
- **(T2) Φ is a group homomorphism.** Scalars commute with matrices, and U(1) is abelian.
- **(T3) The kernel.** Φ(h, g, α) = 1 holds exactly when g = I₂, α³ = 1 (which gives α⁻³ = 1) and αh = I₃, that is h = α⁻¹I₃ = α²I₃.
  - So ker Φ = {(α²I₃, I₂, α) : α³ = 1}.
  - This is exactly Physlib's set above, so the informal lemma is true.

## 3. Does the frozen statement say exactly that?

### What the spec defines

`checker/spec_patisalam_inclSM_ker.lean` imports only Physlib and defines:
- `GaugeGroupPS = SU(4) × SU(2) × SU(2)`, using `Matrix.specialUnitaryGroup`, which is `unitaryGroup ⊓ MonoidHom.mker detMonoidHom`.
- `psMatrix4 x = reindex finSumFinEquiv finSumFinEquiv (fromBlocks (α • h) 0 0 (α⁻¹ ^ 3 • 1₁))`.
- `psMatrixR x = diagonal ![α ^ 3, α⁻¹ ^ 3]`.
- `spec := ∃ f : StandardModel.GaugeGroupI →* GaugeGroupPS, (∀ x, components = psMatrix4 x, x.2.1, psMatrixR x) ∧ f.ker = StandardModel.gaugeGroupℤ₃SubGroup`.

### Mathlib definitions checked in source

- `finSumFinEquiv` sends `inl i ↦ i` and `inr j ↦ 3 + j`.
- `reindex e e M = M.submatrix e.symm e.symm`.
- `MonoidHom.ker f = {x | f x = 1}`.

The three components determine f completely, so the `∃` is not a loophole: the spec holds exactly when T1, T2 and T3 hold.

### Machine-checked sanity lemmas

These are in my file `ReproSanity.lean`, which imports only the compiled spec; the full text is in Appendix A.
- **Four block lemmas:**
  - `psMatrix4 x i.castSucc j.castSucc = α * h i j`
  - `psMatrix4 x i.castSucc (Fin.last 3) = 0`
  - `psMatrix4 x (Fin.last 3) j.castSucc = 0`
  - `psMatrix4 x (Fin.last 3) (Fin.last 3) = α ^ (-3 : ℤ)`
- **One explicit index formula, `ps4_explicit`:** α h on indices 0, 1, 2; α⁻³ at index 3; zero elsewhere.
- **`psR_explicit`:** `psMatrixR x = !![α ^ 3, 0; 0, α ^ (-3 : ℤ)]`.
- **`mem_Z3_iff`:** `g ∈ StandardModel.gaugeGroupℤ₃SubGroup ↔ ∃ ω : ℂ, ω ^ 3 = 1 ∧ g.1 = ω ^ 2 • 1 ∧ g.2.1 = 1 ∧ g.2.2 = ω`.

Output (exit 0, nothing else printed):

```
'ReproSanity.ps4_explicit' depends on axioms: [propext, Classical.choice, Quot.sound]
'ReproSanity.psR_explicit' depends on axioms: [propext, Classical.choice, Quot.sound]
'ReproSanity.mem_Z3_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
```

**Verdict on the statement:** it formalizes the informal lemma faithfully. `inclSM` is exactly as its docstring says, and the kernel is required to equal Physlib's own subgroup. No mismatch.

## 4. My own checks (all written before reading the object)

### 4a. Numeric sanity check

I used numpy with a fixed seed. This is a spot check and is not part of the basis for passing (the claim is a proof, not an exhaustive search).

```
T1 (image in SU(4)xSU(2)xSU(2)) on 2000 samples: True
T2 (homomorphism) on 1000 pairs: True | identity -> identity: True
Z3 elements (z^2 I3, conj(z^3) I2, z), z^3=1, lie in SU(3)xSU(2)xU(1): True
Z3 elements map to identity: True
Z6 \ Z3 elements do NOT map to identity: True
min distance of incl(random x) from identity: 0.8244
on a 3001-point circle of (w^2 I3, I2, w): kernel hits at w = exp(2 pi i k/3), k in [0, 1, 2]
NUMERIC SANITY: OK
```

- Repeated runs give identical output (md5 d0856c38738c2f6ab98206f2c82a1d86).
- My first run printed MISMATCH because of a bug in my own script: the angle 2π was counted as k = 3 instead of 0 mod 3. After that fix it printed OK.

### 4b. An independent Lean proof of `V3R1T4S.spec`

The file is `ReproIndep.lean` (full text in Appendix B). It imports only the compiled frozen statement.

- It builds its own homomorphism F = (blockdiag, g, diag).
- **Image lands in the special unitary groups.** Unitarity comes from `fromBlocks_conjTranspose`, `fromBlocks_multiply` and `submatrix_mul_equiv`. The determinant comes from `det_fromBlocks_zero₂₁` and `det_smul`.
- **Multiplicativity** is proved block by block.
- **Kernel ⊆ subgroup:** α³ = 1 comes from the (0,0) entry of the diag component. Then h = α²·1 comes from the top-left block. Finally x = `gaugeGroupℤ₃OfRoot (rootsOfUnity.mkOfPowEq α _)`.
- **Subgroup ⊆ kernel:** a direct computation for each z in μ₃.

Output (exit 0, no warnings, no `sorry`):

```
'ReproIndep.indep_proof' depends on axioms: [propext, Classical.choice, Quot.sound]
```

So the frozen statement is true at Physlib 76245c85, independently of the author's proof. My own Lean files needed three tactic-level fixes while I wrote them. All three errors were in my files: `simp` rewrote `Fin.last 3` to `3`, one name was ambiguous, and one rewrite hit a dependent `Decidable` instance.

### 4c. My own check of the object

My runner calls `lean` directly; it does not use `checker/lean_claim_check.py`.
- It runs from the Physlib checkout, so elan selects v4.34.1.
- LEAN_PATH is my folder followed by the path `lake env` gives inside the Physlib checkout.
- It passes `--root=<my folder>`.

Steps:
1. Compiled the spec on its own as module `V3R1T4SSpec`: exit 0, no output.
2. Compiled a hash-verified copy of the object (not yet read) as module `V3R1T4SClaim`: exit 0, no output (no error, no warning, no `sorry`).
3. Ran my check file `ReproCheck.lean` (Appendix C). It exited 0 and printed:

```
def V3R1T4S.spec : Prop :=
∃ f,
  (∀ (x : StandardModel.GaugeGroupI),
      ↑(f x).1 = V3R1T4S.psMatrix4 x ∧ ↑(f x).2.1 = ↑x.2.1 ∧ ↑(f x).2.2 = V3R1T4S.psMatrixR x) ∧
    f.ker = StandardModel.gaugeGroupℤ₃SubGroup
@[reducible] def V3R1T4S.GaugeGroupPS : Type :=
↥(Matrix.specialUnitaryGroup (Fin 4) ℂ) ×
  ↥(Matrix.specialUnitaryGroup (Fin 2) ℂ) × ↥(Matrix.specialUnitaryGroup (Fin 2) ℂ)
def V3R1T4S.psMatrix4 : StandardModel.GaugeGroupI → Matrix (Fin 4) (Fin 4) ℂ :=
fun x => (Matrix.reindex finSumFinEquiv finSumFinEquiv) (Matrix.fromBlocks (↑x.2.2 • ↑x.1) 0 0 ((↑x.2.2)⁻¹ ^ 3 • 1))
def V3R1T4S.psMatrixR : StandardModel.GaugeGroupI → Matrix (Fin 2) (Fin 2) ℂ :=
fun x => Matrix.diagonal ![↑x.2.2 ^ 3, (↑x.2.2)⁻¹ ^ 3]
@[reducible] def StandardModel.GaugeGroupI : Type :=
↥(Matrix.specialUnitaryGroup (Fin 3) ℂ) × ↥(Matrix.specialUnitaryGroup (Fin 2) ℂ) × ↥(unitary ℂ)
def StandardModel.gaugeGroupℤ₃SubGroup : Subgroup StandardModel.GaugeGroupI :=
StandardModel.gaugeGroupℤ₃Hom.range
def StandardModel.gaugeGroupℤ₃Hom : ↥(rootsOfUnity 3 ℂ) →* StandardModel.GaugeGroupI :=
StandardModel.gaugeGroupℤ₆Hom.comp StandardModel.gaugeGroupℤ₃RootToℤ₆Root
def StandardModel.gaugeGroupℤ₃RootToℤ₆Root : ↥(rootsOfUnity 3 ℂ) →* ↥(rootsOfUnity 6 ℂ) :=
Subgroup.inclusion StandardModel.gaugeGroupℤ₃RootToℤ₆Root._proof_2
'repro_check' depends on axioms: [propext, Classical.choice, Quot.sound]
type of repro_check is exactly the constant V3R1T4S.spec: true
V3R1T4S.spec comes from module V3R1T4SSpec: true
V3R1T4S.claim comes from module V3R1T4SClaim: true
V3R1T4S.claim is a theorem
constants added by V3R1T4SClaim: 31
  theorem: V3R1T4S.claim
  theorem: V3R1T4S.KF.blockA_unitary
  theorem: V3R1T4S.KF.blockD_unitary
  theorem: V3R1T4S.KF.coe_ne_zero
  theorem: V3R1T4S.KF.coe_root
  def: V3R1T4S.KF.hom4
  def: V3R1T4S.KF.homR
  def: V3R1T4S.KF.inclSM
  theorem: V3R1T4S.KF.inclSM_apply
  theorem: V3R1T4S.KF.inclSM_eq_one_iff
  theorem: V3R1T4S.KF.inclSM_ker
  theorem: V3R1T4S.KF.psMatrix4_det
  theorem: V3R1T4S.KF.psMatrix4_eq_one_iff
  theorem: V3R1T4S.KF.psMatrix4_mem
  theorem: V3R1T4S.KF.psMatrix4_mul
  theorem: V3R1T4S.KF.psMatrix4_unitary
  theorem: V3R1T4S.KF.psMatrixR_det
  theorem: V3R1T4S.KF.psMatrixR_eq_one_iff
  theorem: V3R1T4S.KF.psMatrixR_mem
  theorem: V3R1T4S.KF.psMatrixR_mul
  theorem: V3R1T4S.KF.psMatrixR_unitary
  theorem: V3R1T4S.KF.reindex_one
  theorem: V3R1T4S.KF.star_coe
  theorem: V3R1T4S.KF.star_invpow3_mul
  theorem: V3R1T4S.KF.star_pow3_mul
  theorem: V3R1T4S.psMatrix4.eq_1
  theorem: V3R1T4S.psMatrixR.eq_1
  theorem: V3R1T4S.KF.hom4._proof_1
  theorem: V3R1T4S.KF.hom4._proof_2
  theorem: V3R1T4S.KF.homR._proof_1
  theorem: V3R1T4S.KF.homR._proof_2
```

What this shows:
- The object adds 3 definitions and 28 theorems, and no axiom, opaque constant or inductive type.
- The two `eq_1` entries are equation lemmas for the spec's definitions, generated when the object unfolds them.

## 5. The package's own checker, exactly as REPRODUCE.md says

I ran this from `claim/`, with `<workspace>` standing for the V3R1T4S workspace root:

```
. <workspace>/tools/lean_env.sh ; export ELAN_NO_OVERRIDE_NOTICE=1 ; cd claim/
sh <workspace>/tools/lean_slot.sh python3 -I checker/lean_claim_check.py --physlib <workspace>/lean/physlib \
  --spec checker/spec_patisalam_inclSM_ker.lean --candidate object/PatiSalamInclSMKer.lean
```

- Run 1 started at 2026-10-15T07:35:58Z, took 23 s and exited 0.
- Run 2 started at 2026-10-15T07:36:27Z and exited 0.
- The two outputs are byte-identical (sha256 e96148eb8cc9743f1cde21633f813cd3541f835a6bdea00d19a24b58e45b0c7f):

```
spec compile: exit 0
candidate compile: exit 0
check file: exit 0
'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]
axioms: ['Classical.choice', 'Quot.sound', 'propext']
PASS
```

The last line is `PASS`, as REPRODUCE.md expects. No `problem:` lines were printed, so the checker's source policy found nothing.

## 6. The object, step by step (read after sections 2 to 5)

`object/PatiSalamInclSMKer.lean` imports only `Physlib` and `V3R1T4SSpec`. It uses plain tactic proofs inside `namespace V3R1T4S.KF`. I re-derived every step:

| lines | lemma | re-derivation |
|---|---|---|
| 16–20 | `coe_ne_zero` | If α = 0, then star α·α = 1 becomes 0 = 1. |
| 22–23 | `star_coe` | star α·α = 1 gives star α = α⁻¹. |
| 25–26 | `star_pow3_mul` | star(α³)α³ = (star α·α)³ = 1. |
| 28–29 | `star_invpow3_mul` | star(α⁻¹)³α⁻³ = ((star α)⁻¹)³α⁻³ = α³α⁻³ = (αα⁻¹)³ = 1. |
| 33–38 | `blockA_unitary` | (αh)ᴴ(αh) = (ᾱα)(hᴴh) = 1, since h is in U(3). |
| 40–44 | `blockD_unitary` | The same argument for the 1×1 block α⁻³. |
| 46–49 | `reindex_one` | Reindexing 1 along an equivalence gives 1. |
| 51–60 | `psMatrix4_unitary` | (reindex M)ᴴ(reindex M) = reindex(MᴴM), and MᴴM = fromBlocks(AᴴA, 0, 0, DᴴD) = fromBlocks(1, 0, 0, 1) = 1. |
| 62–68 | `psMatrix4_det` | Reindexing keeps det; det fromBlocks(A, 0, 0, D) = det A·det D = α³·det h·α⁻³ = 1. |
| 70–73 | `psMatrix4_mem` | Unitary with det 1 means it lies in SU(4). |
| 75–89 | `psMatrix4_mul` | Reindexing is multiplicative. Block by block, (αβ)(hh′) = (αh)(βh′) and ((αβ)⁻¹)³ = α⁻³β⁻³; the off-diagonal blocks are 0. |
| 93–111 | `psMatrixR_unitary`, `_det`, `_mem` | The entries satisfy star(α³)α³ = 1 and star(α⁻³)α⁻³ = 1; det = α³α⁻³ = 1. |
| 113–122 | `psMatrixR_mul` | (αβ)³ = α³β³ and ((αβ)⁻¹)³ = α⁻³β⁻³. |
| 126–133 | `hom4`, `homR`, `inclSM` | `MonoidHom.mk'` turns a multiplicative map between groups into a monoid hom. Then inclSM = hom4 × (Physlib's `GaugeGroupI.toSU2` × homR). |
| 135–139 | `inclSM_apply` | The components are definitionally `psMatrix4 x`, `x.2.1` and `psMatrixR x` (`rfl`). This is the spec's first conjunct. |
| 143–157 | `psMatrix4_eq_one_iff` | Reindexing is injective. `fromBlocks_inj` then gives αh = 1, and the 1×1 block gives α⁻³ = 1. The converse is by rewriting. |
| 159–170 | `psMatrixR_eq_one_iff` | The (0,0) entry gives α³ = 1. The converse uses α⁻³ = (α³)⁻¹ = 1. |
| 172–190 | `inclSM_eq_one_iff` | inclSM x = 1 holds exactly when α³ = 1, αh = 1 and g = 1. |
| 192–194 | `coe_root` | The value of the ℤ₃→ℤ₆ inclusion of `mkOfPowEq α` is α (`rfl`). |
| 196–232 | `inclSM_ker` | **⊆:** h = α²·(αh) = (α²α)h, so h = α²·1. Then x = `gaugeGroupℤ₃OfRoot (mkOfPowEq α)` componentwise: SU(3) part α²·1, SU(2) part star(α)³·1 = star(α³)·1 = 1 = g, U(1) part α. **⊇:** for β in μ₃, β·β²·1 = 1, star(β)³·1 = 1 and β³ = 1. |
| 236–237 | `V3R1T4S.claim` | `⟨inclSM, inclSM_apply, inclSM_ker⟩`. |

Every step is sound, and the route is the same as my own proof in 4b.

**Source-policy scan.** Beyond the checker's own policy, I scanned the object's text, including comments, for each of these, and none occurs:
- `axiom`, `instance`, `attribute`, `notation`
- `infix`, `infixl`, `infixr`, `prefix`, `postfix`
- `macro`, `macro_rules`, `syntax`, `elab`, `elab_rules`
- `run_cmd`, `run_elab`, `run_meta`, `initialize`
- `unsafe`, `implemented_by`, `extern`, `opaque`
- `native_decide`, `decide`, `set_option`, `sorry`, `admit`
- `private`, `local`, `export`, `open`, `simproc`, `partial`, `termination_by`, `decreasing_by`
- `Lean.`, `#eval`, `#exit`, `@[`

**Characters.** The only non-ASCII characters are ordinary math symbols. There are no format, control or bidi characters, no CR and no tabs, so the displayed source is the compiled source.

## 7. Determinism

- **Package checker:** two runs produced byte-identical output.
- **My pipeline:** in a clean rerun (my `.olean` files deleted, then spec, sanity, independent proof, object and check file all recompiled), all five logs were identical to the first run.
- **Numeric check:** identical output across runs.

## 8. Mismatches, limits, notes

- **Mismatches: none.** Everything checkable matches what the claim says:
  - the hashes;
  - the statement's faithfulness to the informal lemma;
  - the claimed kernel, which equals `StandardModel.gaugeGroupℤ₃SubGroup`;
  - `PASS` from the package checker;
  - the axiom set {propext, Classical.choice, Quot.sound};
  - determinism.
- **Limit (commit):**
  - CLAIM.md says the proof was made against Physlib be0f21e5. That commit is not on this machine; MACHINE_NOTE.md disclosed this before the panel.
  - I reproduced and independently re-proved the claim against 76245c85 only, and verified nothing about be0f21e5 itself.
  - The one cross-commit fact I could check: the PatiSalam file at 76245c85 has exactly the sha256 that CLAIM.md records for the fetched page.
- **Not assessed:** the "Target note" says this Pati-Salam claim is a follow-on filed under the Georgi-Glashow quarry id. Whether that is acceptable is a charter question outside the REPRODUCE role.
- **Note on the checker, not affecting this verdict:** the forbidden-word patterns in `checker/lean_claim_check.py` use `\b` word boundaries, so they do not catch:
  - `macro_rules` or `elab_rules`;
  - `infixl`, `infixr`, `prefix` or `postfix`;
  - `@[...]` attributes other than those naming a forbidden word, or `open ... in`;
  - meta code that goes through `modifyEnv` inside an `elab_rules`.

  The object uses none of these (section 6). The verdict also does not rest on the checker alone: it rests on my own compile and check (4c) and my independent proof (4b).

## Appendix A — ReproSanity.lean (mine; imports only the compiled frozen statement)

```lean
import V3R1T4SSpec

/-! REPRODUCE skeptic: sanity lemmas about the frozen statement, written without looking at the object.
They show the spec's ingredients are what the informal statement says:
* `psMatrix4 x` is blockdiag(α h, α⁻³) (α h on indices 0,1,2 and α⁻³ on index 3, zeros elsewhere);
* `psMatrixR x` is diag(α³, α⁻³);
* Physlib's `StandardModel.gaugeGroupℤ₃SubGroup` is exactly {(ω² I₃, I₂, ω) : ω³ = 1}. -/

open Matrix

namespace ReproSanity

variable (x : StandardModel.GaugeGroupI)

theorem ps4_topLeft (i j : Fin 3) :
    V3R1T4S.psMatrix4 x i.castSucc j.castSucc =
      (x.2.2 : ℂ) * (x.1 : Matrix (Fin 3) (Fin 3) ℂ) i j := by
  simp [V3R1T4S.psMatrix4]

theorem ps4_topRight (i : Fin 3) : V3R1T4S.psMatrix4 x i.castSucc (Fin.last 3) = 0 := by
  rw [V3R1T4S.psMatrix4, reindex_apply, submatrix_apply, finSumFinEquiv_symm_apply_castSucc,
    finSumFinEquiv_symm_last]
  simp

theorem ps4_bottomLeft (j : Fin 3) : V3R1T4S.psMatrix4 x (Fin.last 3) j.castSucc = 0 := by
  rw [V3R1T4S.psMatrix4, reindex_apply, submatrix_apply, finSumFinEquiv_symm_apply_castSucc,
    finSumFinEquiv_symm_last]
  simp

theorem ps4_bottomRight :
    V3R1T4S.psMatrix4 x (Fin.last 3) (Fin.last 3) = (x.2.2 : ℂ) ^ (-3 : ℤ) := by
  rw [V3R1T4S.psMatrix4, reindex_apply, submatrix_apply, finSumFinEquiv_symm_last]
  simp

/-- The same, as one explicit index formula for blockdiag(α h, α⁻³). -/
theorem ps4_explicit :
    V3R1T4S.psMatrix4 x = Matrix.of (fun i j : Fin 4 =>
      if h : i.val < 3 ∧ j.val < 3 then
        (x.2.2 : ℂ) * (x.1 : Matrix (Fin 3) (Fin 3) ℂ) ⟨i.val, h.1⟩ ⟨j.val, h.2⟩
      else if i.val = 3 ∧ j.val = 3 then (x.2.2 : ℂ) ^ (-3 : ℤ) else 0) := by
  ext i j
  induction i using Fin.lastCases with
  | last =>
    induction j using Fin.lastCases with
    | last => simpa using ps4_bottomRight x
    | cast j => simpa [j.isLt.ne] using ps4_bottomLeft x j
  | cast i =>
    induction j using Fin.lastCases with
    | last => simpa [i.isLt.ne] using ps4_topRight x i
    | cast j => simpa [i.isLt, j.isLt] using ps4_topLeft x i j

theorem psR_explicit :
    V3R1T4S.psMatrixR x = !![(x.2.2 : ℂ) ^ 3, 0; 0, (x.2.2 : ℂ) ^ (-3 : ℤ)] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [V3R1T4S.psMatrixR]

/-- Physlib's ℤ₃ subgroup, characterized explicitly. -/
theorem mem_Z3_iff (g : StandardModel.GaugeGroupI) :
    g ∈ StandardModel.gaugeGroupℤ₃SubGroup ↔
      ∃ ω : ℂ, ω ^ 3 = 1 ∧ (g.1 : Matrix (Fin 3) (Fin 3) ℂ) = ω ^ 2 • (1 : Matrix (Fin 3) (Fin 3) ℂ) ∧
        (g.2.1 : Matrix (Fin 2) (Fin 2) ℂ) = 1 ∧ (g.2.2 : ℂ) = ω := by
  rw [StandardModel.mem_gaugeGroupℤ₃SubGroup_iff]
  constructor
  · rintro ⟨z, rfl⟩
    have hz : ((z : ℂˣ) : ℂ) ^ 3 = 1 := (mem_rootsOfUnity' 3 (z : ℂˣ)).mp z.prop
    refine ⟨((z : ℂˣ) : ℂ), hz, ?_, ?_, rfl⟩
    · exact StandardModel.gaugeGroupℤ₆SU3OfRoot_eq_mul_id _
    · have h := StandardModel.gaugeGroupℤ₆SU2OfRoot_eq_mul_id (StandardModel.gaugeGroupℤ₃RootToℤ₆Root z)
      change _ = star ((z : ℂˣ) : ℂ) ^ 3 • (1 : Matrix (Fin 2) (Fin 2) ℂ) at h
      change (StandardModel.gaugeGroupℤ₆SU2OfRoot (StandardModel.gaugeGroupℤ₃RootToℤ₆Root z)).1 = 1
      rw [h, ← star_pow, hz, star_one, one_smul]
  · rintro ⟨ω, hω, h1, h2, h3⟩
    refine ⟨rootsOfUnity.mkOfPowEq ω hω, Prod.ext (Subtype.ext ?_) (Prod.ext (Subtype.ext ?_) (Subtype.ext ?_))⟩
    · change (StandardModel.gaugeGroupℤ₆SU3OfRoot _).1 = _
      rw [StandardModel.gaugeGroupℤ₆SU3OfRoot_eq_mul_id, h1]
      rfl
    · change (StandardModel.gaugeGroupℤ₆SU2OfRoot _).1 = _
      rw [StandardModel.gaugeGroupℤ₆SU2OfRoot_eq_mul_id, h2]
      change star ω ^ 3 • (1 : Matrix (Fin 2) (Fin 2) ℂ) = 1
      rw [← star_pow, hω, star_one, one_smul]
    · exact h3.symm

end ReproSanity

#print axioms ReproSanity.ps4_explicit
#print axioms ReproSanity.psR_explicit
#print axioms ReproSanity.mem_Z3_iff
```

## Appendix B — ReproIndep.lean (mine; an independent proof of `V3R1T4S.spec`)

```lean
import V3R1T4SSpec

/-! REPRODUCE skeptic: an independent proof of the frozen statement `V3R1T4S.spec`, written from the
definitions before reading the object. Imports only the compiled frozen statement (and through it Physlib). -/

open Matrix StandardModel

namespace ReproIndep

/-- The block matrix `fromBlocks (α h) 0 0 (α⁻³)` before reindexing to `Fin 4`. -/
noncomputable def blk (x : GaugeGroupI) : Matrix (Fin 3 ⊕ Fin 1) (Fin 3 ⊕ Fin 1) ℂ :=
  fromBlocks ((x.2.2 : ℂ) • (x.1 : Matrix (Fin 3) (Fin 3) ℂ)) 0 0
    (((x.2.2 : ℂ)⁻¹ ^ 3) • (1 : Matrix (Fin 1) (Fin 1) ℂ))

lemma ps4_eq (x : GaugeGroupI) :
    V3R1T4S.psMatrix4 x = reindex finSumFinEquiv finSumFinEquiv (blk x) := rfl

lemma u_star_mul (x : GaugeGroupI) : star (x.2.2 : ℂ) * (x.2.2 : ℂ) = 1 :=
  Unitary.coe_star_mul_self x.2.2

lemma u_ne_zero (x : GaugeGroupI) : (x.2.2 : ℂ) ≠ 0 :=
  right_ne_zero_of_mul_eq_one (u_star_mul x)

lemma u_inv3_star_mul (x : GaugeGroupI) :
    star ((x.2.2 : ℂ)⁻¹ ^ 3) * (x.2.2 : ℂ)⁻¹ ^ 3 = 1 := by
  rw [star_pow, star_inv₀, ← mul_pow, ← mul_inv, u_star_mul, inv_one, one_pow]

lemma u3_star_mul (x : GaugeGroupI) : star ((x.2.2 : ℂ) ^ 3) * (x.2.2 : ℂ) ^ 3 = 1 := by
  rw [star_pow, ← mul_pow, u_star_mul, one_pow]

lemma blk_unitary (x : GaugeGroupI) : star (blk x) * blk x = 1 := by
  have hh : star (x.1 : Matrix (Fin 3) (Fin 3) ℂ) * (x.1 : Matrix (Fin 3) (Fin 3) ℂ) = 1 :=
    mem_unitaryGroup_iff'.mp (mem_specialUnitaryGroup_iff.mp x.1.prop).1
  rw [star_eq_conjTranspose, blk, fromBlocks_conjTranspose, fromBlocks_multiply, ← fromBlocks_one]
  simp only [conjTranspose_zero, Matrix.zero_mul, Matrix.mul_zero, add_zero, zero_add,
    conjTranspose_smul, conjTranspose_one]
  congr 1
  · rw [Matrix.smul_mul, Matrix.mul_smul, smul_smul, ← star_eq_conjTranspose, hh,
      u_star_mul, one_smul]
  · rw [Matrix.smul_mul, Matrix.mul_smul, smul_smul, Matrix.one_mul, u_inv3_star_mul, one_smul]

lemma blk_det (x : GaugeGroupI) : det (blk x) = 1 := by
  have hdet : det (x.1 : Matrix (Fin 3) (Fin 3) ℂ) = 1 := (mem_specialUnitaryGroup_iff.mp x.1.prop).2
  rw [blk, det_fromBlocks_zero₂₁, det_smul, det_smul, hdet, det_one, Fintype.card_fin,
    Fintype.card_fin, pow_one, mul_one, mul_one, inv_pow, mul_inv_cancel₀ (pow_ne_zero 3 (u_ne_zero x))]

lemma ps4_mem (x : GaugeGroupI) : V3R1T4S.psMatrix4 x ∈ specialUnitaryGroup (Fin 4) ℂ := by
  rw [mem_specialUnitaryGroup_iff, mem_unitaryGroup_iff', ps4_eq]
  constructor
  · rw [star_eq_conjTranspose, conjTranspose_reindex, reindex_apply, reindex_apply,
      submatrix_mul_equiv, ← star_eq_conjTranspose, blk_unitary, submatrix_one_equiv]
  · rw [det_reindex_self, blk_det]

lemma psR_mem (x : GaugeGroupI) : V3R1T4S.psMatrixR x ∈ specialUnitaryGroup (Fin 2) ℂ := by
  rw [mem_specialUnitaryGroup_iff, mem_unitaryGroup_iff']
  constructor
  · rw [V3R1T4S.psMatrixR, star_eq_conjTranspose, diagonal_conjTranspose, diagonal_mul_diagonal,
      ← diagonal_one]
    congr 1
    funext i
    fin_cases i
    · exact u3_star_mul x
    · exact u_inv3_star_mul x
  · rw [V3R1T4S.psMatrixR, det_diagonal, Fin.prod_univ_two]
    change (x.2.2 : ℂ) ^ 3 * (x.2.2 : ℂ)⁻¹ ^ 3 = 1
    rw [inv_pow, mul_inv_cancel₀ (pow_ne_zero 3 (u_ne_zero x))]

lemma blk_mul (x y : GaugeGroupI) : blk (x * y) = blk x * blk y := by
  rw [blk, blk, blk, fromBlocks_multiply]
  simp only [Matrix.zero_mul, Matrix.mul_zero, add_zero, zero_add]
  congr 1
  · rw [Matrix.smul_mul, Matrix.mul_smul, smul_smul]
    rfl
  · rw [Matrix.smul_mul, Matrix.mul_smul, smul_smul, Matrix.one_mul, ← mul_pow, ← mul_inv]
    rfl

lemma ps4_mul (x y : GaugeGroupI) :
    V3R1T4S.psMatrix4 (x * y) = V3R1T4S.psMatrix4 x * V3R1T4S.psMatrix4 y := by
  rw [ps4_eq, ps4_eq, ps4_eq, blk_mul, reindex_apply, reindex_apply, reindex_apply,
    submatrix_mul_equiv]

lemma psR_mul (x y : GaugeGroupI) :
    V3R1T4S.psMatrixR (x * y) = V3R1T4S.psMatrixR x * V3R1T4S.psMatrixR y := by
  rw [V3R1T4S.psMatrixR, V3R1T4S.psMatrixR, V3R1T4S.psMatrixR, diagonal_mul_diagonal]
  congr 1
  funext i
  fin_cases i
  · change ((x.2.2 : ℂ) * (y.2.2 : ℂ)) ^ 3 = (x.2.2 : ℂ) ^ 3 * (y.2.2 : ℂ) ^ 3
    rw [mul_pow]
  · change ((x.2.2 : ℂ) * (y.2.2 : ℂ))⁻¹ ^ 3 = (x.2.2 : ℂ)⁻¹ ^ 3 * (y.2.2 : ℂ)⁻¹ ^ 3
    rw [mul_inv, mul_pow]

lemma ps4_one : V3R1T4S.psMatrix4 1 = 1 := by
  have hb : blk 1 = 1 := by
    change fromBlocks ((1 : ℂ) • (1 : Matrix (Fin 3) (Fin 3) ℂ)) 0 0
      (((1 : ℂ)⁻¹ ^ 3) • (1 : Matrix (Fin 1) (Fin 1) ℂ)) = 1
    rw [inv_one, one_pow, one_smul, one_smul, fromBlocks_one]
  rw [ps4_eq, hb, reindex_apply, submatrix_one_equiv]

lemma psR_one : V3R1T4S.psMatrixR 1 = 1 := by
  change diagonal ![(1 : ℂ) ^ 3, (1 : ℂ)⁻¹ ^ 3] = 1
  rw [inv_one, one_pow, ← diagonal_one]
  congr 1
  funext i
  fin_cases i <;> rfl

/-- The map `(h, g, α) ↦ (blockdiag (α h, α⁻³), g, diag (α³, α⁻³))` as a monoid hom. -/
noncomputable def F : GaugeGroupI →* V3R1T4S.GaugeGroupPS where
  toFun x := (⟨V3R1T4S.psMatrix4 x, ps4_mem x⟩, x.2.1, ⟨V3R1T4S.psMatrixR x, psR_mem x⟩)
  map_one' := Prod.ext (Subtype.ext ps4_one) (Prod.ext rfl (Subtype.ext psR_one))
  map_mul' x y := Prod.ext (Subtype.ext (ps4_mul x y)) (Prod.ext rfl (Subtype.ext (psR_mul x y)))

theorem F_ker : F.ker = gaugeGroupℤ₃SubGroup := by
  ext x
  rw [MonoidHom.mem_ker, mem_gaugeGroupℤ₃SubGroup_iff]
  constructor
  · intro hx
    have h4 : V3R1T4S.psMatrix4 x = 1 :=
      congrArg (fun p : V3R1T4S.GaugeGroupPS => (p.1 : Matrix (Fin 4) (Fin 4) ℂ)) hx
    have h2 : (x.2.1 : Matrix (Fin 2) (Fin 2) ℂ) = 1 :=
      congrArg (fun p : V3R1T4S.GaugeGroupPS => (p.2.1 : Matrix (Fin 2) (Fin 2) ℂ)) hx
    have hR : V3R1T4S.psMatrixR x = 1 :=
      congrArg (fun p : V3R1T4S.GaugeGroupPS => (p.2.2 : Matrix (Fin 2) (Fin 2) ℂ)) hx
    -- α³ = 1 from the (0,0) entry of diag(α³, α⁻³) = 1
    have ha3 : (x.2.2 : ℂ) ^ 3 = 1 := by
      have := congrFun (congrFun hR 0) 0
      rwa [V3R1T4S.psMatrixR, diagonal_apply_eq, one_apply_eq] at this
    -- h = α² • 1 from the top-left block α h = 1
    have hh : (x.1 : Matrix (Fin 3) (Fin 3) ℂ) = (x.2.2 : ℂ) ^ 2 • (1 : Matrix (Fin 3) (Fin 3) ℂ) := by
      ext i j
      have hij := congrFun (congrFun h4 i.castSucc) j.castSucc
      rw [ps4_eq, reindex_apply, submatrix_apply, finSumFinEquiv_symm_apply_castSucc,
        finSumFinEquiv_symm_apply_castSucc, blk, fromBlocks_apply₁₁, Matrix.smul_apply, smul_eq_mul] at hij
      rw [Matrix.smul_apply, smul_eq_mul]
      have h1 : (1 : Matrix (Fin 4) (Fin 4) ℂ) i.castSucc j.castSucc =
          (1 : Matrix (Fin 3) (Fin 3) ℂ) i j := by
        rw [one_apply, one_apply]
        exact if_congr (Fin.castSucc_injective 3).eq_iff rfl rfl
      rw [h1] at hij
      calc (x.1 : Matrix (Fin 3) (Fin 3) ℂ) i j
          = (x.2.2 : ℂ) ^ 3 * (x.1 : Matrix (Fin 3) (Fin 3) ℂ) i j := by rw [ha3, one_mul]
        _ = (x.2.2 : ℂ) ^ 2 * ((x.2.2 : ℂ) * (x.1 : Matrix (Fin 3) (Fin 3) ℂ) i j) := by ring
        _ = (x.2.2 : ℂ) ^ 2 * (1 : Matrix (Fin 3) (Fin 3) ℂ) i j := by rw [hij]
    refine ⟨rootsOfUnity.mkOfPowEq (x.2.2 : ℂ) ha3,
      Prod.ext (Subtype.ext ?_) (Prod.ext (Subtype.ext ?_) (Subtype.ext ?_))⟩
    · change (gaugeGroupℤ₆SU3OfRoot _).1 = _
      rw [gaugeGroupℤ₆SU3OfRoot_eq_mul_id, hh]
      rfl
    · change (gaugeGroupℤ₆SU2OfRoot _).1 = _
      rw [gaugeGroupℤ₆SU2OfRoot_eq_mul_id, h2]
      change star (x.2.2 : ℂ) ^ 3 • (1 : Matrix (Fin 2) (Fin 2) ℂ) = 1
      rw [← star_pow, ha3, star_one, one_smul]
    · rfl
  · rintro ⟨z, rfl⟩
    have hz : ((z : ℂˣ) : ℂ) ^ 3 = 1 := (mem_rootsOfUnity' 3 (z : ℂˣ)).mp z.prop
    have h1 : ((gaugeGroupℤ₃OfRoot z).1 : Matrix (Fin 3) (Fin 3) ℂ) = ((z : ℂˣ) : ℂ) ^ 2 • 1 :=
      gaugeGroupℤ₆SU3OfRoot_eq_mul_id _
    have h3 : ((gaugeGroupℤ₃OfRoot z).2.2 : ℂ) = ((z : ℂˣ) : ℂ) := rfl
    refine Prod.ext (Subtype.ext ?_) (Prod.ext (Subtype.ext ?_) (Subtype.ext ?_))
    · change V3R1T4S.psMatrix4 (gaugeGroupℤ₃OfRoot z) = 1
      have hb : blk (gaugeGroupℤ₃OfRoot z) = 1 := by
        have hz3 : ((z : ℂˣ) : ℂ) * ((z : ℂˣ) : ℂ) ^ 2 = 1 := by rw [← hz]; ring
        rw [blk, h1, h3, smul_smul, hz3, one_smul, inv_pow, hz, inv_one, one_smul, fromBlocks_one]
      rw [ps4_eq, hb, reindex_apply, submatrix_one_equiv]
    · change (gaugeGroupℤ₆SU2OfRoot (gaugeGroupℤ₃RootToℤ₆Root z)).1 = 1
      rw [gaugeGroupℤ₆SU2OfRoot_eq_mul_id]
      change star ((z : ℂˣ) : ℂ) ^ 3 • (1 : Matrix (Fin 2) (Fin 2) ℂ) = 1
      rw [← star_pow, hz, star_one, one_smul]
    · change V3R1T4S.psMatrixR (gaugeGroupℤ₃OfRoot z) = 1
      rw [V3R1T4S.psMatrixR, h3, inv_pow, hz, inv_one, ← diagonal_one]
      congr 1
      funext i
      fin_cases i <;> rfl

/-- The frozen statement, proved independently. -/
theorem indep_proof : V3R1T4S.spec := ⟨F, fun _ => ⟨rfl, rfl, rfl⟩, F_ker⟩

end ReproIndep

#print axioms ReproIndep.indep_proof
```

## Appendix C — ReproCheck.lean (mine; my check of the object)

```lean
import V3R1T4SSpec
import V3R1T4SClaim

/-! REPRODUCE skeptic's own check of the object (written before reading the object). -/

-- the statement as compiled from the frozen file
#print V3R1T4S.spec
#print V3R1T4S.GaugeGroupPS
#print V3R1T4S.psMatrix4
#print V3R1T4S.psMatrixR
-- Physlib definitions the statement depends on (as compiled in the local Physlib build)
#print StandardModel.GaugeGroupI
#print StandardModel.gaugeGroupℤ₃SubGroup
#print StandardModel.gaugeGroupℤ₃Hom
#print StandardModel.gaugeGroupℤ₃RootToℤ₆Root

theorem repro_check : V3R1T4S.spec := V3R1T4S.claim

#print axioms repro_check

open Lean in
#eval show CoreM Unit from do
  let env ← getEnv
  let some ci := env.find? `repro_check | throwError "repro_check missing"
  IO.println s!"type of repro_check is exactly the constant V3R1T4S.spec: {ci.type == mkConst `V3R1T4S.spec}"
  IO.println s!"V3R1T4S.spec comes from module V3R1T4SSpec: {env.getModuleIdxFor? `V3R1T4S.spec == env.getModuleIdx? `V3R1T4SSpec}"
  IO.println s!"V3R1T4S.claim comes from module V3R1T4SClaim: {env.getModuleIdxFor? `V3R1T4S.claim == env.getModuleIdx? `V3R1T4SClaim}"
  match env.find? `V3R1T4S.claim with
  | some (.thmInfo _) => IO.println "V3R1T4S.claim is a theorem"
  | some _ => IO.println "V3R1T4S.claim is NOT a theorem"
  | none => IO.println "V3R1T4S.claim not found"
  -- inventory of every constant the object's module adds, with its kind
  let some idx := env.getModuleIdx? `V3R1T4SClaim | throwError "module V3R1T4SClaim not loaded"
  let mut names : Array Name := #[]
  for (n, _) in env.constants.map₁.toList do
    if env.getModuleIdxFor? n == some idx then names := names.push n
  IO.println s!"constants added by V3R1T4SClaim: {names.size}"
  for n in names.qsort Name.lt do
    let kind := match env.find? n with
      | some (.thmInfo _) => "theorem" | some (.defnInfo _) => "def"
      | some (.axiomInfo _) => "AXIOM" | some (.opaqueInfo _) => "opaque"
      | some (.inductInfo _) => "inductive" | some (.ctorInfo _) => "constructor"
      | some (.recInfo _) => "recursor" | some (.quotInfo _) => "quot" | none => "?"
    IO.println s!"  {kind}: {n}"
```

Verdict: confirmed against Physlib 76245c854e4827a1dd7f20d1c053b61219cc8fbb (Lean 4.34.1, Mathlib d13f23b7):
- the frozen statement faithfully formalizes `PatiSalam.inclSM_ker`;
- the object proves it, checked by the Lean kernel, with only propext, Classical.choice and Quot.sound;
- the package checker prints `PASS` deterministically;
- my independent proof confirms the statement.

The claim's be0f21e5 provenance could not be checked on this machine (disclosed in MACHINE_NOTE.md).
pass: true
