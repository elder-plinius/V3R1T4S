# CRITERION skeptic verdict — indus-temporal-heldout-structure (object-type claim)

Scope: read-only over claim/ (README.md, null_test.md, REPRODUCE.md, object/*.json, code/*.py,
baseline/record.md, data/ pins). Independent re-runs: pool build, exact-seq dedup + full
3x10,000 paired bootstrap (seed 20261117), pool-rule audit, data-pin sha256 verification.

## Core conditions (letter-by-letter)

- **Concrete structural property, example-listed**: 4-class object-type prediction from the sign
  sequence (seal/tablet/pottery/other), per-object accuracy. "Prediction of seal versus tablet
  object type from sequence" is an enumerated example property; 4-class is the same property. OK.
- **Fitted only on M77**: claim model (TemplateModel n<=3, add-one, wildcard OOV) fits on 3,548
  non-empty M77 lines only (object/output_sweep_main.json m77.lines=3548, vocab 417). Class priors
  come from the M77 fit (Seal 0.7587 / Tablet 0.1993 / Pottery 0.0360 / Other 0.0059,
  object/claim_model_frozen.json); KN discount grid is tuned on a 10% M77 object split (in-M77
  hyperparameter selection, disclosed in the kn3 record); the synthetic control is built from the
  M77 training stream. No held-out data enters any fit. Pool construction (PREREG.v2 rules:
  post-1977, M77-leak drop, identity dedup) is the frozen held-out definition, not a fit. OK.
- **Frozen in a timestamped file**: object/claim_model_frozen.json (frozen_at 2026-11-17T02:58:37Z,
  seed, ctx-counts sha256, priors, KN discounts). OK.
- **Paired-bootstrap p < 0.001 against BOTH, same resamples, simultaneously**: nulltest.py draws
  one index array per site (B=10,000, seed 20261117) and computes all three accuracies on the
  same resampled objects; p = fraction of resamples with claim <= max(KN, synth) — i.e. against
  both baselines simultaneously. object/output_nulltest.json: pooled p=0.0, Mohenjo-daro p=0.0,
  Harappa p=0.0 (all < 0.001; 0/10,000). Same statistic in output_sweep_main.json
  (p_boot_claim_vs_both=0.0 at all three). OK.
- **Replicate separately on >=2 sites, named in (d)**: Mohenjo-daro (n=665) and Harappa (n=590),
  both n>=20, both p=0.0, both beating both baselines (MD: 0.7098 > 0.3293 KN and > 0.1173
  synth; Harappa: 0.4017 > 0.2153 KN and > 0.2441 synth). These are exactly the sites (d) names.
  OK. (Dholavira 0.7593 / Lothal 0.8571 also pass; not required.)

## (a)–(d)

- **(a) First-publication source after 1977, documented, rest excluded**: pool rule in
  pipeline.build_pool_v2 is `post97 = site in (Dholavira, Lothal) [pinned excavation reports:
  dholavira2015-seal-catalogue.json, lothal-sealings-frenez-tosi2005.json] OR cisi starts with a
  CISI prefix (14 documented prefixes) AND not M77-attested`, with per-object `post97_rule`
  recorded in pool_detail. I re-audited all 1,613 pool objects: 0 violate the rule; 0 empty
  cisi. CISI-numbered vs Dholavira/Lothal handled by class; everything else excluded. OK.
- **(b) Dedup by seal impression identity, 386-identity directory, one per identity**:
  data/identity-directory.json has exactly 386 entries (sha256 matches the pin). Pipeline uses
  length>=2 cores (294 keys; 92 single-sign cores dropped as too generic, disclosed) in
  union-find: pool_kept 2,363 -> pool_reps 1,613, i.e. one rep per identity. No duplicate
  (cisi, sequence) pair exists in the pool (verified 0). OK.
- **(c) Not equivalent to P1-P9/Q1-Q14 or published positional findings**: judged
  object/output_novelty_diff.json myself. All comparators are in-sample (ending frequencies,
  terminal-zone compliance, numeral paradigms, emblem independence, twin rates, stability
  bounds) or descriptive 1977-era tables (Mahadevan 1977), in-sample EBUDS statistics
  (Rao/Yadav), or a 179-seal CISI-vol-3 sub-corpus (Kriger & Hunt 2026). None is a temporal
  M77->post-1977 predictive object-type accuracy vs tuned KN + SIGIL control. Closest, Q13
  (temporal rate stability), measures an in-sample bound, not held-out dual-baseline
  prediction — not equivalent. SIGIL 2608.02999 is design rationale, not a competitor. OK.
- **(d) Beat both baselines on MD and Harappa separately**: as above, verified numerically at
  both sites (and in my independent re-run). OK.

## Null models (task item 2)

null_test.md: controls 30,000 (>= 400 ✓), real beats all controls ✓ (0.5846/0.7098/0.4017 >
best_control 0.3255/0.3970/0.3136 and > real KN/synth at each site), command present ✓.
Numbers in null_test.md match object/output_nulltest.json exactly. Synthetic control:
class-conditional position-unigram over the M77 training stream, add-1 + M77 prior
(code/sweep_main.py, code/nulltest.py). Judged fair SIGIL-style: non-linguistic
(position-independent draws, no n-gram structure), length-matched by construction (each
object scored at its own length), unigram-matched as corpus position-conditionals. The
strictest reading ("matched on the held-out unigram") would be marginally stronger; the
criterion's "fitted only on M77" supports the M77-side match. Honest. One stretch: the
"400-draw synthetic pool per object" line — no 400-draw code path exists; the >=400 rule
stands on the 30,000 comparisons alone. Documentary, not substantive.

## Baseline record (task item 3)

baseline/record.md + object/output_baseline_repro.json: registry counts exact (M77 3573/418,
indus_website 2543/592, CISI 179/182 — expected == reproduced); same data, same metric.
In-sample Q/P tolerance misses (Q1 0.7155 vs 0.740; Q1-marked 0.0951 vs 0.062; Q3 28.75 vs
25.50; P1 0.2719 vs 0.33; P3 0.87/0.87 vs 0.76/0.24) are all recorded as NO/UNRESOLVED within
±0.02 with documented export/dedup explanations, explicitly "never retuned" and not depended on
by the claim. Unresolved baseline: K-H 2026 179-unicorn numbers not reproduced (exact 179-set
not pinned); recorded, not claimed — the claim's comparison is unaffected. OK.

## Hidden quantifiers / stretched definitions found

1. **Exact-seq dedup not executed as a code step**: the pool is unique on (object ID, sequence)
   by construction (0 duplicate pairs verified), and identity-core dedup handles seal
   identities. 57 groups of objects with identical exact sequences but different object IDs
   (180 objects) remain — allowed by the literal "(object ID, exact sequence)" wording. My
   independent exact-seq-dedup re-run (n=1,490 pooled / 619 MD / 553 Harappa) still gives
   p=0.0 and claim > both baselines at both sites (pooled 0.5839 vs 0.2772/0.1718; MD 0.7221
   vs 0.3199/0.1131; Harappa 0.3888 vs 0.2224/0.2206). No scope impact.
2. **Merged corpus carries 776 duplicate cisi IDs (2,104 extra records)**: an object ID with
   two distinct recorded sequences contributes two pool entries, each a distinct (ID, seq)
   pair. Literal wording permits it; noted.
3. **"400-draw synthetic pool"** — see above: claimed, not in code; immaterial.
4. **Class-prior mismatch**: M77 priors (Seal 0.7587) vs held-out Seal share (0.5889) — an
   M77-only fit as required; the effect stands despite it (Harappa pooled-2c 0.4487 still >
   both baselines).
5. **p = 0.0 is 0/10,000** — an upper bound of 1e-4, still < 0.001. OK.
6. **p2/p3 partial wins both negative** (p2 p=0.9864/0.9589 vs majority/KN-feature; p3
   0/31 events, p=1.0; object/output_sweep_secondary.json): the win is property A
   (object-type), not an enumerated partial win.
7. **Language**: "structural finding ... never decipherment" throughout (README,
   claim_object.json, novelty_diff); no sign-to-sound language anywhere. The Seal-prediction
   bias (108/147 Pottery predicted Seal) is the predicted property, not a decipherment claim.
   OK.

## Per-site numbers vs frozen thresholds (task item 4)

Threshold (claim_object.json): p < 0.001 at pooled AND MD AND Harappa, each n>=20, beating BOTH
baselines. Pooled n=1613: 0.5846 > 0.2808 & 0.1872, p=0.0. MD n=665: 0.7098 > 0.3293 & 0.1173,
p=0.0. Harappa n=590: 0.4017 > 0.2153 & 0.2441, p=0.0. All conditions met at all three sets ->
the FULL criterion is met, not p1 (p1 requires one of MD/Harappa to fail). p2/p3 are negative
and are not the win being claimed.

**confirmed_scope**: The class-conditional positional trigram model (n<=3, add-one, wildcard OOV,
seed 20261117) fitted only on the M77 1977 corpus predicts the 4-class object type
(seal/tablet/pottery/other) of the 1,613-object deduplicated post-1977 held-out pool (pooled
n=1613: 0.5846 vs Kneser-Ney 0.2808 and synthetic 0.1872, p=0.0; Mohenjo-daro n=665: 0.7098 vs
0.3293/0.1173, p=0.0; Harappa n=590: 0.4017 vs 0.2153/0.2441, p=0.0; paired bootstrap 10,000
resamples), beating both baselines simultaneously at pooled, Mohenjo-daro and Harappa — a full-
criterion win, not any of the enumerated partial wins p1/p2/p3.

context: subagent — a fresh isolated OpenClaw subagent that saw only the claim folder
pass: true
