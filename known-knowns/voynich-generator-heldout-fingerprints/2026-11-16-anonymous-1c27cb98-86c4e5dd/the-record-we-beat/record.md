# The record we beat (target: voynich-generator-heldout-fingerprints, outcome (B))

Status source (fetched by the run's scout, one honest GET, no retries):
- URL: https://www.voynich.nu/transcr.html
- Fetched: 2026-11-16T11:42:08Z (UTC)
- HTTP status: 200
- Page sha256: 57f8aaf6b1cdd6a292361b3a94e723f8fb14f0960b2cb349acee142fbadb19a5 (saved in the run's data/transcr.html)

The published record the falsification is judged against (the "table" for this target is the
pre-registered 99.9% Voynich quire-bootstrap envelope of the H1 statistic, computed at
verification time from ZL3b-n.txt / IT2a-n.txt, plus the published Naibbe point estimate):
- Published Naibbe H1 (edit-1 adjacency ratio), single-corpus, from arXiv 2608.17096
  (Rozanova & Temerev, 2026) Table 4: Naibbe (Caesar) 0.82 vs Voynich 1.12 (A 1.20, B 1.07).
  This is the pre-cutoff record; the claim's new object is the pooled, both-dialect,
  both-transliteration, 99.9%-Voynich-quire-bootstrap-envelope falsification (see
  criterion_verbatim.txt in this folder for the verbatim success criterion).
- The run's reproduced Naibbe H1 (pinned driver, token-identical): 0.825 (vs published 0.82).
- The run's recomputed observed Voynich H1: A 1.197/1.238, B 1.067/1.066 (ZL3b/IT2a) vs
  published 1.20/1.07 (reproduction gate, within +/-0.05).

The falsification (this claim): pooled unmodified Naibbe H1 = 0.7981 (A-mode) / 0.7917
(B-mode), OUTSIDE (below) the 99.9% Voynich quire-bootstrap envelope in all four
(dialect x transliteration) cells and below the minimum of all 16,000 Voynich quire-bootstrap
controls (global min 0.8990).
