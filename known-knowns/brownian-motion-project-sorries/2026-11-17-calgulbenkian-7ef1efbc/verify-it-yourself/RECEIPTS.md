# Verification Receipt (`brownian-motion-project-sorries`)

Command: `sh verify-it-yourself/run_checks.sh`

```text
[1/5] Pinned checkout & manifest schema verified (commit=8fd8dc52830c, toolchain=leanprover/lean4:v4.36.0-rc2)
[2/5] Forbidden-token & verbatim statement/header/suffix diff audit passed
[3/5] Zero-warning prefix check & full repository lake build succeeded (LEAN_NUM_THREADS=2, git-clean)
[4/5] Kernel signature & axiom audit passed: 'ProbabilityTheory.IsBrownianReal.reflection' depends on axioms: ['propext', 'Classical.choice', 'Quot.sound']
[5/5] Object SHA-256 & byte-count verified: sha256=7ef1efbcd7a5d841a015f7503d6bcf17f46a96cf7c2dfd8838765bf0bd4de25f (49468 bytes)
PASS
```
