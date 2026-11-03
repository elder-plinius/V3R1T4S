# Receipts (real output, 2026-11-03T04:42:08Z)

## sh verify-it-yourself/run_checks.sh
```
== 1. object/VALUE.txt: hash vs INDEX.csv and every pinned file
object/VALUE.txt sha256 matches INDEX.csv
value line: ['value: 150'] INDEX value: 150 ok
26 pinned files checked; recorded but not shipped: tools/geng
ok
== 2. saved outputs: graph counts (A001349), published a(1..7), A and B agree graph by graph on a(8) = 150
n=1 A graphs=1 max=2  B graphs=1 max=2  A001349=1 OEIS=2 ok
n=2 A graphs=1 max=2  B graphs=1 max=2  A001349=1 OEIS=2 ok
n=3 A graphs=2 max=4  B graphs=2 max=4  A001349=2 OEIS=4 ok
n=4 A graphs=6 max=6  B graphs=6 max=6  A001349=6 OEIS=6 ok
n=5 A graphs=21 max=16  B graphs=21 max=16  A001349=21 OEIS=16 ok
n=6 A graphs=112 max=26  B graphs=112 max=26  A001349=112 OEIS=26 ok
n=7 A graphs=853 max=66  B graphs=853 max=66  A001349=853 OEIS=66 ok
part 0: A graphs=924 max=78 | B graphs=924 max=78 | per-graph lines identical=True | histograms consistent=True | witness GEnffs ok
part 1: A graphs=2268 max=112 | B graphs=2268 max=112 | per-graph lines identical=True | histograms consistent=True | witness G?bevw ok
part 2: A graphs=2141 max=124 | B graphs=2141 max=124 | per-graph lines identical=True | histograms consistent=True | witness G?rfUw ok
part 3: A graphs=273 max=68 | B graphs=273 max=68 | per-graph lines identical=True | histograms consistent=True | witness G?z\~w ok
part 4: A graphs=97 max=68 | B graphs=97 max=68 | per-graph lines identical=True | histograms consistent=True | witness GErtv{ ok
part 5: A graphs=2562 max=150 | B graphs=2562 max=150 | per-graph lines identical=True | histograms consistent=True | witness GCQfBg ok
part 6: A graphs=1473 max=114 | B graphs=1473 max=114 | per-graph lines identical=True | histograms consistent=True | witness GCrmt{ ok
part 7: A graphs=1379 max=107 | B graphs=1379 max=107 | per-graph lines identical=True | histograms consistent=True | witness GCZK}s ok
n=8 total graphs A=11117 B=11117 (A001349(8)=11117); A and B per-graph maxima identical: True; max=150; graphs reaching it: ['GCQfBg']; next best 124 on ['G?rfUw'] ok
A357951_8.txt states the value, witness and count: ok
completeness.txt: geng count, labelg-distinct count and A001349(8) all 11117: ok
A357951(1..8) from saved outputs: [2, 2, 4, 6, 16, 26, 66, 150]
ok
== 3. witness simulation from the definition (pure Python, outer-totalistic: own state + number of ON neighbours)
witness GCQfBg n=8 edges=11 degrees=[1, 2, 3, 3, 3, 3, 3, 4] connected=True B=[0, 2] S=[1, 3, 4] (outer-totalistic, node not counted) start=1 transient=0 cycle_length=150 expected=150
ok
graph GCQfBg: max over 65536 rules (all counts 0..n-1) and 256 starts = 150 (first at B=[0, 2, 7] S=[1, 3, 4]) expected=150
ok
graph G?rfUw: max over 4096 rules (counts 0..maxdeg, complete) and 256 starts = 124 (first at B=[0, 1, 3, 4, 5] S=[2]) expected=124
ok
witness FBjng n=7 edges=13 degrees=[3, 3, 3, 3, 4, 5, 5] connected=True B=[0, 1, 3] S=[2, 4, 5] (outer-totalistic, node not counted) start=1 transient=0 cycle_length=66 expected=66
ok
== 4. definition-level exhaustive check, n = 1..6, from all labelled graphs (no nauty)
n=1 labelled_graphs=1 iso_classes=1 connected=1 (A001349=1) max_period=2 oeis=2 ok
n=2 labelled_graphs=2 iso_classes=2 connected=1 (A001349=1) max_period=2 oeis=2 ok
n=3 labelled_graphs=8 iso_classes=4 connected=2 (A001349=2) max_period=4 oeis=4 ok
n=4 labelled_graphs=64 iso_classes=11 connected=6 (A001349=6) max_period=6 oeis=6 ok
n=5 labelled_graphs=1024 iso_classes=34 connected=21 (A001349=21) max_period=16 oeis=16 ok
n=6 labelled_graphs=32768 iso_classes=156 connected=112 (A001349=112) max_period=26 oeis=26 ok
ok
== 5. saved optimal graphs n = 1..7, the OEIS n = 7 example, the n = 8 witness and runner-up: pure Python, C and Go
@ python=2 otA=2 otB=2 expected=2 ok
A_ python=2 otA=2 otB=2 expected=2 ok
BW python=4 otA=4 otB=4 expected=4 ok
CU python=6 otA=6 otB=6 expected=6 ok
DUw python=16 otA=16 otB=16 expected=16 ok
EQzW python=26 otA=26 otB=26 expected=26 ok
FEjvW python=66 otA=66 otB=66 expected=66 ok
FBjng python=66 otA=66 otB=66 expected=66 ok
G?rfUw python=124 otA=124 otB=124 expected=124 ok
GCQfBg python=150 otA=150 otB=150 expected=150 ok
summary: A357951(8) = 150 (witness GCQfBg, rule B={0,2} S={1,3,4}, start 1, outer-totalistic)
PASS
```

## FULL=1 GENG=[nauty 2.8.8 geng] sh verify-it-yourself/run_checks.sh (8 cores shared with other jobs, started 2026-11-03T04:33:01Z; steps 1-5 as above, then step 6; wall time 5m55.164s)
```
== 6. FULL: Programs A and B over all connected graphs with 1..8 nodes
n = 1..7: fresh A and B outputs identical to saved
part 0: fresh A and B outputs identical to saved
part 1: fresh A and B outputs identical to saved
part 2: fresh A and B outputs identical to saved
part 3: fresh A and B outputs identical to saved
part 4: fresh A and B outputs identical to saved
part 5: fresh A and B outputs identical to saved
part 6: fresh A and B outputs identical to saved
part 7: fresh A and B outputs identical to saved
summary: A357951(8) = 150 (witness GCQfBg, rule B={0,2} S={1,3,4}, start 1, outer-totalistic)
PASS
```
