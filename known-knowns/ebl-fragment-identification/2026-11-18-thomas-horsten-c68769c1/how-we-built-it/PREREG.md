# PREREG — ebl-fragment-identification (run 2026-11-17-2142)

Frozen 2026-11-17 23:58 UTC (before the first scored alignment of the search population).
`null_test: required`

## Success criterion (verbatim, from repo/bank/targets.json, ebl-fragment-identification)
At least 1 fragment must meet all of the following. (a) Its eBL record has no joins, no
corpus-chapter manuscript link, and no reference or genre naming the matched composition.
(b) It aligns to a specific composition witness (eBL corpus chapter or an Oracc edition) over
at least 3 consecutive lines or at least 15 consecutive signs, with at most 10% sign mismatches
after normalising sign readings. (c) The alignment score has p < 1e-4 against a null of the same
fragment aligned to all corpus lines with line order shuffled, Bonferroni-corrected over all
fragments searched. (d) The match is not returned in the top 10 of eBL's own fragment matcher
for that fragment. (e) The matched lines are not a formula that recurs in at least 5 unrelated
compositions. Claim as 'candidate identification', confirmed only when an Assyriologist or the
eBL team accepts it. Fragment status (a) and the eBL matcher output (d) are re-checked live at
verification time; an identification recorded in eBL or published before the claim voids it.

## Partial wins (verbatim)
- p1: A fragment meeting conditions (a), (c), (d) and (e) of the full criterion whose alignment
  to a specific composition witness covers 2 consecutive lines or 10-14 consecutive signs
  (below the full 3-line / 15-sign bar) with at most 10% sign mismatches after normalisation,
  at Bonferroni-corrected p < 1e-4 against the shuffled-line null.
- p2: A fragment meeting conditions (a), (b), (c) and (e) whose correct composition appears in
  eBL's own fragment-matcher top 10 but is not recorded anywhere in its eBL record (no join,
  corpus-chapter manuscript link, reference or genre naming it) and is not identified in the
  publications its record cites.

## Input data (frozen, hashed in scout.md / data/hashes_round1.txt)
- Fragments: /api/fragments/all-signs → data/fragments_all_signs.json
  (sha256 f8c66dc2…; 39,017 transliterated fragments, 627,745 lines, 5,746,787 sign tokens).
- Corpus witnesses: /api/corpus/all-signs → data/corpus_all_signs.json
  (sha256 8c1edadb…; 228 chapters, 9,401 lines, 124,324 sign tokens).
- Chapter id + manuscript links for condition (a): from the same corpus dump
  (textId/stage/name + manuscripts[].museumNumber).
- Oracc: NOT used as a witness this run (no Oracc dump in budget); witness set = the 228
  eBL corpus chapters. Stated, not hidden.
- Everything is sign-NAME data (the public 'signs' field); restorations are encoded like
  attested signs → the attested-position re-check below is mandatory (bank pitfall).

## Unplaced-fragment definition + search population (criterion a; frozen)
A fragment is a SEARCH candidate (unplaced) when, in its public eBL record, ALL hold:
- joins == []  (field: joins)
- no corpus-chapter manuscript link (checked against manuscripts[] of all 228 chapters; the
  fragment's museumNumber is not in any chapter's manuscript list)
- no reference / uncuratedReference / note / dossier / genre naming the matched composition
  (fields: references[], uncuratedReferences[], notes, dossiers[], genres[]; read
  references[].notes and dossiers[] per the 2026-10-16 finding).
Because the bulk dump carries only {_id, signs}, the FULL record check (joins, references,
genres, notes, manuscripts) is done LIVE per candidate at verification (and again before any
claim) via GET /api/fragments/{id}. For the offline search we pre-screen with a deterministic
rule on the dump (the 'unplaced' fields are then verified live on survivors only):

