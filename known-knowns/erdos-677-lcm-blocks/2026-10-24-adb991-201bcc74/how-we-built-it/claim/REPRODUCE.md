# Reproduce (from this claim folder)

Requirements: Python 3 with gmpy2, mpmath and numpy (for example `python3 -m venv v && v/bin/pip install gmpy2
mpmath numpy`; below, `PY` is that python), a C compiler, 4 cores, and about 1 GB of memory. No network access.
Run each step with `PY -I`.

## Step 2 of the proof (small X): seconds

```sh
cd object
gcc -O2 -march=native -o search677b search677b.c -lm
./search677b 1100000 4242 my_search.txt          # last line: "# COMPLETE kmin=3 kmax=147 total_candidates=2 ..."
PY -I verify_cands.py my_search.txt               # "candidates: 2 exact-equal: 0 ..."
```

The seed (4242) only changes the hash: with another seed, the candidate list must still contain no exact-equal pair.

## Step 3 of the proof (the ratio set is complete): about 1 minute

```sh
PY -I taskA_ratio_audit.py 3000                   # last lines: "TOTAL missing over k=3..25: 0" ...
```

## Step 4 (margin, rigorous arithmetic)

```sh
PY -I rig_margin.py 3 25 1000000 1 1000           # interval arithmetic, about 3 min: "TOTAL pairs=63041 failures=0 undecided=0"
PY -I rig_margin_exact.py 3 25 1000000 1 1000     # exact rationals, about 1 h on one core: same TOTAL line
```

## Step 5 (enumeration): about 30-40 min of wall time on 4 idle cores (k = 23 and 25 take the longest)

```sh
QEXP=495 PY -I deep_rig.py 3 18 1040 0.001 1000000
QEXP=495 PY -I deep_rig.py 19 22 1040 0.001 1000000
QEXP=495 PY -I deep_rig.py 23 23 1040 0.001 1000000
QEXP=495 PY -I deep_rig.py 24 24 1040 0.001 1000000
QEXP=495 PY -I deep_rig.py 25 25 1040 0.001 1000000
```

Each run's last line is `TOTAL window candidates=... product solutions=0 (X0=1000000, QMAX=10^495)`. The per-k lines
must match object/out/deep_rig_final_*.txt, apart from the times.

`deep_rig.py ... validate` (DIG = 200) compares the enumeration with brute force for q ≤ 4000.

To judge a single triple in exact integers: `python3 -I checker/check677.py n m k`.
