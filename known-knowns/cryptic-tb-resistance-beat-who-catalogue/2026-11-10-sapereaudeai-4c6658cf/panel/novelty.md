# Panel: NOVELTY skeptic, run 2026-11-10-1136, target cryptic-tb-resistance-beat-who-catalogue, claim p2 (leakage demonstration, ETH)

context: subagent (Agent tool, subagent_type novelty)

Started 2026-11-10T11:56:40Z (date -u); file written about 12:12Z. I read only claim/ (CLAIM.md, scout.md, PREREG.md,
PREREG.v2.md, PREREG.v3.md, null_test.md), the bank entry in repo/bank/targets.json and the read-only repo copy. I opened
nothing in attempts/, notes or other panel files, and nothing under cache/. Scratch files are in work/panel_novelty/
(fetch_log.txt, reuse_index.html, tgp/, gh_readmes/, other/). Nothing here is clinical advice.

## Question

Is this demonstration already published or filed in this repo, or an equivalent one (a quantified inflation from a
random split versus a cluster- or lineage-aware split, for the same model and drug, on the CRyPTIC reuse table, with
split files and code released)? If so, it is not new.

The claim: on the 12,287-row reuse table CRyPTIC_reuse_table_20240917.csv, for ETH (HIGH-quality R/S), one fixed
genome-wide 10-nearest-neighbour model on the released SNP distances. It scores sensitivity at 95% specificity of
0.3496 on the frozen 12-SNP single-linkage split v2, against 0.5135 to 0.6678 (mean 0.6003) on 400 random isolate-level
splits of the same TEST size. Mean inflation 0.2507 (minimum 0.1639), and all 400 random splits score higher. The
split file has sha256 3b4ed122...0a56; the 400 random TEST index sets, the per-split metrics and the code are released.

## Status source (one honest request)

- URL: https://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/reuse/
- Time: 2026-11-10T11:56:58Z. Request: curl, User-Agent "V3R1T4S-panel-novelty", 60 s timeout. Result: HTTP 200,
  2,640 bytes, sha256 c03a58ed942be8ae941c69700299a73900262ede94ffa74885ca88b3ade5843c. This matches byte for byte
  the copy the claim fetched at 11:38:39Z.
- What it shows:
  - CHANGELOG (2024-09-17 10:42, 864 B) and CRyPTIC_excluded_samples_20220607.tsv.
  - Five reuse tables: 20221019 (4.5M), 20231027 (4.6M), 20231107 (4.6M), 20231208 (4.7M) and 20240917
    (2024-09-17 10:26, 5.1M).
  - README (2021-10-21, 5.3K).
- The pinned table 20240917 is still the newest. No newer table and no new file.
- The listing contains no instructions to agents. A plain directory index cannot show a published leakage result, so
  the novelty question rests on the searches below.

## Fetch log (every network attempt; UTC)

