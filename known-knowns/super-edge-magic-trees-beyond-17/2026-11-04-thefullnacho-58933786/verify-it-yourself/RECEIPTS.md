# Receipts: real output of verify-it-yourself/run_checks.sh

## Full run (clean copy of this package, the five certificates in a local folder via CERT_DIR)

started 2026-11-04T03:15:34Z, finished 2026-11-04T03:21:08Z (date -u); exit=0, 334 s wall on a 32-thread desktop at nice 19 (two checker processes in parallel); peak RSS 879220 kB.

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
PASS
== 3. two independent checkers over every line of n = 18..22
-- indep_check.py --regen (WROM regeneration, 1:1 canonical match, A000055 by Otter's formula)
n=18 lines=123867 distinct=123867 A000055(Otter)=123867 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=123867 missing=0 extra=0 -> PASS
n=19 lines=317955 distinct=317955 A000055(Otter)=317955 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=317955 missing=0 extra=0 -> PASS
n=20 lines=823065 distinct=823065 A000055(Otter)=823065 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=823065 missing=0 extra=0 -> PASS
n=21 lines=2144505 distinct=2144505 A000055(Otter)=2144505 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=2144505 missing=0 extra=0 -> PASS
n=22 lines=5623756 distinct=5623756 A000055(Otter)=5623756 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=5623756 missing=0 extra=0 -> PASS
-- verify_sem_coverage.py (AHU canonical codes, distinct count = A000055 from the b-file)
n=18 lines=123867 distinct_canonical=123867 A000055=123867 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=19 lines=317955 distinct_canonical=317955 A000055=317955 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=20 lines=823065 distinct_canonical=823065 A000055=823065 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=21 lines=2144505 distinct_canonical=2144505 A000055=2144505 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=22 lines=5623756 distinct_canonical=5623756 A000055=5623756 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
PASS
```

## Calibration of indep_check.py (attempts/detector-calibration/code/calibrate.py of run 2026-11-03-2244)

```
ok   otter 14 values
ok   canon_complete_n7 11 keys from 16807 labelled trees
ok   canon_complete_n8 23 keys from 262144 labelled trees
ok   wrom_counts_4_16 
ok   wrom_equals_pruefer_n8 
ok   clean_sample_no_line_faults n=21 lines=2000 distinct=2000 A000055(Otter)=2144505
ok   inject_swap_labels bad_label=1
ok   inject_repeat_label bad_label=1
ok   inject_cycle_edge not_tree=1
ok   inject_exact_dup dup=1
ok   inject_iso_dup dup=1
ok   inject_wrong_n wrong_n=1
ok   inject_vertex_oob not_tree=1
PASS
```

The panel skeptics ran further injected defects through their own checkers and through indep_check.py (panel/reproduce.md, panel/criterion.md); all were rejected.

## Live-download run (kit/check_run.py --package, after Zenodo v2 was published)

2026-11-04T03:41:53Z to 03:49:16Z (443 s): a clean copy of this package with no local certificates, so run_checks.sh
fetched the archive from record 23918679 and cert_n21.txt.xz, cert_n22.txt.xz from record 23935954, matched every
hash, and both checkers passed all five orders. check_run.py output:

```
ok:   package 2026-11-04-thefullnacho-58933786: run_checks.sh prints PASS from a clean copy
ok:   package 2026-11-04-thefullnacho-58933786: a corrupted copy of the object is rejected
CHECK_RUN: PASS
```
