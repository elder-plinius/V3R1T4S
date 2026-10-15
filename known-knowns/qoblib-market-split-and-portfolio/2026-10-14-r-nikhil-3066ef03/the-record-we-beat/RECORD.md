# The record we beat

Cell: QOBLIB class 06 portfolio, instance `po_a200_t10_orig`, budget B = 50, lambda = 1e-2
(`a200_t10_orig_b050_l1e-02`). The class minimises.

| source | URL | fetched (UTC) | HTTP | sha256 of the response | extracted |
|---|---|---|---|---|---|
| official best-known table | https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md | 2026-10-14T17:20:24Z | 200 | 05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a | no row for any a200 or a400 instance |
| open QOBLIB pull requests | https://api.github.com/repos/ZIB-AOPT/QOBLIB/pulls?state=open&per_page=100 | 2026-10-14T17:20:25Z | 200 | 9f2351223d48cb59a41245f5e0ac3fcff70a8030642076e3f65c9a496541492a | class-06 PRs #87, #64, #44 open |
| PR #44 head tree | https://api.github.com/repos/mnn31/QOBLIB/git/trees/b7359bb00be23ea7ba57aa1f1c557241e26ec725?recursive=1 | 2026-10-14T17:20:38Z | 200 | 78c6906afbfa78702f8a21e3e53b0a2fa103c8119421984ee14b81fa3cbde440 | no a200/a400 file |

Values posted for the cell (solution files read from the PR heads; re-evaluated exactly, both reproduce):

| PR | head commit | file | sha256 of the file | objective |
|---|---|---|---|---|
| #87 (RestrictedChainDP) | 1772e1d7f5341b1b87f7e66029cf143b075ca259 | 06-portfolio/submissions/20261009_RestrictedChainDP_Gupta/a200_t10_orig_b050_l1e-02/a200_t10_orig_b050_l1e-02_solution.sol | df44335103ccd97d7110b456b22f082cc7df8ca8f9a4ede8d319f4be6064f561 | **−551385** (the bar) |
| #64 (4colors-Optimizer) | e2fefab5060ea7f65fd906048d8dcb98b02643ed | 06-portfolio/submissions/20260908_4colors-Optimizer_4colors/a200_t10_orig_b050_l1e-02/a200_t10_orig_b050_l1e-02_solution.sol | 6224003b825a010a50bcc86681379f22c0e9d30fd2be1c3b0f2f49eb6fc29955 | −300647 |

Headers were not recorded for the 17:20 fetches. The same table and PR list were first fetched at 2026-10-14T15:20:01Z
with identical sha256 values. The panel's NOVELTY skeptic fetched the sources again at 17:24:41Z–17:28:42Z
(panel/novelty.md). The honesty gate re-read them once each at 2026-10-14T22:20:58Z, HTTP 200:

- table: sha256 05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a (byte-identical), selected headers
  `etag: "b8d113952e45aebb91be82ab051a193b5f7c92736b83c957b3470b0de433681e"`, `date: Wed, 14 Oct 2026 22:20:58 GMT`;
- open PRs: sha256 c26d7d62269bfbd9e2efaa2514e3e257ac10db5fc29d6589d6b71c58ca8121ea, same 24 PRs, class-06 heads
  unchanged (only PR #88, class 04, changed its update time), selected header `date: Wed, 14 Oct 2026 22:21:00 GMT`.
