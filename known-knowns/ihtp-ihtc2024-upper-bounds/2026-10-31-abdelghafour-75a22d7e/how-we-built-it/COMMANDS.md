# Commands that built the object
Inputs: the organisers' m08.json (from ihtc2024_final_instances.zip) and their published sol_m08.json
(https://ihtc2024.github.io/assets/files/solutions/hidden/IHTP/sol_m08.json).

    clang++ -O2 -std=c++17 -o anneal anneal.cc
    python3 ihtp_flat.py export m08.json sol_m08.json m08.flat        # published solution -> flat
    ./anneal m08.flat run1.best 150 1                                       # run 1: 150 s, seed 1
    python3 ihtp_flat.py import m08.json run1.best run1_sol.json
    python3 ihtp_flat.py export m08.json run1_sol.json run1.flat
    ./anneal run1.flat run2.best 300 2                                         # run 2: 300 s, seed 2
    python3 ihtp_flat.py import m08.json run2.best sol_m08.json

Annealing depends on wall-clock time, so a rerun gives a solution of similar but not identical cost.
