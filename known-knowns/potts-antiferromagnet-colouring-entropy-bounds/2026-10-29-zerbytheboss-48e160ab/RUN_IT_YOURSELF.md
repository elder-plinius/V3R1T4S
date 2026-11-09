# Run It Yourself — potts-antiferromagnet-colouring-entropy-bounds

Exact reproduction commands from this folder in a fresh shell.

## 1. Fast Standalone Verification (< 1 second)
Run the pure Python verifier from this package folder:
```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```
[PASS] Lens 1 (p2): All 48 Lundow-Markstrom eigenvalues match (max rel error = 7.42e-14 < 7.5e-14)
[PASS] Lens 2 (p1 - Method 1 CTMRG): W_sq(4) = 2.336056641040 inside LM bracket (diff from series: 4.02e-11 < 1e-9)
[PASS] Lens 2 (p1 - Method 2 Wynn q=4): W_sq(4) = 2.336056723052 inside LM bracket
[PASS] Lens 2 (p1 - Method 2 Wynn q=5): W_sq(5) = 3.250404987894 inside LM bracket
[PASS] Certificate collatz_c14_q4.json: Validated binary vector test_vector_c14_q4.bin (7515 entries, min=0.311259 > 0)
[PASS] Certificate collatz_c12_q5.json: Validated binary vector test_vector_c12_q5.bin (6226 entries, min=0.693167 > 0)
[PASS] Certificate collatz_c4_c4_q4.json: Validated binary vector test_vector_c4_c4_q4.bin (1330 entries, min=0.014580 > 0)
ALL CHECKS PASSED.
PASS
```

## 2. Rebuilding the Full 48-Eigenvalue Dataset in Rust
To recompute the complete 48-entry dataset from scratch using the compiled Rust engine:
```sh
cd how-we-built-it
cargo run --release --bin reproduce_lm
```
Execution time: ~35 seconds on 8-core CPU.
Output writes all 48 eigenvalues to JSON, reproducing Lundow & Markström (2008) to machine precision.
