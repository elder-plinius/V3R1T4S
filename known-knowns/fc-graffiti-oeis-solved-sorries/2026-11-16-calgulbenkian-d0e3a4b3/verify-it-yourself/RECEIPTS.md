# Verification Receipts: `fc-graffiti-oeis-solved-sorries`

Command executed from the package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Exit code: `0`

Captured standard output:

```text
[1/5] Manifest & object integrity verified: sha256=d0e3a4b3ef31bab45d3fb0a942cb1cb804b321d7d6e1004cdac8f5b01a85b31d (17593 bytes)
[2/5] Forbidden-token & import hygiene audit passed (0 forbidden tokens)
[3/5] Upstream pinned environment & verbatim statement match verified (commit=e028240a6182, toolchain=leanprover/lean4:v4.33.1)
[4/5] Lean 4 kernel & FC linter build succeeded (exit=0, warnings=0)
[5/5] Axiom audit passed: 'WrittenOnTheWallII.GraphConjecture25.conjecture25' depends on axioms: ['propext', 'Classical.choice', 'Quot.sound']
PASS
```
