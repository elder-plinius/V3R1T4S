# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run from the package folder on 2026-11-27 (Python 3 standard library):

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

Output of `sh how-we-built-it/rebuild.sh` on 2026-11-27 (Linux x86-64, g++ 13.3):

```
seed sha256 b342cddfbbf96828dff9f5763b2d63138af014c7d0f94e8a41197dd88cd01868
seed words: 777
step 1: size 778, random seed 1005: RESULT FOUND pen 0 steps 7029649 restarts 7 cpu 78.8
search output equals the object (without its first line), byte for byte
PASS
```
