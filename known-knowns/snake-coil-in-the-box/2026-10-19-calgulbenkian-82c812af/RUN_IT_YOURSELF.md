# Run it yourself

From this package folder, in a fresh shell (python3 3.8 or later, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. The first step compares every file in `object/` with `SHA256SUMS` and prints `FAIL` if one differs. The checker alone:

```sh
python3 -I verify-it-yourself/check_snake.py object/p3_co13_drifted_r0_Q13_2930.txt 13 coil the-record-we-beat/published.json
```

Expected: The checker prints one JSON line with `"valid": true`, `"length": 2930`, `"calibration_all_reproduce": true` (it re-verifies the published sample record of the same dimension and type and gets the table length), and the run ends with `ALL CHECKS PASS`.

Rough time: a few seconds.

The claim folder called `the-record-we-beat/` here `table-record/`; the checker file's own comments still use the old name.

How to rebuild the object: The object is a transition sequence (one base-36 digit per step from vertex 0). It came out of the contributor's local-search programs described in `how-we-built-it/README.md`; the exact command line and seed file were not recorded in the snapshot, so a rebuild is not promised to give the same file. The check does not depend on how the file was found.
