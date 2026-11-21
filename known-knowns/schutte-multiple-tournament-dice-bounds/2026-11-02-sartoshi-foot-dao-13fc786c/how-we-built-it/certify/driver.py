"""Certification driver (D-023). Usage (from the workspace root):
    nohup nice -n 19 venv-schutte/bin/python -I certify/driver.py run  > logs/certify-work/driver.out 2>&1 &
Per job: solve.py (CNF + binary DRAT) -> drat-trim (DRAT -> LRAT) -> cake_lpr (verified LRAT check) -> one ledger row -> delete
the proof, the LRAT file and the CNF. Resumable: jobs with a final row in certify/ledger.tsv are skipped.
Stop: touch certify/STOP (running jobs finish, nothing new starts, the driver exits). PID: certify/driver.pid.
Limits: nice 19, at most SLOTS jobs, RSS cap per process (polled every 2 s, the child is killed by its recorded PID),
wall-clock caps per stage. Retry rule: a TIMEOUT/MEMOUT/CONVERT_FAIL/ERROR on attempt 1 is retried once with doubled caps
(12 GB, at most one such retry at a time); a second failure is final FAILED. SAT and CHECK_FAIL are final at once."""
import sys, os, time, json, hashlib, subprocess, threading, datetime, shutil, signal

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERT = os.path.join(WS, 'certify'); WORK = os.path.join(WS, 'logs', 'certify-work'); JOBS = os.path.join(WORK, 'jobs')
TOOLS = os.path.join(WS, 'logs', 'certify-tools')
PY = os.path.join(WS, 'venv-schutte', 'bin', 'python')
DRAT_TRIM = os.path.join(TOOLS, 'drat-trim', 'drat-trim'); CAKE = os.path.join(TOOLS, 'cake_lpr', 'cake_lpr')
LEDGER = os.path.join(CERT, 'ledger.tsv'); STOP = os.path.join(CERT, 'STOP'); PIDF = os.path.join(CERT, 'driver.pid')
STATUS = os.path.join(CERT, 'status.txt'); PIDLOG = os.path.join(WORK, 'pids.log')
SLOTS = 3; GB = 1024 ** 3; MIN_FREE = 15 * GB
COLS = ['utc_end', 'job', 'attempt', 'verdict', 'cnf_sha256', 'vars', 'clauses', 'proof_sha256', 'proof_bytes', 'lrat_bytes',
        'solve_s', 'convert_s', 'check_s', 'peak_rss_mb', 'note']
FINAL = {'VERIFIED', 'SAT', 'CHECK_FAIL', 'FAILED'}
lock = threading.Lock()

def utc(): return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def rss_kb(pid):
    r = subprocess.run(['ps', '-o', 'rss=', '-p', str(pid)], capture_output=True, text=True).stdout.split()
    return int(r[0]) if r else 0

def run_stage(cmd, wd, cap_s, cap_bytes, tag, peak):
    """Runs one niced child; returns (exit code or 'TIMEOUT'/'MEMOUT', seconds, stdout text)."""
    out = open(os.path.join(wd, tag + '.out'), 'w'); err = open(os.path.join(wd, tag + '.err'), 'w')
    t0 = time.time(); p = subprocess.Popen(['nice', '-n', '19'] + cmd, stdout=out, stderr=err, cwd=wd)
    with lock: open(PIDLOG, 'a').write(f'{utc()} pid {p.pid} {tag} {os.path.basename(wd)}\n')
    why = None
    while p.poll() is None:
        time.sleep(min(2.0, 0.1 + (time.time() - t0) / 10))  # fine polling for short stages, every 2 s for long ones
        r = rss_kb(p.pid) * 1024; peak[0] = max(peak[0], r)
        if r > cap_bytes: why = 'MEMOUT'
        elif time.time() - t0 > cap_s: why = 'TIMEOUT'
        if why:
            try: os.kill(p.pid, signal.SIGKILL)  # only this recorded child PID
            except ProcessLookupError: pass
            p.wait(); break
    out.close(); err.close()
    txt = open(os.path.join(wd, tag + '.out')).read()
    return (why or p.returncode), round(time.time() - t0, 1), txt

def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()

def dir_bytes(d):
    t = 0
    for root, _, fs in os.walk(d):
        for f in fs:
            try: t += os.path.getsize(os.path.join(root, f))
            except OSError: pass
    return t

