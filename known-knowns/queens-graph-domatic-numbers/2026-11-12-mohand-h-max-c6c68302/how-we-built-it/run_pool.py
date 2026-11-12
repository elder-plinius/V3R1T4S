"""Parallel driver of the chain: W workers; each takes the next unfinished (module, class) and runs stage_l12.py and
then stage_a4.py for it, with exactly the arguments, output folders and log names of the sequential loop, at low
priority. Used from 2026-11-11T23:10Z on, when the human lifted the "one computation at a time" limit; classes 0 to 3
of encoding 1 were produced by the sequential loop before that.
A class counts as finished when l12.json and state.json say so. The exit code of each Python process is recorded in
the pid file but not used: on this machine the process sometimes ends with the Windows code 0xC0000409 AFTER its last
output line (seen for classes 2 and 3 of encoding 1 under the sequential loop), with complete and consistent files.
Each class has its own folders and its own temporary folder, so the workers share nothing but the two log files
written here under a lock. The solver is deterministic, so the files do not depend on the number of workers.
Usage: python run_pool.py W n kind K M chain_root drat-trim-bin encoder_dir pidfile TASKS sets5.txt sets6.txt
       TASKS like  enc2:0-19,enc1:4-19  (taken in round-robin order over the listed modules)"""
import json, os, subprocess, sys, threading, time

W, n, kind, K, M, root, dt, encdir, pidfile, tasks_arg = sys.argv[1:11]
sets = [os.path.abspath(p) for p in sys.argv[11:]]
here = os.path.dirname(os.path.abspath(__file__))
root, dt, encdir = os.path.abspath(root), os.path.abspath(dt), os.path.abspath(encdir)
lock = threading.Lock()
stop = [False]


def utc():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def note(path, line):
    with lock:
        with open(path, 'a') as f:
            f.write(line + '\n')


def l12_ok(d12):
    try:
        l = json.load(open(os.path.join(d12, 'l12.json')))
        return len(l) == 2 and all(r['drat_trim'] == 's VERIFIED' for r in l)
    except Exception:
        return False


def a4_ok(d4):
    try:
        st = json.load(open(os.path.join(d4, 'state.json')))
        return (st.get('glue') or {}).get('drat_trim') == 's VERIFIED' and st['verified'] >= 1 and \
            st['verified'] == len(set(r['piece'] for r in st['pieces'] if r['drat_trim'] == 's VERIFIED'))
    except Exception:
        return False


def last_line(path):
    try:
        lines = [l.strip() for l in open(path, errors='replace') if l.strip() and not l.startswith('c ')]
        return lines[-1] if lines else '(no output)'
    except Exception:
        return '(no log)'


def run(script, args, tag, env, what):
    with open(os.path.join(root, tag + '.log'), 'a') as lo, open(os.path.join(root, tag + '.err'), 'a') as er:
        p = subprocess.Popen([sys.executable, '-B', os.path.join(here, script)] + args, stdout=lo, stderr=er, env=env,
                             creationflags=subprocess.BELOW_NORMAL_PRIORITY_CLASS)
        note(pidfile, '%s PID %d %s BelowNormal (pool of %s)' % (utc(), p.pid, what, W))
        code = p.wait()
        note(pidfile, '%s PID %d exit %d' % (utc(), p.pid, code))


queues = []
for part in tasks_arg.split(','):
    mod, rng = part.split(':'); a, b = rng.split('-')
    queues.append([(mod, c) for c in range(int(a), int(b) + 1)])
tasks = []
while any(queues):
    for q in queues:
        if q:
            tasks.append(q.pop(0))
tasks = [(mod, c) for mod, c in tasks
         if not (l12_ok(os.path.join(root, '%s-c%02d-l12' % (mod, c))) and a4_ok(os.path.join(root, '%s-c%02d-a4' % (mod, c))))]
print('%s pool of %s workers, %d classes to do: %s' % (utc(), W, len(tasks), ' '.join('%s:%d' % t for t in tasks)), flush=True)


def worker():
    while True:
        with lock:
            if stop[0] or not tasks:
                return
            mod, c = tasks.pop(0)
        env = dict(os.environ); env['CLS'] = str(c); env['PYTHONPATH'] = encdir
        d12 = os.path.join(root, '%s-c%02d-l12' % (mod, c)); d4 = os.path.join(root, '%s-c%02d-a4' % (mod, c))
        t12 = '%s-c%02d-l12-stage_l12' % (mod, c); t4 = '%s-c%02d-a4-stage_a4' % (mod, c)
        t = time.time()
        if not l12_ok(d12):
            run('stage_l12.py', [mod, n, kind, K, M, d12, dt] + sets, t12, env, 'stage_l12 %s class %d' % (mod, c))
        if l12_ok(d12) and not a4_ok(d4):
            run('stage_a4.py', [mod, n, kind, K, M, d4, '1000000', dt] + sets, t4, env, 'stage_a4 %s class %d' % (mod, c))
        ok = l12_ok(d12) and a4_ok(d4)
        line = '%s %s class %d | %s | %s' % (utc(), mod, c, last_line(os.path.join(root, t12 + '.log')), last_line(os.path.join(root, t4 + '.log')))
        note(os.path.join(root, 'master.log'), line)
        print(line + ' | %.0fs%s' % (time.time() - t, '' if ok else ' | NOT COMPLETE, the pool stops taking new classes'), flush=True)
        if not ok:
            stop[0] = True


threads = [threading.Thread(target=worker) for _ in range(int(W))]
for th in threads:
    th.start()
for th in threads:
    th.join()
note(os.path.join(root, 'master.log'), '%s POOL END (stop=%s)' % (utc(), stop[0]))
print('%s POOL END (stop=%s)' % (utc(), stop[0]), flush=True)
sys.exit(1 if stop[0] else 0)
