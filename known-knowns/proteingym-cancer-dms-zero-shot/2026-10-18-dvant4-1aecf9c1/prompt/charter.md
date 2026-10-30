# Research charter v6 (2026-10-18)

## Thesis
Old records that were kept to be checked: ledgers, tallies, telegrams, administrative tablets. This charter brings
a data analyst's habits (reconcile the totals, join the records, distrust a match until a null says otherwise) and
a feel for how institutions and games encode rules to historical and linguistic material, where arithmetic and
record linkage can settle old questions without "reading" a lost language. Two quarries turn the same
catalogue audit on the sky's archives: variable stars, and the Apollo seismic records of the
Moon. Two more
turn it on modern reference tables: the USGS earthquake catalogue, audited against the open waveforms it was
built from, and a public variant-effect benchmark, where any gain must survive a leakage audit. Pure mathematics
is out by choice.

## Quarries

### Q0 oracle-bone
- **Question:** A frozen image-retrieval method that ranks the accepted modern character in its top 10 for more
  held-out oracle-bone characters than the best published method, on the unseen-character split of arXiv 2604.09668
  (p1, 54.3% top-10) or a HUST-OBC / EVOBC time split (p2); only then, candidate identifications for undeciphered signs.
- **Shape:** record (p1/p2, paired bootstrap p < 0.01); existence (candidate identification, expert-adjudicated).
- **Where defined:** bank `oracle-bone-undeciphered-chars` (OracleFusion arXiv 2506.21101; generative dictionary
  retrieval arXiv 2604.09668; Open-Oracle; HUST-OBC; EVOBC).
- **Status to confirm first:** the best published top-10 on each split (Open-Oracle repo, citing papers after
  2026-04), and whether the split files and dataset licences allow local training.
- **Why us:** a time split is a held-out test set, and leakage between train and test is the analyst's first
  suspicion; the oracle-bone, bronze and seal forms are a record-linkage chain. Local RTX 4070 SUPER (12 GB) for
  overnight training.
- **Weight:** 5 · **wild:** no

### Q3 ebl-orphans
- **Question:** Two or more unidentified eBL cuneiform fragments that duplicate each other: witnesses of a
  composition nobody has reconstructed.
- **Shape:** existence.
- **Where defined:** bank `ebl-unidentified-fragment-overlaps` (Simonjetz et al., LREC-COLING 2024).
- **Status to confirm first:** eBL API statistics, and whether a candidate pair already has a join or reference.
- **Why us:** large-scale fuzzy matching and dedup is everyday data work; patience over many nights.
- **Weight:** 3 · **wild:** yes

### Q7 akkadian-lacunae
- **Question:** A frozen system that restores masked words in Akkadian transliterations with hit@5 and MRR both
  strictly above MBERT+Akk (0.89 / 0.83) and above a reproduced baseline on the same frozen 80/20 by-text split.
- **Shape:** record (full criterion); p1 one metric or a genre subset; p2 a sealed natural-lacuna holdout.
- **Where defined:** bank `akkadian-lacuna-restoration-heldout` (Lazar, Saret, Yehudai, Horowitz, Wasserman &
  Stanovsky, EMNLP 2021, arXiv 2109.04513; SLAB-NLP/Akk data and code).
- **Status to confirm first:** the repository commit (dfd2a66d), any later paper reporting hit@k or MRR on this task,
  and that the reproduced baseline lands within 0.02 of hit@5 0.89 before anything else is trained.
- **Why us:** Oracc is full of parallel manuscripts and duplicate compositions, so leakage between train and test is
  the first thing to audit; formulaic passages make retrieval over the training split a record-linkage problem.
  Local GPU for overnight fine-tuning.
- **Weight:** 4 · **wild:** no

### Q8 cuneiform-detection
- **Question:** A class-agnostic cuneiform sign detector that beats the best published AP@50 and AP@75 for one
  rendering of the Mainz benchmark, on a frozen segment-level split, with the RepPoints baseline reproduced within
  0.03 AP@50 on the same split.
- **Shape:** record; p1 a margin on AP@50 or AP@90; p2 cross-rendering transfer.
- **Where defined:** bank `cuneiform-sign-detection-maicubeda` (Stotzner, Homburg & Mara 2023, arXiv 2308.11277;
  MaiCuBeDa Hilprecht, doi:10.11588/DATA/QSNIQ2, CC BY-SA 4.0).
- **Status to confirm first:** dataset file ids and hashes (about 9.3 GB), and any result on MaiCuBeDa after the 2023
  Table 2 values.
