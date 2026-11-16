# Run It Yourself (`gf2-polymult-8term-25-products` `p2`, `0x91`)

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
File: object/gf128_0x91_82gates.slp.txt
Field: GF(2^7) mod 0x91
Gates: 82 (AND=34, XOR=48, XNOR=0), Depth: 6, AND-depth: 1
Exhaustive truth-table check: 16384 / 16384 input pairs matched exactly (0 mismatches).
PASS
```
