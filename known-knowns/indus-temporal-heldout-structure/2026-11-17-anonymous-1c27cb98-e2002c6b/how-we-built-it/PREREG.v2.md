# PREREG.v2 — indus-temporal-heldout-structure (supersedes PREREG.md for the held-out rules; model,
# statistic, seed and thresholds unchanged)

timestamp: 2026-11-17T03:25Z (UTC)
reason for v2: before the first scored run I found two data-rule defects in PREREG.md §"Held-out set
construction" that would have made the pool tiny (57 objects) and biased:
  (1) PREREG.md rule 5 said held-out objects with an OOV sign are "recorded, never a drop" but the
      pool code also required `seq_m is not None` (i.e. dropped them). Fixed: OOV sign -> fixed
      wildcard token in the mapped sequence (no drop).
  (2) PREREG.md rule 4's identity dedup used ALL 386 identity cores including 1-sign cores, which
      merged most of the corpus into a handful of groups (3,507 -> ~140 representatives). Fixed:
      identity cores of length >= 2 only (the 386-directory's recurring cores; 1-sign cores are too
      generic to identify a seal), and in addition every held-out object whose identity core (length
      >= 2, mapped through the bridge) is attested in the M77 training objects is EXCLUDED (verifier
      condition: "no held-out sequence or seal identity appears in training").
Everything else (the claim, the property, the baselines, the statistic, the thresholds, the seed,
the training set, the direction check) is unchanged from PREREG.md. This is a corrected plan, not a
retune: no measured output existed before this file (the first scored sweep is run after it).

## Corrected held-out rules (all else as PREREG.md)
1. **Pool:** paragorth `merged-corpus-reading-order.json` (pinned 92fc8439...), objects with >= 2
   non-zero signs.
2. **Post-1977 (condition a), documented per object:**
   - site Dholavira: excavation reports Rao 2003/2004 + the 2015 seal catalogue
     (`dholavira2015-seal-catalogue.json` in this run's data/corpus) — post-1977 excavation report;
   - site Lothal: Frenez & Tosi 2005 Lothal sealings (`lothal-sealings-frenez-tosi2005.json`) —
     post-1977 excavation report;
   - any object with a CISI-database number of prefix M-, H-, L-, K-, C-, Ns-, B-, Ad-, Agr-, Blk-,
     Ai-, Krs-, Rgr-, Sktd- (the CISI volumes 1-3 + post-1977 report series): for the two criterion
     sites (Mohenjo-daro, Harappa) an object whose (mapped) sequence OR (length>=2, mapped) identity
     core also occurs in the M77 training objects is the pre-1977 (CISI 1-2 / M77-era) material and
     is excluded; the remainder of the CISI-numbered MD/H objects is the post-1977 (CISI vol 3 /
     post-1986 Harappa) material. (Documented approximation of "first-publication source dated after
     1977": the verifier can rebuild this exact rule from the pinned files; it is a conservative
     read — it excludes, it never adds, objects with a M77-era attestation.)
3. **Non-duplicate:** dedup by (object id + exact sequence) — each merged object is one row; drop
   any held-out object whose (Wells) sequence, mapped through the bridge with OOV->wildcard, equals
   a M77 training sequence (leak), or whose length>=2 identity core (mapped) is attested in a M77
   object (seal-identity leak, condition b's training side).
4. **Seal-identity dedup (condition b):** union-find over held-out objects sharing a length>=2
   identity core from `identity-directory.json` (the 386-identity directory); one representative per
   identity. Sealings of the same seal count once.
5. **Sign-space mapping (frozen rule):** bridge_extended.json; a sign with no bridge entry, or an
   empty bridge entry (832, 65, 794), maps to the fixed wildcard token -999; a multi-candidate
   bridge entry maps to its first candidate (fixed file order). The model, the KN baseline and the
   synthetic control all see the identical mapped sequences.

## Everything else
As PREREG.md: the class-conditional template claim model (n<=3, add-one, wildcard OOV), the
class-conditional tuned KN baseline (3-gram where the class stream has >= 3,000 training tokens,
otherwise the same fitter with backoff-dominated behavior; discount grid-tuned per class on the 10%
M77 object split, seed 20261117), the SIGIL-style class-conditional position-unigram control
(matched on unigram + length distribution by construction), paired bootstrap B=10,000 seed 20261117,
p < 0.001 required at pooled AND Mohenjo-daro AND Harappa (each with n >= 20 after all rules), the
2-class seal-vs-tablet secondary, the p2 field-symbol property (terminal 2 signs -> 9-family), the
p3 ligature property, the novelty diff, and the step-3c baseline reproductions.
null_test: required
