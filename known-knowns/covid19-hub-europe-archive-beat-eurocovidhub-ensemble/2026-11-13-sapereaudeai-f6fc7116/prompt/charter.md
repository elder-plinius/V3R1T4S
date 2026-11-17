# Research charter v15-eurocovid (2026-11-13, side workspace)

## Thesis
Seeds were drawn at random: chemistry-materials and recreational-math, with the method cards representation,
evaluator-first and smaller-first. The edge is a chemist's habit carried into puzzle tables: treat every search as an
energy landscape with funnels and basins, build a fast exact evaluator before searching, and calibrate on small
cases whose answers are proved. One quiet machine with modest free memory favours CPU-bound, small-state searches
that accumulate across many short runs. Since v9 the first quarry is one the human named: new exact still-life counts
for Life-like rules (OEIS A175000, A166476, A175001, A175002). This is exhaustive enumeration with two independent
enumerators, the smaller-first habit in its purest form. The gold bars (v8) are quarry 2 after two NOTHING runs whose
findings await outside-expert review. Rotation, Rongorongo, eBL, co-orbital and precovery follow.
The same habits carry over: build and calibrate an exact evaluator before searching (here the image-retrieval and
astrometry chain, checked on observations already in the MPC record), and choose the search space with care (here
objects whose back-propagated error ellipses are small and fall inside archive coverage).
Since v11 the first quarry is again one the human named: hidden repeating fast radio burst sources in the
CHIME/FRB Catalog 2. It is a catalogue-only search (a few MB, no fragile archive services), where the
evaluator-first habit means building and calibrating the false-alarm machinery on known repeaters first.
Since v12 the first quarry is a medical one the human named: predicting tuberculosis drug resistance from
genomes better than the WHO mutation catalogue on the CRyPTIC compendium. The evaluator-first habit here means
fixing the cluster-aware split and the phenotype filters before any model is trained.
Since v13 the first quarry is again an astronomical one the human named: historical outbursts in a century
of Harvard photographic plates (DASCH DR7). Evaluator-first here means separating plate defects from real
brightenings, and calibrating on known outbursts, before hunting.
Since v14 the first quarry is a clinical-genetics one the human named: how phenotype-driven gene ranking
tools perform on published rare-disease cases, and how much of that performance is annotation leakage.
Since v15 the first quarry is a microbiome one the human named: how much of the published accuracy of
gut-metagenome disease classifiers comes from confounders rather than disease.

## Quarries
1. **eurocovid**: bank `covid19-hub-europe-archive-beat-eurocovidhub-ensemble` (chosen by the main session overnight on
   2026-11-13 under the human's standing instruction to pick the next promising subject that needs no installs and no
   manual downloads; run in this side workspace in parallel with other runs). Question: the European COVID-19 Forecast
   Hub archive, which publishes its own scores file: the bank's binding criterion (beat EuroCOVIDhub-ensemble over a
   declared period under the as-of discipline); or partial wins p1 (strictly below the baseline AND the median
   submitted model with the bootstrap interval excluding zero), p2 (beat the ensemble on the smaller countries, bottom
   half by mean reported count, across all forecast dates) and p3 (an independent scoring reproduction: recompute the
   published per-model WIS decomposition in scores.csv from data-processed and the truth data, documenting every model
   whose recomputed value differs by more than 1% and why). Shape: audit or record. Where defined: the bank entry.
   Why us: three reproduction and audit wins tonight used exactly this formula. Weight 5. Wild: no.
