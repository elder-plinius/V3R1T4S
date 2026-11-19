# Node-Kayles on 3 x n lattices, m x n grids, and generalized Petersen graphs GP(n,2): open outcomes and nimbers (OEIS A316632, A316533)

🕸️ **Graphs, games and automata** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-hours (canonical connected-component Sprague-Grundy DP with multi-word bitmasks and graph-isomorphism hashing) · open as of 2026-11-19

## The problem

Node-Kayles (a normal-play independent-set game) on a simple graph G is an impartial game in which two players alternately choose a vertex v in V(G) and delete its closed neighborhood N_G[v] = {v} union N_G(v); the last player to move wins. In 'Nimber Sequences of Node-Kayles Games' (Journal of Integer Sequences, Vol. 23, 2020, Article 20.3.5), Sierra Brown, Spencer Daugherty, Eugene Fiorini, Barbara Maldonado, Diego Manzano-Ruiz, Sean Rainville, Riley Waechter, and Tony W. H. Wong determined closed-form or periodic nimber sequences for 3-paths, 2 x n ladders (period 2), 4 x n lattices (identically 0 by the modulo-4 row involution Theorem 6), prism graphs, hypercubes, and several linked cycle/diamond families, and proved that for the m x n lattice graph L_{m x n}, G(L_{m x n}) = 0 whenever both m and n are even and G(L_{m x n}) > 0 whenever both m and n are odd (Theorem 5). OEIS A316632 (updated 2026-11-15 with b316632.txt to n = 34) now lists n = 1..34 (2, 1, 1, 0, 3, 3, 2, 2, 2, 3, 3, 5, 2, 4, 1, 3, 2, 2, 1, 1, 5, 0, 1, 1, 3, 0, 2, 5, 1, 0, 2, 6, 1, 5; Brown et al. n = 1..13, Max Fan n = 14..16, Alex Towell n = 17, and Xinyu Miao n = 18..34 from yuzhouren2000/nodekayles, after tavisrudd/othello commit 39fd65b6b1c7 on 2026-07-05 earlier gave n = 18..22), while OEIS A316533 remains at n = 5..26 (1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0; even n are 0 by Theorem 12 and odd n lie in {0,1,2}), both with keyword 'more'. In addition, yuzhouren2000/nodekayles (commits 0f684257c348 on 2026-10-15T23:48Z and b8e1253a3217 on 2026-10-17, data/grid_values.csv) resolved 8 of the 12 open Brown et al. Table 1 cells (L_{5 x 8} = 0, L_{6 x 7} = 3, L_{5 x 10} = 1, L_{6 x 9} = 5, L_{7 x 8} = 0, L_{5 x 9} = 4, L_{7 x 7} = 1, L_{7 x 9} = 2). As of 2026-11-19, the remaining open targets are: (1) OEIS A316632 for n >= 35; (2) OEIS A316533 for n >= 27 (odd n = 27, 29, 31, ...); and (3) the remaining 4 open cells of Brown et al. Table 1 (odd-by-even outcome/nimber cells L_{7 x 10}, L_{8 x 9}, L_{9 x 10} and odd-by-odd exact nimber cell L_{9 x 9}, where G > 0 is already proved by Theorem 5).

## What counts as a win

CONFIRMED: (1) the next 12 contiguous indexed terms of OEIS A316533 (G(GP(n,2)) for n = 27..38, comprising the 6 unknown odd indices n = 27, 29, 31, 33, 35, 37 and the 6 even indices which equal 0 by Theorem 12) OR the next 5 contiguous exact terms of OEIS A316632 beyond yuzhouren2000/nodekayles (G(L_{3 x n}) for n = 35..39), OR (2) at least 2 of the 4 remaining open cells of Brown et al.'s Table 1, consisting of exact Sprague-Grundy nimbers (or certified 1st/2nd-player outcomes) for unknown-outcome odd-by-even grids in {L_{7 x 10}, L_{8 x 9}, L_{9 x 10}} and/or the exact Sprague-Grundy nimber for L_{9 x 9} (an outcome-only claim does not count for L_{9 x 9} since Theorem 5 already proves G > 0). All claimed values must be computed by two independently written solvers using distinct algorithms that both reproduce every shaded (published) entry in Table 1 of Brown et al. (2020) (including G(L_{5 x 7}) = 2), the 8 Table 1 cells published in yuzhouren2000/nodekayles (L_{5 x 8}=0, L_{6 x 7}=3, L_{5 x 10}=1, L_{6 x 9}=5, L_{7 x 8}=0, L_{5 x 9}=4, L_{7 x 7}=1, L_{7 x 9}=2), all 34 published terms of A316632 (OEIS n = 1..34 / yuzhouren2000/nodekayles), and all published terms of A316533 (n = 5..26).

