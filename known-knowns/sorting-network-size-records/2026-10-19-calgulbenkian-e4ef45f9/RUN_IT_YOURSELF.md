# Run it yourself

From this package folder, in a fresh shell (python3 3.8 or later, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. The first step compares every file in `object/` with `SHA256SUMS` and prints `FAIL` if one differs. The checker alone:

```sh
python3 -I verify-it-yourself/check_sorter.py object/N38_S253_D16.txt 38 253 16 the-record-we-beat/listed.json
```

Expected: The checker prints one JSON line with `"SORTS": true`, `"size": 253`, `"depth": 16`, `"not_dominated_by_any_listed_pair": true`, and the run ends with `ALL CHECKS PASS`.

Rough time: a few seconds.

The claim folder called `the-record-we-beat/` here `table-record/`; the checker file's own comments may still use the old name.

How to rebuild the object: The object is a plain list of comparators (first line `n size`, then `i j` per line). It came out of the contributor's search programs described in `how-we-built-it/README.md`; the exact command lines were not recorded in the snapshot, so a rebuild is not promised to give the same file. The check does not depend on how the file was found.
