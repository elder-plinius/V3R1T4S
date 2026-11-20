# PREREG — indus-temporal-heldout-structure (frozen 2026-11-17, BEFORE any model is measured)

timestamp: 2026-11-17T02:50Z (UTC)
run: runs/2026-11-17-0212
target: indus-temporal-heldout-structure

## Criterion (verbatim, bank/targets.json)
See `target.md` section "Success criterion (verbatim, bank targets.json)". One concrete structural
claim, fitted only on M77, frozen in a timestamped file; on the post-M77 non-duplicate held-out
texts (dedup by object ID + exact sequence) it must predict a measurable property with paired-
bootstrap p < 0.001 against BOTH (i) a tuned Kneser-Ney 3-gram on the same M77 data and (ii) a
SIGIL-style non-linguistic synthetic control matched on unigram and length distribution; the effect
must replicate separately on at least 2 sites; (a) each held-out object has a documented post-1977
first-publication source; (b) dedup by seal-identity (paragorth's 386-identity directory); (c) not
equivalent to paragorth P1-P9/Q1-Q14 or to Mahadevan 1977 / Rao 2009-10 / Yadav / Kriger-Hunt 2026;
(d) beat both baselines on Mohenjo-daro and on Harappa separately. The claim says 'structural
finding', never 'decipherment'.

## The one structural claim (menu item: criterion's "prediction of object type from sequence")

**CLAIM (full criterion):** "A sign-sequence model fitted only on the M77 (1977) corpus predicts the
object class (seal / tablet / pottery / other, 4-class) of deduplicated post-1977 held-out Indus
inscriptions from their sign sequence, a property a random (non-linguistic) sequence of the same
length and sign frequencies does not carry: per-site class accuracy on the held-out set exceeds
both a tuned Kneser-Ney 3-gram (same M77 fit) and a SIGIL-style length+unigram-matched synthetic
control, by paired-bootstrap p < 0.001 (10,000 resamples), replicating separately on Mohenjo-daro
and on Harappa. This is a structural finding (object-type predictability of the sign sequence across
a time split), not a decipherment."

- **Measurable property:** per-object correct 4-class object-type rate (accuracy) of the frozen
  model on the held-out set, reported pooled, per-site, and as the 2-class seal-vs-tablet rate.
- **Model (frozen, M77-only):** a position-aware, class-conditional n-gram "template" model
  (n<=3) per object class: score(seq, class) = log P(class prior) + sum over positions i of
  log P(sign_i | sign_{i-1}, sign_{i-2}, position-i, class), add-one smoothing, OOV signs handled
  by a fixed wildcard token. The model sees only M77 lines (sequences + their object class). No
  held-out information touches it. Its parameters (n, smoothing, position-window) are fixed HERE
  and frozen with seed 20261117 (the model itself is deterministic given these; the seed governs
  only the bootstrap and the synthetic control).
- **Baseline (i) tuned KN 3-gram:** Kneser-Ney 3-gram over the M77 sign stream (same M77 fit),
  discount lambda tuned on a held-out 10% of M77 (the only data it may tune on; seed 20261117),
  class posterior = P(class prior) x KN3 sequence likelihood, per-object, same scoring as the
  claim model.
- **Baseline (ii) SIGIL-style synthetic control:** for each held-out object, 400 synthetic
  sequences of the same length whose sign at each position is drawn independently from that
  position's empirical sign marginal in the held-out set (matched on unigram AND length
  distribution, non-linguistic: no sequential structure beyond position marginals), seed 20261117.
  The control's "accuracy" is its per-object class-accuracy rate over its 400 draws (a non-
  linguistic sequence carries the object-type signal only if the position marginals do).
- **Statistics / thresholds (exact):**
  - Per site s in {pooled, Mohenjo-daro, Harappa}: paired-bootstrap p = fraction of 10,000
    resamples (resample the site's held-out objects with replacement, recompute all three
    accuracies on the resample) in which claim-model accuracy <= max(KN3 accuracy, synthetic-
    control accuracy). PASS requires p < 0.001 at pooled AND Mohenjo-daro AND Harappa.
  - Secondary (reported, not the gate): seal-vs-tablet 2-class accuracy with the same p rule.
  - Minimum support: per-site n_heldout >= 20 objects after all dedup rules (a site with fewer
    is reported as "insufficient support" and cannot carry the (d) replication; pooled must be
    >= 100). If a site is insufficient, the claim can be at most p1 (one site) even if pooled
    passes.
  - The claim wins the FULL criterion iff p<0.001 at pooled, MD and Harappa (with both sites
    n>=20), AND all conditions (a)-(c) hold, AND it beats BOTH baselines at every one of the
    three sites (not just pooled).

