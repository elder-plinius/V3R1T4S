# Reversed Zeckendorf game: second-player winning starting numbers beyond n = 129 (OEIS A389618) and the Batterman et al. infinite P-position conjecture

🕸️ **Graphs, games and automata** · harvest (many cells or partial wins within reach) · tractability ★★★★☆ · compute: laptop-minutes to laptop-hours (the game graph for n has exactly A003107(n) vertices, every partition of n into Fibonacci parts being reachable: 384,715 at n = 129, 2,704,186 at n = 180 and 21,890,964 at n = 250; a topological retrograde pass avoids the O(|V|^2) list scans of the 2023 reference code) · open as of 2026-11-06

## The problem

The Reversed Zeckendorf Game, introduced by Z. X. Batterman, A. Jambhale, S. J. Miller, A. L. Narayanan, K. Sharma, A. K. Yang, and C. Yao ('The Reversed Zeckendorf Game', arXiv:2309.12748v2, 2023; Fibonacci Quarterly 63:2, 2025, 215-239) and catalogued by N. J. A. Sloane in OEIS A389617, A389618, and A389619 (December 2025), reverses the classical Zeckendorf game of Baird-Smith, Epstein, Flint, and Miller (2018). Indexing the Fibonacci numbers by F_1 = 1, F_2 = 2, F_3 = 3, F_4 = 5, ..., the game for a positive integer n >= 2 starts at the unique Zeckendorf decomposition of n into non-consecutive Fibonacci parts. Two players alternate moves under normal play (last player able to move wins), choosing either: (i) Split: replace one F_{i+1} with F_i + F_{i-1} for i >= 2, or replace one F_2 with 2 F_1; or (ii) Combine: replace F_{i-2} + F_{i+1} with 2 F_i for i > 2, or replace F_1 + F_3 with 2 F_2. The game terminates when all pieces are in the first bin (n copies of F_1). Batterman et al. proved constructively that Player 1 wins whenever n = F_{i+1} + F_{i-2} (Theorem 1.1) and solved starting positions restricted to {1, 2, 3} (Theorem 1.6), while posing Conjecture 1.2: Player 2 has a winning strategy for infinitely many n (and Conjecture 1.3: the limiting fraction of Player 1 wins is 1/phi ~ 0.618). Because the reference Python implementation in Appendix B of arXiv:2309.12748v2 used linear list membership (`if current_state in calculated_states`) and repeated full-graph scans (`while not_done`), their computation took about 2 hours at n = 129; Appendix B also mentions about 24 hours for n = 144, but no outcome beyond n = 129 is published. Table A1 of arXiv:2309.12748v2 publishes for all 2 <= n <= 129 the exact vertex counts, edge counts (A389617, offset n = 2, displayed on OEIS through its 64th term n = 65 with 68,351 edges and tabulated in Table A1 through n = 129 with 384,715 vertices and 2,945,040 edges), 49 second-player wins in 2 <= n <= 129 (A389618: 3, 5, 8, 9, 11, 13, 14, ..., 128, 129), and 79 first-player wins in 2 <= n <= 127 (A389619, which also prepends n = 1 as an 80th entry by OEIS cataloguing convention). The vertex count for n is A003107(n) (OEIS A389617 comment). As of 2026-11-06 (OEIS A389617-A389619 and an arXiv search), no outcomes or edge counts are published for any n >= 130, and Conjecture 1.2 remains open.

## What counts as a win

