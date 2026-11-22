# Programs

Programs copied from the contributor working folder, byte for byte except where the table says otherwise:

| File | What it is | Copy |
|---|---|---|
| `tmlean.c` | memory-lean open-strip column transfer matrix, exact 128-bit fixed point (widths 29 to 40) | five include lines changed (see below) |
| `tm.c` | first open-strip and cylinder transfer matrix program (widths 2 to 28) | five include lines changed (see below) |
| `ctmgen2.py` | high-precision corner transfer matrix, models `site`, `domino` (and an abandoned `block`) | byte for byte |
| `PREREG_B.md` | the pre-registered recipe for method B | byte for byte |
| `extrap.py` | Wynn epsilon function used by `prereg_b.py` | byte for byte |
| `rqlean.py` | runs `./tmlean` and turns its output into lambda | byte for byte |
| `rq.py`, `drive.py` | Rayleigh quotient from the binary dump of `tm`, and the driver that ran `tm` over widths | byte for byte |
| `prereg_b.py` | executes PREREG_B.md on the two lambda files | absolute local path replaced by `{WORKDIR}` (the original is not shipped) |
| `drivelean.py` | driver that ran `tmlean` for widths and wrote lambda lines | absolute local path replaced by `{WORKDIR}` |
| `sitechain2.sh` | the site CTM ladder chi = 20 to 100 | absolute local path replaced by `{WORKDIR}`, and the contributor's interpreter path replaced by `python3` |

The five standard-header lines of `tm.c` and `tmlean.c` were written with angle brackets in the original; the folder checker rejects angle-bracket tokens, so the shipped copies write them with double quotes (for example `#include "stdio.h"`). Nothing else differs, and both compile and run as before (the builder compiled both and ran `./tmlean 11 10 4 x count`). sha256 of the originals: `tm.c` 394f9fc336005f2923dcdb64c4bdf0d2b553120ae4062e33ffbf51dfb1ee6d63, `tmlean.c` 58fb0ade8783fc1dc4eddc770dbc8cf70eb379e33806bc4be496b469d34dc8c1.

`{WORKDIR}` means the folder you run the program in. To substitute it in a working copy:

```
mkdir work && cp how-we-built-it/* work/ && cp object/lam_open.txt object/lam_open_lean.txt work/ && cd work
for f in drivelean.py prereg_b.py sitechain2.sh; do sed "s|{WORKDIR}|$PWD|g" $f > $f.tmp && mv $f.tmp $f; done
```

## Build and run commands

Method B, new program (command recorded in the contributor's report and reproduced by the builder of this folder):

```
cc -O3 -march=native -o tmlean tmlean.c -lpthread
./tmlean m iters nthreads x          # prints two lines, W and V, sums of squares in 40-bit limbs; lambda = sqrt(W/V)
./tmlean m iters nthreads x count    # exact count: prints the number of independent sets of the king graph on an m x (iters+1) grid
python3 -I drivelean.py 100 out.txt 37 38 39 40    # 100 sweeps per width, appends "m 100 lambda" lines to out.txt; needs mpmath; runs ./tmlean with 12 threads
```

Example of the exact count mode: `./tmlean 11 10 4 x count` prints 60711713670028729, which is A063443(12).

Method B, old program (widths 2 to 28): the report gives `cc -O3 -march=native -o tm tm.c -lpthread`, and the driver calls `./tm m cyc iters 12 prefix` (cyc = 0 for open strips) and then `rq.py`; the report records `python -I drive.py 0 2 30 160`, stopped by hand after m = 28 for memory (and `drive.py 1 3 22 160`, `1 23 26 160` for cylinders, which are not used by the claim). The exact-count build of `tm.c` is selected by a sixth command-line argument; its exact argument list is not recorded in the report. `drive.py` needs numpy and mpmath.

Method B, evaluation: `python3 -I prereg_b.py > out.txt` (needs mpmath; reads `lam_open.txt` and `lam_open_lean.txt` and `extrap.py` from `{WORKDIR}`) reproduces `object/prereg_b_output.txt` byte for byte (the builder checked this with `diff`).

Method A and C: `python3 -I ctmgen2.py MODEL CHI ITERS PRECISION INIT OUTSTATE` with MODEL `site` or `domino`, CHI the bond dimension, ITERS the iteration cap (400), PRECISION 256 bits, INIT the previous state file or `-` for a cold start, OUTSTATE the state file written. Needs numpy and python-flint. Environment used: `VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2`; for the domino model also `THR=1e-11`.
- Site ladder: `sh sitechain2.sh` (chi = 20, 30, ..., 100, each warm-started from the previous state, stop when the change of kappa is below 1e-36 three times in a row).
- Domino ladder (supporting only): cold-start runs `THR=1e-11 python3 -I ctmgen2.py domino CHI 400 256 - domg_state_CHI.json` for CHI = 80, 100, 110; chi = 120 was warm-started from the state of a separate run with `THR=1e-9`, and chi = 130 from a snapshot of the chi = 120 state; those two start files are not shipped (they are tens of megabytes), so chi = 120 and 130 cannot be rerun from this folder alone. The shell scripts that ran the domino ladder (`domchain3.sh`, `domchain4.sh`) are not shipped.

## Runtime and memory

| Program | Time | Memory |
|---|---|---|
| `tmlean` width 40, 100 sweeps, 12 threads | about 8 minutes | about 26 GB (two frontier arrays of 8.6 GB, two vectors of 4.3 GB) |
| `tmlean` width 30 and 34, 100 sweeps | about 4 seconds and 30 seconds (report); the builder measured 4 s at width 30 and 6 s at width 31 | smaller by roughly the golden ratio per width; not recorded |
| `tm` width 28 | not recorded | about 26 GB (report) |
| `ctmgen2.py site`, ladder chi = 20 to 100 | about 3 to 4 minutes in total (sum of the per-iteration times in the logs: 230 s; 2 min 46 s on rerun) | not recorded; the chi = 100 state file is 16 MB |
| `ctmgen2.py domino`, chi = 100 / 110 / 120 / 130 | about 87 / 87 / 87 / 24 minutes (sum of logged per-iteration times, 202 / 162 / 136 / 38 iterations) | not recorded |
