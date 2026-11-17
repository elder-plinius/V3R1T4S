# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded on the contributor's machine: Linux x86_64, 4 cores (Intel Xeon @ 2.80GHz), 15 GB of memory. Every
run was started from the package folder as `taskset -c 0-2 nice -n 10 sh verify-it-yourself/run_checks.sh`
(pinned to 3 cores, low priority); start and end times from `date -u`, wall time from `date +%s`. After these runs only comment lines of
`run_checks.sh` (the time and memory estimates in its header) were edited; the code that produced the output is
unchanged.

## 1. The package as shipped, default rows (exit 0, 5706 s, 2026-10-23T20:04:17Z to 2026-10-23T21:39:23Z)

```
package check: anomaly-free-atlas-qmax: SMnuR Q_max 17 and 18 (default rows: SMnuR:17 SMnuR:18)
object/counts.txt sha256: 0728c1c828aa06c5ec5cb37cdc30feedfd6fe9d18a012bf8bf60fa7da27c828b
threads per lister: 3, parallel counter jobs: 3, Python checker on lists up to 2000000 lines
step 1 counts file: 2 rows, count = lines + 1 in every row: ok
  422864d72b2d5635fa585d8eb6bb9e9ace6e67be004c344cbbaff26942eca681  verify-it-yourself/checklist.c
  86055d4c7612bdd37db98766f79c88c6397cb72960aa9ec925c87aa41969ca6d  verify-it-yourself/check_list.py
  cfff71674e953ca1de84b443ae1341e07bfc0131d742a83802da6ca8c2c9d774  how-we-built-it/source/count.c
  9a52ff2c7a7952acc0ccffeceac2fa3bd346cd14155672d898bf505160833216  how-we-built-it/source/fix.py
  7d3d74c92db4d2bf90bfed58283e32c053fe82154bdcf41164942b6486cfb1d8  how-we-built-it/source/conventions.py
  4c14e8ea97f17cce68e88c5dbb3b4eb324f804e68b95d457b20ab531eb4feba6  how-we-built-it/source/csenum2.c
step 2 build: ok
step 3 stored lists: 0 checked
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
  (SM counter, Q_max 1..10: 0 s)
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
  recount SMnuR Q_max 17: 1643386480 = object/counts.txt count: ok
  recount SMnuR Q_max 18: 2720672222 = object/counts.txt count: ok
  (SMnuR counter, Q_max 1..18: 1413 s)
  SMnuR Q_max 17 by csenum2: lines 1643386479, sha256 385eb5abe1adb8107c6d678374555095202c3c7fcae17316f8334730d5e61023, C checker PASS (1643386479 valid), Python checker not run (more than 2000000 lines), 1525 s
  SMnuR Q_max 17 by csenum2: matches object/counts.txt
  SMnuR Q_max 18 by csenum2: lines 2720672221, sha256 ba766218c78ca20f29c48f2bb677bca4a31235f398638ba317315b7bf8994d3c, C checker PASS (2720672221 valid), Python checker not run (more than 2000000 lines), 2767 s
  SMnuR Q_max 18 by csenum2: matches object/counts.txt
step 5 regenerated lists: 2 streams, all equal to object/counts.txt
rows checked: 2 of 2 (default)
PASS
```

## 2. Control: one digit of the object changed (exit 1, 0 s)

In a copy of the package, the middle digit of object/counts.txt (line 2, row SMnuR 17) was changed from 4 to 1 in the count recorded for the independent counters (1643386480 to 1643386180), the same corruption repo/kit/check_run.py applies to a copy of the package (the middle ASCII digit of the first text file in object/ is changed).

```
package check: anomaly-free-atlas-qmax: SMnuR Q_max 17 and 18 (default rows: SMnuR:17 SMnuR:18)
object/counts.txt sha256: 7568703fa65f36c2ad790a0b083b6b8e7f68f6c51b83384615c2ca1cac2faa64
threads per lister: 3, parallel counter jobs: 3, Python checker on lists up to 2000000 lines
counts file: SMnuR:17: recorded independent count 1643386180 differs from count 1643386480
problem: object/counts.txt
FAIL
```
