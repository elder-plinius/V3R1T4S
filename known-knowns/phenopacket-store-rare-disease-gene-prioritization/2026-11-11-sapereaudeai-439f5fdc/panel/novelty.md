# NOVELTY skeptic: run 2026-11-11-1855, target phenopacket-store-rare-disease-gene-prioritization, partial win p1

context: subagent (Claude Code Agent tool, fresh context)
written: 2026-11-11, started 19:06:34Z (date -u); read only the claim/ package (claim.md, then prereg/PREREG.md, then
results/, null_test.md, REPRODUCE.md, baseline/README.md, code/frozen_method.py and code/rdlib.py headers).
Copies of everything fetched are in panel/work_novelty/ (scratch).

## Claim under test (from claim.md)
On the 2,038 of 10,189 included phenopacket-store 0.1.27 cases with <= 3 distinct observed HPO terms, same cleaned HPOA
for both tools and the same 19,274-gene protein-coding candidate space, the frozen ranker reaches gene-level MRR 0.1384
vs 0.1047 for LIRICAL 2.4.1 phenotype-only (ratio 1.3218; paired case-bootstrap 95% CI of the difference
[0.0257, 0.0420]; real difference beats all 400 label-swap controls). I re-read results/p1_subset_cases.tsv: 2,038 rows
(n_terms 1/2/3 = 520/691/827), MRR 0.1384 vs 0.1047, ratio 1.3218, matching results/p1_summary.json.
The ranker is the published Phenomizer-style asymmetric best-match-average information-content score, unmodified and
untuned; it is named as such in code/rdlib.py and code/frozen_method.py (cited there to the 2009 Phenomizer paper).

## Status source (one fetch, no retry)
- URL: https://api.github.com/repos/monarch-initiative/phenopacket-store/releases?per_page=5 (API form of the status
  page https://github.com/monarch-initiative/phenopacket-store/releases)
- time: 2026-11-11T19:07:15Z, HTTP 200
- value: latest release tag 0.1.27, published 2026-06-09T16:47:04Z, single asset all_phenopackets.zip (19,431,098
  bytes), digest sha256:d0c70005bb09b87035087516252b6b539fbc0415be7c664b73c9cde7eedf205a. Previous tags 0.1.26
  (2026-01-13), 0.1.25, 0.1.24, 0.1.23. Matches claim.md and inputs/all_phenopackets_0.1.27.zip as cited.
  No release carries evaluation or ranking assets (only the corpus zip).

