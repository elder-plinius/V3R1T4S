# REPRODUCE skeptic verdict: physlib-restricted-lorentz-connected

context: subagent (fresh Agent-tool context; saw only claim/)

(Saved by the run's main session from the skeptic's final message, verbatim apart from de-indentation; the skeptic
was told to return its verdict as text. Its scratch work is in runs/2026-10-14-0608/panel_work/reproduce/.)

Scope note: Besides claim/, I read only these:
- the Lean toolchain: lean, lake, leanchecker v4.34.1, and the leanchecker source shipped with it;
- the built Physlib/Mathlib sources under the workspace's lean/physlib, read-only;
- the two wrapper scripts REPRODUCE.md told me to run:
  - tools/lean_env.sh only sets ELAN_HOME, XDG_CACHE_HOME and PATH;
  - tools/lean_slot.sh takes a flock slot, then runs the command unchanged under nice;
- five Physlib files at commit be0f21e, fetched with read-only HTTP GETs from raw.githubusercontent.com to compare hashes.

I did not open attempts/, notes, reports, briefs, other runs, other panel folders, or any run file outside claim/. I wrote scratch files only in panel_work/reproduce/. Paths are relative to claim/ unless marked `<ws>`, which stands for the workspace root.

## 1. Published definition and my own statement (written before I opened the object)

The published statement is in source/status_page_Restricted_Basic.lean, lines 61-63. Its sha256 is e41850ba01879f3a9a6c3934efd85aab5b4a1a48c8d8a4621da63f7c5296f1c9, as CLAIM.md says. The file is byte-identical to Physlib/Relativity/LorentzGroup/Restricted/Basic.lean in the local checkout:

```lean
/-- The restricted Lorentz group is connected. -/
semiformal_result "FXNL5" restricted_isConnected {d : ℕ} :
  IsConnected (restricted d : Set (LorentzGroup d))
```

It sits inside `namespace LorentzGroup`, with `open Matrix`, `open minkowskiMatrix` and `open TopologicalSpace`.

Definitions I read in Physlib:
- `LorentzGroup d := {Λ : Matrix (Fin 1 ⊕ Fin d) (Fin 1 ⊕ Fin d) ℝ | Λ * dual Λ = 1}`, where `dual Λ = η * Λᵀ * η` and `η = indefiniteDiagonal = diag(1, -1, …, -1)`. Its topology is the subtype topology.
- `restricted d` is a Subgroup with carrier `{Λ | IsProper Λ ∧ IsOrthochronous Λ}`, where `IsProper Λ := Λ.1.det = 1` and `IsOrthochronous Λ := 0 ≤ Λ.1 (Sum.inl 0) (Sum.inl 0)`.
- Mathlib defines `IsConnected s := s.Nonempty ∧ IsPreconnected s`.

My statement file is panel_work/reproduce/ReproStmt.lean. It imports only Physlib.Relativity.LorentzGroup.Restricted.Basic and does not copy the frozen spec. It states:
- **StmtA:** `∀ {d : ℕ}, IsConnected ((LorentzGroup.restricted d : Subgroup (LorentzGroup d)) : Set (LorentzGroup d))`
- **StmtA':** the same with an explicit `∀ d`.
- **StmtB:** `∀ d, IsConnected {Λ : LorentzGroup d | Λ.1.det = 1 ∧ 0 ≤ Λ.1 (Sum.inl 0) (Sum.inl 0)}`
- **StmtB':** StmtB with `IsConnected` unfolded to `Nonempty ∧ IsPreconnected`.
- **StmtC (textbook form, in the ambient matrix space):** `∀ d, IsConnected {M : Matrix (Fin 1 ⊕ Fin d) (Fin 1 ⊕ Fin d) ℝ | Mᵀ * minkowskiMatrix * M = minkowskiMatrix ∧ M.det = 1 ∧ 0 ≤ M (Sum.inl 0) (Sum.inl 0)}`
- **eta_is_diag:** `minkowskiMatrix = diagonal (Sum.elim 1 (-1))`, proved in the file.

I compiled and hashed this file before reading checker/ or object/:
```
Wed Oct 14 07:03:01 UTC 2026
rc=0
Wed Oct 14 07:03:29 UTC 2026
Wed Oct 14 07:03:32 UTC 2026
2c2be25ea910a7e8b4292286f4436b9ef607edfb164e1e0fddba8b0344934d63  .../panel_work/reproduce/ReproStmt.lean
```

## 2. My own compile and check

