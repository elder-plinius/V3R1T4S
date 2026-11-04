# NOTES enc2-mitm (second, independent encoding), run 2026-10-27-1709
Hypothesis: a meet-in-the-middle CNF (left forward superset F of reachable states at middle column m, right backward superset B, join clauses -F[m][s] v -B[m][s]) is UNSAT exactly when no h x w orphan exists, giving a second certificate written without tcnf.c code.
Validation: first-SAT widths match mitm.c on all 18 control (rule, h) cases (output/control_rules.txt); 4 SAT models brute-force confirmed as orphans (output/model_*.txt).
Life (output/life.tsv): UNSAT with LRAT verified (CaDiCaL + lrat-check) for h=3 w=3,5,8; h=4 w=4..8; h=5 w=2..6. 5x6 needs ~4 GB (bad_alloc at 2.5 GB).
Open: 5x7, 5x8 (likely need the cube option and several segments).
2026-10-29 15:00 ET: cube drivers mcube.sh/mdrive.sh/msummary.sh added; split validated (output/cube_controls.txt). 5x7 cube col 4: 13/32 UNSAT + LRAT verified (~3.6 min CPU each).
