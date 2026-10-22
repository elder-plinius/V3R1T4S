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
curl -A 'V3R1T4S-research (honest client; curl)' -o hsp4-170-posted.txt https://packomania.com/hsp4/txt/hsp4-170.txt
python3 -I verify-it-yourself/packcheck.py --kind ball --dim 4 --object object/WIN_hsp4_170.txt --expect-n 170 --table-radius 0.215589695168 --margin 1e-10 --posted hsp4-170-posted.txt
```

Expected extra lines: `max_abs_sorted_distance_difference=` about 9.0e-3 and `differs_from_posted_by_more_than_1e-8=True`.

## Rebuild

The two programs that produced the object are in `how-we-built-it/` (`transplant_scan.c`, `hsp_basin_opt.c`; C compiler only). `how-we-built-it/README.md` says which steps are documented and which command lines are not recorded. A rebuild from the posted N = 166 and N = 169 files is not promised to be byte-identical.
