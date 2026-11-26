# The record we beat (metadata only)

No third-party page is copied here. Each row records one plain HTTP GET (`User-Agent: V3R1T4S-Research-Scout/1.0`, zero retries) during live scouting.

| Source | URL | UTC fetch time | HTTP status | sha256 of fetched page | Extracted status / value |
|---|---|---|---|---|---|
| OEIS A005271 HTML | https://oeis.org/A005271 | 2026-11-18T05:50:21Z | 200 | `57485a625af607e78a38e8e107b4f9c70da8d17f47932f18706277987b38d821` | Sequence ends at `a(7) = 391689748492473664721077609089` (revision 68, `2026-05-30`); keyword `nonn,hard,more,nice`; `a(8)` and `a(8) mod p` (`p >= 3`) unlisted |
| OEIS A005271 JSON | https://oeis.org/search?q=id:A005271&fmt=json | 2026-11-18T05:50:22Z | 200 | `f709375e16328959c0a589dd0abd90daeff8e248a086725c0cbdaea34efd640c` | Zero odd-prime congruences for `a(8)` in comments, formulas, links, or cross-references |
| OEIS A005271 b-file | https://oeis.org/A005271/b005271.txt | 2026-11-18T05:50:22Z | 200 | `c8da5b8d8f3bc4cb02ecf4eb925199c32b1e1e8404b4a8eb9c889fd640fab23d` | `1..7` only (`a(7) = 391689748492473664721077609089`) |
| J. Propp (`arXiv:math/9801061`) | https://arxiv.org/abs/math/9801061 | 2026-11-18T05:50:22Z | 200 | `bc91cc026b365f35199b3138ff06b91f489c85d493d2a5edefc81f91fef31df7` | Problem 20 progress report gives Lovasz parity `a(n) == n (mod 2)` via coordinate reflections; no odd-prime congruences |
| V3R1T4S pull requests (`state=all`) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100 | 2026-11-18T06:21:36Z | 200 | `6bdf40e58a446854255fd1987e3984df6e96af4f3b0af388e3a0b5e3b1744e5d` | Zero open or closed PRs on `hypercube-q8-perfect-matchings` |

Compared cell: `A005271(8) mod 5` (previously unknown in OEIS `A005271`, Propp `arXiv:math/9801061`, Ostergard-Pettersson 2013, and citing literature). Our certificate establishes `A005271(8) == 3 (mod 5)` via the exact Sylow `5`-subgroup fixed-point count `|Fix_{M(Q_8)}(P_5)| = 743141892135168`.
