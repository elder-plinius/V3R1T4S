# Receipts (real output, 2026-11-03T10:00:10Z)

## sh verify-it-yourself/run_checks.sh (x86-64 with BMI2, cc = gcc; no geng on PATH, FULL mode not run)
```
== 1. object/VALUE.txt: hash vs INDEX.csv and every pinned file
object/VALUE.txt sha256 matches INDEX.csv
value line: ['value: 71'] INDEX value: 71 ok
151 pinned files checked; recorded but not shipped: tools/geng
ok
== 2. saved outputs: graph counts (A000088, A001349), a(1..9) published, A and B agree on a(11) = 71
A n=1 graphs=1 maxperiod=1 ok
A n=2 graphs=2 maxperiod=1 ok
A n=3 graphs=4 maxperiod=1 ok
A n=4 graphs=11 maxperiod=1 ok
A n=5 graphs=34 maxperiod=2 ok
A n=6 graphs=156 maxperiod=4 ok
A n=7 graphs=1044 maxperiod=8 ok
A n=8 graphs=12346 maxperiod=14 ok
A n=9 graphs=274668 maxperiod=27 ok
A n=10 graphs=12005168 maxperiod=46 (reproduced, not claimed) ok
A n=11 residue files=64 summaries=64 ok
A n=11 graphs=1018997864 (A000088(11)=1018997864) connected=1006700565 (A001349(11)=1006700565) ok
A n=11 maxperiod=71, graphs reaching it=2 ok
A n=11 disconnected graphs: max per-graph period 46 ok
B order=1 connected_graphs=1 max_cycle=1 ok
B order=2 connected_graphs=1 max_cycle=1 ok
B order=3 connected_graphs=2 max_cycle=1 ok
B order=4 connected_graphs=6 max_cycle=1 ok
B order=5 connected_graphs=21 max_cycle=2 ok
B order=6 connected_graphs=112 max_cycle=4 ok
B order=7 connected_graphs=853 max_cycle=8 ok
B order=8 connected_graphs=11117 max_cycle=14 ok
B order=9 connected_graphs=261080 max_cycle=27 ok
B order=10 connected_graphs=11716571 max_cycle=46 ok
B order=11 connected_graphs=1006700565 max_cycle=71 ok
B order=11 parts=64 re-merged: graphs=1006700565, same periods and histogram as B_order11.txt ok
B combine (recomputed here) a(1..11)=[1, 1, 1, 1, 2, 4, 8, 14, 27, 46, 71] ok
B combine saved output matches ok
A connected histogram == B histogram (1006700565 graphs) ok
A and B: same connected graphs with max >= 40 (1718 / 1718) ok
A max 71 == B connected max 71 == B combine a(11) 71 ok
ok
== 3. witness simulation from the definition (pure Python)
witness J?qrdjivb}_ n=11 edges=31 start=752 preperiod=0 cycle_length=71 expected=71
ok
witness JCpbdo}ttv_ n=11 edges=31 start=1728 preperiod=0 cycle_length=71 expected=71
ok
graph J?qrdjivb}_ n=11 all 2048 starts: max cycle_length=71 expected=71
ok
graph JCpbdo}ttv_ n=11 all 2048 starts: max cycle_length=71 expected=71
ok
graph JCpbbqkVt^_ n=11 all 2048 starts: max cycle_length=61 expected=61
ok
== 4. definition-level exhaustive check over all labelled graphs, n = 1..6 (no nauty)
n=1 labelled_graphs=1 max_period=1 oeis=1
n=2 labelled_graphs=2 max_period=1 oeis=1
n=3 labelled_graphs=8 max_period=1 oeis=1
n=4 labelled_graphs=64 max_period=1 oeis=1
n=5 labelled_graphs=1024 max_period=2 oeis=2
n=6 labelled_graphs=32768 max_period=4 oeis=4
ok
== 5. both C programs on the published optimal graphs and the witnesses (no nauty needed)
D]{ lifeA=2 lifeB=2 expected=2 ok
E]yw lifeA=4 lifeB=4 expected=4 ok
FE~vw lifeA=8 lifeB=8 expected=8 ok
GEnvZ{ lifeA=14 lifeB=14 expected=14 ok
HCZJtzm lifeA=27 lifeB=27 expected=27 ok
I?zUvYujw lifeA=46 lifeB=46 expected=46 ok
J?qrdjivb}_ lifeA=71 lifeB=71 expected=71 ok
JCpbdo}ttv_ lifeA=71 lifeB=71 expected=71 ok
JCpbbqkVt^_ lifeA=61 lifeB=61 expected=61 ok
summary: A384209(11) = 71 (witness J?qrdjivb}_ from state 752)
PASS
```