SEARCH POPULATION P (frozen selection rule, deterministic from the hashed dumps):
  P = { fragment f : f has >= 3 non-empty lines AND max line length >= 15 signs AND
        total sign tokens <= 800 }.
  |P| = 11,635 (computed from data/fragments_all_signs.json with the token cap; the 12,687 figure quoted
  in the first draft of this file omitted the 800-token cap — corrected 2026-11-17 23:59 UTC before any
  scored alignment; the selection RULE is unchanged).
Rationale: the three length gates reach the (b) bars (3 lines OR 15 signs); the token cap
bounds null cost. This is the frozen "all fragments searched" set; its size N = |P| is the
Bonferroni denominator for condition (c) (we search and screen all N; the expensive null is
run on the ranked (b)-passing subset S below, so N is the honest denominator).

## Composition-witness set (frozen)
The 228 chapters of /api/corpus/all-signs (hash above), identified by
"/genre/category/index/stage/name". No Oracc editions this run (stated). No dedup beyond
the eBL id: two chapter ids that share a textId+stage+name are distinct records and both kept.

## Normalisation (frozen, applied identically to fragment AND chapter sides — same pipeline)
- NFC normalise each token.
- variant reading "a/b/c" -> keep the PRIMARY reading "a" (first element); variants recorded
  but the alignment scores the primary reading.
- damaged/unknown sign token "X" -> the special wildcard token X (matches any real token with
  score xmatch=+1, a penalty vs a real match +3; an X aligned to a real token is NOT counted
  a hard mismatch).
- all other sign tokens kept verbatim (ABZ codes are case-stable; numerals/kept).
- lines = whitespace-free split; empty lines kept as separators (line tracking uses the
  line index of each token).
Freeze: the rule above is the only normalisation; it is applied before ANY scoring.

## Aligner (independent; frozen parameters)
- Banded Smith-Waterman sign-level local alignment over the flat token sequence with line
  tracking (code/swalign.c + code/sw.py). Scoring matrix (frozen): match +3, mismatch -1,
  gap -2, wildcard (X vs real) +1. min_block = 6 aligned signs. Band: full (band=0) for the
  null (fragment vs whole corpus pool) and for final candidates; band=40 for the cheap real
  screening. (band only prunes; the null is full.)
- The C aligner was verified to match an independent Python reference on 400 random pairs
  (0/400 disagreement) — recorded in the report.
- eBL's own matcher is NOT used for the primary alignment (its lineToVec output is used only
  for condition d, re-implemented offline from code/ebl-api fragment_matcher.py logic).

## Condition (b) bar (frozen)
A candidate (fragment f, chapter c) PASSES the full bar if the best alignment has
(consec_lines_a >= 3 OR aligned >= 15) AND mismatch_frac <= 0.10.
p1 bar (lens partial-p1): (consec_lines_a >= 2 OR 10 <= aligned <= 14) AND mismatch_frac <= 0.10.

## Condition (d): eBL's own matcher top-10 (frozen re-implementation)
eBL's fragment matcher (FragmentMatcher.rank_line_to_vec, ebl-api commit 545294b) compares the
fragment's lineToVec (line-structure vectors: START=0/TEXT_LINE=1/rulings/END=5) against every
other fragment's lineToVec and returns a ranking (top-15; we take top-10). "The match is not
returned in the top 10" = the claimed composition's chapter is not among the top-10
fragment-to-CHAPTER ngram-matcher hits. We run eBL's PUBLIC ngram-matcher (TF-IDF, default
n∈{1,2,3}) on the fragment's signs vs the 228 chapters (offline, from the same hashed dumps)
and record the top-10; the claimed chapter must be ABSENT from that top-10. (The in-platform
lineToVec /match route is also 403-public per the related target; the ngram-matcher library on
public data is the executable baseline the bank names.)

