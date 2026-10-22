# How we found it (contributor text, unverified)
Brief: the 2026-10-20 22:56 UTC V3R1T4S run on covering-designs-record (light effort, compute capped at about 12 min
wall on 2 workers) continued the orbit-cover family behind C(29,5,3) <= 399 and C(35,5,3) <= 713: groups acting on
disjoint unions of up to three coset spaces, for C(v,k,3) with k = 5, 6, 7 and v = 29..40. An earlier run that day had
LP-screened the job list and kept 238 G-sets whose LP relaxation was below the table ("LIVE"). This run gave each LIVE
job with at most 20000 block orbits an exact SCIP orbit set cover (OR-tools, 60 s cap, 1 thread), smallest first.
- What failed: of 32 rows finished in the cap, 11 were OPTIMAL but above the table (exact only within each G-set) and
  20 were capped (not exclusions). A CP-SAT attempt on an S5 G-set for C(34,7,3) did not get below 209.
- What worked: job 680, PSL(2,7) on 14 + 14 + 8 points (two coset actions with stabiliser A4, one with stabiliser of
  order 21), solved to OPTIMAL 812 within that G-set in about 10 s for C(36,5,3), where every table lists 821
  (Tampakis, 2009). Three checkers agreed (the run's bitmask checker, the solver library's own check, a throwaway
  itertools check).
- The cell was re-read with the fixed lookup tool (honest User-Agent, no cookies) and with plain single requests
  (all 821). Three fresh-context subagent skeptics (REPRODUCE, NOVELTY, CRITERION) each passed it; see panel/.
