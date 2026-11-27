# Verification receipts

All output below is pasted from real runs on 2026-11-27 (UTC). NUMERICAL for the times.

**Machine.** A 28-core desktop (Apple M3 Ultra, 96 GB memory), macOS, Python 3.9.6, Apple clang 21.0.0. It was not idle: other jobs kept the load average between about 25 and 39 during these runs, so the times are pessimistic for this machine. No laptop run was made; see the note on laptop time at the end.

## 1. The clean package

Command, from the package folder, with a 880-second alarm and the shell's `time`:

```sh
sh verify-it-yourself/run_checks.sh
```

Output:

```text
== Checker 1: verify-it-yourself/check.py (Python standard library, 4 processes)
[OK] Consecutive odd primes verified; prod(first 14) = 307,444,891,294,245,705 > 6,557,114,959,770,375
[OK] Manifest verified: 9 files, 5,604,948 bytes total (all <= 1,000,000 B, all SHA-256 exact)
[OK] U1_U738: 738 Lemma U certs verified exact (max B = 0.999141 < 1) [0.74s]
[OK] omega= 9: all 5028/5028 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=10: all 1484/1484 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=11: all  248/ 248 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=12: all   21/  21 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=13: all    1/   1 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] G01_G13: 13 anchored model(s), 692 rows verified exact (min surplus = 0.238151) [5.56s]
[OK] F9: 23 anchored model(s), 736 rows verified exact (min surplus = 0.016067) [11.46s]
[OK] A8: 1 anchored model(s), 28,057 rows verified exact (min surplus = 0.002004) [163.76s]
[OK] Theorem A (omega(L) >= 9) and all 6,782 exponent vectors verified unconditionally
[SUMMARY] Verified Theorem A + 738 scalar certs + 37 anchored models (29,485 rows), covering all 6,782 exponent vectors for omega in 9..13 in 182.24s.
PASS
== Checker 1 finished in 182 s, exit code 0
== Checker 2: verify-it-yourself/alternate/ (Python standard library and a C++17 kernel)
A8: 1 models, 28057 exact rows, least surplus 28353678790630767758519622060026627651479943597269246597082274387654587/14150648987289441510301945000553393239539993933702819833147809824000000000
F9: 23 models, 736 exact rows, least surplus 7353010244456360618611/457648694712387914811075
G: 13 models, 692 exact rows, least surplus 31892572639/133917433650
5028 nine-prime vectors dominated
10 primes: 1484 vectors, 1467 by scalar caps, 1467 directly below 1 with the selected parameters, 17 for anchored bounds
11 primes: 248 vectors, 247 by scalar caps, 247 directly below 1 with the selected parameters, 1 for anchored bounds
12 primes: 21 vectors, 21 by scalar caps, 21 directly below 1 with the selected parameters, 0 for anchored bounds
13 primes: 1 vectors, 1 by scalar caps, 1 directly below 1 with the selected parameters, 0 for anchored bounds
Greatest of 738 stored scalar bounds: 130157612206585412852431229/130269519960832360564391936 at (4, 2, 2, 1, 2, 1, 1, 1, 1, 1)
Direct scalar exclusions: 1736. The 18 residual vectors have exactly the 13 declared maximal anchored caps.
PASS
== Checker 2 finished in 14 s including the build, exit code 0
== Both checkers passed
PASS
```

Wall-clock time and exit code (`/usr/bin/time -p`): real 196.92 , exit=0. Finished at 2026-11-27T01:23:38Z. A second clean run with `TMPDIR` pointed at a new empty folder also ended with `PASS` (real 197.66 s, exit code 0; checker 1 finished in 183 s, checker 2 in 15 s including the build), and that folder was empty afterwards: the script removed its temporary folder and the compiled library. No `__pycache__` folder or compiled library was left in the package. The same held for the two corrupted runs in section 2.

## 2. A corrupted copy: one digit changed in a certificate file

The whole package was copied to a temporary folder. In the copy, the first data row of `object/certs/nine_finite.tsv` (line 11, model F9_01, key (1, 2, 1, -1, 1, 0, 0, 0, -1)) had the stored reserve `R_exact` changed from `163/4` to `161/4`, one digit. Nothing else was changed. `sh verify-it-yourself/run_checks.sh` in the copy printed:

```text
== Checker 1: verify-it-yourself/check.py (Python standard library, 4 processes)
[OK] Consecutive odd primes verified; prod(first 14) = 307,444,891,294,245,705 > 6,557,114,959,770,375
ERROR: SHA-256 mismatch on certs/nine_finite.tsv: actual=75e7c8f362c2e8af508aa7c727dfe86cdedd1594b0f3fdfd9497be7c26f92cd0 manifest=152cddf4a84cae30001fdaeb80a086105c2ece1d0b711a505049a5c229035a87
FAIL
== Checker 1 finished in 0 s, exit code 1
Checker 1 did not pass
FAIL
```

real 0.12 , exit=1. The first checker rejects the file through the SHA-256 digest in `object/MANIFEST.json`.

**The same change with the manifest re-hashed**, so that only the arithmetic can catch it (the digest and byte count of `certs/nine_finite.tsv` in the copy's `MANIFEST.json` were recomputed for the changed file):

```text
== Checker 1: verify-it-yourself/check.py (Python standard library, 4 processes)
[OK] Consecutive odd primes verified; prod(first 14) = 307,444,891,294,245,705 > 6,557,114,959,770,375
[OK] Manifest verified: 9 files, 5,604,948 bytes total (all <= 1,000,000 B, all SHA-256 exact)
[OK] U1_U738: 738 Lemma U certs verified exact (max B = 0.999141 < 1) [0.74s]
[OK] omega= 9: all 5028/5028 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=10: all 1484/1484 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=11: all  248/ 248 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=12: all   21/  21 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=13: all    1/   1 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] G01_G13: 13 anchored model(s), 692 rows verified exact (min surplus = 0.238151) [5.58s]
ERROR: R mismatch in F9_01 basic (1, 2, 1, -1, 1, 0, 0, 0, -1): calc=163/4 stored=161/4
FAIL
== Checker 1 finished in 7 s, exit code 1
Checker 1 did not pass
FAIL
```

real 7.46 , exit=1. The second checker, run on its own on this copy (`python3 -B verify-it-yourself/alternate/check_alternate.py object <library>` after building the library as in `run_checks.sh`), also rejects it, with exit code 1:

```text
A8: 1 models, 28057 exact rows, least surplus 28353678790630767758519622060026627651479943597269246597082274387654587/14150648987289441510301945000553393239539993933702819833147809824000000000
invalid inequality in F9_01: basic (1, 2, 1, -1, 1, 0, 0, 0, -1)
FAIL
```

The first line of that output ends in a long fraction, shown in full in section 1.

## 3. The first checker with one process

To bound the time on a machine with fewer free cores, the first checker was also run alone with one process, from the package folder:

```sh
python3 -B verify-it-yourself/check.py --dir object --procs 1
```

Output:

```text
[OK] Consecutive odd primes verified; prod(first 14) = 307,444,891,294,245,705 > 6,557,114,959,770,375
[OK] Manifest verified: 9 files, 5,604,948 bytes total (all <= 1,000,000 B, all SHA-256 exact)
[OK] U1_U738: 738 Lemma U certs verified exact (max B = 0.999141 < 1) [0.74s]
[OK] omega= 9: all 5028/5028 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=10: all 1484/1484 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=11: all  248/ 248 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=12: all   21/  21 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=13: all    1/   1 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] G01_G13: 13 anchored model(s), 692 rows verified exact (min surplus = 0.238151) [17.98s]
[OK] F9: 23 anchored model(s), 736 rows verified exact (min surplus = 0.016067) [38.53s]
[OK] A8: 1 anchored model(s), 28,057 rows verified exact (min surplus = 0.002004) [365.81s]
[OK] Theorem A (omega(L) >= 9) and all 6,782 exponent vectors verified unconditionally
[SUMMARY] Verified Theorem A + 738 scalar certs + 37 anchored models (29,485 rows), covering all 6,782 exponent vectors for omega in 9..13 in 423.77s.
PASS
```

Wall-clock time (`/usr/bin/time -p`): real 423.87 s, exit code 0. Load averages (1, 5, 15 minutes) before and after: 38.61 32.28 27.00; 20.14 29.60 28.47.

## Note on laptop time

No laptop was available for a measurement. On the machine above, under heavy load, the whole script took 197 s with 4 processes, and the first checker alone took 424 s with one process; the second checker took 14 s including its build. All three numbers are well inside the 900-second limit, but they are desktop numbers, not laptop numbers.

## 4. The final script, with the manifest comparison

After the runs above, one step was added at the top of `run_checks.sh`: it compares the sha256 of `object/MANIFEST.json` with the value recorded in `INDEX.csv`. The manifest lists every certificate file with its sha256, so this ties every byte of the manifest and of the certificate files to the package's index row. The two checkers are unchanged. The complete output of the final script on the clean package, run on the same machine on 2026-11-27 (finished 02:04 UTC):

```text
== object/MANIFEST.json sha256: 909804ef2bf322270ec686552d0952780851e07d3c8471cbfac58507b3c715d6
== Checker 1: verify-it-yourself/check.py (Python standard library, 4 processes)
[OK] Consecutive odd primes verified; prod(first 14) = 307,444,891,294,245,705 > 6,557,114,959,770,375
[OK] Manifest verified: 9 files, 5,604,948 bytes total (all <= 1,000,000 B, all SHA-256 exact)
[OK] U1_U738: 738 Lemma U certs verified exact (max B = 0.999141 < 1) [0.72s]
[OK] omega= 9: all 5028/5028 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=10: all 1484/1484 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=11: all  248/ 248 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=12: all   21/  21 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] omega=13: all    1/   1 exponent vectors < 6,557,114,959,770,375 dominated by declared caps
[OK] G01_G13: 13 anchored model(s), 692 rows verified exact (min surplus = 0.238151) [5.46s]
[OK] F9: 23 anchored model(s), 736 rows verified exact (min surplus = 0.016067) [11.35s]
[OK] A8: 1 anchored model(s), 28,057 rows verified exact (min surplus = 0.002004) [164.46s]
[OK] Theorem A (omega(L) >= 9) and all 6,782 exponent vectors verified unconditionally
[SUMMARY] Verified Theorem A + 738 scalar certs + 37 anchored models (29,485 rows), covering all 6,782 exponent vectors for omega in 9..13 in 182.69s.
PASS
== Checker 1 finished in 183 s, exit code 0
== Checker 2: verify-it-yourself/alternate/ (Python standard library and a C++17 kernel)
A8: 1 models, 28057 exact rows, least surplus 28353678790630767758519622060026627651479943597269246597082274387654587/14150648987289441510301945000553393239539993933702819833147809824000000000
F9: 23 models, 736 exact rows, least surplus 7353010244456360618611/457648694712387914811075
G: 13 models, 692 exact rows, least surplus 31892572639/133917433650
5028 nine-prime vectors dominated
10 primes: 1484 vectors, 1467 by scalar caps, 1467 directly below 1 with the selected parameters, 17 for anchored bounds
11 primes: 248 vectors, 247 by scalar caps, 247 directly below 1 with the selected parameters, 1 for anchored bounds
12 primes: 21 vectors, 21 by scalar caps, 21 directly below 1 with the selected parameters, 0 for anchored bounds
13 primes: 1 vectors, 1 by scalar caps, 1 directly below 1 with the selected parameters, 0 for anchored bounds
Greatest of 738 stored scalar bounds: 130157612206585412852431229/130269519960832360564391936 at (4, 2, 2, 1, 2, 1, 1, 1, 1, 1)
Direct scalar exclusions: 1736. The 18 residual vectors have exactly the 13 declared maximal anchored caps.
PASS
== Checker 2 finished in 15 s including the build, exit code 0
== Both checkers passed
PASS
```

Wall-clock time (`/usr/bin/time -p`): real 197.53, user 604.71, sys 3.80. Exit code 0.

A copy of the package with one digit changed inside `object/MANIFEST.json` (in a descriptive text field that neither checker reads) now ends as follows:

```text
== object/MANIFEST.json sha256: 1166dae22f02994774cbeb5ed2730e4bc21d165ab5d24e848b1927f637316532
object/MANIFEST.json does not match the sha256 recorded in INDEX.csv
FAIL
```

