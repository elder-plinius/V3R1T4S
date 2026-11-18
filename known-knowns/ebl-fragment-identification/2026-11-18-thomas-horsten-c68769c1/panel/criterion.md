# CRITERION panel — ebl-fragment-identification, run 2026-11-17-2142
Role: DECISION. I judge the criterion literally against the frozen claim folder (claim-copy);
I did not re-run the null (REPRODUCE's job). Spot-checked (b)/(e)/(c)-arithmetic via checker_helper.py:
all match the claim objects. Files below are relative to claim/.

## Claim under test
BM.68403 → corpus chapter /L/3/10 (Standard Babylonian), claimed as PARTIAL WIN p2 (not the full criterion).

## (a) — PASS (partial, flagged)
- data/records/BM.68403.json: joins == [] ✓. BM.68403 is not in manuscripts[] of any of the 228 corpus
  chapters (checked against all 1,873 distinct museum numbers in data/corpus_all_signs.json) ✓.
- Naming under the frozen rule (code/check_a.py): series words for (L,3) = {lexical}. 'lexical' IS in the
  record text (cited title "The Lexical Texts in the Schøyen Collection"). Number tokens = {'-','10'}
  (chapter name '-' + str(idx) 10): NEITHER appears in the record text (0 hits each).
  Series present + number absent ⇒ PARTIAL under the frozen rule (pass, flagged). The genre-level
  'lexical' in a cited title is NOT a naming of THIS composition under the rule — stated, not hidden.
- The record's own genre path (CANONICAL/Literature/Hymns/Divine) contains neither the (L,3) series name
  nor any number token ⇒ the genre path itself does not name L/3/10.

## (b) — PASS (attested split flagged)
- object_BM.68403.json: 270 signs aligned, mismatch_frac 0.0926 (≤ 0.10), 24 consecutive lines (≥ 3) ⇒
  literal (b) satisfied under the frozen normalisation (NFC, primary reading, X wildcard; PREREG.md).
- Attested split (PREREG bank pitfall — restorations are encoded like attested signs): only 11/24 lines
  and 128/281 block signs (45.5%) are attested. The criterion's (b) text requires the alignment bars only;
  it contains no attestation sub-clause. Verdict: literal (b) PASSES; the attested split is reported and
  flagged for acceptance — it is NOT a (b) failure. The helper re-check shows the attested positions still
  meet the line/sign bar.

## (c) — PASS
- null_result_BM.68403.json: K = 1,000,000, seed grid 20261117+k, np.random.default_rng(seed).permutation(11461)
  over the 11,461-line corpus pool. This shuffles LINE ORDER and preserves sign content — exactly what
  "line order shuffled" specifies ⇒ the null model is faithful to the criterion's wording.
- p_raw = (1+0)/(1,000,001) = 9.99999e-07; p_bonf = min(1, p_raw × N), N = |S| = 40 ⇒ 3.999996e-05 < 1e-4 (strict).
- N = 40 is the honest denominator: |S| = 40 is the set of fragments ACTUALLY null-searched, frozen in
  PREREG.md before the first scored alignment; using the full search population |P| = 11,635 would only
  over-correct. The PREREG reachability clause (|S| = 40 > 39 ⇒ K_claim = 1,000,000) was satisfied
  (40/1,000,001 = 4.0e-5 < 1e-4).
- Real score 612 beats every control (control_max = 46, 0 of 1M controls ≥ 612), as PREREG requires.

## p2 top-10 / record / publications clauses
- Top-10: condition_d.tfidf_top10 ranks /L/3/10 at position 0 (in_top10: true) ⇒ the p2 condition "correct
  composition appears in eBL's own fragment-matcher top 10" holds.
- Is the offline TF-IDF a stretched reading of "eBL's own fragment matcher"? NO (judgment): the baseline is
  eBL's own public ngram-matcher library (commit e8918de), frozen in PREREG.md before scoring; the
  in-platform lineToVec /match route is 403-public (REPRODUCE.md, re-checked 2026-11-18; scout.md), so the
  public ngram-matcher is the executable baseline the bank names. Not a custom matcher.
- "Not recorded anywhere in its eBL record": holds as (a) above (partial 'lexical' flagged).
- "Not identified in the publications its record cites": judged on the cited works' titles/notes in
  data/records/BM.68403.json — none names L/3/10 or identifies BM.68403 as a witness of it (titles concern
  the fragment's Nabu-hymn colophon, school/lexical context, reviews; closest is "The Lexical Texts in the
  Schøyen Collection", p.155). Book PAGES are not in the claim folder ⇒ residual risk (Civil 2010 p.155)
  is a stated caveat, not a failure. The claim's wording does NOT overreach the evidence in the folder.

## (e) — PASS
- condition_e: e_n_unrelated = 1 distinct unrelated textId (only /L/1/1 Old Babylonian) < the ≥5-unrelated-
  compositions disqualification threshold (frozen operational definition, PREREG.md; helper spot-check agrees)
  ⇒ not a formula; (e) passes.

## Non-subsumption
- Full criterion (d) requires the match NOT in the top-10 — here it is rank-0 ⇒ full (d) fails ⇒ not a
  full-criterion win.
- p1 requires (a),(c),(d),(e) with the shorter 2-line / 10–14-sign bar and NOT-in-top10 — here the match is
  in-top10 and (b) full-pass ⇒ not p1.
- ⇒ the claim is a genuine, NON-SUBSUMED p2.

## Hidden-quantifier findings
1. (b) carries no attestation quantifier; the PREREG attested-position re-check is a bank pitfall to report,
   not a (b) sub-clause — attested split flagged, not failed.
2. (c) "Bonferroni-corrected over all fragments searched": frozen N = |S| = 40 (fragments actually
   null-searched) pre-scoring; |P| = 11,635 would be a stricter (more conservative) reading — no post-hoc stretch.
3. p2 "recorded anywhere" / "not identified": operationalized over the record's fields (joins, chapter
   manuscripts, references/uncuratedReferences/notes/dossiers/genres) and over cited works' titles+notes;
   cited-book pages outside the folder are caveats, not violations.
4. 'lexical' as genre-level series word: series-present + number-absent = partial pass under the frozen rule —
   flagged in object condition_a.partials, not hidden.
5. (e) "unrelated compositions" = distinct eBL chapter textIds (excluding the claimed chapter), frozen; count = 1.

## confirmed_scope
BM.68403 aligns to eBL corpus chapter /L/3/10 (Standard Babylonian; 24 consecutive lines, 270 signs, 9.26% mismatch;
p_bonf ≈ 4.0e-05 < 1e-4 against 1,000,000 shuffled-line nulls, N = |S| = 40) and thereby meets partial win p2, since
/L/3/10 ranks 0 in eBL's public ngram-matcher top 10 while being named nowhere in BM.68403's eBL record (joins empty,
no corpus-chapter manuscript link, genre-level 'lexical' only — partial, flagged) and not identified in the titles/notes
of the works that record cites (cited-book pages, e.g. Civil 2010 p.155, are outside the claim folder), with the matched
block being ~45% restoration (11/24 lines, 128/281 signs attested) — a confirmed p2 remains a "candidate
identification" per the criterion, accepted only by the eBL team or an Assyriologist.

context: subagent
pass: true