The claim files are unchanged. All four hashes equal the ones in CLAIM.md, and I re-hashed them after all runs, at 07:14:39:
```
8bef4eda0ca4af1b97b2b4911b75917a647fb74d73b3d56273c6779c313dc38d  object/RestrictedIsConnected.lean
fe8150105b484db9421b2b91e140666f4a74d2b596a531b57494a505b89bca52  checker/spec_restricted_isConnected.lean
fe7aaf99a0b13f23a3c232a5a5fbfa8d33750e5f809cc0bf36e3c87ef9a828de  checker/lean_claim_check.py
e41850ba01879f3a9a6c3934efd85aab5b4a1a48c8d8a4621da63f7c5296f1c9  source/status_page_Restricted_Basic.lean
```

I copied the spec to panel_work/reproduce/build/V3R1T4SSpec.lean and the object to panel_work/reproduce/build/V3R1T4SClaim.lean. I compiled each from `<ws>`/lean/physlib with:

`sh <ws>/tools/lean_slot.sh lake env sh -c 'LEAN_PATH="<build>:<reproduce>:$LEAN_PATH" exec lean --root=<build> -o <build>/X.olean <build>/X.lean'`

Both compiled with exit code 0 and printed nothing: no warnings and no `sorry`.
```
Wed Oct 14 07:06:39 UTC 2026
spec rc=0
Wed Oct 14 07:07:16 UTC 2026
Wed Oct 14 07:07:20 UTC 2026
claim rc=0
Wed Oct 14 07:07:43 UTC 2026
```

My check file is panel_work/reproduce/build/ReproCheck.lean. It imports ReproStmt and V3R1T4SClaim, then does the following:
- **StmtA:** `theorem repro_A : ReproStmt.StmtA := V3R1T4S.claim`, a plain term that only unfolds definitions.
- **StmtA' and StmtB:** unfold, then `exact`.
- **StmtB':** `⟨h.nonempty, h.isPreconnected⟩`.
- **StmtC:** take the image of the set under the continuous `Subtype.val`, then use Physlib's `mem_iff_transpose_mul_minkowskiMatrix_mul_self`.
- **Spec equality:** `theorem spec_eq_mine : V3R1T4S.spec = ReproStmt.StmtA := rfl`.
- **Expr comparison:** a meta-level check that the two definition bodies are the same term.
- **Constant scan:** every constant that module V3R1T4SClaim adds is scanned for axiom, opaque, quot, unsafe or implemented_by.

Output:
```
Wed Oct 14 07:09:02 UTC 2026
check rc=0
Wed Oct 14 07:10:07 UTC 2026
@V3R1T4S.claim : V3R1T4S.spec
value(ReproStmt.StmtA) == value(V3R1T4S.spec) [alpha-eqv]: true
Expr.equal (binder names+info too): true
type(V3R1T4S.claim) == const V3R1T4S.spec: true
constants from module V3R1T4SClaim: 43
'repro_A' depends on axioms: [propext, Classical.choice, Quot.sound]
'repro_A'' depends on axioms: [propext, Classical.choice, Quot.sound]
'repro_B' depends on axioms: [propext, Classical.choice, Quot.sound]
'repro_B'' depends on axioms: [propext, Classical.choice, Quot.sound]
'repro_C' depends on axioms: [propext, Classical.choice, Quot.sound]
'spec_eq_mine' depends on axioms: [propext, Classical.choice, Quot.sound]
'V3R1T4S.claim' depends on axioms: [propext, Classical.choice, Quot.sound]
'ReproStmt.eta_is_diag' depends on axioms: [propext, Classical.choice, Quot.sound]
```
- No SUSPICIOUS line was printed, so none of the 43 constants is an axiom, opaque, quot or unsafe constant, or carries implemented_by.
- The `pp.explicit` prints of the two statements (in panel_work/reproduce/build/repro_check.log) are identical. Both use `IsConnected`, `instTopologicalSpaceElemMatrixSumFinOfNatNatRealLorentzGroup`, `SetLike.coe`, `Subgroup.instSetLike`, `lorentzGroupIsGroup` and `restricted d`.

**Spec vs. source.** panel_work/reproduce/build/ReproSrcCtx.lean re-elaborates the source's statement text in the source file's own context: namespace LorentzGroup, its three `open`s, and only that module's imports and declarations.
```
Wed Oct 14 07:12:10 UTC 2026
rc=0
Wed Oct 14 07:12:22 UTC 2026
source-context statement: Expr.equal with ReproStmt.StmtA = true
IsConnected resolves to: [IsConnected]
```
So the source statement, my StmtA and the frozen `V3R1T4S.spec` are structurally identical terms: same instances, same `{d : ℕ}` binder. This holds both in the source file's environment and in the full `import Physlib` environment.

