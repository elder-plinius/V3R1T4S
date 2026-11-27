# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
== exact check of the code against the table cell
file sha256 1c25d94ca5861e9762b92ce4dc28d493bf2c2d5827466cb73cdf949c73079642
n = 29, d = 6, w = 6, words read: 1207
pairs checked: 727821 (all of them)
distance distribution: 6:74765 8:189907 10:316695 12:146454
minimum distance: 6
table lower bound 1205, upper bound 1459, size 1207: margin over the lower bound 2
PASS
== planted bugs (each must be rejected)
planted bug: pair moved too close (word 1: 1 moved from position 4 to 2) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: changed weight (word 1, position 1, 0 -> 1) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: duplicated word (word 1 written over the last word) -> checker exit 1, last line FAIL (rejected, as required)
PASS
PASS
```

The two steps can also be run one at a time:

```sh
python3 verify-it-yourself/check_cw.py object/A-29-6-6-1207words.txt 29 6 6 1207 1205 1459 1c25d94ca5861e9762b92ce4dc28d493bf2c2d5827466cb73cdf949c73079642
python3 verify-it-yourself/planted_bugs.py object/A-29-6-6-1207words.txt 29 6 6 1207 1205 1459
```

check_cw.py arguments: code file, n, d, w, claimed size, table lower bound, table upper bound, expected sha256 (optional).

## Rebuild

```sh
sh how-we-built-it/rebuild.sh
```

Needs curl, a C++17 compiler and Python 3. It downloads the seed code https://aeb.win.tue.nl/codes/cwc/d6/a29.6.6.1205H, checks its sha256 (898cb1edd43ef9ebacc3abc6bca16eeb95e04ecdef4ac3c72f7a301d5d589c8f), converts it to 0/1 rows (how-we-built-it/seed_to_rows.py), compiles how-we-built-it/cwbst.cpp, replays the recorded run(s) in how-we-built-it/chain.tsv (one core; 194 CPU seconds in the original), checks each step's iteration count and compares the output with the object byte for byte. Output of one replay:

```
seed sha256 898cb1edd43ef9ebacc3abc6bca16eeb95e04ecdef4ac3c72f7a301d5d589c8f
seed words: 1205
step 1: size 1206, random seed 1001: RESULT FOUND pen 0 steps 3035422 restarts 3 cpu 46.4
step 2: size 1207, random seed 1011: RESULT FOUND pen 0 steps 5010566 restarts 5 cpu 80.2
search output equals the object (without its first line), byte for byte
PASS
```

## Where it came from

how-we-built-it/COMMANDS.md describes the program and the exact commands; how-we-built-it/logs/ holds the record of the original run(s) and the output of a replay.
