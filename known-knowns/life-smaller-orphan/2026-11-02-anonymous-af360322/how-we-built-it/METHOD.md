# METHOD
Predecessor grid (h+2) x (w+2), columns are (h+2)-bit words. Target column t (1..w) is a function of predecessor columns t-1,t,t+1.
tcnf (encoding A): see data/tcnf_route/NOTES.md and code/tcnf_route/tcnf.c; a transfer encoding of the set of reachable predecessor-column pairs;
 the formula is SAT iff some target has no predecessor (UNSAT = no orphan). tcnfc.c = same clauses + units on the target column (cube).
mcnf (encoding B): header comment of code/mcnf_route/mcnf.c: left forward superset F, right backward superset B, join -F[m][s] v -B[m][s].
 Usage: mcnf h w m BM SM [cubecol cubeval]; cube runs used m=w/2=4, cubecol=4. Target vars X(i,t) = 1+(t-1)h+i, so column 4 is vars 16..20 for h=5.
Cube driver: code/*/cube.sh, mcube.sh: generate CNF, cadical-cli -q --lrat=true --binary=false f.cnf f.lrat, then lrat-check f.cnf f.lrat;
 a result file is written only after "c VERIFIED". summary.sh / msummary.sh report ALL_UNSAT_VERIFIED(covered) only if all 2^h values are present.
Coverage argument: every target assignment fixes column 4 to exactly one of the 32 values, so if every cube (full formula + those 5 units) is UNSAT,
 the full formula is UNSAT. subseq.c checks the cube file = full file's clauses in order + unit clauses on target vars only.
Tools: claim/tools/cadical-cli (CaDiCaL), lrat-check (from drat-trim), kissat.
