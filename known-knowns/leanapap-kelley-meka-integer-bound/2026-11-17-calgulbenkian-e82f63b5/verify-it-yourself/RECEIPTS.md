# Verification Receipts (`leanapap-kelley-meka-integer-bound`)

Command executed from package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Captured output:

```text
[1/5] Pinned LeanAPAP checkout & manifest schema verified (commit=fb5cb9c4f594, toolchain=leanprover/lean4:v4.36.0-rc2)
[2/5] Forbidden-token, import-hygiene & verbatim statement diff audit passed across all 6 files
[3/5] Cold 6-module compilation, zero-warning linter check & full LeanAPAP lake build succeeded (LEAN_NUM_THREADS=2, git-clean)
[4/5] Kernel signature & axiom audit passed: 'int' depends on axioms: ['propext', 'Classical.choice', 'Quot.sound']
[5/5] All 6 object files SHA-256 & byte-counts verified (Integer.lean sha256=e82f63b5324cb2854fa6bfe9c92ec853d49798d350068e10957738abce223240, total_proof_bytes=361067)
PASS
```
