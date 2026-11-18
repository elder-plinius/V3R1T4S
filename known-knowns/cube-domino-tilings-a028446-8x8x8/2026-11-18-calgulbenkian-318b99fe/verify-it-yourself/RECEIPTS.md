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
