# Commands that built the object
    g++ -O2 -std=c++17 -o sa_bin how-we-built-it/sa.cpp
    ./sa_bin set5.exam <start.sol> <seconds> <seed> <T0> <out.sol>
Lineage (lineage.txt, every file scored by verify-it-yourself/check.py; paths are the authors' workspace):
OptHub's posted set5.sol (2,327) -> 120 s, seed 3, T0 3 -> 2,312 -> 3600 s, seed 101, T0 3 -> 2,305 (the object; the
one-hour step ran through run_hour.py). The search is time-limited, so a rerun gives a different timetable.
Control: an improving-only local search with the same moves, 30 s from the posted file: 2,327 and 2,326 (hillclimb_control.txt).
No packages beyond a C++17 compiler and Python 3.
