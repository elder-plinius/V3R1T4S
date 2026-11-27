# Run it yourself

Requirements: `python3` 3.9 or later (standard library only, no packages to install) and a C++17 compiler `c++`. Rebuilding the certificates (section 3) also needs a C compiler `cc`.

## 1. Check the claim

From this package folder, in a fresh shell:

```sh
sh verify-it-yourself/run_checks.sh
```

It first compares the sha256 of `object/MANIFEST.json` with the value recorded in `INDEX.csv` (the manifest lists every certificate file with its sha256) and prints that sha256 on a line of its own before the output shown below. Then it runs, in order:

1. `python3 -B verify-it-yourself/check.py --dir object --procs N` with N = the number of processors, at most 4. This checker uses only the Python standard library and no floating point. It checks the manifest hashes and size limits, all 738 scalar certificates, all 29,485 anchored inequalities of the 37 anchored certificates, the completeness of every certificate, and the domination of all 6,782 exponent vectors (PROOF.md Section 9.4).
2. `c++ -O3 -std=c++17 -fPIC -shared verify-it-yourself/alternate/finite_geometry.cpp` into a temporary folder, then `python3 -B verify-it-yourself/alternate/check_alternate.py object <that library>`. This second checker was written separately, with its own exact arithmetic and its own integer kernel for the geometric maximum (derivation in `verify-it-yourself/alternate/ALTERNATE.md`). It reads the same nine certificate files.

The file formats and the checks are specified in `verify-it-yourself/FORMAT.md`.

The last line is `PASS` only if both checkers end with `PASS`; otherwise it is `FAIL`. The temporary folder is removed at the end.

Expected output (from the run recorded in `verify-it-yourself/RECEIPTS.md`; the times vary from machine to machine):

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

Measured on 2026-11-27 (UTC) on a 28-core desktop (Apple M3 Ultra) under heavy load from other jobs: 197 s in all (first checker 182 s with 4 processes, second checker 14 s including its build); the first checker alone with one process took 424 s. Not measured on a laptop. Details in `verify-it-yourself/RECEIPTS.md`.

To run the first checker with one process only: `python3 -B verify-it-yourself/check.py --dir object --procs 1`.

## 2. Optional extra checks shipped with the second checker

- `python3 -B verify-it-yourself/alternate/verify_nine.py object/certs/nine_finite.tsv`: a third, Python-only check of the nine-prime branch with a different maximizer (see `verify-it-yourself/alternate/BASIC-CHECK.md`); `verify-it-yourself/alternate/nine-finite.json` is the companion table it can also read.
- `verify-it-yourself/alternate/REFEREE.md`: a referee report with a verdict on each of the 28 named results of PROOF.md (contributor text, written by one of the models that rechecked the certificates).

## 3. Rebuild the certificate files

`how-we-built-it/README.md` gives the exact commands. They copy `how-we-built-it/` to a temporary folder, rebuild the nine-prime table, the scalar certificates, the ten- and eleven-prime anchored certificates, the eight-prime certificate and the manifest, and compare each result byte for byte with `object/`.

In a real run on 2026-11-27 (UTC) the rebuild took 145 s in all and every one of the ten files (`object/MANIFEST.json` and the nine files in `object/certs/`) came out byte-identical; the step times are in `how-we-built-it/README.md`.
