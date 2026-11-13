# Research charter v8-glaciers (2026-11-08, side workspace)

## Thesis
Seeds were drawn at random: chemistry-materials and recreational-math, with the method cards representation,
evaluator-first and smaller-first. The edge is a chemist's habit carried into puzzle tables: treat every search as an
energy landscape with funnels and basins, build a fast exact evaluator before searching, and calibrate on small
cases whose answers are proved. One quiet machine with modest free memory favours CPU-bound, small-state searches
that accumulate across many short runs. Since v8 the first quarry is one the human named: the 1933 Chinese gold bar
cryptograms, attacked as a search over small, period-appropriate system families (commercial test keys, check codes,
classical polyalphabetics), with every decode scored by language statistics against a shuffled-letter null. Rotation
(v7) is quarry 2; all its Gaia-only leads proved already published. Rongorongo is 3, eBL 4 (PR #944), co-orbital 5 and
precovery 6 (its lead was reported to the MPC on 2026-11-08).
The same habits carry over: build and calibrate an exact evaluator before searching (here the image-retrieval and
astrometry chain, checked on observations already in the MPC record), and choose the search space with care (here
objects whose back-propagated error ellipses are small and fall inside archive coverage).

## Quarries
1. **glaciers**: bank `massbalancemachine-norway-test-glaciers-rmse` (named by the human on 2026-11-08). Question: a
   model trained only on the 18 training glaciers' shipped rows (CV within them) whose RMSE on the test glaciers is below
   MassBalanceMachine's for annual, winter and summer balance (Ba <= 0.99, Bw <= 0.58, Bs <= 0.69 m w.e., at 2-decimal
   rounding), using no observation of a test glacier; or one of the entry's partial wins. Shape: record. Where defined: the
   bank entry, which holds the binding criterion; repository khsjursen/ML_MB_Norway. Status to confirm first: the
   repository notebook's RMSEs, reproduced, and any newer paper on the same test sets. Why us: evaluator-first fits.
   Reproduce MBM's own numbers before trusting any gain. Weight 5. Wild: no.
2. **rotation** (one NOTHING run; Gaia-only candidates were all already in DAMIT or MacLennan 2026; new periods need ZTF, ATLAS or TESS data): bank `asteroid-rotation-period-not-in-lcdb` (named by the human on 2026-11-04). Question: an asteroid
   with no LCDB entry and no published period, whose public survey photometry gives a period with FAP < 1e-4, a bimodal
   fold with two maxima and minima of amplitude > 0.1 mag, P/2 and 2P rejected at delta chi^2 > 25, and the period
   recovered within 1% in two apparitions or two surveys. Shape: existence (one object), or the batch partial win p1
   (10 objects). Where defined: the bank entry, which holds the binding criterion and the full novelty list (LCDB
   2023, DAMIT, the Gaia DR3 inversions, the ATLAS inversions, Durech & Hanus 2026, recent arXiv sets, ADS). Sources:
   the Gaia archive (SSO tables), ZTF photometry (alert brokers or IRSA), JPL Horizons for geometry. Status to confirm
   first: the LCDB page and every novelty list for each candidate. Why us: evaluator-first fits. Reproduce published
   LCDB U=3 periods with the same pipeline before trusting a new one. Weight 3. Wild: no.
3. **rongorongo** (three NOTHING runs on 2026-11-04; (A) exhausted under the published inventories, (B) lead D5 is exploratory): bank `rongorongo-graphemes-parallels` (named by the human on 2026-11-04). Question: outcome (A), a
   new parallel passage between two tablets, or between two sections at least 2 lines apart: >= 10 aligned positions,
   <= 2 mismatches beyond accepted allograph pairs, p < 0.001 against glyph-shuffled tablets of the same composition
   (Bonferroni over all tablet pairs), plus a local-repetition-preserving null for formula-heavy passages. It must be
   absent from the published lists (Barthel 1958, Pozdniakov, Horley, Sproat 2003, the ipezygj parallels3 output).
   Or outcome (B), a held-out-validated merge set. Shape: existence (one passage) or record (merge-set recall). Where
   defined: the bank entry, which holds the binding criterion. Sources: jgregoriods/rongopy, ipezygj/rongorongo-
   catalogue-audit (fetch_data.py, parallels3.py), kohaumotu tracings. Status to confirm first: the audit repository's
   parallels3 output, and which published lists are open. Why us: evaluator-first fits. Reproduce known parallels
   (Sproat 2003, parallels3) with the aligner and both nulls before claiming any new one; results must hold under two
   catalogues. Weight 2. Wild: no.
