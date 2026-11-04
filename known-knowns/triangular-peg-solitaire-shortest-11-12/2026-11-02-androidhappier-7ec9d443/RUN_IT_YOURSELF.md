# Run it yourself (fresh shell, from this folder)

## 1. Checks (under one second; python3, optionally a C compiler)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

## 2. The simulators by hand
    python3 verify-it-yourself/check_peg.py 12 object/T12_25moves.txt a3 25 j12
    # check_peg: n=12 vacancy=a3 moves=25 jumps=76 pegs_left=1 finish=j12 merges=0 VALID
    python3 verify-it-yourself/pegcheck.py 12 object/T12_25moves.txt
    # n=12 start_vacancy=a3 pegs_left=1 finish=j12 jumps=76 moves=25 VALID
    cc -O2 -o pegsim2 verify-it-yourself/pegsim2.c && ./pegsim2 12 object/T12_25moves.txt
    # n=12 jumps=76 moves=25 pegs_left=1 VALID
    python3 verify-it-yourself/check_bound.py    # object/BOUND.txt matches the values recomputed from the solution

## 3. Rebuild the object (optional; about 4 to 10 minutes on one core, up to about 1 GB of RAM; gcc with __int128)
    gcc -O2 -march=native -o beam3 how-we-built-it/beam3.c
    BEAM_V=2 ./beam3 12 200000 3 45 > found.txt 2> found.log
    tail -1 found.txt > T12_rebuilt.txt
    python3 verify-it-yourself/pegcheck.py 12 T12_rebuilt.txt     # moves=25 VALID
    cmp T12_rebuilt.txt object/T12_25moves.txt                     # identical (the run's output, how-we-built-it/logs/)

Expected: the run's saved output how-we-built-it/logs/T12_B200000_W3_V2.txt ends with the line in
object/T12_25moves.txt. With BEAM_SEED=21 or 22 the search finds other 25-move solutions (logs/..._s21.txt, _s22.txt).
