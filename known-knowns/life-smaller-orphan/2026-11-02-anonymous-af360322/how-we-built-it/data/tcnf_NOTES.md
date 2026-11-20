# NOTES cube-and-conquer of tcnf (run 2026-10-27-1709)
Encoding: tcnf (runs/2026-10-26-1706/attempts/drat-route/code/tcnf.c, copied unchanged to code/tcnf.c). UNSAT <=> no h x w orphan.
Cube formula G(c,val) (code/tcnfc.c): tcnf clauses in the same order, minus column-c transfer clauses containing -E[c][v] with v != val,
plus h unit clauses fixing target column c to val. G is a subset of (tcnf + cube units), so G UNSAT => tcnf AND cube UNSAT.
The 2^h cubes on column c enumerate every value of that column, so all G(c,val) UNSAT => tcnf UNSAT => no orphan.
Subset check: code/subseq (G's clauses form an in-order subsequence of tcnf's lines, extra lines are only units on target vars):
 tcnfc 4 8 c4 v5 SUBSET_OK matched=1848910 units=4.
Solver/checker: CaDiCaL 3.0.1 (tools/cadical-zig/cadical-cli --lrat=true --binary=false), lrat-check from drat-trim repo
 (tools/drat-trim/lrat-check). LRAT checking is ~100x faster than drat-trim here (4x8 cube: 0.8 s vs drat-trim 167 s unsplit).
 lrat-check rejects planted bugs (output/controls_seg1.txt). A result file is written only for a finished verdict (cube.sh);
 killed cubes leave nothing and are rerun (resumable). Driver: code/drive.sh DEADLINE JOBS h:w:c[:BM:SM]; table: code/summary.sh.
Memory: 5x6 cube peak RSS ~2.0 GB (measured); 5x7/5x8 run with ulimit -v 3 GB, 3 workers.
Timing (seg 1): 4x8 cubes ~15-25 s; 5x4 ~3 s; 5x6 ~60 s; 5x7 ~215-245 s solve + ~6 s check. GUESS 5x8 ~15 min/cube -> ~8 h CPU total.
- 2026-10-27T14:37:18-04:00 seg2: 5x7 tcnf 32/32 cubes UNSAT+LRAT-verified; 5x8 0/32 (3 cubes killed at deadline >6 min); mcnf 5x6 bad_alloc at 2.5 GB.
- 2026-10-28T13:35:56-04:00 day2 seg1: 5x8 tcnf 12/32 cubes UNSAT+LRAT-verified (new v0,v8-v11); cube.sh gained MINLEFT start cutoff.
