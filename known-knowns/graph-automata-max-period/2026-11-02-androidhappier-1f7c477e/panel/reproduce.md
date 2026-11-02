# REPRODUCE skeptic verdict: A384209(10) = 46

context: subagent (executor, reproduce)

I copied claim/ to my scratch copy and worked only there. I wrote nothing into claim/ and read nothing else under the v3r1t4s tree.

## 1. Own checker, written before reading code/*.c or code/*.py
Definition used (OEIS A384209, quoted from data/A384209.txt): "Maximum period for Game of Life on a simple graph with n
vertices. The usual rules of Game of Life apply: A live vertex lives on to the next generation only if it has 2 or 3
living neighbors. A dead vertex comes alive if it has exactly 3 living neighbors."

My program (mine.c, kept in my scratch copy, not in claim/) does the following:
- It decodes graph6 per the nauty spec: N(n) = first char - 63, then the upper triangle in column order (j=1..n-1, i=0..j-1), 6 bits per char, MSB first.
- Each step, a vertex is born or survives exactly as the definition says: next = (alive && cnt in {2,3}) || (!alive && cnt == 3), where cnt = popcount(state & adj[v]).
- It builds the full successor map on all 2^n states. It finds the cycles of that functional graph with a walk-and-stamp pass and takes the longest cycle as the period of the graph.
- Over the whole input it reports the maximum period and how many graphs reach it. A separate sim mode steps one start state directly.

## 2. Check on the published terms (tools/geng, sha256 75d1bf016a93b090ca471254605b735865162a864e4682c544df90a81e91f450)
```
n=1: graphs=1 maxperiod=1 attaining=1
n=2: graphs=2 maxperiod=1 attaining=2
n=3: graphs=4 maxperiod=1 attaining=4
n=4: graphs=11 maxperiod=1 attaining=11
n=5: graphs=34 maxperiod=2 attaining=1
n=6: graphs=156 maxperiod=4 attaining=1
n=7: graphs=1044 maxperiod=8 attaining=1
n=8: graphs=12346 maxperiod=14 attaining=1
n=9: graphs=274668 maxperiod=27 attaining=1
```
The values 1,1,1,1,2,4,8,14,27 match the published DATA. The graph counts match A000088(1..9). For n=5..9 exactly one graph reaches the maximum, which matches the OEIS comment that the optimal graph is unique.

Published optimal graphs, run one at a time (D]{, E]yw, FE~vw, GEnvZ{, HCZJtzm):
```
graphs=1 maxperiod=2 attaining=1
graphs=1 maxperiod=4 attaining=1
graphs=1 maxperiod=8 attaining=1
graphs=1 maxperiod=14 attaining=1
graphs=1 maxperiod=27 attaining=1
```

## 3. Exhaustive n = 10 with my program (all graphs, connected or not)
Run 1: `geng -q 10 r/4`, r = 0..3, at nice 15 with 4 processes:
```
graphs=3003652 maxperiod=38 attaining=1
graphs=2790736 maxperiod=46 attaining=1
graphs=3092500 maxperiod=46 attaining=1
graphs=3118280 maxperiod=33 attaining=2
best 46 I?zUvYujw cycstate 62
best 46 IEhffT{^w cycstate 842
```
The four counts sum to 12005168 (3003652+2790736+3092500+3118280 = 12005168), which equals A000088(10).

