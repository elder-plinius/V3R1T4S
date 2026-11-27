# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run from the package folder on 2026-11-27 (Python 3 standard library):

```
== exact check of the code against the table cell
file sha256 4b977585972408991e43784ce2f81591c529d9f3a9d770ee9fc4262eb056e3ba
n = 27, d = 8, w = 12, words read: 3387
pairs checked: 5734191 (all of them)
distance distribution: 8:654035 10:288850 12:2442986 14:949326 16:1118579 18:228926 20:49452 22:749 24:1288
minimum distance: 8
table lower bound 3374, upper bound 10460, size 3387: margin over the lower bound 13
PASS
== planted bugs (each must be rejected)
planted bug: pair moved too close (word 1: 1 moved from position 9 to 10) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: changed weight (word 1, position 0, 0 -> 1) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: duplicated word (word 1 written over the last word) -> checker exit 1, last line FAIL (rejected, as required)
PASS
PASS
```

Output of `sh how-we-built-it/rebuild.sh` on 2026-11-27 (Linux x86-64, g++ 13.3):

```
seed sha256 91aff7ff2e09ed7449bd464412f5ceba1e37e02d5d2f08fc46ee89d835baf7a6
seed words: 3374
step 1: size 3375, random seed 1002: RESULT FOUND pen 0 steps 102469 restarts 0 cpu 8.5
step 2: size 3376, random seed 1001: RESULT FOUND pen 0 steps 30924 restarts 0 cpu 5.9
step 3: size 3377, random seed 1003: RESULT FOUND pen 0 steps 32966 restarts 0 cpu 6.2
step 4: size 3378, random seed 1001: RESULT FOUND pen 0 steps 40104 restarts 0 cpu 6.5
step 5: size 3379, random seed 1001: RESULT FOUND pen 0 steps 32818 restarts 0 cpu 6.2
step 6: size 3380, random seed 1001: RESULT FOUND pen 0 steps 58467 restarts 0 cpu 7.2
step 7: size 3381, random seed 1001: RESULT FOUND pen 0 steps 56931 restarts 0 cpu 6.5
step 8: size 3382, random seed 1001: RESULT FOUND pen 0 steps 27316 restarts 0 cpu 5.9
step 9: size 3383, random seed 1002: RESULT FOUND pen 0 steps 37095 restarts 0 cpu 6.2
step 10: size 3384, random seed 1001: RESULT FOUND pen 0 steps 1789499 restarts 1 cpu 88.9
step 11: size 3385, random seed 1009: RESULT FOUND pen 0 steps 33756 restarts 0 cpu 6.2
step 12: size 3386, random seed 1001: RESULT FOUND pen 0 steps 630983 restarts 0 cpu 34.1
step 13: size 3387, random seed 1001: RESULT FOUND pen 0 steps 2157585 restarts 2 cpu 106.3
search output equals the object (without its first line), byte for byte
PASS
```
