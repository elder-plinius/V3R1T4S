# Independent brute-force completeness check (segment 2, 2026-10-23 ~10:15-10:30 ET)
Code: brute.c (k<=2), brute3.c (k=3). Written separately from fsearch.c (no shared code; plain array simulation).
Convention: checker onset s (= fsearch t - 1, same offset as crosscheck.txt). Filter-onset s = least s with
H[u]==H[u-104] for all u in [s+104, NS). Every true highway with onset s passes the filter, so "no config has
filter-s < X" proves g > X for that config class (given the box argument).
- k=0: blank grid, filter-s=895 over NS=1000 (no highway before 1000; consistent with 9977).
- k=1, box R=35 (5041 cells), NS=1000, escapes=0: min filter-s=309, unique (0,-2). Next best 312 at (1,3).
- k=2, box R=35, all 12,703,320 pairs, NS=1000, escapes=0: min filter-s=161, unique {(-1,3),(1,3)}.
  => matches fsearch g(1)=310, g(2)=162 and uniqueness.
- Box argument (k<=2): for every set C' of <=2 cells inside the box the ant never leaves the box in NS steps
  (escapes=0). For any finite C, C' = C ∩ box gives an identical first NS steps, so C passes the filter iff C' does.
  Hence g(1)=310 and g(2)=162 are proven over ALL placements (exactly / at most k cells), modulo code correctness.
- k=3, box R=14 (841 cells, 98.8M triples), NS=500: min filter-s=125, unique {(3,-5),(1,-3),(0,-2)} (matches
  fsearch g(3)=126). NOT complete: 5,780 triples let the ant leave the box within 500 steps, so far cells could
  matter for those; this is supporting evidence only for k=3.
