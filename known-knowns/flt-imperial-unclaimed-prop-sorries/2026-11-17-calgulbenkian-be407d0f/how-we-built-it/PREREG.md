# Pre-Registration: `flt-imperial-unclaimed-prop-sorries`

- `frozen_utc`: `2026-11-16T03:00:51Z`
- `target_id`: `flt-imperial-unclaimed-prop-sorries`
- `null_test`: not needed because kernel-checked formal proof in Lean 4

## Success Criterion (Verbatim from `wave9_candidates.json`)

Success means a patch that replaces exactly one Prop-valued `sorry` (a theorem, lemma or Prop-valued instance, never a sorry inside a def or structure) in a declaration on live FLT main, re-fetched immediately before claiming. At that moment the declaration must not be touched by any open FLT pull request, must not be named in an assigned or claimed issue, and must not already be proved in the repository under another name (as the PGL2 Defs/Proofs pair is). Its statement must not depend on a sorried definition (isCorepresentable_narrowSLiftFunctor and B4_proof do on 2026-10-30). The instance IsQuaternionAlgebra E (E ⊗[F] D) is excluded while issue #631 is open. The statement must be unchanged (diff-checked). The project must compile with `lake build` at the pinned lean-toolchain and lake-manifest. `#print axioms` on the declaration must show only a subset of {propext, Classical.choice, Quot.sound}: no sorryAx, no knownin1980s, Mazur_statement or Odlyzko_statement, no new axiom, no native_decide. No PR is opened and no issue is claimed. The claim is for the checked patch.

## Partial Wins (Verbatim from `wave9_candidates.json`)

- **p1:** Group.subsingleton_of_pow_prime_eq_one (or its additive version, which @[to_additive] generates) proved sorry-free in the FLT repo with the statement unchanged, using only Mathlib and FLT lemmas that are already sorry-free.
- **p2:** A sorry-free Lean proof, in a separate file that compiles against FLT main, of de Smit-Lenstra Prop. 2.3(1) for one explicit finite group G (e.g. G cyclic of prime order), stated through the FLT `deformationFunctor` API: the special case is corepresentable.

## Target Declaration & Exact Deterministic Referee (`verify-it-yourself/run_checks.sh` + `verify_flt_subsingleton.py`)

Target declaration: `Group.subsingleton_of_pow_prime_eq_one` (together with its `@[to_additive]`-generated `AddGroup.subsingleton_of_nsmul_prime_eq_zero`) in `FLT/Patching/Utils/CompactHausdorffRings.lean`.

A claim passes (`PASS`, exit status `0`) if and only if all five mechanical gates succeed (`FAIL`, exit status `1` otherwise):

1. **Object & Manifest Integrity**: `object/proof_manifest.json` and `object/CompactHausdorffRings.lean` match exact byte size and SHA-256 digest.
2. **Forbidden-Token Scan**: `object/CompactHausdorffRings.lean` (both raw and comment-stripped) contains zero occurrences of `sorry`, `admit`, `axiom`, `native_decide`, `ofReduceBool`, `implemented_by`, `extern`, or `skipKernelTC`, and preserves the exact three upstream `public import` lines.
3. **Pinned Toolchain, Manifest & Verbatim Diff Audit**:
   - `ImperialCollegeLondon/FLT` `main` HEAD matches `a3210204ad8876e851e32f73dd97d882bf1ccd0a`, `lean-toolchain` is `leanprover/lean4:v4.35.0`, and `mathlib` revision in `lake-manifest.json` is `56a005855ea17e0b0958f73ec801ae140b0a1679`.
   - Every upstream docstring, attribute, and theorem/def/instance signature in `FLT/Patching/Utils/CompactHausdorffRings.lean` (`sha256: 72b11ca144f518793a167af9109a5b31fa4e3b03377ef4ecd3e99bcf9c002eda`) — specifically `@[to_additive] theorem Group.subsingleton_of_pow_prime_eq_one` and all downstream declarations (`Group.totallyDisconnected_of_pow_prime_eq_one`, `Group.rootable`, `CommGroup.no_compact_automorphisms`, and `instance : TotallyDisconnectedSpace R`) — matches upstream verbatim except that `sorry` in `Group.subsingleton_of_pow_prime_eq_one` is replaced by a complete proof.
4. **Clean `lake build` & Linter Compilation**:
   - Staging `object/CompactHausdorffRings.lean` into a clean `FLT` checkout (restoring `FLT` git-clean in a `finally` block) and running `LEAN_NUM_THREADS=2 lake build FLT.Patching.Utils.CompactHausdorffRings` plus `lake env lean` with all `lakefile.toml` options (`weak.linter.flexible = true`, `weak.linter.mathlibStandardSet = true`, `warn.sorry = true`, `autoImplicit = false`, `relaxedAutoImplicit = false`) succeeds with exit code `0` and zero warnings/errors.
5. **Kernel Type & Axiom Check**:
   - `#check @Group.subsingleton_of_pow_prime_eq_one` and `#check @AddGroup.subsingleton_of_nsmul_prime_eq_zero` match their exact upstream canonical kernel types (`pp.fullNames true`, `pp.universes true`), and `#print axioms` on both declarations (as well as downstream `Group.totallyDisconnected_of_pow_prime_eq_one`) lists only a subset of `{propext, Classical.choice, Quot.sound}`.
