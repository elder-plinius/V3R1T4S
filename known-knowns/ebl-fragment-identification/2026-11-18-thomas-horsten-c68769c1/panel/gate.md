# Honesty gate — run 2026-11-17-2142 (ebl-fragment-identification)

status: CONFIRMED_PARTIAL
confirmed_scope: BM.68403 aligns to eBL corpus chapter /L/3/10 (Standard Babylonian; 24 consecutive lines, 270 signs, 9.26% mismatch; p_bonf ≈ 4.0e-05 < 1e-4 against 1,000,000 shuffled-line nulls, N = |S| = 40) and thereby meets partial win p2, since /L/3/10 ranks 0 in eBL's public ngram-matcher top 10 while being named nowhere in BM.68403's eBL record (joins empty, no corpus-chapter manuscript link, genre-level 'lexical' only — partial, flagged) and not identified in the titles/notes of the works that record cites (cited-book pages, e.g. Civil 2010 p.155, are outside the claim folder), with the matched block being ~45% restoration (11/24 lines, 128/281 signs attested) — a confirmed p2 remains a "candidate identification" per the criterion, accepted only by the eBL team or an Assyriologist.

## Panel (step 6)

Three fresh isolated subagent contexts, each given ONLY the claim/ folder (a
self-contained copy; they could see no run-folder state, notes, or verdicts):

- panel/reproduce.md — REPRODUCE — `context: subagent`, `pass: true`. Re-derived
  (b) with the frozen C aligner (full-chapter scan, band 0, min_block 6) → top hit
  /L/3/10/Standard Babylonian/-, score 612, aligned 270, misfrac 0.0926, 24 consecutive
  lines, spans (3,26)/(56,66); attested split 11/24 lines / 128/281 signs (b_attested
  true); (e) recurrence = exactly 1 unrelated textId (/L/1/1, threshold 118) < 5;
  (c) p-rule arithmetic verified (p_raw = 1/1000001 = 9.99999e-07, p_bonf = 40 × p_raw
  = 3.999996e-05 < 1e-4, real 612 > control_max 46); (a) joins==[] + no ms-link + no
  naming (genre-level 'lexical' partial); (d) TF-IDF top-10 rank 0. No non-determinism.
- panel/novelty.md — NOVELTY — `context: subagent`, `pass: true`. Live eBL re-check
  2026-11-18 02:06 UTC (statistics 200; /fragments/BM.68403 200; /match 403): record
  joins==[], genre-level 'lexical' only, no field names L/3/10; no chapter lists BM.68403
  in manuscripts[]; the 30 cited works' titles/notes do not identify the pair (closest:
  Civil 2010 'The Lexical Texts in the Schøyen Collection' p.155 — title-level, a stated
  residual, not a naming); bounded web check found no pre-2026-11-18 eBL/published
  identification of the pair.
- panel/criterion.md — CRITERION — `context: subagent`, `pass: true`. Judged p2
  literally: (a) PASS (flagged partial), (b) PASS (attested split reported, not a (b)
  sub-clause), (c) PASS (null faithful to 'line order shuffled'; N=|S|=40 the honest
  denominator; PREREG reachability |S|=40>39 → K_claim=1,000,000 satisfied), (d) rank-0
  in eBL's public ngram-matcher (the in-platform /match is 403-public; the public
  ngram-matcher is the executable baseline, frozen in PREREG — not a stretch), (e) 1 < 5
  unrelated. Non-subsumed: full (d) needs NOT-in-top-10 (it is rank-0) and p1 needs the
  shorter bar + NOT-in-top-10 — so this is a genuine, non-subsumed p2.

## Gate decisions (downgrade-only)

- All three skeptics pass; no hedging panelist, no reproduction mismatch (REPRODUCE
  re-derived (b) two independent ways, identical), no stretched definition beyond what
  the frozen PREREG + saved outputs support. Status CONFIRMED_PARTIAL (p2), NOT
  CONFIRMED_SOLUTION (the full criterion's (d) is deliberately failed — the match is
  rank-0 in the matcher top-10, which is exactly the p2 shape).
- The claim is a p2 (partial win), not a full-criterion win. Per the criterion's own
  acceptance clause, a confirmed partial is still a 'candidate identification' — final
  acceptance is the eBL team's / an Assyriologist's. The confirmed_scope states the two
  caveats (the matched block is ~45% restoration; the cited-book pages, e.g. Civil 2010
  p.155, are outside the claim folder and were checked only at title/note level).
- (c) is the strongest gate and was decided at the frozen K_claim = 1,000,000 (|S| = 40
  > 39 per the PREREG reachability clause), not at the K=400,000 diagnostic: real 612
  vs control_max 46, 0 of 1,000,000 controls ≥ 612, p_bonf = 3.999996e-05 < 1e-4,
  real beats every control.
- Downgrade-only checks all held: the (a) 'lexical' genre-level partial is flagged
  (not hidden), the attested split is reported (not a (b) failure), the N=40 denominator
  is the honest (not widened) one, and the p2 publication clause is judged on the
  evidence present (titles/notes), with book pages stated as a residual.
- A CONFIRMED_* status stands only if `kit/check_run.py` prints PASS and outbox/ holds
  the package; if not, the status is PROMISING.
