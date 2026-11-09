#!/bin/sh
# The PREREG.v2 one look, with PREREG.v3 A-D and the PREREG.v5 common-offset rule. Runs only frozen code
# (runs/2026-10-16-1714 and runs/2026-10-16-2357); this script only calls it, in the order the preregs list.
# usage (from the workspace root): sh runs/2026-10-17-2357/attempts/timeline-aligner/code/one_look.sh <python> <outdir>
set -u
PY="$1"; OUT="$2"
A=runs/2026-10-16-1714/attempts
TA=$A/timeline-aligner/code
EP=$A/exact-polynomial
MC=$A/timeline-aligner/mc
TRI=runs/2026-10-16-2357/attempts/evaluator-first/out/triangular_test_output.txt
CO=runs/2026-10-16-2357/attempts/timeline-aligner/code/common_offset.py
KAG=$($PY -c "import math; print('%.14f' % (1 - 2 * math.sin(math.pi / 18)))")
SQ=0.59274605079210
echo "one look started $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "== 1. kagome site, 60-block primary fit (PREREG.v2 kill rule: |p_MC - exact| <= 3 sigma_MC)"
$PY $TA/fss_mc.py $MC/kagome_site --exact $KAG | tee $OUT/fss_kagome_site_60.txt
echo "== 2. square site (PREREG.v3 A: |p_MC - 0.59274605079210| <= 3 sigma_MC)"
$PY $TA/fss_mc.py $MC/square_site --exact $SQ | tee $OUT/fss_square_site_60.txt
echo "== 3. PREREG.v5 addition 2, common offset (kagome, square, triangular L = 16, 32, 64)"
$PY $CO $OUT/fss_kagome_site_60.txt $OUT/fss_square_site_60.txt $TRI | tee $OUT/common_offset.txt
echo "== 4. (3^3,4^2) site (PREREG.v3 B: rule (a) form against the TM ST site series; table = Suding and Ziff 0.550213(3))"
$PY $TA/agreement.py $EP/out/st_site_series.txt $MC/st_site 0.550213 3e-6 | tee $OUT/agreement_st_site_60.txt
echo "== 5. #23 site: rules (a) and (b), TM with every n present (PREREG.v3 D), table 0.5720(2)"
$PY $TA/agreement.py $EP/out/r23_site_series.txt $MC/r23_site 0.5720 2e-4 | tee $OUT/agreement_r23_site_60.txt
echo "== 6. #23 site check torus 2048 x 512 (PREREG.v3 C, not in the fit)"
$PY $TA/analyze_mc.py "$MC/r23_site_check/*.hist" | tee $OUT/check_torus.txt
echo "== 7. #23 bond: 60-block primary fit; (c) MC part against the table 0.45844622(40); TM-MC bond check"
$PY $TA/agreement.py $EP/out/r23_bond_series.txt $MC/r23_bond 0.45844622 4e-7 | tee $OUT/agreement_r23_bond_60.txt
echo "one look finished $(date -u +%Y-%m-%dT%H:%M:%SZ)"
