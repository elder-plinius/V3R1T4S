# Honesty gate (partial win p1)

status: CONFIRMED_PARTIAL
confirmed_scope: With one pre-registered, frozen, zero-shot configuration (equal-weight mean of the z-scored top-12 of 95 published ProteinGym v1.3 model columns, selected only on 187 non-cancer assays sharing no UniProt id with any target), M1 exceeds the maximum over all 97 model columns of the 2026-10-18 live ProteinGym DMS-level Spearman table by at least 0.015 on four of the 13 pre-registered cancer-gene assays — PTEN_HUMAN_Matreyek_2021 (+0.0498), P53_HUMAN_Kotler_2018 (+0.0466), BRCA1_HUMAN_Findlay_2018 (+0.0330) and PTEN_HUMAN_Mighell_2018 (+0.0174), three distinct cancer genes — while losing on the other nine, a 4/13 rate consistent with the pre-registered 16% per-assay base rate and therefore no evidence of general superiority on cancer-gene assays.

Read by the run's main session on 2026-10-18T21:05:22Z:
- reproduce.md: pass: true (fresh subagent). Exhaustive re-implementation reproduces all 13 files to <= 5.2e-10; label randomisation changes nothing.
- novelty.md: pass: true (fresh subagent). Table re-fetched 2026-10-18T20:56:17Z, HTTP 200, same sha256; no p1 claim in 453 PRs or TROPHY_CASE; no higher per-assay value in the literature. VenusRAR (arXiv 2602.00197) reports a better benchmark-wide mean but no per-assay values.
- criterion.md: pass: true (fresh subagent). Scope limited to the four assays, with no general-superiority reading.
- Downgrade checks: no hedged verdict; reproduction exact; every margin strictly >= 0.015; p1 is one enumerated multi-assay partial win carried by one frozen configuration (all 13 files shipped, not a bundle); table fetch < 1 h old; plain GETs only.
- Overlap: PTEN_HUMAN_Matreyek_2021 is also the single-assay full-criterion claim in draft PR #463. The report flags this so the maintainers can reconcile the two rather than credit that assay twice.
