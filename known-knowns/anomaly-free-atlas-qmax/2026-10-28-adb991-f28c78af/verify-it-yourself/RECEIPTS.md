# Receipts: real output of verify-it-yourself/run_checks.sh

Recorded on the contributor's machine: Linux x86_64, 4 cores (Intel Xeon Processor @ 2.80GHz), 15 GB of memory,
gcc 13.3.0, Python 3.13.16. Every run was started from the package folder (or a copy of it) as
`taskset -c 0-2 nice -n 10 sh verify-it-yourself/run_checks.sh` (pinned to 3 cores, low priority), with `TMPDIR`
pointing to a scratch folder; start time from `date -u`, wall time from `date +%s`.
Sections 1, 3 and 4 were recorded before section 2. Between them only documentation changed (README.md, this
file, SHA256SUMS and one token of panel/reproduce.md, see README.md); `verify-it-yourself/` code, `object/` and
`how-we-built-it/source/` are unchanged.

## 1. The package as shipped, default rows (exit 0, 298 s, 2026-10-28T12:34:21Z to 2026-10-28T12:39:19Z)

```
package check: anomaly-free-atlas-qmax: SMnuR Q_max 19 and SM Q_max 32..35 (default rows: SM:32 SM:33)
object/counts.txt sha256: f28c78af6a83c2ba2c08944e389294071fb1f6a1f18c0a2770b6c6b7472bc60e
threads per csenum2 lister: 3, parallel counter jobs: 3, parallel acclist streams: 2, Python checker on lists up to 2000000 lines
step 1 counts file: 5 rows, count = lines + 1 in every row: ok
  422864d72b2d5635fa585d8eb6bb9e9ace6e67be004c344cbbaff26942eca681  verify-it-yourself/checklist.c
  86055d4c7612bdd37db98766f79c88c6397cb72960aa9ec925c87aa41969ca6d  verify-it-yourself/check_list.py
  ec310d4b84cabddcfb66d3aa686efae4a79776fb1abfa4d7cd51f06714cbdac9  how-we-built-it/source/mitm.c
  de18d2f44c2d895880b45f13a99753c92d050c09287efce2a4b5545768d362c8  how-we-built-it/source/acclist.c
  4c14e8ea97f17cce68e88c5dbb3b4eb324f804e68b95d457b20ab531eb4feba6  how-we-built-it/source/csenum2.c
step 2 build: ok
step 3 stored lists: 0 checked
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
  recount SM Q_max 32: 15866882 = object/counts.txt count: ok
  recount SM Q_max 33: 19550225 = object/counts.txt count: ok
  (mitm counter, 20 calibration values and 2 rows: 24 s)
  SM Q_max 32 by acclist: lines 15866881, sha256 3a5d7d1695cd98e6aa70ecc3c0ff9121f9312a11f0123ec6e6cec7a8ad408a07, C checker PASS (15866881 valid), Python checker not run (more than 2000000 lines), 213 s
  SM Q_max 32 by acclist: matches object/counts.txt
  SM Q_max 33 by acclist: lines 19550224, sha256 fab3aded0a00e3dfeedf3c45386728a3d9bd3f6bf22f748c58c0dcea7f1ee86c, C checker PASS (19550224 valid), Python checker not run (more than 2000000 lines), 273 s
  SM Q_max 33 by acclist: matches object/counts.txt
step 5 regenerated lists: 2 streams, all equal to object/counts.txt
rows checked: 2 of 5 (default)
PASS
```

## 2. The package as shipped, all rows: `--all` (exit 0, 6427 s, 2026-10-28T12:50:40Z to 2026-10-28T14:37:47Z)

Same machine and command with `--all`, run when nothing else was running. The resident memory of the `csenum2`
process, sampled with `ps` during the SMnuR 19 stream, reached 4418556 KB (about 4.4 GB).

