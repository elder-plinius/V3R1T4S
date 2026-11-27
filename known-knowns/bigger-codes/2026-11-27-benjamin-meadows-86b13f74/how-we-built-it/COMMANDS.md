# Commands

The search program is `cwbst.cpp` (C++17, standard library only): a seeded bit-swap tabu search for binary constant-weight codes. Its move scheme and parameter names (tabu tenure drawn from a range, aspiration on a new best penalty, restart after a run without improvement) follow `bit-swap-tabu.c` by Christopher D. Rosin (https://github.com/Constructive-Codes/CWBC, MIT licence; notice in `LICENSE-CWBC`); starting from a known code is the seeded variant described by William Echols (arXiv:2608.13906). The bitset bookkeeping is the program's own.

Seed code: https://aeb.win.tue.nl/codes/cwc/d10/a25.10.12.141H (sha256 71f7603eac9ee759f07696eb2741dcb9b159503eee639f13a28bfd66493a4a97). It is converted to one 0/1 row per word, in the file's order, by `seed_to_rows.py`.

```sh
c++ -O2 -std=c++17 -o cwbst how-we-built-it/cwbst.cpp
curl -sS -o a25.10.12.141H https://aeb.win.tue.nl/codes/cwc/d10/a25.10.12.141H
python3 how-we-built-it/seed_to_rows.py a25.10.12.141H 25 > start.txt
./cwbst 25 12 10 142 1017 120 out-142.txt start.txt 5 15 1000000
```

Arguments: n = 25, w = 12, d = 10, target size, random seed, CPU-second limit, output file, start file, tabu tenure minimum and maximum, restart after this many iterations without improvement. The program reads the start file's words, adds the missing word(s) of least distance shortfall against them, and then repeats: pick a random word in conflict (distance below 10 to some other word) and a random partner it conflicts with; over both words, try every move of a 1 to a 0 position, and apply the move with the lowest penalty (sum over pairs at distance below 10 of 10 minus their distance), skipping tabu moves unless they beat the best penalty so far, ties broken by the seeded generator (std::mt19937). It stops when the penalty is 0 and writes the words. It is deterministic for a given random seed and start file; the CPU limit only decides whether a run stops before it succeeds.

The run, in order (`chain.tsv`; each run's output is the next run's start file; tabu settings by seed parity: even seeds 1 5 1000000000, odd seeds 5 15 1000000):

| step | size | random seed | tabu min, max, restart | steps to penalty 0 | CPU s (original) |
|---|---|---|---|---|---|
| 1 | 142 | 1017 | 5 15 1000000 | 22733579 | 80.7 |

Total CPU time of the original run: 80.7 s. The original runs ran on Linux x86-64 (g++ 13.3, -O3 -march=native); `logs/original-runs.tsv` lists the original runs of the chain (the runs that found nothing are not listed). `sh how-we-built-it/rebuild.sh` downloads the seed file, checks its sha256, converts it, compiles with -O2 (plus -mpopcnt on x86-64, for speed only), replays every step with the recorded seed and settings, checks that each ends with the recorded step count, and compares the final output with the object byte for byte; `logs/rebuild-run.log` is the output of one such replay.
