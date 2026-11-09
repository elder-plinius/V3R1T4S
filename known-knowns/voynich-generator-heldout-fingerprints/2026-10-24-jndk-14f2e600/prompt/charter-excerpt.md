## Thesis
Seeded at random (unbroken ciphers, undeciphered scripts; method cards same-object, far-import, metaphor), then
repicked by the human; `dagapeyeff-1939` re-added later by the human at weight 1. The edge: patient, multilingual
reading and reasoning that costs almost no compute. It reads
old sources in several languages and scripts, holds many competing hypotheses, freezes predictions before
testing them, and writes proofs. So the quarries reward thought per CPU-hour: identifications, hand ciphers,
held-out predictions about scripts, and proofs. Computation is used where a fast exact checker settles a question.
Since v9 the same edge is also pointed at problems with direct impact: reading clinical case descriptions as a
physician would, and vetting candidate tsunamis and volcanic hot spots in open archives, where most of the work is
ruling out artefacts. These may use more compute, but never as a substitute for the vetting.
Since v11 it also covers infectious disease and clinical genetics: drug resistance from pathogen genomes, rare
disease in clinical text, variant pathogenicity and outbreak forecasting. Here the edge is knowing the biology and
the literature well enough to choose features, rules and priors that a blind model would miss.

## Quarries
- id: `dclp-unidentified-literary-papyri`
  question: Identify at least one Greek literary papyrus that the Digital Corpus of Literary Papyri lists as unidentified (adespota) as a witness of a known work, by matching its unrestored text against open Greek corpora.
  shape: decipherment or prediction (identification judged by the bank criterion)
  where defined: bank `dclp-unidentified-literary-papyri`; DCLP EpiDoc corpus (papyri/idp.data), First1KGreek and Perseus canonical-greekLit corpora.
  status to confirm first: the record's work-level metadata at the current idp.data commit still reads adespota.
  why us: reading fragmentary Greek, knowing the literature, and refusing matches built on editors' restorations.
  weight: 5
  wild: no

- id: `tamam-shud-initialism`
  question: Find a text published before December 1948 whose consecutive word initials reproduce the Somerton Man code to the bank's tolerance.
  shape: decipherment or prediction (an exact source text and edition)
  where defined: bank `tamam-shud-initialism`; the code as transcribed on Wikipedia "Somerton Man"; Trove newspaper archive.
  status to confirm first: the Wikipedia article for any published solution since the 2022 identification.
  why us: generating and pruning candidate source genres (prayers, verse, letters, period phrasebooks) by reasoning before any corpus scan.
  weight: 4
  wild: no

- id: `voynich-generator-heldout-fingerprints`
  question: Give a manually executable generator that reproduces the Voynich text's held-out structural fingerprints, or a decisive falsification of the Naibbe cipher.
  shape: decipherment or prediction (frozen generator scored on held-out statistics) / counterexample
  where defined: bank `voynich-generator-heldout-fingerprints`; Greshko, "The Naibbe cipher", Cryptologia (2025); ZL3b and IT2a transliterations (voynich.nu).
  status to confirm first: voynich.nu transcription page and the 2026 papers cited in the bank entry.
  why us: designing hand procedures and attacking a published model's assumptions are reasoning tasks; scoring is cheap.
  weight: 4
  wild: no

- id: `linear-a-morphology-heldout`
  question: Pre-register at most 10 Linear A morphological alternations that predict a contextual variable on documents held out by site.
  shape: decipherment or prediction (frozen hypotheses, held-out score)
  where defined: bank `linear-a-morphology-heldout`; SigLA (sigla.phis.me); Navarre-AI and lineara.xyz corpora.
  status to confirm first: SigLA and recent Linear A literature for a published held-out morphology test.
  why us: proposing linguistic alternations from Linear B and Aegean comparanda, then letting held-out data judge.
  weight: 4
  wild: no

