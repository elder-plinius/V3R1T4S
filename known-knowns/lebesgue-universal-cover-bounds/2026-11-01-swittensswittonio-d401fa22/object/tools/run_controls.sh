#!/bin/bash
# runs the interval verifier (1 thread) on the author's valid control cert and on 14 tampered copies; expected: valid + accept_m_K_* VERIFIED, all others rejected/failed
cd "$(dirname "$0")/.."
mkdir -p outputs/controls; : > outputs/controls_summary.txt
BIN=work/run_bin/LebVerify.dll
DN=dotnet
for f in work/certB_test.bin work/tamper/*.bin; do
  n=$(basename $f .bin)
  "$DN" $BIN verify $f --threads 1 --claim none > outputs/controls/$n.txt 2>&1; ec=$?
  echo "$n exit=$ec : $(grep -E 'RESULT|REJECTED' outputs/controls/$n.txt | tr '\n' ' ' | cut -c1-200)" >> outputs/controls_summary.txt
done
echo DONE >> outputs/controls_summary.txt
