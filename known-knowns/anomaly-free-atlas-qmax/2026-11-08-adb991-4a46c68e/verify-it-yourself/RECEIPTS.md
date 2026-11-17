# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded on the contributor's machine: Linux x86_64, 4 cores (Intel Xeon @ 2.10GHz), 15 GB of memory (a session
memory cap of about 7.4 GB), gcc 13.3.0, Python 3 (standard library). Every run was started from a copy of the
package's object/, verify-it-yourself/ and how-we-built-it/ folders (the folders the script reads) as
`sh verify-it-yourself/run_checks.sh` (sections 1 and 3 under `nice -n 10`), with the default settings. Start and end
times from `date -u`. Sections 1 and 3 ran at the same time on the 4 cores.

## 1. Default mode, the package as shipped (exit 0, 949 s, 2026-11-08T10:03:11Z to 2026-11-08T10:19:00Z)

```
package check: anomaly-free-atlas-qmax: SM Q_max 39 and 40 (default rows: SM:39)
object/counts.txt sha256: 4a46c68e4e655eaf511a4367b399341dbd162251e8b95c94a2af3df67bada066
threads per csenum2 lister: 3, parallel counter jobs: 3, parallel acclist streams: 2, Python checker on lists up to 2000000 lines
step 1 counts file: 2 rows, count = lines + 1 in every row: ok
  422864d72b2d5635fa585d8eb6bb9e9ace6e67be004c344cbbaff26942eca681  verify-it-yourself/checklist.c
  86055d4c7612bdd37db98766f79c88c6397cb72960aa9ec925c87aa41969ca6d  verify-it-yourself/check_list.py
  ec310d4b84cabddcfb66d3aa686efae4a79776fb1abfa4d7cd51f06714cbdac9  how-we-built-it/source/mitm.c
  de18d2f44c2d895880b45f13a99753c92d050c09287efce2a4b5545768d362c8  how-we-built-it/source/acclist.c
step 2 build: ok
step 3 stored lists: 0 checked
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
  recount SM Q_max 39: 51237625 = object/counts.txt count: ok
  (mitm counter, 20 calibration values and 1 rows: 53 s)
  SM Q_max 39 by acclist: lines 51237624, sha256 0ec7c2c03acf589cbce61249d265f7352db69f43ebaaeee3d1bcc74c6f348743, C checker PASS (51237624 valid), Python checker not run (more than 2000000 lines), 895 s
  SM Q_max 39 by acclist: matches object/counts.txt
step 5 regenerated lists: 1 streams, all equal to object/counts.txt
rows checked: 1 of 2 (default)
PASS
```

## 2. Control: one digit of the object changed (exit 1, 0 s, 2026-11-08T10:03:22Z)

In a copy of the package, the middle ASCII digit of the first text file in object/ was changed, the same corruption
repo/kit/check_run.py applies to a copy of the package (from the script that applied it):

```
object/counts.txt line 2: digit 5 -> 1; sha256 10060fac930c307fce4451e33ed0f880af18616f13212626c5c1b2036ebc624a
context before: SM 40 58626334 58626333 8d83e4182d630423ce5fa25512de702d30cb1889af96bdeaea001ebf7e673694 acclist checklist:PASS mitm.c:58626334
context after:  SM 40 18626334 58626333 8d83e4182d630423ce5fa25512de702d30cb1889af96bdeaea001ebf7e673694 acclist checklist:PASS mitm.c:58626334
```

```
package check: anomaly-free-atlas-qmax: SM Q_max 39 and 40 (default rows: SM:39)
object/counts.txt sha256: 10060fac930c307fce4451e33ed0f880af18616f13212626c5c1b2036ebc624a
threads per csenum2 lister: 3, parallel counter jobs: 3, parallel acclist streams: 2, Python checker on lists up to 2000000 lines
counts file: SM Q_max 40: count 18626334 is not lines 58626333 + 1
problem: object/counts.txt
FAIL
```

## 3. Control: a count changed consistently in all three fields (exit 1, 54 s, 2026-11-08T10:03:11Z to 2026-11-08T10:04:05Z)

In another copy, the SM 39 row of object/counts.txt was changed so that the count, the line count and the recorded
mitm.c value stay consistent with each other. Step 1 cannot see this; the recount without a list catches it.

```
object/counts.txt row SM 39: count 51237625 -> 51237626, lines 51237624 -> 51237625, mitm.c field 51237625 -> 51237626 (consistent, so rows.py passes)
before: SM 39 51237625 51237624 0ec7c2c03acf589cbce61249d265f7352db69f43ebaaeee3d1bcc74c6f348743 acclist checklist:PASS mitm.c:51237625
after:  SM 39 51237626 51237625 0ec7c2c03acf589cbce61249d265f7352db69f43ebaaeee3d1bcc74c6f348743 acclist checklist:PASS mitm.c:51237626
```

```
package check: anomaly-free-atlas-qmax: SM Q_max 39 and 40 (default rows: SM:39)
object/counts.txt sha256: 7cf0a8135b2b33b58b0b0f8fb22c4709bb9cc115a387aa93a4071fa01d8bce43
threads per csenum2 lister: 3, parallel counter jobs: 3, parallel acclist streams: 2, Python checker on lists up to 2000000 lines
step 1 counts file: 2 rows, count = lines + 1 in every row: ok
  422864d72b2d5635fa585d8eb6bb9e9ace6e67be004c344cbbaff26942eca681  verify-it-yourself/checklist.c
  86055d4c7612bdd37db98766f79c88c6397cb72960aa9ec925c87aa41969ca6d  verify-it-yourself/check_list.py
  ec310d4b84cabddcfb66d3aa686efae4a79776fb1abfa4d7cd51f06714cbdac9  how-we-built-it/source/mitm.c
  de18d2f44c2d895880b45f13a99753c92d050c09287efce2a4b5545768d362c8  how-we-built-it/source/acclist.c
step 2 build: ok
step 3 stored lists: 0 checked
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
problem: recount SM Q_max 39: counter gives 51237625, object/counts.txt says 51237626
FAIL
```

## 4. Mode --all

Not run by the contributor with this script. The panel's REPRODUCE skeptic regenerated both lists in full in the
claim run (SM 39: 931 s, SM 40: 1127 s, in parallel) with the claim's checker and its own, and the claim run's lister
did the same (872 s and 1072 s); every hash and line count equals object/counts.txt (`panel/reproduce.md`,
`object/receipts/`).
