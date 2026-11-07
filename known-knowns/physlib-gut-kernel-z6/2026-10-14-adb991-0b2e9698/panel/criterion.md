# CRITERION skeptic: physlib-gut-kernel-z6 (run 2026-10-14-0616)

context: subagent (fresh Agent-tool context; saw only claim/)

(Saved by the run's main session from the skeptic's final message, verbatim apart from de-indentation; the skeptic
was told to return its verdict as text. Its scratch work is in runs/2026-10-14-0616/panel_work/criterion/.)

What I read besides claim/ (all within the brief):
- Physlib/Mathlib sources in the built Physlib checkout, read-only.
- The two slot-gate scripts the brief says to run. tools/lean_env.sh sets PATH and cache dirs. tools/lean_slot.sh takes a flock slot and runs the command at nice 10. Neither changes the check.

I opened no attempts, notes, reports, briefs, dossiers or other runs. A `ps` listing taken to see slot status showed other runs' command lines; I opened none of their files.

## Decision
- **Full success criterion of CLAIM.md:** met.
- **Partial wins:** the source enumerates none, and none is claimed.
- **Fidelity:** the frozen statement checker/spec_inclSM_ker.lean reads the informal docstrings literally and faithfully. No downgrade.

## 1. Fidelity of checker/spec_inclSM_ker.lean to source/status_page_GeorgiGlashow_Basic.lean

**Integrity.** `sha256sum` matches CLAIM.md for all four files:
```
0b2e9698935d6a53381d1015fdac67779ff1d6b9761358e79767391d12c1663d  object/InclSMKer.lean
685fe987fb3c56f5bb42c79116e7bb5c4375fef3794a6b67e37aa953f89afcea  checker/spec_inclSM_ker.lean
fe7aaf99a0b13f23a3c232a5a5fbfa8d33750e5f809cc0bf36e3c87ef9a828de  checker/lean_claim_check.py
34f66288e28cd4f26f1d2338bf092acb6dc5cd92ecd54fa2c129e3e567152682  source/status_page_GeorgiGlashow_Basic.lean
```
- The source copy is byte-identical to Physlib/Particles/BeyondTheStandardModel/GeorgiGlashow/Basic.lean in the checkout (`diff` gave no output: "IDENTICAL to local physlib copy").
- The "verbatim" quote in CLAIM.md equals source lines 28–49 (programmatic check printed `True`).
- Physlib's `InformalLemma` and `InformalDefinition` structures have only the fields `deps` and `tag` (Physlib/Meta/Informal/Basic.lean). So the docstrings are the entire mathematical content to be faithful to.

**Elaborated statement**, from `#print` in panel_work/criterion/build/CritSanity.lean (log: panel_work/criterion/sanity_run2.log):
```
def V3R1T4S.spec : Prop :=
∃ f, (∀ (x : StandardModel.GaugeGroupI), ↑(f x) = V3R1T4S.inclSMMatrix x) ∧ f.ker = StandardModel.gaugeGroupℤ₆SubGroup
def V3R1T4S.inclSMMatrix : StandardModel.GaugeGroupI → Matrix (Fin 5) (Fin 5) ℂ :=
fun x => (reindex finSumFinEquiv finSumFinEquiv) (fromBlocks (↑x.2.2 ^ 3 • ↑x.2.1) 0 0 ((↑x.2.2)⁻¹ ^ 2 • ↑x.1))
@[reducible] def V3R1T4S.GaugeGroupGG : Type :=
↥(specialUnitaryGroup (Fin 5) ℂ)
@[reducible] def StandardModel.GaugeGroupI : Type :=
↥(specialUnitaryGroup (Fin 3) ℂ) × ↥(specialUnitaryGroup (Fin 2) ℂ) × ↥(unitary ℂ)
def StandardModel.gaugeGroupℤ₆SubGroup : Subgroup StandardModel.GaugeGroupI :=
StandardModel.gaugeGroupℤ₆Hom.range
```
In the source, `f : StandardModel.GaugeGroupI →* V3R1T4S.GaugeGroupGG`.

**`GaugeGroupI` (6V2WM), "SU(5)".** The spec uses `Matrix.specialUnitaryGroup (Fin 5) ℂ`. In Mathlib this is `unitaryGroup n α ⊓ MonoidHom.mker detMonoidHom`, i.e. unitary 5×5 complex matrices of determinant 1, with Mathlib's group instance. Faithful.

