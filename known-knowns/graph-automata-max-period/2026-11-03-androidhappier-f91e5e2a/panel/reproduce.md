# Reproduce skeptic: A357953(10) = 624

context: subagent (executor Task)
date: 2026-11-03, 06:54–08:16 EST
claim copy examined: panel0423-reproduce/ (a byte copy of claim/). Scratch dir: rep0423/ (box workspace). All paths below are relative to one of these two.

## Definition used (OEIS A357953, quoted from claim data/A357953.txt, read before any author code)
"Maximum period of a totalistic cellular automaton on a connected graph with n nodes (not counting the state of the updated node itself)." ... "the state of a node in the next generation depends only on the number of ON-nodes among its neighbors ... a(n) is the maximum of the length of that cycle, over all connected graphs with n nodes, all totalistic updating rules, and all initial states."

## Independent checker (written before reading code/A or code/B)
- rep0423/mychk.c (sha256 8860094ec7cda13edc5ac9fac50bded49e373dbeda24802a9957bc78adaf4be6): reads graph6 and parses it myself. Next state: v is ON iff popcount(N(v) & s) is in R. Only neighbours are counted; v's own bit is never added. Rules: all subsets of {0..maxdeg}. This loses nothing because a count at v is at most deg(v) <= maxdeg, so bits of R above maxdeg never act. All 2^n starts. Cycle length comes from a stamp+index walk over the whole functional graph, using 64-bit stamps. I fixed a uint32 overflow risk in my own first draft before any n=10 run.
- `-sim` mode: a separate naive direct simulation. It stores the trajectory until the first repeat, then re-walks the cycle to confirm its length.
- rep0423/mychk2.c (sha256 d268f1b1…0c4b, binary mychk2 56ad1817…771a): the same checker, but it walks rules in Gray-code order (nx[s] ^= M_k[s]). Its output is identical to mychk on n=1..9 and on geng -cq 10 0/512 (3102 graphs, `diff` empty).
- geng: claim tools/geng and the box's tools/bin/geng are the same binary, nauty 2.8.8, sha256 75d1bf016a93b090ca471254605b735865162a864e4682c544df90a81e91f450.

## Results
1. Small orders, my checker, all rules and all starts: a(1..8) = 1,2,2,6,7,18,38,96 (graph counts 1,1,2,6,21,112,853,11117, which match A001349). These equal the OEIS DATA. a(9) = 180, reached only by H?`DBbS (261080 graphs = A001349(9)). mychk and mychk2 give identical n=9 output (rep0423/n9.txt, n9g.txt).
2. Witness, naive simulation: `mychk -sim 'I?AAD@oIg' 0,2 2` gives preperiod 0, cycle_length 624, recheck_cycle 624. The graph has 10 nodes and 11 edges, is connected (checked by a separate Python BFS), and has degrees [2,2,3,1,1,1,2,2,4,4]. The author's code/stepper.py gives the same 624. The runners-up also check out: ICQfRh|z_ with {0,2,4} from start 0 gives 470, and I?B@mRgno with {0,2,4,5} from start 5 gives 429.
3. **Full n=10 run with my own checker** (rep0423/run10.sh): `geng -cq 10 r/32 | mychk2 150` for r = 0..31, 5 jobs at a time, nice 19, from 06:59 to about 08:10 EST. All 32 outputs are complete (each has a count= line). Outputs are in rep0423/out10/M10_r*of32.txt.
   - total graphs **11716571 = A001349(10)**
   - global max **624**, in residue class 7 only, on graph **I?AAD@oIg** with rule mask 5 = {0,2}. It is the only graph at 624; the next values are 470, 464, 429, 413, 410.
   - 106581 graphs have a per-graph max of at least 150.
4. Comparison with the author's saved outputs (rep0423/cmp.py, my own comparator, not code/compare_AB.py; output in rep0423/cmp_out.txt):
   - For all 32 of 32 classes, my graph count, max, full histogram of per-graph maxima, and full list of (graph6, max) for max >= 150 are identical to result/A10_r*of32.txt.
   - Saved A and saved B agree class by class on all of these fields.
   - Mismatching classes: 0.
5. Program B spot rebuild: I built code/B/main.go fresh (`go build`) and reran it on the witness class `geng -cq 10 7/32 | totBgo nbr 150` (07:01–07:46 EST). Its output is byte-identical to result/B10_r7of32.txt (sha256 3efa1abd…047, which is also the sha of A10_r7of32.txt). That output says graphs=358450, maxperiod=624, witness I?AAD@oIg, mask 5, state 2.
6. Fresh builds of A (totF.c) and B reproduce a(1..8) = 1,2,2,6,7,18,38,96 with the matching graph counts.
7. Integrity: all 81 sha256 entries in VALUE.txt verify against the files.
8. Determinism: the fresh B rerun on r7 is byte-identical to the saved file, and my exhaustive run matches A's saved outputs in every class. I found no non-determinism.

## Notes (do not affect the verdict)
- The OEIS n = 8 example string 'G?CidW' with rule {0,2,4} reaches only period 10 under the standard graph6 decoding. Its complement, G~zTYc, reaches 96. So the OEIS example string looks like it encodes the complement graph. The claim uses its own n = 8 witness, GCz^nw, which gives 96. The OEIS n = 7 example FJe~O with {0,2} does give 38.
- Independence: my checker was written from the definition alone. Its Gray-code/XOR rule walk turns out to resemble Program A's design, but the source was written separately and the results also agree with B, which uses a different design (binary rule order and Kahn peeling).
- I killed no other jobs.

## Verdict
An independent exhaustive recompute over all 11716571 connected graphs on 10 nodes, all relevant rules, and all 1024 starts gives A357953(10) = 624. The witness I?AAD@oIg, R = {0,2}, start 2 has cycle length 624 under direct simulation. a(1..9) reproduce. My results match the saved A and B outputs in all 32 classes, and the B rebuild for class 7 is byte-identical to the saved output.

pass: true
