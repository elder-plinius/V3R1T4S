# The record we compared against
- URL: https://api.github.com/repositories/283947278/git/trees/master?recursive=1 (IEAWindSystems/iea37-wflo-casestudies,
  folder cs1-2/iea37-cs1-results)
- Fetched: 2026-10-20T01:08:33Z (scout, HTTP 200, page sha256
  c3a54a267ffb10a994f309ac609e4e1e572428e554739fa9057b80d92aca7bf3) and 2026-10-20T02:24:14Z (NOVELTY skeptic, HTTP 200,
  same tree sha 267f6e5d2906400b2ee0a8ff533da7ebcc4bb47a); repository last pushed 2020-11-13. Each of the 12
  16-turbine result files fetched once, HTTP 200.
- Cell: highest 16-turbine AEP under the official iea37-aepcalc.py: participant 12 (iea37-par12-opt16.yaml, git blob
  283959cbd7c1916fac9ee87e7715ae8fef4add18), 421561.89715 MWh, max hub radius 1303.518 m (outside). Best strictly
  feasible table entry: participant 5, 414141.29376. Participant 4 (SNOPT+WEC) 418924.40636 (radius 1300 + 3.9e-12 m).
- Best feasible value in the literature found: DPCRO-SL, arXiv 2212.00742, Table 4: 419935.7905 (its Table 5 layout,
  rounded to 0.1 m, re-scores to 419933.316).
