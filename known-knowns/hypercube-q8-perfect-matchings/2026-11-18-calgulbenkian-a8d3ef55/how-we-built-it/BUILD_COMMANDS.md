# Exact Build and Reproduction Commands

No third-party dependencies are required (standard C99 compiler and Python 3 standard library only).

## 1. Engine A1 — C99 Gray-Code Glynn Permanent (Full `Q_1..Q_6` + Sylow Quotients `Q_5..Q_8`)

```sh
cc -O3 -Wall -Wextra -std=c99 how-we-built-it/q8_sylow_perm.c -o q8_sylow_perm
./q8_sylow_perm
```

Reproduces `A005271(1..6)` (`1, 2, 9, 272, 589185, 16332454526976`) in full-cube permanent mode (~3 seconds) and outputs `|Fix_{M(Q_n)}(P_5)| = 0, 836, 5741584, 743141892135168` for `n = 5, 6, 7, 8` (~0.2 seconds).

## 2. Engine A2 — Zero-Shared-Code Pure Python 256-Bit Hypercube Vertex-Mask DP

```sh
python3 how-we-built-it/q8_bitmask_dp.py
```

Runs directly on the `2^n`-vertex hypercube `Q_n` without permanents or quotient matrices (~0.5 seconds total) and reproduces `|Fix_{M(Q_8)}(P_5)| = 743141892135168` (`mod 5 = 3`).

## 3. Standalone Package Verification

```sh
sh verify-it-yourself/run_checks.sh
```