Run 2 used a different split, `geng -q 10 r/8`, r = 0..7, at nice 15 with at most 4 processes:
```
total=12005168 max=46 attaining=2
best 46 I?zUvYujw cycstate 62
best 46 IEhffT{^w cycstate 842
```
The two runs agree: maximum period 46, reached by exactly 2 of the 12005168 graphs (I?zUvYujw and IEhffT{^w).

My histogram of graphs by maximum period (period count):
```
1 3463579 2 5693002 3 910964 4 905687 5 226281 6 383232 7 147319 8 114543 9 63615 10 40779 11 16961 12 12347 13 6706 14 7738 15 3560 16 2991 17 1667 18 1284 19 761 20 771 21 272 22 417 23 140 24 210 25 79 26 60 27 92 28 40 29 13 30 23 31 12 32 7 33 4 34 3 35 3 38 2 39 1 44 1 46 2
```

## 4. Witness simulation (my stepper)
```
t=0 state=62
t=1 state=882
... (t=2..44 printed in full in my run, all distinct)
t=45 state=382
n=10 g6=I?zUvYujw start=62 preperiod=0 period=46
n=10 g6=IEhffT{^w start=842 preperiod=0 period=46
n=10 g6=IEhffT{^w start=47 preperiod=0 period=46
```
Note on my first sim attempt: it printed "n=52 ... period=1" because of an argv-indexing bug in my sim mode only (it decoded the word "sim" as the graph). I fixed the indexing, rebuilt, and the output above is from the fixed build. The exhaustive mode was not affected; it reads stdin, and its n=1..9 and published-graph checks are above.

## 5. Author's code and saved outputs
I read these only after steps 1-4.

- code/lifeA.c uses the same rule (c==3 || alive&&c==2, which is equivalent to the definition), the same graph6 decoding and the same stamp-walk cycle search. code/lifeB.c is a bit-sliced successor map with in-degree peeling, run on connected graphs only. code/combine.py takes the lcm over partitions, which is valid because a disjoint union evolves component by component. code/stepper.py is a pure-Python stepper.
- result/A_n1_9.txt matches my n=1..9 values and counts.
- result/A_n10_merged.txt reports "total_graphs 12005168 ... match" and "max_period (46, 'I?zUvYujw', '62')". Its graphs_by_max_period list is identical to my histogram:
```
author_hist == my_hist: True sum 12005168
```
- result/combine_n1_10.txt ends with "n=10 a(n)=46 connected_max=46"; result/B_order10.txt has "order=10 connected_graphs=11716571 max_cycle=46". Both agree with my result: the two 46-graphs are counted among connected graphs and no disconnected union exceeds 46.
- result/witness_simulation.txt gives cycle_length=46 for I?zUvYujw/62, I?zUvYujw/31, IEhffT{^w/842 and IEhffT{^w/47, which agrees with my stepper.

### Rebuild and rerun of Program A (gcc -O2, per REPRODUCE.md, at nice 15 with at most 4 processes)
For n=1..9 the output is identical to result/A_n1_9.txt (maxperiod 1 1 1 1 2 4 8 14 27). For n=10, run 1:
```
n=10 graphs=1309798 maxperiod=34 witness_graph6=ICR`~`x~_ witness_state=493
n=10 graphs=1382073 maxperiod=46 witness_graph6=I?zUvYujw witness_state=62
n=10 graphs=1426606 maxperiod=39 witness_graph6=ICRduvs]W witness_state=23
n=10 graphs=1714279 maxperiod=33 witness_graph6=ICXetiyxg witness_state=960
n=10 graphs=1693854 maxperiod=38 witness_graph6=I?`FUjy|W witness_state=721
n=10 graphs=1408663 maxperiod=34 witness_graph6=I?o~VaynO witness_state=39
n=10 graphs=1665894 maxperiod=46 witness_graph6=IEhffT{^w witness_state=842
n=10 graphs=1404001 maxperiod=32 witness_graph6=ICrfRi}|w witness_state=118
```
The part counts sum to 12005168. I ran the same 8 parts a second time to check determinism and compared the outputs byte for byte:
```
part 0 identical
part 1 identical
part 2 identical
part 3 identical
part 4 identical
part 5 identical
part 6 identical
part 7 identical
lifeA hist == my hist
```

### Program B, partial rerun
I rebuilt lifeB.c and ran it on connected orders 1..9. Every output is byte-identical to the saved file ("B_order1 identical to saved" ... "B_order9 identical to saved"). The connected counts are 1,1,2,6,21,112,853,11117,261080, which match A001349. I did not rerun lifeB for order 10. combine.py over the rebuilt orders 1..9 plus the saved result/B_order10.txt prints "n=10 a(n)=46 connected_max=46". Rerunning code/stepper.py on I?zUvYujw 62 gives "preperiod=0 cycle_length=46".

## Concern: geng is the only enumerator
Every exhaustive run here, mine and the author's, gets its graphs from the same tools/geng binary. The checks against it:
- geng's totals match A000088 for n=1..10 (n=10: `geng -u 10` prints ">Z 12005168 graphs generated") and A001349 for connected graphs (`geng -c -u 10` prints ">Z 11716571 graphs generated").
- Two different residue splits (r/4 and r/8) give identical totals, maximum and histogram.

geng promises its outputs are pairwise non-isomorphic. Given that, the correct count means every isomorphism class is covered. I did not test isomorphism independently (no labelg or second generator was available). This is a shared dependency, not an observed problem. Within that standard caveat, the enumeration is complete.

## Verdict
My own checker was written from the definition before I read the author's code. It ran exhaustively over all 12005168 graphs on 10 vertices with all 2^10 states, twice with different splits, and found a maximum period of 46, reached by exactly 2 graphs (I?zUvYujw, IEhffT{^w). The witness I?zUvYujw from state 62 has preperiod 0 and period 46. The author's Program A agrees with my per-period histogram exactly and is deterministic over two reruns. Program B's saved outputs and my partial rerun agree too. I found no mismatches, missing objects or non-determinism.

pass: true
