# Programs

Copied from the contributor's working folder, byte for byte except where the table says otherwise. These are the programs that produced method A (the CTM values) and method B3 (the open-strip eigenvalues and the Wynn extrapolation).

| File | What it is | Copy |
|---|---|---|
| `mdtm.c` | monomer-dimer row transfer matrix (open or periodic rows), double and exact 128-bit modes; mode `hp` with P = 0 produced the open-strip values | the six standard-header include lines changed from angle brackets to double quotes (see below) |
| `hprun.py` | driver for mode `hp`: double power iteration, exact refinement, fixed-point power iteration, writes `hp_P0_m*.json` | absolute local paths replaced by `{WORKDIR}/` |
| `wynnB3.py` | the Wynn epsilon recipe of `object/PREREG_B3.md`; reads `hp_P0_m*.json`, prints `object/B3_result.txt` | absolute local path replaced by `{WORKDIR}/` |
| `ctm_md.py` | high-precision corner transfer matrix, model `vertex` (monomer-dimer vertex model) | byte for byte |
| `ctmchain.py` | method A pre-registered ladder chi = 12, 16, ..., stop rule | absolute local paths replaced (`{WORKDIR}/ctm_md.py`, interpreter path replaced by `python3`) |
| `ctmchain_ext.py` | method A extension chi = 32 to 48, warm-started from the chi = 28 state | same replacements as `ctmchain.py` |

The six standard-header lines of `mdtm.c` were written with angle brackets in the original; the folder rules reject angle-bracket tokens, so the shipped copy writes them with double quotes (for example `#include "stdio.h"`). Nothing else differs. sha256 of the original `mdtm.c`: 44c92bdda412d9a929dfae23b913abe7970fb1f37020d8e0c2e44cfff8ad37e6. The builder compiled the shipped copy and checked it (below).

`{WORKDIR}` means the folder you run the programs in. To make a working copy:

```
mkdir work && cp programs/* work/ && cd work
for f in hprun.py wynnB3.py ctmchain.py ctmchain_ext.py; do sed "s|{WORKDIR}|$PWD|g" $f > $f.tmp && mv $f.tmp $f; done
```

## Build and run commands (from the contributor's report, reproduced by the builder of this folder)

Method B3, strips:

```
cc -O3 -mcpu=native -DEXACT mdtm.c -o mdtm_ex       # exact 128-bit integers
cc -O3 -mcpu=native mdtm.c -o mdtm_dbl              # double precision
./mdtm_ex count 4 0 4                               # prints 10012 = A028420(4): matchings of the 4 x 4 board (open rows, P = 0)
P=0 python3 -I hprun.py 3,4,5,6,7,8,9,10,11,12,13,14   # needs mpmath; writes hp_P0_m3.json ... hp_P0_m14.json
P=0 python3 -I hprun.py 29                          # width 29 (see memory below)
python3 -I wynnB3.py 4 > B3_result_rerun.txt        # needs mpmath and all hp_P0_m*.json for m = 3..29
```

`-mcpu=native` is the flag the report records (Apple clang on arm64); on another platform use `-march=native`. `hprun.py` runs `mdtm_dbl` and `mdtm_ex` from `{WORKDIR}/` with `NTH=12` threads. The report ran the widths in groups with `hprun.py` (`4,6,...,28`, `5,7,...,23`, `25,27`, `29` for the periodic family, P = 1; the open family used the same driver with `P=0`); the exact command lines for the open family are not recorded beyond the log `object/hprun_open.out`, which lists widths 3 to 29 with the time of each.

Method A, CTM:

```
python3 -m pip install numpy python-flint mpmath      # versions the author used are not recorded
VECLIB_MAXIMUM_THREADS=2 OMP_NUM_THREADS=2 python3 -I ctm_md.py vertex 12 400 256 - ctm_state_12.json    # one rung: model, chi, iteration cap, bits, previous state or -, output state
python3 -I ctmchain.py        # the pre-registered ladder; writes ctm_chi*.log, ctm_state_*.json, ctm_ladder.json
python3 -I ctmchain_ext.py    # the extension chi = 32..48; needs ctm_state_28.json from the previous step
```

Run `ctmchain.py` and `ctmchain_ext.py` in the working folder (they write their logs in the current directory).

## What the builder of this folder ran

On 2026-10-19 (UTC) in a scratch copy: the shipped `mdtm.c` compiled with both commands and printed 10012 for `count 4 0 4` and 2810694 for `count 5 0 5`; `hprun.py` with `P=0` for widths 3 to 14 gave `hp_P0_m*.json` files byte-for-byte identical to the shipped ones for the widths compared (3, 4, 7, 12, 14); `wynnB3.py 4` on the shipped `hp_P0_m*.json` printed text identical to `object/B3_result.txt` and wrote a `wynnB3_m0_4_all.json` identical to the shipped one; one CTM rung (`ctm_md.py vertex 12 400 256 - ...`) reproduced `object/ctm_chi12.log` (iteration number, kappa and singular value columns). The full ladders and widths above 14 were not rerun by the builder.

## Runtime and memory

| Program | Time | Memory |
|---|---|---|
| `hprun.py` open strips, widths 3 to 29, one width after another | summed from `object/hprun_open.out`: 680 s in all; width 24: 7.8 s, 25: 15.9 s, 26: 31.8 s, 27: 61.8 s, 28: 177.8 s, 29: 377.3 s (the report notes that the 29 run took about 10 minutes under load, the log of an earlier run of the periodic family has 393 s) | the report records peak about 13 GB at width 28 and about 26 GB at width 29 (state space 2^29, 8.6 GB per exact vector); smaller widths proportionally less; run no other job above 10 GB alongside |
| `wynnB3.py` | seconds (mpmath, 70 digits) | small |
| `ctm_md.py` vertex, one rung | from the logs: chi = 12 about 1.2 s, chi = 28 about 1.1 s, chi = 48 about 4.9 s (sum of the per-iteration times); the whole ladder chi = 12 to 48 sums to about 19 s | not recorded; the chi = 48 state file is 2.7 MB |
