# Run it yourself

All commands run from this package folder in a fresh shell. Python 3.8 or later, standard library only.

## 1. Quick check

```sh
sh verify-it-yourself/run_checks.sh
```

About 8 seconds. Expected: the last line is `PASS`. The real output is in `verify-it-yourself/RECEIPTS.md`.

## 2. The checker alone

```sh
python3 -I verify-it-yourself/mindist_gf4.py object/win_q4_n163_k11_d104.json
```

Expected last output line (abbreviated): `{"n": 163, "k": 11, "messages_nonzero": 4194303, "expected": 4194303, "rank_k": true, "min_distance": 104, "A_d": 7956, "claimed_d": 104}`

## 3. The C cross-check by hand (optional)

```sh
cc -O2 -o md verify-it-yourself/mindist4_gf4.c
python3 -I verify-it-yourself/json2txt.py object/win_q4_n163_k11_d104.json > g.txt
./md g.txt
```

Expected: one line ending `min_distance=104 A_d=7956` with `rank_deficient=no`.

## Rebuilding the object

The object is the output of a search or a solver run by the contributor, not of a deterministic recipe we can replay. The programs are in `how-we-built-it/`, with the commands as far as the snapshot records them and an honest list of what it does not record. Nothing in the quick check needs them.
