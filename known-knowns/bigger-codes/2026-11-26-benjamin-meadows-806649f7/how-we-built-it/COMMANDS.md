# Commands

The search program is `bststate.cpp` (C++17, standard library only), a seeded bit-swap tabu search in the style of Echols, arXiv:2608.13906. Its usage line names it `bstfast`; the binary used was built as `bststate`.

```sh
c++ -O2 -std=c++17 -o bststate how-we-built-it/bststate.cpp
curl -sS -o a30.12.9.44 https://aeb.win.tue.nl/codes/cwc/d12/a30.12.9.44   # sha256 56d5cb3304998a0322d495e97dbb128b8c3710a8201bcdd080d75c0d72d2f4cd
./bststate 30 9 12 45 1008 300 out.txt a30.12.9.44 1 5 1000000000
```

Arguments: n = 30, w = 9, d = 12, size 45, random seed 1008, time limit 300 s, output file, seed file, tabu tenure drawn from 1 to 5 iterations, restart after 10^9 iterations without improvement (in effect, no restart).

What the program does: it reads the 44 seed words, adds the one weight-9 word with the smallest total distance shortfall against them (it is unique; shortfall 6), then repeats: pick a random word in conflict (distance below 12 to some other word) and a random partner it conflicts with; over both words of the pair, try every move of a 1 to a 0 position where the two words agree, and apply the move with the lowest penalty (penalty = sum over pairs at distance below 12 of 12 minus their distance), skipping tabu moves unless they beat the best penalty so far, ties broken by the seeded generator (std::mt19937). It stops when the penalty is 0 and writes the 45 words.

The original run (log `logs/run-seed1008-original.log`) reported `SOLVED iter 19272004` after 53.07 s. A second run of the same source and command, compiled with g++ 14.2 at -O2, reported the same iteration count after 73.82 s (log `logs/run-seed1008-rerun.log`) and wrote the same 45 lines byte for byte; `rebuild.sh` with Apple clang on macOS also reached it at iteration 19272004 (10.3 s) and matched the object byte for byte. The result depends on the seed and the iteration count only; the time limit just has to be long enough.

`sh how-we-built-it/rebuild.sh` downloads the seed file, checks its sha256, compiles (supplying a stand-in `<bits/stdc++.h>` for compilers without one), runs (with a 600 s limit) and compares the output with the object.

Other runs: the same command with seed 1009 and tabu tenure 10 to 30 was stopped by hand after about 93 s at best penalty 2 (592 restarts, which the program makes when no move is allowed). Other seeds and settings were not recorded for this cell.
