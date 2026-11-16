# Pre-Registration: `leancamcombi-bkr-reimer-inequality`

- `frozen_utc`: `2026-11-15T15:08:30Z`
- `target_id`: `leancamcombi-bkr-reimer-inequality`
- `null_test`: not needed because kernel-checked formal proof in Lean 4

## Success Criterion (Verbatim from `bank/targets.json`)

Success means a sorry-free proof of `Finset.card_certificator_le` exactly as stated on live LeanCamCombi master, re-fetched immediately before claiming (the statement and the certificator definition are diff-checked). Issue #34 must still be open with no PR proving the lemma. The proof must compile with `lake build` at the pinned toolchain and manifest, and `#print axioms` must show only propext/Classical.choice/Quot.sound (no native_decide, no new axiom).

## Partial Wins (Verbatim from `bank/targets.json`)

- **p1:** The inequality for up-sets: if 𝒜 and ℬ are both upper sets, 2^n · #(𝒜 □ ℬ) ≤ #𝒜 · #ℬ (the original van den Berg-Kesten case; IsUpperSet.certificator_eq_disjSups in the file rewrites 𝒜 □ ℬ as 𝒜 ○ ℬ), proved sorry-free as a separate lemma.

## Exact Deterministic Referee (`verify-it-yourself/run_checks.sh` + `verify_leancamcombi.py`)

A claim passes (`PASS`, exit status `0`) if and only if all five mechanical gates succeed (`FAIL`, exit status `1` otherwise):

1. **Object & Manifest Integrity**: `object/proof_manifest.json` and `object/VanDenBergKesten.lean` match exact byte size and SHA-256 digest.
2. **Forbidden-Token Scan**: `object/VanDenBergKesten.lean` (both raw and comment-stripped) contains zero occurrences of `sorry`, `admit`, `axiom`, `native_decide`, `ofReduceBool`, `implemented_by`, `extern`, or `skipKernelTC`.
3. **Pinned Toolchain, Manifest & Verbatim Diff Audit**:
   - `LeanCamCombi` (`cam-combi`) `master` HEAD matches `0a42535119073f677dd60a28acbbdcda11b87f60`, `lean-toolchain` is `leanprover/lean4:v4.36.0-rc2`, and `mathlib` revision in `lake-manifest.json` is `dc2a600cfb9d99eb348ee7cb84b28167ad205265`.
   - Every upstream definition and theorem signature in `CamCombi/PlainCombi/VanDenBergKesten.lean` — specifically `Finset.certificator`, `scoped[FinsetFamily] infixl:70 " □ "`, all existing lemmas, and the exact declaration `lemma card_certificator_le : 2 ^ Fintype.card α * #(𝒜 □ ℬ) ≤ #𝒜 * #ℬ` — matches `data/VanDenBergKesten.lean` (`sha256: 9c109ea9c6cb4cf479a6b3d07a5a581e28b41106cb82c54c7ca92c8da91421d2`) verbatim except that `:= sorry` is replaced by a complete proof.
4. **Clean `lake build` & Linter Compilation**:
   - Compiling the patched `CamCombi/PlainCombi/VanDenBergKesten.lean` (in an isolated temporary/restored overlay against `LeanCamCombi` with all `lakefile.toml` options including `weak.linter.mathlibStandardSet = true`, `autoImplicit = false`, `relaxedAutoImplicit = false`) succeeds with exit code `0` and zero warnings/errors.
5. **Kernel Type & Axiom Check**:
   - `#check @Finset.card_certificator_le` matches the exact upstream type signature and `#print axioms Finset.card_certificator_le` lists only a subset of `{propext, Classical.choice, Quot.sound}`.
