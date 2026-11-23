# REPRODUCE skeptic — Indus object-type claim (run 2026-11-17-0212)

Method: I wrote my own checker (independent loaders, pool builder, template/KN/synthetic
scorers, bootstrap) from the claim definition in README.md, before reading the author's model
code. The author's code/ was run only in a scratch copy (twice, to confirm determinism).
All file references below are relative to claim/. Data pins verified: all four pinned sha256
values (data/m77_indusscript_real_corpus.csv, data/im77_corpus_lines.csv,
data/merged-corpus-reading-order.json, data/identity-directory.json) match the values in
README.md exactly.

## Re-derived numbers (mine vs stored — all exact matches)
- M77 training set (joyboseroy M77 lines, object type/site aligned from im77 by text_no +
  k-th line): 3548 non-empty lines; class counts Seal 2694 / Tablet 707 / Pottery 127 /
  Other 20; vocab 417 (registry's 418 signs minus MSg0). Identical to the m77 block in
  object/output_sweep_main.json.
- Held-out pool (post-1977 rule = Dholavira/Lothal site OR CISI-prefixed cisi; drop mapped
  sequence already in M77; identity-core dedup with length>=2 cores from
  data/identity-directory.json; drop cores attested in M77; OOV sign -> wildcard -999):
  identity_keys_len2=294, m77_attested_keys=130, pool_kept=2363, pool_reps=1613; by-site
  MD 665 / Harappa 590 / Dholavira 108 / Lothal 91 / Kalibangan 76 / Chanhu-daro 34 /
  Nausharo 25 (+24 objects at 7 minor sites). All identical to the stored poolinfo/by_site
  and to object/claim_object.json.
- Per-object predictions: re-scored the FULL held-out set (1613/1613, not a sample). The
  multiset of (cisi, site, otype, seq_m, pred_claim, pred_kn, pred_synth, ok_claim) is
  identical to object/output_sweep_main.json pool_detail, 0 mismatches, no missing objects.
- Per-site 4-class accuracies (mine = stored): pooled 0.5846 / 0.2808 / 0.1872;
  Mohenjo-daro 0.7098 / 0.3293 / 0.1173; Harappa 0.4017 / 0.2153 / 0.2441; Dholavira
  0.7593 / 0.3241 / 0.2407; Lothal 0.8571 / 0.4505 / 0.3516. 2-class (Seal-vs-Tablet)
  blocks also identical (0.6532/0.2834/0.1936 pooled; 0.7528/0.3333/0.1148 MD;
  0.4487/0.207/0.2592 Harappa). Claim beats BOTH baselines at every site.
- Paired bootstrap, re-run by me at full B=10,000, seed 20261117, shared resample indices
  across the three systems, p = fraction of resamples with claim <= max(KN, synth):
  p = 0.0 at pooled, MD and Harappa (0/10000 resamples); max over resamples of
  max(KN,synth) = 0.3255 / 0.3970 / 0.3136 — identical to object/output_nulltest.json
  (real_beats_all_controls true in all three; n>=20 holds: 1613/665/590).
- KN3 tuning record reproduced by my own refit: per-class order 3 (Seal) / 2 (others),
  lambda 0.8, train/tune tokens 9864/1030, 1962/185, 263/18, 42/8 (10% object split,
  seed 20261117 shuffle, NLL grid-tuning).
- Robustness probes: scratch rerun of probes.py output == object/output_probes.json
  (H5 0.5877/0.5592/0.5629/0.5784/0.5846; H7 0.6162, OOV fraction 0.2861; H8 exact 0,
  one-edit 870).

## Leak check (re-run by me on data/)
- Held-out mapped sequences appearing in the M77 sequence set: 0. Held-out objects with a
  length>=2 identity core attested in M77: 0 (checked on both kept=2363 and reps=1613).
  Consistent with H8 exact_M77_seq_match = 0.

## Frozen model record
- ctx-counts sha256 b4abeb67... (object/claim_model_frozen.json, same value in
  object/claim_object.json) IS reproduced by refitting the author's TemplateModel on M77 in
  the scratch copy; class priors (0.7587/0.1993/0.0360/0.0059) and kn3 lambdas (0.8 x4)
  match too.
- My independent template implementation hashes differently (72016c21...) because the
  author's wildcard loop adds +1 for the BOS wildcard twice (the BOS ctx is included in the
  context set it iterates over). No effect on any reported number: all per-object
  predictions and accuracies are identical between my and the author's fit.

## Orientation
Recomputed from data/: M77 first-position entropy 6.5980 vs final 4.7442 (final more
constrained); merged corpus 7.0105 vs 5.1724; reversing swaps the pair. Matches
object/output_direction_check.json (as_stored_matches true in both corpora) and its stored
im77 direction-code counts exactly.

## Non-determinism
- Only RNG draws in the pipeline: random.Random(20261117) (KN 10% split shuffle) and
  np.random.default_rng(20261117) (every bootstrap). No unseeded draw; the synthetic
  control is a deterministic scorer.
- Scratch reruns (sweep_main x2 + nulltest): property_A, m77, kn3, heldout, pool_detail
  content, and nulltest all identical to the stored object/*.json (only wall-clock
  timestamps differ); the frozen ctx-sha reproduces on rerun. My fully independent
  re-derivation matches on every claim-relevant value.

## Discrepancies found (none in the claim's property/statistic)
- The p2 field-symbol block inside object/output_sweep_main.json (acc_claim 0.0121,
  p 0.0003) predates the current code/: rerunning code/ now gives 0.7421 vs 0.7602
  per-site-majority (p 0.9995), and object/output_sweep_secondary.json records
  0.7511/0.7602 (p 0.9864). All versions agree on the verdict (p2 does NOT beat the
  per-site majority; a recorded negative partial-win check). 544 pool rows also carry
  symfam "Bull" in the stored file where current code emits "Unicorn" (the recorded DB
  cross-coding artifact). p2/symfam feed no number in the claim's property A or its p.
- 1136/1613 held-out objects contain >=1 OOV sign (mean OOV fraction 0.286); H7 shows
  accuracy rises to 0.6162 when wildcard positions are excluded, so OOV wildcards do not
  inflate the headline number.

## Verdict
Every property and claimed value of the object-type claim — pool construction, M77 training
set, per-site accuracies of all three systems, the full 10,000-resample paired-bootstrap
p-values, per-object predictions, M77-leak exclusion, frozen ctx-sha, and the orientation
check — was re-derived with my own checker and matches the stored files exactly (to
reported precision). No FAIL condition triggered: no mismatch in the claim's property or
statistic, no missing object, no unseeded RNG. Minor non-claim discrepancies (p2 block
version drift, symfam labels) are noted above.

context: subagent — started as a fresh isolated OpenClaw subagent that saw only the claim folder (plus a scratch copy of it and python3/sha256sum); wrote my own checker from the README definition before reading the author's model code
pass: true