def run_job(job, wd, attempt, solve_cap, mem, keep=False, disk_peak=None):
    """Full pipeline for one job; returns a ledger row dict. keep=True leaves the files (validation only)."""
    os.makedirs(wd, exist_ok=True)
    row = dict(job=job, attempt=attempt, verdict='ERROR', cnf_sha256='-', vars='-', clauses='-', proof_sha256='-', proof_bytes=0,
               lrat_bytes=0, solve_s='-', convert_s='-', check_s='-', peak_rss_mb=0, note='')
    peak = [0]; mult = 1 if attempt == 1 else 2
    def finish(v, note=''):
        row['verdict'] = v; row['note'] = note; row['peak_rss_mb'] = round(peak[0] / 2 ** 20)
        if disk_peak is not None: disk_peak[0] = max(disk_peak[0], dir_bytes(wd))
        if not keep: shutil.rmtree(wd, ignore_errors=True)
        return row
    rc, ts, txt = run_stage([PY, '-I', os.path.join(CERT, 'solve.py'), job, wd], wd, solve_cap * mult, mem, 'solve', peak)
    row['solve_s'] = ts
    if rc in ('TIMEOUT', 'MEMOUT'): return finish(rc, 'solve')
    try: info = json.loads(txt.strip().splitlines()[-1])
    except Exception: return finish('ERROR', f'solve rc={rc}')
    row.update(cnf_sha256=info['cnf_sha256'], vars=info['vars'], clauses=info['clauses'], solve_s=info['solve_s'])
    if info['result'] == 'SAT': return finish('SAT', 'solver found a model')
    cnf, drat, lrat = (os.path.join(wd, x) for x in ('f.cnf', 'proof.drat', 'proof.lrat'))
    row['proof_bytes'] = os.path.getsize(drat); row['proof_sha256'] = sha_file(drat)
    if disk_peak is not None: disk_peak[0] = max(disk_peak[0], dir_bytes(wd))
    cap_c = max(900, 6 * info['solve_s']) * mult
    rc, tc, txt = run_stage([DRAT_TRIM, cnf, drat, '-i', '-w', '-L', lrat, '-t', str(int(cap_c))], wd, cap_c + 60, mem, 'convert', peak)
    row['convert_s'] = tc
    if rc in ('TIMEOUT', 'MEMOUT'): return finish(rc, 'convert')
    if not any(l.strip() == 's VERIFIED' for l in txt.splitlines()):
        return finish('TIMEOUT' if 's TIMEOUT' in txt else 'CONVERT_FAIL', 'drat-trim: ' + ' | '.join(txt.strip().splitlines()[-2:])[:150])
    row['lrat_bytes'] = os.path.getsize(lrat)
    if disk_peak is not None: disk_peak[0] = max(disk_peak[0], dir_bytes(wd))
    os.remove(drat)  # the DRAT file is no longer needed; its sha256 is in the row
    if sha_file(cnf) != info['cnf_sha256']: return finish('ERROR', 'CNF changed before the check')
    heap, stack = (4500, 1000) if attempt == 1 else (10000, 1500)
    cap_k = max(600, 3 * tc) * mult
    rc, tk, txt = run_stage([CAKE, f'--CML_HEAP_SIZE={heap}', f'--CML_STACK_SIZE={stack}', cnf, lrat], wd, cap_k, mem + GB, 'check', peak)
    row['check_s'] = tk
    errt = open(os.path.join(wd, 'check.err')).read()
    if rc in ('TIMEOUT', 'MEMOUT'): return finish(rc, 'check')
    if 'exhausted' in errt: return finish('MEMOUT', 'cake_lpr: ' + errt.strip()[:100])
    if rc == 0 and txt.splitlines() == ['s VERIFIED UNSAT']: return finish('VERIFIED')
    return finish('CHECK_FAIL', f'cake_lpr rc={rc}: ' + (txt + errt).strip().replace('\n', ' | ')[:150])

def write_row(row):
    with lock:
        new = not os.path.exists(LEDGER)
        with open(LEDGER, 'a') as f:
            if new: f.write('\t'.join(COLS) + '\n')
            row['utc_end'] = utc(); f.write('\t'.join(str(row[c]) for c in COLS) + '\n')

def read_ledger():
    rows = []
    if os.path.exists(LEDGER):
        for l in open(LEDGER).read().splitlines()[1:]:
            f = l.split('\t')
            if len(f) == len(COLS): rows.append(dict(zip(COLS, f)))
    return rows

def load_jobs():
    return [dict(zip(['job', 'tier', 'prior_s'], l.split('\t'))) for l in open(os.path.join(CERT, 'jobs.tsv')).read().splitlines()[1:]]

