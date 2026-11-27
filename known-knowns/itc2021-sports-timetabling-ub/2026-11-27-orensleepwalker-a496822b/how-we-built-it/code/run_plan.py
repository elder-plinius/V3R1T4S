"""Orchestrator for plan.json (Andy, 2026-11-26). Resumable from logs/results.jsonl. Stops launching at the deadline; no run outlives it."""
import sys, os, json, time, subprocess, calendar, shutil
sys.path.insert(0, os.path.abspath('../2026-11-25-itc2021-scout')); import split
P = json.load(open('plan.json')); S = '../2026-11-25-itc2021-scout'; SP = json.load(open(S + '/data/split.json'))
DL = calendar.timegm(time.strptime(P['deadline_utc'], '%Y-%m-%dT%H:%M:%SZ')); RX = os.path.abspath('../2026-11-26-robinx-build/src/RobinX')
RES = 'logs/results.jsonl'; done = [json.loads(l) for l in open(RES)] if os.path.exists(RES) else []
key = lambda g, md, rd, k: '%s|%s|%d|%s' % (g, md, rd, k); seen = {d['key'] for d in done}
nm = lambda k: 'ITC2021_' + k.replace(' ', '_')
def robinx(inst, sol):
    import re
    o = subprocess.run([RX, '-i', inst, '-s', sol], capture_output=True, text=True, timeout=120).stdout
    m = re.findall(r'^\s*Objective:\s+(\d+)\s+(\d+)\s*$', o, re.M); return tuple(map(int, m[0])) if len(m) == 1 else None
def survivor_v2(rec):   # plan_amendment_v2.md
    return (not rec.get('win')) and 'best' in rec and (rec.get('improved', 0) > 0 or rec.get('plateau_moves', 0) >= 5)
best_file = {}   # instance -> our best timetable so far (below the record)
for d in done:
    if d.get('win'): best_file[d['inst']] = d['win_file']
def run_one(g, md, rd, k, start, secs):
    tag = '%s_%s_r%d_%s' % (g, md, rd, nm(k)); pfx = 'out/' + tag; t0 = time.time()
    if os.path.exists(pfx + '.json') and os.path.exists(pfx + '.state.xml'):
        res = json.load(open(pfx + '.json')); res.pop('mode', None); res['recovered'] = True
    else:
        res = None
    cap = P['memory_cap_gb'] * 2 ** 30; hard_left = DL - time.time()
    code = "import resource, sys, runpy; resource.setrlimit(resource.RLIMIT_AS, (%d, %d)); sys.argv = ['lns.py', %r, %r, %r, '%d', %r, '%d']; runpy.run_path('lns.py', run_name='__main__')" % (cap, cap, '%s/inst/%s.xml' % (S, nm(k)), start, md, secs, pfx, P['seed'])
    if res is None:
      try:
        p = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, timeout=max(60, min(secs + 900, hard_left)), env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        line = (p.stdout.strip().splitlines() or ['{}'])[-1]; res = json.loads(line) if line.startswith('{') else {'error': (p.stderr or '')[-300:]}
      except subprocess.TimeoutExpired: res = {'error': 'timeout'}
    res.pop('mode', None)
    rec = dict(key=key(g, md, rd, k), group=g, mode=md, round=rd, inst=k, secs_planned=secs, wall=round(time.time() - t0), start_file=start, ub=SP[k]['ub'], **res)
    if 'best' in res:
        total = res['best'] + (SP[k]['venue'] if md == 'fixed' else 0); rec['best_total'] = total
        bf = pfx + '.best.xml'
        if total < SP[k]['ub'] and os.path.exists(bf):
            v = split.evaluate('%s/inst/%s.xml' % (S, nm(k)), bf); rx = robinx('%s/inst/%s.xml' % (S, nm(k)), bf)
            rec.update(check_split=[v['hard'], v['venue'] + v['opp']], check_robinx=rx)
            if v['hard'] == 0 and v['venue'] + v['opp'] == total and rx == (0, total): rec['win'] = True; rec['win_file'] = bf; best_file[k] = bf
        rec['survivor'] = survivor_v2(rec)
        rec['state_file'] = pfx + '.state.xml'
    open(RES, 'a').write(json.dumps(rec) + '\n'); print(json.dumps(rec), flush=True); done.append(rec); return rec
for g in ('D', 'E'):
    for md in P['modes']:
        alive = list(P['groups'][g]); state = {}
        for rd, secs in enumerate(P['rounds_seconds'], 1):
            nxt = []
            for k in alive:
                kk = key(g, md, rd, k)
                prev = [d for d in done if d['key'] == kk]
                if prev: rec = prev[-1]
                else:
                    left = DL - time.time() - 60
                    if left < 120: print('deadline reached; stopping', flush=True); open('logs/stopped.txt', 'w').write(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + ' deadline\n'); sys.exit(0)
                    if rd == 1: start = best_file.get(k, '%s/sol/%s.record.xml' % (S, nm(k))) if md == 'open' else '%s/sol/%s.record.xml' % (S, nm(k))
                    else: start = state[k]
                    rec = run_one(g, md, rd, k, start, int(min(secs, left)))
                if rec.get('state_file') and os.path.exists(rec['state_file']): state[k] = rec['state_file']
                if survivor_v2(rec) and k in state: nxt.append(k)
            alive = nxt
            if not alive: break
open('logs/finished.txt', 'w').write(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + ' all steps done\n'); print('all steps done', flush=True)
