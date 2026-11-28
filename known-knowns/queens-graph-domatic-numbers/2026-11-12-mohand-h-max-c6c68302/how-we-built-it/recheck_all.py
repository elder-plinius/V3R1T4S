"""Run drat-trim again on EVERY saved (formula, proof) pair of the chain of one encoding, J checks at a time, and
record for each one the verdict and what drat-trim says about it (lemmas in the core, RAT lemmas, time).
It takes the pairs from the folders themselves (L1, L2, every piece-NN, glue of every class), not from the recorded
results, and it never skips a pair: a missing proof file is a failure.
Output: one line per check in the results file, then totals. Last printed line:
    RECHECK <enc>: <n> of <n> checks VERIFIED          (or ... NOT ALL VERIFIED)
Another checker can be given in place of drat-trim, provided it is called as "checker formula proof" and prints a line
starting with "s "; extra arguments for it are read from the environment variable RECHECK_ARGS.
Usage: python recheck_all.py chain_root enc K drat-trim-bin results.txt J [first_class last_class]"""
import os, re, subprocess, sys, threading, time

EXTRA = os.environ.get('RECHECK_ARGS', '').split()

root, enc, K, dt, out, J = sys.argv[1], sys.argv[2], int(sys.argv[3]), os.path.abspath(sys.argv[4]), sys.argv[5], int(sys.argv[6])
first, last = (int(sys.argv[7]), int(sys.argv[8])) if len(sys.argv) > 8 else (0, K - 1)
jobs = []
for c in range(first, last + 1):
    d12 = os.path.join(root, '%s-c%02d-l12' % (enc, c)); d4 = os.path.join(root, '%s-c%02d-a4' % (enc, c))
    jobs += [(c, name, os.path.join(d12, name + '.cnf'), os.path.join(d12, name + '.bin')) for name in ('L1', 'L2')]
    i = 0
    while os.path.exists(os.path.join(d4, 'piece-%02d.cnf' % i)):
        jobs.append((c, 'piece-%02d' % i, os.path.join(d4, 'piece-%02d.cnf' % i), os.path.join(d4, 'piece-%02d.bin' % i))); i += 1
    jobs.append((c, 'glue', os.path.join(d4, 'glue.cnf'), os.path.join(d4, 'glue.bin')))
results = {}
lock = threading.Lock()
todo = list(range(len(jobs)))
t0 = time.time()


def work():
    while True:
        with lock:
            if not todo:
                return
            k = todo.pop(0)
        c, name, cnf, prf = jobs[k]
        if not (os.path.exists(cnf) and os.path.exists(prf)):
            res = ('MISSING FILE', 0, 0, -1, 0.0, 0)
        else:
            t = time.time()
            r = subprocess.run([dt, cnf, prf] + EXTRA, capture_output=True, text=True, creationflags=getattr(subprocess, 'BELOW_NORMAL_PRIORITY_CLASS', 0))
            o = r.stdout.replace('\r', '\n')
            st = [l.strip() for l in o.split('\n') if l.strip().startswith('s ')]
            m = re.search(r'c (\d+) of (\d+) lemmas in core', o); rat = re.search(r'c (\d+) RAT lemmas in core', o)
            res = (st[-1] if st else 'no status line (exit %d)' % r.returncode, int(m.group(1)) if m else 0, int(m.group(2)) if m else 0,
                   int(rat.group(1)) if rat else -1, time.time() - t, os.path.getsize(prf))
        with lock:
            results[k] = res
            done = len(results)
            if done % 34 == 0 or done == len(jobs):
                print('%d of %d checks done, %.0fs' % (done, len(jobs), time.time() - t0), flush=True)


threads = [threading.Thread(target=work) for _ in range(J)]
for th in threads:
    th.start()
for th in threads:
    th.join()
ok = 0; rat_total = 0; cpu = 0.0; big = 0
with open(out, 'w', newline='\n') as f:
    for k, (c, name, cnf, prf) in enumerate(jobs):
        v, a, b, rat, sec, size = results[k]
        f.write('%s c%02d %-8s %-12s core_lemmas=%d of %d rat_in_core=%d proof_bytes=%d check_s=%.1f\n' % (enc, c, name, v.replace(' ', '_'), a, b, rat, size, sec))
        ok += v == 's VERIFIED'; rat_total += max(rat, 0); cpu += sec; big = max(big, size)
    f.write('total: %d checks, %d VERIFIED, RAT lemmas in cores %d, largest proof %d bytes, sum of check times %.0fs, wall time %.0fs with %d at a time\n' % (
        len(jobs), ok, rat_total, big, cpu, time.time() - t0, J))
print('sum of check times %.0fs, wall time %.0fs, largest proof %d bytes, RAT lemmas in cores: %d' % (cpu, time.time() - t0, big, rat_total))
print('RECHECK %s: %d of %d checks VERIFIED%s' % (enc, ok, len(jobs), '' if ok == len(jobs) and len(jobs) == (last - first + 1) * 34 else ' -- NOT ALL VERIFIED OR UNEXPECTED NUMBER OF CHECKS'))
sys.exit(0 if ok == len(jobs) else 1)