def state(jobs, rows):
    st = {}
    for r in rows:
        j = r['job']; s = st.setdefault(j, dict(final=None, fails=0))
        if r['verdict'] in FINAL: s['final'] = r['verdict']
        else: s['fails'] += 1
    return st

def main():
    os.makedirs(JOBS, exist_ok=True)
    open(PIDF, 'w').write(f'{os.getpid()}\n')
    for d in os.listdir(JOBS): shutil.rmtree(os.path.join(JOBS, d), ignore_errors=True)  # partial jobs of a crashed driver restart from scratch
    jobs = load_jobs(); prior = {j['job']: float(j['prior_s']) for j in jobs}; tier = {j['job']: j['tier'] for j in jobs}
    running = {}; disk_peak = [0]; t_start = time.time(); done_here = 0; work_here = 0.0; pipe_here = 0.0; last_status = 0
    def worker(job, attempt, cap, mem):
        nonlocal done_here, work_here, pipe_here
        row = run_job(job, os.path.join(JOBS, job.replace('/', '__')), attempt, cap, mem, disk_peak=disk_peak)
        if row['verdict'] not in FINAL and (attempt >= 2 or tier[job] == 'hard'): row['note'] += '; final after retry rule'; row['verdict'] = 'FAILED'
        write_row(row)
        with lock:
            done_here += 1; work_here += prior[job]
            pipe_here += sum(float(row[k]) for k in ('solve_s', 'convert_s', 'check_s') if row[k] != '-')
            running.pop(job, None)
    while True:
        st = state(jobs, read_ledger())
        todo = [j['job'] for j in jobs if (st.get(j['job'], {}).get('final') is None) and j['job'] not in running]
        stopping = os.path.exists(STOP)
        free = shutil.disk_usage(WORK).free
        if not stopping and free > MIN_FREE:
            with lock: nrun = len(running); retry_running = any(a >= 2 for a in running.values())
            for j in todo:
                if nrun >= SLOTS: break
                a = st.get(j, {}).get('fails', 0) + 1
                if a >= 2 and retry_running: continue
                cap = 7200 if tier[j] == 'hard' else max(600, 3 * prior[j] + 300)
                mem = 6 * GB if a == 1 else 12 * GB
                with lock: running[j] = a
                threading.Thread(target=worker, args=(j, a, cap, mem), daemon=True).start()
                nrun += 1; retry_running = retry_running or a >= 2
        with lock: nrun = len(running)
        if time.time() - last_status > 60 or (not todo and nrun == 0) or (stopping and nrun == 0):
            last_status = time.time(); rows = read_ledger(); st = state(jobs, rows)
            cnt = {}
            for j in jobs: v = st.get(j['job'], {}).get('final') or ('retry-pending' if st.get(j['job'], {}).get('fails') else 'pending'); cnt[v] = cnt.get(v, 0) + 1
            rem = sum(prior[j['job']] for j in jobs if not st.get(j['job'], {}).get('final'))
            el = time.time() - t_start; eta = '-'
            if work_here > 0 and el > 0: eta = f'{rem / (work_here / el) / 3600:.1f} h (from this driver run: {work_here:.0f} prior-solver-s done in {el:.0f} s wall)'
            with lock:
                txt = (f'updated {utc()}\ndriver pid {os.getpid()}\njobs {len(jobs)}: {cnt}\nrunning {sorted(running.items())}\n'
                       f'pipeline seconds (solve+convert+check) per prior solver second, this run: {pipe_here / work_here if work_here else 0:.2f}\n'
                       f'ETA {eta}\nwork-dir peak {disk_peak[0] / GB:.2f} GB; free disk {free / GB:.0f} GB\nSTOP file: {stopping}\n')
            open(STATUS, 'w').write(txt)
        if (stopping or not todo) and nrun == 0: break
        time.sleep(1)
    if not os.path.exists(STOP):
        with open(os.path.join(CERT, 'assemble.out'), 'w') as f:
            subprocess.run(['nice', '-n', '19', PY, '-I', os.path.join(CERT, 'assemble.py')], stdout=f, stderr=subprocess.STDOUT)
    open(STATUS, 'a').write(f'driver exited {utc()} ({"STOP file" if os.path.exists(STOP) else "queue empty; see assemble.out"})\n')
    os.remove(PIDF)

if __name__ == '__main__':
    assert sys.argv[1:] == ['run'], __doc__
    main()
