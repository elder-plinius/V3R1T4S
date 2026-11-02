# Commands (lane sph-d25-32, spherical codes d = 25..32, d+2 <= N <= 3d)

Files here are the lane's code (`src/`), run logs (`runs/`) and per-cell results (`cells.tsv`) as committed.

    python3 src/screen.py d N 25 SEED OUT TABLE        # stage 1: 25 s per cell (seeds.py + pen.py)
    python3 src/deep.py 31 64 SECONDS SEED OUT 0.030322662292   # stage 2: ~1000 loose restarts, top 6 fully descended
    python3 src/mbh.py 31 64 SECONDS SEED INFILE OUT 0.030322662292   # stage 3: basin hopping from the stage-2 best
    python3 src/check.py FILE                          # the lane's 50-digit check

Argument forms are from the scripts' argv handling; seeds and seconds per run are in `runs/*.log` where recorded.
The lane did not record its exact shell history. Heuristic search is not bit-for-bit reproducible; the checker in
`verify-it-yourself/` is what matters.
