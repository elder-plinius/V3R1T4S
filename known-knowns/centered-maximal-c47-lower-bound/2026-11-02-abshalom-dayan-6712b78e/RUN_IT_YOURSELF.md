# Run it yourself

From this folder, with Python 3 (standard library only) and a C compiler:

    sh verify-it-yourself/run_checks.sh

It runs check_a.py (Python integers, prefix table, sweep along x) and check_b.c (128-bit integers, direct mass sums, sweep along y, separate code) at reach 6, and verify-it-yourself/third/vsweep.c (separate code, written from the definition, enumerates tight boxes up to the tail side S*, gives an inner and an outer union). Expected output, last lines:

    atoms=344 rectangles=188898 pieces=288355 area_num=10845095970898536899315634 (over 2^80) mass_num=5629639765 (over 2^30)
    value=1.711011823672
    strictly_above_bar True margin 0.008288090071964177
    pieces=270257 area_num=10845095970898536899315634 (over 2^80) mass_num=5629639765 (over 2^30)
    value=1.711011823672
    SWEEP V_lower 1.71101182367469 V_upper 1.71101182367477 ...
    PASS

About 2 minutes, 200 MB, on a laptop (check_b about 80 s).

Calibration, from this folder:

    python3 -I verify-it-yourself/check_a.py verify-it-yourself/tests/lin40.json 6      # value=1.685509993354; Lin's formula (2hV-4ab)/(1+w) = 1.68550999335553
    python3 -I verify-it-yourself/check_a.py verify-it-yourself/tests/tomar40.json 6    # value=1.702723733601; the float_ratio in Tomar's own file is 1.7027237336036, the published figure 1.7027237335
    python3 -I verify-it-yourself/tests/small_cases.py                        # hand-computed cases, PASS

verify-it-yourself/tests/lin40.json is Lin's measure from the page's formula rounded to 40 bits, verify-it-yourself/tests/tomar40.json Tomar's exact rational file rounded to 40 bits (verify-it-yourself/tests/mk_cal.py; Tomar's file is not shipped).

Pointwise test from the definition, finite blocks (tests only, not evidence; verify-it-yourself/tests/k56.c, verify-it-yourself/tests/dump_rects.py):

    python3 -I verify-it-yourself/tests/dump_rects.py object/measure.json 6 /path/L3.rects; cc -O2 -o /path/k56 verify-it-yourself/tests/k56.c; python3 -I verify-it-yourself/json2txt.py object/measure.json > /path/L3.txt
    /path/k56 /path/L3.txt 5 5 1 1000000 20261102 /path/L3.rects   # samples=1000000 M_ge_1=998365 in_S=998365 violations=0 missed=0
    /path/k56 /path/L3.txt 5 6 64 1000000 1064                     # N=64 ratio=1.695862 se=0.000636

Other N in the same mode: N=1 1.100660, 2 1.319758, 4 1.493117, 8 1.597918, 16 1.653282, 32 1.681112 (each 1,000,000 samples), 128 1.703585 (se 0.000184), 256 1.707266 (se 0.000131) (each 6,000,000 samples); the gap to 1.71101 halves as N doubles.

Independent quadtree enclosure (verify-it-yourself/third/vtree.c, from the definition, no rectangle enumeration): depth 25, side 2^-23, [1.7110114873, 1.7110120881], about 4 minutes; depth 26, side 2^-24, [1.7110116654, 1.7110119658], about 8 minutes. Sampling (verify-it-yourself/third/vsample.c): 1,000,000 points, V_est 1.71100177, SE 0.00006947.

Rebuild (floats, search only, never evidence): object/family/FAMILY.md gives the commands. object/family/famgen.py regenerates object/measure.json from object/family/L3.par atom for atom:

    python3 -I object/family/famgen.py object/family/L3.par /path/out.json 30

Only object/measure.json is claimed.
