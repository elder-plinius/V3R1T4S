# How we found it (contributor text, unverified)
Brief: the 2026-10-17 13:03 UTC V3R1T4S run on covering-designs-record (light effort, 8 CPU cores) tried a structured
lens (group-orbit covers) and an obstruction lens (lower-bound refreshes).
- What failed: orbit covers under the full groups PGL(2,q), PSL(2,q) and PGammaL(2,q) on PG(1,q) gave nothing below the table. The
  lower-bound lens found only stale Schonheim refreshes, which are not claimed. Trying to push this design to 69 by block surgery,
  simulated annealing and capped CP-SAT over its subgroups did not succeed.
- What worked: smaller subgroups. A5 (order 60) inside PSL(2,19), acting on the 20 points of PG(1,19), has an exact orbit
  cover for C(20,6,3) of 70 blocks (three orbits, sizes 20+20+30), optimal within that family. The table lists 71.
- The run's session crashed after finding it. A later interactive pass rebuilt the design from scratch with fresh code
  (isomorphic result, confirmed with a second solver). The operator then read the live Covering Repository cell by hand,
  because the per-cell pages are challenged for machines. Three fresh-context subagent skeptics (REPRODUCE, NOVELTY, CRITERION) each
  passed it; see panel/.
