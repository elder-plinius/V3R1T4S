# How we found it (contributor text, unverified)
Brief: the 2026-10-19 13:03 UTC V3R1T4S run on covering-designs-record (light effort, 8 CPU cores) resumed a sweep of
orbit covers under small groups (A5, S5, PSL(2,7)) acting on disjoint unions of coset spaces, one exact CP-SAT orbit
set cover per (G-set, cell) job with a 20 s cap.
- What failed: almost every job only tied or lost to the table. Exact repair of near-miss local-search states at
  small v found nothing. That run then stopped before writing its report.
- What worked: PSL(2,7) acting on two 14-point coset spaces of its two non-conjugate A4 subgroups plus one fixed
  point (v = 29) gave a 399-block cover of C(29,5,3) (capped, FEASIBLE). The table lists 413. The 91 blocks through the
  fixed point are the fixed point plus two pairs of one perfect matching of the other 28 points.
- The next run (2026-10-19 23:00 UTC) picked it up as a lead. It re-checked it with independent checkers and tried to
  push it to 398 (annealing, partial CP-SAT re-solves, large-neighbourhood search), without success. We read the live
  Covering Repository cell ourselves in a browser, as submitters, because the per-cell pages are challenged for machines. Three
  fresh-context subagent skeptics (REPRODUCE, NOVELTY, CRITERION) each passed it; see panel/.
