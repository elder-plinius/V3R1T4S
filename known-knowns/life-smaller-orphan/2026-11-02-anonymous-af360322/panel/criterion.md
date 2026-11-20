# CRITERION skeptic verdict: no 5 x w Life orphan for w <= 8 (new size 5x8), target life-smaller-orphan (partial win p1)
context: fresh headless Grok Build CLI session (grok --prompt-file), started with no prior conversation in a copy of claim/

## what you read
- claim/TARGET_CRITERION.md (binding p1), CLAIM.md, METHOD.md, REPRODUCE.md, NOVELTY_RECORD.md
- Encoders: code/tcnf_route/tcnf.c, tcnfc.c, subseq.c, brutepred.c, cube.sh, summary.sh
- Encoders: code/mcnf_route/mcnf.c, mcube.sh, msummary.sh, life.sh, ctl.sh
- Result rows: data/tcnf_route/cubes/h5w8r8_12/c4v0..31.res (and h5w4, h5w6, h5w7, controls); data/mcnf_route/cubes/h5w8r8_12 and h5w7; data/mcnf_route/life.tsv, subset_*.txt, control_rules.txt, cube_controls.txt; data/tcnf_route/subset_day3_seg2.txt, controls_seg1.txt; data/prior_run_2026-10-26-1706/life_h5_w*.txt
- tools/lrat-check, cadical-cli, kissat (binaries/strings only)
- Public: github.com/marijnheule/drat-trim/lrat-check.c (usage string and `c VERIFIED` match the bundled binary)

## what you ran
Compiled from claim/ sources (nice -n 19, timeout 400, ulimit -v 900000) and ran independent checks; CNF/LRAT scratch files deleted after.

Life neighborhood (h=1..5, all 2,396,672 predecessor triples, B3/S23): tcnf `col`, mcnf `nextcol`, and a third implementation: mismatches=0 OK.

Exhaustive predecessor search:
- Life 2x2: 0 orphans; Life 2x3: 0 orphans; B17/S1 h=2 w=2 and w=3: 0 orphans; B64/S1 h=2 w=2: 1 orphan (all-live).
- Rebuilt encoders: both tcnf and mcnf CaDiCaL-exit 20 on those UNSAT cases, exit 10 on B64/S1 2x2. SAT models `oo/oo`, backtracking NO_PREDECESSOR.

Rebuilt LRAT pipeline (claim/tools/cadical-cli --lrat=true --binary=false + claim/tools/lrat-check):
- mcnf 3x3 and tcnf 3x3: cadical_exit=20, `c VERIFIED`
- mcnf 4x4 and tcnf 4x4 (unsplit, 1,052,736 clauses): cadical_exit=20, `c VERIFIED`
- truncated proof: `c NOT VERIFIED`, exit 1
- cadical-cli version 3.0.1; lrat-check usage `FILE1.cnf FILE2.lrat [optional: FILE3.drat]`

Cube units / cover / subseq:
- tcnf 5x8 column 4 vars 4,12,20,28,36 (row-major); mcnf column 4 vars 16..20 (column-major). mcnf v0/v17/v31 units match data/mcnf_route/subset_day6_seg3.txt exactly.
- 32 distinct unit-tuples, partition of {0,1}^5.
- Empirical tcnfc 3x4 c=2 v=5 units `2 0 / -6 0 / 10 0`; mcnf `4 0 / -5 0 / 6 0`.
- subseq 4x4: tcnfc SUBSET_OK matched=800270 units=4; mcnf SUBSET_OK matched=1052736 units=4 (full formula plus units).

Parsed all 5x8 `.res` files (32+32): every val 0..31 present once, `result=20`, `check=c_VERIFIED`, `cube_col=4`, `rule=8/12`. mcnf clause count 16793861 = unsplit 16793856 + 5 units, matching the encoder. tcnf clause counts vary by val as expected from dropped transfer clauses. tcnf 5x4/5x6/5x7 and mcnf 5x7 also 32/32 covered.

