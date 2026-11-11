# NOVELTY skeptic verdict: run 2026-11-11-1032, target phenopacket-store-rare-disease-gene-prioritization, partial win p3

context: subagent (Claude Code Agent tool, fresh context)

Inputs read: claim/claim.md, claim/scout/scout_record.md, claim/scout/phenopacket-store_releases_api.json, claim/baseline/README.md, claim/null_test.md, claim/REPRODUCE.md, the head of claim/prereg/PREREG.md, claim/results/summary.json. Nothing else in the run folder was opened.

## 1. Status source (fetched once, honestly)

- URL: https://github.com/monarch-initiative/phenopacket-store/releases, read through https://api.github.com/repos/monarch-initiative/phenopacket-store/releases?per_page=5
- Fetch: 2026-11-11T11:21:23Z (UTC, from `date -u` just before the request), one plain curl request, User-Agent "V3R1T4S panel skeptic", 30 s timeout, HTTP 200, 17762 bytes. Saved as panel/work_novelty/releases.json (sha256 d8801cded518d91ee242a7b7f61439066620f1684cafe59bd077d7522ba9361f).
- Value: latest release **0.1.27**, published_at 2026-06-09T16:47:04Z, asset all_phenopackets.zip, 19431098 bytes, API digest **sha256:d0c70005bb09b87035087516252b6b539fbc0415be7c664b73c9cde7eedf205a**. No newer release exists. The other releases returned were 0.1.26 (2026-01-13), 0.1.25 (2025-08-04), 0.1.24 and 0.1.23.
- The release and sha256 match what claim/claim.md pins. The only differences from the scout's saved copy (claim/scout/phenopacket-store_releases_api.json) are two download_count fields (2307 -> 2309 and 34 -> 35). The pinned corpus is still the current release.

## 2. What is claimed (p3, not a record value)

Using LIRICAL 2.4.1 in phenotype-only mode on a seeded sample of 500 of the 4,247 phenopacket-store 0.1.27 cases published after HPO v2022-02-14, gene-level MRR over 19,274 protein-coding genes drops from 0.5567 (HPOA v2026-06-06) to 0.0798 when each case is scored with the last HPOA release before its paper. The paired drop is 0.4769, or 85.7% of the contemporary MRR. Top-1 falls from 0.5005 to 0.0490. The claim gives case and publication-cluster bootstrap intervals and a 400-control label-swap null. The design is the example that the bank's own p3 text names ("scoring with annotation releases that predate each case's publication").

## 3. V3R1T4S repository (https://github.com/elder-plinius/V3R1T4S, GitHub API, one request each, 2026-11-11T11:21:42Z to 11:21:56Z, all HTTP 200)

- TROPHY_CASE.md (contents API, blob sha 18b731d7d4bf99efd323d48740284daccb8501b0, 31083 characters): 0 lines match phenopacket, lirical, exomiser, hpo, rare disease or leakage.
- known-knowns/ (31 entries): none is about phenopacket-store, LIRICAL, Exomiser, HPO or rare-disease gene prioritisation. The only name containing "phenotype" is ncbi-pathogen-ast-ecoli-genotype-phenotype-f1, which is unrelated.
- Search over issues and PRs, open and closed: `repo:elder-plinius/V3R1T4S phenopacket` returned total_count 0. So did `... LIRICAL` and `... phenopacket-store-rare-disease-gene-prioritization`.
- Nothing in the repo claims or records this result.

## 4. Literature and code from the last 24 months (WebSearch, WebFetch, PubMed E-utilities, arXiv API)

Searches run: 8 WebSearch queries covering LIRICAL or Exomiser with phenopacket-store, temporal or pre-publication HPOA, circularity and leakage, GitHub/Zenodo HPOA releases, and named papers. Also one PubMed esearch, (phenopacket*) AND (LIRICAL OR Exomiser OR leakage OR circular*) from 2024/11/01 to 2026/11/11, which returned 4 PMIDs: 41929304, 41735669, 41383021 and 39108510. All are LLM benchmarks or reviews. Also one arXiv API query, all:phenopacket, newest first, which returned 4 entries, including 2609.02473 and 2605.22734.

Works opened (WebFetch) and what they report:

