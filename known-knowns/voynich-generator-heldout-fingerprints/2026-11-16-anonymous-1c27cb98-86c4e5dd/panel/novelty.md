context: subagent (fresh isolated OpenClaw subagent, given only claim/)

## Claim (scope as stated)

Outcome-(B) falsification of the unmodified Naibbe cipher (Greshko 2025, default parameters).
Claimed result: Naibbe run on 20 plaintexts (I01–I10 Italian, L01–L10 Latin) x 10 seeds, pooled
per mode (100 runs per mode, 3,049,192 tokens A / 3,057,200 tokens B) gives H1 (edit-1
adjacency-similarity ratio, the Timm-Schinner diagnostic as used in arXiv:2608.17096 Table 4)
of 0.7981215023387158 (A-mode) and 0.791668403014533 (B-mode) (objects/naibbe_batch.json,
fields "pooled.A.stats.H1" / "pooled.B.stats.H1"). Both are OUTSIDE (below) the 99.9%
Voynich quire-bootstrap H1 envelope in all 4 cells and below the minimum of all 16,000
bootstrap controls:

| cell (env files env_H1_*.json, B=4000 quire-bootstrap resamples each) | 99.9% envelope | bootstrap min | Naibbe below? |
|---|---|---|---|
| A / ZL3b | [1.0689697211, 1.3335351592] | 1.0650329877 | yes (A 0.7981, B 0.7917) |
| A / IT2a | [1.0270687806, 1.4341648178] | 1.0254637631 | yes |
| B / ZL3b | [0.9052727061, 1.2113006456] | 0.9037196957 | yes |
| B / IT2a | [0.9011753805, 1.2131119302] | 0.8989687544 | yes |

(null_H1_bootstraps.json holds the 16,000 per-cell control quantiles; the pooled values
0.7981/0.7917 are below every cell minimum and below every 95% envelope too.) Internal
arithmetic is self-consistent (per-plaintext H1 means 0.774–0.815 in objects/naibbe_batch.json
"per_ptext_H1" bracket the pooled values; per-run n_tokens 52,961 x 100 = 5,296,100 matches the
~5.3M-token streams; token counts in the README match the pooled file sizes). H1 is not among
the excluded statistics {edge-glyph coupling, singleton/hapax, 2604.19762 four signatures,
Greshko-2025 limitations}, and "20 plaintexts x 10 seeds" satisfies the volume requirement.

## Status source (one honest fetch)

URL: https://www.voynich.nu/transcr.html — HTTP 200, fetched 2026-11-16 13:59:34 UTC
(web_fetch; content-length consistent with the scout's 2026-11-16 11:42 UTC fetch, sha256
57f8aaf6b1cdd6a292361b3a94e723f8fb14f0960b2cb349acee142fbadb19a5, recorded in
status_source.txt). Value seen: the "Text Analysis - Transliteration of the Text" page is live
and current — it describes the main transliteration lineages (FSG/FG, Currier-D'Imperio/CD,
Takahashi/TT, Landini-Stolfi LSI) and, at the bottom, the link table to the main
transliteration files (ZL/TT/EVA etc.), i.e. the ZL3b/IT2a-n files the criterion's envelopes
must be computed from "as then published" are the published, up-to-date reference. No block;
one fetch only, as required.

## 24-month literature/code search (2024-11 to 2026-11), focused queries

- arXiv 2608.17096 (Rozanova & Temerev, v1 2026-08-17) — https://arxiv.org/abs/2608.17096 :
  full v1 HTML read. Its Table 4 / Table 7 (Appendix A.5) report the edit-1 ratio for
  "Naibbe cipher of Latin (Caesar)" = 0.82 (Pliny row: edge blank, no edit-1 value) against
  Voynich observed-spaces 1.12, weak-spaces-merged 1.14, Currier A 1.20, Currier B 1.07.
  That is a single-corpus (one Caesar plaintext, one stream), single-transliteration (ZL),
  point-estimate observation. The paper contains NO 99.9% envelope and NO per-cell
  (dialect x transliteration) H1 envelope (grep of full v1 HTML: "99.9" x0, "envelope" x0,
  "quantile" x0; CIs are 97.5/2.5 percentiles elsewhere). Its code mirror
  lrozanova/voynich-units (last push 2026-08-17, pre-cutoff) reproduces exactly those
  headline values; no H1 envelope files.
- arXiv 2604.19762 (Parisel, 4-signature test, v2 2026-06-16) — https://arxiv.org/abs/2604.19762 :
  Naibbe appears only as background (the two-class affix system, 2 mentions, 0 adjacency,
  0 edit-1, 0 envelope, 0 hapax/singleton in full v2 HTML). It tests slot-based and Cardan
  grille generators against the 4-signature joint criterion, not Naibbe, and not an
  edit-1 adjacency statistic. Not the claimed object.
- arXiv 2604.25979 (Parisel, Currier A/B switch, v2 2026-05-05) — https://arxiv.org/abs/2604.25979 :
  0 Naibbe mentions in full v2 HTML; its falsification target is a per-folio boolean
  vowel-switch, not edit-1 adjacency. Not the claimed object.
