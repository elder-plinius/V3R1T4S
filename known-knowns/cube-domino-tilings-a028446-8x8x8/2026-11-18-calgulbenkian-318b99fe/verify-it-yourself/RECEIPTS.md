# Standalone Verification Receipts

Command executed from the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Execution window (UTC):** `Started: 2026-11-18T08:21:18Z | Finished: 2026-11-18T08:24:25Z`
- **Wall-clock time:** `187.05s` (`4` threads, `maximum resident set size = 2,263,973,888 bytes = 2.11 GiB`)
- **Exit code:** `0`

## Captured Standard Output

```text
[OK] Graph & GF(2) check: 126x126 biadjacency rank=120, det=0 == V mod 2, v_2(V)=9
[OK] z-reflection theorem: |Fix(zeta)| = 385164950209515287552 == A049507(1)*A049507(3)
[OK] 25-prime CRT & Bregman/row-product bounds verified (combined modulus ~10^158.09)
[OK] Exact D_4 Burnside/Mobius mod 8 check: all 9 subgroup fixed counts match, free_orbits=97720058453603166350467775353912955052944
[OK] Order C reproduced A028446(1) P_2xP_2xP_2               = 9
[OK] Order C reproduced A028446(2) P_4xP_4xP_4               = 5051532105
[OK] Order C reproduced A028454(1) P_4xP_4xP_1               = 36
[OK] Order C reproduced A028454(2) P_4xP_4xP_2               = 32000
[OK] Order C reproduced A028454(3) P_4xP_4xP_3               = 10885344
[OK] Order C reproduced A028454(5) P_4xP_4xP_5               = 2132137503232
[OK] Order C reproduced A028454(6) P_4xP_4xP_6               = 932814464901633
[OK] Order C reproduced A028454(6) P_6xP_4xP_4               = 932814464901633
[OK] Order C reproduced A028454(7) P_4xP_4xP_7               = 403325499406267520
[OK] Order C reproduced A049507(0) P_6xP_6xP_0               = 1
[OK] Order C reproduced A049507(1) P_6xP_6xP_1               = 6728
[OK] Order C reproduced A049507(2) P_6xP_6xP_2               = 53786626921
[OK] Order C reproduced A049507(3) P_6xP_6xP_3               = 57248060375968384
[OK] Order C reproduced A049507(4) P_6xP_6xP_4               = 123115692449982216049513
[OK] Order C reproduced A049507(5) P_6xP_6xP_5               = 216388579168758145017797108072
[OK] Order C reproduced A028446(3) = A049507(6) P_6xP_6xP_6  = 417898687046465734392674187695263185
[OK] Order C fresh prime check M(P_6xP_6xP_7) mod 21713 == 9050 (matches claimed value)
[OK] Order C fresh prime check M(P_6xP_6xP_7) mod 21683 == 16489 (matches claimed value)
PASS
```

## Discovery engine runs (captured standard output)

Both discovery engines were built from `how-we-built-it/` and run to the full `A049507(7)` result; their complete standard output is saved unedited:

| Engine | Command | Log | SHA-256 of log |
|---|---|---|---|
| Engine 1 (`domino_mitm_a.c`, Order A, Prime Set A) | `cc -O3 -Wall -Wextra -pthread how-we-built-it/domino_mitm_a.c -o ./mitm_a && ./mitm_a --solve-667 > engine1_mitm_a.stdout.log` | `verify-it-yourself/engine1_mitm_a.stdout.log` | `0e9287eb08796b9bce5e5e2ac8582737f372e2399889a534932d9f5bb6366b84` |
| Engine 2 (`domino_tilted_b.c`, Order B, Prime Set B) | `cc -O3 -Wall -Wextra -pthread how-we-built-it/domino_tilted_b.c -o ./tilted_b && ./tilted_b --solve-667 > engine2_tilted_b.stdout.log` | `verify-it-yourself/engine2_tilted_b.stdout.log` | `ee4c1fdb1165b4619eaa96c8c2c577d621b6945b4271cc5f9b50c673524745ac` |

- **Machine:** Mac Studio, Apple M3 Ultra (28 cores), macOS 26.6.2.
- **Date:** 2026-11-18. The two runs finished at 19:25:51Z (Engine 1) and 19:40:51Z (Engine 2), in that order.
- **Source used:** copies of `domino_mitm_a.c` (sha256 `a65522ab99c3dd38ca59fff76d29fcb41331e8f528e99869d60d71ab977f56ef`) and `domino_tilted_b.c` (sha256 `b4b2ac3641e71333b13d204e6719d7f91a0784aa73bd2af1a4b0bef0b92a5268`), byte-identical to the files in this package. Both files are unchanged since, except for the one comment fixed at `domino_mitm_a.c` line 808 (see `how-we-built-it/README.md`, "Deviations from PREREG"), which changes no executed code.
- **Each log contains:** the 16 calibration checks, including `A049507(0..6)` (with `A049507(6) = A028446(3)`) and `A028446(1..2)`; the per-prime residues of `A049507(7)`; the CRT reconstructions; and the final `RESULT`. Engine 1 reconstructs from 6 and from all 10 primes, Engine 2 from 10, 12 and all 15, and every reconstruction gives `781760467628825425251897322894619609502208`.
- **The run command was not recorded at the time**; the commands above are the ones in `how-we-built-it/README.md`. A rebuild of the shipped source with that compile line gave executables of the same size as the ones that produced these logs.
