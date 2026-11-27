# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
== exact check of the code against the table cell
file sha256 c78abc24b831d29945e88f58953941927761132fa60f8a2cd2696a5dcec81715
n = 26, d = 10, w = 12, words read: 214
pairs checked: 22791 (all of them)
distance distribution: 10:5210 12:8756 14:2712 16:4676 18:1425 20:12
minimum distance: 10
table lower bound 213, upper bound 691, size 214: margin over the lower bound 1
PASS
== planted bugs (each must be rejected)
planted bug: pair moved too close (word 1: 1 moved from position 19 to 7) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: changed weight (word 1, position 0, 0 -> 1) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: duplicated word (word 1 written over the last word) -> checker exit 1, last line FAIL (rejected, as required)
PASS
PASS
```

The two steps can also be run one at a time:

```sh
python3 verify-it-yourself/check_cw.py object/A-26-10-12-214words.txt 26 10 12 214 213 691 c78abc24b831d29945e88f58953941927761132fa60f8a2cd2696a5dcec81715
python3 verify-it-yourself/planted_bugs.py object/A-26-10-12-214words.txt 26 10 12 214 213 691
```

check_cw.py arguments: code file, n, d, w, claimed size, table lower bound, table upper bound, expected sha256 (optional).

## Rebuild

```sh
sh how-we-built-it/rebuild.sh
```

Needs curl, a C++17 compiler and Python 3. It downloads the seed code https://aeb.win.tue.nl/codes/cwc/d10/a26.10.12.213H, checks its sha256 (662ef208b5b79c7dd842e717caf9fa298cb1f217b9bdcbad433a0cfc363199d4), converts it to 0/1 rows (how-we-built-it/seed_to_rows.py), compiles how-we-built-it/cwbst.cpp, replays the recorded run(s) in how-we-built-it/chain.tsv (one core; 88 CPU seconds in the original), checks each step's iteration count and compares the output with the object byte for byte. Output of one replay:

```
seed sha256 662ef208b5b79c7dd842e717caf9fa298cb1f217b9bdcbad433a0cfc363199d4
seed words: 213
step 1: size 214, random seed 1005: RESULT FOUND pen 0 steps 10436323 restarts 10 cpu 47.6
search output equals the object (without its first line), byte for byte
PASS
```

## Where it came from

how-we-built-it/COMMANDS.md describes the program and the exact commands; how-we-built-it/logs/ holds the record of the original run(s) and the output of a replay.
