# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
== exact check of the code against the table cell
file sha256 5c0ebfcf58bd20ac9e89c62b10560e485e9a416bf027df1dd4c680feaf3354ee
n = 29, d = 10, w = 8, words read: 98
pairs checked: 4753 (all of them)
distance distribution: 10:2327 12:1315 14:714 16:397
minimum distance: 10
table lower bound 96, upper bound 203, size 98: margin over the lower bound 2
PASS
== planted bugs (each must be rejected)
planted bug: pair moved too close (word 1: 1 moved from position 2 to 0) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: changed weight (word 1, position 0, 0 -> 1) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: duplicated word (word 1 written over the last word) -> checker exit 1, last line FAIL (rejected, as required)
PASS
PASS
```

The two steps can also be run one at a time:

```sh
python3 verify-it-yourself/check_cw.py object/A-29-10-8-98words.txt 29 10 8 98 96 203 5c0ebfcf58bd20ac9e89c62b10560e485e9a416bf027df1dd4c680feaf3354ee
python3 verify-it-yourself/planted_bugs.py object/A-29-10-8-98words.txt 29 10 8 98 96 203
```

check_cw.py arguments: code file, n, d, w, claimed size, table lower bound, table upper bound, expected sha256 (optional).

## Rebuild

```sh
sh how-we-built-it/rebuild.sh
```

Needs curl, a C++17 compiler and Python 3. It downloads the seed code https://aeb.win.tue.nl/codes/cwc/d10/a29.10.8.96, checks its sha256 (71b98dcc2ed90dabffe98c800d42162e852cc0babe8511ae3b60897a16f7e26b), converts it to 0/1 rows (how-we-built-it/seed_to_rows.py), compiles how-we-built-it/cwbst.cpp, replays the recorded run(s) in how-we-built-it/chain.tsv (one core; 150 CPU seconds in the original), checks each step's iteration count and compares the output with the object byte for byte. Output of one replay:

```
seed sha256 71b98dcc2ed90dabffe98c800d42162e852cc0babe8511ae3b60897a16f7e26b
seed words: 96
step 1: size 97, random seed 1011: RESULT FOUND pen 0 steps 27332716 restarts 26 cpu 59.5
step 2: size 98, random seed 1001: RESULT FOUND pen 0 steps 36240211 restarts 34 cpu 79.6
search output equals the object (without its first line), byte for byte
PASS
```

## Where it came from

how-we-built-it/COMMANDS.md describes the program and the exact commands; how-we-built-it/logs/ holds the record of the original run(s) and the output of a replay.
