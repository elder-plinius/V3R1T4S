# CLAIM (run 2026-10-27-1709, target life-smaller-orphan, proposed partial win p1)
Conway's Game of Life (B3/S23; in the code rule masks BM=8 (birth on 3), SM=12 (survive on 2,3)).
Claim: there is NO orphan (Garden-of-Eden pattern) of size 5 x w for any w <= 8. Equivalently every 5 x w target pattern, w <= 8,
has a predecessor on the (5+2) x (w+2) grid whose next generation equals the target on the 5 x w box (cells outside the box unconstrained).
The new size is 5 x 8 (area 40). Boxes with both sides <= 7 (so 5 x 7) are covered in the literature (Beer 2023, no orphan in 7x7, as recorded
in NOVELTY_RECORD.md); height <= 4 is Wade 2023. 5x8 and smaller are far below Eker's 12x8 record, so this is NOT a smaller orphan (no main win);
it is offered only as p1: "a DRAT/LRAT-certified proof (two independent encodings) that no orphan exists in some h x w box with h >= 5 not already ruled out".
Evidence for 5 x 8:
- Encoding A (tcnf, column-transfer, code/tcnf_route/tcnf.c, cubes tcnfc.c): 32 cubes (5 target cells of column 4 fixed to each of 32 values), all UNSAT
  under CaDiCaL with LRAT proofs, all checked "c VERIFIED" by lrat-check (drat-trim repo). Result rows: data/tcnf_route/cubes/h5w8r8_12/c4v*.res.
  Coverage: cubes = full formula + 5 unit clauses on the column-4 target vars; subset check SUBSET_OK (data/tcnf_route/subset_day3_seg2.txt).
- Encoding B (mcnf, meet-in-the-middle, code/mcnf_route/mcnf.c, written without tcnf code): 32 cubes on column 4, all UNSAT + LRAT "c VERIFIED".
  Rows: data/mcnf_route/cubes/h5w8r8_12/c4v*.res. Subset check SUBSET_OK for v0, v17, v31 (data/mcnf_route/subset_day6_seg3.txt).
- Smaller widths: tcnf 5x4, 5x6, 5x7 cubed 32/32 LRAT verified; 5x2,5x3,5x5 DRAT verified unsplit (data/prior_run_2026-10-26-1706).
  mcnf 5x2..5x6 unsplit LRAT verified (data/mcnf_route/life.tsv), 5x7 cubed 32/32 (data/mcnf_route/cubes/h5w7r8_12).
- Controls: other rule masks with known first-SAT (orphan-exists) widths reproduce them; SAT models are brute-force confirmed orphans by an
  independent backtracking checker (brutepred.c); lrat-check rejects planted bugs; split validated on solved sizes (4x8, 5x6, 4x6).
- Numerical (not certificates): mitm3.c, o5b and o5 (home PC) find no 5 x w orphan for w <= 8 (o5: w <= 10).
Not done: kissat was NOT run on the 5x8 formulas (criterion (2) of the full win names CaDiCaL and kissat; p1 asks for drat-trim/cake_lpr-checked proofs).
Proof files were deleted after checking (hundreds of MB each); a reviewer can regenerate any cube and re-solve/check it.
