# Commands (lane hsp4-a, search over hsp4 N = 120..210)

Files here are the lane's search code and logs as committed; `best/` (one file per N) is omitted, and the
final packing for this cell is `object/` in this package.

    gcc -O3 -march=native -shared -fPIC -o librelax.so relax.c -lm   # L-BFGS Riesz relaxation, penalty descent (core.py loads it)
    mkdir -p best logs
    python3 run.py 270                       # pass 1: 270 s per cell, all N (random starts + Riesz + basin hopping)
    python3 run.py 150 $(cat pass2.order)    # pass 2: neighbour seeding (chain.py), 150 s per cell
    FRESH=1 python3 run.py 140 $(cat pass3.order)   # pass 3: fresh starts, 140 s per cell
    FRESH=1 python3 run.py 140 $(cat pass4.order)   # pass 4: fresh starts on the nearest unbeaten cells
    python3 finalize.py                      # sequential-LP polish (polish.py, HiGHS) and summary.tsv
    python3 check_lane.py                    # the lane's own 50-digit check of each saved result

`passN.out` hold each pass's per-cell output (N, best radius, difference to the table); `summary.tsv` is the final
table. The pass commands above are reconstructed from run.py's argument handling and the pass order files; the lane
did not record its shell history. Seeds are `1000 * N + (time mod 1000)`, so a rerun is not bit-for-bit
reproducible; the checker in `verify-it-yourself/` is what matters.