4. **ebl-identification**: bank `ebl-fragment-identification` (named by the human on 2026-11-04). Question: an eBL
   fragment with no join, no corpus-chapter link and no reference naming the composition, whose attested signs align to
   a specific composition witness (eBL corpus chapter or an Oracc edition) over >= 3 consecutive lines or >= 15
   consecutive signs with <= 10% mismatches. It must beat a line-order-shuffled null at p < 1e-4 after Bonferroni over
   all fragments searched, must not be in the open-source ngram-matcher's top 10, and must not be a formula recurring in
   >= 5 compositions. Shape: existence (one identification). Where defined: the bank entry, which holds the binding
   criterion, and its sibling `ebl-unidentified-fragment-overlaps` for the data traps. Sources: the eBL public API, the
   ebl-api and ngram-matcher repositories, Oracc. Status to confirm first: the eBL statistics endpoint, each candidate
   fragment's live record, and eBL and Oracc publications naming it. Why us: evaluator-first fits. Calibrate the
   alignment and null on fragments eBL already links to chapters before searching unlinked ones. Weight 3. Wild: no.
5. **coorbital** (parked 2026-11-04: the leads 2020 VK45/VN45 and 2012 UW177 are already published; revisit when 2023-25 short arcs mature): bank `uranus-neptune-coorbital-unrecognised` (named by the human on 2026-11-04). Question: a catalogued
   small body, not on the MPC Uranus/Neptune Trojan lists and not reported as a co-orbital, whose SBDB orbit (data arc
   >= 2 oppositions, condition code <= 5) gives >= 90% of >= 100 covariance clones a librating resonant angle with
   Uranus or Neptune over the bank's time span (REBOUND, giant planets from Horizons, relative energy error < 1e-8).
   Shape: existence (classification of one object). Where defined: the bank entry, which holds the binding criterion.
   Sources: MPC Neptune and Uranus Trojan lists, the JPL SBDB query and orbit APIs, Horizons. Status to confirm
   first: the MPC lists, SBDB candidates near a = 30.1 and 19.2 au, and the literature on each candidate (de la Fuente
   Marcos and de la Fuente Marcos, Alexandersen et al., Rubin/LSST papers). Why us: evaluator-first fits. Reproduce
   known Trojans' libration with the clone pipeline before trusting a new one; the landscape habit becomes reading
   resonant-angle portraits across clones. Weight 2. Wild: no.
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
7. **fullerene**: bank `fullerene-isomer-counts-beyond-c400`. Question: the exact count A007894(201) or A046880(201)
   (C402), with every earlier term reproduced. Shape: bound or proof (exact enumeration). Where defined: OEIS A007894
   and A046880; Brinkmann, Goedgebeur and McKay, arXiv:1207.7010 (2012); the oriented-count formula cited by the
   bank (arXiv:2304.01655). Status to confirm first: whether the b-files already extend past n = 200. Why us: the
   counting becomes lattice arithmetic in the Eisenstein-integer parameterisation; the hard part is the achiral
   correction, a symmetry-restricted count. Weight 3. Wild: no.
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
The seeds are random, so the "edge" is a stance, not an expertise: a chemist's landscape view may add little where
specialists already ran strong annealers. The gold bar quarry now carries most of the weight. It is a famous open
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
- v8-glaciers (2026-11-08): a side workspace, made so a parallel run cannot collide with the main workspace's run on
  chinese-gold-bars. Same as charter v8 except quarry 1, which is the human's named target `massbalancemachine-norway-test-glaciers-rmse`. Results are merged
  back into the main workspace afterwards.
