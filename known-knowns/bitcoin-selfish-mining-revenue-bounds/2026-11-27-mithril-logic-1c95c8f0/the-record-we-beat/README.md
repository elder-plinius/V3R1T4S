# The record we beat (snapshot record, not the page)

- Source: https://arxiv.org/abs/1507.06183 (SSZ, "Optimal Selfish Mining Strategies in Bitcoin"), abstract page.
- UTC fetch time (NOVELTY skeptic): 2026-11-27T02:39:24Z, HTTP 200, page sha256 17034454c06d20f055d997a07fbfc9beed99e36376db3c3425e0f1cf51d99d99 (same as the contributor's 2026-11-27T01:50:26Z fetch). Submission history on the page: v1 22 Jul 2015, v2 23 Jul 2015.
- Selected headers (contributor HEAD request, 2026-11-27T03:14:42Z): HTTP/2 200; content-type: text/html; charset=utf-8; last-modified: Mon, 24 Aug 2026 19:33:27 GMT.
- The abstract page holds no table. The value comes from the paper PDF fetched from arXiv: sha256 0cc1fdc04eb5c925e294eff74dc5388f2921b6cd8164985b29dae4cf34da2b34.
- Extracted cell, Table 2 (gamma = 0, T = 95, epsilon = 1e-5), row alpha = 0.45: lower 0.65177 / epsilon-OPT 0.66891 / upper bound 0.70109. Bank bar: 0.70099 (1e-4 below 0.70109).
- Neighbouring items checked by the NOVELTY skeptic (see panel/novelty.md): open PR #814 claims 0.70099 with T = 95; arXiv 2607.24415 concerns a different question.
