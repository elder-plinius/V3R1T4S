#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (needs python3, curl and sha256sum; about 70 KB of downloads)
# Downloads the Hamburg instance and the posted best timetable from the TimPassLib site, checks their sha256, requires the evaluator
# to reproduce 140850920 for the posted best, then requires object/Timetable.csv to be feasible with total 140833625 (< 140850920). Last line: PASS or FAIL.
set -u
B=https://timpasslib.aalto.fi/data
T=$(mktemp -d) || { echo FAIL; exit 1; }
trap 'rm -rf "$T"' EXIT
bad=0
[ "$(sha256sum object/Timetable.csv | cut -d' ' -f1)" = "fb09dae618a0397f49efc6f8d5a64e5195fa2e424edce26bd8fcb744f8d9cde3" ] || { echo "object sha256 mismatch"; bad=1; }
curl -sS -A 'V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)' -o "$T/inst.zip" "$B/Hamburg.zip" || bad=1
curl -sS -A 'V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)' -o "$T/posted.zip" "$B/Hamburg/140850920_Timetable.zip" || bad=1
[ "$(sha256sum "$T/inst.zip" | cut -d' ' -f1)" = "9ac9bf147b92f86f3fec3dc5af0b7c8027b3e18c5d76f8bd99b0a6a008969a2d" ] || { echo "instance zip sha256 mismatch"; bad=1; }
[ "$(sha256sum "$T/posted.zip" | cut -d' ' -f1)" = "2d8a43e908f9135940a09d02602e8008f4d3d404488941ae93eeae18e49897a3" ] || { echo "posted best zip sha256 mismatch"; bad=1; }
python3 -I -c "
import zipfile,sys
for z,d,names in (('$T/inst.zip','$T/inst',['Config.csv','Events.csv','Activities.csv','OD.csv']),('$T/posted.zip','$T/posted',['Hamburg-140850920-Timetable.csv'])):
    zf=zipfile.ZipFile(z)
    for n in names:
        import os; os.makedirs(d,exist_ok=True); open(d+'/'+n,'wb').write(zf.read(n))
" || bad=1
a=$(python3 -I verify-it-yourself/evaluate.py "$T/inst" "$T/posted/Hamburg-140850920-Timetable.csv")
b=$(python3 -I verify-it-yourself/evaluate.py "$T/inst" object/Timetable.csv)
echo "posted best: $a"
echo "object:      $b"
echo "$a" | grep -q '"feasible": true, "infeasible_activities": 0, "total": 140850920,' || { echo "posted best not reproduced as 140850920"; bad=1; }
echo "$b" | grep -q '"feasible": true, "infeasible_activities": 0, "total": 140833625,' || { echo "object is not feasible with total 140833625"; bad=1; }
if [ "$bad" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
