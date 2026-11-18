# How We Built It

This directory contains the two zero-shared-code C99 discovery engines, the Python algebraic/Burnside audit script, and the pre-registration record (`PREREG.md`). Both C engines use only the C99 standard library plus POSIX `pthread` (and `sys/mman.h` in Engine 2); the audit script uses only the Python 3 standard library.

## 1. Engine 1 — Meet-in-the-Middle Diagonal Pull-DP (`domino_mitm_a.c`)

- **Vertex Order A:** `(x + y + z, z - x, z, x, y)` on `s <= 8`, mirrored from `(5, 5, 6)` down to `s = 9` on `s >= 9`, with 2-vertex outer pinning across the middle independent plane `s = 8` (`peak RAM <= 1.9 GiB`, `<= 4` threads).
- **Moduli:** Prime Set A (`10` distinct 31-bit primes `2147483647 .. 2147483477`, product `~ 2^310.00`).
- **Commands:**

```sh
cc -O3 -Wall -Wextra -pthread how-we-built-it/domino_mitm_a.c -o ./domino_mitm_a
./domino_mitm_a               # runs all 16 OEIS calibration checks including 6x6x6
./domino_mitm_a --solve-667   # runs calibration + full 10-prime A049507(7) computation
rm -f ./domino_mitm_a
```

## 2. Engine 2 — Full End-to-End Tilted-Hyperplane Push-DP (`domino_tilted_b.c`)

- **Vertex Order B:** `(4x + 5y + 5z, x - y, z, x, y)` swept end-to-end across all `252` vertices without Meet-in-the-Middle (`(W_t, K_t)` differs from Order A at `236 / 253` steps; `peak RAM <= 2.12 GiB` in two preallocated `uint16_t` `mmap` buffers, `<= 4` threads).
- **Moduli:** Prime Set B (`15` distinct primes `21841 .. 10909`, disjoint from Prime Set A, product `~ 2^215.17 > Bregman permanent bound 2^173.89`).
- **Commands:**

```sh
cc -O3 -Wall -Wextra -pthread how-we-built-it/domino_tilted_b.c -o ./domino_tilted_b
./domino_tilted_b               # runs all 16 OEIS calibration checks including 6x6x6
./domino_tilted_b --solve-667   # runs calibration + full 15-prime A049507(7) computation
rm -f ./domino_tilted_b
```

## 3. Algebraic & Symmetry Audit (`gf2_and_burnside_audit.py`)

```sh
python3 how-we-built-it/gf2_and_burnside_audit.py
```
