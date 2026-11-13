#!/bin/sh
# Runs the preregistered pilot: 2 instances in parallel, 300 s, 3 workers, seed 1.
cd "$(dirname "$0")/../../.." || exit 1
PY=../../.venv-optiwindnet/bin/python
python3 -c "import json;[print(s['file']) for s in json.load(open('data/selected.json'))]" | PYTHONDONTWRITEBYTECODE=1 xargs -P 2 -I{} sh -c "nice -n 10 $PY attempts/cpsat/code/solve.py data/repo/instances/Example_Instances_FJSSP-WF/{}.fjs 300 3 1 attempts/cpsat/out/{}.json > attempts/cpsat/out/{}.log 2> attempts/cpsat/out/{}.err; echo \$? > attempts/cpsat/out/{}.exit"
date -u +%FT%TZ > attempts/cpsat/out/DONE
