# Run it yourself

From this folder, in a fresh shell, with Python 3 (standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (verify-it-yourself/RECEIPTS.md), under a second on a laptop:

```
sha256 5948af010bf1c2e12ca85af0af8cf84930f34cf3f8db5824147153d7eab95a8c expected
points 575, coordinates per point [6]
fewest significant digits in a coordinate: 26
zero vectors: 0
pairs with cosine above c_table - 1e-10 (exact): 0
c* = 0.7926798356844868804982657898051971213375 at pair (387, 496) (0-based lines)
c_table - c* = 1.004011e-04
PASS
```

The check is exact: coordinates are read as decimals and every one of the 165,025 pairs is compared with the bar
c_table - 1e-10 = 0.792780236685 in integer arithmetic. The last line is PASS or FAIL.

To rebuild the object, see how-we-built-it/COMMANDS.md (numpy and scipy, about 23 minutes on one core in three
steps, starting from the code posted at https://spherical-codes.org/data/6/575). A rebuild lands near, not exactly
on, object/code_6_575.txt.
