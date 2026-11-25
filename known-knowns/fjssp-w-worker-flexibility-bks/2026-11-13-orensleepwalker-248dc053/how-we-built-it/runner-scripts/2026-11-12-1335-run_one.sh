#!/bin/sh
# One instance. Starts only before the frozen deadline and only when the machine has >= 2 GB of memory available (waits otherwise).
# Skips instances that already have an output file. Method = attempts/cpsat/code/solve.py, 300 s, 3 workers, seed 1, no warm start.
cd "$(dirname "$0")/../../.." || exit 1
F="$1"; DL=$(cat data/launch-deadline-epoch.txt); PY=../../.venv-optiwindnet/bin/python
[ "$(date +%s)" -lt "$DL" ] || exit 0
[ -f "attempts/cpsat/out/$F.json" ] && exit 0
while [ "$(awk '/MemAvailable/{print $2}' /proc/meminfo)" -lt 2000000 ]; do [ "$(date +%s)" -lt "$DL" ] || exit 0; sleep 15; done
[ "$(date +%s)" -lt "$DL" ] || exit 0
PYTHONDONTWRITEBYTECODE=1 nice -n 10 "$PY" attempts/cpsat/code/solve.py "data/repo/instances/Example_Instances_FJSSP-WF/$F.fjs" 300 3 1 "attempts/cpsat/out/$F.json" > "attempts/cpsat/out/$F.log" 2> "attempts/cpsat/out/$F.err"
echo $? > "attempts/cpsat/out/$F.exit"
