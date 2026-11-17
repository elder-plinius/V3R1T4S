# Honesty gate (kit/RUN.md step 7), run 2026-11-11-1855, written by the run's main session at 2026-11-11T19:24:04Z

status: CONFIRMED_PARTIAL
confirmed_scope: On the 2,038 of the 10,189 included phenopacket-store 0.1.27 cases with at most 3 distinct observed (non-excluded) HPO terms (hp.obo v2026-06-06, under HP:0000118), with both tools using the same HPOA v2026-06-06 cleaned of every row citing a corpus PMID (sha256 5e1a2fcf77d3ddf7d5d00f54ce8975ecabff3277749359f1e0636a8c6a7caa14) and the same 19,274-gene protein-coding candidate space, the frozen asymmetric-Resnik ranker reaches gene-level MRR 0.1384 against 0.1047 for LIRICAL 2.4.1 phenotype-only on the unmodified phenopackets (ratio 1.32, paired case-bootstrap 95% intervals [0.0257, 0.0420] for the difference and [1.239, 1.420] for the ratio, real difference above all 400 paired label-swap controls), a margin that does not survive counting excluded terms (493 cases, ratio 0.98) and whose publication-cluster ratio interval [1.024, 1.672] does not exclude ratios below 1.10.

Partial win: p1 of phenopacket-store-rare-disease-gene-prioritization.

Read: panel/reproduce.md (pass: true), panel/novelty.md (pass: true), panel/criterion.md (pass: true), each written
by a fresh subagent (Claude Code Agent tool; types reproduce, novelty, criterion) that saw only claim/.

Checks against the downgrade list:
- Hedging panelist: none. CRITERION passes and builds its caveats (observed terms only; S2 reversal; publication-
  cluster ratio interval) into the scope sentence; the scope above is that sentence, unchanged.
- Reproduction: REPRODUCE re-derived the subset from the raw phenopackets, re-scored LIRICAL from the raw outputs for
  all 10,189 cases and the method's full 19,274-gene ranking from scratch for all 2,038 subset cases, and matched every
  claimed number (bootstrap interval and null exactly). Its findings are documentation notes with effects below 1e-7.
- Not re-run by this panel: LIRICAL 2.4.1 itself (about 1.1 GB per JVM, above the 400 MB panel limit). The raw outputs
  were checked for completeness, rc=0 logs and use of the cleaned disease set (REPRODUCE and CRITERION independently),
  and run 2026-11-11-1222's REPRODUCE skeptic re-ran 6 chunks byte-identically. p1 does not itself require a skeptic
  re-run of the tool; this is recorded, not hidden.
- Value vs table: p1 compares with the reference tool run by the claimant; no published value exists for this cell
  (NOVELTY: status fetched 2026-11-11T19:07:15Z, HTTP 200, release 0.1.27 unchanged; literature and repository
  searched; the nearest published comparison, arXiv 2609.02473 Table 1, is not split by term count). Fetch under 6 h old.
- Stretched criterion / hidden quantifier: the subset counts observed terms only, a reading fixed in run 1 and frozen
  before the p1 statistics; CRITERION judged it fair and conventional, and the scope says "observed (non-excluded)".
  The bank asks for case-level bootstrap intervals; the case ratio interval also clears 1.10.
- Benchmark baseline: the comparator is the reference tool run on the same cases, data and candidate space (run 3's
  record), not a published score; not unresolved.
- One object, one cell: the p1 subset rows (object/p1_subset_cases.tsv) and their statistics. Nothing else is bundled.
- Disclosed before the gate: the subset's point MRRs were seen descriptively in run 3 (declared in PREREG.md).
- REPRODUCE's final file (pass: true) also re-ran the original scorer h2h_score.py on all 102 raw LIRICAL chunks:
  h2h_percase.tsv byte-identical to the claimed one.
