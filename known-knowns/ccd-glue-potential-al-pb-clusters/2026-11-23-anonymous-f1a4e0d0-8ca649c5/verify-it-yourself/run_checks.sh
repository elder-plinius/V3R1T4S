#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (last line PASS or FAIL)
# Fetches the two third-party inputs once each (not redistributed here) and checks their sha256 first.
set -u
PY=${V3R1T4S_PYTHON:-python3}
C=verify-it-yourself/cache; mkdir -p "$C"
UA="V3R1T4S-agent (verify-it-yourself)"
get() { [ -f "$C/$2" ] || curl -sS -f -L -A "$UA" -o "$C/$2" "$1" || { echo "fetch failed: $1"; echo FAIL; exit 1; }; }
get https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/lead/points/all.tar Pb_all.tar
get "http://web.archive.org/web/20170523125240id_/http://www.fisica.uniud.it:80/~ercolessi/potentials/Pb/lead.f" lead.f
( cd "$C" && $PY -c "
import hashlib,sys
want={'Pb_all.tar':'dfb0e9720734e2943b34cf6bdce6971546b44071f9df87b021482cd8fb46cbeb','lead.f':'9f016265721a7910a79ccbb5b35a5deffb26dd014779b4ceb9968756f1856cae'}
bad=[f for f,h in want.items() if hashlib.sha256(open(f,'rb').read()).hexdigest()!=h]
print('input sha256 mismatch:',bad) if bad else print('inputs sha256 ok'); sys.exit(1 if bad else 0)" ) || { echo FAIL; exit 1; }
mkdir -p "$C/Pb_points"; tar -xf "$C/Pb_all.tar" -C "$C/Pb_points"
$PY verify-it-yourself/check.py "$C" .
