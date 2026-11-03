# Commands

Build (ziglang 0.16.0 from PyPI):

    python -m ziglang cc -O2 -o covsearch3.exe covsearch3.c

The screen that found the object (run 2026-10-15-2309, `screen3`, cold starts at `live - 1`, 180 s per cell, `pnoise = 0.25`):

    python -I screen.py screen3_cands.csv covers.json covers_index.tsv covsearch3.exe redund.exe screen3_results.csv screen3_cells 180 2 0.25 DEADLINE cold

For `C(53,20,3)` the worker call was:

    covsearch3.exe 53 20 3 34 180 1 found_b34.txt - 10 1000000 0.25 0

`search_b34.log` is that worker's output (finished at step 142760 in 33.3 s).
