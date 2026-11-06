# PREREG (frozen at file write; see PREREG.sha256 for time; local 2026-11-03 14:35 EST)
run: 2026-11-03-1435-dnaedit93  (one-cell sibling claim + bounded push search; layout mirrors runs 1320-dnaedit94 / 1310-dnaedit83)
target: edit-metric-dna-codes-gc
cell: (n,d) = (9,3), w = floor(9/2) = 4 (constraint set E_4^{RC,GC}(n,d,w) of Sun 2010 M.Sc. thesis, Table 7.1)

Contention check (14:34 EST): grep of runs/*/PREREG.md, runs/*/target.md, panel_requests/, outbox/, LOG.md for "(9,3)" / "n9_d3" / "dnaedit93"
finds only "not claimed here"/"not in scope" lines (1152-dnaedit74, 1207-dnaedit95, 1217-dnaedit84, 1235-dnaedit73, 1310-dnaedit83, 1320-dnaedit94,
their outbox packages) and the 1539 carrier's sibling list (claim/extra, not panelled per cell). No run dir named *dnaedit93* exists; no running
dnae process for n=9 d=3 (ps). (8,3) belongs to run 1310-dnaedit83, (9,4) to run 1320-dnaedit94 - NOT touched.

Disclosure: a 1011-word candidate already exists (runs/2026-11-03-1539-dnaedit/claim/extra/r1_n9_d3_G0_k1011.txt,
sha256 12d3e1454d78d554498bfb6190232a694ff3834f2eecf43f5c3d62c9a7315cd5, from 1539 dnae.c G=0 seed 7; 1539 search-engineer report:
"stuck at 1011 from t=2.7 s to 1500 s"). This run was opened knowing that. No claim/ or data/ folder exists in this run at the time of writing.
The bar value 939 is from 1539 target.md / 1320 sources transcription and has not yet been re-read live in this run.

planned method:
 1. byte-copy the 1011 object; verify with check_dna.py + check2.c + check3.py + check4.py (byte copies from run 1320-dnaedit94 claim/checkers).
 2. bounded push search for >= 1012: dnae.c (byte copy, sha256 b4a39bfb...) modes G=0,1,2 with longer restart lengths and new seeds
    (<= 3 concurrent, nice -n 19, timeout-capped), wall-clock <= 30 min total for the push.
 3. Decision rule fixed now: the claimed object is the LARGEST code that all four checkers report VALID at the end of the budget
    (1011 if push finds nothing larger). Seeds/commands logged in data/.
criterion (verbatim from bank): A codeword list for a parameter cell listed in https://brocku.scholaris.ca/items/43d5f016-9190-4ec2-8066-81f3860f672b (thesis tables) or https://arxiv.org/abs/1505.06262, checked for length, alphabet, exact constraint set as defined by that source, all-pairs Levenshtein distance >= d, in a cell that its source does not mark as optimal (the claimant must show this, since many small cells are already exhaustively solved), with size strictly larger than the published lower bound (sources re-fetched live immediately before claiming) and than any later value found by novelty search.
statistic / checker: VALID iff alphabet ACGT, length 9, distinct words, GC weight exactly 4, d_edit(x, rc(x)) >= 3 for every x,
d_edit(x,y) >= 3 and d_edit(x, rc(y)) >= 3 for every pair x != y (Levenshtein with substitutions, insertions, deletions).
success threshold: size > 939 (Sun Table 7.1 row 9, per prior transcription) - must be re-read live in this run with marks; if live value >= claimed
size or marked exact/optimal, claim dies; and > any later GC+RC edit value found by novelty search. Ties fail.
scope: cell (9,3) only. Other cells not claimed.
null_test: not needed (explicit object, deterministic exhaustive checkers, fixed table value).
