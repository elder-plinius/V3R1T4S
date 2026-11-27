# Run It Yourself

1. Verify all primary record codes, companion codes, `SHA256SUMS`, and `--corrupt` rejection (`< 1 s`, Python 3 standard library only):
   ```sh
   sh verify-it-yourself/run_checks.sh
   ```
2. Optionally audit the standalone Lean 4.36.0 kernel proofs (requires Lean `v4.36.0`, zero Mathlib downloads):
   ```sh
   cd lean4_certs
   lake build DeletionCode
   lake env lean AuditAxioms.lean
   lake env leanchecker DeletionCode
   ```
