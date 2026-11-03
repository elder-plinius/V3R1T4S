# Commands

Build (ziglang 0.16.0 from PyPI):

    python -m ziglang cc -O2 -o covsearch3.exe covsearch3.c

Multi-seed driver call that found the object (run 2026-10-15-2309):

    python -I multiseed.py covsearch3.exe 85 24 3 76 1500 runs/C85_24_3_b76 11,12,13,14 0.2,0.25,0.3,0.25 - --stop-on-found

The winning worker call (seed 11, pnoise 0.2):

    covsearch3.exe 85 24 3 76 1500 11 C85_24_3_b76_s11_pn0.2.found.txt - 10 1000000 0.2 0

`C85_24_3_b76_s11_pn0.2.log` is that worker's output (finished at step 701893 in 302.1 s).
