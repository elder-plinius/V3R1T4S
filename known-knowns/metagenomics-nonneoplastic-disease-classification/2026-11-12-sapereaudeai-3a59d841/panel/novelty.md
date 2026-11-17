# Novelty skeptic: metagenomics-nonneoplastic-disease-classification, partial win p3 (MetAML T2D confound audit)

context: subagent (Claude Code Agent tool, subagent_type novelty, fresh context)

Inputs read: claim/CLAIM.md, claim/status_record.md, claim/bank_entry.json, claim/audit_summary.md. Nothing else in the
run folder was opened. Verdict written 2026-11-12, about 20:20Z.

## 1. Status source (fetched once, no retry)

- URL: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4939962/fullTextXML
- Fetch: started 2026-11-12T19:54:36Z, finished by 19:54:42Z, HTTP 200, 181821 bytes, sha256
  1edb0d04fe0a69648c91edb96814d231a01adbb18e8100318017d7e88424661c. These bytes are identical to the scout's fetch in
  claim/status_record.md.
- Values read (RF on species abundance):
  - T2D 0.744 (95% CI 0.688-0.800) and WT2D 0.762 (95% CI 0.651-0.873). Quote: "we obtained very similar AUC values
    for both (0.744, 95% CI: 0.688-0.800 and 0.762, 95% CI: 0.651-0.873 for T2D and WT2D, respectively)".
  - Merged T2D+WT2D: 0.743 (markers 0.736).
  - Merged set plus the healthy controls of the cirrhosis, colorectal, HMP and IBD datasets: 0.837 (markers 0.806).
    Quote: "with a high cross-validation AUC score in predicting type-2 diabetes on the entire set of samples
    (0.837/0.806 for species abundance and marker presence using RF, respectively)".
- What the paper itself says about confounding:
  - It has no covariate-only, depth-only, study-only or within-study label-permutation control for any T2D AUC.
  - Its confounding remarks are only qualitative: "study-specific confounding factors [44, 45] are only partially
    affecting the estimation of the classification performance", and disease prediction "may be overestimated due to
    the presence of confounding factors such as active antibiotics treatment".
  - Its only shuffled-label permutation test is for the sex-classification task.
  - Its "AUC = 0.96" is HMP body-site prediction, not study-of-origin prediction. A search snippet suggested
    otherwise; I checked the full text.

## 2. The claim object

For MetAML's four published T2D AUCs, the claim quantifies how much of each AUC above 0.5 is recoverable:

- from sequencing depth, study of origin, age, BMI and country alone (logistic regression and RF on covariates);
- from the paper's species RF trained on labels permuted within each study (400 permutations);
- from a decomposition into same-study and different-study case/control pairs.

Headline numbers:

- Qin 2012: age alone gives AUC 0.735, which is 96% of the published signal.
- WT2D: BMI gives 0.672 (66%) and depth 0.661 (61%).
- Merged set: all named covariates give 0.711 (87%).
- Pooled set (published 0.837): study of origin alone gives 0.840 (101%), and the within-study-permuted species
  pipeline gives 0.760 (77%).

The novelty question is whether any published or filed work already contains this quantification for these cohorts
and these published AUCs. General statements that confounding exists do not count.

## 3. Sources checked

