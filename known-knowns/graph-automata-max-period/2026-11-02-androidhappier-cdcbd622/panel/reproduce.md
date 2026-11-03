# REPRODUCE panel — A357952(9) = 200

context: subagent (reproduce skeptic, isolated claim copy)

Inputs read: claim/ only (claim.md, table_record.md, REPRODUCE.md, data/A357952.txt, result/*, tools/geng).
I looked at the author's code only after my checker had produced its full n=9 result.

## Definition (quoted from claim/data/A357952.txt, OEIS A357952)
"Maximum period of a totalistic cellular automaton on a connected graph with n nodes (counting the state of the
updated node itself)." "Each node can be in one of two states, ON or OFF. The automaton is totalistic, meaning that the
state of a node in the next generation depends only on the number of ON-nodes among its neighbors and itself. ...
a(n) is the maximum of the length of that cycle, over all connected graphs with n nodes, all totalistic updating rules,
and all initial states." Rule convention (%e): "a set of integers, specifying how many of the neighbors of a node and
the node itself must be ON for the node to be ON in the next generation".
So the class is self-counting: R ⊆ {0..n}, 2^(n+1) rules (1024 at n=9). This is not the neighbours-only A357953 class.

## My own checker (helpers: [scratch]/chk.c, wit.py), written from the definition before I opened code/
- I parse graph6 myself. For every state s and node v, c = popcount(s & (N(v) ∪ {v})). I build disjoint masks
  M_k(s) = {v : c_v(s) = k}, so next_R(s) = OR over k in R of M_k(s).
- The 2^(n+1) rules are visited in Gray-code order, and each rule changes next[] by one XOR with M_k. The author's
  totA uses a per-node count table. My method is different.
- Max cycle over all 2^n starts uses functional-graph cycle detection with per-walk stamps. It is exhaustive and
  does no sampling.
- The witness is checked separately by wit.py, a naive Python stepper that is also my own.

## Results
| check | result |
|---|---|
| tools/geng sha256 | 75d1bf01…91f450, matches claim.md |
| n=1..8 (geng -cq n) | 2,2,4,6,8,18,42,112, matching OEIS DATA; graph counts 1,1,2,6,21,112,853,11117 |
| n=9 full run (geng -cq 9 r/8, r=0..7, all 1024 rules × 512 starts) | max = 200; graphs = 44686+35236+38391+18939+20847+12060+56096+34825 = 261080 = A001349(9); 261080 unique graph6 strings |
| graphs reaching 200 | exactly one: H?o\|]\|~ (next best: 198, then 183, 181, 174) |
| my per-graph maxima vs saved result/A9_part* | identical (cmp on sorted 261080 lines) |
| saved A vs saved B per-graph lines | identical (cmp) |
| my histogram vs saved A histogram (summed over parts) | identical |
| witness H?o\|]\|~, rule {1,3,5}, start 1 (naive stepper) | preperiod 0, period 200, start lies on the cycle; degrees [3,3,3,3,6,6,6,7,7], connected |
| rule {1,3,5,9}, start 1 | also period 200 (consistent with the claim's note) |
| determinism | parts 3/8 and 7/8 re-run, output byte-identical |
| n=1..8 saved A_n1_8 / B_n1_8 | both report 2,2,4,6,8,18,42,112 |

The OEIS entry at claim time (data/A357952.txt, #12) has DATA up to a(8)=112 and no a(9). The draft has no pending
changes (per table_record.md; I did not re-fetch it live).

After my run I glanced at code/totA.c. It uses closed-neighbourhood counts in `self` mode with K=n+1, which matches
the definition. I did not need it for verification.

No mismatch, missing object or non-determinism found.

pass: true
