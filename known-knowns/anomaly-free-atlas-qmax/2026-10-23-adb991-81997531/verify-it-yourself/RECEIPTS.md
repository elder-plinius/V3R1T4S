# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded on the contributor's machine: Linux x86_64, 4 cores (Intel Xeon @ 2.80GHz), 15 GB of memory. Every
run was started from the package folder as `taskset -c 0-2 nice -n 10 sh verify-it-yourself/run_checks.sh`
(pinned to 3 cores, low priority); start and end times from `date -u`, wall time from `date +%s`. After these runs only comment lines of
`run_checks.sh` (the time and memory estimates in its header) were edited; the code that produced the output is
unchanged.

## 1. The package as shipped, default rows (exit 0, 442 s, 2026-10-23T19:56:49Z to 2026-10-23T20:04:11Z)

```
package check: anomaly-free-atlas-qmax: SMnuR Q_max 12..16 and SM Q_max 12..31 (default rows: SMnuR:12 SMnuR:13 SM:12 SM:13 SM:14 SM:15 SM:16 SM:17 SM:18 SM:19 SM:20)
object/counts.txt sha256: 819975316ae3c873b9f4abbbc466062a526f7145ad0297d1d82a7a7dc02683cb
threads per lister: 3, parallel counter jobs: 3, Python checker on lists up to 2000000 lines
step 1 counts file: 25 rows, count = lines + 1 in every row: ok
  422864d72b2d5635fa585d8eb6bb9e9ace6e67be004c344cbbaff26942eca681  verify-it-yourself/checklist.c
  86055d4c7612bdd37db98766f79c88c6397cb72960aa9ec925c87aa41969ca6d  verify-it-yourself/check_list.py
  cfff71674e953ca1de84b443ae1341e07bfc0131d742a83802da6ca8c2c9d774  how-we-built-it/source/count.c
  9a52ff2c7a7952acc0ccffeceac2fa3bd346cd14155672d898bf505160833216  how-we-built-it/source/fix.py
  7d3d74c92db4d2bf90bfed58283e32c053fe82154bdcf41164942b6486cfb1d8  how-we-built-it/source/conventions.py
  de18d2f44c2d895880b45f13a99753c92d050c09287efce2a4b5545768d362c8  how-we-built-it/source/acclist.c
  19860b71d51249e84da6a378846a11b30333eca3d5f93a1413e9d9f8c659bdfc  how-we-built-it/source/csenum.c
step 2 build: ok
step 3 stored lists: 0 checked
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
  recount SM Q_max 12: 67968 = object/counts.txt count: ok
  recount SM Q_max 13: 100388 = object/counts.txt count: ok
  recount SM Q_max 14: 144102 = object/counts.txt count: ok
  recount SM Q_max 15: 223605 = object/counts.txt count: ok
  recount SM Q_max 16: 310691 = object/counts.txt count: ok
  recount SM Q_max 17: 418636 = object/counts.txt count: ok
  recount SM Q_max 18: 628488 = object/counts.txt count: ok
  recount SM Q_max 19: 824232 = object/counts.txt count: ok
  recount SM Q_max 20: 1071441 = object/counts.txt count: ok
  (SM counter, Q_max 1..20: 32 s)
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
  recount SMnuR Q_max 12: 95067546 = object/counts.txt count: ok
  recount SMnuR Q_max 13: 180207252 = object/counts.txt count: ok
  (SMnuR counter, Q_max 1..13: 101 s)
  SMnuR Q_max 12 by csenum: lines 95067545, sha256 c92c6342e2f70126cb61a620f36e589f9b430e3002e1a180af77a088fcd7df84, C checker PASS (95067545 valid), Python checker not run (more than 2000000 lines), 77 s
  SMnuR Q_max 12 by csenum: matches object/counts.txt
  SMnuR Q_max 13 by csenum: lines 180207251, sha256 73dcad862a93788c9665f4b89365ede1d121fb3d5dbf46373c3898acad3a5763, C checker PASS (180207251 valid), Python checker not run (more than 2000000 lines), 147 s
  SMnuR Q_max 13 by csenum: matches object/counts.txt
  SM Q_max 12 by acclist: lines 67967, sha256 23d1469a30ccf713b5129f14e47eb62e19512ee89bd06c2f7422bb35ae5c612f, C checker PASS (67967 valid), Python checker PASS (67967 valid), 1 s
  SM Q_max 12 by acclist: matches object/counts.txt
  SM Q_max 13 by acclist: lines 100387, sha256 262ca74409938625365a4c2da50b95a941bce1c1e3aaf43fae2006afbe92ab9e, C checker PASS (100387 valid), Python checker PASS (100387 valid), 2 s
  SM Q_max 13 by acclist: matches object/counts.txt
  SM Q_max 14 by acclist: lines 144101, sha256 8ce628b32bd21123799290615d6942c68395587b59ac2a3d6648a335bc230f3f, C checker PASS (144101 valid), Python checker PASS (144101 valid), 3 s
  SM Q_max 14 by acclist: matches object/counts.txt
  SM Q_max 15 by acclist: lines 223604, sha256 c51e3b8715f092275326c8ddfaabc806d63616bf71797c92c2a940e7764d4114, C checker PASS (223604 valid), Python checker PASS (223604 valid), 5 s
  SM Q_max 15 by acclist: matches object/counts.txt
  SM Q_max 16 by acclist: lines 310690, sha256 a9c31c0b3c035429776c5e5556fca88c4bbd8e55800734ab16b6c3ab4ad9f61b, C checker PASS (310690 valid), Python checker PASS (310690 valid), 6 s
  SM Q_max 16 by acclist: matches object/counts.txt
  SM Q_max 17 by acclist: lines 418635, sha256 cba838bfc0797d0c33915e45d9ec51f24c1a24b6e9c25d80cd627a7bc46928f8, C checker PASS (418635 valid), Python checker PASS (418635 valid), 9 s
  SM Q_max 17 by acclist: matches object/counts.txt
  SM Q_max 18 by acclist: lines 628487, sha256 7018dde47623603fdb8b9600bdbf0d854cf6002325314864825bc027cc3b62cb, C checker PASS (628487 valid), Python checker PASS (628487 valid), 14 s
  SM Q_max 18 by acclist: matches object/counts.txt
  SM Q_max 19 by acclist: lines 824231, sha256 e4b32bc0dd2c2d6c7bdc0948371c35e2721f273b6d31154243825c64a1e35734, C checker PASS (824231 valid), Python checker PASS (824231 valid), 19 s
  SM Q_max 19 by acclist: matches object/counts.txt
  SM Q_max 20 by acclist: lines 1071440, sha256 f8e2ce35236a5792c3795608aaafcd3f2d4a68f7dfd3bdb0c65bc6efad23e770, C checker PASS (1071440 valid), Python checker PASS (1071440 valid), 24 s
  SM Q_max 20 by acclist: matches object/counts.txt
step 5 regenerated lists: 11 streams, all equal to object/counts.txt
rows checked: 11 of 25 (default)
PASS
```

