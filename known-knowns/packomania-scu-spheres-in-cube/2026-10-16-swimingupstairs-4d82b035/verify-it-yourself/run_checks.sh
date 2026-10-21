#!/bin/sh
# run from the package folder: sh verify-it-yourself/run_checks.sh
# checks object/scu884.txt (N=884) and object/scu881.txt (N=881); last line PASS only if both pass
# step 1: each object file must match the sha256 listed for it in INDEX.csv
# step 2: exact geometry and margin to the table value (check_scu.py)
ok=1
python3 -c '
import csv, hashlib, sys
bad = 0
for row in csv.DictReader(open("INDEX.csv")):
    h = hashlib.sha256(open(row["file"], "rb").read()).hexdigest()
    same = h == row["sha256"]
    bad += not same
    print("sha256 %s %s" % (row["file"], "matches INDEX.csv" if same else "MISMATCH " + h))
sys.exit(1 if bad else 0)
' || ok=0
for job in "object/scu884.txt 884 0.055518673263" "object/scu881.txt 881 0.055610202148"; do
  set -- $job
  out=$(python3 verify-it-yourself/check_scu.py "$1" "$2" "$3") || ok=0
  echo "== $1"
  echo "$out"
  [ "$(echo "$out" | tail -n 1)" = "PASS" ] || ok=0
done
if [ "$ok" = 1 ]; then echo PASS; else echo FAIL; exit 1; fi