| # | source | URL | contains | does not contain |
|---|---|---|---|---|
| 1 | Pasolli et al. 2016 (MetAML), the status source | see section 1 | the four audited AUCs; qualitative confound caveats | any covariate-only, study-only or within-study permutation number for T2D |
| 2 | Wirbel et al. 2021 Genome Biol (SIAMCAT), full text and Additional file 1 | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8008609/fullTextXML ; https://static-content.springer.com/esm/art%3A10.1186%2Fs13059-021-02306-1/MediaObjects/13059_2021_2306_MOESM1_ESM.pdf | country/protocol confounding in Nielsen 2014 UC (UC vs controls AUROC 0.84 with Danish controls vs 0.76 Spain-only; Danish vs Spanish controls AUROC 0.96); Fig. S1 re-runs MetAML's RF AUCs; Fig. S2 shows metformin confounding in Forslund 2015 data; "control augmentation" with external controls | covariate-only, depth-only or study-only AUCs for the MetAML T2D sets; within-study label permutation; any fraction of 0.744/0.762/0.743/0.837. Closest neighbouring cell: same mechanism, different disease and cohort |
| 3 | Forslund et al. 2015 Nature (metformin) | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4681099/fullTextXML | classifiers stratified by metformin in Danish, Swedish and Chinese data | covariate-only or study-only AUCs; MetAML's numbers. Metformin is not a p3-named covariate |
| 4 | Vujkovic-Cvijin et al. 2020 Nature (host variables) | Europe PMC full text failed (section 4); abstract read from https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:33149306%20AND%20SRC:MED&format=json&resultType=core | American Gut Project; matching cases and controls on host variables reduces spurious differences | MetAML cohorts or AUCs |
| 5 | Mei et al. 2024 Nat Med (8,117 metagenomes) | Europe PMC full text failed (section 4); read via https://pmc.ncbi.nlm.nih.gov/articles/PMC11620793/ | 10 cohorts including Qin_2012 and Karlsson_2013; leave-one-dataset-out RF with an age/sex/BMI-only model (average AUC 0.63 for metformin-naive T2D, 0.69 for metformin-treated) vs plus species (0.69, 0.79); study/batch handled by meta-analysis and PERMANOVA (batch variance 8.4% to 4.0%) | study-only AUC, depth, country, within-study label permutation, comparison with MetAML's AUCs. Neighbour: a covariate-only T2D baseline in a different regime |
| 6 | Ghosh et al. 2020 eLife (adjusting for age) | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7065848/fullTextXML | includes QinJ_2012 and KarlssonFH_2013; Table 1 gives QinJ_2012 age-group counts (controls young/middle/elderly 69/89/10, T2D 27/85/57); PERMANOVA age effect larger than disease effect for T2D; same- vs different-age-group classifiers | an age-only AUC or any fraction of MetAML's AUC (see section 5) |
| 7 | Dong et al. 2026 Nutr Diabetes (multi-cohort T2D) | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13057204/fullTextXML | Qin 2012 and Karlsson 2013 reads reprocessed, ages 35-80 only, single 75/25 split; bacteria RF 0.836, plus age/gender/BMI 0.871; a clinical-only model is mentioned in the Methods | the clinical-only model's value in the text; study-only, depth or permutation controls; MetAML comparison |
| 8 | Oh and Zhang 2020 Sci Rep (DeepMicro) | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7138789/fullTextXML | reuses MetAML tables (C-T2D 170/174, EW-T2D 53/43); criticises MetAML's tuning without a validation set | any confound analysis |
| 9 | LaPierre et al. 2019 Methods (MetaPheno), accepted manuscript | https://par.nsf.gov/servlets/purl/10089495 (landing page https://par.nsf.gov/biblio/10089495-metapheno-critical-evaluation-deep-learning-machine-learning-metagenome-based-disease-prediction) | in-depth T2D/obesity analysis with several learners and k-mer features | any confound analysis |
| 10 | Armour et al. 2019 mSystems | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6517693/fullTextXML | study explains 14.9% of T2D beta-diversity variation (PERMANOVA) | AUC-based quantification |
| 11 | Li et al. 2023 Gut Microbes (20 diseases, cross-cohort) | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10161951/fullTextXML | confounder adjustment with limma removeBatchEffect | covariate-only or study-only AUCs for the MetAML T2D sets |
| 12 | Gut Microbes 2025, best practices for microbiome classifiers | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11980492/fullTextXML | confounder adjustment lowers AUCs across diseases, in general | MetAML T2D quantification |
| 13 | Other MetAML-citing full texts: PMC8424122 (T2D feature selection 2021), PMC11442664 (36 studies 2024), PMC10749762 (GDmicro 2023), PMC8131609 (2021), PMC11500453 (MicroHDF 2024), PMC12849458 (AR-CDT NET 2025), PMC9868677 (2023), PMC13601785 (2026 health index; study of origin 13.0% by PERMANOVA), PMC13522148 (2026 new 82-person cohort) | https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/fullTextXML | reuse of the benchmarks, batch-correction remarks | any of the claim's quantities |
| 14 | medRxiv 2026, stage-specific T2D microbiome meta-analysis | https://www.medrxiv.org/content/10.64898/2026.01.20.25341999v1.full.pdf (PDF text did not decode); abstract via Europe PMC DOI search | 16S, 12 other studies, study-stratified permutations for PERMANOVA | MetAML cohorts or AUCs |
| 15 | Europe PMC citation and full-text queries | https://www.ebi.ac.uk/europepmc/webservices/rest/search | CITES:27400279_MED gives 462 records; restricted to T2D plus confound/batch terms gives 52, all titles screened and the relevant ones read (rows 2-13); a full-text query (T2D AND Qin/Karlsson AND metagenom* AND study-of-origin/metadata-only/covariates-alone/within-study permutation AND AUC) gives 1 hit, an unrelated ACNP 2021 poster-abstract book | any prior audit |
| 16 | MetAML code repository (from claim/bank_entry.json primary_sources) | https://github.com/(lab)/metaml, via the GitHub REST API, read-only | no releases or release assets; issues #1-#3 unrelated; head commit 52fbd54a (2020-07-28), the same as the scout's | confound analyses |
| 17 | GitHub search | gh search repos / gh search code | repository searches (metaml confound, metaml study of origin, metaml permutation, microbiome confound audit, T2D metagenome confound AUC) and a code search returned nothing relevant | |
| 18 | General web searches (about eight queries on MetAML, T2D confounding, study-of-origin and metadata-only baselines, depth as predictor, 2025-2026 reanalyses) | WebSearch | the works above | any reanalysis quantifying confounding in MetAML's T2D AUCs |

