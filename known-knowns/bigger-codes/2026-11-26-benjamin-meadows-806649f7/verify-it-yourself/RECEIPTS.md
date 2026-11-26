# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run from the package folder on 2026-11-26 (Python 3 standard library):

```
== exact check of the code against the table cell
file sha256 806649f74bcb4ec5746f248ef5f087f88d56120661f95e0d7a464d9965f9060d
n = 30, d = 12, w = 9, words read: 45
pairs checked: 990 (all of them)
distance distribution: 12:756 14:141 16:36 18:57
minimum distance: 12
table lower bound 44, upper bound 74, size 45: margin over the lower bound 1
PASS
== planted bugs (each must be rejected)
planted bug: pair moved too close (word 1: 1 moved from position 0 to 13) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: changed weight (word 1, position 2, 0 -> 1) -> checker exit 1, last line FAIL (rejected, as required)
planted bug: duplicated word (word 1 written over the last word) -> checker exit 1, last line FAIL (rejected, as required)
PASS
PASS
```

Output of `sh how-we-built-it/rebuild.sh` on 2026-11-26 (Apple clang, macOS):

```
seed sha256 56d5cb3304998a0322d495e97dbb128b8c3710a8201bcdd080d75c0d72d2f4cd
SOLVED iter 19272004 restarts 0 steps 19272004 time 10.2625
search output equals the object (without its first line), byte for byte
PASS
```
