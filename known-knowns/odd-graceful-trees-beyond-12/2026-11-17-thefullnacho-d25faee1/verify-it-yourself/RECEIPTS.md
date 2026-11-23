# Receipts: real output of the package checkers

Times below are in UTC and, where noted, America/New_York (EST, UTC-5) on 17 November 2026.

## A. Self-test and bundled package check

`sh verify-it-yourself/run_checks.sh` was run from a copy of this package with no CERT_DIR and with
archive_url not yet a live https URL, so section 4 (orders 16..23) was skipped. The last line was
`PASS`. The exact text of that run is in the section "Bundled run" below, captured after SHA256SUMS
was computed.

A later `kit/check_run.py --package` run is expected to repeat this from a clean copy of the package
and also to reject a corrupted copy of an `object/` file.

## B. Full certificates, orders 10..23 (C checker)

The standalone checker `verify-it-yourself/check_og.c` (compiled with `cc -O2 -std=c11`) was run
against the fourteen plain-text certificate files, one core, starting 2026-11-17T18:18:08Z
(1:18:08 PM EST) and ending 2026-11-17T18:19:45Z (1:19:45 PM EST). Self-test passed first.
Every order printed PASS. Combined wall time about 97 seconds; n=23 took 61 seconds, n=22 took 23
seconds. This is the package checker, not a fourth skeptic; the three-skeptic panel confirmed n=23
only (see panel/).

```
full C check of cert_n10.txt .. cert_n23.txt
started 2026-11-17T18:18:08Z (2026-11-17 01:18:08 PM EST)
selftest_failures=0
PASS
n=10 lines_ok=106 unique=106 A000055(10)=106 PASS elapsed_sec=0
n=11 lines_ok=235 unique=235 A000055(11)=235 PASS elapsed_sec=0
n=12 lines_ok=551 unique=551 A000055(12)=551 PASS elapsed_sec=0
n=13 lines_ok=1301 unique=1301 A000055(13)=1301 PASS elapsed_sec=0
n=14 lines_ok=3159 unique=3159 A000055(14)=3159 PASS elapsed_sec=0
n=15 lines_ok=7741 unique=7741 A000055(15)=7741 PASS elapsed_sec=0
n=16 lines_ok=19320 unique=19320 A000055(16)=19320 PASS elapsed_sec=0
n=17 lines_ok=48629 unique=48629 A000055(17)=48629 PASS elapsed_sec=0
n=18 lines_ok=123867 unique=123867 A000055(18)=123867 PASS elapsed_sec=1
n=19 lines_ok=317955 unique=317955 A000055(19)=317955 PASS elapsed_sec=1
n=20 lines_ok=823065 unique=823065 A000055(20)=823065 PASS elapsed_sec=3
n=21 lines_ok=2144505 unique=2144505 A000055(21)=2144505 PASS elapsed_sec=8
n=22 lines_ok=5623756 unique=5623756 A000055(22)=5623756 PASS elapsed_sec=23
n=23 lines_ok=14828074 unique=14828074 A000055(23)=14828074 PASS elapsed_sec=61
ended 2026-11-17T18:19:45Z (2026-11-17 01:19:45 PM EST)
```

For each n: bad_tree_or_label=0, duplicates=0, unique=A000055(n)=lines_ok. The checker confirms
each line is a tree with a valid odd-graceful labeling and that the AHU canonical forms are pairwise
distinct. Independent Python regeneration (leaf extension) of all trees on 10..15 vertices is part
of `run_checks.sh` and matched the bundled files one-to-one. Independent regeneration of all
14,828,074 trees on 23 vertices was done by the panel (see panel/criterion.md and panel/reproduce.md)
and by an earlier leaf-extension re-check from the n=22 certificate (REGEN23_MATCH).

## Bundled run

Captured 2026-11-17T18:21Z from `sh verify-it-yourself/run_checks.sh` in the package folder (no CERT_DIR; archive_url not yet a live https URL). Last line PASS.

```
== 0. self-tests
selftest_failures=0
PASS
selftest_failures=0
PASS
== 1. object/ files match SHA256SUMS
checked=9 ok=9 mismatch=0 missing=0 skipped=31
PASS
== 2. sample_labelings.txt (spot check, several orders)
sample_lines_ok=10 unique=10
PASS
== 3. bundled certificates for n=10..15 (complete, in object/)
lines_ok=106 skipped_comments=0 bad_tree_or_label=0 duplicates=0 unique=106
A000055(10)=106
expected=106
Every listed tree is odd-graceful, the trees are pairwise non-isomorphic, and the count matches.
PASS
lines_ok=235 skipped_comments=0 bad_tree_or_label=0 duplicates=0 unique=235
A000055(11)=235
expected=235
Every listed tree is odd-graceful, the trees are pairwise non-isomorphic, and the count matches.
PASS
lines_ok=551 skipped_comments=0 bad_tree_or_label=0 duplicates=0 unique=551
A000055(12)=551
expected=551
Every listed tree is odd-graceful, the trees are pairwise non-isomorphic, and the count matches.
PASS
lines_ok=1301 skipped_comments=0 bad_tree_or_label=0 duplicates=0 unique=1301
A000055(13)=1301
expected=1301
Every listed tree is odd-graceful, the trees are pairwise non-isomorphic, and the count matches.
PASS
lines_ok=3159 skipped_comments=0 bad_tree_or_label=0 duplicates=0 unique=3159
A000055(14)=3159
expected=3159
Every listed tree is odd-graceful, the trees are pairwise non-isomorphic, and the count matches.
PASS
lines_ok=7741 skipped_comments=0 bad_tree_or_label=0 duplicates=0 unique=7741
A000055(15)=7741
expected=7741
Every listed tree is odd-graceful, the trees are pairwise non-isomorphic, and the count matches.
PASS
== 3b. independent regeneration of all trees on 10..15 vertices
n=10 lines=106 unique=106 expected=106
regenerated=106
regen_match=1
PASS
n=11 lines=235 unique=235 expected=235
regenerated=235
regen_match=1
PASS
n=12 lines=551 unique=551 expected=551
regenerated=551
regen_match=1
PASS
n=13 lines=1301 unique=1301 expected=1301
regenerated=1301
regen_match=1
PASS
n=14 lines=3159 unique=3159 expected=3159
regenerated=3159
regen_match=1
PASS
n=15 lines=7741 unique=7741 expected=7741
regenerated=7741
regen_match=1
PASS
== 4. full certificates n=16..23, if present
full certificates for n=16..23 are not in certificates/ and archive_url is not a live https URL yet
skipping section 4 (bundled n=10..15 and the sample were checked)
OVERALL: PASS
PASS
```
