# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
== exact check of the code against the table cell
file sha256 68eabec3d2808175e4f0f8db629c0b6137d8ab94b19e8e24e23186b03f6bc26f
n = 27, d = 8, w = 8, words read: 778
pairs checked: 302253 (all of them)
distance distribution: 8:90546 10:19328 12:161656 14:18110 16:12613
minimum distance: 8
table lower bound 777, upper bound 1252, size 778: margin over the lower bound 1
PASS
== planted bugs (each must be rejected)
planted bug: pair moved too close (word 1: 1 moved from position 14 to 13) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: changed weight (word 1, position 0, 0 -> 1) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: duplicated word (word 1 written over the last word) -> checker exit 1, last line FAIL (rejected, as required)
PASS
PASS
```

The two steps can also be run one at a time:

```sh
python3 verify-it-yourself/check_cw.py object/A-27-8-8-778words.txt 27 8 8 778 777 1252 68eabec3d2808175e4f0f8db629c0b6137d8ab94b19e8e24e23186b03f6bc26f
python3 verify-it-yourself/planted_bugs.py object/A-27-8-8-778words.txt 27 8 8 778 777 1252
```

check_cw.py arguments: code file, n, d, w, claimed size, table lower bound, table upper bound, expected sha256 (optional).

## Rebuild

```sh
sh how-we-built-it/rebuild.sh
```

Needs curl, a C++17 compiler and Python 3. It downloads the seed code https://aeb.win.tue.nl/codes/cwc/d8/a27.8.8.777H, checks its sha256 (b342cddfbbf96828dff9f5763b2d63138af014c7d0f94e8a41197dd88cd01868), converts it to 0/1 rows (how-we-built-it/seed_to_rows.py), compiles how-we-built-it/cwbst.cpp, replays the recorded run(s) in how-we-built-it/chain.tsv (one core; 55 CPU seconds in the original), checks each step's iteration count and compares the output with the object byte for byte. Output of one replay:

```
seed sha256 b342cddfbbf96828dff9f5763b2d63138af014c7d0f94e8a41197dd88cd01868
seed words: 777
step 1: size 778, random seed 1005: RESULT FOUND pen 0 steps 7029649 restarts 7 cpu 78.8
search output equals the object (without its first line), byte for byte
PASS
```

## Where it came from

how-we-built-it/COMMANDS.md describes the program and the exact commands; how-we-built-it/logs/ holds the record of the original run(s) and the output of a replay.
