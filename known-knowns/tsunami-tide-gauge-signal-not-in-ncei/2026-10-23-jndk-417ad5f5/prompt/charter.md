# Research charter v9 (2026-10-23)

## Changelog
- v9 (2026-10-23): added by the human, who asked for quarries with real-world impact, more compute allowed, no
  moonshots: `phenopacket-store-rare-disease-gene-prioritization`, `tsunami-tide-gauge-signal-not-in-ncei`,
  `volcano-thermal-unrest-not-in-gvp`, and `pycox-metabric-gbsg-breast-cancer-survival` (resumed; two runs on
  2026-10-16 reached `progress`, its dossier lists the dead angles). Now 18 quarries. Thesis widened to cover
  discovery in open data archives and clinical benchmarks.
- v8 (2026-10-23): retired `bb6-holdout-certificates` at the human's request: the topic no longer interests them. Preserve the verified p1 and existing p2 evidence; one bounded closeout adjudicates the existing packet, then no automatic resumption. Retirement does not assert the mathematical problem is settled.
- v7 (2026-10-20): added by the human: `dagapeyeff-1939`, re-added from v3 with weight 1. A bank
  `tractability: 2` target whose 87-year resistance puts it in the moonshot realm; kept cheap and
  low-priority on purpose. Its dossier records two untried, period-authentic leads (coordinate-split
  bifid transposition; 79x5 re-collection), so the fresh-lead value justifies a standing slot even at
  low odds, and the bank pays a partial win for a rigorous hoax/underdetermination result.
- v6 (2026-10-17): repicked the quarries by four aims: questions that reward reading, reasoning and proof more than compute; no
  plain "bigger number" hunts; problems where language skill is an advantage; problems that are interesting or useful.
- Retired, with the reason for each (their dossiers keep every result and dead angle):
  - `conway-99-graph`, `antihydra-collatz-cryptid`, `erdos-287-egyptian-gaps`: decades-old moonshots with no
    tractable foothold; the Erdos 287 candidate was dominated by a posted bound.
  - `chinese-gold-bars`, `dorabella-1897`: five and three runs, no structure beyond shuffled controls.
  - `proto-elamite-accounting-balance`: only one usable tablet under a frozen intactness rule.
  - `ebl-fragment-identification`: three runs; its controls could not separate a real match from chance.
- Added, untouched so far: `dclp-unidentified-literary-papyri`, `tamam-shud-initialism`,
  `linear-a-morphology-heldout`, `meroitic-semantic-induction`, `voynich-generator-heldout-fingerprints`,
  `cryptocellar-truppenschluessel-1941`, `mtc3-hutton-cipher-part-5`, `erdos-699-binomial-gcd`.
- Kept 14 quarries, more than the kit's 3-8: the human's explicit choice, to explore more topics.
- Thesis rewritten to state the edge, not the topics; it now records the random seeds and the later repick.
- Numerical quarries are allowed again: the thesis and kill criteria no longer contradict the percolation quarry.
- Lenses rewritten as stances with first moves and a sign of a dead line; they now disagree on purpose.
- Removed all text about machines, coordination and procedure; that lives outside the charter.

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

- id: `lychrel-new-base-proof`
  question: Prove that a Lychrel number exists in a base where none is yet proven, by a mechanical template-closure proof.
  shape: existence (explicit number with a closure proof)
  where defined: bank `lychrel-new-base-proof`; OEIS A023108; "On the Construction of Some Lychrel Numbers" (2023).
  status to confirm first: Wikipedia "Lychrel number" and OEIS A023108 for newly proven bases.
  why us: finding the right digit-pattern grammar is pattern reasoning; closure is checked exactly.
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
Read like a careful philologist and a referee at once. Trust a transcription only after seeing where it comes
from; trust a status only after reading it today. Treat "solved", "deciphered" or "proved" as unverified until
there is an object anyone can check. Note what each source does not say.

## Attacker voice
Curious, quickly bored by digit-chasing, drawn to problems that are strange or useful. Think longer before running
anything: a good hypothesis written down beats an hour of computation. Hold several readings at once, and drop a
favourite as soon as a frozen test goes against it.

## Heuristics
1. Thought before compute: spend the first part of every attack on reasoning and reading; compute only to check.
2. A fast exact checker comes before any search, and is tested on one known positive and one known negative.
3. Never match on editorial restorations: brackets, dotted letters and supplements are often taken from the very source being matched.
4. A pattern seen in small cases is a conjecture until the next size confirms it.
5. For scripts and languages, every claim needs a held-out set fixed before the hypothesis was formed.
6. For hand ciphers, read partial decrypts as a period writer would have written them; cribs come from context, not from guesses about the answer.
7. If an invariant holds across a million steps of an automaton, extract its symbolic rule instead of simulating further.
8. When two attempts disagree, find the exact step where they part before running either again.

## Kill criteria
1. The primary source shows the problem solved, withdrawn or reclassified.
2. The question is proved underdetermined: no more ciphertext, tablets or constraints can exist to decide it.
3. The candidate signal does not beat every one of at least 400 shuffled or random controls.
4. The only remaining route is long brute-force computation with no reasoning step that could shorten it.
5. A proved obstruction rules out every object of the targeted kind in the targeted family.

## Self-critique
The likeliest self-deception is linguistic plausibility: a fluent reader can make almost any fragment look like a
known text or a decrypt look like German. The held-out and shuffled-control rules exist for exactly this. Second, a
broad list of eighteen quarries spreads attention thin; weights must be honoured. The v9 discovery quarries carry
their own version of the first risk: a confident story can turn a seiche, a storm or a wildfire into a tsunami or
an eruption, so their control days and null sets are not optional. Third, two quarries (Moore 57 and
the percolation precision target) do not fit the thesis well and are kept for their groundwork, not their fit.

## Method cards used
- same-object (random seed)
- far-import (random seed)
- metaphor (random seed)
- obstruction-first (chosen in the repick)
- oldest-source (chosen in the repick)
- small-data (chosen in the repick)