**Kernel replay.** The toolchain's `leanchecker -v` replays every new declaration of a module through the kernel, starting from that module's imports.
```
Wed Oct 14 07:15:20 UTC 2026
replaying V3R1T4SClaim
leanchecker rc=0
Wed Oct 14 07:16:31 UTC 2026
replaying V3R1T4SSpec
V3R1T4SSpec rc=0
Wed Oct 14 07:16:58 UTC 2026
replaying Physlib.Relativity.LorentzGroup.Restricted.Basic
Physlib.Relativity.LorentzGroup.Restricted.Basic rc=0
Wed Oct 14 07:17:08 UTC 2026
replaying Physlib.Relativity.LorentzGroup.Restricted.FromBoostRotation
Physlib.Relativity.LorentzGroup.Restricted.FromBoostRotation rc=0
Wed Oct 14 07:17:17 UTC 2026
replaying Physlib.Relativity.Tensors.RealTensor.Velocity.Basic
Physlib.Relativity.Tensors.RealTensor.Velocity.Basic rc=0
Wed Oct 14 07:17:28 UTC 2026
```

## 3. Provided checker, run exactly as REPRODUCE.md says

`. <ws>/tools/lean_env.sh; export ELAN_NO_OVERRIDE_NOTICE=1; cd <claim folder>; sh <ws>/tools/lean_slot.sh python3 -I checker/lean_claim_check.py --physlib <ws>/lean/physlib --spec checker/spec_restricted_isConnected.lean --candidate object/RestrictedIsConnected.lean`

Run 1, saved in panel_work/reproduce/checker_run1.log:
```
Wed Oct 14 07:10:21 UTC 2026
checker rc=0
Wed Oct 14 07:10:59 UTC 2026
spec compile: exit 0
candidate compile: exit 0
check file: exit 0
'V3R1T4S_check' depends on axioms: [propext, Classical.choice, Quot.sound]
axioms: ['Classical.choice', 'Quot.sound', 'propext']
PASS
```

Run 2, saved in panel_work/reproduce/checker_run2.log, ran from 07:12:29 to 07:14:20 UTC with `checker rc=0` and the same lines. `cmp` printed `RUN1 == RUN2 (byte-identical)`, so the result is deterministic.

## 4. Proof audit of object/RestrictedIsConnected.lean (269 lines)

**What the file contains.** It imports only `Physlib` and `V3R1T4SSpec`. Besides those imports it has only:
- `open Matrix`, one namespace and `noncomputable section`;
- `variable {n : ℕ}`;
- two definitions (`hh` and `pairPath`), plus lemmas and theorems.

**What it does not contain.** I scanned the source, including comments, and found none of these:
- `axiom`, `sorry`, `admit`, `instance`, `attribute` or `@[...]`;
- `notation`, `macro`, `syntax`, `elab`, `set_option`;
- `native_decide` or `decide`, `implemented_by`, `extern`, `opaque`, `unsafe`, `partial`, `private`;
- `#eval` or `run_cmd`.

**Characters.** The only non-ASCII characters are standard Lean/Mathlib symbols. There are no invisible or look-alike characters.

**semiformal_result.** The object does not use Physlib's `semiformal_result`. That command's elaborator adds `axiom helper` only inside `withoutModifyingEnv`, so no constant named `LorentzGroup.restricted_isConnected` exists. The axiom lists above show no `helper`.

**Re-derivation of the main steps:**
- `hh w = 1 − (2/(w·w)) w wᵀ`. This is the identity when w = 0, because 2/0 = 0 in Lean.
  - It is symmetric.
  - Applying it twice gives back x, because w·(hh x) = −w·x when w·w ≠ 0. So hh w is orthogonal.
  - For w ≠ 0, the matrix determinant lemma gives det = 1 + w·(−2w/(w·w)) = −1.
