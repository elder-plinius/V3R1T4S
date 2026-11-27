# Run it yourself

From this folder, in a fresh shell (Python 3, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```
== exact check of the code against the table cell
file sha256 86b13f74de60c58c60f8255a4ced73ad9a126038dc79c543021b55b5159bc658
n = 25, d = 10, w = 12, words read: 142
pairs checked: 10011 (all of them)
distance distribution: 10:3930 12:1972 14:2596 16:1119 18:367 20:26 22:1
minimum distance: 10
table lower bound 141, upper bound 433, size 142: margin over the lower bound 1
PASS
== planted bugs (each must be rejected)
planted bug: pair moved too close (word 1: 1 moved from position 4 to 0) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: changed weight (word 1, position 0, 0 -> 1) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: duplicated word (word 1 written over the last word) -> checker exit 1, last line FAIL (rejected, as required)
PASS
PASS
```

The two steps can also be run one at a time:

```sh
python3 verify-it-yourself/check_cw.py object/A-25-10-12-142words.txt 25 10 12 142 141 433 86b13f74de60c58c60f8255a4ced73ad9a126038dc79c543021b55b5159bc658
python3 verify-it-yourself/planted_bugs.py object/A-25-10-12-142words.txt 25 10 12 142 141 433
```

check_cw.py arguments: code file, n, d, w, claimed size, table lower bound, table upper bound, expected sha256 (optional).

## Rebuild

```sh
sh how-we-built-it/rebuild.sh
```

Needs curl, a C++17 compiler and Python 3. It downloads the seed code https://aeb.win.tue.nl/codes/cwc/d10/a25.10.12.141H, checks its sha256 (71f7603eac9ee759f07696eb2741dcb9b159503eee639f13a28bfd66493a4a97), converts it to 0/1 rows (how-we-built-it/seed_to_rows.py), compiles how-we-built-it/cwbst.cpp, replays the recorded run(s) in how-we-built-it/chain.tsv (one core; 81 CPU seconds in the original), checks each step's iteration count and compares the output with the object byte for byte. Output of one replay:

```
seed sha256 71f7603eac9ee759f07696eb2741dcb9b159503eee639f13a28bfd66493a4a97
seed words: 141
step 1: size 142, random seed 1017: RESULT FOUND pen 0 steps 22733579 restarts 20 cpu 71.6
search output equals the object (without its first line), byte for byte
PASS
```

## Where it came from

how-we-built-it/COMMANDS.md describes the program and the exact commands; how-we-built-it/logs/ holds the record of the original run(s) and the output of a replay.
