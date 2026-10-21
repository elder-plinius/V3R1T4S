# Tighten God's number bounds for the 24-puzzle (5x5 sliding tiles, STM)

🕸️ **Graphs, games and automata** · harvest (many cells or partial wins within reach) · tractability ★★☆☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

God's number G for the 5x5 sliding-tile puzzle (single-tile metric) satisfies 152 <= G per the cubeman threads (Rokicki); OEIS A087725 (checked 2026-10-20) now also records 'a(5) >= 154 from ciphrae' (the certificate was not located; the linked ciphrae repository proves only the asymptotic n^3 + O(n^2 log n) bound). The best upper bound is 182 (de Ruiter, 2020 forum claim, not refereed; now also recorded in OEIS A087725 next to Whitmore's 205). Raise the lower bound above 154 (parity forces even steps, so to >= 156) by certifying that some position needs at least 156 moves, or rigorously lower the upper bound below de Ruiter's 182.

## What counts as a win

Lower bound: a solvable position P with a certificate that its optimal length is >= 156, STRICTLY ABOVE the best lower bound in the cubeman threads, OEIS A087725 and a fresh search at verification time: either (a) h(P) >= 156 from a provably admissible heuristic recomputed independently (disjoint additive PDBs, walking distance, or max of these), or (b) a complete IDA* to threshold 154 with no solution, reproduced by an independent solver with matching per-iteration node counts. Upper bound: a phase decomposition with phase-shift offsets, every phase diameter and offset table recomputed by full BFS, giving a rigorous bound STRICTLY BELOW the best claimed upper bound at verification time (de Ruiter's 182 as of 2026-10-03, i.e. <= 180). A result of 182 or more is not a record.

## Partial wins

- **p1:** A rigorous, independently reproduced verification of de Ruiter's 182 upper bound (cubeman node/view/559): every phase diameter, phase-shift offset and combination recomputed by full BFS from scratch with code independent of his, reproducing exactly 182.
- **p2:** A solvable position P with a provably admissible heuristic value h(P) >= 152 (recomputed independently by the skeptic's own PDB/walking-distance code), giving a seconds-checkable certificate of the current lower bound in place of Rokicki's 10-day IDA* search.

## How a win is checked

Recompute the PDBs from scratch with the verifier's own BFS code, look up h(P), and check the additivity partition is disjoint. For IDA* claims, rerun with an independent solver and compare per-iteration node counts. Confirm P's solvability parity. For upper bounds, rerun each phase BFS and check the maximum depth table.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <http://forum.cubeman.org/?q=node/view/238>

## Sources

- <http://forum.cubeman.org/?q=node/view/238>
- <http://forum.cubeman.org/?q=node/view/559>
- <https://oeis.org/A087725>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Search over positions rather than over moves: hill-climb or anneal to find positions maximizing max(additive 6-6-6-6 PDB with reflection, walking distance) in milliseconds per evaluation. If any position scores >= 156, that alone is the certificate (OEIS already records 154). The 180-degree position only scores 140 with WD, but no systematic adversarial search over positions is reported in the sources found.
- Stronger admissible heuristics: 7-7-5-5 or 8-8-8 partitions (with 64 GB RAM limits in mind, using compressed or modular PDBs), plus the maximum over symmetric lookups (transpose and conjugation).
- Finish Rokicki's ply-152 IDA* on the 180-degree position with modern PDBs and 10-core parallel IDA*. If it completes with no solution, the bound becomes 154. Log node counts for verification.
- Upper bound: re-split the three-phase method (which solves 7 tiles, then 9, then the last 8-puzzle) to balance phase diameters. Compute exact phase diameters with disk-based BFS.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Inadmissible heuristics, such as the linear-conflict variants combined incorrectly with additive PDBs.
- Parity: a position needing 'at least 153' automatically needs 154. Make sure the statement is about the correct parity class.
- The forum's metric ambiguity (single-tile STM vs multi-tile MTM). The 152/205 bounds are STM.
- A bound claimed from an IDA* run that was interrupted or that used a buggy goal test.
- The upper bound is 182 (de Ruiter 2020), not 205. Any upper bound from 183 to 204 is old news.
- The ply-152 IDA* on the 180-degree position costs roughly 4-5 times Rokicki's ten-day 2011 run. It is not feasible in one day without much stronger PDBs.
- Forum upper-bound claims are phrased 'I believe'; reproduce before relying on them.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/graphs-games-automata/slide-24-puzzle-lower-bound.md
```

Already set up? Say `run V3R1T4S on slide-24-puzzle-lower-bound`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `slide-24-puzzle-lower-bound`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