2. **raredisease** (p3 and p1 confirmed and filed as #1058 and #1064; full win waits on bank PR #1068): bank `phenopacket-store-rare-disease-gene-prioritization` (named by the human on 2026-11-11). Question: a
   released ranking method whose per-case ranked lists over a fixed candidate space, on a pinned phenopacket-store
   release, beat a pinned reference tool (Exomiser or LIRICAL) on MRR by >= 10% relative and on top-1 recall, outside a
   95% bootstrap interval, using only resources released before the corpus and none derived from the case reports; or
   partial wins p1 (the same on cases with <= 3 HPO terms), p2 (beat the reference on >= 50 cases whose gene has no HPO
   annotation) and p3 (a reproducible leakage/ascertainment audit of how much of a reference tool's performance comes
   from annotations curated from the same publications). Shape: record (beat a comparator) or audit. Where defined: the
   bank entry, which holds the binding criterion. Status to confirm first: published evaluations on the same release.
   Why us: leakage audits and fair, pre-stated comparisons are what won TB's p2. Weight 3. Wild: no.
3. **tbresist** (p2 confirmed 2026-11-10 and filed as claim PR #1055; main criterion waits on bank PR #1045, an external route; no re-test before it merges): bank `cryptic-tb-resistance-beat-who-catalogue` (named by the human on 2026-11-10). Question: for at least
   one drug, a released model whose predictions on a held-out, lineage/cluster-aware split of the pinned CRyPTIC reuse
   table (CRyPTIC_reuse_table_20240917.csv), fixed before training by a published rule, beat the WHO mutation catalogue
   on the bank's stated metric, with identical pre-registered phenotype-quality filters for both predictors; or the
   partial wins (a newer or second-line drug where the catalogue is weakest: BDQ, DLM, CFZ, LZD or ETH; a reproducible
   leakage demonstration that random splits inflate performance; a ranked list of >= 10 candidate resistance variants
   absent from the catalogue). Shape: record (beat a comparator) or existence (variants). Where defined: the bank entry,
   which holds the binding criterion; the EBI FTP release_june2022 and the WHO catalogue edition named there are the
   sources. Status to confirm first: the catalogue edition and any newer CRyPTIC or WHO results. Why us: evaluator-first
   and careful nulls fit; leakage and filter-choice traps are where most published gains come from. Weight 3. Wild: no.
4. **stilllife**: bank `lifelike-rules-still-life-counts` (named by the human on 2026-11-08). Question: a new exact term
   of A175000 (HighLife, a(14)), A166476 (2x2, a(11)), A175001 (Move, a(11)) or A175002 (Maze, a(10)), from two
   independent enumerators that agree. Each must reproduce every listed term, and one must be a general Life-like-rule
   enumerator. Objects are reported as RLE or apgcodes. Shape: record (exact count). Where defined: the bank entry and
   the live OEIS entries. Status to confirm first: the four OEIS entries and the LifeWiki pages for these rules. Why us:
   smaller-first and evaluator-first fit exactly. Reproduce every known term with both enumerators before trusting a new
   one. Weight 5. Wild: no.
5. **goldbars** (two NOTHING runs on 2026-11-08; findings await outside-expert review): bank `chinese-gold-bars` (named by the human on 2026-11-08). Question: a single deterministic system
   and key, or a documented indicator rule, that decodes all 16 cryptogram lines into meaningful text coherent with the
   bars' Chinese inscriptions. Partial wins: p1, an identifiable 1930s generator (test key, check code, textbook scheme)
   reproducing >= 4 lines exactly from bar data at chance probability < 1e-6; or p2, one system and key decoding >= 4
   lines (>= 80 letters) to meaningful text, beating a shuffled-letter null. Shape: existence. Where defined: the bank
   entry, which holds the binding criterion; the IACR page is the transcription and the status source. Status to confirm
   first: the IACR page, Schmeh's top-50 list, and the cipherfoundation transcription. Why us: evaluator-first fits.
   Build an exact, fast language-statistic scorer (quadgrams for English, French and Wade-Giles), calibrated on known
   ciphertexts of the same length, before searching system families. Results stay private until an outside expert has
   reviewed them (DONT_SPOIL_THE_HUNT.md). Weight 3. Wild: no.
6. **precovery**: bank `asteroid-precovery-arc-extension` (named by the human on 2026-11-02). Question: for a known
   minor planet, find at least 2 detections in public ZTF, Pan-STARRS1 or DECam frames at an epoch more than 60 days
   before JPL SBDB first_obs and absent from its MPC observation record. They must lie inside the back-propagated
   3-sigma ellipse, have a consistent motion vector, and refit with residuals under 2 arcsec. Alternatively, the
   partial win precovery-reproduce-known-obs: re-detect recorded observations of at least 10 objects to under
   1 arcsec. Shape: existence (one record per object). Where defined: the bank entry, which holds the binding
   criterion. Sources: JPL SBDB and Horizons, the MPC get-obs API, IRSA IBE (ZTF), ps1images (PS1), NOIRLab SIA
   (DECam). Status to confirm first: SBDB first_obs and the MPC record of each object, re-fetched live, and
   arXiv:2510.07588 (the ZTF precovery pipeline, about 3,000 NEAs). Why us: evaluator-first fits. Build and calibrate
   the retrieval-and-astrometry chain on recorded observations before hunting; the landscape habit becomes choosing
   objects with small ellipses inside archive coverage. Weight 3. Wild: no.
7. **chimefrb** (parked 2026-11-10 after three NOTHING runs; lead under commitment in PR #1042; monthly TNS check for a third burst): bank `chime-frb-cat2-hidden-repeater` (named by the human on 2026-11-09). Question: a group of >= 2
   CHIME/FRB Catalog 2 (version 20251231) bursts that the catalog assigns to different sources, all with
   sidelobe_flag = 0 and excluded_flag = 0, meeting the bank's position, DM and false-alarm conditions after trials;
   or partial wins p1 (a catalog-wide pair search recovering >= 90% of the Cook et al. new repeaters with the same
   false-alarm machinery), p2 (a group meeting everything except 1e-3 < FAP < 1e-2) or p3 (a Catalog-1 one-off
   matching a Catalog-2 burst from a different source). Shape: existence (one group). Where defined: the bank
   entry, which holds the binding criterion; the CHIME/FRB catalog page and Cook et al. (arXiv:2605.08410) are the
   status sources. Status to confirm first: the live catalog file, TNS repeater designations, and repeater papers
   since Cook et al. Why us: evaluator-first fits. Build the false-alarm machinery and calibrate it on the known
   repeaters before trusting any new group. Weight 2. Wild: no.
8. **monostable**: bank `monostable-polyhedron-fewer-than-14-faces`. Question: a homogeneous convex polyhedron with
   exact rational vertices, fewer than 14 faces, resting stably on exactly one face. Shape: existence / record.
   Where defined: Conway and Guy (1969); Reshetov, IJCGA 24(1), 2014; the bank entry. Status to confirm first: any
   smaller monostable polyhedron published since 2014. Why us: treat the centroid's projection margins as a
   potential surface and search shapes the way one searches cluster geometries. Weight 2. Wild: yes.

## Lenses
1. **evaluator-first**, *Make the judge fast before you search* (skeptic: no). Spend the first block of time on an
   exact, fast evaluator: analytic gradients and Hessians, incremental updates for local moves, exact rational
   arithmetic only for the final check. Benchmark it against a naive version on the same inputs and keep both
   outputs equal. Dead sign: after the first block the evaluator is not at least 10x faster than naive, or the two
   disagree on any input.
2. **landscape**, *Search it like a cluster* (skeptic: no). Treat the objective as a potential energy surface:
   basin-hopping, parallel tempering, and restarts from the published best objects, with moves that respect the
   problem's symmetry. Track how many distinct basins you have seen and how often you land in the known best one.
   Dead sign: every funnel ends in the known best value or a symmetric copy, across at least three independent
   move sets.
3. **smaller-first**, *Prove the small cases, then lift* (skeptic: no). Solve the smallest instances exactly where
   the answer is known (small LJ_N minima in the Cambridge Cluster Database, quilts for n <= 18 as proved by Wynn,
   retention for n <= 9 as listed in A201126, fullerene counts for small C_n) and make the method reproduce every one. Tabulate the winners' structure and lift the pattern one size up.
   Dead sign: the method misses a proved small value, or the lifted pattern fails at the first new size.
4. **representation**, *Change the coordinates until it looks easy* (skeptic: no). Recast the object: quilts as
   Smith-diagram networks or Bouwkamp codes, fullerenes as Eisenstein-lattice data, clusters in normal-mode
   coordinates, magic squares as complementary-pair permutations. Search in the new space and map back exactly.
   Dead sign: the new space is no smaller than the old one, or everything it yields is already published.
5. **distant-import**, *Bring the other seed's tools* (skeptic: no). Use the method of the other seed category on
   this quarry: chemistry's global-optimisation and normal-mode analysis on recreational objects, and recreational
   exhaustive enumeration and symmetry breaking on chemical ones. Dead sign: the imported method cannot reproduce a
   known value in its first hour.
6. **already-settled**, *Prove it isn't open* (skeptic: yes). Try to show the quarry is settled, trivial or
   ill-posed: reproduce the table's own values first, look for a later paper or b-file extension, and check whether
   a "new" object is a trivial edit (deletion, relabelling, symmetry, local polish) of a published one. Dead sign:
   you cannot reproduce the table's values; then nothing else is trustworthy until you can.

## Scout voice
Read like a lab notebook referee: quote the definition exactly, copy the current best value and its date, and note
who last moved it. Distrust any number you did not recompute. Prefer the oldest primary source next to the newest
update, and say plainly when a table looks stale or abandoned.

## Attacker voice
Patient and empirical, like a computational chemist mapping a landscape: measure before guessing, keep every
negative, and let the evaluator decide. Willing to try an odd move set for an hour if it ends in an object the
checker can judge.

## Heuristics
1. The first hour builds the evaluator; the search inherits its speed.
2. Reproduce one known value before attempting a new one.
3. Seed from the published best object and say so; beat what trivial edits of it give.
4. Count distinct basins; a search that keeps finding the same one is telling you something.
5. Small proved cases are test oracles, not warm-ups.
6. Keep memory small: stream, chunk, or recompute rather than store.
7. Record covered spaces only when they are exhaustive and stated exactly.
8. A strange move set is fine if it ends in a checkable object.

## Kill criteria
1. The table or b-file already lists a value equal to or better than anything within reach.
2. The method cannot reproduce a proved small case.
3. The only gains come from loosening the definition (tolerances, counting convention, ring or scope).
4. The computation needs more memory than half the free memory, even after chunking.
5. Three independent move sets or representations all stall at the known best value.
6. The quarry turns out to be a duplicate of another quarry in this charter.

## Self-critique
The microbiome quarry now carries most of the weight. Its risks: study-of-origin and batch confounding, cohort
leakage in cross-validation, metadata gaps (age/BMI/country missing for some cohorts), and published AUCs computed
with fold files that were never released.
The rare-disease quarry now carries most of the weight. Its risks: circular annotation leakage, candidate-space
inflation, filtering cases after seeing results, release drift, and running the reference tool unfairly.
The DASCH quarry now carries most of the weight. Its risks: plate defects and emulsion flaws that mimic
brightenings, calibration artefacts that fake long-term trends, blends on low-resolution patrol plates, and
outbursts already catalogued under historical names.
The TB quarry now carries most of the weight. Its risks: population-structure leakage (clonal isolates on both
sides of a random split), phenotype filters chosen after seeing results, and class imbalance for the newer drugs
where resistance is rare; the bank's pitfalls name all three. Nothing here is clinical advice.
The CHIME quarry now carries most of the weight. Its risks: Cook et al. already mined Catalog 2 for repeaters, so
what remains is subtle; chance coincidences among 3,641 sources at CHIME's localisation scale; and an honest
trials factor. Calibrating on the known repeaters and a position-scrambled null is the guard.
The seeds are random, so the "edge" is a stance, not an expertise: a chemist's landscape view may add little where
specialists already ran strong annealers. The still-life quarry now carries most of the weight. Its risks are terms
already published outside OEIS (LifeWiki, catagolue) and rule-specific strictness. The gold bar quarry carried the most
weight in v8. It is a famous open
cryptogram with about 250 letters and very flat statistics, so false decrypts from over-searched key spaces are the
main risk; the shuffled-letter null and the all-16-lines rule are the guard. The rotation quarry carried the most
weight in v7. Its risk was novelty: about 30,000 survey-based spin models since 2022 cover most objects with dense data, and sparse survey
sampling produces aliases. The Rongorongo quarry carried the most weight in v6. Its risks are that the published parallel lists are partly closed books (Barthel 1958), so novelty is hard
to prove, and that formula-sign runs (76/200/606) align by chance. Visual confirmation on the tracings is a check by
a person, never model judgement (kit/POLICY.md). The eBL quarry carried the most weight in v5.
Its traps are formulaic shared runs, editorial restorations counted as attested signs, and a Bonferroni level that
simulation alone cannot reach; the sibling entry's pitfalls name all three. The co-orbital quarry carried the most
weight in v4. Its risks are literature priority (dynamicists classify new TNOs quickly) and orbits too short to give
coherent clones. Precovery, quarry 2, still carries real weight. It
depends on several slow remote services, and on an orbit refit this machine has no library for. A single faint source
inside a large ellipse is the classic false precovery, and the ZTF pipeline of arXiv:2510.07588 has already covered
many easy objects, so the first hour aims at the reproduce-known-obs partial win. Proto-Elamite is paused: two runs
and a recheck showed that system-assignment rules have almost no headroom on the eligible tablets, and both runs
shrank the eligible set with their own added conditions. Fullerene counting may be cluster-scale in
practice despite the bank's laptop estimate. The wild quarry has resisted strong searches since 2014.

## Method cards used
representation, evaluator-first, smaller-first (drawn at random).

## Changelog
- v2 (2026-11-01): the human named `proto-elamite-accounting-balance`, which becomes quarry 1 (AGENTS.md: a named
  problem becomes the charter's first quarry). lj-zpe is retired at the human's request now that all its leads have
  verdicts:
  - N = 38 Ne was confirmed and submitted as draft PR #881. Later it was found to be the posted 38B structure with
    one atom relocated, then quenched; the retraction note is with the human.
  - N = 34, 36, 37 and 44 Ne and N = 34 and 67 Ar are dead as trivial edits of posted structures.

  Thesis and self-critique are updated to match. The other quarries, lenses, heuristics and kill criteria are
  unchanged. v1 is kept as charter.v1.md.
- v3 (2026-11-02): the human named `asteroid-precovery-arc-extension`, which becomes quarry 1 (AGENTS.md: a named
  problem becomes the charter's first quarry). Proto-Elamite is paused at the human's request after two NOTHING runs
  (2026-11-01-1915, 2026-11-02-0327) and an independent recheck. It stays as quarry 2 at weight 1, so 6 quarries,
  still exactly one wild. Thesis and self-critique are updated to match. The other quarries, lenses, heuristics and
  kill criteria are unchanged. v2 is kept as charter.v2.md.
- v4 (2026-11-04): the human named `uranus-neptune-coorbital-unrecognised`, which becomes quarry 1 (AGENTS.md: a named
  problem becomes the charter's first quarry). Precovery moves to quarry 2 at weight 4 after five runs on (2025 LP)
  that ended PROMISING (dossier). That makes 7 quarries, still exactly one wild. REBOUND 5.2.2 was installed in the
  venv at the human's request. v3 is kept as charter.v3.md.
- v5 (2026-11-04): the human named `ebl-fragment-identification`, which becomes quarry 1 (AGENTS.md: a named problem
  becomes the charter's first quarry). Co-orbital is parked as quarry 2 (weight 2) after one NOTHING run: its leads
  were already published (LiDO, arXiv:2610.19865; 2012 UW177). Precovery moves to quarry 3 (weight 3). That makes
  8 quarries, the maximum, still exactly one wild. v4 is kept as charter.v4.md.
- v6 (2026-11-04): the human named `rongorongo-graphemes-parallels`, which becomes quarry 1 (AGENTS.md: a named
  problem becomes the charter's first quarry). eBL identification becomes quarry 2 at weight 3, after one NOTHING run
  that showed its clause (c) null is unreachable (bank PR #944). Co-orbital and precovery move to 3 and 4.
  Proto-Elamite (paused since v3, weight 1, two NOTHING runs) leaves the list to keep 8 quarries; its dossier stays.
  Still exactly one wild. v5 is kept as charter.v5.md.
- v7 (2026-11-04): the human named `asteroid-rotation-period-not-in-lcdb`, which becomes quarry 1. Rongorongo becomes
  quarry 2 at weight 2 after three NOTHING runs (bank PRs #947 and #949). water (magic-square water retention, never
  run) leaves the list to keep 8 quarries. The others are renumbered, still exactly one wild. v6 is kept as
  charter.v6.md.
- v8 (2026-11-08): the human named `chinese-gold-bars`, which becomes quarry 1. Rotation becomes quarry 2 at weight 3.
  perkins (never run) leaves the list to keep 8 quarries. The others are renumbered, still exactly one wild. v7 is kept
  as charter.v7.md.
- v9 (2026-11-08): the human named `lifelike-rules-still-life-counts`, which becomes quarry 1. The gold bars become quarry
  2 at weight 3. fullerene (never run) leaves the list to keep 8 quarries. The others are renumbered, still exactly one
  wild. v8 is kept as charter.v8.md.
- v10 (2026-11-09): the human named `new-periodic-variables-not-in-vsx`, which becomes quarry 1. Still lifes move to 2
  (two PROMISING terms wait on bank PR #1032), the others move down one. Rotation (one NOTHING run; every near-miss was
  already published) leaves the list to keep 8 quarries; its dossier stays, and its lesson (new periods need ZTF,
  ATLAS or TESS data) carries into quarry 1. Still exactly one wild (monostable). v9 is kept as charter.v9.md.
- v11 (2026-11-09): the human named `chime-frb-cat2-hidden-repeater`, which becomes quarry 1 (AGENTS.md: a named
  problem becomes the charter's first quarry). Varstars is parked at quarry 7 (weight 2) after two NOTHING runs
  (2026-11-09-1119, 2026-11-09-1330). Co-orbital (parked since v5) leaves the list to keep 8 quarries; its dossier
  stays. Still exactly one wild. v10 is kept as charter.v10.md.
- v12 (2026-11-10): the human named `cryptic-tb-resistance-beat-who-catalogue`, which becomes quarry 1 (AGENTS.md: a
  named problem becomes the charter's first quarry). CHIME is parked at quarry 7 (weight 2) after three NOTHING runs,
  with a monthly TNS check. Varstars (parked since v11) leaves the list to keep 8 quarries; its dossier stays. Still
  exactly one wild. v11 is kept as charter.v11.md.
- v13 (2026-11-10): the human named `dasch-unreported-historical-outburst`, which becomes quarry 1 (AGENTS.md: a
  named problem becomes the charter's first quarry). TB moves to quarry 2 (weight 3) while bank PR #1045 is
  reviewed. eBL identification (one NOTHING run, clause (c) shown unreachable in #944) leaves the list to keep 8
  quarries; its dossier stays. Still exactly one wild. v12 is kept as charter.v12.md.
- v14 (2026-11-11): the human named `phenopacket-store-rare-disease-gene-prioritization`, which becomes quarry 1
  (AGENTS.md: a named problem becomes the charter's first quarry). DASCH (parked after two NOTHING runs: the plates'
  flags and one-series coverage defeat any calibrated detector) leaves the list to keep 8 quarries; its dossier
  stays. Still exactly one wild. v13 is kept as charter.v13.md.
- v15 (2026-11-12): the human named `metagenomics-nonneoplastic-disease-classification`, which becomes quarry 1
  (AGENTS.md: a named problem becomes the charter's first quarry). Rare disease moves to 2 (weight 3) while bank PR
  #1068 is reviewed. Rongorongo (three NOTHING runs; expert replies pending) leaves the list to keep 8 quarries; its
  dossier stays. Still exactly one wild. v14 is kept as charter.v14.md.
- v15-eurocovid (2026-11-13, side workspace <WORKDIR>): the main session picked the bank target named in quarry 1 overnight, under the human's standing
  instruction (pick the next no-install subject); the main charter is unchanged. Results are merged back into the main workspace afterwards.
