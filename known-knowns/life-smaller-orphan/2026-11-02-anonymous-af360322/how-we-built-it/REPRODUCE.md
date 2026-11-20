# REPRODUCE (cheap steps; full 5x8 is ~7 h CPU per encoding)
gcc -O2 -o mcnf code/mcnf_route/mcnf.c ; gcc -O2 -o tcnfc code/tcnf_route/tcnfc.c ; gcc -O2 -o subseq code/tcnf_route/subseq.c
Life 5x5 mcnf unsplit: ./mcnf 5 5 2 8 12 > f.cnf; tools/cadical-cli -q --lrat=true --binary=false f.cnf f.lrat (exit 20 = UNSAT); tools/lrat-check f.cnf f.lrat
One 5x7 cube (~3-4 min, ~2 GB RSS): ./mcnf 5 7 3 8 12 4 <val> ; one 4x8 tcnfc cube is seconds (see tcnf NOTES for argument order).
Control: a rule with a known orphan width (data/mcnf_route/control_rules.txt) gives SAT at that width.