```
package check: anomaly-free-atlas-qmax: SMnuR Q_max 19 and SM Q_max 32..35 (all rows: SMnuR:19 SM:32 SM:33 SM:34 SM:35)
object/counts.txt sha256: f28c78af6a83c2ba2c08944e389294071fb1f6a1f18c0a2770b6c6b7472bc60e
threads per csenum2 lister: 3, parallel counter jobs: 3, parallel acclist streams: 2, Python checker on lists up to 2000000 lines
step 1 counts file: 5 rows, count = lines + 1 in every row: ok
  422864d72b2d5635fa585d8eb6bb9e9ace6e67be004c344cbbaff26942eca681  verify-it-yourself/checklist.c
  86055d4c7612bdd37db98766f79c88c6397cb72960aa9ec925c87aa41969ca6d  verify-it-yourself/check_list.py
  ec310d4b84cabddcfb66d3aa686efae4a79776fb1abfa4d7cd51f06714cbdac9  how-we-built-it/source/mitm.c
  de18d2f44c2d895880b45f13a99753c92d050c09287efce2a4b5545768d362c8  how-we-built-it/source/acclist.c
  4c14e8ea97f17cce68e88c5dbb3b4eb324f804e68b95d457b20ab531eb4feba6  how-we-built-it/source/csenum2.c
step 2 build: ok
step 3 stored lists: 0 checked
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
  recount SMnuR Q_max 19: 4247050205 = object/counts.txt count: ok
  recount SM Q_max 32: 15866882 = object/counts.txt count: ok
  recount SM Q_max 33: 19550225 = object/counts.txt count: ok
  recount SM Q_max 34: 22847889 = object/counts.txt count: ok
  recount SM Q_max 35: 26469950 = object/counts.txt count: ok
  (mitm counter, 20 calibration values and 5 rows: 191 s)
  SM Q_max 32 by acclist: lines 15866881, sha256 3a5d7d1695cd98e6aa70ecc3c0ff9121f9312a11f0123ec6e6cec7a8ad408a07, C checker PASS (15866881 valid), Python checker not run (more than 2000000 lines), 225 s
  SM Q_max 32 by acclist: matches object/counts.txt
  SM Q_max 33 by acclist: lines 19550224, sha256 fab3aded0a00e3dfeedf3c45386728a3d9bd3f6bf22f748c58c0dcea7f1ee86c, C checker PASS (19550224 valid), Python checker not run (more than 2000000 lines), 287 s
  SM Q_max 33 by acclist: matches object/counts.txt
  SM Q_max 34 by acclist: lines 22847888, sha256 e22875f7b3ded06eeb05e00464da98b943e60db7afac2d673357e1da1e72c74b, C checker PASS (22847888 valid), Python checker not run (more than 2000000 lines), 355 s
  SM Q_max 34 by acclist: matches object/counts.txt
  SM Q_max 35 by acclist: lines 26469949, sha256 f3a6b7ff8fd4abe877c3d3f867877a811a27eb0fe3317495978f6c631a02fa9f, C checker PASS (26469949 valid), Python checker not run (more than 2000000 lines), 439 s
  SM Q_max 35 by acclist: matches object/counts.txt
  SMnuR Q_max 19 by csenum2: lines 4247050204, sha256 0fc9e8b841f69b7825c4de8c8ff1b987f29a2314edce997157069e0b48216f81, C checker PASS (4247050204 valid), Python checker not run (more than 2000000 lines), 5509 s
  SMnuR Q_max 19 by csenum2: matches object/counts.txt
step 5 regenerated lists: 5 streams, all equal to object/counts.txt
rows checked: 5 of 5 (all)
PASS
```

## 3. Control: one digit of the object changed (exit 1, 0 s, started 2026-10-28T12:42:39Z)

In a copy of the package, the middle ASCII digit of object/counts.txt (line 4, row SM 33, the list line count
19550224 -> 19550124) was changed from 2 to 1: the same corruption repo/kit/check_run.py applies to a copy of the
package (the middle ASCII digit of the first text file in object/ is changed).

```
package check: anomaly-free-atlas-qmax: SMnuR Q_max 19 and SM Q_max 32..35 (default rows: SM:32 SM:33)
object/counts.txt sha256: 9aae9ade7abbfc2b8e53eb087e57ec766b11fe6c9c699ded679a701fa6a48b79
threads per csenum2 lister: 3, parallel counter jobs: 3, parallel acclist streams: 2, Python checker on lists up to 2000000 lines
counts file: SM Q_max 33: count 19550225 is not lines 19550124 + 1
problem: object/counts.txt
FAIL
```

## 4. Control: a count changed consistently (exit 1, 30 s)

In another copy, row SM 32 was changed so that it stays internally consistent (count 15866882 -> 15866892, lines
15866881 -> 15866891, recorded counter value mitm.c:15866882 -> mitm.c:15866892); step 1 cannot see this, the
independent recount does.

```
package check: anomaly-free-atlas-qmax: SMnuR Q_max 19 and SM Q_max 32..35 (default rows: SM:32 SM:33)
object/counts.txt sha256: 752fe69c63dc4e8c6c0dc6387c16f1bed5b70ea1b975cae850b91719a3832b11
threads per csenum2 lister: 3, parallel counter jobs: 3, parallel acclist streams: 2, Python checker on lists up to 2000000 lines
step 1 counts file: 5 rows, count = lines + 1 in every row: ok
  422864d72b2d5635fa585d8eb6bb9e9ace6e67be004c344cbbaff26942eca681  verify-it-yourself/checklist.c
  86055d4c7612bdd37db98766f79c88c6397cb72960aa9ec925c87aa41969ca6d  verify-it-yourself/check_list.py
  ec310d4b84cabddcfb66d3aa686efae4a79776fb1abfa4d7cd51f06714cbdac9  how-we-built-it/source/mitm.c
  de18d2f44c2d895880b45f13a99753c92d050c09287efce2a4b5545768d362c8  how-we-built-it/source/acclist.c
  4c14e8ea97f17cce68e88c5dbb3b4eb324f804e68b95d457b20ab531eb4feba6  how-we-built-it/source/csenum2.c
step 2 build: ok
step 3 stored lists: 0 checked
step 4 calibration SM: Q_max 1..10 = 8 22 82 251 626 1983 3902 7068 14354 23800 = published values: ok
step 4 calibration SMnuR: Q_max 1..10 = 38 358 4116 24552 111152 435305 1358388 3612734 9587085 21546920 = published values: ok
problem: recount SM Q_max 32: counter gives 15866882, object/counts.txt says 15866892
FAIL
```

## What the default run does not cover

A changed digit inside the sha256 of a row outside the selected rows (SM 34, 35 or SMnuR 19) is not caught by the
default run, since those lists are not regenerated; `--all` (or `--rows`) checks them. A changed count, line count or
recorded counter value in any row is caught by step 1 unless the change is made consistently in all three columns;
then only the recount of that row (section 4) catches it.