| time | source | result |
|---|---|---|
| 11:56:58 | ftp.ebi.ac.uk .../reuse/ (curl) | HTTP 200 (above) |
| 11:57:51-11:58:12 | 7 x `gh search prs ... --state all` | rejected locally by the gh CLI (bad flag value); no request sent |
| 11:58:22-11:58:53 | `gh search prs --repo elder-plinius/V3R1T4S` for "cryptic", "tuberculosis", "TB resistance", "leakage", "mycobacterium", "WHO catalogue", "ethionamide", "cluster-aware", "CRyPTIC-tb" (open and closed) | all [] except "leakage" (6 PRs, below) |
| 11:59:07 | gh search prs "cryptic-tb-resistance-beat-who-catalogue" | [] |
| 11:59:10, 11:59:14 | gh search issues "tuberculosis", "cryptic" | [], [] |
| 11:59:18 | gh api contents/TROPHY_CASE.md (live default branch) | 200, 31,306 bytes |
| 11:59:22 | gh api contents/known-knowns (live) | 200, 31 entries |
| about 11:59-12:02 | WebSearch (8 queries, below) and WebFetch: PLOS Biol e3003539, bioRxiv AURA 2026.04.25.720842 (2 parts), bioRxiv 2024.01.31.578169v2, arXiv abs 2512.21786 | all returned content |
| 12:02:46 | gh search code "CRyPTIC_reuse_table" | 51 hits (repos below) |
| 12:02:51 | gh search repos "cryptic tuberculosis" | [] |
| 12:03:03-12:03:24 | gh api readme: waqastakkar/tgp-..., dhedhialy/tb-resistance-discovery, ankung79/TB_prediction_marker_2026, rebantamandal/tb-resistance-prediction, manidhar2006/MLNS-Project, guillermocomesanacimadevila/Read2Pred | all 200 |
| 12:03:41-12:05:06 | gh api tgp repo: metadata, tree, releases, ood_gap.svg, stage3_splits.py, figure3_generalisation.svg, config.yaml, PIPELINE.md | all 200 (no releases) |
| 12:05:09, 12:05:13 | gh api readme: sanju99/MtbQuantCNN, linfeng-wang/tb_dr_MIC3 | 200 |
| 12:05:27-12:05:35 | gh api contents: TabArena/data-foundry record, YASH4-HD/variantbridge audit, MLNS-Project ABLATION_RESULTS.md | 200 |
| about 12:06 | WebFetch nature.com/articles/s41467-026-72225-x | HTTP 303 to a cookie-authorise page; not followed |
| about 12:06 | WebFetch medrxiv.org 10.1101/2025.08.05.25333066v1.full | HTTP 403; stopped, not retried |
| 12:07:03 | Europe PMC REST search DOI:10.1038/s41467-026-72225-x (curl) | 200: PMC13315309, open access |
| 12:07:08 | gh api sanju99/MtbQuantCNN tree | 200, 421 paths |
| 12:07:17 | Europe PMC REST PMC13315309/fullTextXML (curl) | 200, 241,823 bytes |
| about 12:07-12:08 | WebFetch pmc.ncbi.nlm.nih.gov PMC10351970, PMC11326700 | 200 |
| 12:08:13-12:08:28 | gh search code "GPI_SNP_DISTANCES", "cryptic tuberculosis leakage split", "CRyPTIC GroupKFold", "cryptic lineage split random tuberculosis" | 3 hits (one repo), [], [], [] |
| 12:08:39 | gh api readme nunder/Sequence_Conservation | 200 |
| about 12:09 | WebFetch PMC12261485; arXiv html 2512.21786 | 200 |
| about 12:09 | WebFetch mdpi.com/2075-4418/15/3/279 | HTTP 403; stopped, not retried |
| 12:09:24 | Europe PMC REST search DOI:10.3390/diagnostics15030279 (curl) | 200: PMC11817661 abstract |

The Nature and medRxiv blocks concern one paper. I read its open-access full text through Europe PMC instead, which is
a separate public archive, not a retry of the blocked hosts. The MDPI block concerns a paper whose Europe PMC abstract
settles its relevance (no ETH). So no source this decision needs went unread.

## This repository (read-only)

- TROPHY_CASE.md, both the local copy (commit cf68067, 2026-11-03) and the live default branch (31,306 bytes at
  11:59:18Z). Neither has a line matching cryptic, tubercul, mycobact or leakage. This target has no trophy.
- known-knowns/: 27 entries locally and 31 live. None is for this target or for M. tuberculosis.
  - The nearest neighbouring object is known-knowns/ncbi-pathogen-ast-ecoli-genotype-phenotype-f1. It is E. coli on the
    NCBI Pathogen Detection export, and its PREREG includes a random-split leakage demonstration as that target's p3.
  - It differs in organism, dataset, drug and target, so it is not this cell.
- known-unknowns/disease-research/cryptic-tb-resistance-beat-who-catalogue.md is the bank page. It calls p2 "the
  standard trap in this dataset, reported as a methodology result" and lists population-structure leakage as a pitfall.
  The bank therefore treats the phenomenon as known and asks for a reproducible, released demonstration of it.