- **Why us:** patches cut from the same segment leak near-identical crops across a random split, the kind of
  inflation an analyst checks before trusting any score; local GPU for detector training.
- **Weight:** 3 · **wild:** no

### Q9 sky-variables
- **Question:** A batch of at least 10 periodic variable stars absent from VSX and from every listed machine
  catalogue (Gaia DR3 variability, ASAS-SN, ZTF periodic variables, ATLAS, CRTS, WISE, OGLE, TESS-EBs, SIMBAD
  variable types), each with its period recovered independently in two public surveys.
- **Shape:** existence (a vetted batch); partial wins: a blind calibration on 50 VSX stars, single-survey candidates,
  and a table of wrong-alias VSX periods corrected in two surveys.
- **Where defined:** bank `new-periodic-variables-not-in-vsx` (AAVSO VSX; Gaia DR3 vari_summary; Chen et al. 2020,
  ApJS 249, 18; Heinze et al. 2018, AJ 156, 241; Drake et al. 2014, 2017; Chen et al. 2018, ApJS 237, 28).
- **Status to confirm first:** the live VSX api.list response for the chosen fields, whether a machine-readable copy of
  the TESS Ten Thousand EB catalogue (arXiv 2506.05631) now exists, and the date of the newest VSX ingestion batch.
- **Why us:** the hard part is a ten-way catalogue cross-match where absence must be proven, not assumed: an
  analyst's join and anti-join, with a null run on known constant stars through the same pipeline.
- **Weight:** 4 · **wild:** no

### Q10 moonquakes
- **Question:** A new event (a member of a catalogued deep-moonquake nest, a shallow moonquake or a meteoroid impact)
  recorded on at least 2 Apollo seismic stations that the PDS expanded lunar event catalogue does not list.
- **Shape:** existence (a vetted event package); partial wins: a single-station nest member with CC >= 0.6 and the
  null passed (p1), recovery of >= 90% of one nest's catalogued events in one year with a measured false-alarm rate
  (p2), a nest relocation with formal errors >= 30% smaller than Nakamura 2005 (p3).
- **Where defined:** bank `apollo-moonquake-missed-vs-pds-catalog` (PDS Geosciences Node expanded event catalogue,
  levent.1008weber.csv, 13,057 events, built on Nakamura's catalogue and Bulow et al. 2005/2007; Apollo PSE network
  XA, stations S12/S14/S15/S16, 6.625 Hz MH* channels, 1969-1977, served by FDSN dataselect).
- **Status to confirm first:** the live PDS catalogue tables (all of them, not only levent), which years and nests
  Bulow et al. already template-matched, and any expanded deep-moonquake list published in the last 24 months.
- **Why us:** the same join and anti-join as Q9, against a closed archive: every candidate must survive a
  time-reversed and station-shifted null over the whole searched span, and must be checked against the catalogue
  by time, not by event type. Small data (a station-year is a fraction of a GB); FFT cross-correlation runs on the
  local GPU or 16 CPU cores.
- **Weight:** 4 · **wild:** no

### Q12 proteingym-cancer
- **Question:** A zero-shot variant-effect method whose Spearman correlation on a cancer-gene deep mutational scan
  in ProteinGym beats the best model column in the live DMS-level table by at least 0.015, with every weight and
  choice fixed before the target assay is scored and fitted only on assays of other proteins.
- **Shape:** record (one assay); partial wins: the same frozen method beats the best by >= 0.015 on three cancer-gene
  assays at once (p1), MSH2_HUMAN_Jia_2020 beaten by >= 0.02 (p2), and a leave-assay-out estimate of how much of the
  gap between the single best model and the ensemble ceiling is reachable without the target's labels (p3).
- **Where defined:** bank `proteingym-cancer-dms-zero-shot` (Notin et al., ProteinGym, NeurIPS 2023 Datasets and
  Benchmarks; OATML-Markslab/ProteinGym, DMS_substitutions_Spearman_DMS_level.csv and the published per-model score
  files).
- **Status to confirm first:** the repository commit and the live per-assay maxima (BRCA1 Findlay 0.560, PTEN Mighell
  0.561, MSH2 Jia 0.409 on 2026-10-13), the list of cancer-gene assays grouped by UniProt id, and any preprint after
  2026-03 reporting higher per-assay values.
