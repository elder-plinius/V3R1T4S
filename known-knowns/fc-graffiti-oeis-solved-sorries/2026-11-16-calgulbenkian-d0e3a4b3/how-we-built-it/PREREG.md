# Pre-Registration: `fc-graffiti-oeis-solved-sorries`

frozen_utc: 2026-11-15T14:19:28Z
target_id: fc-graffiti-oeis-solved-sorries
target_theorem: WrittenOnTheWallII.GraphConjecture25.conjecture25
upstream_file: FormalConjectures/WrittenOnTheWallII/GraphConjecture25.lean
upstream_commit: e028240a61822d970c933f4656f51da025cf200b
null_test: not needed because kernel-checked formal proof in Lean 4

## Frozen Success Criterion (verbatim from `bank/targets.json`)

Success means a verbatim restatement (diffed against the live FC main branch re-fetched immediately before claiming) of one WrittenOnTheWallII or OEIS theorem tagged research solved, ending in `sorry`, with no formal_proof attribute and not the subject of any open FC pull request that proves it or links a proof (searched on GitHub immediately before claiming), proved in full. Lean's kernel is the referee: the submitted file must compile with `lake build` against the repository's pinned lean-toolchain and lake-manifest (Mathlib rev as pinned, no edits to the statement, no new `axiom`, no `sorry`/`admit`, no `native_decide`/`Lean.ofReduceBool`, no `implemented_by`/`extern` tricks, no `set_option debug.skipKernelTC`), and `#print axioms <thm>` must list only a subset of {propext, Classical.choice, Quot.sound}.

## Exact Deterministic Referee & Thresholds

1. **Statement Equivalence**: Exact verbatim declaration header and type of `WrittenOnTheWallII.GraphConjecture25.conjecture25` compared against `data/GraphConjecture25.lean` (SHA-256 `4e107c778baacb7178f63608f320a5dd047d8c868face022f9612394ff57298c`).
2. **Forbidden-Token Audit**: Zero occurrences of `sorry`, `admit`, `axiom`, `native_decide`, `ofReduceBool`, `implemented_by`, `extern`, `skipKernelTC`.
3. **Lean 4 Kernel Check**: Compiles with exit code `0` under `formal-conjectures` pinned toolchain (`leanprover/lean4:v4.33.1`) and `lake-manifest.json` (`mathlib` rev `0df444a360eaa60ab8c11dca51a86af692955474`), and `#print axioms WrittenOnTheWallII.GraphConjecture25.conjecture25` outputs exclusively axioms within `{propext, Classical.choice, Quot.sound}`.
4. **Corruption Sensitivity**: Mutating any digit of `object/proof_manifest.json` or `object/Solution.lean` causes `sh verify-it-yourself/run_checks.sh` to exit non-zero with final line `FAIL`.
