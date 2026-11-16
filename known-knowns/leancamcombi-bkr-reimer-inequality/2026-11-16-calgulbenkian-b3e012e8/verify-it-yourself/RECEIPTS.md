# Verification Receipts: `leancamcombi-bkr-reimer-inequality`

Command executed from the package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Exit code: `0`

Captured standard output:

```text
[1/5] Manifest & object integrity verified: sha256=b3e012e83c4ef62cb15af4da57291f28795c40447c4696345a8bb07199f4f4d8 (47641 bytes)
[2/5] Forbidden-token & public-import hygiene audit passed (0 forbidden tokens)
[3/5] Upstream pinned environment & verbatim diff verified (commit=0a4253511907, toolchain=leanprover/lean4:v4.36.0-rc2)
[4/5] Lean 4 kernel & mathlibStandardSet linter build succeeded (exit=0, warnings=0)
[5/5] Axiom audit passed: 'Finset.card_certificator_le' depends on axioms: ['propext', 'Classical.choice', 'Quot.sound']
PASS
```
