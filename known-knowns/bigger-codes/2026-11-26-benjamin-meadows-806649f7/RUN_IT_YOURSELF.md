# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
== exact check of the code against the table cell
file sha256 806649f74bcb4ec5746f248ef5f087f88d56120661f95e0d7a464d9965f9060d
n = 30, d = 12, w = 9, words read: 45
pairs checked: 990 (all of them)
distance distribution: 12:756 14:141 16:36 18:57
minimum distance: 12
table lower bound 44, upper bound 74, size 45: margin over the lower bound 1
PASS
== planted bugs (each must be rejected)
planted bug: pair moved too close (word 1: 1 moved from position 0 to 13) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: changed weight (word 1, position 2, 0 -> 1) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: duplicated word (word 1 written over the last word) -> checker exit 1, last line FAIL (rejected, as required)
PASS
PASS
```

The two steps can also be run one at a time:

```sh
python3 verify-it-yourself/check_cw.py object/A-30-12-9-45words.txt 30 12 9 45 44 74 806649f74bcb4ec5746f248ef5f087f88d56120661f95e0d7a464d9965f9060d
python3 verify-it-yourself/planted_bugs.py object/A-30-12-9-45words.txt 30 12 9 45 44 74
```

check_cw.py arguments: code file, n, d, w, claimed size, table lower bound, table upper bound, expected sha256 (optional).

## Rebuild

```sh
sh how-we-built-it/rebuild.sh
```

Needs curl, a C++17 compiler and Python 3. It downloads the seed code https://aeb.win.tue.nl/codes/cwc/d12/a30.12.9.44, checks its sha256 (56d5cb3304998a0322d495e97dbb128b8c3710a8201bcdd080d75c0d72d2f4cd), compiles how-we-built-it/bststate.cpp, runs the search once with the recorded seed (one core, 10 s to about 1.5 minutes) and compares the output with the object byte for byte. Expected last lines:

```
SOLVED iter 19272004 restarts 0 steps 19272004 time <seconds>
search output equals the object (without its first line), byte for byte
PASS
```

## Where it came from

how-we-built-it/COMMANDS.md gives the search command and describes the program; the logs of the original run and of a rerun are in how-we-built-it/logs/.