## 2. Control: one digit of the object changed (exit 1, 404 s)

In a copy of the package, the middle digit of object/counts.txt (line 16, row SM 19) was changed from 6 to 1 inside the row's sha256, the same corruption repo/kit/check_run.py applies to a copy of the package (the middle ASCII digit of the first text file in object/ is changed).

```
package check: anomaly-free-atlas-qmax: SMnuR Q_max 12..16 and SM Q_max 12..31 (default rows: SMnuR:12 SMnuR:13 SM:12 SM:13 SM:14 SM:15 SM:16 SM:17 SM:18 SM:19 SM:20)
object/counts.txt sha256: fe5d4cc62f277362925df88f2d60c71d412ee25075b10f3e9838b234ddc6a312
threads per lister: 3, parallel counter jobs: 3, Python checker on lists up to 2000000 lines
step 1 counts file: 25 rows, count = lines + 1 in every row: ok
  422864d72b2d5635fa585d8eb6bb9e9ace6e67be004c344cbbaff26942eca681  verify-it-yourself/checklist.c
  86055d4c7612bdd37db98766f79c88c6397cb72960aa9ec925c87aa41969ca6d  verify-it-yourself/check_list.py
  cfff71674e953ca1de84b443ae1341e07bfc0131d742a83802da6ca8c2c9d774  how-we-built-it/source/count.c
  9a52ff2c7a7952acc0ccffeceac2fa3bd346cd14155672d898bf505160833216  how-we-built-it/source/fix.py
  7d3d74c92db4d2bf90bfed58283e32c053fe82154bdcf41164942b6486cfb1d8  how-we-built-it/source/conventions.py
  de18d2f44c2d895880b45f13a99753c92d050c09287efce2a4b5545768d362c8  how-we-built-it/source/acclist.c
  19860b71d51249e84da6a378846a11b30333eca3d5f93a1413e9d9f8c659bdfc  how-we-built-it/source/csenum.c
step 2 build: ok
step 3 stored lists: 0 checked
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
  recount SM Q_max 12: 67968 = object/counts.txt count: ok
  recount SM Q_max 13: 100388 = object/counts.txt count: ok
  recount SM Q_max 14: 144102 = object/counts.txt count: ok
  recount SM Q_max 15: 223605 = object/counts.txt count: ok
  recount SM Q_max 16: 310691 = object/counts.txt count: ok
  recount SM Q_max 17: 418636 = object/counts.txt count: ok
  recount SM Q_max 18: 628488 = object/counts.txt count: ok
  recount SM Q_max 19: 824232 = object/counts.txt count: ok
  recount SM Q_max 20: 1071441 = object/counts.txt count: ok
  (SM counter, Q_max 1..20: 30 s)
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
  recount SMnuR Q_max 12: 95067546 = object/counts.txt count: ok
  recount SMnuR Q_max 13: 180207252 = object/counts.txt count: ok
  (SMnuR counter, Q_max 1..13: 100 s)
  SMnuR Q_max 12 by csenum: lines 95067545, sha256 c92c6342e2f70126cb61a620f36e589f9b430e3002e1a180af77a088fcd7df84, C checker PASS (95067545 valid), Python checker not run (more than 2000000 lines), 76 s
  SMnuR Q_max 12 by csenum: matches object/counts.txt
  SMnuR Q_max 13 by csenum: lines 180207251, sha256 73dcad862a93788c9665f4b89365ede1d121fb3d5dbf46373c3898acad3a5763, C checker PASS (180207251 valid), Python checker not run (more than 2000000 lines), 139 s
  SMnuR Q_max 13 by csenum: matches object/counts.txt
  SM Q_max 12 by acclist: lines 67967, sha256 23d1469a30ccf713b5129f14e47eb62e19512ee89bd06c2f7422bb35ae5c612f, C checker PASS (67967 valid), Python checker PASS (67967 valid), 2 s
  SM Q_max 12 by acclist: matches object/counts.txt
  SM Q_max 13 by acclist: lines 100387, sha256 262ca74409938625365a4c2da50b95a941bce1c1e3aaf43fae2006afbe92ab9e, C checker PASS (100387 valid), Python checker PASS (100387 valid), 2 s
  SM Q_max 13 by acclist: matches object/counts.txt
  SM Q_max 14 by acclist: lines 144101, sha256 8ce628b32bd21123799290615d6942c68395587b59ac2a3d6648a335bc230f3f, C checker PASS (144101 valid), Python checker PASS (144101 valid), 3 s
  SM Q_max 14 by acclist: matches object/counts.txt
  SM Q_max 15 by acclist: lines 223604, sha256 c51e3b8715f092275326c8ddfaabc806d63616bf71797c92c2a940e7764d4114, C checker PASS (223604 valid), Python checker PASS (223604 valid), 4 s
  SM Q_max 15 by acclist: matches object/counts.txt
  SM Q_max 16 by acclist: lines 310690, sha256 a9c31c0b3c035429776c5e5556fca88c4bbd8e55800734ab16b6c3ab4ad9f61b, C checker PASS (310690 valid), Python checker PASS (310690 valid), 7 s
  SM Q_max 16 by acclist: matches object/counts.txt
  SM Q_max 17 by acclist: lines 418635, sha256 cba838bfc0797d0c33915e45d9ec51f24c1a24b6e9c25d80cd627a7bc46928f8, C checker PASS (418635 valid), Python checker PASS (418635 valid), 9 s
  SM Q_max 17 by acclist: matches object/counts.txt
  SM Q_max 18 by acclist: lines 628487, sha256 7018dde47623603fdb8b9600bdbf0d854cf6002325314864825bc027cc3b62cb, C checker PASS (628487 valid), Python checker PASS (628487 valid), 13 s
  SM Q_max 18 by acclist: matches object/counts.txt
  SM Q_max 19 by acclist: lines 824231, sha256 e4b32bc0dd2c2d6c7bdc0948371c35e2721f273b6d31154243825c64a1e35734, C checker PASS (824231 valid), Python checker PASS (824231 valid), 18 s
  SM Q_max 19 by acclist: MISMATCH; sha256 e4b32bc0dd2c2d6c7bdc0948371c35e2721f273b6d31154243825c64a1e35734, expected e4b32bc0dd2c2d1c7bdc0948371c35e2721f273b6d31154243825c64a1e35734
problem: SM Q_max 19 (acclist)
FAIL
```
