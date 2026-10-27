# REPRODUCE

context: saved counter outputs results/2026-10-15-a396618/verify_out.txt, results/2026-10-15-a396618/search_out.txt, results/2026-10-15-a396618/quick_run.txt, results/2026-10-17-a396618-a24/verify_run.txt, and results/2026-10-18-a396618-a25/sqrt25_out.txt, re-read while assembling this package, plus a fresh run of verify-it-yourself/check.py

Definition used by the counters: a(n) is the number of k with 10^(n-1) <= k^2 < 10^n such that k^2 modulo 10^d is not a square for every d = 1..n-1. Zero counts as a square.

Saved square-root halves (verify_out.txt), which add to the claimed totals:

- a(22): 3169035152 + 3169037037 = 6338072189
- a(23): 10021305758 + 10021215624 = 20042521382

Saved table-counter halves (search_out.txt), a different split and a different program, same totals:

- a(22): 3167978581 + 3170093608 = 6338072189
- a(23): 10020018261 + 10022503121 = 20042521382

quick_run.txt is the square-root counter on a(2) through a(17) against the published prefix. Its last line is PASS.

verify_run.txt for a(24) recomputes a(10) through a(19) against OEIS and then a(24). Its relevant lines are `a(24) = 63380064097  claimed 63380064097  OK` and `PASS`.

sqrt25_out.txt for a(25) is the same square-root counter in two parts: `25 0 100208870556 8730` and `25 1 100215785299 8793`. The sum is 200424655855. The 5-adic counter's four saved parts 55569676883 + 55569740450 + 44642734606 + 44642503916 also add to 200424655855. verify_run_small.txt is only the a(10) through a(19) calibration of that binary; its last line is PASS. There is no separate one-line PASS wrapper around the a(25) halves; the record is the two part lines and the matching 5-adic sum.

The fresh checker in this package recomputes a(2) through a(19) and rejects an object whose terms differ from this list.

pass: true