**Domain of `inclSM` (6V2WS), "SU(3) × SU(2) × U(1)".** Its `deps` name ``StandardModel.GaugeGroupI``, and the spec uses exactly that type, which prints as SU(3) × SU(2) × U(1) in that order. So for x = (h, g, α):
- h = x.1 ∈ SU(3)
- g = x.2.1 ∈ SU(2)
- α = x.2.2 ∈ U(1)

h and g are not swapped; the block sizes force this.

**The map, "(h, g, α) ↦ blockdiag (α ^ 3 g, α ^ (-2) h)".** I proved each block in Lean against the frozen definition. All are axiom-clean (sanity_run2.log).
- `crit_block11`: `inclSMMatrix x (Fin.castAdd 3 i) (Fin.castAdd 3 j) = (x.2.2 : ℂ) ^ 3 * (x.2.1 : Matrix (Fin 2) (Fin 2) ℂ) i j`
- `crit_block22_zpow`: `inclSMMatrix x (Fin.natAdd 2 i) (Fin.natAdd 2 j) = (x.2.2 : ℂ) ^ (-2 : ℤ) * (x.1 : Matrix (Fin 3) (Fin 3) ℂ) i j`. This uses the docstring's integer power, via `crit_zpow : a⁻¹ ^ 2 = a ^ (-2 : ℤ)`.
- `crit_block12`, `crit_block21`: the off-diagonal blocks are 0.
- By `rfl`: `Fin.castAdd 3` sends 0,1 to 0,1, and `Fin.natAdd 2` sends 0,1,2 to 2,3,4.
- Spot checks by `rfl`: `inclSMMatrix x 1 0 = α^3 * g 1 0`, `inclSMMatrix x 4 3 = α⁻¹^2 * h 2 1`, `inclSMMatrix x 0 4 = 0`, `inclSMMatrix x 3 1 = 0`.

So α³g sits top-left (indices 0,1) and α⁻²h bottom-right (indices 2,3,4), which is how "blockdiag (A, B)" reads.

The exponent signs follow the docstring exactly, and this matters. Under the opposite convention (α⁻³ g, α² h) the kernel would be {(α⁻² I₃, α³ I₂, α) : α⁶ = 1}, which is not Physlib's ℤ₆ subgroup. That is hand arithmetic, not checked in Lean. The literal reading is the one under which the informal lemma is true.

**`inclSM_ker`, "The kernel of the map inclSM is equal to the subgroup StandardModel.gaugeGroupℤ₆SubGroup".**
- The spec states `f.ker = StandardModel.gaugeGroupℤ₆SubGroup`. This is `MonoidHom.ker` and a full equality of subgroups, not just ⊆ or ⊇.
- The right-hand side is Physlib's own definition: the range of ζ ↦ (ζ² • 1, (star ζ)³ • 1, ζ) over sixth roots of unity (Physlib/Particles/StandardModel/Basic.lean, `gaugeGroupℤ₆OfRoot` at l.214, `gaugeGroupℤ₆SubGroup` at l.290).
- Faithful.

**`∃ f` is not a stretched reading.** The values clause determines f completely, so no different f can satisfy it.
- `crit_unique`: any two homs satisfying `∀ x, ↑(f x) = inclSMMatrix x` are equal.
- `crit_forall_form`, proved from `V3R1T4S.claim`: every hom satisfying the values clause has `f.ker = gaugeGroupℤ₆SubGroup`. So the ∀-reading holds too.
- The ∃ also carries the content of `inclSM` itself: that these matrices lie in SU(5) and form a group homomorphism.

**Hidden quantifiers or weakening: none.** `V3R1T4S.spec` is a closed Prop with no parameters or hypotheses. `∀ x` ranges over all of StandardModel.GaugeGroupI, and the kernel claim is an equality.

## 2. The object proves the frozen statement

**Provided checker**, run as REPRODUCE.md says through the slot gate. Started 2026-10-14T07:02:03Z, ended 07:03:21Z; log panel_work/criterion/checker_run.log:
```
spec compile: exit 0
candidate compile: exit 0
check file: exit 0
'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]
axioms: ['Classical.choice', 'Quot.sound', 'propext']
PASS
```

