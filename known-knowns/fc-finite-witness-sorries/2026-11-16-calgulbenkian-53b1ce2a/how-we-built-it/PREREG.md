# Pre-Registration: `fc-finite-witness-sorries`

frozen_utc: 2026-11-15T14:19:28Z
target_id: fc-finite-witness-sorries
target_theorem: RamseyNumbers.ramsey_number_six_six_lower_bound
upstream_file: FormalConjectures/Wikipedia/RamseyNumbers.lean
upstream_commit: e028240a61822d970c933f4656f51da025cf200b
null_test: not needed because kernel-checked formal proof in Lean 4

## Frozen Success Criterion (verbatim from `bank/targets.json`)

Success means a Lean file that restates one FC theorem verbatim (diffed against the live main branch of https://github.com/google-deepmind/formal-conjectures re-fetched immediately before claiming) where that theorem is tagged research solved, lives outside FormalConjectures/ErdosProblems, WrittenOnTheWallII and OEIS, ends in `sorry`, has no `formal_proof` attribute, and is not the subject of any open FC pull request that proves it or adds a formal_proof link for it (searched on GitHub immediately before claiming), and proves it. Lean's kernel is the referee: the submitted file must compile with `lake build` against the repository's pinned lean-toolchain and lake-manifest (Mathlib rev as pinned, no edits to the statement, no new `axiom`, no `sorry`/`admit`, no `native_decide`/`Lean.ofReduceBool`, no `implemented_by`/`extern` tricks, no `set_option debug.skipKernelTC`), and `#print axioms <thm>` must list only a subset of {propext, Classical.choice, Quot.sound}. Heavy computation must go through `decide`, `Decidable` instances or proof-by-reflection checked by the kernel; `native_decide` is forbidden.

## Exact Deterministic Referee & Thresholds

1. **Statement Equivalence**: Exact verbatim declaration header and type of `RamseyNumbers.ramsey_number_six_six_lower_bound` compared against `data/RamseyNumbers.lean` (SHA-256 `36d0764d496b8a96b5dd9eaa804dfe4fccffbf8cb4744b9de146cfdaa9def43d`).
2. **Forbidden-Token Audit**: Zero occurrences (outside comments, and checked across the entire proof file) of `sorry`, `admit`, `axiom`, `native_decide`, `ofReduceBool`, `implemented_by`, `extern`, `skipKernelTC`.
3. **Lean 4 Kernel Check**: Compiles with exit code `0` under `formal-conjectures` pinned toolchain (`leanprover/lean4:v4.33.1`) and `lake-manifest.json` (`mathlib` rev `0df444a360eaa60ab8c11dca51a86af692955474`), and `#print axioms RamseyNumbers.ramsey_number_six_six_lower_bound` outputs exclusively axioms within `{propext, Classical.choice, Quot.sound}`.
4. **Corruption Sensitivity**: Mutating any digit of `object/proof_manifest.json` or `object/Solution.lean` causes `sh verify-it-yourself/run_checks.sh` to exit non-zero with final line `FAIL`.
