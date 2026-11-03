# Commands

Build (ziglang 0.16.0 from PyPI; the exact flags of the binary used in run 2026-10-15-1535 were not recorded, and
this command was checked to build a working binary on 2026-10-15):

    python -m ziglang cc -O2 -o covsearch3.exe covsearch3.c

The screen that found the object (run 2026-10-15-1535, "screen2", cold starts at live - 1, 180 s per cell):

    python -I screen.py cands.csv covers.json index.tsv covsearch3.exe redund.exe out.csv cells 180 WORKERS PNOISE DEADLINE cold

screen.py calls covsearch3 with seed 1, tenure 10, maxw 1000000 and maxcand 0. covers.json is the LJCR Zenodo v1.2
covers.json; its designs are extracted and checked with redund.exe even in cold mode, and covers_index.py builds the
byte index. For C(61,25,3) the call was

    covsearch3 61 25 3 27 180 1 found_b27.txt - 10 1000000 PNOISE 0

With `PNOISE = 0.2`, `covsearch3` is deterministic in steps and finishes at step `487885` (~193 s on a single core), writing a file whose sha256 (`097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e`) matches `object/C61_25_3_27blocks.txt` byte for byte (verified in `runs/2026-10-15-2309/attempts/evaluator-first/rebuild_C61/` and `package_code/rebuild/fresh_build_run.log`).

search_b27.log is that call's output.
