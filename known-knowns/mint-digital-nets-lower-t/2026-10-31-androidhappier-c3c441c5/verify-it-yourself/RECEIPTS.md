# Receipts: real output of verify-it-yourself/run_checks.sh

Machine: Linux, 8-core Intel Xeon, Python 3.13.5, gcc as `cc`. Each run was started from a fresh copy of this
package folder, with `sh verify-it-yourself/run_checks.sh`.

## Clean copy (expected last line PASS)

```
2026-10-31T16:28:18Z
== 1. sha256 of object/net_F2_t11_m24_s17.txt
got  c3c441c507605e64d545fb6c6ab57863c7306e8b29dc88bafca22577dfd54618
want c3c441c507605e64d545fb6c6ab57863c7306e8b29dc88bafca22577dfd54618
sha256: match
== 2. object/net_F2_t11_m24_s17_first13rows.txt equals rows 1..13 of each block of object/net_F2_t11_m24_s17.txt
first13rows consistent: True
== 3. Python checker (check_net.py), t=11: every composition of 13 into 17 parts (about 1-2 minutes)
b=2 m=24 s=17 t=11 k=13 compositions_checked=67863915 expected=67863915: all 67863915 compositions of k=13 into s=17 parts have rank 13
PASS
== 4. control: the same object at t=10 must FAIL (shows the checker can reject)
b=2 m=24 s=17 t=10 k=14 compositions_checked=22649 expected=145422675: rank deficient at composition (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 7, 0, 3, 0)
FAIL
control: FAIL at t=10 as expected
== 4b. control: a copy with row 1 of C_17 replaced by row 1 of C_16 must FAIL at t=11
b=2 m=24 s=17 t=11 k=13 compositions_checked=1 expected=67863915: rank deficient at composition (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 12)
FAIL
mutation control: FAIL as expected
== 5. second checker (netcheck_b.c, C, incremental echelon over F_q), t=11
PASS q=2 m=24 s=17 t=11 k=13 compositions_reached=67863915
PASS
exit 0
elapsed 104 s
```

## Corrupted copy (one digit of object/net_F2_t11_m24_s17.txt flipped: the middle digit of the file, which is
## row 12, column 15 of C_9; expected last line FAIL)

```
2026-10-31T16:26:26Z
== 1. sha256 of object/net_F2_t11_m24_s17.txt
got  c016b8df91ad72fbcf0bc1dbe6827734f1fbf6b3aa59e99bad8804625b7907eb
want c3c441c507605e64d545fb6c6ab57863c7306e8b29dc88bafca22577dfd54618
sha256: MISMATCH
== 2. object/net_F2_t11_m24_s17_first13rows.txt equals rows 1..13 of each block of object/net_F2_t11_m24_s17.txt
first13rows consistent: False
== 3. Python checker (check_net.py), t=11: every composition of 13 into 17 parts (about 1-2 minutes)
b=2 m=24 s=17 t=11 k=13 compositions_checked=67863915 expected=67863915: all 67863915 compositions of k=13 into s=17 parts have rank 13
PASS
== 4. control: the same object at t=10 must FAIL (shows the checker can reject)
b=2 m=24 s=17 t=10 k=14 compositions_checked=22649 expected=145422675: rank deficient at composition (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 7, 0, 3, 0)
FAIL
control: FAIL at t=10 as expected
== 4b. control: a copy with row 1 of C_17 replaced by row 1 of C_16 must FAIL at t=11
b=2 m=24 s=17 t=11 k=13 compositions_checked=1 expected=67863915: rank deficient at composition (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 12)
FAIL
mutation control: FAIL as expected
== 5. second checker (netcheck_b.c, C, incremental echelon over F_q), t=11
PASS q=2 m=24 s=17 t=11 k=13 compositions_reached=67863915
FAIL
exit 1
```

Note on the corrupted copy: this particular one-bit change still leaves a valid digital (11,24,17)-net. Both rank
checkers pass it, because many nearby nets also work. The package rejects it because it is not the claimed object:
the sha256 differs and the first13rows file no longer matches. That the checkers can reject a non-net is shown by
the two controls (t = 10 on the real object, and the duplicated-row copy). Both FAIL in every run above.
