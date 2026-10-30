# Receipts — `penney-permutations-rotation-conjecture`

Verification run executed cleanly on macOS (Darwin arm64):
```
$ sh verify-it-yourself/run_checks.sh
All 24 S_4 Penney rotation certificates verified successfully!
PASS
```

## Dual Independent Engines
- Compiled Rust engine (`attempts/lens1_rust/`): exact 256-bit arithmetic, complete S_4 certification in 2.3s.
- Pure Python solver (`attempts/lens2_python/`): independent dynamic programming and brute-force permutation validation.
- Zero floating-point rounding errors in integer certificate checks: $A(H) + B(H) + R(H) == H!$ and $2(A(H) + R(H)) < H!$ verified with exact big integers.