Stored SAT control models: tcnf B17/S1 2x5 `ooooo/ooo.o` NO_PREDECESSOR; mcnf same cube `ooooo/o.ooo` NO_PREDECESSOR under column-major indexing.

## findings
UNSAT is equivalent to "no h x w orphan" in both encoders. Predecessor is the (h+2)x(w+2) window; extra rows/columns are free; each target cell uses its 3x3 in that window. BM=8 and SM=12 are B3/S23 (birth on 3, survive on 2 and 3). Both encodings force a one-way *superset* of reachable predecessor-column pairs (Y/E forced by "column equals v") and then forbid a meeting: tcnf asserts every pair at column w is unreachable; mcnf joins a left-forward superset and a right-backward superset at column m=w/2 and asserts empty intersection. SAT iff some target has empty true reachable set (an orphan); UNSAT iff every target has a predecessor.

The two encodings are independent: different variable order (row-major T vs column-major X), different clause shape (forward-only transfer vs meet-in-the-middle), separately written. They share only the Life neighborhood specification, and that specification was cross-checked.

The 32-cube split is a complete cover of target column 4 (5 bits). tcnfc is a subset of (tcnf + units) because it *drops* transfer clauses whose E-literal is not the cube value; G UNSAT implies tcnf∧units UNSAT, which is the sound direction. mcnf cubes add units only, no drops. Every 5x8 `.res` file has `c_VERIFIED`.

lrat-check is the LRAT checker from the drat-trim repository (Heule), not the `drat-trim` DRAT binary and not cake_lpr. For p1 I accept LRAT proofs checked by this binary as "checked by drat-trim": p1 asks for a DRAT/LRAT-certified proof checked by drat-trim or cake_lpr, the proofs are LRAT, and this is the LRAT checker shipped in that repo. kissat was not run; that is required for full criterion (2), not for p1. The novelty/human LifeWiki gate is out of this role.

5x8 (area 40, h=5) is the p1 box; no 5x8 orphan also implies no 5 x w orphan for w<8, because a smaller orphan would remain an orphan inside a 5x8 window. Smaller-width certificates (mcnf unsplit 5x2..5x6 LRAT; tcnf unsplit DRAT 5x2,5x3,5x5; cubes 5x4/5x6/5x7) agree.

## caveats
- 5x8 proof files were deleted after the original runs (hundreds of MB each). This review re-checked the pipeline on 3x3 and 4x4 unsplit, not a 5x8 cube (~7 h CPU / ~2 GB, over this role's budget). The 5x8 `.res` logs are consistent with the rebuilt encoders (clause counts, unit vars, driver writes a `.res` only after `c VERIFIED`).
- tcnf 5x8 subset checks exist only for v0, v13, v31; mcnf for v0, v17, v31. The generators are uniform in `val`.
- Full-win sanity (100 random non-orphans, Eker 8x12 one-cell flip) and kissat were not required for p1 and were not re-run here.
- prior_run 5x4 unsplit DRAT timed out; that width is covered by 32 tcnf cubes instead.

confirmed_scope: p1 holds for Life B3/S23 on the 5x8 box (hence 5 x w, w<=8): two independent CNF encodings of predecessor existence, each 32/32 column-4 cubes UNSAT with LRAT `c VERIFIED` by drat-trim's lrat-check, encodings and cube cover checked in source plus cheap rebuilt proofs.
scope: verified encoding soundness (UNSAT <=> no (h+2)x(w+2) predecessor of an h x w target, B3/S23 masks 8/12), independence, 32-cube cover and all 5x8 `.res` `c_VERIFIED` rows, and rebuilt CaDiCaL+lrat-check on 3x3/4x4 plus SAT/UNSAT polarity on tiny brute-forced sizes; did not re-solve 5x8, run kissat, or perform the human LifeWiki novelty gate.
pass: true
