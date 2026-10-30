# Run It Yourself — square-grid-lattice-gas-exact-counts-oeis

Exact reproduction commands from this folder in a fresh shell.

## 1. Fast Standalone Verification (< 1 second)
Run the pure Python verifier from this package folder:
```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```
[PASS] Lens 1 (p1): a(1..14) reproduced, world records a(15) [43 digits] & a(16) [49 digits] verified
[PASS] Lieb constant convergence: W15=1.546987 (0.48%), W16=1.546093 (0.42%)
[PASS] Lens 2 (p2): A089980 Row 28 (k=1..20) and A210662 Row 28 (k=1..18) verified
ALL CHECKS PASSED.
PASS
```

## 2. Rebuilding the Terms from Scratch in Rust
To run the square ice flux transfer matrix generator in Rust:
```sh
cd how-we-built-it
rustc -O square_ice_flux.rs -o square_ice_flux
./square_ice_flux
```
Execution time: ~5 seconds for $n=1..14$, ~25 seconds for $n=15$, ~110 seconds for $n=16$.
Outputs match all terms in `object/a054759_results.json` digit-for-digit.
