# Novelty check: V3R1T4S claim ncbi-pathogen-ast-ecoli-genotype-phenotype-f1, gentamicin
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: nothing known ties or beats it - live bar is gentamicin F1 92.4% and accuracy 97.6% (Europe PMC Table 3, read 2026-10-17T01:25:30Z, HTTP 200), the claim is F1 96.28% and accuracy 98.64%; TROPHY_CASE.md, the repo pull requests (open and closed), Europe PMC and arXiv show no other gentamicin predictor on this benchmark (the only related pull request, number 308, is amoxicillin-clavulanic acid only)

Conventions: file names are relative to claim/ unless they start with work/ (my scratch folder, a sibling of claim/). Times come from date -u on this machine (clock read 2026-10-17, about 01:25Z to 01:33Z), HTTP codes from curl -w '%{http_code}', hashes from sha256sum. I did not re-run the model; this file covers novelty only.

## 1. Status source, fetched once

- URL: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML
- Fetch: start 2026-10-17T01:25:30Z, end 2026-10-17T01:25:31Z, HTTP 200, 218472 bytes (work/PMC13513162_live.xml). One request, no retry, no block.
- sha256 e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685. This equals the hash of the saved copy status_source/PMC13513162_fullTextXML.xml and the hash recorded in CLAIM.md, so Table 3 is unchanged since the claimant's reads (2026-10-16T17:08:10Z and 2026-10-16T19:28:36Z).
- Table 3, Gentamicin row, parsed from the live XML: N R/S AST 7344; sensitivity 93.6% (92.1-94.9); specificity 98.3% (98.0-98.7); accuracy 97.6% (97.2-97.9); PPV 91.1%; NPV 98.8%; balanced accuracy 96.0%; F1-Score 92.4% (91.2-93.5).
- Claim as stored in result/scores_gentamicin.json (sha256 adad9247862e9ed2830751b154395c3f9e84b77d73d97818829c65c7bf734ebd) was read, not re-derived: model F1 0.96284 (96.28%), accuracy 0.98644 (98.64%), confusion TP 285 FP 9 TN 1316 FN 13, cluster-bootstrap F1 CI 93.68% to 98.00%; recomputed rule F1 92.41%, accuracy 97.17%, CI 88.09% to 95.31%; paired difference CI 1.81% to 6.95%. I checked the arithmetic from the confusion matrices (570/592 and 560/606) and it matches.
- Margins against the live bar: 96.28 minus 92.4 is 3.88 points; 96.28 minus the recomputed 92.41 is 3.87 points (at least 3 required); accuracy 98.64% is above 97.6%. The model F1 point estimate lies above the upper end of the recomputed rule's interval (95.31%) and above the published interval (91.2-93.5). So the claim strictly exceeds the status-source value.

## 2. This repo (elder-plinius/V3R1T4S)

GitHub REST API, unauthenticated, exactly 3 calls:

1. 2026-10-17T01:26:11Z, HTTP 200: contents of TROPHY_CASE.md at ref main (raw media type), 30936 bytes, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 (work/TROPHY_CASE.md). It declares six result families (degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer bound, VNN-COMP counterexamples, a RobustBench attack) plus two cipher commitments, 53 rows. A case-insensitive grep for ncbi, pathogen, ecoli, E. coli, gentamicin, genotype, phenotype, antibiotic, antimicrob, shigella, lightgbm, salmonella, susceptib, bacteri, genom, tetracycline, ciprofloxacin, ampicillin, meropenem, ceftriaxone returned 0 hits. No entry for this family or for any E. coli result.
2. 2026-10-17T01:26:38Z, HTTP 200: pulls with state=all, per_page=100, newest first (work/gh2_pulls.json, sha256 8442b4b46fada5abffa7a32bb29619109ccb252e64c59026b98c651ef0d4c7fd). It returned 100 pull requests numbered 203 to 308, created 2026-10-16T02:31:01Z to 2026-10-17T01:03:03Z (63 open, 19 closed and merged, 18 closed unmerged); the Link header showed 3 pages in total. A keyword scan of titles, bodies, labels and branch names found exactly one E. coli / NCBI pull request: number 308. The highest number in the list was 308, so nothing newer existed at that moment.
3. 2026-10-17T01:27:21Z, HTTP 200: search/issues with q = repo:elder-plinius/V3R1T4S is:pr ncbi (work/gh3_search.json, sha256 f16a2751a8888eff4206d0e88c109f0ec24fe0cb58388e4edee9c62c8efe90ee). total_count 1, incomplete_results false, the single item is pull request 308. The search covers all pages and both open and closed states, so older pull requests (numbers below 203) that mention ncbi would have appeared; none did. (Index lag is small: number 308, created 01:03:03Z, was already indexed.)