- If |a| = |b| and a ≠ b, then (a−b)·(a−b) = 2(a−b)·a, so hh(a−b) maps a to b.
- `elim_general` is Householder QR, proved by induction on k for every A in SO(n) that fixes e_i for all i ≥ k:
  - **k = 0:** A = 1.
  - **If A e_k = e_k:** apply the induction hypothesis directly.
  - **Otherwise:** let w = A e_k − e_k. Orthogonality gives w ⊥ e_i for i > k, so hh w · A fixes e_i for all i ≥ k.
    - If k = 0, this forces A = hh w, which has det −1. That is a contradiction.
    - If k > 0, let A2 = hh e_0 · hh w · A. Then A2 is in SO(n), still fixes e_i for i ≥ k (since e_0 ⊥ e_i), and A = hh w · hh e_0 · A2. The induction hypothesis applies to A2, and the step hypothesis then applies (n > 1 holds because 0 < k < n).
  - Taking k = n covers every A in SO(n).
- `pair_joined`:
  - If the segment (1−t)u + tv passes through 0, then v is a nonzero multiple of u. So hh v = hh u and the pair equals 1.
  - Otherwise t ↦ hh u · hh((1−t)u + tv) is a continuous path inside SO(n) from 1 to hh u · hh v. The denominator is nonzero all along the segment.
  - Combined with `Joined.mul`, every A in SO(n) is joined to 1. So SO(n) is path connected for every n, including 0 and 1.
- Physlib supplies the homeomorphism `LorentzGroup.toBoostRotation : restricted d ≃ₜ Lorentz.Velocity d × SO(d)` and the lemma `Lorentz.Velocity.isPathConnected`. Together these make the product path connected, and `restricted d` is its image under the continuous surjection `toBoostRotation.symm`.
- Path connected implies connected, which includes nonempty. Finally `V3R1T4S.claim := fun {_} => restricted_isConnected_explicit`.

This is the standard argument that SO⁺(1,d) ≅ H^d × SO(d), with both factors path connected. Every step is sound, and the whole proof is kernel-checked.

## 5. Build provenance (Physlib be0f21e, Lean v4.34.1)

- **Commit:** lean/physlib/.git/HEAD is be0f21e5002d6d73b87f2055530c1e8bf7151546. The HEAD log shows the clone at d76538126ef2…, then `from master to FETCH_HEAD`, which checked out be0f21e at 06:07:38.
- **Toolchain:** the lean-toolchain file says leanprover/lean4:v4.34.1, and `lean --version` reports 4.34.1, commit 5045d005….
- **No local modifications:** I ran no git commands. My read-only index parser, panel_work/reproduce/git_index_check.py, compares the git index's blob hashes with the working files. At 07:06:19, and again at 07:17:43, it printed: `index version 2, entries 1259; checked 656 tracked files under ['Physlib/', 'Physlib.lean', 'lakefile.toml', 'lake-manifest.json', 'lean-toolchain']: modified 0, missing 0, untracked 0`.
- **Matches upstream:** at 07:06:27 I fetched five files at commit be0f21e with read-only HTTP GETs; copies are in panel_work/reproduce/upstream_dl/. These are Restricted/Basic, Restricted/FromBoostRotation, LorentzGroup/Basic, Velocity/Basic and Rotations. All five returned `200 … SAME`: they match the local checkout.
- **Build is current:** `lake build --no-build Physlib`, run from 07:05:30 to 07:05:56 UTC, printed `All targets up-to-date (4676 jobs).` with rc=0.
- **Dependencies:** for all 9 packages, .lake/packages/*/.git/HEAD equals the revision in lake-manifest.json. For example, mathlib is at d13f23b723b8a846827a245b89c10fc7d3f11612. Checked at 07:14:39.
- **Nothing changed during my session:** at 07:17:43, HEAD was unchanged, no source file had been modified after 06:08, and no olean had been rebuilt after 06:30.

## Nits (none affects the verdict)

- CLAIM.md's success-criterion paragraph says the page copy is "saved in `data/status_page_Restricted_Basic.lean`". In claim/ it is actually source/status_page_Restricted_Basic.lean. The status-record bullet gives the correct path, and the file's content and hash match.
- The checker creates and deletes its temporary folder under `<ws>`/lean/tmp, outside claim/. This is harmless.
- Another process rewrote lean/physlib/.git/FETCH_HEAD at 07:03:30, during my session. HEAD and the working tree were not affected (checked above).

## Verdict

- The object is present and every hash matches CLAIM.md.
- The proved statement is structurally identical to the published one and to my independently written statement, including its textbook matrix form (StmtC). It holds for every d : ℕ.
- The only axioms used are propext, Classical.choice and Quot.sound.
- The provided checker passed twice with byte-identical output, and the independent kernel replay was clean.
- The proof is sound on review.

I found no mismatch, no missing object and no non-determinism.

pass: true
