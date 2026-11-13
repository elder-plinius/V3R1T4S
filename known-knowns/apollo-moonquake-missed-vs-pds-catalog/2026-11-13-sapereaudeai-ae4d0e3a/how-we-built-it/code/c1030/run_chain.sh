#!/bin/bash
# Claim run a100_1030: every step after N0, one process at a time (memory), from the run folder.
# Needs PY, APOLLO_WF (S14/S16 waveform folder), APOLLO_ATT (ATT folder), WFCACHE (folder with S12 + S14 1973 for the S12 check).
set -u
export V3_WORKERS=1
T=tools/code; NM=attempts/null-multiplicity; AT=attempts/attribution; GG=attempts/glitch-gates
stamp() { echo "$1 $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $AT/out/chain_times.txt; }
stamp start
$PY -I -B -W ignore $NM/code/n0_analyse.py $T/tools $NM/out/scan12_1973.jsonl ../out/lagtol_scan_1973.jsonl tools/data/catalog/levent.1008weber.csv 55,26 $NM/out/n0 > $NM/out/n0_stdout.txt 2>&1; stamp n0_analyse
$PY -I -W ignore $T/scripts/run_capped.py $T/tools/lagtol_candidates.py tools/frozen/nets25_1973.npz $NM/out/scan12_1973.jsonl tools/data/catalog tools/data/lit $NM/out/cand12 > $NM/out/cand12_stdout.txt 2>&1; stamp candidates
$PY -I -B $NM/code/m4_list.py $NM/out/cand12.json tools/data/lit $T/tools > $NM/out/m4_list.txt 2>&1; stamp m4
$PY -I -W ignore $T/scripts/att_check_1416.py $NM/out/cand12.json $NM/out/scan12_1973.jsonl 100 1973-10-30T02:25:51.509Z > $NM/out/r8_att_A100_1030.txt 2>&1; stamp r8
$PY -I -W ignore $T/scripts/glitch_check_1416.py tools/frozen/nets25_1973.npz $NM/out/cand12.json 100 1973-10-30T02:25:51.509Z > $GG/out/glitch_rule_A100_1030.txt 2>&1; stamp glitch_rule
NULLMAX=$($PY -I -c "import json; print(json.load(open('$NM/out/n0.json'))['N0']['best_control'])")
$PY -I -B -W ignore $GG/code/glitch_gates_1030.py $T/tools tools/frozen/nets25_1973_A100.npz tools/data/lit_acc $GG/out/glitch_gates_A100_1030.json $NULLMAX > $GG/out/glitch_gates_stdout.txt 2>&1; stamp glitch_gates
$PY -I -B -W ignore $AT/code/attrib_a1a2_1030.py $T/tools tools/frozen/nets25_1973.npz $NM/out/cand12_stdout.txt tools/data/catalog/nakamura_2005_dm_arrivals.csv $AT/out/a1a2_1030.json > $AT/out/a1a2_stdout.txt 2>&1; stamp a1a2
$PY -I -B -W ignore $AT/code/s16_mh2_response_1030.py $T/tools tools/data/catalog/levent.1008weber.csv $AT/out/s16_response_1973_1030.jsonl > $AT/out/s16_response_stdout.txt 2>&1; stamp a3_response
$PY -I -B $AT/code/a3_decide_1030.py $AT/out/s16_response_1973_1030.jsonl > $AT/out/a3_decision_1030.txt 2>&1; stamp a3_decide
$PY -I -B $T/fullwin/a4_phase.py $T/tools tools/data/catalog/levent.1008weber.csv > $AT/out/a4_phase.txt 2>&1; stamp a4
$PY -I -B -W ignore $AT/code/reverse_scan_1030.py $T/tools 1 365 $AT/out/reverse_scan_1973_1030.jsonl > $AT/out/reverse_scan_stdout.txt 2>&1; stamp reverse_scan
$PY -I -B $AT/code/a5_analyse_1030.py $AT/out/reverse_scan_1973_1030.jsonl tools/data/catalog/levent.1008weber.csv b > $AT/out/a5_variant_b_1030.txt 2>&1
$PY -I -B $AT/code/a5_analyse_1030.py $AT/out/reverse_scan_1973_1030.jsonl tools/data/catalog/levent.1008weber.csv a > $AT/out/a5_variant_a_1030.txt 2>&1; stamp a5
$PY -I -B -W ignore $AT/code/decphase_1030.py $T/tools tools/data/catalog/levent.1008weber.csv tools/frozen/nets25_1973_A100.npz $AT/out/decphase_1030.json > $AT/out/decphase_stdout.txt 2>&1; stamp d1
APOLLO_WF=$WFCACHE $PY -I -B -W ignore $AT/code/s12_third_1030.py $T/tools tools/frozen/nets25_1973_s12s14.npz $AT/out/s12_third_1030.json ../../lagtol-25nests-1973/out/lagtol_candidates_1973_stdout.txt > $AT/out/s12_third_stdout.txt 2>&1; stamp s12
stamp CHAIN_DONE
