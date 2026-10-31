# Commands that built the object
Inputs: the organisers' i08.json (from ihtc2024_competition_instances.zip) and their published sol_i08.json
(https://ihtc2024.github.io/assets/files/solutions/public/IHTP/sol_i08.json).

    clang++ -O2 -std=c++17 -o anneal anneal.cc
    python3 ihtp_flat.py export i08.json sol_i08.json i08.flat        # published solution -> flat
    ./anneal i08.flat run1.best 150 1                                       # run 1: 150 s, seed 1
    python3 ihtp_flat.py import i08.json run1.best run1_sol.json
    python3 ihtp_flat.py export i08.json run1_sol.json run1.flat
    ./anneal run1.flat run2.best 300 2                                         # run 2: 300 s, seed 2
    python3 ihtp_flat.py import i08.json run2.best sol_i08.json

Annealing depends on wall-clock time, so a rerun gives a solution of similar but not identical cost.
