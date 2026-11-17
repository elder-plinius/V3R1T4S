# Honesty gate (kit/RUN.md step 7), run 2026-11-11-1032, written by the run's main session at 2026-11-11T11:30:32Z

Read: panel/reproduce.md (pass: true), panel/novelty.md (pass: true), panel/criterion.md (pass: true); three fresh
subagent contexts (Claude Code Agent tool, types reproduce, novelty and criterion), each given only claim/.

Downgrade checks:
- Hedging panelist: none. NOVELTY passes the specific quantification (per-case pre-publication HPOA releases with
  LIRICAL on 0.1.27) and says the leave-one-publication-out audit (arXiv 2609.02473) is published and must be cited.
  CRITERION passes with a scope narrower than the claim's framing; that narrower sentence is the confirmed scope.
- Reproduction mismatch: none. REPRODUCE recomputed all 500 cases x 2 conditions from the saved outputs. Its
  numbers agree; the author's scorer reproduces byte-identically; 5 LIRICAL re-runs (3 groups) are bit-identical.
- Table value: p3 is an audit, not a record; the status source was re-read by NOVELTY at 11:21:23Z (0.1.27, same
  asset sha256), under 6 h ago.
- Stretched criterion / hidden quantifier: the "same publications" wording is met through the bank's own example
  design. The scope states that the drop measures all annotations added after each case's pre-publication release,
  not the case's own publication alone.
- Sample presented as complete: no; the scope names the seeded 500-case sample of the 4,247-case subset.
- Capped search, probable prime, evasion, bundling: not applicable / none found.
- Step 3c baseline: the claim compares the reference tool with itself across annotation releases. No improvement
  over a published score is claimed; baseline/README.md says so and CRITERION checked it.
- Process: PREREG.v2-v4 were written before any score of the cases they affected. The main session first saw
  interim numbers at about 11:04Z, after PREREG.v4 (11:01Z). v4 lowers the headline drop (CRITERION computed it).
- Fixes after the panel, recorded and not hidden: the package notes which HGNC file was in the data directories
  (f3051e4a..., the 2026-06-05 archive; the 86cc190f... line is the unused current file), as REPRODUCE and CRITERION
  flagged. The package cites 2609.02473 and the related work NOVELTY found.

status: CONFIRMED_PARTIAL
confirmed_scope: With LIRICAL 2.4.1 in phenotype-only mode (pinned data, HPO ontology v2026-06-06 held fixed), on a seeded random sample of 500 of the 4,247 run-1-included phenopacket-store 0.1.27 cases (211 PMIDs) for which an HPO release predates the case's earliest PubMed date, replacing the contemporary HPOA v2026-06-06 by the last HPOA release published before each case's paper (ids mapped to the v2026-06-06 ontology) lowers the MRR of gene ranks over 19,274 protein-coding genes (derived from LIRICAL's disease post-test probabilities via mim2gene_medgen) from 0.5567 to 0.0798 (paired drop 0.4769, 95% bootstrap over cases [0.4325, 0.5181], over publications [0.3422, 0.6230]; 85.7% of the contemporary MRR) and top-1 recall from 0.5005 to 0.0490 (drop 0.4515, cases [0.4050, 0.4965], publications [0.3297, 0.5864]), a drop that beats all 400 paired label-swap controls (best 0.1063) and that measures the effect of all HPOA annotations added after each case's pre-publication release, not of the case's own publication alone.
