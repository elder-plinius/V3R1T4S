# Commands that built the object
Inputs: the organisers' i16.json (from ihtc2024_competition_instances.zip) and their published sol_i16.json
(https://ihtc2024.github.io/assets/files/solutions/public/IHTP/sol_i16.json).

    clang++ -O2 -std=c++17 -o anneal anneal.cc
    python3 ihtp_flat.py export i16.json sol_i16.json i16.flat        # published solution -> flat
    ./anneal i16.flat run1.best 150 1                                       # run 1: 150 s, seed 1
    python3 ihtp_flat.py import i16.json run1.best run1_sol.json
    python3 ihtp_flat.py export i16.json run1_sol.json run1.flat
    ./anneal run1.flat run2.best 300 2                                         # run 2: 300 s, seed 2
    python3 ihtp_flat.py import i16.json run2.best sol_i16.json

Annealing depends on wall-clock time, so a rerun gives a solution of similar but not identical cost.
