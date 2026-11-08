# Run it yourself

## 1. Check the shipped set

From a fresh shell in this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Needs python3 3.8 or later (standard library) for the branch-and-bound and the exhaustive enumeration. **The ILP, the criterion's second method, needs pulp** (`pip install pulp`; it bundles the CBC solver) and is run by `ilp_sidon.py`. If your python3 has no pulp, `run_checks.sh` prints `ILP SKIPPED: ...`, still runs the other methods, and ends in `PASS` only if every method that ran agreed and both branch-and-bound and exhaustive enumeration ran. With pulp the last line is `ALL CHECKS PASS`. To use another interpreter: `PY=/path/to/python sh verify-it-yourself/run_checks.sh`. Rough laptop time: under a minute (the exhaustive pass walks all 2^21 subsets).

The pieces alone:

```sh
python3 verify-it-yourself/check_e757.py object/witness_n21_s12.json --expect-s 12 --expect-n 21
python3 verify-it-yourself/check_e757.py verify-it-yourself/calibration_ma_tang.json --expect-s 8 --expect-n 14
python3 verify-it-yourself/ilp_sidon.py object/witness_n21_s12.json --expect-s 12
```

Expected lines:

```
n=21 bad_4_subsets=0 relations=19 s_branch_and_bound=12 s_exhaustive_2^n=12 ratio=4/7 n_multiple_of_14=False ratio<4/7=False ratio==4/7=True ratio>=9/17=True
PASS
ILP: n=21 relations=19 status=Optimal s(A)=12 returned_subset_is_sidon=True PASS
```

What is checked: every 4-subset has at least 5 distinct absolute differences (all 5985 of them); s(A) by bitmask branch-and-bound over the relations a+b = c+d with {a,b} different from {c,d} (a = b allowed, so 3-term progressions are forbidden), by exhaustive enumeration of all subsets, and by the ILP; the ratio compared as a fraction; the Ma-Tang 14-set as calibration (s = 8 by every method).

## 2. Rebuild the set

See `how-we-built-it/README.md`. In a scratch copy of the package, `python3 how-we-built-it/glue_a14_b8.py` (standard library only; it writes `result/witness_n21_s12.json` next to the how-we-built-it folder) regenerates the shipped set. Tested on 2026-10-18: the output file's sha256 is 6478bc3cabcce580910f07fd9e3fee3a15d5b398ba12c9f9f557cfa7af7f2539, identical to `object/witness_n21_s12.json`. Check with `shasum -a 256 result/witness_n21_s12.json`.
