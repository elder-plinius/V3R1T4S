# NOVELTY skeptic
context: subagent (fresh-context knowledgeWork subagent started by the parent session; given only claim/ and the kit/RUN.md step-6 NOVELTY instruction)

Instruction (kit/RUN.md step 6, verbatim): "Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value and time. Search the last 24 months of literature, this repo's TROPHY_CASE.md and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record."

Claim judged: partial win p3 in claim/CLAIM.md (fold-to-fold variance audit of the 10 histone tasks of benchmark.csv; paired sign-flip best vs second; test-sampling SE threshold from claim/objects/THRESHOLD.json and claim/objects/FOLD_AUDIT.json). For an audit-type partial win, "beats everything known" is read as: not already published, not subsumed by a published analysis.

## 1. Status source (fetched once, no retries)
- URL (status_source in claim/CLAIM.md): https://huggingface.co/spaces/InstaDeepAI/nucleotide_transformer_benchmark/blob/main/data/benchmark.csv, fetched as its raw file (same path, /resolve/main/), single request.
- Time: 2026-10-21T18:23:59Z. HTTP 200, 274 lines (header + 273 rows), resolved to space commit 90ff8dbbf126daecf33d7c0221e2e5ff241fc354.
- sha256 a93c1e722f6b15312818903dc048207845598925889f415caaf61e3af7d60ca6, identical to claim/data/benchmark.csv. The table has not moved since the claim's copy.
- Values (my own recomputation from the live file, rows with exactly 10 MCC folds, exact two-sided sign-flip over 1024 patterns), best vs second ten-fold mean MCC:
  H2AFZ Enformer 0.5186 vs NT-MS-v2-250M 0.5087, p=0.281; H3K27ac Enformer 0.5169 vs NT-MS-v2-100M 0.4932, p=0.0078;
  H3K27me3 NT-MS-v2-500M 0.6117 vs NT-1000G-2.5B 0.6028, p=0.029; H3K36me3 NT-MS-v2-500M 0.6412 vs DNABERT-2 0.6353, p=0.314;
  H3K4me1 Enformer 0.4991 vs NT-MS-v2-500M 0.4965, p=0.615; H3K4me2 Enformer 0.6183 vs NT-MS-v2-250M 0.5701, p=0.0020;
  H3K4me3 DNABERT-2 0.6462 vs Enformer 0.6412, p=0.494; H3K9ac Enformer 0.5991 vs NT-MS-v2-250M 0.5684, p=0.0156;
  H3K9me3 NT-1000G-2.5B 0.4807 vs NT-MS-v2-500M 0.4750, p=0.451; H4K20me1 NT-1000G-2.5B 0.6588 vs NT-MS-v2-500M 0.6588, p=0.996.
  The six p >= 0.05 tasks are exactly the six named in claim/CLAIM.md (H2AFZ, H3K36me3, H3K4me1, H3K4me3, H3K9me3, H4K20me1). This is a novelty-side consistency check only, not the reproduction.
- The leaderboard itself (app.py, same space) offers mean/median/min/max aggregation of the folds and no significance test or test-set uncertainty.

## 2. Literature, last 24 months (2024-10 to 2026-10), read as data
Read, and none publishes this audit:
- Dalla-Torre et al., Nature Methods 2025 (NT paper, nature.com/articles/s41592-024-02523-z and PMC11810778): shows mean MCC +/- 2 SD over the ten folds and calls models "matched (n=7) or outperformed (n=11)" by bar overlap for 2.5B vs HyenaDNA. Coarse prior acknowledgement that some gaps are within fold spread; no paired test, no best-vs-second per histone task, no test-sampling error. Does not subsume p3.
- Tang, Qi et al., "In Search of Lost DNA Sequence Pretraining", arXiv 2604.16570 (2026): reports seed-to-seed SD on NT histone tasks for their own retrained models (e.g. H3K27me3 2.85/3.57, H3K4me2 3.81 points over 3 seeds) and drops unstable tasks from their testbed. Closest prior: published evidence that NT histone tasks are noisy. It does not use benchmark.csv per-fold numbers, does not test leaderboard ranking differences, and has no test-sampling SE. Overlaps the motivation, does not subsume the claim.
- Vishniakov et al., "Genomic Foundationless Models" / "Tokenization to Transfer", bioRxiv 10.1101/2024.12.18.628606 (v1-v2+): random-init vs pretrained on the NT benchmark; no significance analysis of the leaderboard.
- GENEB (arXiv 2606.04525, ICML 2026): "aggregate leaderboards are unstable" across task categories; frozen-probe protocol, its own runs, not the NT leaderboard folds.
- "Same model, better performance" (arXiv 2510.12617): BEND shuffling artefacts up to 4%; BEND only.
- Feng et al., Nature Communications 2025 (s41467-025-65823-8): DeLong tests on its own zero-shot embedding runs; not the NT leaderboard.
- BioBench Atlas, NT histone task page (snapshot 2026-08-06): isolates benchmark.csv rows with 9/13/14 fold values as nonstandard; no significance or noise analysis.
- rewire bio benchmark catalogue (release 2026-10-16): lists the NT benchmark with 0 linked evaluations; no audit.
PENDING STATUS CHECK (not counted either way): Zeng, ..., Yeo, "Spurious model comparisons are widespread in biomedical artificial intelligence" / "Widespread use of invalid statistical tests in biomedical machine learning", bioRxiv 10.64898/2026.05.17.724301. Only the abstract was readable (doi.org and biorxiv.org timed out, the PDF returned HTTP 429, Europe PMC has no full text). It is a 184-study meta-analysis (IF >= 15) of fold-correlated CV tests; whether the NT paper is among its 184 studies, and whether it re-tested any NT comparison, could not be checked. The gate or a human should open its supplement once.

Methodological note for the gate (not a novelty failure): Zeng et al.'s abstract says tests that treat CV folds as independent inflate false positives. The claim's sign-flip test treats the 10 fold differences as exchangeable although all folds share one test set and overlapping training data. That makes p too small, so the six "not significant" tasks stay not significant (conservative direction), but the "meaningful" verdict on H3K4me2 rests partly on that test (the 2 x SE_test leg helps). CRITERION should weigh this.

## 3. This repo
- TROPHY_CASE.md: no entry about the Nucleotide Transformer benchmark, histone tasks or genomic benchmarks.
- Open pull requests (GitHub API, elder-plinius/V3R1T4S, 293 open PRs read on 2026-10-21): none mention nucleotide-transformer-benchmark-mcc; the only DNA ones are dna-codes King-table and minimizer-density claims. Issue/PR search for "nucleotide": 0 hits.
- known-unknowns/biology/nucleotide-transformer-benchmark-mcc.md lists the target as open as of 2026-10-15. Its idea "use paired tests across folds rather than comparing means" is a hint, not a published result.

## Verdict
Status source read once and unchanged (sha256 matches claim/data/benchmark.csv). In the readable literature of the last 24 months, this repo's trophy case and its open PRs, I found no published per-task paired fold test of the NT leaderboard's histone rankings and no test-sampling SE threshold applied to them. The closest priors (NT paper's +/- 2 SD bars; arXiv 2604.16570's seed-variance filter) motivate the audit but do not contain it. The p3 audit is new as far as this search reaches. One source is PENDING and not counted; the search is not exhaustive.
pass: true
