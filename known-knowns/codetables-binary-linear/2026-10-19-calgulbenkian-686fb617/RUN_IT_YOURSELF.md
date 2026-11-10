# Run it yourself

All commands run from this package folder in a fresh shell. Python 3.8 or later, standard library only.

## 1. Quick check

```sh
sh verify-it-yourself/run_checks.sh
```

About 5 seconds. Expected: the last line is `PASS`. The real output is in `verify-it-yourself/RECEIPTS.md`.

## 2. The checker alone

```sh
python3 -I verify-it-yourself/qecc_check.py object/qecc_p1_n23_k9_d5.json
```

Expected last output line (abbreviated): `{"n": 23, "k": 9, "rank": 14, "self_orthogonal": true, "d": 5, "claimed_d": 5, "consistent": true, "VALID": true}`

## Rebuilding the object

The object is the output of a search or a solver run by the contributor, not of a deterministic recipe we can replay. The programs are in `how-we-built-it/`, with the commands as far as the snapshot records them and an honest list of what it does not record. Nothing in the quick check needs them.