## Held-out set construction (pre-registered rules; verifier can rebuild)
1. **Pool:** paragorth `merged-corpus-reading-order.json` (5,369 objects, pinned
   92fc8439cf87805fa022a16e1e5fd988006ee0f4235d70b775e4388437afe101), Wells coding, per-object
   site / type / field symbol / cisi number.
2. **Post-1977 only (condition a):** keep objects with a documented post-1977 first-publication
   source: (i) site Dholavira (excavation reports Rao 2003/2004; seal catalogue
   `dholavira2015-seal-catalogue.json`); (ii) Lothal (Frenez & Tosi 2005 sealings,
   `lothal-sealings-frenez-tosi2005.json`); (iii) Mohenjo-daro and Harappa objects with a CISI
   database number (M-/H- prefix) NOT in the 1977 M77 object set (i.e. CISI vol 3 / post-1986
   Harappa / post-1977 MD material); (iv) Kalibangan, Chanhu-daro, Nausharo and other CISI-
   numbered sites are kept as pooled-only (they cannot carry the (d) site replication). Objects
   with no cisi number and site not in (i)/(ii) are excluded (no documented post-1977 source).
3. **Non-duplicate (criterion + verifier):** dedup by (object id + exact sequence); drop any held-
   out object whose (Wells) sequence maps to a sequence present in the M77 training set (leak).
4. **Seal-identity dedup (condition b):** using paragorth `identity-directory.json` (386
   recurring identity cores), union-find over held-out objects sharing an identity core; one
   representative per identity. (Sealings of the same seal count once.)
5. **Sign-space mapping:** the M77 model is in Mahadevan coding (418-sign M77 set). A held-out
   object's Wells signs are mapped to Mahadevan via `bridge_extended.json`; signs the bridge has
   no entry for (OOV for the M77 vocabulary) become a fixed wildcard token (recorded per object),
   never a drop, so the model and both baselines see the same sequences.
6. **Direction (recorded 2026-11-17 02:42Z, `code/direction_check.py`, output/
   direction_check.json):** M77 as-stored and the merged corpus as-stored BOTH show the Rao/Yadav
   final-more-constrained fingerprint (M77: initial 6.598 bits > final 4.744 bits; merged: 7.0105
   > 5.1724), so both are scored as-stored (the joyboseroy reversal bug is already fixed in the
   current converters; no reversal applied by us).

## Training set (frozen)
- **M77:** joyboseroy `data/m77_indusscript_real_corpus.csv` (pinned c87b82a6d0ce2d02e70c96711f4ae6fd2a01f8b0dbb9795e564e17b12e2ce1d3), 3,548 non-empty lines, R-L reading order, 418-sign vocab. Object class + site + field symbol aligned from paragorth `im77_corpus_lines.csv` (pinned 385b82bd6a9629e0ab215af46db84ca0c9ec4f6044a2a2ea58a3c64121f26211) by (text_no, k-th line) file order (alignment validated 2026-11-17: 2,583/2,906 objects sequence-multiset identical to im77; the 323 differing objects differ only by im77 empty/placeholder lines).
- **Class mapping (4-class):** seal + sealing -> Seal; miniature tablet + copper tablet + ivory/bone
  rod + bronze implement -> Tablet; pottery graffito -> Pottery; miscellaneous -> Other. (Fixed;
  the 2-class secondary folds Tablet into {Seal, Tablet} vs the rest.)

## Nulls (both required; pre-registered here)
- **(i) tuned Kneser-Ney 3-gram** trained on the same M77 data (as specified above): the primary
  statistical baseline.
- **(ii) SIGIL-style non-linguistic synthetic control** matched on unigram + length distribution
  (as specified above, 400 draws/object, seed 20261117).
- **Paired-bootstrap:** 10,000 resamples, per site and pooled, as above. `null_test: required`
  (this is a "beats chance / beats baseline" claim on an undeciphered script; the category
  undeciphered-scripts mandates the null file). The 400 synthetic draws per object plus the 10,000
  bootstrap resamples are the controls recorded in `null_test.md` (>= 400 controls: satisfied by
  the 10,000 resamples each of which is a recomputed control comparison, and by the 400-draw
  synthetic pool per object).

