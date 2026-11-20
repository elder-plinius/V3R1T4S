# Run It Yourself

All commands below run from this package directory in a fresh POSIX shell (`sh`), using only Python 3 (standard library) and a C99 compiler (`cc` with `-pthread`).

## 1. Run the Standalone Verification Suite (~3 minutes, `<= 2.12 GiB` RAM)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output lines:

```text
[OK] Order C reproduced A028446(3) = A049507(6) P_6xP_6xP_6  = 417898687046465734392674187695263185
[OK] Order C fresh prime check M(P_6xP_6xP_7) mod 21713 == 9050 (matches claimed value)
[OK] Order C fresh prime check M(P_6xP_6xP_7) mod 21683 == 16489 (matches claimed value)
PASS
```

## 2. Rebuild `A049507(7)` from Scratch with Both Independent Discovery Engines

### Engine 1: Meet-in-the-Middle Diagonal Pull-DP (`Order A`, 10 31-bit primes, ~16 minutes on 4 threads, `<= 1.9 GiB` RAM)

```sh
cc -O3 -Wall -Wextra -pthread how-we-built-it/domino_mitm_a.c -o ./domino_mitm_a
./domino_mitm_a --solve-667
rm -f ./domino_mitm_a
```

Expected final output line:

```text
RESULT A049507(7) = 781760467628825425251897322894619609502208
```

### Engine 2: Full End-to-End Tilted-Hyperplane Push-DP (`Order B`, 15 disjoint primes, ~11.5 minutes on 4 threads, `<= 2.12 GiB` RAM)

```sh
cc -O3 -Wall -Wextra -pthread how-we-built-it/domino_tilted_b.c -o ./domino_tilted_b
./domino_tilted_b --solve-667
rm -f ./domino_tilted_b
```

Expected final output line:

```text
RESULT A049507(7) = 781760467628825425251897322894619609502208
```

### Algebraic `GF(2)` & `D_4` Subgroup-Lattice Burnside `mod 8` Audit (~18 seconds)

```sh
python3 how-we-built-it/gf2_and_burnside_audit.py
```
