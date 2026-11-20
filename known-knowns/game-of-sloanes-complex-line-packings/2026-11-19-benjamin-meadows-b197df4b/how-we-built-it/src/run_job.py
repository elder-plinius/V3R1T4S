#!/usr/bin/env python3
"""Run the search job in job.json with gos_kernel.py, the way the original run did (one job, 4 worker slots).

usage: python3 run_job.py [BUDGET_SECONDS]     (default: the job's own budget, 20070 s)
Writes out/best/<cell>_j<k>.txt, out/improved/, out/progress.jsonl and out/results.tsv. The search stops on a
wall-clock budget and its polish steps have time limits, so a rerun on other hardware follows a different
path; it is not expected to reproduce the object digit for digit (see ../../HOW_WE_FOUND_IT.md).
"""
import base64, gzip, json, os, subprocess, sys

jobs = json.load(open('job.json'))
if len(sys.argv) > 1:
    for j in jobs:
        j['budget'] = float(sys.argv[1])
hours = max(j['budget'] for j in jobs) / 3600 + 0.25
src = open('gos_kernel.py').read()
src = src.replace('__SHARD__', 'rerun').replace('__HOURS__', str(hours))
src = src.replace('__DATA__', base64.b64encode(gzip.compress(json.dumps(jobs).encode(), 9)).decode())
open('kernel_job.py', 'w').write(src)
os.makedirs('out', exist_ok=True)
env = dict(os.environ, GOS_OUT='out')
sys.exit(subprocess.call([sys.executable, 'kernel_job.py'], env=env))
