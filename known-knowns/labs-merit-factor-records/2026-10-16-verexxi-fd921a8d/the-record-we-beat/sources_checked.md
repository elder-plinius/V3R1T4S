# Sources checked for L = 242

| source | url | fetched (UTC) | HTTP | lengths it tabulates | row for L? |
|---|---|---|---|---|---|
| 1406.5301 | https://arxiv.org/src/1406.5301 | 2026-10-16T17:00:34Z | 200 | 16 lengths in 181..401 | no |
| 1512.02475 | https://arxiv.org/src/1512.02475 | 2026-10-16T17:00:30Z | 200 | 16 lengths in 67..119 | no |
| 2011.00068 | https://arxiv.org/src/2011.00068 | 2026-10-16T17:00:27Z | 200 | 52 lengths in 201..303 | no |
| 2106.03377 | https://arxiv.org/src/2106.03377 | 2026-10-16T17:03:57Z | 200 | 1 lengths in 449..449 | no |
| 2206.12070 | https://arxiv.org/src/2206.12070 | 2026-10-16T17:00:24Z | 200 | 330 lengths in 172..1006 | yes |
| 2210.15962 | https://arxiv.org/src/2210.15962 | 2026-10-16T17:00:21Z | 200 | 17 lengths in 171..247 | no |
| 2409.07222 | https://arxiv.org/src/2409.07222 | 2026-10-16T17:00:17Z | 200 | 77 lengths in 450..527 | no |
| 2504.00987 | https://arxiv.org/src/2504.00987 | 2026-10-16T17:00:14Z | 200 | 16 lengths in 92..120 | no |
| 2607.09688 | https://arxiv.org/src/2607.09688 | 2026-10-16T17:00:10Z | 200 | 35 lengths in 450..573 | no |
| knauer2004 | https://raw.githubusercontent.com/borkob/git_labs/1aa123407636e48630174e0bf122037e369c1d68/results-2016/2004-Knauer-original.html | 2026-10-16T17:04:54Z | 200 | 262 lengths in 10..304 | yes |

Not readable in this run (PENDING SOURCE CHECK): the git_labs tree listing (github.com 403 from the session proxy),
git_labs results-2016/Merit_Factor_Records-2013-even.html and -odd.html (404 at the paths linked from the Knauer page),
Mertens' open.dat (DNS failure), labraj.feri.um.si (proxy 403), the arXiv API listing (export.arxiv.org 429),
journal-only versions (IEEE Access 2018, MENDEL 2022, Digital Signal Processing 2025, J. Comput. Sci. 2024; hosts unreachable).
arxiv.org itself answered 429 to a search page at about 17:11:35Z; under the human's host rule arxiv.org was not used
again in this run (the TeX sources above were fetched before that). github.com answered 403 at preflight and was not used again.

Statements in the read sources about what was published before them (quoted from the TeX sources fetched above):
- arXiv:2607.09688 (June 2026): "Local search methods in [boskovic17, dimitrov22] have produced sequences with a merit
  factor exceeding 8.0 for 172 <= L <= 268, and exceeding 7.0 for 172 <= L <= 527." Its own table covers 450..527 and 573.
- arXiv:2206.12070 (Dimitrov et al.): "we were able to improve all the results, for all skew-symmetric lengths in the
  range 225-451, announced in literature and reached by using a supercomputer grid."
- arXiv:2210.15962: its solver "found all the known and seven new best-known skew-symmetric sequences for odd instances
  from L=121 to L=223" and was run up to L=247 (comparing against Knauer04, Boskovic17, Brest22).
