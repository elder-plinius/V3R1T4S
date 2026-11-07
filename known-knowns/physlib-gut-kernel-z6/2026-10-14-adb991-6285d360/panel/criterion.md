# Criterion skeptic: `PatiSalam.inclSM_ker` (run 2026-10-14-0701)

context: subagent (fresh context, Claude Code Agent tool)

**What I read.** I read only `claim/` (CLAIM.md, REPRODUCE.md, MACHINE_NOTE.md, checker/, object/, source/) and the Physlib/Mathlib sources of the local Physlib checkout. I got the checkout's commit from its `.git` ref files and ran no git commands. I used the workspace scripts `lean_env.sh` and `lean_slot.sh` as instructed, without reading them.

Two disclosures:
- My first directory listing also showed the sibling folder `2026-10-14-0702/claim`, because the session's working directory pointed there. I saw file names and sizes only and read none of its files.
- A `ps` check for leftover processes of mine also showed command lines of unrelated processes from another run. I used nothing from them.

All scratch work is in `../panel_work/criterion/` (relative to claim/).

## 1. The criterion, read literally

CLAIM.md quotes lines 31–58 of `source/status_page_PatiSalam_Basic.lean`. That file's sha256 (060aeb49…) matches the claim. The local Physlib file `Physlib/Particles/BeyondTheStandardModel/PatiSalam/Basic.lean` at 76245c85 is byte-identical to it.

The criterion is the informal lemma `PatiSalam.inclSM_ker` (tag 6V2RQ): "The kernel of the map `inclSM` is equal to the subgroup `StandardModel.gaugeGroupℤ₃SubGroup`." It depends on two informal definitions:
- `inclSM` (6V2RH): "the group homomorphism SU(3) × SU(2) × U(1) → SU(4) × SU(2) × SU(2) taking (h, g, α) to (blockdiag (α h, α^(-3)), g, diag (α^3, α^(-3)))".
- `GaugeGroupI` (6V2Q2): "SU(4) × SU(2) × SU(2)", not quotiented by ℤ₂.

Success means a kernel-checked proof of the frozen statement that uses only propext, Classical.choice and Quot.sound, or a counterexample. The source lists no partial wins, so only the full criterion can pass.

The claim departs from the literal criterion in two ways:
- **Commit.** The criterion names Physlib be0f21e5, which is not on this machine (see MACHINE_NOTE.md). I checked against 76245c854e4827a1dd7f20d1c053b61219cc8fbb, and my confirmed scope names only that commit.
- **Quarry id.** CLAIM.md's `target:` is the quarry id `physlib-gut-kernel-z6`. Its own Target note says that id names the Georgi–Glashow lemma `GeorgiGlashow.inclSM_ker` (kernel ℤ₆). That lemma is still informal at 76245c85 (`Physlib/Particles/BeyondTheStandardModel/GeorgiGlashow/Basic.lean`), and this claim does not prove it.
  - I judge the criterion as the panel brief and CLAIM.md define it: the Pati–Salam lemma. I was not shown the charter, so I cannot confirm that a "family follow-on" may be scored under this quarry id.
  - This result must not be recorded as a proof of the ℤ₆ Georgi–Glashow lemma.

## 2. Is the frozen statement a faithful, unweakened formalisation?

`checker/spec_patisalam_inclSM_ker.lean` (sha256 ed680955…, matches CLAIM.md) elaborates as follows (`#print V3R1T4S.spec` with full names and coercions shown):

    ∃ f : StandardModel.GaugeGroupI →* V3R1T4S.GaugeGroupPS,
      (∀ x, ↑(f x).1 = V3R1T4S.psMatrix4 x ∧ ↑(f x).2.1 = ↑x.2.1 ∧ ↑(f x).2.2 = V3R1T4S.psMatrixR x) ∧
      f.ker = StandardModel.gaugeGroupℤ₃SubGroup

