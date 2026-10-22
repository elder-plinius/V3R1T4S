# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. The script checks the sha256 of the object against `INDEX.csv`, runs the standalone checker (standard library only), prints the comparison with the saved record in `the-record-we-beat/`, and runs a negative control that must be rejected.

## Check the non-isometry with the posted file (optional, needs the network)

The posted Packomania file is third-party data and is not shipped. To redo the comparison, fetch it once and pass it to the checker:

```sh
curl -A 'V3R1T4S-research (honest client; curl)' -o scu739-posted.txt https://packomania.com/scu/txt/scu739.txt
python3 -I verify-it-yourself/packcheck.py --kind cube --dim 3 --object object/WIN_scu_739.txt --expect-n 739 --table-radius 0.058531064606 --margin 1e-11 --posted scu739-posted.txt
```

Expected extra lines: `max_abs_sorted_distance_difference=` about 7.6e-2 and `differs_from_posted_by_more_than_1e-8=True`.

## Rebuild

`how-we-built-it/scu_attack.c` holds the deletion, L-BFGS and inflation routines the contributor used (C compiler only). `how-we-built-it/README.md` says plainly that the call that produced this object is not in the snapshot version of the file and that the exact commands are not recorded; the object was made from the posted N = 741 packing with 2 spheres removed.
