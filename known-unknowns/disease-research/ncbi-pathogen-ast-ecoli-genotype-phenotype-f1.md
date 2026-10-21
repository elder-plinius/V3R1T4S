# NCBI Pathogen Detection AST: beat the published antibiotic-specific genotype-phenotype F1 for Escherichia coli/Shigella

🧬 **Disease research** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-20

## The problem

NCBI Pathogen Detection publishes, with no login, a single metadata table per organism group that links assembly accessions, AMRFinderPlus resistance-gene annotations and laboratory antimicrobial susceptibility (AST) results (ftp.ncbi.nlm.nih.gov/pathogen/Results/Escherichia_coli_Shigella/latest_snps/Metadata/, PDG000000004.6375.metadata.tsv, 527 MB, refreshed 2026-10-20; the file name changes with each refresh). Abdullateef Abdullah Alshehri's 2026 study in Int J Mol Sci (PMC13513162, NCBI export of 2026-06-11, AMRFinderPlus 4.2.7) froze such an export, kept 10,201 records meeting prespecified eligibility and scored 56,141 genotype-phenotype comparisons across eight priority antibiotics: concordance is high for tetracycline (accuracy 98.4%, F1 98.1%) and ceftriaxone (97.9%, 94.6%) but collapses for amoxicillin-clavulanic acid (73.6%, 44.5%). The gap between a gene-presence lookup and the measured phenotype for beta-lactam/inhibitor combinations is a real, open diagnostics problem, and the whole benchmark is one tab-separated file plus public assemblies.

## What counts as a win

Success means, for at least one of the eight antibiotics, a released predictor plus a saved per-isolate prediction file on a frozen, hash-pinned export of the NCBI Pathogen Detection E. coli/Shigella metadata (export date and sha256 published), with the paper's eligibility and phenotype-mapping rules reimplemented and published as code and applied identically to both predictors, evaluated on a held-out partition split by SNP cluster (PDS accession; no cluster spans train and test, split file committed with sha256), whose F1 for that antibiotic is STRICTLY GREATER (direction: max) than the published genotype-field-inference F1 for that antibiotic, re-read live from https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML immediately before claiming (e.g. 44.5% for amoxicillin-clavulanic acid as read 2026-10-15), by at least 3 points absolute AND outside a 95% bootstrap interval over clusters, with accuracy no lower than the published accuracy for that antibiotic and the full confusion matrix reported. Because the published numbers come from a 2026-06-11 export, a claim on a newer export must also recompute the published rule on the same new export and beat that recomputation. No clinical or treatment interpretation may be attached.

## Partial wins

- **p1:** Beat the published F1 for amoxicillin-clavulanic acid (44.5% as read 2026-10-15) by >= 5 points on a cluster-aware held-out split using only features derivable from the public metadata table (gene calls, point mutations, species, collection metadata), with confusion matrices and bootstrap intervals.
- **p2:** A reproduction result: recompute the published per-antibiotic accuracy and F1 for all eight antibiotics on a fresh export with released code, and document every discrepancy with the published values and its cause (eligibility filter, mapping rule, export date, AMRFinderPlus version).
- **p3:** A leakage demonstration: quantify how much apparent performance a random (non-cluster-aware) split adds over a cluster-aware split for the same model and antibiotic, released as code - the standard trap in surveillance-database benchmarks.

## How a win is checked

Skeptic downloads the frozen metadata table over plain HTTPS, verifies its sha256 against the claimant's, checks the committed split file against the PDS cluster assignments in the table (no cluster on both sides), reruns the attacker's released pipeline to regenerate predictions, independently reimplements the published genotype-field rule, computes both confusion matrices, F1, accuracy and bootstrap intervals over clusters, and re-reads the published table through Europe PMC. Everything is CPU-only on one tab-separated file; adding assemblies is optional and only for the richer feature sets.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML>

## Sources

- <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13513162/fullTextXML>
- <https://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/>
- <https://ftp.ncbi.nlm.nih.gov/pathogen/Results/Escherichia_coli_Shigella/latest_snps/Metadata/>
- <https://www.ncbi.nlm.nih.gov/pathogens/>

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Go beyond presence/absence: amoxicillin-clavulanate failures are driven by promoter mutations, gene copy number, porin loss and bla gene expression, so features counting multiple bla copies, IS elements upstream of ampC and truncated ompF/ompC from the assemblies attack exactly the worst antibiotic.
- CROSS-DOMAIN (coding theory / sparse recovery): treat rare determinants as a sparse support-recovery problem with gene-level groups, so alleles carried by a handful of isolates remain identifiable instead of being swamped.
- CROSS-DOMAIN (survey statistics): surveillance databases are a biased sample - submitting laboratories, countries and years correlate with resistance. Post-stratification and inverse-probability weighting by submitter/year give an honest estimate and double as a confound control.
- CROSS-DOMAIN (phylogenetics): use the SNP clusters both to build honest splits and as evidence - determinants that arise independently in many clusters (homoplasy) are mechanistically causal, unlike clade markers.
- CROSS-DOMAIN (measurement-error modelling from psychometrics): AST results come from different methods and breakpoint versions; model the phenotype as a noisy ordinal measurement with laboratory-specific thresholds rather than as truth.
- Rule learning for auditability: small boolean rules over determinants (set cover, ILP) give clinically inspectable logic, which is what a diagnostics lab can actually adopt.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Population-structure leakage: E. coli is clonal enough that random splits put near-identical isolates on both sides; only SNP-cluster-aware splits count and the skeptic must recheck them.
- Eligibility-filter drift: the published numbers depend on a specific eligibility rule and phenotype mapping (which intermediate calls are kept, which AST standards are accepted). Changing the filter after seeing results manufactures gains.
- Export drift: the metadata table is regenerated continuously and AMRFinderPlus versions change, so a claim on a newer export must recompute the baseline rule on that same export, not quote the paper.
- Class imbalance: for several antibiotics resistance prevalence is low, so accuracy and AUROC look fine for trivial models; F1 with confusion matrices and intervals is the only honest report.
- Scope creep: this is a database-concordance benchmark for surveillance, explicitly not diagnostic validation, and nothing here supports a treatment decision for any patient.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/disease-research/ncbi-pathogen-ast-ecoli-genotype-phenotype-f1.md
```

Already set up? Say `run V3R1T4S on ncbi-pathogen-ast-ecoli-genotype-phenotype-f1`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `ncbi-pathogen-ast-ecoli-genotype-phenotype-f1`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
