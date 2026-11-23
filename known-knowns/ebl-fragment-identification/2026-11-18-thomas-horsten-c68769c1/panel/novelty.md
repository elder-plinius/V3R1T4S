# NOVELTY skeptic check — run 2026-11-17-2142, target ebl-fragment-identification, p2
Claim under test: BM.68403 ~ chapter /L/3/10/Standard Babylonian/- (claim date 2026-11-18).
Files below named relative to claim/ (claim-copy = self-contained copy of run's claim/).

## 1. LIVE eBL re-check (UTC 2026-11-18 02:06:24)
- `GET https://www.ebl.lmu.de/api/statistics` → HTTP 200:
  `{"transliteratedFragments": 39106, "lines": 636199.0, "totalFragments": 328942}`
- `GET https://www.ebl.lmu.de/api/fragments/BM.68403` → HTTP 200 (saved to a scratch file (nov_rec.json, outside the package); keys incl. joins, genres, notes, dossiers, references, uncuratedReferences, publication, description).
- `GET https://www.ebl.lmu.de/api/fragments/BM.68403/match` → HTTP 403 (expected 403-public; offline TF-IDF top-10 in object_BM.68403.json is the executable (d) baseline).

Live record fields (quoted from the scratch copy of the live record, nov_rec.json, saved outside the package):
- joins: `[]` ✓ (claim requires empty)
- genres: `[{"category": ["CANONICAL", "Literature", "Hymns", "Divine"], "uncertain": false}]` — genre-level only, no named composition
- notes: `{"text": "", "parts": []}` (empty)
- dossiers: `[]`; publication: `""`
- description: "Clay tablet; fragment; dedicatory inscription of Nabu-shumu-lishir; Late Babylonian." (museum: THE_BRITISH_MUSEUM, collection: "Sippar")
- Frozen (a) rule applied over whole record (series words incl. 'lexical'; number tokens {'-'}; series+number both => named, series alone or number alone => partial, passes):
  - string hits for 'lexical'/'3/10' in ALL fields (recursive scan):
    - `/references[2]/document/title` => "The Lexical Texts in the Schøyen Collection"
    - `/uncuratedReferences[0]/document` => "Civil 2010 The Lexical Texts in the Schøyen Collection CUSAS 12"
  - No field (references[].notes, references[].document.title, uncuratedReferences, notes, dossiers) contains a number token for /L/3/10 (no '3/10', no 'L 3' text-id).
  - => series word 'lexical' present, number absent => PARTIAL (genre-level), not a named identification. Matches object_BM.68403.json condition_a: `"pass_a": true, "partials": ["series name 'lexical' present (genre-level), number '-' not -> partial"]`. (a) HOLDS live.

## 2. Corpus pre-listing check
`python3` one-liner over data/corpus_all_signs.json (symlink → run data/corpus_all_signs.json; list of 228 chapter nodes): no chapter's `manuscripts[]` lists "BM.68403" (NONE). Output: `chapters listing BM.68403 in manuscripts[]: NONE`.

## 3. Cited-publications check (p2 last clause; title-level, bounded)
13 references + 17 uncurated references in the live record. Each (title / pages from record):
1. Lambert 1978, "Nabu Hymns on Cylinders", ch. in Festschrift Lubor Matouš II — DISCUSSION
2. Civil 2010, "The Lexical Texts in the Schøyen Collection", CUSAS 12 (p. 155) — title says "lexical texts" generically for the Schøyen Collection; does NOT name L/3/10, "lexical text 3", or BM 68403; notes field only "By A.R. George"
3. Gesche 2001, "Schulunterricht in Babylonien im ersten Jahrtausend v. Chr.", AOAT 275 (pp. 98, 130, 183, 345)
4. Mayer 1992, "Ein Hymnus auf Ninurta als Helfer in der Not", OrNS 61: 17-57 (p. 2)
5. Oelsner 2004, review of Gesche, ZA 94: 131-142 (p. 5 / pp. 34)
6. Gesche 2005, "Nos. 65–66: Late Babylonian School Exercise Tablets", CTMMA 2: 257-265 (pp. 310-311)
7. Mayer 1990, "Sechs Šu-ila-Gebete", OrNS 59: 449-490 (p. 7 / pp. 280, 294)
8. Maul, "tikip santakki mala bašmu", Fs Borger (pp. vii-xvii; pp. 12, 14, 386)
9. George & Bongenaar 2002, "Tablets from Sippar: Supplementary bibliography …", OrNS 71: 55-156 (note: "Lambert *Matouš Fs* II pp. 110–11")
10. George 1992, "Babylonian Topographical Texts", OLA 40 (p. 163); "George 2010 The colophon of MS 5007 CUSAS 12" (p. 4)
11. Leichty & Grayson, "Catalogue of the Babylonian Tablets in the British Museum VII: Tablets From Sippar 2" (CBT VII; p. 39)
Verdict: no TITLE and no record NOTE identifies BM.68403 as a witness of L/3/10 or lexical text 3; the closest signal is the 'lexical' series word in Civil 2010's title (the p2 "lexical" partial the claim already flags).

Bounded web check (single search: `"BM 68403" OR "BM.68403" lexical eBL Schøyen`, searxng, 2026-11-18; top 3 hits, no dates exposed by provider):
1. "Lexical and Other Notes on Old Babylonian Letters in the Schøyen Collection" — publications.hse.ru (article page)
2. "CUSAS 12: The Lexical Texts in the Schøyen Collection By Miguel Civil" — eisenbrauns.org (2010 book page)
3. "CUSAS 12, 1.1.1 (P250505)" — cdli.earth (Schøyen lexical tablet artifact page)
None of the top-3 hits identifies BM 68403 with L/3/10 / lexical text 3; hits are collection-level. (Remaining hits: Schøyen variant-readings blog, other CDLI lexical artifacts, eBL magazin, r/Assyriology — none specific to the pair.)

## 4. eBL record novelty (pre-claim identification?)
No eBL record field (references/notes/genres/dossiers/publication) identifies BM.68403 with a NAMED composition; genres is generic "Hymns/Divine" literature. The 'lexical' word is genre/series-level (partial), not an identification of this chapter. Novelty of the BM.68403 ↔ /L/3/10 identification is NOT voided by eBL as of 2026-11-18 02:06 UTC.

## 5. Condition (e) quoted (no re-run), from object_BM.68403.json:
`"condition_e": {"fid": "BM.68403", "chapter": "/L/3/10/Standard Babylonian/-", "block_lines": 24, "block_signs": 297, "e_thr": 118, "attested_frac_lines": 0.46, "e_n_unrelated": 1, "e_pass": true, "e_hits_top6": [{"cid": "/L/1/1/Old Babylonian/I", "textid": ["L", 1, 1], "aligned": 284, "misfrac": 0.028}], "e_textids": [["L", 1, 1]]}`
=> 1 unrelated textId (not >=5), as claimed. (d) baseline also quoted from same file: tfidf_top10[0] = "/L/3/10/Standard Babylonian/-", `"rank": 0, "in_top10": true`, note "offline TF-IDF re-implementation of eBL public ngram-matcher (commit e8918de); /match route 403-public" — consistent with live 403.

## Could / could not verify
- Verified live: eBL record 200 + joins==[] + (a) partial-only; /match 403 (baseline note); corpus: no chapter lists BM.68403.
- Verified at title/field level: 13+17 cited works and record notes do not name the pair; single web search top-3 hits.
- NOT verified (bounded): page-level book content (Civil 2010 p. 155; Gesche 2001 pp. 98/130/183/345; Mayer 1990/1992; CBT VII p. 39), paywalled sources, non-English literature 2024-2026. Residual risk: a page-level statement in Civil 2010 p. 155 could discuss the fragment — title does not identify it with L/3/10.
- Observation: record's museum field says THE_BRITISH_MUSEUM (accession 1882,0918.8401, collection "Sippar"); claim's "Schøyen Collection" label is not contradicted by any eBL field (no collection field names Schøyen), but worth noting.

context: subagent
pass: true