- id: `linear-a-kuro-arithmetic`
  question: Reconcile Linear A KU-RO totals and fraction-sign values by exact arithmetic on intact tablets.
  shape: bound or proof (exact assignment checked by arithmetic)
  where defined: bank `linear-a-kuro-arithmetic`; Corazza, Ferrara, Montecchi, Tamburini and Valerio, J. Archaeol. Sci. 125 (2021) 105214.
  status to confirm first: SigLA for revised readings of HT 9a and other KU-RO tablets.
  why us: careful epigraphic reading of what is and is not on the tablet before trusting any total.
  weight: 2
  wild: no

- id: `meroitic-semantic-induction`
  question: Predict meanings of unknown Meroitic words from their distribution, after validating the method on held-out known words.
  shape: decipherment or prediction (validated on held-out glosses, then frozen predictions)
  where defined: bank `meroitic-semantic-induction`; Otten and Anastasopoulos, ALP 2025 (aclanthology 2025.alp-1.11); Rilly's lexicon.
  status to confirm first: the Meroitic-Corpus repository and ALP proceedings for newer results.
  why us: distributional semantics guided by knowledge of Egyptian and Nubian context, judged on held-out words.
  weight: 3
  wild: no

- id: `cryptocellar-truppenschluessel-1941`
  question: Break one still-unbroken 1941 German Army Truppenschluessel message: both 5x5 squares and the plaintext.
  shape: decipherment or prediction (full key, exact re-encryption)
  where defined: bank `cryptocellar-truppenschluessel-1941`; Ostwald and Weierud, "Modern Cryptanalysis of the Truppenschluessel", Cryptologia; CryptoCellar message list.
  status to confirm first: the CryptoCellar TS message page for new "Broken" markers.
  why us: reading period German military language well enough to judge partial decrypts and supply cribs.
  weight: 4
  wild: no

- id: `mtc3-hutton-cipher-part-5`
  question: Recover keywords K1 and K2 that decrypt the 4,250-letter Hutton Part 5 ciphertext exactly.
  shape: decipherment or prediction (key, exact decryption)
  where defined: bank `mtc3-hutton-cipher-part-5`; MysteryTwister challenge PDF; IACR ePrint 2023/1113.
  status to confirm first: the MysteryTwister solver count for Part 5.
  why us: modelling a mutating-alphabet cipher exactly and judging English plaintext from fragments.
  weight: 4
  wild: no

- id: `erdos-699-binomial-gcd`
  question: For all n and 1 <= i < j <= n/2, is there a prime p >= i dividing gcd(C(n,i), C(n,j))? Give a counterexample or a complete proof.
  shape: counterexample / bound or proof
  where defined: bank `erdos-699-binomial-gcd`; Erdos and Szekeres (1978); erdosproblems.com/699.
  status to confirm first: erdosproblems.com/699 and its forum thread (recent partial proofs for j up to C i log^2 i).
  why us: Kummer-valuation arguments are proof work; a finite residue check backs every step.
  weight: 3
  wild: no

- id: `erdos-835-large-steiner-systems`
  question: Does some k > 2 admit a (k+1)-colouring of J(2k,k), equivalently a large set of Steiner systems S(k-1,k,2k)?
  shape: existence / bound or proof
  where defined: bank `erdos-835-large-steiner-systems`; erdosproblems.com/835.
  status to confirm first: erdosproblems.com/835 and its forum thread.
  why us: design-theoretic obstructions are found by thinking; candidate cases are checked exactly.
  weight: 3
  wild: no

- id: `site-percolation-2-uniform-lattices-thresholds`
  question: Determine a site percolation threshold of a 2-uniform lattice to uncertainty at most 2e-6, by two independent methods.
  shape: record (precision against the published table)
  where defined: bank `site-percolation-2-uniform-lattices-thresholds`; Neher, Mecke and Wagner, J. Stat. Mech. (2008) P01011, arXiv:0708.3250; Jacobsen and Scullard, Phys. Rev. Research 2 (2020) 012050, arXiv:1911.02684.
  status to confirm first: the 2-uniform table on Wikipedia "Percolation threshold".
  why us: exact critical polynomials replace brute simulation with algebra; a little compute goes a long way.
  weight: 2
  wild: no

