# Exact commands used to build the result (from this folder, Linux x86-64, gcc, Go, nauty 2.8.8 geng)

    gcc -O3 -o otA otA.c && go build -o otB otB.go
    for k in 1 2 3 4 5 6 7; do geng -cq $k | ./otA | head -1; done > A_n1_7.txt    # maxperiod 2 2 4 6 16 26 66
    for k in 1 2 3 4 5 6 7; do geng -cq $k | ./otB | head -1; done > B_n1_7.txt    # maxperiod 2 2 4 6 16 26 66
    for r in 0 1 2 3 4 5 6 7; do geng -cq 8 $r/8 | ./otA pg  > A8_part$r.txt & done; wait   # about 1.5 min on 8 cores
    for r in 0 1 2 3 4 5 6 7; do geng -cq 8 $r/8 | ./otB -pg > B8_part$r.txt & done; wait   # about 5 min on 8 cores
    python3 diff_AB.py "A8_part*.txt" "B8_part*.txt"     # 11117 graphs each, 0 mismatches, max 150, only GCQfBg
    python3 ostepper.py 'GCQfBg' 0,2 1,3,4 1             # transient=0 cycle_length=150
    python3 ostepper.py 'FBjng' 0,1,3 2,4,5 1            # OEIS n = 7 example: cycle_length=66
    python3 ospot.py 'GCQfBg'                            # needs numpy: max 150 over all 65536 rules x 256 starts
    geng -cq 8 | wc -l; geng -cq 8 | labelg -q | sort -u | wc -l     # 11117 and 11117 (completeness.txt)

otA.c walks every rule (B,S) with B, S subsets of {0..n-1}; rule bit c means c is in B and bit n+c means c is in S.
Its raw witness mask is B={0,2,7} S={1,3,4}; count 7 cannot occur on GCQfBg (maximum degree 4), so the dynamics equal
B={0,2} S={1,3,4}. otB.go was written separately in Go (own graph6 parser, rules over counts 0..maxdeg only, which is
complete because a node never has more ON neighbours than its degree; in-degree peeling of transient states, then one
walk per cycle). Neither program counts the node in its own sum: the node's own state only selects B or S.

The run launched the n = 8 jobs from its own scripts with the same commands. A357951_8.txt, witness_simulation.txt
and completeness.txt in object/evidence/ are short summaries of the outputs above. The geng binary the run used is
pinned in object/VALUE.txt (tools/geng) but not shipped. PREREG.md is the run's frozen plan; no null_test.md was
required (deterministic exhaustive enumeration, see PREREG.md).
