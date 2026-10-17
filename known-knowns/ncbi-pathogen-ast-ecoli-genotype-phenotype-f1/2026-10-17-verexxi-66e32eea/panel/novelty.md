# Novelty check: E. coli ciprofloxacin claim on ncbi-pathogen-ast-ecoli-genotype-phenotype-f1
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: confirmed against the live Table 3 (ciprofloxacin F1 77.2%, accuracy 89.9%, read 2026-10-17T01:25:24Z): no published or claimed predictor evaluated on the NCBI Pathogen Detection E. coli/Shigella AST benchmark ties or beats the claimed 96.13% F1, and the only same-target claim in the repo (open draft PR 308) is for amoxicillin-clavulanic acid, not ciprofloxacin; this is a benchmark-relative record only, because closest prior art (a Brief Bioinform 2026 model on a different NCBI-derived cohort, random folds, fluoroquinolone F1 0.92 to 0.98 across species) brackets the claimed value

Report written (date -u): 2026-10-17T01:40:06Z

Scope and reading of the rules. I read only the claim package (CLAIM.md, REPRODUCE.md, code/, result/, status_source/) and wrote scratch files to ../work/ (named below relative to claim/). "Everything known" is read as the task states it: any published or claimed genotype-to-phenotype predictor evaluated on the NCBI Pathogen Detection E. coli/Shigella AST data for ciprofloxacin. Results on other cohorts (BV-BRC, GieSSen, reprocessed SRA reads, hospital sets, other organisms) are listed as context, because they use different data, mappings and splits and cannot be compared number to number with this benchmark.

## 1. Claim under test (from CLAIM.md)
Export PDG000000004.6366, held-out whole SNP clusters, ciprofloxacin: LightGBM F1 96.13%, accuracy 98.35%, 1693 comparisons in 1246 clusters. The published genotype-field rule recomputed on the same rows gives F1 80.36%; the paper's published values (Alshehri 2026, Int J Mol Sci 27:7157) are F1 77.2% and accuracy 89.9%.