Pull request 308 in detail (from the list response and one extra request to the raw file host, which is not the REST API): title "[claim] ncbi-pathogen-ast-ecoli-genotype-phenotype-f1: amoxicillin-clavulanic acid F1 91.97%, vs 44.5% for the published rule"; state open, draft true; created 2026-10-17T01:03:03Z; author verexxi; head branch claim/2026-10-17-verexxi-8061f657 on a fork. Its README (fetched 2026-10-17T01:27:36Z, HTTP 200, work/pr308_README.md, sha256 6839b780a83d6ec37812dfe1e94e512d3703de37afa77606f8c65bc1a098adc6) says it is "for amoxicillin-clavulanic acid only" and "Not a claim about other antibiotics (one antibiotic per package)". It cites the same split file hash (68a7e358...577dca) and the same LightGBM design as this claim, so it is evidently a sibling from the same claimant. It contains no gentamicin number. Conclusion: no claim on gentamicin for this target exists in the repo.

## 3. Literature, last 24 months (2024-10-17 to 2026-10-17)

Europe PMC search API (preprints are included through its PPR index) and arXiv API, one plain GET per query. All times are UTC on 2026-10-17.

| time | endpoint | HTTP | what | result |
|---|---|---|---|---|
| 01:27:56Z | Europe PMC search | 200 | DOI 10.3389/fmicb.2026.1842717 (Front Microbiol 2026;17:1842717) | 1 hit, see below |
| 01:28:10Z | Europe PMC full text | 200 | PMC13160890 full XML (sha256 8a5ade838bdd9686295d4a2c1969398e3dcc84a4e4fee6f325df071a17c78cf5) | read, see below |
| 01:28:50Z | Europe PMC search | 503 | broad full-text query with sort=RELEVANCE | body: Search service is temporarily unavailable |
| 01:29:09Z | Europe PMC search | 503 | title/abstract query "Pathogen Detection" + Escherichia/Shigella, with sort=RELEVANCE | same 503 body |
| 01:29:24Z | Europe PMC search | 200 | the same title/abstract query, sort parameter removed (changed request, cause of the 503 not established) | 212 hits; top hit is the benchmark paper PMC13513162 (2026-08-10); the rest are generic pathogen-detection assays and surveillance papers judged by title, none a genotype-to-phenotype predictor |
| 01:29:44Z | Europe PMC search | 200 | title/abstract: ML terms + E. coli + AMR + genome/genotype + gentamicin or aminoglycoside | 6 hits: ST131 lineage prediction from AST phenotypes (Microb Genom 2026), Wan et al. (Front Microbiol), 1D CNN-XGBoost preprint, ruminant AI review and its preprint twin; none on the NCBI Pathogen Detection export |
| 01:29:47Z | Europe PMC search | 200 | full text: "NCBI Pathogen Detection" + gentamicin + coli/Shigella + ML terms | 6 hits, judged by title: a scoping review (PMC13627374) and Salmonella, food-chain, colistin and comparative-genomics papers; no E. coli gentamicin predictor |
| 01:29:50Z | Europe PMC citations | 200 | articles citing the benchmark paper (MED 42653162) | hitCount 0 |
| 01:30:05Z | Europe PMC search | 200 | core record of preprint PPR1092272 | 1D CNN-XGBoost ensemble, 809 E. coli strains, SNP features, macro F1 0.691 for gentamicin (different data, much lower) |
| 01:30:08Z | Europe PMC full text | 200 | scoping review PMC13627374 | mentions Pathogen Detection once (a Salmonella study, 788 isolates) and gentamicin only in clinical or EHR-based studies; no E. coli NCBI gentamicin predictor |
| 01:30:34Z | Europe PMC search | 200 | AMRFinder / genotype-phenotype + E. coli + predict/concordance/classif | 47 hits; screened by title; 7 candidates read at abstract level (below) |
| 01:30:38Z | Europe PMC search | 200 | full text: Pathogen Detection + tree/forest ML + E. coli + AMRFinder + phenotype | 14 hits: reviews and unrelated papers, no predictor on this export |
| 01:30:41Z | Europe PMC search | 200 | author search Alshehri AA with E. coli/AMR terms (benchmark author follow-ups) | 14 hits: the benchmark paper, and a 2026 review of WGS AMR tools whose abstract names no E. coli, NCBI or gentamicin result; the rest unrelated |
| 01:30:44Z | arXiv API (http) | 301 | Pathogen Detection + (gentamicin or AMRFinderPlus or genotype-phenotype) | redirect, empty body |
| 01:31:21Z | Europe PMC search | 200 | abstracts of the 7 candidates | none is a gentamicin predictor on the NCBI Pathogen Detection export (below) |
| 01:31:24Z | arXiv API (https) | 200 | the same query sent once to the https address that the 301 pointed to | totalResults 0 |
| 01:31:27Z | europepmc.org image | 403 | Figure 4 image of Wan et al. | HTML response of 5607 bytes, not an image; not retried |
| 01:32:24Z | Europe PMC search | 200 | full text: Pathogen Detection + E. coli + gentamicin + F1 | 22 hits: the benchmark paper, reviews, conference abstract books; no predictor |
| 01:32:30Z | arXiv API (https) | 200 | gentamicin + E. coli + (machine learning or LightGBM or XGBoost or genotype) | totalResults 1: arXiv 2509.23552v2, the 1D CNN-XGBoost paper above |

