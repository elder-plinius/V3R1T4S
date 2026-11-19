# Run it yourself (fresh shell, from this folder)

## 1. Quick checks (a few seconds)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

Needs Python 3 (standard library only). If a C compiler and/or Go are on PATH, step 5 also compiles the shipped
Programs A (object/code/otA.c) and B (object/code/otB.go) and runs them on the saved optimal graphs, the OEIS n = 7
example, the witness and the runner-up; without them that part is skipped. `SMALL=7 sh verify-it-yourself/run_checks.sh`
extends the nauty-free check of step 4 to n = 7 (slower, pure Python).

## 2. Recompute a(1..8) with both programs (needs a C compiler, Go and nauty 2.8.8's geng; a few minutes on 8 cores)
    FULL=1 sh verify-it-yourself/run_checks.sh   # step 6: fresh A and B outputs identical to object/evidence/, last line PASS

(set GENG=/path/to/geng if geng is not on PATH) or by hand:

    cd how-we-built-it
    gcc -O3 -o otA otA.c && go build -o otB otB.go
    for k in 1 2 3 4 5 6 7; do geng -cq $k | ./otA | head -1; done     # maxperiod 2 2 4 6 16 26 66
    for k in 1 2 3 4 5 6 7; do geng -cq $k | ./otB | head -1; done     # maxperiod 2 2 4 6 16 26 66
    mkdir -p out
    for r in 0 1 2 3 4 5 6 7; do geng -cq 8 $r/8 | ./otA pg  > out/A8_part$r.txt & done; wait
    for r in 0 1 2 3 4 5 6 7; do geng -cq 8 $r/8 | ./otB -pg > out/B8_part$r.txt & done; wait
    python3 diff_AB.py "out/A8_part*.txt" "out/B8_part*.txt"   # 11117 graphs, 0 mismatches, max 150, only GCQfBg
    for f in out/*.txt; do cmp "$f" ../object/evidence/$(basename "$f"); done   # no output: identical

geng's residue split `r/8` is deterministic for a given nauty version; with another version the per-part files may
differ, but the totals, the per-graph maxima and the overall maximum may not.

## 3. The witness alone
    python3 how-we-built-it/ostepper.py 'GCQfBg' 0,2 1,3,4 1                       # transient=0 cycle_length=150
    python3 verify-it-yourself/check_ot.py witness 'GCQfBg' 0,2 1,3,4 1 150         # transient=0 cycle_length=150
    python3 verify-it-yourself/check_ot.py graph 'GCQfBg' 150 all                   # no rule or start on this graph beats 150

B is the birth set (an OFF node turns ON iff its number of ON neighbours is in B), S the survival set (an ON node
stays ON iff its number of ON neighbours is in S). Start 1 means node 0 ON, all others OFF, in graph6 vertex order.

## Rebuilding the object
object/VALUE.txt is a hand-written summary of the outputs above; its pins are `sha256sum` values of the files in
object/code/ and object/evidence/ (and of the geng binary used, which is not shipped).