## Condition (e): formula-recurrence exclusion (frozen, operational)
A matched line sequence (the aligned block on the fragment, normalised) DISQUALIFIES if it
recurs in >= 5 UNRELATED compositions. Operational definition of 'unrelated': >= 5 DISTINCT
eBL chapter textIds (genre/category/index) — excluding the claimed chapter — contain an
alignment of the matched sequence with the same (b) bar (or, for a short p1 sequence, an
exact sign-sequence substring of length >=10 with <=10% mismatch). We count over the 228
corpus chapters (corpus-wide counting per the criterion). If >=5 distinct unrelated textIds
match, the candidate fails (e) (it is a formula, not a composition witness).

## Null design (criterion c; frozen)
- Null = the SAME fragment aligned (C aligner, full band, min_block=6) to the corpus pool
  (all 228 chapters' lines concatenated = 11,461 lines / 124,324 tokens) with LINE ORDER
  SHUFFLED. Shuffle mechanism: per seed, np.random.default_rng(seed).permutation(11461) of the
  line order; token content unchanged (only line order changes). This is a faithful
  "line order shuffled" null (it destroys real cross-line order; sign content is preserved,
  which is exactly what "line order shuffled" specifies).
- Seed grid (frozen): seed = 20261117 + k, k = 0..K-1.
- Control counts (frozen): K_screen = 400 controls for every (b)-passing candidate in S
  (satisfies the kit's >=400-control minimum and gives the best-control ranking). For the
  FINAL claimant, K_claim = 400,000 controls (enlarged so the Bonferroni level is reachable);
  if a claimant's null cannot reach the level, a larger K is a new PREREG.v2, never an edit.
- p-value (frozen): p_raw = (1 + #{controls with score >= real score}) / (K + 1).
  Bonferroni: p_bonf = min(1, p_raw × N), where N = number of fragments actually searched on
  the null = |S| (the ranked (b)-passing set, capped at 40, defined below). 
- Reachability: p_bonf < 1e-4 requires N/(K_claim+1) < 1e-4, i.e. |S| <= 39 with K_claim=400,000
  (39/400001 = 9.75e-5 < 1e-4). If |S| > 39, the claimant uses K_claim = 1,000,000
  (40/1,000,001 = 4.0e-5 < 1e-4). The real result MUST beat every control (best control <
  real score); if it does not, the candidate fails (c) regardless of p.
- The real result must beat EVERY control (report best control score next to the real score).

## Null-searched set S (frozen)
S = the top 40 (b)-passing candidates of P, ranked by: (1) attested sign-token count in the
aligned block descending, (2) rare-4-gram hit count descending, (3) museum-number string
ascending. |S| <= 40. N (Bonferroni denominator) = |S| (the fragments actually null-searched).
If fewer than 40 pass the (b) bar, S = all of them and N = |S|.

## Condition (a) + (d) live re-check (frozen)
At verification (and again immediately before any claim): for the claimant fragment fetch
GET /api/fragments/{id} and confirm joins==[], no chapter manuscript link (vs the 228 chapters'
manuscripts), no reference/uncuratedReference/note/dossier/genre naming the claimed chapter;
re-run the eBL ngram-matcher top-10 and confirm the claimed chapter is absent. (a) and (d) are
live; (b),(c),(e) are re-derived from the saved frozen objects.

## Thresholds summary (frozen)
- full: (>=3 consec lines OR >=15 consec signs) AND <=10% sign mismatches, p_bonf<1e-4,
  beats all controls, (a),(d),(e) hold.
- p1: (2 lines OR 10-14 signs) AND <=10% mismatches, p_bonf<1e-4, (a),(c),(d),(e).
- p2: (a),(b),(c),(e) hold AND the correct composition is in eBL's ngram-matcher top-10 but
  recorded nowhere in the record and not in its cited publications.

## What is NOT frozen / allowed
- The candidate ranking, witness set, normalisation, aligner parameters, null mechanism/seeds,
  control counts and thresholds are ALL frozen before the first scored alignment.
- (a) and (d) are re-checked LIVE (per the criterion) — that is required, not a plan change.