### V3R1T4S repository (https://github.com/(owner)/V3R1T4S, read-only via gh)

- TROPHY_CASE.md: no microbiome, metagenomics or T2D row.
- known-knowns/: 31 folders, none on the microbiome. A grep of the full recursive tree (7438 paths) found only two
  matches: known-unknowns/disease-research/metagenomics-nonneoplastic-disease-classification.md (the bank page, "open
  as of 2026-10-15") and an unrelated CAMI2 page.
- bank/targets.json, entry for this target: status_checked 2026-10-15; no claim recorded.
- Pull requests: all 1019 open and closed PRs (numbers 1-1071) listed, with titles, bodies and branch names grepped.
  The only metagenomics mention is #974 (CAMI2 genome binning, a different target). gh search prs found nothing for
  the target id, "MetAML", "metagenomics", "microbiome" or "confound audit". "type 2 diabetes" matched only #2, an
  unrelated matrix-multiplication claim.
- Issues: all 43 listed; none match.

## 4. Blocked or failed fetches

- Europe PMC fullTextXML for PMC11620793 (Mei 2024): HTTP 500 at 20:02:39Z. Not retried; read the PMC article page
  instead, one request.
- Europe PMC fullTextXML for PMC7677204 (Vujkovic-Cvijin 2020): HTTP 500 at 20:16:19Z. Not retried; read the abstract
  from Europe PMC metadata.
- No 401, 403, 429 or 503 responses and no challenge pages.
- No PDF renderer was available. Text from the SIAMCAT supplement and MetaPheno was decoded with a small zlib/ToUnicode
  script; the medRxiv PDF did not decode, so that source rests on its abstract.
- Paywalled full texts outside the Europe PMC open-access index were not text-searched.

## 5. Comparison with published objects (trivial-derivation check)

- **Pooled set (P2), study of origin only.** This number follows arithmetically from the published sample
  composition. Use the counts the claim uses: T2D 170/174, WT2D 53/43, and 442 controls from the four other datasets.
  Score each sample by its study's case fraction and the AUC is 0.8419, computed from counts alone with no data. The
  claim's 0.840 (LR) and 0.842 (RF) equal this. So the headline "study alone recovers 101% of the published 0.837" is
  a few-line consequence of MetAML's design and published counts. It is new as an explicit, documented statement (no
  source above, MetAML included, states it), not as an empirical discovery. It should be framed that way.
- **Qin 2012, age only (W1).** Ghosh 2020's published age-group counts imply a 3-bin age-only AUC of 0.700, which is
  82% of the published signal above 0.5. The claim's continuous-age 0.735 (96%) refines a confound whose direction and
  rough size were already visible in published data, though nobody stated it as an AUC.
- **Components no published table implies:**
  - within-study label permutation of the species RF (pooled 0.760, 77%; about 0.50 within single cohorts);
  - depth-only and BMI-only AUCs in WT2D (0.661, 0.672);
  - all-covariate AUCs per setting;
  - the same-study / different-study pair decomposition.
- **Neighbouring cells:**
  - SIAMCAT's Nielsen UC/country example: same mechanism, different cohort.
  - Mei 2024's covariate-only leave-one-dataset-out baseline: same disease, different regime and cohort set.
  - Forslund 2015: metformin.

  None gives the claimed numbers by deletion, restriction, relabelling or recombination.
- **Seeds.** The audit is seeded from MetAML (abundance table, published AUCs) and curatedMetagenomicData (metadata).
  The claim names both.

Outside my remit, noted for the other skeptics: MetAML's Methods describe the pooled T2D set as "a total of 908
samples", while the claim's P2 set has 223 + 659 = 882.

## 6. Verdict

I found no published paper, preprint, code repository, release, V3R1T4S trophy, known-knowns entry, PR or issue that
quantifies how much of MetAML's published T2D AUCs (0.744, 0.762, 0.743, 0.837) is recoverable from sequencing depth,
study of origin, age, BMI or country alone, or from within-study label permutation. The nearest prior work shows the
mechanism on another cohort (SIAMCAT), gives a covariate-only T2D baseline in a different regime (Mei 2024), or
documents the Qin 2012 age imbalance without an AUC (Ghosh 2020).

Nothing known equals the claimed quantification, so this is not a tie with prior work. Novelty therefore holds for the
audit as a whole, with two caveats the claim text should carry:

1. The pooled study-only AUC (0.842) is arithmetically implied by MetAML's published sample counts.
2. The Qin 2012 age confound was already visible in Ghosh et al. 2020's published age-group table (implied about 0.70).

Whether the audit meets the p3 wording is for the criterion skeptic, and whether it reproduces is for the reproduce
skeptic.

novelty: PASS (no prior equivalent quantification found; caveats above)
pass: true
