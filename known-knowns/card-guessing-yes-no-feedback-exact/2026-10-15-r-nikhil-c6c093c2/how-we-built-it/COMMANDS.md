# How the objects were built (exact commands)

    c++ -O2 -std=c++17 -I/opt/homebrew/include cg_solver.cpp -o cg_solver -L/opt/homebrew/lib -lgmp -lz
    for n in $(seq 2 16); do ./cg_solver $n 2 n$n.txt.gz; done      # each prints a JSON line with the exact value
    # cg_solver_v2.cpp is identical except for a wider f field (needed for n >= 17); it rebuilds n = 2..16 byte-identically.
    python3 -I bruteforce_raw_definition.py 4 2                      # raw-definition cross-check on tiny decks
    python3 -I strategy_eval.py 5 5 optimal                           # independent Python recursion (ESP deck: 6.628841)
    

Solver: Luo's Appendix A recursion on the canonical state (g, sorted (r_i, f_i) pairs with r_i >= 1); forward
enumeration of reachable states (C > 0) layer by layer in L; backward evaluation of W = C * V+ as exact 128-bit
integers with the arrangement counts from (A.1) summed in GMP; the count identity C = C(yes) + C(no) asserted at every
state and label; output streamed as gzip text, layers in increasing L. Total about 20 minutes for n = 2..16 on a laptop.
PREREG.md is the run's pre-registration (frozen before any value was computed by this solver).
