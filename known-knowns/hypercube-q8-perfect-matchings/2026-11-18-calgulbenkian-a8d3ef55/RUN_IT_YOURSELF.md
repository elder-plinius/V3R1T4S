# Run It Yourself

All commands below run from this folder in a fresh POSIX shell using only the Python 3 standard library (and an optional C99 compiler if rebuilding the C99 permanent binary).

## 1. Run the standalone dual-engine verifier (~0.6 seconds)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
OK: Full-cube A005271(1..5) reproduced by both Engine 1 and Engine 2 (1, 2, 9, 272, 589185)
OK: Q_5 |Fix(P_5)| = 0 (Engine 1 == Engine 2), mod 5 = 0 == A005271(5) mod 5
OK: Q_6 |Fix(P_5)| = 836 (Engine 1 == Engine 2), mod 5 = 1 == A005271(6) mod 5
OK: Q_7 |Fix(P_5)| = 5741584 (Engine 1 == Engine 2), mod 5 = 4 == A005271(7) mod 5
OK: Q_8 |Fix(P_5)| = 743141892135168 (Engine 1 == Engine 2), mod 5 = 3
VERIFIED: A005271(8) == 3 (mod 5) via |Fix_{M(Q_8)}(P_5)| = 743141892135168
PASS
```

## 2. Rebuild and run the two discovery engines from scratch

### Engine A2 (Pure Python 256-bit hypercube vertex-mask DP, ~0.5 seconds)

```sh
python3 how-we-built-it/q8_bitmask_dp.py
```

### Engine A1 (C99 Gray-code Glynn permanent on full `Q_1..Q_6` and Sylow quotients `Q_5..Q_8`, ~3 seconds)

```sh
cc -O3 -Wall -Wextra -std=c99 how-we-built-it/q8_sylow_perm.c -o q8_sylow_perm
./q8_sylow_perm
rm -f q8_sylow_perm
```
