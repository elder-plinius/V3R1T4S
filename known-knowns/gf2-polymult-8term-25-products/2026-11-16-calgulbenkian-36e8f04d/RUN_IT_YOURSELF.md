# Run It Yourself (`gf2-polymult-8term-25-products` `p2`, `0x89`)

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
File: object/gf128_0x89_81gates.slp.txt
Field: GF(2^7) mod 0x89
Gates: 81 (AND=32, XOR=49, XNOR=0), Depth: 6, AND-depth: 1
Exhaustive truth-table check: 16384 / 16384 input pairs matched exactly (0 mismatches).
PASS
```
