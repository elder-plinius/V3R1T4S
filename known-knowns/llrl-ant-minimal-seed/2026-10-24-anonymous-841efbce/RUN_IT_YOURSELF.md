# Run it yourself (fresh shell, from this folder)
1. Onsets of every listed seed: `sh verify-it-yourself/run_checks.sh` -> last line `PASS` (~3 s; needs python3).
   It re-simulates the blank grid (onset 256241) and the 15 seeds in object/minimisers.txt and checks each enters the
   blank grid's period-384 highway word at exactly the listed update.
2. Completeness, checker A (first-read DFS with a 384-phase completion test):
   `cd how-we-built-it/code/hsearch && cc -O2 -o hsearch hsearch.c && ./hsearch LLRL 3 250 256241 384 - 1 0 6`
   -> `RESULT ... K=3 best_onset=245 minimisers=1 ...` (seconds). k=5: `./hsearch LLRL 5 175 256241 384 - 4 $w 6` for
   w=0..3 (one worker takes ~50 min) or the balanced `./qrun.sh 5 174 40 8` (40 pieces, about 1 CPU-hour total).
3. Completeness, checker B (fixed-depth light-cone DFS, written separately):
   `cd how-we-built-it/code/lcone4 && cc -O2 -o lcb_fast lcb_fast.c && ./lcb_fast LLRL 3 245 1 0`
   -> 0 VIOLATION lines (nothing at 244), one MIN at 245, last line `DONE ... leaves=1283843 viol=0 mins=1 flags=0`.
   k=5: `LCB_SPLITD=25 ./lcb_fast LLRL 5 174 40 $i` for i=0..39 (a few CPU-minutes in total; leaves sum 542179718).
4. K0 = 12: `./hsearch LLRL 11 0 256241 384 - 1 0 6` (NONE) and `... 12 0 ...` (10 seeds); same with `./lcb_fast LLRL 11 0 1 0` / `12 0 1 0`.
Full command list with expected outputs: how-we-built-it/REPRODUCE.md; saved outputs: how-we-built-it/data/.
Rebuild the object: object/minimisers.txt lists A's and B's minimiser outputs (identical) in the fixed frame.
