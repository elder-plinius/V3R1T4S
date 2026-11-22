# Run it yourself

The programs in `how-we-built-it/` are our own, and the object is the evidence tables plus the value file.

All commands run from this package folder unless a step says otherwise. Replace `{WORKDIR}` as shown in `how-we-built-it/README.md`.

## 1. Quick check (standard library only)

```
sh verify-it-yourself/run_checks.sh
```

Needs python3 only (no numpy, no mpmath). About 1 second, negligible memory. Expected: lines beginning `ok`, then `failed checks: 0`, and the last line `PASS`. In this package the check also reads `SHA256SUMS` for the object hashes. The check parses the object tables, reruns the Wynn epsilon algorithm in decimal arithmetic at 80 digits for mmax = 22 to 40, counts the stable and shared decimals, counts independent sets of the king graph on n x n grids for n up to 7 against A063443, and recomputes the strip eigenvalues for widths 1 to 6 by exact integer power iteration. Its real output is in `verify-it-yourself/RECEIPTS.md`.

## 2. Rebuild tmlean and rerun widths 37 to 40

```
mkdir work && cp how-we-built-it/* work/ && cp object/lam_open.txt object/lam_open_lean.txt work/ && cd work
for f in drivelean.py prereg_b.py sitechain2.sh; do sed "s|{WORKDIR}|$PWD|g" $f > $f.tmp && mv $f.tmp $f; done
cc -O3 -march=native -o tmlean tmlean.c -lpthread
./tmlean 11 10 4 x count
python3 -I drivelean.py 100 new.txt 37 38 39 40
python3 -I prereg_b.py > out.txt
diff out.txt ../object/prereg_b_output.txt
```

- `./tmlean 11 10 4 x count` prints `60711713670028729` (A063443(12)). Seconds.
- `drivelean.py` needs mpmath. It prints one line per width (width, 45 digits of lambda, seconds) and appends `m 100 lambda` lines to `new.txt`. The lines of `new.txt` for widths 37 to 40 should equal the same lines of `object/lam_open_lean.txt` (the program is exact integer arithmetic; the builder checked widths 30 and 31 this way). Width 40 needs about 26 GB of memory and about 8 minutes with 12 threads; it must not share the machine with another job above 10 GB. Widths 37, 38, 39 need less (not recorded; by the growth of the state space roughly the golden ratio per width, so about 6 GB for width 37).
- `prereg_b.py` needs mpmath; the `diff` is expected to print nothing (the builder checked this on the shipped data).
- To redo widths 29 to 36 as well, use `python3 -I drivelean.py 100 new.txt 29 30 31 32 33 34 35 36` (seconds to a few minutes each).
- Widths 2 to 28 come from `tm.c` (about 26 GB at width 28, time not recorded); `object/lam_open.txt` is the output of that first program. As a cross-check the lean program reproduces widths 24 and 28 (`object/lam_open_lean.txt` lines for m = 24 and 28) to a relative difference of 1.4e-56 and 2.0e-56, which `verify-it-yourself/check_kings.py` recomputes from the shipped files.

## 3. Method A (site CTM) at chi = 90 and chi = 100

```
python3 -m pip install numpy python-flint          # not stdlib; versions the author used are not recorded
cd work
export VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2
sh sitechain2.sh
tail -n 3 sitef_90.log sitef_100.log
```

`sitechain2.sh` runs the whole warm-started ladder chi = 20, 30, ..., 100 (the chi = 90 and chi = 100 stages need the states of the stages before them, so the ladder is run from chi = 20). About 3 to 4 minutes in total (230 s summed from the logs; 2 min 46 s measured on rerun), memory not recorded (the chi = 100 state file is 16 MB). Expected last lines, equal to those in `object/sitef_90.log` and `object/sitef_100.log`:

```
chi = 90:  3 1.34264395112460129785173016187574039571940774850542796384844 ...
chi = 100: 3 1.34264395112460129785173016187574039571943773385025452179048 ...
```

followed by `converged (|dk|<1e-36 x3)`. The builder of the panel claim folder reran the whole ladder (2 min 46 s on the Mac Studio with python-flint and numpy from the contributor's environment): every iteration line of the chi = 90 and chi = 100 logs had the same kappa digits as the shipped logs (the columns after kappa, which hold singular values and timings, were not compared). Timing digits on the right of each line will differ. The shell script writes its logs as `sitef_CHI.log`; compare the kappa digits, not the timings. Domino runs (method C, supporting only) take about 87 minutes each at chi = 100 and 110 and cannot be started for chi = 120 and 130 from this folder alone; see `how-we-built-it/README.md`.
