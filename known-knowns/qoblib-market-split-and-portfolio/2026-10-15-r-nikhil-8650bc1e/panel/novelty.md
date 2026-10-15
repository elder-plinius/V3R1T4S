# NOVELTY verdict: QOBLIB class 06, cell a200_t10_s00_b050_l1e-02 (instance po_a200_t10_s00, B = 50, lambda = 0.01, minimise)

context: subagent (Claude Code Agent tool, fresh context, saw only its copy of claim/ plus the web and TROPHY_CASE.md)

Claimed value: **-644342** (claim/CLAIM.md). This check covers novelty only: whether -644342 is strictly below every
value posted for this exact cell. It does not re-evaluate the claimed solution's feasibility or objective; that belongs
to the other skeptics.

novelty: CONFIRMED (every primary status source returned HTTP 200 on its single request)

## Fetch table

One plain curl request per URL, User-Agent "V3R1T4S-panel", no retries, no cookies, no proxy. Responses saved under
`fetches/` in this working directory. Times are UTC from `date -u`.

| URL | UTC time | HTTP | sha256 of saved response |
|---|---|---|---|
| https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md | 2026-10-15 09:03:29 | 200 | 05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a |
| https://api.github.com/repos/ZIB-AOPT/QOBLIB/pulls?state=open&per_page=100 | 2026-10-15 09:03:30 | 200 | 77717d408a8ac8c2fa14c7146b2ee60e56c42573829dd7260501611d8d19fb3f |
| https://api.github.com/repos/ZIB-AOPT/QOBLIB/pulls?state=closed&per_page=100 | 2026-10-15 09:03:33 | 200 | 6d2a95139fa0a261ef7a2cc59fe026ca63562a25fb1efcecbc63d45a28524612 |
| https://raw.githubusercontent.com/mnn31/QOBLIB/1772e1d7f5341b1b87f7e66029cf143b075ca259/06-portfolio/submissions/20261009_RestrictedChainDP_Gupta/a200_t10_s00_b050_l1e-02/a200_t10_s00_b050_l1e-02_solution.sol | 2026-10-15 09:03:39 | 200 | e886f65ac1b722f117c2333810266ff8ef2aff8a9a5f21d799755bcfcb2ba377 |
| https://raw.githubusercontent.com/marcinjkaminski/QOBLIB-4colors/e2fefab5060ea7f65fd906048d8dcb98b02643ed/06-portfolio/submissions/20260908_4colors-Optimizer_4colors/a200_t10_s00_b050_l1e-02/a200_t10_s00_b050_l1e-02_solution.sol | 2026-10-15 09:03:41 | 200 | b730b88b45af60c58c19b2fb9f4e729f5f1e8d6cf272afe11851f09ab8cf63ef |
| https://raw.githubusercontent.com/KenWuqianghao/qoblib-solvers/main/README.md | 2026-10-15 09:03:42 | 200 | 09b663a71af68a47c241a5e0445ba0331cca0743d1e717ecb5fef42ac88910df |
| https://github.com/mnn31/qoblib-solvers | 2026-10-15 09:03:43 | 200 | ea6fac710ea9d1161470b466cb775dd0c2fd75ded0da255cd3a7550f09104efd |
| https://api.github.com/search/repositories?q=qoblib&per_page=100 | 2026-10-15 09:03:46 | 200 | 24d8dd747c38ed8659969e8e723fe9d8dd713ea2799b81ef8cf9af2a6c94e2a3 |
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15 09:03:48 | 200 | b053bd48c2a3d7016fb9c7018d2401bd5fee52da281c197c438da10211c84d2a |
| https://zib-aopt.github.io/QOBLIB/ | 2026-10-15 09:03:51 | 200 | b75c4b51f3ea7436a98e30c94e15b6769a298fc0257f637b4e93e4f7982e5aab |
| https://raw.githubusercontent.com/mnn31/qoblib-solvers/main/portfolio/README.md | 2026-10-15 09:04:35 | 200 | f440b833ad5ea16cf3138152759de89278ae789c36758d0330637bfa85eaf3cd |
| https://api.github.com/repos/mnn31/qoblib-solvers/git/trees/main?recursive=1 | 2026-10-15 09:04:36 | 200 | 09bcaa5033083f9adc3ec22e9aacb0e72395578034ece2fa04366ee7abd666fb |
| https://api.github.com/repos/ZIB-AOPT/QOBLIB/pulls/44/files?per_page=100 | 2026-10-15 09:04:39 | 200 | e6f8d103c0ebe171fc84dcdff54b1f113bdba6a597ded64554afcb277aa74213 |
| https://raw.githubusercontent.com/Quantum-Global-Group/qoblib-dashboard/main/README.md | 2026-10-15 09:04:41 | 200 | ca069b1655fd91807b84ec71a4beabb1831e860528c3b7f33adbc1fe0e1c3588 |
| https://arxiv.org/html/2504.03832 | 2026-10-15 09:05:21 | 200 | e942ae571e805e3e7c983bc930621a8c86f00569e196627162fa21df755efff1 |
| https://arxiv.org/html/2504.03832v1 | 2026-10-15 09:05:40 | 200 | bf3993ac23cd4ba7d7060e0fc27f91310ea8833b479d77764a69d8d4ca787f1c |
| https://api.github.com/repos/mnn31/QOBLIB/git/trees/b7359bb00be23ea7ba57aa1f1c557241e26ec725?recursive=1 | 2026-10-15 09:06:24 | 200 | 78c6906afbfa78702f8a21e3e53b0a2fa103c8119421984ee14b81fa3cbde440 |

