# Verification Receipts: `ieantn-awaiting-solution-nodes` (`ZetaHadamard.v1`)

Command executed from the package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Exit code: `0` (elapsed: `153.76s`)

Captured standard output:

```text
[1/6] Object & manifest integrity verified: 21 files (338859 bytes), manifest_sha256=0add02ce82202878aeba6671e7c4ab54c67b85a75d88ae1121949f115a7832b9
[2/6] Forbidden-token & import-isolation audit passed (17 Lean modules, 0 forbidden tokens)
[3/6] Pinned upstream IEANTN verified (commit=d60421f10c16, toolchain=leanprover/lean4:v4.34.0-rc2, mathlib=71a80585ee49)
[4/6] Lake build succeeded cleanly (LEAN_NUM_THREADS=2, exit=0, warnings=0)
[5/6] leanprover/comparator verified IEANTN.Nodes.ZetaHadamard.v1.Challenge vs Solution ('Your solution is okay!')
[6/6] Direct #print axioms check passed (['propext', 'Classical.choice', 'Quot.sound']) & IEANTN restored git-clean
PASS
```
