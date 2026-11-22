# Receipts

Output of sh verify-it-yourself/run_checks.sh on 2026-10-19 by the builder (python3 3.9, standard library only), on a machine shared with other jobs, after the review fixes. Total wall time 2044.69 s.

```
== reassemble object/vector_part_*.bin and check the whole first
whole object sha256 matches (13118758b86bc0f0daef592d3e85d353851556e54dcd07ad93b6a1c52fc26e54)
== each part against object/SHA256_PARTS.txt
all parts match
== negative controls (first 3000 states only)
negative control 1 (a vector entry set to 1) rejected as expected
negative control 2 (a vector entry set to 0) rejected as expected
== full check: rebuild all states and transitions, pocket tests, ordered subset-inclusion, exact ratio (about 30 to 60 minutes)
ok   lattice: adjacency symmetric and 3-regular; the 8 symmetries about the origin and translations by 3Z^2 are automorphisms (window +-9)
ok   every vertex has a neighbour with strictly larger and one with strictly smaller x, and the same for y (monotone rays)
ok   monotone-ray property verified at every vertex of the window +-9
ok   all 16873086 test-vector entries are positive integers (min 109952, max 1099511627776)
ok   all directed edges in window +-12 reduce to the two seed states (2 classes)
ok   all vertices in the window are equivalent under the symmetry group: 1 class
   ... 2341270 states processed of 3344017 found, 124s
   ... 4512070 states processed of 6102875 found, 244s
   ... 6449670 states processed of 8438653 found, 364s
   ... 8136870 states processed of 10291129 found, 484s
   ... 9276070 states processed of 11481115 found, 604s
   ... 9588070 states processed of 11818917 found, 724s
   ... 10128870 states processed of 12408995 found, 844s
   ... 11030070 states processed of 13279593 found, 964s
   ... 11816870 states processed of 13998615 found, 1084s
   ... 12594070 states processed of 14667916 found, 1204s
   ... 13326870 states processed of 15200331 found, 1324s
   ... 13988070 states processed of 15697588 found, 1445s
   ... 14648870 states processed of 16172072 found, 1565s
   ... 15286070 states processed of 16419644 found, 1685s
   ... 15931670 states processed of 16658697 found, 1805s
   ... 16596870 states processed of 16873086 found, 1925s
states found 16873086, moves kept 26331184, pruned by test 1 2507806, by test 2 1217699, multi-candidate moves 9458099, 1994s
pocket tests: monotone-ray proofs 50783383, full searches 6822189, full searches that hit the 4096 cap 0
ok   vector length 16873086 against the rebuilt state count 16873086
ok   no full pocket search hit the 4096 cap, so every pocket decision is exact (cap hits: 0)
ok   every rebuilt state is in canonical form (non-canonical: 0)
ok   ordered subset-inclusion invariant holds for every candidate target examined (failures: 0)
second-pass candidates present in the state set (all enter the minimum): 0; of these, strictly lowering the running minimum: 0
exact max (P x)_i / x_i = 710041141248 / 388946198528 = 169287/92732 = 1.825551050339  (state index 6930368)
ok   bound 169287/92732 < 1.82926 - 2e-6 (exact rational comparison)
elapsed 2025 s, peak resident memory: main process 7.5 GB, largest worker 0.7 GB
ok   loop length K = 34 and 16,873,086 states, as claimed (K = 34, N = 16873086)
ok   bound equals the claimed 169287/92732 exactly (got 169287/92732)
PASS
ALL CHECKS PASS
```
