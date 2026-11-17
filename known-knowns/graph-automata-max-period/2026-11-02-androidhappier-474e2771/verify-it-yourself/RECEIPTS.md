# Receipts (real output, 2026-11-02T21:13:29Z)

## sh verify-it-yourself/run_checks.sh
```
== 1. object/VALUE.txt: hash vs INDEX.csv and every pinned file
object/VALUE.txt sha256 matches INDEX.csv
value line: ['value: 180'] INDEX value: 180 ok
24 pinned files checked; recorded but not shipped: tools/geng
ok
== 2. saved outputs: graph counts (A001349), published a(1..8), A and B agree on a(9) = 180
n=1 A graphs=1 max=1  B graphs=1 max=1  A001349=1 OEIS=1 ok
n=2 A graphs=1 max=2  B graphs=1 max=2  A001349=1 OEIS=2 ok
n=3 A graphs=2 max=2  B graphs=2 max=2  A001349=2 OEIS=2 ok
n=4 A graphs=6 max=6  B graphs=6 max=6  A001349=6 OEIS=6 ok
n=5 A graphs=21 max=7  B graphs=21 max=7  A001349=21 OEIS=7 ok
n=6 A graphs=112 max=18  B graphs=112 max=18  A001349=112 OEIS=18 ok
n=7 A graphs=853 max=38  B graphs=853 max=38  A001349=853 OEIS=38 ok
n=8 A graphs=11117 max=96  B graphs=11117 max=96  A001349=11117 OEIS=96 ok
part 0: A graphs=44686 max=120 | B graphs=44686 max=120 | witness H?`cuRU ok
part 1: A graphs=35236 max=135 | B graphs=35236 max=135 | witness HCrRRe{ ok
part 2: A graphs=38391 max=136 | B graphs=38391 max=136 | witness HQyuvh} ok
part 3: A graphs=18939 max=115 | B graphs=18939 max=115 | witness H?red^} ok
part 4: A graphs=20847 max=135 | B graphs=20847 max=135 | witness H?bN@rt ok
part 5: A graphs=12060 max=112 | B graphs=12060 max=112 | witness HEnb~r] ok
part 6: A graphs=56096 max=180 | B graphs=56096 max=180 | witness H?`DBbS ok
part 7: A graphs=34825 max=142 | B graphs=34825 max=142 | witness HCQUVpv ok
n=9 total graphs A=261080 B=261080 (A001349(9)=261080); max A=180 B=180; graphs reaching 180: 1 ok
merged summaries consistent with parts: ok
witness from saved outputs: H?`DBbS A rule_mask=5 state=175; B rule_mask=5 state=2
A357953(1..9) from saved outputs: [1, 2, 2, 6, 7, 18, 38, 96, 180]
ok
== 3. witness simulation from the definition (pure Python)
witness H?`DBbS n=9 edges=11 connected=True rule={0,2} start=175 preperiod=0 cycle_length=180 expected=180
ok
start 2 lies on the cycle through start 175: True (orbit size 180)
ok
graph H?`DBbS: max over all 512 rules and 512 starts = 180 (first at rule {0,2}) expected=180
ok
== 4. definition-level exhaustive check, n = 1..6, from all labelled graphs (no nauty)
n=1 labelled_graphs=1 iso_classes=1 connected=1 (A001349=1) max_period=1 oeis=1 ok
n=2 labelled_graphs=2 iso_classes=2 connected=1 (A001349=1) max_period=2 oeis=2 ok
n=3 labelled_graphs=8 iso_classes=4 connected=2 (A001349=2) max_period=2 oeis=2 ok
n=4 labelled_graphs=64 iso_classes=11 connected=6 (A001349=6) max_period=6 oeis=6 ok
n=5 labelled_graphs=1024 iso_classes=34 connected=21 (A001349=21) max_period=7 oeis=7 ok
n=6 labelled_graphs=32768 iso_classes=156 connected=112 (A001349=112) max_period=18 oeis=18 ok
ok
== 5. the saved optimal graphs for n = 1..8 and the n = 9 witness, pure Python and both C programs
@ python=1 totA=1 totB=1 expected=1 ok
A_ python=2 totA=2 totB=2 expected=2 ok
BW python=2 totA=2 totB=2 expected=2 ok
CU python=6 totA=6 totB=6 expected=6 ok
D]w python=7 totA=7 totB=7 expected=7 ok
ECrw python=18 totA=18 totB=18 expected=18 ok
FQzuo python=38 totA=38 totB=38 expected=38 ok
GCz^nw python=96 totA=96 totB=96 expected=96 ok
H?`DBbS python=180 totA=180 totB=180 expected=180 ok
summary: A357953(9) = 180 (witness H?`DBbS, rule {0,2}, start 175)
PASS
```

## FULL=1 GENG=<nauty 2.8.8 geng> sh verify-it-yourself/run_checks.sh (8 cores; steps 1-5 as above, then step 6; wall time 6 min 10 s)
```
== 6. FULL: Programs A and B over all connected graphs with 9 nodes
part 0: fresh A and B outputs identical to saved
part 1: fresh A and B outputs identical to saved
part 2: fresh A and B outputs identical to saved
part 3: fresh A and B outputs identical to saved
part 4: fresh A and B outputs identical to saved
part 5: fresh A and B outputs identical to saved
part 6: fresh A and B outputs identical to saved
part 7: fresh A and B outputs identical to saved
summary: A357953(9) = 180 (witness H?`DBbS, rule {0,2}, start 175)
PASS
```
