# Receipts (real output, 2026-11-02T09:58:17Z)

## sh verify-it-yourself/run_checks.sh
```
== 1. object/VALUE.txt: hash vs INDEX.csv and every pinned file
object/VALUE.txt sha256 matches INDEX.csv
35 pinned files checked
ok
== 2. saved outputs: graph counts (A000088, A001349), published a(1..9), A and B agree on a(10) = 46
A n=1 graphs=1 maxperiod=1 ok
A n=2 graphs=2 maxperiod=1 ok
A n=3 graphs=4 maxperiod=1 ok
A n=4 graphs=11 maxperiod=1 ok
A n=5 graphs=34 maxperiod=2 ok
A n=6 graphs=156 maxperiod=4 ok
A n=7 graphs=1044 maxperiod=8 ok
A n=8 graphs=12346 maxperiod=14 ok
A n=9 graphs=274668 maxperiod=27 ok
A n=10 graphs=12005168 maxperiod=46 ok
B order=1 connected_graphs=1 ok
B order=2 connected_graphs=1 ok
B order=3 connected_graphs=2 ok
B order=4 connected_graphs=6 ok
B order=5 connected_graphs=21 ok
B order=6 connected_graphs=112 ok
B order=7 connected_graphs=853 ok
B order=8 connected_graphs=11117 ok
B order=9 connected_graphs=261080 ok
B order=10 connected_graphs=11716571 ok
B combine a(1..10)=[1, 1, 1, 1, 2, 4, 8, 14, 27, 46] ok
ok
== 3. witness simulation from the definition (pure Python)
witness I?zUvYujw n=10 start=62 cycle_length=46 expected=46
ok
witness IEhffT{^w n=10 start=842 cycle_length=46 expected=46
ok
== 4. definition-level exhaustive check over all labelled graphs, n = 1..6 (no nauty)
n=1 labelled_graphs=1 max_period=1 oeis=1
n=2 labelled_graphs=2 max_period=1 oeis=1
n=3 labelled_graphs=8 max_period=1 oeis=1
n=4 labelled_graphs=64 max_period=1 oeis=1
n=5 labelled_graphs=1024 max_period=2 oeis=2
n=6 labelled_graphs=32768 max_period=4 oeis=4
ok
== 5. both C programs on the published optimal graphs and the witness (no nauty needed)
D]{ lifeA=2 lifeB=2 expected=2 ok
E]yw lifeA=4 lifeB=4 expected=4 ok
FE~vw lifeA=8 lifeB=8 expected=8 ok
GEnvZ{ lifeA=14 lifeB=14 expected=14 ok
HCZJtzm lifeA=27 lifeB=27 expected=27 ok
I?zUvYujw lifeA=46 lifeB=46 expected=46 ok
IEhffT{^w lifeA=46 lifeB=46 expected=46 ok
summary: A384209(10) = 46 (witness I?zUvYujw from state 62)
PASS
```

## FULL=1 sh verify-it-yourself/run_checks.sh (geng from nauty 2.8.8 on PATH; steps 1-5 as above, then step 6)
```
== 6. FULL: Program A over all graphs on 10 vertices
graphs 12005168 max 46
summary: A384209(10) = 46 (witness I?zUvYujw from state 62)
PASS
```
