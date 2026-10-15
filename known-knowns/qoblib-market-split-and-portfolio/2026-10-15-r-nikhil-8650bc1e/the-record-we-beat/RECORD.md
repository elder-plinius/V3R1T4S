# The record we beat

Cell: QOBLIB class 06 portfolio, instance `po_a200_t10_s00`, budget B = 50, lambda = 1e-2
(`a200_t10_s00_b050_l1e-02`). The class minimises.

| source | URL | fetched (UTC) | HTTP | sha256 of the response | extracted |
|---|---|---|---|---|---|
| official best-known table | https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md | 2026-10-15T09:01:05Z | 200 | 05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a | no row for any a200 or a400 instance |
| open QOBLIB pull requests | https://api.github.com/repos/ZIB-AOPT/QOBLIB/pulls?state=open&per_page=100 | 2026-10-15T09:01:06Z | 200 | 77717d408a8ac8c2fa14c7146b2ee60e56c42573829dd7260501611d8d19fb3f | 24 open; class-06 PRs #87, #64, #44 with unchanged heads |
| KenWuqianghao/qoblib-solvers README | https://raw.githubusercontent.com/KenWuqianghao/qoblib-solvers/main/README.md | 2026-10-15T09:01:09Z | 200 | 09b663a71af68a47c241a5e0445ba0331cca0743d1e717ecb5fef42ac88910df | no value for this cell (its a200_t10_s00 rows are lambda 1e-3 and 5e-4) |

Values posted for the cell (solution files read from the PR heads at 2026-10-15T03:15Z; re-evaluated exactly, both reproduce):

| PR | head commit | file | sha256 of the file | objective |
|---|---|---|---|---|
| #87 (RestrictedChainDP) | 1772e1d7f5341b1b87f7e66029cf143b075ca259 | 06-portfolio/submissions/20261009_RestrictedChainDP_Gupta/a200_t10_s00_b050_l1e-02/a200_t10_s00_b050_l1e-02_solution.sol | e886f65ac1b722f117c2333810266ff8ef2aff8a9a5f21d799755bcfcb2ba377 | **−401535** (the bar) |
| #64 (4colors-Optimizer) | e2fefab5060ea7f65fd906048d8dcb98b02643ed | 06-portfolio/submissions/20260908_4colors-Optimizer_4colors/a200_t10_s00_b050_l1e-02/a200_t10_s00_b050_l1e-02_solution.sol | b730b88b45af60c58c19b2fb9f4e729f5f1e8d6cf272afe11851f09ab8cf63ef | −192428 |

Response headers were not recorded for these fetches. The same table had identical sha256 at 2026-10-15T03:13:17Z
and on 2026-10-14. The panel's NOVELTY skeptic fetched the sources again at 09:03:29Z–09:06:24Z (panel/novelty.md).
