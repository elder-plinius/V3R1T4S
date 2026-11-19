# Run it yourself (fresh shell, from this folder)

## 1. Quick checks (a few seconds)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

Needs Python 3 (standard library only). If a C compiler and/or Go are on PATH, step 5 also compiles the shipped
Programs A (object/code/totA_pg.c) and B (object/code/totB.go) and runs them on the saved optimal graphs and the
witness; without them that part is skipped. `SMALL=7 sh verify-it-yourself/run_checks.sh` extends the nauty-free
check of step 4 to n = 7 (a few minutes).

## 2. Recompute a(1..9) with both programs (needs gcc, Go and nauty 2.8.8's geng; about 16 minutes on 8 cores)
    FULL=1 sh verify-it-yourself/run_checks.sh   # step 6: fresh A and B outputs identical to object/evidence/, last line PASS

(set GENG=/path/to/geng if geng is not on PATH) or by hand:

    cd how-we-built-it
    gcc -O2 -o totA totA_pg.c && go build -o totB totB.go
    for k in 1 2 3 4 5 6 7 8; do geng -cq $k | ./totA self | head -1; done              # maxperiod 2 2 4 6 8 18 42 112
    for k in 1 2 3 4 5 6 7 8; do geng -cq $k | WORKERS=1 ./totB | grep summary; done    # max_cycle 2 2 4 6 8 18 42 112
    mkdir -p out
    for r in 0 1 2 3 4 5 6 7; do geng -cq 9 $r/8 | PERGRAPH=1 ./totA self > out/A9_part$r.txt & done; wait
    for r in 0 1 2 3 4 5 6 7; do geng -cq 9 $r/8 | WORKERS=1 ./totB > out/B9_part$r.txt & done; wait
    python3 diff_AB.py "out/A9_part*.txt" "out/B9_part*.txt"   # 261080 graphs, 0 mismatches, max 200, only H?o|]|~
    for f in out/*.txt; do cmp "$f" ../object/evidence/$(basename "$f"); done   # no output: identical

Note the `self` argument: without it totA counts neighbours only (the A357953 class) and gives different numbers.
geng's residue split `r/8` is deterministic for a given nauty version; with another version the per-part files may
differ, but the totals, the per-graph maxima and the overall maximum may not.

## 3. The witness alone
    python3 how-we-built-it/stepper.py 'H?o|]|~' 1,3,5 1                     # cycle_length 200
    python3 verify-it-yourself/check_self.py witness 'H?o|]|~' 1,3,5 1 200    # preperiod=0 cycle_length=200
    python3 verify-it-yourself/check_self.py graph 'H?o|]|~' 200              # no rule or start on this graph beats 200

## Rebuilding the object
object/VALUE.txt is a hand-written summary of the outputs above; its pins are `sha256sum` values of the files in
object/code/ and object/evidence/ (and of the geng binary used, which is not shipped).
