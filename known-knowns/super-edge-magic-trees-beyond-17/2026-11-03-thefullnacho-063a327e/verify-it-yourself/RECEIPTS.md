# Receipts: real output of verify-it-yourself/run_checks.sh

## Full run (package with the three certificates unpacked into certificates/)

started 2026-11-03T12:40:55Z, finished 2026-11-03T12:45:24Z (date -u); exit=0, seconds=269; one core; peak RSS of the regeneration step 663080 kB in an earlier identical run.

```
== 1. object/ files match SHA256SUMS
ok   object/CERTIFICATES.md
ok   object/certificates.sha256
ok   object/hardest_trees_n19_n20.txt
PASS
== 2. the five hardest trees (object/hardest_trees_n19_n20.txt): labelings
checked 5 labelings, 0 failures
PASS
== 3. full certificates
ok   cert_n18.txt
ok   cert_n19.txt
ok   cert_n20.txt
PASS
== 4. coverage: trees on n vertices, distinct canonical forms, count = A000055(n), every labeling valid
n=18 lines=123867 distinct_canonical=123867 A000055=123867 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=19 lines=317955 distinct_canonical=317955 A000055=317955 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=20 lines=823065 distinct_canonical=823065 A000055=823065 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
== 5. independent regeneration of all trees on 18..20 vertices and one-to-one matching
n=18 regenerated=123867 A000055=123867 cert_lines=123867 distinct=123867 missing=0 extra=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=19 regenerated=317955 A000055=317955 cert_lines=317955 distinct=317955 missing=0 extra=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=20 regenerated=823065 A000055=823065 cert_lines=823065 distinct=823065 missing=0 extra=0 dup=0 unlabeled=0 label_failures=0 -> PASS
OVERALL: PASS
PASS
```

## Corruption tests (the package checkers on altered copies of cert_n18.txt, 2026-11-03)

Each altered copy changes one line of the 123867-line n=18 certificate. Both checkers must print FAIL; the unmodified control must PASS. No checker crashed (0 tracebacks); an out-of-range or negative vertex id now gives FAIL instead of an IndexError.

| copy | verify_sem_coverage.py | verify_cert.py |
|---|---|---|
| control_unmodified | PASS | PASS |
| dup_exact | FAIL | FAIL |
| dup_iso | FAIL | FAIL |
| gap_distinct | FAIL | FAIL |
| malformed_edge | FAIL | FAIL |
| missing | FAIL | FAIL |
| multiedge | FAIL | FAIL |
| nonint_label | FAIL | FAIL |
| nonint_order | FAIL | FAIL |
| nontree_consec | FAIL | FAIL |
| repeat_label | FAIL | FAIL |
| selfloop | FAIL | FAIL |
| shift_labels | FAIL | FAIL |
| swap | FAIL | FAIL |
| truncated_labels | FAIL | FAIL |
| truncated_last | PASS | PASS |
| vertex_negative | FAIL | FAIL |
| vertex_oob | FAIL | FAIL |
| wrong_n | FAIL | FAIL |

truncated_last cuts only the trailing search-statistics fields (the line stays a complete, valid certificate line), so PASS is correct there; truncated_labels cuts into the label field and fails.
