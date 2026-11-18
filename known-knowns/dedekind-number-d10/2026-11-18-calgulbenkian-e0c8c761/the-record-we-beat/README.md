# The record we beat (metadata only)

No third-party page is copied here. Each row records one plain HTTP GET (`User-Agent: V3R1T4S-research/1.0`, zero retries) during live scouting.

| Source | URL | UTC fetch time | HTTP status | sha256 of fetched page | Extracted status / value |
|---|---|---|---|---|---|
| OEIS A000372 HTML | https://oeis.org/A000372 | 2026-11-18T07:50:22Z | 200 | `8e3c908ad2471ff400bee43d8455b0c9ec3035ee3da407337255157bda33a8dc` | Sequence ends at `a(9) = 286386577668298411128469151667598498812366`; keyword `nonn,nice,more`; `a(10)` and prime-power congruences for `a(10)` unlisted |
| OEIS A000372 JSON | https://oeis.org/search?q=id:A000372&fmt=json | 2026-11-18T07:50:22Z | 200 | `42c452b7999076d899c44725bde34bdd0eeb940e94e17eba5ab649ce96308760` | Zero prime-power congruences for `a(10)` in comments, formulas, links, or cross-references |
| Pawelski-Szepietowski 2023 (`arXiv:2302.04615`) | https://arxiv.org/abs/2302.04615 | 2026-11-18T07:50:22Z | 200 | `58dfe30532f53ff3b55932a4c669f0cbf517b5d7f752483c1ba8c37a0b990fbe` | Proves `D(9) == 6 (mod 210)` only; cites Yamamoto's even-`n` parity `D(2m) == 0 (mod 2)` |
| Pawelski-Szepietowski-Szepietowski Nov 2026 (`arXiv:2611.13887v1`) | https://arxiv.org/abs/2611.13887 | 2026-11-18T07:50:23Z | 200 | `c25cdade671f06642d12543a2b4cd7d15988a9a1ba51e2db3cbb9523c477ae23` | Proves squarefree congruences `D(10) == 106 (mod 210)` (`0 mod 2, 1 mod 3, 1 mod 5, 1 mod 7`) via `|X| == |Fix(G, X)| (mod p)`; zero prime-power congruences `mod p^k` (`k >= 2`) |
| Companion repository `bpawelski/dedekind_congruences` | https://raw.githubusercontent.com/bpawelski/dedekind_congruences/main/README.md | 2026-11-18T07:50:23Z | 200 | `c9ac1bf9f569fc89b12d7b46ac3774093af3d48fe744b46d3064a8c6781627d5` | Confirms only prime moduli `2, 3, 5, 7` (`d_10 == 106 mod 210`, `phi_10((1..9)) = 1702659955`, `|P_3^Q| = 6526`) |
| Fihman-Van Hirtum-Plessl July 2026 (`arXiv:2607.08446`) | https://arxiv.org/abs/2607.08446 | 2026-11-18T07:50:23Z | 200 | `0c82d971d824d80b3201fca4b59c350a17af5c292190681317e3f7c653ffcf87` | Statistical 4-digit estimate of `D(10)` only; no exact modular congruences |
| V3R1T4S pull requests (`state=all`) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100 | 2026-11-18T07:50:23Z | 200 | `6bdf40e58a446854255fd1987e3984df6e96af4f3b0af388e3a0b5e3b1744e5d` | Zero open or closed PRs on `dedekind-number-d10` |

Compared cell: `D(10) mod 27` (`3^3 = 27`), completely undetermined by OEIS `A000372`, `arXiv:2302.04615`, and `arXiv:2611.13887v1` (which left `9` possible residues `{1, 4, 7, 10, 13, 16, 19, 22, 25} mod 27`). Our certificate establishes `D(10) == 16 (mod 27)` (and `D(10) == 7 (mod 9)`), while reproducing `D(9) == 24 (mod 27)`.