## Novelty (pre-registered check, run in the skeptic lens and re-run by the NOVELTY panelist)
Diff the claim's prediction signature against:
- paragorth frozen predictions P1-P9 (`preregistration-frozen.json`) and Q1-Q14
  (`preregistration-2-frozen.json`) (+ R1-R13, P4 credentials, P5.x minimum-lot, for completeness):
  the claim's property (temporal, held-out object-type predictability with a time split) does not
  appear in any P/Q statement (all in-sample on the 1977-era corpus or the CISI sub-corpus). Q10
  (emblem independence) is the closest *falsified* relative; the p2 field-symbol angle is judged
  against Q10's in-sample scope only.
- Published positional findings: Mahadevan 1977 (jar endings, position tables — in-sample, 1977);
  Rao et al. 2009 / Yadav et al. 2010 (structural statistics, EBUDS subset, in-sample); Kriger &
  Hunt 2026 (179 MD unicorn seals: 98.3% uniqueness, edge-peaked positional entropy, penultimate
  numerals, 66.9% "2", 8 one-substitution pairs — all in-sample, CISI-vol-3 sub-corpus); arXiv
  2608.02999 (SIGIL: the standard statistics are non-specific — so any claim resting only on those
  statistics is equivalent and excluded; our claim is a *predictive held-out* property).
- The diff output (claim vs each item, with a line of reasoning each) is recorded in the lens
  `report.md` and re-run from scratch by the NOVELTY panelist.

## Partial-win ladders (pre-registered, exact)
- **p1:** same claim, full conditions (a)-(c) and p<0.001 vs both baselines on the POOLED held-out
  set AND on one of {Mohenjo-daro, Harappa} (that site n>=20), but not yet on the other (the
  other site fails p<0.001 or has n<20).
- **p2 (field-symbol conditioning):** a frozen M77-only model predicts the held-out seal's field-
  symbol family (9-family scheme: Unicorn/Bull/Gaur/Zebu/Elephant/Rhino/Tiger/Antelope/Buffalo/
  Other, fixed in `code/pipeline.py`) from the text's terminal segment (last 2 signs; last 1 if
  shorter), per held-out seal with a non-empty DB symbol, accuracy exceeding BOTH the majority-
  motif baseline (most common family in that site's M77 training) AND a KN-3-gram-feature
  classifier (features = (sign, position-from-end) bigrams, M77-fitted, same seed), paired-
  bootstrap p < 0.001 (10,000), not among paragorth's frozen predictions (diff vs Q10's in-sample
  scope recorded). Sites with < 5 such seals are reported as insufficient.
- **p3 (ligature substitution):** a frozen M77-only list of composite signs AB (the M77 top-20
  most-frequent adjacent sign pairs that also appear as a single fused glyph in the sign lists)
  whose substitution rate for the bigram A B in parallel (same-object, other-line / seal-twin)
  contexts of the held-out texts exceeds that of 200 frequency-matched random composite/bigram
  pairs (permutation p < 0.001 = 0 of 200+ pairs beating it, seed 20261117), not among paragorth's
  frozen predictions or the published positional findings.

## Reproduce the published baseline (step 3c, pre-registered scope)
- Reproduce on this data: (1) the corpus registry counts (M77 3,573 lines / 418 signs;
  indus_website 2,543 / 592; CISI 179 / 182) from the CSVs; (2) paragorth's in-sample frozen-
  prediction values Q1 (jar-final rate), Q3 (numeral 3-8 vs 1-2 ratio) and P1/P3 (modal ending,
  terminal compliance) on the im77 corpus using `prereg/test_prereg.py` semantics (expected
  values from `PREREG_RESULTS.md`: Q1 0.740, Q3 ratio 25.50, P1 33%, P3 76%); (3) the published
  2608.02999 non-specificity scope (SIGIL reproduces the standard measures — read once, recorded,
  not re-run: it is the *design rationale* for the two baselines, not a number to reproduce).
  Tolerance: registry counts exact; Q/P in-sample values within +/-0.02 absolute (rounding of the
  1977 export). What we could NOT reproduce within budget is recorded in `baseline/record.md`.

## Freeze
seed(s): 20261117 (bootstrap, synthetic control, permutations; all RNG draws seeded from it).
Model hyperparameters fixed here: n<=3, add-one smoothing, position window = full (positions 1..len),
wildcard token for OOV, 4-class mapping as above, 10% M77 KN-tuning split (first 10% of objects in
text_no order, seed 20261117 for the shuffle). NOTHING below the model's training may change without
a new timestamped PREREG.v2.