- **Domain.** It is Physlib's formal `StandardModel.GaugeGroupI := specialUnitaryGroup (Fin 3) ℂ × specialUnitaryGroup (Fin 2) ℂ × unitary ℂ`, defined in `Physlib/Particles/StandardModel/Basic.lean`. So x = (h, g, α) with h = x.1, g = x.2.1 and α = x.2.2, the same order as the docstring.
- **Codomain.** `GaugeGroupPS` is SU(4) × SU(2) × SU(2), built from Mathlib's `Matrix.specialUnitaryGroup` and not quotiented. This is the informal `PatiSalam.GaugeGroupI`, in the docstring's order.
- **The map.**
  - The first component is `psMatrix4 x = reindex finSumFinEquiv finSumFinEquiv (fromBlocks (α • h) 0 0 (α⁻¹ ^ 3 • 1))`.
  - The second component is g.
  - The third component is `psMatrixR x = diagonal ![α ^ 3, α⁻¹ ^ 3]`.
  - In ℂ, α⁻¹ ^ 3 = α^(-3).
  - I checked the block placement in Lean with the scratch lemmas `crit_block_tl/br/tr/bl` and `crit_R`:
    - entry (castAdd i, castAdd j) is α · h i j;
    - entry (3, 3) is α⁻¹ ^ 3;
    - the off-block entries are 0;
    - psMatrixR = diag(α³, α⁻³).
  - Any other reasonable reading of "blockdiag", such as putting α⁻³ first, gives a conjugate map with the same kernel. The result does not depend on this choice.
- **The `∃ f` quantifier.** It is not a loophole, because the pointwise clause fixes f. I proved in Lean (`crit_unique`) that any two homomorphisms satisfying that clause are equal.
  - So the spec is equivalent to: "the map given by the docstring formula is a group homomorphism into SU(4) × SU(2) × SU(2), and its kernel is gaugeGroupℤ₃SubGroup".
  - The informal lemma takes the homomorphism as given. The spec also requires proving that it exists (unitarity and determinant 1), so the spec is stronger, not weaker.
- **The kernel.** `f.ker` is Mathlib's `MonoidHom.ker`. The right-hand side is Physlib's formal `StandardModel.gaugeGroupℤ₃SubGroup`, the range of `gaugeGroupℤ₃Hom`. That range is {(β² I₃, conj(β)³ I₂, β) : β³ = 1}, which equals {(β² I₃, I₂, β) : β³ = 1}. The spec states equality of subgroups (both inclusions), not just ≤.
- **Mathematical check.** f(h, g, α) = 1 holds exactly when α h = I₃, α⁻³ = 1, g = I₂ and α³ = 1. That is the same as α³ = 1, h = α² I₃ and g = I₂, which is the set above. So the lemma is true, which agrees with the cited ℤ₃ answer.
- **Names with no formal counterpart.** `PatiSalam.GaugeGroupI`, `PatiSalam.inclSM`, "blockdiag" and "diag" are each taken literally from the docstrings, with no stretched definitions. The docstring does not ask for continuity or smoothness of inclSM, and neither affects the kernel.

**Conclusion:** the frozen statement is a faithful, unweakened formalisation, with no hidden quantifier.

## 3. Null models

- **Wrong subgroup.** In Lean (`crit_not_Z6`), the same frozen statement with `gaugeGroupℤ₆SubGroup` in place of ℤ₃ is refuted. Take the ℤ₆ element for α = −1: its g-component is −I₂ and α³ = −1, so it is not in the kernel. The statement therefore separates the correct ℤ₃ answer from a Georgi–Glashow-style ℤ₆ answer.
- **Trivial kernel.** `crit_Z3_nontrivial` proves gaugeGroupℤ₃SubGroup ≠ ⊥, using a primitive cube root of unity. So the statement does not reduce to "inclSM is injective".
- **Explicit content.** `crit_ker_explicit`, which uses the claim, gives: x ∈ gaugeGroupℤ₃SubGroup if and only if α³ = 1, h = α² · 1 and g = 1.
- **Checker on a non-proof.** I ran the unchanged checker on the candidate `theorem V3R1T4S.claim : V3R1T4S.spec := sorryAx _ false`. It prints `problem: non-standard axioms: sorryAx` and `FAIL`, so it does not accept a non-proof.

All the scratch theorems depend only on propext, Classical.choice and Quot.sound.

## 4. Does the object prove exactly the frozen statement?

