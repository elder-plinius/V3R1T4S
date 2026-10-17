# Novelty check: ceftriaxone, ncbi-pathogen-ast-ecoli-genotype-phenotype-f1
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: ceftriaxone F1 97.66% (accuracy 98.76%) strictly beats the live-read published 94.6% (accuracy 97.9%) by 3.06 points and the recomputed rule (94.51%) by 3.15 points; no other predictor on this benchmark, no TROPHY_CASE.md row and no ceftriaxone pull request found (only an open draft for amoxicillin-clavulanic acid, #308).

Scope: I read only the claim package (CLAIM.md, REPRODUCE.md, code/, result/, status_source/) plus public web sources. Scratch files are in work/ next to claim/. All times are UTC from `date -u`, all statuses from `curl -w '%{http_code}'`, all hashes from `sha256sum`.

## 1. Status source, fetched once (no retry)
- URL: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML
- Fetched 2026-10-17T01:25:50Z to 01:25:51Z, HTTP 200, 218472 bytes, saved as work/status_fetch.xml.
- sha256 e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685, identical to status_source/PMC13513162_fullTextXML.xml in the package (so the page is unchanged since the claimant's 2026-10-16T17:08:10Z and 19:28:36Z reads).
- Paper: Alshehri, Int J Mol Sci 2026, 27:7157, "Antibiotic-Specific Genotype-Phenotype Concordance and Cross-Database Interoperability in Public Escherichia coli/Shigella WGS-AMR Metadata". Europe PMC lists it as first published 2026-08-10, revised 2026-08-29, no correction or erratum recorded, 0 citing papers (see section 3).
- Table 3, Ceftriaxone row (parsed from the XML): NR/S AST 6841; sensitivity 92.1%; specificity 99.3%; accuracy 97.9% (97.5 to 98.2); PPV 97.3%; NPV 98.0%; balanced accuracy 95.7%; F1 94.6% (93.7 to 95.4).
- Every other sentence in the paper's main text that mentions ceftriaxone is descriptive (selection of the eight antibiotics, "high concordance"), and the BV-BRC table only counts phenotype entries; no higher ceftriaxone performance figure appears in the main text or tables (the supplementary files were not opened).
- This matches what CLAIM.md quotes (F1 94.6%, accuracy 97.9%).

## 2. The claimed numbers, checked against the package
- result/scores_ceftriaxone.json: model F1 0.97657 (97.66%), accuracy 0.98759 (98.76%), TP 396 FP 10 TN 1116 FN 9; rule recomputed F1 0.94508 (94.51%), accuracy 0.97191, TP 370 FP 8 TN 1118 FN 35.
- I recomputed both confusion matrices from result/test_predictions_ceftriaxone.csv (1531 rows, 1531 isolates, 1114 clusters, ceftriaxone only). They match the scores file exactly (model and rule).
- Margins against the live-read published values: F1 +3.057 points over 94.6 (the paper rounds to one decimal, so the true published value is between 94.55 and 94.65, margin between 3.007 and 3.107); F1 +3.149 points over the recomputed rule; accuracy +0.859 points over the published 97.9 and +1.568 over the recomputed rule.
- The model F1 (97.66) is above the upper end of the published interval (95.4) and above the upper end of the rule's cluster-bootstrap interval on the test rows (96.58). The paired difference interval in the package is 1.21 to 5.44 points (excludes zero).

## 3. Literature, last 24 months (Europe PMC and arXiv)
Window used: FIRST_PDATE 2024-10-01 to 2026-10-17 (slightly wider than 24 months). One plain request per query or page, no retries.

Europe PMC search API (all HTTP 200):
- Q1 at 2026-10-17T01:27:56Z, hitCount 399, first 100 listed: ("Pathogen Detection" OR NDARO OR "National Database of Antibiotic Resistant Organisms") AND (Escherichia OR "E. coli" OR Shigella) AND (ceftriaxone OR cephalosporin OR "third-generation") AND (predict* OR "machine learning" OR classifier OR "genotype-phenotype" OR "genotype to phenotype"). By title, the only item evaluating genotype rules on this export is the benchmark paper itself; the other plausible items were pulled and are covered below. One more title (Pathogens 2025-12-24, multi-resistance patterns in U.S. foodborne pathogens from the NCBI Pathogen Isolates Browser) indicates a descriptive surveillance analysis; I did not read its abstract. Relevance had already decayed to unrelated topics by the end of page 1 (liver guidelines, psychiatry), so I did not page further.
- Q2 at 01:27:57Z, hitCount 42: ceftriaxone AND E. coli AND ML terms AND genomic terms AND F1.
- Q3 at 01:27:59Z, hitCount 17: preprints (SRC:PPR) with AMRFinderPlus or Pathogen Detection, prediction, E. coli, ceftriaxone or cephalosporin.
- Q4 at 01:27:59Z, hitCount 6: genotype-phenotype concordance AND Pathogen Detection AND BV-BRC or PATRIC AND E. coli. Returns the benchmark paper, a Front Microbiol 2026-09-14 review of WGS-based AMR interpretation tools (abstract only, no benchmark result), and unrelated items.
- Q5 at 01:31:42Z, hitCount 44, title/abstract only: Pathogen Detection or NDARO or NCBI AMR or AST browser or AMRFinderPlus, with prediction or ML, with coli or Enterobacterales or Gram-negative.
- Q6 at 01:31:43Z, hitCount 12, title/abstract only: ceftriaxone or third-generation cephalosporin or cefotaxime or ESBL, with genomic terms, ML terms, E. coli.
- Citations of the benchmark paper (PMC source, PMC13513162) at 01:28:00Z: hitCount 0. Nothing has cited it, so nothing has published a result on its benchmark through this route.
- Candidate abstracts pulled at 01:28:30Z (hitCount 9) and 01:31:57Z (hitCount 5); full texts read for three papers (below).

What the closest papers are, and why none is a result on this benchmark:
- Wan et al., Front Microbiol 2026;17:1842717 (named in the task; Europe PMC PMC13160890, first published 2026-04-28; full text fetched 01:26:41Z, HTTP 200, 96282 bytes, sha256 8a5ade838bdd9686295d4a2c1969398e3dcc84a4e4fee6f325df071a17c78cf5). The benchmark paper cites it as its reference 43 (only for amoxicillin-clavulanic acid being weakest). Phenotypes come from BV-BRC, genomes from NCBI, 1952 E. coli genomes, 10 antibiotics, ceftriaxone S 696 / R 444, SNP/gene/k-mer features, "repeated random split validation without independent external validation" (their wording). The text has 0 mentions of "Pathogen Detection" and 0 of "Shigella". Ceftriaxone F1 and accuracy appear only inside a figure (Figure 4 panels), with no number in text or tables, so I cannot quote a value; I could not extract the figure data. It is a different dataset and a random split, so it is not a result on this benchmark either way.
- stackPredAMR, Bioinform Adv 2026-06-02 (PMC13342711, full text read): E. coli, K. pneumoniae, A. baumannii, 18 agents, about 2500 public genomes, BV-BRC data (7 mentions), 0 mentions of "Pathogen Detection" and 0 of ceftriaxone; median F1 0.91 over all tasks.
- Brief Bioinform 2026-07-01 (PMC13520796, full text read): 20,296 genomes from five species, BV-BRC, 0 mentions of "Pathogen Detection", ceftriaxone mentioned once (for A. baumannii class imbalance); mean F1 0.804 to 0.932 across species.
- Abstract only: IJERPH 2026-04-27 (17,122 BV-BRC E. coli isolates, XGBoost accuracy 0.86 overall); Can J Microbiol 2025 (4300 E. coli genomes, k-mer models, mean accuracy 93.6%); Infect Genet Evol One Health study 2026-07-24 (30,554 NCBI E. coli genomes, gradient boosting regression of MICs, R squared 0.88 for imipenem, no ceftriaxone F1 in the abstract, no PMC copy so full text unread); NPJ Antimicrob Resist 2026-05-26 (MIC prediction, 762 E. coli, external F1 0.85); AMRgen preprint (R package for concordance, not a ceftriaxone F1 benchmark); Keynome (956 clinical isolates, 97 species-drug pairs); AMR-GNN (Pseudomonas). None uses the NCBI Pathogen Detection E. coli/Shigella AST export with the paper's eligibility rules and none reports a ceftriaxone F1 near or above 97.66 on it.

arXiv (export.arxiv.org API):
- The first attempt over plain http for both queries returned HTTP 301 with an empty body at 2026-10-17T01:28:31Z (protocol redirect, no data, not a block). I then sent each query once to the https endpoint at 01:28:45Z: HTTP 200 for both, totalResults 0 for both ("Pathogen Detection" AND ceftriaxone; antimicrobial or antibiotic resistance AND Escherichia coli AND genotype or genomic AND LightGBM, gradient boosting or machine learning).

## 4. This repo (github.com/elder-plinius/V3R1T4S)
Three unauthenticated REST calls, no rate limiting, web-page fallback not used:
- Call 1 at 2026-10-17T01:29:24Z: contents of TROPHY_CASE.md on main (raw), HTTP 200, 30936 bytes, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9. Its summary lists six result families (degree-diameter graphs, constant-weight codes, matrix multiplication, the Lehmer bound, VNN-COMP counterexamples, a RobustBench attack) plus two cipher commitments. A case-insensitive search for ncbi, pathogen, ceftriaxone, coli, antibiotic, antimicrob, genotype, phenotype, shigella, amoxicillin returned nothing. No row for this target.
- Call 2 at 01:29:24Z: pulls, state=all, per_page=100, newest first, HTTP 200, 1813066 bytes, sha256 8442b4b46fada5abffa7a32bb29619109ccb252e64c59026b98c651ef0d4c7fd. This is page 1 of 3 (Link header): PRs #203 to #308, created 2026-10-16T02:31:01Z to 2026-10-17T01:03:03Z (63 open, 19 merged, 18 closed unmerged). Searching titles and bodies for ncbi, pathogen, ceftriaxone, e. coli, genotype, phenotype, shigella, antibiotic, antimicrob, lightgbm found exactly one relevant PR: #308.
- Call 3 at 01:30:33Z: search/issues with query "repo:elder-plinius/V3R1T4S is:pr ncbi" (all states, covers pages 2 and 3), HTTP 200, 3432 bytes, total_count 1, incomplete_results false. The single hit is again #308.
- PR #308: state open, draft true, created 2026-10-17T01:03:03Z, author handle verexxi, title "[claim] ncbi-pathogen-ast-ecoli-genotype-phenotype-f1: amoxicillin-clavulanic acid F1 91.97%, vs 44.5% for the published rule". Body (841 characters): LightGBM over exported AMR genotype annotations on held-out whole SNP clusters of the same pinned export PDG000000004.6366; "One antibiotic per claim"; zero mentions of ceftriaxone. It is a different antibiotic, so it neither ties nor beats a ceftriaxone figure. (That it comes from the same pipeline is my inference from the identical export and method wording; the package does not name the claimant.)
- No PR in any state (open, merged, closed) claims this target for ceftriaxone, and nothing was merged for it.

## 5. Reasoning
- Everything known for ceftriaxone on this benchmark is: the published rule at 94.6% F1 and 97.9% accuracy (live read, unchanged), and the same rule recomputed on the claim's test rows at 94.51% F1 and 97.19% accuracy (reproducible from the per-isolate file). The claim exceeds both on F1 and accuracy, so there is no tie.
- The benchmark paper is about two months old (first published 2026-08-10), has zero citing papers, and no other predictor in the searched literature reports a result on the NCBI Pathogen Detection E. coli/Shigella AST export; the nearest work uses BV-BRC labels, random splits, other species or other targets (MIC) and is not comparable and not higher.
- The repo holds no ceftriaxone claim. The only same-target PR is for another antibiotic. The success criterion is stated per antibiotic ("for at least one of the eight antibiotics ... for that antibiotic"), so a claim on a different antibiotic does not compete. If the maintainers instead treat the target as one record, #308 pre-dates this claim, but that would be a process question, not a tie or a loss on the ceftriaxone figure.
- The margin over the published value (3.057 points) clears the 3-point rule even at the least favorable rounding of the paper's 94.6 (3.007).

## 6. Limits of this check (what I could not confirm)
- Absence of evidence: Europe PMC and arXiv keyword searches cannot prove that no unindexed preprint, thesis or repository result exists. Q1 had 399 hits and I read only the first 100 titles.
- Repo: PRs #1 to #202 were covered only by the search call (text containing "ncbi"), not enumerated one by one; a ceftriaxone claim worded without "ncbi" in title, body or comments would be missed. I did not list the files of PR #308 (REST budget of 3 used), so I cannot rule out ceftriaxone files inside that PR's folder; its title, body and the "one antibiotic per claim" rule point to amoxicillin-clavulanic acid only.
- Wan et al.'s ceftriaxone numbers are only in a figure that I did not read; the One Health MIC paper's full text was not available.
- I did not open the benchmark paper's supplementary files, re-run the model, or re-verify the rule reproduction against the paper's supplementary tables (outside novelty and outside the package).
- Outside the novelty remit but worth a statistician's look: the paired difference interval's lower end (1.21 points) is below 3 points, so the "at least 3 points" test holds on the point estimate and "outside a 95% bootstrap interval" holds if read as "above the rule's interval (96.58) / difference excludes zero", but not if read as "whole difference interval above 3 points". Also the rule recomputation is on the 1531 test rows, not on the whole new export.

## 7. Verdict
Nothing found ties or beats ceftriaxone F1 97.66% / accuracy 98.76% on this benchmark; the live published value is 94.6% / 97.9%. Novelty holds, subject to the limits in section 6.

Analysis finished 2026-10-17T01:32:35Z (last command before writing).
pass: true
