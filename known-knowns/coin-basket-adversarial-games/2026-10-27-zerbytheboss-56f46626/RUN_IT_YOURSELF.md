# Run It Yourself — `coin-basket-adversarial-games`

## 1. Quick Verification (Pure Python Standard Library)
To verify all results, first-principles game rules, calibration terms, and newly established values in under 1 second:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
All first-principles game rules, calibration sequences, and new terms verified successfully.
PASS
```

## 2. Recomputing the Exact Minimax Values from Source (Compiled Rust)
To rebuild and run the full high-performance decision-bracket minimax solver from scratch:

```sh
cd how-we-built-it/code
rustc -O -C target-cpu=native solve_a392305.rs -o solve_a392305
./solve_a392305
```

This recomputes the exact minimax margin values $A392305(17)=7, A392305(18)=7, A392305(19)=8, A392305(20)=8$ directly over the quotiented game graph.
