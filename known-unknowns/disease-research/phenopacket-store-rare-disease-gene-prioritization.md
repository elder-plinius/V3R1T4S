# Rare-disease gene prioritisation: beat published ranking performance on a frozen phenopacket-store release

🧬 **Disease research** · harvest (many cells or partial wins within reach) · tractability ★★★☆☆ · compute: laptop-hours · open as of 2026-10-15

## The problem

phenopacket-store (github.com/monarch-initiative/phenopacket-store, release 0.1.27 published 2026-06-09, all_phenopackets.zip) is a large, growing, fully public corpus of GA4GH phenopackets curated from published case reports: thousands of individuals with rare Mendelian disease, each with HPO phenotype terms, the diagnosed disease (OMIM/MONDO) and the causal gene/variant. It is the standard public substrate for evaluating phenotype-driven gene and disease prioritisation (Exomiser, LIRICAL, Phen2Gene, phenotype-similarity algorithms), and the natural metrics are mean reciprocal rank and top-k recall of the causal gene/disease. The corpus is small enough to score in minutes, the ontology resources (HPO, MONDO, HPOA) are public, and the algorithmic question - how to rank a gene list from a noisy, incomplete, publication-biased phenotype profile - is wide open and almost entirely untouched by modern methods. No patient-identifiable data is involved: phenopackets are de-identified case descriptions from the literature.

## What counts as a win

Success means a released ranking method plus saved per-case ranked candidate lists over a FIXED candidate space (all protein-coding genes, or all diseases, stated in advance) for every case in a pinned phenopacket-store release (tag and asset sha256 published), using only ontology/annotation resources whose release dates precede the corpus release and excluding any resource derived from the case reports themselves, such that mean reciprocal rank AND top-1 recall both strictly exceed (direction: max) the values obtained by a publicly available reference tool (Exomiser or LIRICAL, pinned version and pinned data release, run by the claimant AND reproduced by the skeptic on the same corpus and candidate space), by at least 10% relative on MRR and outside a 95% bootstrap interval over cases. If a published evaluation on the same release exists under the same conditions (no resource derived from the case reports, the same candidate space, and the same annotation files given to every method compared), its best value is the bar instead; values published without those restrictions are reported for context but do not set the bar. The reference tool is run on the same annotation files as the claimant's method, cleaned by the same pre-stated rule (e.g. removing every annotation row that cites a PMID of the corpus). This wording applies to evaluations scored after it was adopted. Cases must not be filtered after seeing results; any exclusion rule (e.g. cases without HPO terms) must be pre-stated and applied to every method identically.

## Partial wins

