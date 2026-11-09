# Run It Yourself — levine-hat-two-player-value

Exact reproduction commands from this folder in a fresh shell.

## 1. Fast Standalone Verification (< 1 second)
Run the pure Python checker from this package folder:
```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```
Verified V_{2,4} optimal strategy: 89/256 wins = 89/256 = 0.3476562500
All calibrations h=1..3 verified.
Independent simulation complete: 256/256 games matched.
PASS
```

## 2. Rebuilding the Certificate from Scratch
To run the exhaustive canonical search over all 178,973,355 restricted growth string states in Rust:
```sh
cd how-we-built-it
rustc -O canonical_search.rs -o canonical_search
./canonical_search
```
Execution time: ~2.2 seconds on modern multi-core CPU.
Output confirms max wins = 89 out of 256 with exactly 1,152 attaining canonical strategies.