- **Hashes.** The sha256 of every package file matches CLAIM.md: object 6285d360…, spec ed680955…, checker fe7aaf99…, source 060aeb49….
- **Environment.**
  - The local Physlib HEAD is 76245c854e4827a1dd7f20d1c053b61219cc8fbb, with Lean v4.34.1 and Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612.
  - `lake build --no-build Physlib.Particles.StandardModel.Basic Physlib.Particles.BeyondTheStandardModel.PatiSalam.Basic` reports "All targets up-to-date (3292 jobs)".
  - All 618 Physlib oleans are newer than the checkout.
  - So the check ran against 76245c85 itself, not a stale build.
- **The REPRODUCE.md command** (run 2026-10-15T07:25:45Z to 07:26:07Z):
  - spec compile, candidate compile and check file each exit 0;
  - it prints `'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]`;
  - its last line is `PASS`.
- **Independent checks.**
  - I compiled the spec and the object as modules myself, with no warnings or errors.
  - `#print axioms V3R1T4S.claim` lists only the three standard axioms.
  - `#check` reports `V3R1T4S.claim : V3R1T4S.spec`.
  - `leanchecker V3R1T4SClaim V3R1T4SSpec` (kernel replay) exits 0 with no output.
- **Reading the object.** I read it in full.
  - It contains only plain definitions, lemmas and tactic proofs. There are no axioms, instances, attributes, meta code, `sorry`, `native_decide` or `set_option`, and it does not redefine any name from the spec.
  - It defines `inclSM := hom4.prod (toSU2.prod homR)`, and its components are `rfl`-equal to the spec's.

## 5. Genuine and non-subsumed?

- **Not subsumed.**
  - At 76245c85, `PatiSalam.GaugeGroupI`, `PatiSalam.inclSM` and `PatiSalam.inclSM_ker` exist only as `informal_definition` / `informal_lemma` entries.
  - A grep of the Physlib checkout finds no formal Pati–Salam group and no formal `inclSM`, whether for Pati–Salam, Georgi–Glashow or Spin(10). It also finds no kernel lemma for any of these maps.
  - Mathlib has no Standard Model gauge group.
  - I checked Physlib only, not other runs or open upstream PRs.
- **Not trivial in the protocol's sense.** The statement is non-vacuous (section 3), and unfolding definitions does not prove it. The proof has to:
  - build the homomorphism into SU(4), including block unitarity and the determinant;
  - prove that it is multiplicative;
  - compute the kernel in both directions using roots of unity.

  This takes about 230 lines.
- **Size of the contribution.** The mathematics is elementary linear algebra. The contribution is that an open Physlib informal lemma becomes a kernel-checked theorem, together with formal versions of the two informal definitions it needs. It is a modest but genuine formalisation win, not new mathematics. Upstreaming it would mean renaming from `V3R1T4S.…` to Physlib's `PatiSalam.…` names.

## 6. Not confirmed

- That the proof checks against be0f21e5, which is not available here.
- The claim's byte-identity statements about `Physlib/Particles/StandardModel/Basic.lean` at be0f21e5 and 5f2136528e88.
- That the charter allows this Pati–Salam lemma to count under the quarry id `physlib-gut-kernel-z6`. In any case, it is not a proof of `GeorgiGlashow.inclSM_ker` (ℤ₆).

confirmed_scope: Against Physlib commit 76245c854e4827a1dd7f20d1c053b61219cc8fbb (Lean v4.34.1, Mathlib d13f23b7; not against be0f21e5, which was unavailable), object/PatiSalamInclSMKer.lean (sha256 6285d360e0d0a5a396fb3a5461d732888f314b08dcef13c1eda2bcd63aa3a5bd) is a kernel-checked proof, using only propext, Classical.choice and Quot.sound, of the frozen statement checker/spec_patisalam_inclSM_ker.lean (sha256 ed68095509a7bbdffd578df7ccfba3bfde49cbeb8f5173a65dc62123f24db278), namely that the uniquely determined group homomorphism StandardModel.GaugeGroupI →* SU(4) × SU(2) × SU(2), (h, g, α) ↦ (blockdiag(α h, α⁻³), g, diag(α³, α⁻³)), exists and has kernel exactly StandardModel.gaugeGroupℤ₃SubGroup, which faithfully formalises Physlib's informal lemma PatiSalam.inclSM_ker (tag 6V2RQ) and is not a proof of the ℤ₆ lemma GeorgiGlashow.inclSM_ker named by the quarry id physlib-gut-kernel-z6.

pass: true
