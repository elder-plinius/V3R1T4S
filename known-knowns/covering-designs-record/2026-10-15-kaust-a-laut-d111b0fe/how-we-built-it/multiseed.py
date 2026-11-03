"""Run covsearch3 on one (v,k,t,b) cell with several seeds in parallel, each with its own hard cap.
Records each child's Windows PID in <outdir>/pids.txt, writes one log per seed, stops at the first FOUND only if
--stop-on-found is given (then it kills its own other children by their handles).
usage: python -I multiseed.py engine v k t b secs outdir seeds(comma) pnoises(comma) [init|-] [--stop-on-found]"""
import os, subprocess, sys, time
engine, v, k, t, b, secs, outdir, seeds, pns = sys.argv[1:10]
engine = os.path.abspath(engine)
init = sys.argv[10] if len(sys.argv) > 10 and not sys.argv[10].startswith('--') else '-'
stop = '--stop-on-found' in sys.argv
os.makedirs(outdir, exist_ok=True)
seeds = seeds.split(','); pns = pns.split(',')
pidf = open(os.path.join(outdir, 'pids.txt'), 'a', encoding='utf-8', newline='\n')
procs = []
for i, s in enumerate(seeds):
    pn = pns[i % len(pns)]
    tag = 'C%s_%s_%s_b%s_s%s_pn%s' % (v, k, t, b, s, pn)
    log = open(os.path.join(outdir, tag + '.log'), 'w', encoding='utf-8', newline='\n')
    outp = os.path.join(outdir, tag + '.found.txt')
    p = subprocess.Popen([engine, v, k, t, b, secs, s, outp, init, '10', '1000000', pn, '0'], stdout=log,
                         stderr=subprocess.STDOUT)
    pidf.write('%d %s started %s\n' % (p.pid, tag, time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))); pidf.flush()
    procs.append((p, tag, log, time.time()))
cap = float(secs) + 120
while procs:
    time.sleep(2)
    left = []
    for p, tag, log, t0 in procs:
        rc = p.poll()
        if rc is None and time.time() - t0 > cap:
            p.kill(); rc = p.wait()
        if rc is None:
            left.append((p, tag, log, t0)); continue
        log.close()
        txt = open(os.path.join(outdir, tag + '.log'), encoding='utf-8').read()
        found = 'FOUND covering' in txt
        last = [l for l in txt.splitlines() if 'best=' in l]
        print('%s rc=%s %s %s' % (tag, rc, 'FOUND' if found else 'no', last[-1] if last else ''), flush=True)
        if found and stop:
            for q, tg, lg, _ in procs:
                if q.poll() is None:
                    q.kill(); q.wait()
            left = []
            break
    procs = left
print('done', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), flush=True)