## The cell and its neighbours
Cell: phenopacket-store 0.1.27; included cases with <= 3 observed HPO terms; gene-level MRR over a fixed all-protein-
coding candidate space; method vs LIRICAL (the bank's reference tool) on identical annotation data.

### Literature and code, last 24 months (what each says about this cell)
1. arXiv 2609.02473 "Learning to Fuse LLMs with Ontology Rankers for Rare-Disease Diagnosis" (HTML fetched once,
   sha256 2cbd5910584bfbc0aed0caec3b4a1cad51da7992600d5b74858456bc7199608f). Same release 0.1.27. Table 1:
   disease-level Recall@1 on 2,227 test cases, uncorrected -> sole-source LOPO: Phenomizer 0.4481 -> 0.1217, bare
   semantic-similarity score 0.6484 -> 0.2591, LIRICAL 2.4.1 0.4868 -> 0.1724. Not split by term count. Table 2 splits
   by matched deletion and gold-profile survival; Table 8 splits Phenomizer only (capped vs uncapped) by > 10 vs <= 10
   terms. No semantic-similarity-vs-LIRICAL value on any small-profile subset. Its code repository (named in the paper;
   tree read once: LICENSE, README.md, overview.png, requirements.txt, src/gate.py, src/lopo.py, src/train.py; zero
   releases) publishes no per-case rankings, so the <= 3-term restriction cannot be read off any published material.
   This is the nearest neighbouring cell (see the trivial-edit analysis below).
2. arXiv 2608.14683 "One Score, Two Decisions: Selective Prediction on the Rare-Disease Tail" (HTML fetched once).
   Uses 0.1.27; stratifies only its own IC-overlap retriever by matched-term count; Exomiser 14.0.0 phenotype-only
   reported by prevalence stratum; no LIRICAL or semantic-similarity result by term count.
3. arXiv 2610.33592 "Auditing evaluation artifacts and data leakage in large language model systems for rare disease
   diagnosis" (abstract fetched): LLM-system leakage audit; no term-count LIRICAL comparison on 0.1.27.
4. arXiv 2607.24878 "GraphRareBench" (abstract): 2,365 ontology-derived cases, not phenopacket-store.
5. arXiv 2609.06080 "PhenoBench" (abstract): a deeply phenotyped cohort benchmark, unrelated.
6. bioRxiv 10.64898/2026.08.30.748028 "An annotation-overlap-flagged rare-disease gene-prioritisation benchmark and
   PMC index recipe" (full text fetched once): release 0.1.26, 1,047 sampled cases, 50-gene candidate lists, minimum
   3 terms; a resource with recommended metrics, no LIRICAL or semantic-similarity results. Different release and
   candidate space.
7. PMC11775211 "A phenotype-based AI pipeline outperforms human experts in differentially diagnosing rare diseases
   using EHRs" (2025; fetched once): compares an ensemble with Phenomizer, LIRICAL, Phen2Disease on RAMEDIS, MME, HMS,
   the 384-case LIRICAL set and hospital EHRs (minimum 3 terms per public case); term-count strata only in a
   supplementary table; not phenopacket-store; disease level.
8. doi 10.1186/s13073-025-01496-8 "PhenoDP" (2025): publisher page not read (HTTP 301 without location; the
   link.springer.com form answered 303 to a cookie/authorization endpoint; not pursued). Search snippets: datasets are
   the 381-case LIRICAL set and simulations, patients with < 3 terms removed; not phenopacket-store 0.1.27.
9. Search snippets only (not opened): an LLM-vs-Exomiser benchmark on phenopacket-store 0.1.14 grouping cases by term
   count (< 5, 6-10, 11-20, > 20; Exomiser ahead of LLMs in every group): different release, no LIRICAL, no
   semantic-similarity ranker. A 2025 HGG Advances study running LIRICAL 2.0.4 with LLM-derived profiles on 0.1.24: no
   term-count split in snippets. A 2026 bioRxiv on synthetic phenotype data (1-2-term sets are weakest): generic.
10. Older than 24 months, qualitative prior: Phen2Disease (bioRxiv 10.1101/2022.12.02.518845) reports a semantic-
    similarity model beating LIRICAL "particularly in cohorts with the less average numbers of HPO terms" on other
    corpora. This makes the direction of p1 unsurprising but supplies no value for this cell.
11. Code and release assets: GitHub repository searches (phenopacket+LIRICAL+benchmark, phenopacket-store+benchmark,
    both pushed after 2024-11-01: 0 hits; phenopacket+LIRICAL: one phenopacket-generator tool; phenopacket+gene+
    prioritization: one 2022 phenopacket-distortion tool). hpoadj releases v0.0.1 and v0.0.2 (jars only; Zenodo
    doi 10.5281/zenodo.24054540) and the ESID4HPO analysis repository (zero releases): an HPOA-adjustment tool and a
    118-individual, 3-disease LIRICAL analysis; not this cell.
Finding: no published value of any method on this cell (<= 3-term subset of 0.1.27, gene level, identical candidate
space against LIRICAL), and no published per-case outputs from which it could be derived.

### The V3R1T4S repository
- TROPHY_CASE.md (fetched once, 31,306 bytes): no mention of phenopacket, LIRICAL, Exomiser, HPO, Resnik, rare disease
  or gene prioritisation.
- known-knowns/ (listing fetched once): 31 entries, none on rare-disease or phenotype-driven ranking.
- Pull requests and issues, open and closed (search API, one request per query): "phenopacket", "LIRICAL",
  "Exomiser", "gene prioritization", "HPO" each return only open PR #1058 (created 2026-11-11T12:13:15Z), the p3
  leakage audit of LIRICAL on a 500-case sample, whose body says "no claim on the main criterion, p1 or p2";
  "rare disease" adds closed PR #769 (a different target, traitgym); "Resnik" returns 0. No prior p1 claim and no
  published value in this cell.

## Trivial-edit analysis (kit rule)
- The only published object near this cell is Table 1 of arXiv 2609.02473 (semantic-similarity score ahead of
  LIRICAL 2.4.1 on the 0.1.27 test split). The prereg declared this as a known risk before any p1 number. I judge the
  p1 result NOT to be a restriction of that object in the kit's sense, for three independent reasons:
  (a) Restriction must be performable on published material; the paper publishes aggregate tables and a src-only
      repository, so no <= 3-term value can be read off it.
  (b) The property is not inherited by restriction: the claim's own strata (results/sensitivity/audit.out) show the
      n_terms = 1 stratum reversed (MRR 0.0896 vs 0.0978) and the S2 subset (observed plus excluded <= 3, n=493)
      tied (ratio 0.98), so a full-set advantage does not imply a <= 3-term advantage of >= 10%.
  (c) The published object is a different cell: disease-level Recall@1, 2,227 test cases, sole-source LOPO; the claim
      is gene-level MRR on all 10,189 included cases with every row citing any corpus PMID removed.
  Deletion, relabelling, symmetry, numerical polish and a gene-from-disease propagation rule applied to Table 1 also
  give no value in this cell.
- Seeding: the ranker is a published method used unchanged, and the package names it (code/rdlib.py,
  code/frozen_method.py, prereg/PREREG.md). p1 asks to beat the reference tool, not to improve on published methods;
  no published edit of any published object gives a value in this cell, so there is nothing for the claim to tie.
  The novelty is the measurement on a pinned release, not the method; a write-up should say plainly that the method
  is the 2009 Phenomizer score, and cite arXiv 2609.02473 Table 1 and the older Phen2Disease qualitative prior as
  context.
- Strictly beats everything known: the only known value in the cell is LIRICAL's 0.1047, run by the claimant on the
  same cases; 0.1384 is strictly above it, by a ratio of 1.3218 (>= 1.10). Not a tie.

## Notes for the other skeptics (not novelty grounds; they do not enter this verdict)
- The p1 advantage is concentrated: removing the top-5 contributing PMIDs gives ratio 0.9976 on 1,721 cases; one gene
  (HGNC:7765) contributes 28.4 of the 68.7 summed RR difference; the publication-cluster 95% interval of the ratio is
  [1.0236, 1.6718] (lower end below 1.10) and of the difference [0.0021, 0.0659]; gene-cluster P(ratio >= 1.10) 0.966
  (results/sensitivity/audit.out, results/sensitivity/gene_cluster.out, labelled post hoc). The prereg chose the
  case-level difference interval as the fair reading and declared it was not blind to the subset's point MRRs.
  Whether that reading holds is for CRITERION.

## Fetch log (UTC, URL, HTTP status; one request each, no retries, User-Agent "V3R1T4S-novelty-skeptic/1.0
## (read-only)", curl --max-time; owner segments of non-status repositories written as <owner>)
- 2026-11-11T19:07:15Z https://api.github.com/repos/monarch-initiative/phenopacket-store/releases?per_page=5 200
- 2026-11-11T19:07:26Z https://raw.githubusercontent.com/<owner>/V3R1T4S/main/TROPHY_CASE.md 200
- 2026-11-11T19:07:26Z https://api.github.com/repos/<owner>/V3R1T4S/contents/known-knowns 200
- 2026-11-11T19:07:27Z https://api.github.com/search/issues?q=repo:<owner>/V3R1T4S+phenopacket&per_page=100 200
- 2026-11-11T19:07:46Z https://api.github.com/search/issues?q=repo:<owner>/V3R1T4S+LIRICAL&per_page=100 200
- 2026-11-11T19:07:46Z https://api.github.com/search/issues?q=repo:<owner>/V3R1T4S+Exomiser&per_page=100 200
- 2026-11-11T19:07:47Z https://api.github.com/search/issues?q=repo:<owner>/V3R1T4S+%22gene+prioritization%22&per_page=100 200
- 2026-11-11T19:07:48Z https://api.github.com/search/issues?q=repo:<owner>/V3R1T4S+%22rare+disease%22&per_page=100 200
- 2026-11-11T19:08:17Z https://arxiv.org/html/2609.02473 200
- 2026-11-11T19:08:17Z https://arxiv.org/abs/2608.14683 200
- 2026-11-11T19:08:17Z https://arxiv.org/abs/2607.24878 200
- 2026-11-11T19:08:18Z https://arxiv.org/abs/2609.06080 200
- 2026-11-11T19:09:30Z https://api.github.com/repos/<owner>/PhenoGate/releases?per_page=20 200 (empty list)
- 2026-11-11T19:09:31Z https://api.github.com/repos/<owner>/PhenoGate/git/trees/HEAD?recursive=1 200
- 2026-11-11T19:10:07Z https://pmc.ncbi.nlm.nih.gov/articles/PMC11775211/ 200
- 2026-11-11T19:10:25Z https://api.github.com/search/repositories?q=phenopacket+LIRICAL+benchmark+pushed:%3E2024-11-01&per_page=50 200
- 2026-11-11T19:10:26Z https://api.github.com/search/repositories?q=phenopacket-store+benchmark+pushed:%3E2024-11-01&per_page=50 200
- 2026-11-11T19:10:26Z https://api.github.com/search/issues?q=repo:<owner>/V3R1T4S+Resnik&per_page=50 200
- 2026-11-11T19:10:27Z https://api.github.com/search/issues?q=repo:<owner>/V3R1T4S+HPO&per_page=50 200
- 2026-11-11T19:10:34Z https://api.github.com/search/repositories?q=phenopacket+LIRICAL&per_page=50 200
- 2026-11-11T19:10:34Z https://api.github.com/search/repositories?q=phenopacket+gene+prioritization&per_page=50 200
- 2026-11-11T19:10:48Z https://www.biorxiv.org/content/10.64898/2026.08.30.748028v1.full 200
- 2026-11-11T19:11:05Z https://arxiv.org/html/2608.14683 200
- 2026-11-11T19:11:05Z https://arxiv.org/abs/2610.33592 200
- 2026-11-11T19:11:55Z https://api.github.com/repos/<owner>/hpoadj/releases?per_page=20 200
- 2026-11-11T19:11:56Z https://api.github.com/repos/<owner>/esid4hpo-analysis/releases?per_page=20 200
- 2026-11-11T19:12:26Z https://genomemedicine.biomedcentral.com/articles/10.1186/s13073-025-01496-8 301 (no location; not followed)
- 2026-11-11T19:12:38Z https://link.springer.com/article/10.1186/s13073-025-01496-8 303 (to a cookie/authorization endpoint; not followed)
Web searches (search tool, about 19:08Z-19:13Z): phenopacket-store LIRICAL by number of HPO terms; arXiv 2609.02473;
phenopacket-store 0.1.27 gene prioritisation MRR; LIRICAL vs Phenomizer by term count; hpoadj; phenotype-only gene
prioritisation by number of HPO terms; phenopacket store semantic-similarity vs LIRICAL gene ranking with leakage
control; LIRICAL with one to three terms; PhenoDP term-count strata.

## Verdict
No published or repository result exists for this cell, and none can be derived from published objects by deletion,
restriction, propagation, relabelling, symmetry or polish. The claimed MRR 0.1384 strictly beats the only known value
in the cell (LIRICAL 0.1047, ratio 1.3218). The method is a published 2009 score used unchanged and is named as such.
What is new is the measurement, not the method. Novelty holds for p1. This judges novelty only, not whether the
criterion reading or the robustness is accepted.

This is retrospective statistics on published case reports, not clinical advice.

pass: true
