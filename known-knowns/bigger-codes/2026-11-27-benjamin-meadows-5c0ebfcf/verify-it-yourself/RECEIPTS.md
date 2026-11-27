# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run from the package folder on 2026-11-27 (Python 3 standard library):

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

Output of `sh how-we-built-it/rebuild.sh` on 2026-11-27 (Linux x86-64, g++ 13.3):

```
seed sha256 71b98dcc2ed90dabffe98c800d42162e852cc0babe8511ae3b60897a16f7e26b
seed words: 96
step 1: size 97, random seed 1011: RESULT FOUND pen 0 steps 27332716 restarts 26 cpu 59.5
step 2: size 98, random seed 1001: RESULT FOUND pen 0 steps 36240211 restarts 34 cpu 79.6
search output equals the object (without its first line), byte for byte
PASS
```
