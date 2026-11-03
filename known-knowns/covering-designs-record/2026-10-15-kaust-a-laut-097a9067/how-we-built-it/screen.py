"""Warm-start screening of (v,k,t) cells at b = live - 1.
For each candidate cell: extract the Zenodo v1.2 design, confirm its size equals the live value and that it covers
(redund.exe), delete the block with the fewest uniquely covered t-subsets, and run covsearch3 at b-1 from there.
Resumable: cells already in the results file are skipped. Child PIDs are appended to <out>.pids.

usage: python -I screen.py cands.csv covers.json index.tsv engine redund out.csv celldir secs workers pnoise deadline_unix [warm|cold]
cold: the search starts from random blocks (the published design is still extracted and verified).
cands.csv columns: v,k,t,live (extra columns ignored)."""
import csv, os, subprocess, sys, time, re

cands_p, covers, index, engine, redund, out, celldir, secs, workers, pn, deadline = sys.argv[1:12]
mode = sys.argv[12] if len(sys.argv) > 12 else 'warm'
secs = float(secs); workers = int(workers); deadline = float(deadline)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import covers_index  # noqa: E402

idx = {}
for line in open(index, encoding='utf-8'):
    n, off, ln, nb = line.rstrip('\n').split('\t')
    idx[n] = (int(off), int(ln), int(nb))
done = set()
if os.path.exists(out):
    for r in csv.DictReader(open(out, encoding='utf-8')):
        done.add((int(r['v']), int(r['k']), int(r['t'])))
cands = []
for r in csv.DictReader(open(cands_p, encoding='utf-8')):
    key = (int(r['v']), int(r['k']), int(r['t']))
    if key not in done:
        cands.append((key, int(r['live'])))
fields = ['v', 'k', 't', 'live', 'zen_blocks', 'published_uncovered', 'b_try', 'start_uncovered', 'best_uncovered',
          'found', 'secs', 'finished_utc']
new = not os.path.exists(out)
fo = open(out, 'a', encoding='utf-8', newline='')
w = csv.DictWriter(fo, fieldnames=fields, lineterminator='\n')
if new:
    w.writeheader(); fo.flush()
pidf = open(out + '.pids', 'a', encoding='utf-8', newline='\n')


def prepare(key, live):
    v, k, t = key
    d = os.path.join(celldir, 'C%d_%d_%d' % key)
    os.makedirs(d, exist_ok=True)
    name = 'C(%d,%d,%d)' % key
    if name not in idx:
        return None, {'zen_blocks': 0}
    off, ln, nb = idx[name]
    with open(covers, 'rb') as f:
        f.seek(off); raw = f.read(ln).decode()
    blocks = re.findall(r'\[([\d,\s]+)\]', raw)
    design = os.path.join(d, 'zenodo_design.txt')
    with open(design, 'w', encoding='utf-8', newline='\n') as g:
        for b in blocks:
            g.write(' '.join(x.strip() for x in b.split(',')) + '\n')
    warm = os.path.join(d, 'warm_b%d.txt' % (len(blocks) - 1))
    res = subprocess.run([redund, str(v), str(k), str(t), design, warm], capture_output=True, text=True)
    m = re.search(r'blocks=(\d+) uncovered=(\d+) min_unique=(-?\d+)', res.stdout)
    info = {'zen_blocks': len(blocks)}
    if not m:
        return None, info
    info['published_uncovered'] = int(m.group(2)); info['start_uncovered'] = int(m.group(3))
    open(os.path.join(d, 'redund.txt'), 'w', encoding='utf-8', newline='\n').write(res.stdout)
    if len(blocks) != live or int(m.group(2)) != 0:
        return None, info
    return (d, warm), info


running = []
qi = 0
while (qi < len(cands) or running) and time.time() < deadline:
    while len(running) < workers and qi < len(cands) and time.time() < deadline:
        key, live = cands[qi]; qi += 1
        prep, info = prepare(key, live)
        row = dict(v=key[0], k=key[1], t=key[2], live=live, **info)
        if prep is None:
            row.update(found='skip', finished_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
            w.writerow(row); fo.flush(); continue
        d, warm = prep
        b_try = live - 1
        outp = os.path.join(d, 'found_b%d.txt' % b_try)
        logp = open(os.path.join(d, 'search_b%d.log' % b_try), 'w', encoding='utf-8', newline='\n')
        p = subprocess.Popen([engine, str(key[0]), str(key[1]), str(key[2]), str(b_try), str(secs), '1', outp,
                              warm if mode == 'warm' else '-',
                              '10', '1000000', pn, '0'], stdout=logp, stderr=subprocess.STDOUT)
        pidf.write('%d C(%d,%d,%d) b=%d started %s\n' % (p.pid, key[0], key[1], key[2], b_try,
                                                          time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))
        pidf.flush()
        row['b_try'] = b_try
        running.append((p, row, logp, time.time(), d))
    time.sleep(0.5)
    still = []
    for p, row, logp, t0, d in running:
        rc = p.poll()
        if rc is None and time.time() - t0 > secs + 60:
            p.kill(); rc = p.wait()   # our own child, by its handle
        if rc is None:
            still.append((p, row, logp, t0, d)); continue
        logp.close()
        log = open(os.path.join(d, 'search_b%d.log' % row['b_try']), encoding='utf-8').read()
        m = re.findall(r'best=(\d+)', log)
        row['best_uncovered'] = int(m[-1]) if m else ''
        row['found'] = 'FOUND' if 'FOUND covering' in log else 'no'
        row['secs'] = round(time.time() - t0, 1)
        row['finished_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        w.writerow(row); fo.flush()
        print('C(%d,%d,%d) live=%d try=%d start=%s best=%s %s' % (row['v'], row['k'], row['t'], row['live'], row['b_try'],
              row.get('start_uncovered'), row['best_uncovered'], row['found']), flush=True)
    running = still
print('screen finished or deadline reached; remaining cells', len(cands) - qi)
