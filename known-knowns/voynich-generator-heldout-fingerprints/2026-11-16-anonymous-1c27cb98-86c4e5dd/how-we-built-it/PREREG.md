# PREREG — voynich-generator-heldout-fingerprints (frozen)

Frozen: `date -u` at write time (see file mtime); written BEFORE any lens/attack output is
scored. Later changes are new `PREREG.v2.md` files, never edits.
`null_test: required` (category undeciphered-scripts; a search/statistical claim over
generator output judged against Voynich envelopes — the per-statistic 95% Voynich envelopes
are the null for outcome (A); the 99.9% envelope of the pre-registered falsifying
statistic is the null for outcome (B)).

## 0. Success criterion (verbatim, bank/targets.json)
Two outcomes qualify. (A) A generator. It must reproduce, per Currier dialect (A and B
separately) and on both ZL3b and IT2a, all of the following within the 95% envelope of the
Voynich values: (i) the two Naibbe failure statistics as defined in 2608.17096, edge-glyph
coupling (bits and share of entropy) and singleton-type rate; (ii) all four signatures of
2604.19762; (iii) Parisel's per-folio switch statistic. It must also reproduce at least 4
further pre-registered statistics never used in tuning (held out). It must be
hand-executable: at most 200 table entries plus a written procedure, and at most 1
per-folio state bit beyond the tables. Run it on at least 20 plaintexts from at least 2
period languages x 10 seeds. If space-regime statistics are included, the generator must
emit its own uncertain-space channel under a pre-declared rule. (B) A falsification of
Naibbe on a pre-registered statistic NOT among edge-glyph coupling, singleton or hapax
rate, the 2604.19762 signatures, or limitations in Greshko 2025. Naibbe output (unmodified
author code, default parameters, at least 20 plaintexts x 10 seeds) must fall outside the
99.9% Voynich envelope on A and B and on both transliterations. Neither outcome is a
decipherment. The 95% and 99.9% envelopes are computed at verification time from ZL3b-n.txt
and IT2a-n.txt as then published; any generator or falsification published after 2026-10-03
that already achieves the claimed outcome voids novelty.

## 1. Corpora and parsing (frozen)
- Inputs: ZL3b-n.txt and IT2a-n.txt exactly as fetched (sha256 in scout.md; fetched
  2026-11-16 11:42 UTC). IVTFF parsing (IVTFF_format.pdf v2.0 + plant_crib_attack.py of
  the pinned driver): running text = locus-letter P lines only; page header
  `<fol> <! ...>` supplies `$Q` (quire A..T) and `$L` (Currier language A/B, section-level,
  carries over to the locus lines of that page); body tokens via clean_tokens (strip
  `<...>`, `[x:y]`->x, `{...}`, `'`; split on `[.,\s]+`; keep only `[a-z]+` tokens free of
  `?*<>{}[]()|@`).
- Token stream per (T, d) = tokens of the P lines whose page `$L` = d, split by quire `$Q`
  (Zandbergen quires A..T; a quire belongs to exactly one language).
