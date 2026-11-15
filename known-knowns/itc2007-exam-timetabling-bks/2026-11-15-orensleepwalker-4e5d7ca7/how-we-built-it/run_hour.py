"""One-hour improvement run for the ITC-2007 exam scout (exploratory, not a preregistered claim run).
5 lanes in parallel, one core each. Lanes 1-4: 60 min each on set4/set5. Lane 5: set1, set3, set7 for 20 min each.
Resumable: a job whose result line already exists in results.jsonl is skipped. Every output is re-scored by check.py.
Usage (from the scout folder): python3 -I code/run_hour.py            -> runs, then writes hour1/RESULTS.md
                                python3 -I code/run_hour.py --report   -> only rewrites hour1/RESULTS.md"""
import os, sys, json, subprocess, time, threading
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)
sys.path.insert(0, 'code'); import check
OUT = 'hour1'; RES = f'{OUT}/results.jsonl'
BANK = {'set1': 3085, 'set3': 7041, 'set4': 10448, 'set5': 2327, 'set7': 3225}
LANES = [
    [('L1', 'set5', 'set5_2312.sol', 3600, 101, 3)],
    [('L2', 'set5', 'set5_bank2327.sol', 3600, 102, 6)],
    [('L3', 'set4', 'set4_10440.sol', 3600, 103, 8)],
    [('L4', 'set4', 'set4_bank10465.sol', 3600, 104, 15)],
    [('L5a', 'set1', 'set1_bank3085.sol', 1200, 105, 10), ('L5b', 'set3', 'set3_bank7041.sol', 1200, 106, 25),
     ('L5c', 'set7', 'set7_bank3225.sol', 1200, 107, 10)],
]
lock = threading.Lock()

def done_jobs():
    if not os.path.exists(RES): return set()
    return {json.loads(l)['job'] for l in open(RES) if l.strip()}

def run_lane(lane):
    for job, inst, start, secs, seed, T0 in lane:
        if job in done_jobs(): continue
        sol = f'{OUT}/{job}_{inst}.sol'
        p = subprocess.run(['./code/sa_bin', f'data/inst/{inst}.exam', f'{OUT}/starts/{start}', str(secs), str(seed), str(T0), sol],
                           capture_output=True, text=True)
        rec = dict(job=job, instance=inst, start_file=start, seconds=secs, seed=seed, T0=T0, returncode=p.returncode)
        try: rec['solver'] = json.loads(p.stdout.strip().splitlines()[-1])
        except Exception: rec['solver_error'] = (p.stdout + p.stderr)[-500:]
        if os.path.exists(sol):
            c = check.evaluate(f'data/inst/{inst}.exam', sol)
            rec.update(check_feasible=c['feasible'], check_total=c.get('total'), bank_best=BANK[inst])
        with lock:
            with open(RES, 'a') as fh: fh.write(json.dumps(rec) + '\n')

def report():
    rows = [json.loads(l) for l in open(RES) if l.strip()] if os.path.exists(RES) else []
    L = ['# Hour-1 results (ITC-2007 exam scout)', '', 'Exploratory run, not a claim. Scores are from check.py (independent of the solver).', '',
         '| job | instance | start | seed | T0 | checker valid | checker score | bank best | difference |', '|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        tot = r.get('check_total'); bb = r.get('bank_best', BANK.get(r['instance']))
        diff = (tot - bb) if isinstance(tot, int) else 'n/a'
        L.append(f"| {r['job']} | {r['instance']} | {r['start_file']} | {r['seed']} | {r['T0']} | {r.get('check_feasible', 'NO OUTPUT')} | {tot} | {bb} | {diff} |")
    expected = sum(len(l) for l in LANES)
    L += ['', f'Jobs finished: {len(rows)} of {expected}.']
    open(f'{OUT}/RESULTS.md', 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))

if __name__ == '__main__':
    if '--report' not in sys.argv:
        open(f'{OUT}/run.pid', 'w').write(f'pid {os.getpid()} pgid {os.getpgid(0)} started {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
        if not os.path.exists('code/sa_bin'):
            subprocess.run(['g++', '-O2', '-std=c++17', '-o', 'code/sa_bin', 'code/sa.cpp'], check=True)
        ts = [threading.Thread(target=run_lane, args=(l,)) for l in LANES]
        for t in ts: t.start()
        for t in ts: t.join()
    report()
