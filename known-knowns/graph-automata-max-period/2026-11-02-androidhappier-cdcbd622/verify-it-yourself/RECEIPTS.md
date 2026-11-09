# Receipts (real output, 2026-11-02T22:15:10Z)

## sh verify-it-yourself/run_checks.sh
```
== 1. object/VALUE.txt: hash vs INDEX.csv and every pinned file
object/VALUE.txt sha256 matches INDEX.csv
value line: ['value: 200'] INDEX value: 200 ok
25 pinned files checked; recorded but not shipped: tools/geng
ok
== 2. saved outputs: graph counts (A001349), published a(1..8), A and B agree graph by graph on a(9) = 200
n=1 A graphs=1 max=2  B graphs=1 max=2  A001349=1 OEIS=2 ok
n=2 A graphs=1 max=2  B graphs=1 max=2  A001349=1 OEIS=2 ok
n=3 A graphs=2 max=4  B graphs=2 max=4  A001349=2 OEIS=4 ok
n=4 A graphs=6 max=6  B graphs=6 max=6  A001349=6 OEIS=6 ok
n=5 A graphs=21 max=8  B graphs=21 max=8  A001349=21 OEIS=8 ok
n=6 A graphs=112 max=18  B graphs=112 max=18  A001349=112 OEIS=18 ok
n=7 A graphs=853 max=42  B graphs=853 max=42  A001349=853 OEIS=42 ok
n=8 A graphs=11117 max=112  B graphs=11117 max=112  A001349=11117 OEIS=112 ok
part 0: A graphs=44686 max=159 | B graphs=44686 max=159 | per-graph lines identical=True | histograms consistent=True | witness H?`fMvu ok
part 1: A graphs=35236 max=174 | B graphs=35236 max=174 | per-graph lines identical=True | histograms consistent=True | witness H?rlu}~ ok
part 2: A graphs=38391 max=157 | B graphs=38391 max=157 | per-graph lines identical=True | histograms consistent=True | witness H?otRn~ ok
part 3: A graphs=18939 max=150 | B graphs=18939 max=150 | per-graph lines identical=True | histograms consistent=True | witness HQjVb^~ ok
part 4: A graphs=20847 max=181 | B graphs=20847 max=181 | per-graph lines identical=True | histograms consistent=True | witness HCOedZj ok
part 5: A graphs=12060 max=127 | B graphs=12060 max=127 | per-graph lines identical=True | histograms consistent=True | witness HCZelrl ok
part 6: A graphs=56096 max=198 | B graphs=56096 max=198 | per-graph lines identical=True | histograms consistent=True | witness HEjfayn ok
part 7: A graphs=34825 max=200 | B graphs=34825 max=200 | per-graph lines identical=True | histograms consistent=True | witness H?o|]|~ ok
n=9 total graphs A=261080 B=261080 (A001349(9)=261080); A and B per-graph maxima identical: True; max=200; graphs reaching it: ['H?o|]|~']; next best 198 on ['HEjfayn'] ok
A357952_9.txt states the value, witness and count: ok
A357952(1..9) from saved outputs: [2, 2, 4, 6, 8, 18, 42, 112, 200]
ok
== 3. witness simulation from the definition (pure Python, node counts itself)
witness H?o|]|~ n=9 edges=22 degrees=[3, 3, 3, 3, 6, 6, 6, 7, 7] connected=True rule={1,3,5} (self-counting) start=1 preperiod=0 cycle_length=200 expected=200
ok
witness H?o|]|~ n=9 edges=22 degrees=[3, 3, 3, 3, 6, 6, 6, 7, 7] connected=True rule={1,3,5,9} (self-counting) start=1 preperiod=0 cycle_length=200 expected=200
ok
graph H?o|]|~: max over all 1024 self-counting rules and 512 starts = 200 (first at rule {1,3,5}) expected=200
ok
== 4. definition-level exhaustive check, n = 1..6, from all labelled graphs (no nauty)
n=1 labelled_graphs=1 iso_classes=1 connected=1 (A001349=1) max_period=2 oeis=2 ok
n=2 labelled_graphs=2 iso_classes=2 connected=1 (A001349=1) max_period=2 oeis=2 ok
n=3 labelled_graphs=8 iso_classes=4 connected=2 (A001349=2) max_period=4 oeis=4 ok
n=4 labelled_graphs=64 iso_classes=11 connected=6 (A001349=6) max_period=6 oeis=6 ok
n=5 labelled_graphs=1024 iso_classes=34 connected=21 (A001349=21) max_period=8 oeis=8 ok
n=6 labelled_graphs=32768 iso_classes=156 connected=112 (A001349=112) max_period=18 oeis=18 ok
ok
== 5. saved optimal graphs n = 1..8, the OEIS examples n = 7, 8 and the n = 9 witness: pure Python, C and Go
@ python=2 totA=2 totB=2 expected=2 ok
A_ python=2 totA=2 totB=2 expected=2 ok
BW python=4 totA=4 totB=4 expected=4 ok
CU python=6 totA=6 totB=6 expected=6 ok
DCw python=8 totA=8 totB=8 expected=8 ok
EEjo python=18 totA=18 totB=18 expected=18 ok
FCrfw python=42 totA=42 totB=42 expected=42 ok
G?bevw python=112 totA=112 totB=112 expected=112 ok
F@Unw python=42 totA=42 totB=42 expected=42 ok
G?Dlvw python=112 totA=112 totB=112 expected=112 ok
H?o|]|~ python=200 totA=200 totB=200 expected=200 ok
summary: A357952(9) = 200 (witness H?o|]|~, rule {1,3,5}, start 1, node counted in its own sum)
PASS
```

## FULL=1 GENG=<nauty 2.8.8 geng> sh verify-it-yourself/run_checks.sh (8 cores, started 2026-11-02T21:59:28Z; steps 1-5 as above, then step 6; wall time 15 min 31 s)
```
== 6. FULL: Programs A and B over all connected graphs with 1..9 nodes
n = 1..8: fresh A and B outputs identical to saved
part 0: fresh A and B outputs identical to saved
part 1: fresh A and B outputs identical to saved
part 2: fresh A and B outputs identical to saved
part 3: fresh A and B outputs identical to saved
part 4: fresh A and B outputs identical to saved
part 5: fresh A and B outputs identical to saved
part 6: fresh A and B outputs identical to saved
part 7: fresh A and B outputs identical to saved
summary: A357952(9) = 200 (witness H?o|]|~, rule {1,3,5}, start 1, node counted in its own sum)
PASS
```