- Pull requests (open and closed): no PR mentions cryptic, tuberculosis, mycobacterium, WHO catalogue, ethionamide,
  cluster-aware or the target id. "leakage" matched 6 PRs on other targets (#975 roman-microlensing, #599 jarvis
  exfoliation, #974 cami2 binning, #763 iedb-mhci, #837 dreval-ldo, #568 polaris-moleculeace). None concerns TB or
  CRyPTIC. Issues: none for tuberculosis or cryptic.
- Run 1 on this target (2026-11-10-0944), according to the claim's facts, tried p2 with another model and split and
  found no leakage. Nothing was filed. That is not a prior demonstration.

## Literature, 2024-2026 (CRyPTIC models and population-structure leakage)

Search queries (WebSearch, about 11:59-12:09Z):
- CRyPTIC random vs lineage-aware split inflation
- TB phylogenetic leakage cross-validation 2025
- DataSAIL TB clades
- CRyPTIC random split cluster leakage ethionamide 2026
- leave-one-lineage-out CRyPTIC
- "Whole-genome phenotype prediction ... open problems"
- phylogeny-aware split TB deep learning
- SNP-distance cluster split GroupKFold CRyPTIC
- "DataSAIL" "PRPS" tuberculosis
- Hu/McHardy AMR benchmarking random vs phylogeny-aware
- held-out lineage / phylogenetic split CRyPTIC CNN MIC
- mSphere 2026 generalizability review

Items opened, and what each showed:

1. AURA (bioRxiv 10.64898/2026.04.25.720842, April 2026; code github.com/M-Serajian/AURA). Read in full
   (https://www.biorxiv.org/content/10.64898/2026.04.25.720842v1.full).
   - CRyPTIC isolates "randomly stratified into 80% training and 20% testing"; ETH F1 76.14%.
   - No lineage, cluster or phylogeny split and no random-vs-grouped comparison.
   - Not equivalent.
2. LLMTB (Bioinformatics 41 Suppl 1:i40, July 2025; https://pmc.ncbi.nlm.nih.gov/articles/PMC12261485/).
   - A fixed 6,250 / 5,954 CRyPTIC split, reused from MTB++, of unstated type; ETH test F1 0.7562.
   - No split comparison and no released split files.
   - Not equivalent. MTB++ (Bioinformatics 2024, btae243) is known only from a search snippet: a random train/test split.
3. CNN MIC prediction (Nat Commun 2026, s41467-026-72225-x; full text via Europe PMC PMC13315309; code
   sanju99/MtbQuantCNN, tree checked).
   - Isolates split 80/10/10, "stratified by binary resistance phenotype and primary lineage", which is a random split.
   - Lineage SNPs are used as model inputs. ETH (ETO) is included and compared with the WHO catalogue.
   - No random-vs-cluster comparison.
   - Not equivalent.
4. VAMP-Net (arXiv 2512.21786, v2 April 2026; https://arxiv.org/html/2512.21786).
   - CRyPTIC, with experiments on RIF, RFB, INH and EMB only.
   - A stratified isolate-level 80/10/10 split; no cluster split and no comparison.
   - Not equivalent.
5. Lachapelle et al., CRyPTIC k-mer MIC model (PLoS Comput Biol 20(8):e1012260, 2024-08-05;
   https://pmc.ncbi.nlm.nih.gov/articles/PMC11326700/; code github.com/AlexCryptic/Cryptic_MIC_prediction).
   - A random 75/25 split; ETH essential agreement 91.3%, sensitivity 87.4%, specificity 89.4%.
   - The published version shows no cluster or lineage split. The 2021 preprint's leave-one-site-out arm (search
     snippet) groups by site, not genomic cluster.
   - Not equivalent.
6. Predicting drug resistance ... genomic mutation analysis (Diagnostics 15:279, 2025; Europe PMC abstract
   PMC11817661; the MDPI page returned 403).
   - CRyPTIC data, EMB, INH and RIF only.
   - Not this drug, and no split comparison in the abstract.
7. Feature-weighted lineage models (Bioinformatics 39:btad428, 2023-07-10, older than 24 months;
   https://pmc.ncbi.nlm.nih.gov/articles/PMC10351970/).
   - 18,396 non-CRyPTIC isolates and a stratified random 80/20 split.
   - Lineage dependency is studied by model weighting, not by split.
   - Not equivalent.
8. Biased sampling confounds ML prediction of AMR (PLOS Biol 23(12):e3003539, 2025-12-16;
   https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3003539; code BarquistLab/AMR_prediction).
   - Random versus phylogeny-held-out splits for the same models, on E. coli, K. pneumoniae, S. enterica, S. aureus and
     S. pneumoniae.
   - No M. tuberculosis and no CRyPTIC. A neighbouring cell (other organisms), not this one.
9. Hu et al., Assessing computational predictions of AMR phenotypes (Brief Bioinform 25:bbae206, 2024;
   https://www.biorxiv.org/content/10.1101/2024.01.31.578169v2.full).
   - Random, phylogeny-aware and homology-aware folds across 11 species, including M. tuberculosis, but from PATRIC
     (Dec 2020), not CRyPTIC.
   - The authors could not build an M. tuberculosis tree, and per-dataset values sit in supplementary tables.
   - Folds are released on Mendeley (doi:10.17632/6vc2msmsxj.1), keyed by PATRIC genome IDs.
   - A neighbouring cell (other dataset), not the CRyPTIC reuse table.
10. arXiv abstract 2512.21786 (VAMP-Net, as above).

Known only from search snippets, not opened:
- KG-TRACE (arXiv 2606.26179, 2026): stratified random 70/15/15 split on a 41,460-isolate CRyPTIC v2.1.2 set; INH, RIF,
  EMB and LEV only.
- ALPAR (bioRxiv 2025.07.08.663126): DataSAIL splits on E. coli, not TB.
- Yurtseven et al. 2023 PRPS: PATRIC TB, random splits.
- James et al. 2025 open-problems review (Bioinformatics btaf206): S. aureus.
- Elseifi et al. 2026 mSphere review: a review with no new CRyPTIC experiment shown.

None of these is a random-versus-cluster comparison on CRyPTIC.

## Code (GitHub, including release assets)

`gh search code "CRyPTIC_reuse_table"` returned 51 hits in about 25 repositories. I read the README of each that looked
like a model or evaluation repository.
- No hits: dhedhialy/tb-resistance-discovery (its GroupKFold is by gene, for variant-level ranking, not an isolate split
  comparison), ankung79/TB_prediction_marker_2026 (lineage embeddings, stratified CV), rebantamandal, MLNS-Project
  (threshold-leak fix only), Read2Pred, sanju99/MtbQuantCNN, linfeng-wang/tb_dr_MIC3.
- The TabArena data-foundry record only notes that grouped regimes are possible.
- The variantbridge audit is a grant-style report.
- The only repository that uses the released GPI_SNP_DISTANCES matrix (nunder/Sequence_Conservation) studies intergenic
  conservation.

Closest prior object found: waqastakkar/tgp-Trustworthy_Genotype-to-Phenotype_AMR_Predictio.
- A public repository, created and last pushed 2026-07-05; no releases; no paper ("Citation information will be added
  on release").
- Its config pins the same table, reuse/CRyPTIC_reuse_table_20240917.csv. Its docs say "Random splits over-estimate
  performance ... the random-vs-OOD gap is a headline result".
- It commits reports/figures/ood_gap.svg, "Generalisation gap: random vs cluster-disjoint evaluation". I read the
  values from the SVG text labels and checked their x positions: for each drug the left bar is "random split (leaky)"
  and the right bar is "cluster-disjoint (OOD)".
  - AUROC for all 13 drugs: INH 0.96/0.96, RIF 0.95/0.95, EMB 0.95/0.94, AMI 0.95/0.93, KAN 0.92/0.89, RFB 0.95/0.95,
    LEV 0.94/0.92, MXF 0.93/0.92, ETH 0.94/0.91, BDQ 0.78/0.67, CFZ 0.77/0.65, DLM 0.61/0.48, LZD 0.70/0.64.
  - figure3_generalisation.svg adds a leave-one-site-out bar (ETH 0.90).
- So for ETH, a quantified random-versus-cluster-disjoint gap (0.03 AUROC) for one model on the same pinned table was
  already public, with code (src/tgp/stage3_splits.py: `random_split` versus `grouped_random_split`, seed 1337).
- How it differs from the claim, and why it does not meet p2:
  - (a) No split files are released. data/ holds only a README, and the splits/<strategy>.json files are generated
    locally. reports/metrics.csv is not committed either; only the figures are.
  - (b) Its "clusters" are MiniBatchKMeans with 200 clusters on the binary variant matrix. That gives no SNP-distance
    guarantee: a TEST isolate can have a near-identical TRAIN isolate across a k-means boundary.
  - (c) One random split against one grouped split, with no interval or null distribution on the committed figure. A
    0.03 AUROC gap is not shown to be outside split-to-split noise.
  - (d) The metric is AUROC, which the bank's pitfalls warn against for imbalanced drugs.
  - (e) The model is different: a foundation-model and variant-matrix ensemble against a 10-NN on released SNP distances.

## Reasoning

1. Same cell, inside this repository: nothing. There is no trophy, known-knowns entry, PR or issue for this target or
   for TB, so the claim duplicates nothing filed here.
2. Same cell, published literature, 2024 to 2026: every CRyPTIC model I found uses a random isolate-level split or a
   phenotype- or lineage-stratified random split. I found no paper on the CRyPTIC reuse table that quantifies
   random-split inflation against a cluster-aware split for one model and drug.
3. Same cell, public code: the tgp repository (July 2026) is the closest prior object and must be named. It already
   shows publicly that random splits on this exact pinned table give higher AUROC than cluster-disjoint splits for ETH
   with the same model (0.94 vs 0.91). The qualitative phenomenon is therefore not new, and the bank says as much
   ("the standard trap").
4. Is the claim a trivial edit of tgp's object (deletion, restriction, relabelling, symmetry, propagation, polish)? No.
   - Model, split rule, metric and control design all differ.
   - Nothing indicates it was seeded from tgp, and the claim does not cite it.
5. Does the claim strictly beat everything known on what p2 asks for? Yes. p2 asks for a reproducible demonstration
   with a quantified margin and with the split files and code released.
   - tgp releases code but no split files and no per-split metrics, and gives no evidence its 0.03 ETH gap exceeds
     noise.
   - The claim releases:
     - a committed split file with sha256 and an audited 13-SNP minimum TRAIN-TEST distance;
     - the TEST index sets of all 400 random controls;
     - per-split metrics and per-isolate predictions;
     - code.
   - Its margin is set against a 400-split random null (all 400 above; minimum margin 0.1639) and 100 alternative
     cluster-aware splits (all below the lowest random split).
   - The magnitudes use different metrics, so I do not claim a numerical "bigger gap" record. The claim is the first
     known object on this table that meets the full p2 statement, and the only same-cell prior falls short of it.
     That is not a tie.
6. Neighbouring cells do not pre-empt it. Hu et al. 2024 (PATRIC TB, released folds) and PLOS Biol 2025 (five other
   species) are other datasets or organisms, and the repo's E. coli known-knowns entry is another bank target.
7. What the novelty is: the released, null-controlled demonstration on the CRyPTIC reuse table, not the existence of
   the trap. Leakage on clonal M. tuberculosis is old news, and the PR must not say otherwise.
8. Conditions for the filing:
   - Name waqastakkar/tgp-Trustworthy_Genotype-to-Phenotype_AMR_Predictio (ood_gap.svg, ETH AUROC 0.94 random vs 0.91
     cluster-disjoint, July 2026) as the closest prior public demonstration on the same table.
   - Name Hu et al. 2024 and PLOS Biol 2025 as neighbouring-cell precedents.
   - Frame the result as a reproducible methodology artefact.

novelty: closest prior is a public code repository (tgp, 2026-07-05) with a figure-only random-vs-cluster-disjoint AUROC
gap on the same table, ETH included, and no released split files. I found no published or filed demonstration that meets
the p2 statement. The claim is new as a released, reproducible demonstration, provided it cites that prior.

pass: true
