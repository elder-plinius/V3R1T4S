# Preregistration: `erdos-7-odd-covering-system`

- **Frozen UTC Timestamp**: `2026-11-19T00:07:10Z`
- **Target ID**: `erdos-7-odd-covering-system`
- **Status Source**: `https://www.erdosproblems.com/7` (fetched `2026-11-18T23:58:16Z`, HTTP `200`, SHA256 `df388eda0f656abab95b742da8c20c5440f90eff4e9ca267b8cadb73a7f8f329`)

## 1. Criteria (from `repo/bank/targets.json`)
- **Full Success Criterion**:
  "An explicit finite list of (a_i, n_i) with distinct odd n_i exceeding 1 that covers Z, verified by two independent exact checkers. Alternatively, a complete axiom-free proof of impossibility."
- **Partial Win `p1`**:
  "A rigorous proof, checked line by line or in Lean without extra axioms, that L = lcm(n_i) of any odd distinct-moduli covering has at least 10 distinct prime factors (the forum claims at least 9, unrefereed)."
- **Partial Win `p2`**:
  "A rigorous proof raising the lower bound on L strictly above 11,486,475 (Egeozturk, forum Aug 2026), rechecked by independent code."
  *(Strict Self-Imposed Novelty Gate for `p2`)*: Because Michael Schroeder's Sep 2026 Zenodo preprint `10.5281/zenodo.22759614` claims `L` is at least `9,704,539,845`, we require any `p2` claim to prove from first principles (with zero external axioms) `L` at least `B` with `B` at least `10,000,000,000` (`10^10`), strictly exceeding both `11,486,475` and `9,704,539,845`.

## 2. Exact Verification and Soundness Protocol
1. **Zero External Axioms**: Every mathematical reduction (finite-group prime replacement onto the first `r` odd primes, pure prime-power completion on `Z/NZ`, capped conditional fibre kernels, and nested convex comparison) must be proved completely from first principles with zero reliance on unrefereed preprints or unproved external theorems.
2. **Exact Arithmetic Only**: Zero floating-point arithmetic in any proof step or certificate check. All finite inequalities must be checked in exact arbitrary-precision integer or rational arithmetic.
3. **Dual Zero-Shared-Code Standalone Verifiers**: Any claimed proof and certificate must be verified end-to-end by two genuinely independent standalone verifiers sharing zero code (a standalone ISO C99 exact 128-bit integer verifier and a standalone Python 3 standard-library `fractions.Fraction` verifier) invoked by `sh verify-it-yourself/run_checks.sh` in under `180` seconds, printing `PASS` on the clean certificate and rejecting corrupted certificates with non-zero exit and `FAIL`.

## 3. Null Model Declaration
null_test: not needed because any claim is a deterministic mathematical theorem with an exact integer and rational proof certificate verified exhaustively without statistical or heuristic scoring.
