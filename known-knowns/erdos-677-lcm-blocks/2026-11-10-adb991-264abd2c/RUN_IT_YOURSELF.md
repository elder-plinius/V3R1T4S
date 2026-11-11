# Run it yourself

All commands run in a fresh shell from this package folder. You need Python 3 with gmpy2, mpmath and numpy, a C
compiler, `sha256sum` (or `shasum`) and the usual POSIX tools (`cmp`, `sed`, `awk`, `grep`, `xargs`, `mktemp`). No
network access. If your Python lacks the three modules:

```sh
python3 -m venv v && v/bin/pip install gmpy2 mpmath numpy      # then use PY=v/bin/python3 below
```

The contributor's machine had Python 3.13.16 with gmpy2 2.3.2, mpmath 1.3.0 and numpy 2.5.4, and gcc 13.3.0 as `cc`.

## 1. The check

```sh
PY=python3 sh verify-it-yourself/run_checks.sh           # default: 342 s on the contributor's machine
PY=python3 sh verify-it-yourself/run_checks.sh --all     # everything: about 2.5 hours on 4 cores
```

Expected last line: `PASS` (exit status 0). Environment: `PY` (default `python3`; a relative path is taken relative
to where you start the script), `CC` (default `cc`), `JOBS` (parallel Python jobs, default 4), `PIDLOG` (optional file
that receives each job's PID). Every job runs at `nice -n 10`. The script writes only to a scratch folder from
`mktemp -d`, which it deletes. `sh verify-it-yourself/run_checks.sh --help` prints the header.

The real output, with timings, is in `verify-it-yourself/RECEIPTS.md`. The lines that carry the result in default
mode:

```
step 1 object files: 29 files, sha256 equal to the recorded values, no other file: ok
step 2 saved outputs: ... 4 enumeration shards, ratio counts add up to 114817, product_solutions=0 everywhere, 3288852 window candidates: ok
step 4 small X (n + k <= 1100000, every k, every m): ok
step 5 reruns: ratio audit and interval margin checker (whole ratio list) equal the saved outputs: ok
PASS
```

## 2. What it does

1. Compares the sha256 of the 29 files in `object/` with the values recorded in the script (the same values are
   listed in `README.md`), and refuses any other file in `object/`: the files are the ones the panel read.
2. Checks that the saved outputs say what the claim says: `# COMPLETE kmin=3 kmax=147 total_candidates=2` with a
   k = 29 line `cand=0`; `candidates: 2 exact-equal: 0 ...`; 114817 ratios with `TOTAL missing over k=29..29: 0` and
   no brute-force ratio outside the set; `TOTAL pairs=114817 failures=0 undecided=0` from the interval checker; four
   exact-margin shards, each starting `SHARD i/4` and ending `failures=0 undecided=0`, whose pairs add up to 114817;
   four enumeration shards, each starting `SHARD i/4`, with one k = 29 line `product_solutions=0`, no
   `PRODUCT SOLUTION` line, admissible_r counts adding up to 114817 and 3288852 window candidates in all.
3. Checks that `PY` imports gmpy2, mpmath and numpy (and says how to install them if not), and that `CC` exists.
4. Proof step 2: compiles `object/search677b.c` (`cc -O2 ... -lm`), runs `search677b 1100000 20261109`, then
   `object/verify_cands.py` on its output; both outputs must equal the saved ones apart from the elapsed times. The
   exact judge `verify-it-yourself/check677.py` (written from the definition; the same bytes as the claim's
   `checker/check677.py`) must reject the two candidates, (n, m, k) = (4, 13, 3) and (18, 53, 4): their lcms differ.
5. Reruns, `JOBS` at a time, with `PY -I -B` (no bytecode is written):
   - `object/taskA_ratio_audit_k.py 400 29 29` (proof step 3): byte-identical to the saved output;
   - `object/rig_margin.py 29 29 1000000 1 1000` (proof step 4, interval arithmetic, whole list): equal to the saved
     output with the `time_s=` fields stripped.
   With `--all`, also `SHARD=i/4 object/shard_margin.py 29 29 1000000 1 1000` (exact rationals) and
   `SHARD=i/4 QEXP=495 object/shard_rig.py 29 29 1040 0.001 1000000` for i = 0..3, each whole output equal to its
   saved file with the times stripped.

What the script cannot check: Lemma A, the Step 4 reduction and the completeness argument of the enumeration
(`object/PROOF.md`, to be read), and the correctness of the float64 pre-filters and 1090-digit non-interval
arithmetic in `object/deep_rig.py`, which a rerun reproduces but does not prove (`panel/criterion.md`).

## 3. By hand (from `how-we-built-it/claim/REPRODUCE.md`)

```sh
cd object
cc -O2 -o ../search677b search677b.c -lm
../search677b 1100000 20261109 ../my_search.txt                    # last line: # COMPLETE kmin=3 kmax=147 total_candidates=2 ...
$PY -I -B verify_cands.py ../my_search.txt                         # candidates: 2 exact-equal: 0 ...
$PY -I -B taskA_ratio_audit_k.py 400 29 29                         # TOTAL missing over k=29..29: 0
$PY -I -B rig_margin.py 29 29 1000000 1 1000                       # TOTAL pairs=114817 failures=0 undecided=0
for I in 0 1 2 3; do SHARD=$I/4 $PY -I -B shard_margin.py 29 29 1000000 1 1000 > ../margin$I.txt & done; wait   # ~55 min per shard
for I in 0 1 2 3; do SHARD=$I/4 QEXP=495 $PY -I -B shard_rig.py 29 29 1040 0.001 1000000 > ../shard$I.txt & done; wait   # ~90 min per shard
$PY -I -B sum_shards.py ..                                         # per-k sums over the four shard files
```

Without `QEXP=495` the enumeration silently uses QMAX = 10^515. `python3 -I verify-it-yourself/check677.py n m k`
judges a single triple in exact integers.

Commands used in the run: `how-we-built-it/COMMANDS.md`.
