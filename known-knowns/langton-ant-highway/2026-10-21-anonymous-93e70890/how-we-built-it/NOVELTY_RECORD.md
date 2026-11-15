# NOVELTY_RECORD

## Status source (bank status_source for langton-ant-highway)
URL: https://arxiv.org/pdf/2505.05426 (abstract page https://arxiv.org/abs/2505.05426 fetched)
| URL | UTC | HTTP | file | bytes | sha256 |
|---|---|---|---|---|---|
| https://arxiv.org/abs/2505.05426 | 2026-10-20T23:09:38Z | 200 | data/status/arxiv_2505.05426_abs.html | 38195 | 9d5f01827af97b964dc29f3c2a2c156d203f7395cdfee8277895f022e1db3a76 |
Read: "[2505.05426] Sideways on the highways", only [v1]; abstract: "This limits the well known Highway conjecture on Langton's ant as it shows that a generalised version of this conjecture generically does not hold on generalised ants." The classical conjecture is treated as open.

## Other sources noted by earlier runs (2026-10-16; record pages / abstracts only, not full texts)
- Zenodo 10.5281/zenodo.21716510 (record page only): the conjecture "remains OPEN"; reports excluding other periodic highways of period <= 48 (self-reported).
- arXiv 2606.26677 (abstract only): confinement / escaping-time bounds and a "backtracking branching strategy"; not about exhaustive highway capture in boxes.
No published exhaustive box search with highway certificates at 6x6 was found by those runs; a reviewer should search again (last 24 months, and the V3R1T4S repo TROPHY_CASE.md / open pull requests).

## Target text (verbatim, V3R1T4S bank)
statement: "Conjecture: from every finite initial configuration of black cells, Langton's ant eventually builds the period-104 diagonal highway. It is proven that the ant's trajectory is always unbounded (Cohen-Kong), but not that it always reaches the highway."
p1: "Exhaustive verification of all initial configurations in a 6x6 (or larger) box under a stated symmetry reduction, each with a highway-capture certificate (window at t equals window at t+104 shifted by (+-2,+-2), ant beyond all black cells, and no initial black cell anywhere in the future sweep of the highway) re-checked by an independent simulator on a random 1% sample plus all hard cases."

## Credits
Langton's ant: C. G. Langton (1986). Unboundedness: Bunimovich and Troubetzkoy; Cohen and Kong. Highway conjecture literature as above (V. Lutfalla, arXiv 2505.05426).
