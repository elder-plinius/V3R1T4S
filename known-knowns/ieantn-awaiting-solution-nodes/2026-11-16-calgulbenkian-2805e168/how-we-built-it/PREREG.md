# Pre-Registration: `ieantn-awaiting-solution-nodes`

- `frozen_utc`: `2026-11-15T16:39:28Z`
- `target_id`: `ieantn-awaiting-solution-nodes`
- `selected_node_version`: `ZetaHadamard.v1`
- `selected_challenge_theorem`: `ZetaHadamard.v1.challenge_logDeriv_partial_fractions`
- `null_test`: not needed because formal Lean 4 proof verified by comparator

## Success Criterion (Verbatim from `bank/targets.json`)

Success means a Lake project under Solutions/ < Family > . < version> for one node version. Re-fetch live IEANTN main immediately before claiming. At that point the node version must have no Solutions directory, no lean-comparator receipt, no open issue that is assigned to or claimed for it (a closed issue, such as #64, does not count), and no open PR that touches it. leanprover/comparator must accept it against the node's generated Challenge.lean: same statements, only propext/Classical.choice/Quot.sound, and the node's imports used only as the hypotheses the scaffold provides. Excluded: nodes in the RosserSchoenfeld families (they overlap the PNT+ bank entry), the claimed BKLNW, FKS, Buthe and DudekPlatt families while their issues are open and assigned, and statements that are the headline problem of an active lean-eval problem. No PR is opened.

## Partial Wins (Verbatim from `bank/targets.json`)

- **p1:** CotangentSeries.v1 challenge_cot_series_zeta_values proved and accepted by Comparator, provided Mathlib at the pinned revision does not already contain the expansion.
- **p2:** For a node version that meets every exclusion and claim condition of the success criterion and whose evidence is `literature`, a Comparator-accepted proof of at least one of its conclusions as a conditional theorem from the node's declared imports, with the other conclusions of that node left open.

## Exact Deterministic Referee (`verify-it-yourself/run_checks.sh` + `verify_ieantn.py`)

A claim passes (`PASS`, exit status `0`) if and only if all six mechanical gates succeed (`FAIL`, exit status `1` otherwise):

1. **Object & Manifest Integrity**:
   - `object/proof_manifest.json` matches its pinned SHA-256 digest and required schema.
   - Every file in `object/Solutions/ZetaHadamard.v1/` (`lean-toolchain`, `lakefile.toml`, `lake-manifest.json`, `comparator.json`, and all `.lean` source modules) matches its exact byte count and SHA-256 digest recorded in `object/proof_manifest.json`, with no extra or missing files in `object/`. Modifying any byte or digit in any text file in `object/` causes deterministic rejection (`FAIL`, exit status `1`).
2. **Forbidden-Token & Import-Isolation Audit**:
   - Every `.lean` file in `object/Solutions/ZetaHadamard.v1/` (raw and comment-stripped) contains zero occurrences of `sorry`, `admit`, `axiom`, `native_decide`, `ofReduceBool`, `implemented_by`, `extern`, or `skipKernelTC`.
   - Zero `.lean` files import any `IEANTN.Nodes.*` module other than `IEANTN.Nodes.ZetaHadamard.v1.Conclusions` (matching `ZetaHadamard.v1`'s `imports: []`).
3. **Pinned Upstream IEANTN Environment & Statement Integrity**:
   - `IEANTN` checkout is at pinned commit `d60421f10c16f5f6c2cb75f1067a72e24e616391`, `lean-toolchain` is `leanprover/lean4:v4.34.0-rc2`, and `mathlib` revision is `71a80585ee495fc24472fd0eaffc89d94e4fd8d6`.
   - `IEANTN/Nodes/ZetaHadamard/v1/Conclusions.lean` and `IEANTN/Nodes/ZetaHadamard/v1/Challenge.lean` match their exact upstream SHA-256 digests (`7059789de0f72dcaf892319fc7579709698ae7cb2abcc3ac122e548a3ac5af8b` and `3893a9c73633da712806800cd004278a36be0d9ef29454e178211e82fad1fc94`), and `Solutions/ZetaHadamard.v1` does not exist in clean upstream `IEANTN`.
4. **Lake Build (`LEAN_NUM_THREADS=2`)**:
   - Staging `object/Solutions/ZetaHadamard.v1` into `IEANTN/Solutions/ZetaHadamard.v1` and running `LEAN_NUM_THREADS=2 lake build` compiles `Solution` cleanly with exit code `0` and zero `sorry` warnings.
5. **Lean Comparator Kernel Replay & Challenge Equivalence (`leanprover/comparator`)**:
   - Running `comparator` against `challenge_module: "IEANTN.Nodes.ZetaHadamard.v1.Challenge"`, `solution_module: "Solution"`, `theorem_names: ["ZetaHadamard.v1.challenge_logDeriv_partial_fractions"]`, `permitted_axioms: ["propext", "Classical.choice", "Quot.sound"]` exits with code `0` and outputs `"Your solution is okay!"`.
6. **Direct `#print axioms` Check & Clean Restoration**:
   - `#print axioms ZetaHadamard.v1.challenge_logDeriv_partial_fractions` lists only a subset of `{propext, Classical.choice, Quot.sound}`, and the temporary staged directory `IEANTN/Solutions/ZetaHadamard.v1` is removed in a `finally` block leaving `IEANTN` `git status --porcelain` completely empty.
