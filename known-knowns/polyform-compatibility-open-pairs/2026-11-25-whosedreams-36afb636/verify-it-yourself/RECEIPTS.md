# Receipts (real output, packaging machine, 2026-11-24 ET)

## `sh verify-it-yourself/run_checks.sh` (default KMAX=4, about 5 s)
```
ok   OBJECT_SHA256 lists exactly the files in object/
ok   sha256 of object/SHA256SUMS-archive.txt
ok   sha256 of object/SHA256SUMS-files.txt
ok   sha256 of object/mx_k2_20_bounded_unsat.json
ok   SHA256SUMS-files.txt has 38 distinct files
ok   per_k covers k = 2..20 once each
ok   pair is M-X
ok   k=2: area, board 10x12, unsat+verified, label, sha256s
ok   k=3: area, board 12x14, unsat+verified, label, sha256s
ok   k=4: area, board 13x15, unsat+verified, label, sha256s
ok   k=5: area, board 14x16, unsat+verified, label, sha256s
ok   k=6: area, board 15x17, unsat+verified, label, sha256s
ok   k=7: area, board 16x18, unsat+verified, label, sha256s
ok   k=8: area, board 17x19, unsat+verified, label, sha256s
ok   k=9: area, board 18x20, unsat+verified, label, sha256s
ok   k=10: area, board 19x21, unsat+verified, label, sha256s
ok   k=11: area, board 20x22, unsat+verified, label, sha256s
ok   k=12: area, board 21x23, unsat+verified, label, sha256s
ok   k=13: area, board 22x24, unsat+verified, label, sha256s
ok   k=14: area, board 22x24, unsat+verified, label, sha256s
ok   k=15: area, board 23x25, unsat+verified, label, sha256s
ok   k=16: area, board 24x26, unsat+verified, label, sha256s
ok   k=17: area, board 24x26, unsat+verified, label, sha256s
ok   k=18: area, board 25x27, unsat+verified, label, sha256s
ok   k=19: area, board 26x28, unsat+verified, label, sha256s
ok   k=20: area, board 26x28, unsat+verified, label, sha256s
ok   every file in SHA256SUMS-files.txt belongs to exactly one k
ok   archive sha256 matches SHA256SUMS-archive.txt
ok   archive size recorded
ok   coordinate converter is injective and preserves edge adjacency
ok   24 free heptiamonds (found 24)
ok   X is the only heptiamond with exactly 4 aspects
ok   M: 7 triangles, connected, 6 aspects
ok   object's M is congruent to M from the definition
ok   object's X is congruent to X from the definition
ok   k=2: placements in board M 216 / X 144 (object 216 / 144)
ok   k=3: placements in board M 330 / X 220 (object 330 / 220)
ok   k=4: placements in board M 396 / X 264 (object 396 / 264)
ok   k=5: placements in board M 468 / X 312 (object 468 / 312)
ok   k=6: placements in board M 546 / X 364 (object 546 / 364)
ok   k=7: placements in board M 630 / X 420 (object 630 / 420)
ok   k=8: placements in board M 720 / X 480 (object 720 / 480)
ok   k=9: placements in board M 816 / X 544 (object 816 / 544)
ok   k=10: placements in board M 918 / X 612 (object 918 / 612)
ok   k=11: placements in board M 1026 / X 684 (object 1026 / 684)
ok   k=12: placements in board M 1140 / X 760 (object 1140 / 760)
ok   k=13: placements in board M 1260 / X 840 (object 1260 / 840)
ok   k=14: placements in board M 1260 / X 840 (object 1260 / 840)
ok   k=15: placements in board M 1386 / X 924 (object 1386 / 924)
ok   k=16: placements in board M 1518 / X 1012 (object 1518 / 1012)
ok   k=17: placements in board M 1518 / X 1012 (object 1518 / 1012)
ok   k=18: placements in board M 1656 / X 1104 (object 1656 / 1104)
ok   k=19: placements in board M 1800 / X 1200 (object 1800 / 1200)
ok   k=20: placements in board M 1800 / X 1200 (object 1800 / 1200)
ok   control: M-B (listed 2) has a common figure at k=2
ok   control: M-C (listed 6) has none at k=2
ok   k=2: 14 connected M-figures, 7 connected X-figures, 0 in common (no board limit)
ok   k=3: 261 connected M-figures, 100 connected X-figures, 0 in common (no board limit)
ok   k=4: 7509 connected M-figures, 2230 connected X-figures, 0 in common (no board limit)
PASS
```

## `KMAX=5 sh verify-it-yourself/run_checks.sh` (about 3.5 min), last lines
```
ok   k=3: 261 connected M-figures, 100 connected X-figures, 0 in common (no board limit)
ok   k=4: 7509 connected M-figures, 2230 connected X-figures, 0 in common (no board limit)
ok   k=5: 230145 connected M-figures, 51373 connected X-figures, 0 in common (no board limit)
PASS
```
