#!/bin/sh
# The 3-hour scan. Queue order, 2 instances in parallel. No new instance starts 170 minutes after launch (the deadline is written at launch).
# Launch once with:  setsid nohup sh attempts/cpsat/code/run_scan.sh > attempts/cpsat/out/runner.log 2>&1 < /dev/null &
# After an unexpected stop, relaunch the same command with RESUME=1 in front: the original deadline is kept and finished instances are skipped.
cd "$(dirname "$0")/../../.." || exit 1
if [ -f data/launch-utc.txt ]; then
  if [ -z "$RESUME" ]; then echo "already launched; relaunch only with RESUME=1"; exit 1; fi
  echo "$(date -u +%FT%TZ) resumed" >> data/resume-log.txt
else
  date -u +%FT%TZ > data/launch-utc.txt; echo $(( $(date +%s) + 10200 )) > data/launch-deadline-epoch.txt
fi
echo "$$ $(ps -o pgid= -p $$ | tr -d ' ')" > data/runner-pid.txt
python3 -c "import json;[print(s['file']) for s in json.load(open('data/queue.json'))]" | xargs -P 2 -n 1 sh attempts/cpsat/code/run_one.sh
date -u +%FT%TZ > attempts/cpsat/out/DONE
