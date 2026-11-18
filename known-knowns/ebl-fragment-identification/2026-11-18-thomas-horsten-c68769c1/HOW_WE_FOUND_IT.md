# How we found it (contributor text, unverified)

The run (V3R1T4S, standard effort: 1 target, 4 lenses) attacked the bank target
`ebl-fragment-identification`: find, by sign-sequence alignment, unplaced transliterated
eBL fragments that overlap a known composition, and propose the identification. The
scout confirmed the status is still open (eBL's identification is largely manual; the
in-platform lineToVec matcher is 403-public; the corpus keeps growing — 39,106
transliterated fragments at the 2026-11-18 re-check) and pinned the public corpus +
fragment dumps.

The alignment lens ran the frozen independent Smith-Waterman aligner (match +3 /
mismatch -1 / gap -2 / wildcard +1, min_block 6, deterministic tie-break) over the
11,635-fragment population (>=3 non-empty lines, max line >=15 signs, <=800 tokens)
against all 228 corpus chapters. 40 fragments passed the (b) bar (>=3 consecutive
lines or >=15 signs, <=10% mismatch); the top-40 by candidate hit-count form the
frozen null-search set S (|S| = 40). The (a) unplaced-fragment filter (no joins, no
chapter manuscript link, no naming) left 10; the (e) formula-recurrence filter
(the matched block must NOT recur in >=5 unrelated compositions) left exactly one:
BM.68403.

What failed first: the full-criterion win died at (d) — every (a)+(b)-passer's chapter
is in the eBL matcher top-10, so the full criterion's "NOT in top-10" fails; the
aligner's top pick VAT.8786 (score 799) died at (a) (its record names 'shuila to
Shamash 2'); the p1 candidates (Sm.1309, K.9496) fail (c) at K=400,000. The surviving
p2 claimant BM.68403 -> /L/3/10/Standard Babylonian/- (270 aligned signs, 9.26%
mismatch, 24 consecutive lines; TF-IDF rank 0) then had to clear the frozen null at the
claimant's K = 1,000,000 (the PREREG reachability clause: |S| = 40 > 39). It did:
0 of 1,000,000 shuffled-line controls reached 612 (control_max 46), p_bonf = 4.0e-05 <
1e-4, N = |S| = 40.

Three fresh-context skeptics (panel/) confirmed: REPRODUCE re-derived (b) two
independent ways (identical), verified the (c) p-rule and (e) recurrence; NOVELTY
re-checked eBL live (record joins [], no naming, genre-level 'lexical' only) and a
24-month literature/web search (no pre-2026-11-18 identification of the pair);
CRITERION judged the claim a genuine, non-subsumed p2 (full (d) and p1 both fail by
design). Two caveats carried in the confirmed scope: the matched block is ~45%
editorial restoration (attested-position pitfall — 11/24 lines, 128/281 signs
attested), and the cited-book pages (e.g. Civil 2010 p.155) are outside the claim
folder, so the "not identified in the publications" clause is judged on the record's
own titles/notes. Per the criterion, a confirmed p2 is a *candidate identification*,
accepted only by the eBL team or an Assyriologist.
