# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run from the package folder on 2026-11-27 (Python 3 standard library):

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

Output of `sh how-we-built-it/rebuild.sh` on 2026-11-27 (Linux x86-64, g++ 13.3):

```
seed sha256 662ef208b5b79c7dd842e717caf9fa298cb1f217b9bdcbad433a0cfc363199d4
seed words: 213
step 1: size 214, random seed 1005: RESULT FOUND pen 0 steps 10436323 restarts 10 cpu 47.6
search output equals the object (without its first line), byte for byte
PASS
```
