# Exact commands used to build the result (from this folder, Linux x86-64, gcc -O2, Go 1.27, nauty 2.8.8 geng)

    gcc -O2 -o totA totA_pg.c && go build -o totB totB.go
    for k in 1 2 3 4 5 6 7 8; do geng -cq $k | ./totA self | head -1; done > A_n1_8.txt              # maxperiod 2 2 4 6 8 18 42 112
    for k in 1 2 3 4 5 6 7 8; do geng -cq $k | WORKERS=1 ./totB | grep summary; done > B_n1_8.txt    # max_cycle 2 2 4 6 8 18 42 112
    for r in 0 1 2 3 4 5 6 7; do geng -cq 9 $r/8 | PERGRAPH=1 ./totA self > A9_part$r.txt & done; wait   # about 10 min on 8 cores
    for r in 0 1 2 3 4 5 6 7; do geng -cq 9 $r/8 | WORKERS=1 ./totB > B9_part$r.txt & done; wait         # about 14 min on 8 cores
    python3 diff_AB.py "A9_part*.txt" "B9_part*.txt"      # same graph set, 0 per-graph mismatches, max 200, only H?o|]|~
    python3 stepper.py 'H?o|]|~' 1,3,5 1                  # cycle_length 200
    python3 stepper.py 'H?o|]|~' allrules                 # max_over_all_rules_and_starts 200

`self` makes totA count the updated node in its own sum (K = n + 1, rules R ⊆ {0..n}); without it totA computes the
neighbours-only class of A357953. totA_pg.c is totA.c plus one line that prints `G <graph6> <max>` for each graph when
PERGRAPH is set, so A can be diffed against B graph by graph. totB.go was written separately in Go (own graph6
parser, closed-neighbourhood masks, in-degree peeling of transient states, then one walk per cycle) and always counts
the node itself.

The run launched the n = 9 jobs from its own scripts with the same commands (plus `nice` and a `timeout`).
A357952_9.txt and witness_simulation.txt in object/evidence/ are short hand-written summaries of the diff and stepper
outputs above. The geng binary the run used is pinned in object/VALUE.txt (tools/geng) but not shipped.
