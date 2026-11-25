#!/bin/sh
# Sequential 10-minute scan of the 14 remaining largest Behnke instances.
# Run 1 at a time for memory safety.
cd "$(dirname "$0")/../../.." || exit 1

date -u +%FT%TZ > data/launch-utc.txt
echo "$$ $(ps -o pgid= -p $$ | tr -d ' ')" > data/runner-pid.txt
PY=../../.venv-optiwindnet/bin/python

python3 -c "import json; [print(s['file']) for s in json.load(open('data/queue.json'))]" | while read -r F; do
  [ -z "$F" ] && continue
  if [ -f "attempts/cpsat/out/$F.json" ]; then
    echo "Skipping $F (already has output)"
    continue
  fi
  echo "$(date -u +%FT%TZ) Starting $F (600s, 3 workers, seed 1)"
  PYTHONDONTWRITEBYTECODE=1 nice -n 10 "$PY" attempts/cpsat/code/solve.py \
    "data/repo/instances/Example_Instances_FJSSP-WF/$F.fjs" 600 3 1 \
    "attempts/cpsat/out/$F.json" > "attempts/cpsat/out/$F.log" 2> "attempts/cpsat/out/$F.err"
  EX=$?
  echo "$EX" > "attempts/cpsat/out/$F.exit"
  echo "$(date -u +%FT%TZ) Finished $F with exit code $EX"
done

date -u +%FT%TZ > attempts/cpsat/out/DONE
echo "$(date -u +%FT%TZ) All 14 instances finished."
