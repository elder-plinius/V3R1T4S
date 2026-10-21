# Novelty check: ncbi-pathogen-ast-ecoli-genotype-phenotype-f1, ampicillin
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)
novelty: CONFIRMED within the kit's scope - model F1 98.80% / accuracy 98.78% strictly beats the live-read published ampicillin F1 93.9% / accuracy 94.5% (Table 3, read 2026-10-17T01:25:29Z, HTTP 200) and the recomputed rule's 94.40%; no other predictor or claim for ampicillin on this benchmark found in 24 months of literature, TROPHY_CASE.md on main, or all 300 PRs (the only same-target PR, #308, is amoxicillin-clavulanic acid, not ampicillin)

I saw only the claim package (CLAIM.md, REPRODUCE.md, code/, result/, status_source/). I did not re-run the model or the export download; this file judges novelty only, not correctness. All times are `date -u` readings from my machine. Scratch outputs of every request below are in the sibling work folder (for example ../work/status_live.xml).

## 1. Status source (the bar), fetched once, no retry
- URL: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML
- Fetched 2026-10-17T01:25:28Z to 01:25:29Z, HTTP 200, 218472 bytes, sha256 e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685.
- That sha256 is identical to the saved copy status_source/PMC13513162_fullTextXML.xml (same hash printed by sha256sum for both files), so Table 3 is unchanged since the claim's reads at 2026-10-16T17:08:10Z and 19:28:36Z.
- Paper: Int J Mol Sci 2026, 27(16):7157, "Antibiotic-Specific Genotype-Phenotype Concordance and Cross-Database Interoperability in Public Escherichia coli/Shigella WGS-AMR Metadata", XML pub-date 10 Aug 2026, DOI 10.3390/ijms27167157.
- Table 3, ampicillin row as parsed from the XML (columns: NR/S AST, Sensitivity, Specificity, Accuracy, PPV, NPV, BalancedAccuracy, F1-Score):
  7592 | 89.4% (88.4 to 90.4) | 99.0% (98.7 to 99.3) | 94.5% (94.0 to 95.0) | 98.7% (98.4 to 99.2) | 91.5% (90.5 to 92.2) | 94.2% (93.7 to 94.7) | 93.9% (93.3 to 94.4)
- So the quoted bar is ampicillin F1 93.9% and accuracy 94.5% (table note: intervals come from 10,000 isolate-level nonparametric bootstrap replicates; the claim's success criterion dates the paper's export to 2026-06-11).
- The paper reports one predictor only (the genotype rule). Its text has no machine-learning model, and the post hoc alternative analysis (Section 2.4, Supplementary Table S5) concerns amoxicillin-clavulanic acid, not ampicillin. Every ampicillin mention in the body text was read.

## 2. Claim against the bar (numbers recomputed from the package)
I recomputed both confusion matrices from result/test_predictions_ampicillin.csv (1715 rows, 1257 clusters, 1715 isolates, antibiotic ampicillin only) and compared to result/scores_ampicillin.json and CLAIM.md. All three agree.

| predictor | TP | FP | TN | FN | F1 | accuracy |
|---|---|---|---|---|---|---|
| LightGBM model (claim) | 867 | 8 | 827 | 13 | 98.8034% | 98.7755% |
| published rule recomputed on the same rows | 792 | 6 | 829 | 88 | 94.3981% | 94.5190% |
| published (Table 3, live read) | n/a | n/a | n/a | n/a | 93.9% | 94.5% |

- Margin in F1: +4.90 points over the published 93.9%, +4.41 points over the recomputed rule. Accuracy: +4.28 points over the published 94.5%. Strictly greater on every comparison; not a tie.
- Model cluster-bootstrap F1 interval 98.25% to 99.28% (from scores_ampicillin.json): its lower end is above the published upper end (94.4%) and above the recomputed rule's upper end (95.87%).
- result/split.csv sha256 (computed) 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca, equal to the value in CLAIM.md.
- Margin note for the replication panel, not a novelty issue: the paired-difference interval (3.06 to 5.88 points) clears the criterion's 3-point margin by only 0.06 at its lower end.

## 3. Literature, last 24 months (2024-10-17 to 2026-10-17), one plain request each, no retries
Europe PMC search API (resultType core, pageSize 100, all with the date filter FIRST_PDATE:[2024-10-17 TO 2026-10-17], all HTTP 200). There is no q2: that slot became the citations call.

| label | UTC time | hits | topic of the query |
|---|---|---|---|
| lookup | 2026-10-17T01:26:07Z | 1 | DOI 10.3389/fmicb.2026.1842717 (Front Microbiol 2026;17:1842717) |
| q1 | 01:27:31Z | 199 (first 100 read) | Pathogen Detection AND E. coli/Shigella AND ampicillin AND genotype/prediction/concordance |
| cites | 01:27:48Z | 0 | papers citing the benchmark paper (MED 42653162) via the citations endpoint |
| q3 | 01:27:49Z | 25 | AMRFinderPlus AND E. coli AND ampicillin AND ML terms (LightGBM, XGBoost, random forest, deep learning, and so on) |
| q4 | 01:28:17Z | 32 | genotype-phenotype / phenotype prediction AND E. coli AND ampicillin AND NCBI Pathogen / Isolates Browser / NDARO |
| q5 | 01:28:18Z | 60 | preprints only (SRC:PPR), E. coli AND ampicillin AND genotype AND prediction |
| q6 | 01:28:22Z | 25 | the benchmark paper's title phrases, or author Alshehri AA on AMR/genotype (looking for a preprint, correction or follow-up) |
| q7 | 01:28:23Z | 79 | E. coli AND ampicillin AND whole-genome AND ML AND F1 |
| q8 | 01:32:23Z | 99 | E. coli AND ampicillin AND AMRFinderPlus/ResFinder/CARD/rule-based AND concordance/sensitivity AND NARMS/Pathogen Detection |

arXiv API (export.arxiv.org), all HTTP 200: a1 (01:28:50Z) Pathogen Detection AND ampicillin gave 0; a2 (01:28:50Z) antimicrobial resistance AND E. coli AND genotype/AMRFinderPlus AND ampicillin gave 0; a3 (01:29:12Z) AMRFinderPlus gave 1 hit, off topic (a May 2026 graph-optimization paper); a4 (01:29:13Z) antimicrobial resistance AND genotype-phenotype AND E. coli gave 0.

Candidates examined and why none ties or beats the claim on this benchmark:
- Wan et al., Front Microbiol 2026;17:1842717 (PMC13160890, first published 2026-04-28). Full text fetched 2026-10-17T01:26:15Z, HTTP 200, sha256 8a5ade838bdd9686295d4a2c1969398e3dcc84a4e4fee6f325df071a17c78cf5. Phenotypes from BV-BRC, sequence data downloaded from NCBI, 1952 E. coli genomes (ampicillin S=956, R=2452 in its text), random 60:40 sample split (caret createDataPartition), H2O models. Ampicillin metrics appear only in Figure 4 (no number in the text; the abstract gives only an overall AUC range of 0.6691 to 0.9879). It is not the NCBI Pathogen Detection AST export, not cluster-held-out, and has no quotable ampicillin F1. It is reference 43 of the benchmark paper.
- stackPredAMR (Bioinform Adv 2026, DOI 10.1093/bioadv/vbag153, PMC13342711). Full text fetched 2026-10-17T01:32:25Z, HTTP 200. Data from BV-BRC, cross-validation. Ampicillin: stacked RF accuracy 0.976, F1 0.902 (its Table 3); one-layer RF accuracy 0.974, F1 0.891 (its Table 2). Different benchmark and lower F1.
- Brief Bioinform 2026 (DOI 10.1093/bib/bbag451, PMC13520796). Full text fetched 2026-10-17T01:32:41Z, HTTP 200. 20,296 genomes of five species from NCBI SRA/BioSample plus BV-BRC; abstract reports mean F1 0.804 to 0.932 across species; no ampicillin F1 value found in the text (it only notes ampicillin changed by -0.003 under lineage-blocked validation). Not this benchmark.
- CABBAGE database (Nucleic Acids Res 2026, DOI 10.1093/nar/gkag780): a data resource for benchmarking; abstract reports no ampicillin predictor result.
- Infect Genet Evol 2026 (DOI 10.1016/j.meegid.2026.105998): 30,554 NCBI E. coli genomes, gradient boosting for MICs; abstract says ampicillin predictions "showed poor agreement with observed MICs".
- Abstract-level only (not full text): an Int J Environ Res Public Health 2026 BV-BRC study (accuracy 0.86 best model), a Research Square preprint on ruminant pathogens (190 strains, precision about 85%), and a bioRxiv CRISPR-Cas marker preprint. None targets this export or reports a competing ampicillin F1.
- The remaining hits were reviews, descriptive genomic surveillance, case reports or unrelated (for example the NCBI Pathogen Isolates Browser resistance-pattern survey, which has no predictor). The benchmark paper is the top hit of q1, q4, q6 and q8, and no correction, preprint version or follow-up of it appeared.

## 4. This repository (github.com/elder-plinius/V3R1T4S)
- TROPHY_CASE.md on main: raw download 2026-10-17T01:29:16Z, HTTP 200, 30936 bytes, 100 lines, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9. It lists seven families (degree-diameter graphs, Lehmer's totient problem, matrix multiplication, VNN-COMP counterexamples, RobustBench CIFAR-100 attack, constant-weight codes, cipher-challenge commitments). Case-insensitive match counts for ncbi, pathogen, E. coli, Escherichia, ampicillin, antibiotic, antimicrobial, genotype, phenotype, AMR, Shigella and LightGBM were all 0. No ampicillin or E. coli result is recorded there.
- Pull requests, open and closed: 3 GitHub REST calls (the limit), all unauthenticated, all HTTP 200: pulls?state=all&per_page=100 page 1 at 2026-10-17T01:29:46Z, then page 2 and page 3 at 2026-10-17T01:30:40Z (rate limit remaining 55, 54, 53 of 60). The first response's Link header named page 3 as the last page. Result: 300 PRs (numbers 308 down to 1), 74 open and 226 closed.
- I scanned title, body and branch name of all 300 PRs for the target id, ncbi, pathogen, ampicillin, escherichia, e. coli, ecoli, genotype, antibiotic, "amr " and shigella. Exactly one PR matched: #308. No PR mentions ampicillin.
- PR #308 (open, draft, user verexxi, created 2026-10-17T01:03:03Z, about 26 minutes before my page 1 fetch): title "[claim] ncbi-pathogen-ast-ecoli-genotype-phenotype-f1: amoxicillin-clavulanic acid F1 91.97%, vs 44.5% for the published rule". Same target id, same pinned export PDG000000004.6366, same LightGBM approach, but amoxicillin-clavulanic acid only.
- I also read #308's README as a plain raw download from the fork branch (not a REST call): 2026-10-17T01:31:17Z, HTTP 200, 3153 bytes, sha256 6839b780a83d6ec37812dfe1e94e512d3703de37afa77606f8c65bc1a098adc6. It reports amoxicillin-clavulanic acid F1 91.97%, accuracy 97.68% (TP 189, FP 7, TN 1200, FN 26 on 1422 TEST comparisons in 1045 clusters), says "Not a claim about other antibiotics (one antibiotic per package)", and contains no ampicillin figure (a grep for ampicillin found nothing; the only antibiotic-list match was the sentence about other antibiotics).
- The README quotes its split file hash as 68a7e358...577dca, which matches the full sha256 of this claim's result/split.csv, and its credits wording matches CLAIM.md. So #308 is a sibling package built on the identical cluster split, apparently from the same pipeline; I cannot tell from this evidence whether it is the same person.

## 5. Reasoning
1. The bar is the live-read published ampicillin F1 93.9% and accuracy 94.5% (Table 3, HTTP 200, hash equal to the claim's saved copy). The claim's 98.80% and 98.78% exceed both by more than 4 points, and also exceed the rule recomputed on the same rows (94.40%, 94.52%), which the success criterion requires because the claim uses a newer export than the paper's June one. No tie.
2. "Everything known" for ampicillin on this benchmark: the only published predictor on the NCBI Pathogen Detection E. coli/Shigella AST data that I could find is the paper's own genotype rule (93.9%). The 2026 machine-learning papers I found use other datasets (BV-BRC, mixed sources), other splits (random or cross-validation) or report no usable ampicillin number, and none reports an F1 near 98.8% for ampicillin on this export. No paper cites the benchmark paper in Europe PMC yet (0 citations).
3. Repo state: TROPHY_CASE.md holds no antimicrobial result, and none of the 300 PRs claims ampicillin. The only same-target PR (#308) is a different antibiotic (amoxicillin-clavulanic acid), is a draft, and states it makes no claim about other antibiotics, so it neither ties nor beats the ampicillin number.
4. Under the kit's rule (pass only if the result strictly beats everything known), I can confirm the strict beat against every comparator I could identify, with the limits below.

## 6. Limits and caveats
- Snapshot only. #308 appeared about 26 minutes before my PR fetch; another ampicillin claim could be filed at any time, and the first PR-list page could be stale by minutes.
- Process question for the maintainers, not a novelty finding: the bank criterion says "for at least one of the eight antibiotics", so if the first accepted antibiotic counts as the win for the whole target, the order of #308 and this claim could matter.
- Search limits: Europe PMC (which indexes preprints) and arXiv only; no Google Scholar; q1 had 199 hits and only the first 100 (relevance order) were read; most candidates were judged from abstracts, and only Wan et al., stackPredAMR and the Brief Bioinform paper were checked in full text. Absence of a hit is not proof of absence. Literature older than 24 months was not searched, per the kit, so earlier AMRFinder validation studies (different datasets) were not checked.
- Clock: arXiv's response carried an updated stamp of 2026-10-17T01:29:44Z while my date -u read 01:28:50Z for that request, so my clock may run about one minute behind; every time above is my date -u reading.
- No clinical or treatment interpretation is made or implied; this is a database-concordance comparison.

pass: true