1. **arXiv 2609.02473** (Jiang et al., "Learning to Fuse LLMs with Ontology Rankers for Rare-Disease Diagnosis", 2026-09-02; code https://github.com/Anonymous-Awesome-Submissions/PhenoGate)
   - Section "Exact LOPO for LIRICAL" runs unmodified LIRICAL 2.4.1 on phenopacket-store 0.1.27. It removes a disease-phenotype relation only when the test publication is that relation's sole cited source. The test set is 2,227 cases from 364 publications.
   - Disease-level Recall@1 falls from 0.4868 to 0.1724, a paired drop of 31.43 points with 95% CI [24.82, 38.72]. That is about 65% of the uncorrected value (my arithmetic).
   - It reports no MRR and no gene-level LIRICAL numbers, and uses no historical HPOA releases, publication dates or time-based splits (temporal analysis absent).
   - This is the closest published audit: same tool, version and corpus release, related question, different design and unit.

2. **arXiv 2610.33592** (Yang et al., "Auditing evaluation artifacts and data leakage in LLM systems for rare disease diagnosis", 2026-10-24)
   - It scores datasets against annual ORPHA/OMIM/HPO snapshots from 2021 to 2026, one snapshot for all valid cases at a time. A case is valid for a snapshot if its disease and at least two HPO terms exist in that snapshot.
   - The model is an LR model "specifically LIRICAL". The paper gives no software version and does not say whether the tool or a reimplementation was run. The Phenopacket Store release is not stated.
   - Reported numbers: Phenopacket Recall@1 was 17.2% to 22.6% for the 2021 to 2024 snapshots and 53.6% for the 2025 snapshot. The rest is in a figure only.
   - It has no per-case cutoff by publication date, no gene level, no MRR and no code URL. This is a snapshot-level KB-evolution audit, not the per-case pre-publication design.

3. **arXiv 2608.14683** (Jiang et al., "One Score, Two Decisions", 2026-08-05)
   - It runs its own IC-weighted retriever and Exomiser on phenopacket-store 0.1.27.
   - It uses leave-source-out and a "strict" control that drops any gold term the case's own PMID supports. Both are PMID-based, not temporal. No historical HPOA releases or publication-date cutoffs appear anywhere (checked in Appendix D.1).

4. **bioRxiv 10.64898/2026.08.30.748028** (Angulo, Espinos-Morato, Yeste, posted 2026-09-03)
   - It flags 1,047 phenopacket-store 0.1.26 cases by whether the case PMID is cited in phenotype.hpoa v2026-02-16, and stratifies by publication year (2020 boundary).
   - The abstract says "The resource reports no tool comparisons". There are no MRR or top-1 numbers, and it uses no historical releases.

5. **github.com/P2GX/esid4hpo-analysis**
   - LIRICAL 2.4.1 on 118 literature individuals with three immune diseases. It compares a baseline arm on HPO v2024-08-13 with phenopackets aged down to that vocabulary against a workshop arm on v2026-06-23. It also includes LOO HPOA sensitivity.
   - This is not a per-case publication-date design and not corpus-wide. No numbers appear on the page.

6. **PMC11302616** (Reese et al., medRxiv version of the EJHG 2026 Exomiser-vs-LLM benchmark; the Nature page redirected to a login and was not followed)
   - Exomiser 14.0.1, data 2406, phenopacket-store 0.14. It does no annotation-leakage or publication-date analysis.

7. **github.com/phentrieve/phentrieve/issues/451** (opened 2026-10-27)
   - A non-cited-subset evaluation of a ported scorer, reported as Hit@10. LIRICAL and Exomiser are not run, and there are no pre-publication releases.

Seen as search snippets only, not opened:
- github.com/P2GX/hpoadj and Zenodo 24054540 (an HPOA adjuster with `augment` and `loo` modes only)
- Zenodo 24058794 (ESID4HPO adjusted HPOA files)
- arXiv 2607.24878 (GraphRareBench, ontology-derived cases)
- arXiv 2604.17114 and 2605.22734 (temporal knowledge graphs, not HPOA-release scoring of LIRICAL)
- PhEval (BMC Bioinformatics 2025; one fixed HPOA release, 2024-04-26)
- medRxiv 10.64898/2026.03.26.26349194 (LLM meta-analysis)

## 5. Comparison and trivial-edit test

- **No published work scores the reference tool (LIRICAL or Exomiser) on phenopacket-store with, for each case, the HPOA release that predates that case's publication.** No published LIRICAL MRR or top-1 exists under that design, at gene or disease level.
- **The claim's numbers cannot be derived by trivial edits of a published result.** No deletion, restriction, relabelling or polish of the published numbers produces them:
  - 2609.02473 publishes one disease-level Recall@1 pair under a sole-source LOPO filter of a single contemporary HPOA. The claim uses historical HPOA releases, per-case date assignment, gene-level MRR and top-1, and a different case set (cases published after 2022-02-14).
  - 2610.33592 publishes per-snapshot Recall@1 for all valid cases, in a figure, with an unpinned implementation and corpus release.
  - Getting the claimed quantity needs new LIRICAL runs on historical HPOA files; any of these works would have to re-run, not re-tabulate.
- **The claim's result is not dominated by the published ones.** Its numbers are consistent in direction with them but larger (85.7% of MRR, versus roughly 65% of Recall@1 under LOPO). It adds the bank's named design, gene-level MRR, and case- and publication-cluster intervals.

## 6. Caveats the claim text should carry (do not change the verdict)

1. **A p3-type audit of this tool, version and corpus already exists:** the LOPO audit in arXiv 2609.02473. The claim's novelty therefore rests on its design (per-case pre-publication HPOA, the bank's own example) and its gene-level MRR and top-1. It is not the first leakage audit of LIRICAL on phenopacket-store 0.1.27.
   - claim.md does not cite 2609.02473, 2610.33592 or the bioRxiv flagged benchmark. Only baseline/README.md and the scout record mention 2609.02473 and the bioRxiv preprint. The published claim should cite all three and say how its design differs.
2. **The temporal design removes more than the case's own publication.** It also removes every annotation added after the paper, from other sources and from general curation growth. So 85.7% bounds the own-publication share plus later KB growth.
   - LOPO isolates the own-publication part more cleanly. 2610.33592 shows that general KB growth also moves LR-model Recall@1 on Phenopacket.
   - Whether that still answers p3's "the same publications generated both" is for the CRITERION skeptic. It is not a novelty defect, because the bank names this design.
3. **Coverage limits:**
   - GitHub code search needs authentication and was not used. Code was checked through web search and named repositories only.
   - GitHub's issue/PR search index can lag by minutes.
   - Five related items were seen as snippets only.

## Verdict

novelty: PASS for the specific quantification. The status source confirms phenopacket-store 0.1.27 with the pinned sha256. Nothing in the V3R1T4S repo records this result. No work from the last 24 months found in arXiv, bioRxiv/medRxiv, PubMed, GitHub or Zenodo publishes a per-case pre-publication-HPOA audit of LIRICAL (or Exomiser) on phenopacket-store, or any LIRICAL MRR or top-1 on these cases under that design. The related LOPO, snapshot and flagging works are different quantities that need re-running, not trivial edits. The claim must cite them, especially 2609.02473, and must not present itself as the first leakage audit of LIRICAL on 0.1.27.

pass: true
