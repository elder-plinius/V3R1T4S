# NOVELTY verdict: QOBLIB class 06 portfolio, cell a200_t10_orig_b050_l1e-02

context: subagent (Claude Code Agent tool, fresh context, model opus)

- Cell: instance `po_a200_t10_orig`, budget B = 50, lambda = 1e-2 (file key `a200_t10_orig_b050_l1e-02`). The class minimises.
- Claimed value: -691624. The claim's solution header reads `instance po_a200_t10_orig`, `budget 50`, `lambda 0.01`, `objective -691624`. Its sha256 is `3066ef033d46c6e8fdb38d20f562a6e5ff41b67e4b64881c9988a67fdfe58097`, and all 12 file hashes in the claim package match CLAIM.md.
- Criterion (from CLAIM.md): the bar is the better of the official best-known table and any value posted in an open QOBLIB pull request (#44, #64, #87 and any newer). Strictly smaller wins; a tie is not a record.
- Scope: this judges novelty only. It takes -691624 as the claimed exact objective; feasibility and the exact objective are for the other panel members.
- injection_suspected: none. I scanned the visible text of every saved response; none of the PR bodies, comments, READMEs, abstracts or papers addresses reviewers or agents.
- Verdict written 2026-10-14 22:18 UTC. The status snapshot is from 2026-10-14 17:24:41 to 17:28:42 UTC, after the claim freeze at 17:21:46 UTC. Under the one-request rule nothing was re-fetched.

## Status sources (each fetched once; plain curl, User-Agent "V3R1T4S-panel"; all HTTP 200)

- **Official best-known table** (https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md, fetched 2026-10-14 17:24:41 UTC, HTTP 200, 10450 bytes, sha256 `05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a`).
  - The table has **no row for a200_t10_orig_b050_l1e-02**.
  - Its 129 rows cover only the a003_t02_orig, a010_* and a050_* instances, and there is no a200 or a400 row. The string "a200" occurs once, in the naming-convention example.
  - The response is byte-identical to the claimant's copy fetched at 17:20:24 UTC.
- **Open QOBLIB PRs** (https://api.github.com/repos/ZIB-AOPT/QOBLIB/pulls?state=open&per_page=100, 17:24:54 UTC, HTTP 200, sha256 `9f2351223d48cb59a41245f5e0ac3fcff70a8030642076e3f65c9a496541492a`).
  - 24 open PRs on a single page, byte-identical to the claimant's 17:20:25 record.
  - The class-06 PRs are #87, #64 and #44: their titles are prefixed `[06-portfolio]`, and a regex screen of all 24 titles and bodies found no other.
  - #89 matched the regex only through "solver portfolio"; it is a 05-sports PR. The newer PRs #88 and #89 are 04-steiner and 05-sports.
- **PR #87** (head `1772e1d7f5341b1b87f7e66029cf143b075ca259`):
  - Its head tree is not truncated (19241 entries) and holds exactly one solution file for this cell, `06-portfolio/submissions/20261009_RestrictedChainDP_Gupta/a200_t10_orig_b050_l1e-02/a200_t10_orig_b050_l1e-02_solution.sol` (git blob `d645eb76…`).
  - The raw file's header is **`objective -551385`**, and the summary CSV gives Best Objective Value -551385.
  - The file is byte-identical to the claim's `bar/PR87_…` copy.
- **PR #64** (head `e2fefab5060ea7f65fd906048d8dcb98b02643ed`):
  - Its head tree is not truncated and holds one solution file for the cell, under `20260908_4colors-Optimizer_4colors/` (git blob `0f65c9d4…`).
  - The header is **`objective -300647`**, and the CSV agrees.
  - The file is byte-identical to the claim's `bar/PR64_…` copy.
- **PR #44** (head `b7359bb00be23ea7ba57aa1f1c557241e26ec725`): its head tree is not truncated and has no a200 or a400 path under `06-portfolio/submissions/` (it covers a003 to a010). Its sha256 equals the claimant's record.
- **Comment threads of #87 and #64** (3 comments each): CI validation logs, the maintainer's AI-policy notices and an author reply. Neither thread posts any value for this cell.
- **Recently closed QOBLIB PRs** (one request, the 50 most recent):
  - The class-06-related ones are #36 (checker and canonical format), #31 (ISQR on a003, a004 and a005), #24 (new small instances) and #3 (Arvak on a010). All are merged, and none touches a200.
  - Merged content feeds the auto-generated table, which has no a200 row.
  - Page 2 holds PRs created before 2026-03-08 and was not fetched, per the one-request instruction.

**Bar for this cell: -551385, posted in open PR #87.** The official table has no row. The next value is -300647 (PR #64).

## Literature (last 24 months), GitHub, Zenodo

- **QOBLIB paper arXiv:2504.03832.** The abstract page lists v1 (4 Apr 2025) and v2 (28 Aug 2025, the latest).
  - v1 Table 6 reports Gurobi/ABS2 values for **a200_t10_s00**, a different instance (seed s00, not orig).
  - v2 replaced that table with a050_t15_s00, and its baseline covers n ≤ 50.
  - Neither version has any value for a200_t10_orig at any lambda.
  - The journal version (Nature Computational Science 2026, DOI 10.1038/s43588-026-00991-1, PMC13293884) has no instance-level portfolio values in its main text. It defers baselines to its Supplementary Information, which I did not fetch; the full-length arXiv v2 carries those baseline tables.
- **Papers citing QOBLIB.** Semantic Scholar's citation list has 50 papers, dated 2024-10 to 2026-10-07. I screened the portfolio-related and plausibly relevant ones on their arXiv abstract pages: 2605.17623, 2610.10772, 2606.10098, 2603.13607, 2604.25162 and 2608.28842, plus 2512.22001, 2607.03218 and 2609.15708, which came up in web search.
  - None of them uses QOBLIB a200 instances or reports a value for this cell.
  - They cover single-period mean-variance models, a 150-qubit dynamic-portfolio instance, a 38-asset IBEX model, a Russell 3000 model, Birkhoff, graph and HUBO problems.
  - 2510.27117 (GFORS) was screened by web search only. It covers set cover, knapsack, max cut, 3D assignment and facility location, with no portfolio.
- **Web searches** for "po_a200_t10_orig", "a200_t10_orig_b050_l1e-02", QOBLIB a200 portfolio and related terms found nothing beyond QOBLIB PR #87.
- **GitHub.** A repository search for "QOBLIB" returned 14 repos.
  - mnn31/qoblib-solvers (portfolio README and results README): no a200 values; it points to PR #87.
  - KenWuqianghao/qoblib-solvers (created 2026-09-30) posts 27 portfolio values. These include a200_t10_orig at lambda 1e-3 (-824759) and 5e-4 (-875407), but **none at lambda 1e-2**: its MIQP runs used lambdas 1e-4, 5e-4 and 1e-3, and its MIP/ILS sweeps used 0, 1e-6 and 1e-5. No PR from it appears in the open or closed lists.
  - The qoblib-dashboard best-known JSON mirrors the official table and has no a200 entries.
- **Zenodo** (q=QOBLIB) has 2 records.
  - The QOBLIB v1.1.0 snapshot (2026-03-13) predates every a200 submission.
  - The QUBOLib corpus (2026-09-29): its QOBLIB collection holds only the 128 a010/a050 portfolio reference objectives.
- **Limited fetches.** These were literature-search endpoints, not status sources, and none was retried:
  - export.arxiv.org search returned 429, and export.arxiv.org id_list returned 503.
  - Both Semantic Scholar keyword searches returned 429.
  - Zenodo with size=100 returned 400, a page-size validation error. A different, corrected URL with size=25 then returned 200.
  - The arXiv abstract request for 2510.27117 was cut off by a session pause before any response arrived. It was not re-requested and was screened by web search instead.

## V3R1T4S

- TROPHY_CASE.md (this repo's copy: 53 rows across six result families plus two commitments) has no QOBLIB or portfolio entry.
- V3R1T4S open PRs (27): none mentions QOBLIB, portfolio, a200 or any of the values -691624, -551385 or -300647.

## Decision

-691624 < -551385. The claim is strictly better than the bar by 140239, which is 25.43 % of |bar|. It is not a tie.

Nothing found posts a value for this exact cell other than PR #87 (-551385) and PR #64 (-300647).

The margin is plausible: PR #87's own description says its method is weakest at lambda 1e-2, with a 31.6 % mean gap to the published a050 values.

novelty: strictly beats every known value for a200_t10_orig_b050_l1e-02 (bar -551385, open QOBLIB PR #87; the official table has no row)

## Fetch log (UTC start time from `date -u`; sha256 of the saved response body)

| # | URL | fetched (UTC) | HTTP | bytes | sha256 |
|---|---|---|---|---|---|
| 01 | https://raw.githubusercontent.com/ZIB-AOPT/QOBLIB/main/06-portfolio/solutions/README.md | 2026-10-14 17:24:41 | 200 | 10450 | `05a6d23392d960fb16028cc1e9ba8d7547aa445a0e3f30c433f5f4acab56c09a` |
| 02 | https://api.github.com/repos/ZIB-AOPT/QOBLIB/pulls?state=open&per_page=100 | 2026-10-14 17:24:54 | 200 | 461323 | `9f2351223d48cb59a41245f5e0ac3fcff70a8030642076e3f65c9a496541492a` |
| 03 | https://api.github.com/repos/ZIB-AOPT/QOBLIB/pulls?state=closed&per_page=50 | 2026-10-14 17:25:43 | 200 | 882202 | `459fa39c5f8541f7f6c43b5e9283c950e61a6138f848d04bbc038841148d8d04` |
| 04 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-14 17:26:14 | 200 | 520525 | `d5822135419b495a3de25133a4ad289b0d8e90df7e54e9e751f8b8a00b68bff5` |
| 05 | https://api.github.com/repos/mnn31/QOBLIB/git/trees/1772e1d7f5341b1b87f7e66029cf143b075ca259?recursive=1 | 2026-10-14 17:26:46 | 200 | 5295601 | `a6b6de6f5980804ad0c3836177a21ed9e12e254dc928a631d4ee0163849de251` |
| 06 | https://raw.githubusercontent.com/mnn31/QOBLIB/1772e1d7f5341b1b87f7e66029cf143b075ca259/06-portfolio/submissions/20261009_RestrictedChainDP_Gupta/a200_t10_orig_b050_l1e-02/a200_t10_orig_b050_l1e-02_solution.sol | 2026-10-14 17:27:28 | 200 | 3746 | `df44335103ccd97d7110b456b22f082cc7df8ca8f9a4ede8d319f4be6064f561` |
| 07 | https://raw.githubusercontent.com/mnn31/QOBLIB/1772e1d7f5341b1b87f7e66029cf143b075ca259/06-portfolio/submissions/20261009_RestrictedChainDP_Gupta/a200_t10_orig_b050_l1e-02/a200_t10_orig_b050_l1e-02_summary.csv | 2026-10-14 17:27:29 | 200 | 1950 | `c4c4a7636d5a0ac07d56c36d9499ce83568861da17c7af4e501a848b658072a9` |
| 08 | https://api.github.com/repos/marcinjkaminski/QOBLIB-4colors/git/trees/e2fefab5060ea7f65fd906048d8dcb98b02643ed?recursive=1 | 2026-10-14 17:27:41 | 200 | 5672770 | `4b0e3bfde99e2005f5d36805bef41be6b27746db6a053999c03c34f0ccc9e17f` |
| 09 | https://raw.githubusercontent.com/marcinjkaminski/QOBLIB-4colors/e2fefab5060ea7f65fd906048d8dcb98b02643ed/06-portfolio/submissions/20260908_4colors-Optimizer_4colors/a200_t10_orig_b050_l1e-02/a200_t10_orig_b050_l1e-02_solution.sol | 2026-10-14 17:27:58 | 200 | 3999 | `6224003b825a010a50bcc86681379f22c0e9d30fd2be1c3b0f2f49eb6fc29955` |
| 10 | https://raw.githubusercontent.com/marcinjkaminski/QOBLIB-4colors/e2fefab5060ea7f65fd906048d8dcb98b02643ed/06-portfolio/submissions/20260908_4colors-Optimizer_4colors/a200_t10_orig_b050_l1e-02/a200_t10_orig_b050_l1e-02_summary.csv | 2026-10-14 17:27:59 | 200 | 1232 | `0aba009feef8a90289574548f1aaef3165ec2ddf99c90aa80370aa0b73d2e315` |
| 11 | https://api.github.com/repos/mnn31/QOBLIB/git/trees/b7359bb00be23ea7ba57aa1f1c557241e26ec725?recursive=1 | 2026-10-14 17:28:09 | 200 | 4985842 | `78c6906afbfa78702f8a21e3e53b0a2fa103c8119421984ee14b81fa3cbde440` |
| 12a | https://api.github.com/repos/ZIB-AOPT/QOBLIB/issues/87/comments?per_page=100 | 2026-10-14 17:28:39 | 200 | 68135 | `5ef1c0c6b4e615ea062c7daf2d8b82de3496a7e707fde4532448e1d5451fdf8b` |
| 12b | https://api.github.com/repos/ZIB-AOPT/QOBLIB/issues/64/comments?per_page=100 | 2026-10-14 17:28:40 | 200 | 82622 | `4b8dd6823ec4e011aa103b20457019ac64e4cbaf833fd5270e256bba2f74f45e` |
| 13 | https://export.arxiv.org/api/query?search_query=all:QOBLIB&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 2026-10-14 17:30:03 | 429 | 14 | `467622e2f17f01d302d6c790b13078569f17d71cd83910558535019a594e07c1` |
| 14 | https://export.arxiv.org/api/query?id_list=2504.03832,2607.03218,2605.17623,2509.17876,2609.15708,2512.22001,2606.12612&max_results=20 | 2026-10-14 17:31:21 | 503 | 126 | `c00c6211c3a751584bab0a350d56272b60172019c648cf74a73ae4f9f319602e` |
| 15 | https://api.semanticscholar.org/graph/v1/paper/arXiv:2504.03832/citations?fields=title,year,externalIds,publicationDate&limit=1000 | 2026-10-14 17:32:16 | 200 | 14955 | `2e67a82f675e6a73da51feba112819c4a20cbbe9f9bb7a6e8b0f287fb1b4a226` |
| 16 | https://raw.githubusercontent.com/mnn31/qoblib-solvers/main/portfolio/README.md | 2026-10-14 17:32:18 | 200 | 4256 | `f440b833ad5ea16cf3138152759de89278ae789c36758d0330637bfa85eaf3cd` |
| 17 | https://raw.githubusercontent.com/Quantum-Global-Group/qoblib-dashboard/main/src/data/generated/qoblibPortfolioBestKnown.json | 2026-10-14 17:32:19 | 200 | 19465 | `33fd141ba872aa97e47836e8c0803d27a5d02017d71f88acef4b218d8abe90ba` |
| 18 | https://zenodo.org/api/records?q=QOBLIB&size=100&sort=mostrecent | 2026-10-14 17:32:20 | 400 | 207 | `8105c5098c3b8051ed4e35cc510a7c4af8dcca8edb46986c9a37ba5469c6985c` |
| 19 | https://raw.githubusercontent.com/mnn31/qoblib-solvers/main/portfolio/results/README.md | 2026-10-14 17:33:00 | 200 | 4508 | `1618739ca2fa13e29c9752d534c022cc606202ec1f2d03d1c48dcac103f8cc6b` |
| 20 | https://arxiv.org/abs/2504.03832 | 2026-10-14 17:33:14 | 200 | 49975 | `c99d4be0a46ff34365a3b9231f726859b08c2b5289ff16eb4c0b058c5b446df0` |
| 21 | https://arxiv.org/html/2504.03832v2 | 2026-10-14 17:33:25 | 200 | 1082694 | `e942ae571e805e3e7c983bc930621a8c86f00569e196627162fa21df755efff1` |
| 22 | https://arxiv.org/html/2504.03832v1 | 2026-10-14 17:34:02 | 200 | 1057106 | `bf3993ac23cd4ba7d7060e0fc27f91310ea8833b479d77764a69d8d4ca787f1c` |
| 23 | https://api.semanticscholar.org/graph/v1/paper/search?query=QOBLIB&fields=title,abstract,year,publicationDate,externalIds&limit=100 | 2026-10-14 17:34:43 | 429 | 174 | `65ab993d12c5c2cc9b68e6da2bb79b326930283e520363ffcdc145f88cd5a148` |
| 24 | https://api.semanticscholar.org/graph/v1/paper/search?query=QOBLIB%20portfolio%20optimization%20benchmark&fields=title,abstract,year,publicationDate,externalIds&limit=100 | 2026-10-14 17:34:46 | 429 | 174 | `65ab993d12c5c2cc9b68e6da2bb79b326930283e520363ffcdc145f88cd5a148` |
| 25 | https://arxiv.org/abs/2605.17623 | 2026-10-14 17:35:00 | 200 | 43403 | `1bc9a41f699a92ebbaccc97e3869efa8cb9e7c65f028760ae1d920ceee8bdd9f` |
| 26 | https://arxiv.org/abs/2510.27117 | 2026-10-14 ~17:35 | none (interrupted before any response header; not re-requested) | 0 | n/a |
| 27 | https://arxiv.org/abs/2610.10772 | 2026-10-14 17:57:45 | 200 | 44566 | `c3700ef2f1b213b446578669547af2e4f11671b137e665ce92eaeb992d724a4a` |
| 28 | https://arxiv.org/abs/2606.10098 | 2026-10-14 17:57:50 | 200 | 43676 | `ee3e92ad7f50ef52101832f4a4291f7becd5f2b7b29bde129ba0f047315f8a63` |
| 29 | https://arxiv.org/abs/2603.13607 | 2026-10-14 17:57:54 | 200 | 42781 | `32c5955afb3c3ddaa5aac291490bbaa806b447f7d9f6df78746331ac0a49837e` |
| 30 | https://arxiv.org/abs/2604.25162 | 2026-10-14 17:57:59 | 200 | 43411 | `eaa917d9d7b09077ed8a96e04fbfd3024ff27c154ac25bdb7611c947d379215a` |
| 31 | https://arxiv.org/abs/2608.28842 | 2026-10-14 17:58:04 | 200 | 40721 | `c78cda7db8bc48e2fc2c77da0902e56edc1f6da7ed209a78e76290390d1ff524` |
| 32 | https://arxiv.org/abs/2512.22001 | 2026-10-14 17:58:10 | 200 | 44045 | `da89571f6e29f484f8a95f90efe97923a1f3a23a38b3bfe8bca6878df4d671dc` |
| 33 | https://arxiv.org/abs/2607.03218 | 2026-10-14 17:58:15 | 200 | 42663 | `b0f0679842480f8a0b61db23b2003f252ca4505e597f8ecf230864930cd93a9f` |
| 34 | https://arxiv.org/abs/2609.15708 | 2026-10-14 17:58:20 | 200 | 42684 | `c9492fae4e4b888d6926cd6e90c2743b5360018122b28d29b09ad6df5ff358bf` |
| 35 | https://pmc.ncbi.nlm.nih.gov/articles/PMC13293884/ | 2026-10-14 22:12:55 | 200 | 388178 | `2b9e51662db9764734ad56e9762003b8def02911181d6a14581b8bb04a8855a2` |
| 36 | https://zenodo.org/api/records?q=QOBLIB&size=25&sort=mostrecent | 2026-10-14 22:13:35 | 200 | 20868 | `d374bd0c7ffb40a670902424c9444c324704d50b5d1dcb18fbb7776be0b24b1b` |
| 37 | https://api.github.com/search/repositories?q=QOBLIB&per_page=100 | 2026-10-14 22:13:37 | 200 | 75585 | `f22aaf188e12036ef3f57f4e9beb9f11d1c15a432058ef46021291e2994d679c` |
| 38 | https://raw.githubusercontent.com/KenWuqianghao/qoblib-solvers/main/README.md | 2026-10-14 22:14:21 | 200 | 21333 | `09b663a71af68a47c241a5e0445ba0331cca0743d1e717ecb5fef42ac88910df` |

Web searches (search tool, no direct fetch) covered:
- QOBLIB portfolio a200 best known;
- "po_a200_t10_orig";
- "a200_t10_orig_b050_l1e-02";
- QOBLIB multi-period portfolio results 2026;
- the solver repos of the PR #87 and PR #64 authors;
- QOBLIB 06-portfolio 200 assets lambda 0.01;
- Zenodo QOBLIB portfolio;
- GFORS (2510.27117).

None found a value for this cell other than PR #87.

pass: true
