# Run It Yourself — Site Percolation Threshold of 2-Uniform Tiling #41

## 1. Verify the Results
From this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

The checker runs in $< 1$ second using only the Python 3 standard library (`json`, `math`, `hashlib`).
The final line of output is:
```text
PASS
```

## 2. Rebuild the Numerical Calculations from Scratch
To re-run the two independent computational methods from first principles:

```sh
# Method 1: Newman-Ziff Wrapping-Probability FSS on Periodic Tori
cd how-we-built-it/nz_percolation
cargo run --release -- --calibrate
cargo run --release -- --fss-tiling41

# Method 2: Exact Jacobsen-Scullard Critical Polynomial Roots
cd ../crit_poly
cargo run --release
```

Both methods verify the certified threshold $p_c$ to stated one-sigma uncertainty $\le 2 \times 10^{-6}$.
