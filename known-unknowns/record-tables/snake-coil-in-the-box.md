# Snake-in-the-box / coil-in-the-box records in dimensions 9-13

📊 **Record tables** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

Find longer induced paths (snakes) or induced cycles (coils) in the n-dimensional hypercube Q_n. Maxima are proven for snakes in n <= 8 (98 at n=8). In dimension 9 and up, only lower bounds are known. The live minortriad.com/snake table (dimensions 1-13; snakes, coils and symmetric coils) is ahead of the paper tables of Orland-Fagan et al. (arXiv:2607.15270 v3, 30 Sep 2026) in Q11-Q13. EinsteinArena's 13D snake problem lists 2934.

## What counts as a win

Success means a valid induced path (snake) or induced cycle (coil) in Q_n, 9 <= n <= 13, verified exhaustively (single-bit steps, distinct vertices, popcount(v_i ^ v_j) >= 2 for non-consecutive pairs, closing edge induced for coils), whose edge length is STRICTLY GREATER (direction: max) than the maximum, at verification time, of: the live primary table https://www.minortriad.com/snake/, the Math-AI-Caltech/Snake-in-the-Box README 'subsequent bounds by others' lists (https://github.com/Math-AI-Caltech/Snake-in-the-Box), the latest arXiv:2607.15270 version, the EinsteinArena value (13D snake) and any newer source from a fresh search, for that dimension and type (context on 2026-10-20: snakes Q9-Q13 191/379/750/1480/2946, coils 192/374/740/1468/2930). The verifier's checker must reproduce the exact length of at least one downloaded record file of the same n and type (length-convention calibration); without that calibration the claim is not a record.

## Partial wins

- **p1:** A symmetric-coil record: a coil in Q_n (9 <= n <= 13) that is invariant under the symmetry required by the minortriad symmetric-coil table, verified exhaustively, whose length strictly exceeds the live minortriad symmetric-coil value for that n (context: Q9 186, Q10 370, Q11 730, Q12 1434, Q13 2830).
- **p2:** A Q14 record: a snake or coil in Q14, verified exhaustively, strictly longer than every Q14 value published at verification time (arXiv:2607.15270 v3 tables, EinsteinArena, Math-AI-Caltech repo); counts only if such a published value exists for comparison.
- **p3:** An equal-record snake or coil: length equal to the live record (as defined in the success criterion) for that n and type, 9 <= n <= 13, verified exhaustively, and inequivalent under hypercube automorphisms (coordinate permutations and translations) and reversal (plus cyclic rotation for coils) to every record file published in the Math-AI-Caltech repository and the arXiv:2607.15270 data at verification time, checked by comparing canonical relabelled transition sequences.

## How a win is checked

Use an independent O(L^2) bit check, or O(L*n) with a hash set of vertices plus a check that each vertex's n neighbours contain at most 2 path members (1 for endpoints), all at the right positions. Confirm the length convention against the table by re-verifying a known record snake from the Math-AI-Caltech repo.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.minortriad.com/snake/>

## Sources

- <https://www.minortriad.com/snake/>
- <https://github.com/Math-AI-Caltech/Snake-in-the-Box>
- <https://arxiv.org/abs/2607.15270>
- <https://einsteinarena.com/>
- <https://en.wikipedia.org/wiki/Snake-in-the-box>
- <https://arxiv.org/html/2607.15270v3>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Target coils and symmetric coils, which may be less heavily attacked than snakes in 2026. Convert snakepit ideas to cycles.
- Splice from lower dimensions. Combine two record snakes in Q_{n-1} with a 1-bit lift and search the junction region exhaustively with SAT (pysat) on a small window.
- Do window re-optimization. Take a record snake, cut out a segment of 30-60 vertices, and solve 'longest induced path between the fixed endpoints avoiding the rest's closed neighbourhood' exactly with CP-SAT. Repeat at all offsets.
- Use symmetry prescription. Require invariance under a hypercube automorphism of order 2-4 (a coordinate permutation composed with XOR), which shrinks the space as in symmetric coil records.
- Run Monte-Carlo beam search with a learned 'remaining free volume' heuristic: the count of vertices with no path neighbour.
- Tail re-growth: take record snakes, cut the last 10-30% and regrow exhaustively with a bitset DFS plus a dead-vertex pruning bound. Use all 100+ inequivalent 190-snakes from the paper's repository as seeds for n=9.
- Lift record (n-1) snakes and coils into Q_n through doubling constructions with permutation 'spreads', then local-repair with SAT (pysat with cadical) on a window of the sequence.
- Nested Monte Carlo or limited-discrepancy search with a learned priority, comparing with the Beam Anchor idea from 2607.15270.
- Exploit the 'snakepit' idea from the paper: pack disjoint snakes, then splice them through short bridges found by exact search.
- Symmetric snakes: require the snake to be invariant under a hypercube automorphism of order 2 or 4. This halves the search, and many records are near-symmetric.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Length conventions: edges vs vertices, and whether a coil counts edges in the cycle. Calibrate on a known record.
- Snakes vs coils vs symmetric coils are separate tables.
- Values for Q10-Q13 come from 2607.15270's tables. Confirm the live minortriad value before claiming.
- Paper tables lag the minortriad table. In Q11-Q13 minortriad is already 2-14 edges longer (snakes +4/+4/+14, coils +6/+2/+14).
- Length conventions differ between sources (vertices vs edges, closed vs open).
- Records changed in July-September 2026. Read the latest arXiv version and the repository.
- A path that is only distance-preserving (no chords checked) is not induced.
- The README 'subsequent bounds' already beat the paper at n=11, 12 and 13. Do not use the paper table alone.
- Coil records may have moved after publication, so search for the newest values before claiming a coil.
- Older bank copies list stale values (snake Q13 2934; coils Q11 734, Q12 1466, Q13 2916). The live values on 2026-10-03 were snake Q13 2938 and coils 740/1468/2930.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/record-tables/snake-coil-in-the-box.md
```

Already set up? Say `run V3R1T4S on snake-coil-in-the-box`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `snake-coil-in-the-box`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