- **Why us:** the labels are public, so the whole result is a leakage question: column selection, combination weights
  and same-protein assays must be ruled out before a number is believed (lens 7). p3 measures what an honest
  ensemble can reach. Combining the ~98 published score files runs on CPU; small protein models fit the local GPU.
- **Weight:** 4 · **wild:** no
- **Limits:** laboratory assay correlation only; no result is framed as variant classification for patients.

### Q13 seismic-missed
- **Question:** An earthquake at or above the regional completeness magnitude, located with >= 8 picks on >= 4 open
  stations, that the USGS ComCat catalogue and the ISC bulletin do not list, outside every published enhanced
  catalogue.
- **Shape:** existence (a vetted event package); partial wins: a missed event within 0.3 of Mc (p1), a
  template-matching catalogue for one sparse-network region and year with >= 95% recall of ComCat and >= 3x more
  detections (p2), and a ComCat event mislocated by > 20 km (p3).
- **Where defined:** bank `seismic-missed-events-vs-comcat` (USGS ComCat FDSN event service; EarthScope FDSN
  dataselect and station services; Ross et al. 2019, Science 364, 767, the QTM Southern California catalogue).
- **Status to confirm first:** the regional Mc from a live ComCat query over five years, which regions and years
  published enhanced catalogues (QTM and others) already cover, and the station coverage of the chosen
  sparse-network region.
- **Why us:** the same join and anti-join as Q9 and Q10, now on a living catalogue: Mc is computed before searching,
  and every candidate must survive a station-shifted and time-reversed null over the whole searched span and be
  checked against ComCat by time and place. The Q10 template-matching code carries over; small data per
  station-year, CPU or local GPU.
- **Weight:** 4 · **wild:** no

## Lenses

1. **auditor** (skeptic: no). Treat every tablet as a set of books. Before guessing values, list every way the
   total could legitimately differ from the sum: excluded categories, carried balances, subtotals, units changed
   mid-list. Test each as a global rule. Dead when the best rule closes no more than baseline on held-out data.
2. **record-linkage** (skeptic: no). Treat the corpus as a messy database with duplicate entities. Normalise,
   block, score pairs, and inspect the top of the list by hand. Dead when the top 50 pairs are all known joins
   or no better than a shuffled-corpus null.
3. **financial-instrument** (skeptic: no; far-import card). Ask what a real 1930s commercial or banking document
   had to carry (amount, date, parties, a test key that authenticates it) and search those generator families
   first. Dead when no published family reproduces even one line exactly.
4. **designer** (skeptic: no; backwards card). Assume a person designed the system to be used or played. Write the
   simplest procedure that would emit exactly the observed constraints, then check what else it predicts. Dead
   when the procedure needs a per-message table to fit.
5. **brute-patience** (skeptic: no; brute-scale card). Write a fast exact evaluator, then search a well-defined
   space completely at low priority, checkpointing nightly. Dead when the space is exhausted; record the covered
   space exactly in the dossier.
6. **already-settled** (skeptic: yes). Try to show the quarry is solved, trivial, mistranscribed or ill-posed.
   Check the newest literature, disagreements between editions, and whether a "non-closing" total is really
   damage. A quarry this lens kills is a good night.

7. **leakage-audit** (skeptic: yes). For learned retrieval, restoration or detection: before trusting any accuracy, check that no hidden
   item, its variants or its near-duplicates (rubbings, parallel manuscripts, overlapping crops) appear in training data, pretraining corpora or the
   retrieval dictionary's metadata; rerun the method on a label-shuffled split as the null. Dead when the gain
   disappears after deduplication or the shuffled control matches it.
## Scout voice
Read like a careful analyst auditing a dataset someone else built: who made it, which edition, what was normalised
away, where the totals come from. Prefer primary editions and data repositories over summaries. Note units, dates
and money explicitly.

## Attacker voice
Patient, quantitative, unsentimental about favourite hypotheses. Lives for the moment a column finally sums.
Would rather report a clean null than a pretty story.

## Heuristics
1. Arithmetic before meaning: a total that balances outranks a reading that "makes sense".
2. Every match gets a shuffled-corpus null run through the same code.
3. Transcription disagreements are data; check the photo before blaming the rule.
4. One global rule beats many local ones; count free parameters.
5. Old commercial and military systems were built from published manuals: search those first.
6. Small, complete searches beat large, capped ones.
7. Instruments lie before nature does: gaps, timing jumps, glitches and daily thermal cycles are checked before any
   detection is believed.

