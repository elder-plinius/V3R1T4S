# Run it yourself (fresh shell, from this folder)

## 1. Quick checks (under a minute)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

Needs Python 3 (standard library only). If a C compiler and/or Go (>= 1.21) are on PATH, step 5 also compiles the
shipped Programs A (object/code/A/totF.c) and B (object/code/B/main.go) and runs them on the saved optimal graphs
for n = 1..9, the OEIS n = 7 example, the n = 10 witness and the runner-up; without them that part is skipped.

## 2. Recompute with both programs (needs a C compiler, Go and nauty 2.8.8's geng on PATH, or GENG=/path/to/geng)
    FULL=1 sh verify-it-yourself/run_checks.sh   # a(1..9) and residue class 7/32 (the witness class), ~1 core-hour
    FULL=2 sh verify-it-yourself/run_checks.sh   # all 32 classes: ~2 core-hours (A) + ~12 core-hours (B)

The fresh outputs must be byte-identical to object/evidence/ (step 6 of the script). Or by hand:

    cd how-we-built-it
    gcc -O3 -march=native -o totF totF.c
    mkdir -p B && cp main.go go.mod B/ && (cd B && go build -o ../totBgo .)
    for k in 1 2 3 4 5 6 7 8 9; do geng -cq $k | ./totF | grep '^n='; done        # maxperiod 1 2 2 6 7 18 38 96 180
    for k in 1 2 3 4 5 6 7 8 9; do geng -cq $k | ./totBgo nbr | grep '^n='; done   # same maxima
    mkdir -p out
    seq 0 31 | xargs -P 8 -I{} sh runA.sh 10 {} 32
    seq 0 31 | xargs -P 8 -I{} sh runB.sh 10 {} 32
    mkdir -p A B && cp out/A10_* A/ && cp out/B10_* B/
    python3 compare_AB.py A B                                                      # VERDICT AGREE M = 624
    for f in out/*.txt; do cmp "$f" ../object/evidence/$(basename "$f"); done      # no output: identical

geng's residue split `r/32` is deterministic for a given nauty version; with another version the per-class files may
differ, but the totals, the combined histogram and the overall maximum may not.

## 3. The witness alone
    python3 how-we-built-it/stepper.py 'I?AAD@oIg' 0,2 2                           # preperiod=0 cycle_length=624
    python3 verify-it-yourself/check_tot.py witness 'I?AAD@oIg' 0,2 2 624           # preperiod=0 cycle_length=624
    python3 verify-it-yourself/check_tot.py graph 'I?AAD@oIg' 624 all               # no rule or start on this graph beats 624

Rule R = {0,2}: a node is ON next step iff 0 or 2 of its neighbours are ON now (the node itself not counted). Start
2 means node 1 ON, all others OFF, in graph6 vertex order.

## Rebuilding the object
object/VALUE.txt is a hand-written summary of the outputs above; its pins are `sha256sum` values of the files in
object/code/ and object/evidence/ (and of the geng binary used, which is not shipped).