- Composite collapse (glyph-level stats only): SUBS cth->T, ckh->K, cph->P, cfh->F, ch->C,
  sh->S, iin->N, in->I, ee->E (the driver's plant_crib_attack.collapse).
- Envelope unit: quire. Envelope(S, d, T, 95%) = [2.5th, 97.5th] percentile, 99.9% =
  [0.05th, 99.95th] percentile, of the distribution of S over B=4000 quire-bootstrap
  resamples (resample the dialect's quires WITH replacement, fixed seed 20261116 + 1000*d
  + 100*T_index + S_index, pool the resampled quires' lines, recompute S on the pool).
  Statistics that are ratios of counts (hapax, E->S, MI, edit-1, coverage) are computed on
  the pool. Statistics defined per folio (switch) use the per-folio Voynich distribution
  (197 folios as fetched) with the same bootstrap over folios.

## 2. Exact statistic definitions (frozen; independent reimplementations in
attempts/*/code/, expected-vs-reproduced recorded in baseline/record.md)
- S1 edge-glyph coupling (2608.17096 §2.10/A.8, Table 4 "Voynich, observed spaces"):
  tokens split on BOTH '.' (certain) and ',' (uncertain) separators; per line, pairs
  (last char of collapsed previous token, first char of collapsed next token); observed MI
  (bits) of (left->right); 100 within-line token shuffles (fixed seed), mean shuffled MI;
  S1_bits = MI_obs - mean(MI_shuf); S1_share = S1_bits / H(marginal of the next-token first
  char) (share of the entropy of the predicted variable). Published Voynich: 0.197 bits,
  5.7%; Currier A 0.137 bits (3.9%), B 0.248 bits (7.4%). Naibbe (PR16/paper): 0.006 bits,
  0.2-0.3%.
- S2 singleton-type rate (2608.17096 Table 7 "Hapax"): over the raw (un-collapsed) token
  stream, hapax = (#types with count==1)/(#types). Published Voynich: ~70% (paper: 69.7%
  at 32,747 tokens; Currier A 72% in the §3.1 pinyin comparison). Naibbe: 40.5-41.7%.
- S3 h2 (2608.17096 Table 7 "h2"): first-order conditional entropy of the composite-
  collapsed glyph stream (all P-line tokens concatenated, spaces removed, after SUBS
  collapse), bits/glyph. Published: Voynich 2.69; Naibbe 2.71.
- S4 word-length distribution (2608.17096 joint profile "span"): distribution of raw-
  token lengths (glyph chars, un-collapsed). Frozen summary stats: (a) mean token length,
  (b) share of length-1 tokens. Envelopes via quire bootstrap as in §1.
- S5-S8 the four 2604.19762 signatures (definitions from the paper + the public code
  labyrinthinesecurity/currier-signatures @5d50101; pipeline = the repo's verifier.py
  grapheme tokenizer + evaluate metrics, per-dialect calibration on the manuscript file as
  published — but our envelopes are RECOMPUTED from the fetched ZL3b/IT2a per §1):
  S5 Sig1 E->S: grapheme classes (start if start_count > 2*end_count, end if end_count >
  2*start_count, else ambiguous; start/end counts = occurrences as first/last grapheme of
  a token); E->S% = 100 * (#boundaries where prev token ends in an end-class grapheme and
  next begins with a start-class grapheme)/(#boundaries). Published reference: A 71.0%
  (adaptive [56,86]), B 64.3% ([50,79]).
  S6 Sig2 bilateral positional extremity: Se = #graphemes with (start+1)/(end+1) > 100,
  Ee = #with (end+1)/(start+1) > 100; bilateral iff Se>=1 and Ee>=1; "present in >50% of
  runs" = of the 10 seed-runs of the generator (published: A Se=3, Ee=3; B Se=3, Ee=7).
  S7 Sig3 cross-boundary MI: raw (un-shuffled) MI in bits between the last grapheme of a
  token and the first grapheme of the next (grapheme = the tokenizer's atomic unit, NOT
  the char level of S1). Published: A 0.5856 (>=0.29), B 0.4980 (>=0.25).
  S8 Sig4 boundary distribution shape: first-grapheme rank-frequency Zipf fit: R^2 and CV
  of the (log-rank, log-freq) regression; shape = Zipfian if R^2>0.85 and CV>0.8,
  Plateau if CV<0.5, else Intermediate; pass = non-Plateau. Published: A Zipfian
  (R^2=0.863, CV=1.45), B Intermediate (R^2=0.805, CV=1.53).
  Envelopes for S5-S8: quire bootstrap of the per-quire statistic (S6 is a per-run
  fraction, no envelope: pass = >50% of 10 seed-runs bilateral, matching the paper's
  "present in >50% of runs").
- S9 Parisel per-folio switch statistic (2604.25979 §2.9/§5, eq. 1): a word (collapsed) is
  cho-type iff it contains "cho" or "sho" (in the collapsed form: C+o or S+o) and not
  "che"/"she" (C+e/S+e); che-type iff it contains C+e or S+e and not C+o/S+o; words with
  both or neither are excluded; per folio f: r_cho(f) = n_cho/(n_cho+n_che); switch
  sigma_f = 1 iff r_cho > 0.5. Frozen per-folio "folio" for generated text: 21-line blocks
  (3950 template lines / 185 pages = 21.35; use 21, last block shorter, dropped if <5
  classifiable words). The switch statistic for a corpus = (a) share of folios/blocks in
  the ambiguous band [0.3, 0.5], (b) mean r_cho of cho-state units (r>0.5), (c) mean r_cho
  of che-state units (r<=0.5). Published Voynich (recomputed, not trusted blindly):
  ambiguous 6.8% (10/197 in [0.4,0.6)+[0.2,0.4) tail per Table 7), p1 = 0.682 (105
  folios), p0 = 0.160 (90 folios), BC = 0.661, DeltaAIC = 2549, 195/197 assigned >0.8.
  Pass rule for a generator (pre-declared): ambiguous share within the 95% Voynich
  envelope (bootstrap over folios), AND mean of cho-state within the 95% envelope of the
  Voynich cho-state mean, AND mean of che-state within the 95% envelope of the che-state
  mean (per dialect d the same three checks against the dialect's Voynich units; a
  generator is scored in A-mode and/or B-mode, each mode checked against the envelopes of
  BOTH transliterations of that dialect).
- H1-H4 pre-registered HELD-OUT statistics (>=4, named here before any scoring; none is in
  any published generator's tuning set — the tuning sets: Naibbe (glyph entropy, BPE gap,
  token order, word shape, respacing frequency), slot/grille (S5-S8), self-citation
  (token length + vocabulary size); novelty re-checked in lens 2 incl. post-2026-10-03):
  H1 edit-1 adjacency ratio (2608.17096 Table 4 "Edit-1"): 100 * (observed #adjacent token
  pairs within Levenshtein edit distance 1, on the collapsed tokens) / (same count under
  100 within-line shuffles, mean over shuffles). Published: Voynich 1.12 (A 1.20, B 1.07);
  Naibbe 0.82. THIS IS THE PRE-REGISTERED FALSIFYING STATISTIC FOR OUTCOME (B) (not among
  the excluded set of §0).
  H2 line-initial vs mid-line token-initial JSD (2608.17096 A.7): Jensen-Shannon
  divergence between the glyph distribution of line-initial positions (first glyph of the
  line's first clean token) and mid-line token-initial positions (first glyph of the
  remaining tokens of the same line), per the paper's A.7 (published JSD 0.487 vs 0.200
  for the two line-set definitions; we use the "page-opening + left-margin" definition
  where available, else all-line definition; frozen: all P-line definition, per quire).
  H3 top-50 token coverage (PR16 summary JSON field top_50_token_coverage): total count of
  the 50 most frequent tokens / total tokens. Published: Voynich 0.332; Naibbe 0.377/0.376.
  H4 quire-CV of the hapax rate: coefficient of variation of the per-quire S2 values
  (Voynich is quire-stable per 2608.17096 §3.1; a generator's per-block hapax is expected
  to vary more). Published Voynich value: recomputed from the fetched file (expect small).

## 3. Envelope method summary (frozen)
- At verification time (NOW, from the fetched files): for each S in {S1_bits, S1_share,
  S2, S3, S4a, S4b, S5, S7, S8_R2, S8_CV, S9a, S9b, S9c, H1, H2, H3, H4} and each (d, T) in
  {A,ZL3b; A,IT2a; B,ZL3b; B,IT2a}: B=4000 quire-bootstrap resamples (seeds per §1) ->
  95% and 99.9% percentiles. S6 (bilateral) and the per-folio switch state means use the
  Voynich unit distributions directly (per-folio, or per-run fraction).
- Reproduction gate (before any scoring): the recomputed Voynich values must be within
  tolerance of the published ones: S1_bits 0.197 +/- 0.02 (and A 0.137, B 0.248 +/- 0.02);
  S2 0.70 +/- 0.03; S3 2.69 +/- 0.05; S5 A 0.710/B 0.643 +/- 0.05; S7 A 0.586/B 0.498
  +/- 0.10; S8 shapes as published; S9 p1 0.682/p0 0.160 +/- 0.05. And the Naibbe
  reproduction (pinned driver, baseline/) must land within: edge (PR16 alpha=1) -0.0016
  +/- 0.005, hapax 0.405-0.417, h2 2.707 +/- 0.05, k64 gap 1.028 +/- 0.05, order 1.25%
  +/- 0.3pp, table check 0 unreproducible of 34,764. If a gate fails, the comparison is
  UNRESOLVED for that statistic (recorded; never retuned to pass).

## 4. Pre-registered generator design space (outcome A / p1 / p2 / p3)
Base engine (hand-executable, frozen): Greshko Naibbe procedure — 6 tables x 23 letters =
138 homophone-set entries (unigram/prefix/suffix string sets from the published CSV,
356 unique glyph strings; <=200 entries OK), 52-card deck (alpha 20, beta1/2/3 8 each,
gamma1/2 4 each), respacing P(unigram)=17/36, v1 ambiguity rule (redraw when
prefix+suffix string equals any unigram string). Written procedure = deck/respacing/
ambiguity rules + the modifications below. Plaintexts: 20 chunks (10 Latin: the driver's
prepared Caesar De Bello Gallico I-IV stream, 10 Italian: Dante Commedia via the author's
clean_line pipeline + w->uu, j->i, k->c, v kept), each ~13k words; seeds
2026111601..2026111610 (10) applied to the Naibbe rng per (plaintext, seed) = 200 runs.
Line template: wrap generated tokens into the 3,950-line Voynich length template (the
published control convention; template = per-line token counts of the ZL3b P-lines as
fetched).
Extensions (pre-declared; the ONLY mechanisms allowed; none of H1-H4 may be used in
tuning):
 (E1) edge-boost table: <=64 entries (last-char class -> first-char class -> multiplier m
 in [0, 2, 5, 10] applied to the table-choice weights of the first-letter draw of the next
 token); tuned only against S1/S7 (and S5, S8 when targeting p2) on ONE held-back plaintext
 (chunk 11 of the Latin set is the tuning chunk; chunks 1-10 + all Italian chunks are
  scoring runs — no wait: 20 chunks x 10 seeds; frozen: tuning uses chunk L1 (Latin #1)
  with 3 of the 10 seeds; scoring = all 200 runs; the tuning chunk's values are reported
  but the pass is judged on the pooled 200-run corpus and the per-plaintext means).
 (E2) hapax schedule: the gamma tables (8 of 52 deck weight) may be re-weighted to
 gamma1=g, gamma2=4 (g in {4, 8, 16, 32}), or deck weights rescaled (pre-declared grid
 g in {4, 8, 16, 32}); tuned only against S2 on chunk L1; the chosen g is frozen before
 scoring; the 52-card deck composition (alpha 20, betas 8x3) is otherwise unchanged.
 (E3) p3 switch bit: exactly one per-folio state bit. For each (table, letter) entry,
 homophone strings are grouped: che-class = contains "che" or "she"; cho-class = contains
 "cho" or "sho"; other-class = contains ch/sh with neither vowel class, or no ch/sh.
 When bit=1: sample only from (cho-class UNION other-class); when bit=0: only from
 (che-class UNION other-class); if the chosen class set is empty for an entry, fall back
  to the full entry set. Tables otherwise UNMODIFIED. Pre-declared bit schedules: (i)
  Bernoulli(0.5) seeded per 21-line block (seed = run seed + block index), (ii) constant
  bit per dialect mode (A-mode -> 0 = che-biased, B-mode -> 1 = cho-biased). A p3 pass
  requires ONE pre-declared schedule.
 (E4) dialect mode: A-mode or B-mode changes ONLY the edge-boost multipliers and the
 E3 constant-bit default (the E1 table is tuned separately per mode on chunk L1); no
 other parameter may differ between modes.
Dialect assignment of the generator: it targets the dialect named in its mode; a pass on
"d, T" uses the (d, T) envelope. Full (A) outcome: every S in {S1_bits, S1_share, S2, S3,
S4a, S4b, S5, S6, S7, S8, S9a, S9b, S9c, H1, H2, H3, H4} inside the 95% envelope of BOTH
transliterations, in A-mode AND B-mode (S6: >50% of the 10 runs bilateral in each mode).
p1: the subset {S1_bits, S1_share, S2, S3, S4a, S4b} (the two Naibbe-failure stats + the
already-matched h2/word-length). p2: S5-S8 jointly (per dialect, both transliterations).
p3: S9 under E3 (and no regression on {S1_bits, S2, S3, S4a, S4b} envelopes).

## 5. Pre-registered falsifier (outcome B)
Object: greshko/naibbe-cipher UNMODIFIED (author's naibbe.py v1 procedure, default
parameters: 52-card deck as above, RESPACING=17, UNAMBIGUOUS=True, v1 ambiguity rule,
USE_78_CARD_DECK=False, no 3% space-removal) — executed via the checksum-pinned
reimplementation (lrozanova/voynich-units @956a7c4, analysis/reproduce_naibbe_control.py
sha256 df9f01ed...ecd8e) which reproduces the author's shipped Pliny ciphertext token-
for-token (34,764 tokens, 0 failures, PR16); the driver's four listed deviations are
accepted as "the published procedure" (they match the author's default settings).
Runs: 20 plaintexts (same set as §4) x 10 seeds (same as §4) = 200 runs, each wrapped on
the line template. Statistic: H1 (edit-1 ratio, §2) computed (a) pooled over all 200 runs
(PRIMARY) and (b) per plaintext (mean of the 10 seeds, SECONDARY). PASS (falsified) iff
the PRIMARY value is strictly OUTSIDE the 99.9% Voynich envelope of all four (d, T) cells
(< lo or > hi) AND each of the 20 SECONDARY values is outside the 99.9% envelope of its
dialect's two cells (A chunks vs (A, ZL3b)+(A, IT2a); B chunks vs (B, ZL3b)+(B, IT2a) —
plaintexts are assigned to a target dialect by a pre-declared 10/10 Latin/Italian split
with 5 of each dialect: chunks L1-L5, I1-I5 vs the A envelopes; L6-L10, I6-I10 vs the B
envelopes; rationale recorded in the baseline: dialects differ in exactly these
signatures, and the criterion asks for outside-on-A-and-B, so each half is tested against
one dialect's two transliteration cells).
null_test.md (written after the run, copied from program output): controls: 4000 quire-
bootstrap resamples per (d, T, statistic) (16 statistics x 4 cells); best_control: the
nearest 99.9% envelope bound reached by the real value; real: the observed H1 value(s);
real_beats_all_controls: yes iff real is outside the 99.9% envelope (for the falsifier,
"beats" = outside; direction frozen above); command: how to rerun.

## 6. Hand-executability limits (frozen interpretation)
- <=200 table entries: one entry = one (table, letter) homophone set (Naibbe: 138) OR one
  edge-boost row (E1: <=64) OR one deck-weight row (6). Total allowed <= 200 + the 356
  glyph strings carried BY the entries (strings are data inside entries, not entries).
- Written procedure: deck dealing, respacing probability, ambiguity rule, template wrap,
  E3 bit rule, E2 weight rule — all in <= 1 page of prose + the tables.
- <=1 per-folio state bit: only E3 uses state, exactly 1 bit per 21-line block; E1/E2 are
  stateless table/weight choices.
- No learned model, no fitted n-gram table beyond E1's <=64 multipliers.

## 7. Novelty gate (pre-registered check, lens 2)
- Status source re-fetched live before claiming (one honest GET).
- arXiv listing check: any paper after 2026-10-03 (bank status_checked date) that
  publishes a hand-executable generator already inside the claimed envelopes, or a
  falsification of Naibbe on H1, voids the novelty of that claim (tie is not a win).
- H1-H4 novelty: confirm none appears in the tuning set of any PUBLISHED generator
  (Naibbe Greshko 2025 + repo; slot/grille 2604.19762; Timm-Schinner 2020 self-citation;
  anything newer found by the listing check). H1 additionally must be outside the
  criterion's excluded set (it is: not edge-coupling, not hapax, not S5-S8, not a
  Greshko-2025 limitation — Greshko's published limitations are entropy/BPE/order/
  respacing-related, not edit-distance adjacency).

## 8. Reproduction-before-scoring (step 3c) gate (frozen tolerances in §3)
Baseline = the pinned driver output (baseline/naibbe_driver.json) + PR16 summary values
(edge crossfit, hapax) + the currier-signatures calibration (S5-S8 references). Record
expected-vs-reproduced in baseline/record.md BEFORE the first lens report is written.