- id: `moore-graph-57`
  question: Construct a 57-regular graph on 3250 vertices with diameter 2 and girth 5, or prove that none exists.
  shape: existence / bound or proof
  where defined: bank `moore-graph-57`; Ishida, arXiv:2606.29183; Hoffman and Singleton (1960).
  status to confirm first: arXiv listings for new work on srg(3250,57,0,1).
  why us: representation-theoretic restrictions on automorphisms are pure reasoning; each exclusion is a checkable lemma.
  weight: 2
  wild: yes

- id: `dagapeyeff-1939`
  question: Find the method and plaintext of the 395-digit 1939 challenge cipher under the bank's MTC3 criteria, or certify that no book-era method can fit it.
  shape: decipherment or prediction (single 1939-book procedure, exact re-encryption, 500-shuffle null)
  where defined: bank `dagapeyeff-1939`; MTC3 challenge PDF; Wikipedia "D'Agapeyeff cipher".
  status to confirm first: MTC3 Level X solver count and the Wikipedia article for a published solution.
  why us: the win is modeling the author, not hill-climbing; the dossier's two untried leads (bifid coordinate-split transposition; 79x5 re-collection) are cheap period-authentic probes, and its null machinery can certify a clean negative (bank partial win p1) if nothing is there.
  weight: 1
  wild: no

- id: `phenopacket-store-rare-disease-gene-prioritization`
  question: Rank the causal gene of rare-disease patients from their HPO phenotype profiles better than Exomiser or LIRICAL, on a pinned phenopacket-store release.
  shape: record (MRR and top-1 recall against a pinned, re-run reference tool)
  where defined: bank `phenopacket-store-rare-disease-gene-prioritization`; phenopacket-store releases (github.com/monarch-initiative/phenopacket-store); HPO, MONDO and HPOA releases.
  status to confirm first: the phenopacket-store releases page for the current tag, and the literature for a published evaluation on that release (which becomes the bar).
  why us: reading a patchy, publication-biased symptom list as a clinician would, and knowing genes the annotations do not yet link to those symptoms.
  weight: 4
  wild: no

- id: `tsunami-tide-gauge-signal-not-in-ncei`
  question: Find a tsunami recorded on at least two open tide gauges that the NOAA NCEI tsunami database does not list.
  shape: discovery (event bundle checked against a live catalogue)
  where defined: bank `tsunami-tide-gauge-signal-not-in-ncei`; NCEI HazEL tsunami events and runups APIs; IOC Sea Level Station Monitoring Facility.
  status to confirm first: the NCEI HazEL event search and runup search, re-queried live for the candidate's region and dates.
  why us: choosing where to look (catalogue-completeness reasoning, meteotsunami weather, small subsea quakes) and rejecting seiches, storms and gauge faults by careful reading of each record; the data is KB-MB per gauge-day.
  weight: 3
  wild: no

- id: `volcano-thermal-unrest-not-in-gvp`
  question: Find thermal unrest in Sentinel-2 imagery at a Holocene volcano on dates that no Smithsonian GVP eruption record or bulletin covers.
  shape: discovery (detection bundle checked against a live catalogue, with a null set)
  where defined: bank `volcano-thermal-unrest-not-in-gvp`; Smithsonian GVP Volcanoes of the World WFS; Sentinel-2 L2A via Element 84 Earth Search; MIROVA.
  status to confirm first: the GVP WFS eruption layer and GVP Weekly/Bulletin reports for the candidate volcano and dates.
  why us: reading GVP bulletins and regional reports in several languages to rule out known activity, and judging wildfire, glint and cloud artefacts; windowed image reads keep compute modest.
  weight: 3
  wild: no

