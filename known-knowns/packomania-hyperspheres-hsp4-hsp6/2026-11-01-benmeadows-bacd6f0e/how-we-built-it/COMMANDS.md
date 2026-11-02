# Commands (lane hsp4-b, search over hsp4 N = 211..300)

Files here are the lane's search code as committed (check.py is the lane's own 50-digit checker).

    python3 search.py ...        # round 1: seeds (two-shell, D4 cuts, random), penalty compression, MBH, SLP polish
    sh driver.sh OUT WORKER NWORKERS JOBS   # runs `python3 mbh2.py N seed seconds OUT/npy [init.npy]` per job line
    python3 chain.py N OUT/npy SEED init.npy   # seed N from the best N-1 packing plus one ball at the largest probed hole
    python3 mbh2.py N SEED 1100 OUT/npy init.npy   # 1100 s basin hopping from that seed, then SLP polish
    python3 export.py ...        # write the coordinate file
    python3 check.py FILE        # the lane's 50-digit check

The lane did not record its exact shell history or seeds per run; the argument forms above are taken from the scripts'
usage lines. Heuristic search is not bit-for-bit reproducible; the checker in `verify-it-yourself/` is what matters.
