# REPRODUCE skeptic report: E. coli gentamicin claim (target ncbi-pathogen-ast-ecoli-genotype-phenotype-f1)
context: subagent (Claude Code on the owner's PC, fresh context, Sonnet)

## Verdict in short

Every checkable number in claim/CLAIM.md for gentamicin reproduced exactly, three independent ways: (1) my own checker written from the definition before I opened claim/code, (2) the pipeline rerun as claim/REPRODUCE.md describes (run twice, byte-identical both times), (3) the paper's own supplementary tables. Model: TP 285, FP 9, TN 1316, FN 13, F1 96.2838%, accuracy 98.6445% on 1623 held-out comparisons in 1192 whole SNP clusters. Published rule recomputed on the same rows: TP 280, FP 28, TN 1297, FN 18, F1 92.4092%, accuracy 97.1657%. Published (Table 3, re-read live): F1 92.4%, accuracy 97.6%. Margin over published: +3.88 points. The model's cluster-bootstrap CI (93.68 to 98.00) excludes 92.4.

The only byte-level differences are Windows CRLF line endings (split.csv, predictions csv, two bytes at the end of the model file); the content is identical after CRLF to LF conversion and the sha256 values equal the pinned ones. Caveats I could not remove are listed in section 9 (paired-difference CI lower bound is 1.81 points, so "at least 3 points" holds for the point estimate but not for the CI bound; the margin varies from 2.12 to 6.11 points over five alternative splits; PREREG.md is cited but not in the package).

## 0. Scope and rules followed

- I used only the claim package (claim/CLAIM.md, claim/REPRODUCE.md, claim/code, claim/data, claim/result, claim/status_source). Scratch files are in work/ (next to claim/). claim/ was not written to: I ran the code from a byte-identical copy in work/rerun/code (sha256 of the four .py files identical, see section 6).
- The two NCBI files in claim/data were verified by sha256 and used in place; I did not download them again. I did send two HEAD requests (headers only, no body) to check size and Last-Modified.
- Network use: live re-read of the EuropePMC fullTextXML (HTTP 200), download of the paper's supplementary zip (HTTP 200, needed to derive the published rule independently), two HEAD requests.
- Environment: shared venv (Python 3.12.13, Windows-10-10.0.19045-SP0), pandas 3.0.6, numpy 2.5.4, scikit-learn 1.9.1, lightgbm 4.7.0 (scipy 1.18.1). These equal the pins in claim/REPRODUCE.md. Python 3.14.4 (the default python) was used only to turn the saved XML into text for reading, to probe for a PDF library and for short wait loops; the supplementary PDF text came from pdftotext.
- Heavy jobs: one at a time, started detached with a log. My three background jobs (model run 1, model run 2, five-split robustness loop) all finished with exit 0. A process check at 2026-10-17T06:33:02Z found no python process of mine still running.

## 1. The definition my checker was written from (quoted)

Kit instruction (verbatim): "Before reading the author's code, write your own checker from the definition (quote it). Verify every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."

Success criterion (verbatim from claim/CLAIM.md): "Success means, for at least one of the eight antibiotics, a released predictor plus a saved per-isolate prediction file on a frozen, hash-pinned export of the NCBI Pathogen Detection E. coli/Shigella metadata (export date and sha256 published), with the paper's eligibility and phenotype-mapping rules reimplemented and published as code and applied identically to both predictors, evaluated on a held-out partition split by SNP cluster (PDS accession; no cluster spans train and test, split file committed with sha256), whose F1 for that antibiotic is STRICTLY GREATER (direction: max) than the published genotype-field-inference F1 for that antibiotic, re-read live from https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML immediately before claiming (e.g. 44.5% for amoxicillin-clavulanic acid as read 2026-10-15), by at least 3 points absolute AND outside a 95% bootstrap interval over clusters, with accuracy no lower than the published accuracy for that antibiotic and the full confusion matrix reported. Because the published numbers come from a 2026-06-11 export, a claim on a newer export must also recompute the published rule on the same new export and beat that recomputation. No clinical or treatment interpretation may be attached."

Paper (saved XML, PMC13513162), the parts used:
- Table 1: "Records with assembly accession, AMR genotype field, and interpretable AST phenotype | 10,201".
- Section 4.4: "The primary genotype-phenotype concordance analysis used resistant and susceptible entries only."
- Section 4.5: "Exact duplicate rows were collapsed before analysis. Residual non-identical records sharing an isolate-antibiotic key were retained as submitted".
- Section 4.8: "The F1-score, defined as the harmonic mean of PPV and sensitivity, was calculated as 2 x TP/(2 x TP + FP + FN)." True positive = genotype-positive and phenotype-resistant.
- Table 3, gentamicin row: "Gentamicin | 7344 | 93.6%(92.1-94.9) | 98.3%(98.0-98.7) | 97.6%(97.2-97.9) | 91.1%(89.6-92.8) | 98.8%(98.5-99.1) | 96.0%(95.2-96.6) | 92.4%(91.2-93.5)" (columns: N R/S AST, sensitivity, specificity, accuracy, PPV, NPV, balanced accuracy, F1).
- Supplementary Table S3 (PDF), gentamicin: "Aminoglycoside-modifying enzymes with plausible gentamicin activity, including selected aac, aph, and ant determinants, and 16S rRNA methyltransferases such as armA, rmt genes, or npmA when present."

Split rule (claim/CLAIM.md, section "Rules reimplemented as code", last bullet): whole SNP clusters (PDS_acc from the cluster list, isolates without a PDS are singletons); an isolate is TEST when the integer value of the sha256 hex digest of the string 'V3R1T4S-ecoli-2026-10-16|' followed by the cluster name, taken modulo 100, is below 20.

## 2. Hashes, provenance, live status source

2026-10-17T06:03:22Z to 06:03:24Z, sha256sum from claim/ (all four match claim/CLAIM.md):
- data/PDG000000004.6366.metadata.tsv: 7eb4639d4aa7c621927d0a55e6d185801f4af77401c270f7ad14f3c9ce6d101b (551123573 bytes)
- data/PDG000000004.6366.reference_target.cluster_list.tsv: 58c22fd5c39d083dae3963d332c5ec25ac22c39a4f42675b37e1bb7ca954a7c8 (22021637 bytes)
- status_source/PMC13513162_fullTextXML.xml: e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685
- result/split.csv: 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca

Live status re-read at 2026-10-17T06:09:54Z: curl of https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML gave HTTP 200, 218472 bytes, content-type application/xml, sha256 e0d80a91c21492350c8bc3cbc0d00ad22d9fc912b5cc58e20c736eaf69675685; cmp reports it byte-identical to claim/status_source/PMC13513162_fullTextXML.xml. So Table 3 is unchanged and gentamicin is still F1 92.4%, accuracy 97.6%.

Export provenance at 2026-10-17T06:22:01Z (HEAD only): metadata.tsv HTTP/1.1 200 OK, Last-Modified Fri, 16 Oct 2026 03:34:08 GMT, Content-Length 551123573 (matches CLAIM.md: 2026-10-16 03:34:08 GMT, 551123573 bytes). cluster_list.tsv HTTP/1.1 200 OK, Last-Modified Fri, 16 Oct 2026 09:31:48 GMT, Content-Length 22021637 (size matches CLAIM.md; CLAIM.md gives no date for it).

Paper supplementary package: curl of https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/supplementaryFiles, 2026-10-17T06:09:59Z to 06:11:40Z, HTTP 200, 32354723 bytes, sha256 461aa4c96f77aa90bbfffac29c8d7418673132cd47ce0b383d288ae99d4e66f5 (inner ijms-27-07157-s001.zip holds NCBI_S1 to S15 and Supplementary_V5.pdf).

## 3. My own checker, part 1 (data side), written before opening claim/code

Script work/own_check1.py. It re-derives from the raw export and cluster list (no claim/code import): eligible records, gentamicin R/S labels, the cluster of every eligible isolate, the hash split, and then compares with claim/result/split.csv and claim/result/test_predictions_gentamicin.csv.

First draft (2026-10-17T06:07:07Z to 06:07:17Z) had a bug of mine: I read the TSV with quoting switched off, but NCBI wraps comma-containing fields in double quotes, so the last token of every AST string kept a trailing quote and was not read as R or S. Symptoms: only 21 trimethoprim-sulfamethoxazole R/S comparisons and eligibility of 8394/8127 records (log kept as work/own_check1_firstdraft_QUOTE_NONE.log). I found it by looking at the raw bytes, fixed it with standard CSV quoting, and confirmed the parsed row count equals the raw line count (589253 data lines). The gentamicin set was 7601 in both drafts.

Final run (2026-10-17T06:08:56Z to 06:09:05Z), values found:
- 589253 rows, target_acc unique; AST value tokens after parsing: ND 36828, R 28772, S 103047, I 2486, DD 54, NS 21; no quote left in any AST field.
- Rows with AST field 11052; with assembly accession 482961; with AMR genotype field 589235.
- R/S comparisons in the eight antibiotics (assembly and genotype present): meropenem 6451, amoxicillin-clavulanic acid 6620, ampicillin 8013, ceftriaxone 7098, ciprofloxacin 7923, gentamicin 7601, tetracycline 7304, trimethoprim-sulfamethoxazole 7337 (58347 total, same as the claim's prep log).
- Gentamicin: 7601 comparisons from 7601 isolates, R 1256, S 6345; no isolate has both an R and an S gentamicin entry (so duplicate handling cannot matter for this claim).
- Cluster list: 380990 rows, 380990 unique target_acc, 59507 PDS clusters.
- split.csv: 10836 rows. For every one of the 10836 targets, the cluster in split.csv equals the PDS_acc from the cluster list (singletons labelled NOPDS_ plus the target): 0 differences; 4220 isolates in PDS clusters, 6616 singletons, 8737 clusters. My own hash split gives the same train/test label for every target: 0 differences (train 8539, test 2297). Clusters spanning train and test: 0 of 8737.
- Gentamicin train 5978 comparisons (R 958, S 5020); test 1623 comparisons in 1192 clusters (R 298, S 1325). These equal CLAIM.md and scores_gentamicin.json (n_train 5978, n_test 1623, n_test_clusters 1192, test_R 298).
- claim/result/test_predictions_gentamicin.csv: 1623 rows, no duplicate isolates; the set of (isolate, label) pairs equals my own test set exactly (0 only-mine, 0 only-theirs); the cluster column equals mine; every isolate is TEST in my split.
- Biosample leakage check (informational): no BioSample has targets in both train and test (0 of 8476 eligible BioSamples); no BioSample has more than one eligible target.
- The claim's eligibility universe (10836 = AST field, assembly and genotype all present) is larger than "at least one R/S entry" (8476): the extra 2360 targets carry only ND-type results and no comparison for any antibiotic, so they do not affect gentamicin. All 10836 report AMRFinderPlus 4.2.7 (CLAIM.md says the same).

My eligibility and mapping logic also reproduces the paper's own records (work/own_paper_records_check.py, run on the paper's S1/S9): S1 has 495239 rows; the paper's flag eligible_genotype_phenotype is TRUE on 10201 rows and my formula (assembly, genotype, AST all present) gives 10201 with 0 rows differing; 397761 / 495203 / 10772 counts for assembly / genotype / AST equal the paper's. The long R/S table for the eight antibiotics has 56141 rows and is set-equal to the paper's NCBI_S9 (0 only-mine, 0 only-S9); per-antibiotic counts equal Table 2 (gentamicin 7344).

## 4. Fidelity of the recomputed published rule (independent of claim/code)

The paper gives gentamicin only in words (S3), so the exact rule is defined by the paper's own per-comparison predictions (NCBI_S9) and genotype strings (NCBI_S8). Scripts work/own_rule_learn.py, own_rule_learn2.py, own_rule_apply.py, own_rule_diff.py:
- NCBI_S9 has 7344 gentamicin rows (paper predicted R on 1169). Its matched markers form a whitelist of 17 genes: aac(3)-VIa, aac(3)-IId, aac(6')-Ib-cr5, aac(3)-IIe, aac(3)-IVa, rmtB1, ant(2'')-Ia, aac(6')-Ib3, armA, rmtC, aac(6')-Ib4, aac(6')-Ib, aac(3)-IIg, aac(6')-IIc, aac(6')-Ib', aac(6')-Il, aac(3)-C322.
- "Predicted R iff a COMPLETE hit of one of those 17 genes" reproduces all 7344 paper calls with 0 mismatches (also 0 with COMPLETE plus PARTIAL; 21 mismatches if PARTIAL_END_OF_CONTIG also counted; 23 if any status counts).
- Applied to the 1623 new test rows, this whitelist differs from the claim's rule_pred on 8 rows. All 8 are AST R and carry rmtE (1 row) or rmtE1 (7 rows), a gene the June data never contained. The claim's rule calls them R, which follows the paper's S3 wording "rmt genes". With my June-only whitelist the rule would be TP 272, FP 28, TN 1297, FN 26, F1 90.97%. So the claim's handling of rmtE/rmtE1 is the rule-favourable one (rule F1 92.41% instead of 90.97%), i.e. it does not inflate the model's margin.
- Other unseen aminoglycoside genes in the new gentamicin rows (aadA6, aadA25, aph(3')-VI, bare aac(3)) produce no disagreement on the test rows.
- The author's own rule check (claim/code/ecoli_rule_check.py on the paper's tables, 2026-10-17T06:17:20Z to 06:17:24Z): mismatches 0 for all eight antibiotics; gentamicin TP 1066, FP 103, TN 6102, FN 73, F1 0.923744, identical to the paper's NCBI_S10 matrix (S10: TP 1066, FP 103, TN 6102, FN 73, accuracy 0.976034858, F1 0.923743501). The other seven matrices also equal S10 line by line. (The paper's PDF Table S2 lists slightly different gentamicin counts, R 1129 versus 1139 in S10, but both give the published 92.4% and 97.6%.)