## Partial wins

- **p1:** Extend OEIS A316533 (Node-Kayles on GP(n,2)) contiguously through n = 32 (including odd n = 27, 29, 31) OR extend OEIS A316632 (Node-Kayles on the 3 x n lattice) contiguously beyond n = 34 through n = 37 (n = 35, 36, 37), verified by two independent Sprague-Grundy solvers that reproduce all published terms.
- **p2:** Settle the 1st/2nd-player outcome (or exact nimber) of at least one of the 3 remaining open odd-by-even cells in Brown et al. Table 1 (L_{7 x 10}, L_{8 x 9}, or L_{9 x 10}) OR determine the exact Sprague-Grundy nimber of L_{9 x 9}, verified by two independent solvers that reproduce all published cells of Table 1 and yuzhouren2000/nodekayles.

## How a win is checked

Verify with two independent Sprague-Grundy / heap-sum alpha-beta engines from scratch: (1) a connected-component mex engine using 128-bit (multi-word) bitmask neighborhood deletion and canonical graph/frontier hashing, and (2) an independent transfer-profile or heap-sum alpha-beta solver (`G + Nim(k)`). Both must first reproduce all 34 published terms of A316632 (OEIS n = 1..34 / yuzhouren2000/nodekayles), all 22 terms of A316533 (n = 5..26), all shaded entries of Table 1 in Brown et al. (2020), and all 8 Table 1 cells in yuzhouren2000/nodekayles, and agree on every new term or cell. Keep all package files <= 1 MB (kit/SUBMIT.md).

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://oeis.org/A316632>

## Sources

- <https://cs.uwaterloo.ca/journals/JIS/VOL23/Wong/wong24.pdf>
- <https://oeis.org/A316632>
- <https://oeis.org/A316533>
- <https://oeis.org/A316632/a316632_1.txt>
- <https://oeis.org/A316533/a316533.txt>
- <https://github.com/yuzhouren2000/nodekayles>
- <https://github.com/tavisrudd/othello>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- In both L_{3 x n} and GP(n,2), deleting a closed neighborhood N[v] frequently disconnects the graph into smaller components whose Sprague-Grundy values XOR together (`G(H union K) = G(H) xor G(K)`). The reference Python scripts linked on OEIS (`a316632_1.txt` and `a316533.txt`) used NetworkX `is_isomorphic` in a linear loop over all seen graphs; replacing NetworkX with a 128-bit bitmask + canonical column-profile hash eliminates the linear isomorphism scan.
- On L_{3 x n} (and GP(n,2) after the first move, which breaks the cycles at v into a bounded-pathwidth strip), the nimber of any residual subgraph can be memoized by its canonical column frontier profile.
- For GP(n,2) with odd n, the initial graph is vertex-transitive on the outer cycle and on the inner cycle, so there are only 2 non-isomorphic opening moves (one outer vertex u_0, one inner vertex v_0). Thus G(GP(n,2)) = mex({G(GP(n,2)_{u_0}), G(GP(n,2)_{v_0})}) <= 2, reducing each odd n to just two bounded-pathwidth residual subproblems.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Prior art beyond Brown et al. (2020): tavisrudd/othello (2026-07-05) published A316632(18..22), yuzhouren2000/nodekayles (2026-10-15/17) published A316632(18..34) and 8 of the 12 open Table 1 cells (L_{5 x 8}, L_{6 x 7}, L_{5 x 10}, L_{6 x 9}, L_{7 x 8}, L_{5 x 9}, L_{7 x 7}, L_{7 x 9}), and OEIS A316632 was updated on 2026-11-15 to list all 34 terms (n = 1..34). Recomputing any of those is calibration only, not a new result.
- Use 128-bit (two uint64_t words) or arbitrary-width bitmasks rather than a single 64-bit integer, since L_{3 x 35+} and GP(33,2) exceed 64 vertices and Table 1 grids reach 90 vertices.
- In GP(n,2), the inner vertices v_i are connected to v_{(i+2) mod n}; for odd n this forms a single n-cycle, whereas for even n it forms two (n/2)-cycles.
- In Table 1 of Brown et al. (2020), G(L_{5 x 7}) = 2 is already shaded/solved, and all odd-by-odd grids already have known 1st-player win outcome (G > 0 by Theorem 5); for L_{9 x 9} only the exact nimber is open.
- Always decompose into connected components after each move and XOR their nimbers before taking mex; failing to split disconnected components makes the state space exponential.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/graphs-games-automata/node-kayles-lattices-petersen-a316632-a316533.md
```

Already set up? Say `run V3R1T4S on node-kayles-lattices-petersen-a316632-a316533`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `node-kayles-lattices-petersen-a316632-a316533`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
