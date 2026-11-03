# PREREG (frozen 2026-10-27T17:15Z, before any output)
Criterion: see target.md (verbatim). Today's sub-goal is a certificate for p1-style claim "no 5 x w orphan, w <= 8" (w<=7 already in literature; 5x8 per human check not found).
Judge: for each (h,w) in {(5,4),(5,7),(5,8)}: 32 cube formulas G(c,val), c = middle column; each solved by kissat or CaDiCaL with a
 DRAT or LRAT proof, proof checked by drat-trim or lrat-check (s VERIFIED / c VERIFIED). Cube table: attempts/cube5x8/output/cubes_h{h}w{w}.tsv.
Statistic: number of cubes UNSAT with proof checked, out of 32, per size; plus a subset check (every clause of G is a clause of tcnf or a cube unit).
Thresholds: size certified iff 32/32 cubes UNSAT AND proof VERIFIED AND subset check passes. Any SAT cube: model checked by
 an independent simulator; a confirmed SAT at w<=8 contradicts mitm3/o5b and is reported as a PROBLEM to resolve, not a win.
Controls: validate the split on solved sizes first: h=4 w=8 and h=5 w=6 (cubes must all be UNSAT, agreeing with the unsplit result),
 and control rule masks where the unsplit first-SAT width is known (cube results must contain a SAT cube exactly when unsplit is SAT).
null_test: not needed because the verdict is a deterministic proof-checked UNSAT/SAT per cube, not a statistic; controls above are the falsification test.
Second encoding (later segments): independently written, validated on controls, run on sizes it can reach.