- **p1:** Beat the reference tool's MRR by >= 10% relative on the subset of cases with <= 3 HPO terms (the information-poor regime where phenotype matching is weakest), with bootstrap intervals and identical candidate space.
- **p2:** Beat the reference tool on cases whose causal gene has NO HPO annotation in the pinned HPOA release (i.e. the gene is unannotated, so similarity-to-known-annotations cannot work), demonstrating a genuinely different inference route, with >= 50 such cases and full ranked lists.
- **p3:** A reproducible leakage/ascertainment audit: quantify how much of a reference tool's performance on this corpus is explained by the fact that the same publications generated both the phenopacket and the gene's HPO annotations (e.g. by scoring with annotation releases that predate each case's publication), released as code and numbers.

## How a win is checked

Skeptic downloads the pinned all_phenopackets.zip release asset (hash-checked), pins HPO/HPOA/MONDO releases, runs the reference tool (Exomiser or LIRICAL, pinned version and data) themselves on the same corpus and candidate space, runs the attacker's released method to regenerate ranked lists (bit-for-bit or documented tolerance), recomputes MRR, top-1/top-5/top-10 recall and bootstrap intervals over cases, and checks the exclusion rules and candidate spaces are identical between methods. Everything is CPU-only and minutes-scale once the resources are local.

## Is it still open?

Check the status page before you start and again before you claim anything; tables move fast.

- <https://github.com/monarch-initiative/phenopacket-store/releases>

## Sources

- <https://github.com/monarch-initiative/phenopacket-store/releases>
- <https://github.com/monarch-initiative/phenopacket-store>
- <https://hpo.jax.org/>
- <https://mondo.monarchinitiative.org/>
- The leakage is large and measurable: HPOA v2026-06-06 cites the case's own PMID for 7,646 of the 10,189 single-gene cases of 0.1.27 with observed phenotypic terms, and scoring each case with the last HPOA release published before its paper lowers LIRICAL 2.4.1's gene-level MRR by about 86% on a 500-case sample (claim PR #1058). Any 'beats the reference tool' result must state which annotation files each tool saw.
- A cleaning rule that works: remove every HPOA row whose reference field cites any PMID found in the corpus phenopackets (1,736 PMIDs in 0.1.27). Dropping a row if ANY of its references is a corpus PMID removes 25,965 of 284,703 rows of v2026-06-06. Some sources write 'PMID nnnn' with a space, which escapes a strict 'PMID:' pattern.
- LIRICAL 2.4.1 cannot read the current hgnc_complete_set.txt (a column it expects was removed upstream); a monthly HGNC archive file from before the change (e.g. 2026-06-05) works.
- Historical HPOA releases cite HPO ids that are obsolete in the current hp.json, and LIRICAL aborts on them unless they are mapped first (alt_id and replaced_by); releases v2022-02-14 and v2022-06-11 also contain a few frequency cells written n/m with n > m that LIRICAL refuses to load.
- LIRICAL 2.4.1 has an undocumented 'benchmark --phenotype-only' command that scores many phenopackets in one JVM (about 1.5-2 s per case, against about 13 s for the single-case 'phenopacket' command), with identical rankings in our checks; a full 10,189-case run takes about 4 hours on a laptop.
- Disease names and synonyms in MONDO can carry case-derived information (some MONDO synonyms cite corpus PMIDs); a method that uses them should apply the same cleaning rule as for HPOA.

## Ideas to start from

Starting points, not instructions. The best wins came from angles nobody listed.

- Information-theoretic phenotype matching done right: the classic scores (Resnik/Lin/Phenomizer) use term information content from annotation frequencies; recompute IC on a pinned HPOA, handle term incompleteness explicitly with a missing-at-random model, and score by likelihood ratio rather than similarity (the LIRICAL idea) with properly calibrated noise terms.
- CROSS-DOMAIN (coding theory / nearest-neighbour decoding): treat each disease's annotation set as a codeword over the HPO alphabet and the patient profile as a received word with erasures and substitutions; rank by maximum-likelihood decoding under an explicit erasure/noise channel (erasure probability per term depth), which is exactly the information-poor-profile problem.
- CROSS-DOMAIN (compression / MDL): rank candidate diseases by the description length of the patient profile when encoded with that disease's annotation distribution plus the ontology structure (two-part code), which penalises over-general diseases automatically and needs no tuned weights.
- CROSS-DOMAIN (linguistics / distributional semantics): learn HPO term embeddings from co-occurrence across the corpus and from ontology structure (node2vec on the DAG, PPMI-SVD on case profiles) and score by soft-cosine matching, capturing the synonymy and granularity mismatch that exact-ontology matching misses.
- CROSS-DOMAIN (signal processing on graphs): propagate patient phenotype mass over the HPO DAG and the gene-phenotype bipartite graph with heat-kernel/random-walk-with-restart diffusion, then rank genes by received mass - a cheap, strong baseline class that the rare-disease tools largely do not use.
- Ascertainment-robust design: weight evidence by whether a gene's annotations predate the case's publication, so the method is scored on prospective-style inference; this attacks the single biggest reason published numbers on literature corpora look optimistic.

## Traps

False wins others have fallen for. A claim that walks into one of these will not survive the skeptics.

- Circular annotation leakage: the HPO disease annotations are curated FROM the same case reports that the phenopackets come from, so any similarity method is partly recognising its own training data. A claim must pin annotation releases and ideally use pre-publication annotation snapshots; otherwise an apparent win measures curation overlap.
- Candidate-space inflation: ranking against a short candidate list (e.g. a 200-gene panel) instead of all protein-coding genes makes MRR look wonderful. The candidate space must be fixed, stated and identical for every method compared.
- Case filtering after the fact: dropping cases with few HPO terms, with non-Mendelian inheritance, or where the method failed, silently raises MRR. Exclusions must be pre-registered and applied to all methods.
- Release drift: phenopacket-store grows continuously (0.1.27 on 2026-06-09); comparing to a published number computed on an older release, or to a reference tool run with mismatched HPO/HPOA data releases, invalidates the comparison.
- Metric sleight of hand: top-1 recall, MRR and top-10 recall move differently; improving top-10 while top-1 falls is not a win here, and per-case bootstrap intervals are needed because corpora are dominated by a few heavily curated genes.

## Point your agent at it

```
set up V3R1T4S: https://github.com/elder-plinius/V3R1T4S and hunt known-unknowns/disease-research/phenopacket-store-rare-disease-gene-prioritization.md
```

Already set up? Say `run V3R1T4S on phenopacket-store-rare-disease-gene-prioritization`. Your agent follows [AGENTS.md](../../AGENTS.md): it re-checks the status, freezes its success rule, attacks, and only a three-skeptic panel can confirm a win.

---

_Generated from [`bank/targets.json`](../../bank/targets.json) (id `phenopacket-store-rare-disease-gene-prioritization`). Found it solved, stale or wrong? Open an issue or a pull request against that file._
