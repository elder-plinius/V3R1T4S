"""Fixed-pattern sweep (Andy, 2026-11-25; Boss: "sweep", 2 h budget): for every open instance except Early 9 (done) and Early 14 (opponent part 0),
re-solve the record's opponents with resolve.py (180 s, 6 workers, seed 1, 6 GB address-space cap, hard wall limit), check the output with
split.evaluate (hard 0 and total = venue + opponent) and record it in out/results.jsonl. Resumable. At the end writes out/summary.txt and sends it by
Telegram (shared config.ini, only if [telegram] enabled = true; Boss asked for it). Exploration only: nothing is claimed."""
import sys, os, json, time, subprocess, configparser, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import split
B = json.load(open('data/board.json')); S = json.load(open('data/split.json'))
order = ['Early 12', 'Middle 5', 'Middle 15', 'Middle 12', 'Early 2', 'Early 13', 'Middle 8', 'Late 11', 'Middle 13', 'Early 1', 'Middle 9', 'Late 9', 'Early 4',
         'Early 3', 'Early 6', 'Middle 6', 'Middle 7', 'Late 3', 'Late 6', 'Late 8', 'Late 13']
order += sorted([k for k in S if k not in order and k not in ('Early 9', 'Early 14') and S[k]['opp'] > 0], key=lambda k: S[k]['ub'])
RES = 'out/results.jsonl'; done = {json.loads(l)['inst'] for l in open(RES)} if os.path.exists(RES) else set()
PY = sys.executable; CAP = 6 * 2 ** 30
for k in order:
    if k in done: continue
    nm = 'ITC2021_' + k.replace(' ', '_'); out = 'out/%s.sweep.xml' % nm; t0 = time.time()
    code = "import resource, sys, runpy; resource.setrlimit(resource.RLIMIT_AS, (%d, %d)); sys.argv = ['resolve.py', %r, %r, '180', '6', %r, '1']; runpy.run_path('resolve.py', run_name='__main__')" % (CAP, CAP, 'inst/%s.xml' % nm, 'sol/%s.record.xml' % nm, out)
    try:
        p = subprocess.run([PY, '-c', code], capture_output=True, text=True, timeout=900, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1')); line = (p.stdout.strip().splitlines() or ['{}'])[-1]
        res = json.loads(line) if line.startswith('{') else {'status': 'ERROR', 'err': (p.stderr or '')[-300:]}
    except subprocess.TimeoutExpired: res = {'status': 'TIMEOUT'}
    rec = dict(inst=k, ub=S[k]['ub'], venue=S[k]['venue'], record_opp=S[k]['opp'], wall=round(time.time() - t0), **res)
    if os.path.exists(out) and os.path.getmtime(out) >= t0:
        v = split.evaluate('inst/%s.xml' % nm, out); rec.update(checked_hard=v['hard'], checked_total=v['venue'] + v['opp'], win=v['hard'] == 0 and v['venue'] + v['opp'] < S[k]['ub'])
    open(RES, 'a').write(json.dumps(rec) + '\n'); print(rec, flush=True)
R = [json.loads(l) for l in open(RES)]
wins = [r for r in R if r.get('win')]
lines = ['Andy (Veritas): ITC2021 fixed-pattern sweep finished, %d instances.' % len(R),
         'Records beaten (checker-valid, unreviewed): %d %s' % (len(wins), ', '.join('%s %d->%d' % (r['inst'], r['ub'], r['checked_total']) for r in wins))]
proved = [r['inst'] for r in R if r.get('bound') is not None and r['venue'] + r['bound'] >= r['ub'] and not r.get('win')]
lines.append('Record pattern exhausted (bound reaches the record): %d' % len(proved))
lines.append('Errors/timeouts: %d' % sum(1 for r in R if r.get('status') in ('ERROR', 'TIMEOUT', 'UNKNOWN', 'MODEL_INVALID')))
txt = '\n'.join(lines); open('out/summary.txt', 'w').write(txt + '\n'); print(txt)
try:
    c = configparser.ConfigParser(interpolation=None); c.read('<shared config.ini>')
    if c.get('telegram', 'enabled').strip().lower() == 'true':
        data = urllib.parse.urlencode({'chat_id': c.get('telegram', 'chat_id').strip(), 'text': txt[:3900]}).encode()
        urllib.request.urlopen('https://api.telegram.org/bot%s/sendMessage' % c.get('telegram', 'bot_token').strip(), data=data, timeout=30)
        open('out/telegram.txt', 'w').write('sent\n')
except Exception as ex: open('out/telegram.txt', 'w').write('failed: %s\n' % type(ex).__name__)
