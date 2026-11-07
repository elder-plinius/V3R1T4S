# The record we compared against
- URL: https://api.github.com/repositories/283947278/git/trees/master?recursive=1 (IEAWindSystems/iea37-wflo-casestudies,
  folder cs1-2/iea37-cs1-results)
- Fetched: 2026-10-18T01:07:59Z (scout) and 2026-10-18T03:20:29Z (NOVELTY skeptic), HTTP 200 both, page sha256
  c3a54a267ffb10a994f309ac609e4e1e572428e554739fa9057b80d92aca7bf3 (identical); repository last pushed 2020-11-13.
  Each of the 12 64-turbine result files fetched once, HTTP 200.
- Cell: highest 64-turbine AEP under the official iea37-aepcalc.py: participant 12 (file iea37-par12-opt64.yaml,
  sha256 7e643ef74c61cc2a2af8a93afd2bfb6b9737091ad8a52c8984c2bafa343b9fae, added 2019-07-29), 1526474.80248 MWh, max
  hub radius 3000.0041276 m (outside). Next: participant 4 (SNOPT+WEC, the 2019 paper's winner) 1513311.19361
  (radius 3000 + 1.4e-10 m).
- Paper: Baker et al., AIAA 2019-0540, https://docs.nlr.gov/docs/fy19osti/72935.pdf, fetched 2026-10-18T01:09:42Z,
  HTTP 200, sha256 2d4ca1174f6432d9ac09b7bf8ff5f9c742f6a4146daccdb487e93e30d7259c9c; Table 4 best 1513.31 GWh.
