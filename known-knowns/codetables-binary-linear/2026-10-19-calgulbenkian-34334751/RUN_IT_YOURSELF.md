# Run it yourself

All commands run from this package folder in a fresh shell. Python 3.8 or later, standard library only.

## 1. Quick check

```sh
sh verify-it-yourself/run_checks.sh
```

About 1 second. Expected: the last line is `PASS`. The real output is in `verify-it-yourself/RECEIPTS.md`.

## 2. The checker alone

```sh
python3 -I verify-it-yourself/lp_delsarte_check.py object/lp_cert_q2_n161_k17_dub72.json 72
```

Expected last output line (abbreviated): `{"q": 2, "n": 161, "k": 17, "D": 72, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}`

## Rebuilding the object

The object is the output of a search or a solver run by the contributor, not of a deterministic recipe we can replay. The programs are in `how-we-built-it/`, with the commands as far as the snapshot records them and an honest list of what it does not record. Nothing in the quick check needs them.
