# REPRODUCE skeptic: A357951(8) = 150

context: subagent (reproduce skeptic, isolated claim copy)

Worked only from a private copy of `claim/`. I did not read attempts/, NOTES, REPORT, LOG, dossier or other panelists. I wrote my own checker before opening `code/otA.c` or `code/otB.go`.

## Definition (quoted from claim data, data/A357951.txt)
"Maximum period of an outer totalistic cellular automaton on a connected graph with n nodes."
"Each node can be in one of two states, ON or OFF. The automaton is outer totalistic, meaning that the state of a node in the next generation depends only on the state of that node and the number of ON-nodes among its neighbors. Since there are finitely many states of the automaton, it will eventually enter a cycle. a(n) is the maximum of the length of that cycle, over all connected graphs with n nodes, all outer totalistic updating rules, and all initial states."
Rule convention (%e): "two sets of integers, where the first (second) set specifies how many neighbors must be ON for an OFF-node (ON-node) to turn (stay) ON."
Listed terms: %S 2,2,4,6,16,26,66 (n = 1..7).

## My checker (written from the definition, before reading the author's code)
- `rc.c` (C): decodes graph6 itself. A rule is 2n bits: bit c means c is in B and bit n+c means c is in S. For each rule it builds the successor map over all 2^n states, where node v's next bit is the rule bit at index (own state)*n + (#ON neighbours). It then finds every eventual cycle in that functional graph by walking from each unvisited start with a per-walk stamp and step position. The cycle length is step - pos[repeat].
- Two modes:
  - `full`: all 2^(2n) rules, no pruning.
  - default: only the counts 0..maxdeg. Counts above maxdeg are never consulted, so those rules have identical dynamics.
  Both modes were run exhaustively at n = 8 and gave byte-identical output.
- `iso.c` (C), an independent completeness check: for each graph from geng it tests connectivity by BFS. It computes its own canonical form as the minimum edge code over all 8! = 40320 vertex permutations, then counts distinct classes.
- `wit.py` (pure Python, separate code): a direct node-by-node simulator from a start state, giving the transient and cycle length.

## Results
| Check | Expected | Observed | OK |
|---|---|---|---|
| tools/geng sha256 | 75d1bf01...f450 (claim.md) | 75d1bf016a93b090ca471254605b735865162a864e4682c544df90a81e91f450 | yes |
| a(1..7), my checker (both modes) | 2,2,4,6,16,26,66 | 2,2,4,6,16,26,66 | yes |
| n=7 rule from my checker | OEIS {0,1,3},{2,4,5} | FEjvW, B={0,1,3}, S={2,4,5} | yes |
| OEIS n=7 example FBjng, start node 0 or node 1 ON (wit.py) | 66 | cycle 66, transient 0 | yes |
| n=8 graph count (geng -cq 8, 8 parts) | A001349(8) = 11117 | 11117 | yes |
| n=8 completeness (iso.c) | 11117 connected, pairwise non-isomorphic | 11117, 0 disconnected, 0 duplicate classes | yes |
| n=8 full maximum, my checker (pruned and full 65536 rules) | 150 | 150 | yes |
| Unique optimum | GCQfBg only | only GCQfBg reaches 150; next values are 124, 115, 114, 112 | yes |
| My checker's optimal rule/state | B={0,2}, S={1,3,4} | mask 0x1a05 = B={0,2}, S={1,3,4}; cycle state 1 | yes |
| Witness simulation (wit.py): GCQfBg, B={0,2}, S={1,3,4}, start 1 (node 0 ON) | 150 | transient 0, cycle 150; graph connected, degrees 3,3,3,2,1,3,3,4 | yes |
| My per-graph values vs saved result/A8_part*.txt | 0 mismatches | 11117 graphs, 0 mismatches (concatenated lines byte-identical, sha256 f6e3184d...c404) | yes |
| My per-graph values vs saved result/B8_part*.txt | 0 mismatches | 11117 graphs, 0 mismatches | yes |
| A vs B agreement (saved and rerun) | identical | identical per-graph maxima, n=1..8 | yes |
| Rerun of otA (pg) and otB (-pg), n=8, 8 parts | byte-identical to saved | all 16 part files byte-identical (cmp); n=1..7 summaries 2,2,4,6,16,26,66 for both | yes |
| Determinism of my checker | identical reruns | two pruned runs + one full run byte-identical | yes |

Timings on 8 cores (approximate): my pruned run 1 min, my full run 4.4 min, otA 2.2 min, otB 3.3 min. These ran partly alongside other load.

## Notes
- The n = 8 enumeration is exhaustive, not a sample: every connected 8-node graph, every rule, every one of the 256 start states. My full mode covers all 65536 rules with no pruning.
- No mismatch, missing object or non-determinism was found.

pass: true
