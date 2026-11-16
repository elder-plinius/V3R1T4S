# Verification Receipts: `fc-finite-witness-sorries`

Command executed from the package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Exit code: `0`

Captured standard output:

```text
[1/5] Manifest & object integrity verified: sha256=53b1ce2a8a0e258b3fed499681bbb63ce796625b6bd2f38e093340f483a55275 (17579 bytes)
[2/5] Forbidden-token & import hygiene audit passed (0 forbidden tokens)
[3/5] Upstream pinned environment & verbatim statement match verified (commit=e028240a6182, toolchain=leanprover/lean4:v4.33.1)
[4/5] Lean 4 kernel & FC linter build succeeded (exit=0, warnings=0)
[5/5] Axiom audit passed: 'RamseyNumbers.ramsey_number_six_six_lower_bound' depends on axioms: ['propext', 'Classical.choice', 'Quot.sound']
PASS
```
