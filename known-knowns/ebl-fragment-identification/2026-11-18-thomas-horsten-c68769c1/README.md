# ebl-fragment-identification — candidate identification (submission 2026-11-18-thomas-horsten-c68769c1)

## What

BM.68403 aligns to eBL corpus chapter /L/3/10 (Standard Babylonian; 24 consecutive lines, 270 signs, 9.26% mismatch; p_bonf ≈ 4.0e-05 < 1e-4 against 1,000,000 shuffled-line nulls, N = |S| = 40) and thereby meets partial win p2, since /L/3/10 ranks 0 in eBL's public ngram-matcher top 10 while being named nowhere in BM.68403's eBL record (joins empty, no corpus-chapter manuscript link, genre-level 'lexical' only — partial, flagged) and not identified in the titles/notes of the works that record cites (cited-book pages, e.g. Civil 2010 p.155, are outside the claim folder), with the matched block being ~45% restoration (11/24 lines, 128/281 signs attested) — a confirmed p2 remains a "candidate identification" per the criterion, accepted only by the eBL team or an Assyriologist.

Target: `ebl-fragment-identification` (V3R1T4S target bank, pinned commit
267887db2f73731ac85e21353fde7d82890fe192; success criterion and the p2 partial-win
statement verbatim in the-record-we-beat/criterion_verbatim.txt). This is a *candidate
identification*, not a decipherment: fragment-to-chapter sign-sequence alignment with a
frozen null, judged literally against the bank's partial win p2. It is explicitly NOT a
full-criterion win (condition (d) of the full criterion requires the match to be ABSENT
from the matcher top-10; here it is rank-0, which is exactly the p2 shape), and not p1.

## Check it yourself

    sh verify-it-yourself/run_checks.sh

Expected last line: PASS. It re-derives, with stdlib python3 only (no network, no
third-party packages), from this folder:
- the (b) top-hit alignment with a pure-python port of the frozen C aligner
  (object/... via how-we-built-it/code/swalign.c: Smith-Waterman, match +3 / mismatch
  -1 / gap -2 / wildcard +1, min_block 6, deterministic tie-break) — top hit
  /L/3/10/Standard Babylonian/-, score 612, 270 aligned, 9.26% mismatch, 24 consecutive
  lines, spans (3,26)/(56,66);
- the (b/attested) split (11/24 lines, 128/281 signs attested; ~54% restoration);
- the (c) frozen p-rule arithmetic from the saved K=1,000,000 null summary
  (p_raw = 1/1000001, p_bonf = 40 × p_raw = 3.999996e-05 < 1e-4, real 612 > control_max 46);
- the (d) eBL public ngram-matcher TF-IDF top-10 (re-implementation, commit e8918de)
  with the claimed chapter at rank 0;
- the (e) recurrence count (the 24-line/297-sign block recurs in exactly 1 unrelated
  textId, /L/1/1 Old Babylonian, threshold 118 < 5 ⇒ not a formula);
- the (a) unplaced-fragment rule (joins empty, no chapter manuscript link, no naming —
  genre-level 'lexical' partial flagged);
- the sha256 of every object file against the pins in the checker.

Rough laptop time: < 1 minute (stdlib only; the two full-corpus alignment scans dominate).

## Compared to

- The bank's partial win p2 (criterion_verbatim.txt): (a),(b),(c),(e) hold AND the
  correct composition appears in eBL's own fragment-matcher top 10 but is recorded
  nowhere in the eBL record and not identified in the publications the record cites.
  The object is exactly that. (b) and (c) are re-derived by the checker; (a)/(d)/(e)
  are re-derived from the saved record + corpus dumps; (c) is the saved K=1,000,000
  summary (the full 4 MB control array stays out of git — Recreation below).
- The eBL in-platform lineToVec matcher (`/api/fragments/{id}/match`) is 403-public, so
  the (d) baseline is eBL's own **public** ngram-matcher (commit e8918de), re-implemented
  offline and frozen in PREREG.md — the bank's named matcher for the public route
  (panel/novelty.md re-checked 2026-11-18; scout.md).
- No prior eBL record or pre-2026-11-18 publication identifies the pair (panel/novelty.md).

## Large object files (kept out of git, reproducible)

The full K=1,000,000 control-score array (4,000,532 bytes) is saved in the run folder at
`output/null_1000000_null_claimant.json.npz` (sha256 `dc61a3b121b7ef70...`, full hash in
RUN_IT_YOURSELF.md). It is a deterministic output, not new data:

- Generator: `how-we-built-it/code/null_big2.py` (the frozen "line order shuffled" null:
  per seed k, `np.random.default_rng(20261117+k).permutation(11461)` over the 11,461-line
  corpus pool, sign content unchanged; 24-thread). Every RNG draw is seeded (frozen seed
  grid 20261117+k, no unseeded global state).
- Inputs: the pinned corpus + fragment dumps (sha256s in RUN_IT_YOURSELF.md) and the
  frozen aligner (`how-we-built-it/code/swalign.c`).
- Recreation: `cd how-we-built-it && python3 code/null_big2.py 1000000 fids.json 24`
  (see RUN_IT_YOURSELF.md) reproduces the npz byte-for-byte; the package ships the
  resulting summary (`object/null_result_BM.68403.json`) so the checker needs no 4 MB file.

## Not claimed

- No full-criterion (a)-(e) win: the match IS in the matcher top-10 (rank 0), so the
  full criterion's (d) (absent from top-10) fails by design — this is p2.
- No p1 win (the p1 candidates Sm.1309 / K.9496 fail (c) at K=400,000).
- No decipherment, no reading of the text, no claim about the fragment's museum context
  beyond the eBL record's own fields.
- The matched block is ~45% editorial restoration (attested-position pitfall): the
  (b) bar is met on the aligned signs, and the attested split is reported; an
  Assyriologist weighs the restoration share on acceptance.
- Cited-book **pages** (e.g. Civil 2010 p.155) are outside the claim folder; the p2
  "not identified in the publications" clause is judged on the record's own titles/notes
  (no naming) — the book-level check is a stated residual (panel/novelty.md).

## Credits

- The electronic Babylonian Library (LMU Munich): public API, corpus dumps, the public
  ngram-matcher (e8918de) and lineToVec matcher (ebl-api, ebl-frontend).
- The V3R1T4S target bank entry `ebl-fragment-identification` (criterion + pitfalls).
- Prior V3R1T4S runs on eBL fragment identification (the frozen aligner, normalisation
  and null design carried forward in PREREG.md).
