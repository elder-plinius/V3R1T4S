# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded on the contributor's machine: Linux x86_64, 4 cores, 15 GB of memory, gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0, Python 3.13.16. Every run was
started from the package folder (or a copy of it) as `taskset -c 3 nice -n 10 sh verify-it-yourself/run_checks.sh`
(pinned to one core, low priority, while the panel's reproduction used the other three), with `TMPDIR` pointing to
a scratch folder; start time from `date -u`, wall time from `date +%s`. After these runs only documentation changed
(README.md, HOW_WE_FOUND_IT.md, RUN_IT_YOURSELF.md, this file, panel/ copies and SHA256SUMS); `verify-it-yourself/`
code, `object/` and `how-we-built-it/source/` are unchanged. `--all` was not run for the package (about 2.5 h); the
panel's REPRODUCE skeptic regenerated all four lists in full with its own checker (`panel/reproduce.md`).

## 1. The package as shipped, default rows (exit 0, 571 s, 2026-11-04T11:02:42Z to 2026-11-04T11:12:13Z)

```
package check: anomaly-free-atlas-qmax: SMnuR Q_max 20 and SM Q_max 36..38 (default rows: SM:36)
object/counts.txt sha256: 12f0deb4ad093991fa9b6663c199d5f282bb6a4a79fa805c584ac5e4d542d1ee
threads per csenum2 lister: 3, parallel counter jobs: 3, parallel acclist streams: 2, Python checker on lists up to 2000000 lines
step 1 counts file: 4 rows, count = lines + 1 in every row: ok
  422864d72b2d5635fa585d8eb6bb9e9ace6e67be004c344cbbaff26942eca681  verify-it-yourself/checklist.c
  86055d4c7612bdd37db98766f79c88c6397cb72960aa9ec925c87aa41969ca6d  verify-it-yourself/check_list.py
  ec310d4b84cabddcfb66d3aa686efae4a79776fb1abfa4d7cd51f06714cbdac9  how-we-built-it/source/mitm.c
  de18d2f44c2d895880b45f13a99753c92d050c09287efce2a4b5545768d362c8  how-we-built-it/source/acclist.c
  4c14e8ea97f17cce68e88c5dbb3b4eb324f804e68b95d457b20ab531eb4feba6  how-we-built-it/source/csenum2.c
step 2 build: ok
step 3 stored lists: 0 checked
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
  recount SM Q_max 36: 32457211 = object/counts.txt count: ok
  (mitm counter, 20 calibration values and 1 rows: 50 s)
  SM Q_max 36 by acclist: lines 32457210, sha256 7fd525fd695292d2991dbc051bf7ddf10a35b91d3e85a7a22a165e9183e52b4f, C checker PASS (32457210 valid), Python checker not run (more than 2000000 lines), 520 s
  SM Q_max 36 by acclist: matches object/counts.txt
step 5 regenerated lists: 1 streams, all equal to object/counts.txt
rows checked: 1 of 4 (default)
PASS
```

## 2. Control: one digit of the object changed (exit 1, 0 s, started 2026-11-04T11:01:04Z)

In a copy of the package, the middle ASCII digit of object/counts.txt (byte 286, line 2, row SM 36, in the recorded
count.c value: 32457211 -> 32447211) was changed: the same corruption repo/kit/check_run.py applies to a copy of the
package. (A first version of rows.py did not read that field and passed this copy; rows.py now checks every recorded
counter value against the count, and the copy fails.)

```
package check: anomaly-free-atlas-qmax: SMnuR Q_max 20 and SM Q_max 36..38 (default rows: SM:36)
object/counts.txt sha256: 9fb1e9929b95fc85a8758ee1877f2a9bf388c2557ee80dee92f932ff42cd89c2
threads per csenum2 lister: 3, parallel counter jobs: 3, parallel acclist streams: 2, Python checker on lists up to 2000000 lines
counts file: SM:36: recorded count.c count 32447211 differs from count 32457211
problem: object/counts.txt
FAIL
```

## 3. Control: a count changed consistently (exit 1, 67 s, started 2026-11-04T11:01:35Z)

In another copy, row SM 37 was changed so that it stays internally consistent (count 37347334 -> 37347344, lines
37347333 -> 37347343, mitm.c:37347334 -> mitm.c:37347344); step 1 cannot see this, the independent recount does.

```
package check: anomaly-free-atlas-qmax: SMnuR Q_max 20 and SM Q_max 36..38 (chosen rows: SM:37)
object/counts.txt sha256: 872feac722ffaf2897d9a9644e49571d6b1efd4af8ce45bff9dd8ea38c494306
threads per csenum2 lister: 3, parallel counter jobs: 3, parallel acclist streams: 2, Python checker on lists up to 2000000 lines
step 1 counts file: 4 rows, count = lines + 1 in every row: ok
  422864d72b2d5635fa585d8eb6bb9e9ace6e67be004c344cbbaff26942eca681  verify-it-yourself/checklist.c
  86055d4c7612bdd37db98766f79c88c6397cb72960aa9ec925c87aa41969ca6d  verify-it-yourself/check_list.py
  ec310d4b84cabddcfb66d3aa686efae4a79776fb1abfa4d7cd51f06714cbdac9  how-we-built-it/source/mitm.c
  de18d2f44c2d895880b45f13a99753c92d050c09287efce2a4b5545768d362c8  how-we-built-it/source/acclist.c
  4c14e8ea97f17cce68e88c5dbb3b4eb324f804e68b95d457b20ab531eb4feba6  how-we-built-it/source/csenum2.c
step 2 build: ok
step 3 stored lists: 0 checked
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
problem: recount SM Q_max 37: counter gives 37347334, object/counts.txt says 37347344
FAIL
```