- greshko/naibbe-cipher — https://github.com/greshko/naibbe-cipher : post-2026-10-03 commits
  are 719f2f4c (2026-10-19) and 5145f526 (2026-11-04); both are .DS_Store-only updates
  (verified via commit patches). No post-cutoff claim about a 99.9% envelope or H1 falsification.
- SoylentAquamarine/voynich-collective PR16 "Audit the Naibbe cipher against the Voynich joint
  profile" — created 2026-09-19, merged 2026-09-19 (PRE-cutoff). Its falsifying content:
  16-block held-out edge-coupling test (Voynich +0.1871 vs generated Naibbe -0.0016 bits/
  boundary) + singleton-type gap (69.7% vs 40.5–41.7%) + H1/H2 and 64-merge reproduction.
  It reports that Naibbe matches Voynich H1/H2, i.e. the edge-coupling statistic, not the
  pre-registered 99.9% H1 envelope object; and it is pre-2026-10-03, so it cannot void
  novelty regardless. All 124 PRs in the repo were listed: no post-2026-10-03 PR claims a
  Naibbe 99.9%-envelope/adjacency-similarity falsification (post-cutoff PRs are Turenne
  crosswalks, ZL3a/3b source audits, steering minutes, show-through audits, etc.).
- Other 2024-11..2026-11 Voynich literature (arXiv listing scan, most-recent-first):
  2610.34499 (Zhang et al., 2026-10-25, v2 2026-11-04) "Calibrated Tests" — 0 Naibbe /
  0 adjacency / 0 envelope mentions (abstract read); 2610.08861 (Zenil & Uthamacumaran,
  2026-10-05) — AID/geometry reconstruction, 0 Naibbe, 0 99.9%; 2609.20835 (2026-07-28)
  pastiche grammar, pre-cutoff and different object; 2509.10573 (2025) directionality,
  pre-cutoff. arXiv "Naibbe" query returns 0 papers. GitHub "naibbe" search (4 repos):
  hermesj fork (2025), dninemfive/gnc (.NET reimplementation, 2026-03), tonielee31-ai/
  voynich-manuscript-ai-decoder (2026-04, claims Naibbe as decoding route — the opposite
  direction of a falsification).

## New vs known — precise

KNOWN (already established, all pre-2026-10-03): the qualitative direction that unmodified
Naibbe's edit-1 adjacency ratio is LOW relative to Voynich — 2608.17096 Table 4/7: Naibbe
(Caesar, single corpus) 0.82 vs Voynich 1.12/1.20/1.07 (ZL only), plus PR16's (2026-09-19)
held-out edge-coupling + hapax audit of Naibbe. A skeptic can object that the SIGN of the
effect is published.

NEW in this claim (strictly beyond everything found):
1. A pre-registered 99.9% Voynich quire-bootstrap envelope per cell (4 x 4000-resample
   envelopes) with the pooled Naibbe value BELOW the minimum of all 16,000 bootstrap
   controls — no published source contains a 99.9% H1 envelope, per-cell quantiles, or a
   16,000-control null for this statistic (checked 2608.17096 full text + its code mirror,
   both Parisel papers full text, PR16, all voynich-collective PRs, and all 2025-2026
   Voynich papers/repos above).
2. The 4-cell object: Currier A AND B separately, on BOTH ZL3b and IT2a. 2608.17096's H1
   comparison is ZL-only (its A/B rows are Voynich-only); nothing published splits Naibbe's
   H1 by dialect and by transliteration.
3. Pooled 20-plaintext x 10-seed, both A- and B-mode corpora (3.05M tokens each), versus
   2608.17096's single Caesar stream.
The known observation (0.82 < 1.12) is thus re-confirmed, not re-reported: the claim's
contribution is the rigorous, pre-registered, envelope-based 4-cell, pooled falsification
object — exactly the "new rigorous contribution on top of the known 0.82-vs-1.12
observation" the panel instruction allows to pass.

## Voiding check

No generator or falsification published after 2026-10-03 achieves the claimed outcome.
Candidates checked and rejected as voiding: 2610.34499 / 2610.08861 (no Naibbe H1
envelope), greshko/naibbe-cipher post-cutoff commits (.DS_Store only), voynich-collective
post-cutoff PRs (no Naibbe envelope/adjacency claim). 2608.17096 (2026-08-17) establishes
the single-corpus point estimate only, not the exact 99.9%-envelope/4-cell/pooled object —
and it predates the cutoff, so it does not void even if it had.

Uncertainty (not a blocker): the envelope is computed at verification time from ZL3b-n.txt
/ IT2a-n.txt "as then published" per the criterion, and the status-page fetch confirms the
transliteration reference is live and unchanged in kind since the scout's 11:42 UTC fetch;
the 16,000-control nulls and 95%/99.9% envelopes are reproducible from objects/ via
checker.py (re-derivation is the other panelists' remit).

## Verdict

The pooled, both-dialect, both-transliteration, 99.9%-Voynich-quire-bootstrap-envelope
falsification is strictly beyond the single-corpus 0.82-vs-1.12/1.20/1.07 observation of
2608.17096 Table 4 (and beyond PR16's pre-cutoff edge-coupling audit), and no post-
2026-10-03 publication achieves the exact object. Not a tie. Pass.

pass: true
