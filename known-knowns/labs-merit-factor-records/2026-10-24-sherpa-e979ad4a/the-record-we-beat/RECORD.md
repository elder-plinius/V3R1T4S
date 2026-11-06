# Table and source fetch records (one plain request each; copied from the run's command output)

| source | URL | fetched (UTC) | HTTP | sha256 of the saved file |
|---|---|---|---|---|
| archive `results-2016/2004-Knauer-original.txt` @ 1aa1234 | https://github.com/borkob/git_labs | 2026-10-24T15:12:35Z (gh api, raw) | 200 | 35538ed93257b4131eb93cc548bdd2d4e9d29b677533cd39f6c0882863df57c7 |
| Bošković et al. archive `results-2018/2018-labs-skew.txt` @ 1aa123407636e48630174e0bf122037e369c1d68 | https://github.com/borkob/git_labs | 2026-10-24T15:12:34Z (gh api, raw) | 200 | 1719cd1cf2544f197a621353795c6eef1600479124714682a06eecf14bedd4c1 |
| Dimitrov arXiv:2206.12070 source (e-print) | https://arxiv.org/e-print/2206.12070 | 2026-10-24T15:16:31Z | 200 | 79806b61419d8ace9351322122bebef2408ea191651b725d4986c3376e53f13a |
| Brest & Bošković arXiv:2011.00068v1 source | https://arxiv.org/e-print/2011.00068v1 | 2026-10-24T15:18:39Z | 200 | 7ee37bda33c8b8175e448c146f059661f508fa201511c5e2daabbc445a24deb4 |
| arXiv:2504.00987v2 source (e-print) | https://arxiv.org/e-print/2504.00987v2 | 2026-10-24T19:23:22Z | 200 | bc0b444f8dddf0a13c28c5e4ee8a75cc034befada7231d4047797af80c72f5cd |
| arXiv:2607.09688v1 source (e-print) | https://arxiv.org/e-print/2607.09688v1 | 2026-10-24T19:23:23Z | 200 | 738c297c53b58cbd7ed4cddd7a05f25e379604427d201e2354471bebe47b43a0 |
| arXiv API search for newer results | https://export.arxiv.org/api/query (query in CLAIM.md) | 2026-10-24T19:23:23Z | 200 | fa4754f6b038a073b7c5e30f620bb9d6b5c7327d1c5ecd86a3492b1ffdd6276e |
| borkob/git_labs tree at 1aa1234 | gh api repos/borkob/git_labs/git/trees/1aa1234...?recursive=1 | 2026-10-24T19:23:23Z | 200 | a97e628d75e78653700e442e8340511b1b79bc7039c75bb3f47b78be6ebae222 |
| arXiv:2011.00068v2 source | https://arxiv.org/e-print/2011.00068v2 | 2026-10-24T15:18:39Z | 200 | 886de15b957bf120724b4369c88a99e5d891f437b394cfea914944de391df79b |
| arXiv:2210.15962 source | https://arxiv.org/e-print/2210.15962 | 2026-10-24T15:19:37Z | 200 | 7217b1d4ed4b0ec421956a72c527f715c4a23f5bd3a4161f83c88b73ca7af179 |
| arXiv:2409.07222v1 source | https://arxiv.org/e-print/2409.07222v1 | 2026-10-24T19:55:39Z | 200 | 09b0825c5b7a9fef03f18654399a20f9639b0e131e3054f80a55a8282569b76d |
| archive `results-2016/2004-Knauer-original.txt` @ 1aa1234 | https://github.com/borkob/git_labs | 2026-10-24T15:12:35Z (gh api, raw) | 200 | 35538ed93257b4131eb93cc548bdd2d4e9d29b677533cd39f6c0882863df57c7 |
| archive `results-2016/2004-Knauer-original.html` @ 1aa1234 | https://github.com/borkob/git_labs | 2026-10-24T19:56:33Z (gh api, raw) | 200 | fb4c6009ef0662eb90fa56429f05c812d8ee4117752f2c821ed3bee77b691bc9 |
| ERK'2025 paper (Pšeničnik, Bošković, Brest) | https://erk.fe.uni-lj.si/2025/papers/psenicnik(integer_partitions).pdf | 2026-10-24T20:21:40Z | 200 | 72574b63061ac62707b26b77c02698ef20ac8d0bcde1956e9f7060a443149605 |

## Notes

- The arXiv status page (arXiv:2607.09688) reports values for 450 <= L <= 527 and L = 573 only, so it lists nothing at L = 401.
- `2004-Knauer-original.txt`: the GitHub CLI re-encoded this file from Latin-1 to UTF-8 on download (sha256 89385bc8c3842523bd2b581b1a7a93badb44bd598f84bf09e2249bd11fde73c8). The stored copy was converted back to the original bytes, whose git blob sha1 ca0e6869a97177496462d567357047a503d2c359 equals the tree listing's.


## Extracted cells at L = 401 (no third-party page or PDF is copied into this package)

| source | L = 401 energy | how read |
|---|---|---|
| ERK'2025, Pšeničnik, Bošković, Brest, Figure 2 (sha256 of the PDF above) | 11000 (F = 7.3091) | vector data of the figure, calibrated on the five Table 3 values (`how-we-built-it/code/read_erk2025_fig2.py`) |
| arXiv:2206.12070 (Dimitrov) | 11456 | witness decoded from the TeX source and recomputed |
| arXiv:2011.00068v1 (Brest & Bošković) | 11472 | witness decoded (typeset space removed) and recomputed |
| borkob/git_labs `results-2018/2018-labs-skew.txt` (named in the criterion) | 11888 | witness recomputed |
| arXiv:2607.09688v1, arXiv:2504.00987v2 (named), arXiv:2409.07222v1, arXiv:2210.15962 | no L = 401 value | table rows extracted from each TeX source |