Front Microbiol 2026;17:1842717 (the item named in the kit): Wan F, Tong W, Wu W, Liu J, Huang H, Zhang P, Jiang W, "Utilizing whole genome sequencing data for machine learning driven prediction of antibiotic resistance in Escherichia coli", PMID 42131209, PMC13160890, first published 2026-04-28. Its data are BV-BRC phenotype records for E. coli (via assembly accessions) with raw WGS downloaded from NCBI: 1952 genomes, 10 antibiotics (gentamicin: 2,765 susceptible, 580 resistant, Table 1), features from Snippy SNPs, Bakta/Panaroo gene presence-absence and 11-mer k-mers. It reports AUC (0.6691 to 0.9879 overall; gentamicin, tobramycin and ciprofloxacin described as near saturation). F1 appears only in Figure 4E; no gentamicin F1 is given in the text or tables. It does not use the NCBI Pathogen Detection AST metadata or its AMR genotype field, so it is not a predictor evaluated on this benchmark.

Seven candidates read at abstract level (Europe PMC core records, sha256 08e08e560fc2bb0c1e3aa31c1fbd1237f318dd4c8963f3cf75e9836d6077c8c6): a 2026 review of WGS AMR interpretation tools; a preprint on allelic diversity and multicopy genes (E. faecium and E. coli, tool accuracy, no F1 benchmark of a learned model); the AMRgen R package (descriptive genotype-phenotype analysis); a Salmonella biochip-signal ML paper; a 20-strain 16S functional-profiler comparison; an 18-strain sepsis WGS+ML study; and Can J Microbiol 2025 "Machine learning methods to identify markers and predict antimicrobial resistance in Escherichia coli" (4300 genomes, 34 antimicrobials, k-mer gradient boosting, average accuracy 93.6%; its abstract does not name the NCBI Pathogen Detection export and gives no gentamicin figure; its full text was not read). None reports a gentamicin F1 on the benchmark's data.

## 4. Reasoning

- The bar is the status-source value read live: gentamicin F1 92.4%, accuracy 97.6% (Table 3, unchanged). The claim's 96.28% F1 and 98.64% accuracy exceed it by 3.88 points and 1.04 points; against the recomputed rule on the same new-export rows (92.41%) the margin is 3.87 points. This is a strict win, not a tie.
- "Everything known" for this benchmark: the benchmark paper itself (rule only, no learned model), TROPHY_CASE.md (no E. coli or NCBI family), repo pull requests (only number 308, a different antibiotic and a draft), and the last 24 months of Europe PMC and arXiv (no paper cites the benchmark paper; no learned gentamicin predictor on the NCBI Pathogen Detection E. coli/Shigella AST export; the nearest items use other data and are weaker or unreported for gentamicin).
- Sibling pull request 308 does not touch gentamicin and says so. Whether the bank accepts a second antibiotic claim on the same target is a bank-rule question, not a novelty question; I did not read the bank rules.
- Nothing I found ties or exceeds the claim, so the novelty condition is met on the evidence available.

Residual risks, stated plainly:
1. Wan et al. Figure 4E (gentamicin F1) is unread because the image request returned 403 and I did not retry or look for a workaround. It is off-benchmark (BV-BRC phenotypes, 1952 genomes, its own features), so by the kit's definition it cannot tie or beat a result on this export, but a reader comparing across datasets should not equate the two.
2. The Can J Microbiol 2025 paper's full text was not read; only its abstract (average accuracy 93.6% over 34 antimicrobials).
3. Coverage is limited to Europe PMC (including its preprint index) and arXiv, with keyword queries; a paper that never names Pathogen Detection or gentamicin in indexed text could be missed. Literature before 2024-10-17 was not searched, per the kit.
4. This is a moving target: pull request 308 appeared about 23 minutes before my pull request list request. Re-run the repo search and re-read Table 3 immediately before filing.

## 5. Hashes (all from sha256sum in this session)

- work/PMC13513162_live.xml and status_source/PMC13513162_fullTextXML.xml: e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685
- result/scores_gentamicin.json: adad9247862e9ed2830751b154395c3f9e84b77d73d97818829c65c7bf734ebd
- result/split.csv: 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca
- result/test_predictions_gentamicin.csv: 75e7504f005731e2bf48b7bf8484b44a98afecd30fa4c58fbe7041eb9fb48d28
- work/TROPHY_CASE.md: 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9
- work/gh2_pulls.json: 8442b4b46fada5abffa7a32bb29619109ccb252e64c59026b98c651ef0d4c7fd
- work/gh3_search.json: f16a2751a8888eff4206d0e88c109f0ec24fe0cb58388e4edee9c62c8efe90ee
- work/pr308_README.md: 6839b780a83d6ec37812dfe1e94e512d3703de37afa77606f8c65bc1a098adc6
- work/PMC13160890_fullTextXML.xml: 8a5ade838bdd9686295d4a2c1969398e3dcc84a4e4fee6f325df071a17c78cf5

pass: true
