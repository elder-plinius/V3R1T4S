# Build & Reproduction Commands

All tools require only `python3` (3.8+, standard library only) and a standard C99 compiler (`cc`, `clang`, or `gcc`) with POSIX threads (`-lpthread`).

## 1. Rebuild `object/q7_3_ord3_certificate.json` from scratch

From the package root folder:

```sh
python3 how-we-built-it/build_certificate.py
```

This deterministically constructs $Q^-(5,3)$ ($112$ singular points, $280$ totally singular lines, and an explicit $28$-line spread invariant under an order-$3$ automorphism), constructs $Q^-(7,3)$ ($1{,}066$ singular points, $29{,}848$ lines, $22{,}960$ planes), constructs the $5$ order-$3$ conjugacy class representatives in $\mathrm{PGO}^-(8,3)$, the $5$ involution conjugacy class representatives in $\mathrm{PO}^-(8,3)$, and the $4$ odd-prime Sylow-$\{5,7,13,41\}$ representatives, and writes `object/q7_3_ord3_certificate.json`.

## 2. Run Engine 1 (64-bit SWAR Bit-Parallel Exact Cover Solver on `C3_13`)

```sh
cc -O3 how-we-built-it/solve_ord3_staged_swar.c -o solve_ord3_staged_swar -lpthread
./solve_ord3_staged_swar
```

Expected final line (~15 seconds on 4 cores):

```text
=== STAGED SWAR COMPLETE: sat=0, total_tasks=144, total_nodes=8796560, wall_time=15.600s ===
```

## 3. Run the Independent Zero-Shared-Code Verifier (Python Checker + Engine 2 Row-DLX)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final line (~55 seconds):

```text
PASS
```
