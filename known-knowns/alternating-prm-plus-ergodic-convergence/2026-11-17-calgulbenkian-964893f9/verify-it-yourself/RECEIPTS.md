# Verification Receipts: `alternating-prm-plus-ergodic-convergence` (Partial Win `p2`)

Command executed from an isolated clean copy of the `claim/` directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Exit code: `0`

Captured standard output:

```text
[1/5] Manifest & 119-file object integrity verified: bundle_sha256=28e82bc4279d1b8ce51304f2dc792fe23a91ec7bf2f8208181a141aa1b4ea443 (1398472 bytes)
[2/5] Forbidden-token hygiene audit passed across all 119 Lean files (0 forbidden tokens)
[3/5] Defs.lean paper-update diff & 1,000-iteration float64/Decimal cross-check passed (interval_width=4.372e-15, float64_err=9.992e-16)
[4/5] Clean-room Lean 4 kernel build of all 119 modules succeeded (exit=0, warnings=0, 798.0s)
[5/5] Kernel signature & axiom audit passed on all 4 theorems: axioms=['propext', 'Classical.choice', 'Quot.sound']
PASS
```
