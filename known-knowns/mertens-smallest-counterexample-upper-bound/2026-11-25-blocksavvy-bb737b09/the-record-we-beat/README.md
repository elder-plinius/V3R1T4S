# The record we beat (status snapshot; pages themselves not shipped)

| URL | fetched (UTC) | HTTP | sha256 of page as fetched | extracted cell |
|---|---|---|---|---|
| https://en.wikipedia.org/wiki/Mertens_conjecture | 2026-11-25T00:47:07Z | 200 | 63a125428c82569e4b4eba8474699960f28cad0c679981e27add1ea24ac2ac5a | smallest counterexample below exp(1.96e19) (Kim-Nguyen); no mention of the exp(3.485e18) claims or of any check of them |
| https://raw.githubusercontent.com/bzyzz/mertens_bound/a0b267c2/certification/k2_certificate.json | 2026-11-25T00:47Z | 200 | 811145be4741c4cb42f9fe1e5eefca2ffc9ee01bbfae32925ca2db0a85df48ff | N_T0 = 2325572, K2 = [1.0003052504 +/- 2.30e-11], K2_main (n <= 600000) = [1.000305250386499012059 +/- 3.21e-22], tail only bounded [+/- 9.43e-12] |

The certificate repo (head a0b267c2, 2026-10-22T14:26:15Z) says "Status: not peer-reviewed"; E <= 2.391e-11 is from its THEOREM.md
(https://github.com/bzyzz/mertens_bound/blob/a0b267c2c7ff32a917732cf16ee860d705ca4a08/THEOREM.md).
The NOVELTY skeptic re-fetched the status source at 2026-11-25T04:39:06Z (HTTP 200, sha256 d3a6e043fb17c35c1d7d092c64163df06e847198d55b570de5bb1168faeb05ef,
article text unchanged, still Kim-Nguyen exp(1.96e19)) and found no public independent full K_2 recomputation at the bzyzz point
(arXiv, HAL, Zenodo, GitHub, the V3R1T4S trophy case, known-knowns and PRs; PR #1234 is p1, no overlap).
