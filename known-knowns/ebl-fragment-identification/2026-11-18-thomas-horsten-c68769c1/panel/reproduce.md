# REPRODUCE skeptic — run 2026-11-17-2142, target ebl-fragment-identification, BM.68403 (partial win p2)

Claim: fragment BM.68403 (eBL, Late Babylonian, Sippar) aligns to chapter /L/3/10/Standard Babylonian/-
over 270 signs / 24 consec lines, 9.26% mismatch (<=10%); chapter is rank-0 in eBL public TF-IDF
ngram-matcher top-10; no join/manuscript/reference/genre naming (genre-level partial 'lexical');
shuffled-line null K=1,000,000 seed grid 20261117+k, N=40 Bonferroni gives p_bonf 3.999996e-05 < 1e-4,
real (612) beats every control (control_max 46); matched block recurs in exactly 1 unrelated textId (<5).

All paths relative to claim-copy/ (self-contained copy of claim/).

## Claimed values (object_BM.68403.json, read in full)
- (b): score 612, aligned 270, mismatch_frac 0.0926, consec_lines_a 24, a_span (3,26), b_span (56,66);
  attested: 11/24 lines, 128/281 signs (restored 13 lines / 153 signs).
- (c): K=1,000,000, N=40, real=612, control_max=46, control_p999=30, n_ge=0,
  p_raw=9.99999000001e-07, p_bonf=3.999996000004e-05, beats_all_controls=true, pass=true.
  Rule: "p_raw=(1+#ge)/(K+1); p_bonf=min(1,p_raw*N); N=40=|S| (frozen PREREG);
  |S|=40>39 -> K_claim=1,000,000 per PREREG reachability clause".
- (d): tfidf_top10[0] = /L/3/10/Standard Babylonian/-, rank 0, in_top10 true;
  note: "offline TF-IDF re-implementation of eBL public ngram-matcher (commit e8918de); /match route 403-public".
- (e): block 24 lines / 297 signs, e_thr 118, e_n_unrelated 1, e_pass true;
  single hit /L/1/1/Old Babylonian/I (textid [L,1,1], aligned 284, misfrac 0.028).
- (a): pass_a true, fails [], partials ["series name 'lexical' present (genre-level), number '-' not -> partial"].

## Check 1 — helper re-derivation (checker_helper.py)
Read helper source: frozen aligner (code/search2 Aligner, band=0, min_block=6), frozen (e) threshold
max(15, int(0.4*block_signs)); re-derives (b) top hit (full chapter scan), attested split, (e) count,
(c) arithmetic from saved null_result. (c) is a spot-check of the frozen p-rule against the saved
K=1,000,000 summary (allowed for the p-value), not a re-run of the 1M null. Output (verbatim):
```
(b) top hit: /L/3/10/Standard Babylonian/- score 612 aligned 270 misfrac 0.0926 consec_lines_a 24 a_span (3, 26) b_span (56, 66)
(b) matches claim (612, /L/3/10/Standard Babylonian/-, 270, 0.0926, 24): True
(b/attested) attested_lines 11 / 24 attested_signs 128 / 281 b_attested(>=3L or >=15S): True
(e) block 24 lines / 297 signs; threshold 118 -> hits: [('/L/1/1/Old Babylonian/I', 284, 0.028)] distinct unrelated textIds: 1 e_pass(<5): True
(c) K 1000000 N 40 real 612 control_max 46 n_ge 0 p_raw 9.99999000001e-07 p_bonf 3.999996000004e-05 p_bonf<1e-4: True beats_all: True
```
All match the claim. Hand check of (c): p_raw=(1+0)/1000001=9.99999000001e-07; p_bonf=40*p_raw=3.999996e-05 < 1e-4; 612 > 46 (beats every control). Confirmed.

## Check 2 — independent (b) re-derivation (own script, not the helper)
Own 6-line script: frozen Aligner (band=0, min_block=6), full scan of every corpus chapter,
same corpus + normalise_signs + BM.68403_signs.json:
```
TOP /L/3/10/Standard Babylonian/- 612 270 0.0926
```
Matches the claim exactly (top cid, 612, aligned 270, misfrac 0.0926 <= 0.10). Full scan, not a sample.
Attested split per object file (11/24 lines, 128/281 signs) confirmed by helper via code/attested.py.

## Check 3 — (c) null summary + mechanism (saved, not re-run)
null_result_BM.68403.json key fields (verbatim): real 612, K 1000000, N 40, control_max 46,
control_p999 30, n_ge 0, p_raw 9.99999000001e-07, p_bonf 3.999996000004e-05, beats_all_controls true.
Mechanism = literal "line order shuffled" null, confirmed in PREREG.md L120-125: pool = all 228
chapters' lines concatenated (11,461 lines / 124,324 tokens); per seed
np.random.default_rng(seed).permutation(11461) of the line order; token content unchanged;
seed grid 20261117+k (PREREG L125). PREREG L133-135: reachability — |S|=40>39 -> K_claim=1,000,000
(40/1,000,001 = 4.0e-5 < 1e-4); real MUST beat every control. code/null_big2.py one_seed() implements
exactly rng.permutation(len(pool)) with the same frozen aligner (band=0, min_block=MIN_BLOCK).
The full 1M-control array is NOT in the claim folder (run-folder output/null_1000000_null_claimant.json.npz);
verified p-rule arithmetic + beats-all flag + mechanism from the saved summary only. Not re-running the
1M null (spot check of the frozen rule, kit-permitted for the p-value; the author's K=1,000,000 run is
recorded in null_result). No non-determinism in the saved rule (frozen seed grid).

## Check 4 — (a) record + corpus manuscript check
- data/records/BM.68403.json: `joins: []`. dossiers [], notes.text "".
- Reference notes/document titles scanned (Nabû Hymns on Cylinders, Sechs Šu-ila-Gebete, etc.): none
  name /L/3/10 series+number; no literal "L/3/10". Only series-word hit: "The Lexical Texts in the
  Schøyen Collection" (a reference title) — series 'lexical' without number token '-' -> partial,
  consistent with the frozen rule (code/check_a.py: both series+number => fail; one => partial, passes;
  SERIES[("L",3)] = ["lexical"], number tokens {'-' for /L/3/10).
- BM.68403 in no chapter's manuscripts[] (one-liner, output `[]`).
- (a) PASS with genre-level partial 'lexical' — matches object condition_a (pass_a true, partials as above).

## Check 5 — (d) TF-IDF rank-0
object condition_d: tfidf_top10[0] = /L/3/10/Standard Babylonian/-, rank 0, in_top10 true.
eBL /api/fragments/{number}/match is 403-public (scout.md L35; REPRODUCE.md), so the offline TF-IDF
re-implementation of eBL's public ngram-matcher (cloned at commit e8918de, scout.md L41) is the
executable (d) baseline. p2 only requires the correct composition to be IN the top-10 — rank 0 satisfies it.

## Notes
- Frozen aligner params verified in code/search2.py L13: MATCH, MISMATCH, GAP, XMATCH, MIN_BLOCK = 3, -1, -2, 1, 6;
  all scored paths use align(..., band=0, min_block=MIN_BLOCK) (C kernel swalign.so).
- Two independent (b) runs (helper + own script) give identical results — deterministic aligner, no random
  state on the scored path. No non-determinism observed anywhere on the re-derived path.
- All quoted numbers are from command output / saved JSON, not memory.
- Discrepancies found: none.

context: subagent
pass: true