CONFIRMED: either (A) a kernel-checked formal proof (Lean, Rocq or Isabelle; no sorry, admitted goals or axioms beyond the system's standard ones) of Batterman et al. Conjecture 1.2 establishing that for infinitely many starting integers n >= 2, the initial Zeckendorf decomposition of n is a P-position (second-player win) under the Split and Combine rules; OR (B) the exact 1st/2nd-player outcomes of the Reversed Zeckendorf game for every integer n contiguously in 130..250 (yielding one table of outcomes, vertex counts, and edge counts for n = 130..250 that extends OEIS A389618, A389619, and A389617 through n = 250), computed by two independently written solvers using distinct representations that both reproduce every vertex count, edge count, and win/loss outcome in Table A1 of arXiv:2309.12748v2 for all 2 <= n <= 129 and agree on every n in 130..250.

## Partial wins

- **p1:** Determine the exact 1st/2nd-player outcomes (extending OEIS A389618 and A389619) and exact DAG vertex and edge counts (extending OEIS A389617 and Table A1 of arXiv:2309.12748v2) for every integer n contiguously in 130..180, verified by two independent solvers that reproduce Table A1 of arXiv:2309.12748v2 for all 2 <= n <= 129.

## How a win is checked

For Branch A, build the formal development in a clean project and audit the axioms of the main theorem (Lean: `lake build` and `#print axioms`) proving that the set of n >= 2 for which the Reversed Zeckendorf game is a second-player win is infinite. For Branch B or p1, run two independent solvers from scratch (e.g., a topological-bucket retrograde evaluator in Python/C++ and a packed bit-vector hash-table DAG solver in C/Rust) implementing the exact Split and Combine rules of Section 3 and Appendix B of arXiv:2309.12748v2. Verify that both solvers exactly reproduce all 49 published terms of A389618 (for 2 <= n <= 129), all 79 terms >= 2 of A389619 (for 2 <= n <= 127), and every vertex and edge count in Table A1 of arXiv:2309.12748v2 for 2 <= n <= 129 (including n = 64: 10,936 vertices, 63,222 edges; n = 65: 11,744 vertices, 68,351 edges; n = 129: 384,715 vertices, 2,945,040 edges), and that they agree on every vertex count, edge count, and win/loss outcome for all claimed n >= 130. Package the contiguous table extension as a single table file <= 1 MB (kit/SUBMIT.md).

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://oeis.org/A389618>

## Sources

- <https://oeis.org/A389618>
- <https://oeis.org/A389617>
- <https://oeis.org/A389619>
- <https://arxiv.org/abs/2309.12748>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Every reachable state for a given n is a partition of n into Fibonacci parts F_1, F_2, ..., F_k, and every such partition is reachable, so the game graph for n has exactly A003107(n) vertices. Replacing the O(|V|^2) list lookup and iterative relaxation in Appendix B of arXiv:2309.12748v2 with a hash-set BFS + reverse topological pass dramatically accelerates exact evaluation.
- Every Split move strictly increases the total piece count sum_{i>=1} h_i by +1, while every Combine move leaves sum_{i>=1} h_i unchanged and strictly increases the weighted index sum sum_{i>=1} i * h_i by +1 for i > 2 (since 2i - (i - 2 + i + 1) = +1) or increases h_2 by +2 for i = 2 (F_1 + F_3 -> 2 F_2). Thus bucket-sorting reachable states in descending lexicographic order of (sum_{i>=1} h_i, sum_{i>=1} i * h_i, h_2) yields an explicit topological order of the DAG without recursion.
- For Conjecture 1.2, look for starting Zeckendorf decompositions where every legal first move by Player 1 allows Player 2 to force the game into an all-even bin configuration (Lemma 4.1 of Batterman et al., where Player 2 wins by copycat) or a known P-position in the {1,2,3}-restricted endgame (Theorem 1.6).

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Index convention: F_1 = 1, F_2 = 2, F_3 = 3, F_4 = 5 (there is no F_0 = 0 or duplicate 1). The Combine rule for i = 2 is F_1 + F_3 -> 2 F_2, and the Split rule for i = 1 is F_2 -> 2 F_1.
- In A389617, the offset is n = 2 (the 64th displayed term is n = 65 with 11,744 vertices and 68,351 edges, while n = 64 has 10,936 vertices and 63,222 edges), and Table A1 of arXiv:2309.12748v2 already published vertex and edge counts up to n = 129; treat 2 <= n <= 129 as the calibration baseline and n >= 130 as the open frontier.
- Under the normal-play rules, n = 1 starts at a single F_1 with 0 legal moves (a terminal position); Table A1 of Batterman et al. begins at n = 2, whereas OEIS A389619 includes 1 at the start of its list by cataloguing convention.
- Appendix B of arXiv:2309.12748v2 reports a running time for n = 144 but no outcome; Table A1 and OEIS stop at n = 129. Re-check OEIS A389618 and the authors' later work immediately before claiming.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/graphs-games-automata/reversed-zeckendorf-game-p-positions-a389618.md
```

Already set up? Say `run V3R1T4S on reversed-zeckendorf-game-p-positions-a389618`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `reversed-zeckendorf-game-p-positions-a389618`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
