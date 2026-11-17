# Pre-Registration: `brownian-motion-project-sorries`

- `frozen_utc`: `2026-11-16T03:05:15Z`
- `target_id`: `brownian-motion-project-sorries`
- `selected_declaration`: `ProbabilityTheory.IsBrownianReal.reflection`
- `upstream_relpath`: `BrownianMotion/Gaussian/IteratedLogarithm.lean`
- `upstream_commit`: `8fd8dc52830cdd07cf9cc8eadd533e284425fa6f`
- `null_test`: not needed because kernel-checked formal proof in Lean 4

## Success Criterion (Verbatim from `bank/targets.json`)

Success means a patch that replaces the `sorry` in one of Submartingale.uniformIntegrable_stoppedValue, Martingale.ae_tendsto_limitProcess, Martingale.condExp_limitProcess_ae_eq, Martingale.condExp_limitProcess_ae_eq' or IsBrownianReal.reflection on live brownian-motion master, re-fetched immediately before claiming. At that moment the declaration must not be in a file touched by an open PR and must not be the subject of an assigned or claimed issue. The statement must be unchanged (diff-checked). `lake build` must succeed at the pinned toolchain and manifest, and `#print axioms` on the declaration must show only propext/Classical.choice/Quot.sound (no sorryAx, no new axiom, no native_decide). IsStandardGaussian.tail and hasIntegrableSup_const are false as stated and can never be the full win. stoppedValue_min_ae_le_condExp and isStable_submartingale are excluded while issue #263 is claimed.

## Partial Wins (Verbatim from `bank/targets.json`)

- **p1:** hasStronglyMeasurableSupProcess_const proved sorry-free with the statement unchanged, together with a kernel-checked Lean counterexample to hasIntegrableSup_const as stated (e.g. Ω = ℝ, P = volume, c = 1) and a sorry-free proof of the same lemma with [IsFiniteMeasure P] added.
- **p2:** A kernel-checked Lean proof, compiling against the project, of the negation of IsStandardGaussian.tail as stated (exhibit Ω, P, X with HasLaw X (gaussianReal 0 1) P for which the IsEquivalent fails), together with a sorry-free proof of the corrected statement with the factor 1/√(2π).

## Exact Deterministic Referee (`verify-it-yourself/run_checks.sh` + `verify_brownian.py`)

A claim passes (`PASS`, exit status `0`) if and only if all five mechanical gates succeed (`FAIL`, exit status `1` otherwise):

1. **Object & Manifest Integrity**:
   - `object/proof_manifest.json`, `object/IteratedLogarithm.lean`, and `object/IteratedLogarithm.patch` match exact byte counts and SHA-256 digests recorded in `object/proof_manifest.json`.
2. **Forbidden-Token & Verbatim Statement Diff Audit**:
   - Every added line in `object/IteratedLogarithm.patch` and the entire prefix of `object/IteratedLogarithm.lean` prior to `lemma IsStandardGaussian.tail` (both raw and comment-stripped) contain zero occurrences of `sorry`, `admit`, `axiom`, `native_decide`, `ofReduceBool`, `implemented_by`, `extern`, or `skipKernelTC`.
   - Public imports (`BrownianMotion.Gaussian.BrownianMotion`), namespace/variables, the exact declaration header `lemma IsBrownianReal.reflection (hX : IsBrownianReal X P) {t : ℝ≥0} {c : ℝ} (ht : 0 < t) (hc : 0 ≤ c) : P.real {ω | c ≤ ⨆ s ≤ t, (X s ω).toEReal} = 2 * P.real {ω | c ≤ X t ω} :=`, and the entire suffix starting at `lemma IsStandardGaussian.tail` through `end ProbabilityTheory` match upstream `data/IteratedLogarithm.lean` (`sha256: c5a08861fdcc0f8c122c62efd8c0293c859d5f655f9a9635ebfbcdcde3aa5b44`) character-for-character verbatim, and applying `object/IteratedLogarithm.patch` to upstream `data/IteratedLogarithm.lean` reproduces `object/IteratedLogarithm.lean` byte-for-byte.
3. **Pinned Toolchain, Manifest & Checkout Audit**:
   - `brownian-motion` `master` HEAD matches `8fd8dc52830cdd07cf9cc8eadd533e284425fa6f`, `lean-toolchain` is `leanprover/lean4:v4.36.0-rc2`, and `mathlib` revision in `lake-manifest.json` is `6135ffb78e8bcd3fcc8ec02f3f82ea0b0737358b`.
4. **Full `lake build` & Zero-Warning Linter Compilation**:
   - Staging `object/IteratedLogarithm.lean` into `BrownianMotion/Gaussian/IteratedLogarithm.lean` (always restored in a `finally` block so `git status --porcelain` is empty) and running `LEAN_NUM_THREADS=2 lake build` succeeds with exit code `0`.
   - Compiling the sorry-free prefix through `IsBrownianReal.reflection` with all project `lakefile.toml` options (`pp.unicode.fun=true`, `autoImplicit=false`, `relaxedAutoImplicit=false`, `weak.linter.flexible=true`, `weak.linter.mathlibStandardSet=true`, `linter.style.header=false`, `warn.sorry=true`) succeeds with exit code `0` and zero warnings/errors.
5. **Kernel Type & Axiom Check**:
   - `#check @ProbabilityTheory.IsBrownianReal.reflection` matches the exact universe-polymorphic upstream signature, and `#print axioms ProbabilityTheory.IsBrownianReal.reflection` lists only a subset of `{propext, Classical.choice, Quot.sound}`.
