ok: object-file sha256: all pins match
(b) re-derived top hit: /L/3/10/Standard Babylonian/- score 612 aligned 270 misfrac 0.0926 consec_lines_a 24 a_span (3, 26) b_span (56, 66)
ok: (b) top hit matches object (score/aligned/misfrac/consec/spans)
ok: (b) criterion bar (>=15 signs or >=3 lines, <=10% mismatch): met (270 signs, 24 lines)
(b/attested) attested_lines 11/24 attested_signs 128/281 (restoration pitfall: ~54% of block signs restored)
ok: (b/attested) split matches object (flagged, not a (b) sub-clause)
(c) K=1000000 N=40 real=612 control_max=46 n_ge=0 p_raw=1.0000e-06 p_bonf=4.0000e-05 p_bonf<1e-4=True beats_all=True
ok: (c) p_bonf < 1e-4 and real beats every control (frozen rule, N=|S|=40)
(d) TF-IDF top-10 re-derived: rank of /L/3/10/Standard Babylonian/- = 0 (in top-10: True)
(d) re-derived top-3: ['/L/3/10/Standard Babylonian/-', '/L/3/11/Standard Babylonian/-', '/Mag/2/13/Standard Babylonian/2']
ok: (d) re-derived TF-IDF top-10 matches object (claimed chapter rank 0; p2 requires top-10 presence)
(e) block 24 lines / 297 signs, threshold 118 -> distinct unrelated textIds: 1 [('L', 1, 1)] e_pass(<5): True
(e) hits: [('/L/1/1/Old Babylonian/I', 284, 0.028)]
ok: (e) block recurs in exactly 1 unrelated textId (< 5): not a formula
(a) joins==[]: True; museum-number chapter ms-link: False; naming: series name 'lexical' present (genre-level), number not -> partial -> pass_a=True (partial flagged)
ok: (a) unplaced (joins empty, no chapter manuscript link, no naming; genre-level 'lexical' partial flagged)
PASS
