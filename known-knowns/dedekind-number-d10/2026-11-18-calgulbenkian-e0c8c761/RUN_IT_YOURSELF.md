# Run It Yourself

All commands below run from this package folder in a fresh POSIX shell using Python 3 standard library and a standard C99 compiler (`cc`).

## 1. Run the standalone dual-engine verifier (~75 seconds)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
OK: Exact D(0..7) reproduced via multi-prime CRT Zeta (2, 3, 6, 20, 168, 7581, 7828354, 2414682040998)
OK: P_81 subgroup lattice (50 subgroups) and Table-of-Marks congruence verified over Z
OK: Engine 1 (C99 128-bit Mobius + Galois/Interval) verified D(0..7), D(6..8) mod 9, and all 9 classes
OK: Class 0 (|K|= 9, subs= 3, |B^9/K|=128): Fix_D9=36035591703, Fix_D10=25861677069383652640 (Engine 1 == Engine 2 == Cert)
OK: Class 1 (|K|= 9, subs= 6, |B^9/K|= 96): Fix_D9=103930332, Fix_D10=506885470393492 (Engine 1 == Engine 2 == Cert)
OK: Class 2 (|K|= 9, subs= 4, |B^9/K|= 80): Fix_D9=8405574, Fix_D10=3925342826836 (Engine 1 == Engine 2 == Cert)
OK: Class 3 (|K|= 9, subs= 6, |B^9/K|= 60): Fix_D9=97830, Fix_D10=1702659955 (Engine 1 == Engine 2 == Cert)
OK: Class 4 (|K|= 9, subs= 3, |B^9/K|= 64): Fix_D9=207471, Fix_D10=7751544283 (Engine 1 == Engine 2 == Cert)
OK: Class 5 (|K|=27, subs= 1, |B^9/K|= 64): Fix_D9=232848, Fix_D10=6188212000 (Engine 1 == Engine 2 == Cert)
OK: Class 6 (|K|=27, subs= 2, |B^9/K|= 28): Fix_D9=324, Fix_D10=31798 (Engine 1 == Engine 2 == Cert)
OK: Class 7 (|K|=27, subs= 1, |B^9/K|= 32): Fix_D9=753, Fix_D10=164689 (Engine 1 == Engine 2 == Cert)
OK: Class 8 (|K|=81, subs= 1, |B^9/K|= 24): Fix_D9=132, Fix_D10=6526 (Engine 1 == Engine 2 == Cert)
OK: D(9) reproduced modulo (3, 9, 27) = (0, 6, 24) == D(9) mod (3, 9, 27)
OK: Published arXiv:2611.13887v1 checks reproduced: phi_10(C_9)=1702659955, |P_3^Q|=6526, D(10) == 1 (mod 3)
VERIFIED: D(10) == 16 (mod 27) [and D(10) == 7 (mod 9)] by two independent implementations
PASS
```

## 2. Rebuild and run the two discovery builders from scratch

### Engine 1 (C99 exact 128-bit subgroup-poset Mobius across all 27 subgroups individually, ~50s; add `--with-d8` to also reproduce exact `D(8)` in ~55s)

```sh
cc -O3 -Wall -Wextra -std=c99 -pthread how-we-built-it/engine1_c99_slice.c -o engine1_c99_slice
./engine1_c99_slice
./engine1_c99_slice --with-d8
rm -f engine1_c99_slice
```

### Engine 2 (Pure Python 3 multi-prime finite-field CRT + Table-of-Marks + Markov/Zeta transfer, ~59s)

```sh
python3 how-we-built-it/engine2_py_crt_transfer.py
```
