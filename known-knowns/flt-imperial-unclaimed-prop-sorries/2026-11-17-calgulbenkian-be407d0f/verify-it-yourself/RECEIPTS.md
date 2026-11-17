# Verification Receipt (`flt-imperial-unclaimed-prop-sorries`)

Command: `sh verify-it-yourself/run_checks.sh`

```text
[1/5] Pinned FLT checkout & manifest schema verified (commit=a3210204ad88, toolchain=leanprover/lean4:v4.35.0)
[2/5] Forbidden-token & verbatim upstream statement/downstream diff audit passed
[3/5] Zero-warning linter check & full FLT repository lake build succeeded (LEAN_NUM_THREADS=2, git-clean)
[4/5] Kernel signature & axiom audit passed: Group.subsingleton_of_pow_prime_eq_one=['propext', 'Classical.choice', 'Quot.sound'], AddGroup.subsingleton_of_nsmul_prime_eq_zero=['propext', 'Classical.choice', 'Quot.sound']
[5/5] Object SHA-256 & byte-count verified: sha256=be407d0f4d9d2b6bac5c1b7b64f7ac9361ad711a3c8c4bcf05d8713729bc8bbd (47848 bytes)
PASS
```
