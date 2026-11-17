"""Batch runner for the TimPassLib search jobs in jobs.json (frozen). Sequential, resumable, hard time caps, every result verified by the independent evaluator.
Usage (from the scan folder):  python3 -I code/run_batch.py [jobs.json] [--dir batch]      -> runs jobs, then writes <dir>/RESULTS.md and results.csv
                               python3 -I code/run_batch.py [jobs.json] [--dir batch] --report   -> only rewrites the report
A job is skipped if <dir>/<id>/result.json exists. The runner stops itself after 3 consecutive jobs without a result file."""
import os, sys, json, time, subprocess, csv
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE)
sys.path.insert(0, 'code'); import evaluate_independent as ev
PY = os.path.join(HERE, '../../.venv-optiwindnet/bin/python')
INST = '../2026-11-14-timpasslib-scout/data/inst/'
args = [a for a in sys.argv[1:] if not a.startswith('--')]; JOBS = args[0] if args else 'jobs.json'
DIR = sys.argv[sys.argv.index('--dir') + 1] if '--dir' in sys.argv else 'batch'
if DIR in JOBS: args = [a for a in args if a != DIR]
jobs = json.load(open(JOBS))['jobs']; record = {r['instance']: r['listed_total'] for r in json.load(open('starts/manifest.json')) if r['tag'] == 'record_ramos'}
os.makedirs(DIR, exist_ok=True)
def run():
    open(f'{DIR}/run.pid', 'w').write(f'pid {os.getpid()} pgid {os.getpgid(0)} started {time.strftime("%Y-%m-%d %H:%M:%S")}\n'); fails = 0
    for j in jobs:
        out = f"{DIR}/{j['id']}"; res = f'{out}/result.json'
        if os.path.exists(res): continue
        os.makedirs(out, exist_ok=True); eng = 'joint_lns.py' if j['engine'] == 'joint' else 'hybrid_lns.py'
        extra = ['6', '15', '120', '3'] if j['engine'] == 'joint' else ['6', '15', '30', '3']
        cmd = [PY, '-I', f'code/{eng}', INST + j['instance'], j['start'], out, str(j['seconds']), str(j['seed'])] + extra
        t0 = time.time()
        try: p = subprocess.run(cmd, capture_output=True, text=True, timeout=j['seconds'] + 240, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        except subprocess.TimeoutExpired: p = subprocess.CompletedProcess(cmd, 124, '', 'hard timeout')
        open(f'{out}/stdout.txt', 'w').write(p.stdout + '\n--- stderr\n' + p.stderr[-3000:])
        best = f'{out}/best.csv' if os.path.exists(f'{out}/best.csv') else None
        r = dict(job=j['id'], instance=j['instance'], engine=j['engine'], start=j['start'], seed=j['seed'], seconds=j['seconds'], returncode=p.returncode, wall=round(time.time() - t0))
        try: r['summary'] = json.loads(p.stdout.strip().splitlines()[-1])
        except Exception: r['error'] = (p.stdout + p.stderr)[-300:]
        if best:
            c = ev.evaluate(INST + j['instance'], best); r.update(file=best, indep_feasible=c['feasible'], indep_total=c.get('total'))
        elif 'summary' in r: r.update(file=None, indep_total=r['summary'].get('start_total'), indep_feasible=True, unchanged=True)
        if 'summary' in r or best: fails = 0; json.dump(r, open(res, 'w'))
        else:
            fails += 1; json.dump(dict(r, status='NO_RESULT'), open(res, 'w'))
            if fails >= 3: print('STOPPED: 3 consecutive jobs without a result; see batch/*/stdout.txt', flush=True); break
def report():
    rows = []
    for j in jobs:
        res = f"{DIR}/{j['id']}/result.json"
        if not os.path.exists(res): continue
        r = json.load(open(res)); rec = record[j['instance']]; tot = r.get('indep_total'); st0 = (r.get('summary') or {}).get('start_total')
        lab = 'NO_RESULT' if tot is None else ('INVALID' if not r.get('indep_feasible') else ('BEATS_RECORD' if tot < rec else ('TIES_RECORD' if tot == rec else 'ABOVE_RECORD')))
        rows.append(dict(job=j['id'], instance=j['instance'], engine=j['engine'], start=os.path.basename(j['start']), seed=j['seed'], seconds=j['seconds'], start_total=st0, best_total=tot, record=rec, below_record_by=(rec - tot) if tot else '', label=lab, file=r.get('file') or ''))
    if rows:
        with open(f'{DIR}/results.csv', 'w', newline='') as fh: w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    L = [f'# TimPassLib batch results ({JOBS})', '', f'Jobs finished: {len(rows)} of {len(jobs)}. Every total below is from the independent evaluator. record = the live record (Ramos) on the board of 2026-11-16.', '',
         '| job | instance | engine | start | seed | start total | best total | record | below record by | label |', '|---|---|---|---|---|---:|---:|---:|---:|---|']
    for r in rows: L.append(f"| {r['job']} | {r['instance']} | {r['engine']} | {r['start']} | {r['seed']} | {r['start_total']} | {r['best_total']} | {r['record']} | {r['below_record_by']} | {r['label']} |")
    best = {}
    for r in rows:
        if r['best_total'] and (r['instance'] not in best or r['best_total'] < best[r['instance']]['best_total']): best[r['instance']] = r
    L += ['', '## Best per instance', '', '| instance | best total | record | label | file |', '|---|---:|---:|---|---|'] + [f"| {k} | {v['best_total']} | {v['record']} | {v['label']} | {v['file']} |" for k, v in best.items()]
    open(f'{DIR}/RESULTS.md', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[:6]))
if '--report' not in sys.argv: run()
report()
