# The record we beat (metadata only)

No third-party page is copied here. Each row records one plain HTTP GET (`User-Agent: V3R1T4S-Research-Scout/1.0`, zero retries) during live scouting.

| Source | URL | UTC fetch time | HTTP status | sha256 of fetched page | Extracted status / value |
|---|---|---|---|---|---|
| Wikipedia Percolation threshold | https://en.wikipedia.org/wiki/Percolation_threshold | 2026-11-18T05:50:23Z | 200 | `809405d5d4879a9ce4c4754fdadf47ecbef6f085bb8f6661aea7fed1866ccfd5` | High-dimension hypercubic bond/site series end at `4855/12 sigma^-6` and `119077/96 sigma^-6` (Mertens & Moore 2018) |
| Mertens & Moore (`arXiv:1805.02701` abs) | https://arxiv.org/abs/1805.02701 | 2026-11-18T05:50:22Z | 200 | `90f03436a0fffd90851c8fbe9f4b4ee045c396950f20c23c696defa532119d16` | J. Phys. A 51 (2018) 475001; closed formulas only through `[binom(d, e-2)] D_e(q)` (Theorems 4–6) |
| Mertens & Moore (`arXiv:1805.02701` TeX source) | https://arxiv.org/e-print/1805.02701 | 2026-11-18T05:50:22Z | 200 | `c2277e76b34fa4cab645e15c949eadae6adfb8aabbd3b68c017eb07c4492a2cf` | Section 8 & Table 9 state `[binom(d, e-3)] D_e(q)` is open; Table 9 estimates `(9, 12)` at `4.5` years and `(11, 14)` at `133,800` years |
| Luther & Mertens (`arXiv:1705.03688` TeX source) | https://arxiv.org/e-print/1705.03688 | 2026-11-18T05:52:55Z | 200 | `3301370a76b1270cb83aaa2ad4c311a834291147ca39484504e91873d878b4ed` | Site polycube perimeter formulas only through `k = n - 1` and `k = n - 2` |
| V3R1T4S pull requests (`state=all`) | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100 | 2026-11-18T06:21:36Z | 200 | `6bdf40e58a446854255fd1987e3984df6e96af4f3b0af388e3a0b5e3b1744e5d` | Zero open or closed PRs on `hypercubic-percolation-1-over-d-series-next-term` |
