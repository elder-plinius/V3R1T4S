# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run from the package folder on 2026-11-27 (Python 3 standard library):

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

Output of `sh how-we-built-it/rebuild.sh` on 2026-11-27 (Linux x86-64, g++ 13.3):

```
seed sha256 71f7603eac9ee759f07696eb2741dcb9b159503eee639f13a28bfd66493a4a97
seed words: 141
step 1: size 142, random seed 1017: RESULT FOUND pen 0 steps 22733579 restarts 20 cpu 71.6
search output equals the object (without its first line), byte for byte
PASS
```
