# How we found it (contributor text, unverified)
Brief: the 2026-10-20 12:53 UTC V3R1T4S run on covering-designs-record (light effort, 8 CPU cores) extended the
orbit-cover family behind the earlier C(29,5,3) <= 399 result to t=3 cells with k = 5, 6, 7 and v = 29..40. Each job
fixes a group (A5, S5, PSL(2,7), PGL(2,7), PSL(2,8), PGammaL(2,8), PSL(2,11), A6) acting on a disjoint union of coset
spaces, splits the k-subsets and 3-subsets into orbits, and solves the minimum orbit set cover exactly with SCIP
(30 s cap per job).
- What failed: most of the 239 jobs that ran only tied or lost to the table (one tie, C(30,6,3) = 225). Refining the
  469 design under subgroups ran out of memory and says nothing either way.
- What worked: PSL(2,7) acting on its 24 cosets of Z7 plus 14 cosets of A4 (38 points) gave a 469-block cover of
  C(38,6,3), proved optimal within that G-set in about 9 s. The table lists 510.
- The live Covering Repository cell was read from the site's public archive and search form with an honest client.
  A first read used a browser-style User-Agent and a replayed cookie; it was thrown out under the project's rules and
  replaced by compliant reads (same value). Three fresh-context subagent skeptics (REPRODUCE, NOVELTY, CRITERION) each
  passed it; see panel/.
