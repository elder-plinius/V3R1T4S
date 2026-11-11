# Receipts: real output of verify-it-yourself/run_checks.sh

## Full run, n = 18 to 25 (a clean copy of this package; certificates in a local folder via CERT_DIR)

started 2026-11-10T20:43:23Z, finished 2026-11-10T23:40:00Z (date -u); exit=0; secs=10597.12 s wall; peak RSS 11364932 kB; one core at a time, nice 19, on the contributor's 32-thread desktop.

```
== 1. object/ files match SHA256SUMS
ok   object/CERTIFICATES.md
ok   object/certificates.sha256
PASS
== 2. certificates present and matching object/certificates.sha256
ok   cert_n18.txt
ok   cert_n19.txt
ok   cert_n20.txt
ok   cert_n21.txt.xz
ok   cert_n22.txt.xz
ok   cert_n23.txt.xz
ok   cert_n24.txt.xz
ok   cert_n25.txt.xz
PASS
== 3. indep_check.py --regen: every tree regenerated (WROM) and matched 1:1, A000055 by Otter's formula
n=18 lines=123867 distinct=123867 A000055(Otter)=123867 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=123867 missing=0 extra=0 -> PASS
n=19 lines=317955 distinct=317955 A000055(Otter)=317955 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=317955 missing=0 extra=0 -> PASS
n=20 lines=823065 distinct=823065 A000055(Otter)=823065 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=823065 missing=0 extra=0 -> PASS
n=21 lines=2144505 distinct=2144505 A000055(Otter)=2144505 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=2144505 missing=0 extra=0 -> PASS
n=22 lines=5623756 distinct=5623756 A000055(Otter)=5623756 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=5623756 missing=0 extra=0 -> PASS
n=23 lines=14828074 distinct=14828074 A000055(Otter)=14828074 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=14828074 missing=0 extra=0 -> PASS
n=24 lines=39299897 distinct=39299897 A000055(Otter)=39299897 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=39299897 missing=0 extra=0 -> PASS
n=25 lines=104636890 distinct=104636890 A000055(Otter)=104636890 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=104636890 missing=0 extra=0 -> PASS
== 4. verify_sem_coverage.py: distinct AHU canonical codes, count = A000055 (b-file), every labeling checked
n=18 lines=123867 distinct_canonical=123867 A000055=123867 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=19 lines=317955 distinct_canonical=317955 A000055=317955 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=20 lines=823065 distinct_canonical=823065 A000055=823065 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=21 lines=2144505 distinct_canonical=2144505 A000055=2144505 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=22 lines=5623756 distinct_canonical=5623756 A000055=5623756 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=23 lines=14828074 distinct_canonical=14828074 A000055=14828074 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=24 lines=39299897 distinct_canonical=39299897 A000055=39299897 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=25 lines=104636890 distinct_canonical=104636890 A000055=104636890 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
PASS
```

The checkers were calibrated in run 2026-11-03-2244 (indep_check.py: 13 of 13 tests, including seven injected defect
classes); the panel skeptics ran further injected defects through their own checkers (panel/reproduce.md,
panel/criterion.md). A live-download run by kit/check_run.py follows.

## Live-download run (kit/check_run.py --package --timeout 21600, after Zenodo v3 was published)

2026-11-10T23:40:00Z to 2026-11-11T03:01:33Z: a clean copy of this package with no local certificates; run_checks.sh fetched the archive and
cert_n21 to cert_n25 from record 24116616, matched every hash, and both checkers passed n = 18 to 25. check_run.py output:

```
ok:   package 2026-11-10-thefullnacho-a349985c: run_checks.sh prints PASS from a clean copy
ok:   package 2026-11-10-thefullnacho-a349985c: a corrupted copy of the object is rejected
CHECK_RUN: PASS
```