## 2. Status source, fetched once with no retry
- Command: curl -s -o ../work/status_live.xml -w 'HTTP %{http_code} size_download=%{size_download}' 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML'
- UTC before 2026-10-17T01:25:24Z, UTC after 2026-10-17T01:25:25Z, HTTP 200, size_download 218472 bytes.
- sha256 of ../work/status_live.xml: e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685
- sha256 of status_source/PMC13513162_fullTextXML.xml (the claim's saved copy): e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685 (identical).
- Table 3 (id ijms-27-07157-t003), Ciprofloxacin row, read from the live copy: NR/S AST 7615; Sensitivity 97.3% (96.4 to 98.2); Specificity 88.4% (87.6 to 89.2); Accuracy 89.9% (89.3 to 90.6); PPV 63.9% (61.8 to 66.0); NPV 99.4% (99.1 to 99.6); BalancedAccuracy 92.8% (92.2 to 93.4); F1-Score 77.2% (75.5 to 78.7).
- So the published ciprofloxacin F1 is 77.2% and accuracy is 89.9%. The claimed F1 is higher by 18.93 points and the claimed accuracy by 8.45 points.
- The paper's only post hoc or sensitivity analysis is for amoxicillin-clavulanic acid (alternative rule, F1 62.7%). Tables 2, 3 and 6 are the only tables with a ciprofloxacin row; there is no better published ciprofloxacin number in the text or tables.
- Europe PMC citation lookup for the benchmark paper (https://www.ebi.ac.uk/europepmc/webservices/rest/PMC/PMC13513162/citations, 2026-10-17T01:27:10Z, HTTP 200): hitCount 0, so no indexed paper has cited it yet.

## 3. This repo (github.com/elder-plinius/V3R1T4S)
Three unauthenticated REST calls were used, all HTTP 200, no rate limit hit (core limit 60 with 58 left after call 2; search limit 10 with 9 left after call 3), so the web-page fallback was not needed.
1. GET https://api.github.com/repos/elder-plinius/V3R1T4S/contents/TROPHY_CASE.md?ref=main (raw media type), 2026-10-17T01:27:06Z, HTTP 200, 30936 bytes, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 (../work/gh1_trophy_case.md). It has 53 numbered rows in 7 families: constant-weight-codes 35, degree-diameter 7, fast-matrix-multiplication 5, lehmer 1, robustbench-cifar100 1, sealed-envelopes 2, vnncomp-2026 2. A case-insensitive grep for ncbi, pathogen detection, E. coli, escherichia, ciproflox, genotype, phenotype, antimicrobial, ecoli, shigella, amrfinder, lightgbm, AST and bacteri printed no line. There is no E. coli or AMR row at all.
2. GET https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100, 2026-10-17T01:27:06Z, HTTP 200, 1813066 bytes, sha256 8442b4b46fada5abffa7a32bb29619109ccb252e64c59026b98c651ef0d4c7fd (../work/gh2_pulls.json). The Link header reports 3 pages; I read page 1 only: 100 pull requests numbered 203 to 308 (63 open, 37 closed, 19 merged). A local regex over title, body and branch name (ncbi, pathogen, E. coli, escherichia, cipro, genotype, phenotype, antimicrob, AMR, ecoli, shigella, amrfinder, PDG0) matched exactly one: number 308.
3. GET https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+ncbi&per_page=100, 2026-10-17T01:27:07Z, HTTP 200, 3432 bytes, sha256 f16a2751a8888eff4206d0e88c109f0ec24fe0cb58388e4edee9c62c8efe90ee (../work/gh3_search.json). total_count 1, incomplete_results false. The single item is pull request 308 (open, draft true, created 2026-10-17T01:03:03Z by verexxi), title: "[claim] ncbi-pathogen-ast-ecoli-genotype-phenotype-f1: amoxicillin-clavulanic acid F1 91.97%, vs 44.5% for the published rule". Its body says: F1 91.97% (accuracy 97.68%) on the same pinned export PDG000000004.6366, published rule 44.5% (44.78% recomputed), and "One antibiotic per claim."
- Result: there is no claim, open or closed, on this target for ciprofloxacin, and TROPHY_CASE.md has no row for this target. Pull request 308 is a sibling claim for a different antibiotic from the same pipeline, which the "one antibiotic per claim" rule allows.
- Gap: pages 2 and 3 of the pull request list (numbers below 203) were not listed one by one because the three-call budget was used; they are covered only through the search call, which indexes titles, bodies and comments of open and closed pull requests and returned only number 308. A claim titled with the target id would contain "ncbi" and would have been returned.

## 4. Literature, last 24 months
Window used: FIRST_PDATE from 2024-10-01 to 2026-10-31 (a few weeks wider than 24 months on purpose). Each query was one plain request with no retry; every result set was smaller than the page size, so no second page was needed.

Front Microbiol 2026;17:1842717 (named in the task):
- Europe PMC DOI lookup (2026-10-17T01:27:09Z, HTTP 200): DOI 10.3389/fmicb.2026.1842717 is Wan et al., "Utilizing whole genome sequencing data for machine learning driven prediction of antibiotic resistance in Escherichia coli", PMC13160890, first published 2026-04-28. The benchmark paper cites it as reference 43.
- Full text fetched once (2026-10-17T01:28:40Z, HTTP 200, 96282 bytes, sha256 8a5ade838bdd9686295d4a2c1969398e3dcc84a4e4fee6f325df071a17c78cf5, ../work/fm_ft.xml). Data: phenotypes from BV-BRC, genomes from NCBI, 1952 E. coli genomes, 10 antibiotics. Split: random 60:40 (R caret createDataPartition) with 10-fold cross-validation inside training; no cluster hold-out; the authors list "repeated random split validation without independent external validation" as a limitation. Ciprofloxacin: AUC "approaching 1.0" (near saturation); F1 appears only in the Figure 4E scatter plot, and the text gives no numeric ciprofloxacin F1.
- Verdict on it: a different data source (BV-BRC phenotype records, not the NCBI Pathogen Detection AST export), a different split and no extractable ciprofloxacin F1, so it is not a result on this benchmark and gives no number that ties or beats 96.13%. I cannot rule out that its ciprofloxacin F1 on its own random split is high; that is context, not a competing record.

Europe PMC searches (https://www.ebi.ac.uk/europepmc/webservices/rest/search, format json, resultType lite, pageSize 100), all HTTP 200:
| id | UTC | hitCount | query (abridged) |
|---|---|---|---|
| Q2 | 2026-10-17T01:28:42Z | 91 | ("Pathogen Detection" OR "NCBI AST" OR "AMRFinderPlus" OR "NCBI Pathogen") AND ciprofloxacin AND ("Escherichia coli" OR "E. coli") AND (machine learning OR LightGBM OR XGBoost OR random forest OR gradient boosting OR deep learning OR neural network OR classifier) |
| Q3 | 2026-10-17T01:28:43Z | 75 | (genotype-phenotype OR "genotype to phenotype" OR "genotypic prediction" OR "phenotype prediction") AND "Pathogen Detection" AND ("Escherichia coli" OR "Shigella") |
| Q5 | 2026-10-17T01:28:44Z | 95 | ciprofloxacin AND "Escherichia coli" AND (genom* OR "genotype") AND (machine learning OR deep learning) AND (F1 OR F1-score OR "F1 score") |
| Q6 | 2026-10-17T01:30:42Z | 26 | ("NCBI Pathogen Detection" OR "Pathogen Detection Isolates Browser" OR "NCBI AST") AND (antimicrobial susceptibility OR AST OR phenotype) AND (machine learning OR random forest OR XGBoost OR LightGBM OR gradient boosting OR prediction model OR classifier) |
| Q7 | 2026-10-17T01:30:43Z | 35 | SRC:PPR AND ciprofloxacin AND ("Escherichia coli" OR "E. coli") AND (machine learning OR genotype-phenotype OR "genotype to phenotype" OR prediction) |
Q2, Q3 and Q5 together gave 235 unique records. I read every title of Q3, Q6 and Q7, and the titles of Q2 and Q5 that mention E. coli, resistance, genomes, prediction, learning or quinolones, then read the abstracts of 20 shortlisted records (three Europe PMC core-format requests: 2026-10-17T01:29:35Z, 01:31:16Z and 01:33:24Z, all HTTP 200) and the full text of the two that could plausibly sit on NCBI AST data (fetched once each, 2026-10-17T01:37:45Z and 01:37:46Z, HTTP 200).

arXiv (query API, sorted by submission date, 50 results max):
- A (Pathogen Detection AND antimicrobial AND Escherichia): the http address answered 301 with 0 bytes at 2026-10-17T01:30:44Z (a redirect to https, not a block); I sent the same query once to the https address at 2026-10-17T01:31:11Z, HTTP 200: 1 result, from 2012 (outside the window).
- B (ciprofloxacin AND "Escherichia coli" AND genotype OR machine learning OR deep learning): http 301 at 2026-10-17T01:30:48Z, then https at 2026-10-17T01:31:15Z, HTTP 200: 0 results.
- C (broader abstract query on AMR, genotype or genomic, E. coli, prediction), https, 2026-10-17T01:33:28Z, HTTP 200: 2 results, one from 2014 and one in the window (2509.23552v2, below).

Nearest neighbours that were read:
| work | data | split and metric reported | on the NCBI Pathogen Detection E. coli AST benchmark? |
|---|---|---|---|
| Brief Bioinform 2026-07-01 (PMC13520796), discordance analysis plus ML; closest prior art | 20296 genomes from NCBI SRA and BioSample antibiograms plus BV-BRC; E. coli n = 6668; intermediate grouped with resistant; reads reprocessed by the authors with AMRFinderPlus-based features | Random Forest, five-fold stratified CV (phylogeny-blocked CV only as a robustness check); text: adding point-mutation features raised fluoroquinolone F1 from 0.41 to 0.90 up to 0.92 to 0.98 (a range across five species; no E. coli ciprofloxacin value in the main text; Supplementary Table S6 not opened); also double gyrA+parC mutants 96.9% resistant versus 33.0% for gyrA-only in E. coli ciprofloxacin | no: different cohort, different phenotype mapping (I counted as resistant), drug-class level, random folds, no whole-cluster hold-out; same upstream public source |
| Wan et al., Front Microbiol 2026 | BV-BRC phenotypes, 1952 genomes | random 60:40; AUC near 1.0 for ciprofloxacin, F1 only in a figure | no |
| Preprints.org 2026-10-12, cross-population ciprofloxacin in E. coli | BV-BRC, 7274 genomes | elastic net; AUROC 0.992 in-domain, 0.968 Norway, 0.970 South Asia; F1 not in the abstract | no |
| AMR-EnsembleNet, arXiv 2509.23552v2 | GieSSen set, 809 E. coli (Ren et al. 2022), SNP matrix | stratified random 80:20; ciprofloxacin MCC 0.926; HTML text fetched once (2026-10-17T01:33:46Z, HTTP 200) has 0 matches for "Pathogen Detection" and 0 for "NCBI" | no |
| stackPredAMR, Bioinform Adv 2026 (PMC13342711) | BV-BRC (stated in the full text), E. coli, K. pneumoniae, A. baumannii | cross-validation tables: ciprofloxacin F1 0.832 (one-layer RF) and 0.847 (stacked RF), species not separated | no |
| Research Square 2026-03, ciprofloxacin in Salmonella | NCBI Pathogen Detection, 8759 Salmonella isolates | XGBoost ROC AUC 0.989 | no (other organism) |
| Research Square 2026-02, regional bias | BV-BRC E. coli | sensitivity 61.4% to 81.0% by region at one threshold | no |
| IJERPH 2026, E. coli ML | BV-BRC, 17122 isolates | five-fold CV; best XGBoost accuracy 0.86 | no |
| bioRxiv 2025, K. pneumoniae ciprofloxacin rules | 12167 K. pneumoniae isolates | rules on QRDR mutation counts; agreement above 96% in discovery, 93.12% external | no (other organism) |
| AMRgen (bioRxiv 2026) | public surveillance data | R package for concordance analysis, no predictor F1 in the abstract | no |
Also read (abstract) and set aside as not relevant to this benchmark: aiGeneR 3.0 (UTI E. coli, accuracy 93%), PanARGMiner (feature selection), AMR-GNN (P. aeruginosa), a 762-strain E. coli MIC model (external F1 0.85), a patient-level EHR model and MALDI-TOF papers.

Result: the only published genotype-to-phenotype figure on the NCBI Pathogen Detection E. coli/Shigella AST benchmark for ciprofloxacin is the benchmark paper's own rule (F1 77.2%, accuracy 89.9%). No other predictor evaluated on that benchmark was found in the window. The closest prior art is the Brief Bioinform 2026 model: a related-cohort result, not a result on this benchmark, but its fluoroquinolone F1 range (0.92 to 0.98 under random stratified folds) brackets the claimed 96.13%, which is why the pass below is worded as benchmark-relative.

## 5. Checks on the package itself (supporting, not novelty)
Computed from files in claim/ (no model re-run, no re-download of the 551 MB export):
- sha256 of result/split.csv: 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca (CLAIM.md states 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca: identical).
- sha256 of result/scores_ciprofloxacin.json: 9d226565b2067fb76e147e2bc0842427604dea8f6da02cd38e2e57a2631052a1; sha256 of result/test_predictions_ciprofloxacin.csv: 66e32eea192baad34c9e892bc9fc82eb32a87668791890db310c345b5961052f.
- result/test_predictions_ciprofloxacin.csv: 1693 rows, 1693 distinct isolates, 1246 distinct clusters, one antibiotic (ciprofloxacin).
- Model confusion matrix recomputed from the file: TP 348 FP 12 TN 1317 FN 16, F1 96.13%, accuracy 98.35% (matches CLAIM.md).
- Published rule on the same rows: TP 356 FP 166 TN 1163 FN 8, F1 80.36%, accuracy 89.72% (matches CLAIM.md).
- Split integrity from result/split.csv: all prediction isolates are in the test split, cluster labels agree, clusters present in both train and test: 0 (isolates: 8539 train, 2297 test).
- Paired cluster bootstrap with a fresh seed (12345, 2000 resamples, model minus rule F1): 10.91 to 21.59 points; CLAIM.md reports 11.09% to 21.88% (seed 20261016, 10000 resamples). Same conclusion.

## 6. Reasoning
- Against the published number: model F1 96.13% versus 77.2% is +18.93 points, far above the 3-point margin; the model's own interval (93.65% to 97.84%) does not overlap the published interval (75.5 to 78.7) or the recomputed rule's interval (73.37% to 85.77%). Accuracy 98.35% is not lower than 89.9%. The confusion matrix is reported.
- Against the recomputation on the newer export, which the criterion also requires: 96.13% versus 80.36% is +15.77 points, with the paired interval 10.91 to 21.59 points above zero and above 3.
- No tie: nothing in the repo, in the paper, or in the literature window that is evaluated on this benchmark sits at or above 96.13%.
- The status source was read live and is byte-identical to the claim's saved copy, so the "re-read live immediately before claiming" condition holds as of 2026-10-17T01:25Z.

## 7. Limits of this check and wording guardrails
- It is a snapshot (repo and literature as of about 2026-10-17T01:25Z to 01:38Z). A new pull request by someone else for ciprofloxacin could still appear.
- Pull request pages 2 and 3 were checked through the search index only (see section 3).
- Other cohorts show that ciprofloxacin is highly predictable from genotype (AUROC 0.97 to 0.99 in BV-BRC studies, fluoroquinolone F1 0.92 to 0.98 in the Brief Bioinform study, rules above 96% agreement in K. pneumoniae). The large margin over the paper's rule is largely the rule's weakness: it calls resistant on any single quinolone-target mutation or qnr gene (166 false positives among 1329 susceptible rows). So the pass is for a benchmark-relative record against the published value on this export and split, not for a new method or new biology.
- Wan et al. and the Brief Bioinform paper give no numeric E. coli ciprofloxacin F1 in the text I read, so I could not compare against them even on their own terms; the Brief Bioinform supplement was not opened.
- Out of scope here and not checked: whether the model reproduces from the 551 MB export, and the test-label reuse that CLAIM.md itself discloses in its "Test-label evaluation history".
- Any public wording should say that the model beats the genotype-field rule published in Table 3 of Alshehri 2026 (and its recomputation on the same export) on cluster-held-out NCBI Pathogen Detection E. coli data. It should not say state of the art, first, or best ciprofloxacin predictor, and it should keep the no-clinical-interpretation line.
pass: true
