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

## Deviations from PREREG

`PREREG.md` stays frozen as written, and the code stays as it ran (the only code edit is one comment, in (b)). The shipped code differs from it, or the pre-registration misstates a figure, in these places:

(a) Orders and primes. `PREREG.md` lines 59, 61 and 62 give Order A as `(x+y+z, z, x, y)`, Order B as `(x+(5-y)+z, x, y, z)` and Prime Set B as ten 31-bit primes. The code is different:
- `domino_mitm_a.c` sorts by `(x+y+z, z-x, z, x, y)`.
- `domino_tilted_b.c` sorts by `(4x+5y+5z, x-y, z, x, y)`.
- `domino_tilted_b.c` uses 15 primes from 10909 to 21841 (all below 2^15), not ten 31-bit primes.

(b) The Bregman bound. `PREREG.md` lines 56-57 give `< 2.13e50 < 2^168`. The bound `(3!)^(4/3) * (4!)^(26/4) * (5!)^(56/5) * (6!)^(40/6)` is about 2.21e52 = 2^173.89, as `README.md` line 16 says. The comment at `domino_mitm_a.c` line 808 said "2^168" and now reads "2^173.89". The conclusions are unchanged: the 6 primes that Engine 1 reconstructs from exceed 2^173.89, and so do Engine 2's 15.

(c) The first 12 primes of Prime Set B. The statement in `domino_tilted_b.c` line 12 (and in its "OVERDETERMINED 5-PRIME CHECK" message, line 549) that the first 12 primes exceed the Bregman bound is wrong: their product is about 2^172.94, below 2^173.89. The first 13 primes, about 2^187.35, are the fewest that exceed it. The 12-prime reconstruction in that run is therefore a consistency check, not an unconditional one; the full 15-prime reconstruction (about 2^215.17) is unconditional, and it gives the same integer.
