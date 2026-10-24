# Run it yourself

## 1. Check the shipped code

From a fresh shell in this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Needs python3 (3.8 or later) with numpy; numpy is used only for small integer matrices. If your python3 has no numpy, point PY at one that has it: `PY=/path/to/python sh verify-it-yourself/run_checks.sh`. The last line is `ALL CHECKS PASS`. Rough laptop time: a few seconds. A real run is in `verify-it-yourself/RECEIPTS.md`.

The checker alone:

```sh
python3 verify-it-yourself/check_eaqecc.py object/eaqecc_34_2_24_24.json 23 32
```

Expected last line: `[[34,2,24;24]]_3 PASS`. It reads the 0/1/2 matrix as 56 x 68 generators over GF(3) (columns x_1..x_n then z_1..z_n, symplectic form u_x.v_z - u_z.v_x), computes the rank, c = rank(S J S^T)/2 and k = n - s + c, builds the symplectic dual and the isotropic part, and enumerates every dual vector outside the isotropic part to get the exact minimum distance. The two numbers on the command line are the table cell's d_lower and d_upper. `verify-it-yourself/calibration.py` runs the same functions on hand-derived small cases, and the run script also changes one matrix entry and requires the checker to reject it.

## 2. Rebuild the code

Not possible from this package: the construction script is not in the contributor's snapshot (see `how-we-built-it/README.md`).
