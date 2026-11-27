# Receipts (real output of sh verify-it-yourself/run_checks.sh, 2026-11-25, box under light load)
```
ok:   sha256 chunks_head128.jsonl
ok:   sha256 chunks_tail_1.jsonl
ok:   sha256 chunks_tail_2.jsonl
ok:   contiguous chunks n = 1..2325573, gamma increasing, 5814 records
ok:   head chunks n <= 600,000 at 128 bits
ok:   boundary: gamma_2325572 < 1.3e6 < gamma_2325573, N(T0) = 2325572
ok:   last stored zero is n = 2,325,573 (excluded from the sum)
ok:   K2 re-summed exactly: mid 1.000305250386511540..., rad 3.520417e-15
ok:   overlaps stored arb ball [1.00030525038651 +/- 5.07e-15]
ok:   inside the certificate's K2 ball [1.0003052504 +/- 2.30e-11]
ok:   lower(K2) - 1 - E = 3.052504e-04 > 0 (E = certificate's own value, unchecked)
ok:   head n <= 600,000 overlaps the certificate's K2_main
ok:   INDEX.csv row and sha256 of object/k2_result.json
PASS

real	0m0.058s
user	0m0.031s
sys	0m0.026s
```

With FLINT=1 (python-flint 0.9.0), same lines plus:
```
ok:   FLINT recompute of chunk n0 = 300001
ok:   FLINT recompute of chunk n0 = 1462801
ok:   FLINT recompute of chunk n0 = 2325201
PASS

real	0m24.809s
user	0m24.783s
sys	0m0.020s
```
