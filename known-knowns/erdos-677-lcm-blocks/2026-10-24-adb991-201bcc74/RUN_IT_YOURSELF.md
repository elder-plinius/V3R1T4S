# Run it yourself

All commands run in a fresh shell from this package folder. You need Python 3 with gmpy2, mpmath and numpy, a C
compiler, `sha256sum` (or `shasum`) and the usual POSIX tools (`cmp`, `comm`, `sed`, `awk`, `grep`, `xargs`,
`mktemp`). No network access. If your Python lacks the three modules:

```sh
python3 -m venv v && v/bin/pip install gmpy2 mpmath numpy      # then use PY=v/bin/python3 below
```

The contributor's machine had Python 3.13.16 with gmpy2 2.3.2, mpmath 1.3.0 and numpy 2.5.4.

## 1. The check

```sh
PY=python3 sh verify-it-yourself/run_checks.sh           # default: 164 s with 3 jobs on the contributor's machine
PY=python3 sh verify-it-yourself/run_checks.sh --all     # everything: 5179 s with 3 jobs on the contributor's machine
```

Expected last line: `PASS` (exit status 0). Environment: `PY` (default `python3`; a relative path is taken relative
to where you start the script), `CC` (default `cc`), `JOBS` (parallel Python jobs, default 3; each needs about 1 GB),
`PIDLOG` (optional file that receives each job's PID). Every job runs at `nice -n 10`. The script writes only to a
scratch folder from `mktemp -d`, which it deletes. `sh verify-it-yourself/run_checks.sh --help` prints the header.

The real output, with timings, is in `verify-it-yourself/RECEIPTS.md`. The lines that carry the result in default
mode:

```
step 1 object files: 19 files, sha256 equal to the recorded values, no other file: ok
step 2 saved outputs: ... deep_rig k = 3..25 product_solutions=0, 1174616 window candidates: ok
step 4 small X (n + k <= 1100000, every k, every m): ok
step 5 reruns: ratio audit, interval margin checker and the enumeration for k = 3..16 equal the saved outputs: ok
PASS
```

## 2. What it does

1. Compares the sha256 of the 19 files in `object/` with the values recorded in the script (the same values are
   listed in `README.md`), and refuses any other file in `object/`: the files are the ones the panel read.
2. Checks that the saved outputs say what the claim says: `# COMPLETE kmin=3 kmax=147 total_candidates=2`;
   `candidates: 2 exact-equal: 0`; `TOTAL missing over k=3..25: 0`; `TOTAL pairs=63041 failures=0 undecided=0` in both
   margin outputs; exactly one line per k = 3..25 in the enumeration outputs, each with `product_solutions=0`, no
   `PRODUCT SOLUTION` line, and 1174616 window candidates in all (per-k lines and TOTAL lines both add up to it).
3. Checks that `PY` imports gmpy2, mpmath and numpy (and says how to install them if not), and that `CC` exists.
4. Proof step 2: compiles `object/search677b.c` (`cc -O2 ... -lm`), runs `search677b 1100000 4242`, then
   `object/verify_cands.py` on its output; both outputs must equal the saved ones apart from the elapsed times.
   The exact judge `verify-it-yourself/check677.py` (written from the definition; the same bytes as the claim's
   `checker/check677.py`, sha256 03ecd782d3cfb3437f7b3915b504547b8506a74e39e88bae232e766f94760239) must reject the
   two candidates, (n, m, k) = (4, 13, 3) and (18, 53, 4): their lcms differ.
5. Reruns, `JOBS` at a time, with `PY -I -B` (no bytecode is written):
   - `object/taskA_ratio_audit.py 3000` (proof step 3): byte-identical to `object/out/taskA_ratio_audit_NB3000.txt`;
   - `object/rig_margin.py 3 25 1000000 1 1000` (proof step 4, interval arithmetic): equal to the saved output with
     the `time_s=` fields stripped;
   - `QEXP=495 object/deep_rig.py KMIN KMAX 1040 0.001 1000000` (proof step 5) for k = 3..13, 14 and 15..16: every
     per-k line equal to the saved line in `object/out/deep_rig_final_k3-18_d1040.txt` with the `t=` field stripped.
   With `--all`, the enumeration instead runs as the five commands of `how-we-built-it/claim/REPRODUCE.md`
   (k = 3..18, 19..22, 23, 24, 25), and each whole output, TOTAL line included, must equal its saved file with the
   times stripped; `object/rig_margin_exact.py 3 25 1000000 1 1000` (exact rationals) is rerun and compared too.

What the script cannot check: Lemma A and the completeness argument of the enumeration (`object/PROOF.md`, Steps 1
and 5, to be read), and the correctness of the float64 pre-filters and 1090-digit non-interval arithmetic in
`object/deep_rig.py`, which a rerun reproduces but does not prove (`panel/criterion.md`, section 3, gives the error
analysis).

## 3. By hand (from `how-we-built-it/claim/REPRODUCE.md`)

```sh
cd object
cc -O2 -o ../search677b search677b.c -lm
../search677b 1100000 4242 ../my_search.txt                   # last line: # COMPLETE kmin=3 kmax=147 total_candidates=2 ...
$PY -I -B verify_cands.py ../my_search.txt                    # candidates: 2 exact-equal: 0 ...
$PY -I -B taskA_ratio_audit.py 3000                           # TOTAL missing over k=3..25: 0
$PY -I -B rig_margin.py 3 25 1000000 1 1000                   # TOTAL pairs=63041 failures=0 undecided=0
$PY -I -B rig_margin_exact.py 3 25 1000000 1 1000             # same TOTAL line; about 1 h on one core
QEXP=495 $PY -I -B deep_rig.py 3 18 1040 0.001 1000000        # compare with out/deep_rig_final_k3-18_d1040.txt
QEXP=495 $PY -I -B deep_rig.py 19 22 1040 0.001 1000000
QEXP=495 $PY -I -B deep_rig.py 23 23 1040 0.001 1000000
QEXP=495 $PY -I -B deep_rig.py 24 24 1040 0.001 1000000
QEXP=495 $PY -I -B deep_rig.py 25 25 1040 0.001 1000000
```

Each `deep_rig.py` run ends with `TOTAL window candidates=... product solutions=0 (X0=1000000, QMAX=10^495)`; its
per-k lines must match the saved files apart from the `t=` times. Without `QEXP=495` the program silently uses
QMAX = 10^515 (`panel/criterion.md`, section 4). `$PY -I -B deep_rig.py 3 12 200 0.001 1000000 validate`
compares the enumeration with brute force for q ≤ 4000. `python3 -I verify-it-yourself/check677.py n m k` judges a
single triple in exact integers.

Commands used in the run: `how-we-built-it/COMMANDS.md`.
