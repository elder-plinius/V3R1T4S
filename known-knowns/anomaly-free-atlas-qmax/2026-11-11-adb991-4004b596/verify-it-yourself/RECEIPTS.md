# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded on the contributor's machine: Linux x86_64, 4 cores, 15 GB of memory (a session memory cap of about 7.4 GB),
gcc 13.3.0, Python 3 (standard library). Every run was started from a copy of the package's object/,
verify-it-yourself/ and how-we-built-it/ folders (the folders the script reads) as `sh verify-it-yourself/run_checks.sh`
(sections 1 and 3 under `nice -n 10`), with the default settings. Start and end times from `date -u`. Sections 1 and 3
started together, and a separate counting job (mitm.c for other rows) ran beside section 1 for its first 12 minutes.

## 1. Default mode, the package as shipped (exit 0, 1447 s, 2026-11-12T00:11:26Z to 2026-11-12T00:35:33Z)

```
package check: anomaly-free-atlas-qmax: SM Q_max 41 and 42 (default rows: SM:41)
object/counts.txt sha256: 4004b5967da833d3bb727cb0f304c93db08d44d999b5bb5c18e3281ecf054103
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
  recount SM Q_max 41: 66526761 = object/counts.txt count: ok
  (mitm counter, 20 calibration values and 1 rows: 92 s)
  SM Q_max 41 by acclist: lines 66526760, sha256 ad5133b7fcbe5ec91cc5416bda0b5a8629e0b85ba5d2d4c0aa89ef4f4282f6ec, C checker PASS (66526760 valid), Python checker not run (more than 2000000 lines), 1354 s
  SM Q_max 41 by acclist: matches object/counts.txt
step 5 regenerated lists: 1 streams, all equal to object/counts.txt
rows checked: 1 of 2 (default)
PASS
```

## 2. Control: one digit of the object changed (exit 1, 0 s, 2026-11-12T00:11:27Z)

In a copy of the package, the middle ASCII digit of the first text file in object/ was changed, the same corruption
repo/kit/check_run.py applies to a copy of the package (from the script that applied it):

```
object/counts.txt line 2: digit 4 -> 1; sha256 aba5953077475448899852978a633bcca615e3869818c833298593aa66b3e095
context before: SM 42 79174540 79174539 8d6d0fcd99099ba8b46071ba4a6e1051fa8fcb1fb165f8c55c7f150bcbed6df2 acclist checklist:PASS mitm.c:79174540
context after:  SM 12 79174540 79174539 8d6d0fcd99099ba8b46071ba4a6e1051fa8fcb1fb165f8c55c7f150bcbed6df2 acclist checklist:PASS mitm.c:79174540
```

```
package check: anomaly-free-atlas-qmax: SM Q_max 41 and 42 (default rows: SM:41)
object/counts.txt sha256: aba5953077475448899852978a633bcca615e3869818c833298593aa66b3e095
threads per csenum2 lister: 3, parallel counter jobs: 3, parallel acclist streams: 2, Python checker on lists up to 2000000 lines
counts file: rows in file (SM:12 SM:41) differ from the claimed rows (SM:41 SM:42)
problem: object/counts.txt
FAIL
```

## 3. Control: a count changed consistently in all three fields (exit 1, 93 s, 2026-11-12T00:11:26Z to 2026-11-12T00:12:59Z)

In another copy, the SM 41 row of object/counts.txt was changed so that the count, the line count and the recorded
mitm.c value stay consistent with each other. Step 1 cannot see this; the recount without a list catches it.

```
object/counts.txt row SM 41: count 66526761 -> 66526762, lines 66526760 -> 66526761, mitm.c field 66526761 -> 66526762 (consistent, so rows.py passes)
```

```
package check: anomaly-free-atlas-qmax: SM Q_max 41 and 42 (default rows: SM:41)
object/counts.txt sha256: cb00ffac27e6dd641e16389321608880592caa3348251e70ccf2f1e24b12fe30
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
problem: recount SM Q_max 41: counter gives 66526761, object/counts.txt says 66526762
FAIL
```

## 4. Mode --all

Not run by the contributor with this script. The panel's REPRODUCE skeptic regenerated both lists in full in the
claim run (SM 41: 1249 s, SM 42: 1529 s, in parallel) with the claim's checker and its own strict checker, and the
claim run's lister did the same (1171 s and 1448 s); every hash and line count equals object/counts.txt
(`panel/reproduce.md`, `object/receipts/`).
