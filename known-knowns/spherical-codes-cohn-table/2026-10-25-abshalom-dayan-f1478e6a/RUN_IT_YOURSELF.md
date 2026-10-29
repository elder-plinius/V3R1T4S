# Run it yourself

From this folder, in a fresh shell, with Python 3 (standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (verify-it-yourself/RECEIPTS.md), under a second on a laptop:

```
sha256 f1478e6af59430f60997ba2d052fd658e92314fa61deb5439ff49df96d595411 expected
points 256, coordinates per point [6]
fewest significant digits in a coordinate: 26
zero vectors: 0
pairs with cosine above c_table - 1e-10 (exact): 0
c* = 0.7048987224974410014732802770067601805699 at pair (55, 247) (0-based lines)
c_table - c* = 3.324685e-05
PASS
```

The check is exact: coordinates are read as decimals and every one of the 32,640 pairs is compared with the bar
c_table - 1e-10 = 0.704931969252 in integer arithmetic. The last line is PASS or FAIL.

To rebuild the object, see how-we-built-it/COMMANDS.md (numpy and scipy, about five minutes on one core in two
steps, starting from the code posted at https://spherical-codes.org/data/6/256). A rebuild lands near, not exactly on,
object/code_6_256.txt.

Named but not shipped: how-we-built-it/ and the-record-we-beat/ name run-workspace items that are not in this package and are not needed to check the claim:

- the run that made the object, named by its date and time (PREREG.md, PREREG_seed_run.md);
- its output deep_6_256.txt under runs/ and log deep_6_256.log (PREREG.md); the output is byte-identical to object/code_6_256.txt;
- data/queue_scout.out, attempts/claim-object/result/ and target.md (PREREG.md);
- the run's checker/check_mp.py, checker/check_exact.py and checker/fetch_live.sh (PREREG.md, PREREG_seed_run.md);
- COMMANDS.md's file names: 6_256.txt is the table's posted code at https://spherical-codes.org/data/6/256; slp_6_256.txt is step 1's output; code_6_256.txt is step 2's output, which is object/code_6_256.txt;
- the earlier /plain reads saved in the workspace (the-record-we-beat/RECORD.md).