## Kill criteria
1. A rule that needs per-tablet or per-message choices to fit.
2. No improvement over the published baseline on held-out data.
3. A result that a shuffled or random control matches.
4. The match is already in the record's references or a newer paper.
5. The quarry's status page shows it solved.

## Self-critique
Accounting tablets attract this charter because they look like familiar data, which may hide how much damage and
editorial reconstruction sits in the numerals; expect most "new closures" to be transcription artefacts. Template
matching on Apollo data rewards whoever scans longest, and Bulow et al. already scanned many nests, so expect
most "new" moonquakes to be catalogued events, glitches or thermal moonquakes; the null over the whole searched
span is the only number that counts. Earthquake catalogues are densest where it is easiest to look, so
most "missed" earthquakes will sit below Mc, be blasts, or fall inside an enhanced catalogue someone already built;
only an event that clears Mc and the null counts. The learned-benchmark quarries (Q7, Q8, Q12)
can only beat a number, never read anything; their worth is a clean, reproducible comparison against a reproduced
baseline. On ProteinGym the published ensembles are already strong and the labels are public, so a small gain is
most likely leakage or noise until the pre-registration and the leave-assay-out fit say otherwise. Several quarries depend on community repositories whose transcriptions may disagree with the printed
editions.

## Method cards used
object-as-data, backwards, brute-scale, far-import, same-object (chosen to fit the card, not drawn at random).

## Changelog
- v2 (2026-10-14): added Q0 oracle-bone (weight 5) at the user's request ("run V3R1T4S on Chinese oracle
  bone script"), made it the first quarry, and added lens 7 leakage-audit for learned-retrieval quarries. Recorded the
  local GPU in settings.md. Everything else is unchanged from v1.
- v3 (2026-10-15): at the user's request, added the two bank targets from the 2026-10-15 feasibility ranking that
  were not yet in the charter: Q7 akkadian-lacunae (weight 4) and Q8 cuneiform-detection (weight 3). Retired Q6
  gold-bars to stay within 8 quarries: its letter-balance finding was already published (Bourdeau, 972 Cyphersolver,
  2026-09) and 11 cipher families and 7 generator families were dead (dossier). The wild mark moved to Q5 noita-eyes.
  Lens 7 now also covers restoration and detection models. Everything else is unchanged from v2.
- v4 (2026-10-15): at the user's request, retired Q1 pe-ledger (settled unreachable on current data: system rules gain
  at most 4 tablets corpus-wide, below the criterion's 5, and p3's best possible p is 0.045; see its dossier) and added
  Q9 sky-variables (bank `new-periodic-variables-not-in-vsx`, weight 4), the bank's most tractable target. The thesis
  now names the one sky-archive quarry. Everything else is unchanged from v3.
- v5 (2026-10-18): at the user's request, added Q10 moonquakes (bank `apollo-moonquake-missed-vs-pds-catalog`,
  weight 4), ranked first of the eight new earth-and-sky targets (feasibility/SKY-TARGETS-2026-10-17.md). Retired
  Q5 noita-eyes to stay within 8 quarries: weight 2, one run (NOTHING, 11 families dead, see its dossier), and the
  quarry adding least to the state of knowledge. The wild mark moved to Q4 adfgvx-1918. Added heuristic 7
  (instrument artefacts first) and replaced the self-critique's game sentence with one about the moonquake search.
  The thesis now names both sky-archive quarries. Also at the user's request, retired Q2 kuro-fractions (one run
  on 2026-10-14, see its dossier) and added Q11 tb-resistance (bank `cryptic-tb-resistance-beat-who-catalogue`,
  weight 4), the top pick of feasibility/BIO-TARGETS-2026-10-17.md. Everything else is unchanged from v4.
- v6 (2026-10-18): at the user's request, retired Q11 tb-resistance (one heavy run, NOTHING: the WHO 2023 catalogue
  was not beaten at equal specificity, p2 flawed, p3 0, and the grade-3 side lead died; see its dossier) and Q4
  adfgvx-1918 (no new same-key traffic; our attacks lack power at these lengths, see its dossier). Added Q12
  proteingym-cancer (bank `proteingym-cancer-dms-zero-shot`, weight 4, rank 2 of feasibility/BIO-TARGETS-2026-10-17.md)
  and Q13 seismic-missed (bank `seismic-missed-events-vs-comcat`, weight 4, rank 1 of
  feasibility/UNSCREENED-2026-10-18.md). The wild mark moved to Q3 ebl-orphans. The thesis and self-critique now
  name the two new quarries instead of tuberculosis. Everything else is unchanged from v5.
