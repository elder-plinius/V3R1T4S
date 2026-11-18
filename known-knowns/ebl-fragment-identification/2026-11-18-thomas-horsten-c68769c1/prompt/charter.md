# Research charter v1 (2026-11-16)

## Thesis
Edge: the named target is a corpus-alignment harvest on Rongorongo, so the charter leads with statistical text-structure work (frozen nulls, held-out prediction, alignment statistics) and pairs it with two other checkable ancient-writing problems plus one distant, well-defined record hunt. Every quarry ends in an object a stranger's computer can re-check: an alignment with a frozen null, a held-out prediction with a published split, or an explicit sequence of moves a checker replays in minutes. The random seeds (categories disease-research and wildcard; method cards metaphor, solver, representation) are noted but bent toward the human's stated curiosity: undeciphered scripts and ancient writing.

## Quarries
1. id: rongorongo-graphemes-parallels (bank, undeciphered-scripts, weight 5, wild no)
   Question: does a Smith-Waterman alignment pass across the Rongorongo corpus contain a new parallel passage (>=10 aligned positions, <=2 mismatches, accepted-allograph substitutions only, Bonferroni-corrected p < 0.001 against both the glyph-shuffle null and the local-repetition-preserving null, absent from Barthel 1958, Pozdniakov 1996/2007, Horley 2009/2021, Sproat 2003 and ipezygj parallels3, visually confirmed on tracings), or a better grapheme merge set (outcome B, +20% held-out parallels vs Horley's basic-glyph map)?
   Shape: harvest. Defined by: bank target `rongorongo-graphemes-parallels` and its success criterion (verbatim in bank/targets.json); corpus via jgregoriods/rongopy or ipezygj/rongorongo-catalogue-audit fetch_data.py; status source https://github.com/jgregoriods/rongopy.
   Status to confirm first: fetch the status source; confirm still undeciphered, that no 2026-11 publication or repo update supersedes the published parallel lists.
   Why us: the named first quarry; alignment statistics with frozen nulls is exactly the method the bank's verifier will re-run.
2. id: voynich-generator-heldout-fingerprints (bank, undeciphered-scripts, weight 2, wild no)
   Question: does any historically plausible hand-executable generator reproduce all published Voynich structural fingerprints (the Naibbe failure statistics of arXiv:2608.17096 plus the 4-signature joint test of arXiv:2604.19762) per Currier dialect and on both ZL3b and IT2a within the 95% envelope, or can the Naibbe cipher be decisively falsified against a fingerprint not used in its design?
   Shape: harvest / decisive falsification. Defined by: bank target `voynich-generator-heldout-fingerprints` (success criterion verbatim in bank/targets.json, citing Greshko 2025, arXiv:2608.17096, arXiv:2604.19762).
   Status to confirm first: fetch the cited arXiv pages once each and confirm the fingerprint values are still the published ones.
   Why us: same held-out-fingerprint method as quarry 1; cheap to run as a second lens inside the same corpus-work habit.
3. id: indus-temporal-heldout-structure (bank, undeciphered-scripts, weight 2, wild no)
   Question: is there a structural regularity of the Indus script (sign class, segment reuse, numeral strokes) fitted only on Mahadevan's 1977 corpus that predicts a measurable property on post-1977 held-out texts at paired-bootstrap p < 0.001 against both a tuned Kneser-Ney 3-gram and a SIGIL-style synthetic control, replicating on at least 2 sites?
   Shape: harvest, temporal held-out. Defined by: bank target `indus-temporal-heldout-structure` (success criterion verbatim in bank/targets.json).
   Status to confirm first: confirm M77 concordance and the indus_website / ICIT corpora are reachable and the 1977 time split is still the natural one.
   Why us: same discipline (freeze-then-hold-out) as quarry 1; the 2025 prize and 2026 unaccepted claims mean a *structural* result (not a decipherment) is the safe, checkable shape.
4. id: knotinfo-unknotting-number-unknown (bank, wildcard, weight 1, wild yes)
   Question: for one of the 4,991 KnotInfo knots whose unknotting number is still an interval, can an explicit crossing-change sequence (verified diagram code, c crossings, c strictly below the listed upper bound and every published bound) be found, closing the interval at c = a, or at least lowering the bound (p1) or certifying a single crossing change for a [1,2] knot (p2)?
   Shape: explicit object, mechanically checkable (SnapPy/Regina, under 30 minutes for the skeptic). Defined by: bank target `knotinfo-unknotting-number-unknown` (success criterion verbatim in bank/targets.json, including the arXiv:2603.07955 and arXiv:2409.09032 comparators).
   Status to confirm first: re-fetch knotinfo.org or the database_knotinfo mirror (whichever is newer) and confirm the chosen knot is still interval-valued; check whether Dranowski-Kabkov-Tubbenhauer's pending RL bounds are still "not installed".
   Why us: the random wildcard draw; the "solver" method card fits directly (recast as a bounded search over crossing subsets of a small diagram), and it keeps the charter from piling onto the crowd's famous problems.

## Lenses
1. key: aligner; title: Frozen nulls, honest alignments (skeptic: no)
   Run the strongest published alignment pipeline (Smith-Waterman with the stated matrix, per the target's verifier description) on the corpus exactly as the verifier would; freeze the matrix, alphabet, alphabet-reduction (catalogue choice) and both null designs in PREREG.md before scoring; then enumerate candidate passages and test every condition of the criterion literally. First moves: pull the corpus (rongopy or ipezygj fetch_data.py, record hashes), build the two shufflers (glyph-shuffle; local-repetition-preserving shuffle), 400 controls minimum. Dead sign: every candidate fails the Bonferroni threshold or is present in a published list.
2. key: skeptic; title: Already-settled attack (skeptic: yes)
   Assume the target is already settled and hunt for it: re-derive the published parallel lists (Barthel, Pozdniakov, Horley, Sproat, Kudrjavtsev, ipezygj parallels3) and the recent papers (DSH 2025 I/Gv/T segmentation; Korovina LT4HALA 2026; the Sept 2026 catalogue audit) to find passages or merge sets that meet the criterion but were never filed here. First moves: list every published passage with its tablet pair and line spans; diff against our alignment output. Dead sign: our best candidate is subsumed by a published one under trivial edits.
3. key: representation; title: Change the alphabet (method card: representation)
   The catalogue audit showed catalogue choice moves conditional entropy ~4x more than the signal, so the representation is the attack surface: build the same alignments under CEIPP numeric, Horley basic glyphs and a fresh allograph-merge set derived from the substitution evidence (parallels3.py table, held-out-tablet protocol per the undeciphered-scripts policy). First moves: tabulate which candidate passages survive or appear only under one catalogue; report results under at least 2 catalogues as the criterion requires. Dead sign: a passage that only exists under one catalogue and vanishes under another.
4. key: extender; title: Push the strongest published computation further (method card: solver)
   Take Korovina's syllabic-substitution GA or ipezygj's parallels3 output as the starting computation and push strictly further: more substitutions, more seed alignments, larger neighbourhoods, with saved certificates; for the merge-set outcome, start from Horley's basic-glyph map and grow the merge set under the held-out protocol. First moves: rerun the published pipeline, record its exact score, define "further" in PREREG.md before moving. Dead sign: no configuration beats the published score after the frozen search space is exhausted.
5. key: contrarian; title: Doubt the transcription (method card: metaphor, applied to the oldest sources)
   Treat the digitised corpora as data that may be wrong: check the kohaumotu tracings against the published sign lists for the specific passages that nearly win; a near-miss that dies on one dubious sign is either a data finding (report it, rule 14) or a reason to prefer a different catalogue. First moves: for the top 10 candidates, pull the tracing images and verify each aligned position by eye, recording which are confident. Dead sign: the best candidate rests on signs the tracer itself marks uncertain.

## Scout voice
Read for checkable structure, not meaning: every source entry that names a frozen split, a published list, a named algorithm and its parameters, or a machine-replayable verifier is gold; entries that offer "plausible readings" or "decipherment" are bait for this charter and get logged, not followed. Watch for status movement: the category's tables move fast, and a tie is not a win.

## Attacker voice
Temperament: patient statistician with a skeptic's reflex — the freeze happens before the measurement, every number is pasted from a command, and a clean negative with the covered space stated exactly is a good day. Angle: attack the representation and the null first, because that is where the false "found it" hides; only then spend the budget on the search itself.

## Heuristics
- Freeze the matrix, alphabet, thresholds and both null designs in PREREG.md before the first scored alignment; a changed plan is a new timestamped prereg, never an edit.
- 400 controls minimum; for formula-sign passages (repeated 76/200/606 runs) the local-repetition-preserving null is the one that bites — run it on every candidate, not just the suspicious ones.
- Bonferroni over all tablet pairs actually searched, stated explicitly in the report.
- One object or one cell per claim; never bundle a passage and a merge set into one claim.
- Record every fetch: URL, UTC time, HTTP status, sha256; one honest GET per page, no retries after a block.
- Re-fetch the status source right before claiming, not just at scout time.
- LLM-judged readings are never evidence (undeciphered-scripts policy): a reading "making sense" appears only as a note, never as proof.
- If a passage is new but rests on 7-9 positions, it is partial win p1, not a win — label it exactly.

## Kill criteria
- Candidate present in any published list (Barthel 1958; Pozdniakov 1996/2007; Horley 2009/2021; Sproat 2003; ipezygj parallels3) after trivial edits (subsequence, rotation, one-side extension).
- Bonferroni-corrected p >= 0.001 against either null, or the passage made only of high-frequency formula signs that does not beat the local-repetition-preserving null.
- More than 2 mismatches with a substitution not an accepted Barthel/Pozdniakov/Horley allograph pair.
- Same-tablet passage or sections less than 2 lines apart.
- Merge set that does not beat Horley's basic-glyph map by the required margin on held-out tablets (p3: 10%; B: 20%), or fails under a second catalogue.
- Visual confirmation fails on any tracing of the claimed passage.

## Self-critique
Most likely self-deceptions: (1) choosing the catalogue or alphabet reduction after seeing which one produces a candidate — the charter's remedy is lens 3's "under at least 2 catalogues" rule, enforced as a kill criterion; (2) treating a near-miss (7-9 positions) as a win — the remedy is the explicit p1 label and nothing wider; (3) letting "it reads like a calendar" sneak in as evidence — the remedy is the no-LLM-readings rule and the Mamari-lunar partial win p2, which is only usable with a frozen model; (4) over-claiming novelty by forgetting the 2025-2026 literature (DSH 2025, Korovina 2026, the Sept 2026 audit) — the remedy is the skeptic lens running before any claim is packaged.

## Method cards used
metaphor (applied as "doubt the transcription" in the contrarian lens), solver (as "recast as a bounded search" in the extender lens and for the knot quarry), representation (as its own lens). Random category draws (disease-research, wildcard) contributed the knot quarry; disease-research itself was folded in only if a later run shows an ECG/forecasting angle the human wants — not now.