## 5. My own checker, part 2 (metrics), run on the claimed files

Script work/own_check2.py, 2026-10-17T06:15:41Z to 06:15:46Z. Labels are my own (section 3); F1 = 2TP/(2TP+FP+FN); cross-checked against scikit-learn.
- Model: TP 285, FP 9, TN 1316, FN 13; F1 96.2838%; accuracy 98.6445%; n 1623.
- Rule: TP 280, FP 28, TN 1297, FN 18; F1 92.4092%; accuracy 97.1657%.
- claim/result/scores_gentamicin.json: every confusion count, F1, accuracy, n_test, cluster count and test_R equals my recomputation.
- Threshold 0.4751: model_pred is R exactly when model_prob is at or above the threshold (0 mismatches; also 0 for strictly above).
- Cluster bootstrap, 10000 resamples of the 1192 clusters, percentile CI. Seed 20261016 (the claim's seed): model F1 93.68 to 98.00; rule F1 88.09 to 95.31; paired difference 1.81 to 6.95; model accuracy 98.00 to 99.19. Seeds 777 and 424242 give model 93.68 to 98.04 and 93.72 to 98.05, difference 1.78 to 6.78 and 1.82 to 6.90. At the claim's seed my independent implementation (work/own_boot_exact.py, 2026-10-17T06:33:20Z) matches the claimed intervals exactly: model [0.9368191721132898, 0.98], rule [0.8808976810901267, 0.9530685920577617], difference [0.01805471109083793, 0.06954306627343083], maximum absolute difference 0.0.
- Isolate-level bootstrap (the paper's unit): model 94.63 to 97.73, rule 90.10 to 94.45, difference 2.23 to 5.70.
- Discordant correctness: model right and rule wrong on 27 rows, rule right and model wrong on 3; exact two-sided sign test p = 8.43e-06.
- Bootstrap fraction of resamples with model F1 at or below the published 0.924: 0.0020. Fraction with paired difference below 3 points: 0.2239.

Criterion arithmetic from these numbers:
- F1 margin over published 92.4: +3.8838 points (needs strictly greater and at least 3): met.
- F1 margin over the rule recomputed on the same export: +3.8745 points: met.
- Accuracy 98.6445% versus published 97.6%: met (also above the recomputed rule's 97.1657%).
- Model cluster-bootstrap CI 93.68 to 98.00 excludes the published 92.4: yes. Model point F1 96.28 lies outside the recomputed rule's cluster-bootstrap CI 88.09 to 95.31: yes. Paired-difference CI 1.81 to 6.95 excludes 0: yes. Paired-difference CI lower bound at least 3 points: no (1.81).
- Full confusion matrices for model and rule are in CLAIM.md and the scores file: yes. No clinical interpretation is attached in CLAIM.md: yes.

## 6. Rerun of the pipeline as claim/REPRODUCE.md describes

Code copy: sha256 of ecoli_model.py dec8853545a7c6cbc3949f765d1b7ed644e599a39c92c4feecdc6b9b9fa4096e, ecoli_prep.py 04edd89fc224f2316896d83556fcabd43312c3173aec29a0c0a7b1c34a388e4b, ecoli_rules.py bda6261870da679c445eb236a0bf13bf4dffd6d54c3ce44285d74f915585cc3c, ecoli_rule_check.py 96b08c65b3a9a4e394c81f0b9a5a7f0e4a7fde1e87747eaa5620595ddd2206ac; the copy in work/rerun/code is identical to claim/code (diff of the hash lists empty). Commands run from work/rerun with the shared venv python, flags -P -s as in REPRODUCE.md, data read from claim/data:

1. Prep, 2026-10-17T06:17:33Z to 06:17:43Z, exit 0: python -P -s code/ecoli_prep.py (metadata tsv) (cluster list tsv) prep. Output: rows in export 589253, eligible 10836, with PDS 4220, clusters 8737; amrfinder versions among eligible {'4.2.7': 10836}; long R/S rows 58347, conflicting isolate-antibiotic keys 2; split train 8539, test 2297; gentamicin n 7601 R 1256, test n 1623 R 298.
2. Split comparison: cmp prep/split.csv against claim/result/split.csv reports "differ: char 25, line 1". Cause: pandas on Windows writes CRLF (the rerun file is 439675 bytes versus 428838, a difference of 10837 bytes, equal to the number of lines). After tr -d of CR, cmp reports identical and sha256 is 68a7e3585874da61bcab5a8f2157bd8f4cbfb0f1156a69289cb62959f0577dca, equal to the pinned hash. (Raw rerun file sha256 9b5ac08e89f7b1e8ed4d07f2d825fa805edf5a4d45b0597369eb5d463e9ce668.) So the REPRODUCE.md "cmp" line is not Windows-safe, but the split content reproduces exactly.
3. Model run 1, started 2026-10-17T06:18:14Z, finished 2026-10-17T06:20:24Z ("JOB DONE", exit 0): python -P -s code/ecoli_model.py prep rerun cluster. All eight antibiotics took about 2 minutes 10 seconds here (REPRODUCE.md estimates 3-5 minutes each).
4. Comparison with claim/result (work/compare_rerun.py):
   - rerun results.json["gentamicin"] versus claim/result/scores_gentamicin.json: 0 differing fields over diff_CI, mode, model, n_test, n_test_clusters, n_train, n_trees, oof_train_f1, rule, test_R, threshold, vocab (n_trees 243, threshold 0.4751, n_train 5978, vocab 213 on both sides; floats compared exactly).
   - rerun test_predictions.csv holds 12450 rows for all eight antibiotics; its 1623 gentamicin rows equal claim/result/test_predictions_gentamicin.csv string-exactly in all seven columns (isolate, antibiotic, cluster, AST_call, rule_pred, model_prob to six decimals, model_pred), same row order. After CRLF to LF and keeping the gentamicin lines the file is byte-identical to the claim's, sha256 75e7504f005731e2bf48b7bf8484b44a98afecd30fa4c58fbe7041eb9fb48d28 on both sides.
   - rerun model_gentamicin.txt versus claim/result/model_gentamicin.txt: identical except for two CR bytes in the last two lines (437450 versus 437448 bytes; Python text mode on Windows). After removing CR the sha256 is 75f88e78b536702a64817e5a0de4073944373d99d685ef28880f13693e3e0715 on both sides, so every tree and leaf value is identical.
5. My own checker (section 5) run on the rerun's gentamicin predictions and scores (2026-10-17T06:21:10Z): output identical to the run on the claimed files, line for line.
6. Determinism: model run 2 (python -P -s code/ecoli_model.py prep rerun2 cluster, 2026-10-17T06:21:58Z to 06:25:05Z, exit 0). results.json, test_predictions.csv and all eight model files are byte-identical to run 1 (cmp on each; sha256 of results.json 3a76c93bfb2cebc65b8f3424c76e23fbfd59978fdf01da21af0bd97342b85c54, of test_predictions.csv 6385ef7a23b8f3d697f2ef2c734493434d2ffbf4236beafe98a8e2c0d5d6938f, of the raw model_gentamicin.txt 1f70cba93f0a9d8756652990259b7dff239241752351ba7533c6454120b8a0e8, identical in both runs). Run 2's gentamicin results and predictions again equal the claim's. The claim's files were produced on another machine, so the match also shows cross-platform determinism. No non-determinism found.

## 7. Code review for leakage (done after my checker existed)

Read in full: claim/code/ecoli_prep.py, ecoli_model.py, ecoli_rules.py, ecoli_rule_check.py.
- Features (227 for gentamicin): 213 genotype-token indicators (vocabulary built from TRAIN isolates only, tokens seen in at least 10 train isolates, status class COMPLETE/POINT versus other), token count, acquired beta-lactamase count, quinolone-target point-mutation count, the published rule's R/S output for each of the eight antibiotics, collection year, scientific_name code, epi_type code. No AST_phenotypes, number_drugs_* or any label-derived column is used (the isolate table carries AST_phenotypes but featurize never reads it).
- Training and threshold: 5-fold GroupKFold by cluster on TRAIN comparisons only; trees = mean of early-stopped iterations; threshold = argmax of F1 on out-of-fold TRAIN predictions; hyperparameters are constants in the file; seed 20261016, 4 threads. Test labels appear only in the final scoring block, after predictions are computed.
- Released model importance (work/own_importance.py): the published-rule feature for gentamicin carries 69.19% of total gain; then n:aac(3)-IId 4.21%, n:sul1 3.73%, n:aac(3)-IIe 3.49%, n:aac(3)-VIa 3.18%, token count 3.05%, year 1.97%. Collection-metadata features (year, scientific_name code, epi_type code) total about 2.2% of gain. Nothing here looks like a label proxy.

## 8. Informational diagnostics (not used for the verdict)

a) Sensitivity to which 20% of clusters is TEST. I built five alternative salted cluster splits with the same hash rule (salts ALT-A to ALT-E, my own files, 0 clusters spanning train and test in each) and ran the unmodified claim/code model script on each (2026-10-17T06:26:19Z to 06:32:24Z, all exit 0). Gentamicin:

| split | n test | clusters | R | model F1 | rule F1 | margin | model acc | rule acc | paired CI |
|---|---|---|---|---|---|---|---|---|---|
| claimed split | 1623 | 1192 | 298 | 96.28 | 92.41 | 3.87 | 98.64 | 97.17 | 1.81 to 6.95 |
| ALT-A | 1572 | 1209 | 243 | 96.07 | 90.91 | 5.16 | 98.79 | 97.14 | 2.86 to 8.00 |
| ALT-B | 1445 | 1168 | 198 | 94.87 | 92.42 | 2.45 | 98.62 | 97.92 | 0.39 to 4.69 |
| ALT-C | 1502 | 1183 | 235 | 93.91 | 89.92 | 4.00 | 98.14 | 96.80 | 1.86 to 6.64 |
| ALT-D | 1525 | 1167 | 263 | 94.80 | 88.69 | 6.11 | 98.23 | 95.93 | 3.35 to 9.48 |
| ALT-E | 1416 | 1167 | 225 | 96.90 | 94.78 | 2.12 | 99.01 | 98.31 | 0.45 to 4.07 |

Over the five alternatives the margin over the recomputed rule averages 3.97 points (min 2.12, max 6.11); it is at least 3 points on 3 of 5; the paired CI excludes 0 on 5 of 5; model F1 is above the published 92.4 on 5 of 5 and model accuracy is at least 97.6 on 5 of 5. The direction is robust; the size of the margin is split-dependent. These runs only characterise the claim; they were not used to choose anything.

b) Where the rule loses. Of the rule's 28 false positives on the claimed test rows, 22 involve aac(6')-Ib-cr5 (21 alone, 1 with aac(3)-IIe); the others are 4 aac(3)-VIa, 1 aac(3)-IIe, 1 aac(6')-Ib4. A post hoc rule without the aac(6')-Ib family would score TP 279, FP 6, TN 1319, FN 19, F1 95.71%, accuracy 98.46% on these same rows (diagnostic only, it uses test labels) versus the model's 96.28% and 98.64%. So most of the model's gain over the published rule is learning that aac(6')-Ib-cr5 alone does not predict gentamicin resistance. That does not break the criterion, which asks for a released predictor that beats the published rule, but it is the honest explanation of the gain.

## 9. Mismatches, caveats, and what I could not verify

Mismatches found: none in content. Platform-only byte differences: CRLF in the rerun's split.csv (so the cmp line in REPRODUCE.md fails on Windows), in its predictions csv, and two CR bytes at the end of its model file; all identical after CRLF to LF and equal to the pinned/claimed sha256 where one exists. A bug in my own first-draft checker (quote handling) was found and fixed, see section 3.

Caveats:
1. Reading of "by at least 3 points absolute AND outside a 95% bootstrap interval over clusters". On the plain reading (point estimate at least 3 points above the published 92.4 and above the baseline's bootstrap interval, or the paired CI excluding zero) it is met: +3.88 points, model CI 93.68 to 98.00 excludes 92.4, paired CI 1.81 to 6.95 excludes 0. On a stricter reading that would require the lower CI bound itself to be at least 3 points above the baseline it is not met (lower bounds 93.68 versus 95.4, and 1.81 versus 3). In the bootstrap, 22.4% of resamples have a paired margin under 3 points.
2. Split-dependence of the margin, section 8a.
3. PREREG.md and the "test-label evaluation history" in CLAIM.md cannot be checked from the package (PREREG.md is not included). The code path itself uses no test labels before scoring and the hyperparameters are fixed constants, and the released model is exactly what that code produces from the train split, but earlier development choices are invisible to me. The criterion does not require pre-registration.
4. The published rule for genes outside the paper's data (rmtE, rmtE1) rests on the paper's S3 wording "rmt genes"; the claim's reading is the rule-favourable one (section 4).
5. The claim's eligibility universe includes records whose AST entries are all ND; harmless for gentamicin (section 3).
6. claim/code/__pycache__ holds a stale compiled file from the author's run; irrelevant to results.

## 10. Reasoning

The claim asserts specific numbers and properties. For gentamicin I re-derived the labels, the eligible comparisons, the cluster assignments and the hash split from the raw pinned export with my own code and they match the claim on every row (1623 test comparisons, 1192 clusters, 0 split disagreements, no cluster or BioSample straddling the split). I recomputed F1, accuracy, confusion matrices and the cluster-bootstrap intervals from the saved predictions and my own labels and got the claimed values, the intervals exactly at the claimed seed. I derived the published rule independently from the paper's own prediction table, showed it reproduces the paper's 7344 gentamicin calls, and showed the claim's recomputed rule differs from that reading only on 8 rmtE/rmtE1 rows in the direction that helps the rule. I reran the whole released pipeline from the pinned inputs, twice, and every number, prediction and model tree matched the claim (modulo Windows line endings), so the saved model, threshold, predictions and scores are mutually consistent and deterministic. The live status source is unchanged (byte-identical). The one thing that is not airtight is how much the margin is worth statistically (section 9, caveat 1 and 2); on the criterion as worded it is met. Nothing mismatched, nothing required was missing, and nothing was non-deterministic, so I confirm.

pass: true