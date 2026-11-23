"""Run bh.py (this folder) over cells lo..hi with a thread pool of subprocesses; one JSON line per cell (checkpoint).
Usage: driver.py metal lo hi seconds workers seedbase"""
import sys, os, json, subprocess
from concurrent.futures import ThreadPoolExecutor
here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, '..', 'output'); os.makedirs(out, exist_ok=True)
metal, lo, hi, sec, workers, sb = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5]), int(sys.argv[6])
res = os.path.join(out, f'results_{metal}.jsonl'); done = set()
if os.path.exists(res): done = {json.loads(l)['N'] for l in open(res)}
def run(n):
    p = subprocess.run([sys.executable, os.path.join(here, 'bh.py'), metal, str(n), sec, str(sb + n), out], capture_output=True, text=True)
    line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else json.dumps({'N': n, 'error': p.stderr[-300:]})
    with open(res, 'a') as f: f.write(line + '\n')
    return line
with ThreadPoolExecutor(workers) as ex:
    for l in ex.map(run, [n for n in range(hi, lo-1, -1) if n not in done]): print(l, flush=True)