I also ran web searches (WebSearch tool, no saved response) for "QOBLIB portfolio optimization a200_t10_s00 best known
objective", "QOBLIB 06-portfolio submissions a200 lambda 0.01 arXiv OR Zenodo 2025 2026", the exact string
"a200_t10_s00_b050_l1e-02", and "QOBLIB portfolio new best-known solutions a200 a400 heuristic 2026 github". The exact
string returned no hits. None of the searches surfaced a QOBLIB-related Zenodo deposit or an arXiv value for this cell,
apart from the QOBLIB paper covered below.

## Findings per source

1. **Official best-known table** (fetched 09:03:29 UTC). The sha256 matches the claimant's copy. It has **no row** for
   a200_t10_s00 at any B or lambda. "a200" appears only once, on line 7, as the naming-convention example
   ("`aXXX`: Number of assets (e.g., `a200` for 200 assets)"), and the table contains no a400 rows either.
2. **Open QOBLIB PRs** (fetched 09:03:30 UTC, 24 open). The portfolio PRs and their current heads:
   - #87, head mnn31/QOBLIB `1772e1d7f5341b1b87f7e66029cf143b075ca259`. The solution file for this cell has the header
     line `objective -401535` (budget 50, lambda 0.01).
   - #64, head marcinjkaminski/QOBLIB-4colors `e2fefab5060ea7f65fd906048d8dcb98b02643ed`. The solution file for this cell
     has the header line `objective -192428` (budget 50, lambda 1e-2).
   - #44, head mnn31/QOBLIB `b7359bb00be23ea7ba57aa1f1c557241e26ec725`. I read the full recursive tree at that head:
     its ChainDP submission has 642 paths covering a003, a004, a005 and a010 only. It has **no a200 file**.
   - The only open PRs whose title or body mention "a200" are #87 and #64. No PR text mentions 644342, 401535 or 192428.
   - The heads match those stated in CLAIM.md.
3. **Closed/merged QOBLIB PRs** (fetched 09:03:33 UTC, 51 returned). The portfolio-related ones are #36, #31 and #3 (all
   merged), plus #24 (instance upload) and #5. No closed PR title or body mentions "a200". Merged content is reflected in
   the official table, which has no a200 row.
4. **Third-party repositories.**
   - KenWuqianghao/qoblib-solvers README: its a200_t10_s00 rows are `b050_l1e-03` (-817828) and `b050_l5e-04` (-879890)
     only. The README contains no lambda 1e-02 values at all.
   - mnn31/qoblib-solvers: the portfolio README says the a200/a400 values come from the heuristic submitted as QOBLIB
     PR #87. The repository tree (1708 paths, not truncated) holds no a200 files. Its only value for this cell is
     therefore PR #87's -401535.
   - GitHub repository search "qoblib" returned 14 repositories. Apart from the two above, none is a portfolio-results
     repository. Quantum-Global-Group/qoblib-dashboard says it syncs the official `solutions/README.md`, which has no
     a200 rows.
5. **QOBLIB website** (https://zib-aopt.github.io/QOBLIB/). It lists portfolio cells such as a010_t10_orig_b004_*, but no
   string matching a200 occurs in the page.
6. **Literature in the last 24 months.** The QOBLIB paper, arXiv 2504.03832 (April 2025), is the only one I found.
   - v1, Table 6, captioned "a200_t10_s00 instance", row lambda = 0.01: Gurobi incumbent **136536** (LB -5982818.73,
     gap 44.82 %), ABS2 incumbent **-36277**. This model version may differ from the current reference model; v1 has
     half-integer incumbents.
   - In the current v2, Table 6 is relabelled as the a050_t15_s00 instance, so it is not this cell.
   - Either way, both v1 values are far above -644342.
7. **TROPHY_CASE.md** (read-only, 100 lines). It contains no occurrence of "qoblib", "portfolio", "a200", "644342" or
   "401535".
8. **V3R1T4S open PRs** (fetched 09:03:48 UTC, 39 open). No title or body mentions a200_t10_s00, 644342, 401535,
   QOBLIB/qoblib or portfolio.

## Values posted for this exact cell

| source | value |
|---|---|
| QOBLIB PR #87 (RestrictedChainDP, head 1772e1d7) | **-401535** |
| QOBLIB PR #64 (4colors, head e2fefab5) | -192428 |
| arXiv 2504.03832v1 Table 6, ABS2, lambda 0.01 | -36277 |
| arXiv 2504.03832v1 Table 6, Gurobi incumbent, lambda 0.01 | 136536 |
| official best-known table | no row |
| KenWuqianghao/qoblib-solvers, mnn31/qoblib-solvers, QOBLIB website, TROPHY_CASE.md, V3R1T4S open PRs | none for this cell |

**Best posted value for the cell: -401535, QOBLIB PR #87.** Source file:
https://raw.githubusercontent.com/mnn31/QOBLIB/1772e1d7f5341b1b87f7e66029cf143b075ca259/06-portfolio/submissions/20261009_RestrictedChainDP_Gupta/a200_t10_s00_b050_l1e-02/a200_t10_s00_b050_l1e-02_solution.sol
(header `objective -401535`, fetched 2026-10-15 09:03:39 UTC).

## Decision

-644342 < -401535: the claimed value is strictly smaller, by 242807, than the best value I could find posted for this
cell, so this is not a tie. Every primary status source was read with HTTP 200.

Caveat: this pass is conditional on the claimed objective -644342 being correct and the solution feasible under
`bqp_u3_c10.zpl` / `parameter_u3_c10.zpl`. I did not re-evaluate that; the correctness skeptic must.

pass: true