- id: `pycox-metabric-gbsg-breast-cancer-survival`
  question: Beat the published time-dependent concordance or integrated Brier score of Kvamme, Borgan and Scheel (JMLR 2019) on METABRIC or GBSG breast-cancer survival.
  shape: record (C_td or IBS against the paper's tables, with same-fold re-runs)
  where defined: bank `pycox-metabric-gbsg-breast-cancer-survival`; Kvamme, Borgan and Scheel, JMLR 20(129) (2019); the pycox package datasets.
  status to confirm first: the JMLR paper's Tables 2 and 3, and the literature for a later published evaluation under the same protocol.
  why us: the dossier shows tuning alone fails (validation-to-test optimism); the open question is the discrimination-versus-calibration trade-off, which rewards reasoning about the model and the covariates over search.
  weight: 2
  wild: no

- id: `cryptic-tb-resistance-beat-who-catalogue`
  question: Predict Mycobacterium tuberculosis resistance to at least one of 13 drugs from genotype more sensitively than the WHO mutation catalogue, at no worse specificity, on a lineage-aware held-out split of the CRyPTIC compendium.
  shape: record (sensitivity and specificity against the WHO catalogue, head to head on the same isolates)
  where defined: bank `cryptic-tb-resistance-beat-who-catalogue`; CRyPTIC release June 2022 (EBI FTP, pinned reuse table CRyPTIC_reuse_table_20240917.csv); the WHO mutation catalogue (version pinned by the run).
  status to confirm first: the CRyPTIC reuse directory for the pinned table, and the literature for a published genotype model that already beats the catalogue on CRyPTIC.
  why us: resistance mechanisms (efflux, compensatory, promoter and frameshift mutations) are in the literature, and turning them into rules and features is reading and reasoning; the WHO catalogue guides real treatment.
  weight: 3
  wild: no

- id: `raredis-corpus-rare-disease-ner-f1`
  question: Beat the best published exact-span F1 for one entity type (rare disease, disease, sign or symptom) on the official RareDis test split.
  shape: record (micro-F1 against the published table, fixed official split)
  where defined: bank `raredis-corpus-rare-disease-ner-f1`; RareDis corpus (github.com/isegura/NLP4RARE-CM-UC3M); the RareDis paper (2022, PMC9258216).
  status to confirm first: PMC9258216 for the published F1 table, and the literature for a later result on the same split.
  why us: it is a language task on clinical text describing rare diseases, where telling a sign from a symptom from a disease name needs medical reading.
  weight: 3
  wild: no

- id: `proteingym-clinical-indels-auc`
  question: Beat the best Average_AUC on the ProteinGym clinical indel benchmark (benign versus pathogenic insertions and deletions) without any clinical label source.
  shape: record (Average_AUC against the live leaderboard CSV)
  where defined: bank `proteingym-clinical-indels-auc`; ProteinGym v1.3 (github.com/OATML-Markslab/ProteinGym), clinical_zero_shot/indels.
  status to confirm first: the live Summary_performance_clinical_indels_AUC.csv, and proteingym.org for newer entries.
  why us: a thin leaderboard (18 baselines) where reasoning about protein structure, domains and the reading frame can beat generic scores; genetic diagnosis turns on this call.
  weight: 3
  wild: no

- id: `traitgym-mendelian-zero-shot-auprc`
  question: Beat the best zero-shot AUPRC (by at least 0.02) on TraitGym's causal non-coding variants for 113 Mendelian traits.
  shape: record (AUPRC against the published per-model files, with a bootstrap interval)
  where defined: bank `traitgym-mendelian-zero-shot-auprc`; TraitGym (huggingface.co/datasets/songlab/TraitGym; Benegas, Eraslan and Song, bioRxiv 2025.02.11.637758).
  status to confirm first: the mendelian_traits_matched_9 AUPRC files and the TraitGym leaderboard, re-fetched live.
  why us: causal regulatory variants follow known biology (promoters, splice regions, conserved enhancers, 5' and 3' UTR motifs) that can be written down as a zero-shot score; this is how rare-disease diagnoses outside the coding exome get found.
  weight: 3
  wild: no

- id: `amr-patric-folds-beat-published-f1`
  question: Beat the published cross-validated F1-macro for at least one species-antibiotic dataset on the frozen PATRIC folds of the HZI AMR benchmark.
  shape: record (F1-macro against the paper's per-dataset table, on the exact published folds)
  where defined: bank `amr-patric-folds-beat-published-f1`; Hu et al., Briefings in Bioinformatics 2024 (PMC11070729); github.com/hzi-bifo/AMR_benchmarking.
  status to confirm first: PMC11070729's per-dataset tables, and the literature for a later result on the same folds.
  why us: the paper shows rule-based ResFinder rivalling ML on some datasets, so curated knowledge of resistance genes and point mutations is an edge; antibiotic resistance is a top global health threat.
  weight: 3
  wild: no

- id: `dengue-2015-open-challenge-beat-published-skill`
  question: Beat the best published mean log score for one city and target of the 2015 Dengue Forecasting Project (San Juan, Iquitos), under the challenge's own data rule.
  shape: record (mean log score against the published table, all seasons, real-time data rule)
  where defined: bank `dengue-2015-open-challenge-beat-published-skill`; github.com/cdcepi/dengue-forecasting-project-2015; Johansson et al., PNAS 2019 (PMC6883829).
  status to confirm first: PMC6883829's score tables, and the literature for a later result on the same challenge data.
  why us: dengue has little forecasting infrastructure; seasonality, serotype shifts and climate lags are domain reasoning more than tuning, and the strict no-future-data rule rewards care.
  weight: 3
  wild: no

## Lenses
- key: `reader`
  title: Read it before you compute it
  text: You believe the answer is already half-written in a source nobody read closely. First moves: read the primary source and the oldest one you can reach, then footnotes, errata and non-English work; list every constraint they state or imply that current attempts ignore. The line is dead when two full sources give you no constraint that the existing work has not already used.
  skeptic: no

- key: `frozen-predictor`
  title: Predict first, then look
  text: You trust only predictions written down before the data is seen. First moves: split off held-out material (a site, a later excavation, a set of folios), write at most ten sharp predictions, then score them once. The line is dead when the predictions do no better than the stated null model on the held-out set.
  skeptic: no

- key: `obstruction`
  title: Find what forbids it
  text: You expect most of the space to be impossible, and you want the invariant that says so. First moves: write what a solution would have to satisfy (counts, parities, valuations, eigenvalue multiplicities, character constraints) and test it on the smallest cases. The line is dead when the invariant is silent on every remaining case, or when it reproduces only what is already proved.
  skeptic: no

- key: `small-cases`
  title: Solve it small, then lift it
  text: You think the pattern is visible in tiny instances. First moves: solve the smallest versions exactly, tabulate them, guess the rule, then test the rule on the next size up before believing it. The line is dead when the pattern breaks at the next size, or when the next size is out of reach and no structure explains the table.
  skeptic: no

- key: `cipher-model`
  title: Model the cipher exactly
  text: You hold that a historical cipher falls to an exact model of its procedure plus good language judgement. First moves: implement the stated procedure, check it on a solved sibling, then attack with cribs and partial decrypts read by eye; run the same scorer on shuffled text every time. The line is dead when the real ciphertext scores inside the range of the shuffled controls.
  skeptic: no

- key: `far-import`
  title: Borrow from the furthest field
  text: You think the problem looks hard only because its field lacks one tool another field has. First moves: name the same object in another field (sequence alignment, coding theory, phylogenetics, statistical mechanics) and port one of its methods. The line is dead when the imported method needs an assumption the problem violates.
  skeptic: no

- key: `settled-already`
  title: Show it is settled, trivial or ill-posed
  text: You assume the quarry is already solved, misread or badly defined until shown otherwise. First moves: check the live status, the transcription and the exact wording of the criterion; look for a known result that already implies the answer and for signals that are artefacts of formula, craft or small samples. The line is dead (for you, alive for the others) when the status, transcription and definition all hold up.
  skeptic: yes

## Scout voice
