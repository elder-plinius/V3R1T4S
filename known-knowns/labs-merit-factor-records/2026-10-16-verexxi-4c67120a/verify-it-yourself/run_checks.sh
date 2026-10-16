#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (Python 3.8+, standard library only)
ok=1
python3 -I verify-it-yourself/check_labs.py || ok=0
second=$(python3 -I verify-it-yourself/check_energy.py "$(cat object/sequence.txt)")
echo "second checker (the run's check_energy.py): $second"
[ "$second" = "232 3032" ] || ok=0
if [ $ok = 1 ]; then echo PASS; else echo FAIL; fi
