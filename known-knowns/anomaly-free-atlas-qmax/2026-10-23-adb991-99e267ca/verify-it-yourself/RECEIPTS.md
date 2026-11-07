# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded on the contributor's machine: Linux x86_64, 4 cores (Intel Xeon @ 2.80GHz), 15 GB of memory. Every
run was started from the package folder as `taskset -c 0-2 nice -n 10 sh verify-it-yourself/run_checks.sh`
(pinned to 3 cores, low priority); start and end times from `date -u`, wall time from `date +%s`.

## 1. The package as shipped, default rows (exit 0, 83 s, 2026-10-23T21:39:33Z to 2026-10-23T21:40:56Z)

```
package check: anomaly-free-atlas-qmax: SM and SMnuR at Q_max 11 (default rows: SM:11 SMnuR:11)
object/counts.txt sha256: 99e267ca14fc30433b2679902e6e9da10e7ecd9bc9a0fbc8b9b06d15b372bc5f
threads per lister: 3, parallel counter jobs: 3, Python checker on lists up to 2000000 lines
step 1 counts file: 2 rows, count = lines + 1 in every row: ok
  422864d72b2d5635fa585d8eb6bb9e9ace6e67be004c344cbbaff26942eca681  verify-it-yourself/checklist.c
  86055d4c7612bdd37db98766f79c88c6397cb72960aa9ec925c87aa41969ca6d  verify-it-yourself/check_list.py
  cfff71674e953ca1de84b443ae1341e07bfc0131d742a83802da6ca8c2c9d774  how-we-built-it/source/count.c
  9a52ff2c7a7952acc0ccffeceac2fa3bd346cd14155672d898bf505160833216  how-we-built-it/source/fix.py
  7d3d74c92db4d2bf90bfed58283e32c053fe82154bdcf41164942b6486cfb1d8  how-we-built-it/source/conventions.py
  de18d2f44c2d895880b45f13a99753c92d050c09287efce2a4b5545768d362c8  how-we-built-it/source/acclist.c
step 2 build: ok
  stored list object/SM_q11.txt.gz (SM Q_max 11): lines 37005, sha256 723e21fb6c46023dcfe04c77eee556a2759066277d57c7ab092c430b80667d68, C checker PASS (37005 valid), Python checker PASS (37005 valid), 1 s
  stored list object/SM_q11.txt.gz (SM Q_max 11): matches object/counts.txt
step 3 stored lists: 1 checked
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
  recount SM Q_max 11: 37006 = object/counts.txt count: ok
  (SM counter, Q_max 1..11: 1 s)
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
  recount SMnuR Q_max 11: 45378378 = object/counts.txt count: ok
  (SMnuR counter, Q_max 1..11: 26 s)
  SM Q_max 11 by acclist: lines 37005, sha256 723e21fb6c46023dcfe04c77eee556a2759066277d57c7ab092c430b80667d68, C checker PASS (37005 valid), Python checker PASS (37005 valid), 1 s
  SM Q_max 11 by acclist: matches object/counts.txt
  SMnuR Q_max 11 by acclist: lines 45378377, sha256 f4e16ec8613a78ef6437fde6c43e56320fbb6bc901fa072c0889667d96dbdaf4, C checker PASS (45378377 valid), Python checker not run (more than 2000000 lines), 54 s
  SMnuR Q_max 11 by acclist: matches object/counts.txt
step 5 regenerated lists: 2 streams, all equal to object/counts.txt
rows checked: 2 of 2 (default)
PASS
```

## 2. Control: one digit of the object changed (exit 1, 0 s)

In a copy of the package, the middle digit of object/counts.txt (line 2) was changed from 1 to 0, the same corruption repo/kit/check_run.py applies to a copy of the package (the middle ASCII digit of the first text file in object/ is changed). Here it renames the stored list in the SM row from object/SM_q11.txt.gz to object/SM_q10.txt.gz.

```
package check: anomaly-free-atlas-qmax: SM and SMnuR at Q_max 11 (default rows: SM:11 SMnuR:11)
object/counts.txt sha256: a24abbe758c8e3daee4df41d4e4477c32d8ed666fea6f7397ce30b07f24c48c6
threads per lister: 3, parallel counter jobs: 3, Python checker on lists up to 2000000 lines
counts file: SM:11: the list file object/SM_q10.txt.gz named in the row is not in the package
problem: object/counts.txt
FAIL
```

## 3. Control: one digit of a list hash changed (exit 1, 84 s)

In another copy, one hex digit of the SMnuR list's sha256 in object/counts.txt (line 3) was changed from 8 to 9 (f4e16ec8... to f4e16ec9...). The check regenerates the list and rejects the hash.

```
package check: anomaly-free-atlas-qmax: SM and SMnuR at Q_max 11 (default rows: SM:11 SMnuR:11)
object/counts.txt sha256: aa24c90075fbb462dc0b82d69f72c76bcd4e01e99490f59cb91764e69d6be7c7
threads per lister: 3, parallel counter jobs: 3, Python checker on lists up to 2000000 lines
step 1 counts file: 2 rows, count = lines + 1 in every row: ok
  422864d72b2d5635fa585d8eb6bb9e9ace6e67be004c344cbbaff26942eca681  verify-it-yourself/checklist.c
  86055d4c7612bdd37db98766f79c88c6397cb72960aa9ec925c87aa41969ca6d  verify-it-yourself/check_list.py
  cfff71674e953ca1de84b443ae1341e07bfc0131d742a83802da6ca8c2c9d774  how-we-built-it/source/count.c
  9a52ff2c7a7952acc0ccffeceac2fa3bd346cd14155672d898bf505160833216  how-we-built-it/source/fix.py
  7d3d74c92db4d2bf90bfed58283e32c053fe82154bdcf41164942b6486cfb1d8  how-we-built-it/source/conventions.py
  de18d2f44c2d895880b45f13a99753c92d050c09287efce2a4b5545768d362c8  how-we-built-it/source/acclist.c
step 2 build: ok
  stored list object/SM_q11.txt.gz (SM Q_max 11): lines 37005, sha256 723e21fb6c46023dcfe04c77eee556a2759066277d57c7ab092c430b80667d68, C checker PASS (37005 valid), Python checker PASS (37005 valid), 1 s
  stored list object/SM_q11.txt.gz (SM Q_max 11): matches object/counts.txt
step 3 stored lists: 1 checked
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
  recount SM Q_max 11: 37006 = object/counts.txt count: ok
  (SM counter, Q_max 1..11: 0 s)
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
  recount SMnuR Q_max 11: 45378378 = object/counts.txt count: ok
  (SMnuR counter, Q_max 1..11: 27 s)
  SM Q_max 11 by acclist: lines 37005, sha256 723e21fb6c46023dcfe04c77eee556a2759066277d57c7ab092c430b80667d68, C checker PASS (37005 valid), Python checker PASS (37005 valid), 0 s
  SM Q_max 11 by acclist: matches object/counts.txt
  SMnuR Q_max 11 by acclist: lines 45378377, sha256 f4e16ec8613a78ef6437fde6c43e56320fbb6bc901fa072c0889667d96dbdaf4, C checker PASS (45378377 valid), Python checker not run (more than 2000000 lines), 55 s
  SMnuR Q_max 11 by acclist: MISMATCH; sha256 f4e16ec8613a78ef6437fde6c43e56320fbb6bc901fa072c0889667d96dbdaf4, expected f4e16ec9613a78ef6437fde6c43e56320fbb6bc901fa072c0889667d96dbdaf4
problem: SMnuR Q_max 11 (acclist)
FAIL
```
