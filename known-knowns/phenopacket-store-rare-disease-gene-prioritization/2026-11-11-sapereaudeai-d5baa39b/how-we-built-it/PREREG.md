# PREREG (frozen 2026-11-11T10:41:46Z, before any LIRICAL output on an audit case exists)

Run 2 on `phenopacket-store-rare-disease-gene-prioritization`. Before this file, LIRICAL was run only on development
cases (40 included cases published BEFORE 2022-02-14, so outside the audit subset; list in work/dev_cases.txt) to
measure timing and check the output format. No audit case has been run.

## Criterion (verbatim, bank) and the target of this run
Full criterion and partial wins: copied verbatim in target.md. This run addresses p3 only:
> **p3**: A reproducible leakage/ascertainment audit: quantify how much of a reference tool's performance on this corpus is explained by the fact that the same publications generated both the phenopacket and the gene's HPO annotations (e.g. by scoring with annotation releases that predate each case's publication), released as code and numbers.

## Readings chosen up front (most favourable fair reading, fixed before results)
- R1 "reference tool" = LIRICAL, which the bank names ("Exomiser or LIRICAL, pinned version and pinned data release"). Pinned: LIRICAL 2.4.1 (lirical-cli-2.4.1.jar, `--version` = "lirical v2.4.1"), Temurin JRE 21.0.13+9, data files listed with sha256 in data/lirical_data_sha256.txt (hp.json of HPO v2026-06-06; hgnc_complete_set 2026-06-05 HGNC monthly archive; mim2gene_medgen fetched 2026-11-11; the six Jannovar .ser files of Zenodo 5410367, md5 checked against Zenodo; phenotype.hpoa = the HPO GitHub release asset of the condition's release, the same files and hashes as run 1).
  - The current HGNC file (fetched 2026-11-11) is not readable by LIRICAL 2.4.1 (a column was removed upstream, so the parser reads ensembl ids as entrez ids and aborts on a duplicate key). The 2026-06-05 archive, which predates the corpus release, is used instead. Recorded, not a choice made on results.
- R2 (run 1, unchanged) publication date = earliest of PubMed pubdate and epubdate; a release predates a case if its GitHub published_at is strictly earlier; each case gets the latest such release among the 13 run-1 releases. Per-case assignment taken unchanged from run 1's work/PRE_percase.tsv.
- R3 (run 1, unchanged) contemporary release = HPO v2026-06-06 (last release before corpus 0.1.27 of 2026-06-09).
- R4 p3 fair reading (the human's standing rule): the audit must quantify the effect with numbers, code and intervals. The bank sets no minimum effect size, so none is set here. "How much of the performance is explained" is quantified as the paired drop MRR(C) - MRR(PRE) and top1(C) - top1(PRE) on the same cases, and as the fraction of contemporary performance lost, dMRR / MRR(C).
- R5 "on this corpus": a pre-registered seeded random sample of the corpus cases for which a pre-publication release exists (run 1's temporal subset, 4,247 of the 10,189 included cases) is the corpus the audit speaks for. The confirmed scope will say exactly that and nothing wider.
- R6 LIRICAL is run in its own phenotype-only mode on the unmodified phenopacket (observed AND excluded terms, as the tool reads them), with all defaults except --parallelism 4. Its genotype input is not used (phenotype-only), so the causal gene is not given to it.

## Design (sized from measured timing; escape hatch, fixed before any audit output)
- Timing measured on development cases: `benchmark --phenotype-only` (LIRICAL's own multi-phenopacket command) took 40 s for 20 cases with 4 threads (about 1.65 s per case after about 7 s of loading); the single-case `phenopacket` command took 13 s per case and gave the same top-4 diseases and post-test probabilities as `benchmark` on development case 1. All 4,247 cases under two conditions would take about 4 h, which does not fit before the 12:30 UTC hard stop with the panel. Declared escape hatch: a seeded random sample.
- Sample: N = 500 cases, `random.Random(20261111).sample(sorted(case_ids_of_run1_temporal_subset), 500)`; file work/sample500.txt, sha256 7189abc4f04b108a9a9604743aaa0dd6ff9ad419d73afc968e56b9d3cb47e086; 211 distinct PMIDs; 12 release groups.
- Execution: release groups in the seeded order of work/group_order.txt (random.Random(20261112)); for each group, one JVM with the v2026-06-06 data directory (condition C) and then one JVM with the group's pre-publication data directory (condition PRE), each on exactly the group's cases. One JVM at a time, -Xmx1g, --parallelism 4.
- Command: `java -Xmx1g -XX:ActiveProcessorCount=4 -jar lirical-cli-2.4.1.jar benchmark --phenotype-only --parallelism 4 -d <datadir> -o <out.csv.gz> <phenopackets...>` (work/run_lirical_group.sh).

## Statistics (gene level primary)
- Candidate space: run 1's 19,274 HGNC protein-coding genes (identical to run 1).
- Disease to gene: the mim2gene_medgen file in the data directory (the file LIRICAL itself loads), rows of type "phenotype" with a numeric GeneID; OMIM:<MIM> -> NCBIGene:<GeneID> -> HGNC id via the entrez_id column of hgnc_complete_set 2026-06-05.
- Gene score in one LIRICAL output = max post_test_proba over the output's diseases linked to the gene; a gene with no linked disease scores 0. Causal gene = run 1's HGNC id for the case. Rank = expected rank under uniform random tie-breaking among exactly equal scores (parsed doubles). Per case: RR = E[1/rank], top1 = P(rank = 1), top10 = P(rank <= 10). MRR = mean RR; top-1 recall = mean top1.
- Secondary (descriptive): disease level. Candidate space = the OMIM diseases in the condition-C output of the case; disease score = post_test_proba, 0 if absent from the output; the causal disease = LIRICAL's own is_causal flag (best-ranked causal row; 0 if absent). Same expected-rank rule.
- Primary audit statistics on the cases complete in both conditions: dMRR = MRR(C) - MRR(PRE); dTop1 = top1(C) - top1(PRE); share = dMRR / MRR(C). Also MRR, top-1, top-10 per condition.
- Intervals: 95% percentile bootstrap, 2000 resamples, seed 20261111: case-level (the bank's "over cases") and publication-cluster (resample PMIDs).
- Context only (not a comparator): run 1's Python baseline values on the same sampled cases, read from run 1's PRE_percase.tsv.

## Null design
null_test: required
- N-SF (primary; this run's design is paired): 400 controls; control k swaps each case's C and PRE values with probability 1/2 (random.Random(20261111 + k)) and recomputes dMRR. The real dMRR must exceed all 400 controls.
- N2 (run 1's temporal date-permutation placebo) needs every sampled case scored under every one of the 12 releases (about 12 x the runtime); it does not fit. Declared now: N2 is not run for LIRICAL this run, and the report says so.

## Escape hatches (declared now)
- E1 time cap: if the 24 JVM runs are not finished by 11:25:00 UTC, the running JVM is stopped by its recorded PID; the analysis uses the release groups complete in both conditions, and the report lists the missing groups and counts. No other change.
- E2 tool rejects a phenopacket (parse or validation failure, or a case missing from an output): the case is dropped from BOTH conditions, counted and listed.
- E3 a causal gene without an NCBIGene id in HGNC 2026-06-05: kept; it can only score 0 (counted).

## Claim rule (p3)
A p3 partial-win claim is made if the audit above runs with LIRICAL under both conditions on the sampled cases and is released as code plus per-case numbers with the intervals above, with null_test.md written. The claim sentence states the measured drop and intervals whatever their size (R4: no minimum effect). If the real dMRR does not beat all 400 N-SF controls, the claim reads "no detectable drop" and is still reported, not hidden.

## Published baseline (step 3c)
The reference tool itself is what is audited; no score of ours is compared against it, so no improvement is claimed. Context: arXiv 2609.02473 (LIRICAL 2.4.1, 0.1.27, leave-one-publication-out, Recall@1 0.4868 -> 0.1724 on 2,227 cases). Different design and case set; context only. Our condition-C numbers on the sample are reported next to it, not compared.
