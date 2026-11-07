# Run it yourself (fresh shell, from this folder)

## 1. Check the solution (under 2 seconds)
    sh verify-it-yourself/run_checks.sh                                   # last line: PASS

Or one simulator at a time:
    python3 verify-it-yourself/check_peg.py 11 object/T11_22moves.txt a2 22 j11
    #   check_peg: n=11 vacancy=a2 moves=22 jumps=64 pegs_left=1 finish=j11 merges=0 VALID
    python3 verify-it-yourself/pegcheck.py 11 object/T11_22moves.txt
    #   n=11 start_vacancy=a2 pegs_left=1 finish=j11 jumps=64 moves=22 VALID
    cc -O2 -o pegsim2 verify-it-yourself/pegsim2.c && ./pegsim2 11 object/T11_22moves.txt
    #   n=11 jumps=64 moves=22 pegs_left=1 VALID

## 2. Rebuild the object (optional; about 2.5 to 5 minutes on one core, about 1 GB of RAM; needs gcc with __int128)
    gcc -O2 -march=native -o beam3 how-we-built-it/beam3.c
    BEAM_V=2 ./beam3 11 200000 2 45 > beam.txt 2> beam.log
    tail -1 beam.txt > found.txt && python3 verify-it-yourself/check_peg.py 11 found.txt a2 22 j11

Expected: beam.txt ends with "SOLVED n=11 moves=22", "start a2" and the move line, and found.txt is byte-identical
to object/T11_22moves.txt (`cmp found.txt object/T11_22moves.txt`). The beam is deterministic with these arguments
(no seed). The run's own stderr log is how-we-built-it/beam_T11_B200000_W2_V2.log. Arguments: n=11, beam width
B=200000, Merson-region weight W=2, at most 45 move layers; BEAM_V=2 adds a dead-peg penalty to the ranking.