**Independent recompile** in panel_work/criterion/build (script panel_work/criterion/run_indep.sh, log panel_work/criterion/indep_run.log). I used my own sha-verified copies, compiled as separate modules (V3R1T4SSpec, then V3R1T4SClaim), then a fresh Check.lean:
```
== spec compile (2026-10-14T07:07:02Z)
exit=0
== object compile (2026-10-14T07:07:12Z)
exit=0
== fresh check file (2026-10-14T07:07:24Z)
'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]
exit=0
```
sanity_run2.log also shows `'V3R1T4S.claim' depends on axioms: [propext, Classical.choice, Quot.sound]`, and the same for `V3R1T4S.KF.inclSMHom` and `V3R1T4S.KF.ker_eq`, with `exit=0`. indep_run.log also contains errors from the first draft of my own helper lemmas in CritSanity.lean. Those were tactic problems in my file, not in the object; I fixed them and the rerun in sanity_run2.log is clean.

**Nothing in the object redefines notions the statement uses.**
- Running the checker's own forbidden-pattern list over the object's code gives `forbidden-pattern hits: none`.
- It has no `@[...]` attributes and no `set_option`.
- Its imports are `['Physlib', 'V3R1T4SSpec']`.
- It declares only new names in namespace `V3R1T4S.KF`: scal_mul_star, scal_star_mul, scal_ne_zero, scal_inv, inclSMMatrix_mem, inclSMMatrix_one, inclSMMatrix_mul, inclSMHom, inclSMHom_coe, inclSMMatrix_eq_one_iff, ker_eq. Plus `theorem V3R1T4S.claim`.
- The statement's meaning is fixed before the object is loaded: the spec is compiled first as its own module, and `theorem V3R1T4S_check : V3R1T4S.spec := V3R1T4S.claim` elaborates in a fresh file.

**Physlib commit and toolchain.**
- The checkout's HEAD is be0f21e5002d6d73b87f2055530c1e8bf7151546, with 0 tracked-file changes.
- That came from a read-only git query run before I registered the brief's "no git". It wrote nothing: `.git/index` mtime 06:12:01Z predates this session.
- Toolchain: leanprover/lean4:v4.34.1.

## 3. Genuine, non-subsumed; null models

**Non-subsumed.** The claim meets the full criterion, so it is not a partial win covered by a bigger one.

At this Physlib commit the result is not already formal:
- A grep of Physlib/, PhyslibAlpha/ and QuantumInfo/ for `inclSM`, `GeorgiGlashow` and `embedSMℤ₆` finds only `informal_definition` and `informal_lemma` entries.
- A grep of those trees and Mathlib for `specialUnitaryGroup (Fin 5)` finds no match.

Whether it has been done elsewhere, such as an upstream PR, is outside what I may look at; that is the novelty lens's question.

**Null models do not apply.** This is a deterministic, kernel-checked proof with no sampling or randomness. The axiom list excludes `sorryAx` and native_decide's `Lean.ofReduceBool`.

The relevant analogue is non-vacuity, which I checked in Lean (all axiom-clean):
- `crit_Z6_ne_bot`: gaugeGroupℤ₆SubGroup ≠ ⊥, shown with ζ = −1.
- `crit_Z6_ne_top`: gaugeGroupℤ₆SubGroup ≠ ⊤, shown with (1, 1, i).
- `crit_ker_nontrivial_proper`: every f satisfying the values clause has f.ker ≠ ⊥ ∧ f.ker ≠ ⊤.

So the statement is neither trivial nor vacuous, and no degenerate f can satisfy it.

## Non-blocking note
CLAIM.md says the copy is "saved in `data/status_page_GeorgiGlashow_Basic.lean`" and quotes "lines 28-50". The file actually lives at source/status_page_GeorgiGlashow_Basic.lean, as CLAIM.md's own status record says. The quote is lines 28–49, and line 50 is blank. The hash and content are correct.

confirmed_scope: Against Physlib be0f21e5002d6d73b87f2055530c1e8bf7151546 with Lean v4.34.1, object/InclSMKer.lean kernel-checks, using only the axioms propext, Classical.choice and Quot.sound, the frozen statement checker/spec_inclSM_ker.lean, a literal and unweakened formalisation of Physlib's informal lemma GeorgiGlashow.inclSM_ker (tag 6V2W2) with its informal dependencies GaugeGroupI (6V2WM) and inclSM (6V2WS), which asserts that the map StandardModel.GaugeGroupI = SU(3) × SU(2) × U(1) → Matrix.specialUnitaryGroup (Fin 5) ℂ sending (h, g, α) to blockdiag(α^3 g, α^(-2) h) (2×2 block on indices 0,1, 3×3 block on indices 2,3,4) is a group homomorphism, necessarily the unique one with these values, whose kernel equals StandardModel.gaugeGroupℤ₆SubGroup.
pass: true
